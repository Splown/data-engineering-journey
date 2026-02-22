# Nordic Trading Scanner

Webbapp för att skanna svenska + norska aktier med real data från Stooq, Nasdaq Europe/Nordic company news-sida, Oslo company news-sida och GDELT.

## Start

```bash
pip install -r requirements.txt
python app.py
```

Öppna `http://localhost:8000`.

## Flöde

1. Gå till **Admin** och kör `Refresh prices now`, `Refresh news now`, sedan `Run scan now`.
2. Dashboard visar Top 20 kandidater (inte köp/sälj-råd).
3. Universe kan importeras via CSV i Admin.
