CREATE OR REPLACE FUNCTION NthHighestSalary(N INT) RETURNS TABLE (Salary INT) AS $$
BEGIN
  RETURN QUERY (
    -- Write your SQL query statement below.
    select case when n <= 0 then NULL::INT
    else (select distinct e.salary
    from employee e
    order by e.salary desc
    limit 1 offset (n-1))
    end
  );
END;
$$ LANGUAGE plpgsql;