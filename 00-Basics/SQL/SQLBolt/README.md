#  data-engineering-journey

# SQLBolt Solutions  ✅

This directory contains my solutions to **all 18 interactive lessons on [SQLBolt](https://sqlbolt.com/)**.  
Each file is numbered to match the lesson and holds the full set of executable queries.

---

## 📂 Folder structure

```text
00-basics/
└── SQL/
    ├── Lesson01.sql
    ├── Lesson02.sql
    ├── Lesson03.sql
    ├── Lesson04.sql
    ├── Lesson05.sql
    ├── Lesson06.sql
    ├── Lesson07.sql
    ├── Lesson08.sql
    ├── Lesson09.sql
    ├── Lesson10.sql
    ├── Lesson11.sql
    ├── Lesson12.sql
    ├── Lesson13.sql
    ├── Lesson14.sql
    ├── Lesson15.sql
    ├── Lesson16.sql
    ├── Lesson17.sql
    ├── Lesson18.sql
    └── README.md
```

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
