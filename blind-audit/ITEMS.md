# Blinded review of benchmark reference queries

153 items. Read `PROTOCOL.md` before starting, and record every verdict in `RESPONSES.csv`.

For each item you are given a natural-language question and the reference query the benchmark ships as its correct answer. Your task is to judge **the reference query**: does it correctly answer the question against this database? Run it. No model output is shown anywhere in this package, and the items are in a shuffled order that carries no information.


## Items

### Q001

Database: `car_1`  (schema in the appendix)

**Question.** What is the number of nations with more than 2 car makers ?

**Reference query under review.**
```sql
select count(*) from countries as t1 join car_makers as t2 on t1.countryid  =  t2.country group by t1.countryid having count(*)  >  2
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q002

Database: `wta_1`  (schema in the appendix)

**Question.** Find the name and rank points of the person who won the most times.

**Reference query under review.**
```sql
SELECT winner_name ,  winner_rank_points FROM matches GROUP BY winner_name ORDER BY count(*) DESC LIMIT 1
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q003

Database: `tvshow`  (schema in the appendix)

**Question.** Find the series name and country of the tv channel that is playing some cartoons  Ben Jones and Michael Chang directs?

**Reference query under review.**
```sql
SELECT T1.series_name ,  T1.country FROM TV_Channel AS T1 JOIN cartoon AS T2 ON T1.id = T2.Channel WHERE T2.directed_by  =  'Michael Chang' INTERSECT SELECT T1.series_name ,  T1.country FROM TV_Channel AS T1 JOIN cartoon AS T2 ON T1.id = T2.Channel WHERE T2.directed_by  =  'Ben Jones'
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q004

Database: `battle_death`  (schema in the appendix)

**Question.** Show names, results and bulgarian commanders of the battles with no ships lost in the 'English Channel'.

**Reference query under review.**
```sql
SELECT name ,  RESULT ,  bulgarian_commander FROM battle EXCEPT SELECT T1.name ,  T1.result ,  T1.bulgarian_commander FROM battle AS T1 JOIN ship AS T2 ON T1.id  =  T2.lost_in_battle WHERE T2.location  =  'English Channel'
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q005

Database: `flight_2`  (schema in the appendix)

**Question.** How many flights depart from Aberdeen?

**Reference query under review.**
```sql
SELECT count(*) FROM FLIGHTS AS T1 JOIN AIRPORTS AS T2 ON T1.SourceAirport  =  T2.AirportCode WHERE T2.City  =  "Aberdeen"
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q006

Database: `flight_2`  (schema in the appendix)

**Question.** How many flights arriving in Aberdeen ?

**Reference query under review.**
```sql
SELECT count(*) FROM FLIGHTS AS T1 JOIN AIRPORTS AS T2 ON T1.DestAirport  =  T2.AirportCode WHERE T2.City  =  "Aberdeen"
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q007

Database: `car_1`  (schema in the appendix)

**Question.** How many nations has more than 2 car makers ?

**Reference query under review.**
```sql
select count(*) from countries as t1 join car_makers as t2 on t1.countryid  =  t2.country group by t1.countryid having count(*)  >  2
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q008

Database: `world_1`  (schema in the appendix)

**Question.** Give the names of countries officially use English and French

**Reference query under review.**
```sql
SELECT T1.Name FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code  =  T2.CountryCode WHERE T2.Language  =  "English" AND T2.IsOfficial  =  "T" INTERSECT SELECT T1.Name FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code  =  T2.CountryCode WHERE T2.Language  =  "French" AND T2.IsOfficial  =  "T"
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q009

Database: `student_transcripts_tracking`  (schema in the appendix)

**Question.** Find the semester when both Master students and Bachelor students got enrolled in.

**Reference query under review.**
```sql
SELECT DISTINCT T2.semester_id FROM Degree_Programs AS T1 JOIN Student_Enrolment AS T2 ON T1.degree_program_id  =  T2.degree_program_id WHERE degree_summary_name  =  'Master' INTERSECT SELECT DISTINCT T2.semester_id FROM Degree_Programs AS T1 JOIN Student_Enrolment AS T2 ON T1.degree_program_id  =  T2.degree_program_id WHERE degree_summary_name  =  'Bachelor'
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q010

Database: `world_1`  (schema in the appendix)

**Question.** What is the average life expectancy in African countries that are republics?

**Reference query under review.**
```sql
SELECT avg(LifeExpectancy) FROM country WHERE Continent  =  "Africa" AND GovernmentForm  =  "Republic"
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q011

Database: `concert_singer`  (schema in the appendix)

**Question.** What are the names of all stadiums that did not have a concert in 2014?

**Reference query under review.**
```sql
SELECT name FROM stadium EXCEPT SELECT T2.name FROM concert AS T1 JOIN stadium AS T2 ON T1.stadium_id  =  T2.stadium_id WHERE T1.year  =  2014
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q012

Database: `concert_singer`  (schema in the appendix)

**Question.** Show name, country, age for all singers from the oldest to the youngest.

**Reference query under review.**
```sql
SELECT name ,  country ,  age FROM singer ORDER BY age DESC
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q013

Database: `world_1`  (schema in the appendix)

**Question.** What are the names of all the countries that founded after 1950?

**Reference query under review.**
```sql
SELECT Name FROM country WHERE IndepYear  >  1950
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q014

Database: `course_teach`  (schema in the appendix)

**Question.** List the most common place that the teachers come from

**Reference query under review.**
```sql
SELECT Hometown FROM teacher GROUP BY Hometown ORDER BY COUNT(*) DESC LIMIT 1
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q015

Database: `dog_kennels`  (schema in the appendix)

**Question.** What are the names of the dogs for which the owner spent more than 1000 for treatment?

**Reference query under review.**
```sql
select name from dogs where dog_id not in ( select dog_id from treatments group by dog_id having sum(cost_of_treatment)  >  1000 )
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q016

Database: `dog_kennels`  (schema in the appendix)

**Question.** How much is the most recent treatment?

**Reference query under review.**
```sql
SELECT cost_of_treatment FROM Treatments ORDER BY date_of_treatment DESC LIMIT 1
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q017

Database: `flight_2`  (schema in the appendix)

**Question.** How many flights does 'JetBlue Airways' have?

**Reference query under review.**
```sql
SELECT count(*) FROM FLIGHTS AS T1 JOIN AIRLINES AS T2 ON T1.Airline  =  T2.uid WHERE T2.Airline = "JetBlue Airways"
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q018

Database: `world_1`  (schema in the appendix)

**Question.** What is the total number of countries where Spanish is spoken by the largest percentage of people?

**Reference query under review.**
```sql
SELECT count(*) ,   max(Percentage) FROM countrylanguage WHERE LANGUAGE  =  "Spanish" GROUP BY CountryCode
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q019

Database: `pets_1`  (schema in the appendix)

**Question.** How many pets are over 10 lbs?

**Reference query under review.**
```sql
SELECT count(*) FROM pets WHERE weight  >  10
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q020

Database: `world_1`  (schema in the appendix)

**Question.** Return the country codes for countries that do not speak English.

**Reference query under review.**
```sql
SELECT CountryCode FROM countrylanguage EXCEPT SELECT CountryCode FROM countrylanguage WHERE LANGUAGE  =  "English"
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q021

Database: `world_1`  (schema in the appendix)

**Question.** What are the countries that have greater surface area than any country in Europe?

