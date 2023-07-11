/*
Consider the following simplified database schema for a movie database:

Table: movies
Columns: movie_id, title, release_year, director_id

Table: directors
Columns: director_id, director_name

Table: genres
Columns: genre_id, genre_name

Table: movie_genres
Columns: movie_id, genre_id

*/

 CREATE TABLE directors (
  director_id INT PRIMARY KEY,
  director_name VARCHAR(20)
 );


CREATE TABLE genres(
  genre_id INT PRIMARY KEY,
  genre_name VARCHAR(20)
 );

 
 CREATE TABLE movies (
  movie_id INT PRIMARY KEY,
  title VARCHAR(20) UNIQUE,
  release_year VARCHAR(4),
  director_id INT NOT NULL,
   FOREIGN KEY (director_id) REFERENCES directors(director_id)
);

 CREATE TABLE movie_genres(
   movie_id INT NOT NULL,
   genre_id INT NOT NULL,
   FOREIGN KEY (movie_id) REFERENCES movies(movie_id),
   FOREIGN KEY (genre_id) REFERENCES genres(genre_id)
 );
 
 INSERT INTO genres VALUES (1001,'Action'),(1002,'Horror'),(1003,' Triller'),(1004,'Crime'),(1005,'Drama'),(1006,'Comedy');
   
 INSERT INTO directors VALUES (1000, 'Amar Kaushik'),(1001,'Venkat Prabhu'),(1002,'Karthik Varma Dandu'),(1003,'Sukumar'),
(1004,'Rajkumar Hirani'),(1005,'Hanu Raghavapudi'),(1006,'Prashanth Neel'),(1007,'S.S.Rajamouli');
  
 INSERT INTO movies VALUES ( 1, 'Bhediya', '2023', 1000),(2, 'Custody', '2023' , 1001),(3, 'Virupaksha', '2023', 1002), 
(4, 'Pushpa', '2022', 1003), (5, '3 Idiots', '2009', 1004),(6, 'Sita Ramam','2022',1005),(7, 'Ugram','2023',1006),(8,'RRR','2022',1007),(9,'Bahunali-1','2015',1007);
   
 INSERT INTO movie_genres VALUES (1,1002),(2,1001),(3,1003),(4,1004),(5,1006),(6,1005),(7,1003),(8,1005),(9,'1001');

/*1. Write a query to retrieve the movie title and the corresponding director name for all movies.*/
    SELECT m.title,d.director_name
    FROM movies m
    INNER JOIN directors d
    ON m.director_id = d.director_id;
/*2. Write a query to retrieve the movie title, release year, and the corresponding director name (if available) for all movies.*/
    SELECT m.title,m.release_year,d.director_name
    FROM movies m
    INNER JOIN directors d
    ON m.director_id = d.director_id;
/*3. Write a query to retrieve the director name and the titles of the movies they have directed (if available) for all directors.*/
    SELECT d.director_name, m.title
    FROM directors d 
    LEFT JOIN movies m
    ON d.director_id = m.director_id ;
/*4. Write a query to retrieve the movie title, release year, and the corresponding director name (if available) for all movies and directors.*/
    SELECT m.title, m.release_year, d.director_name
    FROM movies m
    RIGHT JOIN directors d
    ON d.director_id = m.director_id;
/*5. Write a query to retrieve the movie title and genre name for all combinations of movies and genres*/
    SELECT m.title, g.genre_name
    FROM movies m
    RIGHT JOIN genres g
    ON g.genre_id = m.director_id;
