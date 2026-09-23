# Item sheet

1028 items. For each one: read the question, run the SQL on the named database,
and record one verdict in RESPONSES.csv. Schemas are listed at the end.

## AL0001

Question: For each place, how many teachers are from there?

Database: `course_teach`

```sql
SELECT Hometown , COUNT(*) FROM teacher GROUP BY Hometown
```

## AL0002

Question: What are the ids and names of the battles that led to more than 10 people died.

Database: `battle_death`

```sql
SELECT T1.id , T1.name FROM battle AS T1 JOIN ship AS T2 ON T1.id = T2.lost_in_battle JOIN death AS T3 ON T2.id = T3.caused_by_ship_id GROUP BY T1.id HAVING sum(T3.killed) > 10
```

## AL0003

Question: Find the first name of students who have cat or dog.

Database: `pets_1`

```sql
SELECT T1.Fname
FROM Student AS T1
INNER JOIN Has_Pet AS T2 ON T1.StuID = T2.StuID
INNER JOIN Pets AS T3 ON T2.PetID = T3.PetID
WHERE T3.PetType IN ('cat', 'dog')
```

## AL0004

Question: Which language is the most popular in Aruba?

Database: `world_1`

```sql
SELECT Language
FROM countrylanguage
WHERE CountryCode = (
    SELECT Code FROM country WHERE Name = 'Aruba'
)
ORDER BY Percentage DESC
LIMIT 1
```

## AL0005

Question: How many flights arriving in Aberdeen ?

Database: `flight_2`

```sql
SELECT COUNT(*)
FROM flights f
JOIN airports a ON f.DestAirport = a.AirportCode
WHERE a.City = 'Aberdeen'
```

## AL0006

Question: Which airlines have departures from CVO but not from APG?

Database: `flight_2`

```sql
SELECT T1.Airline
FROM airlines AS T1
INNER JOIN flights AS T2 ON T1.uid = T2.Airline
WHERE T2.SourceAirport = 'CVO'
AND T1.uid NOT IN (
    SELECT Airline
    FROM flights
    WHERE SourceAirport = 'APG'
)
```

## AL0007

Question: List the first and last name of all players ordered by their age.

Database: `wta_1`

```sql
SELECT first_name, last_name
FROM players
ORDER BY strftime('%Y', 'now') - strftime('%Y', birth_date)
```

## AL0008

Question: Show the stadium name and capacity with most number of concerts in  2014 or after.

Database: `concert_singer`

```sql
SELECT T2.Name, T2.Capacity
FROM concert AS T1
INNER JOIN stadium AS T2 ON T1.Stadium_ID = T2.Stadium_ID
WHERE T1.Year >= 2014
GROUP BY T2.Name, T2.Capacity
ORDER BY COUNT(T1.concert_ID) DESC
LIMIT 1
```

## AL0009

Question: What region does Angola belong to and what is its population?

Database: `world_1`

```sql
SELECT Region , Population FROM country WHERE Name = "Angola"
```

## AL0010

Question: how many singers are from each country?

Database: `singer`

```sql
SELECT Citizenship, COUNT(*) FROM singer GROUP BY Citizenship
```

## AL0011

Question: What is the average, minimum, and maximum age of all singers from France?

Database: `concert_singer`

```sql
SELECT AVG(Age), MIN(Age), MAX(Age)
FROM singer
WHERE Country = 'France'
```

## AL0012

Question: For a volvo , how many cylinders does the version with least accelerate have?

Database: `car_1`

```sql
SELECT T1.cylinders FROM CARS_DATA AS T1 JOIN CAR_NAMES AS T2 ON T1.Id = T2.MakeId WHERE T2.Make LIKE "%volvo%" ORDER BY T1.accelerate ASC LIMIT 1
```

## AL0013

Question: Which district has both stores with less than 3000 goods and stores with more than 10000 goods?

Database: `employee_hire_evaluation`

```sql
SELECT District
FROM shop
WHERE Number_products < 3000
INTERSECT
SELECT District
FROM shop
WHERE Number_products > 10000
```

## AL0014

Question: What are the names of all European countries with at least 3 manufacturers?

Database: `car_1`

```sql
SELECT T1.CountryName
FROM countries AS T1
INNER JOIN continents AS T2 ON T1.Continent = T2.ContId
INNER JOIN car_makers AS T3 ON T1.CountryId = T3.Country
WHERE T2.Continent = 'europe'
GROUP BY T1.CountryName
HAVING COUNT(T3.Id) >= 3
```

## AL0015

Question: What are the first names and birth dates of players from the USA?

Database: `wta_1`

```sql
SELECT first_name , birth_date FROM players WHERE country_code = 'USA'
```

## AL0016

Question: How many ships ended up being Captured?

Database: `battle_death`

```sql
SELECT count(*) FROM ship WHERE disposition_of_ship = 'Captured'
```

## AL0017

Question: Show location and name for all stadiums that can fit between 5000 and 10000 people.

Database: `concert_singer`

```sql
SELECT LOCATION , name FROM stadium WHERE capacity BETWEEN 5000 AND 10000
```

## AL0018

Question: What is the title of all the cartools that are on the TV Channel with Sky Radio?

Database: `tvshow`

```sql
SELECT T1.Title FROM Cartoon AS T1 JOIN TV_Channel AS T2 ON T1.Channel = T2.id WHERE T2.series_name = "Sky Radio"
```

## AL0019

Question: What are the id, name and membership level of people who have paid the largest amount of money overall in all museum tickets?

Database: `museum_visit`

```sql
SELECT T1.ID, T1.Name, T1.Level_of_membership
FROM visitor AS T1
INNER JOIN visit AS T2 ON T1.ID = T2.visitor_ID
ORDER BY T2.Total_spent DESC
LIMIT 1
```

## AL0020

Question: What are the names and release years for all the songs of the youngest singer?

Database: `concert_singer`

```sql
SELECT song_name , song_release_year FROM singer ORDER BY age LIMIT 1
```

## AL0021

Question: What is the weekly rank for the  """"A Love of a Lifetime""""?

Database: `tvshow`

```sql
SELECT Weekly_Rank FROM TV_series WHERE Episode = 'A Love of a Lifetime'
```

## AL0022

Question: Find the make and production time of the cars that were produced in the earliest ?

Database: `car_1`

```sql
SELECT T1.Make, T2.Year
FROM car_names AS T1
INNER JOIN cars_data AS T2 ON T1.MakeId = T2.Id
ORDER BY T2.Year ASC
LIMIT 1
```

## AL0023

Question: What are the names of the stadiums without any concerts?

Database: `concert_singer`

```sql
SELECT name FROM stadium WHERE stadium_id NOT IN (SELECT stadium_id FROM concert)
```

## AL0024

Question: What is the name of the series that has the  """"A Love of a Lifetime""""?

Database: `tvshow`

```sql
SELECT T1.series_name
FROM TV_Channel AS T1
INNER JOIN TV_series AS T2 ON T1.id = T2.Channel
WHERE T2.Episode = 'A Love of a Lifetime'
```

## AL0025

Question: Which flight numbers correspond to United Airlines flights?

Database: `flight_2`

```sql
SELECT T1.FlightNo FROM FLIGHTS AS T1 JOIN AIRLINES AS T2 ON T1.Airline = T2.uid WHERE T2.Airline = "United Airlines"
```

## AL0026

Question: List all song names by singers older than average .

Database: `concert_singer`

```sql
SELECT Song_Name
FROM singer
WHERE Age > (SELECT AVG(Age) FROM singer)
```

## AL0027

Question: Show the name of teachers who are either 32 or 33 years old?

Database: `course_teach`

```sql
SELECT Name FROM teacher WHERE Age = 32 OR Age = 33
```

## AL0028

Question: What is the model for the car that is lighter than the average?

Database: `car_1`

```sql
SELECT T1.Model FROM CAR_NAMES AS T1 JOIN CARS_DATA AS T2 ON T1.MakeId = T2.Id WHERE T2.weight < (SELECT avg(weight) FROM CARS_DATA)
```

## AL0029

Question: What are the record companies of orchestras in descending order of time in which they started?

Database: `orchestra`

```sql
SELECT Record_Company
FROM orchestra
ORDER BY Year_of_Founded DESC
```

## AL0030

Question: What are different nationalities of people and the corresponding number of people from each country?

Database: `poker_player`

```sql
SELECT Nationality, COUNT(*) FROM people GROUP BY Nationality
```

## AL0031

Question: how many singers are from each country?

Database: `singer`

```sql
SELECT Citizenship , COUNT(*) FROM singer GROUP BY Citizenship
```

## AL0032

Question: List the name of teachers who are not from Little Lever Urban District.

Database: `course_teach`

```sql
SELECT Name FROM teacher WHERE Hometown != "Little Lever Urban District"
```

## AL0033

Question: What is the number of cartoones  Joseph Kuh writes?

Database: `tvshow`

```sql
SELECT count(*) FROM cartoon WHERE written_by = 'Joseph Kuhr'
```

## AL0034

Question: List singer names and number of concerts for each person.

Database: `concert_singer`

```sql
SELECT T1.Name, COUNT(T2.concert_ID) AS number_of_concerts
FROM singer AS T1
INNER JOIN singer_in_concert AS T2 ON T1.Singer_ID = T2.Singer_ID
GROUP BY T1.Name
```

## AL0035

Question: Show all countries and the number of singers in each nation.

Database: `concert_singer`

```sql
SELECT country , count(*) FROM singer GROUP BY country
```

## AL0036

Question: What are the id and names of the countries which have more than 3 car makers or produce the 'fiat' ?

Database: `car_1`

```sql
SELECT T1.CountryId, T1.CountryName
FROM countries AS T1
INNER JOIN car_makers AS T2 ON T1.CountryId = T2.Country
GROUP BY T1.CountryId, T1.CountryName
HAVING COUNT(T2.Id) > 3 OR SUM(CASE WHEN T2.Maker = 'fiat' THEN 1 ELSE 0 END) > 0
```

## AL0037

Question: What are the nations having at least one car maker? List name and id.

Database: `car_1`

```sql
SELECT T1.CountryName , T1.CountryId FROM COUNTRIES AS T1 JOIN CAR_MAKERS AS T2 ON T1.CountryId = T2.Country GROUP BY T1.CountryId HAVING count(*) >= 1
```

## AL0038

Question: What is the description of the treatment type that is the cheapest overall?

Database: `dog_kennels`

```sql
SELECT T1.treatment_type_description FROM Treatment_Types AS T1 JOIN Treatments AS T2 ON T1.treatment_type_code = T2.treatment_type_code GROUP BY T1.treatment_type_code ORDER BY avg(cost_of_treatment) LIMIT 1
```

## AL0039

Question: What is the name of the nation with the most car makers?

Database: `car_1`

```sql
SELECT T1.CountryName FROM COUNTRIES AS T1 JOIN CAR_MAKERS AS T2 ON T1.CountryId = T2.Country GROUP BY T1.CountryName ORDER BY Count(*) DESC LIMIT 1
```

## AL0040

Question: How many cities in each district have more number of people than average?

Database: `world_1`

```sql
SELECT count(*) , district FROM city WHERE population > (SELECT avg(population) FROM city) GROUP BY district
```

## AL0041

Question: What are the names of all cartoons Ben Jones directs?

Database: `tvshow`

```sql
SELECT Title
FROM Cartoon
WHERE Directed_by = 'Ben Jones'
```

## AL0042

Question: What is the total ticket expense of the lv 1 visitors?

Database: `museum_visit`

```sql
SELECT sum(t2.Total_spent) FROM visitor AS t1 JOIN visit AS t2 ON t1.id = t2.visitor_id WHERE t1.level_of_membership = 1
```

## AL0043

Question: List the title of all cartoon  Ben Jones or Brandon Vietti directs.

Database: `tvshow`

```sql
SELECT Title FROM Cartoon WHERE Directed_by = "Ben Jones" OR Directed_by = "Brandon Vietti"
```

## AL0044

Question: What is the id, line 1, and line 2 of the place with the most students?

Database: `student_transcripts_tracking`

```sql
SELECT T1.address_id , T1.line_1 , T1.line_2 FROM addresses AS T1 JOIN students AS T2 ON T1.address_id = T2.current_address_id GROUP BY T1.address_id ORDER BY count(*) DESC LIMIT 1
```

## AL0045

Question: Which place holds the most number of students currently? List the id and all lines.

Database: `student_transcripts_tracking`

```sql
SELECT T1.address_id , T1.line_1 , T1.line_2 , T1.line_3 FROM addresses AS T1 JOIN students AS T2 ON T1.address_id = T2.current_address_id GROUP BY T1.address_id ORDER BY count(*) DESC LIMIT 1
```

## AL0046

Question: Show names of people who  is not  from Russia.

Database: `poker_player`

```sql
SELECT Name
FROM people
WHERE Nationality != 'Russia'
```

## AL0047

Question: Return the record companies of orchestras, sorted ascending by the time they have existed.

Database: `orchestra`

```sql
SELECT Record_Company FROM orchestra ORDER BY Year_of_Founded ASC
```

## AL0048

Question: Find the type and weight of the youngest pet.

Database: `pets_1`

```sql
SELECT PetType, weight
FROM Pets
ORDER BY pet_age ASC
LIMIT 1
```

## AL0049

Question: What is the continent  which Anguilla belongs to?

Database: `world_1`

```sql
SELECT Continent FROM country WHERE Name = "Anguilla"
```

## AL0050

Question: Find the first name of students who have cat or dog.

Database: `pets_1`

```sql
SELECT DISTINCT T1.fname FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid = T2.stuid JOIN pets AS T3 ON T3.petid = T2.petid WHERE T3.pettype = 'cat' OR T3.pettype = 'dog'
```

## AL0051

Question: List the first name and birth date of all players from USA.

Database: `wta_1`

```sql
SELECT first_name, birth_date
FROM players
WHERE country_code = 'USA'
```

## AL0052

Question: How long is the people’s average life expectancy in Central Africa?

Database: `world_1`

```sql
SELECT avg(LifeExpectancy) FROM country WHERE Region = "Central Africa"
```

## AL0053

Question: What are the cities who have more than 160000 people and less than 900000 people?

Database: `world_1`

```sql
SELECT Name
FROM city
WHERE Population > 160000 AND Population < 900000
```

## AL0054

Question: What is the average life expectancy in African countries that are republics?

Database: `world_1`

```sql
SELECT avg(LifeExpectancy) FROM country WHERE Region = "Africa" AND GovernmentForm = "Republic"
```

## AL0055

Question: What are the dog name, age and weight of the dogs that were abandoned?

Database: `dog_kennels`

```sql
SELECT name, age, weight
FROM Dogs
WHERE abandoned_yn = '1'
```

## AL0056

Question: What is the maximum miles per gallon of the 8 CYL cars or cars produced before 1980 ?

Database: `car_1`

```sql
SELECT MAX(MPG) FROM cars_data WHERE Cylinders = 8 OR Year < 1980
```

## AL0057

Question: List the Episode of all  TV series showed on TV Channel with  """"Sky Radio"""".

Database: `tvshow`

```sql
SELECT T2.Episode FROM TV_Channel AS T1 JOIN TV_series AS T2 ON T1.id = T2.Channel WHERE T1.series_name = "Sky Radio"
```

## AL0058

Question: What is the name of country that has the shortest life expectancy in Asia?

Database: `world_1`

```sql
SELECT Name FROM country WHERE Continent = "Asia" ORDER BY LifeExpectancy LIMIT 1
```

## AL0059

Question: What is the series name and country of all TV channels that are playing cartoons  Ben Jones and Michael Chang directs?

Database: `tvshow`

```sql
SELECT DISTINCT T.series_name, T.Country
FROM TV_Channel T
INNER JOIN Cartoon C ON T.id = C.Channel
WHERE C.Directed_by IN ('Ben Jones', 'Michael Chang')
```

## AL0060

Question: Give the average life expectancy for countries in Africa which are republics?

Database: `world_1`

```sql
SELECT AVG(LifeExpectancy)
FROM country
WHERE Continent = 'Africa' AND GovernmentForm = 'Republic'
```

## AL0061

Question: What are the names of all stadiums that did not have a concert in 2014?

Database: `concert_singer`

```sql
SELECT name FROM stadium WHERE stadium_id NOT IN (SELECT stadium_id FROM concert WHERE YEAR = 2014)
```

## AL0062

Question: What is the content of TV Channel with ""Sky Radio""?

Database: `tvshow`

```sql
SELECT Content FROM TV_Channel WHERE series_name = 'Sky Radio'
```

## AL0063

Question: What is the number of car models created by American Motor Company?

Database: `car_1`

```sql
SELECT count(*) FROM CAR_MAKERS AS T1 JOIN MODEL_LIST AS T2 ON T1.Id = T2.Maker WHERE T1.FullName = 'American Motor Company'
```

## AL0064

Question: What is the TV Channel that shows The Rise of the Blue Beetle!? List the TV Channel's series name.

Database: `tvshow`

```sql
SELECT T1.series_name FROM TV_Channel AS T1 JOIN cartoon AS T2 ON T1.id = T2.Channel WHERE T2.Title = "The Rise of the Blue Beetle!"
```

## AL0065

Question: What is the description of the treatment type that is the cheapest overall?

Database: `dog_kennels`

```sql
SELECT T1.treatment_type_description
FROM Treatment_Types AS T1
INNER JOIN Treatments AS T2 ON T1.treatment_type_code = T2.treatment_type_code
ORDER BY T2.cost_of_treatment ASC
LIMIT 1
```

## AL0066

Question: How many flights arrive at ATO?

Database: `flight_2`

```sql
SELECT count(*) FROM FLIGHTS WHERE DestAirport = "ATO"
```

## AL0067

Question: How many models does each manufacturer produce? List maker full name, id and the number.

Database: `car_1`

```sql
SELECT T1.FullName, T1.Id, COUNT(T2.Model)
FROM car_makers AS T1
INNER JOIN model_list AS T2 ON T1.Id = T2.Maker
GROUP BY T1.Id, T1.FullName
```

## AL0068

Question: What is the average life expectancy in African countries that are republics?

Database: `world_1`

```sql
SELECT AVG(LifeExpectancy)
FROM country
WHERE Continent = 'Africa' AND GovernmentForm = 'Republic'
```

## AL0069

Question: What are the codes of the countries that do not speak English and are not Republic?

Database: `world_1`

```sql
SELECT Code FROM country WHERE GovernmentForm != "Republic" EXCEPT SELECT CountryCode FROM countrylanguage WHERE LANGUAGE = "English"
```

## AL0070

Question: Which dogs are owned by someone who lives in Virginia? List the owner's first name and the dog's name.

Database: `dog_kennels`

```sql
SELECT T1.first_name, T2.name
FROM Owners AS T1
INNER JOIN Dogs AS T2 ON T1.owner_id = T2.owner_id
WHERE T1.state = 'Virginia'
```

## AL0071

Question: Give the total population and average  corresponding to countries in Noth America that is bigger than 3000 square miles.

Database: `world_1`

```sql
SELECT sum(population) , avg(population) FROM country WHERE continent = "north america" AND surfacearea > 3000
```

## AL0072

Question: What are the names of the teachers who do not come from Little Lever Urban District?

Database: `course_teach`

```sql
SELECT Name
FROM teacher
WHERE Hometown != 'Little Lever Urban District'
```

## AL0073

Question: Which language is the most popular in Aruba?

Database: `world_1`

```sql
SELECT T2.Language FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode WHERE T1.Name = "Aruba" ORDER BY T2.Percentage DESC LIMIT 1
```

## AL0074

Question: Show names of people who  is not  from Russia.

Database: `poker_player`

```sql
SELECT Name FROM people WHERE Nationality != "Russia"
```

## AL0075

Question: What is the series name of the TV Channel that shows ""The Rise of the Blue Beetle""?

Database: `tvshow`

```sql
SELECT T.series_name
FROM Cartoon C
JOIN TV_Channel T ON C.Channel = T.id
WHERE C.Title = 'The Rise of the Blue Beetle!'
```

## AL0076

Question: find the names of loser and winner who played in the match that last for the longest of time.

Database: `wta_1`

```sql
SELECT winner_name , loser_name FROM matches ORDER BY minutes DESC LIMIT 1
```

## AL0077

Question: what are the different names of the singers that have  sold than 300000 copies?

Database: `singer`

```sql
SELECT DISTINCT T1.Name FROM singer AS T1 JOIN song AS T2 ON T1.Singer_ID = T2.Singer_ID WHERE T2.Sales > 300000
```

## AL0078

Question: Find the first name and age of students who have a dog but do not have a cat.

Database: `pets_1`

```sql
SELECT T1.fname , T1.age FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid = T2.stuid JOIN pets AS T3 ON T2.petid = T3.petid WHERE T3.pettype = 'dog' EXCEPT SELECT T1.fname , T1.age FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid = T2.stuid JOIN pets AS T3 ON T2.petid = T3.petid WHERE T3.pettype = 'cat'
```

## AL0079

Question: Find the id and zip code of the person who spent the most money in total for his or her dogs.

Database: `dog_kennels`

```sql
SELECT T1.owner_id, T1.zip_code
FROM Owners AS T1
INNER JOIN Dogs AS T2 ON T1.owner_id = T2.owner_id
INNER JOIN Treatments AS T3 ON T2.dog_id = T3.dog_id
GROUP BY T1.owner_id, T1.zip_code
ORDER BY SUM(T3.cost_of_treatment) DESC
LIMIT 1
```

## AL0080

Question: Find the city with the most people that uses English.

Database: `world_1`

```sql
SELECT T1.Name
FROM city AS T1
INNER JOIN countrylanguage AS T2 ON T1.CountryCode = T2.CountryCode
WHERE T2.Language = 'English'
ORDER BY T1.Population DESC
LIMIT 1
```

## AL0081

Question: Who owns the youngest dog? Give me his or her last name.

Database: `dog_kennels`

```sql
SELECT T1.last_name
FROM Owners AS T1
INNER JOIN Dogs AS T2 ON T1.owner_id = T2.owner_id
ORDER BY T2.date_of_birth DESC
LIMIT 1
```

## AL0082

Question: How many TV Channel using  English?

Database: `tvshow`

```sql
SELECT COUNT(*) FROM TV_Channel WHERE Language = 'English'
```

## AL0083

Question: What are the regions that use English or Dutch?

Database: `world_1`

```sql
SELECT DISTINCT T1.Region
FROM country AS T1
INNER JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode
WHERE T2.Language IN ('English', 'Dutch')
```

## AL0084

Question: What is the first name and country code of the oldest player?

Database: `wta_1`

```sql
SELECT first_name, country_code
FROM players
ORDER BY birth_date ASC
LIMIT 1
```

## AL0085

Question: what is the name and nation of the singer who have a song having 'Hey' in its title?

Database: `concert_singer`

```sql
SELECT Name, Country
FROM singer
WHERE Song_Name LIKE '%Hey%'
```

## AL0086

Question: What language is predominantly spoken in Aruba?

Database: `world_1`

```sql
SELECT T2.Language FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode WHERE T1.Name = "Aruba" ORDER BY T2.Percentage DESC LIMIT 1
```

## AL0087

Question: Show the stadium name and capacity with most number of concerts in  2014 or after.

Database: `concert_singer`

```sql
SELECT T2.name , T2.capacity FROM concert AS T1 JOIN stadium AS T2 ON T1.stadium_id = T2.stadium_id WHERE T1.year >= 2014 GROUP BY T2.stadium_id ORDER BY count(*) DESC LIMIT 1
```

## AL0088

Question: What are the different models created by either General Motors or over 3500 lbs?

Database: `car_1`

```sql
SELECT DISTINCT T1.Model
FROM car_names AS T1
INNER JOIN cars_data AS T2 ON T1.MakeId = T2.Id
INNER JOIN model_list AS T3 ON T1.Model = T3.Model
INNER JOIN car_makers AS T4 ON T3.Maker = T4.Id
WHERE T4.FullName = 'General Motors' OR T2.Weight > 3500
```

## AL0089

Question: What are flight numbers of flights arriving at APG?

Database: `flight_2`

```sql
SELECT FlightNo
FROM flights
WHERE DestAirport = 'APG'
```

## AL0090

Question: which countries' tv channels are playing some cartoon  Todd Casey writes?

Database: `tvshow`

```sql
SELECT DISTINCT T1.Country
FROM TV_Channel AS T1
INNER JOIN Cartoon AS T2 ON T1.id = T2.Channel
WHERE T2.Written_by = 'Todd Casey'
```

## AL0091

Question: What is the first name of every student who has a dog but does not have a cat?

Database: `pets_1`

```sql
SELECT T1.Fname
FROM Student AS T1
INNER JOIN Has_Pet AS T2 ON T1.StuID = T2.StuID
INNER JOIN Pets AS T3 ON T2.PetID = T3.PetID
WHERE T3.PetType = 'dog'
AND T1.StuID NOT IN (
    SELECT T4.StuID
    FROM Has_Pet AS T4
    INNER JOIN Pets AS T5 ON T4.PetID = T5.PetID
    WHERE T5.PetType = 'cat'
)
```

## AL0092

Question: What are the first names and country codes for players who won both the WTA Championships and the Australian Open?

Database: `wta_1`

```sql
SELECT DISTINCT p.first_name, p.country_code
FROM players p
INNER JOIN matches m1 ON p.player_id = m1.winner_id
INNER JOIN matches m2 ON p.player_id = m2.winner_id
WHERE m1.tourney_name = 'WTA Championships'
  AND m2.tourney_name = 'Australian Open'
```

## AL0093

Question: Give the country codes for countries in which people does not speak English.

Database: `world_1`

```sql
SELECT Code FROM country EXCEPT SELECT CountryCode FROM countrylanguage WHERE LANGUAGE = "English"
```

## AL0094

Question: For each place, how many teachers are from there?

Database: `course_teach`

```sql
SELECT Hometown, COUNT(*) FROM teacher GROUP BY Hometown
```

## AL0095

Question: For  volvo, how many cylinders does the car with the least accelerate have?

Database: `car_1`

```sql
SELECT T3.Cylinders
FROM car_makers AS T1
INNER JOIN model_list AS T2 ON T1.Id = T2.Maker
INNER JOIN car_names AS T4 ON T2.Model = T4.Model
INNER JOIN cars_data AS T3 ON T4.MakeId = T3.Id
WHERE T1.Maker = 'volvo'
ORDER BY T3.Accelerate ASC
LIMIT 1
```

## AL0096

Question: Give the country codes for countries in which people does not speak English.

Database: `world_1`

```sql
SELECT CountryCode
FROM countrylanguage
WHERE Language != 'English'
```

## AL0097

Question: How many high schoolers are there in  9 or 10?

Database: `network_1`

```sql
SELECT count(*) FROM Highschooler WHERE grade = 9 OR grade = 10
```

## AL0098

Question: What are the names and release years for all the songs of the youngest singer?

Database: `concert_singer`

```sql
SELECT Song_Name, Song_release_year
FROM singer
WHERE Age = (SELECT MIN(Age) FROM singer)
```

## AL0099

Question: Return the names of cities that have between 160000 and 900000 people.

Database: `world_1`

```sql
SELECT Name
FROM city
WHERE Population BETWEEN 160000 AND 900000
```

## AL0100

Question: Give the name of the nation that uses the greatest amount of languages.

Database: `world_1`

```sql
SELECT T1.Name FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode GROUP BY T1.Name ORDER BY COUNT(*) DESC LIMIT 1
```

## AL0101

Question: Find the id and name of the museum that has the most employees?

Database: `museum_visit`

```sql
SELECT museum_id , name FROM museum ORDER BY num_of_staff DESC LIMIT 1
```

## AL0102

Question: Show different hometown of teachers and the number of teachers from each place.

Database: `course_teach`

```sql
SELECT Hometown, COUNT(*) FROM teacher GROUP BY Hometown
```

## AL0103

Question: What language is predominantly spoken in Aruba?

Database: `world_1`

```sql
SELECT T2.Language
FROM country AS T1
INNER JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode
WHERE T1.Name = 'Aruba'
ORDER BY T2.Percentage DESC
LIMIT 1
```

## AL0104

Question: Find the number of shops in each place.

Database: `employee_hire_evaluation`

```sql
SELECT count(*) , LOCATION FROM shop GROUP BY LOCATION
```

## AL0105

Question: What is the id of the semester that had both Masters and Bachelors students enrolled?

Database: `student_transcripts_tracking`

```sql
SELECT T1.semester_id
FROM Student_Enrolment AS T1
INNER JOIN Degree_Programs AS T2 ON T1.degree_program_id = T2.degree_program_id
WHERE T2.degree_summary_name = 'Master'
INTERSECT
SELECT T1.semester_id
FROM Student_Enrolment AS T1
INNER JOIN Degree_Programs AS T2 ON T1.degree_program_id = T2.degree_program_id
WHERE T2.degree_summary_name = 'Bachelor'
```

## AL0106

Question: Which shops have more than average merchandise? Give me the shop names.

Database: `employee_hire_evaluation`

```sql
SELECT Name
FROM shop
WHERE Number_products > (SELECT AVG(Number_products) FROM shop)
```

## AL0107

Question: What are the package options and the name of the series for the TV Channel that supports HDTV?

Database: `tvshow`

```sql
SELECT Package_Option, series_name
FROM TV_Channel
WHERE Hight_definition_TV = 'yes'
```

## AL0108

Question: Which airlines have a flight from  AHD?

Database: `flight_2`

```sql
SELECT T1.Airline FROM AIRLINES AS T1 JOIN FLIGHTS AS T2 ON T1.uid = T2.Airline WHERE T2.SourceAirport = "AHD"
```

## AL0109

Question: List the title of all  Cartoons showed on TV Channel with  ""Sky Radio"".

Database: `tvshow`

```sql
SELECT T1.Title
FROM Cartoon AS T1
INNER JOIN TV_Channel AS T2 ON T1.Channel = T2.id
WHERE T2.series_name = 'Sky Radio'
```

## AL0110

Question: What are the names of the singers who are not French?

Database: `singer`

```sql
SELECT Name FROM singer WHERE Citizenship != "France"
```

## AL0111

Question: Count the number of high schoolers in grades 9 or 10.

Database: `network_1`

```sql
SELECT count(*) FROM Highschooler WHERE grade = 9 OR grade = 10
```

## AL0112

Question: How many 'United Airlines' flights go to 'ASY'?

Database: `flight_2`

```sql
SELECT count(*) FROM FLIGHTS AS T1 JOIN AIRLINES AS T2 ON T1.Airline = T2.uid WHERE T2.Airline = "United Airlines" AND T1.DestAirport = "ASY"
```

## AL0113

Question: Give the flight numbers of flights landing at APG.

Database: `flight_2`

```sql
SELECT FlightNo FROM FLIGHTS WHERE DestAirport = "APG"
```

## AL0114

Question: What type of pet is the youngest animal, and how much does it weigh?

Database: `pets_1`

```sql
SELECT PetType, weight
FROM Pets
ORDER BY pet_age ASC
LIMIT 1
```

## AL0115

Question: What are the region and population of Angola?

Database: `world_1`

```sql
SELECT Region, Population
FROM country
WHERE Name = 'Angola'
```

## AL0116

Question: How many singers are from each nation?

Database: `concert_singer`

```sql
SELECT Country, COUNT(*) FROM singer GROUP BY Country
```

## AL0117

Question: What are the names of singers ordered by ascending wealth?

Database: `singer`

```sql
SELECT Name
FROM singer
ORDER BY Net_Worth_Millions ASC
```

## AL0118

Question: Which language is the most popular on Asian ?

Database: `world_1`

```sql
SELECT T2.Language
FROM country AS T1
INNER JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode
WHERE T1.Continent = 'Asia'
ORDER BY T2.Percentage DESC
LIMIT 1
```

## AL0119

Question: What is the official language spoken in the country lead by Beatrix?

Database: `world_1`

```sql
SELECT T2.Language FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode WHERE T1.HeadOfState = "Beatrix" AND T2.IsOfficial = "T"
```

## AL0120

Question: What is the total ticket expense of the lv 1 visitors?

Database: `museum_visit`

```sql
SELECT SUM(Total_spent)
FROM visit
INNER JOIN visitor ON visit.visitor_ID = visitor.ID
WHERE visitor.Level_of_membership = 1
```

## AL0121

Question: What are the students' first names who have both cats and dogs?

Database: `pets_1`

```sql
SELECT T1.Fname
FROM Student AS T1
INNER JOIN Has_Pet AS T2 ON T1.StuID = T2.StuID
INNER JOIN Pets AS T3 ON T2.PetID = T3.PetID
GROUP BY T1.Fname
HAVING SUM(CASE WHEN T3.PetType = 'cat' THEN 1 ELSE 0 END) > 0
   AND SUM(CASE WHEN T3.PetType = 'dog' THEN 1 ELSE 0 END) > 0
```

## AL0122

Question: What are the dog name, age and weight of the dogs that were abandoned?

Database: `dog_kennels`

```sql
SELECT name , age , weight FROM Dogs WHERE abandoned_yn = 1
```

## AL0123

Question: Find the manager name and district of the shop with the most goods.

Database: `employee_hire_evaluation`

```sql
SELECT manager_name , district FROM shop ORDER BY number_products DESC LIMIT 1
```

## AL0124

Question: What are the nations having at least one car maker? List name and id.

Database: `car_1`

```sql
SELECT DISTINCT T1.CountryId, T1.CountryName
FROM countries AS T1
INNER JOIN car_makers AS T2 ON T1.CountryId = T2.Country
```

## AL0125

Question: What is the continent  which Anguilla belongs to?

Database: `world_1`

```sql
SELECT Continent FROM country WHERE Name = 'Anguilla'
```

## AL0126

Question: What are the names and ids of all car companies with more than 3 models?

Database: `car_1`

```sql
SELECT T1.Id, T1.Maker
FROM car_makers AS T1
INNER JOIN model_list AS T2 ON T1.Id = T2.Maker
GROUP BY T1.Id, T1.Maker
HAVING COUNT(T2.Model) > 3
```

## AL0127

Question: How many languages are spoken in Aruba?

Database: `world_1`

```sql
SELECT COUNT(*) FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode WHERE T1.Name = "Aruba"
```

## AL0128

Question: What are the different years in which there were cars produced between 3000 and 4000 pounds?

Database: `car_1`

```sql
SELECT DISTINCT YEAR FROM CARS_DATA WHERE Weight BETWEEN 3000 AND 4000
```

## AL0129

Question: What is the lowest grade of students who do not have any friends?

Database: `network_1`

```sql
SELECT min(grade) FROM Highschooler WHERE id NOT IN (SELECT student_id FROM Friend)
```

## AL0130

Question: Find the name of the winner who has the highest rank points and participated in the Australian Open.

Database: `wta_1`

```sql
SELECT winner_name FROM matches WHERE tourney_name = 'Australian Open' ORDER BY winner_rank_points DESC LIMIT 1
```

## AL0131

Question: What is the name and capacity of the stadium  with the most concerts after 2013?

Database: `concert_singer`

```sql
SELECT T2.name , T2.capacity FROM concert AS T1 JOIN stadium AS T2 ON T1.stadium_id = T2.stadium_id WHERE T1.year > 2013 GROUP BY T2.stadium_id ORDER BY count(*) DESC LIMIT 1
```

## AL0132

Question: Find the name and rank points of the person who won the most times.

Database: `wta_1`

