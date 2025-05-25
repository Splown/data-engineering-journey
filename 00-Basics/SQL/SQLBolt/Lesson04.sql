/*
There are a few concepts in this lesson, but all are pretty straight-forward to apply. To spice things up, we've gone and scrambled the Movies table for you in the exercise to better mimic what kind of data you might see in real life. Try and use the necessary keywords and clauses introduced above in your queries.

Table: movies
id	title	director	year	length_minutes
1	Ratatouille	Brad Bird	2007	115
2	The Incredibles	Brad Bird	2004	116
3	Monsters, Inc.	Pete Docter	2001	92
4	Monsters University	Dan Scanlon	2013	110
5	A Bug's Life	John Lasseter	1998	95
6	Toy Story 2	John Lasseter	1999	93
7	Brave	Brenda Chapman	2012	102
8	Cars 2	John Lasseter	2011	120
9	Up	Pete Docter	2009	101
10	Cars	John Lasseter	2006	117
11	Toy Story	John Lasseter	1995	81
12	Finding Nemo	Andrew Stanton	2003	107
13	WALL-E	Andrew Stanton	2008	104
14	Toy Story 3	Lee Unkrich	2010	103

Exercise 4 — Tasks
List all directors of Pixar movies (alphabetically), without duplicates
List the last four Pixar movies released (ordered from most recent to least)
List the first five Pixar movies sorted alphabetically
List the next five Pixar movies sorted alphabetically
*/

-- Solution 1:
SELECT distinct Director FROM movies order by 1;

-- Solution 2:
SELECT title FROM movies order by year desc limit 4;

-- Solution 3:
SELECT title FROM movies order by 1 limit 5;

-- Solution 4:
SELECT title FROM movies order by 1 limit 5 offset 5;