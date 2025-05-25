-- Write your PostgreSQL query statement below
WITH filtered AS (
  -- Behåll bara rader med ≥100 personer och numrera dem i stigande id-ordning
  SELECT
    id,
    visit_date,
    people,
    ROW_NUMBER() OVER (ORDER BY id) AS rn
  FROM Stadium
  WHERE people >= 100
),
grp AS (
  -- Identifiera grupper av på varandra följande id genom id − rn
  SELECT
    id,
    visit_date,
    people,
    id - rn AS grp_id
  FROM filtered
),
valid_groups AS (
  -- Välj bara de grupper som har minst 3 rader
  SELECT
    grp_id
  FROM grp
  GROUP BY grp_id
  HAVING COUNT(*) >= 3
)
-- Hämta alla rader som tillhör en giltig grupp och sortera på datum
SELECT
  g.id,
  g.visit_date,
  g.people
FROM grp g
JOIN valid_groups v
  ON g.grp_id = v.grp_id
ORDER BY g.visit_date;