**Reference query under review.**
```sql
SELECT Name FROM country WHERE SurfaceArea  >  (SELECT min(SurfaceArea) FROM country WHERE Continent  =  "Europe")
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q022

Database: `world_1`  (schema in the appendix)

**Question.** What is the official language used in the country the name of whose chief of state is Beatrix.

**Reference query under review.**
```sql
SELECT T2.Language FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code  =  T2.CountryCode WHERE T1.HeadOfState  =  "Beatrix" AND T2.IsOfficial  =  "T"
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q023

Database: `concert_singer`  (schema in the appendix)

**Question.** List singer names and number of concerts for each person.

**Reference query under review.**
```sql
SELECT T2.name ,  count(*) FROM singer_in_concert AS T1 JOIN singer AS T2 ON T1.singer_id  =  T2.singer_id GROUP BY T2.singer_id
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q024

Database: `world_1`  (schema in the appendix)

**Question.** Count the number of countries for which Spanish is predominantly spoken .

**Reference query under review.**
```sql
SELECT count(*) ,   max(Percentage) FROM countrylanguage WHERE LANGUAGE  =  "Spanish" GROUP BY CountryCode
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q025

Database: `concert_singer`  (schema in the appendix)

**Question.** What are the names and release years for all the songs of the youngest singer?

**Reference query under review.**
```sql
SELECT song_name ,  song_release_year FROM singer ORDER BY age LIMIT 1
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q026

Database: `pets_1`  (schema in the appendix)

**Question.** Find the first name and age of students who have a dog but do not have a cat.

**Reference query under review.**
```sql
SELECT T1.fname ,  T1.age FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid  =  T2.stuid JOIN pets AS T3 ON T3.petid  =  T2.petid WHERE T3.pettype  =  'dog' AND T1.stuid NOT IN (SELECT T1.stuid FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid  =  T2.stuid JOIN pets AS T3 ON T3.petid  =  T2.petid WHERE T3.pettype  =  'cat')
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q027

Database: `dog_kennels`  (schema in the appendix)

**Question.** How many dogs younger than average?

**Reference query under review.**
```sql
SELECT count(*) FROM Dogs WHERE age  <  ( SELECT avg(age) FROM Dogs )
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q028

Database: `car_1`  (schema in the appendix)

**Question.** Which countries in europe have at least 3 car manufacturers?

**Reference query under review.**
```sql
SELECT T1.CountryName FROM COUNTRIES AS T1 JOIN CONTINENTS AS T2 ON T1.Continent  =  T2.ContId JOIN CAR_MAKERS AS T3 ON T1.CountryId  =  T3.Country WHERE T2.Continent  =  'europe' GROUP BY T1.CountryName HAVING count(*)  >=  3;
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q029

Database: `car_1`  (schema in the appendix)

**Question.** For all of the 4 CYL cars, which model has the most horsepower?

**Reference query under review.**
```sql
SELECT T1.Model FROM CAR_NAMES AS T1 JOIN CARS_DATA AS T2 ON T1.MakeId  =  T2.Id WHERE T2.Cylinders  =  4 ORDER BY T2.horsepower DESC LIMIT 1;
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q030

Database: `wta_1`  (schema in the appendix)

**Question.** What are the names of players who won in both 2013 and 2016?

**Reference query under review.**
```sql
SELECT winner_name FROM matches WHERE YEAR  =  2013 INTERSECT SELECT winner_name FROM matches WHERE YEAR  =  2016
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q031

Database: `concert_singer`  (schema in the appendix)

**Question.** Find the name and location of the stadiums which some concerts happened in both 2014 and 2015.

**Reference query under review.**
```sql
SELECT T2.name ,  T2.location FROM concert AS T1 JOIN stadium AS T2 ON T1.stadium_id  =  T2.stadium_id WHERE T1.Year  =  2014 INTERSECT SELECT T2.name ,  T2.location FROM concert AS T1 JOIN stadium AS T2 ON T1.stadium_id  =  T2.stadium_id WHERE T1.Year  =  2015
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q032

Database: `world_1`  (schema in the appendix)

**Question.** How many cities in each district have more number of people than average?

**Reference query under review.**
```sql
SELECT count(*) ,  District FROM city WHERE Population  >  (SELECT avg(Population) FROM city) GROUP BY District
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q033

Database: `pets_1`  (schema in the appendix)

**Question.** Find the weight of the youngest dog.

**Reference query under review.**
```sql
SELECT weight FROM pets ORDER BY pet_age LIMIT 1
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q034

Database: `world_1`  (schema in the appendix)

**Question.** Which continent has the most diverse languages?

**Reference query under review.**
```sql
SELECT T1.Continent FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code  =  T2.CountryCode GROUP BY T1.Continent ORDER BY COUNT(*) DESC LIMIT 1
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q035

Database: `student_transcripts_tracking`  (schema in the appendix)

**Question.** What is the id, line 1, and line 2 of the place with the most students?

**Reference query under review.**
```sql
SELECT T1.address_id ,  T1.line_1 ,  T1.line_2 FROM Addresses AS T1 JOIN Students AS T2 ON T1.address_id  =  T2.current_address_id GROUP BY T1.address_id ORDER BY count(*) DESC LIMIT 1
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q036

Database: `car_1`  (schema in the appendix)

**Question.** Find the name of the makers that produced some cars in 1970?

**Reference query under review.**
```sql
SELECT DISTINCT T1.Maker FROM CAR_MAKERS AS T1 JOIN MODEL_LIST AS T2 ON T1.Id  =  T2.Maker JOIN CAR_NAMES AS T3 ON T2.model  =  T3.model JOIN CARS_DATA AS T4 ON T3.MakeId  =  T4.id WHERE T4.year  =  '1970';
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q037

Database: `course_teach`  (schema in the appendix)

**Question.** List the name of teachers who are not from Little Lever Urban District.

**Reference query under review.**
```sql
select name from teacher where hometown != "little lever urban district"
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q038

Database: `flight_2`  (schema in the appendix)

**Question.** Find all airlines that have flights from 'CVO' but not from 'APG'.

**Reference query under review.**
```sql
SELECT T1.Airline FROM AIRLINES AS T1 JOIN FLIGHTS AS T2 ON T1.uid  =  T2.Airline WHERE T2.SourceAirport  =  "CVO" EXCEPT SELECT T1.Airline FROM AIRLINES AS T1 JOIN FLIGHTS AS T2 ON T1.uid  =  T2.Airline WHERE T2.SourceAirport  =  "APG"
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q039

Database: `world_1`  (schema in the appendix)

**Question.** Which countries larger than that of any country in Europe by land?

**Reference query under review.**
```sql
SELECT Name FROM country WHERE SurfaceArea  >  (SELECT min(SurfaceArea) FROM country WHERE Continent  =  "Europe")
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q040

Database: `dog_kennels`  (schema in the appendix)

**Question.** Who owns the youngest dog? Give me his or her last name.

**Reference query under review.**
```sql
SELECT T1.last_name FROM Owners AS T1 JOIN Dogs AS T2 ON T1.owner_id  =  T2.owner_id WHERE T2.age  =  ( SELECT max(age) FROM Dogs )
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q041

Database: `dog_kennels`  (schema in the appendix)

**Question.** List the emails of the professionals who live in Hawaii or Wisconsin.

**Reference query under review.**
```sql
SELECT email_address FROM Professionals WHERE state  =  'Hawaii' OR state  =  'Wisconsin'
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q042

Database: `world_1`  (schema in the appendix)

**Question.** Return the different names of cities that are in Asia and for which Chinese is used officially .

**Reference query under review.**
```sql
SELECT DISTINCT T3.Name FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code  =  T2.CountryCode JOIN city AS T3 ON T1.Code  =  T3.CountryCode WHERE T2.IsOfficial  =  'T' AND T2.Language  =  'Chinese' AND T1.Continent  =  "Asia"
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q043

