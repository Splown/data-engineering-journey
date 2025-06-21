# LeetCode SQL track  🏅

*26 problems solved so far – all accepted on LeetCode MySQL 8 runner.*

| # | Title | Main concept | File |
|---|-------|--------------|------|
| 175 | Combine Two Tables | `LEFT JOIN` vs `INNER JOIN` | [lc175_combine_two_tables.sql](lc175_combine_two_tables.sql) |
| 176 | Second Highest Salary | `MAX`, sub-query | [176_second_highest_salary.sql](176_second_highest_salary.sql) |
| 177 | Nth Highest Salary | `DENSE_RANK()` / `LIMIT 1 OFFSET n` | [177_nth_highest_salary.sql](177_nth_highest_salary.sql) |
| 178 | Rank Scores | `RANK()` window func | [178_rank_scores.sql](178_rank_scores.sql) |
| 183 | Customers Who Never Order | anti-JOIN (`LEFT JOIN … WHERE NULL`) | [183_customers_who_never_order.sql](183_customers_who_never_order.sql) |
| 184 | Department Highest Salary | correlated sub-query + `GROUP BY` | [184_department_highest_salary.sql](184_department_highest_salary.sql) |
| 185 | Department Top 3 Salaries | `DENSE_RANK()`, partition | [185_department_top_three_salaries.sql](185_department_top_three_salaries.sql) |
| 196 | Delete Duplicate Emails | `DELETE` with self-JOIN | [lc196_delete_duplicate_emails.sql](lc196_delete_duplicate_emails.sql) |
| 197 | Rising Temperature | self-JOIN on `DATEDIFF` | [197_rising_temperature.sql](197_rising_temperature.sql) |
| 570 | Managers ≥5 Reports | `GROUP BY HAVING` | [570_managers_with_at_least_5_direct_reports.sql](570_managers_with_at_least_5_direct_reports.sql) |
| 595 | Big Countries | simple `WHERE`, aliases | [lc595_big_countries.sql](lc595_big_countries.sql) |
| 601 | Human Traffic of Stadium | sliding window with self-JOIN | [601_human_traffic_of_stadium.sql](601_human_traffic_of_stadium.sql) |
| 610 | Triangle Judgement | CASE / math logic | [610_triangle_judgement.sql](610_triangle_judgement.sql) |
| 627 | Swap Salary | `UPDATE` & temp col | [627_swap_salary.sql](627_swap_salary.sql) |
| 1084 | Sales Analysis III | `WHERE NOT EXISTS` | [1084_sales_analysis_iii.sql](1084_sales_analysis_iii.sql) |
| 1148 | Article Views I | `COUNT(DISTINCT)` | [lc1148_article_views.sql](lc1148_article_views.sql) |
| 1179 | Reformat Department Table | `CASE`, pivot | [1179_reformat_department_table.sql](1179_reformat_department_table.sql) |
| 1251 | Average Selling Price | join + `AVG()` | [1251_average_selling_price.sql](1251_average_selling_price.sql) |
| 1327 | List Products Ordered in Period | `BETWEEN` dates | [1327_list_the_products_ordered_in_a_period.sql](1327_list_the_products_ordered_in_a_period.sql) |
| 1485 | Group Sold Products By Date | JSON / group concat | [1485_group_sold_products_by_the_date.sql](1485_group_sold_products_by_the_date.sql) |
| 1517 | Find Users With Valid Emails | `REGEXP` validation | [1517_find_users_with_valid_e_mails.sql](1517_find_users_with_valid_e_mails.sql) |
| 1661 | Average Time of Process per Machine | window avg | [1661_average_time_of_process_per_machine.sql](1661_average_time_of_process_per_machine.sql) |
| 1667 | Fix Names in a Table | string ops, `CONCAT`, `UPPER()` | [lc1667_fix_names_in_a_table.sql](lc1667_fix_names_in_a_table.sql) |
| 1693 | Daily Leads & Partners | `DATE`, `GROUP BY` | [1693_daily_leads_and_partners.sql](1693_daily_leads_and_partners.sql) |
| 1934 | Confirmation Rate | division, cast to decimal | [1934_confirmation_rate.sql](1934_confirmation_rate.sql) |
| 1965 | Employees With Missing Info | `UNION`, data quality | [1965_employees_with_missing_information.sql](1965_employees_with_missing_information.sql) |

---

## 2️⃣ `00-basics/SQL/README.md`

```md
# SQL Foundations  🚀

This root folder tracks all structured-query learning in my **Data-Engineering-Journey**.
```
