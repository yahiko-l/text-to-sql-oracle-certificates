# Semantic audit dossier: every wrong answer of the two cells REPAIR contrasts

Built 2026-09-06. Population definition: every answer either the current-practice cell A or the strong cell D returns and the strong oracle rejects.

2779 such answers across 12 pools (6096 answers examined per cell) collapse to 742 distinct (question, returned SQL) cases over 203 questions. Every case in the population was judged: this is a census, not a sample.

240 of those cases were judged in an earlier round under the same protocol and are not repeated here. The 502 listed below are the ones still to judge.

In every case the distilled test suite rejects the returned query. In 472 of the 502 the shipped benchmark database rejects it too, and then the first disagreeing instance IS that shipped database, which the benchmark provides rather than generates. Exculpating such a case as an instance defect is therefore a claim about the benchmark's own database. The comparator is the official `result_eq`, called with the gold first, and whether row order is compared is a property of the gold, as in the frozen analyser.

`instances disagreeing` counts suite instances where the two queries differ. A difference on one instance out of fifty and a difference on all of them are very different evidence, so the count is given for every case.


## Cases

### R001  (question 25, database `concert_singer`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed303, kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 33/49, 25/50, 31/50, 31/50, 32/50
- Instances disagreeing: 27 of 32 (84%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** List all singer names in concerts in  2014.

**Gold.**
```sql
SELECT T2.name FROM singer_in_concert AS T1 JOIN singer AS T2 ON T1.singer_id  =  T2.singer_id JOIN concert AS T3 ON T1.concert_id  =  T3.concert_id WHERE T3.year  =  2014
```

**Returned.**
```sql
SELECT DISTINCT T3.Name
FROM concert AS T1
INNER JOIN singer_in_concert AS T2 ON T1.concert_ID = T2.concert_ID
INNER JOIN singer AS T3 ON T2.Singer_ID = T3.Singer_ID
WHERE T1.Year = '2014'
```

**First disagreeing instance** `concert_singer.sqlite` (this is the shipped benchmark database).

Gold returns 6 row(s), 1 column(s):

    Timbaland
    Justin Brown
    John Nizinik
    Justin Brown
    Tribal King
    Rose White

Returned query gives 5 row(s), 1 column(s):

    Timbaland
    Justin Brown
    John Nizinik
    Tribal King
    Rose White

Difference: duplicate_multiplicity_only; 5 row(s) in common, 0 only in the gold, 0 only in the returned result.

### R002  (question 26, database `concert_singer`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303, kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 44/50, 43/50, 43/50, 41/50, 42/50, 43/50
- Instances disagreeing: 27 of 32 (84%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the names of the singers who performed in a concert in 2014?

**Gold.**
```sql
SELECT T2.name FROM singer_in_concert AS T1 JOIN singer AS T2 ON T1.singer_id  =  T2.singer_id JOIN concert AS T3 ON T1.concert_id  =  T3.concert_id WHERE T3.year  =  2014
```

**Returned.**
```sql
SELECT DISTINCT T3.Name
FROM concert AS T1
INNER JOIN singer_in_concert AS T2 ON T1.concert_ID = T2.concert_ID
INNER JOIN singer AS T3 ON T2.Singer_ID = T3.Singer_ID
WHERE T1.Year = '2014'
```

**First disagreeing instance** `concert_singer.sqlite` (this is the shipped benchmark database).

Gold returns 6 row(s), 1 column(s):

    Timbaland
    Justin Brown
    John Nizinik
    Justin Brown
    Tribal King
    Rose White

Returned query gives 5 row(s), 1 column(s):

    Timbaland
    Justin Brown
    John Nizinik
    Tribal King
    Rose White

Difference: duplicate_multiplicity_only; 5 row(s) in common, 0 only in the gold, 0 only in the returned result.

### R003  (question 41, database `pets_1`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303
- Returned in cell: both A and D
- Class mass: 43/50, 38/50, 40/50
- Instances disagreeing: 26 of 27 (96%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find the first name of students who have cat or dog.

**Gold.**
```sql
SELECT DISTINCT T1.Fname FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid  =  T2.stuid JOIN pets AS T3 ON T3.petid  =  T2.petid WHERE T3.pettype  =  'cat' OR T3.pettype  =  'dog'
```

**Returned.**
```sql
SELECT T1.Fname
FROM Student AS T1
INNER JOIN Has_Pet AS T2 ON T1.StuID = T2.StuID
INNER JOIN Pets AS T3 ON T2.PetID = T3.PetID
WHERE T3.PetType IN ('cat', 'dog')
```

**First disagreeing instance** `pets_1.sqlite` (this is the shipped benchmark database).

Gold returns 2 row(s), 1 column(s):

    Linda
    Tracy

Returned query gives 3 row(s), 1 column(s):

    Linda
    Tracy
    Tracy

Difference: duplicate_multiplicity_only; 2 row(s) in common, 0 only in the gold, 0 only in the returned result.

### R004  (question 42, database `pets_1`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303
- Returned in cell: both A and D
- Class mass: 29/50, 32/50, 31/50
- Instances disagreeing: 26 of 27 (96%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the first names of every student who has a cat or dog?

**Gold.**
```sql
SELECT DISTINCT T1.Fname FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid  =  T2.stuid JOIN pets AS T3 ON T3.petid  =  T2.petid WHERE T3.pettype  =  'cat' OR T3.pettype  =  'dog'
```

**Returned.**
```sql
SELECT T1.Fname
FROM Student AS T1
INNER JOIN Has_Pet AS T2 ON T1.StuID = T2.StuID
INNER JOIN Pets AS T3 ON T2.PetID = T3.PetID
WHERE T3.PetType IN ('cat', 'dog')
```

**First disagreeing instance** `pets_1.sqlite` (this is the shipped benchmark database).

Gold returns 2 row(s), 1 column(s):

    Linda
    Tracy

Returned query gives 3 row(s), 1 column(s):

    Linda
    Tracy
    Tracy

Difference: duplicate_multiplicity_only; 2 row(s) in common, 0 only in the gold, 0 only in the returned result.

### R005  (question 50, database `pets_1`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303
- Returned in cell: both A and D
- Class mass: 34/50, 36/50, 40/50
- Instances disagreeing: 25 of 27 (93%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the first name of every student who has a dog but does not have a cat?

**Gold.**
```sql
SELECT T1.fname ,  T1.age FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid  =  T2.stuid JOIN pets AS T3 ON T3.petid  =  T2.petid WHERE T3.pettype  =  'dog' AND T1.stuid NOT IN (SELECT T1.stuid FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid  =  T2.stuid JOIN pets AS T3 ON T3.petid  =  T2.petid WHERE T3.pettype  =  'cat')
```

**Returned.**
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

**First disagreeing instance** `pets_1.sqlite` (this is the shipped benchmark database).

Gold returns 2 row(s), 2 column(s):

    Tracy | 19
    Tracy | 19

Returned query gives 2 row(s), 1 column(s):

    Tracy
    Tracy

Difference: col_count_differs, disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R006  (question 65, database `car_1`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 38/50, 42/50, 14/50
- Instances disagreeing: 4 of 60 (7%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find the make and production time of the cars that were produced in the earliest ?

**Gold.**
```sql
SELECT T2.Make ,  T1.Year FROM CARS_DATA AS T1 JOIN CAR_NAMES AS T2 ON T1.Id  =  T2.MakeId WHERE T1.Year  =  (SELECT min(YEAR) FROM CARS_DATA);
```

**Returned.**
```sql
SELECT T1.Make, T2.Year
FROM car_names AS T1
INNER JOIN cars_data AS T2 ON T1.MakeId = T2.Id
ORDER BY T2.Year ASC
LIMIT 1
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 35 row(s), 2 column(s):

    chevrolet chevelle malibu | 1970
    buick skylark 320 | 1970
    plymouth satellite | 1970
    amc rebel sst | 1970
    ford torino | 1970
    ford galaxie 500 | 1970
    chevrolet impala | 1970
    plymouth fury iii | 1970
    pontiac catalina | 1970
    amc ambassador dpl | 1970
    citroen ds-21 pallas | 1970
    chevrolet chevelle concours (sw) | 1970
    ... (35 rows total)

Returned query gives 1 row(s), 2 column(s):

    chevrolet chevelle malibu | 1970

Difference: rep_subset_of_gold; 1 row(s) in common, 34 only in the gold, 0 only in the returned result.

### R007  (question 66, database `car_1`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303, kwai-autosql-14b/seed101, kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 31/50, 34/50, 33/50, 10/50, 10/50
- Instances disagreeing: 60 of 60 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the maker of the carr produced in the earliest  and what  year was it?

**Gold.**
```sql
SELECT T2.Make ,  T1.Year FROM CARS_DATA AS T1 JOIN CAR_NAMES AS T2 ON T1.Id  =  T2.MakeId WHERE T1.Year  =  (SELECT min(YEAR) FROM CARS_DATA);
```

**Returned.**
```sql
SELECT T4.Maker, T1.Year
FROM cars_data AS T1
INNER JOIN car_names AS T2 ON T1.Id = T2.MakeId
INNER JOIN model_list AS T3 ON T2.Model = T3.Model
INNER JOIN car_makers AS T4 ON T3.Maker = T4.Id
ORDER BY T1.Year ASC
LIMIT 1
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 35 row(s), 2 column(s):

    chevrolet chevelle malibu | 1970
    buick skylark 320 | 1970
    plymouth satellite | 1970
    amc rebel sst | 1970
    ford torino | 1970
    ford galaxie 500 | 1970
    chevrolet impala | 1970
    plymouth fury iii | 1970
    pontiac catalina | 1970
    amc ambassador dpl | 1970
    citroen ds-21 pallas | 1970
    chevrolet chevelle concours (sw) | 1970
    ... (35 rows total)

Returned query gives 1 row(s), 2 column(s):

    gm | 1970

Difference: disjoint; 0 row(s) in common, 35 only in the gold, 1 only in the returned result.

### R008  (question 73, database `car_1`)

- Returned by: kwai-autosql-32b/seed101
- Returned in cell: both A and D
- Class mass: 25/50
- Instances disagreeing: 2 of 60 (3%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the accelerate of amc hornet sportabout (sw)?

**Gold.**
```sql
SELECT T1.Accelerate FROM CARS_DATA AS T1 JOIN CAR_NAMES AS T2 ON T1.Id  =  T2.MakeId WHERE T2.Make  =  'amc hornet sportabout (sw)';
```

**Returned.**
```sql
SELECT T2.Accelerate
FROM car_names AS T1
INNER JOIN cars_data AS T2 ON T1.MakeId = T2.Id
WHERE T1.Model = 'amc hornet sportabout (sw)'
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    13.5

Returned query gives 0 row(s), None column(s):

    (no rows)

Difference: rep_empty; 0 row(s) in common, 1 only in the gold, 0 only in the returned result.

### R009  (question 82, database `car_1`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202
- Returned in cell: both A and D
- Class mass: 40/50, 37/50
- Instances disagreeing: 59 of 60 (98%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the number of the cars with  more than 150 hp?

**Gold.**
```sql
SELECT count(*) FROM CARS_DATA WHERE horsepower  >  150;
```

**Returned.**
```sql
SELECT COUNT(*)
FROM cars_data
WHERE CAST(Horsepower AS INTEGER) > 150
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    281

Returned query gives 1 row(s), 1 column(s):

    49

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R010  (question 83, database `car_1`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-14b/seed101, kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 41/50, 40/50, 26/50, 30/50
- Instances disagreeing: 59 of 60 (98%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the number of cars with over 150 hp?

**Gold.**
```sql
SELECT count(*) FROM CARS_DATA WHERE horsepower  >  150;
```

**Returned.**
```sql
SELECT COUNT(*)
FROM cars_data
WHERE CAST(Horsepower AS INTEGER) > 150
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    281

Returned query gives 1 row(s), 1 column(s):

    49

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R011  (question 86, database `car_1`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed303
- Returned in cell: both A and D
- Class mass: 38/50, 39/50
- Instances disagreeing: 58 of 60 (97%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Which model saves the most gasoline?

**Gold.**
```sql
SELECT T1.Model FROM CAR_NAMES AS T1 JOIN CARS_DATA AS T2 ON T1.MakeId  =  T2.Id ORDER BY T2.mpg DESC LIMIT 1;
```

**Returned.**
```sql
SELECT T2.Model
FROM cars_data AS T1
INNER JOIN car_names AS T2 ON T1.Id = T2.MakeId
ORDER BY CAST(T1.MPG AS REAL) DESC
LIMIT 1
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    citroen

Returned query gives 1 row(s), 1 column(s):

    mazda

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R012  (question 87, database `car_1`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303
- Returned in cell: both A and D
- Class mass: 38/50, 41/50, 37/50
- Instances disagreeing: 58 of 60 (97%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What is the car wmodel that is the most fuel efficient?

**Gold.**
```sql
select t1.model from car_names as t1 join cars_data as t2 on t1.makeid  =  t2.id order by t2.mpg desc limit 1;
```

**Returned.**
```sql
SELECT T2.Model
FROM cars_data AS T1
INNER JOIN car_names AS T2 ON T1.Id = T2.MakeId
ORDER BY CAST(T1.MPG AS REAL) DESC
LIMIT 1
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    citroen

Returned query gives 1 row(s), 1 column(s):

    mazda

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R013  (question 98, database `car_1`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 44/50, 45/50, 37/50, 39/50, 41/50
- Instances disagreeing: 30 of 60 (50%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the names and ids of all car companies with more than 3 models?

**Gold.**
```sql
SELECT T1.FullName ,  T1.Id FROM CAR_MAKERS AS T1 JOIN MODEL_LIST AS T2 ON T1.Id  =  T2.Maker GROUP BY T1.Id HAVING count(*)  >  3;
```

**Returned.**
```sql
SELECT T1.Id, T1.Maker
FROM car_makers AS T1
INNER JOIN model_list AS T2 ON T1.Id = T2.Maker
GROUP BY T1.Id, T1.Maker
HAVING COUNT(T2.Model) > 3
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 2 row(s), 2 column(s):

    General Motors | 4
    Chrysler | 6

Returned query gives 2 row(s), 2 column(s):

    4 | gm
    6 | chrysler

Difference: disjoint; 0 row(s) in common, 2 only in the gold, 2 only in the returned result.

### R014  (question 101, database `car_1`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303
- Returned in cell: both A and D
- Class mass: 49/50, 45/50, 46/50
- Instances disagreeing: 49 of 60 (82%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** In which years cars were produced between 3000 and 4000 pounds?

**Gold.**
```sql
select distinct year from cars_data where weight between 3000 and 4000;
```

**Returned.**
```sql
SELECT Year
FROM cars_data
WHERE Weight BETWEEN 3000 AND 4000
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 13 row(s), 1 column(s):

    1970
    1971
    1972
    1973
    1974
    1975
    1976
    1977
    1978
    1979
    1980
    1981
    ... (13 rows total)

Returned query gives 107 row(s), 1 column(s):

    1970
    1970
    1970
    1970
    1970
    1970
    1970
    1970
    1970
    1970
    1970
    1970
    ... (107 rows total)

Difference: duplicate_multiplicity_only; 13 row(s) in common, 0 only in the gold, 0 only in the returned result.

### R015  (question 105, database `car_1`)

- Returned by: kwai-autosql-32b/seed101
- Returned in cell: both A and D
- Class mass: 38/50
- Instances disagreeing: 60 of 60 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** How many nations has more than 2 car makers ?

**Gold.**
```sql
select count(*) from countries as t1 join car_makers as t2 on t1.countryid  =  t2.country group by t1.countryid having count(*)  >  2
```

**Returned.**
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

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 4 row(s), 1 column(s):

    4
    4
    3
    5

Returned query gives 1 row(s), 1 column(s):

    4

Difference: rep_subset_of_gold; 1 row(s) in common, 2 only in the gold, 0 only in the returned result.

### R016  (question 106, database `car_1`)

- Returned by: kwai-autosql-32b/seed101
- Returned in cell: A only
- Class mass: 36/50
- Instances disagreeing: 60 of 60 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the number of nations with more than 2 car makers ?

**Gold.**
```sql
select count(*) from countries as t1 join car_makers as t2 on t1.countryid  =  t2.country group by t1.countryid having count(*)  >  2
```

**Returned.**
```sql
SELECT COUNT(*) FROM (
    SELECT Country FROM car_makers
    GROUP BY Country
    HAVING COUNT(*) > 2
)
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 4 row(s), 1 column(s):

    4
    4
    3
    5

Returned query gives 1 row(s), 1 column(s):

    4

Difference: rep_subset_of_gold; 1 row(s) in common, 2 only in the gold, 0 only in the returned result.

### R017  (question 106, database `car_1`)

- Returned by: kwai-autosql-32b/seed101
- Returned in cell: D only
- Class mass: 19/50
- Instances disagreeing: 60 of 60 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the number of nations with more than 2 car makers ?

**Gold.**
```sql
select count(*) from countries as t1 join car_makers as t2 on t1.countryid  =  t2.country group by t1.countryid having count(*)  >  2
```

**Returned.**
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

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 4 row(s), 1 column(s):

    4
    4
    3
    5

Returned query gives 1 row(s), 1 column(s):

    4

Difference: rep_subset_of_gold; 1 row(s) in common, 2 only in the gold, 0 only in the returned result.

### R018  (question 107, database `car_1`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 41/50, 40/50, 43/50, 37/50, 34/50
- Instances disagreeing: 52 of 60 (87%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** For all of the 4 CYL cars, which model has the most horsepower?

**Gold.**
```sql
SELECT T1.Model FROM CAR_NAMES AS T1 JOIN CARS_DATA AS T2 ON T1.MakeId  =  T2.Id WHERE T2.Cylinders  =  4 ORDER BY T2.horsepower DESC LIMIT 1;
```

**Returned.**
```sql
SELECT T2.Model
FROM cars_data AS T1
INNER JOIN car_names AS T2 ON T1.Id = T2.MakeId
WHERE T1.Cylinders = 4
ORDER BY CAST(T1.Horsepower AS INTEGER) DESC
LIMIT 1
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    ford

Returned query gives 1 row(s), 1 column(s):

    citroen

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R019  (question 109, database `car_1`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303
- Returned in cell: both A and D
- Class mass: 40/50, 40/50, 39/50
- Instances disagreeing: 56 of 60 (93%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Which models are lighter than 3500 but not built by the 'Ford Motor Company'?

**Gold.**
```sql
SELECT DISTINCT T1.model FROM MODEL_LIST AS T1 JOIN CAR_NAMES AS T2 ON T1.Model  =  T2.Model JOIN CARS_DATA AS T3 ON T2.MakeId  =  T3.Id JOIN CAR_MAKERS AS T4 ON T1.Maker  =  T4.Id WHERE T3.weight  <  3500 AND T4.FullName != 'Ford Motor Company';
```

**Returned.**
```sql
SELECT T1.Model
FROM car_names AS T1
INNER JOIN cars_data AS T2 ON T1.MakeId = T2.Id
INNER JOIN model_list AS T3 ON T1.Model = T3.Model
INNER JOIN car_makers AS T4 ON T3.Maker = T4.Id
WHERE T2.Weight < 3500
  AND T4.FullName != 'Ford Motor Company'
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 26 row(s), 1 column(s):

    plymouth
    amc
    citroen
    buick
    toyota
    datsun
    volkswagen
    peugeot
    audi
    saab
    bmw
    chevrolet
    ... (26 rows total)

Returned query gives 252 row(s), 1 column(s):

    plymouth
    amc
    citroen
    buick
    toyota
    plymouth
    amc
    datsun
    volkswagen
    peugeot
    audi
    saab
    ... (252 rows total)

Difference: duplicate_multiplicity_only; 26 row(s) in common, 0 only in the gold, 0 only in the returned result.

### R020  (question 114, database `flight_2`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303, kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 50/50, 50/50, 50/50, 50/50, 50/50, 50/50
- Instances disagreeing: 16 of 56 (29%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What country is Jetblue Airways affiliated with?

**Gold.**
```sql
SELECT Country FROM AIRLINES WHERE Airline  =  "JetBlue Airways"
```

**Returned.**
```sql
SELECT Country FROM airlines WHERE Airline = 'Jetblue Airways'
```

**First disagreeing instance** `flight_2.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    USA

Returned query gives 0 row(s), None column(s):

    (no rows)

Difference: rep_empty; 0 row(s) in common, 1 only in the gold, 0 only in the returned result.

### R021  (question 116, database `flight_2`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303, kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 50/50, 50/50, 49/50, 50/50, 50/50, 50/50
- Instances disagreeing: 16 of 56 (29%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Which abbreviation corresponds to Jetblue Airways?

**Gold.**
```sql
SELECT Abbreviation FROM AIRLINES WHERE Airline  =  "JetBlue Airways"
```

**Returned.**
```sql
SELECT Abbreviation FROM airlines WHERE Airline = 'Jetblue Airways'
```

**First disagreeing instance** `flight_2.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    JetBlue

Returned query gives 0 row(s), None column(s):

    (no rows)

Difference: rep_empty; 0 row(s) in common, 1 only in the gold, 0 only in the returned result.

### R022  (question 140, database `flight_2`)

- Returned by: kwai-autosql-32b/seed101
- Returned in cell: both A and D
- Class mass: 43/50
- Instances disagreeing: 8 of 56 (14%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Give the number of Jetblue Airways flights.

**Gold.**
```sql
SELECT count(*) FROM FLIGHTS AS T1 JOIN AIRLINES AS T2 ON T1.Airline  =  T2.uid WHERE T2.Airline = "JetBlue Airways"
```

**Returned.**
```sql
SELECT COUNT(*)
FROM flights
JOIN airlines ON flights.Airline = airlines.uid
WHERE airlines.Airline = 'Jetblue Airways'
```

**First disagreeing instance** `flight_2.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    100

Returned query gives 1 row(s), 1 column(s):

    0

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R023  (question 168, database `flight_2`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303
- Returned in cell: both A and D
- Class mass: 45/50, 46/50, 48/50
- Instances disagreeing: 33 of 56 (59%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Which airports do not have departing or arriving flights?

**Gold.**
```sql
SELECT AirportName FROM Airports WHERE AirportCode NOT IN (SELECT SourceAirport FROM Flights UNION SELECT DestAirport FROM Flights)
```

**Returned.**
```sql
SELECT AirportCode
FROM airports
WHERE AirportCode NOT IN (
    SELECT SourceAirport FROM flights
    UNION
    SELECT DestAirport FROM flights
)
```

**First disagreeing instance** `flight_2.sqlite` (this is the shipped benchmark database).

Gold returns 100 row(s), 1 column(s):

    Phillips AAF 
    Municipal 
    Dyess AFB 
    Municipal 
    Virginia Highlands 
    Ada 
    Adak Island Ns 
    Lenawee County 
    Municipal 
    Municipal 
    Ainsworth 
    Akhiok SPB 
    ... (100 rows total)

Returned query gives 100 row(s), 1 column(s):

    AAF
    ABI
    ABL
    ABQ
    ABR
    ABY
    ACV
    ADG
    ADK
    ADM
    ADR
    ADT
    ... (100 rows total)

Difference: disjoint; 0 row(s) in common, 89 only in the gold, 100 only in the returned result.

### R024  (question 191, database `course_teach`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303
- Returned in cell: both A and D
- Class mass: 50/50, 50/50, 50/50
- Instances disagreeing: 16 of 25 (64%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** List the name of teachers who are not from Little Lever Urban District.

**Gold.**
```sql
select name from teacher where hometown != "little lever urban district"
```

**Returned.**
```sql
SELECT Name
FROM teacher
WHERE Hometown != 'Little Lever Urban District'
```

**First disagreeing instance** `course_teach.sqlite` (this is the shipped benchmark database).

Gold returns 7 row(s), 1 column(s):

    Joseph Huts
    Gustaaf Deloor
    Vicente Carretero
    John Deloor
    Kearsley Brown
    Anne Walker
    Lucy Wong

Returned query gives 6 row(s), 1 column(s):

    Joseph Huts
    Gustaaf Deloor
    Vicente Carretero
    John Deloor
    Kearsley Brown
    Lucy Wong

Difference: rep_subset_of_gold; 6 row(s) in common, 1 only in the gold, 0 only in the returned result.

### R025  (question 192, database `course_teach`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303
- Returned in cell: both A and D
- Class mass: 50/50, 50/50, 50/50
- Instances disagreeing: 16 of 25 (64%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the names of the teachers who do not come from Little Lever Urban District?

**Gold.**
```sql
select name from teacher where hometown != "little lever urban district"
```

**Returned.**
```sql
SELECT Name
FROM teacher
WHERE Hometown != 'Little Lever Urban District'
```

**First disagreeing instance** `course_teach.sqlite` (this is the shipped benchmark database).

Gold returns 7 row(s), 1 column(s):

    Joseph Huts
    Gustaaf Deloor
    Vicente Carretero
    John Deloor
    Kearsley Brown
    Anne Walker
    Lucy Wong

Returned query gives 6 row(s), 1 column(s):

    Joseph Huts
    Gustaaf Deloor
    Vicente Carretero
    John Deloor
    Kearsley Brown
    Lucy Wong

Difference: rep_subset_of_gold; 6 row(s) in common, 1 only in the gold, 0 only in the returned result.

### R026  (question 213, database `museum_visit`)

- Returned by: kwai-autosql-32b/seed101
- Returned in cell: both A and D
- Class mass: 50/50
- Instances disagreeing: 35 of 35 (100%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What are the id, name and membership level of people who have paid the largest amount of money overall in all museum tickets?

**Gold.**
```sql
SELECT t2.visitor_id ,  t1.name ,  t1.Level_of_membership FROM visitor AS t1 JOIN visit AS t2 ON t1.id  =  t2.visitor_id GROUP BY t2.visitor_id ORDER BY sum(t2.Total_spent) DESC LIMIT 1
```

**Returned.**
```sql
SELECT T1.ID, T1.Name, T1.Level_of_membership
FROM visitor AS T1
INNER JOIN visit AS T2 ON T1.ID = T2.visitor_ID
ORDER BY T2.Total_spent DESC
LIMIT 1
```

**First disagreeing instance** `museum_visit.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 3 column(s):

    3 | Arjen Robben | 1

Returned query gives 1 row(s), 3 column(s):

    3 | Arjen Robben | 1

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R027  (question 223, database `wta_1`)

- Returned by: kwai-autosql-32b/seed101
- Returned in cell: A only
- Class mass: 33/50
- Instances disagreeing: 8 of 33 (24%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the names of players who won in both 2013 and 2016?

**Gold.**
```sql
SELECT winner_name FROM matches WHERE YEAR  =  2013 INTERSECT SELECT winner_name FROM matches WHERE YEAR  =  2016
```

**Returned.**
```sql
SELECT T1.first_name, T1.last_name
FROM players AS T1
INNER JOIN matches AS T2 ON T1.player_id = T2.winner_id
WHERE T2.year IN (2013, 2016)
GROUP BY T1.first_name, T1.last_name
HAVING COUNT(DISTINCT T2.year) = 2
```

**First disagreeing instance** `wta_1.sqlite` (this is the shipped benchmark database).

Gold returns 5 row(s), 1 column(s):

    Angelique Kerber
    Petra Kvitova
    Sara Errani
    Serena Williams
    Victoria Azarenka

Returned query gives 5 row(s), 2 column(s):

    Angelique | Kerber
    Petra | Kvitova
    Sara | Errani
    Serena | Williams
    Victoria | Azarenka

Difference: col_count_differs, disjoint; 0 row(s) in common, 5 only in the gold, 5 only in the returned result.

### R028  (question 230, database `wta_1`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303, omnisql-32b/seed202, omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 41/50, 41/50, 47/50, 41/50, 36/50
- Instances disagreeing: 33 of 33 (100%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** List the first and last name of all players ordered by their age.

**Gold.**
```sql
SELECT first_name ,  last_name FROM players ORDER BY birth_date
```

**Returned.**
```sql
SELECT first_name, last_name
FROM players
ORDER BY strftime('%Y', 'now') - strftime('%Y', birth_date)
```

**First disagreeing instance** `wta_1.sqlite` (this is the shipped benchmark database).

Gold returns 20662 row(s), 2 column(s):

    Thelma | Long
    Pauline | Addie
    Milly | Vagn Nielsen
    Vera | Johansen
    Reiko | Miyagi
    Louise | Brown
    Gertrude | Moran
    Zsuzsa | Kormoczy
    Peggy | Brixhe
    Betty | Pratt
    Doris | Hart
    Dorothy | Knode
    ... (20662 rows total)

Returned query gives 20662 row(s), 2 column(s):

    Martina | Hingis
    Mirjana | Lucic
    Justine | Henin
    Kerry Anne | Guse
    Jolene | Watanabe Giltz
    Karina | Habsudova
    Silvija | Talaja
    Alicia | Molik
    Tamarine | Tanasugarn
    Rita | Grande
    Katarina | Srebotnik
    Jana | Nejedly
    ... (20662 rows total)

Difference: row_order_only; 20658 row(s) in common, 0 only in the gold, 0 only in the returned result.

### R029  (question 231, database `wta_1`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303
- Returned in cell: both A and D
- Class mass: 31/50, 34/50, 27/50
- Instances disagreeing: 33 of 33 (100%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What are the full names of all players, sorted by age?

**Gold.**
```sql
SELECT first_name ,  last_name FROM players ORDER BY birth_date
```

**Returned.**
```sql
SELECT first_name, last_name
FROM players
ORDER BY strftime('%Y', 'now') - strftime('%Y', birth_date)
```

**First disagreeing instance** `wta_1.sqlite` (this is the shipped benchmark database).

Gold returns 20662 row(s), 2 column(s):

    Thelma | Long
    Pauline | Addie
    Milly | Vagn Nielsen
    Vera | Johansen
    Reiko | Miyagi
    Louise | Brown
    Gertrude | Moran
    Zsuzsa | Kormoczy
    Peggy | Brixhe
    Betty | Pratt
    Doris | Hart
    Dorothy | Knode
    ... (20662 rows total)

Returned query gives 20662 row(s), 2 column(s):

    Martina | Hingis
    Mirjana | Lucic
    Justine | Henin
    Kerry Anne | Guse
    Jolene | Watanabe Giltz
    Karina | Habsudova
    Silvija | Talaja
    Alicia | Molik
    Tamarine | Tanasugarn
    Rita | Grande
    Katarina | Srebotnik
    Jana | Nejedly
    ... (20662 rows total)

Difference: row_order_only; 20658 row(s) in common, 0 only in the gold, 0 only in the returned result.

### R030  (question 232, database `wta_1`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303, omnisql-32b/seed101, omnisql-32b/seed202, omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 42/50, 43/50, 45/50, 25/50, 30/50, 23/50
- Instances disagreeing: 8 of 33 (24%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** List the first and last name of all players who are left handed  in the order of age.

**Gold.**
```sql
SELECT first_name ,  last_name FROM players WHERE hand  =  'L' ORDER BY birth_date
```

**Returned.**
```sql
SELECT first_name, last_name
FROM players
WHERE hand = 'L'
ORDER BY strftime('%Y', 'now') - strftime('%Y', birth_date)
```

**First disagreeing instance** `wta_1.sqlite` (this is the shipped benchmark database).

Gold returns 487 row(s), 2 column(s):

    Ann | Jones
    Wendy | Gilchrist
    Martina | Navratilova
    Mary | Carillo
    Katerina | Bohmova
    Petra | Delhees Jauch
    Nancy | Loeffler Caro
    Lise | Gregory
    Rene | Collins
    Nicole | Arendt
    Florencia | Labat
    Sabine | Appelmans
    ... (487 rows total)

Returned query gives 487 row(s), 2 column(s):

    Florencia | Labat
    Magui | Serna
    Amanda | Grahame
    Sabine | Appelmans
    Jelena | Kostanic Tosic
    Gala | Leon Garcia
    Patty | Schnyder
    Anne Gaelle | Sidot
    Julie | Pullin
    Barbara | Schwartz
    Anca | Barna
    Amelie | Cocheteux
    ... (487 rows total)

Difference: row_order_only; 486 row(s) in common, 0 only in the gold, 0 only in the returned result.

### R031  (question 233, database `wta_1`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed303
- Returned in cell: both A and D
- Class mass: 19/50, 31/50
- Instances disagreeing: 8 of 33 (24%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What are the full names of all left handed players, in order of age?

**Gold.**
```sql
SELECT first_name ,  last_name FROM players WHERE hand  =  'L' ORDER BY birth_date
```

**Returned.**
```sql
SELECT first_name, last_name
FROM players
WHERE hand = 'L'
ORDER BY strftime('%Y', 'now') - strftime('%Y', birth_date)
```

**First disagreeing instance** `wta_1.sqlite` (this is the shipped benchmark database).

Gold returns 487 row(s), 2 column(s):

    Ann | Jones
    Wendy | Gilchrist
    Martina | Navratilova
    Mary | Carillo
    Katerina | Bohmova
    Petra | Delhees Jauch
    Nancy | Loeffler Caro
    Lise | Gregory
    Rene | Collins
    Nicole | Arendt
    Florencia | Labat
    Sabine | Appelmans
    ... (487 rows total)

Returned query gives 487 row(s), 2 column(s):

    Florencia | Labat
    Magui | Serna
    Amanda | Grahame
    Sabine | Appelmans
    Jelena | Kostanic Tosic
    Gala | Leon Garcia
    Patty | Schnyder
    Anne Gaelle | Sidot
    Julie | Pullin
    Barbara | Schwartz
    Anca | Barna
    Amelie | Cocheteux
    ... (487 rows total)

Difference: row_order_only; 486 row(s) in common, 0 only in the gold, 0 only in the returned result.

### R032  (question 234, database `wta_1`)

- Returned by: kwai-autosql-32b/seed101
- Returned in cell: both A and D
- Class mass: 13/50
- Instances disagreeing: 33 of 33 (100%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Find the name and rank points of the person who won the most times.

**Gold.**
```sql
SELECT winner_name ,  winner_rank_points FROM matches GROUP BY winner_name ORDER BY count(*) DESC LIMIT 1
```

**Returned.**
```sql
SELECT p.first_name, p.last_name, r.ranking_points
FROM matches m
INNER JOIN players p ON m.winner_id = p.player_id
INNER JOIN rankings r ON m.winner_id = r.player_id
GROUP BY m.winner_id
ORDER BY COUNT(m.winner_id) DESC
LIMIT 1
```

**First disagreeing instance** `wta_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    Angelique Kerber | 3715

Returned query gives 1 row(s), 3 column(s):

    Serena | Williams | 23

Difference: col_count_differs, disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R033  (question 235, database `wta_1`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202
- Returned in cell: both A and D
- Class mass: 20/50, 17/50
- Instances disagreeing: 33 of 33 (100%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What is the name of the player who has won the most matches, and how many rank points does this player have?

**Gold.**
```sql
SELECT winner_name ,  winner_rank_points FROM matches GROUP BY winner_name ORDER BY count(*) DESC LIMIT 1
```

**Returned.**
```sql
SELECT p.first_name, p.last_name, r.ranking_points
FROM matches m
JOIN players p ON m.winner_id = p.player_id
JOIN rankings r ON m.winner_id = r.player_id
GROUP BY m.winner_id, p.first_name, p.last_name, r.ranking_points
ORDER BY COUNT(m.winner_id) DESC
LIMIT 1
```

**First disagreeing instance** `wta_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    Angelique Kerber | 3715

Returned query gives 1 row(s), 3 column(s):

    Karolina | Pliskova | 4

Difference: col_count_differs, disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R034  (question 249, database `wta_1`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303
- Returned in cell: both A and D
- Class mass: 46/50, 48/50, 48/50
- Instances disagreeing: 4 of 33 (12%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find the number of left handed winners who participated in the WTA Championships.

**Gold.**
```sql
SELECT count(DISTINCT winner_name) FROM matches WHERE tourney_name  =  'WTA Championships' AND winner_hand  =  'L'
```

**Returned.**
```sql
SELECT COUNT(*)
FROM matches
WHERE winner_hand = 'L'
  AND tourney_name = 'WTA Championships'
```

**First disagreeing instance** `wta_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    2

Returned query gives 1 row(s), 1 column(s):

    3

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R035  (question 252, database `battle_death`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303
- Returned in cell: both A and D
- Class mass: 50/50, 50/50, 50/50
- Instances disagreeing: 27 of 28 (96%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What is the ship id and name that caused most total injuries?

**Gold.**
```sql
SELECT T2.id ,  T2.name FROM death AS T1 JOIN ship AS t2 ON T1.caused_by_ship_id  =  T2.id GROUP BY T2.id ORDER BY count(*) DESC LIMIT 1
```

**Returned.**
```sql
SELECT T1.id, T1.name
FROM ship AS T1
INNER JOIN death AS T2 ON T1.id = T2.caused_by_ship_id
GROUP BY T1.id, T1.name
ORDER BY SUM(T2.injured) DESC
LIMIT 1
```

**First disagreeing instance** `battle_death.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    5 | Three Brothers

Returned query gives 1 row(s), 2 column(s):

    4 | HMS Avon

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R036  (question 253, database `battle_death`)

- Returned by: kwai-autosql-32b/seed101
- Returned in cell: D only
- Class mass: 14/50
- Instances disagreeing: 3 of 28 (11%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** List the name and date the battle that has lost  Lettice and HMS Atalanta

**Gold.**
```sql
SELECT T1.name ,  T1.date FROM battle AS T1 JOIN ship AS T2 ON T1.id  =  T2.lost_in_battle WHERE T2.name  =  'Lettice' INTERSECT SELECT T1.name ,  T1.date FROM battle AS T1 JOIN ship AS T2 ON T1.id  =  T2.lost_in_battle WHERE T2.name  =  'HMS Atalanta'
```

**Returned.**
```sql
SELECT b.name, b.date
FROM battle b
JOIN ship s1 ON b.id = s1.lost_in_battle
JOIN ship s2 ON b.id = s2.lost_in_battle
WHERE s1.name = 'Lettice' AND s2.name = 'HMS Atalanta'
```

**First disagreeing instance** `battle_deathv515patch4.sqlite`.

Gold returns 2 row(s), 2 column(s):

    Battle of Philippopolis | East
    East | 1234

Returned query gives 1 row(s), 2 column(s):

    East | 1234

Difference: rep_subset_of_gold; 1 row(s) in common, 1 only in the gold, 0 only in the returned result.

### R037  (question 259, database `student_transcripts_tracking`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303
- Returned in cell: both A and D
- Class mass: 50/50, 50/50, 49/49
- Instances disagreeing: 22 of 55 (40%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find the last name of the students who currently live in North Carolina but have not registered in any degree program.

**Gold.**
```sql
SELECT T1.last_name FROM Students AS T1 JOIN Addresses AS T2 ON T1.current_address_id  =  T2.address_id WHERE T2.state_province_county  =  'NorthCarolina' EXCEPT SELECT DISTINCT T3.last_name FROM Students AS T3 JOIN Student_Enrolment AS T4 ON T3.student_id  =  T4.student_id
```

**Returned.**
```sql
SELECT T1.last_name
FROM Students AS T1
INNER JOIN Addresses AS T2 ON T1.current_address_id = T2.address_id
WHERE T2.state_province_county = 'North Carolina'
  AND T1.student_id NOT IN (SELECT student_id FROM Student_Enrolment)
```

**First disagreeing instance** `student_transcripts_tracking.sqlite` (this is the shipped benchmark database).

Gold returns 2 row(s), 1 column(s):

    Gleichner
    Weimann

Returned query gives 0 row(s), None column(s):

    (no rows)

Difference: rep_empty; 0 row(s) in common, 2 only in the gold, 0 only in the returned result.

### R038  (question 260, database `student_transcripts_tracking`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303
- Returned in cell: both A and D
- Class mass: 49/49, 50/50, 50/50
- Instances disagreeing: 22 of 55 (40%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the last name of the students who live in North Carolina but have not registered in any degree programs?

**Gold.**
```sql
SELECT T1.last_name FROM Students AS T1 JOIN Addresses AS T2 ON T1.current_address_id  =  T2.address_id WHERE T2.state_province_county  =  'NorthCarolina' EXCEPT SELECT DISTINCT T3.last_name FROM Students AS T3 JOIN Student_Enrolment AS T4 ON T3.student_id  =  T4.student_id
```

**Returned.**
```sql
SELECT T1.last_name
FROM Students AS T1
INNER JOIN Addresses AS T2 ON T1.current_address_id = T2.address_id
WHERE T2.state_province_county = 'North Carolina'
  AND T1.student_id NOT IN (SELECT student_id FROM Student_Enrolment)
```

**First disagreeing instance** `student_transcripts_tracking.sqlite` (this is the shipped benchmark database).

Gold returns 2 row(s), 1 column(s):

    Gleichner
    Weimann

Returned query gives 0 row(s), None column(s):

    (no rows)

Difference: rep_empty; 0 row(s) in common, 2 only in the gold, 0 only in the returned result.

### R039  (question 262, database `student_transcripts_tracking`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303, kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303, omnisql-32b/seed101, omnisql-32b/seed202, omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 50/50, 50/50, 50/50, 50/50, 50/50, 50/50, 50/50, 50/50, 49/50
- Instances disagreeing: 3 of 55 (5%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the mobile phone number of the student named Timmothy Ward ?

**Gold.**
```sql
select cell_mobile_number from students where first_name  =  'timmothy' and last_name  =  'ward'
```

**Returned.**
```sql
SELECT cell_mobile_number
FROM Students
WHERE first_name = 'Timmothy' AND last_name = 'Ward'
```

**First disagreeing instance** `student_transcripts_tracking.sqlite` (this is the shipped benchmark database).

Gold returns 0 row(s), None column(s):

    (no rows)

Returned query gives 1 row(s), 1 column(s):

    (096)889-8954x524

Difference: gold_empty; 0 row(s) in common, 0 only in the gold, 1 only in the returned result.

### R040  (question 266, database `student_transcripts_tracking`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303, kwai-autosql-14b/seed101, kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 47/50, 49/50, 25/50, 38/50, 44/50
- Instances disagreeing: 55 of 55 (100%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Which place holds the most number of students currently? List the id and all lines.

**Gold.**
```sql
SELECT T1.address_id ,  T1.line_1 ,  T1.line_2 FROM Addresses AS T1 JOIN Students AS T2 ON T1.address_id  =  T2.current_address_id GROUP BY T1.address_id ORDER BY count(*) DESC LIMIT 1
```

**Returned.**
```sql
SELECT T1.address_id, T1.line_1, T1.line_2, T1.line_3
FROM Addresses AS T1
INNER JOIN Students AS T2 ON T1.address_id = T2.current_address_id
GROUP BY T1.address_id
ORDER BY COUNT(T2.student_id) DESC
LIMIT 1
```

**First disagreeing instance** `student_transcripts_tracking.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 3 column(s):

    9 | 0643 Muller Vista | Suite 383

Returned query gives 1 row(s), 4 column(s):

    9 | 0643 Muller Vista | Suite 383 | NULL

Difference: col_count_differs, disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R041  (question 267, database `student_transcripts_tracking`)

- Returned by: kwai-autosql-32b/seed101
- Returned in cell: D only
- Class mass: 12/50
- Instances disagreeing: 39 of 55 (71%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What is the id, line 1, and line 2 of the place with the most students?

**Gold.**
```sql
SELECT T1.address_id ,  T1.line_1 ,  T1.line_2 FROM Addresses AS T1 JOIN Students AS T2 ON T1.address_id  =  T2.current_address_id GROUP BY T1.address_id ORDER BY count(*) DESC LIMIT 1
```

**Returned.**
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

**First disagreeing instance** `student_transcripts_trackingv5080.sqlite`.

Gold returns 1 row(s), 3 column(s):

    9700166583 | 10 | 6

Returned query gives 1 row(s), 3 column(s):

    7818984859 | 0643 Muller Vista | Tep7c2

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R042  (question 268, database `student_transcripts_tracking`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed303, kwai-autosql-14b/seed202
- Returned in cell: both A and D
- Class mass: 37/50, 41/50, 44/50
- Instances disagreeing: 40 of 55 (73%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find the semester when both Master students and Bachelor students got enrolled in.

**Gold.**
```sql
SELECT DISTINCT T2.semester_id FROM Degree_Programs AS T1 JOIN Student_Enrolment AS T2 ON T1.degree_program_id  =  T2.degree_program_id WHERE degree_summary_name  =  'Master' INTERSECT SELECT DISTINCT T2.semester_id FROM Degree_Programs AS T1 JOIN Student_Enrolment AS T2 ON T1.degree_program_id  =  T2.degree_program_id WHERE degree_summary_name  =  'Bachelor'
```

**Returned.**
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

**First disagreeing instance** `student_transcripts_tracking.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    13

Returned query gives 1 row(s), 1 column(s):

    fall 2018

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R043  (question 270, database `student_transcripts_tracking`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303, kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 50/50, 50/50, 50/50, 50/50, 50/50, 50/50
- Instances disagreeing: 16 of 55 (29%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find the first name of the students who permanently live in Haiti or have the cell phone number 09700166582.

**Gold.**
```sql
select t1.first_name from students as t1 join addresses as t2 on t1.permanent_address_id  =  t2.address_id where t2.country  =  'haiti' or t1.cell_mobile_number  =  '09700166582'
```

**Returned.**
```sql
SELECT T1.first_name
FROM Students AS T1
INNER JOIN Addresses AS T2 ON T1.permanent_address_id = T2.address_id
WHERE T2.country = 'Haiti' OR T1.cell_mobile_number = '09700166582'
```

**First disagreeing instance** `student_transcripts_tracking.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    Jarvis

Returned query gives 4 row(s), 1 column(s):

    Hobart
    Warren
    Jarvis
    Delaney

Difference: gold_subset_of_rep; 1 row(s) in common, 0 only in the gold, 3 only in the returned result.

### R044  (question 271, database `student_transcripts_tracking`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 50/50, 50/50, 50/50, 50/50
- Instances disagreeing: 16 of 55 (29%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the first names of the students who live in Haiti permanently or have the cell phone number 09700166582?

**Gold.**
```sql
select t1.first_name from students as t1 join addresses as t2 on t1.permanent_address_id  =  t2.address_id where t2.country  =  'haiti' or t1.cell_mobile_number  =  '09700166582'
```

**Returned.**
```sql
SELECT T1.first_name
FROM Students AS T1
INNER JOIN Addresses AS T2 ON T1.permanent_address_id = T2.address_id
WHERE T2.country = 'Haiti' OR T1.cell_mobile_number = '09700166582'
```

**First disagreeing instance** `student_transcripts_tracking.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    Jarvis

Returned query gives 4 row(s), 1 column(s):

    Hobart
    Warren
    Jarvis
    Delaney

Difference: gold_subset_of_rep; 1 row(s) in common, 0 only in the gold, 3 only in the returned result.

### R045  (question 309, database `tvshow`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202
- Returned in cell: both A and D
- Class mass: 41/50, 42/50
- Instances disagreeing: 12 of 25 (48%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** which countries' tv channels are not playing any cartoon  Todd Casey writes?

**Gold.**
```sql
SELECT country FROM TV_Channel EXCEPT SELECT T1.country FROM TV_Channel AS T1 JOIN cartoon AS T2 ON T1.id = T2.Channel WHERE T2.written_by  =  'Todd Casey'
```

**Returned.**
```sql
SELECT DISTINCT Country
FROM TV_Channel
WHERE id NOT IN (
    SELECT Channel
    FROM Cartoon
    WHERE Written_by = 'Todd Casey'
)
```

**First disagreeing instance** `tvshow.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    Poland

Returned query gives 3 row(s), 1 column(s):

    Italy
    United Kingdom
    Poland

Difference: gold_subset_of_rep; 1 row(s) in common, 0 only in the gold, 2 only in the returned result.

### R046  (question 310, database `tvshow`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 33/50, 32/50
- Instances disagreeing: 12 of 25 (48%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the countries that are not playing cartoons  Todd Casey writes?

**Gold.**
```sql
SELECT country FROM TV_Channel EXCEPT SELECT T1.country FROM TV_Channel AS T1 JOIN cartoon AS T2 ON T1.id = T2.Channel WHERE T2.written_by  =  'Todd Casey'
```

**Returned.**
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

**First disagreeing instance** `tvshow.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    Poland

Returned query gives 3 row(s), 1 column(s):

    Italy
    United Kingdom
    Poland

Difference: gold_subset_of_rep; 1 row(s) in common, 0 only in the gold, 2 only in the returned result.

### R047  (question 311, database `tvshow`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed303
- Returned in cell: both A and D
- Class mass: 23/50, 23/50
- Instances disagreeing: 25 of 25 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find the series name and country of the tv channel that is playing some cartoons  Ben Jones and Michael Chang directs?

**Gold.**
```sql
SELECT T1.series_name ,  T1.country FROM TV_Channel AS T1 JOIN cartoon AS T2 ON T1.id = T2.Channel WHERE T2.directed_by  =  'Michael Chang' INTERSECT SELECT T1.series_name ,  T1.country FROM TV_Channel AS T1 JOIN cartoon AS T2 ON T1.id = T2.Channel WHERE T2.directed_by  =  'Ben Jones'
```

**Returned.**
```sql
SELECT DISTINCT T.series_name, T.Country
FROM Cartoon C
INNER JOIN TV_Channel T ON C.Channel = T.id
WHERE C.Directed_by IN ('Ben Jones', 'Michael Chang')
```

**First disagreeing instance** `tvshow.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    MTV Dance | United Kingdom

Returned query gives 6 row(s), 2 column(s):

    Sky Radio | Italy
    Music Box Italia | Italy
    MTV Hits | Italy
    MTV Rocks | United Kingdom
    MTV Dance | United Kingdom
    Classica | Italy

Difference: gold_subset_of_rep; 1 row(s) in common, 0 only in the gold, 5 only in the returned result.

### R048  (question 312, database `tvshow`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202
- Returned in cell: both A and D
- Class mass: 29/50, 25/50
- Instances disagreeing: 25 of 25 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the series name and country of all TV channels that are playing cartoons  Ben Jones and Michael Chang directs?

**Gold.**
```sql
SELECT T1.series_name ,  T1.country FROM TV_Channel AS T1 JOIN cartoon AS T2 ON T1.id = T2.Channel WHERE T2.directed_by  =  'Michael Chang' INTERSECT SELECT T1.series_name ,  T1.country FROM TV_Channel AS T1 JOIN cartoon AS T2 ON T1.id = T2.Channel WHERE T2.directed_by  =  'Ben Jones'
```

**Returned.**
```sql
SELECT DISTINCT T.series_name, T.Country
FROM TV_Channel T
INNER JOIN Cartoon C ON T.id = C.Channel
WHERE C.Directed_by IN ('Ben Jones', 'Michael Chang')
```

**First disagreeing instance** `tvshow.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    MTV Dance | United Kingdom

Returned query gives 6 row(s), 2 column(s):

    Sky Radio | Italy
    Music Box Italia | Italy
    MTV Hits | Italy
    MTV Rocks | United Kingdom
    MTV Dance | United Kingdom
    Classica | Italy

Difference: gold_subset_of_rep; 1 row(s) in common, 0 only in the gold, 5 only in the returned result.

### R049  (question 315, database `tvshow`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303, omnisql-32b/seed101, omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 48/50, 46/50, 50/50, 28/50, 37/50, 43/50, 43/50
- Instances disagreeing: 25 of 25 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** find id of the tv channels that from the nations where have more than two tv channels.

**Gold.**
```sql
SELECT id FROM tv_channel GROUP BY country HAVING count(*)  >  2
```

**Returned.**
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

**First disagreeing instance** `tvshow.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    700

Returned query gives 12 row(s), 1 column(s):

    700
    701
    703
    704
    705
    708
    713
    714
    715
    717
    719
    728

Difference: gold_subset_of_rep; 1 row(s) in common, 0 only in the gold, 11 only in the returned result.

### R050  (question 362, database `world_1`)

- Returned by: kwai-autosql-32b/seed101
- Returned in cell: A only
- Class mass: 10/50
- Instances disagreeing: 5 of 46 (11%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the average GNP and total population in all US territory nations?

**Gold.**
```sql
SELECT avg(GNP) ,  sum(population) FROM country WHERE GovernmentForm  =  "US Territory"
```

**Returned.**
```sql
SELECT AVG(GNP) AS AverageGNP, SUM(Population) AS TotalPopulation
FROM country
WHERE GovernmentForm LIKE '%United States%'
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    510.3333333333333 | 329000

Returned query gives 1 row(s), 2 column(s):

    NULL | NULL

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R051  (question 362, database `world_1`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202
- Returned in cell: both A and D
- Class mass: 9/50, 10/50
- Instances disagreeing: 16 of 46 (35%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the average GNP and total population in all US territory nations?

**Gold.**
```sql
SELECT avg(GNP) ,  sum(population) FROM country WHERE GovernmentForm  =  "US Territory"
```

**Returned.**
```sql
SELECT AVG(GNP), SUM(Population)
FROM country
WHERE Region = 'Caribbean'
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    510.3333333333333 | 329000

Returned query gives 1 row(s), 2 column(s):

    4316.091666666666 | 38140000

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R052  (question 363, database `world_1`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303
- Returned in cell: both A and D
- Class mass: 18/50, 13/50, 17/48
- Instances disagreeing: 16 of 46 (35%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Give the mean GNP and total population of nations which are considered US territory.

**Gold.**
```sql
SELECT avg(GNP) ,  sum(population) FROM country WHERE GovernmentForm  =  "US Territory"
```

**Returned.**
```sql
SELECT AVG(GNP) AS MeanGNP, SUM(Population) AS TotalPopulation
FROM country
WHERE Region = 'Caribbean'
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    510.3333333333333 | 329000

Returned query gives 1 row(s), 2 column(s):

    4316.091666666666 | 38140000

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R053  (question 382, database `world_1`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303, kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 48/50, 47/50, 47/50, 45/50, 48/50, 45/50
- Instances disagreeing: 22 of 46 (48%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the countries where either English or Dutch is officially spoken ?

**Gold.**
```sql
select t1.name from country as t1 join countrylanguage as t2 on t1.code  =  t2.countrycode where t2.language  =  "english" and isofficial  =  "t" union select t1.name from country as t1 join countrylanguage as t2 on t1.code  =  t2.countrycode where t2.language  =  "dutch" and isofficial  =  "t"
```

**Returned.**
```sql
SELECT T1.Name
FROM country AS T1
INNER JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode
WHERE T2.Language IN ('English', 'Dutch') AND T2.IsOfficial = 'T'
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 0 row(s), None column(s):

    (no rows)

Returned query gives 48 row(s), 1 column(s):

    Aruba
    Anguilla
    Netherlands Antilles
    American Samoa
    Antigua and Barbuda
    Australia
    Belgium
    Belize
    Bermuda
    Barbados
    Canada
    Cocos (Keeling) Islands
    ... (48 rows total)

Difference: gold_empty; 0 row(s) in common, 0 only in the gold, 48 only in the returned result.

### R054  (question 383, database `world_1`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303
- Returned in cell: both A and D
- Class mass: 32/50, 34/50, 35/49
- Instances disagreeing: 31 of 46 (67%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Which language is the most popular on Asian ?

**Gold.**
```sql
SELECT T2.Language FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code  =  T2.CountryCode WHERE T1.Continent  =  "Asia" GROUP BY T2.Language ORDER BY COUNT (*) DESC LIMIT 1
```

**Returned.**
```sql
SELECT T2.Language
FROM country AS T1
INNER JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode
WHERE T1.Continent = 'Asia'
ORDER BY T2.Percentage DESC
LIMIT 1
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    Arabic

Returned query gives 1 row(s), 1 column(s):

    Dhivehi

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R055  (question 387, database `world_1`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed303
- Returned in cell: both A and D
- Class mass: 37/50, 41/50
- Instances disagreeing: 37 of 46 (80%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Find the city with the most people that uses English.

**Gold.**
```sql
SELECT T1.Name ,  T1.Population FROM city AS T1 JOIN countrylanguage AS T2 ON T1.CountryCode  =  T2.CountryCode WHERE T2.Language  =  "English" ORDER BY T1.Population DESC LIMIT 1
```

**Returned.**
```sql
SELECT T1.Name
FROM city AS T1
INNER JOIN countrylanguage AS T2 ON T1.CountryCode = T2.CountryCode
WHERE T2.Language = 'English'
ORDER BY T1.Population DESC
LIMIT 1
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    New York | 8008278

Returned query gives 1 row(s), 1 column(s):

    New York

Difference: col_count_differs, disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R056  (question 388, database `world_1`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303, kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 44/50, 47/50, 43/50, 50/50, 46/50, 50/50
- Instances disagreeing: 37 of 46 (80%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What is the most populace city that speaks English?

**Gold.**
```sql
SELECT T1.Name ,  T1.Population FROM city AS T1 JOIN countrylanguage AS T2 ON T1.CountryCode  =  T2.CountryCode WHERE T2.Language  =  "English" ORDER BY T1.Population DESC LIMIT 1
```

**Returned.**
```sql
SELECT T1.Name
FROM city AS T1
INNER JOIN countrylanguage AS T2 ON T1.CountryCode = T2.CountryCode
WHERE T2.Language = 'English'
ORDER BY T1.Population DESC
LIMIT 1
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    New York | 8008278

Returned query gives 1 row(s), 1 column(s):

    New York

Difference: col_count_differs, disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R057  (question 390, database `world_1`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303, kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 33/50, 36/50, 31/50, 29/50, 36/50, 38/50
- Instances disagreeing: 46 of 46 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is average life expectancy in the countries where English is not used officially ?

**Gold.**
```sql
SELECT avg(LifeExpectancy) FROM country WHERE Name NOT IN (SELECT T1.Name FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code  =  T2.CountryCode WHERE T2.Language  =  "English" AND T2.IsOfficial  =  "T")
```

**Returned.**
```sql
SELECT AVG(T1.LifeExpectancy)
FROM country AS T1
INNER JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode
WHERE T2.Language = 'English' AND T2.IsOfficial = 'F'
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    65.4827027027027

Returned query gives 1 row(s), 1 column(s):

    74.95

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R058  (question 400, database `world_1`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303
- Returned in cell: both A and D
- Class mass: 38/49, 42/50, 40/50
- Instances disagreeing: 28 of 46 (61%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the African countries that have less people than any country in Asia?

**Gold.**
```sql
SELECT Name FROM country WHERE Continent  =  "Africa"  AND population  <  (SELECT max(population) FROM country WHERE Continent  =  "Asia")
```

**Returned.**
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

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 58 row(s), 1 column(s):

    Angola
    Burundi
    Benin
    Burkina Faso
    Botswana
    Central African Republic
    Côte d’Ivoire
    Cameroon
    Congo, The Democratic Republic of the
    Congo
    Comoros
    Cape Verde
    ... (58 rows total)

Returned query gives 5 row(s), 1 column(s):

    British Indian Ocean Territory
    Mayotte
    Saint Helena
    Sao Tome and Principe
    Seychelles

Difference: rep_subset_of_gold; 5 row(s) in common, 53 only in the gold, 0 only in the returned result.

### R059  (question 402, database `world_1`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303
- Returned in cell: both A and D
- Class mass: 28/50, 33/50, 30/50
- Instances disagreeing: 29 of 46 (63%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Which Asian countries have more people than any country in Africa?

**Gold.**
```sql
SELECT Name FROM country WHERE Continent  =  "Asia"  AND population  >  (SELECT max(population) FROM country WHERE Continent  =  "Africa")
```

**Returned.**
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

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 6 row(s), 1 column(s):

    Bangladesh
    China
    Indonesia
    India
    Japan
    Pakistan

Returned query gives 51 row(s), 1 column(s):

    Afghanistan
    United Arab Emirates
    Armenia
    Azerbaijan
    Bangladesh
    Bahrain
    Brunei
    Bhutan
    China
    Cyprus
    Georgia
    Hong Kong
    ... (51 rows total)

Difference: gold_subset_of_rep; 6 row(s) in common, 0 only in the gold, 45 only in the returned result.

### R060  (question 403, database `world_1`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303
- Returned in cell: both A and D
- Class mass: 45/50, 43/50, 45/50
- Instances disagreeing: 29 of 46 (63%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the Asian countries have more people than that of any country in Africa?

**Gold.**
```sql
SELECT Name FROM country WHERE Continent  =  "Asia"  AND population  >  (SELECT min(population) FROM country WHERE Continent  =  "Africa")
```

**Returned.**
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

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 51 row(s), 1 column(s):

    Afghanistan
    United Arab Emirates
    Armenia
    Azerbaijan
    Bangladesh
    Bahrain
    Brunei
    Bhutan
    China
    Cyprus
    Georgia
    Hong Kong
    ... (51 rows total)

Returned query gives 6 row(s), 1 column(s):

    Bangladesh
    China
    Indonesia
    India
    Japan
    Pakistan

Difference: rep_subset_of_gold; 6 row(s) in common, 45 only in the gold, 0 only in the returned result.

### R061  (question 404, database `world_1`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202
- Returned in cell: both A and D
- Class mass: 18/50, 18/50
- Instances disagreeing: 32 of 46 (70%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the country codes for countries that do not speak English?

**Gold.**
```sql
SELECT CountryCode FROM countrylanguage EXCEPT SELECT CountryCode FROM countrylanguage WHERE LANGUAGE  =  "English"
```

**Returned.**
```sql
SELECT Code
FROM country
WHERE Code NOT IN (
    SELECT CountryCode
    FROM countrylanguage
    WHERE Language = 'English'
)
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 173 row(s), 1 column(s):

    AFG
    AGO
    ALB
    AND
    ARE
    ARG
    ARM
    AUT
    AZE
    BDI
    BEL
    BEN
    ... (173 rows total)

Returned query gives 179 row(s), 1 column(s):

    AFG
    AGO
    ALB
    AND
    ARE
    ARG
    ARM
    ATA
    ATF
    AUT
    AZE
    BDI
    ... (179 rows total)

Difference: gold_subset_of_rep; 173 row(s) in common, 0 only in the gold, 6 only in the returned result.

### R062  (question 405, database `world_1`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303, kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 16/50, 15/50, 20/50, 21/50
- Instances disagreeing: 44 of 46 (96%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Return the country codes for countries that do not speak English.

**Gold.**
```sql
SELECT CountryCode FROM countrylanguage EXCEPT SELECT CountryCode FROM countrylanguage WHERE LANGUAGE  =  "English"
```

**Returned.**
```sql
SELECT CountryCode
FROM countrylanguage
WHERE Language != 'English'
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 173 row(s), 1 column(s):

    AFG
    AGO
    ALB
    AND
    ARE
    ARG
    ARM
    AUT
    AZE
    BDI
    BEL
    BEN
    ... (173 rows total)

Returned query gives 924 row(s), 1 column(s):

    ABW
    ABW
    ABW
    AFG
    AFG
    AFG
    AFG
    AFG
    AGO
    AGO
    AGO
    AGO
    ... (924 rows total)

Difference: gold_subset_of_rep; 173 row(s) in common, 0 only in the gold, 50 only in the returned result.

### R063  (question 406, database `world_1`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303, kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 47/50, 47/50, 50/50, 50/50, 49/50, 50/50
- Instances disagreeing: 44 of 46 (96%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the country codes of countries where people speak other than English?

**Gold.**
```sql
SELECT DISTINCT CountryCode FROM countrylanguage WHERE LANGUAGE != "English"
```

**Returned.**
```sql
SELECT CountryCode
FROM countrylanguage
WHERE Language != 'English'
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 223 row(s), 1 column(s):

    ABW
    AFG
    AGO
    ALB
    AND
    ANT
    ARE
    ARG
    ARM
    ASM
    ATG
    AUS
    ... (223 rows total)

Returned query gives 924 row(s), 1 column(s):

    ABW
    ABW
    ABW
    AFG
    AFG
    AFG
    AFG
    AFG
    AGO
    AGO
    AGO
    AGO
    ... (924 rows total)

Difference: duplicate_multiplicity_only; 223 row(s) in common, 0 only in the gold, 0 only in the returned result.

### R064  (question 407, database `world_1`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303, kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 19/50, 20/50, 21/50, 37/50, 36/50, 35/50
- Instances disagreeing: 44 of 46 (96%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Give the country codes for countries in which people does not speak English.

**Gold.**
```sql
SELECT DISTINCT CountryCode FROM countrylanguage WHERE LANGUAGE != "English"
```

**Returned.**
```sql
SELECT CountryCode
FROM countrylanguage
WHERE Language != 'English'
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 223 row(s), 1 column(s):

    ABW
    AFG
    AGO
    ALB
    AND
    ANT
    ARE
    ARG
    ARM
    ASM
    ATG
    AUS
    ... (223 rows total)

Returned query gives 924 row(s), 1 column(s):

    ABW
    ABW
    ABW
    AFG
    AFG
    AFG
    AFG
    AFG
    AGO
    AGO
    AGO
    AGO
    ... (924 rows total)

Difference: duplicate_multiplicity_only; 223 row(s) in common, 0 only in the gold, 0 only in the returned result.

### R065  (question 410, database `world_1`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303
- Returned in cell: both A and D
- Class mass: 43/50, 41/50, 46/50
- Instances disagreeing: 9 of 46 (20%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Which cities are in European countries where English is not spoken officially?

**Gold.**
```sql
SELECT DISTINCT T2.Name FROM country AS T1 JOIN city AS T2 ON T2.CountryCode  =  T1.Code WHERE T1.Continent  =  'Europe' AND T1.Name NOT IN (SELECT T3.Name FROM country AS T3 JOIN countrylanguage AS T4 ON T3.Code  =  T4.CountryCode WHERE T4.IsOfficial  =  'T' AND T4.Language  =  'English')
```

**Returned.**
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

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 753 row(s), 1 column(s):

    Amsterdam
    Rotterdam
    Haag
    Utrecht
    Eindhoven
    Tilburg
    Groningen
    Breda
    Apeldoorn
    Nijmegen
    Enschede
    Haarlem
    ... (753 rows total)

Returned query gives 755 row(s), 1 column(s):

    Tirana
    Andorra la Vella
    Wien
    Graz
    Linz
    Salzburg
    Innsbruck
    Klagenfurt
    Antwerpen
    Gent
    Charleroi
    Liège
    ... (755 rows total)

Difference: duplicate_multiplicity_only; 753 row(s) in common, 0 only in the gold, 0 only in the returned result.

### R066  (question 411, database `world_1`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303
- Returned in cell: both A and D
- Class mass: 49/49, 49/50, 48/48
- Instances disagreeing: 1 of 46 (2%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Whic`h unique cities are in  Asian countries where Chinese is the official ?

**Gold.**
```sql
select distinct t3.name from country as t1 join countrylanguage as t2 on t1.code  =  t2.countrycode join city as t3 on t1.code  =  t3.countrycode where t2.isofficial  =  't' and t2.language  =  'chinese' and t1.continent  =  "asia"
```

**Returned.**
```sql
SELECT DISTINCT T1.Name
FROM city AS T1
INNER JOIN country AS T2 ON T1.CountryCode = T2.Code
INNER JOIN countrylanguage AS T3 ON T2.Code = T3.CountryCode
WHERE T2.Continent = 'Asia'
  AND T3.Language = 'Chinese'
  AND T3.IsOfficial = 'T'
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 0 row(s), None column(s):

    (no rows)

Returned query gives 359 row(s), 1 column(s):

    Shanghai
    Peking
    Chongqing
    Tianjin
    Wuhan
    Harbin
    Shenyang
    Kanton [Guangzhou]
    Chengdu
    Nanking [Nanjing]
    Changchun
    Xi´an
    ... (359 rows total)

Difference: gold_empty; 0 row(s) in common, 0 only in the gold, 359 only in the returned result.

### R067  (question 413, database `world_1`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303, kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 48/50, 50/50, 49/50, 50/50, 50/50, 50/50
- Instances disagreeing: 44 of 46 (96%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What are the name, independence year, and surface area of the country with the least number of nationalities?

**Gold.**
```sql
SELECT Name ,  SurfaceArea ,  IndepYear FROM country ORDER BY Population LIMIT 1
```

**Returned.**
```sql
SELECT T1.Name, T1.IndepYear, T1.SurfaceArea
FROM country AS T1
INNER JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode
GROUP BY T1.Code
ORDER BY COUNT(T2.Language) ASC
LIMIT 1
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 3 column(s):

    Antarctica | 13120000.0 | NULL

Returned query gives 1 row(s), 3 column(s):

    Anguilla | NULL | 96.0

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R068  (question 427, database `world_1`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303
- Returned in cell: both A and D
- Class mass: 50/50, 49/50, 49/50
- Instances disagreeing: 40 of 46 (87%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the total population and average area of countries in North America who is bigger than 3000 square miles

**Gold.**
```sql
select sum(population) ,  avg(surfacearea) from country where continent  =  "north america" and surfacearea  >  3000
```

**Returned.**
```sql
SELECT SUM(Population) AS TotalPopulation, AVG(SurfaceArea) AS AverageArea
FROM country
WHERE Continent = 'North America' AND SurfaceArea > 3000
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    NULL | NULL

Returned query gives 1 row(s), 2 column(s):

    480753000 | 1344763.7222222222

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R069  (question 428, database `world_1`)

- Returned by: kwai-autosql-32b/seed101
- Returned in cell: both A and D
- Class mass: 35/50
- Instances disagreeing: 40 of 46 (87%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Give the total population and average  corresponding to countries in Noth America that is bigger than 3000 square miles.

**Gold.**
```sql
select sum(population) ,  avg(surfacearea) from country where continent  =  "north america" and surfacearea  >  3000
```

**Returned.**
```sql
SELECT SUM(Population), AVG(Population)
FROM country
WHERE Continent = 'North America' AND SurfaceArea > 3000
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    NULL | NULL

Returned query gives 1 row(s), 2 column(s):

    480753000 | 26708500.0

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R070  (question 431, database `world_1`)

- Returned by: kwai-autosql-32b/seed101
- Returned in cell: both A and D
- Class mass: 17/50
- Instances disagreeing: 46 of 46 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the language spoken by the largest percentage of people in each nation?

**Gold.**
```sql
SELECT LANGUAGE ,  CountryCode ,  max(Percentage) FROM countrylanguage GROUP BY CountryCode
```

**Returned.**
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

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 233 row(s), 3 column(s):

    Papiamento | ABW | 76.7
    Pashto | AFG | 52.4
    Ovimbundu | AGO | 37.2
    English | AIA | 0.0
    Albaniana | ALB | 97.9
    Spanish | AND | 44.6
    Papiamento | ANT | 86.2
    Arabic | ARE | 42.0
    Spanish | ARG | 96.8
    Armenian | ARM | 93.4
    Samoan | ASM | 90.6
    Creole English | ATG | 95.7
    ... (233 rows total)

Returned query gives 233 row(s), 1 column(s):

    Papiamento
    Pashto
    Ovimbundu
    English
    Albaniana
    Spanish
    Papiamento
    Arabic
    Spanish
    Armenian
    Samoan
    Creole English
    ... (233 rows total)

Difference: col_count_differs, disjoint; 0 row(s) in common, 233 only in the gold, 131 only in the returned result.

### R071  (question 432, database `world_1`)

- Returned by: kwai-autosql-32b/seed101
- Returned in cell: both A and D
- Class mass: 25/49
- Instances disagreeing: 46 of 46 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the codes of the different nations, and what are the languages spoken by the greatest percentage of people for each?

**Gold.**
```sql
SELECT LANGUAGE ,  CountryCode ,  max(Percentage) FROM countrylanguage GROUP BY CountryCode
```

**Returned.**
```sql
SELECT CountryCode, Language
FROM countrylanguage
WHERE (CountryCode, Percentage) IN (
    SELECT CountryCode, MAX(Percentage)
    FROM countrylanguage
    GROUP BY CountryCode
)
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 233 row(s), 3 column(s):

    Papiamento | ABW | 76.7
    Pashto | AFG | 52.4
    Ovimbundu | AGO | 37.2
    English | AIA | 0.0
    Albaniana | ALB | 97.9
    Spanish | AND | 44.6
    Papiamento | ANT | 86.2
    Arabic | ARE | 42.0
    Spanish | ARG | 96.8
    Armenian | ARM | 93.4
    Samoan | ASM | 90.6
    Creole English | ATG | 95.7
    ... (233 rows total)

Returned query gives 241 row(s), 2 column(s):

    ABW | Papiamento
    AFG | Pashto
    AGO | Ovimbundu
    AIA | English
    ALB | Albaniana
    AND | Spanish
    ANT | Papiamento
    ARE | Arabic
    ARG | Spanish
    ARM | Armenian
    ASM | Samoan
    ATG | Creole English
    ... (241 rows total)

Difference: col_count_differs, disjoint; 0 row(s) in common, 233 only in the gold, 241 only in the returned result.

### R072  (question 433, database `world_1`)

- Returned by: kwai-autosql-32b/seed101
- Returned in cell: both A and D
- Class mass: 19/50
- Instances disagreeing: 46 of 46 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the total number of countries where Spanish is spoken by the largest percentage of people?

**Gold.**
```sql
SELECT count(*) ,   max(Percentage) FROM countrylanguage WHERE LANGUAGE  =  "Spanish" GROUP BY CountryCode
```

**Returned.**
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

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 28 row(s), 2 column(s):

    1 | 7.4
    1 | 44.6
    1 | 96.8
    1 | 31.6
    1 | 87.7
    1 | 0.7
    1 | 89.7
    1 | 99.0
    1 | 97.5
    1 | 100.0
    1 | 98.0
    1 | 93.0
    ... (28 rows total)

Returned query gives 1 row(s), 1 column(s):

    21

Difference: col_count_differs, disjoint; 0 row(s) in common, 27 only in the gold, 1 only in the returned result.

### R073  (question 434, database `world_1`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202
- Returned in cell: both A and D
- Class mass: 31/50, 29/50
- Instances disagreeing: 46 of 46 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Count the number of countries for which Spanish is predominantly spoken .

**Gold.**
```sql
SELECT count(*) ,   max(Percentage) FROM countrylanguage WHERE LANGUAGE  =  "Spanish" GROUP BY CountryCode
```

**Returned.**
```sql
SELECT COUNT(*)
FROM countrylanguage
WHERE Language = 'Spanish' AND IsOfficial = 'T'
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 28 row(s), 2 column(s):

    1 | 7.4
    1 | 44.6
    1 | 96.8
    1 | 31.6
    1 | 87.7
    1 | 0.7
    1 | 89.7
    1 | 99.0
    1 | 97.5
    1 | 100.0
    1 | 98.0
    1 | 93.0
    ... (28 rows total)

Returned query gives 1 row(s), 1 column(s):

    20

Difference: col_count_differs, disjoint; 0 row(s) in common, 27 only in the gold, 1 only in the returned result.

### R074  (question 435, database `world_1`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303, kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 39/50, 39/50, 34/50, 50/50, 50/50, 50/50
- Instances disagreeing: 43 of 46 (93%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the codes of countries where Spanish is spoken by the largest percentage of people?

**Gold.**
```sql
SELECT CountryCode ,  max(Percentage) FROM countrylanguage WHERE LANGUAGE  =  "Spanish" GROUP BY CountryCode
```

**Returned.**
```sql
SELECT CountryCode
FROM countrylanguage
WHERE Language = 'Spanish'
ORDER BY Percentage DESC
LIMIT 1
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 28 row(s), 2 column(s):

    ABW | 7.4
    AND | 44.6
    ARG | 96.8
    BLZ | 31.6
    BOL | 87.7
    CAN | 0.7
    CHL | 89.7
    COL | 99.0
    CRI | 97.5
    CUB | 100.0
    DOM | 98.0
    ECU | 93.0
    ... (28 rows total)

Returned query gives 1 row(s), 1 column(s):

    CUB

Difference: col_count_differs, disjoint; 0 row(s) in common, 28 only in the gold, 1 only in the returned result.

### R075  (question 436, database `world_1`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303, kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 39/50, 28/50, 24/49, 30/50, 29/50, 35/50
- Instances disagreeing: 43 of 46 (93%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Return the codes of countries for which Spanish is predominantly spoken .

**Gold.**
```sql
SELECT CountryCode ,  max(Percentage) FROM countrylanguage WHERE LANGUAGE  =  "Spanish" GROUP BY CountryCode
```

**Returned.**
```sql
SELECT CountryCode
FROM countrylanguage
WHERE Language = 'Spanish'
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 28 row(s), 2 column(s):

    ABW | 7.4
    AND | 44.6
    ARG | 96.8
    BLZ | 31.6
    BOL | 87.7
    CAN | 0.7
    CHL | 89.7
    COL | 99.0
    CRI | 97.5
    CUB | 100.0
    DOM | 98.0
    ECU | 93.0
    ... (28 rows total)

Returned query gives 28 row(s), 1 column(s):

    ABW
    AND
    ARG
    BLZ
    BOL
    CAN
    CHL
    COL
    CRI
    CUB
    DOM
    ECU
    ... (28 rows total)

Difference: col_count_differs, disjoint; 0 row(s) in common, 28 only in the gold, 28 only in the returned result.

### R076  (question 459, database `network_1`)

- Returned by: kwai-autosql-32b/seed101
- Returned in cell: D only
- Class mass: 26/50
- Instances disagreeing: 22 of 29 (76%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** How many likes does Kyle have?

**Gold.**
```sql
SELECT count(*) FROM Likes AS T1 JOIN Highschooler AS T2 ON T1.student_id  =  T2.id WHERE T2.name  =  "Kyle"
```

**Returned.**
```sql
SELECT COUNT(*)
FROM Likes
JOIN Highschooler ON Highschooler.ID = Likes.liked_id
WHERE Highschooler.name = 'Kyle'
```

**First disagreeing instance** `network_1v5080.sqlite`.

Gold returns 1 row(s), 1 column(s):

    21

Returned query gives 1 row(s), 1 column(s):

    30

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R077  (question 461, database `network_1`)

- Returned by: kwai-autosql-32b/seed101
- Returned in cell: both A and D
- Class mass: 24/50
- Instances disagreeing: 27 of 29 (93%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find the average grade of all students who have some friends.

**Gold.**
```sql
SELECT avg(grade) FROM Highschooler WHERE id IN (SELECT T1.student_id FROM Friend AS T1 JOIN Highschooler AS T2 ON T1.student_id  =  T2.id)
```

**Returned.**
```sql
SELECT AVG(T1.grade)
FROM Highschooler AS T1
INNER JOIN Friend AS T2 ON T1.ID = T2.student_id
```

**First disagreeing instance** `network_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    10.428571428571429

Returned query gives 1 row(s), 1 column(s):

    10.25

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R078  (question 467, database `dog_kennels`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed303
- Returned in cell: both A and D
- Class mass: 38/49, 20/50
- Instances disagreeing: 48 of 48 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the names of the dogs for which the owner spent more than 1000 for treatment?

**Gold.**
```sql
select name from dogs where dog_id not in ( select dog_id from treatments group by dog_id having sum(cost_of_treatment)  >  1000 )
```

**Returned.**
```sql
SELECT T1.name
FROM Dogs AS T1
INNER JOIN Treatments AS T2 ON T1.dog_id = T2.dog_id
GROUP BY T1.dog_id, T1.name
HAVING SUM(T2.cost_of_treatment) > 1000
```

**First disagreeing instance** `dog_kennels.sqlite` (this is the shipped benchmark database).

Gold returns 12 row(s), 1 column(s):

    Kacey
    Hipolito
    Mavis
    Houston
    Jeffrey
    Merritt
    Narciso
    George
    Bessie
    Betty
    Holden
    Jesus

Returned query gives 3 row(s), 1 column(s):

    Troy
    Lyric
    Evangeline

Difference: disjoint; 0 row(s) in common, 12 only in the gold, 3 only in the returned result.

### R079  (question 476, database `dog_kennels`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303
- Returned in cell: both A and D
- Class mass: 26/50, 33/50, 30/50
- Instances disagreeing: 40 of 48 (83%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the first name and last name of the professionals who have done treatment cheaper than average?

**Gold.**
```sql
SELECT DISTINCT T1.first_name ,  T1.last_name FROM Professionals AS T1 JOIN Treatments AS T2 WHERE cost_of_treatment  <  ( SELECT avg(cost_of_treatment) FROM Treatments )
```

**Returned.**
```sql
SELECT DISTINCT T1.first_name, T1.last_name
FROM Professionals T1
INNER JOIN Treatments T2 ON T1.professional_id = T2.professional_id
WHERE T2.cost_of_treatment < (SELECT AVG(cost_of_treatment) FROM Treatments)
```

**First disagreeing instance** `dog_kennels.sqlite` (this is the shipped benchmark database).

Gold returns 15 row(s), 2 column(s):

    Taryn | Braun
    Jayson | Ullrich
    Olaf | Watsica
    Vernice | Tillman
    Danny | Considine
    Ruben | O'Reilly
    Velva | Hayes
    Karley | Hyatt
    Monte | Kshlerin
    Domenica | Jacobs
    Brady | Pouros
    Winfield | Christiansen
    ... (15 rows total)

Returned query gives 5 row(s), 2 column(s):

    Domenica | Jacobs
    Vernice | Tillman
    Karley | Hyatt
    Ruben | O'Reilly
    Monte | Kshlerin

Difference: rep_subset_of_gold; 5 row(s) in common, 10 only in the gold, 0 only in the returned result.

### R080  (question 477, database `dog_kennels`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303
- Returned in cell: both A and D
- Class mass: 29/49, 29/49, 36/50
- Instances disagreeing: 40 of 48 (83%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Which professionals have operated a treatment that is less expansive than the average? Give me theor first names and last names.

**Gold.**
```sql
SELECT DISTINCT T1.first_name ,  T1.last_name FROM Professionals AS T1 JOIN Treatments AS T2 WHERE cost_of_treatment  <  ( SELECT avg(cost_of_treatment) FROM Treatments )
```

**Returned.**
```sql
SELECT DISTINCT T1.first_name, T1.last_name
FROM Professionals T1
INNER JOIN Treatments T2 ON T1.professional_id = T2.professional_id
WHERE T2.cost_of_treatment < (SELECT AVG(cost_of_treatment) FROM Treatments)
```

**First disagreeing instance** `dog_kennels.sqlite` (this is the shipped benchmark database).

Gold returns 15 row(s), 2 column(s):

    Taryn | Braun
    Jayson | Ullrich
    Olaf | Watsica
    Vernice | Tillman
    Danny | Considine
    Ruben | O'Reilly
    Velva | Hayes
    Karley | Hyatt
    Monte | Kshlerin
    Domenica | Jacobs
    Brady | Pouros
    Winfield | Christiansen
    ... (15 rows total)

Returned query gives 5 row(s), 2 column(s):

    Domenica | Jacobs
    Vernice | Tillman
    Karley | Hyatt
    Ruben | O'Reilly
    Monte | Kshlerin

Difference: rep_subset_of_gold; 5 row(s) in common, 10 only in the gold, 0 only in the returned result.

### R081  (question 480, database `dog_kennels`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303, kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 47/50, 45/50, 46/50, 35/50, 40/50, 38/50
- Instances disagreeing: 41 of 48 (85%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** List the last name of the owner owning the youngest dog.

**Gold.**
```sql
SELECT T1.last_name FROM Owners AS T1 JOIN Dogs AS T2 ON T1.owner_id  =  T2.owner_id WHERE T2.age  =  ( SELECT max(age) FROM Dogs )
```

**Returned.**
```sql
SELECT T2.last_name
FROM Dogs AS T1
INNER JOIN Owners AS T2 ON T1.owner_id = T2.owner_id
ORDER BY T1.date_of_birth DESC
LIMIT 1
```

**First disagreeing instance** `dog_kennels.sqlite` (this is the shipped benchmark database).

Gold returns 3 row(s), 1 column(s):

    Feil
    Fisher
    Rippin

Returned query gives 1 row(s), 1 column(s):

    Mertz

Difference: disjoint; 0 row(s) in common, 3 only in the gold, 1 only in the returned result.

### R082  (question 481, database `dog_kennels`)

- Returned by: kwai-autosql-32b/seed101
- Returned in cell: both A and D
- Class mass: 43/50
- Instances disagreeing: 41 of 48 (85%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Who owns the youngest dog? Give me his or her last name.

**Gold.**
```sql
SELECT T1.last_name FROM Owners AS T1 JOIN Dogs AS T2 ON T1.owner_id  =  T2.owner_id WHERE T2.age  =  ( SELECT max(age) FROM Dogs )
```

**Returned.**
```sql
SELECT T1.last_name
FROM Owners AS T1
INNER JOIN Dogs AS T2 ON T1.owner_id = T2.owner_id
ORDER BY T2.date_of_birth DESC
LIMIT 1
```

**First disagreeing instance** `dog_kennels.sqlite` (this is the shipped benchmark database).

Gold returns 3 row(s), 1 column(s):

    Feil
    Fisher
    Rippin

Returned query gives 1 row(s), 1 column(s):

    Mertz

Difference: disjoint; 0 row(s) in common, 3 only in the gold, 1 only in the returned result.

### R083  (question 507, database `real_estate_properties`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303, kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303, omnisql-32b/seed101
- Returned in cell: both A and D
- Class mass: 49/50, 50/50, 49/50, 50/50, 49/50, 49/50, 30/50
- Instances disagreeing: 9 of 32 (28%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the names of properties that are either houses or apartments with more than 1 room?

**Gold.**
```sql
SELECT property_name FROM Properties WHERE property_type_code  =  "House" UNION SELECT property_name FROM Properties WHERE property_type_code  =  "Apartment" AND room_count  >  1
```

**Returned.**
```sql
SELECT property_name
FROM Properties
WHERE property_type_code IN ('House', 'Apartment')
  AND room_count > 1
```

**First disagreeing instance** `real_estate_properties.sqlite` (this is the shipped benchmark database).

Gold returns 8 row(s), 1 column(s):

    longacre
    parc coliseum
    parc east
    park
    renoir
    ten tower
    the cole
    vogue

Returned query gives 7 row(s), 1 column(s):

    park
    parc east
    vogue
    longacre
    renoir
    ten tower
    parc coliseum

Difference: rep_subset_of_gold; 7 row(s) in common, 1 only in the gold, 0 only in the returned result.

### R084  (question 86, database `car_1`)

- Returned by: kwai-autosql-32b/seed202
- Returned in cell: both A and D
- Class mass: 42/50
- Instances disagreeing: 58 of 60 (97%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Which model saves the most gasoline?

**Gold.**
```sql
SELECT T1.Model FROM CAR_NAMES AS T1 JOIN CARS_DATA AS T2 ON T1.MakeId  =  T2.Id ORDER BY T2.mpg DESC LIMIT 1;
```

**Returned.**
```sql
SELECT T1.Model
FROM car_names AS T1
INNER JOIN cars_data AS T2 ON T1.MakeId = T2.Id
ORDER BY CAST(T2.MPG AS REAL) DESC
LIMIT 1
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    citroen

Returned query gives 1 row(s), 1 column(s):

    mazda

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R085  (question 105, database `car_1`)

- Returned by: kwai-autosql-32b/seed202
- Returned in cell: A only
- Class mass: 41/50
- Instances disagreeing: 60 of 60 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** How many nations has more than 2 car makers ?

**Gold.**
```sql
select count(*) from countries as t1 join car_makers as t2 on t1.countryid  =  t2.country group by t1.countryid having count(*)  >  2
```

**Returned.**
```sql
SELECT COUNT(*)
FROM (
    SELECT T1.Country
    FROM car_makers AS T1
    JOIN countries AS T2 ON T1.Country = T2.CountryId
    GROUP BY T1.Country
    HAVING COUNT(T1.Id) > 2
) AS subquery
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 4 row(s), 1 column(s):

    4
    4
    3
    5

Returned query gives 1 row(s), 1 column(s):

    4

Difference: rep_subset_of_gold; 1 row(s) in common, 2 only in the gold, 0 only in the returned result.

### R086  (question 105, database `car_1`)

- Returned by: kwai-autosql-32b/seed202
- Returned in cell: D only
- Class mass: 26/50
- Instances disagreeing: 60 of 60 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** How many nations has more than 2 car makers ?

**Gold.**
```sql
select count(*) from countries as t1 join car_makers as t2 on t1.countryid  =  t2.country group by t1.countryid having count(*)  >  2
```

**Returned.**
```sql
SELECT COUNT(*)
FROM (
    SELECT T2.CountryName
    FROM car_makers T1
    INNER JOIN countries T2 ON T1.Country = T2.CountryId
    GROUP BY T2.CountryName
    HAVING COUNT(*) > 2
)
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 4 row(s), 1 column(s):

    4
    4
    3
    5

Returned query gives 1 row(s), 1 column(s):

    4

Difference: rep_subset_of_gold; 1 row(s) in common, 2 only in the gold, 0 only in the returned result.

### R087  (question 106, database `car_1`)

- Returned by: kwai-autosql-32b/seed202
- Returned in cell: both A and D
- Class mass: 42/50
- Instances disagreeing: 60 of 60 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the number of nations with more than 2 car makers ?

**Gold.**
```sql
select count(*) from countries as t1 join car_makers as t2 on t1.countryid  =  t2.country group by t1.countryid having count(*)  >  2
```

**Returned.**
```sql
SELECT COUNT(*)
FROM (
    SELECT T1.CountryName
    FROM countries AS T1
    INNER JOIN car_makers AS T2 ON T1.CountryId = T2.Country
    GROUP BY T1.CountryName
    HAVING COUNT(T2.Id) > 2
) AS subquery
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 4 row(s), 1 column(s):

    4
    4
    3
    5

Returned query gives 1 row(s), 1 column(s):

    4

Difference: rep_subset_of_gold; 1 row(s) in common, 2 only in the gold, 0 only in the returned result.

### R088  (question 108, database `car_1`)

- Returned by: kwai-autosql-32b/seed202, kwai-autosql-32b/seed303
- Returned in cell: both A and D
- Class mass: 24/49, 24/49
- Instances disagreeing: 60 of 60 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the maximum miles per gallon of the 8 CYL cars or cars produced before 1980 ?

**Gold.**
```sql
select max(mpg) from cars_data where cylinders  =  8 or year  <  1980
```

**Returned.**
```sql
SELECT MAX(CAST(MPG AS REAL)) AS MaxMPG
FROM cars_data
WHERE Cylinders = 8 OR Year < 1980
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    null

Returned query gives 1 row(s), 1 column(s):

    43.1

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R089  (question 140, database `flight_2`)

- Returned by: kwai-autosql-32b/seed202
- Returned in cell: both A and D
- Class mass: 46/50
- Instances disagreeing: 8 of 56 (14%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Give the number of Jetblue Airways flights.

**Gold.**
```sql
SELECT count(*) FROM FLIGHTS AS T1 JOIN AIRLINES AS T2 ON T1.Airline  =  T2.uid WHERE T2.Airline = "JetBlue Airways"
```

**Returned.**
```sql
SELECT COUNT(*) FROM flights WHERE Airline = (SELECT uid FROM airlines WHERE Airline = 'Jetblue Airways')
```

**First disagreeing instance** `flight_2.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    100

Returned query gives 1 row(s), 1 column(s):

    0

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R090  (question 213, database `museum_visit`)

- Returned by: kwai-autosql-32b/seed202, kwai-autosql-32b/seed303
- Returned in cell: both A and D
- Class mass: 50/50, 49/50
- Instances disagreeing: 35 of 35 (100%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What are the id, name and membership level of people who have paid the largest amount of money overall in all museum tickets?

**Gold.**
```sql
SELECT t2.visitor_id ,  t1.name ,  t1.Level_of_membership FROM visitor AS t1 JOIN visit AS t2 ON t1.id  =  t2.visitor_id GROUP BY t2.visitor_id ORDER BY sum(t2.Total_spent) DESC LIMIT 1
```

**Returned.**
```sql
SELECT v.ID, v.Name, v.Level_of_membership
FROM visitor v
JOIN visit vi ON v.ID = vi.visitor_ID
ORDER BY vi.Total_spent DESC
LIMIT 1
```

**First disagreeing instance** `museum_visit.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 3 column(s):

    3 | Arjen Robben | 1

Returned query gives 1 row(s), 3 column(s):

    3 | Arjen Robben | 1

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R091  (question 223, database `wta_1`)

- Returned by: kwai-autosql-32b/seed202, kwai-autosql-32b/seed303
- Returned in cell: A only
- Class mass: 36/50, 36/50
- Instances disagreeing: 8 of 33 (24%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the names of players who won in both 2013 and 2016?

**Gold.**
```sql
SELECT winner_name FROM matches WHERE YEAR  =  2013 INTERSECT SELECT winner_name FROM matches WHERE YEAR  =  2016
```

**Returned.**
```sql
SELECT p.first_name, p.last_name
FROM players p
WHERE p.player_id IN (
    SELECT winner_id FROM matches WHERE year = 2013
    INTERSECT
    SELECT winner_id FROM matches WHERE year = 2016
)
```

**First disagreeing instance** `wta_1.sqlite` (this is the shipped benchmark database).

Gold returns 5 row(s), 1 column(s):

    Angelique Kerber
    Petra Kvitova
    Sara Errani
    Serena Williams
    Victoria Azarenka

Returned query gives 5 row(s), 2 column(s):

    Serena | Williams
    Victoria | Azarenka
    Angelique | Kerber
    Sara | Errani
    Petra | Kvitova

Difference: col_count_differs, disjoint; 0 row(s) in common, 5 only in the gold, 5 only in the returned result.

### R092  (question 223, database `wta_1`)

- Returned by: kwai-autosql-32b/seed202
- Returned in cell: D only
- Class mass: 17/50
- Instances disagreeing: 8 of 33 (24%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the names of players who won in both 2013 and 2016?

**Gold.**
```sql
SELECT winner_name FROM matches WHERE YEAR  =  2013 INTERSECT SELECT winner_name FROM matches WHERE YEAR  =  2016
```

**Returned.**
```sql
SELECT T1.first_name, T1.last_name
FROM players AS T1
INNER JOIN matches AS T2 ON T1.player_id = T2.winner_id
WHERE T2.year = 2013
INTERSECT
SELECT T1.first_name, T1.last_name
FROM players AS T1
INNER JOIN matches AS T2 ON T1.player_id = T2.winner_id
WHERE T2.year = 2016
```

**First disagreeing instance** `wta_1.sqlite` (this is the shipped benchmark database).

Gold returns 5 row(s), 1 column(s):

    Angelique Kerber
    Petra Kvitova
    Sara Errani
    Serena Williams
    Victoria Azarenka

Returned query gives 5 row(s), 2 column(s):

    Angelique | Kerber
    Petra | Kvitova
    Sara | Errani
    Serena | Williams
    Victoria | Azarenka

Difference: col_count_differs, disjoint; 0 row(s) in common, 5 only in the gold, 5 only in the returned result.

### R093  (question 234, database `wta_1`)

- Returned by: kwai-autosql-32b/seed202
- Returned in cell: both A and D
- Class mass: 15/50
- Instances disagreeing: 33 of 33 (100%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Find the name and rank points of the person who won the most times.

**Gold.**
```sql
SELECT winner_name ,  winner_rank_points FROM matches GROUP BY winner_name ORDER BY count(*) DESC LIMIT 1
```

**Returned.**
```sql
SELECT 
    p.first_name,
    p.last_name,
    r.ranking_points
FROM 
    matches m
INNER JOIN 
    players p ON m.winner_id = p.player_id
INNER JOIN 
    rankings r ON m.winner_id = r.player_id
GROUP BY 
    m.winner_id
ORDER BY 
    COUNT(m.winner_id) DESC
LIMIT 1
```

**First disagreeing instance** `wta_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    Angelique Kerber | 3715

Returned query gives 1 row(s), 3 column(s):

    Serena | Williams | 23

Difference: col_count_differs, disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R094  (question 266, database `student_transcripts_tracking`)

- Returned by: kwai-autosql-32b/seed202, kwai-autosql-32b/seed303, kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 26/50, 49/50, 19/50, 45/50, 24/50
- Instances disagreeing: 55 of 55 (100%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Which place holds the most number of students currently? List the id and all lines.

**Gold.**
```sql
SELECT T1.address_id ,  T1.line_1 ,  T1.line_2 FROM Addresses AS T1 JOIN Students AS T2 ON T1.address_id  =  T2.current_address_id GROUP BY T1.address_id ORDER BY count(*) DESC LIMIT 1
```

**Returned.**
```sql
SELECT T1.address_id, T1.line_1, T1.line_2, T1.line_3
FROM Addresses AS T1
INNER JOIN Students AS T2 ON T1.address_id = T2.current_address_id
GROUP BY T1.address_id, T1.line_1, T1.line_2, T1.line_3
ORDER BY COUNT(T2.student_id) DESC
LIMIT 1
```

**First disagreeing instance** `student_transcripts_tracking.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 3 column(s):

    9 | 0643 Muller Vista | Suite 383

Returned query gives 1 row(s), 4 column(s):

    9 | 0643 Muller Vista | Suite 383 | NULL

Difference: col_count_differs, disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R095  (question 267, database `student_transcripts_tracking`)

- Returned by: kwai-autosql-32b/seed202
- Returned in cell: D only
- Class mass: 13/50
- Instances disagreeing: 39 of 55 (71%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What is the id, line 1, and line 2 of the place with the most students?

**Gold.**
```sql
SELECT T1.address_id ,  T1.line_1 ,  T1.line_2 FROM Addresses AS T1 JOIN Students AS T2 ON T1.address_id  =  T2.current_address_id GROUP BY T1.address_id ORDER BY count(*) DESC LIMIT 1
```

**Returned.**
```sql
SELECT A.address_id, A.line_1, A.line_2
FROM Addresses A
INNER JOIN (
    SELECT address_id
    FROM (
        SELECT current_address_id AS address_id FROM Students
        UNION ALL
        SELECT permanent_address_id AS address_id FROM Students
    ) AS combined_addresses
    GROUP BY address_id
    ORDER BY COUNT(address_id) DESC
    LIMIT 1
) AS most_popular_address
ON A.address_id = most_popular_address.address_id
```

**First disagreeing instance** `student_transcripts_trackingv5080.sqlite`.

Gold returns 1 row(s), 3 column(s):

    9700166583 | 10 | 6

Returned query gives 1 row(s), 3 column(s):

    7818984859 | 0643 Muller Vista | Tep7c2

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R096  (question 268, database `student_transcripts_tracking`)

- Returned by: kwai-autosql-32b/seed202
- Returned in cell: both A and D
- Class mass: 40/50
- Instances disagreeing: 40 of 55 (73%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find the semester when both Master students and Bachelor students got enrolled in.

**Gold.**
```sql
SELECT DISTINCT T2.semester_id FROM Degree_Programs AS T1 JOIN Student_Enrolment AS T2 ON T1.degree_program_id  =  T2.degree_program_id WHERE degree_summary_name  =  'Master' INTERSECT SELECT DISTINCT T2.semester_id FROM Degree_Programs AS T1 JOIN Student_Enrolment AS T2 ON T1.degree_program_id  =  T2.degree_program_id WHERE degree_summary_name  =  'Bachelor'
```

**Returned.**
```sql
SELECT T1.semester_name
FROM Semesters T1
INNER JOIN Student_Enrolment T2 ON T1.semester_id = T2.semester_id
INNER JOIN Degree_Programs T3 ON T2.degree_program_id = T3.degree_program_id
WHERE T3.degree_summary_name = 'Master'
INTERSECT
SELECT T1.semester_name
FROM Semesters T1
INNER JOIN Student_Enrolment T2 ON T1.semester_id = T2.semester_id
INNER JOIN Degree_Programs T3 ON T2.degree_program_id = T3.degree_program_id
WHERE T3.degree_summary_name = 'Bachelor'
```

**First disagreeing instance** `student_transcripts_tracking.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    13

Returned query gives 1 row(s), 1 column(s):

    fall 2018

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R097  (question 271, database `student_transcripts_tracking`)

- Returned by: kwai-autosql-32b/seed202, kwai-autosql-32b/seed303
- Returned in cell: both A and D
- Class mass: 50/50, 50/50
- Instances disagreeing: 16 of 55 (29%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the first names of the students who live in Haiti permanently or have the cell phone number 09700166582?

**Gold.**
```sql
select t1.first_name from students as t1 join addresses as t2 on t1.permanent_address_id  =  t2.address_id where t2.country  =  'haiti' or t1.cell_mobile_number  =  '09700166582'
```

**Returned.**
```sql
SELECT T1.first_name
FROM Students AS T1
LEFT JOIN Addresses AS T2 ON T1.permanent_address_id = T2.address_id
WHERE T2.country = 'Haiti' OR T1.cell_mobile_number = '09700166582'
```

**First disagreeing instance** `student_transcripts_tracking.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    Jarvis

Returned query gives 4 row(s), 1 column(s):

    Hobart
    Warren
    Jarvis
    Delaney

Difference: gold_subset_of_rep; 1 row(s) in common, 0 only in the gold, 3 only in the returned result.

### R098  (question 310, database `tvshow`)

- Returned by: kwai-autosql-32b/seed202, kwai-autosql-14b/seed101
- Returned in cell: both A and D
- Class mass: 32/50, 37/50
- Instances disagreeing: 12 of 25 (48%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the countries that are not playing cartoons  Todd Casey writes?

**Gold.**
```sql
SELECT country FROM TV_Channel EXCEPT SELECT T1.country FROM TV_Channel AS T1 JOIN cartoon AS T2 ON T1.id = T2.Channel WHERE T2.written_by  =  'Todd Casey'
```

**Returned.**
```sql
SELECT DISTINCT Country
FROM TV_Channel
WHERE id NOT IN (
    SELECT Channel
    FROM Cartoon
    WHERE Written_by = 'Todd Casey'
)
```

**First disagreeing instance** `tvshow.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    Poland

Returned query gives 3 row(s), 1 column(s):

    Italy
    United Kingdom
    Poland

Difference: gold_subset_of_rep; 1 row(s) in common, 0 only in the gold, 2 only in the returned result.

### R099  (question 311, database `tvshow`)

- Returned by: kwai-autosql-32b/seed202
- Returned in cell: both A and D
- Class mass: 27/50
- Instances disagreeing: 25 of 25 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find the series name and country of the tv channel that is playing some cartoons  Ben Jones and Michael Chang directs?

**Gold.**
```sql
SELECT T1.series_name ,  T1.country FROM TV_Channel AS T1 JOIN cartoon AS T2 ON T1.id = T2.Channel WHERE T2.directed_by  =  'Michael Chang' INTERSECT SELECT T1.series_name ,  T1.country FROM TV_Channel AS T1 JOIN cartoon AS T2 ON T1.id = T2.Channel WHERE T2.directed_by  =  'Ben Jones'
```

**Returned.**
```sql
SELECT DISTINCT T.series_name, T.Country
FROM TV_Channel T
INNER JOIN Cartoon C ON T.id = C.Channel
WHERE C.Directed_by IN ('Ben Jones', 'Michael Chang')
```

**First disagreeing instance** `tvshow.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    MTV Dance | United Kingdom

Returned query gives 6 row(s), 2 column(s):

    Sky Radio | Italy
    Music Box Italia | Italy
    MTV Hits | Italy
    MTV Rocks | United Kingdom
    MTV Dance | United Kingdom
    Classica | Italy

Difference: gold_subset_of_rep; 1 row(s) in common, 0 only in the gold, 5 only in the returned result.

### R100  (question 362, database `world_1`)

- Returned by: kwai-autosql-32b/seed202
- Returned in cell: D only
- Class mass: 8/50
- Instances disagreeing: 17 of 46 (37%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the average GNP and total population in all US territory nations?

**Gold.**
```sql
SELECT avg(GNP) ,  sum(population) FROM country WHERE GovernmentForm  =  "US Territory"
```

**Returned.**
```sql
SELECT AVG(GNP) AS AverageGNP, SUM(Population) AS TotalPopulation
FROM country
WHERE GovernmentForm LIKE '%Territory%'
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    510.3333333333333 | 329000

Returned query gives 1 row(s), 2 column(s):

    435.81290322580645 | 1338350

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R101  (question 374, database `world_1`)

- Returned by: kwai-autosql-32b/seed202
- Returned in cell: D only
- Class mass: 27/50
- Instances disagreeing: 9 of 46 (20%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the names of nations speak both English and French?

**Gold.**
```sql
SELECT T1.Name FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code  =  T2.CountryCode WHERE T2.Language  =  "English" INTERSECT SELECT T1.Name FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code  =  T2.CountryCode WHERE T2.Language  =  "French"
```

**Returned.**
```sql
SELECT T1.Name
FROM country T1
INNER JOIN countrylanguage T2 ON T1.Code = T2.CountryCode AND T2.Language = 'English'
INNER JOIN countrylanguage T3 ON T1.Code = T3.CountryCode AND T3.Language = 'French'
```

**First disagreeing instance** `world_1v50811.sqlite`.

Gold returns 6 row(s), 1 column(s):

    3000
    Chinese
    Martinique
    Mauritania
    aGbRLc9RUYaP
    p86MwSIdU2FOuqnWIEao4A16JDOFm

Returned query gives 5 row(s), 1 column(s):

    Mauritania
    3000
    aGbRLc9RUYaP
    Martinique
    p86MwSIdU2FOuqnWIEao4A16JDOFm

Difference: rep_subset_of_gold; 5 row(s) in common, 1 only in the gold, 0 only in the returned result.

### R102  (question 387, database `world_1`)

- Returned by: kwai-autosql-32b/seed202, kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 37/50, 46/50, 45/50, 46/50
- Instances disagreeing: 37 of 46 (80%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Find the city with the most people that uses English.

**Gold.**
```sql
SELECT T1.Name ,  T1.Population FROM city AS T1 JOIN countrylanguage AS T2 ON T1.CountryCode  =  T2.CountryCode WHERE T2.Language  =  "English" ORDER BY T1.Population DESC LIMIT 1
```

**Returned.**
```sql
SELECT T1.Name
FROM city AS T1
INNER JOIN country AS T2 ON T1.CountryCode = T2.Code
INNER JOIN countrylanguage AS T3 ON T2.Code = T3.CountryCode
WHERE T3.Language = 'English'
ORDER BY T1.Population DESC
LIMIT 1
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    New York | 8008278

Returned query gives 1 row(s), 1 column(s):

    New York

Difference: col_count_differs, disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R103  (question 428, database `world_1`)

- Returned by: kwai-autosql-32b/seed202, kwai-autosql-32b/seed303
- Returned in cell: both A and D
- Class mass: 33/50, 33/50
- Instances disagreeing: 40 of 46 (87%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Give the total population and average  corresponding to countries in Noth America that is bigger than 3000 square miles.

**Gold.**
```sql
select sum(population) ,  avg(surfacearea) from country where continent  =  "north america" and surfacearea  >  3000
```

**Returned.**
```sql
SELECT SUM(Population) AS TotalPopulation, AVG(Population) AS AveragePopulation
FROM country
WHERE Continent = 'North America' AND SurfaceArea > 3000
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    NULL | NULL

Returned query gives 1 row(s), 2 column(s):

    480753000 | 26708500.0

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R104  (question 431, database `world_1`)

- Returned by: kwai-autosql-32b/seed202
- Returned in cell: both A and D
- Class mass: 18/50
- Instances disagreeing: 46 of 46 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the language spoken by the largest percentage of people in each nation?

**Gold.**
```sql
SELECT LANGUAGE ,  CountryCode ,  max(Percentage) FROM countrylanguage GROUP BY CountryCode
```

**Returned.**
```sql
SELECT cl.Language
FROM countrylanguage cl
WHERE cl.Percentage = (
    SELECT MAX(Percentage)
    FROM countrylanguage
    WHERE CountryCode = cl.CountryCode
)
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 233 row(s), 3 column(s):

    Papiamento | ABW | 76.7
    Pashto | AFG | 52.4
    Ovimbundu | AGO | 37.2
    English | AIA | 0.0
    Albaniana | ALB | 97.9
    Spanish | AND | 44.6
    Papiamento | ANT | 86.2
    Arabic | ARE | 42.0
    Spanish | ARG | 96.8
    Armenian | ARM | 93.4
    Samoan | ASM | 90.6
    Creole English | ATG | 95.7
    ... (233 rows total)

Returned query gives 241 row(s), 1 column(s):

    Papiamento
    Pashto
    Ovimbundu
    English
    Albaniana
    Spanish
    Papiamento
    Arabic
    Spanish
    Armenian
    Samoan
    Creole English
    ... (241 rows total)

Difference: col_count_differs, disjoint; 0 row(s) in common, 233 only in the gold, 136 only in the returned result.

### R105  (question 432, database `world_1`)

- Returned by: kwai-autosql-32b/seed202
- Returned in cell: both A and D
- Class mass: 27/50
- Instances disagreeing: 46 of 46 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the codes of the different nations, and what are the languages spoken by the greatest percentage of people for each?

**Gold.**
```sql
SELECT LANGUAGE ,  CountryCode ,  max(Percentage) FROM countrylanguage GROUP BY CountryCode
```

**Returned.**
```sql
SELECT CountryCode, Language
FROM (
    SELECT CountryCode, Language,
           ROW_NUMBER() OVER (PARTITION BY CountryCode ORDER BY Percentage DESC) AS rn
    FROM countrylanguage
)
WHERE rn = 1
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 233 row(s), 3 column(s):

    Papiamento | ABW | 76.7
    Pashto | AFG | 52.4
    Ovimbundu | AGO | 37.2
    English | AIA | 0.0
    Albaniana | ALB | 97.9
    Spanish | AND | 44.6
    Papiamento | ANT | 86.2
    Arabic | ARE | 42.0
    Spanish | ARG | 96.8
    Armenian | ARM | 93.4
    Samoan | ASM | 90.6
    Creole English | ATG | 95.7
    ... (233 rows total)

Returned query gives 233 row(s), 2 column(s):

    ABW | Papiamento
    AFG | Pashto
    AGO | Ovimbundu
    AIA | English
    ALB | Albaniana
    AND | Spanish
    ANT | Papiamento
    ARE | Arabic
    ARG | Spanish
    ARM | Armenian
    ASM | Samoan
    ATG | Creole English
    ... (233 rows total)

Difference: col_count_differs, disjoint; 0 row(s) in common, 233 only in the gold, 233 only in the returned result.

### R106  (question 433, database `world_1`)

- Returned by: kwai-autosql-32b/seed202
- Returned in cell: both A and D
- Class mass: 17/50
- Instances disagreeing: 46 of 46 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the total number of countries where Spanish is spoken by the largest percentage of people?

**Gold.**
```sql
SELECT count(*) ,   max(Percentage) FROM countrylanguage WHERE LANGUAGE  =  "Spanish" GROUP BY CountryCode
```

**Returned.**
```sql
SELECT COUNT(*)
FROM (
    SELECT CountryCode
    FROM countrylanguage
    WHERE Language = 'Spanish'
    AND Percentage = (
        SELECT MAX(Percentage)
        FROM countrylanguage AS cl2
        WHERE cl2.CountryCode = countrylanguage.CountryCode
    )
) AS largest_spanish
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 28 row(s), 2 column(s):

    1 | 7.4
    1 | 44.6
    1 | 96.8
    1 | 31.6
    1 | 87.7
    1 | 0.7
    1 | 89.7
    1 | 99.0
    1 | 97.5
    1 | 100.0
    1 | 98.0
    1 | 93.0
    ... (28 rows total)

Returned query gives 1 row(s), 1 column(s):

    21

Difference: col_count_differs, disjoint; 0 row(s) in common, 27 only in the gold, 1 only in the returned result.

### R107  (question 434, database `world_1`)

- Returned by: kwai-autosql-32b/seed202
- Returned in cell: D only
- Class mass: 18/50
- Instances disagreeing: 46 of 46 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Count the number of countries for which Spanish is predominantly spoken .

**Gold.**
```sql
SELECT count(*) ,   max(Percentage) FROM countrylanguage WHERE LANGUAGE  =  "Spanish" GROUP BY CountryCode
```

**Returned.**
```sql
SELECT COUNT(*) FROM countrylanguage WHERE Language = 'Spanish'
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 28 row(s), 2 column(s):

    1 | 7.4
    1 | 44.6
    1 | 96.8
    1 | 31.6
    1 | 87.7
    1 | 0.7
    1 | 89.7
    1 | 99.0
    1 | 97.5
    1 | 100.0
    1 | 98.0
    1 | 93.0
    ... (28 rows total)

Returned query gives 1 row(s), 1 column(s):

    28

Difference: col_count_differs, disjoint; 0 row(s) in common, 27 only in the gold, 1 only in the returned result.

### R108  (question 442, database `orchestra`)

- Returned by: kwai-autosql-32b/seed202
- Returned in cell: both A and D
- Class mass: 29/50
- Instances disagreeing: 28 of 28 (100%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Return the record companies of orchestras, sorted ascending by the time they have existed.

**Gold.**
```sql
SELECT Record_Company FROM orchestra ORDER BY Year_of_Founded DESC
```

**Returned.**
```sql
SELECT Record_Company
FROM orchestra
ORDER BY Year_of_Founded ASC
```

**First disagreeing instance** `orchestra.sqlite` (this is the shipped benchmark database).

Gold returns 12 row(s), 1 column(s):

    Columbia Masterworks
    Philips
    Philips Classics Records
    RCA
    EMI
    Koch Records / Naxos Records
    Decca Records
    Mercury Records
    Deutsche Grammophon
    Kultur
    Decca Records
    Delos Records

Returned query gives 12 row(s), 1 column(s):

    Kultur
    Decca Records
    Delos Records
    Mercury Records
    Deutsche Grammophon
    Decca Records
    Koch Records / Naxos Records
    EMI
    Philips
    Philips Classics Records
    RCA
    Columbia Masterworks

Difference: row_order_only; 11 row(s) in common, 0 only in the gold, 0 only in the returned result.

### R109  (question 457, database `network_1`)

- Returned by: kwai-autosql-32b/seed202
- Returned in cell: D only
- Class mass: 26/50
- Instances disagreeing: 22 of 29 (76%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** How many friends does Kyle have?

**Gold.**
```sql
SELECT count(*) FROM Friend AS T1 JOIN Highschooler AS T2 ON T1.student_id  =  T2.id WHERE T2.name  =  "Kyle"
```

**Returned.**
```sql
SELECT COUNT(*)
FROM Friend
WHERE student_id = (
    SELECT ID
    FROM Highschooler
    WHERE name = 'Kyle'
)
```

**First disagreeing instance** `network_1v5080.sqlite`.

Gold returns 1 row(s), 1 column(s):

    19

Returned query gives 1 row(s), 1 column(s):

    1

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R110  (question 462, database `network_1`)

- Returned by: kwai-autosql-32b/seed202
- Returned in cell: both A and D
- Class mass: 25/50
- Instances disagreeing: 27 of 29 (93%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the average grade of students who have friends?

**Gold.**
```sql
SELECT avg(grade) FROM Highschooler WHERE id IN (SELECT T1.student_id FROM Friend AS T1 JOIN Highschooler AS T2 ON T1.student_id  =  T2.id)
```

**Returned.**
```sql
SELECT AVG(T1.grade)
FROM Highschooler AS T1
INNER JOIN Friend AS T2 ON T1.ID = T2.student_id
```

**First disagreeing instance** `network_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    10.428571428571429

Returned query gives 1 row(s), 1 column(s):

    10.25

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R111  (question 467, database `dog_kennels`)

- Returned by: kwai-autosql-32b/seed202, kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 34/49, 47/50, 50/50, 50/50
- Instances disagreeing: 48 of 48 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the names of the dogs for which the owner spent more than 1000 for treatment?

**Gold.**
```sql
select name from dogs where dog_id not in ( select dog_id from treatments group by dog_id having sum(cost_of_treatment)  >  1000 )
```

**Returned.**
```sql
SELECT T1.name
FROM Dogs AS T1
INNER JOIN Treatments AS T2 ON T1.dog_id = T2.dog_id
GROUP BY T1.dog_id
HAVING SUM(T2.cost_of_treatment) > 1000
```

**First disagreeing instance** `dog_kennels.sqlite` (this is the shipped benchmark database).

Gold returns 12 row(s), 1 column(s):

    Kacey
    Hipolito
    Mavis
    Houston
    Jeffrey
    Merritt
    Narciso
    George
    Bessie
    Betty
    Holden
    Jesus

Returned query gives 3 row(s), 1 column(s):

    Troy
    Lyric
    Evangeline

Difference: disjoint; 0 row(s) in common, 12 only in the gold, 3 only in the returned result.

### R112  (question 481, database `dog_kennels`)

- Returned by: kwai-autosql-32b/seed202, kwai-autosql-32b/seed303, kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 45/50, 45/50, 43/50, 40/50, 41/50
- Instances disagreeing: 41 of 48 (85%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Who owns the youngest dog? Give me his or her last name.

**Gold.**
```sql
SELECT T1.last_name FROM Owners AS T1 JOIN Dogs AS T2 ON T1.owner_id  =  T2.owner_id WHERE T2.age  =  ( SELECT max(age) FROM Dogs )
```

**Returned.**
```sql
SELECT T2.last_name
FROM Dogs AS T1
INNER JOIN Owners AS T2 ON T1.owner_id = T2.owner_id
ORDER BY T1.date_of_birth DESC
LIMIT 1
```

**First disagreeing instance** `dog_kennels.sqlite` (this is the shipped benchmark database).

Gold returns 3 row(s), 1 column(s):

    Feil
    Fisher
    Rippin

Returned query gives 1 row(s), 1 column(s):

    Mertz

Difference: disjoint; 0 row(s) in common, 3 only in the gold, 1 only in the returned result.

### R113  (question 29, database `concert_singer`)

- Returned by: kwai-autosql-32b/seed303
- Returned in cell: D only
- Class mass: 28/50
- Instances disagreeing: 1 of 32 (3%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find the name and location of the stadiums which some concerts happened in both 2014 and 2015.

**Gold.**
```sql
SELECT T2.name ,  T2.location FROM concert AS T1 JOIN stadium AS T2 ON T1.stadium_id  =  T2.stadium_id WHERE T1.Year  =  2014 INTERSECT SELECT T2.name ,  T2.location FROM concert AS T1 JOIN stadium AS T2 ON T1.stadium_id  =  T2.stadium_id WHERE T1.Year  =  2015
```

**Returned.**
```sql
SELECT DISTINCT s.Name, s.Location
FROM stadium s
INNER JOIN concert c ON s.Stadium_ID = c.Stadium_ID
WHERE c.Year IN ('2014', '2015')
GROUP BY s.Stadium_ID
HAVING COUNT(DISTINCT c.Year) = 2
```

**First disagreeing instance** `concert_singerv515nightpatch9.sqlite`.

Gold returns 8 row(s), 2 column(s):

    %Auditions% | Hey
    %Auditions% | Stirling AlbionDgvVj
    0 | U
    0PYn0D | ntvj1u
    Hampden Park | Taz Ci
    QzjTP9R6tkTNHsnR | Stirling Albion
    ampden Park | Stirling Albion
    hxxexfPE | Peterhead

Returned query gives 7 row(s), 2 column(s):

    %Auditions% | Stirling AlbionDgvVj
    ampden Park | Stirling Albion
    0PYn0D | ntvj1u
    0 | U
    hxxexfPE | Peterhead
    QzjTP9R6tkTNHsnR | Stirling Albion
    Hampden Park | Taz Ci

Difference: rep_subset_of_gold; 7 row(s) in common, 1 only in the gold, 0 only in the returned result.

### R114  (question 65, database `car_1`)

- Returned by: kwai-autosql-32b/seed303, kwai-autosql-14b/seed101, kwai-autosql-14b/seed202
- Returned in cell: both A and D
- Class mass: 39/50, 10/50, 11/50
- Instances disagreeing: 4 of 60 (7%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find the make and production time of the cars that were produced in the earliest ?

**Gold.**
```sql
SELECT T2.Make ,  T1.Year FROM CARS_DATA AS T1 JOIN CAR_NAMES AS T2 ON T1.Id  =  T2.MakeId WHERE T1.Year  =  (SELECT min(YEAR) FROM CARS_DATA);
```

**Returned.**
```sql
SELECT T2.Make, T1.Year
FROM cars_data AS T1
INNER JOIN car_names AS T2 ON T1.Id = T2.MakeId
ORDER BY T1.Year ASC
LIMIT 1
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 35 row(s), 2 column(s):

    chevrolet chevelle malibu | 1970
    buick skylark 320 | 1970
    plymouth satellite | 1970
    amc rebel sst | 1970
    ford torino | 1970
    ford galaxie 500 | 1970
    chevrolet impala | 1970
    plymouth fury iii | 1970
    pontiac catalina | 1970
    amc ambassador dpl | 1970
    citroen ds-21 pallas | 1970
    chevrolet chevelle concours (sw) | 1970
    ... (35 rows total)

Returned query gives 1 row(s), 2 column(s):

    chevrolet chevelle malibu | 1970

Difference: rep_subset_of_gold; 1 row(s) in common, 34 only in the gold, 0 only in the returned result.

### R115  (question 82, database `car_1`)

- Returned by: kwai-autosql-32b/seed303, kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 42/50, 26/50, 32/50, 28/50
- Instances disagreeing: 59 of 60 (98%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the number of the cars with  more than 150 hp?

**Gold.**
```sql
SELECT count(*) FROM CARS_DATA WHERE horsepower  >  150;
```

**Returned.**
```sql
SELECT COUNT(*) FROM cars_data WHERE CAST(Horsepower AS INTEGER) > 150
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    281

Returned query gives 1 row(s), 1 column(s):

    49

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R116  (question 83, database `car_1`)

- Returned by: kwai-autosql-32b/seed303
- Returned in cell: both A and D
- Class mass: 36/50
- Instances disagreeing: 59 of 60 (98%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the number of cars with over 150 hp?

**Gold.**
```sql
SELECT count(*) FROM CARS_DATA WHERE horsepower  >  150;
```

**Returned.**
```sql
SELECT COUNT(*) FROM cars_data WHERE CAST(Horsepower AS INTEGER) > 150
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    281

Returned query gives 1 row(s), 1 column(s):

    49

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R117  (question 98, database `car_1`)

- Returned by: kwai-autosql-32b/seed303
- Returned in cell: both A and D
- Class mass: 47/50
- Instances disagreeing: 30 of 60 (50%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the names and ids of all car companies with more than 3 models?

**Gold.**
```sql
SELECT T1.FullName ,  T1.Id FROM CAR_MAKERS AS T1 JOIN MODEL_LIST AS T2 ON T1.Id  =  T2.Maker GROUP BY T1.Id HAVING count(*)  >  3;
```

**Returned.**
```sql
SELECT T1.Id, T1.Maker
FROM car_makers AS T1
INNER JOIN model_list AS T2 ON T1.Id = T2.Maker
GROUP BY T1.Id, T1.Maker
HAVING COUNT(T2.ModelId) > 3
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 2 row(s), 2 column(s):

    General Motors | 4
    Chrysler | 6

Returned query gives 2 row(s), 2 column(s):

    4 | gm
    6 | chrysler

Difference: disjoint; 0 row(s) in common, 2 only in the gold, 2 only in the returned result.

### R118  (question 105, database `car_1`)

- Returned by: kwai-autosql-32b/seed303
- Returned in cell: A only
- Class mass: 39/50
- Instances disagreeing: 60 of 60 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** How many nations has more than 2 car makers ?

**Gold.**
```sql
select count(*) from countries as t1 join car_makers as t2 on t1.countryid  =  t2.country group by t1.countryid having count(*)  >  2
```

**Returned.**
```sql
SELECT COUNT(*)
FROM (
    SELECT Country
    FROM car_makers
    GROUP BY Country
    HAVING COUNT(Id) > 2
)
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 4 row(s), 1 column(s):

    4
    4
    3
    5

Returned query gives 1 row(s), 1 column(s):

    4

Difference: rep_subset_of_gold; 1 row(s) in common, 2 only in the gold, 0 only in the returned result.

### R119  (question 105, database `car_1`)

- Returned by: kwai-autosql-32b/seed303
- Returned in cell: D only
- Class mass: 24/50
- Instances disagreeing: 60 of 60 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** How many nations has more than 2 car makers ?

**Gold.**
```sql
select count(*) from countries as t1 join car_makers as t2 on t1.countryid  =  t2.country group by t1.countryid having count(*)  >  2
```

**Returned.**
```sql
SELECT COUNT(*)
FROM (
    SELECT T1.CountryName
    FROM countries AS T1
    INNER JOIN car_makers AS T2 ON T1.CountryId = T2.Country
    GROUP BY T1.CountryName
    HAVING COUNT(T2.Id) > 2
) AS subquery
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 4 row(s), 1 column(s):

    4
    4
    3
    5

Returned query gives 1 row(s), 1 column(s):

    4

Difference: rep_subset_of_gold; 1 row(s) in common, 2 only in the gold, 0 only in the returned result.

### R120  (question 106, database `car_1`)

- Returned by: kwai-autosql-32b/seed303
- Returned in cell: A only
- Class mass: 42/50
- Instances disagreeing: 60 of 60 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the number of nations with more than 2 car makers ?

**Gold.**
```sql
select count(*) from countries as t1 join car_makers as t2 on t1.countryid  =  t2.country group by t1.countryid having count(*)  >  2
```

**Returned.**
```sql
SELECT COUNT(*)
FROM (
    SELECT Country
    FROM car_makers
    GROUP BY Country
    HAVING COUNT(*) > 2
)
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 4 row(s), 1 column(s):

    4
    4
    3
    5

Returned query gives 1 row(s), 1 column(s):

    4

Difference: rep_subset_of_gold; 1 row(s) in common, 2 only in the gold, 0 only in the returned result.

### R121  (question 106, database `car_1`)

- Returned by: kwai-autosql-32b/seed303
- Returned in cell: D only
- Class mass: 26/50
- Instances disagreeing: 60 of 60 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the number of nations with more than 2 car makers ?

**Gold.**
```sql
select count(*) from countries as t1 join car_makers as t2 on t1.countryid  =  t2.country group by t1.countryid having count(*)  >  2
```

**Returned.**
```sql
SELECT COUNT(*) AS Number_of_Nations
FROM (
    SELECT countries.CountryName
    FROM car_makers
    INNER JOIN countries ON car_makers.Country = countries.CountryId
    GROUP BY countries.CountryName
    HAVING COUNT(car_makers.Id) > 2
) AS subquery
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 4 row(s), 1 column(s):

    4
    4
    3
    5

Returned query gives 1 row(s), 1 column(s):

    4

Difference: rep_subset_of_gold; 1 row(s) in common, 2 only in the gold, 0 only in the returned result.

### R122  (question 140, database `flight_2`)

- Returned by: kwai-autosql-32b/seed303
- Returned in cell: both A and D
- Class mass: 41/50
- Instances disagreeing: 8 of 56 (14%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Give the number of Jetblue Airways flights.

**Gold.**
```sql
SELECT count(*) FROM FLIGHTS AS T1 JOIN AIRLINES AS T2 ON T1.Airline  =  T2.uid WHERE T2.Airline = "JetBlue Airways"
```

**Returned.**
```sql
SELECT COUNT(*) FROM flights
JOIN airlines ON flights.Airline = airlines.uid
WHERE airlines.Airline = 'Jetblue Airways'
```

**First disagreeing instance** `flight_2.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    100

Returned query gives 1 row(s), 1 column(s):

    0

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R123  (question 223, database `wta_1`)

- Returned by: kwai-autosql-32b/seed303
- Returned in cell: D only
- Class mass: 17/50
- Instances disagreeing: 8 of 33 (24%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the names of players who won in both 2013 and 2016?

**Gold.**
```sql
SELECT winner_name FROM matches WHERE YEAR  =  2013 INTERSECT SELECT winner_name FROM matches WHERE YEAR  =  2016
```

**Returned.**
```sql
SELECT DISTINCT p.first_name, p.last_name
FROM matches m
INNER JOIN players p ON m.winner_id = p.player_id
WHERE m.year = 2013
INTERSECT
SELECT DISTINCT p.first_name, p.last_name
FROM matches m
INNER JOIN players p ON m.winner_id = p.player_id
WHERE m.year = 2016
```

**First disagreeing instance** `wta_1.sqlite` (this is the shipped benchmark database).

Gold returns 5 row(s), 1 column(s):

    Angelique Kerber
    Petra Kvitova
    Sara Errani
    Serena Williams
    Victoria Azarenka

Returned query gives 5 row(s), 2 column(s):

    Angelique | Kerber
    Petra | Kvitova
    Sara | Errani
    Serena | Williams
    Victoria | Azarenka

Difference: col_count_differs, disjoint; 0 row(s) in common, 5 only in the gold, 5 only in the returned result.

### R124  (question 234, database `wta_1`)

- Returned by: kwai-autosql-32b/seed303
- Returned in cell: both A and D
- Class mass: 17/50
- Instances disagreeing: 33 of 33 (100%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Find the name and rank points of the person who won the most times.

**Gold.**
```sql
SELECT winner_name ,  winner_rank_points FROM matches GROUP BY winner_name ORDER BY count(*) DESC LIMIT 1
```

**Returned.**
```sql
SELECT p.first_name, p.last_name, r.ranking_points
FROM matches m
INNER JOIN players p ON m.winner_id = p.player_id
INNER JOIN rankings r ON m.winner_id = r.player_id
GROUP BY m.winner_id, p.first_name, p.last_name, r.ranking_points
ORDER BY COUNT(m.winner_id) DESC
LIMIT 1
```

**First disagreeing instance** `wta_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    Angelique Kerber | 3715

Returned query gives 1 row(s), 3 column(s):

    Karolina | Pliskova | 4

Difference: col_count_differs, disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R125  (question 235, database `wta_1`)

- Returned by: kwai-autosql-32b/seed303
- Returned in cell: both A and D
- Class mass: 20/50
- Instances disagreeing: 33 of 33 (100%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What is the name of the player who has won the most matches, and how many rank points does this player have?

**Gold.**
```sql
SELECT winner_name ,  winner_rank_points FROM matches GROUP BY winner_name ORDER BY count(*) DESC LIMIT 1
```

**Returned.**
```sql
SELECT 
    p.first_name, 
    p.last_name, 
    r.ranking_points
FROM 
    matches m
INNER JOIN 
    players p ON m.winner_id = p.player_id
INNER JOIN 
    rankings r ON m.winner_id = r.player_id
GROUP BY 
    m.winner_id, p.first_name, p.last_name, r.ranking_points
ORDER BY 
    COUNT(m.winner_id) DESC
LIMIT 1
```

**First disagreeing instance** `wta_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    Angelique Kerber | 3715

Returned query gives 1 row(s), 3 column(s):

    Karolina | Pliskova | 4

Difference: col_count_differs, disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R126  (question 309, database `tvshow`)

- Returned by: kwai-autosql-32b/seed303
- Returned in cell: both A and D
- Class mass: 40/50
- Instances disagreeing: 12 of 25 (48%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** which countries' tv channels are not playing any cartoon  Todd Casey writes?

**Gold.**
```sql
SELECT country FROM TV_Channel EXCEPT SELECT T1.country FROM TV_Channel AS T1 JOIN cartoon AS T2 ON T1.id = T2.Channel WHERE T2.written_by  =  'Todd Casey'
```

**Returned.**
```sql
SELECT DISTINCT Country
FROM TV_Channel
WHERE id NOT IN (
    SELECT T1.Channel
    FROM Cartoon AS T1
    WHERE T1.Written_by = 'Todd Casey'
)
```

**First disagreeing instance** `tvshow.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    Poland

Returned query gives 3 row(s), 1 column(s):

    Italy
    United Kingdom
    Poland

Difference: gold_subset_of_rep; 1 row(s) in common, 0 only in the gold, 2 only in the returned result.

### R127  (question 310, database `tvshow`)

- Returned by: kwai-autosql-32b/seed303
- Returned in cell: both A and D
- Class mass: 29/48
- Instances disagreeing: 12 of 25 (48%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the countries that are not playing cartoons  Todd Casey writes?

**Gold.**
```sql
SELECT country FROM TV_Channel EXCEPT SELECT T1.country FROM TV_Channel AS T1 JOIN cartoon AS T2 ON T1.id = T2.Channel WHERE T2.written_by  =  'Todd Casey'
```

**Returned.**
```sql
SELECT DISTINCT Country
FROM TV_Channel
WHERE id NOT IN (
    SELECT T1.Channel
    FROM Cartoon AS T1
    WHERE T1.Written_by = 'Todd Casey'
)
```

**First disagreeing instance** `tvshow.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    Poland

Returned query gives 3 row(s), 1 column(s):

    Italy
    United Kingdom
    Poland

Difference: gold_subset_of_rep; 1 row(s) in common, 0 only in the gold, 2 only in the returned result.

### R128  (question 312, database `tvshow`)

- Returned by: kwai-autosql-32b/seed303
- Returned in cell: both A and D
- Class mass: 27/50
- Instances disagreeing: 25 of 25 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the series name and country of all TV channels that are playing cartoons  Ben Jones and Michael Chang directs?

**Gold.**
```sql
SELECT T1.series_name ,  T1.country FROM TV_Channel AS T1 JOIN cartoon AS T2 ON T1.id = T2.Channel WHERE T2.directed_by  =  'Michael Chang' INTERSECT SELECT T1.series_name ,  T1.country FROM TV_Channel AS T1 JOIN cartoon AS T2 ON T1.id = T2.Channel WHERE T2.directed_by  =  'Ben Jones'
```

**Returned.**
```sql
SELECT DISTINCT T.series_name, T.Country
FROM Cartoon C
JOIN TV_Channel T ON C.Channel = T.id
WHERE C.Directed_by IN ('Ben Jones', 'Michael Chang')
```

**First disagreeing instance** `tvshow.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    MTV Dance | United Kingdom

Returned query gives 6 row(s), 2 column(s):

    Sky Radio | Italy
    Music Box Italia | Italy
    MTV Hits | Italy
    MTV Rocks | United Kingdom
    MTV Dance | United Kingdom
    Classica | Italy

Difference: gold_subset_of_rep; 1 row(s) in common, 0 only in the gold, 5 only in the returned result.

### R129  (question 362, database `world_1`)

- Returned by: kwai-autosql-32b/seed303, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 13/50, 19/50, 12/50
- Instances disagreeing: 5 of 46 (11%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the average GNP and total population in all US territory nations?

**Gold.**
```sql
SELECT avg(GNP) ,  sum(population) FROM country WHERE GovernmentForm  =  "US Territory"
```

**Returned.**
```sql
SELECT AVG(GNP), SUM(Population)
FROM country
WHERE GovernmentForm LIKE '%United States%'
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    510.3333333333333 | 329000

Returned query gives 1 row(s), 2 column(s):

    NULL | NULL

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R130  (question 366, database `world_1`)

- Returned by: kwai-autosql-32b/seed303
- Returned in cell: D only
- Class mass: 30/50
- Instances disagreeing: 26 of 46 (57%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the total number of languages used in Aruba?

**Gold.**
```sql
SELECT COUNT(T2.Language) FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code  =  T2.CountryCode WHERE T1.Name  =  "Aruba"
```

**Returned.**
```sql
SELECT COUNT(Language)
FROM countrylanguage
WHERE CountryCode = (
    SELECT Code
    FROM country
    WHERE Name = 'Aruba'
)
```

**First disagreeing instance** `world_1v50811.sqlite`.

Gold returns 1 row(s), 1 column(s):

    33

Returned query gives 1 row(s), 1 column(s):

    15

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R131  (question 404, database `world_1`)

- Returned by: kwai-autosql-32b/seed303, kwai-autosql-14b/seed101
- Returned in cell: both A and D
- Class mass: 21/50, 21/50
- Instances disagreeing: 44 of 46 (96%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the country codes for countries that do not speak English?

**Gold.**
```sql
SELECT CountryCode FROM countrylanguage EXCEPT SELECT CountryCode FROM countrylanguage WHERE LANGUAGE  =  "English"
```

**Returned.**
```sql
SELECT CountryCode
FROM countrylanguage
WHERE Language != 'English'
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 173 row(s), 1 column(s):

    AFG
    AGO
    ALB
    AND
    ARE
    ARG
    ARM
    AUT
    AZE
    BDI
    BEL
    BEN
    ... (173 rows total)

Returned query gives 924 row(s), 1 column(s):

    ABW
    ABW
    ABW
    AFG
    AFG
    AFG
    AFG
    AFG
    AGO
    AGO
    AGO
    AGO
    ... (924 rows total)

Difference: gold_subset_of_rep; 173 row(s) in common, 0 only in the gold, 50 only in the returned result.

### R132  (question 431, database `world_1`)

- Returned by: kwai-autosql-32b/seed303
- Returned in cell: both A and D
- Class mass: 20/50
- Instances disagreeing: 46 of 46 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the language spoken by the largest percentage of people in each nation?

**Gold.**
```sql
SELECT LANGUAGE ,  CountryCode ,  max(Percentage) FROM countrylanguage GROUP BY CountryCode
```

**Returned.**
```sql
SELECT T1.CountryCode, T1.Language
FROM countrylanguage AS T1
INNER JOIN (
    SELECT CountryCode, MAX(Percentage) AS MaxPercentage
    FROM countrylanguage
    GROUP BY CountryCode
) AS T2
ON T1.CountryCode = T2.CountryCode AND T1.Percentage = T2.MaxPercentage
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 233 row(s), 3 column(s):

    Papiamento | ABW | 76.7
    Pashto | AFG | 52.4
    Ovimbundu | AGO | 37.2
    English | AIA | 0.0
    Albaniana | ALB | 97.9
    Spanish | AND | 44.6
    Papiamento | ANT | 86.2
    Arabic | ARE | 42.0
    Spanish | ARG | 96.8
    Armenian | ARM | 93.4
    Samoan | ASM | 90.6
    Creole English | ATG | 95.7
    ... (233 rows total)

Returned query gives 241 row(s), 2 column(s):

    ABW | Papiamento
    AFG | Pashto
    AGO | Ovimbundu
    AIA | English
    ALB | Albaniana
    AND | Spanish
    ANT | Papiamento
    ARE | Arabic
    ARG | Spanish
    ARM | Armenian
    ASM | Samoan
    ATG | Creole English
    ... (241 rows total)

Difference: col_count_differs, disjoint; 0 row(s) in common, 233 only in the gold, 241 only in the returned result.

### R133  (question 432, database `world_1`)

- Returned by: kwai-autosql-32b/seed303
- Returned in cell: both A and D
- Class mass: 32/50
- Instances disagreeing: 46 of 46 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the codes of the different nations, and what are the languages spoken by the greatest percentage of people for each?

**Gold.**
```sql
SELECT LANGUAGE ,  CountryCode ,  max(Percentage) FROM countrylanguage GROUP BY CountryCode
```

**Returned.**
```sql
SELECT T1.CountryCode, T1.Language
FROM countrylanguage AS T1
INNER JOIN (
    SELECT CountryCode, MAX(Percentage) AS MaxPercentage
    FROM countrylanguage
    GROUP BY CountryCode
) AS T2
ON T1.CountryCode = T2.CountryCode AND T1.Percentage = T2.MaxPercentage
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 233 row(s), 3 column(s):

    Papiamento | ABW | 76.7
    Pashto | AFG | 52.4
    Ovimbundu | AGO | 37.2
    English | AIA | 0.0
    Albaniana | ALB | 97.9
    Spanish | AND | 44.6
    Papiamento | ANT | 86.2
    Arabic | ARE | 42.0
    Spanish | ARG | 96.8
    Armenian | ARM | 93.4
    Samoan | ASM | 90.6
    Creole English | ATG | 95.7
    ... (233 rows total)

Returned query gives 241 row(s), 2 column(s):

    ABW | Papiamento
    AFG | Pashto
    AGO | Ovimbundu
    AIA | English
    ALB | Albaniana
    AND | Spanish
    ANT | Papiamento
    ARE | Arabic
    ARG | Spanish
    ARM | Armenian
    ASM | Samoan
    ATG | Creole English
    ... (241 rows total)

Difference: col_count_differs, disjoint; 0 row(s) in common, 233 only in the gold, 241 only in the returned result.

### R134  (question 433, database `world_1`)

- Returned by: kwai-autosql-32b/seed303
- Returned in cell: both A and D
- Class mass: 19/50
- Instances disagreeing: 46 of 46 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the total number of countries where Spanish is spoken by the largest percentage of people?

**Gold.**
```sql
SELECT count(*) ,   max(Percentage) FROM countrylanguage WHERE LANGUAGE  =  "Spanish" GROUP BY CountryCode
```

**Returned.**
```sql
SELECT COUNT(*)
FROM countrylanguage cl1
WHERE Language = 'Spanish'
  AND Percentage = (
    SELECT MAX(Percentage)
    FROM countrylanguage cl2
    WHERE cl2.CountryCode = cl1.CountryCode
  )
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 28 row(s), 2 column(s):

    1 | 7.4
    1 | 44.6
    1 | 96.8
    1 | 31.6
    1 | 87.7
    1 | 0.7
    1 | 89.7
    1 | 99.0
    1 | 97.5
    1 | 100.0
    1 | 98.0
    1 | 93.0
    ... (28 rows total)

Returned query gives 1 row(s), 1 column(s):

    21

Difference: col_count_differs, disjoint; 0 row(s) in common, 27 only in the gold, 1 only in the returned result.

### R135  (question 434, database `world_1`)

- Returned by: kwai-autosql-32b/seed303
- Returned in cell: A only
- Class mass: 23/50
- Instances disagreeing: 46 of 46 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Count the number of countries for which Spanish is predominantly spoken .

**Gold.**
```sql
SELECT count(*) ,   max(Percentage) FROM countrylanguage WHERE LANGUAGE  =  "Spanish" GROUP BY CountryCode
```

**Returned.**
```sql
SELECT COUNT(*) FROM countrylanguage WHERE Language = 'Spanish' AND IsOfficial = 'T'
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 28 row(s), 2 column(s):

    1 | 7.4
    1 | 44.6
    1 | 96.8
    1 | 31.6
    1 | 87.7
    1 | 0.7
    1 | 89.7
    1 | 99.0
    1 | 97.5
    1 | 100.0
    1 | 98.0
    1 | 93.0
    ... (28 rows total)

Returned query gives 1 row(s), 1 column(s):

    20

Difference: col_count_differs, disjoint; 0 row(s) in common, 27 only in the gold, 1 only in the returned result.

### R136  (question 434, database `world_1`)

- Returned by: kwai-autosql-32b/seed303
- Returned in cell: D only
- Class mass: 23/50
- Instances disagreeing: 46 of 46 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Count the number of countries for which Spanish is predominantly spoken .

**Gold.**
```sql
SELECT count(*) ,   max(Percentage) FROM countrylanguage WHERE LANGUAGE  =  "Spanish" GROUP BY CountryCode
```

**Returned.**
```sql
SELECT COUNT(*)
FROM countrylanguage
WHERE Language = 'Spanish'
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 28 row(s), 2 column(s):

    1 | 7.4
    1 | 44.6
    1 | 96.8
    1 | 31.6
    1 | 87.7
    1 | 0.7
    1 | 89.7
    1 | 99.0
    1 | 97.5
    1 | 100.0
    1 | 98.0
    1 | 93.0
    ... (28 rows total)

Returned query gives 1 row(s), 1 column(s):

    28

Difference: col_count_differs, disjoint; 0 row(s) in common, 27 only in the gold, 1 only in the returned result.

### R137  (question 467, database `dog_kennels`)

- Returned by: kwai-autosql-32b/seed303
- Returned in cell: A only
- Class mass: 37/50
- Instances disagreeing: 48 of 48 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the names of the dogs for which the owner spent more than 1000 for treatment?

**Gold.**
```sql
select name from dogs where dog_id not in ( select dog_id from treatments group by dog_id having sum(cost_of_treatment)  >  1000 )
```

**Returned.**
```sql
SELECT T1.name
FROM Dogs AS T1
INNER JOIN Treatments AS T2 ON T1.dog_id = T2.dog_id
GROUP BY T1.name
HAVING SUM(T2.cost_of_treatment) > 1000
```

**First disagreeing instance** `dog_kennels.sqlite` (this is the shipped benchmark database).

Gold returns 12 row(s), 1 column(s):

    Kacey
    Hipolito
    Mavis
    Houston
    Jeffrey
    Merritt
    Narciso
    George
    Bessie
    Betty
    Holden
    Jesus

Returned query gives 3 row(s), 1 column(s):

    Evangeline
    Lyric
    Troy

Difference: disjoint; 0 row(s) in common, 12 only in the gold, 3 only in the returned result.

### R138  (question 31, database `concert_singer`)

- Returned by: kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 31/50, 34/50, 36/50
- Instances disagreeing: 32 of 32 (100%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Find the number of concerts happened in the stadium that can accommodate the most people.

**Gold.**
```sql
select count(*) from concert where stadium_id = (select stadium_id from stadium order by capacity desc limit 1)
```

**Returned.**
```sql
SELECT COUNT(T1.concert_ID)
FROM concert AS T1
INNER JOIN stadium AS T2 ON T1.Stadium_ID = T2.Stadium_ID
ORDER BY T2.Capacity DESC
LIMIT 1
```

**First disagreeing instance** `concert_singer.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    0

Returned query gives 1 row(s), 1 column(s):

    6

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R139  (question 32, database `concert_singer`)

- Returned by: kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 36/50, 32/50, 33/50
- Instances disagreeing: 32 of 32 (100%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What are the number of concerts that occurred in the stadium with space for the most people?

**Gold.**
```sql
select count(*) from concert where stadium_id = (select stadium_id from stadium order by capacity desc limit 1)
```

**Returned.**
```sql
SELECT COUNT(T1.concert_ID)
FROM concert AS T1
INNER JOIN stadium AS T2 ON T1.Stadium_ID = T2.Stadium_ID
ORDER BY T2.Capacity DESC
LIMIT 1
```

**First disagreeing instance** `concert_singer.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    0

Returned query gives 1 row(s), 1 column(s):

    6

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R140  (question 46, database `pets_1`)

- Returned by: kwai-autosql-14b/seed101
- Returned in cell: both A and D
- Class mass: 27/50
- Instances disagreeing: 16 of 27 (59%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What major is every student who does not own a cat, and also how old are they?

**Gold.**
```sql
SELECT major ,  age FROM student WHERE stuid NOT IN (SELECT T1.stuid FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid  =  T2.stuid JOIN pets AS T3 ON T3.petid  =  T2.petid WHERE T3.pettype  =  'cat')
```

**Returned.**
```sql
SELECT DISTINCT Major, Age
FROM Student
WHERE StuID NOT IN (
    SELECT StuID
    FROM Has_Pet
    INNER JOIN Pets ON Has_Pet.PetID = Pets.PetID
    WHERE Pets.PetType = 'cat'
)
```

**First disagreeing instance** `pets_1.sqlite` (this is the shipped benchmark database).

Gold returns 33 row(s), 2 column(s):

    600 | 19
    600 | 21
    600 | 20
    600 | 26
    600 | 18
    600 | 18
    600 | 20
    600 | 19
    600 | 17
    600 | 22
    600 | 20
    600 | 18
    ... (33 rows total)

Returned query gives 21 row(s), 2 column(s):

    600 | 19
    600 | 21
    600 | 20
    600 | 26
    600 | 18
    600 | 17
    600 | 22
    600 | 16
    600 | 27
    520 | 22
    520 | 19
    540 | 17
    ... (21 rows total)

Difference: duplicate_multiplicity_only; 21 row(s) in common, 0 only in the gold, 0 only in the returned result.

### R141  (question 49, database `pets_1`)

- Returned by: kwai-autosql-14b/seed101
- Returned in cell: both A and D
- Class mass: 48/50
- Instances disagreeing: 20 of 27 (74%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find the first name and age of students who have a dog but do not have a cat.

**Gold.**
```sql
SELECT T1.fname ,  T1.age FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid  =  T2.stuid JOIN pets AS T3 ON T3.petid  =  T2.petid WHERE T3.pettype  =  'dog' AND T1.stuid NOT IN (SELECT T1.stuid FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid  =  T2.stuid JOIN pets AS T3 ON T3.petid  =  T2.petid WHERE T3.pettype  =  'cat')
```

**Returned.**
```sql
SELECT DISTINCT T1.Fname, T1.Age
FROM Student AS T1
INNER JOIN Has_Pet AS T2 ON T1.StuID = T2.StuID
INNER JOIN Pets AS T3 ON T2.PetID = T3.PetID
WHERE T3.PetType = 'dog'
AND T1.StuID NOT IN (
    SELECT T2.StuID
    FROM Has_Pet AS T2
    INNER JOIN Pets AS T3 ON T2.PetID = T3.PetID
    WHERE T3.PetType = 'cat'
)
```

**First disagreeing instance** `pets_1.sqlite` (this is the shipped benchmark database).

Gold returns 2 row(s), 2 column(s):

    Tracy | 19
    Tracy | 19

Returned query gives 1 row(s), 2 column(s):

    Tracy | 19

Difference: duplicate_multiplicity_only; 1 row(s) in common, 0 only in the gold, 0 only in the returned result.

### R142  (question 50, database `pets_1`)

- Returned by: kwai-autosql-14b/seed101
- Returned in cell: both A and D
- Class mass: 50/50
- Instances disagreeing: 25 of 27 (93%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the first name of every student who has a dog but does not have a cat?

**Gold.**
```sql
SELECT T1.fname ,  T1.age FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid  =  T2.stuid JOIN pets AS T3 ON T3.petid  =  T2.petid WHERE T3.pettype  =  'dog' AND T1.stuid NOT IN (SELECT T1.stuid FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid  =  T2.stuid JOIN pets AS T3 ON T3.petid  =  T2.petid WHERE T3.pettype  =  'cat')
```

**Returned.**
```sql
SELECT DISTINCT T1.Fname
FROM Student AS T1
INNER JOIN Has_Pet AS T2 ON T1.StuID = T2.StuID
INNER JOIN Pets AS T3 ON T2.PetID = T3.PetID
WHERE T3.PetType = 'dog'
AND T1.StuID NOT IN (
    SELECT T2.StuID
    FROM Has_Pet AS T2
    INNER JOIN Pets AS T3 ON T2.PetID = T3.PetID
    WHERE T3.PetType = 'cat'
)
```

**First disagreeing instance** `pets_1.sqlite` (this is the shipped benchmark database).

Gold returns 2 row(s), 2 column(s):

    Tracy | 19
    Tracy | 19

Returned query gives 1 row(s), 1 column(s):

    Tracy

Difference: col_count_differs, disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R143  (question 63, database `car_1`)

- Returned by: kwai-autosql-14b/seed101
- Returned in cell: A only
- Class mass: 26/50
- Instances disagreeing: 41 of 60 (68%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find the name of the makers that produced some cars in 1970?

**Gold.**
```sql
SELECT DISTINCT T1.Maker FROM CAR_MAKERS AS T1 JOIN MODEL_LIST AS T2 ON T1.Id  =  T2.Maker JOIN CAR_NAMES AS T3 ON T2.model  =  T3.model JOIN CARS_DATA AS T4 ON T3.MakeId  =  T4.id WHERE T4.year  =  '1970';
```

**Returned.**
```sql
SELECT DISTINCT T3.Maker
FROM cars_data AS T1
INNER JOIN car_names AS T2 ON T1.Id = T2.MakeId
INNER JOIN car_makers AS T3 ON T2.Make = T3.Maker
WHERE T1.Year = 1970
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 11 row(s), 1 column(s):

    gm
    chrysler
    amc
    ford
    citroen
    toyota
    nissan
    volkswagen
    peugeaut
    saab
    bmw

Returned query gives 0 row(s), None column(s):

    (no rows)

Difference: rep_empty; 0 row(s) in common, 11 only in the gold, 0 only in the returned result.

### R144  (question 64, database `car_1`)

- Returned by: kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 20/50, 23/50, 25/50
- Instances disagreeing: 41 of 60 (68%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the name of the different car makers who produced a car in 1970?

**Gold.**
```sql
SELECT DISTINCT T1.Maker FROM CAR_MAKERS AS T1 JOIN MODEL_LIST AS T2 ON T1.Id  =  T2.Maker JOIN CAR_NAMES AS T3 ON T2.model  =  T3.model JOIN CARS_DATA AS T4 ON T3.MakeId  =  T4.id WHERE T4.year  =  '1970';
```

**Returned.**
```sql
SELECT DISTINCT T3.FullName
FROM cars_data AS T1
INNER JOIN car_names AS T2 ON T1.Id = T2.MakeId
INNER JOIN car_makers AS T3 ON T2.Make = T3.Maker
WHERE T1.Year = 1970
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 11 row(s), 1 column(s):

    gm
    chrysler
    amc
    ford
    citroen
    toyota
    nissan
    volkswagen
    peugeaut
    saab
    bmw

Returned query gives 0 row(s), None column(s):

    (no rows)

Difference: rep_empty; 0 row(s) in common, 11 only in the gold, 0 only in the returned result.

### R145  (question 65, database `car_1`)

- Returned by: kwai-autosql-14b/seed101, kwai-autosql-14b/seed303
- Returned in cell: A only
- Class mass: 10/50, 18/50
- Instances disagreeing: 58 of 60 (97%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find the make and production time of the cars that were produced in the earliest ?

**Gold.**
```sql
SELECT T2.Make ,  T1.Year FROM CARS_DATA AS T1 JOIN CAR_NAMES AS T2 ON T1.Id  =  T2.MakeId WHERE T1.Year  =  (SELECT min(YEAR) FROM CARS_DATA);
```

**Returned.**
```sql
SELECT T1.Maker, T3.Year
FROM car_makers AS T1
INNER JOIN car_names AS T2 ON T1.Id = T2.Make
INNER JOIN cars_data AS T3 ON T2.MakeId = T3.Id
ORDER BY T3.Year ASC
LIMIT 1
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 35 row(s), 2 column(s):

    chevrolet chevelle malibu | 1970
    buick skylark 320 | 1970
    plymouth satellite | 1970
    amc rebel sst | 1970
    ford torino | 1970
    ford galaxie 500 | 1970
    chevrolet impala | 1970
    plymouth fury iii | 1970
    pontiac catalina | 1970
    amc ambassador dpl | 1970
    citroen ds-21 pallas | 1970
    chevrolet chevelle concours (sw) | 1970
    ... (35 rows total)

Returned query gives 0 row(s), None column(s):

    (no rows)

Difference: rep_empty; 0 row(s) in common, 35 only in the gold, 0 only in the returned result.

### R146  (question 77, database `car_1`)

- Returned by: kwai-autosql-14b/seed101
- Returned in cell: both A and D
- Class mass: 23/50
- Instances disagreeing: 31 of 60 (52%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the count of the car models produced in the United States?

**Gold.**
```sql
SELECT count(*) FROM MODEL_LIST AS T1 JOIN CAR_MAKERS AS T2 ON T1.Maker  =  T2.Id JOIN COUNTRIES AS T3 ON T2.Country  =  T3.CountryId WHERE T3.CountryName  =  'usa';
```

**Returned.**
```sql
SELECT COUNT(T3.Model)
FROM countries AS T1
INNER JOIN car_makers AS T2 ON T1.CountryId = T2.Country
INNER JOIN car_names AS T3 ON T2.Id = T3.MakeId
WHERE T1.CountryName = 'usa'
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    13

Returned query gives 1 row(s), 1 column(s):

    4

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R147  (question 91, database `car_1`)

- Returned by: kwai-autosql-14b/seed101
- Returned in cell: A only
- Class mass: 18/50
- Instances disagreeing: 10 of 60 (17%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the average edispl for all volvos?

**Gold.**
```sql
SELECT avg(T2.edispl) FROM CAR_NAMES AS T1 JOIN CARS_DATA AS T2 ON T1.MakeId  =  T2.Id WHERE T1.Model  =  'volvo';
```

**Returned.**
```sql
SELECT AVG(T3.Edispl)
FROM car_makers AS T1
INNER JOIN car_names AS T2 ON T1.Maker = T2.Make
INNER JOIN cars_data AS T3 ON T2.MakeId = T3.Id
WHERE T1.Maker = 'volvo'
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    133.5

Returned query gives 1 row(s), 1 column(s):

    NULL

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R148  (question 91, database `car_1`)

- Returned by: kwai-autosql-14b/seed101
- Returned in cell: D only
- Class mass: 9/50
- Instances disagreeing: 11 of 60 (18%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the average edispl for all volvos?

**Gold.**
```sql
SELECT avg(T2.edispl) FROM CAR_NAMES AS T1 JOIN CARS_DATA AS T2 ON T1.MakeId  =  T2.Id WHERE T1.Model  =  'volvo';
```

**Returned.**
```sql
SELECT AVG(T3.Edispl)
FROM car_makers AS T1
INNER JOIN model_list AS T2 ON T1.Id = T2.Maker
INNER JOIN cars_data AS T3 ON T2.ModelId = T3.Id
WHERE T1.Maker = 'volvo'
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    133.5

Returned query gives 1 row(s), 1 column(s):

    360.0

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R149  (question 99, database `car_1`)

- Returned by: kwai-autosql-14b/seed101
- Returned in cell: A only
- Class mass: 19/50
- Instances disagreeing: 58 of 60 (97%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Which distinctive models are produced by General Motors or heavier than 3500?

**Gold.**
```sql
SELECT DISTINCT T2.Model FROM CAR_NAMES AS T1 JOIN MODEL_LIST AS T2 ON T1.Model  =  T2.Model JOIN CAR_MAKERS AS T3 ON T2.Maker  =  T3.Id JOIN CARS_DATA AS T4 ON T1.MakeId  =  T4.Id WHERE T3.FullName  =  'General Motors' OR T4.weight  >  3500;
```

**Returned.**
```sql
SELECT DISTINCT T2.Model
FROM car_makers AS T1
INNER JOIN car_names AS T2 ON T1.Maker = T2.Make
INNER JOIN cars_data AS T3 ON T2.MakeId = T3.Id
WHERE T1.FullName = 'American Motor Company' OR T3.Weight > 3500
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 13 row(s), 1 column(s):

    chevrolet
    buick
    ford
    plymouth
    pontiac
    amc
    dodge
    mercury
    oldsmobile
    chrysler
    mercedes-benz
    cadillac
    ... (13 rows total)

Returned query gives 0 row(s), None column(s):

    (no rows)

Difference: rep_empty; 0 row(s) in common, 13 only in the gold, 0 only in the returned result.

### R150  (question 100, database `car_1`)

- Returned by: kwai-autosql-14b/seed101
- Returned in cell: A only
- Class mass: 13/50
- Instances disagreeing: 27 of 60 (45%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the different models created by either General Motors or over 3500 lbs?

**Gold.**
```sql
SELECT DISTINCT T2.Model FROM CAR_NAMES AS T1 JOIN MODEL_LIST AS T2 ON T1.Model  =  T2.Model JOIN CAR_MAKERS AS T3 ON T2.Maker  =  T3.Id JOIN CARS_DATA AS T4 ON T1.MakeId  =  T4.Id WHERE T3.FullName  =  'General Motors' OR T4.weight  >  3500;
```

**Returned.**
```sql
SELECT DISTINCT T1.Model
FROM car_names AS T1
INNER JOIN cars_data AS T2 ON T1.MakeId = T2.Id
INNER JOIN car_makers AS T3 ON T1.Make = T3.Maker
WHERE T3.FullName = 'American Motor Company'
UNION
SELECT DISTINCT T1.Model
FROM car_names AS T1
INNER JOIN cars_data AS T2 ON T1.MakeId = T2.Id
WHERE T2.Weight > 3500
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 13 row(s), 1 column(s):

    chevrolet
    buick
    ford
    plymouth
    pontiac
    amc
    dodge
    mercury
    oldsmobile
    chrysler
    mercedes-benz
    cadillac
    ... (13 rows total)

Returned query gives 14 row(s), 1 column(s):

    amc
    buick
    cadillac
    chevrolet
    chrysler
    dodge
    ford
    hi
    mercedes
    mercedes-benz
    mercury
    oldsmobile
    ... (14 rows total)

Difference: gold_subset_of_rep; 13 row(s) in common, 0 only in the gold, 1 only in the returned result.

### R151  (question 100, database `car_1`)

- Returned by: kwai-autosql-14b/seed101
- Returned in cell: D only
- Class mass: 8/50
- Instances disagreeing: 57 of 60 (95%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the different models created by either General Motors or over 3500 lbs?

**Gold.**
```sql
SELECT DISTINCT T2.Model FROM CAR_NAMES AS T1 JOIN MODEL_LIST AS T2 ON T1.Model  =  T2.Model JOIN CAR_MAKERS AS T3 ON T2.Maker  =  T3.Id JOIN CARS_DATA AS T4 ON T1.MakeId  =  T4.Id WHERE T3.FullName  =  'General Motors' OR T4.weight  >  3500;
```

**Returned.**
```sql
SELECT DISTINCT T3.Model
FROM car_makers AS T1
INNER JOIN car_names AS T3 ON T1.Id = T3.MakeId
INNER JOIN cars_data AS T2 ON T2.Id = T3.MakeId
WHERE T1.FullName = 'General Motors' OR T2.Weight > 3500
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 13 row(s), 1 column(s):

    chevrolet
    buick
    ford
    plymouth
    pontiac
    amc
    dodge
    mercury
    oldsmobile
    chrysler
    mercedes-benz
    cadillac
    ... (13 rows total)

Returned query gives 7 row(s), 1 column(s):

    chevrolet
    buick
    amc
    ford
    plymouth
    pontiac
    dodge

Difference: rep_subset_of_gold; 7 row(s) in common, 6 only in the gold, 0 only in the returned result.

### R152  (question 105, database `car_1`)

- Returned by: kwai-autosql-14b/seed101
- Returned in cell: D only
- Class mass: 19/50
- Instances disagreeing: 60 of 60 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** How many nations has more than 2 car makers ?

**Gold.**
```sql
select count(*) from countries as t1 join car_makers as t2 on t1.countryid  =  t2.country group by t1.countryid having count(*)  >  2
```

**Returned.**
```sql
SELECT COUNT(*)
FROM (
  SELECT T1.Country
  FROM car_makers AS T1
  INNER JOIN countries AS T2 ON T1.Country = T2.CountryId
  GROUP BY T1.Country
  HAVING COUNT(T1.Id) > 2
) AS subquery
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 4 row(s), 1 column(s):

    4
    4
    3
    5

Returned query gives 1 row(s), 1 column(s):

    4

Difference: rep_subset_of_gold; 1 row(s) in common, 2 only in the gold, 0 only in the returned result.

### R153  (question 107, database `car_1`)

- Returned by: kwai-autosql-14b/seed101
- Returned in cell: both A and D
- Class mass: 31/50
- Instances disagreeing: 52 of 60 (87%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** For all of the 4 CYL cars, which model has the most horsepower?

**Gold.**
```sql
SELECT T1.Model FROM CAR_NAMES AS T1 JOIN CARS_DATA AS T2 ON T1.MakeId  =  T2.Id WHERE T2.Cylinders  =  4 ORDER BY T2.horsepower DESC LIMIT 1;
```

**Returned.**
```sql
SELECT T2.Model
FROM cars_data AS T1
INNER JOIN car_names AS T2 ON T1.Id = T2.MakeId
WHERE T1.Cylinders = 4
ORDER BY CAST(T1.Horsepower AS REAL) DESC
LIMIT 1
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    ford

Returned query gives 1 row(s), 1 column(s):

    citroen

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R154  (question 140, database `flight_2`)

- Returned by: kwai-autosql-14b/seed101, kwai-autosql-14b/seed202
- Returned in cell: both A and D
- Class mass: 49/50, 48/50
- Instances disagreeing: 8 of 56 (14%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Give the number of Jetblue Airways flights.

**Gold.**
```sql
SELECT count(*) FROM FLIGHTS AS T1 JOIN AIRLINES AS T2 ON T1.Airline  =  T2.uid WHERE T2.Airline = "JetBlue Airways"
```

**Returned.**
```sql
SELECT COUNT(*)
FROM flights
INNER JOIN airlines ON flights.Airline = airlines.uid
WHERE airlines.Airline = 'Jetblue Airways'
```

**First disagreeing instance** `flight_2.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    100

Returned query gives 1 row(s), 1 column(s):

    0

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R155  (question 148, database `flight_2`)

- Returned by: kwai-autosql-14b/seed101
- Returned in cell: D only
- Class mass: 27/50
- Instances disagreeing: 4 of 56 (7%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Which airlines have a flight from  AHD?

**Gold.**
```sql
SELECT T1.Airline FROM AIRLINES AS T1 JOIN FLIGHTS AS T2 ON T1.uid  =  T2.Airline WHERE T2.SourceAirport  =  "AHD"
```

**Returned.**
```sql
SELECT DISTINCT T1.Airline
FROM airlines AS T1
INNER JOIN flights AS T2 ON T1.uid = T2.Airline
WHERE T2.SourceAirport = 'AHD'
```

**First disagreeing instance** `flight_2v5081.sqlite`.

Gold returns 2 row(s), 1 column(s):

    Virgin America
    Virgin America

Returned query gives 1 row(s), 1 column(s):

    Virgin America

Difference: duplicate_multiplicity_only; 1 row(s) in common, 0 only in the gold, 0 only in the returned result.

### R156  (question 191, database `course_teach`)

- Returned by: kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 50/50, 50/50, 50/50
- Instances disagreeing: 16 of 25 (64%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** List the name of teachers who are not from Little Lever Urban District.

**Gold.**
```sql
select name from teacher where hometown != "little lever urban district"
```

**Returned.**
```sql
SELECT Name FROM teacher WHERE Hometown != 'Little Lever Urban District'
```

**First disagreeing instance** `course_teach.sqlite` (this is the shipped benchmark database).

Gold returns 7 row(s), 1 column(s):

    Joseph Huts
    Gustaaf Deloor
    Vicente Carretero
    John Deloor
    Kearsley Brown
    Anne Walker
    Lucy Wong

Returned query gives 6 row(s), 1 column(s):

    Joseph Huts
    Gustaaf Deloor
    Vicente Carretero
    John Deloor
    Kearsley Brown
    Lucy Wong

Difference: rep_subset_of_gold; 6 row(s) in common, 1 only in the gold, 0 only in the returned result.

### R157  (question 192, database `course_teach`)

- Returned by: kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 50/50, 50/50, 50/50
- Instances disagreeing: 16 of 25 (64%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the names of the teachers who do not come from Little Lever Urban District?

**Gold.**
```sql
select name from teacher where hometown != "little lever urban district"
```

**Returned.**
```sql
SELECT Name FROM teacher WHERE Hometown != 'Little Lever Urban District'
```

**First disagreeing instance** `course_teach.sqlite` (this is the shipped benchmark database).

Gold returns 7 row(s), 1 column(s):

    Joseph Huts
    Gustaaf Deloor
    Vicente Carretero
    John Deloor
    Kearsley Brown
    Anne Walker
    Lucy Wong

Returned query gives 6 row(s), 1 column(s):

    Joseph Huts
    Gustaaf Deloor
    Vicente Carretero
    John Deloor
    Kearsley Brown
    Lucy Wong

Difference: rep_subset_of_gold; 6 row(s) in common, 1 only in the gold, 0 only in the returned result.

### R158  (question 213, database `museum_visit`)

- Returned by: kwai-autosql-14b/seed101, kwai-autosql-14b/seed202
- Returned in cell: both A and D
- Class mass: 50/50, 46/50
- Instances disagreeing: 35 of 35 (100%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What are the id, name and membership level of people who have paid the largest amount of money overall in all museum tickets?

**Gold.**
```sql
SELECT t2.visitor_id ,  t1.name ,  t1.Level_of_membership FROM visitor AS t1 JOIN visit AS t2 ON t1.id  =  t2.visitor_id GROUP BY t2.visitor_id ORDER BY sum(t2.Total_spent) DESC LIMIT 1
```

**Returned.**
```sql
SELECT T2.ID, T2.Name, T2.Level_of_membership
FROM visit AS T1
INNER JOIN visitor AS T2 ON T1.visitor_ID = T2.ID
ORDER BY T1.Total_spent DESC
LIMIT 1
```

**First disagreeing instance** `museum_visit.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 3 column(s):

    3 | Arjen Robben | 1

Returned query gives 1 row(s), 3 column(s):

    3 | Arjen Robben | 1

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R159  (question 213, database `museum_visit`)

- Returned by: kwai-autosql-14b/seed101, kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 27/50, 48/50
- Instances disagreeing: 35 of 35 (100%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What are the id, name and membership level of people who have paid the largest amount of money overall in all museum tickets?

**Gold.**
```sql
SELECT t2.visitor_id ,  t1.name ,  t1.Level_of_membership FROM visitor AS t1 JOIN visit AS t2 ON t1.id  =  t2.visitor_id GROUP BY t2.visitor_id ORDER BY sum(t2.Total_spent) DESC LIMIT 1
```

**Returned.**
```sql
SELECT T2.ID, T2.Name, T2.Level_of_membership
FROM visit AS T1
INNER JOIN visitor AS T2 ON T1.visitor_ID = T2.ID
GROUP BY T2.ID, T2.Name, T2.Level_of_membership
ORDER BY SUM(T1.Total_spent) DESC
LIMIT 1
```

**First disagreeing instance** `museum_visit.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 3 column(s):

    3 | Arjen Robben | 1

Returned query gives 1 row(s), 3 column(s):

    3 | Arjen Robben | 1

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R160  (question 228, database `wta_1`)

- Returned by: kwai-autosql-14b/seed101
- Returned in cell: A only
- Class mass: 24/50
- Instances disagreeing: 31 of 33 (94%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Find the first name and country code of the oldest player.

**Gold.**
```sql
SELECT first_name ,  country_code FROM players ORDER BY birth_date LIMIT 1
```

**Returned.**
```sql
SELECT first_name, country_code
FROM players
ORDER BY (strftime('%Y', 'now') - strftime('%Y', birth_date)) DESC
LIMIT 1
```

**First disagreeing instance** `wta_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    Thelma | AUS

Returned query gives 1 row(s), 2 column(s):

    Martina | SUI

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R161  (question 230, database `wta_1`)

- Returned by: kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303, omnisql-32b/seed101
- Returned in cell: both A and D
- Class mass: 49/50, 45/50, 46/50, 37/50
- Instances disagreeing: 33 of 33 (100%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** List the first and last name of all players ordered by their age.

**Gold.**
```sql
SELECT first_name ,  last_name FROM players ORDER BY birth_date
```

**Returned.**
```sql
SELECT first_name, last_name
FROM players
ORDER BY (strftime('%Y', 'now') - strftime('%Y', birth_date))
```

**First disagreeing instance** `wta_1.sqlite` (this is the shipped benchmark database).

Gold returns 20662 row(s), 2 column(s):

    Thelma | Long
    Pauline | Addie
    Milly | Vagn Nielsen
    Vera | Johansen
    Reiko | Miyagi
    Louise | Brown
    Gertrude | Moran
    Zsuzsa | Kormoczy
    Peggy | Brixhe
    Betty | Pratt
    Doris | Hart
    Dorothy | Knode
    ... (20662 rows total)

Returned query gives 20662 row(s), 2 column(s):

    Martina | Hingis
    Mirjana | Lucic
    Justine | Henin
    Kerry Anne | Guse
    Jolene | Watanabe Giltz
    Karina | Habsudova
    Silvija | Talaja
    Alicia | Molik
    Tamarine | Tanasugarn
    Rita | Grande
    Katarina | Srebotnik
    Jana | Nejedly
    ... (20662 rows total)

Difference: row_order_only; 20658 row(s) in common, 0 only in the gold, 0 only in the returned result.

### R162  (question 231, database `wta_1`)

- Returned by: kwai-autosql-14b/seed101
- Returned in cell: both A and D
- Class mass: 45/50
- Instances disagreeing: 33 of 33 (100%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What are the full names of all players, sorted by age?

**Gold.**
```sql
SELECT first_name ,  last_name FROM players ORDER BY birth_date
```

**Returned.**
```sql
SELECT first_name, last_name
FROM players
ORDER BY (strftime('%Y', 'now') - strftime('%Y', birth_date)) ASC
```

**First disagreeing instance** `wta_1.sqlite` (this is the shipped benchmark database).

Gold returns 20662 row(s), 2 column(s):

    Thelma | Long
    Pauline | Addie
    Milly | Vagn Nielsen
    Vera | Johansen
    Reiko | Miyagi
    Louise | Brown
    Gertrude | Moran
    Zsuzsa | Kormoczy
    Peggy | Brixhe
    Betty | Pratt
    Doris | Hart
    Dorothy | Knode
    ... (20662 rows total)

Returned query gives 20662 row(s), 2 column(s):

    Martina | Hingis
    Mirjana | Lucic
    Justine | Henin
    Kerry Anne | Guse
    Jolene | Watanabe Giltz
    Karina | Habsudova
    Silvija | Talaja
    Alicia | Molik
    Tamarine | Tanasugarn
    Rita | Grande
    Katarina | Srebotnik
    Jana | Nejedly
    ... (20662 rows total)

Difference: row_order_only; 20658 row(s) in common, 0 only in the gold, 0 only in the returned result.

### R163  (question 232, database `wta_1`)

- Returned by: kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 40/50, 36/50, 42/50
- Instances disagreeing: 8 of 33 (24%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** List the first and last name of all players who are left handed  in the order of age.

**Gold.**
```sql
SELECT first_name ,  last_name FROM players WHERE hand  =  'L' ORDER BY birth_date
```

**Returned.**
```sql
SELECT first_name, last_name
FROM players
WHERE hand = 'L'
ORDER BY (strftime('%Y', 'now') - strftime('%Y', birth_date))
```

**First disagreeing instance** `wta_1.sqlite` (this is the shipped benchmark database).

Gold returns 487 row(s), 2 column(s):

    Ann | Jones
    Wendy | Gilchrist
    Martina | Navratilova
    Mary | Carillo
    Katerina | Bohmova
    Petra | Delhees Jauch
    Nancy | Loeffler Caro
    Lise | Gregory
    Rene | Collins
    Nicole | Arendt
    Florencia | Labat
    Sabine | Appelmans
    ... (487 rows total)

Returned query gives 487 row(s), 2 column(s):

    Florencia | Labat
    Magui | Serna
    Amanda | Grahame
    Sabine | Appelmans
    Jelena | Kostanic Tosic
    Gala | Leon Garcia
    Patty | Schnyder
    Anne Gaelle | Sidot
    Julie | Pullin
    Barbara | Schwartz
    Anca | Barna
    Amelie | Cocheteux
    ... (487 rows total)

Difference: row_order_only; 486 row(s) in common, 0 only in the gold, 0 only in the returned result.

### R164  (question 233, database `wta_1`)

- Returned by: kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 34/50, 41/50, 39/50
- Instances disagreeing: 8 of 33 (24%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What are the full names of all left handed players, in order of age?

**Gold.**
```sql
SELECT first_name ,  last_name FROM players WHERE hand  =  'L' ORDER BY birth_date
```

**Returned.**
```sql
SELECT first_name, last_name
FROM players
WHERE hand = 'L'
ORDER BY (strftime('%Y', 'now') - strftime('%Y', birth_date))
```

**First disagreeing instance** `wta_1.sqlite` (this is the shipped benchmark database).

Gold returns 487 row(s), 2 column(s):

    Ann | Jones
    Wendy | Gilchrist
    Martina | Navratilova
    Mary | Carillo
    Katerina | Bohmova
    Petra | Delhees Jauch
    Nancy | Loeffler Caro
    Lise | Gregory
    Rene | Collins
    Nicole | Arendt
    Florencia | Labat
    Sabine | Appelmans
    ... (487 rows total)

Returned query gives 487 row(s), 2 column(s):

    Florencia | Labat
    Magui | Serna
    Amanda | Grahame
    Sabine | Appelmans
    Jelena | Kostanic Tosic
    Gala | Leon Garcia
    Patty | Schnyder
    Anne Gaelle | Sidot
    Julie | Pullin
    Barbara | Schwartz
    Anca | Barna
    Amelie | Cocheteux
    ... (487 rows total)

Difference: row_order_only; 486 row(s) in common, 0 only in the gold, 0 only in the returned result.

### R165  (question 234, database `wta_1`)

- Returned by: kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 19/50, 14/50, 14/50
- Instances disagreeing: 33 of 33 (100%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Find the name and rank points of the person who won the most times.

**Gold.**
```sql
SELECT winner_name ,  winner_rank_points FROM matches GROUP BY winner_name ORDER BY count(*) DESC LIMIT 1
```

**Returned.**
```sql
SELECT P.first_name, P.last_name, R.ranking_points
FROM matches M
INNER JOIN players P ON M.winner_id = P.player_id
INNER JOIN rankings R ON P.player_id = R.player_id
GROUP BY P.first_name, P.last_name, R.ranking_points
ORDER BY COUNT(M.winner_id) DESC
LIMIT 1
```

**First disagreeing instance** `wta_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    Angelique Kerber | 3715

Returned query gives 1 row(s), 3 column(s):

    Karolina | Pliskova | 4

Difference: col_count_differs, disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R166  (question 235, database `wta_1`)

- Returned by: kwai-autosql-14b/seed101, kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 22/50, 22/50
- Instances disagreeing: 33 of 33 (100%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What is the name of the player who has won the most matches, and how many rank points does this player have?

**Gold.**
```sql
SELECT winner_name ,  winner_rank_points FROM matches GROUP BY winner_name ORDER BY count(*) DESC LIMIT 1
```

**Returned.**
```sql
SELECT p.first_name, p.last_name, r.ranking_points
FROM matches m
INNER JOIN players p ON m.winner_id = p.player_id
INNER JOIN rankings r ON p.player_id = r.player_id
GROUP BY p.first_name, p.last_name, r.ranking_points
ORDER BY COUNT(m.winner_id) DESC
LIMIT 1
```

**First disagreeing instance** `wta_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    Angelique Kerber | 3715

Returned query gives 1 row(s), 3 column(s):

    Karolina | Pliskova | 4

Difference: col_count_differs, disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R167  (question 249, database `wta_1`)

- Returned by: kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 45/50, 42/50, 41/50
- Instances disagreeing: 4 of 33 (12%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find the number of left handed winners who participated in the WTA Championships.

**Gold.**
```sql
SELECT count(DISTINCT winner_name) FROM matches WHERE tourney_name  =  'WTA Championships' AND winner_hand  =  'L'
```

**Returned.**
```sql
SELECT COUNT(winner_id)
FROM matches
WHERE tourney_name = 'WTA Championships' AND winner_hand = 'L'
```

**First disagreeing instance** `wta_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    2

Returned query gives 1 row(s), 1 column(s):

    3

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R168  (question 252, database `battle_death`)

- Returned by: kwai-autosql-14b/seed101, kwai-autosql-14b/seed303
- Returned in cell: A only
- Class mass: 50/50, 48/50
- Instances disagreeing: 28 of 28 (100%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What is the ship id and name that caused most total injuries?

**Gold.**
```sql
SELECT T2.id ,  T2.name FROM death AS T1 JOIN ship AS t2 ON T1.caused_by_ship_id  =  T2.id GROUP BY T2.id ORDER BY count(*) DESC LIMIT 1
```

**Returned.**
```sql
SELECT T2.id, T2.name
FROM death AS T1
INNER JOIN ship AS T2 ON T1.caused_by_ship_id = T2.id
ORDER BY T1.injured DESC
LIMIT 1
```

**First disagreeing instance** `battle_death.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    5 | Three Brothers

Returned query gives 1 row(s), 2 column(s):

    4 | HMS Avon

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R169  (question 252, database `battle_death`)

- Returned by: kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 29/50, 48/50, 28/50
- Instances disagreeing: 27 of 28 (96%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What is the ship id and name that caused most total injuries?

**Gold.**
```sql
SELECT T2.id ,  T2.name FROM death AS T1 JOIN ship AS t2 ON T1.caused_by_ship_id  =  T2.id GROUP BY T2.id ORDER BY count(*) DESC LIMIT 1
```

**Returned.**
```sql
SELECT T2.id, T2.name
FROM death AS T1
INNER JOIN ship AS T2 ON T1.caused_by_ship_id = T2.id
GROUP BY T2.id, T2.name
ORDER BY SUM(T1.injured) DESC
LIMIT 1
```

**First disagreeing instance** `battle_death.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    5 | Three Brothers

Returned query gives 1 row(s), 2 column(s):

    4 | HMS Avon

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R170  (question 253, database `battle_death`)

- Returned by: kwai-autosql-14b/seed101, kwai-autosql-14b/seed202
- Returned in cell: both A and D
- Class mass: 32/50, 32/50
- Instances disagreeing: 17 of 28 (61%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** List the name and date the battle that has lost  Lettice and HMS Atalanta

**Gold.**
```sql
SELECT T1.name ,  T1.date FROM battle AS T1 JOIN ship AS T2 ON T1.id  =  T2.lost_in_battle WHERE T2.name  =  'Lettice' INTERSECT SELECT T1.name ,  T1.date FROM battle AS T1 JOIN ship AS T2 ON T1.id  =  T2.lost_in_battle WHERE T2.name  =  'HMS Atalanta'
```

**Returned.**
```sql
SELECT T2.name, T2.date
FROM ship AS T1
INNER JOIN battle AS T2 ON T1.lost_in_battle = T2.id
WHERE T1.name IN ('Lettice', 'HMS Atalanta')
```

**First disagreeing instance** `battle_death.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    Siege of Constantinople | 1235

Returned query gives 2 row(s), 2 column(s):

    Siege of Constantinople | 1235
    Siege of Constantinople | 1235

Difference: duplicate_multiplicity_only; 1 row(s) in common, 0 only in the gold, 0 only in the returned result.

### R171  (question 259, database `student_transcripts_tracking`)

- Returned by: kwai-autosql-14b/seed101, kwai-autosql-14b/seed202
- Returned in cell: both A and D
- Class mass: 50/50, 50/50
- Instances disagreeing: 22 of 55 (40%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find the last name of the students who currently live in North Carolina but have not registered in any degree program.

**Gold.**
```sql
SELECT T1.last_name FROM Students AS T1 JOIN Addresses AS T2 ON T1.current_address_id  =  T2.address_id WHERE T2.state_province_county  =  'NorthCarolina' EXCEPT SELECT DISTINCT T3.last_name FROM Students AS T3 JOIN Student_Enrolment AS T4 ON T3.student_id  =  T4.student_id
```

**Returned.**
```sql
SELECT T1.last_name
FROM Students AS T1
INNER JOIN Addresses AS T2 ON T1.current_address_id = T2.address_id
WHERE T2.state_province_county = 'North Carolina'
AND T1.student_id NOT IN (SELECT student_id FROM Student_Enrolment)
```

**First disagreeing instance** `student_transcripts_tracking.sqlite` (this is the shipped benchmark database).

Gold returns 2 row(s), 1 column(s):

    Gleichner
    Weimann

Returned query gives 0 row(s), None column(s):

    (no rows)

Difference: rep_empty; 0 row(s) in common, 2 only in the gold, 0 only in the returned result.

### R172  (question 260, database `student_transcripts_tracking`)

- Returned by: kwai-autosql-14b/seed101
- Returned in cell: both A and D
- Class mass: 50/50
- Instances disagreeing: 22 of 55 (40%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the last name of the students who live in North Carolina but have not registered in any degree programs?

**Gold.**
```sql
SELECT T1.last_name FROM Students AS T1 JOIN Addresses AS T2 ON T1.current_address_id  =  T2.address_id WHERE T2.state_province_county  =  'NorthCarolina' EXCEPT SELECT DISTINCT T3.last_name FROM Students AS T3 JOIN Student_Enrolment AS T4 ON T3.student_id  =  T4.student_id
```

**Returned.**
```sql
SELECT DISTINCT T1.last_name
FROM Students AS T1
INNER JOIN Addresses AS T2 ON T1.current_address_id = T2.address_id
WHERE T2.state_province_county = 'North Carolina'
AND T1.student_id NOT IN (SELECT student_id FROM Student_Enrolment)
```

**First disagreeing instance** `student_transcripts_tracking.sqlite` (this is the shipped benchmark database).

Gold returns 2 row(s), 1 column(s):

    Gleichner
    Weimann

Returned query gives 0 row(s), None column(s):

    (no rows)

Difference: rep_empty; 0 row(s) in common, 2 only in the gold, 0 only in the returned result.

### R173  (question 268, database `student_transcripts_tracking`)

- Returned by: kwai-autosql-14b/seed101, kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 45/50, 46/50
- Instances disagreeing: 40 of 55 (73%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find the semester when both Master students and Bachelor students got enrolled in.

**Gold.**
```sql
SELECT DISTINCT T2.semester_id FROM Degree_Programs AS T1 JOIN Student_Enrolment AS T2 ON T1.degree_program_id  =  T2.degree_program_id WHERE degree_summary_name  =  'Master' INTERSECT SELECT DISTINCT T2.semester_id FROM Degree_Programs AS T1 JOIN Student_Enrolment AS T2 ON T1.degree_program_id  =  T2.degree_program_id WHERE degree_summary_name  =  'Bachelor'
```

**Returned.**
```sql
SELECT T3.semester_name
FROM Degree_Programs AS T1
INNER JOIN Student_Enrolment AS T2 ON T1.degree_program_id = T2.degree_program_id
INNER JOIN Semesters AS T3 ON T2.semester_id = T3.semester_id
WHERE T1.degree_summary_name = 'Master'
INTERSECT
SELECT T3.semester_name
FROM Degree_Programs AS T1
INNER JOIN Student_Enrolment AS T2 ON T1.degree_program_id = T2.degree_program_id
INNER JOIN Semesters AS T3 ON T2.semester_id = T3.semester_id
WHERE T1.degree_summary_name = 'Bachelor'
```

**First disagreeing instance** `student_transcripts_tracking.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    13

Returned query gives 1 row(s), 1 column(s):

    fall 2018

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R174  (question 309, database `tvshow`)

- Returned by: kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 41/50, 43/50, 41/50
- Instances disagreeing: 12 of 25 (48%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** which countries' tv channels are not playing any cartoon  Todd Casey writes?

**Gold.**
```sql
SELECT country FROM TV_Channel EXCEPT SELECT T1.country FROM TV_Channel AS T1 JOIN cartoon AS T2 ON T1.id = T2.Channel WHERE T2.written_by  =  'Todd Casey'
```

**Returned.**
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

**First disagreeing instance** `tvshow.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    Poland

Returned query gives 3 row(s), 1 column(s):

    Italy
    United Kingdom
    Poland

Difference: gold_subset_of_rep; 1 row(s) in common, 0 only in the gold, 2 only in the returned result.

### R175  (question 311, database `tvshow`)

- Returned by: kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 33/50, 39/50, 33/50
- Instances disagreeing: 25 of 25 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find the series name and country of the tv channel that is playing some cartoons  Ben Jones and Michael Chang directs?

**Gold.**
```sql
SELECT T1.series_name ,  T1.country FROM TV_Channel AS T1 JOIN cartoon AS T2 ON T1.id = T2.Channel WHERE T2.directed_by  =  'Michael Chang' INTERSECT SELECT T1.series_name ,  T1.country FROM TV_Channel AS T1 JOIN cartoon AS T2 ON T1.id = T2.Channel WHERE T2.directed_by  =  'Ben Jones'
```

**Returned.**
```sql
SELECT DISTINCT T1.series_name, T1.Country
FROM TV_Channel AS T1
INNER JOIN Cartoon AS T2 ON T1.id = T2.Channel
WHERE T2.Directed_by = 'Ben Jones' OR T2.Directed_by = 'Michael Chang'
```

**First disagreeing instance** `tvshow.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    MTV Dance | United Kingdom

Returned query gives 6 row(s), 2 column(s):

    Sky Radio | Italy
    Music Box Italia | Italy
    MTV Hits | Italy
    MTV Rocks | United Kingdom
    MTV Dance | United Kingdom
    Classica | Italy

Difference: gold_subset_of_rep; 1 row(s) in common, 0 only in the gold, 5 only in the returned result.

### R176  (question 312, database `tvshow`)

- Returned by: kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 31/50, 31/50, 28/50
- Instances disagreeing: 25 of 25 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the series name and country of all TV channels that are playing cartoons  Ben Jones and Michael Chang directs?

**Gold.**
```sql
SELECT T1.series_name ,  T1.country FROM TV_Channel AS T1 JOIN cartoon AS T2 ON T1.id = T2.Channel WHERE T2.directed_by  =  'Michael Chang' INTERSECT SELECT T1.series_name ,  T1.country FROM TV_Channel AS T1 JOIN cartoon AS T2 ON T1.id = T2.Channel WHERE T2.directed_by  =  'Ben Jones'
```

**Returned.**
```sql
SELECT DISTINCT T1.series_name, T1.Country
FROM TV_Channel AS T1
INNER JOIN Cartoon AS T2 ON T1.id = T2.Channel
WHERE T2.Directed_by = 'Ben Jones' OR T2.Directed_by = 'Michael Chang'
```

**First disagreeing instance** `tvshow.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    MTV Dance | United Kingdom

Returned query gives 6 row(s), 2 column(s):

    Sky Radio | Italy
    Music Box Italia | Italy
    MTV Hits | Italy
    MTV Rocks | United Kingdom
    MTV Dance | United Kingdom
    Classica | Italy

Difference: gold_subset_of_rep; 1 row(s) in common, 0 only in the gold, 5 only in the returned result.

### R177  (question 315, database `tvshow`)

- Returned by: kwai-autosql-14b/seed101
- Returned in cell: both A and D
- Class mass: 29/50
- Instances disagreeing: 25 of 25 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** find id of the tv channels that from the nations where have more than two tv channels.

**Gold.**
```sql
SELECT id FROM tv_channel GROUP BY country HAVING count(*)  >  2
```

**Returned.**
```sql
SELECT T1.id
FROM TV_Channel AS T1
INNER JOIN (
    SELECT Country
    FROM TV_Channel
    GROUP BY Country
    HAVING COUNT(id) > 2
) AS T2 ON T1.Country = T2.Country
```

**First disagreeing instance** `tvshow.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    700

Returned query gives 12 row(s), 1 column(s):

    700
    701
    703
    704
    705
    708
    713
    714
    715
    717
    719
    728

Difference: gold_subset_of_rep; 1 row(s) in common, 0 only in the gold, 11 only in the returned result.

### R178  (question 362, database `world_1`)

- Returned by: kwai-autosql-14b/seed101
- Returned in cell: both A and D
- Class mass: 18/50
- Instances disagreeing: 5 of 46 (11%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the average GNP and total population in all US territory nations?

**Gold.**
```sql
SELECT avg(GNP) ,  sum(population) FROM country WHERE GovernmentForm  =  "US Territory"
```

**Returned.**
```sql
SELECT AVG(GNP), SUM(Population)
FROM country
WHERE GovernmentForm LIKE 'Territory of the United States%'
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    510.3333333333333 | 329000

Returned query gives 1 row(s), 2 column(s):

    NULL | NULL

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R179  (question 363, database `world_1`)

- Returned by: kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 17/50, 19/49, 27/50
- Instances disagreeing: 5 of 46 (11%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Give the mean GNP and total population of nations which are considered US territory.

**Gold.**
```sql
SELECT avg(GNP) ,  sum(population) FROM country WHERE GovernmentForm  =  "US Territory"
```

**Returned.**
```sql
SELECT AVG(GNP), SUM(Population)
FROM country
WHERE GovernmentForm LIKE '%United States%'
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    510.3333333333333 | 329000

Returned query gives 1 row(s), 2 column(s):

    NULL | NULL

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R180  (question 369, database `world_1`)

- Returned by: kwai-autosql-14b/seed101, kwai-autosql-14b/seed303
- Returned in cell: D only
- Class mass: 31/50, 29/50
- Instances disagreeing: 3 of 46 (7%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** How many official languages are spoken in Afghanistan?

**Gold.**
```sql
SELECT COUNT(*) FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code  =  T2.CountryCode WHERE T1.Name  =  "Afghanistan" AND IsOfficial  =  "T"
```

**Returned.**
```sql
SELECT COUNT(Language)
FROM countrylanguage
WHERE CountryCode = 'AFG' AND IsOfficial = 'T'
```

**First disagreeing instance** `world_1v50811.sqlite`.

Gold returns 1 row(s), 1 column(s):

    1

Returned query gives 1 row(s), 1 column(s):

    0

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R181  (question 391, database `world_1`)

- Returned by: kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 30/50, 34/50, 37/50
- Instances disagreeing: 46 of 46 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Give the mean life expectancy of countries in which English is not officially spoken .

**Gold.**
```sql
SELECT avg(LifeExpectancy) FROM country WHERE Name NOT IN (SELECT T1.Name FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code  =  T2.CountryCode WHERE T2.Language  =  "English" AND T2.IsOfficial  =  "T")
```

**Returned.**
```sql
SELECT AVG(T1.LifeExpectancy)
FROM country AS T1
INNER JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode
WHERE T2.Language = 'English' AND T2.IsOfficial = 'F'
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    65.4827027027027

Returned query gives 1 row(s), 1 column(s):

    74.95

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R182  (question 392, database `world_1`)

- Returned by: kwai-autosql-14b/seed101
- Returned in cell: A only
- Class mass: 27/50
- Instances disagreeing: 46 of 46 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the total number of people living in the nations that do not use English?

**Gold.**
```sql
SELECT sum(Population) FROM country WHERE Name NOT IN (SELECT T1.Name FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code  =  T2.CountryCode WHERE T2.Language  =  "English")
```

**Returned.**
```sql
SELECT SUM(T1.Population)
FROM country AS T1
INNER JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode
WHERE T2.Language != 'English'
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    5451331150

Returned query gives 1 row(s), 1 column(s):

    52858768750

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R183  (question 399, database `world_1`)

- Returned by: kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 24/50, 26/50, 23/50
- Instances disagreeing: 37 of 46 (80%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Which countries larger than that of any country in Europe by land?

**Gold.**
```sql
SELECT Name FROM country WHERE SurfaceArea  >  (SELECT min(SurfaceArea) FROM country WHERE Continent  =  "Europe")
```

**Returned.**
```sql
SELECT Name
FROM country
WHERE SurfaceArea > (SELECT MAX(SurfaceArea) FROM country WHERE Continent = 'Europe')
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 238 row(s), 1 column(s):

    Aruba
    Afghanistan
    Angola
    Anguilla
    Albania
    Andorra
    Netherlands Antilles
    United Arab Emirates
    Argentina
    Armenia
    American Samoa
    Antarctica
    ... (238 rows total)

Returned query gives 0 row(s), None column(s):

    (no rows)

Difference: rep_empty; 0 row(s) in common, 238 only in the gold, 0 only in the returned result.

### R184  (question 400, database `world_1`)

- Returned by: kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303, omnisql-32b/seed101, omnisql-32b/seed202, omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 35/50, 37/50, 37/50, 47/50, 47/50, 42/50
- Instances disagreeing: 28 of 46 (61%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the African countries that have less people than any country in Asia?

**Gold.**
```sql
SELECT Name FROM country WHERE Continent  =  "Africa"  AND population  <  (SELECT max(population) FROM country WHERE Continent  =  "Asia")
```

**Returned.**
```sql
SELECT Name
FROM country
WHERE Continent = 'Africa'
  AND Population < (SELECT MIN(Population) FROM country WHERE Continent = 'Asia')
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 58 row(s), 1 column(s):

    Angola
    Burundi
    Benin
    Burkina Faso
    Botswana
    Central African Republic
    Côte d’Ivoire
    Cameroon
    Congo, The Democratic Republic of the
    Congo
    Comoros
    Cape Verde
    ... (58 rows total)

Returned query gives 5 row(s), 1 column(s):

    British Indian Ocean Territory
    Mayotte
    Saint Helena
    Sao Tome and Principe
    Seychelles

Difference: rep_subset_of_gold; 5 row(s) in common, 53 only in the gold, 0 only in the returned result.

### R185  (question 403, database `world_1`)

- Returned by: kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 27/50, 31/50, 31/50
- Instances disagreeing: 29 of 46 (63%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the Asian countries have more people than that of any country in Africa?

**Gold.**
```sql
SELECT Name FROM country WHERE Continent  =  "Asia"  AND population  >  (SELECT min(population) FROM country WHERE Continent  =  "Africa")
```

**Returned.**
```sql
SELECT Name
FROM country
WHERE Continent = 'Asia'
  AND Population > (SELECT MAX(Population) FROM country WHERE Continent = 'Africa')
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 51 row(s), 1 column(s):

    Afghanistan
    United Arab Emirates
    Armenia
    Azerbaijan
    Bangladesh
    Bahrain
    Brunei
    Bhutan
    China
    Cyprus
    Georgia
    Hong Kong
    ... (51 rows total)

Returned query gives 6 row(s), 1 column(s):

    Bangladesh
    China
    Indonesia
    India
    Japan
    Pakistan

Difference: rep_subset_of_gold; 6 row(s) in common, 45 only in the gold, 0 only in the returned result.

### R186  (question 405, database `world_1`)

- Returned by: kwai-autosql-14b/seed101, kwai-autosql-14b/seed202
- Returned in cell: both A and D
- Class mass: 24/50, 25/50
- Instances disagreeing: 32 of 46 (70%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Return the country codes for countries that do not speak English.

**Gold.**
```sql
SELECT CountryCode FROM countrylanguage EXCEPT SELECT CountryCode FROM countrylanguage WHERE LANGUAGE  =  "English"
```

**Returned.**
```sql
SELECT Code
FROM country
WHERE Code NOT IN (
  SELECT CountryCode
  FROM countrylanguage
  WHERE Language = 'English'
)
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 173 row(s), 1 column(s):

    AFG
    AGO
    ALB
    AND
    ARE
    ARG
    ARM
    AUT
    AZE
    BDI
    BEL
    BEN
    ... (173 rows total)

Returned query gives 179 row(s), 1 column(s):

    AFG
    AGO
    ALB
    AND
    ARE
    ARG
    ARM
    ATA
    ATF
    AUT
    AZE
    BDI
    ... (179 rows total)

Difference: gold_subset_of_rep; 173 row(s) in common, 0 only in the gold, 6 only in the returned result.

### R187  (question 410, database `world_1`)

- Returned by: kwai-autosql-14b/seed101
- Returned in cell: both A and D
- Class mass: 29/50
- Instances disagreeing: 9 of 46 (20%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Which cities are in European countries where English is not spoken officially?

**Gold.**
```sql
SELECT DISTINCT T2.Name FROM country AS T1 JOIN city AS T2 ON T2.CountryCode  =  T1.Code WHERE T1.Continent  =  'Europe' AND T1.Name NOT IN (SELECT T3.Name FROM country AS T3 JOIN countrylanguage AS T4 ON T3.Code  =  T4.CountryCode WHERE T4.IsOfficial  =  'T' AND T4.Language  =  'English')
```

**Returned.**
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

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 753 row(s), 1 column(s):

    Amsterdam
    Rotterdam
    Haag
    Utrecht
    Eindhoven
    Tilburg
    Groningen
    Breda
    Apeldoorn
    Nijmegen
    Enschede
    Haarlem
    ... (753 rows total)

Returned query gives 755 row(s), 1 column(s):

    Tirana
    Andorra la Vella
    Wien
    Graz
    Linz
    Salzburg
    Innsbruck
    Klagenfurt
    Antwerpen
    Gent
    Charleroi
    Liège
    ... (755 rows total)

Difference: duplicate_multiplicity_only; 753 row(s) in common, 0 only in the gold, 0 only in the returned result.

### R188  (question 411, database `world_1`)

- Returned by: kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 50/50, 50/50, 50/50
- Instances disagreeing: 1 of 46 (2%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Whic`h unique cities are in  Asian countries where Chinese is the official ?

**Gold.**
```sql
select distinct t3.name from country as t1 join countrylanguage as t2 on t1.code  =  t2.countrycode join city as t3 on t1.code  =  t3.countrycode where t2.isofficial  =  't' and t2.language  =  'chinese' and t1.continent  =  "asia"
```

**Returned.**
```sql
SELECT DISTINCT T3.Name
FROM country AS T1
INNER JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode
INNER JOIN city AS T3 ON T1.Code = T3.CountryCode
WHERE T1.Continent = 'Asia'
  AND T2.Language = 'Chinese'
  AND T2.IsOfficial = 'T'
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 0 row(s), None column(s):

    (no rows)

Returned query gives 359 row(s), 1 column(s):

    Shanghai
    Peking
    Chongqing
    Tianjin
    Wuhan
    Harbin
    Shenyang
    Kanton [Guangzhou]
    Chengdu
    Nanking [Nanjing]
    Changchun
    Xi´an
    ... (359 rows total)

Difference: gold_empty; 0 row(s) in common, 0 only in the gold, 359 only in the returned result.

### R189  (question 427, database `world_1`)

- Returned by: kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 44/50, 49/50, 46/50
- Instances disagreeing: 40 of 46 (87%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the total population and average area of countries in North America who is bigger than 3000 square miles

**Gold.**
```sql
select sum(population) ,  avg(surfacearea) from country where continent  =  "north america" and surfacearea  >  3000
```

**Returned.**
```sql
SELECT SUM(Population), AVG(SurfaceArea)
FROM country
WHERE Continent = 'North America' AND SurfaceArea > 3000
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    NULL | NULL

Returned query gives 1 row(s), 2 column(s):

    480753000 | 1344763.7222222222

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R190  (question 428, database `world_1`)

- Returned by: kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 29/50, 27/50, 29/50
- Instances disagreeing: 40 of 46 (87%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Give the total population and average  corresponding to countries in Noth America that is bigger than 3000 square miles.

**Gold.**
```sql
select sum(population) ,  avg(surfacearea) from country where continent  =  "north america" and surfacearea  >  3000
```

**Returned.**
```sql
SELECT SUM(Population), AVG(LifeExpectancy)
FROM country
WHERE Continent = 'North America' AND SurfaceArea > 3000
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    NULL | NULL

Returned query gives 1 row(s), 2 column(s):

    480753000 | 71.18333333333334

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R191  (question 431, database `world_1`)

- Returned by: kwai-autosql-14b/seed101
- Returned in cell: both A and D
- Class mass: 12/50
- Instances disagreeing: 46 of 46 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the language spoken by the largest percentage of people in each nation?

**Gold.**
```sql
SELECT LANGUAGE ,  CountryCode ,  max(Percentage) FROM countrylanguage GROUP BY CountryCode
```

**Returned.**
```sql
SELECT T1.Language
FROM countrylanguage T1
INNER JOIN (
    SELECT CountryCode, MAX(Percentage) AS max_percentage
    FROM countrylanguage
    GROUP BY CountryCode
) T2 ON T1.CountryCode = T2.CountryCode AND T1.Percentage = T2.max_percentage
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 233 row(s), 3 column(s):

    Papiamento | ABW | 76.7
    Pashto | AFG | 52.4
    Ovimbundu | AGO | 37.2
    English | AIA | 0.0
    Albaniana | ALB | 97.9
    Spanish | AND | 44.6
    Papiamento | ANT | 86.2
    Arabic | ARE | 42.0
    Spanish | ARG | 96.8
    Armenian | ARM | 93.4
    Samoan | ASM | 90.6
    Creole English | ATG | 95.7
    ... (233 rows total)

Returned query gives 241 row(s), 1 column(s):

    Papiamento
    Pashto
    Ovimbundu
    English
    Albaniana
    Spanish
    Papiamento
    Arabic
    Spanish
    Armenian
    Samoan
    Creole English
    ... (241 rows total)

Difference: col_count_differs, disjoint; 0 row(s) in common, 233 only in the gold, 136 only in the returned result.

### R192  (question 432, database `world_1`)

- Returned by: kwai-autosql-14b/seed101, kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 18/50, 20/50
- Instances disagreeing: 46 of 46 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the codes of the different nations, and what are the languages spoken by the greatest percentage of people for each?

**Gold.**
```sql
SELECT LANGUAGE ,  CountryCode ,  max(Percentage) FROM countrylanguage GROUP BY CountryCode
```

**Returned.**
```sql
SELECT CountryCode, Language
FROM countrylanguage
WHERE (CountryCode, Percentage) IN (
  SELECT CountryCode, MAX(Percentage)
  FROM countrylanguage
  GROUP BY CountryCode
)
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 233 row(s), 3 column(s):

    Papiamento | ABW | 76.7
    Pashto | AFG | 52.4
    Ovimbundu | AGO | 37.2
    English | AIA | 0.0
    Albaniana | ALB | 97.9
    Spanish | AND | 44.6
    Papiamento | ANT | 86.2
    Arabic | ARE | 42.0
    Spanish | ARG | 96.8
    Armenian | ARM | 93.4
    Samoan | ASM | 90.6
    Creole English | ATG | 95.7
    ... (233 rows total)

Returned query gives 241 row(s), 2 column(s):

    ABW | Papiamento
    AFG | Pashto
    AGO | Ovimbundu
    AIA | English
    ALB | Albaniana
    AND | Spanish
    ANT | Papiamento
    ARE | Arabic
    ARG | Spanish
    ARM | Armenian
    ASM | Samoan
    ATG | Creole English
    ... (241 rows total)

Difference: col_count_differs, disjoint; 0 row(s) in common, 233 only in the gold, 241 only in the returned result.

### R193  (question 433, database `world_1`)

- Returned by: kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 31/50, 34/50, 32/50
- Instances disagreeing: 46 of 46 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the total number of countries where Spanish is spoken by the largest percentage of people?

**Gold.**
```sql
SELECT count(*) ,   max(Percentage) FROM countrylanguage WHERE LANGUAGE  =  "Spanish" GROUP BY CountryCode
```

**Returned.**
```sql
SELECT COUNT(*)
FROM countrylanguage
WHERE Language = 'Spanish'
ORDER BY Percentage DESC
LIMIT 1
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 28 row(s), 2 column(s):

    1 | 7.4
    1 | 44.6
    1 | 96.8
    1 | 31.6
    1 | 87.7
    1 | 0.7
    1 | 89.7
    1 | 99.0
    1 | 97.5
    1 | 100.0
    1 | 98.0
    1 | 93.0
    ... (28 rows total)

Returned query gives 1 row(s), 1 column(s):

    28

Difference: col_count_differs, disjoint; 0 row(s) in common, 27 only in the gold, 1 only in the returned result.

### R194  (question 434, database `world_1`)

- Returned by: kwai-autosql-14b/seed101
- Returned in cell: both A and D
- Class mass: 25/50
- Instances disagreeing: 46 of 46 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Count the number of countries for which Spanish is predominantly spoken .

**Gold.**
```sql
SELECT count(*) ,   max(Percentage) FROM countrylanguage WHERE LANGUAGE  =  "Spanish" GROUP BY CountryCode
```

**Returned.**
```sql
SELECT COUNT(CountryCode)
FROM countrylanguage
WHERE Language = 'Spanish' AND IsOfficial = 'T'
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 28 row(s), 2 column(s):

    1 | 7.4
    1 | 44.6
    1 | 96.8
    1 | 31.6
    1 | 87.7
    1 | 0.7
    1 | 89.7
    1 | 99.0
    1 | 97.5
    1 | 100.0
    1 | 98.0
    1 | 93.0
    ... (28 rows total)

Returned query gives 1 row(s), 1 column(s):

    20

Difference: col_count_differs, disjoint; 0 row(s) in common, 27 only in the gold, 1 only in the returned result.

### R195  (question 461, database `network_1`)

- Returned by: kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 41/50, 37/50, 39/50
- Instances disagreeing: 27 of 29 (93%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find the average grade of all students who have some friends.

**Gold.**
```sql
SELECT avg(grade) FROM Highschooler WHERE id IN (SELECT T1.student_id FROM Friend AS T1 JOIN Highschooler AS T2 ON T1.student_id  =  T2.id)
```

**Returned.**
```sql
SELECT AVG(H.grade)
FROM Highschooler H
INNER JOIN Friend F ON H.ID = F.student_id
```

**First disagreeing instance** `network_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    10.428571428571429

Returned query gives 1 row(s), 1 column(s):

    10.25

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R196  (question 462, database `network_1`)

- Returned by: kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 44/50, 46/50, 48/50
- Instances disagreeing: 27 of 29 (93%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the average grade of students who have friends?

**Gold.**
```sql
SELECT avg(grade) FROM Highschooler WHERE id IN (SELECT T1.student_id FROM Friend AS T1 JOIN Highschooler AS T2 ON T1.student_id  =  T2.id)
```

**Returned.**
```sql
SELECT AVG(H.grade)
FROM Highschooler H
INNER JOIN Friend F ON H.ID = F.student_id
```

**First disagreeing instance** `network_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    10.428571428571429

Returned query gives 1 row(s), 1 column(s):

    10.25

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R197  (question 474, database `dog_kennels`)

- Returned by: kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 33/49, 32/50, 26/50
- Instances disagreeing: 45 of 48 (94%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Who has paid the largest amount of money in total for their dogs? Show the id and zip code.

**Gold.**
```sql
SELECT T1.owner_id ,  T1.zip_code FROM Owners AS T1 JOIN Dogs AS T2 ON T1.owner_id  =  T2.owner_id JOIN Treatments AS T3 ON T2.dog_id  =  T3.dog_id GROUP BY T1.owner_id ORDER BY sum(T3.cost_of_treatment) DESC LIMIT 1
```

**Returned.**
```sql
SELECT T1.owner_id, T1.zip_code
FROM Owners AS T1
INNER JOIN Dogs AS T2 ON T1.owner_id = T2.owner_id
INNER JOIN Charges AS T3 ON T2.dog_id = T3.charge_id
GROUP BY T1.owner_id, T1.zip_code
ORDER BY SUM(T3.charge_amount) DESC
LIMIT 1
```

**First disagreeing instance** `dog_kennels.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    3 | 02647

Returned query gives 1 row(s), 2 column(s):

    1 | 93165

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R198  (question 475, database `dog_kennels`)

- Returned by: kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 24/49, 25/50, 20/50
- Instances disagreeing: 45 of 48 (94%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Find the id and zip code of the person who spent the most money in total for his or her dogs.

**Gold.**
```sql
SELECT T1.owner_id ,  T1.zip_code FROM Owners AS T1 JOIN Dogs AS T2 ON T1.owner_id  =  T2.owner_id JOIN Treatments AS T3 ON T2.dog_id  =  T3.dog_id GROUP BY T1.owner_id ORDER BY sum(T3.cost_of_treatment) DESC LIMIT 1
```

**Returned.**
```sql
SELECT T1.owner_id, T1.zip_code
FROM Owners AS T1
INNER JOIN Dogs AS T2 ON T1.owner_id = T2.owner_id
INNER JOIN Charges AS T3 ON T2.dog_id = T3.charge_id
GROUP BY T1.owner_id, T1.zip_code
ORDER BY SUM(T3.charge_amount) DESC
LIMIT 1
```

**First disagreeing instance** `dog_kennels.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    3 | 02647

Returned query gives 1 row(s), 2 column(s):

    1 | 93165

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R199  (question 476, database `dog_kennels`)

- Returned by: kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 49/50, 49/50, 49/50
- Instances disagreeing: 40 of 48 (83%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the first name and last name of the professionals who have done treatment cheaper than average?

**Gold.**
```sql
SELECT DISTINCT T1.first_name ,  T1.last_name FROM Professionals AS T1 JOIN Treatments AS T2 WHERE cost_of_treatment  <  ( SELECT avg(cost_of_treatment) FROM Treatments )
```

**Returned.**
```sql
SELECT DISTINCT P.first_name, P.last_name
FROM Professionals P
INNER JOIN Treatments T ON P.professional_id = T.professional_id
WHERE T.cost_of_treatment < (SELECT AVG(cost_of_treatment) FROM Treatments)
```

**First disagreeing instance** `dog_kennels.sqlite` (this is the shipped benchmark database).

Gold returns 15 row(s), 2 column(s):

    Taryn | Braun
    Jayson | Ullrich
    Olaf | Watsica
    Vernice | Tillman
    Danny | Considine
    Ruben | O'Reilly
    Velva | Hayes
    Karley | Hyatt
    Monte | Kshlerin
    Domenica | Jacobs
    Brady | Pouros
    Winfield | Christiansen
    ... (15 rows total)

Returned query gives 5 row(s), 2 column(s):

    Domenica | Jacobs
    Vernice | Tillman
    Karley | Hyatt
    Ruben | O'Reilly
    Monte | Kshlerin

Difference: rep_subset_of_gold; 5 row(s) in common, 10 only in the gold, 0 only in the returned result.

### R200  (question 477, database `dog_kennels`)

- Returned by: kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 49/50, 50/50, 49/50
- Instances disagreeing: 40 of 48 (83%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Which professionals have operated a treatment that is less expansive than the average? Give me theor first names and last names.

**Gold.**
```sql
SELECT DISTINCT T1.first_name ,  T1.last_name FROM Professionals AS T1 JOIN Treatments AS T2 WHERE cost_of_treatment  <  ( SELECT avg(cost_of_treatment) FROM Treatments )
```

**Returned.**
```sql
SELECT DISTINCT P.first_name, P.last_name
FROM Professionals P
INNER JOIN Treatments T ON P.professional_id = T.professional_id
WHERE T.cost_of_treatment < (SELECT AVG(cost_of_treatment) FROM Treatments)
```

**First disagreeing instance** `dog_kennels.sqlite` (this is the shipped benchmark database).

Gold returns 15 row(s), 2 column(s):

    Taryn | Braun
    Jayson | Ullrich
    Olaf | Watsica
    Vernice | Tillman
    Danny | Considine
    Ruben | O'Reilly
    Velva | Hayes
    Karley | Hyatt
    Monte | Kshlerin
    Domenica | Jacobs
    Brady | Pouros
    Winfield | Christiansen
    ... (15 rows total)

Returned query gives 5 row(s), 2 column(s):

    Domenica | Jacobs
    Vernice | Tillman
    Karley | Hyatt
    Ruben | O'Reilly
    Monte | Kshlerin

Difference: rep_subset_of_gold; 5 row(s) in common, 10 only in the gold, 0 only in the returned result.

### R201  (question 46, database `pets_1`)

- Returned by: kwai-autosql-14b/seed202
- Returned in cell: both A and D
- Class mass: 26/50
- Instances disagreeing: 16 of 27 (59%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What major is every student who does not own a cat, and also how old are they?

**Gold.**
```sql
SELECT major ,  age FROM student WHERE stuid NOT IN (SELECT T1.stuid FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid  =  T2.stuid JOIN pets AS T3 ON T3.petid  =  T2.petid WHERE T3.pettype  =  'cat')
```

**Returned.**
```sql
SELECT DISTINCT S.Major, S.Age
FROM Student S
WHERE S.StuID NOT IN (
    SELECT HP.StuID
    FROM Has_Pet HP
    INNER JOIN Pets P ON HP.PetID = P.PetID
    WHERE P.PetType = 'cat'
)
```

**First disagreeing instance** `pets_1.sqlite` (this is the shipped benchmark database).

Gold returns 33 row(s), 2 column(s):

    600 | 19
    600 | 21
    600 | 20
    600 | 26
    600 | 18
    600 | 18
    600 | 20
    600 | 19
    600 | 17
    600 | 22
    600 | 20
    600 | 18
    ... (33 rows total)

Returned query gives 21 row(s), 2 column(s):

    600 | 19
    600 | 21
    600 | 20
    600 | 26
    600 | 18
    600 | 17
    600 | 22
    600 | 16
    600 | 27
    520 | 22
    520 | 19
    540 | 17
    ... (21 rows total)

Difference: duplicate_multiplicity_only; 21 row(s) in common, 0 only in the gold, 0 only in the returned result.

### R202  (question 49, database `pets_1`)

- Returned by: kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 43/50, 48/50
- Instances disagreeing: 20 of 27 (74%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find the first name and age of students who have a dog but do not have a cat.

**Gold.**
```sql
SELECT T1.fname ,  T1.age FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid  =  T2.stuid JOIN pets AS T3 ON T3.petid  =  T2.petid WHERE T3.pettype  =  'dog' AND T1.stuid NOT IN (SELECT T1.stuid FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid  =  T2.stuid JOIN pets AS T3 ON T3.petid  =  T2.petid WHERE T3.pettype  =  'cat')
```

**Returned.**
```sql
SELECT DISTINCT S.Fname, S.Age
FROM Student S
INNER JOIN Has_Pet HP ON S.StuID = HP.StuID
INNER JOIN Pets P ON HP.PetID = P.PetID
WHERE P.PetType = 'dog'
AND S.StuID NOT IN (
    SELECT HP2.StuID
    FROM Has_Pet HP2
    INNER JOIN Pets P2 ON HP2.PetID = P2.PetID
    WHERE P2.PetType = 'cat'
)
```

**First disagreeing instance** `pets_1.sqlite` (this is the shipped benchmark database).

Gold returns 2 row(s), 2 column(s):

    Tracy | 19
    Tracy | 19

Returned query gives 1 row(s), 2 column(s):

    Tracy | 19

Difference: duplicate_multiplicity_only; 1 row(s) in common, 0 only in the gold, 0 only in the returned result.

### R203  (question 50, database `pets_1`)

- Returned by: kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 48/50, 49/50
- Instances disagreeing: 25 of 27 (93%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the first name of every student who has a dog but does not have a cat?

**Gold.**
```sql
SELECT T1.fname ,  T1.age FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid  =  T2.stuid JOIN pets AS T3 ON T3.petid  =  T2.petid WHERE T3.pettype  =  'dog' AND T1.stuid NOT IN (SELECT T1.stuid FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid  =  T2.stuid JOIN pets AS T3 ON T3.petid  =  T2.petid WHERE T3.pettype  =  'cat')
```

**Returned.**
```sql
SELECT DISTINCT S.Fname
FROM Student S
INNER JOIN Has_Pet HP ON S.StuID = HP.StuID
INNER JOIN Pets P ON HP.PetID = P.PetID
WHERE P.PetType = 'dog'
AND S.StuID NOT IN (
    SELECT HP2.StuID
    FROM Has_Pet HP2
    INNER JOIN Pets P2 ON HP2.PetID = P2.PetID
    WHERE P2.PetType = 'cat'
)
```

**First disagreeing instance** `pets_1.sqlite` (this is the shipped benchmark database).

Gold returns 2 row(s), 2 column(s):

    Tracy | 19
    Tracy | 19

Returned query gives 1 row(s), 1 column(s):

    Tracy

Difference: col_count_differs, disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R204  (question 63, database `car_1`)

- Returned by: kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Returned in cell: A only
- Class mass: 18/50, 22/50
- Instances disagreeing: 41 of 60 (68%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find the name of the makers that produced some cars in 1970?

**Gold.**
```sql
SELECT DISTINCT T1.Maker FROM CAR_MAKERS AS T1 JOIN MODEL_LIST AS T2 ON T1.Id  =  T2.Maker JOIN CAR_NAMES AS T3 ON T2.model  =  T3.model JOIN CARS_DATA AS T4 ON T3.MakeId  =  T4.id WHERE T4.year  =  '1970';
```

**Returned.**
```sql
SELECT DISTINCT T3.FullName
FROM cars_data AS T1
INNER JOIN car_names AS T2 ON T1.Id = T2.MakeId
INNER JOIN car_makers AS T3 ON T2.Make = T3.Maker
WHERE T1.Year = 1970
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 11 row(s), 1 column(s):

    gm
    chrysler
    amc
    ford
    citroen
    toyota
    nissan
    volkswagen
    peugeaut
    saab
    bmw

Returned query gives 0 row(s), None column(s):

    (no rows)

Difference: rep_empty; 0 row(s) in common, 11 only in the gold, 0 only in the returned result.

### R205  (question 65, database `car_1`)

- Returned by: kwai-autosql-14b/seed202
- Returned in cell: A only
- Class mass: 14/50
- Instances disagreeing: 58 of 60 (97%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find the make and production time of the cars that were produced in the earliest ?

**Gold.**
```sql
SELECT T2.Make ,  T1.Year FROM CARS_DATA AS T1 JOIN CAR_NAMES AS T2 ON T1.Id  =  T2.MakeId WHERE T1.Year  =  (SELECT min(YEAR) FROM CARS_DATA);
```

**Returned.**
```sql
SELECT T1.FullName, T3.Year
FROM car_makers AS T1
INNER JOIN car_names AS T2 ON T1.Id = T2.Make
INNER JOIN cars_data AS T3 ON T2.MakeId = T3.Id
ORDER BY T3.Year ASC
LIMIT 1
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 35 row(s), 2 column(s):

    chevrolet chevelle malibu | 1970
    buick skylark 320 | 1970
    plymouth satellite | 1970
    amc rebel sst | 1970
    ford torino | 1970
    ford galaxie 500 | 1970
    chevrolet impala | 1970
    plymouth fury iii | 1970
    pontiac catalina | 1970
    amc ambassador dpl | 1970
    citroen ds-21 pallas | 1970
    chevrolet chevelle concours (sw) | 1970
    ... (35 rows total)

Returned query gives 0 row(s), None column(s):

    (no rows)

Difference: rep_empty; 0 row(s) in common, 35 only in the gold, 0 only in the returned result.

### R206  (question 66, database `car_1`)

- Returned by: kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Returned in cell: A only
- Class mass: 15/50, 13/50
- Instances disagreeing: 59 of 60 (98%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the maker of the carr produced in the earliest  and what  year was it?

**Gold.**
```sql
SELECT T2.Make ,  T1.Year FROM CARS_DATA AS T1 JOIN CAR_NAMES AS T2 ON T1.Id  =  T2.MakeId WHERE T1.Year  =  (SELECT min(YEAR) FROM CARS_DATA);
```

**Returned.**
```sql
SELECT T3.Maker, T1.Year
FROM cars_data AS T1
INNER JOIN car_names AS T2 ON T1.Id = T2.MakeId
INNER JOIN car_makers AS T3 ON T2.Make = T3.FullName
ORDER BY T1.Year ASC
LIMIT 1
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 35 row(s), 2 column(s):

    chevrolet chevelle malibu | 1970
    buick skylark 320 | 1970
    plymouth satellite | 1970
    amc rebel sst | 1970
    ford torino | 1970
    ford galaxie 500 | 1970
    chevrolet impala | 1970
    plymouth fury iii | 1970
    pontiac catalina | 1970
    amc ambassador dpl | 1970
    citroen ds-21 pallas | 1970
    chevrolet chevelle concours (sw) | 1970
    ... (35 rows total)

Returned query gives 0 row(s), None column(s):

    (no rows)

Difference: rep_empty; 0 row(s) in common, 35 only in the gold, 0 only in the returned result.

### R207  (question 66, database `car_1`)

- Returned by: kwai-autosql-14b/seed202
- Returned in cell: D only
- Class mass: 11/50
- Instances disagreeing: 35 of 60 (58%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the maker of the carr produced in the earliest  and what  year was it?

**Gold.**
```sql
SELECT T2.Make ,  T1.Year FROM CARS_DATA AS T1 JOIN CAR_NAMES AS T2 ON T1.Id  =  T2.MakeId WHERE T1.Year  =  (SELECT min(YEAR) FROM CARS_DATA);
```

**Returned.**
```sql
SELECT T3.Maker, T1.Year
FROM cars_data AS T1
INNER JOIN car_names AS T2 ON T1.Id = T2.MakeId
INNER JOIN car_makers AS T3 ON T2.Make = T3.Maker
ORDER BY T1.Year ASC
LIMIT 1
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 35 row(s), 2 column(s):

    chevrolet chevelle malibu | 1970
    buick skylark 320 | 1970
    plymouth satellite | 1970
    amc rebel sst | 1970
    ford torino | 1970
    ford galaxie 500 | 1970
    chevrolet impala | 1970
    plymouth fury iii | 1970
    pontiac catalina | 1970
    amc ambassador dpl | 1970
    citroen ds-21 pallas | 1970
    chevrolet chevelle concours (sw) | 1970
    ... (35 rows total)

Returned query gives 1 row(s), 2 column(s):

    subaru | 1974

Difference: disjoint; 0 row(s) in common, 35 only in the gold, 1 only in the returned result.

### R208  (question 77, database `car_1`)

- Returned by: kwai-autosql-14b/seed202
- Returned in cell: both A and D
- Class mass: 26/50
- Instances disagreeing: 31 of 60 (52%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the count of the car models produced in the United States?

**Gold.**
```sql
SELECT count(*) FROM MODEL_LIST AS T1 JOIN CAR_MAKERS AS T2 ON T1.Maker  =  T2.Id JOIN COUNTRIES AS T3 ON T2.Country  =  T3.CountryId WHERE T3.CountryName  =  'usa';
```

**Returned.**
```sql
SELECT COUNT(T3.Model)
FROM car_makers AS T1
INNER JOIN countries AS T2 ON T1.Country = T2.CountryId
INNER JOIN car_names AS T3 ON T1.Id = T3.MakeId
WHERE T2.CountryName = 'usa'
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    13

Returned query gives 1 row(s), 1 column(s):

    4

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R209  (question 90, database `car_1`)

- Returned by: kwai-autosql-14b/seed202
- Returned in cell: A only
- Class mass: 17/50
- Instances disagreeing: 16 of 60 (27%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the average edispl of the cars of  volvo?

**Gold.**
```sql
SELECT avg(T2.edispl) FROM CAR_NAMES AS T1 JOIN CARS_DATA AS T2 ON T1.MakeId  =  T2.Id WHERE T1.Model  =  'volvo';
```

**Returned.**
```sql
SELECT AVG(T3.Edispl)
FROM car_makers AS T1
INNER JOIN car_names AS T2 ON T1.Id = T2.Make
INNER JOIN cars_data AS T3 ON T2.MakeId = T3.Id
WHERE T1.Maker = 'volvo'
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    133.5

Returned query gives 1 row(s), 1 column(s):

    NULL

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R210  (question 91, database `car_1`)

- Returned by: kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Returned in cell: A only
- Class mass: 19/50, 16/50
- Instances disagreeing: 16 of 60 (27%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the average edispl for all volvos?

**Gold.**
```sql
SELECT avg(T2.edispl) FROM CAR_NAMES AS T1 JOIN CARS_DATA AS T2 ON T1.MakeId  =  T2.Id WHERE T1.Model  =  'volvo';
```

**Returned.**
```sql
SELECT AVG(T3.Edispl)
FROM car_makers AS T1
INNER JOIN car_names AS T2 ON T1.Id = T2.Make
INNER JOIN cars_data AS T3 ON T2.MakeId = T3.Id
WHERE T1.Maker = 'volvo'
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    133.5

Returned query gives 1 row(s), 1 column(s):

    NULL

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R211  (question 100, database `car_1`)

- Returned by: kwai-autosql-14b/seed202
- Returned in cell: A only
- Class mass: 15/50
- Instances disagreeing: 20 of 60 (33%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the different models created by either General Motors or over 3500 lbs?

**Gold.**
```sql
SELECT DISTINCT T2.Model FROM CAR_NAMES AS T1 JOIN MODEL_LIST AS T2 ON T1.Model  =  T2.Model JOIN CAR_MAKERS AS T3 ON T2.Maker  =  T3.Id JOIN CARS_DATA AS T4 ON T1.MakeId  =  T4.Id WHERE T3.FullName  =  'General Motors' OR T4.weight  >  3500;
```

**Returned.**
```sql
SELECT DISTINCT T3.Model
FROM car_makers AS T1
INNER JOIN car_names AS T3 ON T1.Id = T3.Make
INNER JOIN cars_data AS T2 ON T3.MakeId = T2.Id
WHERE T1.FullName = 'General Motors'
UNION
SELECT DISTINCT T3.Model
FROM car_names AS T3
INNER JOIN cars_data AS T2 ON T3.MakeId = T2.Id
WHERE T2.Weight > 3500
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 13 row(s), 1 column(s):

    chevrolet
    buick
    ford
    plymouth
    pontiac
    amc
    dodge
    mercury
    oldsmobile
    chrysler
    mercedes-benz
    cadillac
    ... (13 rows total)

Returned query gives 14 row(s), 1 column(s):

    amc
    buick
    cadillac
    chevrolet
    chrysler
    dodge
    ford
    hi
    mercedes
    mercedes-benz
    mercury
    oldsmobile
    ... (14 rows total)

Difference: gold_subset_of_rep; 13 row(s) in common, 0 only in the gold, 1 only in the returned result.

### R212  (question 105, database `car_1`)

- Returned by: kwai-autosql-14b/seed202
- Returned in cell: D only
- Class mass: 16/50
- Instances disagreeing: 56 of 60 (93%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** How many nations has more than 2 car makers ?

**Gold.**
```sql
select count(*) from countries as t1 join car_makers as t2 on t1.countryid  =  t2.country group by t1.countryid having count(*)  >  2
```

**Returned.**
```sql
SELECT COUNT(T1.CountryName)
FROM countries AS T1
INNER JOIN car_makers AS T2 ON T1.CountryId = T2.Country
GROUP BY T1.CountryName
HAVING COUNT(T2.Id) > 2
```

**First disagreeing instance** `car_1v5080.sqlite`.

Gold returns 13 row(s), 1 column(s):

    3
    5
    4
    4
    4
    4
    3
    4
    3
    3
    4
    4
    ... (13 rows total)

Returned query gives 13 row(s), 1 column(s):

    7
    3
    4
    4
    4
    4
    8
    3
    6
    4
    3
    4
    ... (13 rows total)

Difference: gold_subset_of_rep; 3 row(s) in common, 0 only in the gold, 3 only in the returned result.

### R213  (question 231, database `wta_1`)

- Returned by: kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 43/50, 46/50
- Instances disagreeing: 33 of 33 (100%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What are the full names of all players, sorted by age?

**Gold.**
```sql
SELECT first_name ,  last_name FROM players ORDER BY birth_date
```

**Returned.**
```sql
SELECT first_name, last_name
FROM players
ORDER BY (strftime('%Y', 'now') - strftime('%Y', birth_date))
```

**First disagreeing instance** `wta_1.sqlite` (this is the shipped benchmark database).

Gold returns 20662 row(s), 2 column(s):

    Thelma | Long
    Pauline | Addie
    Milly | Vagn Nielsen
    Vera | Johansen
    Reiko | Miyagi
    Louise | Brown
    Gertrude | Moran
    Zsuzsa | Kormoczy
    Peggy | Brixhe
    Betty | Pratt
    Doris | Hart
    Dorothy | Knode
    ... (20662 rows total)

Returned query gives 20662 row(s), 2 column(s):

    Martina | Hingis
    Mirjana | Lucic
    Justine | Henin
    Kerry Anne | Guse
    Jolene | Watanabe Giltz
    Karina | Habsudova
    Silvija | Talaja
    Alicia | Molik
    Tamarine | Tanasugarn
    Rita | Grande
    Katarina | Srebotnik
    Jana | Nejedly
    ... (20662 rows total)

Difference: row_order_only; 20658 row(s) in common, 0 only in the gold, 0 only in the returned result.

### R214  (question 234, database `wta_1`)

- Returned by: kwai-autosql-14b/seed202
- Returned in cell: A only
- Class mass: 24/50
- Instances disagreeing: 33 of 33 (100%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Find the name and rank points of the person who won the most times.

**Gold.**
```sql
SELECT winner_name ,  winner_rank_points FROM matches GROUP BY winner_name ORDER BY count(*) DESC LIMIT 1
```

**Returned.**
```sql
SELECT T1.first_name, T1.last_name, T3.ranking_points
FROM players AS T1
INNER JOIN matches AS T2 ON T1.player_id = T2.winner_id
INNER JOIN rankings AS T3 ON T1.player_id = T3.player_id
GROUP BY T1.player_id
ORDER BY COUNT(T2.winner_id) DESC
LIMIT 1
```

**First disagreeing instance** `wta_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    Angelique Kerber | 3715

Returned query gives 1 row(s), 3 column(s):

    Serena | Williams | 23

Difference: col_count_differs, disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R215  (question 235, database `wta_1`)

- Returned by: kwai-autosql-14b/seed202
- Returned in cell: A only
- Class mass: 26/50
- Instances disagreeing: 33 of 33 (100%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What is the name of the player who has won the most matches, and how many rank points does this player have?

**Gold.**
```sql
SELECT winner_name ,  winner_rank_points FROM matches GROUP BY winner_name ORDER BY count(*) DESC LIMIT 1
```

**Returned.**
```sql
SELECT P.first_name, P.last_name, R.ranking_points
FROM matches M
INNER JOIN players P ON M.winner_id = P.player_id
INNER JOIN rankings R ON P.player_id = R.player_id
GROUP BY M.winner_id
ORDER BY COUNT(M.winner_id) DESC
LIMIT 1
```

**First disagreeing instance** `wta_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    Angelique Kerber | 3715

Returned query gives 1 row(s), 3 column(s):

    Serena | Williams | 23

Difference: col_count_differs, disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R216  (question 235, database `wta_1`)

- Returned by: kwai-autosql-14b/seed202
- Returned in cell: D only
- Class mass: 17/50
- Instances disagreeing: 33 of 33 (100%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What is the name of the player who has won the most matches, and how many rank points does this player have?

**Gold.**
```sql
SELECT winner_name ,  winner_rank_points FROM matches GROUP BY winner_name ORDER BY count(*) DESC LIMIT 1
```

**Returned.**
```sql
SELECT P.first_name, P.last_name, R.ranking_points
FROM matches M
INNER JOIN players P ON M.winner_id = P.player_id
INNER JOIN rankings R ON P.player_id = R.player_id
GROUP BY P.first_name, P.last_name, R.ranking_points
ORDER BY COUNT(M.winner_id) DESC
LIMIT 1
```

**First disagreeing instance** `wta_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    Angelique Kerber | 3715

Returned query gives 1 row(s), 3 column(s):

    Karolina | Pliskova | 4

Difference: col_count_differs, disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R217  (question 260, database `student_transcripts_tracking`)

- Returned by: kwai-autosql-14b/seed202
- Returned in cell: both A and D
- Class mass: 50/50
- Instances disagreeing: 22 of 55 (40%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the last name of the students who live in North Carolina but have not registered in any degree programs?

**Gold.**
```sql
SELECT T1.last_name FROM Students AS T1 JOIN Addresses AS T2 ON T1.current_address_id  =  T2.address_id WHERE T2.state_province_county  =  'NorthCarolina' EXCEPT SELECT DISTINCT T3.last_name FROM Students AS T3 JOIN Student_Enrolment AS T4 ON T3.student_id  =  T4.student_id
```

**Returned.**
```sql
SELECT T1.last_name
FROM Students T1
INNER JOIN Addresses T2 ON T1.current_address_id = T2.address_id OR T1.permanent_address_id = T2.address_id
WHERE T2.state_province_county = 'North Carolina'
AND T1.student_id NOT IN (SELECT student_id FROM Student_Enrolment)
```

**First disagreeing instance** `student_transcripts_tracking.sqlite` (this is the shipped benchmark database).

Gold returns 2 row(s), 1 column(s):

    Gleichner
    Weimann

Returned query gives 0 row(s), None column(s):

    (no rows)

Difference: rep_empty; 0 row(s) in common, 2 only in the gold, 0 only in the returned result.

### R218  (question 310, database `tvshow`)

- Returned by: kwai-autosql-14b/seed202
- Returned in cell: both A and D
- Class mass: 30/50
- Instances disagreeing: 12 of 25 (48%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the countries that are not playing cartoons  Todd Casey writes?

**Gold.**
```sql
SELECT country FROM TV_Channel EXCEPT SELECT T1.country FROM TV_Channel AS T1 JOIN cartoon AS T2 ON T1.id = T2.Channel WHERE T2.written_by  =  'Todd Casey'
```

**Returned.**
```sql
SELECT DISTINCT Country
FROM TV_Channel
WHERE id NOT IN (
    SELECT DISTINCT Channel
    FROM Cartoon
    WHERE Written_by = 'Todd Casey'
)
```

**First disagreeing instance** `tvshow.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    Poland

Returned query gives 3 row(s), 1 column(s):

    Italy
    United Kingdom
    Poland

Difference: gold_subset_of_rep; 1 row(s) in common, 0 only in the gold, 2 only in the returned result.

### R219  (question 369, database `world_1`)

- Returned by: kwai-autosql-14b/seed202
- Returned in cell: D only
- Class mass: 28/50
- Instances disagreeing: 3 of 46 (7%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** How many official languages are spoken in Afghanistan?

**Gold.**
```sql
SELECT COUNT(*) FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code  =  T2.CountryCode WHERE T1.Name  =  "Afghanistan" AND IsOfficial  =  "T"
```

**Returned.**
```sql
SELECT COUNT(Language)
FROM countrylanguage
WHERE CountryCode = (
  SELECT Code
  FROM country
  WHERE Name = 'Afghanistan'
) AND IsOfficial = 'T'
```

**First disagreeing instance** `world_1v50811.sqlite`.

Gold returns 1 row(s), 1 column(s):

    1

Returned query gives 1 row(s), 1 column(s):

    0

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R220  (question 404, database `world_1`)

- Returned by: kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 26/50, 26/50
- Instances disagreeing: 44 of 46 (96%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the country codes for countries that do not speak English?

**Gold.**
```sql
SELECT CountryCode FROM countrylanguage EXCEPT SELECT CountryCode FROM countrylanguage WHERE LANGUAGE  =  "English"
```

**Returned.**
```sql
SELECT CountryCode FROM countrylanguage WHERE Language != 'English'
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 173 row(s), 1 column(s):

    AFG
    AGO
    ALB
    AND
    ARE
    ARG
    ARM
    AUT
    AZE
    BDI
    BEL
    BEN
    ... (173 rows total)

Returned query gives 924 row(s), 1 column(s):

    ABW
    ABW
    ABW
    AFG
    AFG
    AFG
    AFG
    AFG
    AGO
    AGO
    AGO
    AGO
    ... (924 rows total)

Difference: gold_subset_of_rep; 173 row(s) in common, 0 only in the gold, 50 only in the returned result.

### R221  (question 410, database `world_1`)

- Returned by: kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 26/50, 31/50
- Instances disagreeing: 9 of 46 (20%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Which cities are in European countries where English is not spoken officially?

**Gold.**
```sql
SELECT DISTINCT T2.Name FROM country AS T1 JOIN city AS T2 ON T2.CountryCode  =  T1.Code WHERE T1.Continent  =  'Europe' AND T1.Name NOT IN (SELECT T3.Name FROM country AS T3 JOIN countrylanguage AS T4 ON T3.Code  =  T4.CountryCode WHERE T4.IsOfficial  =  'T' AND T4.Language  =  'English')
```

**Returned.**
```sql
SELECT T1.Name
FROM city AS T1
INNER JOIN country AS T2 ON T1.CountryCode = T2.Code
WHERE T2.Continent = 'Europe'
AND T1.CountryCode NOT IN (
  SELECT CountryCode
  FROM countrylanguage
  WHERE Language = 'English' AND IsOfficial = 'T'
)
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 753 row(s), 1 column(s):

    Amsterdam
    Rotterdam
    Haag
    Utrecht
    Eindhoven
    Tilburg
    Groningen
    Breda
    Apeldoorn
    Nijmegen
    Enschede
    Haarlem
    ... (753 rows total)

Returned query gives 755 row(s), 1 column(s):

    Tirana
    Andorra la Vella
    Wien
    Graz
    Linz
    Salzburg
    Innsbruck
    Klagenfurt
    Antwerpen
    Gent
    Charleroi
    Liège
    ... (755 rows total)

Difference: duplicate_multiplicity_only; 753 row(s) in common, 0 only in the gold, 0 only in the returned result.

### R222  (question 431, database `world_1`)

- Returned by: kwai-autosql-14b/seed202
- Returned in cell: both A and D
- Class mass: 14/50
- Instances disagreeing: 46 of 46 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the language spoken by the largest percentage of people in each nation?

**Gold.**
```sql
SELECT LANGUAGE ,  CountryCode ,  max(Percentage) FROM countrylanguage GROUP BY CountryCode
```

**Returned.**
```sql
SELECT T1.Language
FROM countrylanguage AS T1
INNER JOIN (
  SELECT CountryCode, MAX(Percentage) AS max_percentage
  FROM countrylanguage
  GROUP BY CountryCode
) AS T2 ON T1.CountryCode = T2.CountryCode AND T1.Percentage = T2.max_percentage
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 233 row(s), 3 column(s):

    Papiamento | ABW | 76.7
    Pashto | AFG | 52.4
    Ovimbundu | AGO | 37.2
    English | AIA | 0.0
    Albaniana | ALB | 97.9
    Spanish | AND | 44.6
    Papiamento | ANT | 86.2
    Arabic | ARE | 42.0
    Spanish | ARG | 96.8
    Armenian | ARM | 93.4
    Samoan | ASM | 90.6
    Creole English | ATG | 95.7
    ... (233 rows total)

Returned query gives 241 row(s), 1 column(s):

    Papiamento
    Pashto
    Ovimbundu
    English
    Albaniana
    Spanish
    Papiamento
    Arabic
    Spanish
    Armenian
    Samoan
    Creole English
    ... (241 rows total)

Difference: col_count_differs, disjoint; 0 row(s) in common, 233 only in the gold, 136 only in the returned result.

### R223  (question 432, database `world_1`)

- Returned by: kwai-autosql-14b/seed202
- Returned in cell: both A and D
- Class mass: 17/50
- Instances disagreeing: 46 of 46 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the codes of the different nations, and what are the languages spoken by the greatest percentage of people for each?

**Gold.**
```sql
SELECT LANGUAGE ,  CountryCode ,  max(Percentage) FROM countrylanguage GROUP BY CountryCode
```

**Returned.**
```sql
SELECT T1.CountryCode, T1.Language
FROM countrylanguage T1
INNER JOIN (
  SELECT CountryCode, MAX(Percentage) AS max_percentage
  FROM countrylanguage
  GROUP BY CountryCode
) T2 ON T1.CountryCode = T2.CountryCode AND T1.Percentage = T2.max_percentage
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 233 row(s), 3 column(s):

    Papiamento | ABW | 76.7
    Pashto | AFG | 52.4
    Ovimbundu | AGO | 37.2
    English | AIA | 0.0
    Albaniana | ALB | 97.9
    Spanish | AND | 44.6
    Papiamento | ANT | 86.2
    Arabic | ARE | 42.0
    Spanish | ARG | 96.8
    Armenian | ARM | 93.4
    Samoan | ASM | 90.6
    Creole English | ATG | 95.7
    ... (233 rows total)

Returned query gives 241 row(s), 2 column(s):

    ABW | Papiamento
    AFG | Pashto
    AGO | Ovimbundu
    AIA | English
    ALB | Albaniana
    AND | Spanish
    ANT | Papiamento
    ARE | Arabic
    ARG | Spanish
    ARM | Armenian
    ASM | Samoan
    ATG | Creole English
    ... (241 rows total)

Difference: col_count_differs, disjoint; 0 row(s) in common, 233 only in the gold, 241 only in the returned result.

### R224  (question 434, database `world_1`)

- Returned by: kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 26/50, 26/50
- Instances disagreeing: 46 of 46 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Count the number of countries for which Spanish is predominantly spoken .

**Gold.**
```sql
SELECT count(*) ,   max(Percentage) FROM countrylanguage WHERE LANGUAGE  =  "Spanish" GROUP BY CountryCode
```

**Returned.**
```sql
SELECT COUNT(CountryCode)
FROM countrylanguage
WHERE Language = 'Spanish'
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 28 row(s), 2 column(s):

    1 | 7.4
    1 | 44.6
    1 | 96.8
    1 | 31.6
    1 | 87.7
    1 | 0.7
    1 | 89.7
    1 | 99.0
    1 | 97.5
    1 | 100.0
    1 | 98.0
    1 | 93.0
    ... (28 rows total)

Returned query gives 1 row(s), 1 column(s):

    28

Difference: col_count_differs, disjoint; 0 row(s) in common, 27 only in the gold, 1 only in the returned result.

### R225  (question 46, database `pets_1`)

- Returned by: kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 29/50
- Instances disagreeing: 16 of 27 (59%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What major is every student who does not own a cat, and also how old are they?

**Gold.**
```sql
SELECT major ,  age FROM student WHERE stuid NOT IN (SELECT T1.stuid FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid  =  T2.stuid JOIN pets AS T3 ON T3.petid  =  T2.petid WHERE T3.pettype  =  'cat')
```

**Returned.**
```sql
SELECT DISTINCT T1.Major, T1.Age
FROM Student AS T1
WHERE T1.StuID NOT IN (
    SELECT T2.StuID
    FROM Has_Pet AS T2
    INNER JOIN Pets AS T3 ON T2.PetID = T3.PetID
    WHERE T3.PetType = 'cat'
)
```

**First disagreeing instance** `pets_1.sqlite` (this is the shipped benchmark database).

Gold returns 33 row(s), 2 column(s):

    600 | 19
    600 | 21
    600 | 20
    600 | 26
    600 | 18
    600 | 18
    600 | 20
    600 | 19
    600 | 17
    600 | 22
    600 | 20
    600 | 18
    ... (33 rows total)

Returned query gives 21 row(s), 2 column(s):

    600 | 19
    600 | 21
    600 | 20
    600 | 26
    600 | 18
    600 | 17
    600 | 22
    600 | 16
    600 | 27
    520 | 22
    520 | 19
    540 | 17
    ... (21 rows total)

Difference: duplicate_multiplicity_only; 21 row(s) in common, 0 only in the gold, 0 only in the returned result.

### R226  (question 73, database `car_1`)

- Returned by: kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 28/50
- Instances disagreeing: 2 of 60 (3%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the accelerate of amc hornet sportabout (sw)?

**Gold.**
```sql
SELECT T1.Accelerate FROM CARS_DATA AS T1 JOIN CAR_NAMES AS T2 ON T1.Id  =  T2.MakeId WHERE T2.Make  =  'amc hornet sportabout (sw)';
```

**Returned.**
```sql
SELECT T3.Accelerate
FROM model_list AS T1
INNER JOIN car_names AS T2 ON T1.Model = T2.Model
INNER JOIN cars_data AS T3 ON T2.MakeId = T3.Id
WHERE T1.Model = 'amc hornet sportabout (sw)'
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    13.5

Returned query gives 0 row(s), None column(s):

    (no rows)

Difference: rep_empty; 0 row(s) in common, 1 only in the gold, 0 only in the returned result.

### R227  (question 91, database `car_1`)

- Returned by: kwai-autosql-14b/seed303
- Returned in cell: D only
- Class mass: 9/50
- Instances disagreeing: 11 of 60 (18%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the average edispl for all volvos?

**Gold.**
```sql
SELECT avg(T2.edispl) FROM CAR_NAMES AS T1 JOIN CARS_DATA AS T2 ON T1.MakeId  =  T2.Id WHERE T1.Model  =  'volvo';
```

**Returned.**
```sql
SELECT AVG(T3.Edispl)
FROM car_makers AS T1
INNER JOIN model_list AS T2 ON T1.Id = T2.Maker
INNER JOIN car_names AS T4 ON T2.ModelId = T4.MakeId
INNER JOIN cars_data AS T3 ON T4.MakeId = T3.Id
WHERE T1.Maker = 'volvo'
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    133.5

Returned query gives 1 row(s), 1 column(s):

    360.0

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R228  (question 99, database `car_1`)

- Returned by: kwai-autosql-14b/seed303
- Returned in cell: A only
- Class mass: 11/50
- Instances disagreeing: 31 of 60 (52%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Which distinctive models are produced by General Motors or heavier than 3500?

**Gold.**
```sql
SELECT DISTINCT T2.Model FROM CAR_NAMES AS T1 JOIN MODEL_LIST AS T2 ON T1.Model  =  T2.Model JOIN CAR_MAKERS AS T3 ON T2.Maker  =  T3.Id JOIN CARS_DATA AS T4 ON T1.MakeId  =  T4.Id WHERE T3.FullName  =  'General Motors' OR T4.weight  >  3500;
```

**Returned.**
```sql
SELECT DISTINCT T1.Model
FROM car_names AS T1
INNER JOIN cars_data AS T2 ON T1.MakeId = T2.Id
INNER JOIN car_makers AS T3 ON T1.Make = T3.Maker
WHERE T3.FullName = 'General Motors'
UNION
SELECT DISTINCT T1.Model
FROM car_names AS T1
INNER JOIN cars_data AS T2 ON T1.MakeId = T2.Id
WHERE T2.Weight > 3500
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 13 row(s), 1 column(s):

    chevrolet
    buick
    ford
    plymouth
    pontiac
    amc
    dodge
    mercury
    oldsmobile
    chrysler
    mercedes-benz
    cadillac
    ... (13 rows total)

Returned query gives 14 row(s), 1 column(s):

    amc
    buick
    cadillac
    chevrolet
    chrysler
    dodge
    ford
    hi
    mercedes
    mercedes-benz
    mercury
    oldsmobile
    ... (14 rows total)

Difference: gold_subset_of_rep; 13 row(s) in common, 0 only in the gold, 1 only in the returned result.

### R229  (question 99, database `car_1`)

- Returned by: kwai-autosql-14b/seed303
- Returned in cell: D only
- Class mass: 6/50
- Instances disagreeing: 20 of 60 (33%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Which distinctive models are produced by General Motors or heavier than 3500?

**Gold.**
```sql
SELECT DISTINCT T2.Model FROM CAR_NAMES AS T1 JOIN MODEL_LIST AS T2 ON T1.Model  =  T2.Model JOIN CAR_MAKERS AS T3 ON T2.Maker  =  T3.Id JOIN CARS_DATA AS T4 ON T1.MakeId  =  T4.Id WHERE T3.FullName  =  'General Motors' OR T4.weight  >  3500;
```

**Returned.**
```sql
SELECT DISTINCT T3.Model
FROM car_makers AS T1
INNER JOIN model_list AS T2 ON T1.Id = T2.Maker
INNER JOIN car_names AS T3 ON T2.Model = T3.Model
INNER JOIN cars_data AS T4 ON T3.MakeId = T4.Id
WHERE T1.FullName = 'American Motor Company' OR T4.Weight > 3500
```

**First disagreeing instance** `car_1v5081.sqlite`.

Gold returns 6 row(s), 1 column(s):

    349921lVw
    4000
    2uNZ9bnY(h
    3500
    39993jo0X
    zR

Returned query gives 7 row(s), 1 column(s):

    1975
    349921lVw
    4000
    2uNZ9bnY(h
    3500
    39993jo0X
    zR

Difference: gold_subset_of_rep; 6 row(s) in common, 0 only in the gold, 1 only in the returned result.

### R230  (question 100, database `car_1`)

- Returned by: kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 11/50
- Instances disagreeing: 58 of 60 (97%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the different models created by either General Motors or over 3500 lbs?

**Gold.**
```sql
SELECT DISTINCT T2.Model FROM CAR_NAMES AS T1 JOIN MODEL_LIST AS T2 ON T1.Model  =  T2.Model JOIN CAR_MAKERS AS T3 ON T2.Maker  =  T3.Id JOIN CARS_DATA AS T4 ON T1.MakeId  =  T4.Id WHERE T3.FullName  =  'General Motors' OR T4.weight  >  3500;
```

**Returned.**
```sql
SELECT DISTINCT T2.Model
FROM car_makers AS T1
INNER JOIN car_names AS T2 ON T1.Id = T2.Make
INNER JOIN cars_data AS T3 ON T2.MakeId = T3.Id
WHERE T1.FullName = 'General Motors' OR T3.Weight > 3500
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 13 row(s), 1 column(s):

    chevrolet
    buick
    ford
    plymouth
    pontiac
    amc
    dodge
    mercury
    oldsmobile
    chrysler
    mercedes-benz
    cadillac
    ... (13 rows total)

Returned query gives 0 row(s), None column(s):

    (no rows)

Difference: rep_empty; 0 row(s) in common, 13 only in the gold, 0 only in the returned result.

### R231  (question 101, database `car_1`)

- Returned by: kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 26/50
- Instances disagreeing: 49 of 60 (82%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** In which years cars were produced between 3000 and 4000 pounds?

**Gold.**
```sql
select distinct year from cars_data where weight between 3000 and 4000;
```

**Returned.**
```sql
SELECT Year FROM cars_data WHERE Weight BETWEEN 3000 AND 4000
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 13 row(s), 1 column(s):

    1970
    1971
    1972
    1973
    1974
    1975
    1976
    1977
    1978
    1979
    1980
    1981
    ... (13 rows total)

Returned query gives 107 row(s), 1 column(s):

    1970
    1970
    1970
    1970
    1970
    1970
    1970
    1970
    1970
    1970
    1970
    1970
    ... (107 rows total)

Difference: duplicate_multiplicity_only; 13 row(s) in common, 0 only in the gold, 0 only in the returned result.

### R232  (question 105, database `car_1`)

- Returned by: kwai-autosql-14b/seed303
- Returned in cell: D only
- Class mass: 18/50
- Instances disagreeing: 60 of 60 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** How many nations has more than 2 car makers ?

**Gold.**
```sql
select count(*) from countries as t1 join car_makers as t2 on t1.countryid  =  t2.country group by t1.countryid having count(*)  >  2
```

**Returned.**
```sql
SELECT COUNT(*)
FROM (
  SELECT Country
  FROM car_makers
  GROUP BY Country
  HAVING COUNT(Id) > 2
)
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 4 row(s), 1 column(s):

    4
    4
    3
    5

Returned query gives 1 row(s), 1 column(s):

    4

Difference: rep_subset_of_gold; 1 row(s) in common, 2 only in the gold, 0 only in the returned result.

### R233  (question 106, database `car_1`)

- Returned by: kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 21/50
- Instances disagreeing: 60 of 60 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the number of nations with more than 2 car makers ?

**Gold.**
```sql
select count(*) from countries as t1 join car_makers as t2 on t1.countryid  =  t2.country group by t1.countryid having count(*)  >  2
```

**Returned.**
```sql
SELECT COUNT(*)
FROM (
  SELECT T1.Country
  FROM car_makers AS T1
  INNER JOIN countries AS T2 ON T1.Country = T2.CountryId
  GROUP BY T1.Country
  HAVING COUNT(T1.Id) > 2
) AS subquery
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 4 row(s), 1 column(s):

    4
    4
    3
    5

Returned query gives 1 row(s), 1 column(s):

    4

Difference: rep_subset_of_gold; 1 row(s) in common, 2 only in the gold, 0 only in the returned result.

### R234  (question 140, database `flight_2`)

- Returned by: kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 49/50
- Instances disagreeing: 8 of 56 (14%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Give the number of Jetblue Airways flights.

**Gold.**
```sql
SELECT count(*) FROM FLIGHTS AS T1 JOIN AIRLINES AS T2 ON T1.Airline  =  T2.uid WHERE T2.Airline = "JetBlue Airways"
```

**Returned.**
```sql
SELECT COUNT(f.Airline)
FROM flights f
INNER JOIN airlines a ON f.Airline = a.uid
WHERE a.Airline = 'Jetblue Airways'
```

**First disagreeing instance** `flight_2.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    100

Returned query gives 1 row(s), 1 column(s):

    0

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R235  (question 234, database `wta_1`)

- Returned by: kwai-autosql-14b/seed303
- Returned in cell: A only
- Class mass: 18/50
- Instances disagreeing: 33 of 33 (100%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Find the name and rank points of the person who won the most times.

**Gold.**
```sql
SELECT winner_name ,  winner_rank_points FROM matches GROUP BY winner_name ORDER BY count(*) DESC LIMIT 1
```

**Returned.**
```sql
SELECT T3.first_name, T3.last_name, T2.ranking_points
FROM matches AS T1
INNER JOIN rankings AS T2 ON T1.winner_id = T2.player_id
INNER JOIN players AS T3 ON T1.winner_id = T3.player_id
GROUP BY T1.winner_id
ORDER BY COUNT(T1.winner_id) DESC
LIMIT 1
```

**First disagreeing instance** `wta_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    Angelique Kerber | 3715

Returned query gives 1 row(s), 3 column(s):

    Serena | Williams | 23

Difference: col_count_differs, disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R236  (question 253, database `battle_death`)

- Returned by: kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 33/50
- Instances disagreeing: 17 of 28 (61%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** List the name and date the battle that has lost  Lettice and HMS Atalanta

**Gold.**
```sql
SELECT T1.name ,  T1.date FROM battle AS T1 JOIN ship AS T2 ON T1.id  =  T2.lost_in_battle WHERE T2.name  =  'Lettice' INTERSECT SELECT T1.name ,  T1.date FROM battle AS T1 JOIN ship AS T2 ON T1.id  =  T2.lost_in_battle WHERE T2.name  =  'HMS Atalanta'
```

**Returned.**
```sql
SELECT T1.name, T1.date
FROM battle AS T1
INNER JOIN ship AS T2 ON T1.id = T2.lost_in_battle
WHERE T2.name IN ('Lettice', 'HMS Atalanta')
```

**First disagreeing instance** `battle_death.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    Siege of Constantinople | 1235

Returned query gives 2 row(s), 2 column(s):

    Siege of Constantinople | 1235
    Siege of Constantinople | 1235

Difference: duplicate_multiplicity_only; 1 row(s) in common, 0 only in the gold, 0 only in the returned result.

### R237  (question 259, database `student_transcripts_tracking`)

- Returned by: kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 50/50
- Instances disagreeing: 22 of 55 (40%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find the last name of the students who currently live in North Carolina but have not registered in any degree program.

**Gold.**
```sql
SELECT T1.last_name FROM Students AS T1 JOIN Addresses AS T2 ON T1.current_address_id  =  T2.address_id WHERE T2.state_province_county  =  'NorthCarolina' EXCEPT SELECT DISTINCT T3.last_name FROM Students AS T3 JOIN Student_Enrolment AS T4 ON T3.student_id  =  T4.student_id
```

**Returned.**
```sql
SELECT T1.last_name
FROM Students T1
INNER JOIN Addresses T2 ON T1.current_address_id = T2.address_id
WHERE T2.state_province_county = 'North Carolina'
AND T1.student_id NOT IN (SELECT student_id FROM Student_Enrolment)
```

**First disagreeing instance** `student_transcripts_tracking.sqlite` (this is the shipped benchmark database).

Gold returns 2 row(s), 1 column(s):

    Gleichner
    Weimann

Returned query gives 0 row(s), None column(s):

    (no rows)

Difference: rep_empty; 0 row(s) in common, 2 only in the gold, 0 only in the returned result.

### R238  (question 260, database `student_transcripts_tracking`)

- Returned by: kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 50/50
- Instances disagreeing: 22 of 55 (40%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the last name of the students who live in North Carolina but have not registered in any degree programs?

**Gold.**
```sql
SELECT T1.last_name FROM Students AS T1 JOIN Addresses AS T2 ON T1.current_address_id  =  T2.address_id WHERE T2.state_province_county  =  'NorthCarolina' EXCEPT SELECT DISTINCT T3.last_name FROM Students AS T3 JOIN Student_Enrolment AS T4 ON T3.student_id  =  T4.student_id
```

**Returned.**
```sql
SELECT T1.last_name
FROM Students T1
INNER JOIN Addresses T2 ON T1.current_address_id = T2.address_id
WHERE T2.state_province_county = 'North Carolina'
AND T1.student_id NOT IN (SELECT student_id FROM Student_Enrolment)
```

**First disagreeing instance** `student_transcripts_tracking.sqlite` (this is the shipped benchmark database).

Gold returns 2 row(s), 1 column(s):

    Gleichner
    Weimann

Returned query gives 0 row(s), None column(s):

    (no rows)

Difference: rep_empty; 0 row(s) in common, 2 only in the gold, 0 only in the returned result.

### R239  (question 431, database `world_1`)

- Returned by: kwai-autosql-14b/seed303
- Returned in cell: both A and D
- Class mass: 11/50
- Instances disagreeing: 46 of 46 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the language spoken by the largest percentage of people in each nation?

**Gold.**
```sql
SELECT LANGUAGE ,  CountryCode ,  max(Percentage) FROM countrylanguage GROUP BY CountryCode
```

**Returned.**
```sql
SELECT CountryCode, Language
FROM (
  SELECT CountryCode, Language, Percentage,
         ROW_NUMBER() OVER (PARTITION BY CountryCode ORDER BY Percentage DESC) AS rn
  FROM countrylanguage
)
WHERE rn = 1
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 233 row(s), 3 column(s):

    Papiamento | ABW | 76.7
    Pashto | AFG | 52.4
    Ovimbundu | AGO | 37.2
    English | AIA | 0.0
    Albaniana | ALB | 97.9
    Spanish | AND | 44.6
    Papiamento | ANT | 86.2
    Arabic | ARE | 42.0
    Spanish | ARG | 96.8
    Armenian | ARM | 93.4
    Samoan | ASM | 90.6
    Creole English | ATG | 95.7
    ... (233 rows total)

Returned query gives 233 row(s), 2 column(s):

    ABW | Papiamento
    AFG | Pashto
    AGO | Ovimbundu
    AIA | English
    ALB | Albaniana
    AND | Spanish
    ANT | Papiamento
    ARE | Arabic
    ARG | Spanish
    ARM | Armenian
    ASM | Samoan
    ATG | Creole English
    ... (233 rows total)

Difference: col_count_differs, disjoint; 0 row(s) in common, 233 only in the gold, 233 only in the returned result.

### R240  (question 3, database `concert_singer`)

- Returned by: omnisql-32b/seed101
- Returned in cell: D only
- Class mass: 15/50
- Instances disagreeing: 32 of 32 (100%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Show the name and the release year of the song by the youngest singer.

**Gold.**
```sql
SELECT song_name ,  song_release_year FROM singer ORDER BY age LIMIT 1
```

**Returned.**
```sql
SELECT Name, Song_release_year
FROM singer
ORDER BY Age ASC
LIMIT 1
```

**First disagreeing instance** `concert_singer.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    Love | 2016

Returned query gives 1 row(s), 2 column(s):

    Tribal King | 2016

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R241  (question 22, database `concert_singer`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed202
- Returned in cell: D only
- Class mass: 24/50, 22/50
- Instances disagreeing: 23 of 32 (72%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Show the name and theme for all concerts and the number of singers in each.

**Gold.**
```sql
SELECT T2.concert_name ,  T2.theme ,  count(*) FROM singer_in_concert AS T1 JOIN concert AS T2 ON T1.concert_id  =  T2.concert_id GROUP BY T2.concert_id
```

**Returned.**
```sql
SELECT 
    concert.concert_Name, 
    concert.Theme, 
    COUNT(singer_in_concert.Singer_ID) AS singer_count
FROM 
    concert
INNER JOIN 
    singer_in_concert 
ON 
    concert.concert_ID = singer_in_concert.concert_ID
GROUP BY 
    concert.concert_Name, 
    concert.Theme
```

**First disagreeing instance** `concert_singertest0.sqlite`.

Gold returns 109 row(s), 3 column(s):

    36sQO mF | 0 | 1
     | ruJKIParty All Night | 1
    20 | 21 | 1
    1 | Bleeding Love | 1
    Week 2 | Happy Tonight | 1
    M8nuCa | 21 | 1
      X7a3V2nA2r | 20 | 1
    JPZCP8Xfwj e | 2 | 1
    21 | 21 | 1
    Home Visits | 1 | 1
    21 | France | 1
    19 | BTA2 )IT gK ef | 3
    ... (109 rows total)

Returned query gives 98 row(s), 3 column(s):

     | 20 | 1
     | ruJKIParty All Night | 1
     | ylMKYS9a | 1
      X7a3V2nA2r | 20 | 1
     Tz)XD6W | tpi25LK | 1
    )YlLbPyg6 | 1 | 1
    0 | 1 | 1
    0 | 1643K  | 2
    0 | 2 | 2
    0 | 9 | 1
    0 | Free choice 2 | 1
    0 | Happy TonightXYW4D | 1
    ... (98 rows total)

Difference: values differ; 88 row(s) in common, 17 only in the gold, 10 only in the returned result.

### R242  (question 25, database `concert_singer`)

- Returned by: omnisql-32b/seed101
- Returned in cell: both A and D
- Class mass: 27/50
- Instances disagreeing: 27 of 32 (84%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** List all singer names in concerts in  2014.

**Gold.**
```sql
SELECT T2.name FROM singer_in_concert AS T1 JOIN singer AS T2 ON T1.singer_id  =  T2.singer_id JOIN concert AS T3 ON T1.concert_id  =  T3.concert_id WHERE T3.year  =  2014
```

**Returned.**
```sql
SELECT DISTINCT singer.Name
FROM concert
INNER JOIN singer_in_concert ON concert.concert_ID = singer_in_concert.concert_ID
INNER JOIN singer ON singer_in_concert.Singer_ID = singer.Singer_ID
WHERE concert.Year = '2014'
```

**First disagreeing instance** `concert_singer.sqlite` (this is the shipped benchmark database).

Gold returns 6 row(s), 1 column(s):

    Timbaland
    Justin Brown
    John Nizinik
    Justin Brown
    Tribal King
    Rose White

Returned query gives 5 row(s), 1 column(s):

    Timbaland
    Justin Brown
    John Nizinik
    Tribal King
    Rose White

Difference: duplicate_multiplicity_only; 5 row(s) in common, 0 only in the gold, 0 only in the returned result.

### R243  (question 44, database `pets_1`)

- Returned by: omnisql-32b/seed101
- Returned in cell: D only
- Class mass: 22/50
- Instances disagreeing: 20 of 27 (74%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the students' first names who have both cats and dogs?

**Gold.**
```sql
SELECT T1.Fname FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid  =  T2.stuid JOIN pets AS T3 ON T3.petid  =  T2.petid WHERE T3.pettype  =  'cat' INTERSECT SELECT T1.Fname FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid  =  T2.stuid JOIN pets AS T3 ON T3.petid  =  T2.petid WHERE T3.pettype  =  'dog'
```

**Returned.**
```sql
SELECT s.Fname
FROM Student s
JOIN Has_Pet hp ON s.StuID = hp.StuID
JOIN Pets p ON hp.PetID = p.PetID
WHERE p.PetType IN ('cat', 'dog')
GROUP BY s.StuID, s.Fname
HAVING COUNT(DISTINCT p.PetType) = 2
```

**First disagreeing instance** `pets_1v5080.sqlite`.

Gold returns 5 row(s), 1 column(s):

    0
    003
    10
    David
    Oy01U(d

Returned query gives 4 row(s), 1 column(s):

    Oy01U(d
    David
    003
    0

Difference: rep_subset_of_gold; 4 row(s) in common, 1 only in the gold, 0 only in the returned result.

### R244  (question 49, database `pets_1`)

- Returned by: omnisql-32b/seed101
- Returned in cell: A only
- Class mass: 29/50
- Instances disagreeing: 20 of 27 (74%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find the first name and age of students who have a dog but do not have a cat.

**Gold.**
```sql
SELECT T1.fname ,  T1.age FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid  =  T2.stuid JOIN pets AS T3 ON T3.petid  =  T2.petid WHERE T3.pettype  =  'dog' AND T1.stuid NOT IN (SELECT T1.stuid FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid  =  T2.stuid JOIN pets AS T3 ON T3.petid  =  T2.petid WHERE T3.pettype  =  'cat')
```

**Returned.**
```sql
SELECT S.Fname, S.Age
FROM Student S
WHERE S.StuID IN (
  SELECT HP.StuID
  FROM Has_Pet HP
  INNER JOIN Pets P ON HP.PetID = P.PetID
  WHERE P.PetType = 'dog'
)
AND S.StuID NOT IN (
  SELECT HP.StuID
  FROM Has_Pet HP
  INNER JOIN Pets P ON HP.PetID = P.PetID
  WHERE P.PetType = 'cat'
)
```

**First disagreeing instance** `pets_1.sqlite` (this is the shipped benchmark database).

Gold returns 2 row(s), 2 column(s):

    Tracy | 19
    Tracy | 19

Returned query gives 1 row(s), 2 column(s):

    Tracy | 19

Difference: duplicate_multiplicity_only; 1 row(s) in common, 0 only in the gold, 0 only in the returned result.

### R245  (question 50, database `pets_1`)

- Returned by: omnisql-32b/seed101
- Returned in cell: A only
- Class mass: 33/50
- Instances disagreeing: 25 of 27 (93%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the first name of every student who has a dog but does not have a cat?

**Gold.**
```sql
SELECT T1.fname ,  T1.age FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid  =  T2.stuid JOIN pets AS T3 ON T3.petid  =  T2.petid WHERE T3.pettype  =  'dog' AND T1.stuid NOT IN (SELECT T1.stuid FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid  =  T2.stuid JOIN pets AS T3 ON T3.petid  =  T2.petid WHERE T3.pettype  =  'cat')
```

**Returned.**
```sql
SELECT DISTINCT S.Fname
FROM Student S
JOIN Has_Pet HP ON S.StuID = HP.StuID
JOIN Pets P ON HP.PetID = P.PetID
WHERE P.PetType = 'dog'
EXCEPT
SELECT DISTINCT S.Fname
FROM Student S
JOIN Has_Pet HP ON S.StuID = HP.StuID
JOIN Pets P ON HP.PetID = P.PetID
WHERE P.PetType = 'cat'
```

**First disagreeing instance** `pets_1.sqlite` (this is the shipped benchmark database).

Gold returns 2 row(s), 2 column(s):

    Tracy | 19
    Tracy | 19

Returned query gives 1 row(s), 1 column(s):

    Tracy

Difference: col_count_differs, disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R246  (question 50, database `pets_1`)

- Returned by: omnisql-32b/seed101
- Returned in cell: D only
- Class mass: 16/50
- Instances disagreeing: 25 of 27 (93%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the first name of every student who has a dog but does not have a cat?

**Gold.**
```sql
SELECT T1.fname ,  T1.age FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid  =  T2.stuid JOIN pets AS T3 ON T3.petid  =  T2.petid WHERE T3.pettype  =  'dog' AND T1.stuid NOT IN (SELECT T1.stuid FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid  =  T2.stuid JOIN pets AS T3 ON T3.petid  =  T2.petid WHERE T3.pettype  =  'cat')
```

**Returned.**
```sql
SELECT S.Fname
FROM Student S
JOIN Has_Pet HP ON S.StuID = HP.StuID
JOIN Pets P ON HP.PetID = P.PetID
WHERE P.PetType = 'dog'
  AND NOT EXISTS (
    SELECT 1
    FROM Has_Pet HP2
    JOIN Pets P2 ON HP2.PetID = P2.PetID
    WHERE HP2.StuID = S.StuID AND P2.PetType = 'cat'
  )
```

**First disagreeing instance** `pets_1.sqlite` (this is the shipped benchmark database).

Gold returns 2 row(s), 2 column(s):

    Tracy | 19
    Tracy | 19

Returned query gives 2 row(s), 1 column(s):

    Tracy
    Tracy

Difference: col_count_differs, disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R247  (question 66, database `car_1`)

- Returned by: omnisql-32b/seed101
- Returned in cell: both A and D
- Class mass: 8/50
- Instances disagreeing: 60 of 60 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the maker of the carr produced in the earliest  and what  year was it?

**Gold.**
```sql
SELECT T2.Make ,  T1.Year FROM CARS_DATA AS T1 JOIN CAR_NAMES AS T2 ON T1.Id  =  T2.MakeId WHERE T1.Year  =  (SELECT min(YEAR) FROM CARS_DATA);
```

**Returned.**
```sql
SELECT cm.Maker, cd.Year
FROM cars_data cd
JOIN car_names cn ON cd.Id = cn.MakeId
JOIN model_list ml ON cn.Model = ml.Model
JOIN car_makers cm ON ml.Maker = cm.Id
WHERE cd.Year = (
    SELECT MIN(Year) FROM cars_data
)
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 35 row(s), 2 column(s):

    chevrolet chevelle malibu | 1970
    buick skylark 320 | 1970
    plymouth satellite | 1970
    amc rebel sst | 1970
    ford torino | 1970
    ford galaxie 500 | 1970
    chevrolet impala | 1970
    plymouth fury iii | 1970
    pontiac catalina | 1970
    amc ambassador dpl | 1970
    citroen ds-21 pallas | 1970
    chevrolet chevelle concours (sw) | 1970
    ... (35 rows total)

Returned query gives 34 row(s), 2 column(s):

    gm | 1970
    gm | 1970
    chrysler | 1970
    amc | 1970
    ford | 1970
    ford | 1970
    gm | 1970
    chrysler | 1970
    gm | 1970
    amc | 1970
    citroen | 1970
    gm | 1970
    ... (34 rows total)

Difference: disjoint; 0 row(s) in common, 35 only in the gold, 11 only in the returned result.

### R248  (question 75, database `car_1`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 40/50, 43/50
- Instances disagreeing: 14 of 60 (23%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the number of makers of care in France?

**Gold.**
```sql
SELECT count(*) FROM CAR_MAKERS AS T1 JOIN COUNTRIES AS T2 ON T1.Country  =  T2.CountryId WHERE T2.CountryName  =  'france';
```

**Returned.**
```sql
SELECT COUNT(*) 
FROM car_makers 
JOIN countries ON car_makers.Country = countries.CountryId 
WHERE countries.CountryName = 'France'
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    3

Returned query gives 1 row(s), 1 column(s):

    0

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R249  (question 77, database `car_1`)

- Returned by: omnisql-32b/seed101
- Returned in cell: both A and D
- Class mass: 26/50
- Instances disagreeing: 33 of 60 (55%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the count of the car models produced in the United States?

**Gold.**
```sql
SELECT count(*) FROM MODEL_LIST AS T1 JOIN CAR_MAKERS AS T2 ON T1.Maker  =  T2.Id JOIN COUNTRIES AS T3 ON T2.Country  =  T3.CountryId WHERE T3.CountryName  =  'usa';
```

**Returned.**
```sql
SELECT 
    COUNT(DISTINCT M.Model) AS US_Car_Models_Count
FROM 
    car_makers CM
JOIN 
    countries C ON CM.Country = C.CountryId
JOIN 
    model_list M ON CM.Id = M.Maker
WHERE 
    C.CountryName = 'United States'
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    13

Returned query gives 1 row(s), 1 column(s):

    0

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R250  (question 82, database `car_1`)

- Returned by: omnisql-32b/seed101
- Returned in cell: A only
- Class mass: 25/50
- Instances disagreeing: 59 of 60 (98%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the number of the cars with  more than 150 hp?

**Gold.**
```sql
SELECT count(*) FROM CARS_DATA WHERE horsepower  >  150;
```

**Returned.**
```sql
SELECT COUNT(*) 
FROM cars_data 
WHERE CAST(Horsepower AS REAL) > 150
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    281

Returned query gives 1 row(s), 1 column(s):

    49

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R251  (question 85, database `car_1`)

- Returned by: omnisql-32b/seed101
- Returned in cell: D only
- Class mass: 22/50
- Instances disagreeing: 11 of 60 (18%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the names of all European countries with at least 3 manufacturers?

**Gold.**
```sql
SELECT T1.CountryName FROM COUNTRIES AS T1 JOIN CONTINENTS AS T2 ON T1.Continent  =  T2.ContId JOIN CAR_MAKERS AS T3 ON T1.CountryId  =  T3.Country WHERE T2.Continent  =  'europe' GROUP BY T1.CountryName HAVING count(*)  >=  3;
```

**Returned.**
```sql
SELECT c.CountryName
FROM car_makers cm
JOIN countries c ON cm.Country = c.CountryId
WHERE c.Continent = (SELECT ContId FROM continents WHERE Continent = 'Europe')
GROUP BY c.CountryName
HAVING COUNT(cm.Id) >= 3
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 2 row(s), 1 column(s):

    france
    germany

Returned query gives 0 row(s), None column(s):

    (no rows)

Difference: rep_empty; 0 row(s) in common, 2 only in the gold, 0 only in the returned result.

### R252  (question 91, database `car_1`)

- Returned by: omnisql-32b/seed101
- Returned in cell: A only
- Class mass: 20/50
- Instances disagreeing: 11 of 60 (18%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the average edispl for all volvos?

**Gold.**
```sql
SELECT avg(T2.edispl) FROM CAR_NAMES AS T1 JOIN CARS_DATA AS T2 ON T1.MakeId  =  T2.Id WHERE T1.Model  =  'volvo';
```

**Returned.**
```sql
SELECT AVG(Edispl) AS AverageEdispl
FROM cars_data
WHERE Id IN (
    SELECT MakeId
    FROM car_names
    WHERE Make = 'volvo'
)
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    133.5

Returned query gives 1 row(s), 1 column(s):

    NULL

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R253  (question 91, database `car_1`)

- Returned by: omnisql-32b/seed101
- Returned in cell: D only
- Class mass: 15/50
- Instances disagreeing: 18 of 60 (30%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the average edispl for all volvos?

**Gold.**
```sql
SELECT avg(T2.edispl) FROM CAR_NAMES AS T1 JOIN CARS_DATA AS T2 ON T1.MakeId  =  T2.Id WHERE T1.Model  =  'volvo';
```

**Returned.**
```sql
SELECT AVG(cd.Edispl) AS AverageEdispl
FROM cars_data cd
INNER JOIN car_names cn ON cd.Id = cn.MakeId
INNER JOIN model_list ml ON cn.Model = ml.Model
INNER JOIN car_makers cm ON ml.Maker = cm.Id
WHERE cm.Maker = 'volvo'
```

**First disagreeing instance** `car_1v50811.sqlite`.

Gold returns 1 row(s), 1 column(s):

    NULL

Returned query gives 1 row(s), 1 column(s):

    436889768.3333333

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R254  (question 92, database `car_1`)

- Returned by: omnisql-32b/seed101
- Returned in cell: both A and D
- Class mass: 5/50
- Instances disagreeing: 60 of 60 (100%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What car has the most different versions?

**Gold.**
```sql
SELECT Model FROM CAR_NAMES GROUP BY Model ORDER BY count(*) DESC LIMIT 1;
```

**Returned.**
```sql
SELECT Model, COUNT(*) AS VersionCount
FROM model_list
GROUP BY Model
ORDER BY VersionCount DESC
LIMIT 1
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    ford

Returned query gives 1 row(s), 2 column(s):

    amc | 1

Difference: col_count_differs, disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R255  (question 98, database `car_1`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 31/50, 36/50
- Instances disagreeing: 30 of 60 (50%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the names and ids of all car companies with more than 3 models?

**Gold.**
```sql
SELECT T1.FullName ,  T1.Id FROM CAR_MAKERS AS T1 JOIN MODEL_LIST AS T2 ON T1.Id  =  T2.Maker GROUP BY T1.Id HAVING count(*)  >  3;
```

**Returned.**
```sql
SELECT cm.Id, cm.Maker
FROM car_makers cm
JOIN model_list ml ON cm.Id = ml.Maker
GROUP BY cm.Id, cm.Maker
HAVING COUNT(ml.Model) > 3
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 2 row(s), 2 column(s):

    General Motors | 4
    Chrysler | 6

Returned query gives 2 row(s), 2 column(s):

    4 | gm
    6 | chrysler

Difference: disjoint; 0 row(s) in common, 2 only in the gold, 2 only in the returned result.

### R256  (question 99, database `car_1`)

- Returned by: omnisql-32b/seed101
- Returned in cell: A only
- Class mass: 18/50
- Instances disagreeing: 28 of 60 (47%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Which distinctive models are produced by General Motors or heavier than 3500?

**Gold.**
```sql
SELECT DISTINCT T2.Model FROM CAR_NAMES AS T1 JOIN MODEL_LIST AS T2 ON T1.Model  =  T2.Model JOIN CAR_MAKERS AS T3 ON T2.Maker  =  T3.Id JOIN CARS_DATA AS T4 ON T1.MakeId  =  T4.Id WHERE T3.FullName  =  'General Motors' OR T4.weight  >  3500;
```

**Returned.**
```sql
SELECT DISTINCT cn.Model
FROM car_names cn
JOIN model_list ml ON cn.Model = ml.Model
JOIN car_makers cm ON ml.Maker = cm.Id
WHERE cm.Maker = 'General Motors'

UNION

SELECT DISTINCT cn.Model
FROM car_names cn
JOIN cars_data cd ON cn.MakeId = cd.Id
WHERE cd.Weight > 3500
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 13 row(s), 1 column(s):

    chevrolet
    buick
    ford
    plymouth
    pontiac
    amc
    dodge
    mercury
    oldsmobile
    chrysler
    mercedes-benz
    cadillac
    ... (13 rows total)

Returned query gives 14 row(s), 1 column(s):

    amc
    buick
    cadillac
    chevrolet
    chrysler
    dodge
    ford
    hi
    mercedes
    mercedes-benz
    mercury
    oldsmobile
    ... (14 rows total)

Difference: gold_subset_of_rep; 13 row(s) in common, 0 only in the gold, 1 only in the returned result.

### R257  (question 99, database `car_1`)

- Returned by: omnisql-32b/seed101
- Returned in cell: D only
- Class mass: 6/50
- Instances disagreeing: 12 of 60 (20%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Which distinctive models are produced by General Motors or heavier than 3500?

**Gold.**
```sql
SELECT DISTINCT T2.Model FROM CAR_NAMES AS T1 JOIN MODEL_LIST AS T2 ON T1.Model  =  T2.Model JOIN CAR_MAKERS AS T3 ON T2.Maker  =  T3.Id JOIN CARS_DATA AS T4 ON T1.MakeId  =  T4.Id WHERE T3.FullName  =  'General Motors' OR T4.weight  >  3500;
```

**Returned.**
```sql
SELECT DISTINCT ML.Model
FROM model_list ML
INNER JOIN car_makers CM ON ML.Maker = CM.Id
WHERE CM.FullName = 'General Motors'

UNION

SELECT DISTINCT CN.Model
FROM car_names CN
INNER JOIN cars_data CD ON CN.MakeId = CD.Id
WHERE CD.Weight > 3500
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 13 row(s), 1 column(s):

    chevrolet
    buick
    ford
    plymouth
    pontiac
    amc
    dodge
    mercury
    oldsmobile
    chrysler
    mercedes-benz
    cadillac
    ... (13 rows total)

Returned query gives 14 row(s), 1 column(s):

    amc
    buick
    cadillac
    chevrolet
    chrysler
    dodge
    ford
    hi
    mercedes
    mercedes-benz
    mercury
    oldsmobile
    ... (14 rows total)

Difference: gold_subset_of_rep; 13 row(s) in common, 0 only in the gold, 1 only in the returned result.

### R258  (question 100, database `car_1`)

- Returned by: omnisql-32b/seed101
- Returned in cell: A only
- Class mass: 17/50
- Instances disagreeing: 3 of 60 (5%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the different models created by either General Motors or over 3500 lbs?

**Gold.**
```sql
SELECT DISTINCT T2.Model FROM CAR_NAMES AS T1 JOIN MODEL_LIST AS T2 ON T1.Model  =  T2.Model JOIN CAR_MAKERS AS T3 ON T2.Maker  =  T3.Id JOIN CARS_DATA AS T4 ON T1.MakeId  =  T4.Id WHERE T3.FullName  =  'General Motors' OR T4.weight  >  3500;
```

**Returned.**
```sql
SELECT DISTINCT 
    c.Model
FROM 
    car_names c
JOIN 
    model_list m ON c.Model = m.Model
JOIN 
    car_makers mk ON m.Maker = mk.Id
WHERE 
    mk.FullName = 'General Motors'
UNION
SELECT DISTINCT 
    c.Model
FROM 
    cars_data cd
JOIN 
    car_names c ON cd.Id = c.MakeId
WHERE 
    cd.Weight > 3500
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 13 row(s), 1 column(s):

    chevrolet
    buick
    ford
    plymouth
    pontiac
    amc
    dodge
    mercury
    oldsmobile
    chrysler
    mercedes-benz
    cadillac
    ... (13 rows total)

Returned query gives 14 row(s), 1 column(s):

    amc
    buick
    cadillac
    chevrolet
    chrysler
    dodge
    ford
    hi
    mercedes
    mercedes-benz
    mercury
    oldsmobile
    ... (14 rows total)

Difference: gold_subset_of_rep; 13 row(s) in common, 0 only in the gold, 1 only in the returned result.

### R259  (question 100, database `car_1`)

- Returned by: omnisql-32b/seed101
- Returned in cell: D only
- Class mass: 7/50
- Instances disagreeing: 12 of 60 (20%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the different models created by either General Motors or over 3500 lbs?

**Gold.**
```sql
SELECT DISTINCT T2.Model FROM CAR_NAMES AS T1 JOIN MODEL_LIST AS T2 ON T1.Model  =  T2.Model JOIN CAR_MAKERS AS T3 ON T2.Maker  =  T3.Id JOIN CARS_DATA AS T4 ON T1.MakeId  =  T4.Id WHERE T3.FullName  =  'General Motors' OR T4.weight  >  3500;
```

**Returned.**
```sql
SELECT DISTINCT Model
FROM model_list AS m
JOIN car_makers AS cm ON m.Maker = cm.Id
WHERE cm.FullName = 'General Motors'

UNION

SELECT DISTINCT Model
FROM car_names AS cn
JOIN cars_data AS cd ON cn.MakeId = cd.Id
WHERE cd.Weight > 3500
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 13 row(s), 1 column(s):

    chevrolet
    buick
    ford
    plymouth
    pontiac
    amc
    dodge
    mercury
    oldsmobile
    chrysler
    mercedes-benz
    cadillac
    ... (13 rows total)

Returned query gives 14 row(s), 1 column(s):

    amc
    buick
    cadillac
    chevrolet
    chrysler
    dodge
    ford
    hi
    mercedes
    mercedes-benz
    mercury
    oldsmobile
    ... (14 rows total)

Difference: gold_subset_of_rep; 13 row(s) in common, 0 only in the gold, 1 only in the returned result.

### R260  (question 105, database `car_1`)

- Returned by: omnisql-32b/seed101
- Returned in cell: both A and D
- Class mass: 47/50
- Instances disagreeing: 60 of 60 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** How many nations has more than 2 car makers ?

**Gold.**
```sql
select count(*) from countries as t1 join car_makers as t2 on t1.countryid  =  t2.country group by t1.countryid having count(*)  >  2
```

**Returned.**
```sql
SELECT COUNT(*)
FROM (
    SELECT Country
    FROM car_makers
    GROUP BY Country
    HAVING COUNT(*) > 2
)
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 4 row(s), 1 column(s):

    4
    4
    3
    5

Returned query gives 1 row(s), 1 column(s):

    4

Difference: rep_subset_of_gold; 1 row(s) in common, 2 only in the gold, 0 only in the returned result.

### R261  (question 106, database `car_1`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed202
- Returned in cell: both A and D
- Class mass: 48/50, 45/50
- Instances disagreeing: 60 of 60 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the number of nations with more than 2 car makers ?

**Gold.**
```sql
select count(*) from countries as t1 join car_makers as t2 on t1.countryid  =  t2.country group by t1.countryid having count(*)  >  2
```

**Returned.**
```sql
SELECT COUNT(*) 
FROM (
    SELECT Country 
    FROM car_makers 
    GROUP BY Country 
    HAVING COUNT(*) > 2
)
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 4 row(s), 1 column(s):

    4
    4
    3
    5

Returned query gives 1 row(s), 1 column(s):

    4

Difference: rep_subset_of_gold; 1 row(s) in common, 2 only in the gold, 0 only in the returned result.

### R262  (question 109, database `car_1`)

- Returned by: omnisql-32b/seed101
- Returned in cell: both A and D
- Class mass: 26/50
- Instances disagreeing: 56 of 60 (93%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Which models are lighter than 3500 but not built by the 'Ford Motor Company'?

**Gold.**
```sql
SELECT DISTINCT T1.model FROM MODEL_LIST AS T1 JOIN CAR_NAMES AS T2 ON T1.Model  =  T2.Model JOIN CARS_DATA AS T3 ON T2.MakeId  =  T3.Id JOIN CAR_MAKERS AS T4 ON T1.Maker  =  T4.Id WHERE T3.weight  <  3500 AND T4.FullName != 'Ford Motor Company';
```

**Returned.**
```sql
SELECT cn.Model
FROM cars_data cd
JOIN car_names cn ON cd.Id = cn.MakeId
JOIN model_list ml ON cn.Model = ml.Model
JOIN car_makers cm ON ml.Maker = cm.Id
WHERE cd.Weight < 3500 AND cm.FullName != 'Ford Motor Company'
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 26 row(s), 1 column(s):

    plymouth
    amc
    citroen
    buick
    toyota
    datsun
    volkswagen
    peugeot
    audi
    saab
    bmw
    chevrolet
    ... (26 rows total)

Returned query gives 252 row(s), 1 column(s):

    plymouth
    amc
    citroen
    buick
    toyota
    plymouth
    amc
    datsun
    volkswagen
    peugeot
    audi
    saab
    ... (252 rows total)

Difference: duplicate_multiplicity_only; 26 row(s) in common, 0 only in the gold, 0 only in the returned result.

### R263  (question 114, database `flight_2`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed202, omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 47/50, 46/50, 49/50
- Instances disagreeing: 16 of 56 (29%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What country is Jetblue Airways affiliated with?

**Gold.**
```sql
SELECT Country FROM AIRLINES WHERE Airline  =  "JetBlue Airways"
```

**Returned.**
```sql
SELECT Country
FROM airlines
WHERE Airline = 'Jetblue Airways'
```

**First disagreeing instance** `flight_2.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    USA

Returned query gives 0 row(s), None column(s):

    (no rows)

Difference: rep_empty; 0 row(s) in common, 1 only in the gold, 0 only in the returned result.

### R264  (question 116, database `flight_2`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed202, omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 50/50, 50/50, 49/50
- Instances disagreeing: 16 of 56 (29%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Which abbreviation corresponds to Jetblue Airways?

**Gold.**
```sql
SELECT Abbreviation FROM AIRLINES WHERE Airline  =  "JetBlue Airways"
```

**Returned.**
```sql
SELECT Abbreviation
FROM airlines
WHERE Airline = 'Jetblue Airways'
```

**First disagreeing instance** `flight_2.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    JetBlue

Returned query gives 0 row(s), None column(s):

    (no rows)

Difference: rep_empty; 0 row(s) in common, 1 only in the gold, 0 only in the returned result.

### R265  (question 140, database `flight_2`)

- Returned by: omnisql-32b/seed101
- Returned in cell: both A and D
- Class mass: 47/50
- Instances disagreeing: 8 of 56 (14%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Give the number of Jetblue Airways flights.

**Gold.**
```sql
SELECT count(*) FROM FLIGHTS AS T1 JOIN AIRLINES AS T2 ON T1.Airline  =  T2.uid WHERE T2.Airline = "JetBlue Airways"
```

**Returned.**
```sql
SELECT COUNT(*) AS NumberOfFlights
FROM flights
JOIN airlines ON flights.Airline = airlines.uid
WHERE airlines.Airline = 'Jetblue Airways'
```

**First disagreeing instance** `flight_2.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    100

Returned query gives 1 row(s), 1 column(s):

    0

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R266  (question 191, database `course_teach`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed202, omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 50/50, 50/50, 50/50
- Instances disagreeing: 16 of 25 (64%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** List the name of teachers who are not from Little Lever Urban District.

**Gold.**
```sql
select name from teacher where hometown != "little lever urban district"
```

**Returned.**
```sql
SELECT Name 
FROM teacher 
WHERE Hometown != 'Little Lever Urban District'
```

**First disagreeing instance** `course_teach.sqlite` (this is the shipped benchmark database).

Gold returns 7 row(s), 1 column(s):

    Joseph Huts
    Gustaaf Deloor
    Vicente Carretero
    John Deloor
    Kearsley Brown
    Anne Walker
    Lucy Wong

Returned query gives 6 row(s), 1 column(s):

    Joseph Huts
    Gustaaf Deloor
    Vicente Carretero
    John Deloor
    Kearsley Brown
    Lucy Wong

Difference: rep_subset_of_gold; 6 row(s) in common, 1 only in the gold, 0 only in the returned result.

### R267  (question 192, database `course_teach`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed202, omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 50/50, 50/50, 50/50
- Instances disagreeing: 16 of 25 (64%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the names of the teachers who do not come from Little Lever Urban District?

**Gold.**
```sql
select name from teacher where hometown != "little lever urban district"
```

**Returned.**
```sql
SELECT Name 
FROM teacher 
WHERE Hometown != 'Little Lever Urban District'
```

**First disagreeing instance** `course_teach.sqlite` (this is the shipped benchmark database).

Gold returns 7 row(s), 1 column(s):

    Joseph Huts
    Gustaaf Deloor
    Vicente Carretero
    John Deloor
    Kearsley Brown
    Anne Walker
    Lucy Wong

Returned query gives 6 row(s), 1 column(s):

    Joseph Huts
    Gustaaf Deloor
    Vicente Carretero
    John Deloor
    Kearsley Brown
    Lucy Wong

Difference: rep_subset_of_gold; 6 row(s) in common, 1 only in the gold, 0 only in the returned result.

### R268  (question 213, database `museum_visit`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed202, omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 43/50, 47/50, 44/50
- Instances disagreeing: 35 of 35 (100%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What are the id, name and membership level of people who have paid the largest amount of money overall in all museum tickets?

**Gold.**
```sql
SELECT t2.visitor_id ,  t1.name ,  t1.Level_of_membership FROM visitor AS t1 JOIN visit AS t2 ON t1.id  =  t2.visitor_id GROUP BY t2.visitor_id ORDER BY sum(t2.Total_spent) DESC LIMIT 1
```

**Returned.**
```sql
SELECT 
    visitor.ID, 
    visitor.Name, 
    visitor.Level_of_membership
FROM 
    visit
INNER JOIN 
    visitor 
ON 
    visit.visitor_ID = visitor.ID
GROUP BY 
    visitor.ID
ORDER BY 
    SUM(visit.Total_spent) DESC
LIMIT 1
```

**First disagreeing instance** `museum_visit.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 3 column(s):

    3 | Arjen Robben | 1

Returned query gives 1 row(s), 3 column(s):

    3 | Arjen Robben | 1

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R269  (question 231, database `wta_1`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed202, omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 29/50, 34/50, 28/50
- Instances disagreeing: 33 of 33 (100%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What are the full names of all players, sorted by age?

**Gold.**
```sql
SELECT first_name ,  last_name FROM players ORDER BY birth_date
```

**Returned.**
```sql
SELECT first_name || ' ' || last_name AS full_name
FROM players
ORDER BY strftime('%Y', 'now') - strftime('%Y', birth_date)
```

**First disagreeing instance** `wta_1.sqlite` (this is the shipped benchmark database).

Gold returns 20662 row(s), 2 column(s):

    Thelma | Long
    Pauline | Addie
    Milly | Vagn Nielsen
    Vera | Johansen
    Reiko | Miyagi
    Louise | Brown
    Gertrude | Moran
    Zsuzsa | Kormoczy
    Peggy | Brixhe
    Betty | Pratt
    Doris | Hart
    Dorothy | Knode
    ... (20662 rows total)

Returned query gives 20662 row(s), 1 column(s):

    Martina Hingis
    Mirjana Lucic
    Justine Henin
    Kerry Anne Guse
    Jolene Watanabe Giltz
    Karina Habsudova
    Silvija Talaja
    Alicia Molik
    Tamarine Tanasugarn
    Rita Grande
    Katarina Srebotnik
    Jana Nejedly
    ... (20662 rows total)

Difference: col_count_differs, disjoint; 0 row(s) in common, 20658 only in the gold, 20658 only in the returned result.

### R270  (question 233, database `wta_1`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed202
- Returned in cell: A only
- Class mass: 20/50, 22/50
- Instances disagreeing: 10 of 33 (30%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What are the full names of all left handed players, in order of age?

**Gold.**
```sql
SELECT first_name ,  last_name FROM players WHERE hand  =  'L' ORDER BY birth_date
```

**Returned.**
```sql
SELECT first_name || ' ' || last_name AS full_name
FROM players
WHERE hand = 'L'
ORDER BY strftime('%Y', 'now') - strftime('%Y', birth_date)
```

**First disagreeing instance** `wta_1.sqlite` (this is the shipped benchmark database).

Gold returns 487 row(s), 2 column(s):

    Ann | Jones
    Wendy | Gilchrist
    Martina | Navratilova
    Mary | Carillo
    Katerina | Bohmova
    Petra | Delhees Jauch
    Nancy | Loeffler Caro
    Lise | Gregory
    Rene | Collins
    Nicole | Arendt
    Florencia | Labat
    Sabine | Appelmans
    ... (487 rows total)

Returned query gives 487 row(s), 1 column(s):

    Florencia Labat
    Magui Serna
    Amanda Grahame
    Sabine Appelmans
    Jelena Kostanic Tosic
    Gala Leon Garcia
    Patty Schnyder
    Anne Gaelle Sidot
    Julie Pullin
    Barbara Schwartz
    Anca Barna
    Amelie Cocheteux
    ... (487 rows total)

Difference: col_count_differs, disjoint; 0 row(s) in common, 486 only in the gold, 486 only in the returned result.

### R271  (question 233, database `wta_1`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed202, omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 15/50, 15/50, 20/50
- Instances disagreeing: 10 of 33 (30%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What are the full names of all left handed players, in order of age?

**Gold.**
```sql
SELECT first_name ,  last_name FROM players WHERE hand  =  'L' ORDER BY birth_date
```

**Returned.**
```sql
SELECT first_name || ' ' || last_name AS full_name
FROM players
WHERE hand = 'L'
ORDER BY birth_date ASC
```

**First disagreeing instance** `wta_1.sqlite` (this is the shipped benchmark database).

Gold returns 487 row(s), 2 column(s):

    Ann | Jones
    Wendy | Gilchrist
    Martina | Navratilova
    Mary | Carillo
    Katerina | Bohmova
    Petra | Delhees Jauch
    Nancy | Loeffler Caro
    Lise | Gregory
    Rene | Collins
    Nicole | Arendt
    Florencia | Labat
    Sabine | Appelmans
    ... (487 rows total)

Returned query gives 487 row(s), 1 column(s):

    Ann Jones
    Wendy Gilchrist
    Martina Navratilova
    Mary Carillo
    Katerina Bohmova
    Petra Delhees Jauch
    Nancy Loeffler Caro
    Lise Gregory
    Rene Collins
    Nicole Arendt
    Florencia Labat
    Sabine Appelmans
    ... (487 rows total)

Difference: col_count_differs, disjoint; 0 row(s) in common, 486 only in the gold, 486 only in the returned result.

### R272  (question 235, database `wta_1`)

- Returned by: omnisql-32b/seed101
- Returned in cell: both A and D
- Class mass: 12/49
- Instances disagreeing: 33 of 33 (100%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What is the name of the player who has won the most matches, and how many rank points does this player have?

**Gold.**
```sql
SELECT winner_name ,  winner_rank_points FROM matches GROUP BY winner_name ORDER BY count(*) DESC LIMIT 1
```

**Returned.**
```sql
SELECT 
    p.first_name || ' ' || p.last_name AS player_name,
    r.ranking_points
FROM 
    players p
JOIN 
    rankings r ON p.player_id = r.player_id
JOIN 
    (SELECT 
         winner_id, 
         COUNT(*) AS match_count
     FROM 
         matches
     GROUP BY 
         winner_id
     ORDER BY 
         match_count DESC
     LIMIT 1) top_winner
ON 
    p.player_id = top_winner.winner_id
```

**First disagreeing instance** `wta_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    Angelique Kerber | 3715

Returned query gives 635 row(s), 2 column(s):

    Angelique Kerber | 16
    Angelique Kerber | 16
    Angelique Kerber | 16
    Angelique Kerber | 17
    Angelique Kerber | 17
    Angelique Kerber | 17
    Angelique Kerber | 17
    Angelique Kerber | 17
    Angelique Kerber | 17
    Angelique Kerber | 17
    Angelique Kerber | 17
    Angelique Kerber | 17
    ... (635 rows total)

Difference: gold_subset_of_rep; 1 row(s) in common, 0 only in the gold, 217 only in the returned result.

### R273  (question 252, database `battle_death`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 32/50, 26/50
- Instances disagreeing: 27 of 28 (96%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What is the ship id and name that caused most total injuries?

**Gold.**
```sql
SELECT T2.id ,  T2.name FROM death AS T1 JOIN ship AS t2 ON T1.caused_by_ship_id  =  T2.id GROUP BY T2.id ORDER BY count(*) DESC LIMIT 1
```

**Returned.**
```sql
SELECT 
    ship.id, 
    ship.name 
FROM 
    ship 
INNER JOIN 
    death 
ON 
    ship.id = death.caused_by_ship_id 
GROUP BY 
    ship.id 
ORDER BY 
    SUM(death.injured) DESC 
LIMIT 1
```

**First disagreeing instance** `battle_death.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    5 | Three Brothers

Returned query gives 1 row(s), 2 column(s):

    4 | HMS Avon

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R274  (question 253, database `battle_death`)

- Returned by: omnisql-32b/seed101
- Returned in cell: D only
- Class mass: 19/50
- Instances disagreeing: 17 of 28 (61%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** List the name and date the battle that has lost  Lettice and HMS Atalanta

**Gold.**
```sql
SELECT T1.name ,  T1.date FROM battle AS T1 JOIN ship AS T2 ON T1.id  =  T2.lost_in_battle WHERE T2.name  =  'Lettice' INTERSECT SELECT T1.name ,  T1.date FROM battle AS T1 JOIN ship AS T2 ON T1.id  =  T2.lost_in_battle WHERE T2.name  =  'HMS Atalanta'
```

**Returned.**
```sql
SELECT 
    battle.name, 
    battle.date
FROM 
    ship
INNER JOIN 
    battle 
ON 
    ship.lost_in_battle = battle.id
WHERE 
    ship.name = 'Lettice' OR ship.name = 'HMS Atalanta'
```

**First disagreeing instance** `battle_death.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    Siege of Constantinople | 1235

Returned query gives 2 row(s), 2 column(s):

    Siege of Constantinople | 1235
    Siege of Constantinople | 1235

Difference: duplicate_multiplicity_only; 1 row(s) in common, 0 only in the gold, 0 only in the returned result.

### R275  (question 259, database `student_transcripts_tracking`)

- Returned by: omnisql-32b/seed101
- Returned in cell: both A and D
- Class mass: 50/50
- Instances disagreeing: 22 of 55 (40%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find the last name of the students who currently live in North Carolina but have not registered in any degree program.

**Gold.**
```sql
SELECT T1.last_name FROM Students AS T1 JOIN Addresses AS T2 ON T1.current_address_id  =  T2.address_id WHERE T2.state_province_county  =  'NorthCarolina' EXCEPT SELECT DISTINCT T3.last_name FROM Students AS T3 JOIN Student_Enrolment AS T4 ON T3.student_id  =  T4.student_id
```

**Returned.**
```sql
SELECT s.last_name
FROM Students s
JOIN Addresses a ON s.current_address_id = a.address_id
WHERE a.state_province_county = 'North Carolina'
AND s.student_id NOT IN (
    SELECT se.student_id
    FROM Student_Enrolment se
)
```

**First disagreeing instance** `student_transcripts_tracking.sqlite` (this is the shipped benchmark database).

Gold returns 2 row(s), 1 column(s):

    Gleichner
    Weimann

Returned query gives 0 row(s), None column(s):

    (no rows)

Difference: rep_empty; 0 row(s) in common, 2 only in the gold, 0 only in the returned result.

### R276  (question 260, database `student_transcripts_tracking`)

- Returned by: omnisql-32b/seed101
- Returned in cell: both A and D
- Class mass: 50/50
- Instances disagreeing: 22 of 55 (40%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the last name of the students who live in North Carolina but have not registered in any degree programs?

**Gold.**
```sql
SELECT T1.last_name FROM Students AS T1 JOIN Addresses AS T2 ON T1.current_address_id  =  T2.address_id WHERE T2.state_province_county  =  'NorthCarolina' EXCEPT SELECT DISTINCT T3.last_name FROM Students AS T3 JOIN Student_Enrolment AS T4 ON T3.student_id  =  T4.student_id
```

**Returned.**
```sql
SELECT s.last_name
FROM Students s
JOIN Addresses a ON s.current_address_id = a.address_id
LEFT JOIN Student_Enrolment se ON s.student_id = se.student_id
WHERE a.state_province_county = 'North Carolina'
AND se.student_id IS NULL
```

**First disagreeing instance** `student_transcripts_tracking.sqlite` (this is the shipped benchmark database).

Gold returns 2 row(s), 1 column(s):

    Gleichner
    Weimann

Returned query gives 0 row(s), None column(s):

    (no rows)

Difference: rep_empty; 0 row(s) in common, 2 only in the gold, 0 only in the returned result.

### R277  (question 266, database `student_transcripts_tracking`)

- Returned by: omnisql-32b/seed101
- Returned in cell: A only
- Class mass: 25/50
- Instances disagreeing: 55 of 55 (100%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Which place holds the most number of students currently? List the id and all lines.

**Gold.**
```sql
SELECT T1.address_id ,  T1.line_1 ,  T1.line_2 FROM Addresses AS T1 JOIN Students AS T2 ON T1.address_id  =  T2.current_address_id GROUP BY T1.address_id ORDER BY count(*) DESC LIMIT 1
```

**Returned.**
```sql
SELECT a.address_id, a.line_1, a.line_2, a.line_3
FROM Addresses a
JOIN Students s ON a.address_id = s.current_address_id
GROUP BY a.address_id, a.line_1, a.line_2, a.line_3
ORDER BY COUNT(s.student_id) DESC
LIMIT 1
```

**First disagreeing instance** `student_transcripts_tracking.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 3 column(s):

    9 | 0643 Muller Vista | Suite 383

Returned query gives 1 row(s), 4 column(s):

    9 | 0643 Muller Vista | Suite 383 | NULL

Difference: col_count_differs, disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R278  (question 266, database `student_transcripts_tracking`)

- Returned by: omnisql-32b/seed101
- Returned in cell: D only
- Class mass: 15/50
- Instances disagreeing: 55 of 55 (100%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Which place holds the most number of students currently? List the id and all lines.

**Gold.**
```sql
SELECT T1.address_id ,  T1.line_1 ,  T1.line_2 FROM Addresses AS T1 JOIN Students AS T2 ON T1.address_id  =  T2.current_address_id GROUP BY T1.address_id ORDER BY count(*) DESC LIMIT 1
```

**Returned.**
```sql
SELECT 
    Addresses.address_id, 
    Addresses.line_1, 
    Addresses.line_2, 
    Addresses.line_3
FROM 
    Addresses
JOIN 
    Students ON Addresses.address_id = Students.current_address_id
GROUP BY 
    Addresses.address_id
ORDER BY 
    COUNT(Students.student_id) DESC
LIMIT 1
```

**First disagreeing instance** `student_transcripts_tracking.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 3 column(s):

    9 | 0643 Muller Vista | Suite 383

Returned query gives 1 row(s), 4 column(s):

    9 | 0643 Muller Vista | Suite 383 | NULL

Difference: col_count_differs, disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R279  (question 267, database `student_transcripts_tracking`)

- Returned by: omnisql-32b/seed101
- Returned in cell: D only
- Class mass: 16/50
- Instances disagreeing: 31 of 55 (56%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What is the id, line 1, and line 2 of the place with the most students?

**Gold.**
```sql
SELECT T1.address_id ,  T1.line_1 ,  T1.line_2 FROM Addresses AS T1 JOIN Students AS T2 ON T1.address_id  =  T2.current_address_id GROUP BY T1.address_id ORDER BY count(*) DESC LIMIT 1
```

**Returned.**
```sql
SELECT Addresses.address_id, Addresses.line_1, Addresses.line_2
FROM Addresses
JOIN Students ON Addresses.address_id = Students.current_address_id
GROUP BY Addresses.address_id, Addresses.line_1, Addresses.line_2
ORDER BY COUNT(Students.student_id) DESC
LIMIT 1
```

**First disagreeing instance** `student_transcripts_trackingv5080.sqlite`.

Gold returns 1 row(s), 3 column(s):

    9700166583 | 10 | 6

Returned query gives 1 row(s), 3 column(s):

    -7035591255 | 09700166582 | Apt. 335

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R280  (question 268, database `student_transcripts_tracking`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed202
- Returned in cell: both A and D
- Class mass: 27/50, 34/50
- Instances disagreeing: 40 of 55 (73%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find the semester when both Master students and Bachelor students got enrolled in.

**Gold.**
```sql
SELECT DISTINCT T2.semester_id FROM Degree_Programs AS T1 JOIN Student_Enrolment AS T2 ON T1.degree_program_id  =  T2.degree_program_id WHERE degree_summary_name  =  'Master' INTERSECT SELECT DISTINCT T2.semester_id FROM Degree_Programs AS T1 JOIN Student_Enrolment AS T2 ON T1.degree_program_id  =  T2.degree_program_id WHERE degree_summary_name  =  'Bachelor'
```

**Returned.**
```sql
SELECT s.semester_name
FROM Student_Enrolment se
JOIN Degree_Programs dp ON se.degree_program_id = dp.degree_program_id
JOIN Semesters s ON se.semester_id = s.semester_id
WHERE dp.degree_summary_name = 'Master'
INTERSECT
SELECT s.semester_name
FROM Student_Enrolment se
JOIN Degree_Programs dp ON se.degree_program_id = dp.degree_program_id
JOIN Semesters s ON se.semester_id = s.semester_id
WHERE dp.degree_summary_name = 'Bachelor'
```

**First disagreeing instance** `student_transcripts_tracking.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    13

Returned query gives 1 row(s), 1 column(s):

    fall 2018

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R281  (question 269, database `student_transcripts_tracking`)

- Returned by: omnisql-32b/seed101
- Returned in cell: both A and D
- Class mass: 27/50
- Instances disagreeing: 31 of 55 (56%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the id of the semester that had both Masters and Bachelors students enrolled?

**Gold.**
```sql
SELECT DISTINCT T2.semester_id FROM Degree_Programs AS T1 JOIN Student_Enrolment AS T2 ON T1.degree_program_id  =  T2.degree_program_id WHERE degree_summary_name  =  'Master' INTERSECT SELECT DISTINCT T2.semester_id FROM Degree_Programs AS T1 JOIN Student_Enrolment AS T2 ON T1.degree_program_id  =  T2.degree_program_id WHERE degree_summary_name  =  'Bachelor'
```

**Returned.**
```sql
SELECT se.semester_id
FROM Student_Enrolment se
JOIN Degree_Programs dp ON se.degree_program_id = dp.degree_program_id
WHERE dp.degree_summary_name IN ('Masters', 'Bachelors')
GROUP BY se.semester_id
HAVING COUNT(DISTINCT dp.degree_summary_name) = 2
```

**First disagreeing instance** `student_transcripts_tracking.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    13

Returned query gives 0 row(s), None column(s):

    (no rows)

Difference: rep_empty; 0 row(s) in common, 1 only in the gold, 0 only in the returned result.

### R282  (question 270, database `student_transcripts_tracking`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 49/50, 49/50
- Instances disagreeing: 16 of 55 (29%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find the first name of the students who permanently live in Haiti or have the cell phone number 09700166582.

**Gold.**
```sql
select t1.first_name from students as t1 join addresses as t2 on t1.permanent_address_id  =  t2.address_id where t2.country  =  'haiti' or t1.cell_mobile_number  =  '09700166582'
```

**Returned.**
```sql
SELECT s.first_name
FROM Students s
JOIN Addresses a ON s.permanent_address_id = a.address_id
WHERE a.country = 'Haiti' OR s.cell_mobile_number = '09700166582'
```

**First disagreeing instance** `student_transcripts_tracking.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    Jarvis

Returned query gives 4 row(s), 1 column(s):

    Hobart
    Warren
    Jarvis
    Delaney

Difference: gold_subset_of_rep; 1 row(s) in common, 0 only in the gold, 3 only in the returned result.

### R283  (question 271, database `student_transcripts_tracking`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed202
- Returned in cell: both A and D
- Class mass: 50/50, 50/50
- Instances disagreeing: 16 of 55 (29%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the first names of the students who live in Haiti permanently or have the cell phone number 09700166582?

**Gold.**
```sql
select t1.first_name from students as t1 join addresses as t2 on t1.permanent_address_id  =  t2.address_id where t2.country  =  'haiti' or t1.cell_mobile_number  =  '09700166582'
```

**Returned.**
```sql
SELECT s.first_name
FROM Students s
JOIN Addresses a ON s.permanent_address_id = a.address_id
WHERE a.country = 'Haiti' OR s.cell_mobile_number = '09700166582'
```

**First disagreeing instance** `student_transcripts_tracking.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    Jarvis

Returned query gives 4 row(s), 1 column(s):

    Hobart
    Warren
    Jarvis
    Delaney

Difference: gold_subset_of_rep; 1 row(s) in common, 0 only in the gold, 3 only in the returned result.

### R284  (question 311, database `tvshow`)

- Returned by: omnisql-32b/seed101
- Returned in cell: both A and D
- Class mass: 16/50
- Instances disagreeing: 20 of 25 (80%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find the series name and country of the tv channel that is playing some cartoons  Ben Jones and Michael Chang directs?

**Gold.**
```sql
SELECT T1.series_name ,  T1.country FROM TV_Channel AS T1 JOIN cartoon AS T2 ON T1.id = T2.Channel WHERE T2.directed_by  =  'Michael Chang' INTERSECT SELECT T1.series_name ,  T1.country FROM TV_Channel AS T1 JOIN cartoon AS T2 ON T1.id = T2.Channel WHERE T2.directed_by  =  'Ben Jones'
```

**Returned.**
```sql
SELECT 
    TV_Channel.series_name, 
    TV_Channel.Country
FROM 
    Cartoon
INNER JOIN 
    TV_Channel 
ON 
    Cartoon.Channel = TV_Channel.id
WHERE 
    Cartoon.Directed_by LIKE '%Ben Jones%' 
    AND Cartoon.Directed_by LIKE '%Michael Chang%'
```

**First disagreeing instance** `tvshow.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    MTV Dance | United Kingdom

Returned query gives 0 row(s), None column(s):

    (no rows)

Difference: rep_empty; 0 row(s) in common, 1 only in the gold, 0 only in the returned result.

### R285  (question 312, database `tvshow`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed202
- Returned in cell: both A and D
- Class mass: 20/50, 20/50
- Instances disagreeing: 20 of 25 (80%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the series name and country of all TV channels that are playing cartoons  Ben Jones and Michael Chang directs?

**Gold.**
```sql
SELECT T1.series_name ,  T1.country FROM TV_Channel AS T1 JOIN cartoon AS T2 ON T1.id = T2.Channel WHERE T2.directed_by  =  'Michael Chang' INTERSECT SELECT T1.series_name ,  T1.country FROM TV_Channel AS T1 JOIN cartoon AS T2 ON T1.id = T2.Channel WHERE T2.directed_by  =  'Ben Jones'
```

**Returned.**
```sql
SELECT 
    TV_Channel.series_name, 
    TV_Channel.Country
FROM 
    Cartoon
INNER JOIN 
    TV_Channel 
ON 
    Cartoon.Channel = TV_Channel.id
WHERE 
    Cartoon.Directed_by LIKE '%Ben Jones%' 
    AND Cartoon.Directed_by LIKE '%Michael Chang%'
```

**First disagreeing instance** `tvshow.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    MTV Dance | United Kingdom

Returned query gives 0 row(s), None column(s):

    (no rows)

Difference: rep_empty; 0 row(s) in common, 1 only in the gold, 0 only in the returned result.

### R286  (question 336, database `world_1`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed202, omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 31/50, 41/50, 34/50
- Instances disagreeing: 39 of 46 (85%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** How many republic countries are there?

**Gold.**
```sql
SELECT count(*) FROM country WHERE GovernmentForm  =  "Republic"
```

**Returned.**
```sql
SELECT COUNT(*) 
FROM country 
WHERE GovernmentForm LIKE '%Republic%'
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    122

Returned query gives 1 row(s), 1 column(s):

    143

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R287  (question 357, database `world_1`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed202, omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 30/50, 34/50, 27/50
- Instances disagreeing: 5 of 46 (11%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Give the average life expectancy for countries in Africa which are republics?

**Gold.**
```sql
SELECT avg(LifeExpectancy) FROM country WHERE Continent  =  "Africa" AND GovernmentForm  =  "Republic"
```

**Returned.**
```sql
SELECT AVG(LifeExpectancy) 
FROM country 
WHERE Continent = 'Africa' 
  AND GovernmentForm LIKE '%Republic%'
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    50.84347826086957

Returned query gives 1 row(s), 1 column(s):

    51.06122448979592

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R288  (question 362, database `world_1`)

- Returned by: omnisql-32b/seed101
- Returned in cell: A only
- Class mass: 29/50
- Instances disagreeing: 5 of 46 (11%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the average GNP and total population in all US territory nations?

**Gold.**
```sql
SELECT avg(GNP) ,  sum(population) FROM country WHERE GovernmentForm  =  "US Territory"
```

**Returned.**
```sql
SELECT AVG(GNP) AS AverageGNP, SUM(Population) AS TotalPopulation
FROM country
WHERE Region = 'US Territory'
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    510.3333333333333 | 329000

Returned query gives 1 row(s), 2 column(s):

    NULL | NULL

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R289  (question 362, database `world_1`)

- Returned by: omnisql-32b/seed101
- Returned in cell: D only
- Class mass: 23/50
- Instances disagreeing: 5 of 46 (11%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the average GNP and total population in all US territory nations?

**Gold.**
```sql
SELECT avg(GNP) ,  sum(population) FROM country WHERE GovernmentForm  =  "US Territory"
```

**Returned.**
```sql
SELECT AVG(GNP) AS AverageGNP, SUM(Population) AS TotalPopulation
FROM country
WHERE GovernmentForm = 'US territory'
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    510.3333333333333 | 329000

Returned query gives 1 row(s), 2 column(s):

    NULL | NULL

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R290  (question 363, database `world_1`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 16/47, 22/46
- Instances disagreeing: 5 of 46 (11%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Give the mean GNP and total population of nations which are considered US territory.

**Gold.**
```sql
SELECT avg(GNP) ,  sum(population) FROM country WHERE GovernmentForm  =  "US Territory"
```

**Returned.**
```sql
SELECT AVG(GNP) AS MeanGNP, SUM(Population) AS TotalPopulation
FROM country
WHERE Code2 = 'US'
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    510.3333333333333 | 329000

Returned query gives 1 row(s), 2 column(s):

    8510700.0 | 278357000

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R291  (question 370, database `world_1`)

- Returned by: omnisql-32b/seed101
- Returned in cell: both A and D
- Class mass: 44/50
- Instances disagreeing: 39 of 46 (85%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What is name of the nation that speaks the largest number of languages?

**Gold.**
```sql
SELECT T1.Name FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code  =  T2.CountryCode GROUP BY T1.Name ORDER BY COUNT(*) DESC LIMIT 1
```

**Returned.**
```sql
SELECT 
    c.Name
FROM 
    country AS c
INNER JOIN 
    countrylanguage AS cl
ON 
    c.Code = cl.CountryCode
GROUP BY 
    c.Code
ORDER BY 
    COUNT(DISTINCT cl.Language) DESC
LIMIT 1
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    United States

Returned query gives 1 row(s), 1 column(s):

    Canada

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R292  (question 371, database `world_1`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 40/50, 42/50
- Instances disagreeing: 39 of 46 (85%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Give the name of the nation that uses the greatest amount of languages.

**Gold.**
```sql
SELECT T1.Name FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code  =  T2.CountryCode GROUP BY T1.Name ORDER BY COUNT(*) DESC LIMIT 1
```

**Returned.**
```sql
SELECT country.Name
FROM country
INNER JOIN countrylanguage ON country.Code = countrylanguage.CountryCode
GROUP BY country.Code
ORDER BY COUNT(countrylanguage.Language) DESC
LIMIT 1
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    United States

Returned query gives 1 row(s), 1 column(s):

    Canada

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R293  (question 372, database `world_1`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed202, omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 35/50, 31/49, 30/50
- Instances disagreeing: 46 of 46 (100%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Which continent has the most diverse languages?

**Gold.**
```sql
SELECT T1.Continent FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code  =  T2.CountryCode GROUP BY T1.Continent ORDER BY COUNT(*) DESC LIMIT 1
```

**Returned.**
```sql
SELECT 
    c.Continent, 
    COUNT(DISTINCT cl.Language) AS LanguageCount
FROM 
    country AS c
INNER JOIN 
    countrylanguage AS cl
ON 
    c.Code = cl.CountryCode
GROUP BY 
    c.Continent
ORDER BY 
    LanguageCount DESC
LIMIT 1
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    Africa

Returned query gives 1 row(s), 2 column(s):

    Africa | 215

Difference: col_count_differs, disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R294  (question 373, database `world_1`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed202, omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 28/48, 39/50, 34/48
- Instances disagreeing: 46 of 46 (100%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Which continent speaks the most languages?

**Gold.**
```sql
SELECT T1.Continent FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code  =  T2.CountryCode GROUP BY T1.Continent ORDER BY COUNT(*) DESC LIMIT 1
```

**Returned.**
```sql
SELECT 
    c.Continent, 
    COUNT(DISTINCT cl.Language) AS LanguageCount
FROM 
    country AS c
INNER JOIN 
    countrylanguage AS cl
ON 
    c.Code = cl.CountryCode
GROUP BY 
    c.Continent
ORDER BY 
    LanguageCount DESC
LIMIT 1
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    Africa

Returned query gives 1 row(s), 2 column(s):

    Africa | 215

Difference: col_count_differs, disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R295  (question 382, database `world_1`)

- Returned by: omnisql-32b/seed101
- Returned in cell: both A and D
- Class mass: 47/50
- Instances disagreeing: 22 of 46 (48%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the countries where either English or Dutch is officially spoken ?

**Gold.**
```sql
select t1.name from country as t1 join countrylanguage as t2 on t1.code  =  t2.countrycode where t2.language  =  "english" and isofficial  =  "t" union select t1.name from country as t1 join countrylanguage as t2 on t1.code  =  t2.countrycode where t2.language  =  "dutch" and isofficial  =  "t"
```

**Returned.**
```sql
SELECT DISTINCT country.Name
FROM country
INNER JOIN countrylanguage
ON country.Code = countrylanguage.CountryCode
WHERE (countrylanguage.Language = 'English' OR countrylanguage.Language = 'Dutch')
  AND countrylanguage.IsOfficial = 'T'
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 0 row(s), None column(s):

    (no rows)

Returned query gives 48 row(s), 1 column(s):

    Aruba
    Anguilla
    Netherlands Antilles
    American Samoa
    Antigua and Barbuda
    Australia
    Belgium
    Belize
    Bermuda
    Barbados
    Canada
    Cocos (Keeling) Islands
    ... (48 rows total)

Difference: gold_empty; 0 row(s) in common, 0 only in the gold, 48 only in the returned result.

### R296  (question 383, database `world_1`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 36/50, 37/50
- Instances disagreeing: 31 of 46 (67%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Which language is the most popular on Asian ?

**Gold.**
```sql
SELECT T2.Language FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code  =  T2.CountryCode WHERE T1.Continent  =  "Asia" GROUP BY T2.Language ORDER BY COUNT (*) DESC LIMIT 1
```

**Returned.**
```sql
SELECT cl.Language
FROM country AS c
INNER JOIN countrylanguage AS cl ON c.Code = cl.CountryCode
WHERE c.Continent = 'Asia'
ORDER BY cl.Percentage DESC
LIMIT 1
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    Arabic

Returned query gives 1 row(s), 1 column(s):

    Dhivehi

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R297  (question 387, database `world_1`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed202, omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 48/50, 50/50, 48/50
- Instances disagreeing: 37 of 46 (80%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Find the city with the most people that uses English.

**Gold.**
```sql
SELECT T1.Name ,  T1.Population FROM city AS T1 JOIN countrylanguage AS T2 ON T1.CountryCode  =  T2.CountryCode WHERE T2.Language  =  "English" ORDER BY T1.Population DESC LIMIT 1
```

**Returned.**
```sql
SELECT city.Name
FROM city
INNER JOIN countrylanguage ON city.CountryCode = countrylanguage.CountryCode
WHERE countrylanguage.Language = 'English'
ORDER BY city.Population DESC
LIMIT 1
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    New York | 8008278

Returned query gives 1 row(s), 1 column(s):

    New York

Difference: col_count_differs, disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R298  (question 388, database `world_1`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed202, omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 48/50, 47/50, 50/50
- Instances disagreeing: 37 of 46 (80%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What is the most populace city that speaks English?

**Gold.**
```sql
SELECT T1.Name ,  T1.Population FROM city AS T1 JOIN countrylanguage AS T2 ON T1.CountryCode  =  T2.CountryCode WHERE T2.Language  =  "English" ORDER BY T1.Population DESC LIMIT 1
```

**Returned.**
```sql
SELECT city.Name
FROM city
INNER JOIN countrylanguage ON city.CountryCode = countrylanguage.CountryCode
WHERE countrylanguage.Language = 'English'
ORDER BY city.Population DESC
LIMIT 1
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    New York | 8008278

Returned query gives 1 row(s), 1 column(s):

    New York

Difference: col_count_differs, disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R299  (question 390, database `world_1`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed202, omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 37/50, 35/50, 37/50
- Instances disagreeing: 46 of 46 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is average life expectancy in the countries where English is not used officially ?

**Gold.**
```sql
SELECT avg(LifeExpectancy) FROM country WHERE Name NOT IN (SELECT T1.Name FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code  =  T2.CountryCode WHERE T2.Language  =  "English" AND T2.IsOfficial  =  "T")
```

**Returned.**
```sql
SELECT AVG(country.LifeExpectancy)
FROM country
INNER JOIN countrylanguage
ON country.Code = countrylanguage.CountryCode
WHERE countrylanguage.Language = 'English' AND countrylanguage.IsOfficial = 'F'
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    65.4827027027027

Returned query gives 1 row(s), 1 column(s):

    74.95

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R300  (question 391, database `world_1`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed202, omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 25/50, 23/50, 18/50
- Instances disagreeing: 46 of 46 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Give the mean life expectancy of countries in which English is not officially spoken .

**Gold.**
```sql
SELECT avg(LifeExpectancy) FROM country WHERE Name NOT IN (SELECT T1.Name FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code  =  T2.CountryCode WHERE T2.Language  =  "English" AND T2.IsOfficial  =  "T")
```

**Returned.**
```sql
SELECT AVG(country.LifeExpectancy)
FROM country
INNER JOIN countrylanguage
ON country.Code = countrylanguage.CountryCode
WHERE countrylanguage.Language = 'English' AND countrylanguage.IsOfficial = 'F'
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    65.4827027027027

Returned query gives 1 row(s), 1 column(s):

    74.95

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R301  (question 398, database `world_1`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed202
- Returned in cell: both A and D
- Class mass: 49/50, 49/50
- Instances disagreeing: 37 of 46 (80%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the countries that have greater surface area than any country in Europe?

**Gold.**
```sql
SELECT Name FROM country WHERE SurfaceArea  >  (SELECT min(SurfaceArea) FROM country WHERE Continent  =  "Europe")
```

**Returned.**
```sql
SELECT Name 
FROM country 
WHERE SurfaceArea > (SELECT MAX(SurfaceArea) FROM country WHERE Continent = 'Europe')
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 238 row(s), 1 column(s):

    Aruba
    Afghanistan
    Angola
    Anguilla
    Albania
    Andorra
    Netherlands Antilles
    United Arab Emirates
    Argentina
    Armenia
    American Samoa
    Antarctica
    ... (238 rows total)

Returned query gives 0 row(s), None column(s):

    (no rows)

Difference: rep_empty; 0 row(s) in common, 238 only in the gold, 0 only in the returned result.

### R302  (question 399, database `world_1`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed202, omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 48/50, 50/50, 49/50
- Instances disagreeing: 37 of 46 (80%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Which countries larger than that of any country in Europe by land?

**Gold.**
```sql
SELECT Name FROM country WHERE SurfaceArea  >  (SELECT min(SurfaceArea) FROM country WHERE Continent  =  "Europe")
```

**Returned.**
```sql
SELECT Name
FROM country
WHERE SurfaceArea > (
    SELECT MAX(SurfaceArea)
    FROM country
    WHERE Continent = 'Europe'
)
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 238 row(s), 1 column(s):

    Aruba
    Afghanistan
    Angola
    Anguilla
    Albania
    Andorra
    Netherlands Antilles
    United Arab Emirates
    Argentina
    Armenia
    American Samoa
    Antarctica
    ... (238 rows total)

Returned query gives 0 row(s), None column(s):

    (no rows)

Difference: rep_empty; 0 row(s) in common, 238 only in the gold, 0 only in the returned result.

### R303  (question 403, database `world_1`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed202
- Returned in cell: both A and D
- Class mass: 50/50, 49/50
- Instances disagreeing: 29 of 46 (63%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the Asian countries have more people than that of any country in Africa?

**Gold.**
```sql
SELECT Name FROM country WHERE Continent  =  "Asia"  AND population  >  (SELECT min(population) FROM country WHERE Continent  =  "Africa")
```

**Returned.**
```sql
SELECT Name 
FROM country 
WHERE Continent = 'Asia' 
  AND Population > (SELECT MAX(Population) FROM country WHERE Continent = 'Africa')
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 51 row(s), 1 column(s):

    Afghanistan
    United Arab Emirates
    Armenia
    Azerbaijan
    Bangladesh
    Bahrain
    Brunei
    Bhutan
    China
    Cyprus
    Georgia
    Hong Kong
    ... (51 rows total)

Returned query gives 6 row(s), 1 column(s):

    Bangladesh
    China
    Indonesia
    India
    Japan
    Pakistan

Difference: rep_subset_of_gold; 6 row(s) in common, 45 only in the gold, 0 only in the returned result.

### R304  (question 404, database `world_1`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed202, omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 20/50, 18/50, 22/50
- Instances disagreeing: 32 of 46 (70%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the country codes for countries that do not speak English?

**Gold.**
```sql
SELECT CountryCode FROM countrylanguage EXCEPT SELECT CountryCode FROM countrylanguage WHERE LANGUAGE  =  "English"
```

**Returned.**
```sql
SELECT Code 
FROM country 
WHERE Code NOT IN (
    SELECT CountryCode 
    FROM countrylanguage 
    WHERE Language = 'English'
)
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 173 row(s), 1 column(s):

    AFG
    AGO
    ALB
    AND
    ARE
    ARG
    ARM
    AUT
    AZE
    BDI
    BEL
    BEN
    ... (173 rows total)

Returned query gives 179 row(s), 1 column(s):

    AFG
    AGO
    ALB
    AND
    ARE
    ARG
    ARM
    ATA
    ATF
    AUT
    AZE
    BDI
    ... (179 rows total)

Difference: gold_subset_of_rep; 173 row(s) in common, 0 only in the gold, 6 only in the returned result.

### R305  (question 405, database `world_1`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed202
- Returned in cell: both A and D
- Class mass: 19/50, 19/50
- Instances disagreeing: 32 of 46 (70%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Return the country codes for countries that do not speak English.

**Gold.**
```sql
SELECT CountryCode FROM countrylanguage EXCEPT SELECT CountryCode FROM countrylanguage WHERE LANGUAGE  =  "English"
```

**Returned.**
```sql
SELECT Code 
FROM country 
WHERE Code NOT IN (
    SELECT CountryCode 
    FROM countrylanguage 
    WHERE Language = 'English'
)
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 173 row(s), 1 column(s):

    AFG
    AGO
    ALB
    AND
    ARE
    ARG
    ARM
    AUT
    AZE
    BDI
    BEL
    BEN
    ... (173 rows total)

Returned query gives 179 row(s), 1 column(s):

    AFG
    AGO
    ALB
    AND
    ARE
    ARG
    ARM
    ATA
    ATF
    AUT
    AZE
    BDI
    ... (179 rows total)

Difference: gold_subset_of_rep; 173 row(s) in common, 0 only in the gold, 6 only in the returned result.

### R306  (question 407, database `world_1`)

- Returned by: omnisql-32b/seed101
- Returned in cell: both A and D
- Class mass: 18/50
- Instances disagreeing: 41 of 46 (89%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Give the country codes for countries in which people does not speak English.

**Gold.**
```sql
SELECT DISTINCT CountryCode FROM countrylanguage WHERE LANGUAGE != "English"
```

**Returned.**
```sql
SELECT CountryCode 
FROM countrylanguage 
EXCEPT 
SELECT CountryCode 
FROM countrylanguage 
WHERE Language = 'English'
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 223 row(s), 1 column(s):

    ABW
    AFG
    AGO
    ALB
    AND
    ANT
    ARE
    ARG
    ARM
    ASM
    ATG
    AUS
    ... (223 rows total)

Returned query gives 173 row(s), 1 column(s):

    AFG
    AGO
    ALB
    AND
    ARE
    ARG
    ARM
    AUT
    AZE
    BDI
    BEL
    BEN
    ... (173 rows total)

Difference: rep_subset_of_gold; 173 row(s) in common, 50 only in the gold, 0 only in the returned result.

### R307  (question 410, database `world_1`)

- Returned by: omnisql-32b/seed101
- Returned in cell: both A and D
- Class mass: 27/50
- Instances disagreeing: 9 of 46 (20%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Which cities are in European countries where English is not spoken officially?

**Gold.**
```sql
SELECT DISTINCT T2.Name FROM country AS T1 JOIN city AS T2 ON T2.CountryCode  =  T1.Code WHERE T1.Continent  =  'Europe' AND T1.Name NOT IN (SELECT T3.Name FROM country AS T3 JOIN countrylanguage AS T4 ON T3.Code  =  T4.CountryCode WHERE T4.IsOfficial  =  'T' AND T4.Language  =  'English')
```

**Returned.**
```sql
SELECT c.Name
FROM city AS c
INNER JOIN country AS co ON c.CountryCode = co.Code
WHERE co.Continent = 'Europe'
  AND co.Code NOT IN (
      SELECT cl.CountryCode
      FROM countrylanguage AS cl
      WHERE cl.Language = 'English' AND cl.IsOfficial = 'T'
  )
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 753 row(s), 1 column(s):

    Amsterdam
    Rotterdam
    Haag
    Utrecht
    Eindhoven
    Tilburg
    Groningen
    Breda
    Apeldoorn
    Nijmegen
    Enschede
    Haarlem
    ... (753 rows total)

Returned query gives 755 row(s), 1 column(s):

    Tirana
    Andorra la Vella
    Wien
    Graz
    Linz
    Salzburg
    Innsbruck
    Klagenfurt
    Antwerpen
    Gent
    Charleroi
    Liège
    ... (755 rows total)

Difference: duplicate_multiplicity_only; 753 row(s) in common, 0 only in the gold, 0 only in the returned result.

### R308  (question 411, database `world_1`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed202, omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 50/50, 50/50, 50/50
- Instances disagreeing: 1 of 46 (2%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Whic`h unique cities are in  Asian countries where Chinese is the official ?

**Gold.**
```sql
select distinct t3.name from country as t1 join countrylanguage as t2 on t1.code  =  t2.countrycode join city as t3 on t1.code  =  t3.countrycode where t2.isofficial  =  't' and t2.language  =  'chinese' and t1.continent  =  "asia"
```

**Returned.**
```sql
SELECT DISTINCT city.Name
FROM city
INNER JOIN country ON city.CountryCode = country.Code
INNER JOIN countrylanguage ON country.Code = countrylanguage.CountryCode
WHERE country.Continent = 'Asia'
  AND countrylanguage.Language = 'Chinese'
  AND countrylanguage.IsOfficial = 'T'
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 0 row(s), None column(s):

    (no rows)

Returned query gives 359 row(s), 1 column(s):

    Shanghai
    Peking
    Chongqing
    Tianjin
    Wuhan
    Harbin
    Shenyang
    Kanton [Guangzhou]
    Chengdu
    Nanking [Nanjing]
    Changchun
    Xi´an
    ... (359 rows total)

Difference: gold_empty; 0 row(s) in common, 0 only in the gold, 359 only in the returned result.

### R309  (question 413, database `world_1`)

- Returned by: omnisql-32b/seed101
- Returned in cell: both A and D
- Class mass: 48/50
- Instances disagreeing: 44 of 46 (96%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What are the name, independence year, and surface area of the country with the least number of nationalities?

**Gold.**
```sql
SELECT Name ,  SurfaceArea ,  IndepYear FROM country ORDER BY Population LIMIT 1
```

**Returned.**
```sql
SELECT 
    c.Name, 
    c.IndepYear, 
    c.SurfaceArea
FROM 
    country AS c
INNER JOIN 
    countrylanguage AS cl
ON 
    c.Code = cl.CountryCode
GROUP BY 
    c.Code
ORDER BY 
    COUNT(cl.Language) ASC
LIMIT 1
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 3 column(s):

    Antarctica | 13120000.0 | NULL

Returned query gives 1 row(s), 3 column(s):

    Anguilla | NULL | 96.0

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R310  (question 427, database `world_1`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed202, omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 49/50, 48/50, 45/50
- Instances disagreeing: 40 of 46 (87%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the total population and average area of countries in North America who is bigger than 3000 square miles

**Gold.**
```sql
select sum(population) ,  avg(surfacearea) from country where continent  =  "north america" and surfacearea  >  3000
```

**Returned.**
```sql
SELECT 
    SUM(Population) AS TotalPopulation, 
    AVG(SurfaceArea) AS AverageSurfaceArea
FROM 
    country
WHERE 
    Continent = 'North America' 
    AND SurfaceArea > 3000
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    NULL | NULL

Returned query gives 1 row(s), 2 column(s):

    480753000 | 1344763.7222222222

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R311  (question 428, database `world_1`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed202, omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 42/50, 41/50, 44/50
- Instances disagreeing: 40 of 46 (87%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Give the total population and average  corresponding to countries in Noth America that is bigger than 3000 square miles.

**Gold.**
```sql
select sum(population) ,  avg(surfacearea) from country where continent  =  "north america" and surfacearea  >  3000
```

**Returned.**
```sql
SELECT 
    SUM(Population) AS TotalPopulation, 
    AVG(Population) AS AveragePopulation
FROM 
    country
WHERE 
    Continent = 'North America' 
    AND SurfaceArea > 3000
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    NULL | NULL

Returned query gives 1 row(s), 2 column(s):

    480753000 | 26708500.0

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R312  (question 431, database `world_1`)

- Returned by: omnisql-32b/seed101
- Returned in cell: both A and D
- Class mass: 12/49
- Instances disagreeing: 46 of 46 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the language spoken by the largest percentage of people in each nation?

**Gold.**
```sql
SELECT LANGUAGE ,  CountryCode ,  max(Percentage) FROM countrylanguage GROUP BY CountryCode
```

**Returned.**
```sql
SELECT 
    c.Name AS Country, 
    cl.Language AS MostSpokenLanguage
FROM 
    country AS c
INNER JOIN 
    countrylanguage AS cl
ON 
    c.Code = cl.CountryCode
WHERE 
    cl.Percentage = (
        SELECT MAX(cl_inner.Percentage)
        FROM countrylanguage AS cl_inner
        WHERE cl_inner.CountryCode = c.Code
    )
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 233 row(s), 3 column(s):

    Papiamento | ABW | 76.7
    Pashto | AFG | 52.4
    Ovimbundu | AGO | 37.2
    English | AIA | 0.0
    Albaniana | ALB | 97.9
    Spanish | AND | 44.6
    Papiamento | ANT | 86.2
    Arabic | ARE | 42.0
    Spanish | ARG | 96.8
    Armenian | ARM | 93.4
    Samoan | ASM | 90.6
    Creole English | ATG | 95.7
    ... (233 rows total)

Returned query gives 241 row(s), 2 column(s):

    Aruba | Papiamento
    Afghanistan | Pashto
    Angola | Ovimbundu
    Anguilla | English
    Albania | Albaniana
    Andorra | Spanish
    Netherlands Antilles | Papiamento
    United Arab Emirates | Arabic
    Argentina | Spanish
    Armenia | Armenian
    American Samoa | Samoan
    Antigua and Barbuda | Creole English
    ... (241 rows total)

Difference: col_count_differs, disjoint; 0 row(s) in common, 233 only in the gold, 241 only in the returned result.

### R313  (question 432, database `world_1`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed202
- Returned in cell: both A and D
- Class mass: 40/48, 45/48
- Instances disagreeing: 46 of 46 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the codes of the different nations, and what are the languages spoken by the greatest percentage of people for each?

**Gold.**
```sql
SELECT LANGUAGE ,  CountryCode ,  max(Percentage) FROM countrylanguage GROUP BY CountryCode
```

**Returned.**
```sql
SELECT 
    CountryCode, 
    Language
FROM 
    countrylanguage
WHERE 
    (CountryCode, Percentage) IN (
        SELECT 
            CountryCode, 
            MAX(Percentage)
        FROM 
            countrylanguage
        GROUP BY 
            CountryCode
    )
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 233 row(s), 3 column(s):

    Papiamento | ABW | 76.7
    Pashto | AFG | 52.4
    Ovimbundu | AGO | 37.2
    English | AIA | 0.0
    Albaniana | ALB | 97.9
    Spanish | AND | 44.6
    Papiamento | ANT | 86.2
    Arabic | ARE | 42.0
    Spanish | ARG | 96.8
    Armenian | ARM | 93.4
    Samoan | ASM | 90.6
    Creole English | ATG | 95.7
    ... (233 rows total)

Returned query gives 241 row(s), 2 column(s):

    ABW | Papiamento
    AFG | Pashto
    AGO | Ovimbundu
    AIA | English
    ALB | Albaniana
    AND | Spanish
    ANT | Papiamento
    ARE | Arabic
    ARG | Spanish
    ARM | Armenian
    ASM | Samoan
    ATG | Creole English
    ... (241 rows total)

Difference: col_count_differs, disjoint; 0 row(s) in common, 233 only in the gold, 241 only in the returned result.

### R314  (question 433, database `world_1`)

- Returned by: omnisql-32b/seed101
- Returned in cell: A only
- Class mass: 16/50
- Instances disagreeing: 46 of 46 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the total number of countries where Spanish is spoken by the largest percentage of people?

**Gold.**
```sql
SELECT count(*) ,   max(Percentage) FROM countrylanguage WHERE LANGUAGE  =  "Spanish" GROUP BY CountryCode
```

**Returned.**
```sql
SELECT COUNT(DISTINCT cl.CountryCode) AS TotalCountries
FROM countrylanguage AS cl
WHERE cl.Language = 'Spanish'
  AND cl.Percentage = (
    SELECT MAX(cl2.Percentage)
    FROM countrylanguage AS cl2
    WHERE cl2.CountryCode = cl.CountryCode
  )
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 28 row(s), 2 column(s):

    1 | 7.4
    1 | 44.6
    1 | 96.8
    1 | 31.6
    1 | 87.7
    1 | 0.7
    1 | 89.7
    1 | 99.0
    1 | 97.5
    1 | 100.0
    1 | 98.0
    1 | 93.0
    ... (28 rows total)

Returned query gives 1 row(s), 1 column(s):

    21

Difference: col_count_differs, disjoint; 0 row(s) in common, 27 only in the gold, 1 only in the returned result.

### R315  (question 433, database `world_1`)

- Returned by: omnisql-32b/seed101
- Returned in cell: D only
- Class mass: 15/50
- Instances disagreeing: 46 of 46 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the total number of countries where Spanish is spoken by the largest percentage of people?

**Gold.**
```sql
SELECT count(*) ,   max(Percentage) FROM countrylanguage WHERE LANGUAGE  =  "Spanish" GROUP BY CountryCode
```

**Returned.**
```sql
SELECT COUNT(*)
FROM (
    SELECT CountryCode
    FROM countrylanguage
    WHERE Language = 'Spanish'
    AND Percentage = (
        SELECT MAX(Percentage)
        FROM countrylanguage AS cl2
        WHERE cl2.CountryCode = countrylanguage.CountryCode
        AND cl2.Language = 'Spanish'
    )
) AS subquery
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 28 row(s), 2 column(s):

    1 | 7.4
    1 | 44.6
    1 | 96.8
    1 | 31.6
    1 | 87.7
    1 | 0.7
    1 | 89.7
    1 | 99.0
    1 | 97.5
    1 | 100.0
    1 | 98.0
    1 | 93.0
    ... (28 rows total)

Returned query gives 1 row(s), 1 column(s):

    28

Difference: col_count_differs, disjoint; 0 row(s) in common, 27 only in the gold, 1 only in the returned result.

### R316  (question 434, database `world_1`)

- Returned by: omnisql-32b/seed101
- Returned in cell: both A and D
- Class mass: 27/49
- Instances disagreeing: 46 of 46 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Count the number of countries for which Spanish is predominantly spoken .

**Gold.**
```sql
SELECT count(*) ,   max(Percentage) FROM countrylanguage WHERE LANGUAGE  =  "Spanish" GROUP BY CountryCode
```

**Returned.**
```sql
SELECT COUNT(DISTINCT T1.CountryCode)
FROM countrylanguage AS T1
INNER JOIN (
    SELECT CountryCode, MAX(Percentage) AS MaxPercentage
    FROM countrylanguage
    GROUP BY CountryCode
) AS T2
ON T1.CountryCode = T2.CountryCode AND T1.Percentage = T2.MaxPercentage
WHERE T1.Language = 'Spanish'
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 28 row(s), 2 column(s):

    1 | 7.4
    1 | 44.6
    1 | 96.8
    1 | 31.6
    1 | 87.7
    1 | 0.7
    1 | 89.7
    1 | 99.0
    1 | 97.5
    1 | 100.0
    1 | 98.0
    1 | 93.0
    ... (28 rows total)

Returned query gives 1 row(s), 1 column(s):

    21

Difference: col_count_differs, disjoint; 0 row(s) in common, 27 only in the gold, 1 only in the returned result.

### R317  (question 435, database `world_1`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed202, omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 30/50, 27/50, 29/50
- Instances disagreeing: 43 of 46 (93%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the codes of countries where Spanish is spoken by the largest percentage of people?

**Gold.**
```sql
SELECT CountryCode ,  max(Percentage) FROM countrylanguage WHERE LANGUAGE  =  "Spanish" GROUP BY CountryCode
```

**Returned.**
```sql
SELECT CountryCode
FROM countrylanguage
WHERE Language = 'Spanish'
  AND Percentage = (
    SELECT MAX(Percentage)
    FROM countrylanguage
    WHERE Language = 'Spanish'
  )
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 28 row(s), 2 column(s):

    ABW | 7.4
    AND | 44.6
    ARG | 96.8
    BLZ | 31.6
    BOL | 87.7
    CAN | 0.7
    CHL | 89.7
    COL | 99.0
    CRI | 97.5
    CUB | 100.0
    DOM | 98.0
    ECU | 93.0
    ... (28 rows total)

Returned query gives 2 row(s), 1 column(s):

    CUB
    SLV

Difference: col_count_differs, disjoint; 0 row(s) in common, 28 only in the gold, 2 only in the returned result.

### R318  (question 436, database `world_1`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed202, omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 30/50, 26/50, 22/50
- Instances disagreeing: 43 of 46 (93%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Return the codes of countries for which Spanish is predominantly spoken .

**Gold.**
```sql
SELECT CountryCode ,  max(Percentage) FROM countrylanguage WHERE LANGUAGE  =  "Spanish" GROUP BY CountryCode
```

**Returned.**
```sql
SELECT CountryCode
FROM countrylanguage
WHERE Language = 'Spanish'
  AND Percentage = (
    SELECT MAX(Percentage)
    FROM countrylanguage AS cl2
    WHERE cl2.CountryCode = countrylanguage.CountryCode
  )
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 28 row(s), 2 column(s):

    ABW | 7.4
    AND | 44.6
    ARG | 96.8
    BLZ | 31.6
    BOL | 87.7
    CAN | 0.7
    CHL | 89.7
    COL | 99.0
    CRI | 97.5
    CUB | 100.0
    DOM | 98.0
    ECU | 93.0
    ... (28 rows total)

Returned query gives 21 row(s), 1 column(s):

    AND
    ARG
    BOL
    CHL
    COL
    CRI
    CUB
    DOM
    ECU
    ESP
    GTM
    HND
    ... (21 rows total)

Difference: col_count_differs, disjoint; 0 row(s) in common, 28 only in the gold, 21 only in the returned result.

### R319  (question 461, database `network_1`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed202
- Returned in cell: both A and D
- Class mass: 26/50, 29/50
- Instances disagreeing: 27 of 29 (93%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find the average grade of all students who have some friends.

**Gold.**
```sql
SELECT avg(grade) FROM Highschooler WHERE id IN (SELECT T1.student_id FROM Friend AS T1 JOIN Highschooler AS T2 ON T1.student_id  =  T2.id)
```

**Returned.**
```sql
SELECT AVG(H.grade) AS average_grade
FROM Highschooler AS H
INNER JOIN Friend AS F ON H.ID = F.student_id
```

**First disagreeing instance** `network_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    10.428571428571429

Returned query gives 1 row(s), 1 column(s):

    10.25

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R320  (question 462, database `network_1`)

- Returned by: omnisql-32b/seed101
- Returned in cell: both A and D
- Class mass: 30/50
- Instances disagreeing: 27 of 29 (93%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the average grade of students who have friends?

**Gold.**
```sql
SELECT avg(grade) FROM Highschooler WHERE id IN (SELECT T1.student_id FROM Friend AS T1 JOIN Highschooler AS T2 ON T1.student_id  =  T2.id)
```

**Returned.**
```sql
SELECT AVG(Highschooler.grade) AS average_grade
FROM Friend
INNER JOIN Highschooler ON Friend.student_id = Highschooler.ID
```

**First disagreeing instance** `network_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    10.428571428571429

Returned query gives 1 row(s), 1 column(s):

    10.25

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R321  (question 463, database `network_1`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed202, omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 38/50, 39/50, 43/50
- Instances disagreeing: 11 of 29 (38%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find the minimum grade of students who have no friends.

**Gold.**
```sql
SELECT min(grade) FROM Highschooler WHERE id NOT IN (SELECT T1.student_id FROM Friend AS T1 JOIN Highschooler AS T2 ON T1.student_id  =  T2.id)
```

**Returned.**
```sql
SELECT MIN(grade)
FROM Highschooler
WHERE ID NOT IN (
    SELECT student_id
    FROM Friend
    UNION
    SELECT friend_id
    FROM Friend
)
```

**First disagreeing instance** `network_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    10

Returned query gives 1 row(s), 1 column(s):

    NULL

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R322  (question 464, database `network_1`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed202, omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 33/50, 34/50, 30/50
- Instances disagreeing: 11 of 29 (38%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the lowest grade of students who do not have any friends?

**Gold.**
```sql
SELECT min(grade) FROM Highschooler WHERE id NOT IN (SELECT T1.student_id FROM Friend AS T1 JOIN Highschooler AS T2 ON T1.student_id  =  T2.id)
```

**Returned.**
```sql
SELECT MIN(grade)
FROM Highschooler
WHERE ID NOT IN (
    SELECT student_id
    FROM Friend
    UNION
    SELECT friend_id
    FROM Friend
)
```

**First disagreeing instance** `network_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    10

Returned query gives 1 row(s), 1 column(s):

    NULL

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R323  (question 467, database `dog_kennels`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed202
- Returned in cell: both A and D
- Class mass: 46/50, 46/50
- Instances disagreeing: 48 of 48 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the names of the dogs for which the owner spent more than 1000 for treatment?

**Gold.**
```sql
select name from dogs where dog_id not in ( select dog_id from treatments group by dog_id having sum(cost_of_treatment)  >  1000 )
```

**Returned.**
```sql
SELECT d.name
FROM Dogs d
JOIN Treatments t ON d.dog_id = t.dog_id
GROUP BY d.dog_id, d.name
HAVING SUM(t.cost_of_treatment) > 1000
```

**First disagreeing instance** `dog_kennels.sqlite` (this is the shipped benchmark database).

Gold returns 12 row(s), 1 column(s):

    Kacey
    Hipolito
    Mavis
    Houston
    Jeffrey
    Merritt
    Narciso
    George
    Bessie
    Betty
    Holden
    Jesus

Returned query gives 3 row(s), 1 column(s):

    Troy
    Lyric
    Evangeline

Difference: disjoint; 0 row(s) in common, 12 only in the gold, 3 only in the returned result.

### R324  (question 468, database `dog_kennels`)

- Returned by: omnisql-32b/seed101
- Returned in cell: D only
- Class mass: 20/50
- Instances disagreeing: 48 of 48 (100%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Which person has the most dogs? List the id, first name and last name.

**Gold.**
```sql
SELECT T1.owner_id ,  T2.first_name ,  T2.last_name FROM Dogs AS T1 JOIN Owners AS T2 ON T1.owner_id  =  T2.owner_id GROUP BY T1.owner_id ORDER BY count(*) DESC LIMIT 1
```

**Returned.**
```sql
SELECT o.owner_id, o.first_name, o.last_name, COUNT(d.dog_id) AS number_of_dogs
FROM Owners o
JOIN Dogs d ON o.owner_id = d.owner_id
GROUP BY o.owner_id, o.first_name, o.last_name
ORDER BY number_of_dogs DESC
LIMIT 1
```

**First disagreeing instance** `dog_kennels.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 3 column(s):

    14 | Rachelle | Funk

Returned query gives 1 row(s), 4 column(s):

    14 | Rachelle | Funk | 3

Difference: col_count_differs, disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R325  (question 470, database `dog_kennels`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed202, omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 46/50, 44/50, 46/50
- Instances disagreeing: 45 of 48 (94%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Which doctors have done at least two treatments? List theid, role, and first name.

**Gold.**
```sql
SELECT T1.professional_id ,  T1.role_code ,  T1.first_name FROM Professionals AS T1 JOIN Treatments AS T2 ON T1.professional_id  =  T2.professional_id GROUP BY T1.professional_id HAVING count(*)  >=  2
```

**Returned.**
```sql
SELECT p.professional_id, p.role_code, p.first_name
FROM Professionals p
JOIN Treatments t ON p.professional_id = t.professional_id
WHERE p.role_code = 'Doctor'
GROUP BY p.professional_id, p.role_code, p.first_name
HAVING COUNT(t.treatment_id) >= 2
```

**First disagreeing instance** `dog_kennels.sqlite` (this is the shipped benchmark database).

Gold returns 6 row(s), 3 column(s):

    4 | Veterenarian | Vernice
    6 | Veterenarian | Ruben
    8 | Employee | Karley
    9 | Veterenarian | Monte
    10 | Employee | Domenica
    14 | Employee | Sigurd

Returned query gives 0 row(s), None column(s):

    (no rows)

Difference: rep_empty; 0 row(s) in common, 6 only in the gold, 0 only in the returned result.

### R326  (question 474, database `dog_kennels`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed202
- Returned in cell: both A and D
- Class mass: 16/50, 24/50
- Instances disagreeing: 48 of 48 (100%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Who has paid the largest amount of money in total for their dogs? Show the id and zip code.

**Gold.**
```sql
SELECT T1.owner_id ,  T1.zip_code FROM Owners AS T1 JOIN Dogs AS T2 ON T1.owner_id  =  T2.owner_id JOIN Treatments AS T3 ON T2.dog_id  =  T3.dog_id GROUP BY T1.owner_id ORDER BY sum(T3.cost_of_treatment) DESC LIMIT 1
```

**Returned.**
```sql
SELECT o.owner_id, o.zip_code, SUM(t.cost_of_treatment) AS total_cost
FROM Owners o
JOIN Dogs d ON o.owner_id = d.owner_id
JOIN Treatments t ON d.dog_id = t.dog_id
GROUP BY o.owner_id, o.zip_code
ORDER BY total_cost DESC
LIMIT 1
```

**First disagreeing instance** `dog_kennels.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    3 | 02647

Returned query gives 1 row(s), 3 column(s):

    3 | 02647 | 1601

Difference: col_count_differs, disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R327  (question 476, database `dog_kennels`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed202
- Returned in cell: both A and D
- Class mass: 30/50, 31/50
- Instances disagreeing: 46 of 48 (96%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the first name and last name of the professionals who have done treatment cheaper than average?

**Gold.**
```sql
SELECT DISTINCT T1.first_name ,  T1.last_name FROM Professionals AS T1 JOIN Treatments AS T2 WHERE cost_of_treatment  <  ( SELECT avg(cost_of_treatment) FROM Treatments )
```

**Returned.**
```sql
SELECT P.first_name, P.last_name
FROM Professionals P
JOIN Treatments T ON P.professional_id = T.professional_id
WHERE T.cost_of_treatment < (SELECT AVG(cost_of_treatment) FROM Treatments)
```

**First disagreeing instance** `dog_kennels.sqlite` (this is the shipped benchmark database).

Gold returns 15 row(s), 2 column(s):

    Taryn | Braun
    Jayson | Ullrich
    Olaf | Watsica
    Vernice | Tillman
    Danny | Considine
    Ruben | O'Reilly
    Velva | Hayes
    Karley | Hyatt
    Monte | Kshlerin
    Domenica | Jacobs
    Brady | Pouros
    Winfield | Christiansen
    ... (15 rows total)

Returned query gives 8 row(s), 2 column(s):

    Domenica | Jacobs
    Vernice | Tillman
    Karley | Hyatt
    Vernice | Tillman
    Ruben | O'Reilly
    Domenica | Jacobs
    Monte | Kshlerin
    Monte | Kshlerin

Difference: rep_subset_of_gold; 5 row(s) in common, 10 only in the gold, 0 only in the returned result.

### R328  (question 477, database `dog_kennels`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed202, omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 34/50, 29/50, 34/50
- Instances disagreeing: 40 of 48 (83%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Which professionals have operated a treatment that is less expansive than the average? Give me theor first names and last names.

**Gold.**
```sql
SELECT DISTINCT T1.first_name ,  T1.last_name FROM Professionals AS T1 JOIN Treatments AS T2 WHERE cost_of_treatment  <  ( SELECT avg(cost_of_treatment) FROM Treatments )
```

**Returned.**
```sql
SELECT DISTINCT p.first_name, p.last_name
FROM Professionals p
JOIN Treatments t ON p.professional_id = t.professional_id
WHERE t.cost_of_treatment < (SELECT AVG(cost_of_treatment) FROM Treatments)
```

**First disagreeing instance** `dog_kennels.sqlite` (this is the shipped benchmark database).

Gold returns 15 row(s), 2 column(s):

    Taryn | Braun
    Jayson | Ullrich
    Olaf | Watsica
    Vernice | Tillman
    Danny | Considine
    Ruben | O'Reilly
    Velva | Hayes
    Karley | Hyatt
    Monte | Kshlerin
    Domenica | Jacobs
    Brady | Pouros
    Winfield | Christiansen
    ... (15 rows total)

Returned query gives 5 row(s), 2 column(s):

    Domenica | Jacobs
    Vernice | Tillman
    Karley | Hyatt
    Ruben | O'Reilly
    Monte | Kshlerin

Difference: rep_subset_of_gold; 5 row(s) in common, 10 only in the gold, 0 only in the returned result.

### R329  (question 480, database `dog_kennels`)

- Returned by: omnisql-32b/seed101
- Returned in cell: both A and D
- Class mass: 23/50
- Instances disagreeing: 45 of 48 (94%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** List the last name of the owner owning the youngest dog.

**Gold.**
```sql
SELECT T1.last_name FROM Owners AS T1 JOIN Dogs AS T2 ON T1.owner_id  =  T2.owner_id WHERE T2.age  =  ( SELECT max(age) FROM Dogs )
```

**Returned.**
```sql
SELECT O.last_name
FROM Owners O
JOIN Dogs D ON O.owner_id = D.owner_id
WHERE D.age = (
    SELECT MIN(age)
    FROM Dogs
)
```

**First disagreeing instance** `dog_kennels.sqlite` (this is the shipped benchmark database).

Gold returns 3 row(s), 1 column(s):

    Feil
    Fisher
    Rippin

Returned query gives 1 row(s), 1 column(s):

    Nicolas

Difference: disjoint; 0 row(s) in common, 3 only in the gold, 1 only in the returned result.

### R330  (question 481, database `dog_kennels`)

- Returned by: omnisql-32b/seed101
- Returned in cell: A only
- Class mass: 21/50
- Instances disagreeing: 42 of 48 (88%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Who owns the youngest dog? Give me his or her last name.

**Gold.**
```sql
SELECT T1.last_name FROM Owners AS T1 JOIN Dogs AS T2 ON T1.owner_id  =  T2.owner_id WHERE T2.age  =  ( SELECT max(age) FROM Dogs )
```

**Returned.**
```sql
SELECT O.last_name
FROM Owners O
JOIN Dogs D ON O.owner_id = D.owner_id
WHERE D.date_of_birth = (
  SELECT MAX(date_of_birth)
  FROM Dogs
)
```

**First disagreeing instance** `dog_kennels.sqlite` (this is the shipped benchmark database).

Gold returns 3 row(s), 1 column(s):

    Feil
    Fisher
    Rippin

Returned query gives 1 row(s), 1 column(s):

    Mertz

Difference: disjoint; 0 row(s) in common, 3 only in the gold, 1 only in the returned result.

### R331  (question 481, database `dog_kennels`)

- Returned by: omnisql-32b/seed101
- Returned in cell: D only
- Class mass: 12/50
- Instances disagreeing: 45 of 48 (94%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Who owns the youngest dog? Give me his or her last name.

**Gold.**
```sql
SELECT T1.last_name FROM Owners AS T1 JOIN Dogs AS T2 ON T1.owner_id  =  T2.owner_id WHERE T2.age  =  ( SELECT max(age) FROM Dogs )
```

**Returned.**
```sql
SELECT o.last_name
FROM Owners o
JOIN Dogs d ON o.owner_id = d.owner_id
WHERE d.age = (SELECT MIN(age) FROM Dogs)
```

**First disagreeing instance** `dog_kennels.sqlite` (this is the shipped benchmark database).

Gold returns 3 row(s), 1 column(s):

    Feil
    Fisher
    Rippin

Returned query gives 1 row(s), 1 column(s):

    Nicolas

Difference: disjoint; 0 row(s) in common, 3 only in the gold, 1 only in the returned result.

### R332  (question 44, database `pets_1`)

- Returned by: omnisql-32b/seed202
- Returned in cell: D only
- Class mass: 20/50
- Instances disagreeing: 20 of 27 (74%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the students' first names who have both cats and dogs?

**Gold.**
```sql
SELECT T1.Fname FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid  =  T2.stuid JOIN pets AS T3 ON T3.petid  =  T2.petid WHERE T3.pettype  =  'cat' INTERSECT SELECT T1.Fname FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid  =  T2.stuid JOIN pets AS T3 ON T3.petid  =  T2.petid WHERE T3.pettype  =  'dog'
```

**Returned.**
```sql
SELECT S.Fname
FROM Student S
JOIN Has_Pet HP ON S.StuID = HP.StuID
JOIN Pets P ON HP.PetID = P.PetID
WHERE P.PetType IN ('cat', 'dog')
GROUP BY S.StuID
HAVING COUNT(DISTINCT P.PetType) = 2
```

**First disagreeing instance** `pets_1v5080.sqlite`.

Gold returns 5 row(s), 1 column(s):

    0
    003
    10
    David
    Oy01U(d

Returned query gives 4 row(s), 1 column(s):

    Oy01U(d
    David
    003
    0

Difference: rep_subset_of_gold; 4 row(s) in common, 1 only in the gold, 0 only in the returned result.

### R333  (question 49, database `pets_1`)

- Returned by: omnisql-32b/seed202
- Returned in cell: A only
- Class mass: 34/50
- Instances disagreeing: 23 of 27 (85%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find the first name and age of students who have a dog but do not have a cat.

**Gold.**
```sql
SELECT T1.fname ,  T1.age FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid  =  T2.stuid JOIN pets AS T3 ON T3.petid  =  T2.petid WHERE T3.pettype  =  'dog' AND T1.stuid NOT IN (SELECT T1.stuid FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid  =  T2.stuid JOIN pets AS T3 ON T3.petid  =  T2.petid WHERE T3.pettype  =  'cat')
```

**Returned.**
```sql
SELECT S.Fname, S.Age
FROM Student S
JOIN Has_Pet HP ON S.StuID = HP.StuID
JOIN Pets P ON HP.PetID = P.PetID
WHERE P.PetType = 'dog'
EXCEPT
SELECT S.Fname, S.Age
FROM Student S
JOIN Has_Pet HP ON S.StuID = HP.StuID
JOIN Pets P ON HP.PetID = P.PetID
WHERE P.PetType = 'cat'
```

**First disagreeing instance** `pets_1.sqlite` (this is the shipped benchmark database).

Gold returns 2 row(s), 2 column(s):

    Tracy | 19
    Tracy | 19

Returned query gives 1 row(s), 2 column(s):

    Tracy | 19

Difference: duplicate_multiplicity_only; 1 row(s) in common, 0 only in the gold, 0 only in the returned result.

### R334  (question 49, database `pets_1`)

- Returned by: omnisql-32b/seed202
- Returned in cell: D only
- Class mass: 16/50
- Instances disagreeing: 20 of 27 (74%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find the first name and age of students who have a dog but do not have a cat.

**Gold.**
```sql
SELECT T1.fname ,  T1.age FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid  =  T2.stuid JOIN pets AS T3 ON T3.petid  =  T2.petid WHERE T3.pettype  =  'dog' AND T1.stuid NOT IN (SELECT T1.stuid FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid  =  T2.stuid JOIN pets AS T3 ON T3.petid  =  T2.petid WHERE T3.pettype  =  'cat')
```

**Returned.**
```sql
SELECT 
    T1.Fname, 
    T1.Age
FROM 
    Student AS T1
WHERE 
    T1.StuID IN 
    (
        SELECT 
            HP.StuID
        FROM 
            Has_Pet AS HP
        JOIN 
            Pets AS P 
        ON 
            HP.PetID = P.PetID
        WHERE 
            P.PetType = 'dog'
    )
    AND 
    T1.StuID NOT IN 
    (
        SELECT 
            HP.StuID
        FROM 
            Has_Pet AS HP
        JOIN 
            Pets AS P 
        ON 
            HP.PetID = P.PetID
        WHERE 
            P.PetType = 'cat'
    )
```

**First disagreeing instance** `pets_1.sqlite` (this is the shipped benchmark database).

Gold returns 2 row(s), 2 column(s):

    Tracy | 19
    Tracy | 19

Returned query gives 1 row(s), 2 column(s):

    Tracy | 19

Difference: duplicate_multiplicity_only; 1 row(s) in common, 0 only in the gold, 0 only in the returned result.

### R335  (question 50, database `pets_1`)

- Returned by: omnisql-32b/seed202
- Returned in cell: both A and D
- Class mass: 41/50
- Instances disagreeing: 25 of 27 (93%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the first name of every student who has a dog but does not have a cat?

**Gold.**
```sql
SELECT T1.fname ,  T1.age FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid  =  T2.stuid JOIN pets AS T3 ON T3.petid  =  T2.petid WHERE T3.pettype  =  'dog' AND T1.stuid NOT IN (SELECT T1.stuid FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid  =  T2.stuid JOIN pets AS T3 ON T3.petid  =  T2.petid WHERE T3.pettype  =  'cat')
```

**Returned.**
```sql
SELECT DISTINCT S.Fname
FROM Student S
INNER JOIN Has_Pet HP ON S.StuID = HP.StuID
INNER JOIN Pets P ON HP.PetID = P.PetID
WHERE P.PetType = 'dog'
AND S.StuID NOT IN (
    SELECT HP.StuID
    FROM Has_Pet HP
    INNER JOIN Pets P ON HP.PetID = P.PetID
    WHERE P.PetType = 'cat'
)
```

**First disagreeing instance** `pets_1.sqlite` (this is the shipped benchmark database).

Gold returns 2 row(s), 2 column(s):

    Tracy | 19
    Tracy | 19

Returned query gives 1 row(s), 1 column(s):

    Tracy

Difference: col_count_differs, disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R336  (question 66, database `car_1`)

- Returned by: omnisql-32b/seed202
- Returned in cell: both A and D
- Class mass: 10/50
- Instances disagreeing: 60 of 60 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the maker of the carr produced in the earliest  and what  year was it?

**Gold.**
```sql
SELECT T2.Make ,  T1.Year FROM CARS_DATA AS T1 JOIN CAR_NAMES AS T2 ON T1.Id  =  T2.MakeId WHERE T1.Year  =  (SELECT min(YEAR) FROM CARS_DATA);
```

**Returned.**
```sql
SELECT cm.Maker, cd.Year
FROM cars_data cd
JOIN car_names cn ON cd.Id = cn.MakeId
JOIN model_list ml ON cn.Model = ml.Model
JOIN car_makers cm ON ml.Maker = cm.Id
WHERE cd.Year = (SELECT MIN(Year) FROM cars_data)
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 35 row(s), 2 column(s):

    chevrolet chevelle malibu | 1970
    buick skylark 320 | 1970
    plymouth satellite | 1970
    amc rebel sst | 1970
    ford torino | 1970
    ford galaxie 500 | 1970
    chevrolet impala | 1970
    plymouth fury iii | 1970
    pontiac catalina | 1970
    amc ambassador dpl | 1970
    citroen ds-21 pallas | 1970
    chevrolet chevelle concours (sw) | 1970
    ... (35 rows total)

Returned query gives 34 row(s), 2 column(s):

    gm | 1970
    gm | 1970
    chrysler | 1970
    amc | 1970
    ford | 1970
    ford | 1970
    gm | 1970
    chrysler | 1970
    gm | 1970
    amc | 1970
    citroen | 1970
    gm | 1970
    ... (34 rows total)

Difference: disjoint; 0 row(s) in common, 35 only in the gold, 11 only in the returned result.

### R337  (question 75, database `car_1`)

- Returned by: omnisql-32b/seed202
- Returned in cell: both A and D
- Class mass: 42/50
- Instances disagreeing: 14 of 60 (23%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the number of makers of care in France?

**Gold.**
```sql
SELECT count(*) FROM CAR_MAKERS AS T1 JOIN COUNTRIES AS T2 ON T1.Country  =  T2.CountryId WHERE T2.CountryName  =  'france';
```

**Returned.**
```sql
SELECT COUNT(cm.Id) AS NumberOfCarMakers
FROM car_makers cm
JOIN countries c ON cm.Country = c.CountryId
WHERE c.CountryName = 'France'
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    3

Returned query gives 1 row(s), 1 column(s):

    0

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R338  (question 77, database `car_1`)

- Returned by: omnisql-32b/seed202
- Returned in cell: both A and D
- Class mass: 28/50
- Instances disagreeing: 33 of 60 (55%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the count of the car models produced in the United States?

**Gold.**
```sql
SELECT count(*) FROM MODEL_LIST AS T1 JOIN CAR_MAKERS AS T2 ON T1.Maker  =  T2.Id JOIN COUNTRIES AS T3 ON T2.Country  =  T3.CountryId WHERE T3.CountryName  =  'usa';
```

**Returned.**
```sql
SELECT COUNT(*)
FROM model_list
JOIN car_makers ON model_list.Maker = car_makers.Id
JOIN countries ON car_makers.Country = countries.CountryId
WHERE countries.CountryName = 'USA'
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    13

Returned query gives 1 row(s), 1 column(s):

    0

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R339  (question 91, database `car_1`)

- Returned by: omnisql-32b/seed202
- Returned in cell: A only
- Class mass: 21/50
- Instances disagreeing: 11 of 60 (18%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the average edispl for all volvos?

**Gold.**
```sql
SELECT avg(T2.edispl) FROM CAR_NAMES AS T1 JOIN CARS_DATA AS T2 ON T1.MakeId  =  T2.Id WHERE T1.Model  =  'volvo';
```

**Returned.**
```sql
SELECT AVG(Edispl) AS average_edispl
FROM cars_data
JOIN car_names ON cars_data.Id = car_names.MakeId
WHERE car_names.Make = 'volvo'
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    133.5

Returned query gives 1 row(s), 1 column(s):

    NULL

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R340  (question 91, database `car_1`)

- Returned by: omnisql-32b/seed202
- Returned in cell: D only
- Class mass: 13/50
- Instances disagreeing: 18 of 60 (30%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the average edispl for all volvos?

**Gold.**
```sql
SELECT avg(T2.edispl) FROM CAR_NAMES AS T1 JOIN CARS_DATA AS T2 ON T1.MakeId  =  T2.Id WHERE T1.Model  =  'volvo';
```

**Returned.**
```sql
SELECT AVG(T1.Edispl) AS Average_Displacement
FROM cars_data AS T1
INNER JOIN car_names AS T2 ON T1.Id = T2.MakeId
INNER JOIN model_list AS T3 ON T2.Model = T3.Model
INNER JOIN car_makers AS T4 ON T3.Maker = T4.Id
WHERE T4.Maker = 'volvo'
```

**First disagreeing instance** `car_1v50811.sqlite`.

Gold returns 1 row(s), 1 column(s):

    NULL

Returned query gives 1 row(s), 1 column(s):

    436889768.3333333

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R341  (question 92, database `car_1`)

- Returned by: omnisql-32b/seed202
- Returned in cell: both A and D
- Class mass: 8/50
- Instances disagreeing: 60 of 60 (100%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What car has the most different versions?

**Gold.**
```sql
SELECT Model FROM CAR_NAMES GROUP BY Model ORDER BY count(*) DESC LIMIT 1;
```

**Returned.**
```sql
SELECT 
    Make, 
    COUNT(DISTINCT Model) AS model_count
FROM 
    car_names
GROUP BY 
    Make
ORDER BY 
    model_count DESC
LIMIT 1
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    ford

Returned query gives 1 row(s), 2 column(s):

    volkswagen rabbit | 2

Difference: col_count_differs, disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R342  (question 98, database `car_1`)

- Returned by: omnisql-32b/seed202
- Returned in cell: both A and D
- Class mass: 36/50
- Instances disagreeing: 30 of 60 (50%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the names and ids of all car companies with more than 3 models?

**Gold.**
```sql
SELECT T1.FullName ,  T1.Id FROM CAR_MAKERS AS T1 JOIN MODEL_LIST AS T2 ON T1.Id  =  T2.Maker GROUP BY T1.Id HAVING count(*)  >  3;
```

**Returned.**
```sql
SELECT cm.Id, cm.Maker
FROM car_makers AS cm
JOIN model_list AS ml ON cm.Id = ml.Maker
GROUP BY cm.Id, cm.Maker
HAVING COUNT(ml.Model) > 3
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 2 row(s), 2 column(s):

    General Motors | 4
    Chrysler | 6

Returned query gives 2 row(s), 2 column(s):

    4 | gm
    6 | chrysler

Difference: disjoint; 0 row(s) in common, 2 only in the gold, 2 only in the returned result.

### R343  (question 99, database `car_1`)

- Returned by: omnisql-32b/seed202
- Returned in cell: A only
- Class mass: 16/50
- Instances disagreeing: 27 of 60 (45%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Which distinctive models are produced by General Motors or heavier than 3500?

**Gold.**
```sql
SELECT DISTINCT T2.Model FROM CAR_NAMES AS T1 JOIN MODEL_LIST AS T2 ON T1.Model  =  T2.Model JOIN CAR_MAKERS AS T3 ON T2.Maker  =  T3.Id JOIN CARS_DATA AS T4 ON T1.MakeId  =  T4.Id WHERE T3.FullName  =  'General Motors' OR T4.weight  >  3500;
```

**Returned.**
```sql
SELECT DISTINCT 
    ml.Model
FROM 
    car_names cn
JOIN 
    model_list ml ON cn.Model = ml.Model
JOIN 
    car_makers cm ON ml.Maker = cm.Id
JOIN 
    cars_data cd ON cn.MakeId = cd.Id
WHERE 
    cm.Maker = 'General Motors'
UNION
SELECT DISTINCT 
    cn.Model
FROM 
    car_names cn
JOIN 
    cars_data cd ON cn.MakeId = cd.Id
WHERE 
    cd.Weight > 3500
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 13 row(s), 1 column(s):

    chevrolet
    buick
    ford
    plymouth
    pontiac
    amc
    dodge
    mercury
    oldsmobile
    chrysler
    mercedes-benz
    cadillac
    ... (13 rows total)

Returned query gives 14 row(s), 1 column(s):

    amc
    buick
    cadillac
    chevrolet
    chrysler
    dodge
    ford
    hi
    mercedes
    mercedes-benz
    mercury
    oldsmobile
    ... (14 rows total)

Difference: gold_subset_of_rep; 13 row(s) in common, 0 only in the gold, 1 only in the returned result.

### R344  (question 99, database `car_1`)

- Returned by: omnisql-32b/seed202
- Returned in cell: D only
- Class mass: 9/50
- Instances disagreeing: 26 of 60 (43%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Which distinctive models are produced by General Motors or heavier than 3500?

**Gold.**
```sql
SELECT DISTINCT T2.Model FROM CAR_NAMES AS T1 JOIN MODEL_LIST AS T2 ON T1.Model  =  T2.Model JOIN CAR_MAKERS AS T3 ON T2.Maker  =  T3.Id JOIN CARS_DATA AS T4 ON T1.MakeId  =  T4.Id WHERE T3.FullName  =  'General Motors' OR T4.weight  >  3500;
```

**Returned.**
```sql
SELECT DISTINCT c.Model
FROM car_names c
JOIN cars_data cd ON c.MakeId = cd.Id
JOIN model_list ml ON c.Model = ml.Model
JOIN car_makers cm ON ml.Maker = cm.Id
WHERE cm.Maker = 'General Motors' OR cd.Weight > 3500
```

**First disagreeing instance** `car_1v50813.sqlite`.

Gold returns 31 row(s), 1 column(s):

    1974
    qyuDNq(nn8ZhzguxpL
    196
    Ford Motor Company
    scion
    eDAGeneral Motorsumk
    zvbhM)6C2CfKEKU
    jqF2W6JdR09aA2lVN
    xNv1969ZPZ
    General Motors
    4
    eDHnlM0LEX6)o8Z
    ... (31 rows total)

Returned query gives 32 row(s), 1 column(s):

    1974
    qyuDNq(nn8ZhzguxpL
    196
    Ford Motor Company
    scion
    eDAGeneral Motorsumk
    zvbhM)6C2CfKEKU
    jqF2W6JdR09aA2lVN
    xNv1969ZPZ
    General Motors
    4
    eDHnlM0LEX6)o8Z
    ... (32 rows total)

Difference: gold_subset_of_rep; 31 row(s) in common, 0 only in the gold, 1 only in the returned result.

### R345  (question 100, database `car_1`)

- Returned by: omnisql-32b/seed202
- Returned in cell: A only
- Class mass: 16/50
- Instances disagreeing: 29 of 60 (48%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the different models created by either General Motors or over 3500 lbs?

**Gold.**
```sql
SELECT DISTINCT T2.Model FROM CAR_NAMES AS T1 JOIN MODEL_LIST AS T2 ON T1.Model  =  T2.Model JOIN CAR_MAKERS AS T3 ON T2.Maker  =  T3.Id JOIN CARS_DATA AS T4 ON T1.MakeId  =  T4.Id WHERE T3.FullName  =  'General Motors' OR T4.weight  >  3500;
```

**Returned.**
```sql
SELECT DISTINCT Model
FROM model_list ml
JOIN car_makers cm ON ml.Maker = cm.Id
WHERE cm.Maker = 'General Motors'
UNION
SELECT DISTINCT cn.Model
FROM car_names cn
JOIN cars_data cd ON cn.MakeId = cd.Id
WHERE cd.Weight > 3500
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 13 row(s), 1 column(s):

    chevrolet
    buick
    ford
    plymouth
    pontiac
    amc
    dodge
    mercury
    oldsmobile
    chrysler
    mercedes-benz
    cadillac
    ... (13 rows total)

Returned query gives 14 row(s), 1 column(s):

    amc
    buick
    cadillac
    chevrolet
    chrysler
    dodge
    ford
    hi
    mercedes
    mercedes-benz
    mercury
    oldsmobile
    ... (14 rows total)

Difference: gold_subset_of_rep; 13 row(s) in common, 0 only in the gold, 1 only in the returned result.

### R346  (question 105, database `car_1`)

- Returned by: omnisql-32b/seed202
- Returned in cell: A only
- Class mass: 49/50
- Instances disagreeing: 60 of 60 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** How many nations has more than 2 car makers ?

**Gold.**
```sql
select count(*) from countries as t1 join car_makers as t2 on t1.countryid  =  t2.country group by t1.countryid having count(*)  >  2
```

**Returned.**
```sql
SELECT COUNT(*)
FROM (
    SELECT c.CountryName
    FROM car_makers AS cm
    INNER JOIN countries AS c ON cm.Country = c.CountryId
    GROUP BY c.CountryName
    HAVING COUNT(cm.Id) > 2
) AS subquery
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 4 row(s), 1 column(s):

    4
    4
    3
    5

Returned query gives 1 row(s), 1 column(s):

    4

Difference: rep_subset_of_gold; 1 row(s) in common, 2 only in the gold, 0 only in the returned result.

### R347  (question 105, database `car_1`)

- Returned by: omnisql-32b/seed202
- Returned in cell: D only
- Class mass: 26/50
- Instances disagreeing: 60 of 60 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** How many nations has more than 2 car makers ?

**Gold.**
```sql
select count(*) from countries as t1 join car_makers as t2 on t1.countryid  =  t2.country group by t1.countryid having count(*)  >  2
```

**Returned.**
```sql
SELECT COUNT(*)
FROM (
    SELECT countries.CountryId
    FROM car_makers
    INNER JOIN countries ON car_makers.Country = countries.CountryId
    GROUP BY countries.CountryId
    HAVING COUNT(car_makers.Id) > 2
) AS filtered_countries
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 4 row(s), 1 column(s):

    4
    4
    3
    5

Returned query gives 1 row(s), 1 column(s):

    4

Difference: rep_subset_of_gold; 1 row(s) in common, 2 only in the gold, 0 only in the returned result.

### R348  (question 109, database `car_1`)

- Returned by: omnisql-32b/seed202
- Returned in cell: both A and D
- Class mass: 16/50
- Instances disagreeing: 56 of 60 (93%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Which models are lighter than 3500 but not built by the 'Ford Motor Company'?

**Gold.**
```sql
SELECT DISTINCT T1.model FROM MODEL_LIST AS T1 JOIN CAR_NAMES AS T2 ON T1.Model  =  T2.Model JOIN CARS_DATA AS T3 ON T2.MakeId  =  T3.Id JOIN CAR_MAKERS AS T4 ON T1.Maker  =  T4.Id WHERE T3.weight  <  3500 AND T4.FullName != 'Ford Motor Company';
```

**Returned.**
```sql
SELECT 
  cn.Model
FROM 
  cars_data cd
  INNER JOIN car_names cn ON cd.Id = cn.MakeId
  INNER JOIN model_list ml ON cn.Model = ml.Model
  INNER JOIN car_makers cm ON ml.Maker = cm.Id
WHERE 
  cd.Weight < 3500 
  AND cm.FullName <> 'Ford Motor Company'
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 26 row(s), 1 column(s):

    plymouth
    amc
    citroen
    buick
    toyota
    datsun
    volkswagen
    peugeot
    audi
    saab
    bmw
    chevrolet
    ... (26 rows total)

Returned query gives 252 row(s), 1 column(s):

    plymouth
    amc
    citroen
    buick
    toyota
    plymouth
    amc
    datsun
    volkswagen
    peugeot
    audi
    saab
    ... (252 rows total)

Difference: duplicate_multiplicity_only; 26 row(s) in common, 0 only in the gold, 0 only in the returned result.

### R349  (question 112, database `car_1`)

- Returned by: omnisql-32b/seed202
- Returned in cell: D only
- Class mass: 13/50
- Instances disagreeing: 10 of 60 (17%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the ids and names of all countries that either have more than 3 car makers or produce fiats?

**Gold.**
```sql
select t1.countryid ,  t1.countryname from countries as t1 join car_makers as t2 on t1.countryid  =  t2.country group by t1.countryid having count(*)  >  3 union select t1.countryid ,  t1.countryname from countries as t1 join car_makers as t2 on t1.countryid  =  t2.country join model_list as t3 on t2.id  =  t3.maker where t3.model  =  'fiat';
```

**Returned.**
```sql
SELECT 
    countries.CountryId,
    countries.CountryName
FROM 
    countries
WHERE 
    countries.CountryId IN (
        SELECT 
            car_makers.Country 
        FROM 
            car_makers
        GROUP BY 
            car_makers.Country 
        HAVING 
            COUNT(car_makers.Maker) > 3
    )
UNION 
SELECT 
    countries.CountryId,
    countries.CountryName
FROM 
    countries
WHERE 
    countries.CountryId IN (
        SELECT 
            car_makers.Country 
        FROM 
            car_makers 
        JOIN 
            car_names ON car_makers.Maker = car_names.Make 
        WHERE 
            car_names.Make = 'Fiat'
    )
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 4 row(s), 2 column(s):

    1 | usa
    2 | germany
    4 | japan
    5 | italy

Returned query gives 3 row(s), 2 column(s):

    1 | usa
    2 | germany
    4 | japan

Difference: rep_subset_of_gold; 3 row(s) in common, 1 only in the gold, 0 only in the returned result.

### R350  (question 140, database `flight_2`)

- Returned by: omnisql-32b/seed202
- Returned in cell: both A and D
- Class mass: 38/50
- Instances disagreeing: 8 of 56 (14%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Give the number of Jetblue Airways flights.

**Gold.**
```sql
SELECT count(*) FROM FLIGHTS AS T1 JOIN AIRLINES AS T2 ON T1.Airline  =  T2.uid WHERE T2.Airline = "JetBlue Airways"
```

**Returned.**
```sql
SELECT COUNT(*) 
FROM flights 
JOIN airlines ON flights.Airline = airlines.uid 
WHERE airlines.Airline = 'Jetblue Airways'
```

**First disagreeing instance** `flight_2.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    100

Returned query gives 1 row(s), 1 column(s):

    0

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R351  (question 148, database `flight_2`)

- Returned by: omnisql-32b/seed202
- Returned in cell: D only
- Class mass: 28/50
- Instances disagreeing: 4 of 56 (7%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Which airlines have a flight from  AHD?

**Gold.**
```sql
SELECT T1.Airline FROM AIRLINES AS T1 JOIN FLIGHTS AS T2 ON T1.uid  =  T2.Airline WHERE T2.SourceAirport  =  "AHD"
```

**Returned.**
```sql
SELECT DISTINCT airlines.Airline
FROM flights
INNER JOIN airlines ON flights.Airline = airlines.uid
WHERE flights.SourceAirport = 'AHD'
```

**First disagreeing instance** `flight_2v5081.sqlite`.

Gold returns 2 row(s), 1 column(s):

    Virgin America
    Virgin America

Returned query gives 1 row(s), 1 column(s):

    Virgin America

Difference: duplicate_multiplicity_only; 1 row(s) in common, 0 only in the gold, 0 only in the returned result.

### R352  (question 168, database `flight_2`)

- Returned by: omnisql-32b/seed202
- Returned in cell: both A and D
- Class mass: 18/50
- Instances disagreeing: 33 of 56 (59%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Which airports do not have departing or arriving flights?

**Gold.**
```sql
SELECT AirportName FROM Airports WHERE AirportCode NOT IN (SELECT SourceAirport FROM Flights UNION SELECT DestAirport FROM Flights)
```

**Returned.**
```sql
SELECT AirportCode
FROM airports
WHERE AirportCode NOT IN (SELECT SourceAirport FROM flights)
  AND AirportCode NOT IN (SELECT DestAirport FROM flights)
```

**First disagreeing instance** `flight_2.sqlite` (this is the shipped benchmark database).

Gold returns 100 row(s), 1 column(s):

    Phillips AAF 
    Municipal 
    Dyess AFB 
    Municipal 
    Virginia Highlands 
    Ada 
    Adak Island Ns 
    Lenawee County 
    Municipal 
    Municipal 
    Ainsworth 
    Akhiok SPB 
    ... (100 rows total)

Returned query gives 100 row(s), 1 column(s):

    AAF
    ABI
    ABL
    ABQ
    ABR
    ABY
    ACV
    ADG
    ADK
    ADM
    ADR
    ADT
    ... (100 rows total)

Difference: disjoint; 0 row(s) in common, 89 only in the gold, 100 only in the returned result.

### R353  (question 223, database `wta_1`)

- Returned by: omnisql-32b/seed202
- Returned in cell: D only
- Class mass: 13/50
- Instances disagreeing: 7 of 33 (21%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the names of players who won in both 2013 and 2016?

**Gold.**
```sql
SELECT winner_name FROM matches WHERE YEAR  =  2013 INTERSECT SELECT winner_name FROM matches WHERE YEAR  =  2016
```

**Returned.**
```sql
SELECT 
    p.first_name || ' ' || p.last_name AS player_name
FROM 
    players p
WHERE 
    p.player_id IN (
        SELECT 
            m.winner_id
        FROM 
            matches m
        WHERE 
            m.year = 2013
        INTERSECT
        SELECT 
            m.winner_id
        FROM 
            matches m
        WHERE 
            m.year = 2016
    )
```

**First disagreeing instance** `wta_1v5080.sqlite`.

Gold returns 1 row(s), 1 column(s):

    3

Returned query gives 0 row(s), None column(s):

    (no rows)

Difference: rep_empty; 0 row(s) in common, 1 only in the gold, 0 only in the returned result.

### R354  (question 234, database `wta_1`)

- Returned by: omnisql-32b/seed202
- Returned in cell: both A and D
- Class mass: 7/50
- Instances disagreeing: 33 of 33 (100%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Find the name and rank points of the person who won the most times.

**Gold.**
```sql
SELECT winner_name ,  winner_rank_points FROM matches GROUP BY winner_name ORDER BY count(*) DESC LIMIT 1
```

**Returned.**
```sql
SELECT p.first_name, p.last_name, m.winner_rank_points
FROM matches m
JOIN players p ON m.winner_id = p.player_id
GROUP BY m.winner_id
ORDER BY COUNT(*) DESC
LIMIT 1
```

**First disagreeing instance** `wta_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    Angelique Kerber | 3715

Returned query gives 1 row(s), 3 column(s):

    Angelique | Kerber | 3715

Difference: col_count_differs, disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R355  (question 235, database `wta_1`)

- Returned by: omnisql-32b/seed202
- Returned in cell: both A and D
- Class mass: 9/50
- Instances disagreeing: 33 of 33 (100%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What is the name of the player who has won the most matches, and how many rank points does this player have?

**Gold.**
```sql
SELECT winner_name ,  winner_rank_points FROM matches GROUP BY winner_name ORDER BY count(*) DESC LIMIT 1
```

**Returned.**
```sql
SELECT 
    p.first_name || ' ' || p.last_name AS player_name,
    r.ranking_points
FROM players p
JOIN (
    SELECT winner_id, COUNT(*) AS total_wins
    FROM matches
    GROUP BY winner_id
    ORDER BY total_wins DESC
    LIMIT 1
) m ON p.player_id = m.winner_id
JOIN rankings r ON p.player_id = r.player_id
```

**First disagreeing instance** `wta_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    Angelique Kerber | 3715

Returned query gives 635 row(s), 2 column(s):

    Angelique Kerber | 16
    Angelique Kerber | 16
    Angelique Kerber | 16
    Angelique Kerber | 17
    Angelique Kerber | 17
    Angelique Kerber | 17
    Angelique Kerber | 17
    Angelique Kerber | 17
    Angelique Kerber | 17
    Angelique Kerber | 17
    Angelique Kerber | 17
    Angelique Kerber | 17
    ... (635 rows total)

Difference: gold_subset_of_rep; 1 row(s) in common, 0 only in the gold, 217 only in the returned result.

### R356  (question 236, database `wta_1`)

- Returned by: omnisql-32b/seed202
- Returned in cell: D only
- Class mass: 15/50
- Instances disagreeing: 9 of 33 (27%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Find the name of the winner who has the highest rank points and participated in the Australian Open.

**Gold.**
```sql
SELECT winner_name FROM matches WHERE tourney_name  =  'Australian Open' ORDER BY winner_rank_points DESC LIMIT 1
```

**Returned.**
```sql
SELECT 
    p.first_name || ' ' || p.last_name AS winner_name
FROM 
    matches m
JOIN 
    players p ON m.winner_id = p.player_id
WHERE 
    m.tourney_name = 'Australian Open'
ORDER BY 
    m.winner_rank_points DESC
LIMIT 1
```

**First disagreeing instance** `wta_1v5080.sqlite`.

Gold returns 1 row(s), 1 column(s):

    11dVZOO

Returned query gives 1 row(s), 1 column(s):

    200001 10

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R357  (question 237, database `wta_1`)

- Returned by: omnisql-32b/seed202
- Returned in cell: D only
- Class mass: 13/50
- Instances disagreeing: 9 of 33 (27%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What is the name of the winner with the most rank points who participated in the Australian Open?

**Gold.**
```sql
SELECT winner_name FROM matches WHERE tourney_name  =  'Australian Open' ORDER BY winner_rank_points DESC LIMIT 1
```

**Returned.**
```sql
SELECT 
    p.first_name || ' ' || p.last_name AS winner_name
FROM 
    matches m
JOIN 
    players p ON m.winner_id = p.player_id
JOIN 
    rankings r ON m.winner_id = r.player_id
WHERE 
    m.tourney_name = 'Australian Open'
ORDER BY 
    r.ranking_points DESC
LIMIT 1
```

**First disagreeing instance** `wta_1v5080.sqlite`.

Gold returns 1 row(s), 1 column(s):

    11dVZOO

Returned query gives 1 row(s), 1 column(s):

    R 19

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R358  (question 252, database `battle_death`)

- Returned by: omnisql-32b/seed202
- Returned in cell: both A and D
- Class mass: 26/50
- Instances disagreeing: 27 of 28 (96%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What is the ship id and name that caused most total injuries?

**Gold.**
```sql
SELECT T2.id ,  T2.name FROM death AS T1 JOIN ship AS t2 ON T1.caused_by_ship_id  =  T2.id GROUP BY T2.id ORDER BY count(*) DESC LIMIT 1
```

**Returned.**
```sql
SELECT 
    ship.id, 
    ship.name 
FROM 
    ship 
INNER JOIN 
    death 
ON 
    ship.id = death.caused_by_ship_id 
GROUP BY 
    ship.id, ship.name 
ORDER BY 
    SUM(death.injured) DESC 
LIMIT 1
```

**First disagreeing instance** `battle_death.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    5 | Three Brothers

Returned query gives 1 row(s), 2 column(s):

    4 | HMS Avon

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R359  (question 253, database `battle_death`)

- Returned by: omnisql-32b/seed202
- Returned in cell: D only
- Class mass: 15/50
- Instances disagreeing: 17 of 28 (61%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** List the name and date the battle that has lost  Lettice and HMS Atalanta

**Gold.**
```sql
SELECT T1.name ,  T1.date FROM battle AS T1 JOIN ship AS T2 ON T1.id  =  T2.lost_in_battle WHERE T2.name  =  'Lettice' INTERSECT SELECT T1.name ,  T1.date FROM battle AS T1 JOIN ship AS T2 ON T1.id  =  T2.lost_in_battle WHERE T2.name  =  'HMS Atalanta'
```

**Returned.**
```sql
SELECT 
    battle.name AS battle_name, 
    battle.date AS battle_date
FROM 
    ship
INNER JOIN 
    battle 
ON 
    ship.lost_in_battle = battle.id
WHERE 
    ship.name IN ('Lettice', 'HMS Atalanta')
```

**First disagreeing instance** `battle_death.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    Siege of Constantinople | 1235

Returned query gives 2 row(s), 2 column(s):

    Siege of Constantinople | 1235
    Siege of Constantinople | 1235

Difference: duplicate_multiplicity_only; 1 row(s) in common, 0 only in the gold, 0 only in the returned result.

### R360  (question 259, database `student_transcripts_tracking`)

- Returned by: omnisql-32b/seed202
- Returned in cell: both A and D
- Class mass: 50/50
- Instances disagreeing: 22 of 55 (40%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find the last name of the students who currently live in North Carolina but have not registered in any degree program.

**Gold.**
```sql
SELECT T1.last_name FROM Students AS T1 JOIN Addresses AS T2 ON T1.current_address_id  =  T2.address_id WHERE T2.state_province_county  =  'NorthCarolina' EXCEPT SELECT DISTINCT T3.last_name FROM Students AS T3 JOIN Student_Enrolment AS T4 ON T3.student_id  =  T4.student_id
```

**Returned.**
```sql
SELECT s.last_name
FROM Students s
JOIN Addresses a ON s.current_address_id = a.address_id
LEFT JOIN Student_Enrolment se ON s.student_id = se.student_id
WHERE a.state_province_county = 'North Carolina'
AND se.student_enrolment_id IS NULL
```

**First disagreeing instance** `student_transcripts_tracking.sqlite` (this is the shipped benchmark database).

Gold returns 2 row(s), 1 column(s):

    Gleichner
    Weimann

Returned query gives 0 row(s), None column(s):

    (no rows)

Difference: rep_empty; 0 row(s) in common, 2 only in the gold, 0 only in the returned result.

### R361  (question 260, database `student_transcripts_tracking`)

- Returned by: omnisql-32b/seed202
- Returned in cell: both A and D
- Class mass: 50/50
- Instances disagreeing: 22 of 55 (40%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the last name of the students who live in North Carolina but have not registered in any degree programs?

**Gold.**
```sql
SELECT T1.last_name FROM Students AS T1 JOIN Addresses AS T2 ON T1.current_address_id  =  T2.address_id WHERE T2.state_province_county  =  'NorthCarolina' EXCEPT SELECT DISTINCT T3.last_name FROM Students AS T3 JOIN Student_Enrolment AS T4 ON T3.student_id  =  T4.student_id
```

**Returned.**
```sql
SELECT s.last_name
FROM Students s
JOIN Addresses a ON s.current_address_id = a.address_id
LEFT JOIN Student_Enrolment se ON s.student_id = se.student_id
WHERE a.state_province_county = 'North Carolina' AND se.degree_program_id IS NULL
```

**First disagreeing instance** `student_transcripts_tracking.sqlite` (this is the shipped benchmark database).

Gold returns 2 row(s), 1 column(s):

    Gleichner
    Weimann

Returned query gives 0 row(s), None column(s):

    (no rows)

Difference: rep_empty; 0 row(s) in common, 2 only in the gold, 0 only in the returned result.

### R362  (question 266, database `student_transcripts_tracking`)

- Returned by: omnisql-32b/seed202, omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 22/50, 22/50
- Instances disagreeing: 55 of 55 (100%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Which place holds the most number of students currently? List the id and all lines.

**Gold.**
```sql
SELECT T1.address_id ,  T1.line_1 ,  T1.line_2 FROM Addresses AS T1 JOIN Students AS T2 ON T1.address_id  =  T2.current_address_id GROUP BY T1.address_id ORDER BY count(*) DESC LIMIT 1
```

**Returned.**
```sql
SELECT a.address_id, a.line_1, a.line_2, a.line_3
FROM Addresses a
JOIN Students s ON a.address_id = s.current_address_id
GROUP BY a.address_id, a.line_1, a.line_2, a.line_3
ORDER BY COUNT(*) DESC
LIMIT 1
```

**First disagreeing instance** `student_transcripts_tracking.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 3 column(s):

    9 | 0643 Muller Vista | Suite 383

Returned query gives 1 row(s), 4 column(s):

    9 | 0643 Muller Vista | Suite 383 | NULL

Difference: col_count_differs, disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R363  (question 269, database `student_transcripts_tracking`)

- Returned by: omnisql-32b/seed202
- Returned in cell: both A and D
- Class mass: 26/50
- Instances disagreeing: 31 of 55 (56%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the id of the semester that had both Masters and Bachelors students enrolled?

**Gold.**
```sql
SELECT DISTINCT T2.semester_id FROM Degree_Programs AS T1 JOIN Student_Enrolment AS T2 ON T1.degree_program_id  =  T2.degree_program_id WHERE degree_summary_name  =  'Master' INTERSECT SELECT DISTINCT T2.semester_id FROM Degree_Programs AS T1 JOIN Student_Enrolment AS T2 ON T1.degree_program_id  =  T2.degree_program_id WHERE degree_summary_name  =  'Bachelor'
```

**Returned.**
```sql
SELECT 
    se.semester_id
FROM 
    Semesters se
JOIN 
    Student_Enrolment se1 ON se.semester_id = se1.semester_id
JOIN 
    Degree_Programs dp ON se1.degree_program_id = dp.degree_program_id
WHERE 
    dp.degree_summary_name = 'Master'

INTERSECT

SELECT 
    se.semester_id
FROM 
    Semesters se
JOIN 
    Student_Enrolment se1 ON se.semester_id = se1.semester_id
JOIN 
    Degree_Programs dp ON se1.degree_program_id = dp.degree_program_id
WHERE 
    dp.degree_summary_name = 'Bachelors'
```

**First disagreeing instance** `student_transcripts_tracking.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    13

Returned query gives 0 row(s), None column(s):

    (no rows)

Difference: rep_empty; 0 row(s) in common, 1 only in the gold, 0 only in the returned result.

### R364  (question 270, database `student_transcripts_tracking`)

- Returned by: omnisql-32b/seed202
- Returned in cell: both A and D
- Class mass: 48/50
- Instances disagreeing: 16 of 55 (29%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find the first name of the students who permanently live in Haiti or have the cell phone number 09700166582.

**Gold.**
```sql
select t1.first_name from students as t1 join addresses as t2 on t1.permanent_address_id  =  t2.address_id where t2.country  =  'haiti' or t1.cell_mobile_number  =  '09700166582'
```

**Returned.**
```sql
SELECT S.first_name
FROM Students S
JOIN Addresses A ON S.permanent_address_id = A.address_id
WHERE A.country = 'Haiti' OR S.cell_mobile_number = '09700166582'
```

**First disagreeing instance** `student_transcripts_tracking.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    Jarvis

Returned query gives 4 row(s), 1 column(s):

    Hobart
    Warren
    Jarvis
    Delaney

Difference: gold_subset_of_rep; 1 row(s) in common, 0 only in the gold, 3 only in the returned result.

### R365  (question 309, database `tvshow`)

- Returned by: omnisql-32b/seed202, omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 20/50, 17/50
- Instances disagreeing: 25 of 25 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** which countries' tv channels are not playing any cartoon  Todd Casey writes?

**Gold.**
```sql
SELECT country FROM TV_Channel EXCEPT SELECT T1.country FROM TV_Channel AS T1 JOIN cartoon AS T2 ON T1.id = T2.Channel WHERE T2.written_by  =  'Todd Casey'
```

**Returned.**
```sql
SELECT Country
FROM TV_Channel
WHERE id NOT IN (
    SELECT Channel
    FROM Cartoon
    WHERE Written_by = 'Todd Casey'
)
```

**First disagreeing instance** `tvshow.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    Poland

Returned query gives 13 row(s), 1 column(s):

    Italy
    Italy
    Italy
    Italy
    United Kingdom
    Italy
    Poland
    Italy
    Italy
    Italy
    Italy
    Italy
    ... (13 rows total)

Difference: gold_subset_of_rep; 1 row(s) in common, 0 only in the gold, 2 only in the returned result.

### R366  (question 311, database `tvshow`)

- Returned by: omnisql-32b/seed202
- Returned in cell: A only
- Class mass: 24/50
- Instances disagreeing: 25 of 25 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find the series name and country of the tv channel that is playing some cartoons  Ben Jones and Michael Chang directs?

**Gold.**
```sql
SELECT T1.series_name ,  T1.country FROM TV_Channel AS T1 JOIN cartoon AS T2 ON T1.id = T2.Channel WHERE T2.directed_by  =  'Michael Chang' INTERSECT SELECT T1.series_name ,  T1.country FROM TV_Channel AS T1 JOIN cartoon AS T2 ON T1.id = T2.Channel WHERE T2.directed_by  =  'Ben Jones'
```

**Returned.**
```sql
SELECT 
    TV_Channel.series_name, 
    TV_Channel.Country
FROM 
    Cartoon
INNER JOIN 
    TV_Channel
ON 
    Cartoon.Channel = TV_Channel.id
WHERE 
    Cartoon.Directed_by LIKE '%Ben Jones%' 
    OR Cartoon.Directed_by LIKE '%Michael Chang%'
```

**First disagreeing instance** `tvshow.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    MTV Dance | United Kingdom

Returned query gives 8 row(s), 2 column(s):

    Sky Radio | Italy
    Music Box Italia | Italy
    MTV Hits | Italy
    MTV Rocks | United Kingdom
    MTV Dance | United Kingdom
    MTV Dance | United Kingdom
    Classica | Italy
    MTV Dance | United Kingdom

Difference: gold_subset_of_rep; 1 row(s) in common, 0 only in the gold, 5 only in the returned result.

### R367  (question 311, database `tvshow`)

- Returned by: omnisql-32b/seed202
- Returned in cell: D only
- Class mass: 13/50
- Instances disagreeing: 25 of 25 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find the series name and country of the tv channel that is playing some cartoons  Ben Jones and Michael Chang directs?

**Gold.**
```sql
SELECT T1.series_name ,  T1.country FROM TV_Channel AS T1 JOIN cartoon AS T2 ON T1.id = T2.Channel WHERE T2.directed_by  =  'Michael Chang' INTERSECT SELECT T1.series_name ,  T1.country FROM TV_Channel AS T1 JOIN cartoon AS T2 ON T1.id = T2.Channel WHERE T2.directed_by  =  'Ben Jones'
```

**Returned.**
```sql
SELECT 
    TV_Channel.series_name, 
    TV_Channel.Country
FROM 
    Cartoon
INNER JOIN 
    TV_Channel 
ON 
    Cartoon.Channel = TV_Channel.id
WHERE 
    Cartoon.Directed_by IN ('Ben Jones', 'Michael Chang')
```

**First disagreeing instance** `tvshow.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    MTV Dance | United Kingdom

Returned query gives 8 row(s), 2 column(s):

    Sky Radio | Italy
    Music Box Italia | Italy
    MTV Hits | Italy
    MTV Rocks | United Kingdom
    MTV Dance | United Kingdom
    MTV Dance | United Kingdom
    Classica | Italy
    MTV Dance | United Kingdom

Difference: gold_subset_of_rep; 1 row(s) in common, 0 only in the gold, 5 only in the returned result.

### R368  (question 315, database `tvshow`)

- Returned by: omnisql-32b/seed202
- Returned in cell: both A and D
- Class mass: 41/50
- Instances disagreeing: 25 of 25 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** find id of the tv channels that from the nations where have more than two tv channels.

**Gold.**
```sql
SELECT id FROM tv_channel GROUP BY country HAVING count(*)  >  2
```

**Returned.**
```sql
SELECT id
FROM TV_Channel
WHERE Country IN (
    SELECT Country
    FROM TV_Channel
    GROUP BY Country
    HAVING COUNT(*) > 2
)
```

**First disagreeing instance** `tvshow.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    700

Returned query gives 12 row(s), 1 column(s):

    700
    701
    703
    704
    705
    708
    713
    714
    715
    717
    719
    728

Difference: gold_subset_of_rep; 1 row(s) in common, 0 only in the gold, 11 only in the returned result.

### R369  (question 362, database `world_1`)

- Returned by: omnisql-32b/seed202
- Returned in cell: both A and D
- Class mass: 31/50
- Instances disagreeing: 5 of 46 (11%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the average GNP and total population in all US territory nations?

**Gold.**
```sql
SELECT avg(GNP) ,  sum(population) FROM country WHERE GovernmentForm  =  "US Territory"
```

**Returned.**
```sql
SELECT 
    AVG(GNP) AS Average_GNP, 
    SUM(Population) AS Total_Population
FROM 
    country
WHERE 
    Region = 'US territory'
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    510.3333333333333 | 329000

Returned query gives 1 row(s), 2 column(s):

    NULL | NULL

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R370  (question 363, database `world_1`)

- Returned by: omnisql-32b/seed202
- Returned in cell: both A and D
- Class mass: 20/48
- Instances disagreeing: 5 of 46 (11%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Give the mean GNP and total population of nations which are considered US territory.

**Gold.**
```sql
SELECT avg(GNP) ,  sum(population) FROM country WHERE GovernmentForm  =  "US Territory"
```

**Returned.**
```sql
SELECT 
    AVG(GNP) AS MeanGNP, 
    SUM(Population) AS TotalPopulation
FROM 
    country
WHERE 
    HeadOfState = 'United States'
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    510.3333333333333 | 329000

Returned query gives 1 row(s), 2 column(s):

    NULL | NULL

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R371  (question 370, database `world_1`)

- Returned by: omnisql-32b/seed202
- Returned in cell: both A and D
- Class mass: 43/50
- Instances disagreeing: 39 of 46 (85%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What is name of the nation that speaks the largest number of languages?

**Gold.**
```sql
SELECT T1.Name FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code  =  T2.CountryCode GROUP BY T1.Name ORDER BY COUNT(*) DESC LIMIT 1
```

**Returned.**
```sql
SELECT country.Name
FROM country
INNER JOIN countrylanguage ON country.Code = countrylanguage.CountryCode
GROUP BY country.Code
ORDER BY COUNT(countrylanguage.Language) DESC
LIMIT 1
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    United States

Returned query gives 1 row(s), 1 column(s):

    Canada

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R372  (question 371, database `world_1`)

- Returned by: omnisql-32b/seed202
- Returned in cell: both A and D
- Class mass: 40/50
- Instances disagreeing: 39 of 46 (85%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Give the name of the nation that uses the greatest amount of languages.

**Gold.**
```sql
SELECT T1.Name FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code  =  T2.CountryCode GROUP BY T1.Name ORDER BY COUNT(*) DESC LIMIT 1
```

**Returned.**
```sql
SELECT 
    country.Name
FROM 
    country
INNER JOIN 
    countrylanguage
ON 
    country.Code = countrylanguage.CountryCode
GROUP BY 
    country.Code
ORDER BY 
    COUNT(countrylanguage.Language) DESC
LIMIT 1
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    United States

Returned query gives 1 row(s), 1 column(s):

    Canada

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R373  (question 382, database `world_1`)

- Returned by: omnisql-32b/seed202, omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 49/50, 49/50
- Instances disagreeing: 22 of 46 (48%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the countries where either English or Dutch is officially spoken ?

**Gold.**
```sql
select t1.name from country as t1 join countrylanguage as t2 on t1.code  =  t2.countrycode where t2.language  =  "english" and isofficial  =  "t" union select t1.name from country as t1 join countrylanguage as t2 on t1.code  =  t2.countrycode where t2.language  =  "dutch" and isofficial  =  "t"
```

**Returned.**
```sql
SELECT country.Name
FROM country
INNER JOIN countrylanguage
ON country.Code = countrylanguage.CountryCode
WHERE (countrylanguage.Language = 'English' OR countrylanguage.Language = 'Dutch')
  AND countrylanguage.IsOfficial = 'T'
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 0 row(s), None column(s):

    (no rows)

Returned query gives 48 row(s), 1 column(s):

    Aruba
    Anguilla
    Netherlands Antilles
    American Samoa
    Antigua and Barbuda
    Australia
    Belgium
    Belize
    Bermuda
    Barbados
    Canada
    Cocos (Keeling) Islands
    ... (48 rows total)

Difference: gold_empty; 0 row(s) in common, 0 only in the gold, 48 only in the returned result.

### R374  (question 383, database `world_1`)

- Returned by: omnisql-32b/seed202
- Returned in cell: both A and D
- Class mass: 34/50
- Instances disagreeing: 31 of 46 (67%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Which language is the most popular on Asian ?

**Gold.**
```sql
SELECT T2.Language FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code  =  T2.CountryCode WHERE T1.Continent  =  "Asia" GROUP BY T2.Language ORDER BY COUNT (*) DESC LIMIT 1
```

**Returned.**
```sql
SELECT 
    countrylanguage.Language
FROM 
    country
INNER JOIN 
    countrylanguage
ON 
    country.Code = countrylanguage.CountryCode
WHERE 
    country.Continent = 'Asia'
ORDER BY 
    countrylanguage.Percentage DESC
LIMIT 1
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    Arabic

Returned query gives 1 row(s), 1 column(s):

    Dhivehi

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R375  (question 407, database `world_1`)

- Returned by: omnisql-32b/seed202
- Returned in cell: both A and D
- Class mass: 22/50
- Instances disagreeing: 46 of 46 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Give the country codes for countries in which people does not speak English.

**Gold.**
```sql
SELECT DISTINCT CountryCode FROM countrylanguage WHERE LANGUAGE != "English"
```

**Returned.**
```sql
SELECT Code 
FROM country 
WHERE Code NOT IN (
    SELECT CountryCode 
    FROM countrylanguage 
    WHERE Language = 'English'
)
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 223 row(s), 1 column(s):

    ABW
    AFG
    AGO
    ALB
    AND
    ANT
    ARE
    ARG
    ARM
    ASM
    ATG
    AUS
    ... (223 rows total)

Returned query gives 179 row(s), 1 column(s):

    AFG
    AGO
    ALB
    AND
    ARE
    ARG
    ARM
    ATA
    ATF
    AUT
    AZE
    BDI
    ... (179 rows total)

Difference: values differ; 173 row(s) in common, 50 only in the gold, 6 only in the returned result.

### R376  (question 410, database `world_1`)

- Returned by: omnisql-32b/seed202
- Returned in cell: both A and D
- Class mass: 24/50
- Instances disagreeing: 9 of 46 (20%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Which cities are in European countries where English is not spoken officially?

**Gold.**
```sql
SELECT DISTINCT T2.Name FROM country AS T1 JOIN city AS T2 ON T2.CountryCode  =  T1.Code WHERE T1.Continent  =  'Europe' AND T1.Name NOT IN (SELECT T3.Name FROM country AS T3 JOIN countrylanguage AS T4 ON T3.Code  =  T4.CountryCode WHERE T4.IsOfficial  =  'T' AND T4.Language  =  'English')
```

**Returned.**
```sql
SELECT c.Name
FROM city c
JOIN country co ON c.CountryCode = co.Code
WHERE co.Continent = 'Europe'
  AND c.CountryCode NOT IN (
    SELECT cl.CountryCode
    FROM countrylanguage cl
    WHERE cl.Language = 'English' AND cl.IsOfficial = 'T'
  )
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 753 row(s), 1 column(s):

    Amsterdam
    Rotterdam
    Haag
    Utrecht
    Eindhoven
    Tilburg
    Groningen
    Breda
    Apeldoorn
    Nijmegen
    Enschede
    Haarlem
    ... (753 rows total)

Returned query gives 755 row(s), 1 column(s):

    Tirana
    Andorra la Vella
    Wien
    Graz
    Linz
    Salzburg
    Innsbruck
    Klagenfurt
    Antwerpen
    Gent
    Charleroi
    Liège
    ... (755 rows total)

Difference: duplicate_multiplicity_only; 753 row(s) in common, 0 only in the gold, 0 only in the returned result.

### R377  (question 413, database `world_1`)

- Returned by: omnisql-32b/seed202
- Returned in cell: both A and D
- Class mass: 49/50
- Instances disagreeing: 44 of 46 (96%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What are the name, independence year, and surface area of the country with the least number of nationalities?

**Gold.**
```sql
SELECT Name ,  SurfaceArea ,  IndepYear FROM country ORDER BY Population LIMIT 1
```

**Returned.**
```sql
SELECT 
    c.Name, 
    c.IndepYear, 
    c.SurfaceArea
FROM 
    country AS c
INNER JOIN 
    countrylanguage AS cl
ON 
    c.Code = cl.CountryCode
GROUP BY 
    c.Code
ORDER BY 
    COUNT(DISTINCT cl.Language)
LIMIT 1
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 3 column(s):

    Antarctica | 13120000.0 | NULL

Returned query gives 1 row(s), 3 column(s):

    Anguilla | NULL | 96.0

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R378  (question 431, database `world_1`)

- Returned by: omnisql-32b/seed202, omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 15/50, 18/50
- Instances disagreeing: 46 of 46 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the language spoken by the largest percentage of people in each nation?

**Gold.**
```sql
SELECT LANGUAGE ,  CountryCode ,  max(Percentage) FROM countrylanguage GROUP BY CountryCode
```

**Returned.**
```sql
SELECT 
    c.Name AS CountryName, 
    cl.Language AS MostSpokenLanguage
FROM 
    country AS c
INNER JOIN 
    countrylanguage AS cl
ON 
    c.Code = cl.CountryCode
WHERE 
    cl.Percentage = (
        SELECT MAX(cl2.Percentage)
        FROM countrylanguage AS cl2
        WHERE cl2.CountryCode = cl.CountryCode
    )
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 233 row(s), 3 column(s):

    Papiamento | ABW | 76.7
    Pashto | AFG | 52.4
    Ovimbundu | AGO | 37.2
    English | AIA | 0.0
    Albaniana | ALB | 97.9
    Spanish | AND | 44.6
    Papiamento | ANT | 86.2
    Arabic | ARE | 42.0
    Spanish | ARG | 96.8
    Armenian | ARM | 93.4
    Samoan | ASM | 90.6
    Creole English | ATG | 95.7
    ... (233 rows total)

Returned query gives 241 row(s), 2 column(s):

    Aruba | Papiamento
    Afghanistan | Pashto
    Angola | Ovimbundu
    Anguilla | English
    Albania | Albaniana
    Andorra | Spanish
    Netherlands Antilles | Papiamento
    United Arab Emirates | Arabic
    Argentina | Spanish
    Armenia | Armenian
    American Samoa | Samoan
    Antigua and Barbuda | Creole English
    ... (241 rows total)

Difference: col_count_differs, disjoint; 0 row(s) in common, 233 only in the gold, 241 only in the returned result.

### R379  (question 433, database `world_1`)

- Returned by: omnisql-32b/seed202
- Returned in cell: both A and D
- Class mass: 18/50
- Instances disagreeing: 46 of 46 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the total number of countries where Spanish is spoken by the largest percentage of people?

**Gold.**
```sql
SELECT count(*) ,   max(Percentage) FROM countrylanguage WHERE LANGUAGE  =  "Spanish" GROUP BY CountryCode
```

**Returned.**
```sql
SELECT COUNT(*) AS TotalCountries
FROM countrylanguage
WHERE Language = 'Spanish'
  AND Percentage = (
    SELECT MAX(Percentage)
    FROM countrylanguage
    WHERE Language = 'Spanish'
  )
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 28 row(s), 2 column(s):

    1 | 7.4
    1 | 44.6
    1 | 96.8
    1 | 31.6
    1 | 87.7
    1 | 0.7
    1 | 89.7
    1 | 99.0
    1 | 97.5
    1 | 100.0
    1 | 98.0
    1 | 93.0
    ... (28 rows total)

Returned query gives 1 row(s), 1 column(s):

    2

Difference: col_count_differs, disjoint; 0 row(s) in common, 27 only in the gold, 1 only in the returned result.

### R380  (question 434, database `world_1`)

- Returned by: omnisql-32b/seed202
- Returned in cell: both A and D
- Class mass: 28/50
- Instances disagreeing: 46 of 46 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Count the number of countries for which Spanish is predominantly spoken .

**Gold.**
```sql
SELECT count(*) ,   max(Percentage) FROM countrylanguage WHERE LANGUAGE  =  "Spanish" GROUP BY CountryCode
```

**Returned.**
```sql
SELECT COUNT(DISTINCT T1.CountryCode)
FROM countrylanguage AS T1
WHERE T1.Language = 'Spanish'
  AND T1.Percentage = (
    SELECT MAX(Percentage)
    FROM countrylanguage AS T2
    WHERE T2.CountryCode = T1.CountryCode
  )
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 28 row(s), 2 column(s):

    1 | 7.4
    1 | 44.6
    1 | 96.8
    1 | 31.6
    1 | 87.7
    1 | 0.7
    1 | 89.7
    1 | 99.0
    1 | 97.5
    1 | 100.0
    1 | 98.0
    1 | 93.0
    ... (28 rows total)

Returned query gives 1 row(s), 1 column(s):

    21

Difference: col_count_differs, disjoint; 0 row(s) in common, 27 only in the gold, 1 only in the returned result.

### R381  (question 462, database `network_1`)

- Returned by: omnisql-32b/seed202
- Returned in cell: both A and D
- Class mass: 29/50
- Instances disagreeing: 27 of 29 (93%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the average grade of students who have friends?

**Gold.**
```sql
SELECT avg(grade) FROM Highschooler WHERE id IN (SELECT T1.student_id FROM Friend AS T1 JOIN Highschooler AS T2 ON T1.student_id  =  T2.id)
```

**Returned.**
```sql
SELECT AVG(H.grade) AS average_grade
FROM Highschooler H
INNER JOIN Friend F ON H.ID = F.student_id
```

**First disagreeing instance** `network_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    10.428571428571429

Returned query gives 1 row(s), 1 column(s):

    10.25

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R382  (question 468, database `dog_kennels`)

- Returned by: omnisql-32b/seed202
- Returned in cell: both A and D
- Class mass: 27/50
- Instances disagreeing: 48 of 48 (100%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Which person has the most dogs? List the id, first name and last name.

**Gold.**
```sql
SELECT T1.owner_id ,  T2.first_name ,  T2.last_name FROM Dogs AS T1 JOIN Owners AS T2 ON T1.owner_id  =  T2.owner_id GROUP BY T1.owner_id ORDER BY count(*) DESC LIMIT 1
```

**Returned.**
```sql
SELECT o.owner_id, o.first_name, o.last_name, COUNT(d.dog_id) AS num_dogs
FROM Owners o
JOIN Dogs d ON o.owner_id = d.owner_id
GROUP BY o.owner_id, o.first_name, o.last_name
ORDER BY num_dogs DESC
LIMIT 1
```

**First disagreeing instance** `dog_kennels.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 3 column(s):

    14 | Rachelle | Funk

Returned query gives 1 row(s), 4 column(s):

    14 | Rachelle | Funk | 3

Difference: col_count_differs, disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R383  (question 480, database `dog_kennels`)

- Returned by: omnisql-32b/seed202
- Returned in cell: A only
- Class mass: 23/50
- Instances disagreeing: 42 of 48 (88%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** List the last name of the owner owning the youngest dog.

**Gold.**
```sql
SELECT T1.last_name FROM Owners AS T1 JOIN Dogs AS T2 ON T1.owner_id  =  T2.owner_id WHERE T2.age  =  ( SELECT max(age) FROM Dogs )
```

**Returned.**
```sql
SELECT O.last_name
FROM Owners O
JOIN Dogs D ON O.owner_id = D.owner_id
WHERE D.date_of_birth = (SELECT MAX(date_of_birth) FROM Dogs)
```

**First disagreeing instance** `dog_kennels.sqlite` (this is the shipped benchmark database).

Gold returns 3 row(s), 1 column(s):

    Feil
    Fisher
    Rippin

Returned query gives 1 row(s), 1 column(s):

    Mertz

Difference: disjoint; 0 row(s) in common, 3 only in the gold, 1 only in the returned result.

### R384  (question 480, database `dog_kennels`)

- Returned by: omnisql-32b/seed202
- Returned in cell: D only
- Class mass: 14/50
- Instances disagreeing: 41 of 48 (85%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** List the last name of the owner owning the youngest dog.

**Gold.**
```sql
SELECT T1.last_name FROM Owners AS T1 JOIN Dogs AS T2 ON T1.owner_id  =  T2.owner_id WHERE T2.age  =  ( SELECT max(age) FROM Dogs )
```

**Returned.**
```sql
SELECT 
    o.last_name 
FROM 
    Owners o
WHERE 
    o.owner_id = (
        SELECT 
            d.owner_id 
        FROM 
            Dogs d
        WHERE 
            d.dog_id = (
                SELECT 
                    dog_id 
                FROM 
                    Dogs 
                ORDER BY 
                    date_of_birth DESC 
                LIMIT 1
            )
    )
```

**First disagreeing instance** `dog_kennels.sqlite` (this is the shipped benchmark database).

Gold returns 3 row(s), 1 column(s):

    Feil
    Fisher
    Rippin

Returned query gives 1 row(s), 1 column(s):

    Mertz

Difference: disjoint; 0 row(s) in common, 3 only in the gold, 1 only in the returned result.

### R385  (question 481, database `dog_kennels`)

- Returned by: omnisql-32b/seed202
- Returned in cell: both A and D
- Class mass: 22/50
- Instances disagreeing: 42 of 48 (88%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Who owns the youngest dog? Give me his or her last name.

**Gold.**
```sql
SELECT T1.last_name FROM Owners AS T1 JOIN Dogs AS T2 ON T1.owner_id  =  T2.owner_id WHERE T2.age  =  ( SELECT max(age) FROM Dogs )
```

**Returned.**
```sql
SELECT O.last_name
FROM Owners O
JOIN Dogs D ON O.owner_id = D.owner_id
WHERE D.date_of_birth = (
    SELECT MAX(date_of_birth)
    FROM Dogs
)
```

**First disagreeing instance** `dog_kennels.sqlite` (this is the shipped benchmark database).

Gold returns 3 row(s), 1 column(s):

    Feil
    Fisher
    Rippin

Returned query gives 1 row(s), 1 column(s):

    Mertz

Difference: disjoint; 0 row(s) in common, 3 only in the gold, 1 only in the returned result.

### R386  (question 507, database `real_estate_properties`)

- Returned by: omnisql-32b/seed202, omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 31/50, 31/50
- Instances disagreeing: 9 of 32 (28%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the names of properties that are either houses or apartments with more than 1 room?

**Gold.**
```sql
SELECT property_name FROM Properties WHERE property_type_code  =  "House" UNION SELECT property_name FROM Properties WHERE property_type_code  =  "Apartment" AND room_count  >  1
```

**Returned.**
```sql
SELECT property_name
FROM Properties
WHERE property_type_code IN ('House', 'Apartment') AND room_count > 1
```

**First disagreeing instance** `real_estate_properties.sqlite` (this is the shipped benchmark database).

Gold returns 8 row(s), 1 column(s):

    longacre
    parc coliseum
    parc east
    park
    renoir
    ten tower
    the cole
    vogue

Returned query gives 7 row(s), 1 column(s):

    park
    parc east
    vogue
    longacre
    renoir
    ten tower
    parc coliseum

Difference: rep_subset_of_gold; 7 row(s) in common, 1 only in the gold, 0 only in the returned result.

### R387  (question 41, database `pets_1`)

- Returned by: omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 25/50
- Instances disagreeing: 26 of 27 (96%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find the first name of students who have cat or dog.

**Gold.**
```sql
SELECT DISTINCT T1.Fname FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid  =  T2.stuid JOIN pets AS T3 ON T3.petid  =  T2.petid WHERE T3.pettype  =  'cat' OR T3.pettype  =  'dog'
```

**Returned.**
```sql
SELECT Student.Fname
FROM Student
INNER JOIN Has_Pet ON Student.StuID = Has_Pet.StuID
INNER JOIN Pets ON Has_Pet.PetID = Pets.PetID
WHERE Pets.PetType IN ('cat', 'dog')
```

**First disagreeing instance** `pets_1.sqlite` (this is the shipped benchmark database).

Gold returns 2 row(s), 1 column(s):

    Linda
    Tracy

Returned query gives 3 row(s), 1 column(s):

    Linda
    Tracy
    Tracy

Difference: duplicate_multiplicity_only; 2 row(s) in common, 0 only in the gold, 0 only in the returned result.

### R388  (question 49, database `pets_1`)

- Returned by: omnisql-32b/seed303
- Returned in cell: A only
- Class mass: 26/50
- Instances disagreeing: 20 of 27 (74%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find the first name and age of students who have a dog but do not have a cat.

**Gold.**
```sql
SELECT T1.fname ,  T1.age FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid  =  T2.stuid JOIN pets AS T3 ON T3.petid  =  T2.petid WHERE T3.pettype  =  'dog' AND T1.stuid NOT IN (SELECT T1.stuid FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid  =  T2.stuid JOIN pets AS T3 ON T3.petid  =  T2.petid WHERE T3.pettype  =  'cat')
```

**Returned.**
```sql
SELECT S.Fname, S.Age
FROM Student S
WHERE EXISTS (
    SELECT 1
    FROM Has_Pet HP
    JOIN Pets P ON HP.PetID = P.PetID
    WHERE HP.StuID = S.StuID AND P.PetType = 'dog'
)
AND NOT EXISTS (
    SELECT 1
    FROM Has_Pet HP
    JOIN Pets P ON HP.PetID = P.PetID
    WHERE HP.StuID = S.StuID AND P.PetType = 'cat'
)
```

**First disagreeing instance** `pets_1.sqlite` (this is the shipped benchmark database).

Gold returns 2 row(s), 2 column(s):

    Tracy | 19
    Tracy | 19

Returned query gives 1 row(s), 2 column(s):

    Tracy | 19

Difference: duplicate_multiplicity_only; 1 row(s) in common, 0 only in the gold, 0 only in the returned result.

### R389  (question 50, database `pets_1`)

- Returned by: omnisql-32b/seed303
- Returned in cell: A only
- Class mass: 38/50
- Instances disagreeing: 25 of 27 (93%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the first name of every student who has a dog but does not have a cat?

**Gold.**
```sql
SELECT T1.fname ,  T1.age FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid  =  T2.stuid JOIN pets AS T3 ON T3.petid  =  T2.petid WHERE T3.pettype  =  'dog' AND T1.stuid NOT IN (SELECT T1.stuid FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid  =  T2.stuid JOIN pets AS T3 ON T3.petid  =  T2.petid WHERE T3.pettype  =  'cat')
```

**Returned.**
```sql
SELECT S.Fname
FROM Student S
JOIN Has_Pet HP ON S.StuID = HP.StuID
JOIN Pets P ON HP.PetID = P.PetID
WHERE P.PetType = 'dog'
EXCEPT
SELECT S.Fname
FROM Student S
JOIN Has_Pet HP ON S.StuID = HP.StuID
JOIN Pets P ON HP.PetID = P.PetID
WHERE P.PetType = 'cat'
```

**First disagreeing instance** `pets_1.sqlite` (this is the shipped benchmark database).

Gold returns 2 row(s), 2 column(s):

    Tracy | 19
    Tracy | 19

Returned query gives 1 row(s), 1 column(s):

    Tracy

Difference: col_count_differs, disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R390  (question 50, database `pets_1`)

- Returned by: omnisql-32b/seed303
- Returned in cell: D only
- Class mass: 15/50
- Instances disagreeing: 25 of 27 (93%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the first name of every student who has a dog but does not have a cat?

**Gold.**
```sql
SELECT T1.fname ,  T1.age FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid  =  T2.stuid JOIN pets AS T3 ON T3.petid  =  T2.petid WHERE T3.pettype  =  'dog' AND T1.stuid NOT IN (SELECT T1.stuid FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid  =  T2.stuid JOIN pets AS T3 ON T3.petid  =  T2.petid WHERE T3.pettype  =  'cat')
```

**Returned.**
```sql
SELECT DISTINCT S.Fname
FROM Student AS S
JOIN Has_Pet AS HP ON S.StuID = HP.StuID
JOIN Pets AS P ON HP.PetID = P.PetID
WHERE P.PetType = 'dog'
  AND S.StuID NOT IN (
    SELECT StuID
    FROM Has_Pet AS HP
    JOIN Pets AS P ON HP.PetID = P.PetID
    WHERE P.PetType = 'cat'
  )
```

**First disagreeing instance** `pets_1.sqlite` (this is the shipped benchmark database).

Gold returns 2 row(s), 2 column(s):

    Tracy | 19
    Tracy | 19

Returned query gives 1 row(s), 1 column(s):

    Tracy

Difference: col_count_differs, disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R391  (question 63, database `car_1`)

- Returned by: omnisql-32b/seed303
- Returned in cell: A only
- Class mass: 15/50
- Instances disagreeing: 41 of 60 (68%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find the name of the makers that produced some cars in 1970?

**Gold.**
```sql
SELECT DISTINCT T1.Maker FROM CAR_MAKERS AS T1 JOIN MODEL_LIST AS T2 ON T1.Id  =  T2.Maker JOIN CAR_NAMES AS T3 ON T2.model  =  T3.model JOIN CARS_DATA AS T4 ON T3.MakeId  =  T4.id WHERE T4.year  =  '1970';
```

**Returned.**
```sql
SELECT DISTINCT cm.Maker
FROM car_makers cm
JOIN model_list ml ON cm.Id = ml.Maker
JOIN car_names cn ON ml.ModelId = cn.MakeId
JOIN cars_data cd ON cn.MakeId = cd.Id
WHERE cd.Year = 1970
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 11 row(s), 1 column(s):

    gm
    chrysler
    amc
    ford
    citroen
    toyota
    nissan
    volkswagen
    peugeaut
    saab
    bmw

Returned query gives 22 row(s), 1 column(s):

    amc
    volkswagen
    bmw
    gm
    ford
    chrysler
    citroen
    nissan
    fiat
    honda
    mazda
    daimler benz
    ... (22 rows total)

Difference: gold_subset_of_rep; 11 row(s) in common, 0 only in the gold, 11 only in the returned result.

### R392  (question 66, database `car_1`)

- Returned by: omnisql-32b/seed303
- Returned in cell: A only
- Class mass: 11/50
- Instances disagreeing: 60 of 60 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the maker of the carr produced in the earliest  and what  year was it?

**Gold.**
```sql
SELECT T2.Make ,  T1.Year FROM CARS_DATA AS T1 JOIN CAR_NAMES AS T2 ON T1.Id  =  T2.MakeId WHERE T1.Year  =  (SELECT min(YEAR) FROM CARS_DATA);
```

**Returned.**
```sql
SELECT cm.Maker, cd.Year
FROM cars_data cd
JOIN car_names cn ON cd.Id = cn.MakeId
JOIN car_makers cm ON cn.Make = cm.FullName
WHERE cd.Year = (SELECT MIN(Year) FROM cars_data)
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 35 row(s), 2 column(s):

    chevrolet chevelle malibu | 1970
    buick skylark 320 | 1970
    plymouth satellite | 1970
    amc rebel sst | 1970
    ford torino | 1970
    ford galaxie 500 | 1970
    chevrolet impala | 1970
    plymouth fury iii | 1970
    pontiac catalina | 1970
    amc ambassador dpl | 1970
    citroen ds-21 pallas | 1970
    chevrolet chevelle concours (sw) | 1970
    ... (35 rows total)

Returned query gives 0 row(s), None column(s):

    (no rows)

Difference: rep_empty; 0 row(s) in common, 35 only in the gold, 0 only in the returned result.

### R393  (question 77, database `car_1`)

- Returned by: omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 27/50
- Instances disagreeing: 33 of 60 (55%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the count of the car models produced in the United States?

**Gold.**
```sql
SELECT count(*) FROM MODEL_LIST AS T1 JOIN CAR_MAKERS AS T2 ON T1.Maker  =  T2.Id JOIN COUNTRIES AS T3 ON T2.Country  =  T3.CountryId WHERE T3.CountryName  =  'usa';
```

**Returned.**
```sql
SELECT 
  COUNT(DISTINCT ml.Model) AS total_car_models
FROM 
  model_list ml
JOIN 
  car_makers cm ON ml.Maker = cm.Id
JOIN 
  countries c ON cm.Country = c.CountryId
WHERE 
  c.CountryName = 'United States'
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    13

Returned query gives 1 row(s), 1 column(s):

    0

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R394  (question 85, database `car_1`)

- Returned by: omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 28/50
- Instances disagreeing: 11 of 60 (18%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the names of all European countries with at least 3 manufacturers?

**Gold.**
```sql
SELECT T1.CountryName FROM COUNTRIES AS T1 JOIN CONTINENTS AS T2 ON T1.Continent  =  T2.ContId JOIN CAR_MAKERS AS T3 ON T1.CountryId  =  T3.Country WHERE T2.Continent  =  'europe' GROUP BY T1.CountryName HAVING count(*)  >=  3;
```

**Returned.**
```sql
SELECT c.CountryName
FROM car_makers cm
JOIN countries c ON cm.Country = c.CountryId
JOIN continents cont ON c.Continent = cont.ContId
WHERE cont.Continent = 'Europe'
GROUP BY c.CountryName
HAVING COUNT(cm.Id) >= 3
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 2 row(s), 1 column(s):

    france
    germany

Returned query gives 0 row(s), None column(s):

    (no rows)

Difference: rep_empty; 0 row(s) in common, 2 only in the gold, 0 only in the returned result.

### R395  (question 92, database `car_1`)

- Returned by: omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 6/50
- Instances disagreeing: 60 of 60 (100%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What car has the most different versions?

**Gold.**
```sql
SELECT Model FROM CAR_NAMES GROUP BY Model ORDER BY count(*) DESC LIMIT 1;
```

**Returned.**
```sql
SELECT 
    Make AS MostDifferentCar,
    COUNT(*) AS NumberOfVersions
FROM 
    car_names
GROUP BY 
    Make
ORDER BY 
    NumberOfVersions DESC
LIMIT 1
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    ford

Returned query gives 1 row(s), 2 column(s):

    ford pinto | 6

Difference: col_count_differs, disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R396  (question 100, database `car_1`)

- Returned by: omnisql-32b/seed303
- Returned in cell: A only
- Class mass: 12/50
- Instances disagreeing: 26 of 60 (43%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the different models created by either General Motors or over 3500 lbs?

**Gold.**
```sql
SELECT DISTINCT T2.Model FROM CAR_NAMES AS T1 JOIN MODEL_LIST AS T2 ON T1.Model  =  T2.Model JOIN CAR_MAKERS AS T3 ON T2.Maker  =  T3.Id JOIN CARS_DATA AS T4 ON T1.MakeId  =  T4.Id WHERE T3.FullName  =  'General Motors' OR T4.weight  >  3500;
```

**Returned.**
```sql
SELECT DISTINCT T1.Model 
FROM car_names AS T1
INNER JOIN car_makers AS T2 ON T1.Make = T2.FullName 
WHERE T2.FullName = "General Motors"

UNION

SELECT DISTINCT T1.Model 
FROM car_names AS T1
INNER JOIN cars_data AS T3 ON T1.MakeId = T3.Id 
WHERE T3.Weight > 3500
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 13 row(s), 1 column(s):

    chevrolet
    buick
    ford
    plymouth
    pontiac
    amc
    dodge
    mercury
    oldsmobile
    chrysler
    mercedes-benz
    cadillac
    ... (13 rows total)

Returned query gives 14 row(s), 1 column(s):

    amc
    buick
    cadillac
    chevrolet
    chrysler
    dodge
    ford
    hi
    mercedes
    mercedes-benz
    mercury
    oldsmobile
    ... (14 rows total)

Difference: gold_subset_of_rep; 13 row(s) in common, 0 only in the gold, 1 only in the returned result.

### R397  (question 100, database `car_1`)

- Returned by: omnisql-32b/seed303
- Returned in cell: D only
- Class mass: 5/50
- Instances disagreeing: 58 of 60 (97%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the different models created by either General Motors or over 3500 lbs?

**Gold.**
```sql
SELECT DISTINCT T2.Model FROM CAR_NAMES AS T1 JOIN MODEL_LIST AS T2 ON T1.Model  =  T2.Model JOIN CAR_MAKERS AS T3 ON T2.Maker  =  T3.Id JOIN CARS_DATA AS T4 ON T1.MakeId  =  T4.Id WHERE T3.FullName  =  'General Motors' OR T4.weight  >  3500;
```

**Returned.**
```sql
SELECT DISTINCT T1.Model
FROM model_list AS T1
INNER JOIN car_makers AS T2 ON T1.Maker = T2.Id
INNER JOIN cars_data AS T3 ON T1.ModelId = T3.Id
WHERE T2.FullName = 'General Motors' OR T3.Weight > 3500
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 13 row(s), 1 column(s):

    chevrolet
    buick
    ford
    plymouth
    pontiac
    amc
    dodge
    mercury
    oldsmobile
    chrysler
    mercedes-benz
    cadillac
    ... (13 rows total)

Returned query gives 21 row(s), 1 column(s):

    amc
    audi
    buick
    cadillac
    capri
    chevrolet
    chrysler
    citroen
    datsun
    fiat
    ford
    honda
    ... (21 rows total)

Difference: values differ; 10 row(s) in common, 3 only in the gold, 11 only in the returned result.

### R398  (question 105, database `car_1`)

- Returned by: omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 50/50
- Instances disagreeing: 60 of 60 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** How many nations has more than 2 car makers ?

**Gold.**
```sql
select count(*) from countries as t1 join car_makers as t2 on t1.countryid  =  t2.country group by t1.countryid having count(*)  >  2
```

**Returned.**
```sql
SELECT COUNT(*) 
FROM (
    SELECT Country 
    FROM car_makers 
    GROUP BY Country 
    HAVING COUNT(*) > 2
) AS filtered_countries
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 4 row(s), 1 column(s):

    4
    4
    3
    5

Returned query gives 1 row(s), 1 column(s):

    4

Difference: rep_subset_of_gold; 1 row(s) in common, 2 only in the gold, 0 only in the returned result.

### R399  (question 106, database `car_1`)

- Returned by: omnisql-32b/seed303
- Returned in cell: A only
- Class mass: 48/50
- Instances disagreeing: 60 of 60 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the number of nations with more than 2 car makers ?

**Gold.**
```sql
select count(*) from countries as t1 join car_makers as t2 on t1.countryid  =  t2.country group by t1.countryid having count(*)  >  2
```

**Returned.**
```sql
SELECT COUNT(*)
FROM (
    SELECT T2.CountryName
    FROM car_makers AS T1
    INNER JOIN countries AS T2 ON T1.Country = T2.CountryId
    GROUP BY T2.CountryName
    HAVING COUNT(*) > 2
) AS subquery
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 4 row(s), 1 column(s):

    4
    4
    3
    5

Returned query gives 1 row(s), 1 column(s):

    4

Difference: rep_subset_of_gold; 1 row(s) in common, 2 only in the gold, 0 only in the returned result.

### R400  (question 106, database `car_1`)

- Returned by: omnisql-32b/seed303
- Returned in cell: D only
- Class mass: 28/50
- Instances disagreeing: 60 of 60 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the number of nations with more than 2 car makers ?

**Gold.**
```sql
select count(*) from countries as t1 join car_makers as t2 on t1.countryid  =  t2.country group by t1.countryid having count(*)  >  2
```

**Returned.**
```sql
SELECT COUNT(*)
FROM (
    SELECT Country
    FROM car_makers
    GROUP BY Country
    HAVING COUNT(*) > 2
) AS EligibleCountries
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 4 row(s), 1 column(s):

    4
    4
    3
    5

Returned query gives 1 row(s), 1 column(s):

    4

Difference: rep_subset_of_gold; 1 row(s) in common, 2 only in the gold, 0 only in the returned result.

### R401  (question 109, database `car_1`)

- Returned by: omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 25/50
- Instances disagreeing: 56 of 60 (93%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Which models are lighter than 3500 but not built by the 'Ford Motor Company'?

**Gold.**
```sql
SELECT DISTINCT T1.model FROM MODEL_LIST AS T1 JOIN CAR_NAMES AS T2 ON T1.Model  =  T2.Model JOIN CARS_DATA AS T3 ON T2.MakeId  =  T3.Id JOIN CAR_MAKERS AS T4 ON T1.Maker  =  T4.Id WHERE T3.weight  <  3500 AND T4.FullName != 'Ford Motor Company';
```

**Returned.**
```sql
SELECT cn.Model
FROM cars_data cd
JOIN car_names cn ON cd.Id = cn.MakeId
JOIN model_list ml ON cn.Model = ml.Model
JOIN car_makers cm ON ml.Maker = cm.Id
WHERE cd.Weight < 3500
AND cm.FullName != 'Ford Motor Company'
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 26 row(s), 1 column(s):

    plymouth
    amc
    citroen
    buick
    toyota
    datsun
    volkswagen
    peugeot
    audi
    saab
    bmw
    chevrolet
    ... (26 rows total)

Returned query gives 252 row(s), 1 column(s):

    plymouth
    amc
    citroen
    buick
    toyota
    plymouth
    amc
    datsun
    volkswagen
    peugeot
    audi
    saab
    ... (252 rows total)

Difference: duplicate_multiplicity_only; 26 row(s) in common, 0 only in the gold, 0 only in the returned result.

### R402  (question 112, database `car_1`)

- Returned by: omnisql-32b/seed303
- Returned in cell: D only
- Class mass: 13/50
- Instances disagreeing: 10 of 60 (17%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the ids and names of all countries that either have more than 3 car makers or produce fiats?

**Gold.**
```sql
select t1.countryid ,  t1.countryname from countries as t1 join car_makers as t2 on t1.countryid  =  t2.country group by t1.countryid having count(*)  >  3 union select t1.countryid ,  t1.countryname from countries as t1 join car_makers as t2 on t1.countryid  =  t2.country join model_list as t3 on t2.id  =  t3.maker where t3.model  =  'fiat';
```

**Returned.**
```sql
SELECT 
    c.CountryId,
    c.CountryName
FROM 
    countries c
INNER JOIN 
    car_makers cm ON c.CountryId = cm.Country
GROUP BY 
    c.CountryId, c.CountryName
HAVING 
    COUNT(cm.Id) > 3

UNION

SELECT 
    c.CountryId,
    c.CountryName
FROM 
    countries c
INNER JOIN 
    car_makers cm ON c.CountryId = cm.Country
INNER JOIN 
    car_names cn ON cm.Id = cn.MakeId
INNER JOIN 
    model_list ml ON cn.Model = ml.Model
WHERE 
    ml.Model = 'fiat'
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 4 row(s), 2 column(s):

    1 | usa
    2 | germany
    4 | japan
    5 | italy

Returned query gives 3 row(s), 2 column(s):

    1 | usa
    2 | germany
    4 | japan

Difference: rep_subset_of_gold; 3 row(s) in common, 1 only in the gold, 0 only in the returned result.

### R403  (question 140, database `flight_2`)

- Returned by: omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 43/50
- Instances disagreeing: 8 of 56 (14%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Give the number of Jetblue Airways flights.

**Gold.**
```sql
SELECT count(*) FROM FLIGHTS AS T1 JOIN AIRLINES AS T2 ON T1.Airline  =  T2.uid WHERE T2.Airline = "JetBlue Airways"
```

**Returned.**
```sql
SELECT COUNT(*) 
FROM flights 
INNER JOIN airlines ON flights.Airline = airlines.uid 
WHERE airlines.Airline = 'Jetblue Airways'
```

**First disagreeing instance** `flight_2.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    100

Returned query gives 1 row(s), 1 column(s):

    0

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R404  (question 223, database `wta_1`)

- Returned by: omnisql-32b/seed303
- Returned in cell: D only
- Class mass: 12/50
- Instances disagreeing: 7 of 33 (21%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the names of players who won in both 2013 and 2016?

**Gold.**
```sql
SELECT winner_name FROM matches WHERE YEAR  =  2013 INTERSECT SELECT winner_name FROM matches WHERE YEAR  =  2016
```

**Returned.**
```sql
SELECT 
    p.first_name || ' ' || p.last_name AS player_name
FROM 
    matches m
JOIN 
    players p ON m.winner_id = p.player_id
WHERE 
    m.year = 2013
INTERSECT
SELECT 
    p.first_name || ' ' || p.last_name AS player_name
FROM 
    matches m
JOIN 
    players p ON m.winner_id = p.player_id
WHERE 
    m.year = 2016
```

**First disagreeing instance** `wta_1v5080.sqlite`.

Gold returns 1 row(s), 1 column(s):

    3

Returned query gives 0 row(s), None column(s):

    (no rows)

Difference: rep_empty; 0 row(s) in common, 1 only in the gold, 0 only in the returned result.

### R405  (question 234, database `wta_1`)

- Returned by: omnisql-32b/seed303
- Returned in cell: D only
- Class mass: 9/50
- Instances disagreeing: 32 of 33 (97%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Find the name and rank points of the person who won the most times.

**Gold.**
```sql
SELECT winner_name ,  winner_rank_points FROM matches GROUP BY winner_name ORDER BY count(*) DESC LIMIT 1
```

**Returned.**
```sql
SELECT 
    T2.first_name || ' ' || T2.last_name AS name,
    T1.winner_rank_points AS rank_points
FROM 
    matches AS T1
INNER JOIN 
    players AS T2 ON T1.winner_id = T2.player_id
GROUP BY 
    T1.winner_id
ORDER BY 
    COUNT(T1.winner_id) DESC
LIMIT 1
```

**First disagreeing instance** `wta_1v5080.sqlite`.

Gold returns 1 row(s), 2 column(s):

    1 | 2841

Returned query gives 1 row(s), 2 column(s):

    50 n1Dy71YAK | 9

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R406  (question 235, database `wta_1`)

- Returned by: omnisql-32b/seed303
- Returned in cell: A only
- Class mass: 8/50
- Instances disagreeing: 33 of 33 (100%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What is the name of the player who has won the most matches, and how many rank points does this player have?

**Gold.**
```sql
SELECT winner_name ,  winner_rank_points FROM matches GROUP BY winner_name ORDER BY count(*) DESC LIMIT 1
```

**Returned.**
```sql
SELECT 
  P.first_name || ' ' || P.last_name AS player_name, 
  R.ranking_points
FROM 
  players P
  INNER JOIN (
    SELECT 
      winner_id, 
      COUNT(*) AS win_count
    FROM 
      matches
    GROUP BY 
      winner_id
    ORDER BY 
      win_count DESC
    LIMIT 1
  ) MW ON P.player_id = MW.winner_id
  INNER JOIN (
    SELECT 
      player_id, 
      ranking_points, 
      ranking_date
    FROM 
      rankings
    WHERE 
      (player_id, ranking_date) IN (
        SELECT 
          player_id, 
          MAX(ranking_date) 
        FROM 
          rankings 
        GROUP BY 
          player_id
      )
  ) R ON P.player_id = R.player_id
```

**First disagreeing instance** `wta_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    Angelique Kerber | 3715

Returned query gives 1 row(s), 2 column(s):

    Angelique Kerber | 3156

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R407  (question 235, database `wta_1`)

- Returned by: omnisql-32b/seed303
- Returned in cell: D only
- Class mass: 3/50
- Instances disagreeing: 33 of 33 (100%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What is the name of the player who has won the most matches, and how many rank points does this player have?

**Gold.**
```sql
SELECT winner_name ,  winner_rank_points FROM matches GROUP BY winner_name ORDER BY count(*) DESC LIMIT 1
```

**Returned.**
```sql
SELECT 
    p.first_name || ' ' || p.last_name AS PlayerName,
    SUM(r.ranking_points) AS TotalRankPoints
FROM 
    matches m
INNER JOIN 
    players p ON m.winner_id = p.player_id
INNER JOIN 
    rankings r ON p.player_id = r.player_id
GROUP BY 
    p.player_id, p.first_name, p.last_name
ORDER BY 
    COUNT(m.match_num) DESC
LIMIT 1
```

**First disagreeing instance** `wta_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    Angelique Kerber | 3715

Returned query gives 1 row(s), 2 column(s):

    Serena Williams | 63492420

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R408  (question 249, database `wta_1`)

- Returned by: omnisql-32b/seed303
- Returned in cell: A only
- Class mass: 25/50
- Instances disagreeing: 4 of 33 (12%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find the number of left handed winners who participated in the WTA Championships.

**Gold.**
```sql
SELECT count(DISTINCT winner_name) FROM matches WHERE tourney_name  =  'WTA Championships' AND winner_hand  =  'L'
```

**Returned.**
```sql
SELECT COUNT(*) 
FROM matches 
WHERE tourney_name = 'WTA Championships' AND winner_hand = 'L'
```

**First disagreeing instance** `wta_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    2

Returned query gives 1 row(s), 1 column(s):

    3

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R409  (question 249, database `wta_1`)

- Returned by: omnisql-32b/seed303
- Returned in cell: D only
- Class mass: 17/50
- Instances disagreeing: 6 of 33 (18%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find the number of left handed winners who participated in the WTA Championships.

**Gold.**
```sql
SELECT count(DISTINCT winner_name) FROM matches WHERE tourney_name  =  'WTA Championships' AND winner_hand  =  'L'
```

**Returned.**
```sql
SELECT 
    COUNT(DISTINCT m.winner_id) AS count_left_hand_winners
FROM 
    matches m
JOIN 
    players p ON m.winner_id = p.player_id
WHERE 
    m.tourney_name = 'WTA Championships' 
    AND p.hand = 'L'
```

**First disagreeing instance** `wta_1v50815.sqlite`.

Gold returns 1 row(s), 1 column(s):

    4

Returned query gives 1 row(s), 1 column(s):

    0

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R410  (question 253, database `battle_death`)

- Returned by: omnisql-32b/seed303
- Returned in cell: D only
- Class mass: 16/50
- Instances disagreeing: 3 of 28 (11%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** List the name and date the battle that has lost  Lettice and HMS Atalanta

**Gold.**
```sql
SELECT T1.name ,  T1.date FROM battle AS T1 JOIN ship AS T2 ON T1.id  =  T2.lost_in_battle WHERE T2.name  =  'Lettice' INTERSECT SELECT T1.name ,  T1.date FROM battle AS T1 JOIN ship AS T2 ON T1.id  =  T2.lost_in_battle WHERE T2.name  =  'HMS Atalanta'
```

**Returned.**
```sql
SELECT 
    b.name AS battle_name, 
    b.date AS battle_date
FROM 
    battle AS b
INNER JOIN 
    ship AS s
ON 
    b.id = s.lost_in_battle
WHERE 
    s.name IN ('Lettice', 'HMS Atalanta')
GROUP BY 
    b.id
HAVING 
    COUNT(DISTINCT s.name) = 2
```

**First disagreeing instance** `battle_deathv515patch4.sqlite`.

Gold returns 2 row(s), 2 column(s):

    Battle of Philippopolis | East
    East | 1234

Returned query gives 1 row(s), 2 column(s):

    East | 1234

Difference: rep_subset_of_gold; 1 row(s) in common, 1 only in the gold, 0 only in the returned result.

### R411  (question 259, database `student_transcripts_tracking`)

- Returned by: omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 50/50
- Instances disagreeing: 22 of 55 (40%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find the last name of the students who currently live in North Carolina but have not registered in any degree program.

**Gold.**
```sql
SELECT T1.last_name FROM Students AS T1 JOIN Addresses AS T2 ON T1.current_address_id  =  T2.address_id WHERE T2.state_province_county  =  'NorthCarolina' EXCEPT SELECT DISTINCT T3.last_name FROM Students AS T3 JOIN Student_Enrolment AS T4 ON T3.student_id  =  T4.student_id
```

**Returned.**
```sql
SELECT s.last_name
FROM Students s
JOIN Addresses a ON s.current_address_id = a.address_id
WHERE a.state_province_county = 'North Carolina'
AND s.student_id NOT IN (
    SELECT student_id
    FROM Student_Enrolment
)
```

**First disagreeing instance** `student_transcripts_tracking.sqlite` (this is the shipped benchmark database).

Gold returns 2 row(s), 1 column(s):

    Gleichner
    Weimann

Returned query gives 0 row(s), None column(s):

    (no rows)

Difference: rep_empty; 0 row(s) in common, 2 only in the gold, 0 only in the returned result.

### R412  (question 260, database `student_transcripts_tracking`)

- Returned by: omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 50/50
- Instances disagreeing: 22 of 55 (40%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the last name of the students who live in North Carolina but have not registered in any degree programs?

**Gold.**
```sql
SELECT T1.last_name FROM Students AS T1 JOIN Addresses AS T2 ON T1.current_address_id  =  T2.address_id WHERE T2.state_province_county  =  'NorthCarolina' EXCEPT SELECT DISTINCT T3.last_name FROM Students AS T3 JOIN Student_Enrolment AS T4 ON T3.student_id  =  T4.student_id
```

**Returned.**
```sql
SELECT s.last_name
FROM Students s
JOIN Addresses a ON s.current_address_id = a.address_id
WHERE a.state_province_county = 'North Carolina'
AND s.student_id NOT IN (
    SELECT se.student_id
    FROM Student_Enrolment se
)
```

**First disagreeing instance** `student_transcripts_tracking.sqlite` (this is the shipped benchmark database).

Gold returns 2 row(s), 1 column(s):

    Gleichner
    Weimann

Returned query gives 0 row(s), None column(s):

    (no rows)

Difference: rep_empty; 0 row(s) in common, 2 only in the gold, 0 only in the returned result.

### R413  (question 268, database `student_transcripts_tracking`)

- Returned by: omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 33/50
- Instances disagreeing: 40 of 55 (73%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find the semester when both Master students and Bachelor students got enrolled in.

**Gold.**
```sql
SELECT DISTINCT T2.semester_id FROM Degree_Programs AS T1 JOIN Student_Enrolment AS T2 ON T1.degree_program_id  =  T2.degree_program_id WHERE degree_summary_name  =  'Master' INTERSECT SELECT DISTINCT T2.semester_id FROM Degree_Programs AS T1 JOIN Student_Enrolment AS T2 ON T1.degree_program_id  =  T2.degree_program_id WHERE degree_summary_name  =  'Bachelor'
```

**Returned.**
```sql
SELECT 
    s.semester_name
FROM 
    Semesters s
JOIN 
    Student_Enrolment se ON s.semester_id = se.semester_id
JOIN 
    Degree_Programs dp ON se.degree_program_id = dp.degree_program_id
WHERE 
    dp.degree_summary_name = 'Master'
INTERSECT
SELECT 
    s.semester_name
FROM 
    Semesters s
JOIN 
    Student_Enrolment se ON s.semester_id = se.semester_id
JOIN 
    Degree_Programs dp ON se.degree_program_id = dp.degree_program_id
WHERE 
    dp.degree_summary_name = 'Bachelor'
```

**First disagreeing instance** `student_transcripts_tracking.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    13

Returned query gives 1 row(s), 1 column(s):

    fall 2018

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R414  (question 269, database `student_transcripts_tracking`)

- Returned by: omnisql-32b/seed303
- Returned in cell: D only
- Class mass: 22/50
- Instances disagreeing: 31 of 55 (56%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the id of the semester that had both Masters and Bachelors students enrolled?

**Gold.**
```sql
SELECT DISTINCT T2.semester_id FROM Degree_Programs AS T1 JOIN Student_Enrolment AS T2 ON T1.degree_program_id  =  T2.degree_program_id WHERE degree_summary_name  =  'Master' INTERSECT SELECT DISTINCT T2.semester_id FROM Degree_Programs AS T1 JOIN Student_Enrolment AS T2 ON T1.degree_program_id  =  T2.degree_program_id WHERE degree_summary_name  =  'Bachelor'
```

**Returned.**
```sql
SELECT s.semester_id
FROM Semesters s
JOIN Student_Enrolment se ON s.semester_id = se.semester_id
JOIN Degree_Programs dp ON se.degree_program_id = dp.degree_program_id
WHERE dp.degree_summary_name IN ('Masters', 'Bachelors')
GROUP BY s.semester_id
HAVING COUNT(DISTINCT dp.degree_summary_name) = 2
```

**First disagreeing instance** `student_transcripts_tracking.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    13

Returned query gives 0 row(s), None column(s):

    (no rows)

Difference: rep_empty; 0 row(s) in common, 1 only in the gold, 0 only in the returned result.

### R415  (question 271, database `student_transcripts_tracking`)

- Returned by: omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 50/50
- Instances disagreeing: 16 of 55 (29%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the first names of the students who live in Haiti permanently or have the cell phone number 09700166582?

**Gold.**
```sql
select t1.first_name from students as t1 join addresses as t2 on t1.permanent_address_id  =  t2.address_id where t2.country  =  'haiti' or t1.cell_mobile_number  =  '09700166582'
```

**Returned.**
```sql
SELECT S.first_name
FROM Students S
JOIN Addresses A ON S.permanent_address_id = A.address_id
WHERE A.country = 'Haiti' OR S.cell_mobile_number = '09700166582'
```

**First disagreeing instance** `student_transcripts_tracking.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    Jarvis

Returned query gives 4 row(s), 1 column(s):

    Hobart
    Warren
    Jarvis
    Delaney

Difference: gold_subset_of_rep; 1 row(s) in common, 0 only in the gold, 3 only in the returned result.

### R416  (question 311, database `tvshow`)

- Returned by: omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 20/50
- Instances disagreeing: 25 of 25 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find the series name and country of the tv channel that is playing some cartoons  Ben Jones and Michael Chang directs?

**Gold.**
```sql
SELECT T1.series_name ,  T1.country FROM TV_Channel AS T1 JOIN cartoon AS T2 ON T1.id = T2.Channel WHERE T2.directed_by  =  'Michael Chang' INTERSECT SELECT T1.series_name ,  T1.country FROM TV_Channel AS T1 JOIN cartoon AS T2 ON T1.id = T2.Channel WHERE T2.directed_by  =  'Ben Jones'
```

**Returned.**
```sql
SELECT 
    TV_Channel.series_name, 
    TV_Channel.Country
FROM 
    Cartoon
INNER JOIN 
    TV_Channel 
ON 
    Cartoon.Channel = TV_Channel.id
WHERE 
    Cartoon.Directed_by = 'Ben Jones' 
    OR Cartoon.Directed_by = 'Michael Chang'
```

**First disagreeing instance** `tvshow.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    MTV Dance | United Kingdom

Returned query gives 8 row(s), 2 column(s):

    Sky Radio | Italy
    Music Box Italia | Italy
    MTV Hits | Italy
    MTV Rocks | United Kingdom
    MTV Dance | United Kingdom
    MTV Dance | United Kingdom
    Classica | Italy
    MTV Dance | United Kingdom

Difference: gold_subset_of_rep; 1 row(s) in common, 0 only in the gold, 5 only in the returned result.

### R417  (question 312, database `tvshow`)

- Returned by: omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 22/50
- Instances disagreeing: 25 of 25 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the series name and country of all TV channels that are playing cartoons  Ben Jones and Michael Chang directs?

**Gold.**
```sql
SELECT T1.series_name ,  T1.country FROM TV_Channel AS T1 JOIN cartoon AS T2 ON T1.id = T2.Channel WHERE T2.directed_by  =  'Michael Chang' INTERSECT SELECT T1.series_name ,  T1.country FROM TV_Channel AS T1 JOIN cartoon AS T2 ON T1.id = T2.Channel WHERE T2.directed_by  =  'Ben Jones'
```

**Returned.**
```sql
SELECT 
    TV_Channel.series_name, 
    TV_Channel.Country
FROM 
    Cartoon
INNER JOIN 
    TV_Channel 
ON 
    Cartoon.Channel = TV_Channel.id
WHERE 
    Cartoon.Directed_by = 'Ben Jones' 
    OR Cartoon.Directed_by = 'Michael Chang'
```

**First disagreeing instance** `tvshow.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    MTV Dance | United Kingdom

Returned query gives 8 row(s), 2 column(s):

    Sky Radio | Italy
    Music Box Italia | Italy
    MTV Hits | Italy
    MTV Rocks | United Kingdom
    MTV Dance | United Kingdom
    MTV Dance | United Kingdom
    Classica | Italy
    MTV Dance | United Kingdom

Difference: gold_subset_of_rep; 1 row(s) in common, 0 only in the gold, 5 only in the returned result.

### R418  (question 362, database `world_1`)

- Returned by: omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 30/50
- Instances disagreeing: 5 of 46 (11%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the average GNP and total population in all US territory nations?

**Gold.**
```sql
SELECT avg(GNP) ,  sum(population) FROM country WHERE GovernmentForm  =  "US Territory"
```

**Returned.**
```sql
SELECT AVG(GNP) AS AverageGNP, SUM(Population) AS TotalPopulation
FROM country
WHERE Region = 'US territory'
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    510.3333333333333 | 329000

Returned query gives 1 row(s), 2 column(s):

    NULL | NULL

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R419  (question 370, database `world_1`)

- Returned by: omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 39/50
- Instances disagreeing: 39 of 46 (85%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What is name of the nation that speaks the largest number of languages?

**Gold.**
```sql
SELECT T1.Name FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code  =  T2.CountryCode GROUP BY T1.Name ORDER BY COUNT(*) DESC LIMIT 1
```

**Returned.**
```sql
SELECT c.Name
FROM country AS c
INNER JOIN countrylanguage AS cl ON c.Code = cl.CountryCode
GROUP BY c.Code
ORDER BY COUNT(cl.Language) DESC
LIMIT 1
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    United States

Returned query gives 1 row(s), 1 column(s):

    Canada

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R420  (question 388, database `world_1`)

- Returned by: omnisql-32b/seed303
- Returned in cell: D only
- Class mass: 26/50
- Instances disagreeing: 37 of 46 (80%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What is the most populace city that speaks English?

**Gold.**
```sql
SELECT T1.Name ,  T1.Population FROM city AS T1 JOIN countrylanguage AS T2 ON T1.CountryCode  =  T2.CountryCode WHERE T2.Language  =  "English" ORDER BY T1.Population DESC LIMIT 1
```

**Returned.**
```sql
SELECT city.Name
FROM city
INNER JOIN countrylanguage ON city.CountryCode = countrylanguage.CountryCode
WHERE countrylanguage.Language = 'English' AND countrylanguage.IsOfficial = 'T'
ORDER BY city.Population DESC
LIMIT 1
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    New York | 8008278

Returned query gives 1 row(s), 1 column(s):

    New York

Difference: col_count_differs, disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R421  (question 398, database `world_1`)

- Returned by: omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 47/50
- Instances disagreeing: 37 of 46 (80%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the countries that have greater surface area than any country in Europe?

**Gold.**
```sql
SELECT Name FROM country WHERE SurfaceArea  >  (SELECT min(SurfaceArea) FROM country WHERE Continent  =  "Europe")
```

**Returned.**
```sql
SELECT Name
FROM country
WHERE SurfaceArea > (
    SELECT MAX(SurfaceArea)
    FROM country
    WHERE Continent = 'Europe'
)
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 238 row(s), 1 column(s):

    Aruba
    Afghanistan
    Angola
    Anguilla
    Albania
    Andorra
    Netherlands Antilles
    United Arab Emirates
    Argentina
    Armenia
    American Samoa
    Antarctica
    ... (238 rows total)

Returned query gives 0 row(s), None column(s):

    (no rows)

Difference: rep_empty; 0 row(s) in common, 238 only in the gold, 0 only in the returned result.

### R422  (question 403, database `world_1`)

- Returned by: omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 50/50
- Instances disagreeing: 29 of 46 (63%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the Asian countries have more people than that of any country in Africa?

**Gold.**
```sql
SELECT Name FROM country WHERE Continent  =  "Asia"  AND population  >  (SELECT min(population) FROM country WHERE Continent  =  "Africa")
```

**Returned.**
```sql
SELECT Name
FROM country
WHERE Continent = 'Asia' AND Population > (
    SELECT MAX(Population)
    FROM country
    WHERE Continent = 'Africa'
)
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 51 row(s), 1 column(s):

    Afghanistan
    United Arab Emirates
    Armenia
    Azerbaijan
    Bangladesh
    Bahrain
    Brunei
    Bhutan
    China
    Cyprus
    Georgia
    Hong Kong
    ... (51 rows total)

Returned query gives 6 row(s), 1 column(s):

    Bangladesh
    China
    Indonesia
    India
    Japan
    Pakistan

Difference: rep_subset_of_gold; 6 row(s) in common, 45 only in the gold, 0 only in the returned result.

### R423  (question 407, database `world_1`)

- Returned by: omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 17/50
- Instances disagreeing: 41 of 46 (89%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Give the country codes for countries in which people does not speak English.

**Gold.**
```sql
SELECT DISTINCT CountryCode FROM countrylanguage WHERE LANGUAGE != "English"
```

**Returned.**
```sql
SELECT DISTINCT CountryCode
FROM countrylanguage
WHERE CountryCode NOT IN (
    SELECT CountryCode
    FROM countrylanguage
    WHERE Language = 'English'
)
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 223 row(s), 1 column(s):

    ABW
    AFG
    AGO
    ALB
    AND
    ANT
    ARE
    ARG
    ARM
    ASM
    ATG
    AUS
    ... (223 rows total)

Returned query gives 173 row(s), 1 column(s):

    AFG
    AGO
    ALB
    AND
    ARE
    ARG
    ARM
    AUT
    AZE
    BDI
    BEL
    BEN
    ... (173 rows total)

Difference: rep_subset_of_gold; 173 row(s) in common, 50 only in the gold, 0 only in the returned result.

### R424  (question 410, database `world_1`)

- Returned by: omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 23/50
- Instances disagreeing: 9 of 46 (20%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Which cities are in European countries where English is not spoken officially?

**Gold.**
```sql
SELECT DISTINCT T2.Name FROM country AS T1 JOIN city AS T2 ON T2.CountryCode  =  T1.Code WHERE T1.Continent  =  'Europe' AND T1.Name NOT IN (SELECT T3.Name FROM country AS T3 JOIN countrylanguage AS T4 ON T3.Code  =  T4.CountryCode WHERE T4.IsOfficial  =  'T' AND T4.Language  =  'English')
```

**Returned.**
```sql
SELECT city.Name
FROM city
INNER JOIN country ON city.CountryCode = country.Code
WHERE country.Continent = 'Europe'
  AND city.CountryCode NOT IN (
      SELECT countrylanguage.CountryCode
      FROM countrylanguage
      WHERE countrylanguage.Language = 'English' AND countrylanguage.IsOfficial = 'T'
  )
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 753 row(s), 1 column(s):

    Amsterdam
    Rotterdam
    Haag
    Utrecht
    Eindhoven
    Tilburg
    Groningen
    Breda
    Apeldoorn
    Nijmegen
    Enschede
    Haarlem
    ... (753 rows total)

Returned query gives 755 row(s), 1 column(s):

    Tirana
    Andorra la Vella
    Wien
    Graz
    Linz
    Salzburg
    Innsbruck
    Klagenfurt
    Antwerpen
    Gent
    Charleroi
    Liège
    ... (755 rows total)

Difference: duplicate_multiplicity_only; 753 row(s) in common, 0 only in the gold, 0 only in the returned result.

### R425  (question 413, database `world_1`)

- Returned by: omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 47/50
- Instances disagreeing: 44 of 46 (96%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What are the name, independence year, and surface area of the country with the least number of nationalities?

**Gold.**
```sql
SELECT Name ,  SurfaceArea ,  IndepYear FROM country ORDER BY Population LIMIT 1
```

**Returned.**
```sql
SELECT 
    c.Name, 
    c.IndepYear, 
    c.SurfaceArea
FROM 
    country AS c
INNER JOIN 
    countrylanguage AS cl
ON 
    c.Code = cl.CountryCode
GROUP BY 
    cl.CountryCode
ORDER BY 
    COUNT(cl.Language) ASC
LIMIT 1
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 3 column(s):

    Antarctica | 13120000.0 | NULL

Returned query gives 1 row(s), 3 column(s):

    Anguilla | NULL | 96.0

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R426  (question 432, database `world_1`)

- Returned by: omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 37/50
- Instances disagreeing: 46 of 46 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the codes of the different nations, and what are the languages spoken by the greatest percentage of people for each?

**Gold.**
```sql
SELECT LANGUAGE ,  CountryCode ,  max(Percentage) FROM countrylanguage GROUP BY CountryCode
```

**Returned.**
```sql
SELECT 
    cl.CountryCode, 
    cl.Language
FROM 
    countrylanguage cl
WHERE 
    cl.Percentage = (
        SELECT MAX(cl2.Percentage)
        FROM countrylanguage cl2
        WHERE cl2.CountryCode = cl.CountryCode
    )
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 233 row(s), 3 column(s):

    Papiamento | ABW | 76.7
    Pashto | AFG | 52.4
    Ovimbundu | AGO | 37.2
    English | AIA | 0.0
    Albaniana | ALB | 97.9
    Spanish | AND | 44.6
    Papiamento | ANT | 86.2
    Arabic | ARE | 42.0
    Spanish | ARG | 96.8
    Armenian | ARM | 93.4
    Samoan | ASM | 90.6
    Creole English | ATG | 95.7
    ... (233 rows total)

Returned query gives 241 row(s), 2 column(s):

    ABW | Papiamento
    AFG | Pashto
    AGO | Ovimbundu
    AIA | English
    ALB | Albaniana
    AND | Spanish
    ANT | Papiamento
    ARE | Arabic
    ARG | Spanish
    ARM | Armenian
    ASM | Samoan
    ATG | Creole English
    ... (241 rows total)

Difference: col_count_differs, disjoint; 0 row(s) in common, 233 only in the gold, 241 only in the returned result.

### R427  (question 433, database `world_1`)

- Returned by: omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 18/50
- Instances disagreeing: 46 of 46 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the total number of countries where Spanish is spoken by the largest percentage of people?

**Gold.**
```sql
SELECT count(*) ,   max(Percentage) FROM countrylanguage WHERE LANGUAGE  =  "Spanish" GROUP BY CountryCode
```

**Returned.**
```sql
SELECT COUNT(DISTINCT cl.CountryCode) AS TotalCountries
FROM countrylanguage AS cl
WHERE cl.Language = 'Spanish'
  AND cl.Percentage = (
    SELECT MAX(cl2.Percentage)
    FROM countrylanguage AS cl2
    WHERE cl2.CountryCode = cl.CountryCode
      AND cl2.Language = 'Spanish'
  )
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 28 row(s), 2 column(s):

    1 | 7.4
    1 | 44.6
    1 | 96.8
    1 | 31.6
    1 | 87.7
    1 | 0.7
    1 | 89.7
    1 | 99.0
    1 | 97.5
    1 | 100.0
    1 | 98.0
    1 | 93.0
    ... (28 rows total)

Returned query gives 1 row(s), 1 column(s):

    28

Difference: col_count_differs, disjoint; 0 row(s) in common, 27 only in the gold, 1 only in the returned result.

### R428  (question 434, database `world_1`)

- Returned by: omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 26/50
- Instances disagreeing: 46 of 46 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Count the number of countries for which Spanish is predominantly spoken .

**Gold.**
```sql
SELECT count(*) ,   max(Percentage) FROM countrylanguage WHERE LANGUAGE  =  "Spanish" GROUP BY CountryCode
```

**Returned.**
```sql
SELECT COUNT(DISTINCT T1.CountryCode) AS SpanishDominantCountries
FROM countrylanguage AS T1
WHERE T1.Language = 'Spanish'
  AND T1.Percentage = (
    SELECT MAX(T2.Percentage)
    FROM countrylanguage AS T2
    WHERE T2.CountryCode = T1.CountryCode
  )
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 28 row(s), 2 column(s):

    1 | 7.4
    1 | 44.6
    1 | 96.8
    1 | 31.6
    1 | 87.7
    1 | 0.7
    1 | 89.7
    1 | 99.0
    1 | 97.5
    1 | 100.0
    1 | 98.0
    1 | 93.0
    ... (28 rows total)

Returned query gives 1 row(s), 1 column(s):

    21

Difference: col_count_differs, disjoint; 0 row(s) in common, 27 only in the gold, 1 only in the returned result.

### R429  (question 460, database `network_1`)

- Returned by: omnisql-32b/seed303
- Returned in cell: D only
- Class mass: 25/50
- Instances disagreeing: 24 of 29 (83%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Return the number of likes Kyle has.

**Gold.**
```sql
SELECT count(*) FROM Likes AS T1 JOIN Highschooler AS T2 ON T1.student_id  =  T2.id WHERE T2.name  =  "Kyle"
```

**Returned.**
```sql
SELECT COUNT(*) AS like_count
FROM Likes
WHERE liked_id = (SELECT ID FROM Highschooler WHERE name = 'Kyle')
```

**First disagreeing instance** `network_1v5080.sqlite`.

Gold returns 1 row(s), 1 column(s):

    21

Returned query gives 1 row(s), 1 column(s):

    4

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R430  (question 461, database `network_1`)

- Returned by: omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 33/50
- Instances disagreeing: 27 of 29 (93%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find the average grade of all students who have some friends.

**Gold.**
```sql
SELECT avg(grade) FROM Highschooler WHERE id IN (SELECT T1.student_id FROM Friend AS T1 JOIN Highschooler AS T2 ON T1.student_id  =  T2.id)
```

**Returned.**
```sql
SELECT AVG(H.grade) AS average_grade
FROM Highschooler AS H
INNER JOIN Friend AS F
ON H.ID = F.student_id
```

**First disagreeing instance** `network_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    10.428571428571429

Returned query gives 1 row(s), 1 column(s):

    10.25

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R431  (question 462, database `network_1`)

- Returned by: omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 35/50
- Instances disagreeing: 27 of 29 (93%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the average grade of students who have friends?

**Gold.**
```sql
SELECT avg(grade) FROM Highschooler WHERE id IN (SELECT T1.student_id FROM Friend AS T1 JOIN Highschooler AS T2 ON T1.student_id  =  T2.id)
```

**Returned.**
```sql
SELECT AVG(H.grade) AS average_grade
FROM Highschooler AS H
INNER JOIN Friend AS F
ON H.ID = F.student_id
```

**First disagreeing instance** `network_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    10.428571428571429

Returned query gives 1 row(s), 1 column(s):

    10.25

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R432  (question 467, database `dog_kennels`)

- Returned by: omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 46/50
- Instances disagreeing: 48 of 48 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the names of the dogs for which the owner spent more than 1000 for treatment?

**Gold.**
```sql
select name from dogs where dog_id not in ( select dog_id from treatments group by dog_id having sum(cost_of_treatment)  >  1000 )
```

**Returned.**
```sql
SELECT 
    D.name
FROM 
    Dogs D
JOIN 
    Treatments T ON D.dog_id = T.dog_id
GROUP BY 
    D.dog_id, D.name
HAVING 
    SUM(T.cost_of_treatment) > 1000
```

**First disagreeing instance** `dog_kennels.sqlite` (this is the shipped benchmark database).

Gold returns 12 row(s), 1 column(s):

    Kacey
    Hipolito
    Mavis
    Houston
    Jeffrey
    Merritt
    Narciso
    George
    Bessie
    Betty
    Holden
    Jesus

Returned query gives 3 row(s), 1 column(s):

    Troy
    Lyric
    Evangeline

Difference: disjoint; 0 row(s) in common, 12 only in the gold, 3 only in the returned result.

### R433  (question 468, database `dog_kennels`)

- Returned by: omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 27/50
- Instances disagreeing: 48 of 48 (100%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Which person has the most dogs? List the id, first name and last name.

**Gold.**
```sql
SELECT T1.owner_id ,  T2.first_name ,  T2.last_name FROM Dogs AS T1 JOIN Owners AS T2 ON T1.owner_id  =  T2.owner_id GROUP BY T1.owner_id ORDER BY count(*) DESC LIMIT 1
```

**Returned.**
```sql
SELECT o.owner_id, o.first_name, o.last_name, COUNT(d.dog_id) AS dog_count
FROM Owners o
JOIN Dogs d ON o.owner_id = d.owner_id
GROUP BY o.owner_id, o.first_name, o.last_name
ORDER BY dog_count DESC
LIMIT 1
```

**First disagreeing instance** `dog_kennels.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 3 column(s):

    14 | Rachelle | Funk

Returned query gives 1 row(s), 4 column(s):

    14 | Rachelle | Funk | 3

Difference: col_count_differs, disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R434  (question 474, database `dog_kennels`)

- Returned by: omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 24/50
- Instances disagreeing: 48 of 48 (100%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Who has paid the largest amount of money in total for their dogs? Show the id and zip code.

**Gold.**
```sql
SELECT T1.owner_id ,  T1.zip_code FROM Owners AS T1 JOIN Dogs AS T2 ON T1.owner_id  =  T2.owner_id JOIN Treatments AS T3 ON T2.dog_id  =  T3.dog_id GROUP BY T1.owner_id ORDER BY sum(T3.cost_of_treatment) DESC LIMIT 1
```

**Returned.**
```sql
SELECT o.owner_id, o.zip_code, SUM(t.cost_of_treatment) AS total_amount_paid
FROM Owners o
JOIN Dogs d ON o.owner_id = d.owner_id
JOIN Treatments t ON d.dog_id = t.dog_id
GROUP BY o.owner_id, o.zip_code
ORDER BY total_amount_paid DESC
LIMIT 1
```

**First disagreeing instance** `dog_kennels.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    3 | 02647

Returned query gives 1 row(s), 3 column(s):

    3 | 02647 | 1601

Difference: col_count_differs, disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R435  (question 476, database `dog_kennels`)

- Returned by: omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 30/50
- Instances disagreeing: 46 of 48 (96%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the first name and last name of the professionals who have done treatment cheaper than average?

**Gold.**
```sql
SELECT DISTINCT T1.first_name ,  T1.last_name FROM Professionals AS T1 JOIN Treatments AS T2 WHERE cost_of_treatment  <  ( SELECT avg(cost_of_treatment) FROM Treatments )
```

**Returned.**
```sql
SELECT p.first_name, p.last_name
FROM Professionals p
JOIN Treatments t ON p.professional_id = t.professional_id
WHERE t.cost_of_treatment < (SELECT AVG(cost_of_treatment) FROM Treatments)
```

**First disagreeing instance** `dog_kennels.sqlite` (this is the shipped benchmark database).

Gold returns 15 row(s), 2 column(s):

    Taryn | Braun
    Jayson | Ullrich
    Olaf | Watsica
    Vernice | Tillman
    Danny | Considine
    Ruben | O'Reilly
    Velva | Hayes
    Karley | Hyatt
    Monte | Kshlerin
    Domenica | Jacobs
    Brady | Pouros
    Winfield | Christiansen
    ... (15 rows total)

Returned query gives 8 row(s), 2 column(s):

    Domenica | Jacobs
    Vernice | Tillman
    Karley | Hyatt
    Vernice | Tillman
    Ruben | O'Reilly
    Domenica | Jacobs
    Monte | Kshlerin
    Monte | Kshlerin

Difference: rep_subset_of_gold; 5 row(s) in common, 10 only in the gold, 0 only in the returned result.

### R436  (question 480, database `dog_kennels`)

- Returned by: omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 27/50
- Instances disagreeing: 42 of 48 (88%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** List the last name of the owner owning the youngest dog.

**Gold.**
```sql
SELECT T1.last_name FROM Owners AS T1 JOIN Dogs AS T2 ON T1.owner_id  =  T2.owner_id WHERE T2.age  =  ( SELECT max(age) FROM Dogs )
```

**Returned.**
```sql
SELECT o.last_name
FROM Owners o
JOIN Dogs d ON o.owner_id = d.owner_id
WHERE d.date_of_birth = (SELECT MAX(date_of_birth) FROM Dogs)
```

**First disagreeing instance** `dog_kennels.sqlite` (this is the shipped benchmark database).

Gold returns 3 row(s), 1 column(s):

    Feil
    Fisher
    Rippin

Returned query gives 1 row(s), 1 column(s):

    Mertz

Difference: disjoint; 0 row(s) in common, 3 only in the gold, 1 only in the returned result.

### R437  (question 481, database `dog_kennels`)

- Returned by: omnisql-32b/seed303
- Returned in cell: both A and D
- Class mass: 23/50
- Instances disagreeing: 41 of 48 (85%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Who owns the youngest dog? Give me his or her last name.

**Gold.**
```sql
SELECT T1.last_name FROM Owners AS T1 JOIN Dogs AS T2 ON T1.owner_id  =  T2.owner_id WHERE T2.age  =  ( SELECT max(age) FROM Dogs )
```

**Returned.**
```sql
SELECT O.last_name
FROM Owners O
JOIN Dogs D ON O.owner_id = D.owner_id
ORDER BY D.date_of_birth DESC
LIMIT 1
```

**First disagreeing instance** `dog_kennels.sqlite` (this is the shipped benchmark database).

Gold returns 3 row(s), 1 column(s):

    Feil
    Fisher
    Rippin

Returned query gives 1 row(s), 1 column(s):

    Mertz

Difference: disjoint; 0 row(s) in common, 3 only in the gold, 1 only in the returned result.

### R438  (question 49, database `pets_1`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed202, xiyansql-32b/seed303
- Returned in cell: both A and D
- Class mass: 50/50, 50/50, 50/50
- Instances disagreeing: 23 of 27 (85%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find the first name and age of students who have a dog but do not have a cat.

**Gold.**
```sql
SELECT T1.fname ,  T1.age FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid  =  T2.stuid JOIN pets AS T3 ON T3.petid  =  T2.petid WHERE T3.pettype  =  'dog' AND T1.stuid NOT IN (SELECT T1.stuid FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid  =  T2.stuid JOIN pets AS T3 ON T3.petid  =  T2.petid WHERE T3.pettype  =  'cat')
```

**Returned.**
```sql
SELECT T1.fname , T1.age FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid = T2.stuid JOIN pets AS T3 ON T2.petid = T3.petid WHERE T3.pettype = 'dog' EXCEPT SELECT T1.fname , T1.age FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid = T2.stuid JOIN pets AS T3 ON T2.petid = T3.petid WHERE T3.pettype = 'cat'
```

**First disagreeing instance** `pets_1.sqlite` (this is the shipped benchmark database).

Gold returns 2 row(s), 2 column(s):

    Tracy | 19
    Tracy | 19

Returned query gives 1 row(s), 2 column(s):

    Tracy | 19

Difference: duplicate_multiplicity_only; 1 row(s) in common, 0 only in the gold, 0 only in the returned result.

### R439  (question 50, database `pets_1`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed202, xiyansql-32b/seed303
- Returned in cell: both A and D
- Class mass: 50/50, 50/50, 50/50
- Instances disagreeing: 25 of 27 (93%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the first name of every student who has a dog but does not have a cat?

**Gold.**
```sql
SELECT T1.fname ,  T1.age FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid  =  T2.stuid JOIN pets AS T3 ON T3.petid  =  T2.petid WHERE T3.pettype  =  'dog' AND T1.stuid NOT IN (SELECT T1.stuid FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid  =  T2.stuid JOIN pets AS T3 ON T3.petid  =  T2.petid WHERE T3.pettype  =  'cat')
```

**Returned.**
```sql
SELECT DISTINCT T1.Fname FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid = T2.stuid JOIN pets AS T3 ON T3.petid = T2.petid WHERE T3.pettype = 'dog' EXCEPT SELECT DISTINCT T1.Fname FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid = T2.stuid JOIN pets AS T3 ON T3.petid = T2.petid WHERE T3.pettype = 'cat'
```

**First disagreeing instance** `pets_1.sqlite` (this is the shipped benchmark database).

Gold returns 2 row(s), 2 column(s):

    Tracy | 19
    Tracy | 19

Returned query gives 1 row(s), 1 column(s):

    Tracy

Difference: col_count_differs, disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R440  (question 63, database `car_1`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed303
- Returned in cell: both A and D
- Class mass: 15/50, 22/50
- Instances disagreeing: 41 of 60 (68%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find the name of the makers that produced some cars in 1970?

**Gold.**
```sql
SELECT DISTINCT T1.Maker FROM CAR_MAKERS AS T1 JOIN MODEL_LIST AS T2 ON T1.Id  =  T2.Maker JOIN CAR_NAMES AS T3 ON T2.model  =  T3.model JOIN CARS_DATA AS T4 ON T3.MakeId  =  T4.id WHERE T4.year  =  '1970';
```

**Returned.**
```sql
SELECT T1.FullName FROM CAR_MAKERS AS T1 JOIN MODEL_LIST AS T2 ON T1.Id = T2.Maker JOIN CAR_NAMES AS T3 ON T2.Model = T3.Model JOIN CARS_DATA AS T4 ON T3.MakeId = T4.Id WHERE T4.Year = 1970
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 11 row(s), 1 column(s):

    gm
    chrysler
    amc
    ford
    citroen
    toyota
    nissan
    volkswagen
    peugeaut
    saab
    bmw

Returned query gives 34 row(s), 1 column(s):

    General Motors
    General Motors
    Chrysler
    American Motor Company
    Ford Motor Company
    Ford Motor Company
    General Motors
    Chrysler
    General Motors
    American Motor Company
    Citroen
    General Motors
    ... (34 rows total)

Difference: disjoint; 0 row(s) in common, 11 only in the gold, 11 only in the returned result.

### R441  (question 64, database `car_1`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed202, xiyansql-32b/seed303
- Returned in cell: both A and D
- Class mass: 38/50, 39/50, 43/50
- Instances disagreeing: 41 of 60 (68%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the name of the different car makers who produced a car in 1970?

**Gold.**
```sql
SELECT DISTINCT T1.Maker FROM CAR_MAKERS AS T1 JOIN MODEL_LIST AS T2 ON T1.Id  =  T2.Maker JOIN CAR_NAMES AS T3 ON T2.model  =  T3.model JOIN CARS_DATA AS T4 ON T3.MakeId  =  T4.id WHERE T4.year  =  '1970';
```

**Returned.**
```sql
SELECT DISTINCT T1.FullName FROM CAR_MAKERS AS T1 JOIN MODEL_LIST AS T2 ON T1.Id = T2.Maker JOIN CAR_NAMES AS T3 ON T2.Model = T3.Model JOIN CARS_DATA AS T4 ON T3.MakeId = T4.Id WHERE T4.Year = 1970
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 11 row(s), 1 column(s):

    gm
    chrysler
    amc
    ford
    citroen
    toyota
    nissan
    volkswagen
    peugeaut
    saab
    bmw

Returned query gives 11 row(s), 1 column(s):

    General Motors
    Chrysler
    American Motor Company
    Ford Motor Company
    Citroen
    Toyota
    Nissan Motors
    Volkswagen
    Peugeaut
    Saab
    BMW

Difference: disjoint; 0 row(s) in common, 11 only in the gold, 11 only in the returned result.

### R442  (question 65, database `car_1`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed202, xiyansql-32b/seed303
- Returned in cell: both A and D
- Class mass: 50/50, 50/50, 50/50
- Instances disagreeing: 4 of 60 (7%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find the make and production time of the cars that were produced in the earliest ?

**Gold.**
```sql
SELECT T2.Make ,  T1.Year FROM CARS_DATA AS T1 JOIN CAR_NAMES AS T2 ON T1.Id  =  T2.MakeId WHERE T1.Year  =  (SELECT min(YEAR) FROM CARS_DATA);
```

**Returned.**
```sql
SELECT T1.Make , T2.Year FROM CAR_NAMES AS T1 JOIN CARS_DATA AS T2 ON T1.MakeId = T2.Id ORDER BY T2.Year ASC LIMIT 1
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 35 row(s), 2 column(s):

    chevrolet chevelle malibu | 1970
    buick skylark 320 | 1970
    plymouth satellite | 1970
    amc rebel sst | 1970
    ford torino | 1970
    ford galaxie 500 | 1970
    chevrolet impala | 1970
    plymouth fury iii | 1970
    pontiac catalina | 1970
    amc ambassador dpl | 1970
    citroen ds-21 pallas | 1970
    chevrolet chevelle concours (sw) | 1970
    ... (35 rows total)

Returned query gives 1 row(s), 2 column(s):

    chevrolet chevelle malibu | 1970

Difference: rep_subset_of_gold; 1 row(s) in common, 34 only in the gold, 0 only in the returned result.

### R443  (question 66, database `car_1`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed303
- Returned in cell: both A and D
- Class mass: 30/50, 29/50
- Instances disagreeing: 60 of 60 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the maker of the carr produced in the earliest  and what  year was it?

**Gold.**
```sql
SELECT T2.Make ,  T1.Year FROM CARS_DATA AS T1 JOIN CAR_NAMES AS T2 ON T1.Id  =  T2.MakeId WHERE T1.Year  =  (SELECT min(YEAR) FROM CARS_DATA);
```

**Returned.**
```sql
SELECT T1.Maker, T2.Year FROM CAR_MAKERS AS T1 JOIN MODEL_LIST AS T3 JOIN CAR_NAMES AS T4 JOIN CARS_DATA AS T2 ON T1.Id = T3.Maker AND T3.Model = T4.Model AND T4.MakeId = T2.Id ORDER BY T2.Year ASC LIMIT 1
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 35 row(s), 2 column(s):

    chevrolet chevelle malibu | 1970
    buick skylark 320 | 1970
    plymouth satellite | 1970
    amc rebel sst | 1970
    ford torino | 1970
    ford galaxie 500 | 1970
    chevrolet impala | 1970
    plymouth fury iii | 1970
    pontiac catalina | 1970
    amc ambassador dpl | 1970
    citroen ds-21 pallas | 1970
    chevrolet chevelle concours (sw) | 1970
    ... (35 rows total)

Returned query gives 1 row(s), 2 column(s):

    gm | 1970

Difference: disjoint; 0 row(s) in common, 35 only in the gold, 1 only in the returned result.

### R444  (question 81, database `car_1`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed202, xiyansql-32b/seed303
- Returned in cell: both A and D
- Class mass: 31/50, 33/50, 30/50
- Instances disagreeing: 60 of 60 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the names and ids of all nations with at least one car maker?

**Gold.**
```sql
SELECT T1.CountryName ,  T1.CountryId FROM COUNTRIES AS T1 JOIN CAR_MAKERS AS T2 ON T1.CountryId  =  T2.Country GROUP BY T1.CountryId HAVING count(*)  >=  1;
```

**Returned.**
```sql
SELECT T2.CountryName , T1.Country FROM CAR_MAKERS AS T1 JOIN COUNTRIES AS T2 ON T1.Country = T2.CountryId GROUP BY T1.Country
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 8 row(s), 2 column(s):

    usa | 1
    germany | 2
    france | 3
    japan | 4
    italy | 5
    sweden | 6
    uk | 7
    korea | 8

Returned query gives 8 row(s), 2 column(s):

    usa | 1
    germany | 2
    france | 3
    japan | 4
    italy | 5
    sweden | 6
    uk | 7
    korea | 8

Difference: disjoint; 0 row(s) in common, 8 only in the gold, 8 only in the returned result.

### R445  (question 85, database `car_1`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed202, xiyansql-32b/seed303
- Returned in cell: both A and D
- Class mass: 40/50, 43/50, 48/50
- Instances disagreeing: 58 of 60 (97%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the names of all European countries with at least 3 manufacturers?

**Gold.**
```sql
SELECT T1.CountryName FROM COUNTRIES AS T1 JOIN CONTINENTS AS T2 ON T1.Continent  =  T2.ContId JOIN CAR_MAKERS AS T3 ON T1.CountryId  =  T3.Country WHERE T2.Continent  =  'europe' GROUP BY T1.CountryName HAVING count(*)  >=  3;
```

**Returned.**
```sql
SELECT T1.CountryName FROM COUNTRIES AS T1 JOIN CAR_MAKERS AS T2 ON T1.CountryId = T2.Country GROUP BY T1.CountryName HAVING count(*) >= 3
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 2 row(s), 1 column(s):

    france
    germany

Returned query gives 4 row(s), 1 column(s):

    france
    germany
    japan
    usa

Difference: gold_subset_of_rep; 2 row(s) in common, 0 only in the gold, 2 only in the returned result.

### R446  (question 92, database `car_1`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed202, xiyansql-32b/seed303
- Returned in cell: both A and D
- Class mass: 33/50, 40/50, 39/50
- Instances disagreeing: 60 of 60 (100%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What car has the most different versions?

**Gold.**
```sql
SELECT Model FROM CAR_NAMES GROUP BY Model ORDER BY count(*) DESC LIMIT 1;
```

**Returned.**
```sql
SELECT T1.Make FROM CAR_NAMES AS T1 JOIN MODEL_LIST AS T2 ON T1.Model = T2.Model GROUP BY T1.Make ORDER BY COUNT(*) DESC LIMIT 1
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    ford

Returned query gives 1 row(s), 1 column(s):

    ford pinto

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R447  (question 105, database `car_1`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed202, xiyansql-32b/seed303
- Returned in cell: both A and D
- Class mass: 33/50, 37/50, 32/50
- Instances disagreeing: 60 of 60 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** How many nations has more than 2 car makers ?

**Gold.**
```sql
select count(*) from countries as t1 join car_makers as t2 on t1.countryid  =  t2.country group by t1.countryid having count(*)  >  2
```

**Returned.**
```sql
SELECT count(*) FROM (SELECT T.Country FROM car_makers AS T GROUP BY T.Country HAVING count(*) > 2)
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 4 row(s), 1 column(s):

    4
    4
    3
    5

Returned query gives 1 row(s), 1 column(s):

    4

Difference: rep_subset_of_gold; 1 row(s) in common, 2 only in the gold, 0 only in the returned result.

### R448  (question 191, database `course_teach`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed202, xiyansql-32b/seed303
- Returned in cell: both A and D
- Class mass: 50/50, 50/50, 50/50
- Instances disagreeing: 16 of 25 (64%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** List the name of teachers who are not from Little Lever Urban District.

**Gold.**
```sql
select name from teacher where hometown != "little lever urban district"
```

**Returned.**
```sql
SELECT Name FROM teacher WHERE Hometown != "Little Lever Urban District"
```

**First disagreeing instance** `course_teach.sqlite` (this is the shipped benchmark database).

Gold returns 7 row(s), 1 column(s):

    Joseph Huts
    Gustaaf Deloor
    Vicente Carretero
    John Deloor
    Kearsley Brown
    Anne Walker
    Lucy Wong

Returned query gives 6 row(s), 1 column(s):

    Joseph Huts
    Gustaaf Deloor
    Vicente Carretero
    John Deloor
    Kearsley Brown
    Lucy Wong

Difference: rep_subset_of_gold; 6 row(s) in common, 1 only in the gold, 0 only in the returned result.

### R449  (question 192, database `course_teach`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed202, xiyansql-32b/seed303
- Returned in cell: both A and D
- Class mass: 50/50, 50/50, 50/50
- Instances disagreeing: 16 of 25 (64%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the names of the teachers who do not come from Little Lever Urban District?

**Gold.**
```sql
select name from teacher where hometown != "little lever urban district"
```

**Returned.**
```sql
SELECT Name FROM teacher WHERE Hometown != "Little Lever Urban District"
```

**First disagreeing instance** `course_teach.sqlite` (this is the shipped benchmark database).

Gold returns 7 row(s), 1 column(s):

    Joseph Huts
    Gustaaf Deloor
    Vicente Carretero
    John Deloor
    Kearsley Brown
    Anne Walker
    Lucy Wong

Returned query gives 6 row(s), 1 column(s):

    Joseph Huts
    Gustaaf Deloor
    Vicente Carretero
    John Deloor
    Kearsley Brown
    Lucy Wong

Difference: rep_subset_of_gold; 6 row(s) in common, 1 only in the gold, 0 only in the returned result.

### R450  (question 213, database `museum_visit`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed202, xiyansql-32b/seed303
- Returned in cell: both A and D
- Class mass: 50/50, 50/50, 50/50
- Instances disagreeing: 35 of 35 (100%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What are the id, name and membership level of people who have paid the largest amount of money overall in all museum tickets?

**Gold.**
```sql
SELECT t2.visitor_id ,  t1.name ,  t1.Level_of_membership FROM visitor AS t1 JOIN visit AS t2 ON t1.id  =  t2.visitor_id GROUP BY t2.visitor_id ORDER BY sum(t2.Total_spent) DESC LIMIT 1
```

**Returned.**
```sql
SELECT t1.id , t1.name , t1.level_of_membership FROM visitor AS t1 JOIN visit AS t2 ON t1.id = t2.visitor_id GROUP BY t1.id ORDER BY sum(t2.total_spent) DESC LIMIT 1
```

**First disagreeing instance** `museum_visit.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 3 column(s):

    3 | Arjen Robben | 1

Returned query gives 1 row(s), 3 column(s):

    3 | Arjen Robben | 1

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R451  (question 232, database `wta_1`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed303
- Returned in cell: both A and D
- Class mass: 26/50, 26/50
- Instances disagreeing: 8 of 33 (24%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** List the first and last name of all players who are left handed  in the order of age.

**Gold.**
```sql
SELECT first_name ,  last_name FROM players WHERE hand  =  'L' ORDER BY birth_date
```

**Returned.**
```sql
SELECT first_name , last_name FROM players WHERE hand = 'L' ORDER BY birth_date DESC
```

**First disagreeing instance** `wta_1.sqlite` (this is the shipped benchmark database).

Gold returns 487 row(s), 2 column(s):

    Ann | Jones
    Wendy | Gilchrist
    Martina | Navratilova
    Mary | Carillo
    Katerina | Bohmova
    Petra | Delhees Jauch
    Nancy | Loeffler Caro
    Lise | Gregory
    Rene | Collins
    Nicole | Arendt
    Florencia | Labat
    Sabine | Appelmans
    ... (487 rows total)

Returned query gives 487 row(s), 2 column(s):

    Noa | Krznaric
    Betina | Tokac
    Isabella | Nunez
    Matilde | Mariani
    Giulia | Morlet
    Najah | Dawson
    Lara | Biter
    Yasmina | Karimjanova
    Ruxandra | Schech
    Ya Hsin | Lee
    Lina | Shokry
    Xiyu | Wang
    ... (487 rows total)

Difference: row_order_only; 486 row(s) in common, 0 only in the gold, 0 only in the returned result.

### R452  (question 234, database `wta_1`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed202, xiyansql-32b/seed303
- Returned in cell: both A and D
- Class mass: 46/50, 45/50, 45/50
- Instances disagreeing: 33 of 33 (100%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Find the name and rank points of the person who won the most times.

**Gold.**
```sql
SELECT winner_name ,  winner_rank_points FROM matches GROUP BY winner_name ORDER BY count(*) DESC LIMIT 1
```

**Returned.**
```sql
SELECT T1.first_name , T1.last_name , T2.winner_rank_points FROM players AS T1 JOIN matches AS T2 ON T1.player_id = T2.winner_id GROUP BY T1.player_id ORDER BY count(*) DESC LIMIT 1
```

**First disagreeing instance** `wta_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    Angelique Kerber | 3715

Returned query gives 1 row(s), 3 column(s):

    Angelique | Kerber | 3715

Difference: col_count_differs, disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R453  (question 235, database `wta_1`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed202, xiyansql-32b/seed303
- Returned in cell: both A and D
- Class mass: 34/50, 35/50, 39/50
- Instances disagreeing: 33 of 33 (100%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What is the name of the player who has won the most matches, and how many rank points does this player have?

**Gold.**
```sql
SELECT winner_name ,  winner_rank_points FROM matches GROUP BY winner_name ORDER BY count(*) DESC LIMIT 1
```

**Returned.**
```sql
SELECT T1.first_name , T1.last_name , T2.ranking_points FROM players AS T1 JOIN rankings AS T2 ON T1.player_id = T2.player_id JOIN matches AS T3 ON T1.player_id = T3.winner_id GROUP BY T1.player_id ORDER BY count(*) DESC LIMIT 1
```

**First disagreeing instance** `wta_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    Angelique Kerber | 3715

Returned query gives 1 row(s), 3 column(s):

    Serena | Williams | 23

Difference: col_count_differs, disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R454  (question 252, database `battle_death`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed202, xiyansql-32b/seed303
- Returned in cell: both A and D
- Class mass: 50/50, 50/50, 50/50
- Instances disagreeing: 27 of 28 (96%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What is the ship id and name that caused most total injuries?

**Gold.**
```sql
SELECT T2.id ,  T2.name FROM death AS T1 JOIN ship AS t2 ON T1.caused_by_ship_id  =  T2.id GROUP BY T2.id ORDER BY count(*) DESC LIMIT 1
```

**Returned.**
```sql
SELECT T1.id , T1.name FROM ship AS T1 JOIN death AS T2 ON T1.id = T2.caused_by_ship_id GROUP BY T1.id ORDER BY sum(T2.injured) DESC LIMIT 1
```

**First disagreeing instance** `battle_death.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    5 | Three Brothers

Returned query gives 1 row(s), 2 column(s):

    4 | HMS Avon

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R455  (question 254, database `battle_death`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed202, xiyansql-32b/seed303
- Returned in cell: both A and D
- Class mass: 43/50, 42/50, 41/50
- Instances disagreeing: 28 of 28 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Show names, results and bulgarian commanders of the battles with no ships lost in the 'English Channel'.

**Gold.**
```sql
SELECT name ,  RESULT ,  bulgarian_commander FROM battle EXCEPT SELECT T1.name ,  T1.result ,  T1.bulgarian_commander FROM battle AS T1 JOIN ship AS T2 ON T1.id  =  T2.lost_in_battle WHERE T2.location  =  'English Channel'
```

**Returned.**
```sql
SELECT t1.name , t1.result , t1.bulgarian_commander FROM battle AS t1 JOIN ship AS t2 ON t1.id = t2.lost_in_battle WHERE t2.location != 'English Channel'
```

**First disagreeing instance** `battle_death.sqlite` (this is the shipped benchmark database).

Gold returns 3 row(s), 3 column(s):

    Battle of Adrianople | Bulgarian victory | Kaloyan
    Battle of Rusion | Bulgarian victory | Kaloyan
    Battle of Serres | Bulgarian victory | Kaloyan

Returned query gives 2 row(s), 3 column(s):

    Battle of Messinopolis | Bulgarian victory | Unknown
    Siege of Constantinople | Two Year Truce | Ivan Asen II

Difference: disjoint; 0 row(s) in common, 3 only in the gold, 2 only in the returned result.

### R456  (question 259, database `student_transcripts_tracking`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed202
- Returned in cell: both A and D
- Class mass: 50/50, 50/50
- Instances disagreeing: 22 of 55 (40%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find the last name of the students who currently live in North Carolina but have not registered in any degree program.

**Gold.**
```sql
SELECT T1.last_name FROM Students AS T1 JOIN Addresses AS T2 ON T1.current_address_id  =  T2.address_id WHERE T2.state_province_county  =  'NorthCarolina' EXCEPT SELECT DISTINCT T3.last_name FROM Students AS T3 JOIN Student_Enrolment AS T4 ON T3.student_id  =  T4.student_id
```

**Returned.**
```sql
SELECT T1.last_name FROM students AS T1 JOIN addresses AS T2 ON T1.current_address_id = T2.address_id WHERE T2.state_province_county = 'North Carolina' EXCEPT SELECT T3.last_name FROM students AS T3 JOIN student_enrolment AS T4 ON T3.student_id = T4.student_id
```

**First disagreeing instance** `student_transcripts_tracking.sqlite` (this is the shipped benchmark database).

Gold returns 2 row(s), 1 column(s):

    Gleichner
    Weimann

Returned query gives 0 row(s), None column(s):

    (no rows)

Difference: rep_empty; 0 row(s) in common, 2 only in the gold, 0 only in the returned result.

### R457  (question 260, database `student_transcripts_tracking`)

- Returned by: xiyansql-32b/seed101
- Returned in cell: both A and D
- Class mass: 50/50
- Instances disagreeing: 22 of 55 (40%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the last name of the students who live in North Carolina but have not registered in any degree programs?

**Gold.**
```sql
SELECT T1.last_name FROM Students AS T1 JOIN Addresses AS T2 ON T1.current_address_id  =  T2.address_id WHERE T2.state_province_county  =  'NorthCarolina' EXCEPT SELECT DISTINCT T3.last_name FROM Students AS T3 JOIN Student_Enrolment AS T4 ON T3.student_id  =  T4.student_id
```

**Returned.**
```sql
SELECT T1.last_name FROM Students AS T1 JOIN Addresses AS T2 ON T1.current_address_id = T2.address_id WHERE T2.state_province_county = 'North Carolina' EXCEPT SELECT T3.last_name FROM Students AS T3 JOIN Student_Enrolment AS T4 ON T3.student_id = T4.student_id
```

**First disagreeing instance** `student_transcripts_tracking.sqlite` (this is the shipped benchmark database).

Gold returns 2 row(s), 1 column(s):

    Gleichner
    Weimann

Returned query gives 0 row(s), None column(s):

    (no rows)

Difference: rep_empty; 0 row(s) in common, 2 only in the gold, 0 only in the returned result.

### R458  (question 262, database `student_transcripts_tracking`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed202, xiyansql-32b/seed303
- Returned in cell: both A and D
- Class mass: 50/50, 50/50, 50/50
- Instances disagreeing: 3 of 55 (5%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the mobile phone number of the student named Timmothy Ward ?

**Gold.**
```sql
select cell_mobile_number from students where first_name  =  'timmothy' and last_name  =  'ward'
```

**Returned.**
```sql
SELECT cell_mobile_number FROM Students WHERE first_name = 'Timmothy' AND last_name = 'Ward'
```

**First disagreeing instance** `student_transcripts_tracking.sqlite` (this is the shipped benchmark database).

Gold returns 0 row(s), None column(s):

    (no rows)

Returned query gives 1 row(s), 1 column(s):

    (096)889-8954x524

Difference: gold_empty; 0 row(s) in common, 0 only in the gold, 1 only in the returned result.

### R459  (question 264, database `student_transcripts_tracking`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed202, xiyansql-32b/seed303
- Returned in cell: both A and D
- Class mass: 39/50, 37/50, 41/50
- Instances disagreeing: 53 of 55 (96%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Who is the earliest graduate of the school? List the first name, middle name and last name.

**Gold.**
```sql
SELECT first_name ,  middle_name ,  last_name FROM Students ORDER BY date_left ASC LIMIT 1
```

**Returned.**
```sql
SELECT T1.first_name , T1.middle_name , T1.last_name FROM Students AS T1 JOIN Transcripts AS T2 ON T1.student_id = T2.transcript_id ORDER BY T2.transcript_date LIMIT 1
```

**First disagreeing instance** `student_transcripts_tracking.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 3 column(s):

    Timmothy | Anna | Ward

Returned query gives 1 row(s), 3 column(s):

    Delaney | Judd | Ankunding

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R460  (question 265, database `student_transcripts_tracking`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed202, xiyansql-32b/seed303
- Returned in cell: both A and D
- Class mass: 32/50, 33/50, 36/50
- Instances disagreeing: 51 of 55 (93%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What is the first, middle, and last name of the earliest school graduate?

**Gold.**
```sql
SELECT first_name ,  middle_name ,  last_name FROM Students ORDER BY date_left ASC LIMIT 1
```

**Returned.**
```sql
SELECT T1.first_name , T1.middle_name , T1.last_name FROM Students AS T1 JOIN Student_Enrolment AS T2 ON T1.student_id = T2.student_id JOIN Transcripts AS T3 ON T2.student_enrolment_id = T3.transcript_id ORDER BY T3.transcript_date LIMIT 1
```

**First disagreeing instance** `student_transcripts_tracking.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 3 column(s):

    Timmothy | Anna | Ward

Returned query gives 1 row(s), 3 column(s):

    Orrin | Neal | Kemmer

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R461  (question 266, database `student_transcripts_tracking`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed202, xiyansql-32b/seed303
- Returned in cell: both A and D
- Class mass: 50/50, 50/50, 50/50
- Instances disagreeing: 55 of 55 (100%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Which place holds the most number of students currently? List the id and all lines.

**Gold.**
```sql
SELECT T1.address_id ,  T1.line_1 ,  T1.line_2 FROM Addresses AS T1 JOIN Students AS T2 ON T1.address_id  =  T2.current_address_id GROUP BY T1.address_id ORDER BY count(*) DESC LIMIT 1
```

**Returned.**
```sql
SELECT T1.address_id , T1.line_1 , T1.line_2 , T1.line_3 FROM addresses AS T1 JOIN students AS T2 ON T1.address_id = T2.current_address_id GROUP BY T1.address_id ORDER BY count(*) DESC LIMIT 1
```

**First disagreeing instance** `student_transcripts_tracking.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 3 column(s):

    9 | 0643 Muller Vista | Suite 383

Returned query gives 1 row(s), 4 column(s):

    9 | 0643 Muller Vista | Suite 383 | NULL

Difference: col_count_differs, disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R462  (question 270, database `student_transcripts_tracking`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed202, xiyansql-32b/seed303
- Returned in cell: both A and D
- Class mass: 50/50, 50/50, 50/50
- Instances disagreeing: 18 of 55 (33%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find the first name of the students who permanently live in Haiti or have the cell phone number 09700166582.

**Gold.**
```sql
select t1.first_name from students as t1 join addresses as t2 on t1.permanent_address_id  =  t2.address_id where t2.country  =  'haiti' or t1.cell_mobile_number  =  '09700166582'
```

**Returned.**
```sql
SELECT T2.first_name FROM addresses AS T1 JOIN students AS T2 ON T1.address_id = T2.permanent_address_id WHERE T1.country = 'Haiti' UNION SELECT first_name FROM students WHERE cell_mobile_number = '09700166582'
```

**First disagreeing instance** `student_transcripts_tracking.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    Jarvis

Returned query gives 4 row(s), 1 column(s):

    Delaney
    Hobart
    Jarvis
    Warren

Difference: gold_subset_of_rep; 1 row(s) in common, 0 only in the gold, 3 only in the returned result.

### R463  (question 271, database `student_transcripts_tracking`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed202, xiyansql-32b/seed303
- Returned in cell: both A and D
- Class mass: 50/50, 50/50, 50/50
- Instances disagreeing: 18 of 55 (33%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the first names of the students who live in Haiti permanently or have the cell phone number 09700166582?

**Gold.**
```sql
select t1.first_name from students as t1 join addresses as t2 on t1.permanent_address_id  =  t2.address_id where t2.country  =  'haiti' or t1.cell_mobile_number  =  '09700166582'
```

**Returned.**
```sql
SELECT T2.first_name FROM addresses AS T1 JOIN students AS T2 ON T1.address_id = T2.permanent_address_id WHERE T1.country = 'Haiti' UNION SELECT first_name FROM students WHERE cell_mobile_number = '09700166582'
```

**First disagreeing instance** `student_transcripts_tracking.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    Jarvis

Returned query gives 4 row(s), 1 column(s):

    Delaney
    Hobart
    Jarvis
    Warren

Difference: gold_subset_of_rep; 1 row(s) in common, 0 only in the gold, 3 only in the returned result.

### R464  (question 309, database `tvshow`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed202, xiyansql-32b/seed303
- Returned in cell: both A and D
- Class mass: 40/50, 42/50, 43/50
- Instances disagreeing: 25 of 25 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** which countries' tv channels are not playing any cartoon  Todd Casey writes?

**Gold.**
```sql
SELECT country FROM TV_Channel EXCEPT SELECT T1.country FROM TV_Channel AS T1 JOIN cartoon AS T2 ON T1.id = T2.Channel WHERE T2.written_by  =  'Todd Casey'
```

**Returned.**
```sql
SELECT country FROM tv_channel WHERE id NOT IN (SELECT channel FROM cartoon WHERE written_by = 'Todd Casey')
```

**First disagreeing instance** `tvshow.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    Poland

Returned query gives 13 row(s), 1 column(s):

    Italy
    Italy
    Italy
    Italy
    United Kingdom
    Italy
    Poland
    Italy
    Italy
    Italy
    Italy
    Italy
    ... (13 rows total)

Difference: gold_subset_of_rep; 1 row(s) in common, 0 only in the gold, 2 only in the returned result.

### R465  (question 311, database `tvshow`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed202, xiyansql-32b/seed303
- Returned in cell: both A and D
- Class mass: 36/50, 34/50, 32/50
- Instances disagreeing: 20 of 25 (80%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find the series name and country of the tv channel that is playing some cartoons  Ben Jones and Michael Chang directs?

**Gold.**
```sql
SELECT T1.series_name ,  T1.country FROM TV_Channel AS T1 JOIN cartoon AS T2 ON T1.id = T2.Channel WHERE T2.directed_by  =  'Michael Chang' INTERSECT SELECT T1.series_name ,  T1.country FROM TV_Channel AS T1 JOIN cartoon AS T2 ON T1.id = T2.Channel WHERE T2.directed_by  =  'Ben Jones'
```

**Returned.**
```sql
SELECT T1.series_name , T1.country FROM TV_Channel AS T1 JOIN cartoon AS T2 ON T1.id = T2.Channel WHERE T2.directed_by = "Ben Jones, Michael Chang"
```

**First disagreeing instance** `tvshow.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    MTV Dance | United Kingdom

Returned query gives 0 row(s), None column(s):

    (no rows)

Difference: rep_empty; 0 row(s) in common, 1 only in the gold, 0 only in the returned result.

### R466  (question 312, database `tvshow`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed202, xiyansql-32b/seed303
- Returned in cell: both A and D
- Class mass: 37/50, 35/50, 32/50
- Instances disagreeing: 20 of 25 (80%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the series name and country of all TV channels that are playing cartoons  Ben Jones and Michael Chang directs?

**Gold.**
```sql
SELECT T1.series_name ,  T1.country FROM TV_Channel AS T1 JOIN cartoon AS T2 ON T1.id = T2.Channel WHERE T2.directed_by  =  'Michael Chang' INTERSECT SELECT T1.series_name ,  T1.country FROM TV_Channel AS T1 JOIN cartoon AS T2 ON T1.id = T2.Channel WHERE T2.directed_by  =  'Ben Jones'
```

**Returned.**
```sql
SELECT T1.series_name , T1.country FROM TV_Channel AS T1 JOIN cartoon AS T2 ON T1.id = T2.Channel WHERE T2.directed_by = "Ben Jones and Michael Chang"
```

**First disagreeing instance** `tvshow.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 2 column(s):

    MTV Dance | United Kingdom

Returned query gives 0 row(s), None column(s):

    (no rows)

Difference: rep_empty; 0 row(s) in common, 1 only in the gold, 0 only in the returned result.

### R467  (question 356, database `world_1`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed202, xiyansql-32b/seed303
- Returned in cell: both A and D
- Class mass: 47/50, 50/50, 49/50
- Instances disagreeing: 13 of 46 (28%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the average life expectancy in African countries that are republics?

**Gold.**
```sql
SELECT avg(LifeExpectancy) FROM country WHERE Continent  =  "Africa" AND GovernmentForm  =  "Republic"
```

**Returned.**
```sql
SELECT avg(LifeExpectancy) FROM country WHERE Region = "Africa" AND GovernmentForm = "Republic"
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    50.84347826086957

Returned query gives 1 row(s), 1 column(s):

    NULL

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R468  (question 357, database `world_1`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed202, xiyansql-32b/seed303
- Returned in cell: both A and D
- Class mass: 49/50, 50/50, 49/50
- Instances disagreeing: 13 of 46 (28%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Give the average life expectancy for countries in Africa which are republics?

**Gold.**
```sql
SELECT avg(LifeExpectancy) FROM country WHERE Continent  =  "Africa" AND GovernmentForm  =  "Republic"
```

**Returned.**
```sql
SELECT avg(LifeExpectancy) FROM country WHERE Region = "Africa" AND GovernmentForm = "Republic"
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    50.84347826086957

Returned query gives 1 row(s), 1 column(s):

    NULL

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R469  (question 365, database `world_1`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed202
- Returned in cell: D only
- Class mass: 28/50, 25/50
- Instances disagreeing: 37 of 46 (80%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** How many different forms of governments are there in Africa?

**Gold.**
```sql
SELECT count(DISTINCT GovernmentForm) FROM country WHERE Continent  =  "Africa"
```

**Returned.**
```sql
SELECT count(DISTINCT GovernmentForm) FROM country WHERE region LIKE "%Africa%"
```

**First disagreeing instance** `world_1v5080.sqlite`.

Gold returns 1 row(s), 1 column(s):

    6

Returned query gives 1 row(s), 1 column(s):

    18

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R470  (question 382, database `world_1`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed202, xiyansql-32b/seed303
- Returned in cell: both A and D
- Class mass: 50/50, 50/50, 50/50
- Instances disagreeing: 22 of 46 (48%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the countries where either English or Dutch is officially spoken ?

**Gold.**
```sql
select t1.name from country as t1 join countrylanguage as t2 on t1.code  =  t2.countrycode where t2.language  =  "english" and isofficial  =  "t" union select t1.name from country as t1 join countrylanguage as t2 on t1.code  =  t2.countrycode where t2.language  =  "dutch" and isofficial  =  "t"
```

**Returned.**
```sql
SELECT T1.Name FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode WHERE T2.IsOfficial = "T" AND T2.Language = "English" UNION SELECT T1.Name FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode WHERE T2.IsOfficial = "T" AND T2.Language = "Dutch"
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 0 row(s), None column(s):

    (no rows)

Returned query gives 48 row(s), 1 column(s):

    American Samoa
    Anguilla
    Antigua and Barbuda
    Aruba
    Australia
    Barbados
    Belgium
    Belize
    Bermuda
    Canada
    Cayman Islands
    Christmas Island
    ... (48 rows total)

Difference: gold_empty; 0 row(s) in common, 0 only in the gold, 48 only in the returned result.

### R471  (question 398, database `world_1`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed202, xiyansql-32b/seed303
- Returned in cell: both A and D
- Class mass: 50/50, 50/50, 50/50
- Instances disagreeing: 34 of 46 (74%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the countries that have greater surface area than any country in Europe?

**Gold.**
```sql
SELECT Name FROM country WHERE SurfaceArea  >  (SELECT min(SurfaceArea) FROM country WHERE Continent  =  "Europe")
```

**Returned.**
```sql
SELECT Name FROM country WHERE SurfaceArea > (SELECT min(SurfaceArea) FROM country WHERE Region = "Europe")
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 238 row(s), 1 column(s):

    Aruba
    Afghanistan
    Angola
    Anguilla
    Albania
    Andorra
    Netherlands Antilles
    United Arab Emirates
    Argentina
    Armenia
    American Samoa
    Antarctica
    ... (238 rows total)

Returned query gives 0 row(s), None column(s):

    (no rows)

Difference: rep_empty; 0 row(s) in common, 238 only in the gold, 0 only in the returned result.

### R472  (question 399, database `world_1`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed202, xiyansql-32b/seed303
- Returned in cell: both A and D
- Class mass: 50/50, 50/50, 50/50
- Instances disagreeing: 41 of 46 (89%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Which countries larger than that of any country in Europe by land?

**Gold.**
```sql
SELECT Name FROM country WHERE SurfaceArea  >  (SELECT min(SurfaceArea) FROM country WHERE Continent  =  "Europe")
```

**Returned.**
```sql
SELECT Name FROM country WHERE SurfaceArea > (SELECT max(SurfaceArea) FROM country WHERE Region = "Europe")
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 238 row(s), 1 column(s):

    Aruba
    Afghanistan
    Angola
    Anguilla
    Albania
    Andorra
    Netherlands Antilles
    United Arab Emirates
    Argentina
    Armenia
    American Samoa
    Antarctica
    ... (238 rows total)

Returned query gives 0 row(s), None column(s):

    (no rows)

Difference: rep_empty; 0 row(s) in common, 238 only in the gold, 0 only in the returned result.

### R473  (question 401, database `world_1`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed202, xiyansql-32b/seed303
- Returned in cell: both A and D
- Class mass: 50/50, 50/50, 50/50
- Instances disagreeing: 28 of 46 (61%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Which African countries have fewer people than that of any country in Asia?

**Gold.**
```sql
SELECT Name FROM country WHERE Continent  =  "Africa"  AND population  <  (SELECT min(population) FROM country WHERE Continent  =  "Asia")
```

**Returned.**
```sql
SELECT Name FROM country WHERE Continent = "Africa" AND population < (SELECT max(population) FROM country WHERE Continent = "Asia")
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 5 row(s), 1 column(s):

    British Indian Ocean Territory
    Mayotte
    Saint Helena
    Sao Tome and Principe
    Seychelles

Returned query gives 58 row(s), 1 column(s):

    Angola
    Burundi
    Benin
    Burkina Faso
    Botswana
    Central African Republic
    Côte d’Ivoire
    Cameroon
    Congo, The Democratic Republic of the
    Congo
    Comoros
    Cape Verde
    ... (58 rows total)

Difference: gold_subset_of_rep; 5 row(s) in common, 0 only in the gold, 53 only in the returned result.

### R474  (question 403, database `world_1`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed202, xiyansql-32b/seed303
- Returned in cell: both A and D
- Class mass: 50/50, 50/50, 50/50
- Instances disagreeing: 29 of 46 (63%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the Asian countries have more people than that of any country in Africa?

**Gold.**
```sql
SELECT Name FROM country WHERE Continent  =  "Asia"  AND population  >  (SELECT min(population) FROM country WHERE Continent  =  "Africa")
```

**Returned.**
```sql
SELECT Name FROM country WHERE Continent = "Asia" AND population > (SELECT max(population) FROM country WHERE Continent = "Africa")
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 51 row(s), 1 column(s):

    Afghanistan
    United Arab Emirates
    Armenia
    Azerbaijan
    Bangladesh
    Bahrain
    Brunei
    Bhutan
    China
    Cyprus
    Georgia
    Hong Kong
    ... (51 rows total)

Returned query gives 6 row(s), 1 column(s):

    Bangladesh
    China
    Indonesia
    India
    Japan
    Pakistan

Difference: rep_subset_of_gold; 6 row(s) in common, 45 only in the gold, 0 only in the returned result.

### R475  (question 404, database `world_1`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed202, xiyansql-32b/seed303
- Returned in cell: both A and D
- Class mass: 50/50, 50/50, 50/50
- Instances disagreeing: 32 of 46 (70%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the country codes for countries that do not speak English?

**Gold.**
```sql
SELECT CountryCode FROM countrylanguage EXCEPT SELECT CountryCode FROM countrylanguage WHERE LANGUAGE  =  "English"
```

**Returned.**
```sql
SELECT Code FROM country EXCEPT SELECT CountryCode FROM countrylanguage WHERE LANGUAGE = "English"
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 173 row(s), 1 column(s):

    AFG
    AGO
    ALB
    AND
    ARE
    ARG
    ARM
    AUT
    AZE
    BDI
    BEL
    BEN
    ... (173 rows total)

Returned query gives 179 row(s), 1 column(s):

    AFG
    AGO
    ALB
    AND
    ARE
    ARG
    ARM
    ATA
    ATF
    AUT
    AZE
    BDI
    ... (179 rows total)

Difference: gold_subset_of_rep; 173 row(s) in common, 0 only in the gold, 6 only in the returned result.

### R476  (question 405, database `world_1`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed202, xiyansql-32b/seed303
- Returned in cell: both A and D
- Class mass: 50/50, 50/50, 50/50
- Instances disagreeing: 32 of 46 (70%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Return the country codes for countries that do not speak English.

**Gold.**
```sql
SELECT CountryCode FROM countrylanguage EXCEPT SELECT CountryCode FROM countrylanguage WHERE LANGUAGE  =  "English"
```

**Returned.**
```sql
SELECT Code FROM country EXCEPT SELECT CountryCode FROM countrylanguage WHERE LANGUAGE = "English"
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 173 row(s), 1 column(s):

    AFG
    AGO
    ALB
    AND
    ARE
    ARG
    ARM
    AUT
    AZE
    BDI
    BEL
    BEN
    ... (173 rows total)

Returned query gives 179 row(s), 1 column(s):

    AFG
    AGO
    ALB
    AND
    ARE
    ARG
    ARM
    ATA
    ATF
    AUT
    AZE
    BDI
    ... (179 rows total)

Difference: gold_subset_of_rep; 173 row(s) in common, 0 only in the gold, 6 only in the returned result.

### R477  (question 407, database `world_1`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed202, xiyansql-32b/seed303
- Returned in cell: both A and D
- Class mass: 50/50, 50/50, 50/50
- Instances disagreeing: 46 of 46 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Give the country codes for countries in which people does not speak English.

**Gold.**
```sql
SELECT DISTINCT CountryCode FROM countrylanguage WHERE LANGUAGE != "English"
```

**Returned.**
```sql
SELECT Code FROM country EXCEPT SELECT CountryCode FROM countrylanguage WHERE LANGUAGE = "English"
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 223 row(s), 1 column(s):

    ABW
    AFG
    AGO
    ALB
    AND
    ANT
    ARE
    ARG
    ARM
    ASM
    ATG
    AUS
    ... (223 rows total)

Returned query gives 179 row(s), 1 column(s):

    AFG
    AGO
    ALB
    AND
    ARE
    ARG
    ARM
    ATA
    ATF
    AUT
    AZE
    BDI
    ... (179 rows total)

Difference: values differ; 173 row(s) in common, 50 only in the gold, 6 only in the returned result.

### R478  (question 410, database `world_1`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed202
- Returned in cell: both A and D
- Class mass: 39/50, 30/50
- Instances disagreeing: 37 of 46 (80%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Which cities are in European countries where English is not spoken officially?

**Gold.**
```sql
SELECT DISTINCT T2.Name FROM country AS T1 JOIN city AS T2 ON T2.CountryCode  =  T1.Code WHERE T1.Continent  =  'Europe' AND T1.Name NOT IN (SELECT T3.Name FROM country AS T3 JOIN countrylanguage AS T4 ON T3.Code  =  T4.CountryCode WHERE T4.IsOfficial  =  'T' AND T4.Language  =  'English')
```

**Returned.**
```sql
SELECT T1.Name FROM city AS T1 JOIN country AS T2 ON T1.CountryCode = T2.Code WHERE T2.Region = "Europe" AND T1.Name NOT IN (SELECT T1.Name FROM city AS T1 JOIN country AS T2 ON T1.CountryCode = T2.Code JOIN countrylanguage AS T3 ON T2.Code = T3.CountryCode WHERE T3.IsOfficial = "T" AND T3.Language = "English")
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 753 row(s), 1 column(s):

    Amsterdam
    Rotterdam
    Haag
    Utrecht
    Eindhoven
    Tilburg
    Groningen
    Breda
    Apeldoorn
    Nijmegen
    Enschede
    Haarlem
    ... (753 rows total)

Returned query gives 0 row(s), None column(s):

    (no rows)

Difference: rep_empty; 0 row(s) in common, 753 only in the gold, 0 only in the returned result.

### R479  (question 411, database `world_1`)

- Returned by: xiyansql-32b/seed101
- Returned in cell: both A and D
- Class mass: 50/50
- Instances disagreeing: 1 of 46 (2%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Whic`h unique cities are in  Asian countries where Chinese is the official ?

**Gold.**
```sql
select distinct t3.name from country as t1 join countrylanguage as t2 on t1.code  =  t2.countrycode join city as t3 on t1.code  =  t3.countrycode where t2.isofficial  =  't' and t2.language  =  'chinese' and t1.continent  =  "asia"
```

**Returned.**
```sql
SELECT DISTINCT T1.Name FROM city AS T1 JOIN country AS T2 ON T1.CountryCode = T2.Code JOIN countrylanguage AS T3 ON T3.CountryCode = T2.Code WHERE T3.IsOfficial = "T" AND T3.Language = "Chinese" AND T2.Continent = "Asia"
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 0 row(s), None column(s):

    (no rows)

Returned query gives 359 row(s), 1 column(s):

    Shanghai
    Peking
    Chongqing
    Tianjin
    Wuhan
    Harbin
    Shenyang
    Kanton [Guangzhou]
    Chengdu
    Nanking [Nanjing]
    Changchun
    Xi´an
    ... (359 rows total)

Difference: gold_empty; 0 row(s) in common, 0 only in the gold, 359 only in the returned result.

### R480  (question 413, database `world_1`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed303
- Returned in cell: both A and D
- Class mass: 50/50, 50/50
- Instances disagreeing: 44 of 46 (96%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What are the name, independence year, and surface area of the country with the least number of nationalities?

**Gold.**
```sql
SELECT Name ,  SurfaceArea ,  IndepYear FROM country ORDER BY Population LIMIT 1
```

**Returned.**
```sql
SELECT T1.Name , T1.IndepYear , T1.SurfaceArea FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode GROUP BY T1.Name ORDER BY COUNT(*) LIMIT 1
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 3 column(s):

    Antarctica | 13120000.0 | NULL

Returned query gives 1 row(s), 3 column(s):

    Anguilla | NULL | 96.0

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R481  (question 425, database `world_1`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed202, xiyansql-32b/seed303
- Returned in cell: both A and D
- Class mass: 37/50, 41/50, 41/50
- Instances disagreeing: 39 of 46 (85%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the names of the countries that are in Europe and have 80000 people?

**Gold.**
```sql
SELECT Name FROM country WHERE continent  =  "Europe" AND Population  =  "80000"
```

**Returned.**
```sql
SELECT Name FROM country WHERE continent = "Europe" AND population > 80000
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 0 row(s), None column(s):

    (no rows)

Returned query gives 38 row(s), 1 column(s):

    Albania
    Austria
    Belgium
    Bulgaria
    Bosnia and Herzegovina
    Belarus
    Switzerland
    Czech Republic
    Germany
    Denmark
    Spain
    Estonia
    ... (38 rows total)

Difference: gold_empty; 0 row(s) in common, 0 only in the gold, 38 only in the returned result.

### R482  (question 426, database `world_1`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed202, xiyansql-32b/seed303
- Returned in cell: both A and D
- Class mass: 34/50, 35/50, 38/50
- Instances disagreeing: 39 of 46 (85%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Give the names of countries that are in Europe and have 80000 people.

**Gold.**
```sql
SELECT Name FROM country WHERE continent  =  "Europe" AND Population  =  "80000"
```

**Returned.**
```sql
SELECT Name FROM country WHERE continent = "Europe" AND population > 80000
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 0 row(s), None column(s):

    (no rows)

Returned query gives 38 row(s), 1 column(s):

    Albania
    Austria
    Belgium
    Bulgaria
    Bosnia and Herzegovina
    Belarus
    Switzerland
    Czech Republic
    Germany
    Denmark
    Spain
    Estonia
    ... (38 rows total)

Difference: gold_empty; 0 row(s) in common, 0 only in the gold, 38 only in the returned result.

### R483  (question 433, database `world_1`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed202
- Returned in cell: both A and D
- Class mass: 46/50, 45/50
- Instances disagreeing: 46 of 46 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the total number of countries where Spanish is spoken by the largest percentage of people?

**Gold.**
```sql
SELECT count(*) ,   max(Percentage) FROM countrylanguage WHERE LANGUAGE  =  "Spanish" GROUP BY CountryCode
```

**Returned.**
```sql
SELECT count(*) FROM (SELECT countrycode FROM countrylanguage WHERE LANGUAGE = "Spanish" ORDER BY percentage DESC LIMIT 1)
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 28 row(s), 2 column(s):

    1 | 7.4
    1 | 44.6
    1 | 96.8
    1 | 31.6
    1 | 87.7
    1 | 0.7
    1 | 89.7
    1 | 99.0
    1 | 97.5
    1 | 100.0
    1 | 98.0
    1 | 93.0
    ... (28 rows total)

Returned query gives 1 row(s), 1 column(s):

    1

Difference: col_count_differs, disjoint; 0 row(s) in common, 27 only in the gold, 1 only in the returned result.

### R484  (question 434, database `world_1`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed202, xiyansql-32b/seed303
- Returned in cell: both A and D
- Class mass: 50/50, 50/50, 50/50
- Instances disagreeing: 46 of 46 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Count the number of countries for which Spanish is predominantly spoken .

**Gold.**
```sql
SELECT count(*) ,   max(Percentage) FROM countrylanguage WHERE LANGUAGE  =  "Spanish" GROUP BY CountryCode
```

**Returned.**
```sql
SELECT count(*) FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode WHERE T2.Language = "Spanish" AND T2.Percentage > 50
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 28 row(s), 2 column(s):

    1 | 7.4
    1 | 44.6
    1 | 96.8
    1 | 31.6
    1 | 87.7
    1 | 0.7
    1 | 89.7
    1 | 99.0
    1 | 97.5
    1 | 100.0
    1 | 98.0
    1 | 93.0
    ... (28 rows total)

Returned query gives 1 row(s), 1 column(s):

    20

Difference: col_count_differs, disjoint; 0 row(s) in common, 27 only in the gold, 1 only in the returned result.

### R485  (question 435, database `world_1`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed202, xiyansql-32b/seed303
- Returned in cell: both A and D
- Class mass: 50/50, 50/50, 50/50
- Instances disagreeing: 43 of 46 (93%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the codes of countries where Spanish is spoken by the largest percentage of people?

**Gold.**
```sql
SELECT CountryCode ,  max(Percentage) FROM countrylanguage WHERE LANGUAGE  =  "Spanish" GROUP BY CountryCode
```

**Returned.**
```sql
SELECT CountryCode FROM countrylanguage WHERE LANGUAGE = "Spanish" ORDER BY Percentage DESC LIMIT 1
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 28 row(s), 2 column(s):

    ABW | 7.4
    AND | 44.6
    ARG | 96.8
    BLZ | 31.6
    BOL | 87.7
    CAN | 0.7
    CHL | 89.7
    COL | 99.0
    CRI | 97.5
    CUB | 100.0
    DOM | 98.0
    ECU | 93.0
    ... (28 rows total)

Returned query gives 1 row(s), 1 column(s):

    CUB

Difference: col_count_differs, disjoint; 0 row(s) in common, 28 only in the gold, 1 only in the returned result.

### R486  (question 436, database `world_1`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed202, xiyansql-32b/seed303
- Returned in cell: both A and D
- Class mass: 43/50, 43/50, 40/50
- Instances disagreeing: 43 of 46 (93%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Return the codes of countries for which Spanish is predominantly spoken .

**Gold.**
```sql
SELECT CountryCode ,  max(Percentage) FROM countrylanguage WHERE LANGUAGE  =  "Spanish" GROUP BY CountryCode
```

**Returned.**
```sql
SELECT CountryCode FROM countrylanguage WHERE LANGUAGE = "Spanish" AND Percentage > 50
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 28 row(s), 2 column(s):

    ABW | 7.4
    AND | 44.6
    ARG | 96.8
    BLZ | 31.6
    BOL | 87.7
    CAN | 0.7
    CHL | 89.7
    COL | 99.0
    CRI | 97.5
    CUB | 100.0
    DOM | 98.0
    ECU | 93.0
    ... (28 rows total)

Returned query gives 20 row(s), 1 column(s):

    ARG
    BOL
    CHL
    COL
    CRI
    CUB
    DOM
    ECU
    ESP
    GTM
    HND
    MEX
    ... (20 rows total)

Difference: col_count_differs, disjoint; 0 row(s) in common, 28 only in the gold, 20 only in the returned result.

### R487  (question 442, database `orchestra`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed202, xiyansql-32b/seed303
- Returned in cell: both A and D
- Class mass: 50/50, 50/50, 50/50
- Instances disagreeing: 28 of 28 (100%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Return the record companies of orchestras, sorted ascending by the time they have existed.

**Gold.**
```sql
SELECT Record_Company FROM orchestra ORDER BY Year_of_Founded DESC
```

**Returned.**
```sql
SELECT Record_Company FROM orchestra ORDER BY Year_of_Founded ASC
```

**First disagreeing instance** `orchestra.sqlite` (this is the shipped benchmark database).

Gold returns 12 row(s), 1 column(s):

    Columbia Masterworks
    Philips
    Philips Classics Records
    RCA
    EMI
    Koch Records / Naxos Records
    Decca Records
    Mercury Records
    Deutsche Grammophon
    Kultur
    Decca Records
    Delos Records

Returned query gives 12 row(s), 1 column(s):

    Kultur
    Decca Records
    Delos Records
    Mercury Records
    Deutsche Grammophon
    Decca Records
    Koch Records / Naxos Records
    EMI
    Philips
    Philips Classics Records
    RCA
    Columbia Masterworks

Difference: row_order_only; 11 row(s) in common, 0 only in the gold, 0 only in the returned result.

### R488  (question 467, database `dog_kennels`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed202, xiyansql-32b/seed303
- Returned in cell: both A and D
- Class mass: 50/50, 50/50, 50/50
- Instances disagreeing: 48 of 48 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the names of the dogs for which the owner spent more than 1000 for treatment?

**Gold.**
```sql
select name from dogs where dog_id not in ( select dog_id from treatments group by dog_id having sum(cost_of_treatment)  >  1000 )
```

**Returned.**
```sql
SELECT T1.name FROM Dogs AS T1 JOIN Treatments AS T2 ON T1.dog_id = T2.dog_id GROUP BY T1.dog_id HAVING sum(T2.cost_of_treatment) > 1000
```

**First disagreeing instance** `dog_kennels.sqlite` (this is the shipped benchmark database).

Gold returns 12 row(s), 1 column(s):

    Kacey
    Hipolito
    Mavis
    Houston
    Jeffrey
    Merritt
    Narciso
    George
    Bessie
    Betty
    Holden
    Jesus

Returned query gives 3 row(s), 1 column(s):

    Troy
    Lyric
    Evangeline

Difference: disjoint; 0 row(s) in common, 12 only in the gold, 3 only in the returned result.

### R489  (question 476, database `dog_kennels`)

- Returned by: xiyansql-32b/seed101
- Returned in cell: both A and D
- Class mass: 50/50
- Instances disagreeing: 40 of 48 (83%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the first name and last name of the professionals who have done treatment cheaper than average?

**Gold.**
```sql
SELECT DISTINCT T1.first_name ,  T1.last_name FROM Professionals AS T1 JOIN Treatments AS T2 WHERE cost_of_treatment  <  ( SELECT avg(cost_of_treatment) FROM Treatments )
```

**Returned.**
```sql
SELECT DISTINCT T1.first_name , T1.last_name FROM professionals AS T1 JOIN treatments AS T2 ON T1.professional_id = T2.professional_id WHERE cost_of_treatment < ( SELECT avg(cost_of_treatment) FROM treatments )
```

**First disagreeing instance** `dog_kennels.sqlite` (this is the shipped benchmark database).

Gold returns 15 row(s), 2 column(s):

    Taryn | Braun
    Jayson | Ullrich
    Olaf | Watsica
    Vernice | Tillman
    Danny | Considine
    Ruben | O'Reilly
    Velva | Hayes
    Karley | Hyatt
    Monte | Kshlerin
    Domenica | Jacobs
    Brady | Pouros
    Winfield | Christiansen
    ... (15 rows total)

Returned query gives 5 row(s), 2 column(s):

    Domenica | Jacobs
    Vernice | Tillman
    Karley | Hyatt
    Ruben | O'Reilly
    Monte | Kshlerin

Difference: rep_subset_of_gold; 5 row(s) in common, 10 only in the gold, 0 only in the returned result.

### R490  (question 477, database `dog_kennels`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed202, xiyansql-32b/seed303
- Returned in cell: both A and D
- Class mass: 50/50, 50/50, 50/50
- Instances disagreeing: 40 of 48 (83%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Which professionals have operated a treatment that is less expansive than the average? Give me theor first names and last names.

**Gold.**
```sql
SELECT DISTINCT T1.first_name ,  T1.last_name FROM Professionals AS T1 JOIN Treatments AS T2 WHERE cost_of_treatment  <  ( SELECT avg(cost_of_treatment) FROM Treatments )
```

**Returned.**
```sql
SELECT DISTINCT T1.first_name , T1.last_name FROM professionals AS T1 JOIN treatments AS T2 ON T1.professional_id = T2.professional_id WHERE T2.cost_of_treatment < ( SELECT avg(cost_of_treatment) FROM treatments )
```

**First disagreeing instance** `dog_kennels.sqlite` (this is the shipped benchmark database).

Gold returns 15 row(s), 2 column(s):

    Taryn | Braun
    Jayson | Ullrich
    Olaf | Watsica
    Vernice | Tillman
    Danny | Considine
    Ruben | O'Reilly
    Velva | Hayes
    Karley | Hyatt
    Monte | Kshlerin
    Domenica | Jacobs
    Brady | Pouros
    Winfield | Christiansen
    ... (15 rows total)

Returned query gives 5 row(s), 2 column(s):

    Domenica | Jacobs
    Vernice | Tillman
    Karley | Hyatt
    Ruben | O'Reilly
    Monte | Kshlerin

Difference: rep_subset_of_gold; 5 row(s) in common, 10 only in the gold, 0 only in the returned result.

### R491  (question 480, database `dog_kennels`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed202, xiyansql-32b/seed303
- Returned in cell: both A and D
- Class mass: 50/50, 50/50, 50/50
- Instances disagreeing: 41 of 48 (85%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** List the last name of the owner owning the youngest dog.

**Gold.**
```sql
SELECT T1.last_name FROM Owners AS T1 JOIN Dogs AS T2 ON T1.owner_id  =  T2.owner_id WHERE T2.age  =  ( SELECT max(age) FROM Dogs )
```

**Returned.**
```sql
SELECT T1.last_name FROM Owners AS T1 JOIN Dogs AS T2 ON T1.owner_id = T2.owner_id ORDER BY T2.date_of_birth DESC LIMIT 1
```

**First disagreeing instance** `dog_kennels.sqlite` (this is the shipped benchmark database).

Gold returns 3 row(s), 1 column(s):

    Feil
    Fisher
    Rippin

Returned query gives 1 row(s), 1 column(s):

    Mertz

Difference: disjoint; 0 row(s) in common, 3 only in the gold, 1 only in the returned result.

### R492  (question 481, database `dog_kennels`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed202, xiyansql-32b/seed303
- Returned in cell: both A and D
- Class mass: 50/50, 50/50, 50/50
- Instances disagreeing: 41 of 48 (85%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Who owns the youngest dog? Give me his or her last name.

**Gold.**
```sql
SELECT T1.last_name FROM Owners AS T1 JOIN Dogs AS T2 ON T1.owner_id  =  T2.owner_id WHERE T2.age  =  ( SELECT max(age) FROM Dogs )
```

**Returned.**
```sql
SELECT T1.last_name FROM Owners AS T1 JOIN Dogs AS T2 ON T1.owner_id = T2.owner_id ORDER BY T2.date_of_birth DESC LIMIT 1
```

**First disagreeing instance** `dog_kennels.sqlite` (this is the shipped benchmark database).

Gold returns 3 row(s), 1 column(s):

    Feil
    Fisher
    Rippin

Returned query gives 1 row(s), 1 column(s):

    Mertz

Difference: disjoint; 0 row(s) in common, 3 only in the gold, 1 only in the returned result.

### R493  (question 66, database `car_1`)

- Returned by: xiyansql-32b/seed202
- Returned in cell: both A and D
- Class mass: 28/50
- Instances disagreeing: 60 of 60 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the maker of the carr produced in the earliest  and what  year was it?

**Gold.**
```sql
SELECT T2.Make ,  T1.Year FROM CARS_DATA AS T1 JOIN CAR_NAMES AS T2 ON T1.Id  =  T2.MakeId WHERE T1.Year  =  (SELECT min(YEAR) FROM CARS_DATA);
```

**Returned.**
```sql
SELECT T1.Maker , T2.Year FROM CAR_MAKERS AS T1 JOIN MODEL_LIST AS T3 JOIN CAR_NAMES AS T4 JOIN CARS_DATA AS T2 ON T1.Id = T3.Maker AND T3.Model = T4.Model AND T4.MakeId = T2.Id ORDER BY T2.Year ASC LIMIT 1
```

**First disagreeing instance** `car_1.sqlite` (this is the shipped benchmark database).

Gold returns 35 row(s), 2 column(s):

    chevrolet chevelle malibu | 1970
    buick skylark 320 | 1970
    plymouth satellite | 1970
    amc rebel sst | 1970
    ford torino | 1970
    ford galaxie 500 | 1970
    chevrolet impala | 1970
    plymouth fury iii | 1970
    pontiac catalina | 1970
    amc ambassador dpl | 1970
    citroen ds-21 pallas | 1970
    chevrolet chevelle concours (sw) | 1970
    ... (35 rows total)

Returned query gives 1 row(s), 2 column(s):

    gm | 1970

Difference: disjoint; 0 row(s) in common, 35 only in the gold, 1 only in the returned result.

### R494  (question 260, database `student_transcripts_tracking`)

- Returned by: xiyansql-32b/seed202
- Returned in cell: both A and D
- Class mass: 50/50
- Instances disagreeing: 22 of 55 (40%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the last name of the students who live in North Carolina but have not registered in any degree programs?

**Gold.**
```sql
SELECT T1.last_name FROM Students AS T1 JOIN Addresses AS T2 ON T1.current_address_id  =  T2.address_id WHERE T2.state_province_county  =  'NorthCarolina' EXCEPT SELECT DISTINCT T3.last_name FROM Students AS T3 JOIN Student_Enrolment AS T4 ON T3.student_id  =  T4.student_id
```

**Returned.**
```sql
SELECT T1.last_name FROM students AS T1 JOIN addresses AS T2 ON T1.current_address_id = T2.address_id WHERE T2.state_province_county = 'North Carolina' EXCEPT SELECT T3.last_name FROM students AS T3 JOIN student_enrolment AS T4 ON T3.student_id = T4.student_id
```

**First disagreeing instance** `student_transcripts_tracking.sqlite` (this is the shipped benchmark database).

Gold returns 2 row(s), 1 column(s):

    Gleichner
    Weimann

Returned query gives 0 row(s), None column(s):

    (no rows)

Difference: rep_empty; 0 row(s) in common, 2 only in the gold, 0 only in the returned result.

### R495  (question 340, database `world_1`)

- Returned by: xiyansql-32b/seed202
- Returned in cell: both A and D
- Class mass: 27/50
- Instances disagreeing: 4 of 46 (9%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Which continent is Anguilla in?

**Gold.**
```sql
SELECT Continent FROM country WHERE Name  =  "Anguilla"
```

**Returned.**
```sql
SELECT T1.Continent FROM country AS T1 JOIN city AS T2 ON T1.Code = T2.CountryCode WHERE T2.Name = "Anguilla"
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 1 column(s):

    North America

Returned query gives 0 row(s), None column(s):

    (no rows)

Difference: rep_empty; 0 row(s) in common, 1 only in the gold, 0 only in the returned result.

### R496  (question 411, database `world_1`)

- Returned by: xiyansql-32b/seed202, xiyansql-32b/seed303
- Returned in cell: both A and D
- Class mass: 50/50, 50/50
- Instances disagreeing: 1 of 46 (2%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Whic`h unique cities are in  Asian countries where Chinese is the official ?

**Gold.**
```sql
select distinct t3.name from country as t1 join countrylanguage as t2 on t1.code  =  t2.countrycode join city as t3 on t1.code  =  t3.countrycode where t2.isofficial  =  't' and t2.language  =  'chinese' and t1.continent  =  "asia"
```

**Returned.**
```sql
SELECT DISTINCT T1.Name FROM city AS T1 JOIN country AS T2 ON T1.CountryCode = T2.Code JOIN countrylanguage AS T3 ON T3.CountryCode = T2.Code WHERE T2.Continent = "Asia" AND T3.IsOfficial = "T" AND T3.Language = "Chinese"
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 0 row(s), None column(s):

    (no rows)

Returned query gives 359 row(s), 1 column(s):

    Shanghai
    Peking
    Chongqing
    Tianjin
    Wuhan
    Harbin
    Shenyang
    Kanton [Guangzhou]
    Chengdu
    Nanking [Nanjing]
    Changchun
    Xi´an
    ... (359 rows total)

Difference: gold_empty; 0 row(s) in common, 0 only in the gold, 359 only in the returned result.

### R497  (question 413, database `world_1`)

- Returned by: xiyansql-32b/seed202
- Returned in cell: both A and D
- Class mass: 50/50
- Instances disagreeing: 44 of 46 (96%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What are the name, independence year, and surface area of the country with the least number of nationalities?

**Gold.**
```sql
SELECT Name ,  SurfaceArea ,  IndepYear FROM country ORDER BY Population LIMIT 1
```

**Returned.**
```sql
SELECT T1.Name , T1.IndepYear , T1.SurfaceArea FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode GROUP BY T1.Code ORDER BY COUNT(*) LIMIT 1
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 1 row(s), 3 column(s):

    Antarctica | 13120000.0 | NULL

Returned query gives 1 row(s), 3 column(s):

    Anguilla | NULL | 96.0

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### R498  (question 476, database `dog_kennels`)

- Returned by: xiyansql-32b/seed202, xiyansql-32b/seed303
- Returned in cell: both A and D
- Class mass: 50/50, 50/50
- Instances disagreeing: 40 of 48 (83%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the first name and last name of the professionals who have done treatment cheaper than average?

**Gold.**
```sql
SELECT DISTINCT T1.first_name ,  T1.last_name FROM Professionals AS T1 JOIN Treatments AS T2 WHERE cost_of_treatment  <  ( SELECT avg(cost_of_treatment) FROM Treatments )
```

**Returned.**
```sql
SELECT DISTINCT T1.first_name , T1.last_name FROM professionals AS T1 JOIN treatments AS T2 ON T1.professional_id = T2.professional_id WHERE cost_of_treatment < (SELECT avg(cost_of_treatment) FROM treatments)
```

**First disagreeing instance** `dog_kennels.sqlite` (this is the shipped benchmark database).

Gold returns 15 row(s), 2 column(s):

    Taryn | Braun
    Jayson | Ullrich
    Olaf | Watsica
    Vernice | Tillman
    Danny | Considine
    Ruben | O'Reilly
    Velva | Hayes
    Karley | Hyatt
    Monte | Kshlerin
    Domenica | Jacobs
    Brady | Pouros
    Winfield | Christiansen
    ... (15 rows total)

Returned query gives 5 row(s), 2 column(s):

    Domenica | Jacobs
    Vernice | Tillman
    Karley | Hyatt
    Ruben | O'Reilly
    Monte | Kshlerin

Difference: rep_subset_of_gold; 5 row(s) in common, 10 only in the gold, 0 only in the returned result.

### R499  (question 259, database `student_transcripts_tracking`)

- Returned by: xiyansql-32b/seed303
- Returned in cell: both A and D
- Class mass: 50/50
- Instances disagreeing: 22 of 55 (40%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find the last name of the students who currently live in North Carolina but have not registered in any degree program.

**Gold.**
```sql
SELECT T1.last_name FROM Students AS T1 JOIN Addresses AS T2 ON T1.current_address_id  =  T2.address_id WHERE T2.state_province_county  =  'NorthCarolina' EXCEPT SELECT DISTINCT T3.last_name FROM Students AS T3 JOIN Student_Enrolment AS T4 ON T3.student_id  =  T4.student_id
```

**Returned.**
```sql
SELECT T1.last_name FROM Students AS T1 JOIN Addresses AS T2 ON T1.current_address_id = T2.address_id WHERE T2.state_province_county = 'North Carolina' EXCEPT SELECT T3.last_name FROM Students AS T3 JOIN Student_Enrolment AS T4 ON T3.student_id = T4.student_id
```

**First disagreeing instance** `student_transcripts_tracking.sqlite` (this is the shipped benchmark database).

Gold returns 2 row(s), 1 column(s):

    Gleichner
    Weimann

Returned query gives 0 row(s), None column(s):

    (no rows)

Difference: rep_empty; 0 row(s) in common, 2 only in the gold, 0 only in the returned result.

### R500  (question 260, database `student_transcripts_tracking`)

- Returned by: xiyansql-32b/seed303
- Returned in cell: both A and D
- Class mass: 50/50
- Instances disagreeing: 22 of 55 (40%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the last name of the students who live in North Carolina but have not registered in any degree programs?

**Gold.**
```sql
SELECT T1.last_name FROM Students AS T1 JOIN Addresses AS T2 ON T1.current_address_id  =  T2.address_id WHERE T2.state_province_county  =  'NorthCarolina' EXCEPT SELECT DISTINCT T3.last_name FROM Students AS T3 JOIN Student_Enrolment AS T4 ON T3.student_id  =  T4.student_id
```

**Returned.**
```sql
SELECT T1.last_name FROM Students AS T1 JOIN Addresses AS T2 ON T1.current_address_id = T2.address_id WHERE T2.state_province_county = "North Carolina" EXCEPT SELECT T3.last_name FROM Students AS T3 JOIN Student_Enrolment AS T4 ON T3.student_id = T4.student_id
```

**First disagreeing instance** `student_transcripts_tracking.sqlite` (this is the shipped benchmark database).

Gold returns 2 row(s), 1 column(s):

    Gleichner
    Weimann

Returned query gives 0 row(s), None column(s):

    (no rows)

Difference: rep_empty; 0 row(s) in common, 2 only in the gold, 0 only in the returned result.

### R501  (question 410, database `world_1`)

- Returned by: xiyansql-32b/seed303
- Returned in cell: both A and D
- Class mass: 35/50
- Instances disagreeing: 37 of 46 (80%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Which cities are in European countries where English is not spoken officially?

**Gold.**
```sql
SELECT DISTINCT T2.Name FROM country AS T1 JOIN city AS T2 ON T2.CountryCode  =  T1.Code WHERE T1.Continent  =  'Europe' AND T1.Name NOT IN (SELECT T3.Name FROM country AS T3 JOIN countrylanguage AS T4 ON T3.Code  =  T4.CountryCode WHERE T4.IsOfficial  =  'T' AND T4.Language  =  'English')
```

**Returned.**
```sql
SELECT T1.Name FROM city AS T1 JOIN country AS T2 ON T1.CountryCode = T2.Code WHERE T2.Region = "Europe" AND T1.Name NOT IN (SELECT T1.Name FROM city AS T1 JOIN country AS T2 ON T1.CountryCode = T2.Code JOIN countrylanguage AS T3 ON T2.Code = T3.CountryCode WHERE T3.Language = "English" AND T3.IsOfficial = "T")
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 753 row(s), 1 column(s):

    Amsterdam
    Rotterdam
    Haag
    Utrecht
    Eindhoven
    Tilburg
    Groningen
    Breda
    Apeldoorn
    Nijmegen
    Enschede
    Haarlem
    ... (753 rows total)

Returned query gives 0 row(s), None column(s):

    (no rows)

Difference: rep_empty; 0 row(s) in common, 753 only in the gold, 0 only in the returned result.

### R502  (question 433, database `world_1`)

- Returned by: xiyansql-32b/seed303
- Returned in cell: both A and D
- Class mass: 46/50
- Instances disagreeing: 46 of 46 (100%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the total number of countries where Spanish is spoken by the largest percentage of people?

**Gold.**
```sql
SELECT count(*) ,   max(Percentage) FROM countrylanguage WHERE LANGUAGE  =  "Spanish" GROUP BY CountryCode
```

**Returned.**
```sql
SELECT count(*) FROM (SELECT * FROM countrylanguage WHERE LANGUAGE = "Spanish" ORDER BY Percentage DESC LIMIT 1)
```

**First disagreeing instance** `world_1.sqlite` (this is the shipped benchmark database).

Gold returns 28 row(s), 2 column(s):

    1 | 7.4
    1 | 44.6
    1 | 96.8
    1 | 31.6
    1 | 87.7
    1 | 0.7
    1 | 89.7
    1 | 99.0
    1 | 97.5
    1 | 100.0
    1 | 98.0
    1 | 93.0
    ... (28 rows total)

Returned query gives 1 row(s), 1 column(s):

    1

Difference: col_count_differs, disjoint; 0 row(s) in common, 27 only in the gold, 1 only in the returned result.


## Schema appendix

### `battle_death`
```
  battle(id, name, date, bulgarian_commander, latin_commander, result)
  death(caused_by_ship_id, id, note, killed, injured)
  ship(lost_in_battle, id, name, tonnage, ship_type, location, disposition_of_ship)
```

### `car_1`
```
  car_makers(Id, Maker, FullName, Country)
  car_names(MakeId, Model, Make)
  cars_data(Id, MPG, Cylinders, Edispl, Horsepower, Weight, Accelerate, Year)
  continents(ContId, Continent)
  countries(CountryId, CountryName, Continent)
  model_list(ModelId, Maker, Model)
```

### `concert_singer`
```
  concert(concert_ID, concert_Name, Theme, Stadium_ID, Year)
  singer(Singer_ID, Name, Country, Song_Name, Song_release_year, Age, Is_male)
  singer_in_concert(concert_ID, Singer_ID)
  stadium(Stadium_ID, Location, Name, Capacity, Highest, Lowest, Average)
```

### `course_teach`
```
  course(Course_ID, Staring_Date, Course)
  course_arrange(Course_ID, Teacher_ID, Grade)
  teacher(Teacher_ID, Name, Age, Hometown)
```

### `dog_kennels`
```
  Breeds(breed_code, breed_name)
  Charges(charge_id, charge_type, charge_amount)
  Dogs(dog_id, owner_id, abandoned_yn, breed_code, size_code, name, age, date_of_birth, gender, weight, date_arrived, date_adopted, date_departed)
  Owners(owner_id, first_name, last_name, street, city, state, zip_code, email_address, home_phone, cell_number)
  Professionals(professional_id, role_code, first_name, street, city, state, zip_code, last_name, email_address, home_phone, cell_number)
  Sizes(size_code, size_description)
  Treatment_Types(treatment_type_code, treatment_type_description)
  Treatments(treatment_id, dog_id, professional_id, treatment_type_code, date_of_treatment, cost_of_treatment)
```

### `flight_2`
```
  airlines(uid, Airline, Abbreviation, Country)
  airports(City, AirportCode, AirportName, Country, CountryAbbrev)
  flights(Airline, FlightNo, SourceAirport, DestAirport)
```

### `museum_visit`
```
  museum(Museum_ID, Name, Num_of_Staff, Open_Year)
  visit(Museum_ID, visitor_ID, Num_of_Ticket, Total_spent)
  visitor(ID, Name, Level_of_membership, Age)
```

### `network_1`
```
  Friend(student_id, friend_id)
  Highschooler(ID, name, grade)
  Likes(student_id, liked_id)
```

### `orchestra`
```
  conductor(Conductor_ID, Name, Age, Nationality, Year_of_Work)
  orchestra(Orchestra_ID, Orchestra, Conductor_ID, Record_Company, Year_of_Founded, Major_Record_Format)
  performance(Performance_ID, Orchestra_ID, Type, Date, Official_ratings_(millions), Weekly_rank, Share)
  show(Show_ID, Performance_ID, If_first_show, Result, Attendance)
```

### `pets_1`
```
  Has_Pet(StuID, PetID)
  Pets(PetID, PetType, pet_age, weight)
  Student(StuID, LName, Fname, Age, Sex, Major, Advisor, city_code)
```

### `real_estate_properties`
```
  Other_Available_Features(feature_id, feature_type_code, feature_name, feature_description)
  Other_Property_Features(property_id, feature_id, property_feature_description)
  Properties(property_id, property_type_code, date_on_market, date_sold, property_name, property_address, room_count, vendor_requested_price, buyer_offered_price, agreed_selling_price, apt_feature_1, apt_feature_2, apt_feature_3, fld_feature_1, fld_feature_2, fld_feature_3, hse_feature_1, hse_feature_2, hse_feature_3, oth_feature_1, oth_feature_2, oth_feature_3, shp_feature_1, shp_feature_2, shp_feature_3, other_property_details)
  Ref_Feature_Types(feature_type_code, feature_type_name)
  Ref_Property_Types(property_type_code, property_type_description)
```

### `student_transcripts_tracking`
```
  Addresses(address_id, line_1, line_2, line_3, city, zip_postcode, state_province_county, country, other_address_details)
  Courses(course_id, course_name, course_description, other_details)
  Degree_Programs(degree_program_id, department_id, degree_summary_name, degree_summary_description, other_details)
  Departments(department_id, department_name, department_description, other_details)
  Sections(section_id, course_id, section_name, section_description, other_details)
  Semesters(semester_id, semester_name, semester_description, other_details)
  Student_Enrolment(student_enrolment_id, degree_program_id, semester_id, student_id, other_details)
  Student_Enrolment_Courses(student_course_id, course_id, student_enrolment_id)
  Students(student_id, current_address_id, permanent_address_id, first_name, middle_name, last_name, cell_mobile_number, email_address, ssn, date_first_registered, date_left, other_student_details)
  Transcript_Contents(student_course_id, transcript_id)
  Transcripts(transcript_id, transcript_date, other_details)
```

### `tvshow`
```
  Cartoon(id, Title, Directed_by, Written_by, Original_air_date, Production_code, Channel)
  TV_Channel(id, series_name, Country, Language, Content, Pixel_aspect_ratio_PAR, Hight_definition_TV, Pay_per_view_PPV, Package_Option)
  TV_series(id, Episode, Air_Date, Rating, Share, 18_49_Rating_Share, Viewers_m, Weekly_Rank, Channel)
```

### `world_1`
```
  city(ID, Name, CountryCode, District, Population)
  country(Code, Name, Continent, Region, SurfaceArea, IndepYear, Population, LifeExpectancy, GNP, GNPOld, LocalName, GovernmentForm, HeadOfState, Capital, Code2)
  countrylanguage(CountryCode, Language, IsOfficial, Percentage)
```

### `wta_1`
```
  matches(best_of, draw_size, loser_age, loser_entry, loser_hand, loser_ht, loser_id, loser_ioc, loser_name, loser_rank, loser_rank_points, loser_seed, match_num, minutes, round, score, surface, tourney_date, tourney_id, tourney_level, tourney_name, winner_age, winner_entry, winner_hand, winner_ht, winner_id, winner_ioc, winner_name, winner_rank, winner_rank_points, winner_seed, year)
  players(player_id, first_name, last_name, hand, birth_date, country_code)
  rankings(ranking_date, ranking, player_id, ranking_points, tours)
```