Database: `student_transcripts_tracking`  (schema in the appendix)

**Question.** Who is the earliest graduate of the school? List the first name, middle name and last name.

**Reference query under review.**
```sql
SELECT first_name ,  middle_name ,  last_name FROM Students ORDER BY date_left ASC LIMIT 1
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q044

Database: `pets_1`  (schema in the appendix)

**Question.** What is the id and weight of every pet who is over 1 year old?

**Reference query under review.**
```sql
SELECT petid ,  weight FROM pets WHERE pet_age  >  1
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q045

Database: `world_1`  (schema in the appendix)

**Question.** What is the total number of languages used in Aruba?

**Reference query under review.**
```sql
SELECT COUNT(T2.Language) FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code  =  T2.CountryCode WHERE T1.Name  =  "Aruba"
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q046

Database: `tvshow`  (schema in the appendix)

**Question.** How many cartoons Joseph Kuhr writes?

**Reference query under review.**
```sql
SELECT count(*) FROM Cartoon WHERE Written_by = "Joseph Kuhr";
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q047

Database: `pets_1`  (schema in the appendix)

**Question.** Find the number of pets that is heavier than 10.

**Reference query under review.**
```sql
SELECT count(*) FROM pets WHERE weight  >  10
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q048

Database: `battle_death`  (schema in the appendix)

**Question.** List the name and date the battle that has lost  Lettice and HMS Atalanta

**Reference query under review.**
```sql
SELECT T1.name ,  T1.date FROM battle AS T1 JOIN ship AS T2 ON T1.id  =  T2.lost_in_battle WHERE T2.name  =  'Lettice' INTERSECT SELECT T1.name ,  T1.date FROM battle AS T1 JOIN ship AS T2 ON T1.id  =  T2.lost_in_battle WHERE T2.name  =  'HMS Atalanta'
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q049

Database: `singer`  (schema in the appendix)

**Question.** What is the msot common country for singer?

**Reference query under review.**
```sql
select citizenship from singer group by citizenship order by count(*) desc limit 1
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q050

Database: `network_1`  (schema in the appendix)

**Question.** What are the names of all high schoolers in  10?

**Reference query under review.**
```sql
SELECT name FROM Highschooler WHERE grade  =  10
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q051

Database: `concert_singer`  (schema in the appendix)

**Question.** What are the names and number of concerts for each person?

**Reference query under review.**
```sql
SELECT T2.name ,  count(*) FROM singer_in_concert AS T1 JOIN singer AS T2 ON T1.singer_id  =  T2.singer_id GROUP BY T2.singer_id
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q052

Database: `car_1`  (schema in the appendix)

**Question.** What is the accelerate of amc hornet sportabout (sw)?

**Reference query under review.**
```sql
SELECT T1.Accelerate FROM CARS_DATA AS T1 JOIN CAR_NAMES AS T2 ON T1.Id  =  T2.MakeId WHERE T2.Make  =  'amc hornet sportabout (sw)';
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q053

Database: `network_1`  (schema in the appendix)

**Question.** How many friends does Kyle have?

**Reference query under review.**
```sql
SELECT count(*) FROM Friend AS T1 JOIN Highschooler AS T2 ON T1.student_id  =  T2.id WHERE T2.name  =  "Kyle"
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q054

Database: `world_1`  (schema in the appendix)

**Question.** What are the codes of countries where Spanish is spoken by the largest percentage of people?

**Reference query under review.**
```sql
SELECT CountryCode ,  max(Percentage) FROM countrylanguage WHERE LANGUAGE  =  "Spanish" GROUP BY CountryCode
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q055

Database: `network_1`  (schema in the appendix)

**Question.** Count the number of friends Kyle has.

**Reference query under review.**
```sql
SELECT count(*) FROM Friend AS T1 JOIN Highschooler AS T2 ON T1.student_id  =  T2.id WHERE T2.name  =  "Kyle"
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q056

Database: `world_1`  (schema in the appendix)

**Question.** Whic`h unique cities are in  Asian countries where Chinese is the official ?

**Reference query under review.**
```sql
select distinct t3.name from country as t1 join countrylanguage as t2 on t1.code  =  t2.countrycode join city as t3 on t1.code  =  t3.countrycode where t2.isofficial  =  't' and t2.language  =  'chinese' and t1.continent  =  "asia"
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q057

Database: `world_1`  (schema in the appendix)

**Question.** What language is predominantly spoken in Aruba?

**Reference query under review.**
```sql
SELECT T2.Language FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code  =  T2.CountryCode WHERE T1.Name  =  "Aruba" ORDER BY Percentage DESC LIMIT 1
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q058

Database: `car_1`  (schema in the appendix)

**Question.** What are the different models created by either General Motors or over 3500 lbs?

**Reference query under review.**
```sql
SELECT DISTINCT T2.Model FROM CAR_NAMES AS T1 JOIN MODEL_LIST AS T2 ON T1.Model  =  T2.Model JOIN CAR_MAKERS AS T3 ON T2.Maker  =  T3.Id JOIN CARS_DATA AS T4 ON T1.MakeId  =  T4.Id WHERE T3.FullName  =  'General Motors' OR T4.weight  >  3500;
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q059

Database: `world_1`  (schema in the appendix)

**Question.** Count the number of countries in Asia.

**Reference query under review.**
```sql
SELECT count(*) FROM country WHERE continent  =  "Asia"
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q060

Database: `car_1`  (schema in the appendix)

**Question.** What is the count of the car models produced in the United States?

**Reference query under review.**
```sql
SELECT count(*) FROM MODEL_LIST AS T1 JOIN CAR_MAKERS AS T2 ON T1.Maker  =  T2.Id JOIN COUNTRIES AS T3 ON T2.Country  =  T3.CountryId WHERE T3.CountryName  =  'usa';
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q061

Database: `course_teach`  (schema in the appendix)

**Question.** What are the names of the teachers who do not come from Little Lever Urban District?

**Reference query under review.**
```sql
select name from teacher where hometown != "little lever urban district"
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q062

Database: `concert_singer`  (schema in the appendix)

**Question.** What are the number of concerts that occurred in the stadium with space for the most people?

**Reference query under review.**
```sql
select count(*) from concert where stadium_id = (select stadium_id from stadium order by capacity desc limit 1)
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q063

Database: `world_1`  (schema in the appendix)

**Question.** What are the Asian countries have more people than that of any country in Africa?

**Reference query under review.**
```sql
SELECT Name FROM country WHERE Continent  =  "Asia"  AND population  >  (SELECT min(population) FROM country WHERE Continent  =  "Africa")
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q064

Database: `dog_kennels`  (schema in the appendix)

**Question.** Which professionals have operated a treatment that is less expansive than the average? Give me theor first names and last names.

**Reference query under review.**
```sql
SELECT DISTINCT T1.first_name ,  T1.last_name FROM Professionals AS T1 JOIN Treatments AS T2 WHERE cost_of_treatment  <  ( SELECT avg(cost_of_treatment) FROM Treatments )
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q065

Database: `world_1`  (schema in the appendix)

**Question.** What are the codes of the different nations, and what are the languages spoken by the greatest percentage of people for each?

**Reference query under review.**
```sql
SELECT LANGUAGE ,  CountryCode ,  max(Percentage) FROM countrylanguage GROUP BY CountryCode
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q066

Database: `flight_2`  (schema in the appendix)

**Question.** What are airlines that have flights arriving at AHD?

