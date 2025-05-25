-- Write your PostgreSQL query statement below
SELECT
  s.user_id,
  CASE
    WHEN COALESCE(c.total, 0) > 0
      THEN ROUND(c.confirmed::numeric / c.total, 2)
    ELSE 0.00
  END AS confirmation_rate
FROM Signups s
LEFT JOIN (
  SELECT
    user_id,
    COUNT(*) AS total,
    SUM(CASE WHEN action = 'confirmed' THEN 1 ELSE 0 END) AS confirmed
  FROM Confirmations
  GROUP BY user_id
) c ON s.user_id = c.user_id;
