/*
For this exercise, we are going to work with our Employees table. 
Notice how the rows in this table have shared data, which will 
give us an opportunity to use aggregate functions to summarize some 
high-level metrics about the teams. Go ahead and give it a shot.

Table: employees
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

Exercise 10 — Tasks
Find the longest time that an employee has been at the studio
For each role, find the average number of years employed by employees in that role
Find the total number of employee years worked in each building
*/

-- Solution 1:
SELECT MAX(years_employed) 
FROM employees;

-- Solution 2:
SELECT role, avg(years_employed)
FROM employees
group by role;

-- Solution 3:
SELECT building, sum(years_employed)
FROM employees
group by building;