```sql
SELECT p.first_name, p.last_name, r.ranking_points
FROM matches m
INNER JOIN players p ON m.winner_id = p.player_id
INNER JOIN rankings r ON m.winner_id = r.player_id
GROUP BY m.winner_id
ORDER BY COUNT(m.winner_id) DESC
LIMIT 1
```

## AL0133

Question: Find the make and production time of the cars that were produced in the earliest ?

Database: `car_1`

```sql
SELECT T1.Make , T2.Year FROM CAR_NAMES AS T1 JOIN CARS_DATA AS T2 ON T1.MakeId = T2.Id ORDER BY T2.Year ASC LIMIT 1
```

## AL0134

Question: Give the names of countries officially use English and French

Database: `world_1`

```sql
SELECT T1.Name FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode WHERE T2.IsOfficial = "T" AND T2.Language = "English" INTERSECT SELECT T1.Name FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode WHERE T2.IsOfficial = "T" AND T2.Language = "French"
```

## AL0135

Question: Find the number of orchestras recorded in """"CD"""" or """"DVD"""".

Database: `orchestra`

```sql
SELECT COUNT(*) FROM orchestra WHERE Major_Record_Format IN ('CD', 'DVD')
```

## AL0136

Question: What are the names of the cartoons sorted alphabetically?

Database: `tvshow`

```sql
SELECT Title
FROM Cartoon
ORDER BY Title ASC
```

## AL0137

Question: Find the manager name and district of the shop with the most goods.

Database: `employee_hire_evaluation`

```sql
SELECT Manager_name, District
FROM shop
ORDER BY Number_products DESC
LIMIT 1
```

## AL0138

Question: Find the name of the shops that do not recruit any employee.

Database: `employee_hire_evaluation`

```sql
SELECT Name
FROM shop
WHERE Shop_ID NOT IN (SELECT Shop_ID FROM hiring)
```

## AL0139

Question: Show the name and theme for all concerts and the number of singers in each.

Database: `concert_singer`

```sql
SELECT T1.concert_Name, T1.Theme, COUNT(T2.Singer_ID) AS num_singers
FROM concert AS T1
INNER JOIN singer_in_concert AS T2 ON T1.concert_ID = T2.concert_ID
GROUP BY T1.concert_Name, T1.Theme
```

## AL0140

Question: Which shops have more than average merchandise? Give me the shop names.

Database: `employee_hire_evaluation`

```sql
SELECT name FROM shop WHERE number_products > (SELECT avg(number_products) FROM shop)
```

## AL0141

Question: find id of the tv channels that from the nations where have more than two tv channels.

Database: `tvshow`

```sql
SELECT id
FROM TV_Channel
WHERE Country IN (
    SELECT Country
    FROM TV_Channel
    GROUP BY Country
    HAVING COUNT(id) > 2
)
```

## AL0142

Question: Find the name of the makers that produced some cars in 1970?

Database: `car_1`

```sql
SELECT DISTINCT T1.Maker
FROM car_makers AS T1
INNER JOIN model_list AS T2 ON T1.Id = T2.Maker
INNER JOIN car_names AS T3 ON T2.Model = T3.Model
INNER JOIN cars_data AS T4 ON T3.MakeId = T4.Id
WHERE T4.Year = 1970
```

## AL0143

Question: Which abbreviation corresponds to Jetblue Airways?

Database: `flight_2`

```sql
SELECT Abbreviation FROM AIRLINES WHERE Airline = "JetBlue Airways"
```

## AL0144

Question: Which shops run with no employees? Find the shop names

Database: `employee_hire_evaluation`

```sql
SELECT Name
FROM shop
WHERE Shop_ID NOT IN (SELECT Shop_ID FROM hiring)
```

## AL0145

Question: What are all the song names by singers who are older than average?

Database: `concert_singer`

```sql
SELECT song_name FROM singer WHERE age > (SELECT avg(age) FROM singer)
```

## AL0146

Question: Count the number of flights departing from 'APG'.

Database: `flight_2`

```sql
SELECT COUNT(*) FROM flights WHERE SourceAirport = 'APG'
```

## AL0147

Question: Count the number of dogs that are younger than the average.

Database: `dog_kennels`

```sql
SELECT COUNT(*)
FROM Dogs
WHERE CAST(age AS INTEGER) < (SELECT AVG(CAST(age AS INTEGER)) FROM Dogs)
```

## AL0148

Question: Where is the youngest teacher from?

Database: `course_teach`

```sql
SELECT Hometown FROM teacher ORDER BY Age ASC LIMIT 1
```

## AL0149

Question: Find the series name and country of the tv channel that is playing some cartoons  Ben Jones and Michael Chang directs?

Database: `tvshow`

```sql
SELECT DISTINCT T.series_name, T.Country
FROM Cartoon C
INNER JOIN TV_Channel T ON C.Channel = T.id
WHERE C.Directed_by IN ('Ben Jones', 'Michael Chang')
```

## AL0150

Question: How many concerts occurred in 2014 or 2015?

Database: `concert_singer`

```sql
SELECT count(*) FROM concert WHERE YEAR = 2014 OR YEAR = 2015
```

## AL0151

Question: How many flights fly from Aberdeen to Ashley?

Database: `flight_2`

```sql
SELECT count(*) FROM FLIGHTS AS T1 JOIN AIRPORTS AS T2 ON T1.DestAirport = T2.AirportCode JOIN AIRPORTS AS T3 ON T1.SourceAirport = T3.AirportCode WHERE T2.City = "Ashley" AND T3.City = "Aberdeen"
```

## AL0152

Question: How many official languages does Afghanistan have?

Database: `world_1`

```sql
SELECT COUNT(*) FROM countrylanguage WHERE CountryCode = 'AFG' AND IsOfficial = 'T'
```

## AL0153

Question: What are the first name and last name of the professionals who have done treatment cheaper than average?

Database: `dog_kennels`

```sql
SELECT DISTINCT T1.first_name , T1.last_name FROM professionals AS T1 JOIN treatments AS T2 ON T1.professional_id = T2.professional_id WHERE cost_of_treatment < ( SELECT avg(cost_of_treatment) FROM treatments )
```

## AL0154

Question: What is the average GNP and total population in all US territory nations?

Database: `world_1`

```sql
SELECT AVG(GNP) AS AverageGNP, SUM(Population) AS TotalPopulation
FROM country
WHERE GovernmentForm LIKE '%United States%'
```

## AL0155

Question: Show the names of all high schoolers in  10.

Database: `network_1`

```sql
SELECT name FROM Highschooler WHERE grade = 10
```

## AL0156

Question: List the last name of the owner owning the youngest dog.

Database: `dog_kennels`

```sql
SELECT T1.last_name FROM Owners AS T1 JOIN Dogs AS T2 ON T1.owner_id = T2.owner_id ORDER BY T2.date_of_birth DESC LIMIT 1
```

## AL0157

Question: What is the number of the cars with  more than 150 hp?

Database: `car_1`

```sql
SELECT COUNT(*)
FROM cars_data
WHERE CAST(Horsepower AS INTEGER) > 150
```

## AL0158

Question: List the first and last name of all players who are left handed  in the order of age.

Database: `wta_1`

```sql
SELECT first_name, last_name
FROM players
WHERE hand = 'L'
ORDER BY strftime('%Y', 'now') - strftime('%Y', birth_date)
```

## AL0159

Question: What are the name, independence year, and surface area of the country with the least number of nationalities?

Database: `world_1`

```sql
SELECT T1.Name, T1.IndepYear, T1.SurfaceArea
FROM country AS T1
INNER JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode
GROUP BY T1.Code
ORDER BY COUNT(T2.Language) ASC
LIMIT 1
```

## AL0160

Question: How many different winners both participated in the WTA Championships and were left handed?

Database: `wta_1`

```sql
SELECT count(DISTINCT winner_name) FROM matches WHERE tourney_name = 'WTA Championships' AND winner_hand = 'L'
```

## AL0161

Question: List the most common place that the teachers come from

Database: `course_teach`

```sql
SELECT Hometown
FROM teacher
GROUP BY Hometown
ORDER BY COUNT(Hometown) DESC
LIMIT 1
```

## AL0162

Question: What are the names of the nations with the 3 lowest number of citizens?

Database: `world_1`

```sql
SELECT Name FROM country ORDER BY Population ASC LIMIT 3
```

## AL0163

Question: How many different winners both participated in the WTA Championships and were left handed?

Database: `wta_1`

```sql
SELECT COUNT(DISTINCT winner_id)
FROM matches
WHERE tourney_name = 'WTA Championships'
  AND winner_hand = 'L'
```

## AL0164

Question: Show names, results and bulgarian commanders of the battles with no ships lost in the 'English Channel'.

Database: `battle_death`

```sql
SELECT t1.name , t1.result , t1.bulgarian_commander FROM battle AS t1 JOIN ship AS t2 ON t1.id = t2.lost_in_battle WHERE t2.location != 'English Channel'
```

## AL0165

Question: For each country, what is the maximum net worth?

Database: `singer`

```sql
SELECT max(Net_Worth_Millions) , Citizenship FROM singer GROUP BY Citizenship
```

## AL0166

Question: What are the package options of all tv channels that are not playing any cartoons  Ben Jones directs?

Database: `tvshow`

```sql
SELECT Package_Option
FROM TV_Channel
WHERE id NOT IN (
    SELECT Channel
    FROM Cartoon
    WHERE Directed_by = 'Ben Jones'
)
```

## AL0167

Question: For all of the 4 CYL cars, which model has the most horsepower?

Database: `car_1`

```sql
SELECT T2.Model
FROM cars_data AS T1
INNER JOIN car_names AS T2 ON T1.Id = T2.MakeId
WHERE T1.Cylinders = 4
ORDER BY CAST(T1.Horsepower AS INTEGER) DESC
LIMIT 1
```

## AL0168

Question: Return the codes of non republic countries that do not speak Englishs.

Database: `world_1`

```sql
SELECT Code
FROM country
WHERE GovernmentForm != 'Republic'
  AND Code NOT IN (
    SELECT CountryCode
    FROM countrylanguage
    WHERE Language = 'English'
  )
```

## AL0169

Question: Which countries in europe have at least 3 car manufacturers?

Database: `car_1`

```sql
SELECT T1.CountryName
FROM countries AS T1
INNER JOIN car_makers AS T2 ON T1.CountryId = T2.Country
INNER JOIN continents AS T3 ON T1.Continent = T3.ContId
WHERE T3.Continent = 'europe'
GROUP BY T1.CountryName
HAVING COUNT(T2.Id) >= 3
```

## AL0170

Question: What are the names of people who are not from Russia?

Database: `poker_player`

```sql
SELECT Name FROM people WHERE Nationality != "Russia"
```

## AL0171

Question: How many different forms of governments are there in Africa?

Database: `world_1`

```sql
SELECT count(DISTINCT GovernmentForm) FROM country WHERE continent = "Africa"
```

## AL0172

Question: What is Weekly Rank of TV series with A Love of a Lifetime?

Database: `tvshow`

```sql
SELECT Weekly_Rank FROM TV_series WHERE Episode = "A Love of a Lifetime"
```

## AL0173

Question: What are the name, population, and life expectancy of the largest Asian country by land?

Database: `world_1`

```sql
SELECT Name, Population, LifeExpectancy
FROM country
WHERE Continent = 'Asia'
ORDER BY SurfaceArea DESC
LIMIT 1
```

## AL0174

Question: What are the name, independence year, and surface area of the country with the least number of nationalities?

Database: `world_1`

```sql
SELECT T1.Name , T1.IndepYear , T1.SurfaceArea FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode GROUP BY T1.Name ORDER BY COUNT(*) LIMIT 1
```

## AL0175

Question: What is the produdction code and channel of the most recent cartoon?

Database: `tvshow`

```sql
SELECT Production_code, Channel
FROM Cartoon
ORDER BY Original_air_date DESC
LIMIT 1
```

## AL0176

Question: Show the name and the release year of the song by the youngest singer.

Database: `concert_singer`

```sql
SELECT Song_Name, Song_release_year
FROM singer
ORDER BY Age ASC
LIMIT 1
```

## AL0177

Question: Return the name of AKO.

Database: `flight_2`

```sql
SELECT AirportName FROM airports WHERE AirportCode = 'AKO'
```

## AL0178

Question: List the dog name, age and weight of the dogs who have been abandoned?

Database: `dog_kennels`

```sql
SELECT name , age , weight FROM Dogs WHERE abandoned_yn = 1
```

## AL0179

Question: What are the names of the teachers who are either 32 or 33?

Database: `course_teach`

```sql
SELECT Name FROM teacher WHERE Age = 32 OR Age = 33
```

## AL0180

Question: Find the minimum grade of students who have no friends.

Database: `network_1`

```sql
SELECT min(grade) FROM Highschooler WHERE id NOT IN (SELECT student_id FROM Friend)
```

## AL0181

Question: What are the names of players who won in both 2013 and 2016?

Database: `wta_1`

```sql
SELECT winner_name
FROM matches
WHERE year = 2013
INTERSECT
SELECT winner_name
FROM matches
WHERE year = 2016
```

## AL0182

Question: List the Episode of all  TV series showed on TV Channel with  """"Sky Radio"""".

Database: `tvshow`

```sql
SELECT T1.Episode
FROM TV_series AS T1
INNER JOIN TV_Channel AS T2 ON T1.Channel = T2.id
WHERE T2.series_name = 'Sky Radio'
```

## AL0183

Question: What is the name of the player who has won the most matches, and how many rank points does this player have?

Database: `wta_1`

```sql
SELECT p.first_name, p.last_name, r.ranking_points
FROM matches m
JOIN players p ON m.winner_id = p.player_id
JOIN rankings r ON m.winner_id = r.player_id
GROUP BY m.winner_id, p.first_name, p.last_name, r.ranking_points
ORDER BY COUNT(m.winner_id) DESC
LIMIT 1
```

## AL0184

Question: Give the average life expectancy for countries in Africa which are republics?

Database: `world_1`

```sql
SELECT avg(LifeExpectancy) FROM country WHERE Region = "Africa" AND GovernmentForm = "Republic"
```

## AL0185

Question: Find the first name of the students who permanently live in Haiti or have the cell phone number 09700166582.

Database: `student_transcripts_tracking`

```sql
SELECT T1.first_name
FROM Students AS T1
INNER JOIN Addresses AS T2 ON T1.permanent_address_id = T2.address_id
WHERE T2.country = 'Haiti' OR T1.cell_mobile_number = '09700166582'
```

## AL0186

Question: Give the airport code and airport name corresonding to Anthony.

Database: `flight_2`

```sql
SELECT AirportCode , AirportName FROM AIRPORTS WHERE city = "Anthony"
```

## AL0187

Question: Return the number of flights departing from Aberdeen.

Database: `flight_2`

```sql
SELECT COUNT(*)
FROM flights
WHERE SourceAirport IN (
    SELECT AirportCode
    FROM airports
    WHERE City = 'Aberdeen'
)
```

## AL0188

Question: What is the money rank of the tallest poker player?

Database: `poker_player`

```sql
SELECT T2.Money_Rank FROM people AS T1 JOIN poker_player AS T2 ON T1.People_ID = T2.People_ID ORDER BY T1.Height DESC LIMIT 1
```

## AL0189

Question: What are the package options and the name of the series for the TV Channel that supports HDTV?

Database: `tvshow`

```sql
SELECT package_option , series_name FROM TV_Channel WHERE Hight_definition_TV = 'yes'
```

## AL0190

Question: How many republic countries are there?

Database: `world_1`

```sql
SELECT count(*) FROM country WHERE GovernmentForm = "Republic"
```

## AL0191

Question: How many dogs are raised by female students?

Database: `pets_1`

```sql
SELECT count(*) FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid = T2.stuid JOIN pets AS T3 ON T3.petid = T2.petid WHERE T1.sex = 'F' AND T3.pettype = 'dog'
```

## AL0192

Question: Give average earnings of poker players who are taller than 200.

Database: `poker_player`

```sql
SELECT AVG(T2.Earnings)
FROM people AS T1
INNER JOIN poker_player AS T2 ON T1.People_ID = T2.People_ID
WHERE T1.Height > 200
```

## AL0193

Question: How many flights depart from Aberdeen and arrive at Ashley?

Database: `flight_2`

```sql
SELECT COUNT(*) AS NumFlights
FROM flights f
JOIN airports src ON f.SourceAirport = src.AirportCode
JOIN airports dst ON f.DestAirport = dst.AirportCode
WHERE src.City = 'Aberdeen' AND dst.City = 'Ashley'
```

## AL0194

Question: What is the total number of people living in the nations that do not use English?

Database: `world_1`

```sql
SELECT sum(Population) FROM country WHERE Name NOT IN (SELECT T1.Name FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode WHERE T2.Language = "English")
```

## AL0195

Question: Find the number of cartoons by each of the listed directors.

Database: `tvshow`

```sql
SELECT count(*) , directed_by FROM cartoon GROUP BY directed_by
```

## AL0196

Question: List all singer names in concerts in  2014.

Database: `concert_singer`

```sql
SELECT DISTINCT T3.Name
FROM concert AS T1
INNER JOIN singer_in_concert AS T2 ON T1.concert_ID = T2.concert_ID
INNER JOIN singer AS T3 ON T2.Singer_ID = T3.Singer_ID
WHERE T1.Year = '2014'
```

## AL0197

Question: Which languages are spoken by only one republic country?

Database: `world_1`

```sql
SELECT T2.Language FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode WHERE T1.GovernmentForm = "Republic" GROUP BY T2.Language HAVING COUNT(*) = 1
```

## AL0198

Question: How many flights fly from Aberdeen to Ashley?

Database: `flight_2`

```sql
SELECT COUNT(*)
FROM flights f
JOIN airports src ON f.SourceAirport = src.AirportCode
JOIN airports dest ON f.DestAirport = dest.AirportCode
WHERE src.City = 'Aberdeen' AND dest.City = 'Ashley'
```

## AL0199

Question: What is the name and directors of all the cartoons that are ordered by the time they came out?

Database: `tvshow`

```sql
SELECT Title, Directed_by
FROM Cartoon
ORDER BY Original_air_date
```

## AL0200

Question: What is the msot common country for singer?

Database: `singer`

```sql
SELECT Citizenship
FROM singer
GROUP BY Citizenship
ORDER BY COUNT(Citizenship) DESC
LIMIT 1
```

## AL0201

Question: What are the first names of the students who live in Haiti permanently or have the cell phone number 09700166582?

Database: `student_transcripts_tracking`

```sql
SELECT T1.first_name
FROM Students AS T1
INNER JOIN Addresses AS T2 ON T1.permanent_address_id = T2.address_id
WHERE T2.country = 'Haiti' OR T1.cell_mobile_number = '09700166582'
```

## AL0202

Question: Which shop has the most employees? Give me the shop name.

Database: `employee_hire_evaluation`

```sql
SELECT T1.Name
FROM shop AS T1
INNER JOIN hiring AS T2 ON T1.Shop_ID = T2.Shop_ID
GROUP BY T1.Shop_ID
ORDER BY COUNT(T2.Employee_ID) DESC
LIMIT 1
```

## AL0203

Question: What are the ids of the TV channels that do not have any cartoons  Ben Jones directs?

Database: `tvshow`

```sql
SELECT id
FROM TV_Channel
WHERE id NOT IN (
    SELECT Channel
    FROM Cartoon
    WHERE Directed_by = 'Ben Jones'
)
```

## AL0204

Question: List all cartoon Ben Jones directs.

Database: `tvshow`

```sql
SELECT Title FROM Cartoon WHERE Directed_by = "Ben Jones"
```

## AL0205

Question: How many flights depart from Aberdeen and arrive at Ashley?

Database: `flight_2`

```sql
SELECT count(*) FROM FLIGHTS AS T1 JOIN AIRPORTS AS T2 ON T1.DestAirport = T2.AirportCode JOIN AIRPORTS AS T3 ON T1.SourceAirport = T3.AirportCode WHERE T2.City = "Ashley" AND T3.City = "Aberdeen"
```

## AL0206

Question: Which Asian countries have more people than any country in Africa?

Database: `world_1`

```sql
SELECT Name
FROM country
WHERE Continent = 'Asia'
  AND Population > (
    SELECT MIN(Population)
    FROM country
    WHERE Continent = 'Africa'
  )
```

## AL0207

Question: Give the airport code and airport name corresonding to Anthony.

Database: `flight_2`

```sql
SELECT AirportCode, AirportName
FROM airports
WHERE City = 'Anthony'
```

## AL0208

Question: Which continent speaks the most languages?

Database: `world_1`

```sql
SELECT T1.Continent FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode GROUP BY T1.Continent ORDER BY COUNT(*) DESC LIMIT 1
```

## AL0209

Question: Find the name of the employee who got the highest one time incentive.

Database: `employee_hire_evaluation`

```sql
SELECT t1.name FROM employee AS t1 JOIN evaluation AS t2 ON t1.Employee_ID = t2.Employee_ID ORDER BY t2.bonus DESC LIMIT 1
```

## AL0210

Question: What are the names of the dogs for which the owner spent more than 1000 for treatment?

Database: `dog_kennels`

```sql
SELECT T1.name
FROM Dogs AS T1
INNER JOIN Treatments AS T2 ON T1.dog_id = T2.dog_id
GROUP BY T1.dog_id, T1.name
HAVING SUM(T2.cost_of_treatment) > 1000
```

## AL0211

Question: Give the mean life expectancy of countries in which English is not officially spoken .

Database: `world_1`

```sql
SELECT AVG(LifeExpectancy)
FROM country
WHERE Code NOT IN (
    SELECT CountryCode
    FROM countrylanguage
    WHERE Language = 'English' AND IsOfficial = 'T'
)
```

## AL0212

Question: List the emails of the professionals who live in Hawaii or Wisconsin.

Database: `dog_kennels`

```sql
SELECT email_address
FROM Professionals
WHERE state IN ('Hawaii', 'Wisconsin')
```

## AL0213

Question: Find the weight of the youngest dog.

Database: `pets_1`

```sql
SELECT weight FROM pets ORDER BY pet_age LIMIT 1
```

## AL0214

Question: Find the cities that have more than one employee under  30 year old.

Database: `employee_hire_evaluation`

```sql
SELECT city FROM employee WHERE age < 30 GROUP BY city HAVING count(*) > 1
```

## AL0215

Question: What is the average miles per gallon(mpg) of the 4 CYL cars?

Database: `car_1`

```sql
SELECT AVG(CAST(MPG AS REAL)) AS AverageMPG
FROM cars_data
WHERE Cylinders = 4
```

## AL0216

Question: Which language is the most popular on Asian ?

Database: `world_1`

```sql
SELECT T2.Language FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode WHERE T1.Continent = "Asia" GROUP BY T2.Language ORDER BY SUM(T2.Percentage) DESC LIMIT 1
```

## AL0217

Question: What are the names of people who are not from Russia?

Database: `poker_player`

```sql
SELECT Name
FROM people
WHERE Nationality != 'Russia'
```

## AL0218

Question: What are the names of singers ordered by ascending wealth?

Database: `singer`

```sql
SELECT Name FROM singer ORDER BY Net_Worth_Millions ASC
```

## AL0219

Question: Please show the most common nationality of singers.

Database: `singer`

```sql
SELECT Citizenship
FROM singer
GROUP BY Citizenship
ORDER BY COUNT(Citizenship) DESC
LIMIT 1
```

## AL0220

Question: List the names of all cartoons in alphabetical order.

Database: `tvshow`

```sql
SELECT Title
FROM Cartoon
ORDER BY Title ASC
```

## AL0221

Question: Find the name and rank of the 3 youngest victors across all matches.

Database: `wta_1`

```sql
SELECT DISTINCT winner_name , winner_rank FROM matches ORDER BY winner_age LIMIT 3
```

## AL0222

Question: What are flight numbers of flights arriving at APG?

Database: `flight_2`

```sql
SELECT FlightNo FROM FLIGHTS WHERE DestAirport = "APG"
```

## AL0223

Question: Which countries larger than that of any country in Europe by land?

Database: `world_1`

```sql
SELECT Name FROM country WHERE SurfaceArea > (SELECT max(SurfaceArea) FROM country WHERE Region = "Europe")
```

## AL0224

Question: For the countries founded before 1930, what is the total number of distinct official languages?

Database: `world_1`

```sql
SELECT COUNT(DISTINCT T2.Language)
FROM country AS T1
INNER JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode
WHERE T1.IndepYear < 1930 AND T2.IsOfficial = 'T'
```

## AL0225

Question: find the id, name and age for people who visited some museums more than once.

Database: `museum_visit`

```sql
SELECT t1.id , t1.name , t1.age FROM visitor AS t1 JOIN visit AS t2 ON t1.id = t2.visitor_id GROUP BY t1.id HAVING count(*) > 1
```

## AL0226

Question: What are the ids and names of the battles that led to more than 10 people died.

Database: `battle_death`

```sql
SELECT T1.id, T1.name
FROM battle AS T1
INNER JOIN ship AS T2 ON T1.id = T2.lost_in_battle
INNER JOIN death AS T3 ON T2.id = T3.caused_by_ship_id
GROUP BY T1.id, T1.name
HAVING SUM(T3.killed) > 10
```

## AL0227

Question: What are the full names of all players, sorted by age?

Database: `wta_1`

```sql
SELECT first_name, last_name
FROM players
ORDER BY strftime('%Y', 'now') - strftime('%Y', birth_date)
```

## AL0228

Question: How many flights land in Aberdeen or Abilene?

Database: `flight_2`

```sql
SELECT count(*) FROM FLIGHTS AS T1 JOIN AIRPORTS AS T2 ON T1.DestAirport = T2.AirportCode WHERE T2.City = "Aberdeen" OR T2.City = "Abilene"
```

## AL0229

Question: How many dogs younger than average?

Database: `dog_kennels`

```sql
SELECT COUNT(*)
FROM Dogs
WHERE CAST(age AS INTEGER) < (SELECT AVG(CAST(age AS INTEGER)) FROM Dogs)
```

## AL0230

Question: What is the average age for all students who do not own any pets?

Database: `pets_1`

```sql
SELECT AVG(Age)
FROM Student
WHERE StuID NOT IN (SELECT StuID FROM Has_Pet)
```

## AL0231

Question: What is the name of the singer with the largest wealth?

Database: `singer`

```sql
SELECT Name
FROM singer
ORDER BY Net_Worth_Millions DESC
LIMIT 1
```

## AL0232

Question: What are the countries that have greater surface area than any country in Europe?

Database: `world_1`

```sql
SELECT Name FROM country WHERE SurfaceArea > (SELECT min(SurfaceArea) FROM country WHERE Region = "Europe")
```

## AL0233

Question: find the number of players for each nation.

Database: `wta_1`

```sql
SELECT country_code, COUNT(*) AS number_of_players
FROM players
GROUP BY country_code
```

## AL0234

Question: Which region is Kabul located in?

Database: `world_1`

```sql
SELECT T2.Region
FROM city AS T1
INNER JOIN country AS T2 ON T1.CountryCode = T2.Code
WHERE T1.Name = 'Kabul'
```

## AL0235

Question: How many flights depart from Aberdeen?

Database: `flight_2`

```sql
SELECT COUNT(*)
FROM flights f
JOIN airports a ON f.SourceAirport = a.AirportCode
WHERE a.City = 'Aberdeen'
```

## AL0236

Question: What are airlines that have flights arriving at AHD?

Database: `flight_2`

```sql
SELECT T1.Airline FROM AIRLINES AS T1 JOIN FLIGHTS AS T2 ON T1.uid = T2.Airline WHERE T2.DestAirport = "AHD"
```

## AL0237

Question: What is the name of the player who has won the most matches, and how many rank points does this player have?

Database: `wta_1`

```sql
SELECT T1.first_name , T1.last_name , T2.ranking_points FROM players AS T1 JOIN rankings AS T2 ON T1.player_id = T2.player_id JOIN matches AS T3 ON T1.player_id = T3.winner_id GROUP BY T1.player_id ORDER BY count(*) DESC LIMIT 1
```

## AL0238

Question: Count the number of United Airlines flights arriving in ASY.

Database: `flight_2`

```sql
SELECT count(*) FROM FLIGHTS AS T1 JOIN AIRLINES AS T2 ON T1.Airline = T2.uid WHERE T1.DestAirport = "ASY" AND T2.Airline = "United Airlines"
```

## AL0239

Question: List the emails of the professionals who live in Hawaii or Wisconsin.

Database: `dog_kennels`

```sql
SELECT email_address FROM professionals WHERE state = 'Hawaii' OR state = 'Wisconsin'
```

## AL0240

Question: Find the districts in which there are both shops selling less than 3000 and more than 10000 merchandise.

Database: `employee_hire_evaluation`

```sql
SELECT District
FROM shop
WHERE Number_products < 3000
INTERSECT
SELECT District
FROM shop
WHERE Number_products > 10000
```

## AL0241

Question: What are the different models for the cards produced after 1980?

Database: `car_1`

```sql
SELECT DISTINCT T1.Model FROM CAR_NAMES AS T1 JOIN CARS_DATA AS T2 ON T1.MakeId = T2.Id WHERE T2.Year > 1980
```

## AL0242

Question: What are the ids and names of all countries that either have more than 3 car makers or produce fiats?

Database: `car_1`

```sql
SELECT CountryId, CountryName
FROM countries
WHERE CountryId IN (
    SELECT Country
    FROM car_makers
    GROUP BY Country
    HAVING COUNT(*) > 3
)
OR CountryId IN (
    SELECT Country
    FROM car_makers
    WHERE Maker = 'fiat'
)
```

## AL0243

Question: Find the id, last name and cell phone of the professionals who live in Indiana or have performed more than two treatments.

Database: `dog_kennels`

```sql
SELECT T1.professional_id, T1.last_name, T1.cell_number
FROM Professionals T1
LEFT JOIN Treatments T2 ON T1.professional_id = T2.professional_id
GROUP BY T1.professional_id, T1.last_name, T1.cell_number
HAVING T1.state = 'Indiana' OR COUNT(T2.treatment_id) > 2
```

## AL0244

Question: What are the names of the teachers who are either 32 or 33?

Database: `course_teach`

```sql
SELECT Name
FROM teacher
WHERE Age IN ('32', '33')
```

## AL0245

Question: What is the car wmodel that is the most fuel efficient?

Database: `car_1`

```sql
SELECT T2.Model
FROM cars_data AS T1
INNER JOIN car_names AS T2 ON T1.Id = T2.MakeId
ORDER BY CAST(T1.MPG AS REAL) DESC
LIMIT 1
```

## AL0246

Question: How many friends does Kyle have?

Database: `network_1`

```sql
SELECT count(*) FROM Friend AS T1 JOIN Highschooler AS T2 ON T1.student_id = T2.id WHERE T2.name = "Kyle"
```

## AL0247

Question: Find the number of pets that is heavier than 10.

Database: `pets_1`

```sql
SELECT count(*) FROM pets WHERE weight > 10
```

## AL0248

Question: Return the different names of cities that are in Asia and for which Chinese is used officially .

Database: `world_1`

```sql
SELECT DISTINCT T1.Name
FROM city AS T1
INNER JOIN country AS T2 ON T1.CountryCode = T2.Code
INNER JOIN countrylanguage AS T3 ON T2.Code = T3.CountryCode
WHERE T2.Continent = 'Asia'
  AND T3.Language = 'Chinese'
  AND T3.IsOfficial = 'T'
```

## AL0249

Question: What is the series name of the TV Channel that shows ""The Rise of the Blue Beetle""?

Database: `tvshow`

```sql
SELECT T1.series_name FROM TV_Channel AS T1 JOIN cartoon AS T2 ON T1.id = T2.Channel WHERE T2.Title = "The Rise of the Blue Beetle!"
```

## AL0250

Question: What are the names of all European countries with at least 3 manufacturers?

Database: `car_1`

```sql
SELECT T1.CountryName FROM COUNTRIES AS T1 JOIN CAR_MAKERS AS T2 ON T1.CountryId = T2.Country GROUP BY T1.CountryName HAVING count(*) >= 3
```

## AL0251

Question: What are the country code and first name of the players who won in both WTA Championships and Australian Open?

Database: `wta_1`

```sql
SELECT T1.country_code , T1.first_name FROM players AS T1 JOIN matches AS T2 ON T1.player_id = T2.winner_id WHERE T2.tourney_name = 'WTA Championships' INTERSECT SELECT T1.country_code , T1.first_name FROM players AS T1 JOIN matches AS T2 ON T1.player_id = T2.winner_id WHERE T2.tourney_name = 'Australian Open'
```

## AL0252

Question: How many concerts occurred in 2014 or 2015?

Database: `concert_singer`

```sql
SELECT COUNT(*) FROM concert WHERE Year IN ('2014', '2015')
```

## AL0253

Question: What are the locations and names of all stations that can accommodate between 5000 and 10000 fans?

Database: `concert_singer`

```sql
SELECT Location, Name
FROM stadium
WHERE Capacity BETWEEN 5000 AND 10000
```

## AL0254

Question: Which model saves the most gasoline?

Database: `car_1`

```sql
SELECT T1.Model FROM CAR_NAMES AS T1 JOIN CARS_DATA AS T2 ON T1.MakeId = T2.Id ORDER BY T2.MPG DESC LIMIT 1
```

## AL0255

Question: What is the average GNP and total population in all US territory nations?

Database: `world_1`

```sql
SELECT avg(GNP) , sum(population) FROM country WHERE GovernmentForm = "US Territory"
```

## AL0256

Question: What is average life expectancy in the countries where English is not used officially ?

Database: `world_1`

```sql
SELECT AVG(T1.LifeExpectancy)
FROM country AS T1
INNER JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode
WHERE T2.Language = 'English' AND T2.IsOfficial = 'F'
```

## AL0257

Question: List the names of all winners who played in both 2013 and 2016.

Database: `wta_1`

```sql
SELECT winner_name FROM matches WHERE YEAR = 2013 INTERSECT SELECT winner_name FROM matches WHERE YEAR = 2016
```

## AL0258

Question: Which airlines have a flight to  AHD?

Database: `flight_2`

```sql
SELECT T1.Airline
FROM airlines AS T1
INNER JOIN flights AS T2 ON T1.uid = T2.Airline
WHERE T2.DestAirport = 'AHD'
```

## AL0259

Question: List the area codes in which voters voted both for 'Tabatha Gehling' and 'Kelly Clauss'.

Database: `voter_1`

```sql
SELECT T1.area_code
FROM AREA_CODE_STATE T1
INNER JOIN VOTES T2 ON T1.state = T2.state
INNER JOIN CONTESTANTS T3 ON T2.contestant_number = T3.contestant_number
WHERE T3.contestant_name IN ('Tabatha Gehling', 'Kelly Clauss')
GROUP BY T1.area_code
HAVING COUNT(DISTINCT T3.contestant_name) = 2
```

## AL0260

Question: What is the weekly rank for the  """"A Love of a Lifetime""""?

Database: `tvshow`

```sql
SELECT Weekly_Rank FROM TV_series WHERE Episode = "A Love of a Lifetime"
```

## AL0261

Question: List the first name and birth date of all players from USA.

Database: `wta_1`

```sql
SELECT first_name , birth_date FROM players WHERE country_code = 'USA'
```

## AL0262

Question: Which district has both stores with less than 3000 goods and stores with more than 10000 goods?

Database: `employee_hire_evaluation`

```sql
SELECT district FROM shop WHERE number_products < 3000 INTERSECT SELECT district FROM shop WHERE number_products > 10000
```

