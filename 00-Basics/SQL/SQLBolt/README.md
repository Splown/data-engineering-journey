#  data-engineering-journey

# SQLBolt Solutions  ✅

This directory contains my solutions to **all 18 interactive lessons on [SQLBolt](https://sqlbolt.com/)**.  
Each file is numbered to match the lesson and holds the full set of executable queries.

---

## 📂 Folder structure

00-basics/
└── SQL/
├── lesson01.sql
├── lesson02.sql
├── ...
├── lesson17.sql
└── lesson18.sql


*Every file can be run stand-alone in any PostgreSQL-compatible environment.*

---

## 📚 Concepts covered

| Lesson | Core concepts                               | Extra notes                    |
|--------|---------------------------------------------|--------------------------------|
| 01–03  | `SELECT`, `WHERE`, `AND / OR`, `LIMIT`      | Basic filtering & ordering     |
| 04–06  | `INSERT`, `UPDATE`, `DELETE`, `BETWEEN`     | Data manipulation              |
| 07–09  | `JOIN` (INNER, LEFT, RIGHT)                 | Multi-table queries            |
| 10–12  | Aggregate functions, `GROUP BY`, `HAVING`   | Calculations & filtering sets  |
| 13–14  | `NULL`, `CASE`, sub-queries                 | Conditional logic              |
| 15–16  | `CREATE TABLE`, `PRIMARY KEY`, `FOREIGN KEY`| Schema design fundamentals     |
| 17–18  | `ALTER TABLE`, inserting bulk data          | Evolution of schemas           |

---

## 💡 Key takeaways

* *Anti-JOIN pattern:* `LEFT JOIN … WHERE t2.id IS NULL` – common interview favourite.  
* *`CASE WHEN`* keeps business logic inside SQL; avoid repetitive post-processing in Python.  
* Always assign **aliases** (`AS`) for readability, especially in nested SELECTs.  
* *Schema evolution* is safer with `ALTER TABLE … ADD COLUMN` + default values to prevent `NULL` floods.