**Reference query under review.**
```sql
SELECT T1.Airline FROM AIRLINES AS T1 JOIN FLIGHTS AS T2 ON T1.uid  =  T2.Airline WHERE T2.DestAirport  =  "AHD"
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q067

Database: `world_1`  (schema in the appendix)

**Question.** What are the population and life expectancies in Brazil?

**Reference query under review.**
```sql
SELECT Population ,  LifeExpectancy FROM country WHERE Name  =  "Brazil"
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q068

Database: `world_1`  (schema in the appendix)

**Question.** Give the average life expectancy for countries in Africa which are republics?

**Reference query under review.**
```sql
SELECT avg(LifeExpectancy) FROM country WHERE Continent  =  "Africa" AND GovernmentForm  =  "Republic"
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q069

Database: `world_1`  (schema in the appendix)

**Question.** What are the names of nations speak both English and French?

**Reference query under review.**
```sql
SELECT T1.Name FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code  =  T2.CountryCode WHERE T2.Language  =  "English" INTERSECT SELECT T1.Name FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code  =  T2.CountryCode WHERE T2.Language  =  "French"
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q070

Database: `pets_1`  (schema in the appendix)

**Question.** How much does the youngest dog weigh?

**Reference query under review.**
```sql
SELECT weight FROM pets ORDER BY pet_age LIMIT 1
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q071

Database: `car_1`  (schema in the appendix)

**Question.** What is the number of cars with over 150 hp?

**Reference query under review.**
```sql
SELECT count(*) FROM CARS_DATA WHERE horsepower  >  150;
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q072

Database: `wta_1`  (schema in the appendix)

**Question.** List the names of all winners who played in both 2013 and 2016.

**Reference query under review.**
```sql
SELECT winner_name FROM matches WHERE YEAR  =  2013 INTERSECT SELECT winner_name FROM matches WHERE YEAR  =  2016
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q073

Database: `concert_singer`  (schema in the appendix)

**Question.** List all singer names in concerts in  2014.

**Reference query under review.**
```sql
SELECT T2.name FROM singer_in_concert AS T1 JOIN singer AS T2 ON T1.singer_id  =  T2.singer_id JOIN concert AS T3 ON T1.concert_id  =  T3.concert_id WHERE T3.year  =  2014
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q074

Database: `battle_death`  (schema in the appendix)

**Question.** What are the ids and names of the battles that led to more than 10 people died.

**Reference query under review.**
```sql
SELECT T1.id ,  T1.name FROM battle AS T1 JOIN ship AS T2 ON T1.id  =  T2.lost_in_battle JOIN death AS T3 ON T2.id  =  T3.caused_by_ship_id GROUP BY T1.id HAVING sum(T3.killed)  >  10
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q075

Database: `world_1`  (schema in the appendix)

**Question.** Give the country codes for countries in which people does not speak English.

**Reference query under review.**
```sql
SELECT DISTINCT CountryCode FROM countrylanguage WHERE LANGUAGE != "English"
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q076

Database: `student_transcripts_tracking`  (schema in the appendix)

**Question.** What are the first names of the students who live in Haiti permanently or have the cell phone number 09700166582?

**Reference query under review.**
```sql
select t1.first_name from students as t1 join addresses as t2 on t1.permanent_address_id  =  t2.address_id where t2.country  =  'haiti' or t1.cell_mobile_number  =  '09700166582'
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q077

Database: `student_transcripts_tracking`  (schema in the appendix)

**Question.** Find the first name of the students who permanently live in Haiti or have the cell phone number 09700166582.

**Reference query under review.**
```sql
select t1.first_name from students as t1 join addresses as t2 on t1.permanent_address_id  =  t2.address_id where t2.country  =  'haiti' or t1.cell_mobile_number  =  '09700166582'
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q078

Database: `network_1`  (schema in the appendix)

**Question.** Find the minimum grade of students who have no friends.

**Reference query under review.**
```sql
SELECT min(grade) FROM Highschooler WHERE id NOT IN (SELECT T1.student_id FROM Friend AS T1 JOIN Highschooler AS T2 ON T1.student_id  =  T2.id)
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q079

Database: `battle_death`  (schema in the appendix)

**Question.** What is the ship id and name that caused most total injuries?

**Reference query under review.**
```sql
SELECT T2.id ,  T2.name FROM death AS T1 JOIN ship AS t2 ON T1.caused_by_ship_id  =  T2.id GROUP BY T2.id ORDER BY count(*) DESC LIMIT 1
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q080

Database: `world_1`  (schema in the appendix)

**Question.** Which continent speaks the most languages?

**Reference query under review.**
```sql
SELECT T1.Continent FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code  =  T2.CountryCode GROUP BY T1.Continent ORDER BY COUNT(*) DESC LIMIT 1
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q081

Database: `car_1`  (schema in the appendix)

**Question.** What is the maximum miles per gallon of the 8 CYL cars or cars produced before 1980 ?

**Reference query under review.**
```sql
select max(mpg) from cars_data where cylinders  =  8 or year  <  1980
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q082

Database: `course_teach`  (schema in the appendix)

**Question.** List the names of teachers from youngest to oldest.

**Reference query under review.**
```sql
SELECT Name FROM teacher ORDER BY Age ASC
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q083

Database: `world_1`  (schema in the appendix)

**Question.** What is the average GNP and total population in all US territory nations?

**Reference query under review.**
```sql
SELECT avg(GNP) ,  sum(population) FROM country WHERE GovernmentForm  =  "US Territory"
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q084

Database: `museum_visit`  (schema in the appendix)

**Question.** find the names of museums which have more staff than the minimum of all museums opened after 2010.

**Reference query under review.**
```sql
SELECT name FROM museum WHERE num_of_staff  >  (SELECT min(num_of_staff) FROM museum WHERE open_year  >  2010)
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q085

Database: `course_teach`  (schema in the appendix)

**Question.** What is the hometown of the youngest teacher?

**Reference query under review.**
```sql
SELECT Hometown FROM teacher ORDER BY Age ASC LIMIT 1
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q086

Database: `wta_1`  (schema in the appendix)

**Question.** What is the name of the player who has won the most matches, and how many rank points does this player have?

**Reference query under review.**
```sql
SELECT winner_name ,  winner_rank_points FROM matches GROUP BY winner_name ORDER BY count(*) DESC LIMIT 1
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q087

Database: `car_1`  (schema in the appendix)

**Question.** What is the car wmodel that is the most fuel efficient?

**Reference query under review.**
```sql
select t1.model from car_names as t1 join cars_data as t2 on t1.makeid  =  t2.id order by t2.mpg desc limit 1;
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q088

Database: `world_1`  (schema in the appendix)

**Question.** Give the names of countries that are in Europe and have 80000 people.

**Reference query under review.**
```sql
SELECT Name FROM country WHERE continent  =  "Europe" AND Population  =  "80000"
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q089

Database: `dog_kennels`  (schema in the appendix)

**Question.** Return the id, first name and last name of the person who has the most dogs.

**Reference query under review.**
```sql
SELECT T1.owner_id ,  T2.first_name ,  T2.last_name FROM Dogs AS T1 JOIN Owners AS T2 ON T1.owner_id  =  T2.owner_id GROUP BY T1.owner_id ORDER BY count(*) DESC LIMIT 1
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q090

Database: `dog_kennels`  (schema in the appendix)

**Question.** What are the first name and last name of the professionals who have done treatment cheaper than average?