## AL0263

Question: What are the names of the singers who are not French?

Database: `singer`

```sql
SELECT Name
FROM singer
WHERE Citizenship != 'France'
```

## AL0264

Question: What are the names of all the countries that founded after 1950?

Database: `world_1`

```sql
SELECT Name FROM country WHERE IndepYear > 1950
```

## AL0265

Question: What grade is Kyle in?

Database: `network_1`

```sql
SELECT grade FROM Highschooler WHERE name = "Kyle"
```

## AL0266

Question: What is last date created of votes from 'CA'?

Database: `voter_1`

```sql
SELECT MAX(created) FROM VOTES WHERE state = 'CA'
```

## AL0267

Question: List the name and date the battle that has lost  Lettice and HMS Atalanta

Database: `battle_death`

```sql
SELECT T1.name , T1.date FROM battle AS T1 JOIN ship AS T2 ON T1.id = T2.lost_in_battle WHERE T2.name = 'Lettice' INTERSECT SELECT T1.name , T1.date FROM battle AS T1 JOIN ship AS T2 ON T1.id = T2.lost_in_battle WHERE T2.name = 'HMS Atalanta'
```

## AL0268

Question: What is the zip code of the address in Port Chelsea?

Database: `student_transcripts_tracking`

```sql
SELECT zip_postcode
FROM Addresses
WHERE city = 'Port Chelsea'
```

## AL0269

Question: Show names for all stadiums except for stadiums having a concert in  2014.

Database: `concert_singer`

```sql
SELECT name FROM stadium EXCEPT SELECT T2.name FROM concert AS T1 JOIN stadium AS T2 ON T1.stadium_id = T2.stadium_id WHERE T1.year = 2014
```

## AL0270

Question: Count the number of countries in Asia.

Database: `world_1`

```sql
SELECT COUNT(*) FROM country WHERE Continent = 'Asia'
```

## AL0271

Question: What are the names of nations speak both English and French?

Database: `world_1`

```sql
SELECT T1.Name FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode WHERE T2.Language = "English" INTERSECT SELECT T1.Name FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode WHERE T2.Language = "French"
```

## AL0272

Question: What are the names and ids of all nations with at least one car maker?

Database: `car_1`

```sql
SELECT T2.CountryName , T1.Country FROM CAR_MAKERS AS T1 JOIN COUNTRIES AS T2 ON T1.Country = T2.CountryId GROUP BY T1.Country
```

## AL0273

Question: List the name of teachers who are not from Little Lever Urban District.

Database: `course_teach`

```sql
SELECT Name
FROM teacher
WHERE Hometown != 'Little Lever Urban District'
```

## AL0274

Question: What is the name of the different car makers who produced a car in 1970?

Database: `car_1`

```sql
SELECT DISTINCT T1.FullName FROM CAR_MAKERS AS T1 JOIN MODEL_LIST AS T2 ON T1.Id = T2.Maker JOIN CAR_NAMES AS T3 ON T2.Model = T3.Model JOIN CARS_DATA AS T4 ON T3.MakeId = T4.Id WHERE T4.Year = 1970
```

## AL0275

Question: What are the different models wthat are lighter than 3500 but were not built by the Ford Motor Company?

Database: `car_1`

```sql
SELECT DISTINCT T1.Model FROM CAR_NAMES AS T1 JOIN CARS_DATA AS T2 ON T1.MakeId = T2.Id JOIN MODEL_LIST AS T3 ON T1.Model = T3.Model JOIN CAR_MAKERS AS T4 ON T3.Maker = T4.Id WHERE T2.Weight < 3500 AND T4.FullName != 'Ford Motor Company'
```

## AL0276

Question: Which country does ""JetBlue Airways"" belong to?

Database: `flight_2`

```sql
SELECT Country FROM AIRLINES WHERE Airline = "JetBlue Airways"
```

## AL0277

Question: What are the full names of all left handed players, in order of age?

Database: `wta_1`

```sql
SELECT first_name , last_name FROM players WHERE hand = 'L' ORDER BY birth_date
```

## AL0278

Question: Which cities are in European countries where English is not spoken officially?

Database: `world_1`

```sql
SELECT T1.Name
FROM city AS T1
INNER JOIN country AS T2 ON T1.CountryCode = T2.Code
WHERE T2.Continent = 'Europe'
  AND T2.Code NOT IN (
    SELECT CountryCode
    FROM countrylanguage
    WHERE Language = 'English' AND IsOfficial = 'T'
  )
```

## AL0279

Question: What is the official language used in the country the name of whose chief of state is Beatrix.

Database: `world_1`

```sql
SELECT T2.Language FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode WHERE T1.HeadOfState = "Beatrix" AND T2.IsOfficial = "T"
```

## AL0280

Question: What are the id and name of the museum that has people come most times?

Database: `museum_visit`

```sql
SELECT T1.Museum_ID, T1.Name
FROM museum AS T1
INNER JOIN visit AS T2 ON T1.Museum_ID = T2.Museum_ID
GROUP BY T1.Museum_ID, T1.Name
ORDER BY COUNT(T2.visitor_ID) DESC
LIMIT 1
```

## AL0281

Question: find the number of players for each nation.

Database: `wta_1`

```sql
SELECT count(*) , country_code FROM players GROUP BY country_code
```

## AL0282

Question: Return the money rank of the tallest poker player.

Database: `poker_player`

```sql
SELECT T2.Money_Rank FROM people AS T1 JOIN poker_player AS T2 ON T1.People_ID = T2.People_ID ORDER BY T1.Height DESC LIMIT 1
```

## AL0283

Question: Sort employee names from youngest to oldest.

Database: `employee_hire_evaluation`

```sql
SELECT Name
FROM employee
ORDER BY Age ASC
```

## AL0284

Question: Who is the earliest graduate of the school? List the first name, middle name and last name.

Database: `student_transcripts_tracking`

```sql
SELECT T1.first_name , T1.middle_name , T1.last_name FROM Students AS T1 JOIN Transcripts AS T2 ON T1.student_id = T2.transcript_id ORDER BY T2.transcript_date LIMIT 1
```

## AL0285

Question: What are the names of nations use both English and French officially?

Database: `world_1`

```sql
SELECT T1.Name
FROM country T1
INNER JOIN countrylanguage T2 ON T1.Code = T2.CountryCode AND T2.Language = 'English' AND T2.IsOfficial = 'T'
INNER JOIN countrylanguage T3 ON T1.Code = T3.CountryCode AND T3.Language = 'French' AND T3.IsOfficial = 'T'
```

## AL0286

Question: What are the ids of the TV channels that do not have any cartoons  Ben Jones directs?

Database: `tvshow`

```sql
SELECT id FROM TV_Channel EXCEPT SELECT channel FROM cartoon WHERE directed_by = 'Ben Jones'
```

## AL0287

Question: Which continent is Anguilla in?

Database: `world_1`

```sql
SELECT Continent FROM country WHERE Name = 'Anguilla'
```

## AL0288

Question: What are the names and locations of the stadiums that had concerts that occurred in both 2014 and 2015?

Database: `concert_singer`

```sql
SELECT T2.name , T2.location FROM concert AS T1 JOIN stadium AS T2 ON T1.stadium_id = T2.stadium_id WHERE T1.year = 2014 INTERSECT SELECT T2.name , T2.location FROM concert AS T1 JOIN stadium AS T2 ON T1.stadium_id = T2.stadium_id WHERE T1.year = 2015
```

## AL0289

Question: Find number of pets owned by students who are older than 20.

Database: `pets_1`

```sql
SELECT COUNT(HP.PetID)
FROM Student S
INNER JOIN Has_Pet HP ON S.StuID = HP.StuID
WHERE S.Age > 20
```

## AL0290

Question: What is the id and weight of every pet who is over 1 year old?

Database: `pets_1`

```sql
SELECT petid , weight FROM pets WHERE pet_age > 1
```

## AL0291

Question: What is the most populace city that speaks English?

Database: `world_1`

```sql
SELECT T1.Name , T1.Population FROM city AS T1 JOIN countrylanguage AS T2 ON T1.CountryCode = T2.CountryCode WHERE T2.Language = "English" ORDER BY T1.Population DESC LIMIT 1
```

## AL0292

Question: How many singers are from each nation?

Database: `concert_singer`

```sql
SELECT country , count(*) FROM singer GROUP BY country
```

## AL0293

Question: Show names for all stadiums except for stadiums having a concert in  2014.

Database: `concert_singer`

```sql
SELECT Name
FROM stadium
WHERE Stadium_ID NOT IN (
    SELECT Stadium_ID
    FROM concert
    WHERE Year = '2014'
)
```

## AL0294

Question: What are the names of the teachers  from youngest to oldest?

Database: `course_teach`

```sql
SELECT Name
FROM teacher
ORDER BY CAST(Age AS INTEGER) ASC
```

## AL0295

Question: Give me the description of the treatment type that is least expensive.

Database: `dog_kennels`

```sql
SELECT T1.treatment_type_description
FROM Treatment_Types AS T1
INNER JOIN Treatments AS T2 ON T1.treatment_type_code = T2.treatment_type_code
ORDER BY T2.cost_of_treatment ASC
LIMIT 1
```

## AL0296

Question: Show location and name for all stadiums that can fit between 5000 and 10000 people.

Database: `concert_singer`

```sql
SELECT Location, Name
FROM stadium
WHERE Capacity BETWEEN 5000 AND 10000
```

## AL0297

Question: how many countries are in Asia?

Database: `world_1`

```sql
SELECT count(*) FROM country WHERE continent = "Asia"
```

## AL0298

Question: What is name of the nation that speaks the largest number of languages?

Database: `world_1`

```sql
SELECT T1.Name
FROM country AS T1
INNER JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode
GROUP BY T1.Name
ORDER BY COUNT(T2.Language) DESC
LIMIT 1
```

## AL0299

Question: Sort employee names from youngest to oldest.

Database: `employee_hire_evaluation`

```sql
SELECT name FROM employee ORDER BY age ASC
```

## AL0300

Question: What is the average, minimum, and maximum age for all French singers?

Database: `concert_singer`

```sql
SELECT avg(age) , min(age) , max(age) FROM singer WHERE country = 'France'
```

## AL0301

Question: What is the pixel aspect ratio and country of origin for all TV channels that do not use English?

Database: `tvshow`

```sql
SELECT pixel_aspect_ratio_PAR , country FROM tv_channel WHERE LANGUAGE != 'English'
```

## AL0302

Question: Find the codes of nations that have more than 50 players.

Database: `wta_1`

```sql
SELECT country_code FROM players GROUP BY country_code HAVING count(*) > 50
```

## AL0303

Question: How many concerts are there in  2014 or 2015?

Database: `concert_singer`

```sql
SELECT count(*) FROM concert WHERE YEAR = 2014 OR YEAR = 2015
```

## AL0304

Question: How many people are there of each country?

Database: `poker_player`

```sql
SELECT Nationality, COUNT(*) FROM people GROUP BY Nationality
```

## AL0305

Question: which countries' tv channels are playing some cartoon  Todd Casey writes?

Database: `tvshow`

```sql
SELECT T1.country FROM tv_channel AS T1 JOIN cartoon AS T2 ON T1.id = T2.Channel WHERE T2.written_by = 'Todd Casey'
```

## AL0306

Question: Find all airlines that have flights from both APG and CVO.

Database: `flight_2`

```sql
SELECT T1.Airline FROM AIRLINES AS T1 JOIN FLIGHTS AS T2 ON T1.uid = T2.Airline WHERE T2.SourceAirport = "APG" INTERSECT SELECT T1.Airline FROM AIRLINES AS T1 JOIN FLIGHTS AS T2 ON T1.uid = T2.Airline WHERE T2.SourceAirport = "CVO"
```

## AL0307

Question: What are flight numbers of ""United Airlines""?

Database: `flight_2`

```sql
SELECT T1.FlightNo FROM FLIGHTS AS T1 JOIN AIRLINES AS T2 ON T1.Airline = T2.uid WHERE T2.Airline = "United Airlines"
```

## AL0308

Question: Which region is Kabul located in?

Database: `world_1`

```sql
SELECT T1.Region FROM country AS T1 JOIN city AS T2 ON T1.Code = T2.CountryCode WHERE T2.Name = "Kabul"
```

## AL0309

Question: Which continent is Anguilla in?

Database: `world_1`

```sql
SELECT Continent FROM country WHERE Name = "Anguilla"
```

## AL0310

Question: What are airport names at Aberdeen?

Database: `flight_2`

```sql
SELECT AirportName FROM AIRPORTS WHERE City = "Aberdeen"
```

## AL0311

Question: What is the average grade of students who have friends?

Database: `network_1`

```sql
SELECT AVG(T1.grade)
FROM Highschooler AS T1
WHERE T1.ID IN (SELECT student_id FROM Friend)
```

## AL0312

Question: How many official languages does Afghanistan have?

Database: `world_1`

```sql
SELECT COUNT(*) FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode WHERE T1.Name = "Afghanistan" AND IsOfficial = "T"
```

## AL0313

Question: Return the country codes for countries that do not speak English.

Database: `world_1`

```sql
SELECT Code FROM country EXCEPT SELECT CountryCode FROM countrylanguage WHERE LANGUAGE = "English"
```

## AL0314

Question: Find the number of cities in each district who have more people than average?

Database: `world_1`

```sql
SELECT District, COUNT(*) AS NumberOfCities
FROM city
WHERE Population > (SELECT AVG(Population) FROM city)
GROUP BY District
```

## AL0315

Question: What is the name of the shop that is recruiting the largest number of employees?

Database: `employee_hire_evaluation`

```sql
SELECT t1.name FROM shop AS t1 JOIN hiring AS t2 ON t1.shop_id = t2.shop_id GROUP BY t1.shop_id ORDER BY count(*) DESC LIMIT 1
```

## AL0316

Question: What is the first, middle, and last name of the earliest school graduate?

Database: `student_transcripts_tracking`

```sql
SELECT T1.first_name , T1.middle_name , T1.last_name FROM Students AS T1 JOIN Student_Enrolment AS T2 ON T1.student_id = T2.student_id JOIN Transcripts AS T3 ON T2.student_enrolment_id = T3.transcript_id ORDER BY T3.transcript_date LIMIT 1
```

## AL0317

Question: Which airlines have a flight to  AHD?

Database: `flight_2`

```sql
SELECT T1.Airline FROM AIRLINES AS T1 JOIN FLIGHTS AS T2 ON T1.uid = T2.Airline WHERE T2.DestAirport = "AHD"
```

## AL0318

Question: Return the different names of cities that are in Asia and for which Chinese is used officially .

Database: `world_1`

```sql
SELECT DISTINCT T1.Name FROM city AS T1 JOIN country AS T2 ON T1.CountryCode = T2.Code JOIN countrylanguage AS T3 ON T3.CountryCode = T2.Code WHERE T2.Continent = "Asia" AND T3.IsOfficial = "T" AND T3.Language = "Chinese"
```

## AL0319

Question: List all airline names and their abbreviations in ""USA"".

Database: `flight_2`

```sql
SELECT Airline, Abbreviation
FROM airlines
WHERE Country = 'USA'
```

## AL0320

Question: List the names of employees and sort from youngest to oldest

Database: `employee_hire_evaluation`

```sql
SELECT Name
FROM employee
ORDER BY Age ASC
```

## AL0321

Question: What is the total surface area of Asia and Europe?

Database: `world_1`

```sql
SELECT SUM(SurfaceArea) AS TotalSurfaceArea
FROM country
WHERE Continent IN ('Asia', 'Europe')
```

## AL0322

Question: Please show the most common nationality of singers.

Database: `singer`

```sql
SELECT Citizenship FROM singer GROUP BY Citizenship ORDER BY COUNT(*) DESC LIMIT 1
```

## AL0323

Question: Return the countries for which there are two or more people from.

Database: `poker_player`

```sql
SELECT Nationality FROM people GROUP BY Nationality HAVING COUNT(*) >= 2
```

## AL0324

Question: What are the citizenships that are shared by singers born  before 1945 and after 1955?

Database: `singer`

```sql
SELECT Citizenship FROM singer WHERE Birth_Year < 1945
INTERSECT
SELECT Citizenship FROM singer WHERE Birth_Year > 1955
```

## AL0325

Question: What is the average GNP and total population in all US territory nations?

Database: `world_1`

```sql
SELECT AVG(GNP), SUM(Population)
FROM country
WHERE Region = 'Caribbean'
```

## AL0326

Question: What is the number of car models created by American Motor Company?

Database: `car_1`

```sql
SELECT COUNT(T2.Model)
FROM car_makers AS T1
INNER JOIN model_list AS T2 ON T1.Id = T2.Maker
WHERE T1.FullName = 'American Motor Company'
```

## AL0327

Question: Find the package choice and series name of the TV channel that has HD TV.

Database: `tvshow`

```sql
SELECT Package_Option, series_name
FROM TV_Channel
WHERE Hight_definition_TV = 'yes'
```

## AL0328

Question: Return the names of cities that have between 160000 and 900000 people.

Database: `world_1`

```sql
SELECT Name FROM city WHERE population BETWEEN 160000 AND 900000
```

## AL0329

Question: What is Kyle's id?

Database: `network_1`

```sql
SELECT ID FROM Highschooler WHERE name = "Kyle"
```

## AL0330

Question: Return the names of non USA conductors.

Database: `orchestra`

```sql
SELECT Name FROM conductor WHERE Nationality != "USA"
```

## AL0331

Question: What is the money rank of the tallest poker player?

Database: `poker_player`

```sql
SELECT T2.Money_Rank
FROM people AS T1
INNER JOIN poker_player AS T2 ON T1.People_ID = T2.People_ID
ORDER BY T1.Height DESC
LIMIT 1
```

## AL0332

Question: Return the names of the 3 most populated countries.

Database: `world_1`

```sql
SELECT Name
FROM country
ORDER BY Population DESC
LIMIT 3
```

## AL0333

Question: What are  the different countries with singers  older than 20?

Database: `concert_singer`

```sql
SELECT DISTINCT Country
FROM singer
WHERE Age > 20
```

## AL0334

Question: What is the average age of the visitors not higher than lv 4?

Database: `museum_visit`

```sql
SELECT avg(age) FROM visitor WHERE level_of_membership <= 4
```

## AL0335

Question: Which cities are in European countries where English is not spoken officially?

Database: `world_1`

```sql
SELECT T1.Name FROM city AS T1 JOIN country AS T2 ON T1.CountryCode = T2.Code WHERE T2.Region = "Europe" AND T1.Name NOT IN (SELECT T1.Name FROM city AS T1 JOIN country AS T2 ON T1.CountryCode = T2.Code JOIN countrylanguage AS T3 ON T2.Code = T3.CountryCode WHERE T3.IsOfficial = "T" AND T3.Language = "English")
```

## AL0336

Question: What is the name and country of origin of every singer who has a song with the word 'Hey' in its title?

Database: `concert_singer`

```sql
SELECT Name, Country
FROM singer
WHERE Song_Name LIKE '%Hey%'
```

## AL0337

Question: Give me Brazil’s population and life expectancies.

Database: `world_1`

```sql
SELECT Population , LifeExpectancy FROM country WHERE Name = "Brazil"
```

## AL0338

Question: What are the countries that are not playing cartoons  Todd Casey writes?

Database: `tvshow`

```sql
SELECT country FROM TV_Channel EXCEPT SELECT T1.country FROM TV_Channel AS T1 JOIN cartoon AS T2 ON T1.id = T2.Channel WHERE T2.written_by = 'Todd Casey'
```

## AL0339

Question: Return the names and surface areas of the 5 largest countries.

Database: `world_1`

```sql
SELECT Name , SurfaceArea FROM country ORDER BY SurfaceArea DESC LIMIT 5
```

## AL0340

Question: Return the names of the 3 countries with the fewest people.

Database: `world_1`

```sql
SELECT Name
FROM country
ORDER BY Population ASC
LIMIT 3
```

## AL0341

Question: Return the number of likes Kyle has.

Database: `network_1`

```sql
SELECT COUNT(*)
FROM Likes
WHERE liked_id = (SELECT ID FROM Highschooler WHERE name = 'Kyle')
```

## AL0342

Question: Count the number of countries for which Spanish is predominantly spoken .

Database: `world_1`

```sql
SELECT count(*) FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode WHERE T2.Language = "Spanish" AND T2.Percentage > 50
```

## AL0343

Question: What is the pixel aspect ratio and country of origin for all TV channels that do not use English?

Database: `tvshow`

```sql
SELECT Pixel_aspect_ratio_PAR, Country
FROM TV_Channel
WHERE Language != 'English'
```

## AL0344

Question: How many visitors below  30 years old are there?

Database: `museum_visit`

```sql
SELECT count(*) FROM visitor WHERE age < 30
```

## AL0345

Question: Find the name and location of the stadiums which some concerts happened in both 2014 and 2015.

Database: `concert_singer`

```sql
SELECT DISTINCT s.Name, s.Location
FROM stadium s
JOIN concert c ON s.Stadium_ID = c.Stadium_ID
WHERE c.Year IN ('2014', '2015')
GROUP BY s.Name, s.Location
HAVING COUNT(DISTINCT c.Year) = 2
```

## AL0346

Question: Return the money rank of the tallest poker player.

Database: `poker_player`

```sql
SELECT T2.Money_Rank
FROM people AS T1
INNER JOIN poker_player AS T2 ON T1.People_ID = T2.People_ID
ORDER BY T1.Height DESC
LIMIT 1
```

## AL0347

Question: What is the mobile phone number of the student named Timmothy Ward ?

Database: `student_transcripts_tracking`

```sql
SELECT cell_mobile_number
FROM Students
WHERE first_name = 'Timmothy' AND last_name = 'Ward'
```

## AL0348

Question: How many cartoons Joseph Kuhr writes?

Database: `tvshow`

```sql
SELECT count(*) FROM cartoon WHERE written_by = 'Joseph Kuhr'
```

## AL0349

Question: Return the name of AKO.

Database: `flight_2`

```sql
SELECT AirportName FROM AIRPORTS WHERE AirportCode = "AKO"
```

## AL0350

Question: Show the name of singers who were born either 1948 or 1949?

Database: `singer`

```sql
SELECT Name
FROM singer
WHERE Birth_Year IN (1948, 1949)
```

## AL0351

Question: What are the names of the singers who born in either 1948 or 1949?

Database: `singer`

```sql
SELECT Name
FROM singer
WHERE Birth_Year IN (1948, 1949)
```

## AL0352

Question: Give the mean life expectancy of countries in which English is not officially spoken .

Database: `world_1`

```sql
SELECT avg(LifeExpectancy) FROM country WHERE Name NOT IN (SELECT T1.Name FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode WHERE T2.IsOfficial = 'T' AND T2.Language = "English")
```

## AL0353

Question: What is the smallest weight of the 8 CYL car produced on 1974 ?

Database: `car_1`

```sql
SELECT min(Weight) FROM CARS_DATA WHERE Cylinders = 8 AND YEAR = 1974
```

## AL0354

Question: How many flights does 'JetBlue Airways' have?

Database: `flight_2`

```sql
SELECT COUNT(*)
FROM flights
JOIN airlines ON flights.Airline = airlines.uid
WHERE airlines.Airline = 'JetBlue Airways'
```

## AL0355

Question: What is the name and country of origin of every singer who has a song with the word 'Hey' in its title?

Database: `concert_singer`

```sql
SELECT name , country FROM singer WHERE song_name LIKE '%Hey%'
```

## AL0356

Question: Give the flight numbers of flights landing at APG.

Database: `flight_2`

```sql
SELECT FlightNo
FROM flights
WHERE DestAirport = 'APG'
```

## AL0357

Question: Find the id and weight of all pets that is older than 1.

Database: `pets_1`

```sql
SELECT PetID, weight
FROM Pets
WHERE pet_age > 1
```

## AL0358

Question: What are the population and life expectancies in Brazil?

Database: `world_1`

```sql
SELECT Population , LifeExpectancy FROM country WHERE Name = "Brazil"
```

## AL0359

Question: What is the first name of every student who has a dog but does not have a cat?

Database: `pets_1`

```sql
SELECT DISTINCT T1.Fname FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid = T2.stuid JOIN pets AS T3 ON T3.petid = T2.petid WHERE T3.pettype = 'dog' EXCEPT SELECT DISTINCT T1.Fname FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid = T2.stuid JOIN pets AS T3 ON T3.petid = T2.petid WHERE T3.pettype = 'cat'
```

## AL0360

Question: Find the number of concerts happened in the stadium that can accommodate the most people.

Database: `concert_singer`

```sql
SELECT count(*) FROM concert WHERE stadium_id = (SELECT stadium_id FROM stadium ORDER BY capacity DESC LIMIT 1)
```

## AL0361

Question: Find the model of the car that is lighter than average .

Database: `car_1`

```sql
SELECT T1.Model
FROM car_names AS T1
INNER JOIN cars_data AS T2 ON T1.MakeId = T2.Id
WHERE T2.Weight < (SELECT AVG(Weight) FROM cars_data)
```

## AL0362

Question: What is the average age for all students who do not own any pets?

Database: `pets_1`

```sql
SELECT avg(age) FROM student WHERE stuid NOT IN (SELECT stuid FROM has_pet)
```

## AL0363

Question: Which flight numbers correspond to United Airlines flights?

Database: `flight_2`

```sql
SELECT T2.FlightNo
FROM airlines AS T1
INNER JOIN flights AS T2 ON T1.uid = T2.Airline
WHERE T1.Airline = 'United Airlines'
```

## AL0364

Question: What are the manager name and district of the shop that sells the most merchandise?

Database: `employee_hire_evaluation`

```sql
SELECT Manager_name, District
FROM shop
ORDER BY Number_products DESC
LIMIT 1
```

## AL0365

Question: Which place holds the most number of students currently? List the id and all lines.

Database: `student_transcripts_tracking`

```sql
SELECT T1.address_id, T1.line_1, T1.line_2, T1.line_3
FROM Addresses AS T1
INNER JOIN Students AS T2 ON T1.address_id = T2.current_address_id
GROUP BY T1.address_id
ORDER BY COUNT(T2.student_id) DESC
LIMIT 1
```

## AL0366

Question: Show the name and the release year of the song by the youngest singer.

Database: `concert_singer`

```sql
SELECT song_name , song_release_year FROM singer ORDER BY age LIMIT 1
```

## AL0367

Question: Show the ID of Kyle.

Database: `network_1`

```sql
SELECT ID FROM Highschooler WHERE name = "Kyle"
```

## AL0368

Question: Return the record companies of orchestras, sorted ascending by the time they have existed.

Database: `orchestra`

```sql
SELECT Record_Company
FROM orchestra
ORDER BY (strftime('%Y', 'now') - Year_of_Founded) ASC
```

## AL0369

Question: find the names of museums which have more staff than the minimum of all museums opened after 2010.

Database: `museum_visit`

```sql
SELECT Name
FROM museum
WHERE Num_of_Staff > (
    SELECT MIN(Num_of_Staff)
    FROM museum
    WHERE Open_Year > '2010'
)
```

## AL0370

Question: What is the air date of """"A Love of a Lifetime""""?

Database: `tvshow`

```sql
SELECT Air_Date FROM TV_series WHERE Episode = "A Love of a Lifetime"
```

## AL0371

Question: Count the number of friends Kyle has.

Database: `network_1`

```sql
SELECT COUNT(*)
FROM Friend
WHERE student_id = (
    SELECT ID
    FROM Highschooler
    WHERE name = 'Kyle'
)
```

## AL0372

Question: List all song names by singers older than average .

Database: `concert_singer`

```sql
SELECT song_name FROM singer WHERE age > (SELECT avg(age) FROM singer)
```

## AL0373

Question: Find the name of tournament that has more than 10 matches.

Database: `wta_1`

```sql
SELECT tourney_name FROM matches GROUP BY tourney_name HAVING count(*) > 10
```

## AL0374

Question: Give the flight numbers of flights leaving from Aberdeen.

Database: `flight_2`

```sql
SELECT T1.FlightNo
FROM flights AS T1
INNER JOIN airports AS T2 ON T1.SourceAirport = T2.AirportCode
WHERE T2.City = 'Aberdeen'
```

## AL0375

Question: Which continent speaks the most languages?

Database: `world_1`

```sql
SELECT T1.Continent
FROM country AS T1
INNER JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode
GROUP BY T1.Continent
ORDER BY COUNT(T2.Language) DESC
LIMIT 1
```

## AL0376

Question: What are the names of nations use both English and French officially?

Database: `world_1`

```sql
SELECT T1.Name FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode WHERE T2.Language = "English" AND T2.IsOfficial = "T" INTERSECT SELECT T1.Name FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode WHERE T2.Language = "French" AND T2.IsOfficial = "T"
```

## AL0377

Question: List the name of singers in ascending order of wealth.

Database: `singer`

```sql
SELECT Name FROM singer ORDER BY Net_Worth_Millions ASC
```

## AL0378

Question: Return the number of United Airlines flights leaving from AHD.

Database: `flight_2`

```sql
SELECT count(*) FROM FLIGHTS AS T1 JOIN AIRLINES AS T2 ON T1.Airline = T2.uid WHERE T1.SourceAirport = "AHD" AND T2.Airline = "United Airlines"
```

## AL0379

Question: Find the last name of the student who has a cat that is 3 years old.

Database: `pets_1`

```sql
SELECT T1.LName
FROM Student AS T1
INNER JOIN Has_Pet AS T2 ON T1.StuID = T2.StuID
INNER JOIN Pets AS T3 ON T2.PetID = T3.PetID
WHERE T3.PetType = 'cat' AND T3.pet_age = 3
```

## AL0380

Question: Give the names of countries that are in Europe and have 80000 people.

Database: `world_1`

```sql
SELECT Name
FROM country
WHERE Continent = 'Europe' AND Population = 80000
```

## AL0381

Question: What is the air date of """"A Love of a Lifetime""""?

Database: `tvshow`

```sql
SELECT Air_Date FROM TV_series WHERE Episode = 'A Love of a Lifetime'
```

## AL0382

Question: Return the names of the 3 countries with the fewest people.

Database: `world_1`

```sql
SELECT Name FROM country ORDER BY Population ASC LIMIT 3
```

## AL0383

Question: What are the names of the teachers whose courses have not been assigned?

Database: `course_teach`

```sql
SELECT Name FROM teacher WHERE Teacher_ID NOT IN (SELECT Teacher_ID FROM course_arrange)
```

## AL0384

Question: Count the number of United Airlines flights that arrive in Aberdeen.

Database: `flight_2`

```sql
SELECT COUNT(*)
FROM flights f
JOIN airlines a ON f.Airline = a.uid
JOIN airports ap ON f.DestAirport = ap.AirportCode
WHERE a.Airline = 'United Airlines' AND ap.City = 'Aberdeen'
```

## AL0385

Question: What is the full name of each car manufacturer, along with its id and how many models it produces?

Database: `car_1`

```sql
SELECT T1.FullName , T1.Id , count(*) FROM CAR_MAKERS AS T1 JOIN MODEL_LIST AS T2 ON T1.Id = T2.Maker GROUP BY T1.Id
```

## AL0386

Question: Find the average grade of all students who have some friends.

Database: `network_1`

```sql
SELECT avg(grade) FROM Highschooler WHERE id IN (SELECT student_id FROM Friend)
```

## AL0387

Question: Find the id, last name and cell phone of the professionals who live in Indiana or have performed more than two treatments.

Database: `dog_kennels`

```sql
SELECT professional_id , last_name , cell_number FROM professionals WHERE state = 'Indiana' UNION SELECT T1.professional_id , T2.last_name , T2.cell_number FROM Treatments AS T1 JOIN professionals AS T2 ON T1.professional_id = T2.professional_id GROUP BY T1.professional_id HAVING count(*) > 2
```

## AL0388

Question: Show the names of all of Kyle's friends.

Database: `network_1`

```sql
SELECT T3.name FROM Friend AS T1 JOIN Highschooler AS T2 ON T1.student_id = T2.id JOIN Highschooler AS T3 ON T1.friend_id = T3.id WHERE T2.name = "Kyle"
```

## AL0389

Question: For all of the 4 CYL cars, which model has the most horsepower?

Database: `car_1`

```sql
SELECT T1.Model FROM CAR_NAMES AS T1 JOIN CARS_DATA AS T2 ON T1.MakeId = T2.Id WHERE T2.Cylinders = 4 ORDER BY T2.horsepower DESC LIMIT 1
```

## AL0390

Question: What are the students' first names who have both cats and dogs?

Database: `pets_1`

```sql
SELECT T1.Fname FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid = T2.stuid JOIN pets AS T3 ON T3.petid = T2.petid WHERE T3.pettype = 'cat' INTERSECT SELECT T1.Fname FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid = T2.stuid JOIN pets AS T3 ON T3.petid = T2.petid WHERE T3.pettype = 'dog'
```

## AL0391

Question: What are the last name of the students who live in North Carolina but have not registered in any degree programs?

Database: `student_transcripts_tracking`

```sql
SELECT T1.last_name FROM Students AS T1 JOIN Addresses AS T2 ON T1.current_address_id = T2.address_id WHERE T2.state_province_county = 'North Carolina' EXCEPT SELECT T3.last_name FROM Students AS T3 JOIN Student_Enrolment AS T4 ON T3.student_id = T4.student_id
```

## AL0392

Question: How many dogs are raised by female students?

Database: `pets_1`

```sql
SELECT COUNT(*)
FROM Has_Pet hp
JOIN Pets p ON hp.PetID = p.PetID
JOIN Student s ON hp.StuID = s.StuID
WHERE p.PetType = 'dog' AND s.Sex = 'F'
```

## AL0393

Question: Who owns the youngest dog? Give me his or her last name.

Database: `dog_kennels`

```sql
SELECT T1.last_name FROM Owners AS T1 JOIN Dogs AS T2 ON T1.owner_id = T2.owner_id ORDER BY T2.date_of_birth DESC LIMIT 1
```

## AL0394

Question: What is the language spoken by the largest percentage of people in each nation?

Database: `world_1`

```sql
SELECT LANGUAGE , CountryCode , max(Percentage) FROM countrylanguage GROUP BY CountryCode
```

## AL0395

Question: Which cities do more than one employee younger than 30 come from?

Database: `employee_hire_evaluation`

```sql
SELECT City
FROM employee
WHERE Age < 30
GROUP BY City
HAVING COUNT(Employee_ID) > 1
```

## AL0396

Question: What are flight numbers of flights arriving at Aberdeen?

Database: `flight_2`

```sql
SELECT T1.FlightNo
FROM flights AS T1
INNER JOIN airports AS T2 ON T1.DestAirport = T2.AirportCode
WHERE T2.City = 'Aberdeen'
```

## AL0397

Question: What are the population, name and leader of the largest country by land?

Database: `world_1`

```sql
SELECT Name , population , HeadOfState FROM country ORDER BY SurfaceArea DESC LIMIT 1
```

## AL0398

Question: What is the full name of each car manufacturer, along with its id and how many models it produces?

Database: `car_1`

```sql
SELECT T1.FullName, T1.Id, COUNT(T2.Model) AS ModelCount
FROM car_makers AS T1
INNER JOIN model_list AS T2 ON T1.Id = T2.Maker
GROUP BY T1.Id, T1.FullName
```

## AL0399

Question: What is the total surface area of Asia and Europe?

Database: `world_1`

```sql
SELECT sum(SurfaceArea) FROM country WHERE Continent = "Asia" OR Continent = "Europe"
```

