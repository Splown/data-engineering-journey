/*
In this exercise, you'll need to create a new table for us to insert some new rows into.

Create a new table named Database with the following columns:
– Name A string (text) describing the name of the database
– Version A number (floating point) of the latest version of this database
– Download_count An integer count of the number of times this database was downloaded

This table has no constraints.
*/

-- Solution:

create table database (
	name STRING PRIMARY KEY,
	version FLOAT,
	download_count INTEGER
)