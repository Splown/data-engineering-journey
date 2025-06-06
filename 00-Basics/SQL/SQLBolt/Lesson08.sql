/*
This exercise will be a sort of review of the last few lessons. 
We're using the same Employees and Buildings table from the last lesson, 
but we've hired a few more people, who haven't yet been assigned a building.

Table: buildings (Read-only)
building_name	capacity
1e	24
1w	32
2e	16
2w	20

Table: employees (Read-only)
role	name	building	years_employed
Engineer	Becky A.	1e	4
Engineer	Dan B.	1e	2
Engineer	Sharon F.	1e	6
Engineer	Dan M.	1e	4
Engineer	Malcom S.	1e	1
Artist	Tylar S.	2w	2
Artist	Sherman D.	2w	8
Artist	Jakob J.	2w	6
Artist	Lillia A.	2w	7
Artist	Brandon J.	2w	7
Manager	Scott K.	1e	9
Manager	Shirlee M.	1e	3
Manager	Daria O.	2w	6
Engineer	Yancy I.		0
Artist	Oliver P.		0
*/

-- Solution 1:
SELECT e.name, e.role
FROM employees e
where e.building is null;

-- Solution 2:
SELECT DISTINCT b.building_name
FROM buildings b
LEFT JOIN employees e
ON b.building_name = e.building
WHERE e.role IS NULL;