## AL0400

Question: What is Weekly Rank of TV series with A Love of a Lifetime?

Database: `tvshow`

```sql
SELECT Weekly_Rank FROM TV_series WHERE Episode = 'A Love of a Lifetime'
```

## AL0401

Question: Give the mean GNP and total population of nations which are considered US territory.

Database: `world_1`

```sql
SELECT avg(GNP) , sum(population) FROM country WHERE GovernmentForm = "US Territory"
```

## AL0402

Question: Show name, country, age for all singers from the oldest to the youngest.

Database: `concert_singer`

```sql
SELECT Name, Country, Age
FROM singer
ORDER BY Age DESC
```

## AL0403

Question: Find the major and age of students who do not have a cat.

Database: `pets_1`

```sql
SELECT Major, Age
FROM Student
WHERE StuID NOT IN (
    SELECT T1.StuID
    FROM Has_Pet AS T1
    INNER JOIN Pets AS T2 ON T1.PetID = T2.PetID
    WHERE T2.PetType = 'cat'
)
```

## AL0404

Question: What is the total number of unique official languages spoken in the countries that are founded before 1930?

Database: `world_1`

```sql
SELECT count(DISTINCT T2.Language) FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode WHERE T1.IndepYear < 1930 AND T2.IsOfficial = 'T'
```

## AL0405

Question: What is the accelerate of amc hornet sportabout (sw)?

Database: `car_1`

```sql
SELECT T2.Accelerate
FROM car_names AS T1
INNER JOIN cars_data AS T2 ON T1.MakeId = T2.Id
WHERE T1.Model = 'amc hornet sportabout (sw)'
```

## AL0406

Question: find id of the tv channels that from the nations where have more than two tv channels.

Database: `tvshow`

```sql
SELECT id FROM tv_channel GROUP BY country HAVING count(*) > 2
```

## AL0407

Question: How many high schoolers are there in  9 or 10?

Database: `network_1`

```sql
SELECT COUNT(*) FROM Highschooler WHERE grade = 9 OR grade = 10
```

## AL0408

Question: What are the last name of the students who live in North Carolina but have not registered in any degree programs?

Database: `student_transcripts_tracking`

```sql
SELECT T1.last_name
FROM Students AS T1
INNER JOIN Addresses AS T2 ON T1.current_address_id = T2.address_id
WHERE T2.state_province_county = 'North Carolina'
  AND T1.student_id NOT IN (SELECT student_id FROM Student_Enrolment)
```

## AL0409

Question: List the number of all matches who played in 2013 or 2016.

Database: `wta_1`

```sql
SELECT count(*) FROM matches WHERE YEAR = 2013 OR YEAR = 2016
```

## AL0410

Question: What are the codes of nations with more than 50 players?

Database: `wta_1`

```sql
SELECT country_code
FROM players
GROUP BY country_code
HAVING COUNT(player_id) > 50
```

## AL0411

Question: Show the citizenship shared by singers born  before 1945 and after 1955.

Database: `singer`

```sql
SELECT Citizenship FROM singer WHERE Birth_Year < 1945 INTERSECT SELECT Citizenship FROM singer WHERE Birth_Year > 1955
```

## AL0412

Question: What are the names and ids of all car companies with more than 3 models?

Database: `car_1`

```sql
SELECT T1.FullName , T1.Id FROM CAR_MAKERS AS T1 JOIN MODEL_LIST AS T2 ON T1.Id = T2.Maker GROUP BY T1.Id HAVING count(*) > 3
```

## AL0413

Question: What are the names of the teachers  from youngest to oldest?

Database: `course_teach`

```sql
SELECT Name
FROM teacher
ORDER BY Age ASC
```

## AL0414

Question: What are the names of all stadiums that did not have a concert in 2014?

Database: `concert_singer`

```sql
SELECT Name
FROM stadium
WHERE Stadium_ID NOT IN (
    SELECT Stadium_ID
    FROM concert
    WHERE Year = '2014'
)
```

## AL0415

Question: Find the number of shops in each place.

Database: `employee_hire_evaluation`

```sql
SELECT Location, COUNT(*) FROM shop GROUP BY Location
```

## AL0416

Question: Count the number of friends Kyle has.

Database: `network_1`

```sql
SELECT count(*) FROM Friend AS T1 JOIN Highschooler AS T2 ON T1.student_id = T2.id WHERE T2.name = "Kyle"
```

## AL0417

Question: What is the number of makers of care in France?

Database: `car_1`

```sql
SELECT COUNT(T1.Id)
FROM car_makers AS T1
INNER JOIN countries AS T2 ON T1.Country = T2.CountryId
WHERE T2.CountryName = 'france'
```

## AL0418

Question: list all cartoon titles and their directors ordered by the time they broadcasted

Database: `tvshow`

```sql
SELECT Title, Directed_by
FROM Cartoon
ORDER BY Original_air_date
```

## AL0419

Question: How many United Airlines flights go to 'Aberdeen'?

Database: `flight_2`

```sql
SELECT COUNT(*)
FROM flights f
JOIN airlines a ON f.Airline = a.uid
JOIN airports ap ON f.DestAirport = ap.AirportCode
WHERE a.Airline = 'United Airlines' AND ap.City = 'Aberdeen'
```

## AL0420

Question: How many cartoons did each director create?

Database: `tvshow`

```sql
SELECT count(*) , directed_by FROM cartoon GROUP BY directed_by
```

## AL0421

Question: Which airports do not have departing or arriving flights?

Database: `flight_2`

```sql
SELECT AirportCode
FROM airports
WHERE AirportCode NOT IN (
    SELECT SourceAirport FROM flights
    UNION
    SELECT DestAirport FROM flights
)
```

## AL0422

Question: How many pets are over 10 lbs?

Database: `pets_1`

```sql
SELECT count(*) FROM pets WHERE weight > 10
```

## AL0423

Question: Return the grade for Kyle.

Database: `network_1`

```sql
SELECT grade FROM Highschooler WHERE name = 'Kyle'
```

## AL0424

Question: Find the production code and channel of the most recently broadcasted cartoon.

Database: `tvshow`

```sql
SELECT Production_code, Channel
FROM Cartoon
ORDER BY Original_air_date DESC
LIMIT 1
```

## AL0425

Question: Find the name and rank points of the person who won the most times.

Database: `wta_1`

```sql
SELECT T1.first_name , T1.last_name , T2.winner_rank_points FROM players AS T1 JOIN matches AS T2 ON T1.player_id = T2.winner_id GROUP BY T1.player_id ORDER BY count(*) DESC LIMIT 1
```

## AL0426

Question: Which shops run with no employees? Find the shop names

Database: `employee_hire_evaluation`

```sql
SELECT name FROM shop WHERE shop_id NOT IN (SELECT shop_id FROM hiring)
```

## AL0427

Question: How many 'United Airlines' flights depart from 'AHD'?

Database: `flight_2`

```sql
SELECT count(*) FROM FLIGHTS AS T1 JOIN AIRLINES AS T2 ON T1.Airline = T2.uid WHERE T2.Airline = "United Airlines" AND T1.SourceAirport = "AHD"
```

## AL0428

Question: Find the names of the visitors that is higher than lv 4, and order the results by the level from high to low.

Database: `museum_visit`

```sql
SELECT Name
FROM visitor
WHERE Level_of_membership > 4
ORDER BY Level_of_membership DESC
```

## AL0429

Question: What are the names of conductors who are not from ""USA""?

Database: `orchestra`

```sql
SELECT Name
FROM conductor
WHERE Nationality != 'USA'
```

## AL0430

Question: Which models are lighter than 3500 but not built by the 'Ford Motor Company'?

Database: `car_1`

```sql
SELECT T1.Model
FROM car_names AS T1
INNER JOIN cars_data AS T2 ON T1.MakeId = T2.Id
INNER JOIN model_list AS T3 ON T1.Model = T3.Model
INNER JOIN car_makers AS T4 ON T3.Maker = T4.Id
WHERE T2.Weight < 3500
  AND T4.FullName != 'Ford Motor Company'
```

## AL0431

Question: What is the last name of the student who has a cat that is 3 years old?

Database: `pets_1`

```sql
SELECT T1.lname FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid = T2.stuid JOIN pets AS T3 ON T3.petid = T2.petid WHERE T3.pet_age = 3 AND T3.pettype = 'cat'
```

## AL0432

Question: What are the names of tournaments that have more than 10 matches?

Database: `wta_1`

```sql
SELECT tourney_name
FROM matches
GROUP BY tourney_name
HAVING COUNT(*) > 10
```

## AL0433

Question: Find the name and rank of the 3 youngest victors across all matches.

Database: `wta_1`

```sql
SELECT winner_name, winner_rank
FROM matches
ORDER BY winner_age ASC
LIMIT 3
```

## AL0434

Question: How many cartoons did each director create?

Database: `tvshow`

```sql
SELECT Directed_by, COUNT(*) FROM Cartoon GROUP BY Directed_by
```

## AL0435

Question: What are the names of the countries that are in Europe and have 80000 people?

Database: `world_1`

```sql
SELECT Name FROM country WHERE continent = "Europe" AND population > 80000
```

## AL0436

Question: Find the number of left handed winners who participated in the WTA Championships.

Database: `wta_1`

```sql
SELECT COUNT(*)
FROM matches
WHERE winner_hand = 'L'
  AND tourney_name = 'WTA Championships'
```

## AL0437

Question: Which employee received the biggest incentive? Give me the employee name.

Database: `employee_hire_evaluation`

```sql
SELECT e.Name
FROM employee e
INNER JOIN evaluation ev ON e.Employee_ID = ev.Employee_ID
ORDER BY ev.Bonus DESC
LIMIT 1
```

## AL0438

Question: Give me Brazil’s population and life expectancies.

Database: `world_1`

```sql
SELECT Population, LifeExpectancy
FROM country
WHERE Name = 'Brazil'
```

## AL0439

Question: Find the number of dogs that are raised by female students.

Database: `pets_1`

```sql
SELECT count(*) FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid = T2.stuid JOIN pets AS T3 ON T3.petid = T2.petid WHERE T1.sex = 'F' AND T3.pettype = 'dog'
```

## AL0440

Question: What are the country codes for countries that do not speak English?

Database: `world_1`

```sql
SELECT Code
FROM country
WHERE Code NOT IN (
    SELECT CountryCode
    FROM countrylanguage
    WHERE Language = 'English'
)
```

## AL0441

Question: List the name of singers whose  is not French.

Database: `singer`

```sql
SELECT Name FROM singer WHERE Citizenship != "France"
```

## AL0442

Question: find the code of the nation where has the greatest number of players.

Database: `wta_1`

```sql
SELECT country_code FROM players GROUP BY country_code ORDER BY count(*) DESC LIMIT 1
```

## AL0443

Question: For  volvo, how many cylinders does the car with the least accelerate have?

Database: `car_1`

```sql
SELECT T1.cylinders FROM CARS_DATA AS T1 JOIN CAR_NAMES AS T2 ON T1.Id = T2.MakeId JOIN MODEL_LIST AS T3 ON T2.Model = T3.Model JOIN CAR_MAKERS AS T4 ON T3.Maker = T4.Id WHERE T4.Maker = 'volvo' ORDER BY T1.accelerate ASC LIMIT 1
```

## AL0444

Question: What is the episode for the TV series called Sky Radio?

Database: `tvshow`

```sql
SELECT T1.Episode FROM TV_series AS T1 JOIN TV_Channel AS T2 ON T1.Channel = T2.id WHERE T2.series_name = "Sky Radio"
```

## AL0445

Question: What is the content of Sky Radio?

Database: `tvshow`

```sql
SELECT Content FROM TV_Channel WHERE series_name = "Sky Radio"
```

## AL0446

Question: how many countries are in Asia?

Database: `world_1`

```sql
SELECT COUNT(*) FROM country WHERE Continent = 'Asia'
```

## AL0447

Question: What are the package options of all tv channels that are not playing any cartoons  Ben Jones directs?

Database: `tvshow`

```sql
SELECT package_option FROM TV_Channel WHERE id NOT IN (SELECT channel FROM cartoon WHERE directed_by = 'Ben Jones')
```

## AL0448

Question: What are the create dates, states, and phone numbers of the votes that were for 'Tabatha Gehling'?

Database: `voter_1`

```sql
SELECT T2.created , T2.state , T2.phone_number FROM contestants AS T1 JOIN votes AS T2 ON T1.contestant_number = T2.contestant_number WHERE T1.contestant_name = 'Tabatha Gehling'
```

## AL0449

Question: How much does the youngest dog weigh?

Database: `pets_1`

```sql
SELECT weight
FROM Pets
WHERE PetType = 'dog'
ORDER BY pet_age ASC
LIMIT 1
```

## AL0450

Question: Give the name of the country in Asia with the lowest life expectancy.

Database: `world_1`

```sql
SELECT Name
FROM country
WHERE Continent = 'Asia'
ORDER BY LifeExpectancy ASC
LIMIT 1
```

## AL0451

Question: How many likes does Kyle have?

Database: `network_1`

```sql
SELECT count(*) FROM Likes AS T1 JOIN Highschooler AS T2 ON T1.student_id = T2.id WHERE T2.name = "Kyle"
```

## AL0452

Question: Find the semester when both Master students and Bachelor students got enrolled in.

Database: `student_transcripts_tracking`

```sql
SELECT T1.semester_name
FROM Semesters AS T1
INNER JOIN Student_Enrolment AS T2 ON T1.semester_id = T2.semester_id
INNER JOIN Degree_Programs AS T3 ON T2.degree_program_id = T3.degree_program_id
WHERE T3.degree_summary_name = 'Master'
INTERSECT
SELECT T1.semester_name
FROM Semesters AS T1
INNER JOIN Student_Enrolment AS T2 ON T1.semester_id = T2.semester_id
INNER JOIN Degree_Programs AS T3 ON T2.degree_program_id = T3.degree_program_id
WHERE T3.degree_summary_name = 'Bachelor'
```

## AL0453

Question: Find the number of dogs that are raised by female students.

Database: `pets_1`

```sql
SELECT COUNT(*)
FROM Student S
JOIN Has_Pet HP ON S.StuID = HP.StuID
JOIN Pets P ON HP.PetID = P.PetID
WHERE S.Sex = 'F' AND P.PetType = 'dog'
```

## AL0454

Question: List the names of conductors from youngest to oldest.

Database: `orchestra`

```sql
SELECT Name
FROM conductor
ORDER BY Age ASC
```

## AL0455

Question: What are the names of properties that are either houses or apartments with more than 1 room?

Database: `real_estate_properties`

```sql
SELECT property_name
FROM Properties
WHERE property_type_code IN ('House', 'Apartment')
  AND room_count > 1
```

## AL0456

Question: How many high schoolers are in each year?

Database: `network_1`

```sql
SELECT grade , count(*) FROM Highschooler GROUP BY grade
```

## AL0457

Question: How many matches were played in 2013 or 2016?

Database: `wta_1`

```sql
SELECT COUNT(*) FROM matches WHERE year = 2013 OR year = 2016
```

## AL0458

Question: Which nation has the most of TV Channels? List the country and number of TV Channels it has.

Database: `tvshow`

```sql
SELECT Country, COUNT(*) AS Number_of_TV_Channels
FROM TV_Channel
GROUP BY Country
ORDER BY Number_of_TV_Channels DESC
LIMIT 1
```

## AL0459

Question: How many people live in countries that do not speak English?

Database: `world_1`

```sql
SELECT SUM(T1.Population) AS TotalPopulation
FROM country AS T1
WHERE T1.Code NOT IN (
    SELECT CountryCode
    FROM countrylanguage
    WHERE Language = 'English'
)
```

## AL0460

Question: which countries' tv channels are not playing any cartoon  Todd Casey writes?

Database: `tvshow`

```sql
SELECT DISTINCT Country
FROM TV_Channel
WHERE id NOT IN (
    SELECT Channel
    FROM Cartoon
    WHERE Written_by = 'Todd Casey'
)
```

## AL0461

Question: How many airlines are from USA?

Database: `flight_2`

```sql
SELECT COUNT(*) FROM airlines WHERE Country = 'USA'
```

## AL0462

Question: Which continent has the most diverse languages?

Database: `world_1`

```sql
SELECT T1.Continent
FROM country AS T1
INNER JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode
GROUP BY T1.Continent
ORDER BY COUNT(T2.Language) DESC
LIMIT 1
```

## AL0463

Question: What are the id, name and membership level of people who have paid the largest amount of money overall in all museum tickets?

Database: `museum_visit`

```sql
SELECT t1.id , t1.name , t1.level_of_membership FROM visitor AS t1 JOIN visit AS t2 ON t1.id = t2.visitor_id GROUP BY t1.id ORDER BY sum(t2.total_spent) DESC LIMIT 1
```

## AL0464

Question: how many cars were produced in 1980?

Database: `car_1`

```sql
SELECT count(*) FROM CARS_DATA WHERE YEAR = 1980
```

## AL0465

Question: What are flight numbers of flights departing from Aberdeen?

Database: `flight_2`

```sql
SELECT T1.FlightNo
FROM flights AS T1
INNER JOIN airports AS T2 ON T1.SourceAirport = T2.AirportCode
WHERE T2.City = 'Aberdeen'
```

## AL0466

Question: What are the African countries that have less people than any country in Asia?

Database: `world_1`

```sql
SELECT Name
FROM country
WHERE Continent = 'Africa'
  AND Population < (
    SELECT MIN(Population)
    FROM country
    WHERE Continent = 'Asia'
  )
```

## AL0467

Question: Find the number of flights landing in Aberdeen or Abilene.

Database: `flight_2`

```sql
SELECT COUNT(*) AS NumberOfFlights
FROM flights f
JOIN airports a ON f.DestAirport = a.AirportCode
WHERE a.City IN ('Aberdeen', 'Abilene')
```

## AL0468

Question: What are the names of players who won in both 2013 and 2016?

Database: `wta_1`

```sql
SELECT winner_name FROM matches WHERE YEAR = 2013 INTERSECT SELECT winner_name FROM matches WHERE YEAR = 2016
```

## AL0469

Question: How many United Airlines flights go to 'Aberdeen'?

Database: `flight_2`

```sql
SELECT count(*) FROM FLIGHTS AS T1 JOIN AIRPORTS AS T2 ON T1.DestAirport = T2.AirportCode JOIN AIRLINES AS T3 ON T3.uid = T1.Airline WHERE T2.City = "Aberdeen" AND T3.Airline = "United Airlines"
```

## AL0470

Question: Find the minimum grade of students who have no friends.

Database: `network_1`

```sql
SELECT MIN(grade)
FROM Highschooler
WHERE ID NOT IN (SELECT student_id FROM Friend)
```

## AL0471

Question: What is the average, minimum, and maximum age for all French singers?

Database: `concert_singer`

```sql
SELECT AVG(Age), MIN(Age), MAX(Age)
FROM singer
WHERE Country = 'France'
```

## AL0472

Question: What are the names of properties that are either houses or apartments with more than 1 room?

Database: `real_estate_properties`

```sql
SELECT property_name FROM properties WHERE property_type_code = "House" UNION SELECT property_name FROM properties WHERE property_type_code = "Apartment" AND room_count > 1
```

## AL0473

Question: Find the type and weight of the youngest pet.

Database: `pets_1`

```sql
SELECT pettype , weight FROM pets ORDER BY pet_age LIMIT 1
```

## AL0474

Question: Which distinctive models are produced by General Motors or heavier than 3500?

Database: `car_1`

```sql
SELECT DISTINCT T1.Model
FROM car_names AS T1
INNER JOIN cars_data AS T2 ON T1.MakeId = T2.Id
INNER JOIN model_list AS T3 ON T1.Model = T3.Model
INNER JOIN car_makers AS T4 ON T3.Maker = T4.Id
WHERE T4.FullName = 'General Motors' OR T2.Weight > 3500
```

## AL0475

Question: What is the msot common country for singer?

Database: `singer`

```sql
SELECT Citizenship FROM singer GROUP BY Citizenship ORDER BY COUNT(*) DESC LIMIT 1
```

## AL0476

Question: List the dog name, age and weight of the dogs who have been abandoned?

Database: `dog_kennels`

```sql
SELECT name, age, weight
FROM Dogs
WHERE abandoned_yn = '1'
```

## AL0477

Question: Find the name of the makers that produced some cars in 1970?

Database: `car_1`

```sql
SELECT T1.FullName FROM CAR_MAKERS AS T1 JOIN MODEL_LIST AS T2 ON T1.Id = T2.Maker JOIN CAR_NAMES AS T3 ON T2.Model = T3.Model JOIN CARS_DATA AS T4 ON T3.MakeId = T4.Id WHERE T4.Year = 1970
```

## AL0478

Question: What is the code of the nation with the most players?

Database: `wta_1`

```sql
SELECT country_code
FROM players
GROUP BY country_code
ORDER BY COUNT(player_id) DESC
LIMIT 1
```

## AL0479

Question: What is the count of the car models produced in the United States?

Database: `car_1`

```sql
SELECT COUNT(T3.Model)
FROM car_makers AS T1
INNER JOIN countries AS T2 ON T1.Country = T2.CountryId
INNER JOIN model_list AS T3 ON T1.Id = T3.Maker
WHERE T2.CountryName = 'usa'
```

## AL0480

Question: What is the car wmodel that is the most fuel efficient?

Database: `car_1`

```sql
SELECT T1.Model FROM CAR_NAMES AS T1 JOIN CARS_DATA AS T2 ON T1.MakeId = T2.Id ORDER BY T2.MPG DESC LIMIT 1
```

## AL0481

Question: What is the Package Option of TV Channel with ""Sky Radio""?

Database: `tvshow`

```sql
SELECT Package_Option FROM TV_Channel WHERE series_name = "Sky Radio"
```

## AL0482

Question: What is the series name and country of all TV channels that are playing cartoons  Ben Jones and Michael Chang directs?

Database: `tvshow`

```sql
SELECT T1.series_name , T1.country FROM TV_Channel AS T1 JOIN cartoon AS T2 ON T1.id = T2.Channel WHERE T2.directed_by = "Ben Jones and Michael Chang"
```

## AL0483

Question: What is the first, middle, and last name of the earliest school graduate?

Database: `student_transcripts_tracking`

```sql
SELECT first_name, middle_name, last_name
FROM Students
ORDER BY date_left ASC
LIMIT 1
```

## AL0484

Question: How many people live in Gelderland ?

Database: `world_1`

```sql
SELECT SUM(Population) FROM city WHERE District = 'Gelderland'
```

## AL0485

Question: How much surface area do the countires in the Carribean cover together?

Database: `world_1`

```sql
SELECT sum(SurfaceArea) FROM country WHERE Region = "Caribbean"
```

## AL0486

Question: What is the name of the winner with the most rank points who participated in the Australian Open?

Database: `wta_1`

```sql
SELECT winner_name FROM matches WHERE tourney_name = 'Australian Open' ORDER BY winner_rank_points DESC LIMIT 1
```

## AL0487

Question: What is the language that is used by the largest number of Asian nations?

Database: `world_1`

```sql
SELECT T2.Language FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode WHERE T1.Continent = "Asia" GROUP BY T2.Language ORDER BY COUNT(*) DESC LIMIT 1
```

## AL0488

Question: How many likes does Kyle have?

Database: `network_1`

```sql
SELECT COUNT(*)
FROM Likes
JOIN Highschooler ON Highschooler.ID = Likes.liked_id
WHERE Highschooler.name = 'Kyle'
```

## AL0489

Question: What is the average earnings of poker players taller than 200?

Database: `poker_player`

```sql
SELECT avg(T1.Earnings) FROM poker_player AS T1 JOIN people AS T2 ON T1.People_ID = T2.People_ID WHERE T2.Height > 200
```

## AL0490

Question: How many car models are produced in the usa?

Database: `car_1`

```sql
SELECT count(*) FROM MODEL_LIST AS T1 JOIN CAR_MAKERS AS T2 ON T1.Maker = T2.Id JOIN COUNTRIES AS T3 ON T2.Country = T3.CountryId WHERE T3.CountryName = 'usa'
```

## AL0491

Question: What is the nation with the most number of TV Channels and how many does it have?

Database: `tvshow`

```sql
SELECT Country, COUNT(*) AS count
FROM TV_Channel
GROUP BY Country
ORDER BY count DESC
LIMIT 1
```

## AL0492

Question: What is the TV Channel with """"A Love of a Lifetime""""? List the TV Channel's series name.

Database: `tvshow`

```sql
SELECT T1.series_name FROM TV_Channel AS T1 JOIN TV_series AS T2 ON T1.id = T2.Channel WHERE T2.Episode = "A Love of a Lifetime"
```

## AL0493

Question: Whic`h unique cities are in  Asian countries where Chinese is the official ?

Database: `world_1`

```sql
SELECT DISTINCT T1.Name
FROM city AS T1
INNER JOIN country AS T2 ON T1.CountryCode = T2.Code
INNER JOIN countrylanguage AS T3 ON T2.Code = T3.CountryCode
WHERE T2.Continent = 'Asia'
  AND T3.Language = 'Chinese'
  AND T3.IsOfficial = 'T'
