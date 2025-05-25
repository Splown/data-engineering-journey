-- Write your PostgreSQL query statement below
SELECT 
    machine_id,
    ROUND(AVG(CASE 
        WHEN activity_type = 'end' THEN timestamp::numeric 
        ELSE -timestamp::numeric 
    END) * 2, 3) AS processing_time
FROM Activity
GROUP BY machine_id;