**Reference query under review.**
```sql
SELECT DISTINCT T1.first_name ,  T1.last_name FROM Professionals AS T1 JOIN Treatments AS T2 WHERE cost_of_treatment  <  ( SELECT avg(cost_of_treatment) FROM Treatments )
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q091

Database: `world_1`  (schema in the appendix)

**Question.** What are the countries where either English or Dutch is officially spoken ?

**Reference query under review.**
```sql
select t1.name from country as t1 join countrylanguage as t2 on t1.code  =  t2.countrycode where t2.language  =  "english" and isofficial  =  "t" union select t1.name from country as t1 join countrylanguage as t2 on t1.code  =  t2.countrycode where t2.language  =  "dutch" and isofficial  =  "t"
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q092

Database: `world_1`  (schema in the appendix)

**Question.** What is name of the nation that speaks the largest number of languages?

**Reference query under review.**
```sql
SELECT T1.Name FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code  =  T2.CountryCode GROUP BY T1.Name ORDER BY COUNT(*) DESC LIMIT 1
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q093

Database: `poker_player`  (schema in the appendix)

**Question.** What are the names of people who are not from Russia?

**Reference query under review.**
```sql
SELECT Name FROM people WHERE Nationality != "Russia"
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q094

Database: `student_transcripts_tracking`  (schema in the appendix)

**Question.** Which place holds the most number of students currently? List the id and all lines.

**Reference query under review.**
```sql
SELECT T1.address_id ,  T1.line_1 ,  T1.line_2 FROM Addresses AS T1 JOIN Students AS T2 ON T1.address_id  =  T2.current_address_id GROUP BY T1.address_id ORDER BY count(*) DESC LIMIT 1
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q095

Database: `car_1`  (schema in the appendix)

**Question.** What is the average edispl of the cars of  volvo?

**Reference query under review.**
```sql
SELECT avg(T2.edispl) FROM CAR_NAMES AS T1 JOIN CARS_DATA AS T2 ON T1.MakeId  =  T2.Id WHERE T1.Model  =  'volvo';
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q096

Database: `world_1`  (schema in the appendix)

**Question.** What are the country codes for countries that do not speak English?

**Reference query under review.**
```sql
SELECT CountryCode FROM countrylanguage EXCEPT SELECT CountryCode FROM countrylanguage WHERE LANGUAGE  =  "English"
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q097

Database: `car_1`  (schema in the appendix)

**Question.** What is the average edispl for all volvos?

**Reference query under review.**
```sql
SELECT avg(T2.edispl) FROM CAR_NAMES AS T1 JOIN CARS_DATA AS T2 ON T1.MakeId  =  T2.Id WHERE T1.Model  =  'volvo';
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q098

Database: `student_transcripts_tracking`  (schema in the appendix)

**Question.** What is the zip code for Port Chelsea?

**Reference query under review.**
```sql
SELECT zip_postcode FROM Addresses WHERE city  =  'Port Chelsea'
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q099

Database: `tvshow`  (schema in the appendix)

**Question.** What is the weekly rank for the  """"A Love of a Lifetime""""?

**Reference query under review.**
```sql
SELECT Weekly_Rank FROM TV_series WHERE Episode = "A Love of a Lifetime";
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q100

Database: `flight_2`  (schema in the appendix)

**Question.** Give the airline called UAL.

**Reference query under review.**
```sql
SELECT Airline FROM AIRLINES WHERE Abbreviation  =  "UAL"
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q101

Database: `world_1`  (schema in the appendix)

**Question.** What is the total population and average area of countries in North America who is bigger than 3000 square miles

**Reference query under review.**
```sql
select sum(population) ,  avg(surfacearea) from country where continent  =  "north america" and surfacearea  >  3000
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q102

Database: `dog_kennels`  (schema in the appendix)

**Question.** Count the number of dogs that are younger than the average.

**Reference query under review.**
```sql
SELECT count(*) FROM Dogs WHERE age  <  ( SELECT avg(age) FROM Dogs )
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q103

Database: `car_1`  (schema in the appendix)

**Question.** Find the make and production time of the cars that were produced in the earliest ?

**Reference query under review.**
```sql
SELECT T2.Make ,  T1.Year FROM CARS_DATA AS T1 JOIN CAR_NAMES AS T2 ON T1.Id  =  T2.MakeId WHERE T1.Year  =  (SELECT min(YEAR) FROM CARS_DATA);
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q104

Database: `network_1`  (schema in the appendix)

**Question.** Which year has the most high schoolers?

**Reference query under review.**
```sql
SELECT grade FROM Highschooler GROUP BY grade ORDER BY count(*) DESC LIMIT 1
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q105

Database: `wta_1`  (schema in the appendix)

**Question.** Find the first name and country code of the oldest player.

**Reference query under review.**
```sql
SELECT first_name ,  country_code FROM players ORDER BY birth_date LIMIT 1
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q106

Database: `dog_kennels`  (schema in the appendix)

**Question.** List the last name of the owner owning the youngest dog.

**Reference query under review.**
```sql
SELECT T1.last_name FROM Owners AS T1 JOIN Dogs AS T2 ON T1.owner_id  =  T2.owner_id WHERE T2.age  =  ( SELECT max(age) FROM Dogs )
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q107

Database: `poker_player`  (schema in the appendix)

**Question.** What is the money rank of the tallest poker player?

**Reference query under review.**
```sql
SELECT T2.Money_Rank FROM people AS T1 JOIN poker_player AS T2 ON T1.People_ID  =  T2.People_ID ORDER BY T1.Height DESC LIMIT 1
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q108

Database: `pets_1`  (schema in the appendix)

**Question.** What are the students' first names who have both cats and dogs?

**Reference query under review.**
```sql
SELECT T1.Fname FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid  =  T2.stuid JOIN pets AS T3 ON T3.petid  =  T2.petid WHERE T3.pettype  =  'cat' INTERSECT SELECT T1.Fname FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid  =  T2.stuid JOIN pets AS T3 ON T3.petid  =  T2.petid WHERE T3.pettype  =  'dog'
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q109

Database: `employee_hire_evaluation`  (schema in the appendix)

**Question.** Sort all the shops by amount of merchandise in descending order, and return the name, location and district of each shop.

**Reference query under review.**
```sql
SELECT name ,  LOCATION ,  district FROM shop ORDER BY number_products DESC
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q110

Database: `course_teach`  (schema in the appendix)

**Question.** Where is the youngest teacher from?

**Reference query under review.**
```sql
SELECT Hometown FROM teacher ORDER BY Age ASC LIMIT 1
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q111

Database: `employee_hire_evaluation`  (schema in the appendix)

**Question.** Find the manager name and district of the shop with the most goods.

**Reference query under review.**
```sql
SELECT manager_name ,  district FROM shop ORDER BY number_products DESC LIMIT 1
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q112

Database: `student_transcripts_tracking`  (schema in the appendix)

**Question.** What is the mobile phone number of the student named Timmothy Ward ?

**Reference query under review.**
```sql
select cell_mobile_number from students where first_name  =  'timmothy' and last_name  =  'ward'
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q113

Database: `wta_1`  (schema in the appendix)

**Question.** Find the number of left handed winners who participated in the WTA Championships.

**Reference query under review.**
```sql
SELECT count(DISTINCT winner_name) FROM matches WHERE tourney_name  =  'WTA Championships' AND winner_hand  =  'L'
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q114

Database: `world_1`  (schema in the appendix)

**Question.** What is the language spoken by the largest percentage of people in each nation?