```

## AL0494

Question: What is the phone number of Timmothy Ward?

Database: `student_transcripts_tracking`

```sql
SELECT cell_mobile_number FROM Students WHERE first_name = 'Timmothy' AND last_name = 'Ward'
```

## AL0495

Question: Find the first name of the students who permanently live in Haiti or have the cell phone number 09700166582.

Database: `student_transcripts_tracking`

```sql
SELECT T2.first_name FROM addresses AS T1 JOIN students AS T2 ON T1.address_id = T2.permanent_address_id WHERE T1.country = 'Haiti' UNION SELECT first_name FROM students WHERE cell_mobile_number = '09700166582'
```

## AL0496

Question: Find the average number of staff working for the museums that were open before 2009.

Database: `museum_visit`

```sql
SELECT AVG(Num_of_Staff)
FROM museum
WHERE Open_Year < 2009
```

## AL0497

Question: Count the number of high schoolers in grades 9 or 10.

Database: `network_1`

```sql
SELECT COUNT(*) FROM Highschooler WHERE grade = 9 OR grade = 10
```

## AL0498

Question: What is the name for AKO?

Database: `flight_2`

```sql
SELECT AirportName FROM airports WHERE AirportCode = 'AKO'
```

## AL0499

Question: Which countries larger than that of any country in Europe by land?

Database: `world_1`

```sql
SELECT Name
FROM country
WHERE SurfaceArea > (
    SELECT MIN(SurfaceArea)
    FROM country
    WHERE Continent = 'Europe'
)
```

## AL0500

Question: What are the names of the nations with the 3 lowest number of citizens?

Database: `world_1`

```sql
SELECT Name
FROM country
ORDER BY Population ASC
LIMIT 3
```

## AL0501

Question: Return the number of likes Kyle has.

Database: `network_1`

```sql
SELECT count(*) FROM Likes AS T1 JOIN Highschooler AS T2 ON T1.student_id = T2.id WHERE T2.name = "Kyle"
```

## AL0502

Question: For the countries founded before 1930, what is the total number of distinct official languages?

Database: `world_1`

```sql
SELECT count(DISTINCT T2.Language) FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode WHERE T1.IndepYear < 1930 AND T2.IsOfficial = 'T'
```

## AL0503

Question: Show the names of all of Kyle's friends.

Database: `network_1`

```sql
SELECT H2.name
FROM Highschooler H1
JOIN Friend F ON H1.ID = F.student_id
JOIN Highschooler H2 ON F.friend_id = H2.ID
WHERE H1.name = 'Kyle'
```

## AL0504

Question: What region does Angola belong to and what is its population?

Database: `world_1`

```sql
SELECT Region, Population
FROM country
WHERE Name = 'Angola'
```

## AL0505

Question: List the mony made by each poker players in descending order.

Database: `poker_player`

```sql
SELECT Earnings
FROM poker_player
ORDER BY Earnings DESC
```

## AL0506

Question: What are the first name and last name of the professionals who have done treatment cheaper than average?

Database: `dog_kennels`

```sql
SELECT DISTINCT T1.first_name, T1.last_name
FROM Professionals T1
INNER JOIN Treatments T2 ON T1.professional_id = T2.professional_id
WHERE T2.cost_of_treatment < (SELECT AVG(cost_of_treatment) FROM Treatments)
```

## AL0507

Question: find the pixel aspect ratio and nation of the tv channels that do not use English.

Database: `tvshow`

```sql
SELECT pixel_aspect_ratio_par , country FROM tv_channel WHERE LANGUAGE != 'English'
```

## AL0508

Question: Which distinctive models are produced by General Motors or heavier than 3500?

Database: `car_1`

```sql
SELECT DISTINCT T1.Model FROM CAR_NAMES AS T1 JOIN CARS_DATA AS T2 ON T1.MakeId = T2.Id JOIN MODEL_LIST AS T3 ON T1.Model = T3.Model JOIN CAR_MAKERS AS T4 ON T3.Maker = T4.Id WHERE T4.Maker = 'gm' OR T2.weight > 3500
```

## AL0509

Question: What is the official language spoken in the country lead by Beatrix?

Database: `world_1`

```sql
SELECT T2.Language
FROM country AS T1
INNER JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode
WHERE T1.HeadOfState = 'Beatrix' AND T2.IsOfficial = 'T'
```

## AL0510

Question: How many type of governments are in Africa?

Database: `world_1`

```sql
SELECT COUNT(DISTINCT GovernmentForm) FROM country WHERE Continent = 'Africa'
```

## AL0511

Question: What are the full names of all left handed players, in order of age?

Database: `wta_1`

```sql
SELECT first_name, last_name
FROM players
WHERE hand = 'L'
ORDER BY birth_date ASC
```

## AL0512

Question: How many people live in Asia, and what is the largest GNP among them?

Database: `world_1`

```sql
SELECT sum(population) , max(GNP) FROM country WHERE continent = "Asia"
```

## AL0513

Question: What is the number of car models that are produced by each company and what is the id and full name of each maker?

Database: `car_1`

```sql
SELECT T1.Id, T1.FullName, COUNT(T2.Model) AS NumModels
FROM car_makers AS T1
INNER JOIN model_list AS T2 ON T1.Id = T2.Maker
GROUP BY T1.Id, T1.FullName
```

## AL0514

Question: What is the id of the semester that had both Masters and Bachelors students enrolled?

Database: `student_transcripts_tracking`

```sql
SELECT T1.semester_id FROM student_enrolment AS T1 JOIN degree_programs AS T2 ON T1.degree_program_id = T2.degree_program_id WHERE T2.degree_summary_name = 'Master' INTERSECT SELECT T1.semester_id FROM student_enrolment AS T1 JOIN degree_programs AS T2 ON T1.degree_program_id = T2.degree_program_id WHERE T2.degree_summary_name = 'Bachelor'
```

## AL0515

Question: Find the name of airports which do not have any flight in and out.

Database: `flight_2`

```sql
SELECT AirportName FROM Airports WHERE AirportCode NOT IN (SELECT SourceAirport FROM Flights UNION SELECT DestAirport FROM Flights)
```

## AL0516

Question: What are the population, name and leader of the largest country by land?

Database: `world_1`

```sql
SELECT Population, Name, HeadOfState
FROM country
ORDER BY SurfaceArea DESC
LIMIT 1
```

## AL0517

Question: List the name and date the battle that has lost  Lettice and HMS Atalanta

Database: `battle_death`

```sql
SELECT b.name, b.date
FROM battle b
JOIN ship s1 ON b.id = s1.lost_in_battle
JOIN ship s2 ON b.id = s2.lost_in_battle
WHERE s1.name = 'Lettice' AND s2.name = 'HMS Atalanta'
```

## AL0518

Question: Count the number of flights departing from 'APG'.

Database: `flight_2`

```sql
SELECT count(*) FROM FLIGHTS WHERE SourceAirport = "APG"
```

## AL0519

Question: Which languages are spoken by only one republic country?

Database: `world_1`

```sql
SELECT T1.Language
FROM countrylanguage AS T1
INNER JOIN country AS T2 ON T1.CountryCode = T2.Code
WHERE T2.GovernmentForm = 'Republic'
GROUP BY T1.Language
HAVING COUNT(T1.CountryCode) = 1
```

## AL0520

Question: Return the codes of countries for which Spanish is predominantly spoken .

Database: `world_1`

```sql
SELECT CountryCode FROM countrylanguage WHERE LANGUAGE = "Spanish" AND Percentage > 50
```

## AL0521

Question: What are the countries that have cartoons on TV that Todd Casey writes?

Database: `tvshow`

```sql
SELECT DISTINCT T2.Country
FROM Cartoon AS T1
INNER JOIN TV_Channel AS T2 ON T1.Channel = T2.id
WHERE T1.Written_by = 'Todd Casey'
```

## AL0522

Question: List the mony made by each poker players in descending order.

Database: `poker_player`

```sql
SELECT Earnings FROM poker_player ORDER BY Earnings DESC
```

## AL0523

Question: Return the countries for which there are two or more people from.

Database: `poker_player`

```sql
SELECT Nationality
FROM people
GROUP BY Nationality
HAVING COUNT(*) >= 2
```

## AL0524

Question: Which airlines have departing flights from both APG and CVO ?

Database: `flight_2`

```sql
SELECT T1.Airline
FROM airlines AS T1
INNER JOIN flights AS T2 ON T1.uid = T2.Airline
WHERE T2.SourceAirport = 'APG'
INTERSECT
SELECT T1.Airline
FROM airlines AS T1
INNER JOIN flights AS T2 ON T1.uid = T2.Airline
WHERE T2.SourceAirport = 'CVO'
```

## AL0525

Question: What is the name of the museum that had no person come yet?

Database: `museum_visit`

```sql
SELECT Name
FROM museum
WHERE Museum_ID NOT IN (SELECT Museum_ID FROM visit)
```

## AL0526

Question: What is the accelerate of amc hornet sportabout (sw)?

Database: `car_1`

```sql
SELECT T1.Accelerate FROM CARS_DATA AS T1 JOIN CAR_NAMES AS T2 ON T1.Id = T2.MakeId WHERE T2.Make = 'amc hornet sportabout (sw)'
```

## AL0527

Question: Show name, country, age for all singers from the oldest to the youngest.

Database: `concert_singer`

```sql
SELECT name , country , age FROM singer ORDER BY age DESC
```

## AL0528

Question: What are the titles of all cartoons  Ben Jones or Brandon Vietti directs?

Database: `tvshow`

```sql
SELECT Title FROM Cartoon WHERE Directed_by = "Ben Jones" OR Directed_by = "Brandon Vietti"
```

## AL0529

Question: How many nations has more than 2 car makers ?

Database: `car_1`

```sql
SELECT COUNT(*) AS NationCount
FROM (
    SELECT countries.CountryName
    FROM car_makers
    INNER JOIN countries ON car_makers.Country = countries.CountryId
    GROUP BY countries.CountryName
    HAVING COUNT(car_makers.Id) > 2
)
```

## AL0530

Question: List the name of singers whose  is not French.

Database: `singer`

```sql
SELECT Name
FROM singer
WHERE Citizenship != 'France'
```

## AL0531

Question: Find the number of flights landing in Aberdeen or Abilene.

Database: `flight_2`

```sql
SELECT count(*) FROM FLIGHTS AS T1 JOIN AIRPORTS AS T2 ON T1.DestAirport = T2.AirportCode WHERE T2.City = "Aberdeen" OR T2.City = "Abilene"
```

## AL0532

Question: What are the first names and birth dates of players from the USA?

Database: `wta_1`

```sql
SELECT first_name, birth_date
FROM players
WHERE country_code = 'USA'
```

## AL0533

Question: Count the number of countries for which Spanish is predominantly spoken .

Database: `world_1`

```sql
SELECT COUNT(*)
FROM countrylanguage
WHERE Language = 'Spanish' AND IsOfficial = 'T'
```

## AL0534

Question: Find the codes of nations that have more than 50 players.

Database: `wta_1`

```sql
SELECT country_code
FROM players
GROUP BY country_code
HAVING COUNT(player_id) > 50
```

## AL0535

Question: Which dogs are owned by someone who lives in Virginia? List the owner's first name and the dog's name.

Database: `dog_kennels`

```sql
SELECT T1.first_name , T2.name FROM Owners AS T1 JOIN Dogs AS T2 ON T1.owner_id = T2.owner_id WHERE T1.state = 'Virginia'
```

## AL0536

Question: How many ships ended up being Captured?

Database: `battle_death`

```sql
SELECT COUNT(*) FROM ship WHERE disposition_of_ship = 'Captured'
```

## AL0537

Question: what are the different names of the singers that have  sold than 300000 copies?

Database: `singer`

```sql
SELECT DISTINCT T1.Name
FROM singer AS T1
INNER JOIN song AS T2 ON T1.Singer_ID = T2.Singer_ID
WHERE T2.Sales > 300000
```

## AL0538

Question: List the most common place that the teachers come from

Database: `course_teach`

```sql
SELECT Hometown FROM teacher GROUP BY Hometown ORDER BY COUNT(*) DESC LIMIT 1
```

## AL0539

Question: What are flight numbers of flights departing from APG?

Database: `flight_2`

```sql
SELECT FlightNo FROM FLIGHTS WHERE SourceAirport = "APG"
```

## AL0540

Question: What are the different models created by either General Motors or over 3500 lbs?

Database: `car_1`

```sql
SELECT DISTINCT T1.Model FROM CAR_NAMES AS T1 JOIN CARS_DATA AS T2 ON T1.MakeId = T2.Id JOIN MODEL_LIST AS T3 ON T1.Model = T3.Model JOIN CAR_MAKERS AS T4 ON T3.Maker = T4.Id WHERE T4.FullName = 'General Motors' OR T2.weight > 3500
```

## AL0541

Question: What is the number of nations with more than 2 car makers ?

Database: `car_1`

```sql
SELECT COUNT(*)
FROM (
    SELECT T2.CountryName
    FROM car_makers AS T1
    INNER JOIN countries AS T2 ON T1.Country = T2.CountryId
    GROUP BY T2.CountryName
    HAVING COUNT(T1.Id) > 2
) AS NationWithMoreThan2Makers
```

## AL0542

Question: Which country does ""JetBlue Airways"" belong to?

Database: `flight_2`

```sql
SELECT Country FROM airlines WHERE Airline = 'JetBlue Airways'
```

## AL0543

Question: What is the average miles per gallon(mpg) of the 4 CYL cars?

Database: `car_1`

```sql
SELECT avg(mpg) FROM CARS_DATA WHERE Cylinders = 4
```

## AL0544

Question: What are airlines that have some flight departing from AHD?

Database: `flight_2`

```sql
SELECT T1.Airline
FROM airlines AS T1
INNER JOIN flights AS T2 ON T1.uid = T2.Airline
WHERE T2.SourceAirport = 'AHD'
```

## AL0545

Question: What are the names of the winner and loser who played in the longest match?

Database: `wta_1`

```sql
SELECT winner_name, loser_name
FROM matches
ORDER BY minutes DESC
LIMIT 1
```

## AL0546

Question: How many likes does Kyle have?

Database: `network_1`

```sql
SELECT COUNT(*)
FROM Likes
WHERE liked_id = (SELECT ID FROM Highschooler WHERE name = 'Kyle')
```

## AL0547

Question: List the names of teachers from youngest to oldest.

Database: `course_teach`

```sql
SELECT Name
FROM teacher
ORDER BY CAST(Age AS INTEGER) ASC
```

## AL0548

Question: What grade is Kyle in?

Database: `network_1`

```sql
SELECT grade FROM Highschooler WHERE name = 'Kyle'
```

## AL0549

Question: What is the total number of unique official languages spoken in the countries that are founded before 1930?

Database: `world_1`

```sql
SELECT COUNT(DISTINCT T2.Language)
FROM country AS T1
INNER JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode
WHERE T1.IndepYear < 1930 AND T2.IsOfficial = 'T'
```

## AL0550

Question: Show the citizenship shared by singers born  before 1945 and after 1955.

Database: `singer`

```sql
SELECT Citizenship
FROM singer
WHERE Birth_Year < 1945
INTERSECT
SELECT Citizenship
FROM singer
WHERE Birth_Year > 1955
```

## AL0551

Question: What are the airline names and abbreviations for airlines in the USA?

Database: `flight_2`

```sql
SELECT Airline, Abbreviation
FROM airlines
WHERE Country = 'USA'
```

## AL0552

Question: What is the total population and maximum GNP in Asia?

Database: `world_1`

```sql
SELECT SUM(Population), MAX(GNP)
FROM country
WHERE Continent = 'Asia'
```

## AL0553

Question: Find the model of the car that is lighter than average .

Database: `car_1`

```sql
SELECT T1.Model FROM CAR_NAMES AS T1 JOIN CARS_DATA AS T2 ON T1.MakeId = T2.Id WHERE T2.weight < (SELECT avg(weight) FROM CARS_DATA)
```

## AL0554

Question: List the names of employees and sort from youngest to oldest

Database: `employee_hire_evaluation`

```sql
SELECT name FROM employee ORDER BY age ASC
```

## AL0555

Question: What are the codes of the different nations, and what are the languages spoken by the greatest percentage of people for each?

Database: `world_1`

```sql
SELECT CountryCode, Language
FROM countrylanguage
WHERE (CountryCode, Percentage) IN (
    SELECT CountryCode, MAX(Percentage)
    FROM countrylanguage
    GROUP BY CountryCode
)
```

## AL0556

Question: Show the names of all high schoolers in  10.

Database: `network_1`

```sql
SELECT name
FROM Highschooler
WHERE grade = 10
```

## AL0557

Question: How many continents speak Chinese?

Database: `world_1`

```sql
SELECT count(DISTINCT Continent) FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode WHERE T2.Language = "Chinese"
```

## AL0558

Question: What are airport names at Aberdeen?

Database: `flight_2`

```sql
SELECT AirportName FROM airports WHERE City = 'Aberdeen'
```

## AL0559

Question: How many shops are there in each place?

Database: `employee_hire_evaluation`

```sql
SELECT Location, COUNT(*) FROM shop GROUP BY Location
```

## AL0560

Question: Return the codes of countries for which Spanish is predominantly spoken .

Database: `world_1`

```sql
SELECT CountryCode
FROM countrylanguage
WHERE Language = 'Spanish'
```

## AL0561

Question: What are the towns from which at least two teachers come from?

Database: `course_teach`

```sql
SELECT Hometown
FROM teacher
GROUP BY Hometown
HAVING COUNT(*) >= 2
```

## AL0562

Question: How many official languages are spoken in Afghanistan?

Database: `world_1`

```sql
SELECT COUNT(*) FROM countrylanguage WHERE CountryCode = 'AFG' AND IsOfficial = 'T'
```

## AL0563

Question: How much does the youngest dog weigh?

Database: `pets_1`

```sql
SELECT weight FROM pets ORDER BY pet_age LIMIT 1
```

## AL0564

Question: How many players are from each nation?

Database: `wta_1`

```sql
SELECT count(*) , country_code FROM players GROUP BY country_code
```

## AL0565

Question: What are the names of the people who teach math?

Database: `course_teach`

```sql
SELECT T.Name
FROM teacher T
JOIN course_arrange CA ON T.Teacher_ID = CA.Teacher_ID
JOIN course C ON CA.Course_ID = C.Course_ID
WHERE C.Course = 'Math'
```

## AL0566

Question: What is the number of distinct continents where Chinese is spoken?

Database: `world_1`

```sql
SELECT count(DISTINCT continent) FROM country AS T1 JOIN countrylanguage AS T2 ON T1.code = T2.countrycode WHERE T2.language = "Chinese"
```

## AL0567

Question: Return the names and surface areas of the 5 largest countries.

Database: `world_1`

```sql
SELECT Name, SurfaceArea
FROM country
ORDER BY SurfaceArea DESC
LIMIT 5
```

## AL0568

Question: Find the average age of students who do not have any pet.

Database: `pets_1`

```sql
SELECT avg(age) FROM student WHERE stuid NOT IN (SELECT stuid FROM has_pet)
```

## AL0569

Question: List the airport code and name in Anthony.

Database: `flight_2`

```sql
SELECT AirportCode , AirportName FROM AIRPORTS WHERE city = "Anthony"
```

## AL0570

Question: In 1980, how many cars were made?

Database: `car_1`

```sql
SELECT COUNT(*) FROM cars_data WHERE Year = 1980
```

## AL0571

Question: What are the names and ranks of the three youngest victors across all matches?

Database: `wta_1`

```sql
SELECT winner_name, winner_rank
FROM matches
ORDER BY winner_age ASC
LIMIT 3
```

## AL0572

Question: How many matches were played in 2013 or 2016?

Database: `wta_1`

```sql
SELECT count(*) FROM matches WHERE YEAR = 2013 OR YEAR = 2016
```

## AL0573

Question: What is the name of the series that has the  """"A Love of a Lifetime""""?

Database: `tvshow`

```sql
SELECT T1.series_name FROM TV_Channel AS T1 JOIN TV_series AS T2 ON T1.id = T2.Channel WHERE T2.Episode = "A Love of a Lifetime"
```

## AL0574

Question: Give the names of countries officially use English and French

Database: `world_1`

```sql
SELECT T1.Name
FROM country AS T1
INNER JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode
WHERE T2.Language IN ('English', 'French') AND T2.IsOfficial = 'T'
GROUP BY T1.Name
HAVING COUNT(DISTINCT T2.Language) = 2
```

## AL0575

Question: List the names of all cartoons in alphabetical order.

Database: `tvshow`

```sql
SELECT Title FROM Cartoon ORDER BY title
```

## AL0576

Question: What is the maximum miles per gallon of the 8 CYL cars or cars produced before 1980 ?

Database: `car_1`

```sql
SELECT max(mpg) FROM CARS_DATA WHERE Cylinders = 8 OR YEAR < 1980
```

## AL0577

Question: Return the grade for Kyle.

Database: `network_1`

```sql
SELECT grade
FROM Highschooler
WHERE name = 'Kyle'
```

## AL0578

Question: how many cars were produced in 1980?

Database: `car_1`

```sql
SELECT COUNT(*) FROM cars_data WHERE Year = 1980
```

## AL0579

Question: Find the number of cartoons by each of the listed directors.

Database: `tvshow`

```sql
SELECT Directed_by, COUNT(*) FROM Cartoon GROUP BY Directed_by
```

## AL0580

Question: What are the students' first names who have both cats and dogs?

Database: `pets_1`

```sql
SELECT T1.Fname
FROM Student AS T1
INNER JOIN Has_Pet AS T2 ON T1.StuID = T2.StuID
INNER JOIN Pets AS T3 ON T2.PetID = T3.PetID
WHERE T3.PetType IN ('cat', 'dog')
GROUP BY T1.StuID
HAVING COUNT(DISTINCT T3.PetType) = 2
```

## AL0581

Question: Show the name of teachers who are either 32 or 33 years old?

Database: `course_teach`

```sql
SELECT Name
FROM teacher
WHERE Age IN ('32', '33')
```

## AL0582

Question: What are all the song names by singers who are older than average?

Database: `concert_singer`

```sql
SELECT Song_Name
FROM singer
WHERE Age > (SELECT AVG(Age) FROM singer)
```

## AL0583

Question: find the id of tv channels that do not play any cartoon  Ben Jones directs.

Database: `tvshow`

```sql
SELECT id FROM TV_Channel EXCEPT SELECT channel FROM cartoon WHERE directed_by = 'Ben Jones'
```

## AL0584

Question: Find the names of stores that have more than average goods.

Database: `employee_hire_evaluation`

```sql
SELECT Name
FROM shop
WHERE Number_products > (SELECT AVG(Number_products) FROM shop)
```

## AL0585

Question: Return the number of airlines in the USA.

Database: `flight_2`

```sql
SELECT COUNT(*) FROM airlines WHERE Country = 'USA'
```

## AL0586

Question: How many people live in Gelderland ?

Database: `world_1`

```sql
SELECT sum(population) FROM city WHERE district = "Gelderland"
```

## AL0587

Question: What are the names of conductors, ordered by how old they are?

Database: `orchestra`

```sql
SELECT Name
FROM conductor
ORDER BY Age
```

## AL0588

Question: What are the names of the singers who performed in a concert in 2014?

Database: `concert_singer`

```sql
SELECT DISTINCT T3.Name
FROM concert AS T1
INNER JOIN singer_in_concert AS T2 ON T1.concert_ID = T2.concert_ID
INNER JOIN singer AS T3 ON T2.Singer_ID = T3.Singer_ID
WHERE T1.Year = '2014'
```

## AL0589

Question: Find all airlines that have flights from 'CVO' but not from 'APG'.

Database: `flight_2`

```sql
SELECT T1.Airline FROM AIRLINES AS T1 JOIN FLIGHTS AS T2 ON T1.uid = T2.Airline WHERE T2.SourceAirport = "CVO" EXCEPT SELECT T1.Airline FROM AIRLINES AS T1 JOIN FLIGHTS AS T2 ON T1.uid = T2.Airline WHERE T2.SourceAirport = "APG"
```

## AL0590

Question: Which professionals have operated a treatment that is less expansive than the average? Give me theor first names and last names.

Database: `dog_kennels`

```sql
SELECT DISTINCT T1.first_name, T1.last_name
FROM Professionals T1
INNER JOIN Treatments T2 ON T1.professional_id = T2.professional_id
WHERE T2.cost_of_treatment < (SELECT AVG(cost_of_treatment) FROM Treatments)
```

## AL0591

Question: What is the name and capacity of the stadium  with the most concerts after 2013?

Database: `concert_singer`

```sql
SELECT T2.Name, T2.Capacity
FROM concert AS T1
INNER JOIN stadium AS T2 ON T1.Stadium_ID = T2.Stadium_ID
WHERE T1.Year > '2013'
GROUP BY T1.Stadium_ID
ORDER BY COUNT(T1.concert_ID) DESC
LIMIT 1
```

## AL0592

Question: Find the name of tournament that has more than 10 matches.

Database: `wta_1`

```sql
SELECT tourney_name
FROM matches
GROUP BY tourney_name
HAVING COUNT(*) > 10
```

## AL0593

Question: For each country, what is the maximum net worth?

Database: `singer`

```sql
SELECT Citizenship, MAX(Net_Worth_Millions)
FROM singer
GROUP BY Citizenship
```

## AL0594

Question: What is the language that is used by the largest number of Asian nations?

Database: `world_1`

```sql
SELECT T2.Language
FROM country AS T1
INNER JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode
WHERE T1.Continent = 'Asia'
GROUP BY T2.Language
ORDER BY COUNT(T2.Language) DESC
LIMIT 1
```

## AL0595

Question: What are the id, role, and first name of the people who have performed two or more treatments?

Database: `dog_kennels`

```sql
SELECT T1.professional_id, T1.role_code, T1.first_name
FROM Professionals AS T1
INNER JOIN Treatments AS T2 ON T1.professional_id = T2.professional_id
GROUP BY T1.professional_id, T1.role_code, T1.first_name
HAVING COUNT(T2.treatment_id) >= 2
```

## AL0596

Question: What are the codes of countries where Spanish is spoken by the largest percentage of people?

Database: `world_1`

```sql
SELECT CountryCode FROM countrylanguage WHERE LANGUAGE = "Spanish" ORDER BY Percentage DESC LIMIT 1
```

## AL0597

Question: List the title of all cartoon  Ben Jones or Brandon Vietti directs.

Database: `tvshow`

```sql
SELECT Title
FROM Cartoon
WHERE Directed_by IN ('Ben Jones', 'Brandon Vietti')
```

## AL0598

Question: How many languages are spoken in Aruba?

Database: `world_1`

```sql
SELECT COUNT(Language)
FROM countrylanguage
WHERE CountryCode = (
    SELECT Code
    FROM country
    WHERE Name = 'Aruba'
)
```

## AL0599

Question: What is the smallest weight of the 8 CYL car produced on 1974 ?

Database: `car_1`

```sql
SELECT MIN(Weight) FROM cars_data WHERE Cylinders = 8 AND Year = 1974
```

## AL0600

Question: What is the average edispl for all volvos?

Database: `car_1`

```sql
SELECT avg(T1.edispl) FROM CARS_DATA AS T1 JOIN CAR_NAMES AS T2 ON T1.Id = T2.MakeId WHERE T2.Make LIKE "%volvo%"
```

## AL0601

Question: What is the average horsepower of the cars before 1980?

Database: `car_1`

```sql
SELECT AVG(CAST(Horsepower AS REAL)) AS AverageHorsepower
FROM cars_data
WHERE Year < 1980
```

## AL0602

Question: Find the name and location of the stadiums which some concerts happened in both 2014 and 2015.

Database: `concert_singer`

```sql
SELECT T2.name , T2.location FROM concert AS T1 JOIN stadium AS T2 ON T1.stadium_id = T2.stadium_id WHERE T1.year = 2014 INTERSECT SELECT T2.name , T2.location FROM concert AS T1 JOIN stadium AS T2 ON T1.stadium_id = T2.stadium_id WHERE T1.year = 2015
```

## AL0603

Question: What is the average horsepower of the cars before 1980?

Database: `car_1`

```sql
SELECT avg(horsepower) FROM CARS_DATA WHERE YEAR < 1980
```

## AL0604

Question: Who has paid the largest amount of money in total for their dogs? Show the id and zip code.

Database: `dog_kennels`

```sql
SELECT T1.owner_id, T1.zip_code
FROM Owners AS T1
INNER JOIN Dogs AS T2 ON T1.owner_id = T2.owner_id
INNER JOIN Treatments AS T3 ON T2.dog_id = T3.dog_id
GROUP BY T1.owner_id, T1.zip_code
ORDER BY SUM(T3.cost_of_treatment) DESC
LIMIT 1
```

## AL0605

Question: How many continents speak Chinese?

Database: `world_1`

```sql
SELECT COUNT(DISTINCT T1.Continent)
FROM country AS T1
INNER JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode
WHERE T2.Language = 'Chinese'
```

## AL0606

Question: What are flight numbers of flights departing from Aberdeen?

Database: `flight_2`

```sql
SELECT T1.FlightNo FROM FLIGHTS AS T1 JOIN AIRPORTS AS T2 ON T1.SourceAirport = T2.AirportCode WHERE T2.City = "Aberdeen"
```

## AL0607

Question: What is the average earnings of poker players taller than 200?

Database: `poker_player`

```sql
SELECT AVG(T2.Earnings)
FROM people AS T1
INNER JOIN poker_player AS T2 ON T1.People_ID = T2.People_ID
WHERE T1.Height > 200
```

## AL0608

Question: Give the flight numbers of flights leaving from APG.

Database: `flight_2`

```sql
SELECT FlightNo FROM flights WHERE SourceAirport = 'APG'
```

## AL0609

Question: What are the first names of every student who has a cat or dog?

Database: `pets_1`

```sql
SELECT T1.Fname
FROM Student AS T1
INNER JOIN Has_Pet AS T2 ON T1.StuID = T2.StuID
INNER JOIN Pets AS T3 ON T2.PetID = T3.PetID
WHERE T3.PetType IN ('cat', 'dog')
```

## AL0610

Question: Find the name of airports which do not have any flight in and out.

Database: `flight_2`

```sql
SELECT AirportName
FROM airports
WHERE AirportCode NOT IN (
    SELECT SourceAirport FROM flights
    UNION
    SELECT DestAirport FROM flights
)
```

## AL0611

Question: Which African countries have fewer people than that of any country in Asia?

Database: `world_1`

```sql
SELECT Name
FROM country
WHERE Continent = 'Africa'
  AND Population < (
    SELECT MIN(Population)
    FROM country
    WHERE Continent = 'Asia'
  )
```

## AL0612

Question: Count the number of dogs that are younger than the average.

Database: `dog_kennels`

```sql
SELECT count(*) FROM Dogs WHERE age < ( SELECT avg(age) FROM Dogs )
```

## AL0613

Question: Whic`h unique cities are in  Asian countries where Chinese is the official ?

Database: `world_1`

```sql
SELECT DISTINCT T1.Name FROM city AS T1 JOIN country AS T2 ON T1.CountryCode = T2.Code JOIN countrylanguage AS T3 ON T3.CountryCode = T2.Code WHERE T3.IsOfficial = "T" AND T3.Language = "Chinese" AND T2.Continent = "Asia"
```

## AL0614

Question: List the names of all winners who played in both 2013 and 2016.

Database: `wta_1`

```sql
SELECT winner_name
FROM matches
WHERE year = 2013
INTERSECT
SELECT winner_name
FROM matches
WHERE year = 2016
```

## AL0615

Question: What are airlines that have flights arriving at AHD?

Database: `flight_2`

```sql
SELECT T1.Airline
FROM airlines AS T1
INNER JOIN flights AS T2 ON T1.uid = T2.Airline
WHERE T2.DestAirport = 'AHD'
```

## AL0616

Question: How many different forms of governments are there in Africa?

Database: `world_1`

```sql
SELECT count(DISTINCT GovernmentForm) FROM country WHERE region LIKE "%Africa%"
```

## AL0617

Question: What is the number of makers of care in France?

Database: `car_1`

```sql
SELECT count(*) FROM CAR_MAKERS AS T1 JOIN COUNTRIES AS T2 ON T1.Country = T2.CountryId WHERE T2.CountryName = 'france'
```

## AL0618

Question: What is the average grade of students who have friends?

Database: `network_1`

```sql
SELECT avg(grade) FROM Highschooler WHERE id IN (SELECT student_id FROM Friend)
```

## AL0619

Question: What is the average horsepower for all cards produced before 1980?

Database: `car_1`

```sql
SELECT avg(horsepower) FROM CARS_DATA WHERE YEAR < 1980
```

## AL0620

Question: Give average earnings of poker players who are taller than 200.

Database: `poker_player`

```sql
SELECT avg(T1.Earnings) FROM poker_player AS T1 JOIN people AS T2 ON T1.People_ID = T2.People_ID WHERE T2.Height > 200
```

## AL0621

Question: How many car makers are there in france?

Database: `car_1`

```sql
SELECT count(*) FROM CAR_MAKERS AS T1 JOIN COUNTRIES AS T2 ON T1.Country = T2.CountryId WHERE T2.CountryName = 'france'
```

## AL0622

Question: Return the codes of non republic countries that do not speak Englishs.

Database: `world_1`

```sql
SELECT Code FROM country WHERE GovernmentForm != "Republic" EXCEPT SELECT CountryCode FROM countrylanguage WHERE LANGUAGE = "English"
```

## AL0623

Question: Count the number of flights into ATO.

Database: `flight_2`

```sql
SELECT COUNT(*) FROM flights WHERE DestAirport = 'ATO'
```

## AL0624

Question: What are the titles of all cartoons  Ben Jones or Brandon Vietti directs?

Database: `tvshow`

```sql
SELECT Title
FROM Cartoon
WHERE Directed_by IN ('Ben Jones', 'Brandon Vietti')
```

## AL0625

Question: Which year has the most high schoolers?

Database: `network_1`

```sql
SELECT grade
FROM Highschooler
GROUP BY grade
ORDER BY COUNT(*) DESC
LIMIT 1
```

## AL0626

Question: What are the first names of every student who has a cat or dog?

Database: `pets_1`

```sql
SELECT DISTINCT T1.fname FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid = T2.stuid JOIN pets AS T3 ON T3.petid = T2.petid WHERE T3.pettype = 'cat' OR T3.pettype = 'dog'
```

## AL0627

Question: What is the total number of countries where Spanish is spoken by the largest percentage of people?

Database: `world_1`

```sql
SELECT count(*) FROM (SELECT countrycode FROM countrylanguage WHERE LANGUAGE = "Spanish" ORDER BY percentage DESC LIMIT 1)
```

## AL0628

Question: What is name of the nation that speaks the largest number of languages?

Database: `world_1`

```sql
SELECT T1.Name FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode GROUP BY T1.Name ORDER BY COUNT(*) DESC LIMIT 1
```

## AL0629

Question: What is the number of cars with over 150 hp?

Database: `car_1`

```sql
SELECT COUNT(*)
FROM cars_data
WHERE CAST(Horsepower AS INTEGER) > 150
```

## AL0630

Question: Show names, results and bulgarian commanders of the battles with no ships lost in the 'English Channel'.

Database: `battle_death`

```sql
SELECT name, result, bulgarian_commander
FROM battle
WHERE id NOT IN (
    SELECT lost_in_battle
    FROM ship
    WHERE location = 'English Channel'
)
```

## AL0631

Question: What are the names of the teachers who do not come from Little Lever Urban District?

Database: `course_teach`

```sql
SELECT Name FROM teacher WHERE Hometown != "Little Lever Urban District"
```

## AL0632

Question: Which Asian countries have more people than any country in Africa?

Database: `world_1`

```sql
SELECT Name FROM country WHERE Continent = "Asia" AND population > (SELECT max(population) FROM country WHERE Continent = "Africa")
```

## AL0633

Question: What is the number of nations with more than 2 car makers ?

Database: `car_1`

```sql
SELECT count(*) FROM countries AS t1 JOIN car_makers AS t2 ON t1.countryid = t2.country GROUP BY t1.countryid HAVING count(*) > 2
```

## AL0634

Question: What are the regions that use English or Dutch?

Database: `world_1`

```sql
SELECT DISTINCT T1.Region FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode WHERE T2.Language = "English" OR T2.Language = "Dutch"
```

## AL0635

Question: list all cartoon titles and their directors ordered by the time they broadcasted

Database: `tvshow`

```sql
SELECT title , directed_by FROM cartoon ORDER BY original_air_date
```

## AL0636

Question: How many TV Channels speak English ?

Database: `tvshow`

```sql
SELECT count(*) FROM TV_Channel WHERE LANGUAGE = 'English'
```

## AL0637

Question: Find the production code and channel of the most recently broadcasted cartoon.

Database: `tvshow`

```sql
SELECT production_code , channel FROM cartoon ORDER BY original_air_date DESC LIMIT 1
```

## AL0638

Question: What are all distinct countries where singers older than 20 are from?

Database: `concert_singer`

```sql
SELECT DISTINCT country FROM singer WHERE age > 20
```

## AL0639

Question: What is the id and weight of every pet who is over 1 year old?

Database: `pets_1`

```sql
SELECT PetID, weight
FROM Pets
WHERE pet_age > 1
```

## AL0640

Question: What is the maker of the carr produced in the earliest  and what  year was it?

Database: `car_1`

```sql
SELECT T4.Maker, T1.Year
FROM cars_data AS T1
INNER JOIN car_names AS T2 ON T1.Id = T2.MakeId
INNER JOIN model_list AS T3 ON T2.Model = T3.Model
INNER JOIN car_makers AS T4 ON T3.Maker = T4.Id
ORDER BY T1.Year ASC
LIMIT 1
```

## AL0641

Question: What is the total surface area of the countries in the Caribbean ?

Database: `world_1`

```sql
SELECT sum(SurfaceArea) FROM country WHERE Region = "Caribbean"
```

## AL0642

Question: Find the id of students who do not have a cat.

Database: `pets_1`

```sql
SELECT StuID
FROM Student
WHERE StuID NOT IN (
    SELECT T1.StuID
    FROM Has_Pet AS T1
    INNER JOIN Pets AS T2 ON T1.PetID = T2.PetID
    WHERE T2.PetType = 'cat'
)
```

## AL0643

Question: Find the average grade of all students who have some friends.

Database: `network_1`

```sql
SELECT AVG(T1.grade)
FROM Highschooler AS T1
INNER JOIN Friend AS T2 ON T1.ID = T2.student_id
```

## AL0644

Question: Where is the youngest teacher from?

Database: `course_teach`

```sql
SELECT Hometown
FROM teacher
ORDER BY Age ASC
LIMIT 1
```

## AL0645

Question: Sort all the shops by amount of merchandise in descending order, and return the name, location and district of each shop.

Database: `employee_hire_evaluation`

```sql
SELECT Name, Location, District
FROM shop
ORDER BY Number_products DESC
```

## AL0646

Question: What are the names and locations of the stadiums that had concerts that occurred in both 2014 and 2015?

Database: `concert_singer`

```sql
SELECT DISTINCT s.Name, s.Location
FROM stadium s
INNER JOIN concert c ON s.Stadium_ID = c.Stadium_ID
WHERE c.Year IN ('2014', '2015')
GROUP BY s.Name, s.Location
HAVING COUNT(DISTINCT c.Year) = 2
```

## AL0647

Question: What is the episode for the TV series called Sky Radio?

Database: `tvshow`

```sql
SELECT T1.Episode
FROM TV_series AS T1
INNER JOIN TV_Channel AS T2 ON T1.Channel = T2.id
WHERE T2.series_name = 'Sky Radio'
```

## AL0648

Question: Which countries in europe have at least 3 car manufacturers?

Database: `car_1`

```sql
SELECT T1.CountryName FROM countries AS T1 JOIN car_makers AS T2 ON T1.CountryId = T2.Country WHERE T1.Continent = (SELECT ContId FROM continents WHERE Continent = 'europe') GROUP BY T1.CountryName HAVING count(*) >= 3
```

## AL0649

Question: How is the math described?

Database: `student_transcripts_tracking`

```sql
SELECT course_description FROM Courses WHERE course_name = 'math'
```

## AL0650

Question: What is the first name and country code of the oldest player?

Database: `wta_1`

```sql
SELECT first_name , country_code FROM players ORDER BY birth_date LIMIT 1
```

## AL0651

Question: What are the countries that are not playing cartoons  Todd Casey writes?

Database: `tvshow`

```sql
SELECT DISTINCT Country
FROM TV_Channel
WHERE id NOT IN (
    SELECT T1.Channel
    FROM Cartoon AS T1
    INNER JOIN TV_Channel AS T2 ON T1.Channel = T2.id
    WHERE T1.Written_by = 'Todd Casey'
)
```

## AL0652

Question: How much surface area do the countires in the Carribean cover together?

Database: `world_1`

```sql
SELECT SUM(SurfaceArea) FROM country WHERE Region = 'Caribbean'
```

## AL0653

Question: Find the names of the visitors that is higher than lv 4, and order the results by the level from high to low.

Database: `museum_visit`

```sql
SELECT name FROM visitor WHERE level_of_membership > 4 ORDER BY level_of_membership DESC
```

## AL0654

Question: Find the name of the shops that do not recruit any employee.

Database: `employee_hire_evaluation`

```sql
SELECT name FROM shop WHERE shop_id NOT IN (SELECT shop_id FROM hiring)
```

## AL0655

Question: What is the number of cartoones  Joseph Kuh writes?

Database: `tvshow`

```sql
SELECT COUNT(*) FROM Cartoon WHERE Written_by = 'Joseph Kuhr'
```

## AL0656

Question: What are names of top 3 countries with most people?

Database: `world_1`

```sql
SELECT Name
FROM country
ORDER BY Population DESC
LIMIT 3
```

## AL0657

Question: What is the phone number of Timmothy Ward?

Database: `student_transcripts_tracking`

```sql
SELECT cell_mobile_number
FROM Students
WHERE first_name = 'Timmothy' AND last_name = 'Ward'
```

## AL0658

Question: Find the last name of the students who currently live in North Carolina but have not registered in any degree program.

Database: `student_transcripts_tracking`

```sql
SELECT T1.last_name FROM students AS T1 JOIN addresses AS T2 ON T1.current_address_id = T2.address_id WHERE T2.state_province_county = 'North Carolina' EXCEPT SELECT T3.last_name FROM students AS T3 JOIN student_enrolment AS T4 ON T3.student_id = T4.student_id
```

## AL0659

Question: What are the country codes of countries where people speak other than English?

Database: `world_1`

```sql
SELECT DISTINCT CountryCode FROM countrylanguage WHERE LANGUAGE != "English"
```

## AL0660

Question: What are the names of all high schoolers in  10?

Database: `network_1`

```sql
SELECT name FROM Highschooler WHERE grade = 10
```

## AL0661

Question: What is the total surface area of the countries in the Caribbean ?

Database: `world_1`

```sql
SELECT SUM(SurfaceArea) FROM country WHERE Region = 'Caribbean'
```

## AL0662

Question: Which airports do not have departing or arriving flights?

Database: `flight_2`

```sql
SELECT AirportName FROM Airports WHERE AirportCode NOT IN (SELECT SourceAirport FROM Flights UNION SELECT DestAirport FROM Flights)
```

## AL0663

Question: what is the name and nation of the singer who have a song having 'Hey' in its title?

Database: `concert_singer`

```sql
SELECT name , country FROM singer WHERE song_name LIKE '%Hey%'
```

## AL0664

Question: What are the id, role, and first name of the people who have performed two or more treatments?

Database: `dog_kennels`

```sql
SELECT T1.professional_id , T1.role_code , T1.first_name FROM professionals AS T1 JOIN treatments AS T2 ON T1.professional_id = T2.professional_id GROUP BY T1.professional_id HAVING count(*) >= 2
```

## AL0665

Question: What are  the different countries with singers  older than 20?

Database: `concert_singer`

```sql
SELECT DISTINCT country FROM singer WHERE age > 20
```

## AL0666

Question: Return the names of friends of  Kyle.

Database: `network_1`

```sql
SELECT T2.name FROM Friend AS T1 JOIN Highschooler AS T2 ON T1.friend_id = T2.id WHERE T1.student_id = (SELECT id FROM Highschooler WHERE name = "Kyle")
```

## AL0667

Question: Give the flight numbers of flights leaving from Aberdeen.

Database: `flight_2`

```sql
SELECT T1.FlightNo FROM FLIGHTS AS T1 JOIN AIRPORTS AS T2 ON T1.SourceAirport = T2.AirportCode WHERE T2.City = "Aberdeen"
```

## AL0668

Question: Show distinct names of singers that have songs sell  more than 300000.

Database: `singer`

```sql
SELECT DISTINCT T1.Name
FROM singer AS T1
INNER JOIN song AS T2 ON T1.Singer_ID = T2.Singer_ID
WHERE T2.Sales > 300000
```

## AL0669

Question: Show different nationalities and the maximum net worth of singers of country.

Database: `singer`

```sql
SELECT Citizenship, MAX(Net_Worth_Millions)
FROM singer
GROUP BY Citizenship
```

## AL0670

Question: In 1980, how many cars were made?

Database: `car_1`

```sql
SELECT count(*) FROM CARS_DATA WHERE YEAR = 1980
```

## AL0671

Question: How many cartoons Joseph Kuhr writes?

Database: `tvshow`

```sql
SELECT COUNT(*) FROM Cartoon WHERE Written_by = 'Joseph Kuhr'
```

## AL0672

Question: List all cartoon Ben Jones directs.

Database: `tvshow`

```sql
SELECT Title
FROM Cartoon
WHERE Directed_by = 'Ben Jones'
```

