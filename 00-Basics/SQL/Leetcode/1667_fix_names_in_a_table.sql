select user_id, UPPER(LEFT(name,1)) || LOWER(SUBSTRING(name,2)) AS name
from users
order by user_id 