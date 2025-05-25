SELECT 
    id,
    max(CASE WHEN month = 'Jan' THEN revenue END) AS "Jan_Revenue",
    max(CASE WHEN month = 'Feb' THEN revenue END) AS "Feb_Revenue",
    max(CASE WHEN month = 'Mar' THEN revenue END) AS "Mar_Revenue",
    max(CASE WHEN month = 'Apr' THEN revenue END) AS "Apr_Revenue",
    max(CASE WHEN month = 'May' THEN revenue END) AS "May_Revenue",
    max(CASE WHEN month = 'Jun' THEN revenue END) AS "Jun_Revenue",
    max(CASE WHEN month = 'Jul' THEN revenue END) AS "Jul_Revenue",
    max(CASE WHEN month = 'Aug' THEN revenue END) AS "Aug_Revenue",
    max(CASE WHEN month = 'Sep' THEN revenue END) AS "Sep_Revenue",
    max(CASE WHEN month = 'Oct' THEN revenue END) AS "Oct_Revenue",
    max(CASE WHEN month = 'Nov' THEN revenue END) AS "Nov_Revenue",
    max(CASE WHEN month = 'Dec' THEN revenue END) AS "Dec_Revenue"
FROM Department
GROUP BY id;