**Reference query under review.**
```sql
SELECT LANGUAGE ,  CountryCode ,  max(Percentage) FROM countrylanguage GROUP BY CountryCode
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q115

Database: `car_1`  (schema in the appendix)

**Question.** What is the maker of the carr produced in the earliest  and what  year was it?

**Reference query under review.**
```sql
SELECT T2.Make ,  T1.Year FROM CARS_DATA AS T1 JOIN CAR_NAMES AS T2 ON T1.Id  =  T2.MakeId WHERE T1.Year  =  (SELECT min(YEAR) FROM CARS_DATA);
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q116

Database: `world_1`  (schema in the appendix)

**Question.** Give the total population and average  corresponding to countries in Noth America that is bigger than 3000 square miles.

**Reference query under review.**
```sql
select sum(population) ,  avg(surfacearea) from country where continent  =  "north america" and surfacearea  >  3000
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q117

Database: `world_1`  (schema in the appendix)

**Question.** Give the name of the country in Asia with the lowest life expectancy.

**Reference query under review.**
```sql
SELECT Name FROM country WHERE Continent  =  "Asia" ORDER BY LifeExpectancy LIMIT 1
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q118

Database: `dog_kennels`  (schema in the appendix)

**Question.** Who has paid the largest amount of money in total for their dogs? Show the id and zip code.

**Reference query under review.**
```sql
SELECT T1.owner_id ,  T1.zip_code FROM Owners AS T1 JOIN Dogs AS T2 ON T1.owner_id  =  T2.owner_id JOIN Treatments AS T3 ON T2.dog_id  =  T3.dog_id GROUP BY T1.owner_id ORDER BY sum(T3.cost_of_treatment) DESC LIMIT 1
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q119

Database: `pets_1`  (schema in the appendix)

**Question.** What are the first names of every student who has a cat or dog?

**Reference query under review.**
```sql
SELECT DISTINCT T1.Fname FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid  =  T2.stuid JOIN pets AS T3 ON T3.petid  =  T2.petid WHERE T3.pettype  =  'cat' OR T3.pettype  =  'dog'
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q120

Database: `car_1`  (schema in the appendix)

**Question.** What is the number of the cars with  more than 150 hp?

**Reference query under review.**
```sql
SELECT count(*) FROM CARS_DATA WHERE horsepower  >  150;
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q121

Database: `flight_2`  (schema in the appendix)

**Question.** What are flight numbers of flights departing from APG?

**Reference query under review.**
```sql
SELECT FlightNo FROM FLIGHTS WHERE SourceAirport  =  "APG"
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q122

Database: `pets_1`  (schema in the appendix)

**Question.** How many dogs are raised by female students?

**Reference query under review.**
```sql
SELECT count(*) FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid  =  T2.stuid JOIN pets AS T3 ON T2.petid  =  T3.petid WHERE T1.sex  =  'F' AND T3.pettype  =  'dog'
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q123

Database: `employee_hire_evaluation`  (schema in the appendix)

**Question.** Find the number of shops in each place.

**Reference query under review.**
```sql
SELECT count(*) ,  LOCATION FROM shop GROUP BY LOCATION
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q124

Database: `world_1`  (schema in the appendix)

**Question.** What is the total number of people living in the nations that do not use English?

**Reference query under review.**
```sql
SELECT sum(Population) FROM country WHERE Name NOT IN (SELECT T1.Name FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code  =  T2.CountryCode WHERE T2.Language  =  "English")
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q125

Database: `world_1`  (schema in the appendix)

**Question.** Return the codes of countries for which Spanish is predominantly spoken .

**Reference query under review.**
```sql
SELECT CountryCode ,  max(Percentage) FROM countrylanguage WHERE LANGUAGE  =  "Spanish" GROUP BY CountryCode
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q126

Database: `pets_1`  (schema in the appendix)

**Question.** Find the type and weight of the youngest pet.

**Reference query under review.**
```sql
SELECT pettype ,  weight FROM pets ORDER BY pet_age LIMIT 1
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q127

Database: `network_1`  (schema in the appendix)

**Question.** Show the ID of Kyle.

**Reference query under review.**
```sql
SELECT ID FROM Highschooler WHERE name  =  "Kyle"
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q128

Database: `tvshow`  (schema in the appendix)

**Question.** find id of the tv channels that from the nations where have more than two tv channels.

**Reference query under review.**
```sql
SELECT id FROM tv_channel GROUP BY country HAVING count(*)  >  2
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q129

Database: `network_1`  (schema in the appendix)

**Question.** What is the average grade of students who have friends?

**Reference query under review.**
```sql
SELECT avg(grade) FROM Highschooler WHERE id IN (SELECT T1.student_id FROM Friend AS T1 JOIN Highschooler AS T2 ON T1.student_id  =  T2.id)
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q130

Database: `employee_hire_evaluation`  (schema in the appendix)

**Question.** Which shops run with no employees? Find the shop names

**Reference query under review.**
```sql
SELECT name FROM shop WHERE shop_id NOT IN (SELECT shop_id FROM hiring)
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q131

Database: `orchestra`  (schema in the appendix)

**Question.** What are the names of conductors, ordered by how old they are?

**Reference query under review.**
```sql
SELECT Name FROM conductor ORDER BY Age ASC
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q132

Database: `concert_singer`  (schema in the appendix)

**Question.** Show names for all stadiums except for stadiums having a concert in  2014.

**Reference query under review.**
```sql
SELECT name FROM stadium EXCEPT SELECT T2.name FROM concert AS T1 JOIN stadium AS T2 ON T1.stadium_id  =  T2.stadium_id WHERE T1.year  =  2014
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q133

Database: `employee_hire_evaluation`  (schema in the appendix)

**Question.** Sort employee names from youngest to oldest.

**Reference query under review.**
```sql
SELECT name FROM employee ORDER BY age
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q134

Database: `car_1`  (schema in the appendix)

**Question.** Which model saves the most gasoline?

**Reference query under review.**
```sql
SELECT T1.Model FROM CAR_NAMES AS T1 JOIN CARS_DATA AS T2 ON T1.MakeId  =  T2.Id ORDER BY T2.mpg DESC LIMIT 1;
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q135

Database: `pets_1`  (schema in the appendix)

**Question.** Find the name of students who have both cat and dog.

**Reference query under review.**
```sql
select t1.fname from student as t1 join has_pet as t2 on t1.stuid  =  t2.stuid join pets as t3 on t3.petid  =  t2.petid where t3.pettype  =  'cat' intersect select t1.fname from student as t1 join has_pet as t2 on t1.stuid  =  t2.stuid join pets as t3 on t3.petid  =  t2.petid where t3.pettype  =  'dog'
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q136

Database: `world_1`  (schema in the appendix)

**Question.** How many people live in countries that do not speak English?

**Reference query under review.**
```sql
SELECT sum(Population) FROM country WHERE Name NOT IN (SELECT T1.Name FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code  =  T2.CountryCode WHERE T2.Language  =  "English")
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q137

Database: `world_1`  (schema in the appendix)

**Question.** Return the names of the 3 countries with the fewest people.

**Reference query under review.**
```sql
SELECT Name FROM country ORDER BY Population ASC LIMIT 3
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q138

Database: `car_1`  (schema in the appendix)

**Question.** What car has the most different versions?

**Reference query under review.**
```sql
SELECT Model FROM CAR_NAMES GROUP BY Model ORDER BY count(*) DESC LIMIT 1;
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q139

Database: `car_1`  (schema in the appendix)

**Question.** Which distinctive models are produced by General Motors or heavier than 3500?

**Reference query under review.**
```sql
SELECT DISTINCT T2.Model FROM CAR_NAMES AS T1 JOIN MODEL_LIST AS T2 ON T1.Model  =  T2.Model JOIN CAR_MAKERS AS T3 ON T2.Maker  =  T3.Id JOIN CARS_DATA AS T4 ON T1.MakeId  =  T4.Id WHERE T3.FullName  =  'General Motors' OR T4.weight  >  3500;
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q140

