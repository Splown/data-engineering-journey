import csv
import io
import json
import math
import os
import re
import sqlite3
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from statistics import mean, pstdev
from typing import Any

import feedparser
import requests
from dateutil import parser as date_parser
from flask import Flask, redirect, render_template, request, url_for, flash

APP_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(APP_DIR, "scanner.db")

app = Flask(__name__)
app.secret_key = "nordic-trading-scanner"

DEFAULT_UNIVERSE = [
    ("VOLV-B", "Volvo AB B", "SE", "Nasdaq Stockholm", "volv-b.se"),
    ("ERIC-B", "Ericsson B", "SE", "Nasdaq Stockholm", "eric-b.se"),
    ("ALFA", "Alfa Laval", "SE", "Nasdaq Stockholm", "alfa.se"),
    ("ABB", "ABB Ltd", "SE", "Nasdaq Stockholm", "abb.se"),
    ("ORK", "Orkla", "NO", "Oslo Bors", "ork.ol"),
    ("DNB", "DNB Bank", "NO", "Oslo Bors", "dnb.ol"),
    ("EQNR", "Equinor", "NO", "Oslo Bors", "eqnr.ol"),
    ("MOWI", "Mowi", "NO", "Oslo Bors", "mowi.ol"),
]

NASDAQ_NEWS_URL = "https://www.nasdaq.com/european-market-activity/news/company-news"
OSLO_NEWS_URL = "https://live.euronext.com/en/markets/oslo/equities/company-news"
GDELT_URL = "https://api.gdeltproject.org/api/v2/doc/doc"