## AL0673

Question: What is the total number of languages used in Aruba?

Database: `world_1`

```sql
SELECT COUNT(*) FROM countrylanguage WHERE CountryCode = (SELECT Code FROM country WHERE Name = 'Aruba')
```

## AL0674

Question: How much is the most recent treatment?

Database: `dog_kennels`

```sql
SELECT cost_of_treatment FROM Treatments ORDER BY date_of_treatment DESC LIMIT 1
```

## AL0675

Question: Find the number of concerts happened in the stadium that can accommodate the most people.

Database: `concert_singer`

```sql
SELECT COUNT(T1.concert_ID)
FROM concert AS T1
INNER JOIN stadium AS T2 ON T1.Stadium_ID = T2.Stadium_ID
WHERE T2.Capacity = (SELECT MAX(Capacity) FROM stadium)
```

## AL0676

Question: What are the names of the singers who performed in a concert in 2014?

Database: `concert_singer`

```sql
SELECT T1.Name FROM singer AS T1 JOIN singer_in_concert AS T2 ON T1.Singer_ID = T2.Singer_ID JOIN concert AS T3 ON T2.concert_ID = T3.concert_ID WHERE T3.Year = 2014
```

## AL0677

Question: How much is the most recent treatment?

Database: `dog_kennels`

```sql
SELECT cost_of_treatment
FROM Treatments
ORDER BY date_of_treatment DESC
LIMIT 1
```

## AL0678

Question: What is the model for the car that is lighter than the average?

Database: `car_1`

```sql
SELECT T1.Model
FROM car_names AS T1
INNER JOIN cars_data AS T2 ON T1.MakeId = T2.Id
WHERE T2.Weight < (SELECT AVG(Weight) FROM cars_data)
```

## AL0679

Question: What is the maker of the carr produced in the earliest  and what  year was it?

Database: `car_1`

```sql
SELECT T1.Maker, T2.Year FROM CAR_MAKERS AS T1 JOIN MODEL_LIST AS T3 JOIN CAR_NAMES AS T4 JOIN CARS_DATA AS T2 ON T1.Id = T3.Maker AND T3.Model = T4.Model AND T4.MakeId = T2.Id ORDER BY T2.Year ASC LIMIT 1
```

## AL0680

Question: Which model saves the most gasoline?

Database: `car_1`

```sql
SELECT T2.Model
FROM cars_data AS T1
INNER JOIN car_names AS T2 ON T1.Id = T2.MakeId
ORDER BY CAST(T1.MPG AS REAL) DESC
LIMIT 1
```

## AL0681

Question: How many people live in countries that do not speak English?

Database: `world_1`

```sql
SELECT sum(Population) FROM country WHERE Name NOT IN (SELECT T1.Name FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode WHERE T2.Language = "English")
```

## AL0682

Question: What languages are only used by a single republic country?

Database: `world_1`

```sql
SELECT T1.Language
FROM countrylanguage AS T1
INNER JOIN country AS T2 ON T1.CountryCode = T2.Code
WHERE T2.GovernmentForm = 'Republic'
GROUP BY T1.Language
HAVING COUNT(T1.CountryCode) = 1
```

## AL0683

Question: Give the name, year of independence, and surface area of the country that has the fewest people.

Database: `world_1`

```sql
SELECT Name, IndepYear, SurfaceArea
FROM country
ORDER BY Population ASC
LIMIT 1
```

## AL0684

Question: Return the number of flights arriving in Aberdeen.

Database: `flight_2`

```sql
SELECT count(*) FROM FLIGHTS AS T1 JOIN AIRPORTS AS T2 ON T1.DestAirport = T2.AirportCode WHERE T2.City = "Aberdeen"
```

## AL0685

Question: What are the codes of the different nations, and what are the languages spoken by the greatest percentage of people for each?

Database: `world_1`

```sql
SELECT LANGUAGE , CountryCode , max(Percentage) FROM countrylanguage GROUP BY CountryCode
```

## AL0686

Question: find the pixel aspect ratio and nation of the tv channels that do not use English.

Database: `tvshow`

```sql
SELECT Pixel_aspect_ratio_PAR, Country
FROM TV_Channel
WHERE Language != 'English'
```

## AL0687

Question: Return the name, location and district of all shops odered by the amount of goods they sell from the most to the least.

Database: `employee_hire_evaluation`

```sql
SELECT Name, Location, District
FROM shop
ORDER BY Number_products DESC
```

## AL0688

Question: What are airlines that have some flight departing from AHD?

Database: `flight_2`

```sql
SELECT T1.Airline FROM AIRLINES AS T1 JOIN FLIGHTS AS T2 ON T1.uid = T2.Airline WHERE T2.SourceAirport = "AHD"
```

## AL0689

Question: Which employee received the biggest incentive? Give me the employee name.

Database: `employee_hire_evaluation`

```sql
SELECT t1.name FROM employee AS t1 JOIN evaluation AS t2 ON t1.Employee_ID = t2.Employee_ID ORDER BY t2.bonus DESC LIMIT 1
```

## AL0690

Question: How many nations has more than 2 car makers ?

Database: `car_1`

```sql
SELECT count(*) FROM (SELECT T.Country FROM car_makers AS T GROUP BY T.Country HAVING count(*) > 2)
```

## AL0691

Question: Which professionals live in Indiana or have done treatment on more than 2 treatments? List his or her id, last name and cell phone.

Database: `dog_kennels`

```sql
SELECT professional_id , last_name , cell_number FROM professionals WHERE state = 'Indiana' UNION SELECT T1.professional_id , T2.last_name , T2.cell_number FROM Treatments AS T1 JOIN professionals AS T2 ON T1.professional_id = T2.professional_id GROUP BY T1.professional_id HAVING count(*) > 2
```

## AL0692

Question: What are the names and number of concerts for each person?

Database: `concert_singer`

```sql
SELECT T1.Name, COUNT(T2.concert_ID) AS number_of_concerts
FROM singer AS T1
INNER JOIN singer_in_concert AS T2 ON T1.Singer_ID = T2.Singer_ID
GROUP BY T1.Name
```

## AL0693

Question: What is the abbreviation of ""JetBlue Airways""?

Database: `flight_2`

```sql
SELECT Abbreviation FROM airlines WHERE Airline = 'JetBlue Airways'
```

## AL0694

Question: Give me the description of the treatment type that is least expensive.

Database: `dog_kennels`

```sql
SELECT T1.treatment_type_description FROM Treatment_Types AS T1 JOIN Treatments AS T2 ON T1.treatment_type_code = T2.treatment_type_code ORDER BY T2.cost_of_treatment ASC LIMIT 1
```

## AL0695

Question: What are the ids and names of all countries that either have more than 3 car makers or produce fiats?

Database: `car_1`

```sql
SELECT T1.CountryId , T1.CountryName FROM COUNTRIES AS T1 JOIN CAR_MAKERS AS T2 ON T1.CountryId = T2.Country GROUP BY T1.CountryId HAVING count(*) > 3 UNION SELECT T1.CountryId , T1.CountryName FROM COUNTRIES AS T1 JOIN CAR_MAKERS AS T2 ON T1.CountryId = T2.Country WHERE T2.Maker = 'fiat'
```

## AL0696

Question: How many countries are republic?

Database: `world_1`

```sql
SELECT COUNT(*) FROM country WHERE GovernmentForm = 'Republic'
```

## AL0697

Question: Find the first name and age of students who have a dog but do not have a cat.

Database: `pets_1`

```sql
SELECT T1.Fname, T1.Age
FROM Student AS T1
INNER JOIN Has_Pet AS T2 ON T1.StuID = T2.StuID
INNER JOIN Pets AS T3 ON T2.PetID = T3.PetID
WHERE T3.PetType = 'dog'
AND T1.StuID NOT IN (
    SELECT T4.StuID
    FROM Has_Pet AS T4
    INNER JOIN Pets AS T5 ON T4.PetID = T5.PetID
    WHERE T5.PetType = 'cat'
)
```

## AL0698

Question: Show the name of the teacher who teaches math .

Database: `course_teach`

```sql
SELECT T.Name
FROM course C
JOIN course_arrange CA ON C.Course_ID = CA.Course_ID
JOIN teacher T ON CA.Teacher_ID = T.Teacher_ID
WHERE C.Course = 'Math'
```

## AL0699

Question: Show different hometown of teachers and the number of teachers from each place.

Database: `course_teach`

```sql
SELECT Hometown , COUNT(*) FROM teacher GROUP BY Hometown
```

## AL0700

Question: How many car models are produced in the usa?

Database: `car_1`

```sql
SELECT COUNT(T3.Model)
FROM car_makers AS T1
INNER JOIN countries AS T2 ON T1.Country = T2.CountryId
INNER JOIN model_list AS T3 ON T1.Id = T3.Maker
WHERE T2.CountryName = 'usa'
```

## AL0701

Question: Give the number of Jetblue Airways flights.

Database: `flight_2`

```sql
SELECT count(*) FROM FLIGHTS AS T1 JOIN AIRLINES AS T2 ON T1.Airline = T2.uid WHERE T2.Airline = "JetBlue Airways"
```

## AL0702

Question: Find the number of left handed winners who participated in the WTA Championships.

Database: `wta_1`

```sql
SELECT count(DISTINCT winner_name) FROM matches WHERE tourney_name = 'WTA Championships' AND winner_hand = 'L'
```

## AL0703

Question: How many flights does 'JetBlue Airways' have?

Database: `flight_2`

```sql
SELECT COUNT(*) FROM flights WHERE Airline = (SELECT uid FROM airlines WHERE Airline = 'JetBlue Airways')
```

## AL0704

Question: What are the names of the countries that are in Europe and have 80000 people?

Database: `world_1`

```sql
SELECT Name
FROM country
WHERE Continent = 'Europe' AND Population = 80000
```

## AL0705

Question: What are the names of nations speak both English and French?

Database: `world_1`

```sql
SELECT T1.Name
FROM country AS T1
INNER JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode
WHERE T2.Language IN ('English', 'French')
GROUP BY T1.Name
HAVING COUNT(DISTINCT T2.Language) = 2
```

## AL0706

Question: Which airlines have departures from CVO but not from APG?

Database: `flight_2`

```sql
SELECT T1.Airline FROM AIRLINES AS T1 JOIN FLIGHTS AS T2 ON T1.uid = T2.Airline WHERE T2.SourceAirport = "CVO" EXCEPT SELECT T1.Airline FROM AIRLINES AS T1 JOIN FLIGHTS AS T2 ON T1.uid = T2.Airline WHERE T2.SourceAirport = "APG"
```

## AL0707

Question: Which distinct car models are the produced after 1980?

Database: `car_1`

```sql
SELECT DISTINCT T1.Model FROM CAR_NAMES AS T1 JOIN CARS_DATA AS T2 ON T1.MakeId = T2.Id WHERE T2.Year > 1980
```

## AL0708

Question: What is the content of Sky Radio?

Database: `tvshow`

```sql
SELECT Content FROM TV_Channel WHERE series_name = 'Sky Radio'
```

## AL0709

Question: Show countries where a singer older than 40 and a singer younger than 30 are from.

Database: `concert_singer`

```sql
SELECT Country FROM singer WHERE Age > 40
INTERSECT
SELECT Country FROM singer WHERE Age < 30
```

## AL0710

Question: Which airlines have departing flights from both APG and CVO ?

Database: `flight_2`

```sql
SELECT T1.Airline FROM AIRLINES AS T1 JOIN FLIGHTS AS T2 ON T1.uid = T2.Airline WHERE T2.SourceAirport = "APG" INTERSECT SELECT T1.Airline FROM AIRLINES AS T1 JOIN FLIGHTS AS T2 ON T1.uid = T2.Airline WHERE T2.SourceAirport = "CVO"
```

## AL0711

Question: Return the id, first name and last name of the person who has the most dogs.

Database: `dog_kennels`

```sql
SELECT T1.owner_id , T2.first_name , T2.last_name FROM Dogs AS T1 JOIN Owners AS T2 ON T1.owner_id = T2.owner_id GROUP BY T1.owner_id ORDER BY count(*) DESC LIMIT 1
```

## AL0712

Question: What is the total population of Gelderland ?

Database: `world_1`

```sql
SELECT SUM(Population) FROM city WHERE District = 'Gelderland'
```

## AL0713

Question: How many TV Channels speak English ?

Database: `tvshow`

```sql
SELECT COUNT(*) FROM TV_Channel WHERE Language = 'English'
```

## AL0714

Question: What are flight numbers of ""United Airlines""?

Database: `flight_2`

```sql
SELECT T2.FlightNo
FROM airlines AS T1
INNER JOIN flights AS T2 ON T1.uid = T2.Airline
WHERE T1.Airline = 'United Airlines'
```

## AL0715

Question: How many car models were produced by American Motor Company?

Database: `car_1`

```sql
SELECT COUNT(T2.Model)
FROM car_makers AS T1
INNER JOIN model_list AS T2 ON T1.Id = T2.Maker
WHERE T1.FullName = 'American Motor Company'
```

## AL0716

Question: What are the first names and country codes for players who won both the WTA Championships and the Australian Open?

Database: `wta_1`

```sql
SELECT DISTINCT T1.first_name , T1.country_code FROM players AS T1 JOIN matches AS T2 ON T1.player_id = T2.winner_id WHERE T2.tourney_name = 'WTA Championships' INTERSECT SELECT DISTINCT T1.first_name , T1.country_code FROM players AS T1 JOIN matches AS T2 ON T1.player_id = T2.winner_id WHERE T2.tourney_name = 'Australian Open'
```

## AL0717

Question: What is the zip code for Port Chelsea?

Database: `student_transcripts_tracking`

```sql
SELECT zip_postcode
FROM Addresses
WHERE city = 'Port Chelsea'
```

## AL0718

Question: What are the codes of countries where Spanish is spoken by the largest percentage of people?

Database: `world_1`

```sql
SELECT CountryCode
FROM countrylanguage
WHERE Language = 'Spanish'
ORDER BY Percentage DESC
LIMIT 1
```

## AL0719

Question: What are the names of all cartoons Ben Jones directs?

Database: `tvshow`

```sql
SELECT Title FROM Cartoon WHERE Directed_by = "Ben Jones"
```

## AL0720

Question: How many concerts are there in  2014 or 2015?

Database: `concert_singer`

```sql
SELECT COUNT(*) FROM concert WHERE Year IN ('2014', '2015')
```

## AL0721

Question: What are flight numbers of flights arriving at Aberdeen?

Database: `flight_2`

```sql
SELECT T1.FlightNo FROM FLIGHTS AS T1 JOIN AIRPORTS AS T2 ON T1.DestAirport = T2.AirportCode WHERE T2.City = "Aberdeen"
```

## AL0722

Question: What car has the most different versions?

Database: `car_1`

```sql
SELECT T1.Make FROM CAR_NAMES AS T1 JOIN MODEL_LIST AS T2 ON T1.Model = T2.Model GROUP BY T1.Make ORDER BY COUNT(*) DESC LIMIT 1
```

## AL0723

Question: What are the different years in which there were cars produced between 3000 and 4000 pounds?

Database: `car_1`

```sql
SELECT DISTINCT Year
FROM cars_data
WHERE Weight BETWEEN 3000 AND 4000
```

## AL0724

Question: What are the names of the dogs for which the owner spent more than 1000 for treatment?

Database: `dog_kennels`

```sql
SELECT T1.name FROM Dogs AS T1 JOIN Treatments AS T2 ON T1.dog_id = T2.dog_id GROUP BY T1.dog_id HAVING sum(T2.cost_of_treatment) > 1000
```

## AL0725

Question: What are the opening year and staff number of Plaza Museum?

Database: `museum_visit`

```sql
SELECT Open_Year, Num_of_Staff
FROM museum
WHERE Name = 'Plaza Museum'
```

## AL0726

Question: What are the countries where either English or Dutch is officially spoken ?

Database: `world_1`

```sql
SELECT T1.Name
FROM country AS T1
INNER JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode
WHERE T2.Language IN ('English', 'Dutch') AND T2.IsOfficial = 'T'
```

## AL0727

Question: Show me the price of the most recently performed treatment.

Database: `dog_kennels`

```sql
SELECT cost_of_treatment FROM Treatments ORDER BY date_of_treatment DESC LIMIT 1
```

## AL0728

Question: Which airlines have a flight from  AHD?

Database: `flight_2`

```sql
SELECT T1.Airline
FROM airlines AS T1
INNER JOIN flights AS T2 ON T1.uid = T2.Airline
WHERE T2.SourceAirport = 'AHD'
```

## AL0729

Question: Find the first name and country code of the oldest player.

Database: `wta_1`

```sql
SELECT first_name, country_code
FROM players
ORDER BY birth_date ASC
LIMIT 1
```

## AL0730

Question: List the first and last name of all players who are left handed  in the order of age.

Database: `wta_1`

```sql
SELECT first_name , last_name FROM players WHERE hand = 'L' ORDER BY birth_date DESC
```

## AL0731

Question: When did A Love of a Lifetime air?

Database: `tvshow`

```sql
SELECT Air_Date FROM TV_series WHERE Episode = 'A Love of a Lifetime'
```

## AL0732

Question: What are the emails of the professionals living in either Hawaii or Wisconsin?

Database: `dog_kennels`

```sql
SELECT email_address
FROM Professionals
WHERE state IN ('Hawaii', 'Wisconsin')
```

## AL0733

Question: What are the names of conductors who are not from ""USA""?

Database: `orchestra`

```sql
SELECT Name FROM conductor WHERE Nationality != "USA"
```

## AL0734

Question: Find the id and zip code of the person who spent the most money in total for his or her dogs.

Database: `dog_kennels`

```sql
SELECT T1.owner_id , T1.zip_code FROM Owners AS T1 JOIN Dogs AS T2 ON T1.owner_id = T2.owner_id JOIN Treatments AS T3 ON T2.dog_id = T3.dog_id GROUP BY T1.owner_id ORDER BY sum(T3.cost_of_treatment) DESC LIMIT 1
```

## AL0735

Question: How many different forms of governments are there in Africa?

Database: `world_1`

```sql
SELECT COUNT(DISTINCT GovernmentForm) FROM country WHERE Continent = 'Africa'
```

## AL0736

Question: How many friends does Kyle have?

Database: `network_1`

```sql
SELECT COUNT(f.friend_id)
FROM Highschooler h
JOIN Friend f ON h.ID = f.student_id
WHERE h.name = 'Kyle'
```

## AL0737

Question: Find the series name and country of the tv channel that is playing some cartoons  Ben Jones and Michael Chang directs?

Database: `tvshow`

```sql
SELECT T1.series_name , T1.country FROM TV_Channel AS T1 JOIN cartoon AS T2 ON T1.id = T2.Channel WHERE T2.directed_by = "Ben Jones, Michael Chang"
```

## AL0738

Question: List the name of singers in ascending order of wealth.

Database: `singer`

```sql
SELECT Name
FROM singer
ORDER BY Net_Worth_Millions ASC
```

## AL0739

Question: Return the number of United Airlines flights leaving from AHD.

Database: `flight_2`

```sql
SELECT COUNT(*)
FROM flights
JOIN airlines ON flights.Airline = airlines.uid
WHERE airlines.Airline = 'United Airlines' AND flights.SourceAirport = 'AHD'
```

## AL0740

Question: How many people are there of each country?

Database: `poker_player`

```sql
SELECT Nationality , COUNT(*) FROM people GROUP BY Nationality
```

## AL0741

Question: Return the number of airlines in the USA.

Database: `flight_2`

```sql
SELECT count(*) FROM AIRLINES WHERE Country = "USA"
```

## AL0742

Question: What is the ship id and name that caused most total injuries?

Database: `battle_death`

```sql
SELECT T1.id , T1.name FROM ship AS T1 JOIN death AS T2 ON T1.id = T2.caused_by_ship_id GROUP BY T1.id ORDER BY sum(T2.injured) DESC LIMIT 1
```

## AL0743

Question: Find the name and age of the people who bought the most tickets at once.

Database: `museum_visit`

```sql
SELECT T1.Name, T1.Age
FROM visitor AS T1
INNER JOIN visit AS T2 ON T1.ID = T2.visitor_ID
ORDER BY T2.Num_of_Ticket DESC
LIMIT 1
```

## AL0744

Question: List the first and last name of all players ordered by their age.

Database: `wta_1`

```sql
SELECT first_name , last_name FROM players ORDER BY birth_date
```

## AL0745

Question: What is the name of the shop that is recruiting the largest number of employees?

Database: `employee_hire_evaluation`

```sql
SELECT T1.Name
FROM shop AS T1
INNER JOIN hiring AS T2 ON T1.Shop_ID = T2.Shop_ID
GROUP BY T1.Shop_ID
ORDER BY COUNT(T2.Employee_ID) DESC
LIMIT 1
```

## AL0746

Question: Find the last name of the students who currently live in North Carolina but have not registered in any degree program.

Database: `student_transcripts_tracking`

```sql
SELECT T1.last_name
FROM Students AS T1
INNER JOIN Addresses AS T2 ON T1.current_address_id = T2.address_id
WHERE T2.state_province_county = 'North Carolina'
  AND T1.student_id NOT IN (SELECT student_id FROM Student_Enrolment)
```

## AL0747

Question: Find the name of students who have both cat and dog.

Database: `pets_1`

```sql
SELECT T1.Fname, T1.LName
FROM Student AS T1
INNER JOIN Has_Pet AS T2 ON T1.StuID = T2.StuID
INNER JOIN Pets AS T3 ON T2.PetID = T3.PetID
WHERE T3.PetType IN ('cat', 'dog')
GROUP BY T1.StuID, T1.Fname, T1.LName
HAVING COUNT(DISTINCT T3.PetType) = 2
```

## AL0748

Question: Show different nationalities and the maximum net worth of singers of country.

Database: `singer`

```sql
SELECT Citizenship , max(Net_Worth_Millions) FROM singer GROUP BY Citizenship
```

## AL0749

Question: Find the first names of owners living in Virginia and the names of dogs they own.

Database: `dog_kennels`

```sql
SELECT T1.first_name , T2.name FROM Owners AS T1 JOIN Dogs AS T2 ON T1.owner_id = T2.owner_id WHERE T1.state = 'Virginia'
```

## AL0750

Question: What are the countries that have greater surface area than any country in Europe?

Database: `world_1`

```sql
SELECT Name
FROM country
WHERE SurfaceArea > (
    SELECT MIN(SurfaceArea)
    FROM country
    WHERE Continent = 'Europe'
)
```

## AL0751

Question: What are the country code and first name of the players who won in both WTA Championships and Australian Open?

Database: `wta_1`

```sql
SELECT T3.country_code, T3.first_name
FROM matches AS T1
INNER JOIN players AS T3 ON T1.winner_id = T3.player_id
WHERE T1.tourney_name IN ('WTA Championships', 'Australian Open')
GROUP BY T3.country_code, T3.first_name
HAVING COUNT(DISTINCT T1.tourney_name) = 2
```

## AL0752

Question: List the number of all matches who played in 2013 or 2016.

Database: `wta_1`

```sql
SELECT COUNT(*) FROM matches WHERE year IN (2013, 2016)
```

## AL0753

Question: Return the names of non USA conductors.

Database: `orchestra`

```sql
SELECT Name
FROM conductor
WHERE Nationality != 'USA'
```

## AL0754

Question: Show distinct names of singers that have songs sell  more than 300000.

Database: `singer`

```sql
SELECT DISTINCT T1.Name FROM singer AS T1 JOIN song AS T2 ON T1.Singer_ID = T2.Singer_ID WHERE T2.Sales > 300000
```

## AL0755

Question: Sort all the shops by amount of merchandise in descending order, and return the name, location and district of each shop.

Database: `employee_hire_evaluation`

```sql
SELECT name , LOCATION , district FROM shop ORDER BY number_products DESC
```

## AL0756

Question: What is the number of car models that are produced by each company and what is the id and full name of each maker?

Database: `car_1`

```sql
SELECT T1.Id , T1.FullName , count(*) FROM CAR_MAKERS AS T1 JOIN MODEL_LIST AS T2 ON T1.Id = T2.Maker GROUP BY T1.Id
```

## AL0757

Question: What are the names and number of concerts for each person?

Database: `concert_singer`

```sql
SELECT T2.name , count(*) FROM singer_in_concert AS T1 JOIN singer AS T2 ON T1.singer_id = T2.singer_id GROUP BY T2.singer_id
```

## AL0758

Question: What is the last name of the student who has a cat that is 3 years old?

Database: `pets_1`

```sql
SELECT T1.LName
FROM Student AS T1
INNER JOIN Has_Pet AS T2 ON T1.StuID = T2.StuID
INNER JOIN Pets AS T3 ON T2.PetID = T3.PetID
WHERE T3.PetType = 'cat' AND T3.pet_age = 3
```

## AL0759

Question: Show different nationalities of singers and the number of singers of each.

Database: `singer`

```sql
SELECT Citizenship, COUNT(*) FROM singer GROUP BY Citizenship
```

## AL0760

Question: find the package option of the tv channel that do not have any cartoon  Ben Jones directs.

Database: `tvshow`

```sql
SELECT Package_Option
FROM TV_Channel
WHERE id NOT IN (
    SELECT Channel
    FROM Cartoon
    WHERE Directed_by = 'Ben Jones'
)
```

## AL0761

Question: What is the mobile phone number of the student named Timmothy Ward ?

Database: `student_transcripts_tracking`

```sql
SELECT cell_mobile_number FROM Students WHERE first_name = 'Timmothy' AND last_name = 'Ward'
```

## AL0762

Question: What is average life expectancy in the countries where English is not used officially ?

Database: `world_1`

```sql
SELECT avg(LifeExpectancy) FROM country WHERE Name NOT IN (SELECT T1.Name FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode WHERE T2.IsOfficial = 'T' AND T2.Language = "English")
```

## AL0763

Question: Return the id, first name and last name of the person who has the most dogs.

Database: `dog_kennels`

```sql
SELECT T1.owner_id, T1.first_name, T1.last_name
FROM Owners AS T1
INNER JOIN Dogs AS T2 ON T1.owner_id = T2.owner_id
GROUP BY T1.owner_id, T1.first_name, T1.last_name
ORDER BY COUNT(T2.dog_id) DESC
LIMIT 1
```

## AL0764

Question: Count the number of United Airlines flights arriving in ASY.

Database: `flight_2`

```sql
SELECT COUNT(*)
FROM flights
JOIN airlines ON flights.Airline = airlines.uid
WHERE airlines.Airline = 'United Airlines' AND flights.DestAirport = 'ASY'
```

## AL0765

Question: How many type of governments are in Africa?

Database: `world_1`

```sql
SELECT count(DISTINCT GovernmentForm) FROM country WHERE continent = "Africa"
```

## AL0766

Question: Give the names of nations that speak both English and French.

Database: `world_1`

```sql
SELECT T1.Name
FROM country AS T1
INNER JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode AND T2.Language = 'English'
INNER JOIN countrylanguage AS T3 ON T1.Code = T3.CountryCode AND T3.Language = 'French'
```

## AL0767

Question: What is the name for AKO?

Database: `flight_2`

```sql
SELECT AirportName FROM AIRPORTS WHERE AirportCode = "AKO"
```

## AL0768

Question: How many 'United Airlines' flights go to 'ASY'?

Database: `flight_2`

```sql
SELECT COUNT(*)
FROM flights
JOIN airlines ON flights.Airline = airlines.uid
WHERE airlines.Airline = 'United Airlines' AND flights.DestAirport = 'ASY'
```

## AL0769

Question: Find the semester when both Master students and Bachelor students got enrolled in.

Database: `student_transcripts_tracking`

```sql
SELECT T1.semester_id FROM student_enrolment AS T1 JOIN degree_programs AS T2 ON T1.degree_program_id = T2.degree_program_id WHERE T2.degree_summary_name = 'Master' INTERSECT SELECT T1.semester_id FROM student_enrolment AS T1 JOIN degree_programs AS T2 ON T1.degree_program_id = T2.degree_program_id WHERE T2.degree_summary_name = 'Bachelor'
```

## AL0770

Question: Give the airline called UAL.

Database: `flight_2`

```sql
SELECT Airline FROM airlines WHERE Abbreviation = 'UAL'
```

## AL0771

Question: Which doctors have done at least two treatments? List theid, role, and first name.

Database: `dog_kennels`

```sql
SELECT T1.professional_id, T1.role_code, T1.first_name
FROM Professionals AS T1
INNER JOIN Treatments AS T2 ON T1.professional_id = T2.professional_id
GROUP BY T1.professional_id, T1.role_code, T1.first_name
HAVING COUNT(T2.treatment_id) >= 2
```

## AL0772

Question: What major is every student who does not own a cat, and also how old are they?

Database: `pets_1`

```sql
SELECT major , age FROM student WHERE stuid NOT IN (SELECT T1.stuid FROM has_pet AS T1 JOIN pets AS T2 ON T1.petid = T2.petid WHERE T2.pettype = 'cat')
```

## AL0773

Question: What are the names of the teachers whose courses have not been assigned?

Database: `course_teach`

```sql
SELECT Name
FROM teacher
WHERE Teacher_ID NOT IN (SELECT Teacher_ID FROM course_arrange)
```

## AL0774

Question: What are flight numbers of flights departing from APG?

Database: `flight_2`

```sql
SELECT FlightNo FROM flights WHERE SourceAirport = 'APG'
```

## AL0775

Question: How many shops are there in each place?

Database: `employee_hire_evaluation`

```sql
SELECT count(*) , LOCATION FROM shop GROUP BY LOCATION
```

## AL0776

Question: What is the name of the nation with the most car makers?

Database: `car_1`

```sql
SELECT T2.CountryName
FROM car_makers AS T1
INNER JOIN countries AS T2 ON T1.Country = T2.CountryId
GROUP BY T2.CountryName
ORDER BY COUNT(T1.Id) DESC
LIMIT 1
```

## AL0777

Question: Give the flight numbers of flights leaving from APG.

Database: `flight_2`

```sql
SELECT FlightNo FROM FLIGHTS WHERE SourceAirport = "APG"
```

## AL0778

Question: What are the names of the winner and loser who played in the longest match?

Database: `wta_1`

```sql
SELECT winner_name , loser_name FROM matches ORDER BY minutes DESC LIMIT 1
```

## AL0779

Question: Find the names of stores that have more than average goods.

Database: `employee_hire_evaluation`

```sql
SELECT name FROM shop WHERE number_products > (SELECT avg(number_products) FROM shop)
```

## AL0780

Question: What are the country codes for countries that do not speak English?

Database: `world_1`

```sql
SELECT Code FROM country EXCEPT SELECT CountryCode FROM countrylanguage WHERE LANGUAGE = "English"
```

## AL0781

Question: Which person has the most dogs? List the id, first name and last name.

Database: `dog_kennels`

```sql
SELECT T1.owner_id , T1.first_name , T1.last_name FROM Owners AS T1 JOIN Dogs AS T2 ON T1.owner_id = T2.owner_id GROUP BY T1.owner_id ORDER BY count(*) DESC LIMIT 1
```

## AL0782

Question: How many pets are owned by students that are older than 20?

Database: `pets_1`

```sql
SELECT COUNT(HP.PetID)
FROM Student S
INNER JOIN Has_Pet HP ON S.StuID = HP.StuID
WHERE S.Age > 20
```

## AL0783

Question: Which manufacturers designed more than 3 car models? List full name and the id.

Database: `car_1`

```sql
SELECT T1.FullName, T1.Id
FROM car_makers AS T1
INNER JOIN model_list AS T2 ON T1.Id = T2.Maker
GROUP BY T1.Id, T1.FullName
HAVING COUNT(T2.Model) > 3
```

## AL0784

Question: Find the last name of the student who has a cat that is 3 years old.

Database: `pets_1`

```sql
SELECT T1.lname FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid = T2.stuid JOIN pets AS T3 ON T3.petid = T2.petid WHERE T3.pet_age = 3 AND T3.pettype = 'cat'
```

## AL0785

Question: Who is the student register earliest? List the first name, middle name and last name.

Database: `student_transcripts_tracking`

```sql
SELECT first_name , middle_name , last_name FROM Students ORDER BY date_first_registered ASC LIMIT 1
```

## AL0786

Question: Which cities do more than one employee younger than 30 come from?

Database: `employee_hire_evaluation`

```sql
SELECT city FROM employee WHERE age < 30 GROUP BY city HAVING count(*) > 1
```

## AL0787

Question: Give the names of nations that speak both English and French.

Database: `world_1`

```sql
SELECT T1.Name FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode WHERE T2.Language = "English" INTERSECT SELECT T1.Name FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode WHERE T2.Language = "French"
```

## AL0788

Question: What are the names of the stadiums without any concerts?

Database: `concert_singer`

```sql
SELECT Name
FROM stadium
WHERE Stadium_ID NOT IN (SELECT Stadium_ID FROM concert)
```

## AL0789

Question: How many 'United Airlines' flights depart from 'AHD'?

Database: `flight_2`

```sql
SELECT COUNT(*)
FROM flights
JOIN airlines ON flights.Airline = airlines.uid
WHERE airlines.Airline = 'United Airlines' AND flights.SourceAirport = 'AHD'
```

## AL0790

Question: find the id, name and age for people who visited some museums more than once.

Database: `museum_visit`

```sql
SELECT T1.ID, T1.Name, T1.Age
FROM visitor AS T1
INNER JOIN visit AS T2 ON T1.ID = T2.visitor_ID
GROUP BY T2.visitor_ID
HAVING COUNT(T2.visitor_ID) > 1
```

## AL0791

Question: List the airport code and name in Anthony.

Database: `flight_2`

```sql
SELECT AirportCode, AirportName
FROM airports
WHERE City = 'Anthony'
```

## AL0792

Question: How many car models are produced by each manufacturer? List the count and the maker full name.

Database: `car_1`

```sql
SELECT count(*) , T1.FullName FROM CAR_MAKERS AS T1 JOIN MODEL_LIST AS T2 ON T1.Id = T2.Maker GROUP BY T1.FullName
```

## AL0793

Question: What major is every student who does not own a cat, and also how old are they?

Database: `pets_1`

```sql
SELECT Major, Age
FROM Student
WHERE StuID NOT IN (
    SELECT StuID
    FROM Has_Pet
    JOIN Pets ON Has_Pet.PetID = Pets.PetID
    WHERE Pets.PetType = 'cat'
)
```

## AL0794

Question: How many high schoolers are in each year?

Database: `network_1`

```sql
SELECT grade, COUNT(*) FROM Highschooler GROUP BY grade
```

## AL0795

Question: Count the number of United Airlines flights that arrive in Aberdeen.

Database: `flight_2`

```sql
SELECT count(*) FROM FLIGHTS AS T1 JOIN AIRPORTS AS T2 ON T1.DestAirport = T2.AirportCode JOIN AIRLINES AS T3 ON T3.uid = T1.Airline WHERE T2.City = "Aberdeen" AND T3.Airline = "United Airlines"
```

## AL0796

Question: Count the number of countries in Asia.

Database: `world_1`

```sql
SELECT count(*) FROM country WHERE continent = "Asia"
```

## AL0797

Question: Which manufacturers designed more than 3 car models? List full name and the id.

Database: `car_1`

```sql
SELECT T2.FullName , T1.Maker FROM CAR_MAKERS AS T2 JOIN MODEL_LIST AS T1 ON T1.Maker = T2.Id GROUP BY T1.Maker HAVING count(*) > 3
```

