/*
Here's the definition of a query with a WHERE clause again, 
go ahead and try and write some queries with the operators above to 
limit the results to the information we need in the tasks below.

Select query with constraints
SELECT column, another_column, …
FROM mytable
WHERE condition
    AND/OR another_condition
    AND/OR …;
Table: movies
id	title	director	year	length_minutes
1	Toy Story	John Lasseter	1995	81
2	A Bug's Life	John Lasseter	1998	95
3	Toy Story 2	John Lasseter	1999	93
4	Monsters, Inc.	Pete Docter	2001	92
5	Finding Nemo	Andrew Stanton	2003	107
6	The Incredibles	Brad Bird	2004	116
7	Cars	John Lasseter	2006	117
8	Ratatouille	Brad Bird	2007	115
9	WALL-E	Andrew Stanton	2008	104
10	Up	Pete Docter	2009	101
11	Toy Story 3	Lee Unkrich	2010	103
12	Cars 2	John Lasseter	2011	120
13	Brave	Brenda Chapman	2012	102
14	Monsters University	Dan Scanlon	2013	110
87	WALL-G	Brenda Chapman	2042	97

Find all the Toy Story movies
Find all the movies directed by John Lasseter
Find all the movies (and director) not directed by John Lasseter
Find all the WALL-* movies

*/

-- Solution 1:
SELECT * FROM movies where title like "Toy Story%"

-- Solution 2:
SELECT * FROM movies where director like "John Lasseter"

-- Solution 3:
SELECT title, director FROM movies where director not like "John Lasseter"

-- Solution 4:
SELECT title FROM movies where title like "WALL-%"