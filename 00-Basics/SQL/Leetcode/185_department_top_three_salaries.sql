-- Write your PostgreSQL query statement below
WITH ranked_salaries AS (
  SELECT
    e.id,
    e.name       AS employee,
    e.salary,
    e.departmentid,
    DENSE_RANK() OVER (
      PARTITION BY e.departmentid
      ORDER BY e.salary DESC
    ) AS dr
  FROM Employee e
)
SELECT
  d.name       AS department,
  rs.employee  AS employee,
  rs.salary    AS salary
FROM ranked_salaries rs
JOIN Department d
  ON rs.departmentid = d.id
WHERE rs.dr <= 3
ORDER BY department, salary DESC;