## AL0798

Question: What is the TV Channel with """"A Love of a Lifetime""""? List the TV Channel's series name.

Database: `tvshow`

```sql
SELECT T2.series_name
FROM TV_series AS T1
INNER JOIN TV_Channel AS T2 ON T1.Channel = T2.id
WHERE T1.Episode = 'A Love of a Lifetime'
```

## AL0799

Question: What region is Kabul in?

Database: `world_1`

```sql
SELECT T1.Region FROM country AS T1 JOIN city AS T2 ON T1.Code = T2.CountryCode WHERE T2.Name = "Kabul"
```

## AL0800

Question: When did A Love of a Lifetime air?

Database: `tvshow`

```sql
SELECT Air_Date FROM TV_series WHERE Episode = "A Love of a Lifetime"
```

## AL0801

Question: Show countries where a singer older than 40 and a singer younger than 30 are from.

Database: `concert_singer`

```sql
SELECT country FROM singer WHERE age > 40 INTERSECT SELECT country FROM singer WHERE age < 30
```

## AL0802

Question: Give the names of the nations that were founded after 1950.

Database: `world_1`

```sql
SELECT Name FROM country WHERE IndepYear > 1950
```

## AL0803

Question: What is last date created of votes from 'CA'?

Database: `voter_1`

```sql
SELECT max(created) FROM votes WHERE state = 'CA'
```

## AL0804

Question: What are the African countries that have less people than any country in Asia?

Database: `world_1`

```sql
SELECT Name FROM country WHERE Continent = "Africa" AND population < (SELECT max(population) FROM country WHERE Continent = "Asia")
```

## AL0805

Question: Find all airlines that have flights from both APG and CVO.

Database: `flight_2`

```sql
SELECT T1.Airline
FROM airlines AS T1
INNER JOIN flights AS T2 ON T1.uid = T2.Airline
WHERE T2.SourceAirport IN ('APG', 'CVO')
GROUP BY T1.Airline
HAVING COUNT(DISTINCT T2.SourceAirport) = 2
```

## AL0806

Question: Show the stadium names without any concert.

Database: `concert_singer`

```sql
SELECT name FROM stadium WHERE stadium_id NOT IN (SELECT stadium_id FROM concert)
```

## AL0807

Question: Give the mean GNP and total population of nations which are considered US territory.

Database: `world_1`

```sql
SELECT AVG(GNP) AS MeanGNP, SUM(Population) AS TotalPopulation
FROM country
WHERE Region = 'Caribbean'
```

## AL0808

Question: What are the number of concerts that occurred in the stadium with space for the most people?

Database: `concert_singer`

```sql
SELECT count(*) FROM concert WHERE stadium_id = (SELECT stadium_id FROM stadium ORDER BY capacity DESC LIMIT 1)
```

## AL0809

Question: What type of pet is the youngest animal, and how much does it weigh?

Database: `pets_1`

```sql
SELECT pettype , weight FROM pets ORDER BY pet_age LIMIT 1
```

## AL0810

Question: For a volvo , how many cylinders does the version with least accelerate have?

Database: `car_1`

```sql
SELECT T3.Cylinders
FROM car_makers AS T1
INNER JOIN model_list AS T2 ON T1.Id = T2.Maker
INNER JOIN car_names AS T4 ON T2.Model = T4.Model
INNER JOIN cars_data AS T3 ON T4.MakeId = T3.Id
WHERE T1.Maker = 'volvo'
ORDER BY T3.Accelerate ASC
LIMIT 1
```

## AL0811

Question: Give the flight numbers of flights arriving in Aberdeen.

Database: `flight_2`

```sql
SELECT T1.FlightNo
FROM flights AS T1
INNER JOIN airports AS T2 ON T1.DestAirport = T2.AirportCode
WHERE T2.City = 'Aberdeen'
```

## AL0812

Question: What car has the most different versions?

Database: `car_1`

```sql
SELECT Model
FROM car_names
GROUP BY Model
ORDER BY COUNT(Model) DESC
LIMIT 1
```

## AL0813

Question: How many TV Channel using  English?

Database: `tvshow`

```sql
SELECT count(*) FROM TV_Channel WHERE LANGUAGE = "English"
```

## AL0814

Question: What are the number of votes from 'NY' or 'CA'?

Database: `voter_1`

```sql
SELECT count(*) FROM votes WHERE state = 'NY' OR state = 'CA'
```

## AL0815

Question: Find the major and age of students who do not have a cat.

Database: `pets_1`

```sql
SELECT major , age FROM student WHERE stuid NOT IN (SELECT T1.stuid FROM has_pet AS T1 JOIN pets AS T2 ON T1.petid = T2.petid WHERE T2.pettype = 'cat')
```

## AL0816

Question: find the package option of the tv channel that do not have any cartoon  Ben Jones directs.

Database: `tvshow`

```sql
SELECT package_option FROM TV_Channel WHERE id NOT IN (SELECT channel FROM cartoon WHERE directed_by = 'Ben Jones')
```

## AL0817

Question: What is the total number of people living in the nations that do not use English?

Database: `world_1`

```sql
SELECT SUM(T1.Population) AS TotalPopulation
FROM country AS T1
WHERE T1.Code NOT IN (
    SELECT CountryCode
    FROM countrylanguage
    WHERE Language = 'English'
)
```

## AL0818

Question: What is the name of the museum that had no person come yet?

Database: `museum_visit`

```sql
SELECT name FROM museum WHERE Museum_ID NOT IN (SELECT museum_id FROM visit)
```

## AL0819

Question: List all airline names and their abbreviations in ""USA"".

Database: `flight_2`

```sql
SELECT Airline , Abbreviation FROM AIRLINES WHERE Country = "USA"
```

## AL0820

Question: How many flights depart from Aberdeen?

Database: `flight_2`

```sql
SELECT count(*) FROM FLIGHTS AS T1 JOIN AIRPORTS AS T2 ON T1.SourceAirport = T2.AirportCode WHERE T2.City = "Aberdeen"
```

## AL0821

Question: Find the weight of the youngest dog.

Database: `pets_1`

```sql
SELECT weight
FROM Pets
WHERE PetType = 'dog'
ORDER BY pet_age ASC
LIMIT 1
```

## AL0822

Question: What are the manager name and district of the shop that sells the most merchandise?

Database: `employee_hire_evaluation`

```sql
SELECT manager_name , district FROM shop ORDER BY number_products DESC LIMIT 1
```

## AL0823

Question: Return the number of flights departing from Aberdeen.

Database: `flight_2`

```sql
SELECT count(*) FROM FLIGHTS AS T1 JOIN AIRPORTS AS T2 ON T1.SourceAirport = T2.AirportCode WHERE T2.City = "Aberdeen"
```

## AL0824

Question: How many flights depart from APG?

Database: `flight_2`

```sql
SELECT COUNT(*) FROM flights WHERE SourceAirport = 'APG'
```

## AL0825

Question: find the names of loser and winner who played in the match that last for the longest of time.

Database: `wta_1`

```sql
SELECT loser_name, winner_name
FROM matches
ORDER BY minutes DESC
LIMIT 1
```

## AL0826

Question: What are the id and names of the countries which have more than 3 car makers or produce the 'fiat' ?

Database: `car_1`

```sql
SELECT T1.CountryId , T1.CountryName FROM COUNTRIES AS T1 JOIN CAR_MAKERS AS T2 ON T1.CountryId = T2.Country GROUP BY T1.CountryId HAVING count(*) > 3 UNION SELECT T1.CountryId , T1.CountryName FROM COUNTRIES AS T1 JOIN CAR_MAKERS AS T2 ON T1.CountryId = T2.Country WHERE T2.Maker = 'fiat'
```

## AL0827

Question: What are the emails of the professionals living in either Hawaii or Wisconsin?

Database: `dog_kennels`

```sql
SELECT email_address FROM professionals WHERE state = 'Hawaii' OR state = 'Wisconsin'
```

## AL0828

Question: Which of the nations has the most car makers? List the country name.

Database: `car_1`

```sql
SELECT T1.CountryName FROM COUNTRIES AS T1 JOIN CAR_MAKERS AS T2 ON T1.CountryId = T2.Country GROUP BY T1.CountryName ORDER BY Count(*) DESC LIMIT 1
```

## AL0829

Question: What are the population and life expectancies in Brazil?

Database: `world_1`

```sql
SELECT Population, LifeExpectancy
FROM country
WHERE Name = 'Brazil'
```

## AL0830

Question: which countries' tv channels are not playing any cartoon  Todd Casey writes?

Database: `tvshow`

```sql
SELECT country FROM tv_channel WHERE id NOT IN (SELECT channel FROM cartoon WHERE written_by = 'Todd Casey')
```

## AL0831

Question: What are the airline names and abbreviations for airlines in the USA?

Database: `flight_2`

```sql
SELECT Airline , Abbreviation FROM AIRLINES WHERE Country = "USA"
```

## AL0832

Question: Find the first names of owners living in Virginia and the names of dogs they own.

Database: `dog_kennels`

```sql
SELECT T1.first_name, T2.name
FROM Owners AS T1
INNER JOIN Dogs AS T2 ON T1.owner_id = T2.owner_id
WHERE T1.state = 'Virginia'
```

## AL0833

Question: What are the names and ranks of the three youngest victors across all matches?

Database: `wta_1`

```sql
SELECT DISTINCT winner_name , winner_rank FROM matches ORDER BY winner_age LIMIT 3
```

## AL0834

Question: Find the name of the winner who has the highest rank points and participated in the Australian Open.

Database: `wta_1`

```sql
SELECT winner_name
FROM matches
WHERE tourney_name = 'Australian Open'
ORDER BY winner_rank_points DESC
LIMIT 1
```

## AL0835

Question: What is the total population and average area of countries in North America who is bigger than 3000 square miles

Database: `world_1`

```sql
SELECT SUM(Population) AS TotalPopulation, AVG(SurfaceArea) AS AverageArea
FROM country
WHERE Continent = 'North America' AND SurfaceArea > 3000
```

## AL0836

Question: What is the hometown of the youngest teacher?

Database: `course_teach`

```sql
SELECT Hometown
FROM teacher
ORDER BY CAST(Age AS INTEGER) ASC
LIMIT 1
```

## AL0837

Question: What are the number of votes from 'NY' or 'CA'?

Database: `voter_1`

```sql
SELECT COUNT(*) FROM VOTES WHERE state IN ('NY', 'CA')
```

## AL0838

Question: What are the names of all high schoolers in  10?

Database: `network_1`

```sql
SELECT name
FROM Highschooler
WHERE grade = 10
```

## AL0839

Question: What is the nation with the most number of TV Channels and how many does it have?

Database: `tvshow`

```sql
SELECT country , count(*) FROM tv_channel GROUP BY country ORDER BY count(*) DESC LIMIT 1
```

## AL0840

Question: Find the average number of staff working for the museums that were open before 2009.

Database: `museum_visit`

```sql
SELECT avg(num_of_staff) FROM museum WHERE open_year < 2009
```

## AL0841

Question: How many official languages are spoken in Afghanistan?

Database: `world_1`

```sql
SELECT COUNT(*) FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode WHERE T1.Name = "Afghanistan" AND IsOfficial = "T"
```

## AL0842

Question: How many countries are republic?

Database: `world_1`

```sql
SELECT count(*) FROM country WHERE GovernmentForm = "Republic"
```

## AL0843

Question: What is the name of the different car makers who produced a car in 1970?

Database: `car_1`

```sql
SELECT DISTINCT T1.Maker
FROM car_makers AS T1
INNER JOIN model_list AS T2 ON T1.Id = T2.Maker
INNER JOIN car_names AS T3 ON T2.Model = T3.Model
INNER JOIN cars_data AS T4 ON T3.MakeId = T4.Id
WHERE T4.Year = 1970
```

## AL0844

Question: What is the most populace city that speaks English?

Database: `world_1`

```sql
SELECT T1.Name
FROM city AS T1
INNER JOIN countrylanguage AS T2 ON T1.CountryCode = T2.CountryCode
WHERE T2.Language = 'English'
ORDER BY T1.Population DESC
LIMIT 1
```

## AL0845

Question: Which shop has the most employees? Give me the shop name.

Database: `employee_hire_evaluation`

```sql
SELECT t1.name FROM shop AS t1 JOIN hiring AS t2 ON t1.shop_id = t2.shop_id GROUP BY t1.shop_id ORDER BY count(*) DESC LIMIT 1
```

## AL0846

Question: What is the name of the singer with the largest wealth?

Database: `singer`

```sql
SELECT Name FROM singer ORDER BY Net_Worth_Millions DESC LIMIT 1
```

## AL0847

Question: List the names of teachers who have not been assigned to teach courses.

Database: `course_teach`

```sql
SELECT Name FROM teacher WHERE Teacher_ID NOT IN (SELECT Teacher_ID FROM course_arrange)
```

## AL0848

Question: Which African countries have fewer people than that of any country in Asia?

Database: `world_1`

```sql
SELECT Name FROM country WHERE Continent = "Africa" AND population < (SELECT max(population) FROM country WHERE Continent = "Asia")
```

## AL0849

Question: How many car models were produced by American Motor Company?

Database: `car_1`

```sql
SELECT count(*) FROM CAR_MAKERS AS T1 JOIN MODEL_LIST AS T2 ON T1.Id = T2.Maker WHERE T1.FullName = 'American Motor Company'
```

## AL0850

Question: How long is the people’s average life expectancy in Central Africa?

Database: `world_1`

```sql
SELECT AVG(LifeExpectancy) FROM country WHERE Region = 'Central Africa'
```

## AL0851

Question: What is the average edispl for all volvos?

Database: `car_1`

```sql
SELECT AVG(T3.Edispl)
FROM car_makers AS T1
INNER JOIN model_list AS T2 ON T1.Id = T2.Maker
INNER JOIN car_names AS T4 ON T2.Model = T4.Model
INNER JOIN cars_data AS T3 ON T4.MakeId = T3.Id
WHERE T1.Maker = 'volvo'
```

## AL0852

Question: Give the name of the country in Asia with the lowest life expectancy.

Database: `world_1`

```sql
SELECT Name FROM country WHERE Continent = "Asia" ORDER BY LifeExpectancy LIMIT 1
```

## AL0853

Question: How many car models are produced by each manufacturer? List the count and the maker full name.

Database: `car_1`

```sql
SELECT T1.FullName, COUNT(T2.Model) AS ModelCount
FROM car_makers AS T1
INNER JOIN model_list AS T2 ON T1.Id = T2.Maker
GROUP BY T1.FullName
```

## AL0854

Question: What are the names of tournaments that have more than 10 matches?

Database: `wta_1`

```sql
SELECT tourney_name FROM matches GROUP BY tourney_name HAVING count(*) > 10
```

## AL0855

Question: What are the ids of the students who do not own cats?

Database: `pets_1`

```sql
SELECT StuID FROM student EXCEPT SELECT T1.StuID FROM has_pet AS T1 JOIN pets AS T2 ON T1.petid = T2.petid WHERE T2.pettype = 'cat'
```

## AL0856

Question: What is the code of the nation with the most players?

Database: `wta_1`

```sql
SELECT country_code FROM players GROUP BY country_code ORDER BY count(*) DESC LIMIT 1
```

## AL0857

Question: What is Kyle's id?

Database: `network_1`

```sql
SELECT ID FROM Highschooler WHERE name = 'Kyle'
```

## AL0858

Question: Find number of pets owned by students who are older than 20.

Database: `pets_1`

```sql
SELECT count(*) FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid = T2.stuid WHERE T1.age > 20
```

## AL0859

Question: What are the names of the teachers  from youngest to oldest?

Database: `course_teach`

```sql
SELECT Name FROM teacher ORDER BY Age ASC
```

## AL0860

Question: What are the record companies of orchestras in descending order of time in which they started?

Database: `orchestra`

```sql
SELECT Record_Company FROM orchestra ORDER BY Year_of_Founded DESC
```

## AL0861

Question: What languages are only used by a single republic country?

Database: `world_1`

```sql
SELECT T2.Language FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode WHERE T1.GovernmentForm = "Republic" GROUP BY T2.Language HAVING COUNT(*) = 1
```

## AL0862

Question: How many flights land in Aberdeen or Abilene?

Database: `flight_2`

```sql
SELECT COUNT(*)
FROM flights
WHERE DestAirport IN (
    SELECT AirportCode
    FROM airports
    WHERE City IN ('Aberdeen', 'Abilene')
)
```

## AL0863

Question: What is the average expected life expectancy for countries in Central Africa?

Database: `world_1`

```sql
SELECT AVG(LifeExpectancy)
FROM country
WHERE Region = 'Central Africa'
```

## AL0864

Question: Find the name of the employee who got the highest one time incentive.

Database: `employee_hire_evaluation`

```sql
SELECT e.Name
FROM employee e
INNER JOIN evaluation ev ON e.Employee_ID = ev.Employee_ID
ORDER BY ev.Bonus DESC
LIMIT 1
```

## AL0865

Question: What are the cities who have more than 160000 people and less than 900000 people?

Database: `world_1`

```sql
select name from city where population between 160000 and 900000
```

## AL0866

Question: Which regions speak Dutch or English?

Database: `world_1`

```sql
SELECT DISTINCT T1.Region FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode WHERE T2.Language = "Dutch" OR T2.Language = "English"
```

## AL0867

Question: What are the names and ids of all nations with at least one car maker?

Database: `car_1`

```sql
SELECT DISTINCT T1.CountryName, T1.CountryId
FROM countries AS T1
INNER JOIN car_makers AS T2 ON T1.CountryId = T2.Country
```

## AL0868

Question: Which year has the most high schoolers?

Database: `network_1`

```sql
SELECT grade FROM Highschooler GROUP BY grade ORDER BY count(*) DESC LIMIT 1
```

## AL0869

Question: How many flights does 'JetBlue Airways' have?

Database: `flight_2`

```sql
SELECT count(*) FROM FLIGHTS AS T1 JOIN AIRLINES AS T2 ON T1.Airline = T2.uid WHERE T2.Airline = "JetBlue Airways"
```

## AL0870

Question: How many models does each manufacturer produce? List maker full name, id and the number.

Database: `car_1`

```sql
SELECT T1.FullName , T1.Id , count(*) FROM CAR_MAKERS AS T1 JOIN MODEL_LIST AS T2 ON T1.Id = T2.Maker GROUP BY T1.Id
```

## AL0871

Question: How many friends does Kyle have?

Database: `network_1`

```sql
SELECT COUNT(*) FROM Friend WHERE student_id = (SELECT ID FROM Highschooler WHERE name = 'Kyle')
```

## AL0872

Question: What is the average, minimum, and maximum age of all singers from France?

Database: `concert_singer`

```sql
SELECT avg(age) , min(age) , max(age) FROM singer WHERE country = 'France'
```

## AL0873

Question: What are the ids of the students who do not own cats?

Database: `pets_1`

```sql
SELECT StuID
FROM Student
WHERE StuID NOT IN (
    SELECT T1.StuID
    FROM Has_Pet AS T1
    INNER JOIN Pets AS T2 ON T1.PetID = T2.PetID
    WHERE T2.PetType = 'cat'
)
```

## AL0874

Question: Which models are lighter than 3500 but not built by the 'Ford Motor Company'?

Database: `car_1`

```sql
SELECT T1.Model FROM CAR_NAMES AS T1 JOIN CARS_DATA AS T2 ON T1.MakeId = T2.Id JOIN MODEL_LIST AS T3 ON T1.Model = T3.Model JOIN CAR_MAKERS AS T4 ON T3.Maker = T4.Id WHERE T2.Weight < 3500 EXCEPT SELECT T1.Model FROM CAR_NAMES AS T1 JOIN CARS_DATA AS T2 ON T1.MakeId = T2.Id JOIN MODEL_LIST AS T3 ON T1.Model = T3.Model JOIN CAR_MAKERS AS T4 ON T3.Maker = T4.Id WHERE T4.FullName = 'Ford Motor Company'
```

## AL0875

Question: What are the countries where either English or Dutch is officially spoken ?

Database: `world_1`

```sql
SELECT T1.Name FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode WHERE T2.IsOfficial = "T" AND T2.Language = "English" UNION SELECT T1.Name FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode WHERE T2.IsOfficial = "T" AND T2.Language = "Dutch"
```

## AL0876

Question: What are the id and name of the museum that has people come most times?

Database: `museum_visit`

```sql
SELECT t1.museum_id , t2.name FROM visit AS t1 JOIN museum AS t2 ON t1.museum_id = t2.museum_id GROUP BY t1.museum_id ORDER BY count(*) DESC LIMIT 1
```

## AL0877

Question: How many cities in each district have more number of people than average?

Database: `world_1`

```sql
SELECT District, COUNT(*) AS Count
FROM city
WHERE Population > (SELECT AVG(Population) FROM city)
GROUP BY District
```

## AL0878

Question: What is the Package Option of TV Channel with ""Sky Radio""?

Database: `tvshow`

```sql
SELECT Package_Option FROM TV_Channel WHERE series_name = 'Sky Radio'
```

## AL0879

Question: List all singer names in concerts in  2014.

Database: `concert_singer`

```sql
SELECT T1.Name FROM singer AS T1 JOIN singer_in_concert AS T2 ON T1.Singer_ID = T2.Singer_ID JOIN concert AS T3 ON T2.concert_ID = T3.concert_ID WHERE T3.year = 2014
```

## AL0880

Question: Find all airlines that have flights from 'CVO' but not from 'APG'.

Database: `flight_2`

```sql
SELECT T1.Airline
FROM airlines AS T1
INNER JOIN flights AS T2 ON T1.uid = T2.Airline
WHERE T2.SourceAirport = 'CVO'
AND T1.uid NOT IN (
    SELECT Airline
    FROM flights
    WHERE SourceAirport = 'APG'
)
```

## AL0881

Question: What is the average horsepower for all cards produced before 1980?

Database: `car_1`

```sql
SELECT AVG(CAST(Horsepower AS REAL)) AS AverageHorsepower
FROM cars_data
WHERE Year < 1980
```

## AL0882

Question: What are the different models wthat are lighter than 3500 but were not built by the Ford Motor Company?

Database: `car_1`

```sql
SELECT DISTINCT T1.Model
FROM car_names AS T1
INNER JOIN cars_data AS T2 ON T1.MakeId = T2.Id
INNER JOIN model_list AS T3 ON T1.Model = T3.Model
INNER JOIN car_makers AS T4 ON T3.Maker = T4.Id
WHERE T2.Weight < 3500
  AND T4.FullName != 'Ford Motor Company'
```

## AL0883

Question: List the name and date the battle that has lost  Lettice and HMS Atalanta

Database: `battle_death`

```sql
SELECT b.name, b.date
FROM battle b
INNER JOIN ship s ON b.id = s.lost_in_battle
WHERE s.name IN ('Lettice', 'HMS Atalanta')
GROUP BY b.name, b.date
HAVING COUNT(DISTINCT s.name) = 2
```

## AL0884

Question: Which of the nations has the most car makers? List the country name.

Database: `car_1`

```sql
SELECT T2.CountryName
FROM car_makers AS T1
INNER JOIN countries AS T2 ON T1.Country = T2.CountryId
GROUP BY T2.CountryName
ORDER BY COUNT(T1.Id) DESC
LIMIT 1
```

## AL0885

Question: How many people live in Asia, and what is the largest GNP among them?

Database: `world_1`

```sql
SELECT SUM(Population), MAX(GNP)
FROM country
WHERE Continent = 'Asia'
```

## AL0886

Question: In which years cars were produced between 3000 and 4000 pounds?

Database: `car_1`

```sql
SELECT DISTINCT YEAR FROM CARS_DATA WHERE Weight BETWEEN 3000 AND 4000
```

## AL0887

Question: What is the content of TV Channel with ""Sky Radio""?

Database: `tvshow`

```sql
SELECT Content FROM TV_Channel WHERE series_name = "Sky Radio"
```

## AL0888

Question: How many pets are over 10 lbs?

Database: `pets_1`

```sql
SELECT COUNT(*) FROM Pets WHERE weight > 10
```

## AL0889

Question: What is the name of country that has the shortest life expectancy in Asia?

Database: `world_1`

```sql
SELECT Name
FROM country
WHERE Continent = 'Asia'
ORDER BY LifeExpectancy ASC
LIMIT 1
```

## AL0890

Question: What is the official language used in the country the name of whose chief of state is Beatrix.

Database: `world_1`

```sql
SELECT T2.Language
FROM country AS T1
INNER JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode
WHERE T1.HeadOfState = 'Beatrix' AND T2.IsOfficial = 'T'
```

## AL0891

Question: What are the countries that have cartoons on TV that Todd Casey writes?

Database: `tvshow`

```sql
SELECT T1.country FROM TV_Channel AS T1 JOIN cartoon AS T2 ON T1.id = T2.Channel WHERE T2.written_by = 'Todd Casey'
```

## AL0892

Question: List singer names and number of concerts for each person.

Database: `concert_singer`

```sql
SELECT T1.name , count(*) FROM singer AS T1 JOIN singer_in_concert AS T2 ON T1.singer_id = T2.singer_id GROUP BY T1.singer_id
```

## AL0893

Question: How many flights depart from APG?

Database: `flight_2`

```sql
SELECT count(*) FROM FLIGHTS WHERE SourceAirport = "APG"
```

## AL0894

Question: What are the codes of the countries that do not speak English and are not Republic?

Database: `world_1`

```sql
SELECT Code
FROM country
WHERE GovernmentForm != 'Republic'
  AND Code NOT IN (
    SELECT CountryCode
    FROM countrylanguage
    WHERE Language = 'English'
  )
```

## AL0895

Question: What are the opening year and staff number of Plaza Museum?

Database: `museum_visit`

```sql
SELECT open_year , num_of_staff FROM museum WHERE name = 'Plaza Museum'
```

## AL0896

Question: How many flights arriving in Aberdeen ?

Database: `flight_2`

```sql
SELECT count(*) FROM FLIGHTS AS T1 JOIN AIRPORTS AS T2 ON T1.DestAirport = T2.AirportCode WHERE T2.City = "Aberdeen"
```

## AL0897

Question: What is the name and capacity of the stadium  with the most concerts after 2013?

Database: `concert_singer`

```sql
SELECT T2.Name, T2.Capacity
FROM concert AS T1
INNER JOIN stadium AS T2 ON T1.Stadium_ID = T2.Stadium_ID
WHERE T1.Year > '2013'
GROUP BY T2.Stadium_ID
ORDER BY COUNT(T1.concert_ID) DESC
LIMIT 1
```

## AL0898

Question: Show the number of high schoolers for each year.

Database: `network_1`

```sql
SELECT grade , count(*) FROM Highschooler GROUP BY grade
```

## AL0899

Question: What is the id, line 1, and line 2 of the place with the most students?

Database: `student_transcripts_tracking`

```sql
SELECT T.address_id, A.line_1, A.line_2
FROM (
    SELECT S.current_address_id AS address_id FROM Students S
    UNION ALL
    SELECT S.permanent_address_id AS address_id FROM Students S
) AS T
INNER JOIN Addresses A ON T.address_id = A.address_id
GROUP BY T.address_id
ORDER BY COUNT(T.address_id) DESC
LIMIT 1
```

## AL0900

Question: What is the lowest grade of students who do not have any friends?

Database: `network_1`

```sql
SELECT MIN(grade)
FROM Highschooler
WHERE ID NOT IN (SELECT student_id FROM Friend)
```

## AL0901

Question: What is the TV Channel that shows The Rise of the Blue Beetle!? List the TV Channel's series name.

Database: `tvshow`

```sql
SELECT T.series_name
FROM Cartoon C
JOIN TV_Channel T ON C.Channel = T.id
WHERE C.Title = 'The Rise of the Blue Beetle!'
```

## AL0902

Question: What are the names of airports in Aberdeen?

Database: `flight_2`

```sql
SELECT AirportName FROM AIRPORTS WHERE City = "Aberdeen"
```

## AL0903

Question: Find the package choice and series name of the TV channel that has HD TV.

Database: `tvshow`

```sql
SELECT package_option , series_name FROM TV_Channel WHERE hight_definition_TV = 'yes'
```

## AL0904

Question: List the names of teachers who have not been assigned to teach courses.

Database: `course_teach`

```sql
SELECT Name
FROM teacher
WHERE Teacher_ID NOT IN (SELECT Teacher_ID FROM course_arrange)
```

## AL0905

Question: What is the name of the winner with the most rank points who participated in the Australian Open?

Database: `wta_1`

```sql
SELECT winner_name
FROM matches
WHERE tourney_name = 'Australian Open'
ORDER BY winner_rank_points DESC
LIMIT 1
```

## AL0906

Question: What are the different models for the cards produced after 1980?

Database: `car_1`

```sql
SELECT DISTINCT T2.Model
FROM cars_data AS T1
INNER JOIN car_names AS T2 ON T1.Id = T2.MakeId
WHERE T1.Year > 1980
```

## AL0907

Question: Which distinct car models are the produced after 1980?

Database: `car_1`

```sql
SELECT DISTINCT T1.Model
FROM car_names AS T1
INNER JOIN cars_data AS T2 ON T1.MakeId = T2.Id
WHERE T2.Year > 1980
```

## AL0908

Question: Find the cities that have more than one employee under  30 year old.

Database: `employee_hire_evaluation`

```sql
SELECT City
FROM employee
WHERE Age < 30
GROUP BY City
HAVING COUNT(*) > 1
```

## AL0909

Question: Return the number of flights arriving in Aberdeen.

Database: `flight_2`

```sql
SELECT COUNT(*) AS NumberOfFlights
FROM flights
WHERE DestAirport IN (
    SELECT AirportCode
    FROM airports
    WHERE City = 'Aberdeen'
)
```

## AL0910

Question: How many airlines are from USA?

Database: `flight_2`

```sql
SELECT count(*) FROM AIRLINES WHERE Country = "USA"
```

## AL0911

Question: Give the name, year of independence, and surface area of the country that has the fewest people.

Database: `world_1`

```sql
SELECT Name , IndepYear , SurfaceArea FROM country ORDER BY Population ASC LIMIT 1
```

## AL0912

Question: What is the zip code for Port Chelsea?

Database: `student_transcripts_tracking`

```sql
SELECT zip_postcode FROM addresses WHERE city = 'Port Chelsea'
```

## AL0913

Question: How many players are from each nation?

Database: `wta_1`

```sql
SELECT country_code, COUNT(*) FROM players GROUP BY country_code
```

## AL0914

Question: List the names of conductors from youngest to oldest.

Database: `orchestra`

```sql
SELECT Name FROM conductor ORDER BY Age ASC
```

## AL0915

Question: Give the names of the nations that were founded after 1950.

Database: `world_1`

```sql
SELECT Name
FROM country
WHERE IndepYear > 1950
```

## AL0916

Question: What country is Jetblue Airways affiliated with?

Database: `flight_2`

```sql
SELECT Country FROM airlines WHERE Airline = 'Jetblue Airways'
```

## AL0917

Question: What is the total number of languages used in Aruba?

Database: `world_1`

```sql
SELECT count(*) FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode WHERE T1.Name = "Aruba"
```

## AL0918

Question: Give the number of Jetblue Airways flights.

Database: `flight_2`

```sql
SELECT COUNT(*)
FROM flights
JOIN airlines ON flights.Airline = airlines.uid
WHERE airlines.Airline = 'Jetblue Airways'
```

## AL0919

Question: Give the airline called UAL.

Database: `flight_2`

```sql
SELECT Airline FROM AIRLINES WHERE Abbreviation = "UAL"
```

## AL0920

Question: find the names of museums which have more staff than the minimum of all museums opened after 2010.

Database: `museum_visit`

```sql
SELECT name FROM museum WHERE num_of_staff > (SELECT min(num_of_staff) FROM museum WHERE open_year > 2010)
```

## AL0921

Question: What are the names of the singers who born in either 1948 or 1949?

Database: `singer`

```sql
SELECT Name FROM singer WHERE Birth_Year = 1948 OR Birth_Year = 1949
```

## AL0922

Question: find the id of tv channels that do not play any cartoon  Ben Jones directs.

Database: `tvshow`

```sql
SELECT id
FROM TV_Channel
WHERE id NOT IN (
    SELECT Channel
    FROM Cartoon
    WHERE Directed_by = 'Ben Jones'
)
```

## AL0923

Question: Find the id of students who do not have a cat.

Database: `pets_1`

```sql
SELECT StuID FROM student EXCEPT SELECT T1.StuID FROM has_pet AS T1 JOIN pets AS T2 ON T1.petid = T2.petid WHERE T2.pettype = 'cat'
```

## AL0924

Question: Find the districts in which there are both shops selling less than 3000 and more than 10000 merchandise.

Database: `employee_hire_evaluation`

```sql
SELECT district FROM shop WHERE number_products < 3000 INTERSECT SELECT district FROM shop WHERE number_products > 10000
```

## AL0925

Question: Who is the student register earliest? List the first name, middle name and last name.

Database: `student_transcripts_tracking`

```sql
SELECT first_name, middle_name, last_name
FROM Students
ORDER BY date_first_registered ASC
LIMIT 1
```

## AL0926

Question: What are the names of conductors, ordered by how old they are?

Database: `orchestra`

```sql
SELECT Name FROM conductor ORDER BY Age
```

## AL0927

Question: What is the language spoken by the largest percentage of people in each nation?

Database: `world_1`

```sql
SELECT Language
FROM (
    SELECT 
        CountryCode,
        Language,
        ROW_NUMBER() OVER (PARTITION BY CountryCode ORDER BY Percentage DESC) AS rn
    FROM countrylanguage
) t
WHERE rn = 1
```

## AL0928

Question: List the area codes in which voters voted both for 'Tabatha Gehling' and 'Kelly Clauss'.

Database: `voter_1`

```sql
SELECT T1.area_code FROM area_code_state AS T1 JOIN votes AS T2 ON T1.state = T2.state JOIN contestants AS T3 ON T2.contestant_number = T3.contestant_number WHERE T3.contestant_name = 'Tabatha Gehling' INTERSECT SELECT T1.area_code FROM area_code_state AS T1 JOIN votes AS T2 ON T1.state = T2.state JOIN contestants AS T3 ON T2.contestant_number = T3.contestant_number WHERE T3.contestant_name = 'Kelly Clauss'
```

## AL0929

Question: Count the number of flights into ATO.

Database: `flight_2`

```sql
SELECT count(*) FROM FLIGHTS WHERE DestAirport = "ATO"
```

## AL0930

Question: Show the name of the teacher who teaches math .

Database: `course_teach`

```sql
SELECT T2.Name FROM course_arrange AS T1 JOIN teacher AS T2 ON T1.Teacher_ID = T2.Teacher_ID JOIN course AS T3 ON T1.Course_ID = T3.Course_ID WHERE T3.Course = "Math"
```

## AL0931

Question: What are names of top 3 countries with most people?

Database: `world_1`

```sql
SELECT Name FROM country ORDER BY Population DESC LIMIT 3
```

## AL0932

Question: What is the average edispl of the cars of  volvo?

Database: `car_1`

```sql
SELECT AVG(T3.Edispl)
FROM car_makers AS T1
INNER JOIN model_list AS T2 ON T1.Id = T2.Maker
INNER JOIN car_names AS T4 ON T2.Model = T4.Model
INNER JOIN cars_data AS T3 ON T4.MakeId = T3.Id
WHERE T1.Maker = 'volvo'
```

## AL0933