def db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = db()
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS instruments(
          id INTEGER PRIMARY KEY,
          ticker TEXT UNIQUE,
          name TEXT,
          country TEXT,
          exchange TEXT,
          stooq_symbol TEXT,
          last_updated TEXT
        );
        CREATE TABLE IF NOT EXISTS prices(
          instrument_id INTEGER,
          date TEXT,
          open REAL, high REAL, low REAL, close REAL, volume REAL,
          PRIMARY KEY(instrument_id, date)
        );
        CREATE TABLE IF NOT EXISTS news_items(
          id INTEGER PRIMARY KEY,
          source TEXT,
          published_at TEXT,
          title TEXT,
          url TEXT UNIQUE,
          raw_text TEXT,
          instrument_id INTEGER,
          sentiment TEXT,
          impact_score REAL
        );
        CREATE TABLE IF NOT EXISTS scan_runs(
          id INTEGER PRIMARY KEY,
          run_at TEXT,
          universe_size INTEGER,
          top20_json TEXT
        );
        CREATE TABLE IF NOT EXISTS settings(
          key TEXT PRIMARY KEY,
          value TEXT
        );
        """
    )
    conn.commit()
    conn.close()


def seed_universe() -> None:
    conn = db()
    now = datetime.now(timezone.utc).isoformat()
    for row in DEFAULT_UNIVERSE:
        conn.execute(
            """INSERT OR IGNORE INTO instruments(ticker,name,country,exchange,stooq_symbol,last_updated)
               VALUES (?,?,?,?,?,?)""",
            (*row, now),
        )
    defaults = {"weight_tech": "55", "weight_news": "35", "weight_risk": "-10", "horizon_days": "5"}
    for k, v in defaults.items():
        conn.execute("INSERT OR IGNORE INTO settings(key,value) VALUES(?,?)", (k, v))
    conn.commit()
    conn.close()


def get_settings() -> dict[str, float]:
    conn = db()
    rows = conn.execute("SELECT key,value FROM settings").fetchall()
    conn.close()
    d = {r["key"]: float(r["value"]) for r in rows}
    return d


def fetch_stooq_csv(symbol: str) -> list[dict[str, Any]]:
    url = f"https://stooq.com/q/d/l/?s={symbol}&i=d"
    resp = requests.get(url, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
    resp.raise_for_status()
    reader = csv.DictReader(io.StringIO(resp.text))
    out = []
    for r in reader:
        if not r.get("Close") or r["Close"] in ("0", ""):
            continue
        out.append(
            {
                "date": r["Date"],
                "open": float(r["Open"]),
                "high": float(r["High"]),
                "low": float(r["Low"]),
                "close": float(r["Close"]),
                "volume": float(r["Volume"] or 0),
            }
        )
    return out


def refresh_prices() -> None:
    conn = db()
    instruments = conn.execute("SELECT id,stooq_symbol FROM instruments").fetchall()
    for ins in instruments:
        try:
            rows = fetch_stooq_csv(ins["stooq_symbol"])
            for p in rows[-260:]:
                conn.execute(
                    """INSERT OR REPLACE INTO prices(instrument_id,date,open,high,low,close,volume)
                       VALUES(?,?,?,?,?,?,?)""",
                    (ins["id"], p["date"], p["open"], p["high"], p["low"], p["close"], p["volume"]),
                )
        except Exception:
            pass
    conn.commit()
    conn.close()


def scrape_simple_links(url: str) -> list[tuple[str, str]]:
    html = requests.get(url, timeout=30, headers={"User-Agent": "Mozilla/5.0"}).text
    pairs = re.findall(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', html, flags=re.I | re.S)
    cleaned = []
    for href, text in pairs:
        title = re.sub(r"<[^>]+>", " ", text)
        title = re.sub(r"\s+", " ", title).strip()
        if len(title) < 20:
            continue
        if "news" not in href.lower() and "message" not in href.lower():
            continue
        if href.startswith("/"):
            base = re.match(r"https?://[^/]+", url).group(0)
            href = f"{base}{href}"
        cleaned.append((title[:260], href))
    # dedupe preserve order
    seen, out = set(), []
    for item in cleaned:
        if item[1] in seen:
            continue
        seen.add(item[1])
        out.append(item)
    return out[:120]


def classify_sentiment(text: str) -> tuple[str, float, str]:
    t = text.lower()
    pos = sum(k in t for k in ["record", "growth", "beats", "contract", "profit", "upgrade"])
    neg = sum(k in t for k in ["loss", "downgrade", "warning", "decline", "lawsuit", "delay", "emission"])
    if pos > neg:
        return "positive", min(0.95, 0.5 + 0.1 * (pos - neg)), "Fler positiva än negativa signalord i rubriker senaste perioden."
    if neg > pos:
        return "negative", min(0.95, 0.5 + 0.1 * (neg - pos)), "Fler negativa riskord i rubriker senaste perioden."
    return "neutral", 0.5, "Blandad eller svag tonalitet i tillgängliga källor."


def refresh_exchange_news() -> None:
    conn = db()
    instruments = conn.execute("SELECT id,ticker,name FROM instruments").fetchall()
    refs = {f"{i['ticker']} {i['name']}".lower(): i["id"] for i in instruments}
    for source, url in [("nasdaq", NASDAQ_NEWS_URL), ("oslo", OSLO_NEWS_URL)]:
        try:
            items = scrape_simple_links(url)
            now = datetime.now(timezone.utc).isoformat()
            for title, link in items:
                iid = None
                low = title.lower()
                for i in instruments:
                    if i["ticker"].lower() in low or i["name"].split()[0].lower() in low:
                        iid = i["id"]
                        break
                sentiment, impact, _ = classify_sentiment(title)
                conn.execute(
                    """INSERT OR IGNORE INTO news_items(source,published_at,title,url,raw_text,instrument_id,sentiment,impact_score)
                       VALUES(?,?,?,?,?,?,?,?)""",
                    (source, now, title, link, title, iid, sentiment, impact * 100),
                )
        except Exception:
            continue
    conn.commit()
    conn.close()


def refresh_gdelt(hours: int = 72) -> None:
    conn = db()
    instruments = conn.execute("SELECT id,ticker,name FROM instruments").fetchall()
    for i in instruments:
        query = f'("{i["name"]}" OR "{i["ticker"]}") sourcecountry:(SE OR NO)'
        params = {"query": query, "mode": "ArtList", "format": "json", "maxrecords": 15, "sort": "DateDesc"}
        try:
            data = requests.get(GDELT_URL, params=params, timeout=30).json()
            for art in data.get("articles", [])[:8]:
                text = f"{art.get('title','')} {art.get('seendate','')}"
                sent, conf, _ = classify_sentiment(text)
                conn.execute(
                    """INSERT OR IGNORE INTO news_items(source,published_at,title,url,raw_text,instrument_id,sentiment,impact_score)
                    VALUES(?,?,?,?,?,?,?,?)""",
                    (
                        "gdelt",
                        art.get("seendate", datetime.now(timezone.utc).isoformat()),
                        art.get("title", "No title")[:260],
                        art.get("url", ""),
                        f"publisher={art.get('sourceCommonName','unknown')}",
                        i["id"],
                        sent,
                        conf * 100,
                    ),
                )
        except Exception:
            continue
    conn.commit()
    conn.close()


def ema(values: list[float], period: int) -> list[float]:
    if not values:
        return []
    k = 2 / (period + 1)
    e = [values[0]]
    for v in values[1:]:
        e.append(v * k + e[-1] * (1 - k))
    return e


def rsi(closes: list[float], period: int = 14) -> float:
    if len(closes) < period + 1:
        return 50.0
    gains, losses = [], []
    for i in range(1, len(closes)):
        d = closes[i] - closes[i - 1]
        gains.append(max(0, d))
        losses.append(max(0, -d))
    avg_gain = mean(gains[-period:])
    avg_loss = mean(losses[-period:])
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def compute_scores(instrument_id: int) -> dict[str, float | str]:
    conn = db()
    prices = conn.execute("SELECT * FROM prices WHERE instrument_id=? ORDER BY date", (instrument_id,)).fetchall()
    news = conn.execute("SELECT * FROM news_items WHERE instrument_id=? ORDER BY published_at DESC LIMIT 30", (instrument_id,)).fetchall()
    conn.close()
    if len(prices) < 60:
        return {"tech": 0, "news": 0, "risk": 50, "close": None, "range": "N/A", "reason": ["Otillräcklig prisdata", "Begränsad nyhetstäckning", "Datarisk"]}
    closes = [p["close"] for p in prices]
    highs = [p["high"] for p in prices]
    lows = [p["low"] for p in prices]
    vols = [p["volume"] for p in prices]
    ma20, ma50 = mean(closes[-20:]), mean(closes[-50:])
    ma200 = mean(closes[-200:]) if len(closes) >= 200 else mean(closes)
    last = closes[-1]
    trend = 40 if last > ma20 > ma50 else 20 if last > ma20 else 5
    mom = max(0, 30 - abs(50 - rsi(closes)))
    macd_line = ema(closes, 12)[-1] - ema(closes, 26)[-1]
    signal = ema([a - b for a, b in zip(ema(closes, 12), ema(closes, 26))], 9)[-1]
    mom += 15 if macd_line > signal else 5
    vol_spike = 15 if vols[-1] > 1.6 * mean(vols[-20:]) else 5
    breakout = 15 if last >= max(highs[-20:]) * 0.98 else 5
    tech = min(100, trend + mom + vol_spike + breakout)

    sent_map = {"positive": 1.0, "neutral": 0.5, "negative": 0.0}
    if news:
        avg_sent = mean(sent_map.get(n["sentiment"], 0.5) for n in news)
        intensity = min(1.0, len(news) / 10)
        avg_imp = mean((n["impact_score"] or 50) / 100 for n in news)
        news_score = (0.5 * avg_sent + 0.3 * intensity + 0.2 * avg_imp) * 100
    else:
        news_score = 20

    daily_changes = [abs(closes[i] / closes[i - 1] - 1) for i in range(1, len(closes))]
    risk = min(100, (pstdev(daily_changes[-20:]) * 1000) + (20 if any(c > 0.08 for c in daily_changes[-20:]) else 0))
    week_vol = pstdev(daily_changes[-20:]) * math.sqrt(5)
    lower, upper = week_vol * 100, week_vol * 120

    reason = [
        f"Tekniskt: MA20={ma20:.2f}, MA50={ma50:.2f}, RSI14={rsi(closes):.1f}.",
        f"Nyheter: {len(news)} träffar (Nasdaq/Oslo/GDELT), sentiment-baserad impact.",
        f"Risk: 20d-volatilitet {pstdev(daily_changes[-20:])*100:.2f}% och gap-flaggor beaktade.",
    ]
    return {
        "tech": round(tech, 2),
        "news": round(news_score, 2),
        "risk": round(risk, 2),
        "close": last,
        "last_date": prices[-1]["date"],
        "range": f"-{lower:.1f}% till +{upper:.1f}%",
        "reason": reason,
    }


def run_scan() -> None:
    settings = get_settings()
    conn = db()
    inst = conn.execute("SELECT * FROM instruments").fetchall()
    rows = []
    for i in inst:
        s = compute_scores(i["id"])
        total = (settings.get("weight_tech", 55) * s["tech"] + settings.get("weight_news", 35) * s["news"] + settings.get("weight_risk", -10) * s["risk"]) / 100
        strength = "Strong" if total >= 60 else "Medium" if total >= 45 else "Weak"
        rows.append({
            "id": i["id"], "ticker": i["ticker"], "name": i["name"], "country": i["country"],
            "total": round(total, 2), "tech": s["tech"], "news": s["news"], "risk": s["risk"],
            "close": s.get("close"), "last_date": s.get("last_date"), "range": s["range"], "strength": strength,
            "reason": s["reason"],
        })
    top20 = sorted(rows, key=lambda x: x["total"], reverse=True)[:20]
    conn.execute("INSERT INTO scan_runs(run_at,universe_size,top20_json) VALUES(?,?,?)", (datetime.now(timezone.utc).isoformat(), len(inst), json.dumps(top20)))
    conn.commit()
    conn.close()


@app.route("/")
def dashboard():
    conn = db()
    run = conn.execute("SELECT * FROM scan_runs ORDER BY run_at DESC LIMIT 1").fetchone()
    universe = conn.execute("SELECT country,COUNT(*) c, MAX(last_updated) u FROM instruments GROUP BY country").fetchall()
    conn.close()
    top = json.loads(run["top20_json"]) if run else []
    country = request.args.get("country", "ALL")
    if country in ("SE", "NO"):
        top = [r for r in top if r["country"] == country]
    return render_template("dashboard.html", top=top, universe=universe)


@app.route("/detail/<int:instrument_id>")
def detail(instrument_id: int):
    conn = db()
    i = conn.execute("SELECT * FROM instruments WHERE id=?", (instrument_id,)).fetchone()
    prices = conn.execute("SELECT * FROM prices WHERE instrument_id=? ORDER BY date DESC LIMIT 120", (instrument_id,)).fetchall()
    news = conn.execute("SELECT * FROM news_items WHERE instrument_id=? ORDER BY published_at DESC LIMIT 30", (instrument_id,)).fetchall()
    conn.close()
    s = compute_scores(instrument_id)
    return render_template("detail.html", i=i, prices=list(reversed(prices)), news=news, scores=s)


@app.route("/settings", methods=["GET", "POST"])
def settings():
    conn = db()
    if request.method == "POST":
        for k in ["weight_tech", "weight_news", "weight_risk", "horizon_days"]:
            conn.execute("INSERT OR REPLACE INTO settings(key,value) VALUES(?,?)", (k, request.form.get(k, "0")))
        conn.commit()
        flash("Inställningar sparade")
    rows = conn.execute("SELECT key,value FROM settings").fetchall()
    conn.close()
    return render_template("settings.html", settings={r["key"]: r["value"] for r in rows})


@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        action = request.form.get("action")
        if action == "refresh_prices":
            refresh_prices()
        elif action == "refresh_news":
            refresh_exchange_news(); refresh_gdelt()
        elif action == "scan":
            run_scan()
        flash("Körning klar")
        return redirect(url_for("admin"))
    conn = db()
    suggestions = conn.execute("""SELECT title,source,url FROM news_items WHERE instrument_id IS NULL ORDER BY published_at DESC LIMIT 50""").fetchall()
    logs = conn.execute("SELECT run_at,universe_size FROM scan_runs ORDER BY run_at DESC LIMIT 20").fetchall()
    conn.close()
    return render_template("admin.html", suggestions=suggestions, logs=logs)


@app.route("/admin/import", methods=["POST"])
def import_universe():
    txt = request.form.get("csv_data", "")
    reader = csv.DictReader(io.StringIO(txt))
    conn = db()
    now = datetime.now(timezone.utc).isoformat()
    for r in reader:
        conn.execute(
            "INSERT OR REPLACE INTO instruments(ticker,name,country,exchange,stooq_symbol,last_updated) VALUES(?,?,?,?,?,?)",
            (r["ticker"], r["name"], r["country"], r.get("exchange", ""), r["stooq_symbol"], now),
        )
    conn.commit()
    conn.close()
    flash("Universe importerad")
    return redirect(url_for("admin"))


if __name__ == "__main__":
    init_db()
    seed_universe()
    app.run(host="0.0.0.0", port=8000, debug=True)
