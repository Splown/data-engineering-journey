/*
In this exercise, we are going to play studio executive and add a few movies to the Movies to our portfolio. 
In this table, the Id is an auto-incrementing integer, 
so you can try inserting a row with only the other columns defined.

Since the following lessons will modify the database, 
you'll have to manually run each query once they are ready to go.

Table: movies (Read-only)
id	title	director	year	length_minutes
1	Toy Story	John Lasseter	1995	81
2	A Bug's Life	John Lasseter	1998	95
3	Toy Story 2	John Lasseter	1999	93

Table: boxoffice (Read-only)
movie_id	rating	domestic_sales	international_sales
3	7.9	245852179	239163000
1	8.3	191796233	170162503
2	7.2	162798565	200600000

Exercise 13 — Tasks
Add the studio's new production, Toy Story 4 to the list of movies (you can use any director)
Toy Story 4 has been released to critical acclaim! 
It had a rating of 8.7, and made 340 million domestically and 270 million internationally. 
Add the record to the BoxOffice table.
*/

-- Solution 1:
INSERT INTO Movies
(Title, Director, Year, Length_minutes)
VALUES ("Toy Story 4", "Lee Unkrich", 2020, 102)

-- Solution 2:
INSERT INTO Boxoffice
(Movie_ID, Rating, Domestic_sales, International_sales)
VALUES(15, 8.7, 340000000, 270000000)