Database: `flight_2`  (schema in the appendix)

**Question.** What are the airline names and abbreviations for airlines in the USA?

**Reference query under review.**
```sql
SELECT Airline ,  Abbreviation FROM AIRLINES WHERE Country  =  "USA"
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q141

Database: `world_1`  (schema in the appendix)

**Question.** What are the name, independence year, and surface area of the country with the least number of nationalities?

**Reference query under review.**
```sql
SELECT Name ,  SurfaceArea ,  IndepYear FROM country ORDER BY Population LIMIT 1
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q142

Database: `world_1`  (schema in the appendix)

**Question.** How many republic countries are there?

**Reference query under review.**
```sql
SELECT count(*) FROM country WHERE GovernmentForm  =  "Republic"
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q143

Database: `singer`  (schema in the appendix)

**Question.** What are the names of singers ordered by ascending wealth?

**Reference query under review.**
```sql
SELECT Name FROM singer ORDER BY Net_Worth_Millions ASC
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q144

Database: `car_1`  (schema in the appendix)

**Question.** For  volvo, how many cylinders does the car with the least accelerate have?

**Reference query under review.**
```sql
SELECT T1.cylinders FROM CARS_DATA AS T1 JOIN CAR_NAMES AS T2 ON T1.Id  =  T2.MakeId WHERE T2.Model  =  'volvo' ORDER BY T1.accelerate ASC LIMIT 1;
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q145

Database: `student_transcripts_tracking`  (schema in the appendix)

**Question.** Find the last name of the students who currently live in North Carolina but have not registered in any degree program.

**Reference query under review.**
```sql
SELECT T1.last_name FROM Students AS T1 JOIN Addresses AS T2 ON T1.current_address_id  =  T2.address_id WHERE T2.state_province_county  =  'NorthCarolina' EXCEPT SELECT DISTINCT T3.last_name FROM Students AS T3 JOIN Student_Enrolment AS T4 ON T3.student_id  =  T4.student_id
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q146

Database: `world_1`  (schema in the appendix)

**Question.** What are the cities who have more than 160000 people and less than 900000 people?

**Reference query under review.**
```sql
SELECT name FROM city WHERE Population BETWEEN 160000 AND 900000
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q147

Database: `car_1`  (schema in the appendix)

**Question.** What is the average horsepower of the cars before 1980?

**Reference query under review.**
```sql
SELECT avg(horsepower) FROM CARS_DATA WHERE YEAR  <  1980;
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q148

Database: `course_teach`  (schema in the appendix)

**Question.** What are the names of the teachers  from youngest to oldest?

**Reference query under review.**
```sql
SELECT Name FROM teacher ORDER BY Age ASC
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q149

Database: `pets_1`  (schema in the appendix)

**Question.** What is the first name of every student who has a dog but does not have a cat?

**Reference query under review.**
```sql
SELECT T1.fname ,  T1.age FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid  =  T2.stuid JOIN pets AS T3 ON T3.petid  =  T2.petid WHERE T3.pettype  =  'dog' AND T1.stuid NOT IN (SELECT T1.stuid FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid  =  T2.stuid JOIN pets AS T3 ON T3.petid  =  T2.petid WHERE T3.pettype  =  'cat')
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q150

Database: `world_1`  (schema in the appendix)

**Question.** Give the names of nations that speak both English and French.

**Reference query under review.**
```sql
SELECT T1.Name FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code  =  T2.CountryCode WHERE T2.Language  =  "English" INTERSECT SELECT T1.Name FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code  =  T2.CountryCode WHERE T2.Language  =  "French"
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q151

Database: `network_1`  (schema in the appendix)

**Question.** What is the lowest grade of students who do not have any friends?

**Reference query under review.**
```sql
SELECT min(grade) FROM Highschooler WHERE id NOT IN (SELECT T1.student_id FROM Friend AS T1 JOIN Highschooler AS T2 ON T1.student_id  =  T2.id)
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q152

Database: `world_1`  (schema in the appendix)

**Question.** What are the African countries that have less people than any country in Asia?

**Reference query under review.**
```sql
SELECT Name FROM country WHERE Continent  =  "Africa"  AND population  <  (SELECT max(population) FROM country WHERE Continent  =  "Asia")
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:


### Q153

Database: `wta_1`  (schema in the appendix)

**Question.** How many different winners both participated in the WTA Championships and were left handed?

**Reference query under review.**
```sql
SELECT count(DISTINCT winner_name) FROM matches WHERE tourney_name  =  'WTA Championships' AND winner_hand  =  'L'
```

Verdict: ______  Defect type: ______  Borderline: ______

Note:



## Schema appendix

### `battle_death`

Run queries against `data/spider/test_suite_database/battle_death/battle_death.sqlite`.

```
  battle(id INT, name TEXT, date TEXT, bulgarian_commander TEXT, latin_commander TEXT, result TEXT)
  death(caused_by_ship_id INT, id INT, note TEXT, killed INT, injured INT)
  ship(lost_in_battle INT, id INT, name TEXT, tonnage TEXT, ship_type TEXT, location TEXT, disposition_of_ship TEXT)
```

### `car_1`

Run queries against `data/spider/test_suite_database/car_1/car_1.sqlite`.

```
  car_makers(Id INTEGER, Maker TEXT, FullName TEXT, Country TEXT)
  car_names(MakeId INTEGER, Model TEXT, Make TEXT)
  cars_data(Id INTEGER, MPG TEXT, Cylinders INTEGER, Edispl REAL, Horsepower TEXT, Weight INTEGER, Accelerate REAL, Year INTEGER)
  continents(ContId INTEGER, Continent TEXT)
  countries(CountryId INTEGER, CountryName TEXT, Continent INTEGER)
  model_list(ModelId INTEGER, Maker INTEGER, Model TEXT)
```

### `concert_singer`

Run queries against `data/spider/test_suite_database/concert_singer/concert_singer.sqlite`.

```
  concert(concert_ID INT, concert_Name TEXT, Theme TEXT, Stadium_ID TEXT, Year TEXT)
  singer(Singer_ID INT, Name TEXT, Country TEXT, Song_Name TEXT, Song_release_year TEXT, Age INT, Is_male bool)
  singer_in_concert(concert_ID INT, Singer_ID TEXT)
  stadium(Stadium_ID INT, Location TEXT, Name TEXT, Capacity INT, Highest INT, Lowest INT, Average INT)
```

### `course_teach`

Run queries against `data/spider/test_suite_database/course_teach/course_teach.sqlite`.

```
  course(Course_ID INT, Staring_Date TEXT, Course TEXT)
  course_arrange(Course_ID INT, Teacher_ID INT, Grade INT)
  teacher(Teacher_ID INT, Name TEXT, Age TEXT, Hometown TEXT)
