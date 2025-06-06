/*
It looks like some of the information in our Movies database might be incorrect, 
so go ahead and fix them through the exercises below.

Table: movies
id	title	director	year	length_minutes
1	Toy Story	John Lasseter	1995	81
2	A Bug's Life	El Directore	1998	95
3	Toy Story 2	John Lasseter	1899	93
4	Monsters, Inc.	Pete Docter	2001	92
5	Finding Nemo	Andrew Stanton	2003	107
6	The Incredibles	Brad Bird	2004	116
7	Cars	John Lasseter	2006	117
8	Ratatouille	Brad Bird	2007	115
9	WALL-E	Andrew Stanton	2008	104
10	Up	Pete Docter	2009	101
11	Toy Story 8	El Directore	2010	103
12	Cars 2	John Lasseter	2011	120
13	Brave	Brenda Chapman	2012	102
14	Monsters University	Dan Scanlon	2013	110

Exercise 14 — Tasks
The director for A Bug's Life is incorrect, it was actually directed by John Lasseter
The year that Toy Story 2 was released is incorrect, it was actually released in 1999
Both the title and director for Toy Story 8 is incorrect! 
The title should be "Toy Story 3" and it was directed by Lee Unkrich

*/

-- Solution 1:
update movies
set director = "John Lasseter"
where id = 2

-- Solution 2:
update movies
set year = 1999
where id = 3

-- Solution 3:
update movies
set title = "Toy Story 3", director = "Lee Unkrich"
where id = 11