Question: Which airline is also known as UAL?

Database: `flight_2`

```sql
SELECT Airline FROM airlines WHERE Abbreviation = 'UAL'
```

## AL0934

Question: Show the stadium names without any concert.

Database: `concert_singer`

```sql
SELECT Name
FROM stadium
WHERE Stadium_ID NOT IN (SELECT Stadium_ID FROM concert)
```

## AL0935

Question: Show the ID of Kyle.

Database: `network_1`

```sql
SELECT ID FROM Highschooler WHERE name = 'Kyle'
```

## AL0936

Question: Find the average age of students who do not have any pet.

Database: `pets_1`

```sql
SELECT AVG(Age)
FROM Student
WHERE StuID NOT IN (SELECT StuID FROM Has_Pet)
```

## AL0937

Question: Which abbreviation corresponds to Jetblue Airways?

Database: `flight_2`

```sql
SELECT Abbreviation FROM airlines WHERE Airline = 'Jetblue Airways'
```

## AL0938

Question: How many car makers are there in france?

Database: `car_1`

```sql
SELECT COUNT(T1.Id)
FROM car_makers AS T1
INNER JOIN countries AS T2 ON T1.Country = T2.CountryId
WHERE T2.CountryName = 'france'
```

## AL0939

Question: Show the number of high schoolers for each year.

Database: `network_1`

```sql
SELECT grade, COUNT(*) FROM Highschooler GROUP BY grade
```

## AL0940

Question: What is the number of distinct continents where Chinese is spoken?

Database: `world_1`

```sql
SELECT COUNT(DISTINCT T1.Continent)
FROM country AS T1
INNER JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode
WHERE T2.Language = 'Chinese'
```

## AL0941

Question: How many visitors below  30 years old are there?

Database: `museum_visit`

```sql
SELECT COUNT(*) FROM visitor WHERE Age < 30
```

## AL0942

Question: How many flights arrive at ATO?

Database: `flight_2`

```sql
SELECT COUNT(*) FROM flights WHERE DestAirport = 'ATO'
```

## AL0943

Question: How many dogs younger than average?

Database: `dog_kennels`

```sql
SELECT count(*) FROM Dogs WHERE age < ( SELECT avg(age) FROM Dogs )
```

## AL0944

Question: In which years cars were produced between 3000 and 4000 pounds?

Database: `car_1`

```sql
SELECT Year
FROM cars_data
WHERE Weight BETWEEN 3000 AND 4000
```

## AL0945

Question: What is the total number of countries where Spanish is spoken by the largest percentage of people?

Database: `world_1`

```sql
SELECT COUNT(T1.CountryCode)
FROM countrylanguage AS T1
WHERE T1.Language = 'Spanish'
  AND T1.Percentage = (
    SELECT MAX(T2.Percentage)
    FROM countrylanguage AS T2
    WHERE T2.CountryCode = T1.CountryCode
  )
```

## AL0946

Question: Which doctors have done at least two treatments? List theid, role, and first name.

Database: `dog_kennels`

```sql
SELECT T1.professional_id , T1.role_code , T1.first_name FROM professionals AS T1 JOIN treatments AS T2 ON T1.professional_id = T2.professional_id GROUP BY T1.professional_id HAVING count(*) >= 2
```

## AL0947

Question: What are the number of concerts that occurred in the stadium with space for the most people?

Database: `concert_singer`

```sql
SELECT COUNT(T1.concert_ID)
FROM concert AS T1
INNER JOIN stadium AS T2 ON T1.Stadium_ID = T2.Stadium_ID
WHERE T2.Capacity = (SELECT MAX(Capacity) FROM stadium)
```

## AL0948

Question: What are different nationalities of people and the corresponding number of people from each country?

Database: `poker_player`

```sql
SELECT Nationality , COUNT(*) FROM people GROUP BY Nationality
```

## AL0949

Question: Who has paid the largest amount of money in total for their dogs? Show the id and zip code.

Database: `dog_kennels`

```sql
SELECT T1.owner_id , T2.zip_code FROM Dogs AS T1 JOIN Owners AS T2 ON T1.owner_id = T2.owner_id JOIN Treatments AS T3 ON T1.dog_id = T3.dog_id GROUP BY T1.owner_id ORDER BY sum(T3.cost_of_treatment) DESC LIMIT 1
```

## AL0950

Question: How many pets are owned by students that are older than 20?

Database: `pets_1`

```sql
SELECT count(*) FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid = T2.stuid WHERE T1.age > 20
```

## AL0951

Question: What are the names of players who won in both 2013 and 2016?

Database: `wta_1`

```sql
SELECT T1.first_name, T1.last_name
FROM players AS T1
INNER JOIN matches AS T2 ON T1.player_id = T2.winner_id
WHERE T2.year IN (2013, 2016)
GROUP BY T1.first_name, T1.last_name
HAVING COUNT(DISTINCT T2.year) = 2
```

## AL0952

Question: What is the produdction code and channel of the most recent cartoon?

Database: `tvshow`

```sql
select production_code , channel from cartoon order by original_air_date desc limit 1
```

## AL0953

Question: What is the name and directors of all the cartoons that are ordered by the time they came out?

Database: `tvshow`

```sql
SELECT title , directed_by FROM cartoon ORDER BY original_air_date
```

## AL0954

Question: What are the full names of all players, sorted by age?

Database: `wta_1`

```sql
SELECT first_name , last_name FROM players ORDER BY birth_date
```

## AL0955

Question: Give the total population and average  corresponding to countries in Noth America that is bigger than 3000 square miles.

Database: `world_1`

```sql
SELECT SUM(Population), AVG(Population)
FROM country
WHERE Continent = 'North America' AND SurfaceArea > 3000
```

## AL0956

Question: Give the flight numbers of flights arriving in Aberdeen.

Database: `flight_2`

```sql
SELECT T1.FlightNo FROM FLIGHTS AS T1 JOIN AIRPORTS AS T2 ON T1.DestAirport = T2.AirportCode WHERE T2.City = "Aberdeen"
```

## AL0957

Question: What are the names of the people who teach math?

Database: `course_teach`

```sql
SELECT T2.Name FROM course_arrange AS T1 JOIN teacher AS T2 ON T1.Teacher_ID = T2.Teacher_ID JOIN course AS T3 ON T1.Course_ID = T3.Course_ID WHERE T3.Course = "Math"
```

## AL0958

Question: What is the abbreviation of ""JetBlue Airways""?

Database: `flight_2`

```sql
SELECT Abbreviation FROM AIRLINES WHERE Airline = "JetBlue Airways"
```

## AL0959

Question: Show the name and theme for all concerts and the number of singers in each.

Database: `concert_singer`

```sql
SELECT T1.concert_Name , T1.theme , count(*) FROM concert AS T1 JOIN singer_in_concert AS T2 ON T1.concert_ID = T2.concert_ID GROUP BY T1.concert_ID
```

## AL0960

Question: What is the total population and maximum GNP in Asia?

Database: `world_1`

```sql
SELECT sum(population) , max(GNP) FROM country WHERE continent = "Asia"
```

## AL0961

Question: What are the region and population of Angola?

Database: `world_1`

```sql
SELECT Region , Population FROM country WHERE Name = "Angola"
```

## AL0962

Question: Which professionals live in Indiana or have done treatment on more than 2 treatments? List his or her id, last name and cell phone.

Database: `dog_kennels`

```sql
SELECT professional_id, last_name, cell_number
FROM Professionals
WHERE state = 'Indiana'
UNION
SELECT T.professional_id, P.last_name, P.cell_number
FROM Treatments T
INNER JOIN Professionals P ON T.professional_id = P.professional_id
GROUP BY T.professional_id
HAVING COUNT(T.treatment_id) > 2
```

## AL0963

Question: What is the id, line 1, and line 2 of the place with the most students?

Database: `student_transcripts_tracking`

```sql
SELECT T1.address_id, T1.line_1, T1.line_2
FROM Addresses AS T1
INNER JOIN (
    SELECT current_address_id AS address_id FROM Students
    UNION ALL
    SELECT permanent_address_id AS address_id FROM Students
) AS T2 ON T1.address_id = T2.address_id
GROUP BY T1.address_id, T1.line_1, T1.line_2
ORDER BY COUNT(T2.address_id) DESC
LIMIT 1
```

## AL0964

Question: What is the average expected life expectancy for countries in Central Africa?

Database: `world_1`

```sql
SELECT avg(LifeExpectancy) FROM country WHERE Region = "Central Africa"
```

## AL0965

Question: Find the number of pets that is heavier than 10.

Database: `pets_1`

```sql
SELECT COUNT(*) FROM Pets WHERE weight > 10
```

## AL0966

Question: Return the country codes for countries that do not speak English.

Database: `world_1`

```sql
SELECT CountryCode
FROM countrylanguage
WHERE Language != 'English'
```

## AL0967

Question: What is the ship id and name that caused most total injuries?

Database: `battle_death`

```sql
SELECT T1.id, T1.name
FROM ship AS T1
INNER JOIN death AS T2 ON T1.id = T2.caused_by_ship_id
GROUP BY T1.id, T1.name
ORDER BY SUM(T2.injured) DESC
LIMIT 1
```

## AL0968

Question: What is the total population of Gelderland ?

Database: `world_1`

```sql
SELECT sum(population) FROM city WHERE district = "Gelderland"
```

## AL0969

Question: What is the average edispl of the cars of  volvo?

Database: `car_1`

```sql
SELECT avg(T1.edispl) FROM CARS_DATA AS T1 JOIN CAR_NAMES AS T2 ON T1.Id = T2.MakeId JOIN MODEL_LIST AS T3 ON T2.Model = T3.Model JOIN CAR_MAKERS AS T4 ON T3.Maker = T4.Id WHERE T4.Maker = 'volvo'
```

## AL0970

Question: What are the codes of nations with more than 50 players?

Database: `wta_1`

```sql
SELECT country_code FROM players GROUP BY country_code HAVING count(*) > 50
```

## AL0971

Question: Return the names of friends of  Kyle.

Database: `network_1`

```sql
SELECT H2.name
FROM Highschooler H1
JOIN Friend F ON H1.ID = F.student_id
JOIN Highschooler H2 ON F.friend_id = H2.ID
WHERE H1.name = 'Kyle'
```

## AL0972

Question: Who is the earliest graduate of the school? List the first name, middle name and last name.

Database: `student_transcripts_tracking`

```sql
SELECT first_name, middle_name, last_name
FROM Students
ORDER BY date_left ASC
LIMIT 1
```

## AL0973

Question: What is the title of all the cartools that are on the TV Channel with Sky Radio?

Database: `tvshow`

```sql
SELECT T1.Title
FROM Cartoon AS T1
INNER JOIN TV_Channel AS T2 ON T1.Channel = T2.id
WHERE T2.series_name = 'Sky Radio'
```

## AL0974

Question: List the title of all  Cartoons showed on TV Channel with  ""Sky Radio"".

Database: `tvshow`

```sql
SELECT T1.Title FROM Cartoon AS T1 JOIN TV_Channel AS T2 ON T1.Channel = T2.id WHERE T2.series_name = "Sky Radio"
```

## AL0975

Question: Which continent has the most diverse languages?

Database: `world_1`

```sql
SELECT T1.Continent FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode GROUP BY T1.Continent ORDER BY COUNT(*) DESC LIMIT 1
```

## AL0976

Question: What region is Kabul in?

Database: `world_1`

```sql
SELECT T2.Region
FROM city AS T1
INNER JOIN country AS T2 ON T1.CountryCode = T2.Code
WHERE T1.Name = 'Kabul'
```

## AL0977

Question: What is the hometown of the youngest teacher?

Database: `course_teach`

```sql
SELECT Hometown FROM teacher ORDER BY Age ASC LIMIT 1
```

## AL0978

Question: Give the total surface area covered by countries in Asia or Europe.

Database: `world_1`

```sql
SELECT SUM(SurfaceArea) FROM country WHERE Continent IN ('Asia', 'Europe')
```

## AL0979

Question: What are the Asian countries have more people than that of any country in Africa?

Database: `world_1`

```sql
SELECT Name
FROM country
WHERE Continent = 'Asia'
  AND Population > (
    SELECT MAX(Population)
    FROM country
    WHERE Continent = 'Africa'
  )
```

## AL0980

Question: Which airline is also known as UAL?

Database: `flight_2`

```sql
SELECT Airline FROM AIRLINES WHERE Abbreviation = "UAL"
```

## AL0981

Question: What is the number of the cars with  more than 150 hp?

Database: `car_1`

```sql
SELECT count(*) FROM CARS_DATA WHERE horsepower > 150
```

## AL0982

Question: Find the id and weight of all pets that is older than 1.

Database: `pets_1`

```sql
SELECT petid , weight FROM pets WHERE pet_age > 1
```

## AL0983

Question: What are the first names of the students who live in Haiti permanently or have the cell phone number 09700166582?

Database: `student_transcripts_tracking`

```sql
SELECT T2.first_name FROM addresses AS T1 JOIN students AS T2 ON T1.address_id = T2.permanent_address_id WHERE T1.country = 'Haiti' UNION SELECT first_name FROM students WHERE cell_mobile_number = '09700166582'
```

## AL0984

Question: What are all distinct countries where singers older than 20 are from?

Database: `concert_singer`

```sql
SELECT DISTINCT Country
FROM singer
WHERE Age > 20
```

## AL0985

Question: What are the names of all the countries that founded after 1950?

Database: `world_1`

```sql
SELECT Name
FROM country
WHERE IndepYear > 1950
```

## AL0986

Question: What are the create dates, states, and phone numbers of the votes that were for 'Tabatha Gehling'?

Database: `voter_1`

```sql
SELECT VOTES.created, VOTES.state, VOTES.phone_number
FROM VOTES
INNER JOIN CONTESTANTS ON VOTES.contestant_number = CONTESTANTS.contestant_number
WHERE CONTESTANTS.contestant_name = 'Tabatha Gehling'
```

## AL0987

Question: Return the name, location and district of all shops odered by the amount of goods they sell from the most to the least.

Database: `employee_hire_evaluation`

```sql
SELECT name , LOCATION , district FROM shop ORDER BY number_products DESC
```

## AL0988

Question: What are the citizenships that are shared by singers born  before 1945 and after 1955?

Database: `singer`

```sql
SELECT Citizenship FROM singer WHERE Birth_Year < 1945 INTERSECT SELECT Citizenship FROM singer WHERE Birth_Year > 1955
```

## AL0989

Question: Which nation has the most of TV Channels? List the country and number of TV Channels it has.

Database: `tvshow`

```sql
SELECT country , count(*) FROM tv_channel GROUP BY country ORDER BY count(*) DESC LIMIT 1
```

## AL0990

Question: How many republic countries are there?

Database: `world_1`

```sql
SELECT COUNT(*) FROM country WHERE GovernmentForm = 'Republic'
```

## AL0991

Question: What is the count of the car models produced in the United States?

Database: `car_1`

```sql
SELECT count(*) FROM MODEL_LIST AS T1 JOIN CAR_MAKERS AS T2 ON T1.Maker = T2.Id JOIN COUNTRIES AS T3 ON T2.Country = T3.CountryId WHERE T3.CountryName = 'usa'
```

## AL0992

Question: find the code of the nation where has the greatest number of players.

Database: `wta_1`

```sql
SELECT country_code
FROM players
GROUP BY country_code
ORDER BY COUNT(player_id) DESC
LIMIT 1
```

## AL0993

Question: What are the country codes of countries where people speak other than English?

Database: `world_1`

```sql
SELECT CountryCode
FROM countrylanguage
WHERE Language != 'English'
```

## AL0994

Question: What is the total population and average area of countries in North America who is bigger than 3000 square miles

Database: `world_1`

```sql
SELECT sum(population) , avg(surfacearea) FROM country WHERE continent = "north america" AND surfacearea > 3000
```

## AL0995

Question: What are the full names of all left handed players, in order of age?

Database: `wta_1`

```sql
SELECT first_name, last_name
FROM players
WHERE hand = 'L'
ORDER BY strftime('%Y', 'now') - strftime('%Y', birth_date)
```

## AL0996

Question: Find the name of students who have both cat and dog.

Database: `pets_1`

```sql
SELECT T1.fname , T1.lname FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid = T2.stuid JOIN pets AS T3 ON T2.petid = T3.petid WHERE T3.pettype = 'cat' INTERSECT SELECT T1.fname , T1.lname FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid = T2.stuid JOIN pets AS T3 ON T2.petid = T3.petid WHERE T3.pettype = 'dog'
```

## AL0997

Question: What is the number of cars with over 150 hp?

Database: `car_1`

```sql
SELECT count(*) FROM CARS_DATA WHERE horsepower > 150
```

## AL0998

Question: What are the Asian countries have more people than that of any country in Africa?

Database: `world_1`

```sql
SELECT Name FROM country WHERE Continent = "Asia" AND population > (SELECT max(population) FROM country WHERE Continent = "Africa")
```

## AL0999

Question: What are the names of the cartoons sorted alphabetically?

Database: `tvshow`

```sql
SELECT Title FROM Cartoon ORDER BY title
```

## AL1000

Question: Give the names of countries that are in Europe and have 80000 people.

Database: `world_1`

```sql
SELECT Name FROM country WHERE continent = "Europe" AND population > 80000
```

## AL1001

Question: Find the id and name of the museum that has the most employees?

Database: `museum_visit`

```sql
SELECT Museum_ID, Name
FROM museum
ORDER BY Num_of_Staff DESC
LIMIT 1
```

## AL1002

Question: Find the number of cities in each district who have more people than average?

Database: `world_1`

```sql
SELECT count(*) , district FROM city WHERE population > (SELECT avg(population) FROM city) GROUP BY district
```

## AL1003

Question: What are the descriptions for all the math?

Database: `student_transcripts_tracking`

```sql
SELECT course_description
FROM Courses
WHERE course_name = 'math'
```

## AL1004

Question: Which person has the most dogs? List the id, first name and last name.

Database: `dog_kennels`

```sql
SELECT T1.owner_id, T1.first_name, T1.last_name
FROM Owners AS T1
INNER JOIN Dogs AS T2 ON T1.owner_id = T2.owner_id
GROUP BY T1.owner_id, T1.first_name, T1.last_name
ORDER BY COUNT(T2.dog_id) DESC
LIMIT 1
```

## AL1005

Question: Find the first name and country code of the oldest player.

Database: `wta_1`

```sql
SELECT first_name , country_code FROM players ORDER BY birth_date LIMIT 1
```

## AL1006

Question: What are the towns from which at least two teachers come from?

Database: `course_teach`

```sql
SELECT Hometown FROM teacher GROUP BY Hometown HAVING COUNT(*) >= 2
```

## AL1007

Question: Which regions speak Dutch or English?

Database: `world_1`

```sql
SELECT DISTINCT T1.Region
FROM country AS T1
INNER JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode
WHERE T2.Language IN ('Dutch', 'English')
```

## AL1008

Question: What is the number of nations with more than 2 car makers ?

Database: `car_1`

```sql
SELECT COUNT(*) FROM (
    SELECT Country FROM car_makers
    GROUP BY Country
    HAVING COUNT(*) > 2
)
```

## AL1009

Question: Give the name of the nation that uses the greatest amount of languages.

Database: `world_1`

```sql
SELECT T1.Name
FROM country AS T1
INNER JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode
GROUP BY T1.Name
ORDER BY COUNT(T2.Language) DESC
LIMIT 1
```

## AL1010

Question: Find the number of orchestras recorded in """"CD"""" or """"DVD"""".

Database: `orchestra`

```sql
SELECT count(*) FROM orchestra WHERE major_record_format = "CD" OR major_record_format = "DVD"
```

## AL1011

Question: Return the names of the 3 most populated countries.

Database: `world_1`

```sql
SELECT Name FROM country ORDER BY Population DESC LIMIT 3
```

## AL1012

Question: Find the name and age of the people who bought the most tickets at once.

Database: `museum_visit`

```sql
SELECT t1.name , t1.age FROM visitor AS t1 JOIN visit AS t2 ON t1.id = t2.visitor_id ORDER BY t2.num_of_ticket DESC LIMIT 1
```

## AL1013

Question: Show me the price of the most recently performed treatment.

Database: `dog_kennels`

```sql
SELECT cost_of_treatment
FROM Treatments
ORDER BY date_of_treatment DESC
LIMIT 1
```

## AL1014

Question: Show all countries and the number of singers in each nation.

Database: `concert_singer`

```sql
SELECT Country, COUNT(*) FROM singer GROUP BY Country
```

## AL1015

Question: List the last name of the owner owning the youngest dog.

Database: `dog_kennels`

```sql
SELECT T2.last_name
FROM Dogs AS T1
INNER JOIN Owners AS T2 ON T1.owner_id = T2.owner_id
ORDER BY T1.date_of_birth DESC
LIMIT 1
```

## AL1016

Question: What country is Jetblue Airways affiliated with?

Database: `flight_2`

```sql
SELECT Country FROM AIRLINES WHERE Airline = "JetBlue Airways"
```

## AL1017

Question: Show the name of singers who were born either 1948 or 1949?

Database: `singer`

```sql
SELECT Name FROM singer WHERE Birth_Year = 1948 OR Birth_Year = 1949
```

## AL1018

Question: List the names of teachers from youngest to oldest.

Database: `course_teach`

```sql
SELECT Name FROM teacher ORDER BY Age ASC
```

## AL1019

Question: What are the locations and names of all stations that can accommodate between 5000 and 10000 fans?

Database: `concert_singer`

```sql
SELECT LOCATION , name FROM stadium WHERE capacity BETWEEN 5000 AND 10000
```

## AL1020

Question: What are the descriptions for all the math?

Database: `student_transcripts_tracking`

```sql
SELECT course_description FROM Courses WHERE course_name = 'math'
```

## AL1021

Question: Give the total surface area covered by countries in Asia or Europe.

Database: `world_1`

```sql
SELECT sum(SurfaceArea) FROM country WHERE Continent = "Asia" OR Continent = "Europe"
```

## AL1022

Question: Which professionals have operated a treatment that is less expansive than the average? Give me theor first names and last names.

Database: `dog_kennels`

```sql
SELECT DISTINCT T1.first_name , T1.last_name FROM professionals AS T1 JOIN treatments AS T2 ON T1.professional_id = T2.professional_id WHERE T2.cost_of_treatment < ( SELECT avg(cost_of_treatment) FROM treatments )
```

## AL1023

Question: What are the names of airports in Aberdeen?

Database: `flight_2`

```sql
SELECT AirportName FROM airports WHERE City = 'Aberdeen'
```

## AL1024

Question: Find the city with the most people that uses English.

Database: `world_1`

```sql
SELECT T1.Name , T1.Population FROM city AS T1 JOIN countrylanguage AS T2 ON T1.CountryCode = T2.CountryCode WHERE T2.Language = "English" ORDER BY T1.Population DESC LIMIT 1
```

## AL1025

Question: What is the zip code of the address in Port Chelsea?

Database: `student_transcripts_tracking`

```sql
SELECT zip_postcode FROM addresses WHERE city = 'Port Chelsea'
```

## AL1026

Question: What is the average age of the visitors not higher than lv 4?

Database: `museum_visit`

```sql
SELECT AVG(Age)
FROM visitor
WHERE Level_of_membership <= 4
```

## AL1027

Question: What are the name, population, and life expectancy of the largest Asian country by land?

Database: `world_1`

```sql
SELECT Name , population , LifeExpectancy FROM country WHERE Continent = "Asia" ORDER BY SurfaceArea DESC LIMIT 1
```

## AL1028

Question: Show different nationalities of singers and the number of singers of each.

Database: `singer`

```sql
SELECT Citizenship , COUNT(*) FROM singer GROUP BY Citizenship
```


# Schemas

## battle_death

  battle(id INT, name TEXT, date TEXT, bulgarian_commander TEXT, latin_commander TEXT, result TEXT)
  death(caused_by_ship_id INT, id INT, note TEXT, killed INT, injured INT)
  ship(lost_in_battle INT, id INT, name TEXT, tonnage TEXT, ship_type TEXT, location TEXT, disposition_of_ship TEXT)

## car_1

  car_makers(Id INTEGER, Maker TEXT, FullName TEXT, Country TEXT)
  car_names(MakeId INTEGER, Model TEXT, Make TEXT)
  cars_data(Id INTEGER, MPG TEXT, Cylinders INTEGER, Edispl REAL, Horsepower TEXT, Weight INTEGER, Accelerate REAL, Year INTEGER)
  continents(ContId INTEGER, Continent TEXT)
  countries(CountryId INTEGER, CountryName TEXT, Continent INTEGER)
  model_list(ModelId INTEGER, Maker INTEGER, Model TEXT)

## concert_singer

  concert(concert_ID INT, concert_Name TEXT, Theme TEXT, Stadium_ID TEXT, Year TEXT)
  singer(Singer_ID INT, Name TEXT, Country TEXT, Song_Name TEXT, Song_release_year TEXT, Age INT, Is_male bool)
  singer_in_concert(concert_ID INT, Singer_ID TEXT)
  stadium(Stadium_ID INT, Location TEXT, Name TEXT, Capacity INT, Highest INT, Lowest INT, Average INT)

## course_teach

  course(Course_ID INT, Staring_Date TEXT, Course TEXT)
  course_arrange(Course_ID INT, Teacher_ID INT, Grade INT)
  teacher(Teacher_ID INT, Name TEXT, Age TEXT, Hometown TEXT)

## dog_kennels

  Breeds(breed_code VARCHAR(10), breed_name VARCHAR(80))
  Charges(charge_id INTEGER, charge_type VARCHAR(10), charge_amount DECIMAL(19,4))
  Dogs(dog_id INTEGER, owner_id INTEGER, abandoned_yn VARCHAR(1), breed_code VARCHAR(10), size_code VARCHAR(10), name VARCHAR(50), age VARCHAR(20), date_of_birth DATETIME, gender VARCHAR(1), weight VARCHAR(20), date_arrived DATETIME, date_adopted DATETIME, date_departed DATETIME)
  Owners(owner_id INTEGER, first_name VARCHAR(50), last_name VARCHAR(50), street VARCHAR(50), city VARCHAR(50), state VARCHAR(20), zip_code VARCHAR(20), email_address VARCHAR(50), home_phone VARCHAR(20), cell_number VARCHAR(20))
  Professionals(professional_id INTEGER, role_code VARCHAR(10), first_name VARCHAR(50), street VARCHAR(50), city VARCHAR(50), state VARCHAR(20), zip_code VARCHAR(20), last_name VARCHAR(50), email_address VARCHAR(50), home_phone VARCHAR(20), cell_number VARCHAR(20))
  Sizes(size_code VARCHAR(10), size_description VARCHAR(80))
  Treatment_Types(treatment_type_code VARCHAR(10), treatment_type_description VARCHAR(80))
  Treatments(treatment_id INTEGER, dog_id INTEGER, professional_id INTEGER, treatment_type_code VARCHAR(10), date_of_treatment DATETIME, cost_of_treatment DECIMAL(19,4))

## employee_hire_evaluation

  employee(Employee_ID INT, Name TEXT, Age INT, City TEXT)
  evaluation(Employee_ID TEXT, Year_awarded TEXT, Bonus REAL)
  hiring(Shop_ID INT, Employee_ID INT, Start_from TEXT, Is_full_time bool)
  shop(Shop_ID INT, Name TEXT, Location TEXT, District TEXT, Number_products INT, Manager_name TEXT)

## flight_2

  airlines(uid INTEGER, Airline TEXT, Abbreviation TEXT, Country TEXT)
  airports(City TEXT, AirportCode TEXT, AirportName TEXT, Country TEXT, CountryAbbrev TEXT)
  flights(Airline INTEGER, FlightNo INTEGER, SourceAirport TEXT, DestAirport TEXT)

## museum_visit

  museum(Museum_ID INT, Name TEXT, Num_of_Staff INT, Open_Year TEXT)
  visit(Museum_ID INT, visitor_ID TEXT, Num_of_Ticket INT, Total_spent REAL)
  visitor(ID INT, Name TEXT, Level_of_membership INT, Age INT)

## network_1

  Friend(student_id INT, friend_id INT)
  Highschooler(ID INT, name TEXT, grade INT)
  Likes(student_id INT, liked_id INT)

## orchestra

  conductor(Conductor_ID INT, Name TEXT, Age INT, Nationality TEXT, Year_of_Work INT)
  orchestra(Orchestra_ID INT, Orchestra TEXT, Conductor_ID INT, Record_Company TEXT, Year_of_Founded REAL, Major_Record_Format TEXT)
  performance(Performance_ID INT, Orchestra_ID INT, Type TEXT, Date TEXT, Official_ratings_(millions) REAL, Weekly_rank TEXT, Share TEXT)
  show(Show_ID INT, Performance_ID INT, If_first_show bool, Result TEXT, Attendance REAL)

## pets_1

  Has_Pet(StuID INTEGER, PetID INTEGER)
  Pets(PetID INTEGER, PetType VARCHAR(20), pet_age INTEGER, weight REAL)
  Student(StuID INTEGER, LName VARCHAR(12), Fname VARCHAR(12), Age INTEGER, Sex VARCHAR(1), Major INTEGER, Advisor INTEGER, city_code VARCHAR(3))

## poker_player

  people(People_ID INT, Nationality TEXT, Name TEXT, Birth_Date TEXT, Height REAL)
  poker_player(Poker_Player_ID INT, People_ID INT, Final_Table_Made REAL, Best_Finish REAL, Money_Rank REAL, Earnings REAL)

## real_estate_properties

  Other_Available_Features(feature_id INTEGER, feature_type_code VARCHAR(20), feature_name VARCHAR(80), feature_description VARCHAR(80))
  Other_Property_Features(property_id INTEGER, feature_id INTEGER, property_feature_description VARCHAR(80))
  Properties(property_id INTEGER, property_type_code VARCHAR(20), date_on_market DATETIME, date_sold DATETIME, property_name VARCHAR(80), property_address VARCHAR(255), room_count INTEGER, vendor_requested_price DECIMAL(19,4), buyer_offered_price DECIMAL(19,4), agreed_selling_price DECIMAL(19,4), apt_feature_1 VARCHAR(255), apt_feature_2 VARCHAR(255), apt_feature_3 VARCHAR(255), fld_feature_1 VARCHAR(255), fld_feature_2 VARCHAR(255), fld_feature_3 VARCHAR(255), hse_feature_1 VARCHAR(255), hse_feature_2 VARCHAR(255), hse_feature_3 VARCHAR(255), oth_feature_1 VARCHAR(255), oth_feature_2 VARCHAR(255), oth_feature_3 VARCHAR(255), shp_feature_1 VARCHAR(255), shp_feature_2 VARCHAR(255), shp_feature_3 VARCHAR(255), other_property_details VARCHAR(255))
  Ref_Feature_Types(feature_type_code VARCHAR(20), feature_type_name VARCHAR(80))
  Ref_Property_Types(property_type_code VARCHAR(20), property_type_description VARCHAR(80))

## singer

  singer(Singer_ID INT, Name TEXT, Birth_Year REAL, Net_Worth_Millions REAL, Citizenship TEXT)
  song(Song_ID INT, Title TEXT, Singer_ID INT, Sales REAL, Highest_Position REAL)

## student_transcripts_tracking

  Addresses(address_id INTEGER, line_1 VARCHAR(255), line_2 VARCHAR(255), line_3 VARCHAR(255), city VARCHAR(255), zip_postcode VARCHAR(20), state_province_county VARCHAR(255), country VARCHAR(255), other_address_details VARCHAR(255))
  Courses(course_id INTEGER, course_name VARCHAR(255), course_description VARCHAR(255), other_details VARCHAR(255))
  Degree_Programs(degree_program_id INTEGER, department_id INTEGER, degree_summary_name VARCHAR(255), degree_summary_description VARCHAR(255), other_details VARCHAR(255))
  Departments(department_id INTEGER, department_name VARCHAR(255), department_description VARCHAR(255), other_details VARCHAR(255))
  Sections(section_id INTEGER, course_id INTEGER, section_name VARCHAR(255), section_description VARCHAR(255), other_details VARCHAR(255))
  Semesters(semester_id INTEGER, semester_name VARCHAR(255), semester_description VARCHAR(255), other_details VARCHAR(255))
  Student_Enrolment(student_enrolment_id INTEGER, degree_program_id INTEGER, semester_id INTEGER, student_id INTEGER, other_details VARCHAR(255))
  Student_Enrolment_Courses(student_course_id INTEGER, course_id INTEGER, student_enrolment_id INTEGER)
  Students(student_id INTEGER, current_address_id INTEGER, permanent_address_id INTEGER, first_name VARCHAR(80), middle_name VARCHAR(40), last_name VARCHAR(40), cell_mobile_number VARCHAR(40), email_address VARCHAR(40), ssn VARCHAR(40), date_first_registered DATETIME, date_left DATETIME, other_student_details VARCHAR(255))
  Transcript_Contents(student_course_id INTEGER, transcript_id INTEGER)
  Transcripts(transcript_id INTEGER, transcript_date DATETIME, other_details VARCHAR(255))

## tvshow

  Cartoon(id REAL, Title TEXT, Directed_by TEXT, Written_by TEXT, Original_air_date TEXT, Production_code REAL, Channel TEXT)
  TV_Channel(id TEXT, series_name TEXT, Country TEXT, Language TEXT, Content TEXT, Pixel_aspect_ratio_PAR TEXT, Hight_definition_TV TEXT, Pay_per_view_PPV TEXT, Package_Option TEXT)
  TV_series(id REAL, Episode TEXT, Air_Date TEXT, Rating TEXT, Share REAL, 18_49_Rating_Share TEXT, Viewers_m TEXT, Weekly_Rank REAL, Channel TEXT)

## voter_1

  AREA_CODE_STATE(area_code INTEGER, state varchar(2))
  CONTESTANTS(contestant_number INTEGER, contestant_name varchar(50))
  VOTES(vote_id INTEGER, phone_number INTEGER, state varchar(2), contestant_number INTEGER, created timestamp)

## world_1

  city(ID INTEGER, Name char(35), CountryCode char(3), District char(20), Population INTEGER)
  country(Code char(3), Name char(52), Continent TEXT, Region char(26), SurfaceArea float(10,2), IndepYear INTEGER, Population INTEGER, LifeExpectancy float(3,1), GNP float(10,2), GNPOld float(10,2), LocalName char(45), GovernmentForm char(45), HeadOfState char(60), Capital INTEGER, Code2 char(2))
  countrylanguage(CountryCode char(3), Language char(30), IsOfficial TEXT, Percentage float(4,1))

## wta_1

  matches(best_of INT, draw_size INT, loser_age FLOAT, loser_entry TEXT, loser_hand TEXT, loser_ht INT, loser_id INT, loser_ioc TEXT, loser_name TEXT, loser_rank INT, loser_rank_points INT, loser_seed INT, match_num INT, minutes INT, round TEXT, score TEXT, surface TEXT, tourney_date DATE, tourney_id TEXT, tourney_level TEXT, tourney_name TEXT, winner_age FLOAT, winner_entry TEXT, winner_hand TEXT, winner_ht INT, winner_id INT, winner_ioc TEXT, winner_name TEXT, winner_rank INT, winner_rank_points INT, winner_seed INT, year INT)
  players(player_id INT, first_name TEXT, last_name TEXT, hand TEXT, birth_date DATE, country_code TEXT)
  rankings(ranking_date DATE, ranking INT, player_id INT, ranking_points INT, tours INT)