```

### `dog_kennels`

Run queries against `data/spider/test_suite_database/dog_kennels/dog_kennels.sqlite`.

```
  Breeds(breed_code VARCHAR(10), breed_name VARCHAR(80))
  Charges(charge_id INTEGER, charge_type VARCHAR(10), charge_amount DECIMAL(19,4))
  Dogs(dog_id INTEGER, owner_id INTEGER, abandoned_yn VARCHAR(1), breed_code VARCHAR(10), size_code VARCHAR(10), name VARCHAR(50), age VARCHAR(20), date_of_birth DATETIME, gender VARCHAR(1), weight VARCHAR(20), date_arrived DATETIME, date_adopted DATETIME, date_departed DATETIME)
  Owners(owner_id INTEGER, first_name VARCHAR(50), last_name VARCHAR(50), street VARCHAR(50), city VARCHAR(50), state VARCHAR(20), zip_code VARCHAR(20), email_address VARCHAR(50), home_phone VARCHAR(20), cell_number VARCHAR(20))
  Professionals(professional_id INTEGER, role_code VARCHAR(10), first_name VARCHAR(50), street VARCHAR(50), city VARCHAR(50), state VARCHAR(20), zip_code VARCHAR(20), last_name VARCHAR(50), email_address VARCHAR(50), home_phone VARCHAR(20), cell_number VARCHAR(20))
  Sizes(size_code VARCHAR(10), size_description VARCHAR(80))
  Treatment_Types(treatment_type_code VARCHAR(10), treatment_type_description VARCHAR(80))
  Treatments(treatment_id INTEGER, dog_id INTEGER, professional_id INTEGER, treatment_type_code VARCHAR(10), date_of_treatment DATETIME, cost_of_treatment DECIMAL(19,4))
```

### `employee_hire_evaluation`

Run queries against `data/spider/test_suite_database/employee_hire_evaluation/employee_hire_evaluation.sqlite`.

```
  employee(Employee_ID INT, Name TEXT, Age INT, City TEXT)
  evaluation(Employee_ID TEXT, Year_awarded TEXT, Bonus REAL)
  hiring(Shop_ID INT, Employee_ID INT, Start_from TEXT, Is_full_time bool)
  shop(Shop_ID INT, Name TEXT, Location TEXT, District TEXT, Number_products INT, Manager_name TEXT)
```

### `flight_2`

Run queries against `data/spider/test_suite_database/flight_2/flight_2.sqlite`.

```
  airlines(uid INTEGER, Airline TEXT, Abbreviation TEXT, Country TEXT)
  airports(City TEXT, AirportCode TEXT, AirportName TEXT, Country TEXT, CountryAbbrev TEXT)
  flights(Airline INTEGER, FlightNo INTEGER, SourceAirport TEXT, DestAirport TEXT)
```

### `museum_visit`

Run queries against `data/spider/test_suite_database/museum_visit/museum_visit.sqlite`.

```
  museum(Museum_ID INT, Name TEXT, Num_of_Staff INT, Open_Year TEXT)
  visit(Museum_ID INT, visitor_ID TEXT, Num_of_Ticket INT, Total_spent REAL)
  visitor(ID INT, Name TEXT, Level_of_membership INT, Age INT)
```

### `network_1`

Run queries against `data/spider/test_suite_database/network_1/network_1.sqlite`.

```
  Friend(student_id INT, friend_id INT)
  Highschooler(ID INT, name TEXT, grade INT)
  Likes(student_id INT, liked_id INT)
```

### `orchestra`

Run queries against `data/spider/test_suite_database/orchestra/orchestra.sqlite`.

```
  conductor(Conductor_ID INT, Name TEXT, Age INT, Nationality TEXT, Year_of_Work INT)
  orchestra(Orchestra_ID INT, Orchestra TEXT, Conductor_ID INT, Record_Company TEXT, Year_of_Founded REAL, Major_Record_Format TEXT)
  performance(Performance_ID INT, Orchestra_ID INT, Type TEXT, Date TEXT, Official_ratings_(millions) REAL, Weekly_rank TEXT, Share TEXT)
  show(Show_ID INT, Performance_ID INT, If_first_show bool, Result TEXT, Attendance REAL)
```

### `pets_1`

Run queries against `data/spider/test_suite_database/pets_1/pets_1.sqlite`.

```
  Has_Pet(StuID INTEGER, PetID INTEGER)
  Pets(PetID INTEGER, PetType VARCHAR(20), pet_age INTEGER, weight REAL)
  Student(StuID INTEGER, LName VARCHAR(12), Fname VARCHAR(12), Age INTEGER, Sex VARCHAR(1), Major INTEGER, Advisor INTEGER, city_code VARCHAR(3))
```

### `poker_player`

Run queries against `data/spider/test_suite_database/poker_player/poker_player.sqlite`.

```
  people(People_ID INT, Nationality TEXT, Name TEXT, Birth_Date TEXT, Height REAL)
  poker_player(Poker_Player_ID INT, People_ID INT, Final_Table_Made REAL, Best_Finish REAL, Money_Rank REAL, Earnings REAL)
```

### `singer`

Run queries against `data/spider/test_suite_database/singer/singer.sqlite`.

```
  singer(Singer_ID INT, Name TEXT, Birth_Year REAL, Net_Worth_Millions REAL, Citizenship TEXT)
  song(Song_ID INT, Title TEXT, Singer_ID INT, Sales REAL, Highest_Position REAL)
```

### `student_transcripts_tracking`

Run queries against `data/spider/test_suite_database/student_transcripts_tracking/student_transcripts_tracking.sqlite`.

```
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
```

### `tvshow`

Run queries against `data/spider/test_suite_database/tvshow/tvshow.sqlite`.

```
  Cartoon(id REAL, Title TEXT, Directed_by TEXT, Written_by TEXT, Original_air_date TEXT, Production_code REAL, Channel TEXT)
  TV_Channel(id TEXT, series_name TEXT, Country TEXT, Language TEXT, Content TEXT, Pixel_aspect_ratio_PAR TEXT, Hight_definition_TV TEXT, Pay_per_view_PPV TEXT, Package_Option TEXT)
  TV_series(id REAL, Episode TEXT, Air_Date TEXT, Rating TEXT, Share REAL, 18_49_Rating_Share TEXT, Viewers_m TEXT, Weekly_Rank REAL, Channel TEXT)
```

### `world_1`

Run queries against `data/spider/test_suite_database/world_1/world_1.sqlite`.

```
  city(ID INTEGER, Name char(35), CountryCode char(3), District char(20), Population INTEGER)
  country(Code char(3), Name char(52), Continent TEXT, Region char(26), SurfaceArea float(10,2), IndepYear INTEGER, Population INTEGER, LifeExpectancy float(3,1), GNP float(10,2), GNPOld float(10,2), LocalName char(45), GovernmentForm char(45), HeadOfState char(60), Capital INTEGER, Code2 char(2))
  countrylanguage(CountryCode char(3), Language char(30), IsOfficial TEXT, Percentage float(4,1))
```

### `wta_1`

Run queries against `data/spider/test_suite_database/wta_1/wta_1.sqlite`.

```
  matches(best_of INT, draw_size INT, loser_age FLOAT, loser_entry TEXT, loser_hand TEXT, loser_ht INT, loser_id INT, loser_ioc TEXT, loser_name TEXT, loser_rank INT, loser_rank_points INT, loser_seed INT, match_num INT, minutes INT, round TEXT, score TEXT, surface TEXT, tourney_date DATE, tourney_id TEXT, tourney_level TEXT, tourney_name TEXT, winner_age FLOAT, winner_entry TEXT, winner_hand TEXT, winner_ht INT, winner_id INT, winner_ioc TEXT, winner_name TEXT, winner_rank INT, winner_rank_points INT, winner_seed INT, year INT)
  players(player_id INT, first_name TEXT, last_name TEXT, hand TEXT, birth_date DATE, country_code TEXT)
  rankings(ranking_date DATE, ranking INT, player_id INT, ranking_points INT, tours INT)
```
