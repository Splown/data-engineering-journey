/*
The database needs to be cleaned up a little bit, so try and delete a few rows in the tasks below.

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

Exercise 15 — Tasks
This database is getting too big, lets remove all movies that were released before 2005.
Andrew Stanton has also left the studio, so please remove all movies directed by him.
*/

-- Solution 1:
delete from movies
where year < 2005

-- Solution 2:
delete from movies
where director = "Andrew Stanton"