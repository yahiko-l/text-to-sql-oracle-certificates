# Semantic audit dossier: weak-correct, strong-wrong answers

Built 2026-09-06. Population definition: top class of the single-instance partition whose representative the weak oracle accepts and the strong oracle rejects.

521 such answers across 12 pools (6096 answers examined) collapse to 240 distinct (question, returned SQL) cases over 99 questions. Every case in the population was judged: this is a census, not a sample.

In every case the gold and the returned query agree on the shipped benchmark database and disagree on at least one instance of the distilled test suite. The comparator is the official `result_eq`, called with the gold first, and whether row order is compared is a property of the gold, as in the frozen analyser.

`instances disagreeing` counts suite instances where the two queries differ. A difference on one instance out of fifty and a difference on all of them are very different evidence, so the count is given for every case.


## Cases

### C001  (question 4, database `concert_singer`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303, omnisql-32b/seed101, omnisql-32b/seed202, omnisql-32b/seed303
- Class mass: 48/50, 50/50, 49/50, 47/50, 44/50, 42/50
- Instances disagreeing: 3 of 32 (9%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What are the names and release years for all the songs of the youngest singer?

**Gold.**
```sql
SELECT song_name ,  song_release_year FROM singer ORDER BY age LIMIT 1
```

**Returned.**
```sql
SELECT Song_Name, Song_release_year
FROM singer
WHERE Age = (SELECT MIN(Age) FROM singer)
```

**First disagreeing instance** `concert_singerv515patch4.sqlite`.

Gold returns 1 row(s), 2 column(s):

    Hey | %Hey%

Returned query gives 2 row(s), 2 column(s):

    Hey | %Hey%
    Love | lKJ)2AjFjp

Difference: gold_subset_of_rep; 1 row(s) in common, 0 only in the gold, 1 only in the returned result.

### C002  (question 15, database `concert_singer`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202
- Class mass: 43/50, 37/50
- Instances disagreeing: 17 of 32 (53%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Show the stadium name and capacity with most number of concerts in  2014 or after.

**Gold.**
```sql
SELECT T2.name ,  T2.capacity FROM concert AS T1 JOIN stadium AS T2 ON T1.stadium_id  =  T2.stadium_id WHERE T1.year  >=  2014 GROUP BY T2.stadium_id ORDER BY count(*) DESC LIMIT 1
```

**Returned.**
```sql
SELECT T2.Name, T2.Capacity
FROM concert AS T1
INNER JOIN stadium AS T2 ON T1.Stadium_ID = T2.Stadium_ID
WHERE T1.Year >= 2014
GROUP BY T2.Name, T2.Capacity
ORDER BY COUNT(T1.concert_ID) DESC
LIMIT 1
```

**First disagreeing instance** `concert_singerv5083.sqlite`.

Gold returns 1 row(s), 2 column(s):

    mpr5T0V | 2600364897

Returned query gives 1 row(s), 2 column(s):

    Bayview Stadium | 19

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C003  (question 16, database `concert_singer`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed303
- Class mass: 48/50, 49/49
- Instances disagreeing: 7 of 32 (22%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What is the name and capacity of the stadium  with the most concerts after 2013?

**Gold.**
```sql
select t2.name ,  t2.capacity from concert as t1 join stadium as t2 on t1.stadium_id  =  t2.stadium_id where t1.year  >  2013 group by t2.stadium_id order by count(*) desc limit 1
```

**Returned.**
```sql
SELECT T2.Name, T2.Capacity
FROM concert AS T1
INNER JOIN stadium AS T2 ON T1.Stadium_ID = T2.Stadium_ID
WHERE T1.Year > '2013'
GROUP BY T1.Stadium_ID
ORDER BY COUNT(T1.concert_ID) DESC
LIMIT 1
```

**First disagreeing instance** `concert_singertest0.sqlite`.

Gold returns 1 row(s), 2 column(s):

    0 | 0

Returned query gives 1 row(s), 2 column(s):

    20 | 8774077902

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C004  (question 20, database `concert_singer`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303, kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303, omnisql-32b/seed101, omnisql-32b/seed303
- Class mass: 50/50, 50/50, 49/50, 49/50, 50/50, 50/50, 46/50, 49/50
- Instances disagreeing: 29 of 32 (91%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Show names for all stadiums except for stadiums having a concert in  2014.

**Gold.**
```sql
SELECT name FROM stadium EXCEPT SELECT T2.name FROM concert AS T1 JOIN stadium AS T2 ON T1.stadium_id  =  T2.stadium_id WHERE T1.year  =  2014
```

**Returned.**
```sql
SELECT Name
FROM stadium
WHERE Stadium_ID NOT IN (
    SELECT Stadium_ID
    FROM concert
    WHERE Year = '2014'
)
```

**First disagreeing instance** `concert_singertest0.sqlite`.

Gold returns 14 row(s), 1 column(s):

    )uFP
    03RZUfj(bwx UE
    19
    2h52O0
    Be(
    Recreation Par
    RvI8xFrance
    V2z20hJn
    cmrzmn3fEIv4v2)r
    kHG1vmsN
    lJojzlh5tVtfoa)
    mC
    ... (14 rows total)

Returned query gives 38 row(s), 1 column(s):

    Recreation Park
    20
    2
    20
    France
    Glebe Park
    2
    Recreation Park
    2h52O0
    0
    2
    )uFP
    ... (38 rows total)

Difference: gold_subset_of_rep; 14 row(s) in common, 0 only in the gold, 9 only in the returned result.

### C005  (question 21, database `concert_singer`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303, kwai-autosql-14b/seed202, omnisql-32b/seed101, omnisql-32b/seed202, omnisql-32b/seed303
- Class mass: 50/50, 50/50, 50/50, 49/50, 44/50, 44/50, 45/50
- Instances disagreeing: 29 of 32 (91%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the names of all stadiums that did not have a concert in 2014?

**Gold.**
```sql
SELECT name FROM stadium EXCEPT SELECT T2.name FROM concert AS T1 JOIN stadium AS T2 ON T1.stadium_id  =  T2.stadium_id WHERE T1.year  =  2014
```

**Returned.**
```sql
SELECT Name
FROM stadium
WHERE Stadium_ID NOT IN (
    SELECT Stadium_ID
    FROM concert
    WHERE Year = '2014'
)
```

**First disagreeing instance** `concert_singertest0.sqlite`.

Gold returns 14 row(s), 1 column(s):

    )uFP
    03RZUfj(bwx UE
    19
    2h52O0
    Be(
    Recreation Par
    RvI8xFrance
    V2z20hJn
    cmrzmn3fEIv4v2)r
    kHG1vmsN
    lJojzlh5tVtfoa)
    mC
    ... (14 rows total)

Returned query gives 38 row(s), 1 column(s):

    Recreation Park
    20
    2
    20
    France
    Glebe Park
    2
    Recreation Park
    2h52O0
    0
    2
    )uFP
    ... (38 rows total)

Difference: gold_subset_of_rep; 14 row(s) in common, 0 only in the gold, 9 only in the returned result.

### C006  (question 22, database `concert_singer`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303, kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Class mass: 50/50, 50/50, 50/50, 50/50, 50/50, 50/50
- Instances disagreeing: 23 of 32 (72%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Show the name and theme for all concerts and the number of singers in each.

**Gold.**
```sql
SELECT T2.concert_name ,  T2.theme ,  count(*) FROM singer_in_concert AS T1 JOIN concert AS T2 ON T1.concert_id  =  T2.concert_id GROUP BY T2.concert_id
```

**Returned.**
```sql
SELECT T1.concert_Name, T1.Theme, COUNT(T2.Singer_ID) AS num_singers
FROM concert AS T1
INNER JOIN singer_in_concert AS T2 ON T1.concert_ID = T2.concert_ID
GROUP BY T1.concert_Name, T1.Theme
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

### C007  (question 23, database `concert_singer`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303
- Class mass: 50/50, 50/50, 50/50
- Instances disagreeing: 29 of 32 (91%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** List singer names and number of concerts for each person.

**Gold.**
```sql
SELECT T2.name ,  count(*) FROM singer_in_concert AS T1 JOIN singer AS T2 ON T1.singer_id  =  T2.singer_id GROUP BY T2.singer_id
```

**Returned.**
```sql
SELECT T1.Name, COUNT(T2.concert_ID) AS number_of_concerts
FROM singer AS T1
INNER JOIN singer_in_concert AS T2 ON T1.Singer_ID = T2.Singer_ID
GROUP BY T1.Name
```

**First disagreeing instance** `concert_singertest0.sqlite`.

Gold returns 105 row(s), 2 column(s):

    19 | 2
    Rose White | 1
    2 | 1
    TRcZXxHKP | 1
    IDpR8 | 1
    19 | 3
    20 | 3
    France | 1
    l1Ua98Vy | 1
    K | 2
    0 | 1
    Timbaland | 1
    ... (105 rows total)

Returned query gives 45 row(s), 2 column(s):

     | 4
    0 | 9
    0Yjt87 | 2
    1 | 8
    19 | 10
    19ky90n | 1
    2 | 4
    20 | 13
    21 | 3
    2tN | 2
    5 | 3
    5c  | 2
    ... (45 rows total)

Difference: values differ; 34 row(s) in common, 26 only in the gold, 11 only in the returned result.

### C008  (question 24, database `concert_singer`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303, kwai-autosql-14b/seed101, kwai-autosql-14b/seed303
- Class mass: 48/49, 48/50, 50/50, 50/50, 50/50
- Instances disagreeing: 29 of 32 (91%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the names and number of concerts for each person?

**Gold.**
```sql
SELECT T2.name ,  count(*) FROM singer_in_concert AS T1 JOIN singer AS T2 ON T1.singer_id  =  T2.singer_id GROUP BY T2.singer_id
```

**Returned.**
```sql
SELECT T1.Name, COUNT(T2.concert_ID) AS number_of_concerts
FROM singer AS T1
INNER JOIN singer_in_concert AS T2 ON T1.Singer_ID = T2.Singer_ID
GROUP BY T1.Name
```

**First disagreeing instance** `concert_singertest0.sqlite`.

Gold returns 105 row(s), 2 column(s):

    19 | 2
    Rose White | 1
    2 | 1
    TRcZXxHKP | 1
    IDpR8 | 1
    19 | 3
    20 | 3
    France | 1
    l1Ua98Vy | 1
    K | 2
    0 | 1
    Timbaland | 1
    ... (105 rows total)

Returned query gives 45 row(s), 2 column(s):

     | 4
    0 | 9
    0Yjt87 | 2
    1 | 8
    19 | 10
    19ky90n | 1
    2 | 4
    20 | 13
    21 | 3
    2tN | 2
    5 | 3
    5c  | 2
    ... (45 rows total)

Difference: values differ; 34 row(s) in common, 26 only in the gold, 11 only in the returned result.

### C009  (question 35, database `pets_1`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303, kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303, omnisql-32b/seed101, omnisql-32b/seed202, omnisql-32b/seed303
- Class mass: 50/50, 50/50, 50/50, 50/50, 50/50, 50/50, 50/50, 50/50, 50/50
- Instances disagreeing: 22 of 27 (81%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Find the weight of the youngest dog.

**Gold.**
```sql
SELECT weight FROM pets ORDER BY pet_age LIMIT 1
```

**Returned.**
```sql
SELECT weight
FROM Pets
WHERE PetType = 'dog'
ORDER BY pet_age ASC
LIMIT 1
```

**First disagreeing instance** `pets_1v5080.sqlite`.

Gold returns 1 row(s), 1 column(s):

    10.0

Returned query gives 1 row(s), 1 column(s):

    9.0

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C010  (question 36, database `pets_1`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303, kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303, omnisql-32b/seed101, omnisql-32b/seed202, omnisql-32b/seed303
- Class mass: 50/50, 50/50, 50/50, 50/50, 50/50, 50/50, 50/50, 50/50, 50/50
- Instances disagreeing: 22 of 27 (81%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** How much does the youngest dog weigh?

**Gold.**
```sql
SELECT weight FROM pets ORDER BY pet_age LIMIT 1
```

**Returned.**
```sql
SELECT weight
FROM Pets
WHERE PetType = 'dog'
ORDER BY pet_age ASC
LIMIT 1
```

**First disagreeing instance** `pets_1v5080.sqlite`.

Gold returns 1 row(s), 1 column(s):

    10.0

Returned query gives 1 row(s), 1 column(s):

    9.0

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C011  (question 43, database `pets_1`)

- Returned by: kwai-autosql-32b/seed101
- Class mass: 50/50
- Instances disagreeing: 23 of 27 (85%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find the name of students who have both cat and dog.

**Gold.**
```sql
select t1.fname from student as t1 join has_pet as t2 on t1.stuid  =  t2.stuid join pets as t3 on t3.petid  =  t2.petid where t3.pettype  =  'cat' intersect select t1.fname from student as t1 join has_pet as t2 on t1.stuid  =  t2.stuid join pets as t3 on t3.petid  =  t2.petid where t3.pettype  =  'dog'
```

**Returned.**
```sql
SELECT T1.Fname, T1.LName
FROM Student AS T1
INNER JOIN Has_Pet AS T2 ON T1.StuID = T2.StuID
INNER JOIN Pets AS T3 ON T2.PetID = T3.PetID
WHERE T3.PetType IN ('cat', 'dog')
GROUP BY T1.StuID, T1.Fname, T1.LName
HAVING COUNT(DISTINCT T3.PetType) = 2
```

**First disagreeing instance** `pets_1v5080.sqlite`.

Gold returns 5 row(s), 1 column(s):

    0
    003
    10
    David
    Oy01U(d

Returned query gives 4 row(s), 2 column(s):

    Oy01U(d | AilCTbfL
    David | Linda
    003 | 10
    0 | 9

Difference: col_count_differs, disjoint; 0 row(s) in common, 5 only in the gold, 4 only in the returned result.

### C012  (question 44, database `pets_1`)

- Returned by: kwai-autosql-32b/seed101
- Class mass: 50/50
- Instances disagreeing: 20 of 27 (74%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the students' first names who have both cats and dogs?

**Gold.**
```sql
SELECT T1.Fname FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid  =  T2.stuid JOIN pets AS T3 ON T3.petid  =  T2.petid WHERE T3.pettype  =  'cat' INTERSECT SELECT T1.Fname FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid  =  T2.stuid JOIN pets AS T3 ON T3.petid  =  T2.petid WHERE T3.pettype  =  'dog'
```

**Returned.**
```sql
SELECT T1.Fname
FROM Student AS T1
INNER JOIN Has_Pet AS T2 ON T1.StuID = T2.StuID
INNER JOIN Pets AS T3 ON T2.PetID = T3.PetID
WHERE T3.PetType IN ('cat', 'dog')
GROUP BY T1.StuID
HAVING COUNT(DISTINCT T3.PetType) = 2
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

### C013  (question 69, database `car_1`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303, kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Class mass: 50/50, 50/50, 50/50, 50/50, 50/50, 50/50
- Instances disagreeing: 42 of 60 (70%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Which of the nations has the most car makers? List the country name.

**Gold.**
```sql
SELECT T2.CountryName FROM CAR_MAKERS AS T1 JOIN COUNTRIES AS T2 ON T1.Country  =  T2.CountryId GROUP BY T1.Country ORDER BY Count(*) DESC LIMIT 1;
```

**Returned.**
```sql
SELECT T2.CountryName
FROM car_makers AS T1
INNER JOIN countries AS T2 ON T1.Country = T2.CountryId
GROUP BY T2.CountryName
ORDER BY COUNT(T1.Id) DESC
LIMIT 1
```

**First disagreeing instance** `car_1v5080.sqlite`.

Gold returns 1 row(s), 1 column(s):

    us

Returned query gives 1 row(s), 1 column(s):

    asia

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C014  (question 70, database `car_1`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303, kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Class mass: 49/49, 50/50, 50/50, 50/50, 50/50, 50/50
- Instances disagreeing: 42 of 60 (70%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What is the name of the nation with the most car makers?

**Gold.**
```sql
SELECT T2.CountryName FROM CAR_MAKERS AS T1 JOIN COUNTRIES AS T2 ON T1.Country  =  T2.CountryId GROUP BY T1.Country ORDER BY Count(*) DESC LIMIT 1;
```

**Returned.**
```sql
SELECT T2.CountryName
FROM car_makers AS T1
INNER JOIN countries AS T2 ON T1.Country = T2.CountryId
GROUP BY T2.CountryName
ORDER BY COUNT(T1.Id) DESC
LIMIT 1
```

**First disagreeing instance** `car_1v5080.sqlite`.

Gold returns 1 row(s), 1 column(s):

    us

Returned query gives 1 row(s), 1 column(s):

    asia

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C015  (question 71, database `car_1`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202
- Class mass: 49/50, 45/50
- Instances disagreeing: 57 of 60 (95%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** How many car models are produced by each manufacturer? List the count and the maker full name.

**Gold.**
```sql
select count(*) ,  t2.fullname from model_list as t1 join car_makers as t2 on t1.maker  =  t2.id group by t2.id;
```

**Returned.**
```sql
SELECT T1.FullName, COUNT(T2.Model) AS ModelCount
FROM car_makers AS T1
INNER JOIN model_list AS T2 ON T1.Id = T2.Maker
GROUP BY T1.FullName
```

**First disagreeing instance** `car_1v5080.sqlite`.

Gold returns 32 row(s), 2 column(s):

    1 | WgId2j2tiOKXNbJE)
    1 | 19.0
    1 | 4
    1 | 3
    1 | 5
    1 | eugeaut
    2 | ER5Km8gHv9Mtc9w6Jlv
    1 | General Motors
    2 | JS8WGkUpkQNRnwpw
    1 | 9
    2 | 151
    1 | fia
    ... (32 rows total)

Returned query gives 28 row(s), 2 column(s):

     | 3
    0qSpYywiWEZMmhE9zCeNGcUo5Y | 2
    0xIjVZ | 1
    1 | 1
    151 | 2
    19.0 | 1
    1975 | 1
    3 | 2
    3499 | 1
    4 | 1
    4000N1f3g | 1
    5 | 3
    ... (28 rows total)

Difference: disjoint; 0 row(s) in common, 30 only in the gold, 28 only in the returned result.

### C016  (question 90, database `car_1`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303, kwai-autosql-14b/seed303
- Class mass: 39/49, 31/50, 33/50, 19/50
- Instances disagreeing: 18 of 60 (30%)
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
INNER JOIN model_list AS T2 ON T1.Id = T2.Maker
INNER JOIN car_names AS T4 ON T2.Model = T4.Model
INNER JOIN cars_data AS T3 ON T4.MakeId = T3.Id
WHERE T1.Maker = 'volvo'
```

**First disagreeing instance** `car_1v50811.sqlite`.

Gold returns 1 row(s), 1 column(s):

    NULL

Returned query gives 1 row(s), 1 column(s):

    436889768.3333333

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C017  (question 91, database `car_1`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202
- Class mass: 39/50, 35/50
- Instances disagreeing: 18 of 60 (30%)
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
INNER JOIN car_names AS T4 ON T2.Model = T4.Model
INNER JOIN cars_data AS T3 ON T4.MakeId = T3.Id
WHERE T1.Maker = 'volvo'
```

**First disagreeing instance** `car_1v50811.sqlite`.

Gold returns 1 row(s), 1 column(s):

    NULL

Returned query gives 1 row(s), 1 column(s):

    436889768.3333333

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C018  (question 103, database `car_1`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303
- Class mass: 36/49, 36/50, 29/50
- Instances disagreeing: 17 of 60 (28%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** For  volvo, how many cylinders does the car with the least accelerate have?

**Gold.**
```sql
SELECT T1.cylinders FROM CARS_DATA AS T1 JOIN CAR_NAMES AS T2 ON T1.Id  =  T2.MakeId WHERE T2.Model  =  'volvo' ORDER BY T1.accelerate ASC LIMIT 1;
```

**Returned.**
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

**First disagreeing instance** `car_1v50811.sqlite`.

Gold returns 0 row(s), None column(s):

    (no rows)

Returned query gives 1 row(s), 1 column(s):

    1969

Difference: gold_empty; 0 row(s) in common, 0 only in the gold, 1 only in the returned result.

### C019  (question 104, database `car_1`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303, kwai-autosql-14b/seed101
- Class mass: 45/50, 41/50, 44/50, 23/50
- Instances disagreeing: 17 of 60 (28%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** For a volvo , how many cylinders does the version with least accelerate have?

**Gold.**
```sql
SELECT T1.cylinders FROM CARS_DATA AS T1 JOIN CAR_NAMES AS T2 ON T1.Id  =  T2.MakeId WHERE T2.Model  =  'volvo' ORDER BY T1.accelerate ASC LIMIT 1;
```

**Returned.**
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

**First disagreeing instance** `car_1v50811.sqlite`.

Gold returns 0 row(s), None column(s):

    (no rows)

Returned query gives 1 row(s), 1 column(s):

    1969

Difference: gold_empty; 0 row(s) in common, 0 only in the gold, 1 only in the returned result.

### C020  (question 111, database `car_1`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303, kwai-autosql-14b/seed202
- Class mass: 49/50, 48/50, 49/50, 47/50
- Instances disagreeing: 20 of 60 (33%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the id and names of the countries which have more than 3 car makers or produce the 'fiat' ?

**Gold.**
```sql
SELECT T1.countryId ,  T1.CountryName FROM Countries AS T1 JOIN CAR_MAKERS AS T2 ON T1.CountryId  =  T2.Country GROUP BY T1.countryId HAVING count(*)  >  3 UNION SELECT T1.countryId ,  T1.CountryName FROM Countries AS T1 JOIN CAR_MAKERS AS T2 ON T1.CountryId  =  T2.Country JOIN MODEL_LIST AS T3 ON T2.Id  =  T3.Maker WHERE T3.Model  =  'fiat';
```

**Returned.**
```sql
SELECT T1.CountryId, T1.CountryName
FROM countries AS T1
INNER JOIN car_makers AS T2 ON T1.CountryId = T2.Country
GROUP BY T1.CountryId, T1.CountryName
HAVING COUNT(T2.Id) > 3 OR SUM(CASE WHEN T2.Maker = 'fiat' THEN 1 ELSE 0 END) > 0
```

**First disagreeing instance** `car_1v5080.sqlite`.

Gold returns 8 row(s), 2 column(s):

    -4076741865 | us
    10 | Om
    12 | 400
    19 | ford
    151 | buick
    1981 | asia
    8210699449 | 3499
    9236429507 | mc

Returned query gives 9 row(s), 2 column(s):

    -4076741865 | us
    10 | Om
    12 | 400
    19 | ford
    151 | buick
    1969 | france
    1981 | asia
    8210699449 | 3499
    9236429507 | mc

Difference: gold_subset_of_rep; 8 row(s) in common, 0 only in the gold, 1 only in the returned result.

### C021  (question 112, database `car_1`)

- Returned by: kwai-autosql-32b/seed101
- Class mass: 50/50
- Instances disagreeing: 20 of 60 (33%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the ids and names of all countries that either have more than 3 car makers or produce fiats?

**Gold.**
```sql
select t1.countryid ,  t1.countryname from countries as t1 join car_makers as t2 on t1.countryid  =  t2.country group by t1.countryid having count(*)  >  3 union select t1.countryid ,  t1.countryname from countries as t1 join car_makers as t2 on t1.countryid  =  t2.country join model_list as t3 on t2.id  =  t3.maker where t3.model  =  'fiat';
```

**Returned.**
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

**First disagreeing instance** `car_1v5080.sqlite`.

Gold returns 8 row(s), 2 column(s):

    -4076741865 | us
    10 | Om
    12 | 400
    19 | ford
    151 | buick
    1981 | asia
    8210699449 | 3499
    9236429507 | mc

Returned query gives 9 row(s), 2 column(s):

    -4076741865 | us
    10 | Om
    12 | 400
    19 | ford
    151 | buick
    1981 | asia
    8210699449 | 3499
    9236429507 | mc
    1969 | france

Difference: gold_subset_of_rep; 8 row(s) in common, 0 only in the gold, 1 only in the returned result.

### C022  (question 139, database `flight_2`)

- Returned by: kwai-autosql-32b/seed101
- Class mass: 50/50
- Instances disagreeing: 4 of 56 (7%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** How many flights does 'JetBlue Airways' have?

**Gold.**
```sql
SELECT count(*) FROM FLIGHTS AS T1 JOIN AIRLINES AS T2 ON T1.Airline  =  T2.uid WHERE T2.Airline = "JetBlue Airways"
```

**Returned.**
```sql
SELECT COUNT(*) FROM flights WHERE Airline = (SELECT uid FROM airlines WHERE Airline = 'JetBlue Airways')
```

**First disagreeing instance** `flight_2v50810.sqlite`.

Gold returns 1 row(s), 1 column(s):

    9

Returned query gives 1 row(s), 1 column(s):

    0

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C023  (question 153, database `flight_2`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303
- Class mass: 49/50, 50/50, 50/50
- Instances disagreeing: 5 of 56 (9%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find all airlines that have flights from 'CVO' but not from 'APG'.

**Gold.**
```sql
SELECT T1.Airline FROM AIRLINES AS T1 JOIN FLIGHTS AS T2 ON T1.uid  =  T2.Airline WHERE T2.SourceAirport  =  "CVO" EXCEPT SELECT T1.Airline FROM AIRLINES AS T1 JOIN FLIGHTS AS T2 ON T1.uid  =  T2.Airline WHERE T2.SourceAirport  =  "APG"
```

**Returned.**
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

**First disagreeing instance** `flight_2v5081.sqlite`.

Gold returns 4 row(s), 1 column(s):

    ABR
    SNA
    Virgin America
    hitlDDelta Airlines

Returned query gives 5 row(s), 1 column(s):

    SNA
    ABR
    hitlDDelta Airlines
    SNA
    Virgin America

Difference: duplicate_multiplicity_only; 4 row(s) in common, 0 only in the gold, 0 only in the returned result.

### C024  (question 154, database `flight_2`)

- Returned by: kwai-autosql-32b/seed101
- Class mass: 50/50
- Instances disagreeing: 5 of 56 (9%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Which airlines have departures from CVO but not from APG?

**Gold.**
```sql
SELECT T1.Airline FROM AIRLINES AS T1 JOIN FLIGHTS AS T2 ON T1.uid  =  T2.Airline WHERE T2.SourceAirport  =  "CVO" EXCEPT SELECT T1.Airline FROM AIRLINES AS T1 JOIN FLIGHTS AS T2 ON T1.uid  =  T2.Airline WHERE T2.SourceAirport  =  "APG"
```

**Returned.**
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

**First disagreeing instance** `flight_2v5081.sqlite`.

Gold returns 4 row(s), 1 column(s):

    ABR
    SNA
    Virgin America
    hitlDDelta Airlines

Returned query gives 5 row(s), 1 column(s):

    SNA
    ABR
    hitlDDelta Airlines
    SNA
    Virgin America

Difference: duplicate_multiplicity_only; 4 row(s) in common, 0 only in the gold, 0 only in the returned result.

### C025  (question 189, database `course_teach`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202
- Class mass: 50/50, 49/50
- Instances disagreeing: 24 of 25 (96%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** List the names of teachers from youngest to oldest.

**Gold.**
```sql
SELECT Name FROM teacher ORDER BY Age ASC
```

**Returned.**
```sql
SELECT Name
FROM teacher
ORDER BY CAST(Age AS INTEGER) ASC
```

**First disagreeing instance** `course_teachv5080.sqlite`.

Gold returns 101 row(s), 1 column(s):

    33
    Mat
    xuZxhgnG
    o SWtT  V
    34
    3
    Math
    Vicente Carretero
    Little Lever Urban Distric
    j
    0
    Anne Walker
    ... (101 rows total)

Returned query gives 101 row(s), 1 column(s):

    o SWtT  V
    1
    02qjTn
    KVXZNgZG(F
    0
    31
    33
    Anne Walker
    33
    Math
    Fe
    xuZxhgnG
    ... (101 rows total)

Difference: row_order_only; 48 row(s) in common, 0 only in the gold, 0 only in the returned result.

### C026  (question 195, database `course_teach`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303
- Class mass: 50/50, 50/50, 50/50
- Instances disagreeing: 18 of 25 (72%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What is the hometown of the youngest teacher?

**Gold.**
```sql
SELECT Hometown FROM teacher ORDER BY Age ASC LIMIT 1
```

**Returned.**
```sql
SELECT Hometown
FROM teacher
ORDER BY CAST(Age AS INTEGER) ASC
LIMIT 1
```

**First disagreeing instance** `course_teachv5080.sqlite`.

Gold returns 1 row(s), 1 column(s):

    ftXIphiAAPya

Returned query gives 1 row(s), 1 column(s):

    3

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C027  (question 246, database `wta_1`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303, kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303, omnisql-32b/seed101, omnisql-32b/seed202, omnisql-32b/seed303
- Class mass: 46/50, 46/50, 48/50, 49/50, 50/50, 48/50, 40/50, 37/50, 38/50
- Instances disagreeing: 15 of 33 (45%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Find the name and rank of the 3 youngest victors across all matches.

**Gold.**
```sql
SELECT DISTINCT winner_name ,  winner_rank FROM matches ORDER BY winner_age LIMIT 3
```

**Returned.**
```sql
SELECT winner_name, winner_rank
FROM matches
ORDER BY winner_age ASC
LIMIT 3
```

**First disagreeing instance** `wta_1v5083.sqlite`.

Gold returns 3 row(s), 2 column(s):

    GW9xB39 | 2438785513
    3499 | 24
    Elina Svitolina | 39

Returned query gives 3 row(s), 2 column(s):

    9 | 15
    GW9xB39 | 2438785513
    3499 | 24

Difference: values differ; 2 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C028  (question 247, database `wta_1`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303, kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303, omnisql-32b/seed101, omnisql-32b/seed202, omnisql-32b/seed303
- Class mass: 47/50, 47/50, 45/50, 50/50, 50/50, 49/50, 39/50, 33/50, 40/50
- Instances disagreeing: 15 of 33 (45%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What are the names and ranks of the three youngest victors across all matches?

**Gold.**
```sql
SELECT DISTINCT winner_name ,  winner_rank FROM matches ORDER BY winner_age LIMIT 3
```

**Returned.**
```sql
SELECT winner_name, winner_rank
FROM matches
ORDER BY winner_age ASC
LIMIT 3
```

**First disagreeing instance** `wta_1v5083.sqlite`.

Gold returns 3 row(s), 2 column(s):

    GW9xB39 | 2438785513
    3499 | 24
    Elina Svitolina | 39

Returned query gives 3 row(s), 2 column(s):

    9 | 15
    GW9xB39 | 2438785513
    3499 | 24

Difference: values differ; 2 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C029  (question 248, database `wta_1`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303, kwai-autosql-14b/seed101
- Class mass: 50/50, 50/50, 50/50, 50/50
- Instances disagreeing: 2 of 33 (6%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** How many different winners both participated in the WTA Championships and were left handed?

**Gold.**
```sql
SELECT count(DISTINCT winner_name) FROM matches WHERE tourney_name  =  'WTA Championships' AND winner_hand  =  'L'
```

**Returned.**
```sql
SELECT COUNT(DISTINCT winner_id)
FROM matches
WHERE tourney_name = 'WTA Championships'
  AND winner_hand = 'L'
```

**First disagreeing instance** `wta_1v5085.sqlite`.

Gold returns 1 row(s), 1 column(s):

    6

Returned query gives 1 row(s), 1 column(s):

    7

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C030  (question 254, database `battle_death`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303, kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Class mass: 50/50, 50/50, 48/50, 48/50, 48/50, 44/49
- Instances disagreeing: 17 of 28 (61%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Show names, results and bulgarian commanders of the battles with no ships lost in the 'English Channel'.

**Gold.**
```sql
SELECT name ,  RESULT ,  bulgarian_commander FROM battle EXCEPT SELECT T1.name ,  T1.result ,  T1.bulgarian_commander FROM battle AS T1 JOIN ship AS T2 ON T1.id  =  T2.lost_in_battle WHERE T2.location  =  'English Channel'
```

**Returned.**
```sql
SELECT name, result, bulgarian_commander
FROM battle
WHERE id NOT IN (
    SELECT lost_in_battle
    FROM ship
    WHERE location = 'English Channel'
)
```

**First disagreeing instance** `battle_deathv5083735.sqlite`.

Gold returns 217 row(s), 3 column(s):

     | (HQyWVu58Kg | oY7KaloyanbWa
     | East% | Kaloyan
     | USYHTLatin victory | Unknown
     nqqY0tt4ldRt | East | EPs%East%lSA
    %East% | Brig | jT43P3Q
    %East% | Bulgarian victory | 
    %East% | East | Brig
    %East% | Latin victory | %East%
    %East% | Latin victory | t
    %East% | Pp1t(Ub | %East%
    %East% | Two Year Truce | Brig
    %East% | Two Year Truce | Unknown
    ... (217 rows total)

Returned query gives 225 row(s), 3 column(s):

    Battle of Adrianople | Bulgarian victory | Kaloyan
    East | wo Year Truce | Kaloyan
    Battle of Adrianople | t | East
    ymM7A | Bulgarian victory | East
    East | Eas | RezWT
    zr4Battle of SerresA 3 | 3Cm96bVBQ0GUb | Kaloyan
    Battle of Boruy | Bulgarian victory | Kaloyan
    Battle of Adrianople | Bulgarian victory | (Pf
    Battle of Messinopolis | Brig | Kaloyan
    ZNp1 7dlN 0aKhDewen2w)y( | 0 da)sqf4Q D8s4 | bNCKaloyang6y
    Brig | Latin victory | L0I)
    RNQOdgPlRkGEFZLdQbw | Latin victory | jG3 Bgh
    ... (225 rows total)

Difference: duplicate_multiplicity_only; 217 row(s) in common, 0 only in the gold, 0 only in the returned result.

### C031  (question 267, database `student_transcripts_tracking`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202
- Class mass: 48/50, 46/50
- Instances disagreeing: 39 of 55 (71%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What is the id, line 1, and line 2 of the place with the most students?

**Gold.**
```sql
SELECT T1.address_id ,  T1.line_1 ,  T1.line_2 FROM Addresses AS T1 JOIN Students AS T2 ON T1.address_id  =  T2.current_address_id GROUP BY T1.address_id ORDER BY count(*) DESC LIMIT 1
```

**Returned.**
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

**First disagreeing instance** `student_transcripts_trackingv5080.sqlite`.

Gold returns 1 row(s), 3 column(s):

    9700166583 | 10 | 6

Returned query gives 1 row(s), 3 column(s):

    2368373983 | wc | O))1ebd

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C032  (question 307, database `tvshow`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Class mass: 50/50, 50/50, 50/50, 50/50
- Instances disagreeing: 11 of 25 (44%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** which countries' tv channels are playing some cartoon  Todd Casey writes?

**Gold.**
```sql
SELECT T1.country FROM TV_Channel AS T1 JOIN cartoon AS T2 ON T1.id = T2.Channel WHERE T2.written_by  =  'Todd Casey'
```

**Returned.**
```sql
SELECT DISTINCT T1.Country
FROM TV_Channel AS T1
INNER JOIN Cartoon AS T2 ON T1.id = T2.Channel
WHERE T2.Written_by = 'Todd Casey'
```

**First disagreeing instance** `tvshowv5081.sqlite`.

Gold returns 8 row(s), 1 column(s):

    Todd Casey neY1
    Italy
    Todd Casey
    Italy
    yes
    Italy
    zk9GuItaly
    Italy

Returned query gives 5 row(s), 1 column(s):

    Todd Casey neY1
    Italy
    Todd Casey
    yes
    zk9GuItaly

Difference: duplicate_multiplicity_only; 5 row(s) in common, 0 only in the gold, 0 only in the returned result.

### C033  (question 308, database `tvshow`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed303
- Class mass: 50/50, 50/50
- Instances disagreeing: 11 of 25 (44%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the countries that have cartoons on TV that Todd Casey writes?

**Gold.**
```sql
SELECT T1.country FROM TV_Channel AS T1 JOIN cartoon AS T2 ON T1.id = T2.Channel WHERE T2.written_by  =  'Todd Casey'
```

**Returned.**
```sql
SELECT DISTINCT T2.Country
FROM Cartoon AS T1
INNER JOIN TV_Channel AS T2 ON T1.Channel = T2.id
WHERE T1.Written_by = 'Todd Casey'
```

**First disagreeing instance** `tvshowv5081.sqlite`.

Gold returns 8 row(s), 1 column(s):

    Todd Casey neY1
    Italy
    Todd Casey
    Italy
    yes
    Italy
    zk9GuItaly
    Italy

Returned query gives 5 row(s), 1 column(s):

    Todd Casey neY1
    Italy
    Todd Casey
    yes
    zk9GuItaly

Difference: duplicate_multiplicity_only; 5 row(s) in common, 0 only in the gold, 0 only in the returned result.

### C034  (question 344, database `world_1`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303
- Class mass: 50/50, 50/50, 50/50
- Instances disagreeing: 17 of 46 (37%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Which language is the most popular in Aruba?

**Gold.**
```sql
SELECT T2.Language FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code  =  T2.CountryCode WHERE T1.Name  =  "Aruba" ORDER BY Percentage DESC LIMIT 1
```

**Returned.**
```sql
SELECT Language
FROM countrylanguage
WHERE CountryCode = (
    SELECT Code FROM country WHERE Name = 'Aruba'
)
ORDER BY Percentage DESC
LIMIT 1
```

**First disagreeing instance** `world_1v5082.sqlite`.

Gold returns 1 row(s), 1 column(s):

    Spanish

Returned query gives 1 row(s), 1 column(s):

    159999

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C035  (question 366, database `world_1`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202
- Class mass: 50/50, 50/50
- Instances disagreeing: 26 of 46 (57%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the total number of languages used in Aruba?

**Gold.**
```sql
SELECT COUNT(T2.Language) FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code  =  T2.CountryCode WHERE T1.Name  =  "Aruba"
```

**Returned.**
```sql
SELECT COUNT(*) FROM countrylanguage WHERE CountryCode = (SELECT Code FROM country WHERE Name = 'Aruba')
```

**First disagreeing instance** `world_1v50811.sqlite`.

Gold returns 1 row(s), 1 column(s):

    33

Returned query gives 1 row(s), 1 column(s):

    15

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C036  (question 367, database `world_1`)

- Returned by: kwai-autosql-32b/seed101
- Class mass: 50/50
- Instances disagreeing: 26 of 46 (57%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** How many languages are spoken in Aruba?

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

### C037  (question 368, database `world_1`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303
- Class mass: 50/50, 49/50, 50/50
- Instances disagreeing: 3 of 46 (7%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** How many official languages does Afghanistan have?

**Gold.**
```sql
SELECT COUNT(*) FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code  =  T2.CountryCode WHERE T1.Name  =  "Afghanistan" AND IsOfficial  =  "T"
```

**Returned.**
```sql
SELECT COUNT(*) FROM countrylanguage WHERE CountryCode = 'AFG' AND IsOfficial = 'T'
```

**First disagreeing instance** `world_1v50811.sqlite`.

Gold returns 1 row(s), 1 column(s):

    1

Returned query gives 1 row(s), 1 column(s):

    0

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C038  (question 369, database `world_1`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303
- Class mass: 50/50, 50/50, 50/50
- Instances disagreeing: 3 of 46 (7%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** How many official languages are spoken in Afghanistan?

**Gold.**
```sql
SELECT COUNT(*) FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code  =  T2.CountryCode WHERE T1.Name  =  "Afghanistan" AND IsOfficial  =  "T"
```

**Returned.**
```sql
SELECT COUNT(*) FROM countrylanguage WHERE CountryCode = 'AFG' AND IsOfficial = 'T'
```

**First disagreeing instance** `world_1v50811.sqlite`.

Gold returns 1 row(s), 1 column(s):

    1

Returned query gives 1 row(s), 1 column(s):

    0

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C039  (question 375, database `world_1`)

- Returned by: kwai-autosql-32b/seed101
- Class mass: 50/50
- Instances disagreeing: 9 of 46 (20%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Give the names of nations that speak both English and French.

**Gold.**
```sql
SELECT T1.Name FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code  =  T2.CountryCode WHERE T2.Language  =  "English" INTERSECT SELECT T1.Name FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code  =  T2.CountryCode WHERE T2.Language  =  "French"
```

**Returned.**
```sql
SELECT T1.Name
FROM country AS T1
INNER JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode AND T2.Language = 'English'
INNER JOIN countrylanguage AS T3 ON T1.Code = T3.CountryCode AND T3.Language = 'French'
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

### C040  (question 391, database `world_1`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303
- Class mass: 40/50, 32/50, 34/50
- Instances disagreeing: 9 of 46 (20%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Give the mean life expectancy of countries in which English is not officially spoken .

**Gold.**
```sql
SELECT avg(LifeExpectancy) FROM country WHERE Name NOT IN (SELECT T1.Name FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code  =  T2.CountryCode WHERE T2.Language  =  "English" AND T2.IsOfficial  =  "T")
```

**Returned.**
```sql
SELECT AVG(LifeExpectancy)
FROM country
WHERE Code NOT IN (
    SELECT CountryCode
    FROM countrylanguage
    WHERE Language = 'English' AND IsOfficial = 'T'
)
```

**First disagreeing instance** `world_1v50816.sqlite`.

Gold returns 1 row(s), 1 column(s):

    31606.90900321543

Returned query gives 1 row(s), 1 column(s):

    31473.299524564183

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C041  (question 392, database `world_1`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed303
- Class mass: 48/50, 50/50
- Instances disagreeing: 39 of 46 (85%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the total number of people living in the nations that do not use English?

**Gold.**
```sql
SELECT sum(Population) FROM country WHERE Name NOT IN (SELECT T1.Name FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code  =  T2.CountryCode WHERE T2.Language  =  "English")
```

**Returned.**
```sql
SELECT SUM(T1.Population) AS TotalPopulation
FROM country AS T1
WHERE T1.Code NOT IN (
    SELECT CountryCode
    FROM countrylanguage
    WHERE Language = 'English'
)
```

**First disagreeing instance** `world_1v5080.sqlite`.

Gold returns 1 row(s), 1 column(s):

    268945194457

Returned query gives 1 row(s), 1 column(s):

    273514308785

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C042  (question 393, database `world_1`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303
- Class mass: 49/50, 49/50, 50/50
- Instances disagreeing: 39 of 46 (85%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** How many people live in countries that do not speak English?

**Gold.**
```sql
SELECT sum(Population) FROM country WHERE Name NOT IN (SELECT T1.Name FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code  =  T2.CountryCode WHERE T2.Language  =  "English")
```

**Returned.**
```sql
SELECT SUM(T1.Population) AS TotalPopulation
FROM country AS T1
WHERE T1.Code NOT IN (
    SELECT CountryCode
    FROM countrylanguage
    WHERE Language = 'English'
)
```

**First disagreeing instance** `world_1v5080.sqlite`.

Gold returns 1 row(s), 1 column(s):

    268945194457

Returned query gives 1 row(s), 1 column(s):

    273514308785

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C043  (question 429, database `world_1`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303
- Class mass: 49/50, 47/50, 49/50
- Instances disagreeing: 38 of 46 (83%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the cities who have more than 160000 people and less than 900000 people?

**Gold.**
```sql
SELECT name FROM city WHERE Population BETWEEN 160000 AND 900000
```

**Returned.**
```sql
SELECT Name
FROM city
WHERE Population > 160000 AND Population < 900000
```

**First disagreeing instance** `world_1v5080.sqlite`.

Gold returns 3 row(s), 1 column(s):

    vsgTbpN
    Jql900001MwW
    930

Returned query gives 1 row(s), 1 column(s):

    Jql900001MwW

Difference: rep_subset_of_gold; 1 row(s) in common, 2 only in the gold, 0 only in the returned result.

### C044  (question 457, database `network_1`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed303
- Class mass: 50/50, 50/50
- Instances disagreeing: 22 of 29 (76%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** How many friends does Kyle have?

**Gold.**
```sql
SELECT count(*) FROM Friend AS T1 JOIN Highschooler AS T2 ON T1.student_id  =  T2.id WHERE T2.name  =  "Kyle"
```

**Returned.**
```sql
SELECT COUNT(*) FROM Friend WHERE student_id = (SELECT ID FROM Highschooler WHERE name = 'Kyle')
```

**First disagreeing instance** `network_1v5080.sqlite`.

Gold returns 1 row(s), 1 column(s):

    19

Returned query gives 1 row(s), 1 column(s):

    1

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C045  (question 458, database `network_1`)

- Returned by: kwai-autosql-32b/seed101
- Class mass: 50/50
- Instances disagreeing: 22 of 29 (76%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Count the number of friends Kyle has.

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

### C046  (question 459, database `network_1`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303
- Class mass: 50/50, 50/50, 50/50
- Instances disagreeing: 24 of 29 (83%)
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
WHERE liked_id = (SELECT ID FROM Highschooler WHERE name = 'Kyle')
```

**First disagreeing instance** `network_1v5080.sqlite`.

Gold returns 1 row(s), 1 column(s):

    21

Returned query gives 1 row(s), 1 column(s):

    4

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C047  (question 460, database `network_1`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303
- Class mass: 50/50, 50/50, 50/50
- Instances disagreeing: 24 of 29 (83%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Return the number of likes Kyle has.

**Gold.**
```sql
SELECT count(*) FROM Likes AS T1 JOIN Highschooler AS T2 ON T1.student_id  =  T2.id WHERE T2.name  =  "Kyle"
```

**Returned.**
```sql
SELECT COUNT(*)
FROM Likes
WHERE liked_id = (SELECT ID FROM Highschooler WHERE name = 'Kyle')
```

**First disagreeing instance** `network_1v5080.sqlite`.

Gold returns 1 row(s), 1 column(s):

    21

Returned query gives 1 row(s), 1 column(s):

    4

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C048  (question 468, database `dog_kennels`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303, kwai-autosql-14b/seed303
- Class mass: 50/50, 50/50, 50/50, 48/50
- Instances disagreeing: 22 of 48 (46%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Which person has the most dogs? List the id, first name and last name.

**Gold.**
```sql
SELECT T1.owner_id ,  T2.first_name ,  T2.last_name FROM Dogs AS T1 JOIN Owners AS T2 ON T1.owner_id  =  T2.owner_id GROUP BY T1.owner_id ORDER BY count(*) DESC LIMIT 1
```

**Returned.**
```sql
SELECT T1.owner_id, T1.first_name, T1.last_name
FROM Owners AS T1
INNER JOIN Dogs AS T2 ON T1.owner_id = T2.owner_id
GROUP BY T1.owner_id, T1.first_name, T1.last_name
ORDER BY COUNT(T2.dog_id) DESC
LIMIT 1
```

**First disagreeing instance** `dog_kennelsv5080.sqlite`.

Gold returns 1 row(s), 3 column(s):

    7994075702 | 501 | qwM)4Jaclyn

Returned query gives 1 row(s), 3 column(s):

    999 | bPG%West%CRw | 0

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C049  (question 469, database `dog_kennels`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303, kwai-autosql-14b/seed202
- Class mass: 50/50, 50/50, 50/50, 47/50
- Instances disagreeing: 22 of 48 (46%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Return the id, first name and last name of the person who has the most dogs.

**Gold.**
```sql
SELECT T1.owner_id ,  T2.first_name ,  T2.last_name FROM Dogs AS T1 JOIN Owners AS T2 ON T1.owner_id  =  T2.owner_id GROUP BY T1.owner_id ORDER BY count(*) DESC LIMIT 1
```

**Returned.**
```sql
SELECT T1.owner_id, T1.first_name, T1.last_name
FROM Owners AS T1
INNER JOIN Dogs AS T2 ON T1.owner_id = T2.owner_id
GROUP BY T1.owner_id, T1.first_name, T1.last_name
ORDER BY COUNT(T2.dog_id) DESC
LIMIT 1
```

**First disagreeing instance** `dog_kennelsv5080.sqlite`.

Gold returns 1 row(s), 3 column(s):

    7994075702 | 501 | qwM)4Jaclyn

Returned query gives 1 row(s), 3 column(s):

    999 | bPG%West%CRw | 0

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C050  (question 472, database `dog_kennels`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed303, kwai-autosql-14b/seed101, kwai-autosql-14b/seed303
- Class mass: 49/50, 50/50, 50/50, 50/50
- Instances disagreeing: 15 of 48 (31%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What is the description of the treatment type that is the cheapest overall?

**Gold.**
```sql
SELECT T1.treatment_type_description FROM Treatment_types AS T1 JOIN Treatments AS T2 ON T1.treatment_type_code  =  T2.treatment_type_code GROUP BY T1.treatment_type_code ORDER BY sum(cost_of_treatment) ASC LIMIT 1
```

**Returned.**
```sql
SELECT T1.treatment_type_description
FROM Treatment_Types AS T1
INNER JOIN Treatments AS T2 ON T1.treatment_type_code = T2.treatment_type_code
ORDER BY T2.cost_of_treatment ASC
LIMIT 1
```

**First disagreeing instance** `dog_kennelsv5081.sqlite`.

Gold returns 1 row(s), 1 column(s):

    QOY2(500

Returned query gives 1 row(s), 1 column(s):

    2

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C051  (question 473, database `dog_kennels`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Class mass: 50/50, 50/50, 50/50, 50/50, 50/50
- Instances disagreeing: 15 of 48 (31%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Give me the description of the treatment type that is least expensive.

**Gold.**
```sql
SELECT T1.treatment_type_description FROM Treatment_types AS T1 JOIN Treatments AS T2 ON T1.treatment_type_code  =  T2.treatment_type_code GROUP BY T1.treatment_type_code ORDER BY sum(cost_of_treatment) ASC LIMIT 1
```

**Returned.**
```sql
SELECT T1.treatment_type_description
FROM Treatment_Types AS T1
INNER JOIN Treatments AS T2 ON T1.treatment_type_code = T2.treatment_type_code
ORDER BY T2.cost_of_treatment ASC
LIMIT 1
```

**First disagreeing instance** `dog_kennelsv5081.sqlite`.

Gold returns 1 row(s), 1 column(s):

    QOY2(500

Returned query gives 1 row(s), 1 column(s):

    2

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C052  (question 474, database `dog_kennels`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303
- Class mass: 39/48, 42/50, 40/50
- Instances disagreeing: 1 of 48 (2%)
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
INNER JOIN Treatments AS T3 ON T2.dog_id = T3.dog_id
GROUP BY T1.owner_id, T1.zip_code
ORDER BY SUM(T3.cost_of_treatment) DESC
LIMIT 1
```

**First disagreeing instance** `dog_kennelsv508557.sqlite`.

Gold returns 1 row(s), 2 column(s):

    3501605851 | %West%

Returned query gives 1 row(s), 2 column(s):

    348300858 | 90RK2Uq

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C053  (question 475, database `dog_kennels`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303
- Class mass: 49/50, 49/50, 47/50
- Instances disagreeing: 1 of 48 (2%)
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
INNER JOIN Treatments AS T3 ON T2.dog_id = T3.dog_id
GROUP BY T1.owner_id, T1.zip_code
ORDER BY SUM(T3.cost_of_treatment) DESC
LIMIT 1
```

**First disagreeing instance** `dog_kennelsv508557.sqlite`.

Gold returns 1 row(s), 2 column(s):

    3501605851 | %West%

Returned query gives 1 row(s), 2 column(s):

    348300858 | 90RK2Uq

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C054  (question 484, database `dog_kennels`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303, kwai-autosql-14b/seed101
- Class mass: 23/49, 33/50, 31/50, 49/50
- Instances disagreeing: 47 of 48 (98%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** How many dogs younger than average?

**Gold.**
```sql
SELECT count(*) FROM Dogs WHERE age  <  ( SELECT avg(age) FROM Dogs )
```

**Returned.**
```sql
SELECT COUNT(*)
FROM Dogs
WHERE CAST(age AS INTEGER) < (SELECT AVG(CAST(age AS INTEGER)) FROM Dogs)
```

**First disagreeing instance** `dog_kennelsv5080.sqlite`.

Gold returns 1 row(s), 1 column(s):

    43

Returned query gives 1 row(s), 1 column(s):

    86

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C055  (question 485, database `dog_kennels`)

- Returned by: kwai-autosql-32b/seed101, kwai-autosql-32b/seed202, kwai-autosql-32b/seed303, kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Class mass: 26/50, 30/50, 33/50, 47/50, 48/50, 49/50
- Instances disagreeing: 47 of 48 (98%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Count the number of dogs that are younger than the average.

**Gold.**
```sql
SELECT count(*) FROM Dogs WHERE age  <  ( SELECT avg(age) FROM Dogs )
```

**Returned.**
```sql
SELECT COUNT(*)
FROM Dogs
WHERE CAST(age AS INTEGER) < (SELECT AVG(CAST(age AS INTEGER)) FROM Dogs)
```

**First disagreeing instance** `dog_kennelsv5080.sqlite`.

Gold returns 1 row(s), 1 column(s):

    43

Returned query gives 1 row(s), 1 column(s):

    86

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C056  (question 29, database `concert_singer`)

- Returned by: kwai-autosql-32b/seed202
- Class mass: 49/49
- Instances disagreeing: 1 of 32 (3%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find the name and location of the stadiums which some concerts happened in both 2014 and 2015.

**Gold.**
```sql
SELECT T2.name ,  T2.location FROM concert AS T1 JOIN stadium AS T2 ON T1.stadium_id  =  T2.stadium_id WHERE T1.Year  =  2014 INTERSECT SELECT T2.name ,  T2.location FROM concert AS T1 JOIN stadium AS T2 ON T1.stadium_id  =  T2.stadium_id WHERE T1.Year  =  2015
```

**Returned.**
```sql
SELECT T1.Name, T1.Location
FROM stadium AS T1
WHERE T1.Stadium_ID IN (
    SELECT Stadium_ID FROM concert WHERE Year = '2014'
    INTERSECT
    SELECT Stadium_ID FROM concert WHERE Year = '2015'
)
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

### C057  (question 43, database `pets_1`)

- Returned by: kwai-autosql-32b/seed202
- Class mass: 50/50
- Instances disagreeing: 23 of 27 (85%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find the name of students who have both cat and dog.

**Gold.**
```sql
select t1.fname from student as t1 join has_pet as t2 on t1.stuid  =  t2.stuid join pets as t3 on t3.petid  =  t2.petid where t3.pettype  =  'cat' intersect select t1.fname from student as t1 join has_pet as t2 on t1.stuid  =  t2.stuid join pets as t3 on t3.petid  =  t2.petid where t3.pettype  =  'dog'
```

**Returned.**
```sql
SELECT T1.Fname, T1.LName
FROM Student AS T1
INNER JOIN Has_Pet AS T2 ON T1.StuID = T2.StuID
INNER JOIN Pets AS T3 ON T2.PetID = T3.PetID
WHERE T3.PetType IN ('cat', 'dog')
GROUP BY T1.Fname, T1.LName
HAVING COUNT(DISTINCT T3.PetType) = 2
```

**First disagreeing instance** `pets_1v5080.sqlite`.

Gold returns 5 row(s), 1 column(s):

    0
    003
    10
    David
    Oy01U(d

Returned query gives 4 row(s), 2 column(s):

    0 | 9
    003 | 10
    David | Linda
    Oy01U(d | AilCTbfL

Difference: col_count_differs, disjoint; 0 row(s) in common, 5 only in the gold, 4 only in the returned result.

### C058  (question 44, database `pets_1`)

- Returned by: kwai-autosql-32b/seed202, kwai-autosql-32b/seed303
- Class mass: 50/50, 50/50
- Instances disagreeing: 20 of 27 (74%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the students' first names who have both cats and dogs?

**Gold.**
```sql
SELECT T1.Fname FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid  =  T2.stuid JOIN pets AS T3 ON T3.petid  =  T2.petid WHERE T3.pettype  =  'cat' INTERSECT SELECT T1.Fname FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid  =  T2.stuid JOIN pets AS T3 ON T3.petid  =  T2.petid WHERE T3.pettype  =  'dog'
```

**Returned.**
```sql
SELECT T1.Fname
FROM Student AS T1
INNER JOIN Has_Pet AS T2 ON T1.StuID = T2.StuID
INNER JOIN Pets AS T3 ON T2.PetID = T3.PetID
GROUP BY T1.StuID, T1.Fname
HAVING SUM(CASE WHEN T3.PetType = 'cat' THEN 1 ELSE 0 END) > 0
   AND SUM(CASE WHEN T3.PetType = 'dog' THEN 1 ELSE 0 END) > 0
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

### C059  (question 112, database `car_1`)

- Returned by: kwai-autosql-32b/seed202
- Class mass: 49/50
- Instances disagreeing: 20 of 60 (33%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the ids and names of all countries that either have more than 3 car makers or produce fiats?

**Gold.**
```sql
select t1.countryid ,  t1.countryname from countries as t1 join car_makers as t2 on t1.countryid  =  t2.country group by t1.countryid having count(*)  >  3 union select t1.countryid ,  t1.countryname from countries as t1 join car_makers as t2 on t1.countryid  =  t2.country join model_list as t3 on t2.id  =  t3.maker where t3.model  =  'fiat';
```

**Returned.**
```sql
SELECT CountryId, CountryName
FROM countries
WHERE CountryId IN (
    SELECT Country
    FROM car_makers
    GROUP BY Country
    HAVING COUNT(Id) > 3
    UNION
    SELECT Country
    FROM car_makers
    WHERE Maker = 'fiat'
)
```

**First disagreeing instance** `car_1v5080.sqlite`.

Gold returns 8 row(s), 2 column(s):

    -4076741865 | us
    10 | Om
    12 | 400
    19 | ford
    151 | buick
    1981 | asia
    8210699449 | 3499
    9236429507 | mc

Returned query gives 9 row(s), 2 column(s):

    -4076741865 | us
    10 | Om
    12 | 400
    19 | ford
    151 | buick
    1969 | france
    1981 | asia
    8210699449 | 3499
    9236429507 | mc

Difference: gold_subset_of_rep; 8 row(s) in common, 0 only in the gold, 1 only in the returned result.

### C060  (question 154, database `flight_2`)

- Returned by: kwai-autosql-32b/seed202
- Class mass: 50/50
- Instances disagreeing: 5 of 56 (9%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Which airlines have departures from CVO but not from APG?

**Gold.**
```sql
SELECT T1.Airline FROM AIRLINES AS T1 JOIN FLIGHTS AS T2 ON T1.uid  =  T2.Airline WHERE T2.SourceAirport  =  "CVO" EXCEPT SELECT T1.Airline FROM AIRLINES AS T1 JOIN FLIGHTS AS T2 ON T1.uid  =  T2.Airline WHERE T2.SourceAirport  =  "APG"
```

**Returned.**
```sql
SELECT T1.Airline
FROM airlines AS T1
INNER JOIN flights AS T2 ON T1.uid = T2.Airline
WHERE T2.SourceAirport = 'CVO'
AND T1.uid NOT IN (
    SELECT Airline FROM flights WHERE SourceAirport = 'APG'
)
```

**First disagreeing instance** `flight_2v5081.sqlite`.

Gold returns 4 row(s), 1 column(s):

    ABR
    SNA
    Virgin America
    hitlDDelta Airlines

Returned query gives 5 row(s), 1 column(s):

    SNA
    ABR
    hitlDDelta Airlines
    SNA
    Virgin America

Difference: duplicate_multiplicity_only; 4 row(s) in common, 0 only in the gold, 0 only in the returned result.

### C061  (question 190, database `course_teach`)

- Returned by: kwai-autosql-32b/seed202, kwai-autosql-32b/seed303
- Class mass: 50/50, 50/50
- Instances disagreeing: 24 of 25 (96%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What are the names of the teachers  from youngest to oldest?

**Gold.**
```sql
SELECT Name FROM teacher ORDER BY Age ASC
```

**Returned.**
```sql
SELECT Name
FROM teacher
ORDER BY CAST(Age AS INTEGER) ASC
```

**First disagreeing instance** `course_teachv5080.sqlite`.

Gold returns 101 row(s), 1 column(s):

    33
    Mat
    xuZxhgnG
    o SWtT  V
    34
    3
    Math
    Vicente Carretero
    Little Lever Urban Distric
    j
    0
    Anne Walker
    ... (101 rows total)

Returned query gives 101 row(s), 1 column(s):

    o SWtT  V
    1
    02qjTn
    KVXZNgZG(F
    0
    31
    33
    Anne Walker
    33
    Math
    Fe
    xuZxhgnG
    ... (101 rows total)

Difference: row_order_only; 48 row(s) in common, 0 only in the gold, 0 only in the returned result.

### C062  (question 196, database `course_teach`)

- Returned by: kwai-autosql-32b/seed202, kwai-autosql-32b/seed303
- Class mass: 50/50, 50/50
- Instances disagreeing: 18 of 25 (72%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Where is the youngest teacher from?

**Gold.**
```sql
SELECT Hometown FROM teacher ORDER BY Age ASC LIMIT 1
```

**Returned.**
```sql
SELECT Hometown
FROM teacher
ORDER BY CAST(Age AS INTEGER) ASC
LIMIT 1
```

**First disagreeing instance** `course_teachv5080.sqlite`.

Gold returns 1 row(s), 1 column(s):

    ftXIphiAAPya

Returned query gives 1 row(s), 1 column(s):

    3

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C063  (question 253, database `battle_death`)

- Returned by: kwai-autosql-32b/seed202, kwai-autosql-32b/seed303
- Class mass: 46/50, 43/50
- Instances disagreeing: 16 of 28 (57%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** List the name and date the battle that has lost  Lettice and HMS Atalanta

**Gold.**
```sql
SELECT T1.name ,  T1.date FROM battle AS T1 JOIN ship AS T2 ON T1.id  =  T2.lost_in_battle WHERE T2.name  =  'Lettice' INTERSECT SELECT T1.name ,  T1.date FROM battle AS T1 JOIN ship AS T2 ON T1.id  =  T2.lost_in_battle WHERE T2.name  =  'HMS Atalanta'
```

**Returned.**
```sql
SELECT DISTINCT T1.name, T1.date
FROM battle AS T1
INNER JOIN ship AS T2 ON T1.id = T2.lost_in_battle
WHERE T2.name IN ('Lettice', 'HMS Atalanta')
```

**First disagreeing instance** `battle_deathv5080.sqlite`.

Gold returns 0 row(s), None column(s):

    (no rows)

Returned query gives 11 row(s), 2 column(s):

    1SjnDEnglish Channel | Boril
    %East% | TKJ
    hZDqJBattle of Serres | %East%
    5VU7TUgfOgqy79 | X
    Baldwin I | 1235
    English Channe | C1pIqw(
    2 | 2
    Kaloyan | English Channel
    224 | 8zV0f11
    June 1205 | vSDpp0WuPy51oJz5
    Battle of Boruy | June 1205

Difference: gold_empty; 0 row(s) in common, 0 only in the gold, 11 only in the returned result.

### C064  (question 307, database `tvshow`)

- Returned by: kwai-autosql-32b/seed202, kwai-autosql-32b/seed303
- Class mass: 50/50, 50/50
- Instances disagreeing: 11 of 25 (44%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** which countries' tv channels are playing some cartoon  Todd Casey writes?

**Gold.**
```sql
SELECT T1.country FROM TV_Channel AS T1 JOIN cartoon AS T2 ON T1.id = T2.Channel WHERE T2.written_by  =  'Todd Casey'
```

**Returned.**
```sql
SELECT DISTINCT T2.Country
FROM Cartoon AS T1
INNER JOIN TV_Channel AS T2 ON T1.Channel = T2.id
WHERE T1.Written_by = 'Todd Casey'
```

**First disagreeing instance** `tvshowv5081.sqlite`.

Gold returns 8 row(s), 1 column(s):

    Todd Casey neY1
    Italy
    Todd Casey
    Italy
    yes
    Italy
    zk9GuItaly
    Italy

Returned query gives 5 row(s), 1 column(s):

    Todd Casey neY1
    Italy
    Todd Casey
    yes
    zk9GuItaly

Difference: duplicate_multiplicity_only; 5 row(s) in common, 0 only in the gold, 0 only in the returned result.

### C065  (question 308, database `tvshow`)

- Returned by: kwai-autosql-32b/seed202, kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Class mass: 50/50, 50/50, 50/50, 50/50
- Instances disagreeing: 11 of 25 (44%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the countries that have cartoons on TV that Todd Casey writes?

**Gold.**
```sql
SELECT T1.country FROM TV_Channel AS T1 JOIN cartoon AS T2 ON T1.id = T2.Channel WHERE T2.written_by  =  'Todd Casey'
```

**Returned.**
```sql
SELECT DISTINCT T1.Country
FROM TV_Channel AS T1
INNER JOIN Cartoon AS T2 ON T1.id = T2.Channel
WHERE T2.Written_by = 'Todd Casey'
```

**First disagreeing instance** `tvshowv5081.sqlite`.

Gold returns 8 row(s), 1 column(s):

    Todd Casey neY1
    Italy
    Todd Casey
    Italy
    yes
    Italy
    zk9GuItaly
    Italy

Returned query gives 5 row(s), 1 column(s):

    Todd Casey neY1
    Italy
    Todd Casey
    yes
    zk9GuItaly

Difference: duplicate_multiplicity_only; 5 row(s) in common, 0 only in the gold, 0 only in the returned result.

### C066  (question 367, database `world_1`)

- Returned by: kwai-autosql-32b/seed202, kwai-autosql-32b/seed303
- Class mass: 50/50, 50/50
- Instances disagreeing: 26 of 46 (57%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** How many languages are spoken in Aruba?

**Gold.**
```sql
SELECT COUNT(T2.Language) FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code  =  T2.CountryCode WHERE T1.Name  =  "Aruba"
```

**Returned.**
```sql
SELECT COUNT(*) FROM countrylanguage WHERE CountryCode = (SELECT Code FROM country WHERE Name = 'Aruba')
```

**First disagreeing instance** `world_1v50811.sqlite`.

Gold returns 1 row(s), 1 column(s):

    33

Returned query gives 1 row(s), 1 column(s):

    15

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C067  (question 392, database `world_1`)

- Returned by: kwai-autosql-32b/seed202
- Class mass: 50/50
- Instances disagreeing: 39 of 46 (85%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the total number of people living in the nations that do not use English?

**Gold.**
```sql
SELECT sum(Population) FROM country WHERE Name NOT IN (SELECT T1.Name FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code  =  T2.CountryCode WHERE T2.Language  =  "English")
```

**Returned.**
```sql
SELECT SUM(Population) AS TotalPopulation
FROM country
WHERE Code NOT IN (
    SELECT CountryCode
    FROM countrylanguage
    WHERE Language = 'English'
)
```

**First disagreeing instance** `world_1v5080.sqlite`.

Gold returns 1 row(s), 1 column(s):

    268945194457

Returned query gives 1 row(s), 1 column(s):

    273514308785

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C068  (question 458, database `network_1`)

- Returned by: kwai-autosql-32b/seed202, kwai-autosql-32b/seed303
- Class mass: 50/50, 50/50
- Instances disagreeing: 22 of 29 (76%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Count the number of friends Kyle has.

**Gold.**
```sql
SELECT count(*) FROM Friend AS T1 JOIN Highschooler AS T2 ON T1.student_id  =  T2.id WHERE T2.name  =  "Kyle"
```

**Returned.**
```sql
SELECT COUNT(*) FROM Friend WHERE student_id = (SELECT ID FROM Highschooler WHERE name = 'Kyle')
```

**First disagreeing instance** `network_1v5080.sqlite`.

Gold returns 1 row(s), 1 column(s):

    19

Returned query gives 1 row(s), 1 column(s):

    1

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C069  (question 472, database `dog_kennels`)

- Returned by: kwai-autosql-32b/seed202, kwai-autosql-14b/seed202
- Class mass: 50/50, 50/50
- Instances disagreeing: 15 of 48 (31%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What is the description of the treatment type that is the cheapest overall?

**Gold.**
```sql
SELECT T1.treatment_type_description FROM Treatment_types AS T1 JOIN Treatments AS T2 ON T1.treatment_type_code  =  T2.treatment_type_code GROUP BY T1.treatment_type_code ORDER BY sum(cost_of_treatment) ASC LIMIT 1
```

**Returned.**
```sql
SELECT T2.treatment_type_description
FROM Treatments AS T1
INNER JOIN Treatment_Types AS T2 ON T1.treatment_type_code = T2.treatment_type_code
ORDER BY T1.cost_of_treatment ASC
LIMIT 1
```

**First disagreeing instance** `dog_kennelsv5081.sqlite`.

Gold returns 1 row(s), 1 column(s):

    QOY2(500

Returned query gives 1 row(s), 1 column(s):

    2

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C070  (question 15, database `concert_singer`)

- Returned by: kwai-autosql-32b/seed303
- Class mass: 43/50
- Instances disagreeing: 17 of 32 (53%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Show the stadium name and capacity with most number of concerts in  2014 or after.

**Gold.**
```sql
SELECT T2.name ,  T2.capacity FROM concert AS T1 JOIN stadium AS T2 ON T1.stadium_id  =  T2.stadium_id WHERE T1.year  >=  2014 GROUP BY T2.stadium_id ORDER BY count(*) DESC LIMIT 1
```

**Returned.**
```sql
SELECT T2.Name, T2.Capacity
FROM concert AS T1
INNER JOIN stadium AS T2 ON T1.Stadium_ID = T2.Stadium_ID
WHERE T1.Year >= 2014
GROUP BY T2.Name, T2.Capacity
ORDER BY COUNT(*) DESC
LIMIT 1
```

**First disagreeing instance** `concert_singerv5083.sqlite`.

Gold returns 1 row(s), 2 column(s):

    mpr5T0V | 2600364897

Returned query gives 1 row(s), 2 column(s):

    Bayview Stadium | 19

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C071  (question 43, database `pets_1`)

- Returned by: kwai-autosql-32b/seed303
- Class mass: 50/50
- Instances disagreeing: 23 of 27 (85%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find the name of students who have both cat and dog.

**Gold.**
```sql
select t1.fname from student as t1 join has_pet as t2 on t1.stuid  =  t2.stuid join pets as t3 on t3.petid  =  t2.petid where t3.pettype  =  'cat' intersect select t1.fname from student as t1 join has_pet as t2 on t1.stuid  =  t2.stuid join pets as t3 on t3.petid  =  t2.petid where t3.pettype  =  'dog'
```

**Returned.**
```sql
SELECT T1.Fname, T1.LName
FROM Student AS T1
INNER JOIN Has_Pet AS T2 ON T1.StuID = T2.StuID
INNER JOIN Pets AS T3 ON T2.PetID = T3.PetID
GROUP BY T1.StuID, T1.Fname, T1.LName
HAVING SUM(CASE WHEN T3.PetType = 'cat' THEN 1 ELSE 0 END) > 0
   AND SUM(CASE WHEN T3.PetType = 'dog' THEN 1 ELSE 0 END) > 0
```

**First disagreeing instance** `pets_1v5080.sqlite`.

Gold returns 5 row(s), 1 column(s):

    0
    003
    10
    David
    Oy01U(d

Returned query gives 4 row(s), 2 column(s):

    Oy01U(d | AilCTbfL
    David | Linda
    003 | 10
    0 | 9

Difference: col_count_differs, disjoint; 0 row(s) in common, 5 only in the gold, 4 only in the returned result.

### C072  (question 71, database `car_1`)

- Returned by: kwai-autosql-32b/seed303
- Class mass: 44/50
- Instances disagreeing: 57 of 60 (95%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** How many car models are produced by each manufacturer? List the count and the maker full name.

**Gold.**
```sql
select count(*) ,  t2.fullname from model_list as t1 join car_makers as t2 on t1.maker  =  t2.id group by t2.id;
```

**Returned.**
```sql
SELECT T1.FullName, COUNT(T2.Model)
FROM car_makers AS T1
INNER JOIN model_list AS T2 ON T1.Id = T2.Maker
GROUP BY T1.FullName
```

**First disagreeing instance** `car_1v5080.sqlite`.

Gold returns 32 row(s), 2 column(s):

    1 | WgId2j2tiOKXNbJE)
    1 | 19.0
    1 | 4
    1 | 3
    1 | 5
    1 | eugeaut
    2 | ER5Km8gHv9Mtc9w6Jlv
    1 | General Motors
    2 | JS8WGkUpkQNRnwpw
    1 | 9
    2 | 151
    1 | fia
    ... (32 rows total)

Returned query gives 28 row(s), 2 column(s):

     | 3
    0qSpYywiWEZMmhE9zCeNGcUo5Y | 2
    0xIjVZ | 1
    1 | 1
    151 | 2
    19.0 | 1
    1975 | 1
    3 | 2
    3499 | 1
    4 | 1
    4000N1f3g | 1
    5 | 3
    ... (28 rows total)

Difference: disjoint; 0 row(s) in common, 30 only in the gold, 28 only in the returned result.

### C073  (question 91, database `car_1`)

- Returned by: kwai-autosql-32b/seed303
- Class mass: 37/50
- Instances disagreeing: 18 of 60 (30%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the average edispl for all volvos?

**Gold.**
```sql
SELECT avg(T2.edispl) FROM CAR_NAMES AS T1 JOIN CARS_DATA AS T2 ON T1.MakeId  =  T2.Id WHERE T1.Model  =  'volvo';
```

**Returned.**
```sql
SELECT AVG(T3.Edispl) AS AverageEdispl
FROM car_makers AS T1
INNER JOIN model_list AS T2 ON T1.Id = T2.Maker
INNER JOIN car_names AS T4 ON T2.Model = T4.Model
INNER JOIN cars_data AS T3 ON T4.MakeId = T3.Id
WHERE T1.Maker = 'volvo'
```

**First disagreeing instance** `car_1v50811.sqlite`.

Gold returns 1 row(s), 1 column(s):

    NULL

Returned query gives 1 row(s), 1 column(s):

    436889768.3333333

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C074  (question 112, database `car_1`)

- Returned by: kwai-autosql-32b/seed303
- Class mass: 47/50
- Instances disagreeing: 20 of 60 (33%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the ids and names of all countries that either have more than 3 car makers or produce fiats?

**Gold.**
```sql
select t1.countryid ,  t1.countryname from countries as t1 join car_makers as t2 on t1.countryid  =  t2.country group by t1.countryid having count(*)  >  3 union select t1.countryid ,  t1.countryname from countries as t1 join car_makers as t2 on t1.countryid  =  t2.country join model_list as t3 on t2.id  =  t3.maker where t3.model  =  'fiat';
```

**Returned.**
```sql
SELECT T1.CountryId, T1.CountryName
FROM countries AS T1
INNER JOIN car_makers AS T2 ON T1.CountryId = T2.Country
GROUP BY T1.CountryId, T1.CountryName
HAVING COUNT(T2.Id) > 3 OR SUM(CASE WHEN T2.Maker = 'fiat' THEN 1 ELSE 0 END) > 0
```

**First disagreeing instance** `car_1v5080.sqlite`.

Gold returns 8 row(s), 2 column(s):

    -4076741865 | us
    10 | Om
    12 | 400
    19 | ford
    151 | buick
    1981 | asia
    8210699449 | 3499
    9236429507 | mc

Returned query gives 9 row(s), 2 column(s):

    -4076741865 | us
    10 | Om
    12 | 400
    19 | ford
    151 | buick
    1969 | france
    1981 | asia
    8210699449 | 3499
    9236429507 | mc

Difference: gold_subset_of_rep; 8 row(s) in common, 0 only in the gold, 1 only in the returned result.

### C075  (question 156, database `flight_2`)

- Returned by: kwai-autosql-32b/seed303
- Class mass: 50/50
- Instances disagreeing: 6 of 56 (11%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Which flight numbers correspond to United Airlines flights?

**Gold.**
```sql
SELECT T1.FlightNo FROM FLIGHTS AS T1 JOIN AIRLINES AS T2 ON T2.uid  =  T1.Airline WHERE T2.Airline  =  "United Airlines"
```

**Returned.**
```sql
SELECT FlightNo
FROM flights
WHERE Airline = (SELECT uid FROM airlines WHERE Airline = 'United Airlines')
```

**First disagreeing instance** `flight_2v50812.sqlite`.

Gold returns 22 row(s), 1 column(s):

    -5913650171
    4
    199
    200
    201
    490
    491
    828
    829
    875
    876
    1593237617
    ... (22 rows total)

Returned query gives 14 row(s), 1 column(s):

    -5913650171
    4
    199
    200
    201
    490
    491
    828
    829
    875
    876
    1593237617
    ... (14 rows total)

Difference: rep_subset_of_gold; 14 row(s) in common, 5 only in the gold, 0 only in the returned result.

### C076  (question 267, database `student_transcripts_tracking`)

- Returned by: kwai-autosql-32b/seed303, kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Class mass: 46/50, 46/50, 44/50, 47/50
- Instances disagreeing: 31 of 55 (56%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What is the id, line 1, and line 2 of the place with the most students?

**Gold.**
```sql
SELECT T1.address_id ,  T1.line_1 ,  T1.line_2 FROM Addresses AS T1 JOIN Students AS T2 ON T1.address_id  =  T2.current_address_id GROUP BY T1.address_id ORDER BY count(*) DESC LIMIT 1
```

**Returned.**
```sql
SELECT T1.address_id, T1.line_1, T1.line_2
FROM Addresses AS T1
INNER JOIN Students AS T2 ON T1.address_id = T2.current_address_id
GROUP BY T1.address_id, T1.line_1, T1.line_2
ORDER BY COUNT(T2.student_id) DESC
LIMIT 1
```

**First disagreeing instance** `student_transcripts_trackingv5080.sqlite`.

Gold returns 1 row(s), 3 column(s):

    9700166583 | 10 | 6

Returned query gives 1 row(s), 3 column(s):

    -7035591255 | 09700166582 | Apt. 335

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C077  (question 345, database `world_1`)

- Returned by: kwai-autosql-32b/seed303
- Class mass: 44/50
- Instances disagreeing: 17 of 46 (37%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What language is predominantly spoken in Aruba?

**Gold.**
```sql
SELECT T2.Language FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code  =  T2.CountryCode WHERE T1.Name  =  "Aruba" ORDER BY Percentage DESC LIMIT 1
```

**Returned.**
```sql
SELECT Language
FROM countrylanguage
WHERE CountryCode = (
    SELECT Code FROM country WHERE Name = 'Aruba'
)
ORDER BY Percentage DESC
LIMIT 1
```

**First disagreeing instance** `world_1v5082.sqlite`.

Gold returns 1 row(s), 1 column(s):

    Spanish

Returned query gives 1 row(s), 1 column(s):

    159999

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C078  (question 366, database `world_1`)

- Returned by: kwai-autosql-32b/seed303
- Class mass: 50/50
- Instances disagreeing: 33 of 46 (72%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the total number of languages used in Aruba?

**Gold.**
```sql
SELECT COUNT(T2.Language) FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code  =  T2.CountryCode WHERE T1.Name  =  "Aruba"
```

**Returned.**
```sql
SELECT COUNT(*) FROM countrylanguage WHERE CountryCode = 'ABW'
```

**First disagreeing instance** `world_1v5080.sqlite`.

Gold returns 1 row(s), 1 column(s):

    1

Returned query gives 1 row(s), 1 column(s):

    0

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C079  (question 374, database `world_1`)

- Returned by: kwai-autosql-32b/seed303
- Class mass: 50/50
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
FROM country AS T1
INNER JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode AND T2.Language = 'English'
INNER JOIN countrylanguage AS T3 ON T1.Code = T3.CountryCode AND T3.Language = 'French'
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

### C080  (question 473, database `dog_kennels`)

- Returned by: kwai-autosql-32b/seed303
- Class mass: 50/50
- Instances disagreeing: 15 of 48 (31%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Give me the description of the treatment type that is least expensive.

**Gold.**
```sql
SELECT T1.treatment_type_description FROM Treatment_types AS T1 JOIN Treatments AS T2 ON T1.treatment_type_code  =  T2.treatment_type_code GROUP BY T1.treatment_type_code ORDER BY sum(cost_of_treatment) ASC LIMIT 1
```

**Returned.**
```sql
SELECT T2.treatment_type_description
FROM Treatments AS T1
INNER JOIN Treatment_Types AS T2 ON T1.treatment_type_code = T2.treatment_type_code
ORDER BY T1.cost_of_treatment ASC
LIMIT 1
```

**First disagreeing instance** `dog_kennelsv5081.sqlite`.

Gold returns 1 row(s), 1 column(s):

    QOY2(500

Returned query gives 1 row(s), 1 column(s):

    2

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C081  (question 15, database `concert_singer`)

- Returned by: kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Class mass: 50/50, 50/50, 50/50
- Instances disagreeing: 17 of 32 (53%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Show the stadium name and capacity with most number of concerts in  2014 or after.

**Gold.**
```sql
SELECT T2.name ,  T2.capacity FROM concert AS T1 JOIN stadium AS T2 ON T1.stadium_id  =  T2.stadium_id WHERE T1.year  >=  2014 GROUP BY T2.stadium_id ORDER BY count(*) DESC LIMIT 1
```

**Returned.**
```sql
SELECT T2.Name, T2.Capacity
FROM concert AS T1
INNER JOIN stadium AS T2 ON T1.Stadium_ID = T2.Stadium_ID
WHERE T1.Year >= '2014'
GROUP BY T2.Name, T2.Capacity
ORDER BY COUNT(T1.concert_ID) DESC
LIMIT 1
```

**First disagreeing instance** `concert_singerv5083.sqlite`.

Gold returns 1 row(s), 2 column(s):

    mpr5T0V | 2600364897

Returned query gives 1 row(s), 2 column(s):

    Bayview Stadium | 19

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C082  (question 16, database `concert_singer`)

- Returned by: kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Class mass: 50/50, 50/50, 50/50
- Instances disagreeing: 17 of 32 (53%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What is the name and capacity of the stadium  with the most concerts after 2013?

**Gold.**
```sql
select t2.name ,  t2.capacity from concert as t1 join stadium as t2 on t1.stadium_id  =  t2.stadium_id where t1.year  >  2013 group by t2.stadium_id order by count(*) desc limit 1
```

**Returned.**
```sql
SELECT T2.Name, T2.Capacity
FROM concert AS T1
INNER JOIN stadium AS T2 ON T1.Stadium_ID = T2.Stadium_ID
WHERE T1.Year > '2013'
GROUP BY T2.Name, T2.Capacity
ORDER BY COUNT(T1.concert_ID) DESC
LIMIT 1
```

**First disagreeing instance** `concert_singerv5083.sqlite`.

Gold returns 1 row(s), 2 column(s):

    mpr5T0V | 2600364897

Returned query gives 1 row(s), 2 column(s):

    Bayview Stadium | 19

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C083  (question 21, database `concert_singer`)

- Returned by: kwai-autosql-14b/seed101
- Class mass: 50/50
- Instances disagreeing: 29 of 32 (91%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the names of all stadiums that did not have a concert in 2014?

**Gold.**
```sql
SELECT name FROM stadium EXCEPT SELECT T2.name FROM concert AS T1 JOIN stadium AS T2 ON T1.stadium_id  =  T2.stadium_id WHERE T1.year  =  2014
```

**Returned.**
```sql
SELECT T1.Name
FROM stadium AS T1
WHERE T1.Stadium_ID NOT IN (
    SELECT T2.Stadium_ID
    FROM concert AS T2
    WHERE T2.Year = '2014'
)
```

**First disagreeing instance** `concert_singertest0.sqlite`.

Gold returns 14 row(s), 1 column(s):

    )uFP
    03RZUfj(bwx UE
    19
    2h52O0
    Be(
    Recreation Par
    RvI8xFrance
    V2z20hJn
    cmrzmn3fEIv4v2)r
    kHG1vmsN
    lJojzlh5tVtfoa)
    mC
    ... (14 rows total)

Returned query gives 38 row(s), 1 column(s):

    Recreation Park
    20
    2
    20
    France
    Glebe Park
    2
    Recreation Park
    2h52O0
    0
    2
    )uFP
    ... (38 rows total)

Difference: gold_subset_of_rep; 14 row(s) in common, 0 only in the gold, 9 only in the returned result.

### C084  (question 23, database `concert_singer`)

- Returned by: kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Class mass: 50/50, 50/50, 50/50
- Instances disagreeing: 29 of 32 (91%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** List singer names and number of concerts for each person.

**Gold.**
```sql
SELECT T2.name ,  count(*) FROM singer_in_concert AS T1 JOIN singer AS T2 ON T1.singer_id  =  T2.singer_id GROUP BY T2.singer_id
```

**Returned.**
```sql
SELECT T1.Name, COUNT(T2.concert_ID)
FROM singer AS T1
INNER JOIN singer_in_concert AS T2 ON T1.Singer_ID = T2.Singer_ID
GROUP BY T1.Name
```

**First disagreeing instance** `concert_singertest0.sqlite`.

Gold returns 105 row(s), 2 column(s):

    19 | 2
    Rose White | 1
    2 | 1
    TRcZXxHKP | 1
    IDpR8 | 1
    19 | 3
    20 | 3
    France | 1
    l1Ua98Vy | 1
    K | 2
    0 | 1
    Timbaland | 1
    ... (105 rows total)

Returned query gives 45 row(s), 2 column(s):

     | 4
    0 | 9
    0Yjt87 | 2
    1 | 8
    19 | 10
    19ky90n | 1
    2 | 4
    20 | 13
    21 | 3
    2tN | 2
    5 | 3
    5c  | 2
    ... (45 rows total)

Difference: values differ; 34 row(s) in common, 26 only in the gold, 11 only in the returned result.

### C085  (question 43, database `pets_1`)

- Returned by: kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Class mass: 50/50, 50/50, 50/50
- Instances disagreeing: 23 of 27 (85%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find the name of students who have both cat and dog.

**Gold.**
```sql
select t1.fname from student as t1 join has_pet as t2 on t1.stuid  =  t2.stuid join pets as t3 on t3.petid  =  t2.petid where t3.pettype  =  'cat' intersect select t1.fname from student as t1 join has_pet as t2 on t1.stuid  =  t2.stuid join pets as t3 on t3.petid  =  t2.petid where t3.pettype  =  'dog'
```

**Returned.**
```sql
SELECT DISTINCT S.Fname, S.LName
FROM Student S
INNER JOIN Has_Pet HP ON S.StuID = HP.StuID
INNER JOIN Pets P ON HP.PetID = P.PetID
WHERE P.PetType = 'cat'
INTERSECT
SELECT DISTINCT S.Fname, S.LName
FROM Student S
INNER JOIN Has_Pet HP ON S.StuID = HP.StuID
INNER JOIN Pets P ON HP.PetID = P.PetID
WHERE P.PetType = 'dog'
```

**First disagreeing instance** `pets_1v5080.sqlite`.

Gold returns 5 row(s), 1 column(s):

    0
    003
    10
    David
    Oy01U(d

Returned query gives 4 row(s), 2 column(s):

    0 | 9
    003 | 10
    David | Linda
    Oy01U(d | AilCTbfL

Difference: col_count_differs, disjoint; 0 row(s) in common, 5 only in the gold, 4 only in the returned result.

### C086  (question 55, database `pets_1`)

- Returned by: kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Class mass: 50/50, 50/50, 50/50
- Instances disagreeing: 10 of 27 (37%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find the last name of the student who has a cat that is 3 years old.

**Gold.**
```sql
SELECT T1.lname FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid  =  T2.stuid JOIN pets AS T3 ON T3.petid  =  T2.petid WHERE T3.pet_age  =  3 AND T3.pettype  =  'cat'
```

**Returned.**
```sql
SELECT DISTINCT S.LName
FROM Student S
INNER JOIN Has_Pet HP ON S.StuID = HP.StuID
INNER JOIN Pets P ON HP.PetID = P.PetID
WHERE P.PetType = 'cat' AND P.pet_age = 3
```

**First disagreeing instance** `pets_1v5083.sqlite`.

Gold returns 10 row(s), 1 column(s):

    1003
    2
    0
    ONgJgQVyw
    rwds6
    rwds6
    Andreou
    10
    gppH4e
    cat

Returned query gives 9 row(s), 1 column(s):

    1003
    2
    0
    ONgJgQVyw
    rwds6
    Andreou
    10
    gppH4e
    cat

Difference: duplicate_multiplicity_only; 9 row(s) in common, 0 only in the gold, 0 only in the returned result.

### C087  (question 71, database `car_1`)

- Returned by: kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Class mass: 50/50, 47/50, 47/50
- Instances disagreeing: 57 of 60 (95%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** How many car models are produced by each manufacturer? List the count and the maker full name.

**Gold.**
```sql
select count(*) ,  t2.fullname from model_list as t1 join car_makers as t2 on t1.maker  =  t2.id group by t2.id;
```

**Returned.**
```sql
SELECT T1.FullName, COUNT(T2.Model) AS model_count
FROM car_makers AS T1
INNER JOIN model_list AS T2 ON T1.Id = T2.Maker
GROUP BY T1.FullName
```

**First disagreeing instance** `car_1v5080.sqlite`.

Gold returns 32 row(s), 2 column(s):

    1 | WgId2j2tiOKXNbJE)
    1 | 19.0
    1 | 4
    1 | 3
    1 | 5
    1 | eugeaut
    2 | ER5Km8gHv9Mtc9w6Jlv
    1 | General Motors
    2 | JS8WGkUpkQNRnwpw
    1 | 9
    2 | 151
    1 | fia
    ... (32 rows total)

Returned query gives 28 row(s), 2 column(s):

     | 3
    0qSpYywiWEZMmhE9zCeNGcUo5Y | 2
    0xIjVZ | 1
    1 | 1
    151 | 2
    19.0 | 1
    1975 | 1
    3 | 2
    3499 | 1
    4 | 1
    4000N1f3g | 1
    5 | 3
    ... (28 rows total)

Difference: disjoint; 0 row(s) in common, 30 only in the gold, 28 only in the returned result.

### C088  (question 90, database `car_1`)

- Returned by: kwai-autosql-14b/seed101
- Class mass: 19/50
- Instances disagreeing: 18 of 60 (30%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the average edispl of the cars of  volvo?

**Gold.**
```sql
SELECT avg(T2.edispl) FROM CAR_NAMES AS T1 JOIN CARS_DATA AS T2 ON T1.MakeId  =  T2.Id WHERE T1.Model  =  'volvo';
```

**Returned.**
```sql
SELECT AVG(T4.Edispl)
FROM car_makers AS T1
INNER JOIN model_list AS T2 ON T1.Id = T2.Maker
INNER JOIN car_names AS T3 ON T2.Model = T3.Model
INNER JOIN cars_data AS T4 ON T3.MakeId = T4.Id
WHERE T1.Maker = 'volvo'
```

**First disagreeing instance** `car_1v50811.sqlite`.

Gold returns 1 row(s), 1 column(s):

    NULL

Returned query gives 1 row(s), 1 column(s):

    436889768.3333333

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C089  (question 92, database `car_1`)

- Returned by: kwai-autosql-14b/seed101, kwai-autosql-14b/seed303
- Class mass: 40/50, 35/50
- Instances disagreeing: 14 of 60 (23%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What car has the most different versions?

**Gold.**
```sql
SELECT Model FROM CAR_NAMES GROUP BY Model ORDER BY count(*) DESC LIMIT 1;
```

**Returned.**
```sql
SELECT T1.Model
FROM car_names AS T1
INNER JOIN cars_data AS T2 ON T1.MakeId = T2.Id
GROUP BY T1.Model
ORDER BY COUNT(T1.Model) DESC
LIMIT 1
```

**First disagreeing instance** `car_1v5080.sqlite`.

Gold returns 1 row(s), 1 column(s):

    0

Returned query gives 1 row(s), 1 column(s):

    oldsmobile

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C090  (question 103, database `car_1`)

- Returned by: kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Class mass: 21/50, 19/50, 19/50
- Instances disagreeing: 17 of 60 (28%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** For  volvo, how many cylinders does the car with the least accelerate have?

**Gold.**
```sql
SELECT T1.cylinders FROM CARS_DATA AS T1 JOIN CAR_NAMES AS T2 ON T1.Id  =  T2.MakeId WHERE T2.Model  =  'volvo' ORDER BY T1.accelerate ASC LIMIT 1;
```

**Returned.**
```sql
SELECT T4.Cylinders
FROM car_makers AS T1
INNER JOIN model_list AS T2 ON T1.Id = T2.Maker
INNER JOIN car_names AS T3 ON T2.Model = T3.Model
INNER JOIN cars_data AS T4 ON T3.MakeId = T4.Id
WHERE T1.Maker = 'volvo'
ORDER BY T4.Accelerate ASC
LIMIT 1
```

**First disagreeing instance** `car_1v50811.sqlite`.

Gold returns 0 row(s), None column(s):

    (no rows)

Returned query gives 1 row(s), 1 column(s):

    1969

Difference: gold_empty; 0 row(s) in common, 0 only in the gold, 1 only in the returned result.

### C091  (question 111, database `car_1`)

- Returned by: kwai-autosql-14b/seed101
- Class mass: 45/50
- Instances disagreeing: 20 of 60 (33%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the id and names of the countries which have more than 3 car makers or produce the 'fiat' ?

**Gold.**
```sql
SELECT T1.countryId ,  T1.CountryName FROM Countries AS T1 JOIN CAR_MAKERS AS T2 ON T1.CountryId  =  T2.Country GROUP BY T1.countryId HAVING count(*)  >  3 UNION SELECT T1.countryId ,  T1.CountryName FROM Countries AS T1 JOIN CAR_MAKERS AS T2 ON T1.CountryId  =  T2.Country JOIN MODEL_LIST AS T3 ON T2.Id  =  T3.Maker WHERE T3.Model  =  'fiat';
```

**Returned.**
```sql
SELECT T2.CountryId, T2.CountryName
FROM car_makers AS T1
INNER JOIN countries AS T2 ON T1.Country = T2.CountryId
GROUP BY T2.CountryId, T2.CountryName
HAVING COUNT(T1.Maker) > 3 OR SUM(CASE WHEN T1.Maker = 'fiat' THEN 1 ELSE 0 END) > 0
```

**First disagreeing instance** `car_1v5080.sqlite`.

Gold returns 8 row(s), 2 column(s):

    -4076741865 | us
    10 | Om
    12 | 400
    19 | ford
    151 | buick
    1981 | asia
    8210699449 | 3499
    9236429507 | mc

Returned query gives 9 row(s), 2 column(s):

    -4076741865 | us
    10 | Om
    12 | 400
    19 | ford
    151 | buick
    1969 | france
    1981 | asia
    8210699449 | 3499
    9236429507 | mc

Difference: gold_subset_of_rep; 8 row(s) in common, 0 only in the gold, 1 only in the returned result.

### C092  (question 112, database `car_1`)

- Returned by: kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Class mass: 45/50, 49/50, 46/50
- Instances disagreeing: 20 of 60 (33%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the ids and names of all countries that either have more than 3 car makers or produce fiats?

**Gold.**
```sql
select t1.countryid ,  t1.countryname from countries as t1 join car_makers as t2 on t1.countryid  =  t2.country group by t1.countryid having count(*)  >  3 union select t1.countryid ,  t1.countryname from countries as t1 join car_makers as t2 on t1.countryid  =  t2.country join model_list as t3 on t2.id  =  t3.maker where t3.model  =  'fiat';
```

**Returned.**
```sql
SELECT T1.CountryId, T1.CountryName
FROM countries AS T1
INNER JOIN car_makers AS T2 ON T1.CountryId = T2.Country
GROUP BY T1.CountryId, T1.CountryName
HAVING COUNT(T2.Id) > 3
UNION
SELECT T1.CountryId, T1.CountryName
FROM countries AS T1
INNER JOIN car_makers AS T2 ON T1.CountryId = T2.Country
WHERE T2.Maker = 'fiat'
```

**First disagreeing instance** `car_1v5080.sqlite`.

Gold returns 8 row(s), 2 column(s):

    -4076741865 | us
    10 | Om
    12 | 400
    19 | ford
    151 | buick
    1981 | asia
    8210699449 | 3499
    9236429507 | mc

Returned query gives 9 row(s), 2 column(s):

    -4076741865 | us
    10 | Om
    12 | 400
    19 | ford
    151 | buick
    1969 | france
    1981 | asia
    8210699449 | 3499
    9236429507 | mc

Difference: gold_subset_of_rep; 8 row(s) in common, 0 only in the gold, 1 only in the returned result.

### C093  (question 147, database `flight_2`)

- Returned by: kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Class mass: 50/50, 50/50, 50/50
- Instances disagreeing: 4 of 56 (7%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are airlines that have some flight departing from AHD?

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

### C094  (question 183, database `employee_hire_evaluation`)

- Returned by: kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Class mass: 50/50, 50/50, 50/50
- Instances disagreeing: 18 of 27 (67%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What is the name of the shop that is recruiting the largest number of employees?

**Gold.**
```sql
SELECT t2.name FROM hiring AS t1 JOIN shop AS t2 ON t1.shop_id  =  t2.shop_id GROUP BY t1.shop_id ORDER BY count(*) DESC LIMIT 1
```

**Returned.**
```sql
SELECT T2.Name
FROM hiring AS T1
INNER JOIN shop AS T2 ON T1.Shop_ID = T2.Shop_ID
GROUP BY T2.Name
ORDER BY COUNT(T1.Employee_ID) DESC
LIMIT 1
```

**First disagreeing instance** `employee_hire_evaluationv5083735.sqlite`.

Gold returns 1 row(s), 1 column(s):

    FC Honka

Returned query gives 1 row(s), 1 column(s):

    31

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C095  (question 184, database `employee_hire_evaluation`)

- Returned by: kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Class mass: 50/50, 50/50, 50/50
- Instances disagreeing: 18 of 27 (67%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Which shop has the most employees? Give me the shop name.

**Gold.**
```sql
SELECT t2.name FROM hiring AS t1 JOIN shop AS t2 ON t1.shop_id  =  t2.shop_id GROUP BY t1.shop_id ORDER BY count(*) DESC LIMIT 1
```

**Returned.**
```sql
SELECT T2.Name
FROM hiring AS T1
INNER JOIN shop AS T2 ON T1.Shop_ID = T2.Shop_ID
GROUP BY T2.Name
ORDER BY COUNT(T1.Employee_ID) DESC
LIMIT 1
```

**First disagreeing instance** `employee_hire_evaluationv5083735.sqlite`.

Gold returns 1 row(s), 1 column(s):

    FC Honka

Returned query gives 1 row(s), 1 column(s):

    31

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C096  (question 236, database `wta_1`)

- Returned by: kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Class mass: 38/50, 35/50, 35/50
- Instances disagreeing: 7 of 33 (21%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Find the name of the winner who has the highest rank points and participated in the Australian Open.

**Gold.**
```sql
SELECT winner_name FROM matches WHERE tourney_name  =  'Australian Open' ORDER BY winner_rank_points DESC LIMIT 1
```

**Returned.**
```sql
SELECT T1.winner_name
FROM matches AS T1
INNER JOIN rankings AS T2 ON T1.winner_id = T2.player_id
WHERE T1.tourney_name = 'Australian Open'
ORDER BY T2.ranking_points DESC
LIMIT 1
```

**First disagreeing instance** `wta_1v5080.sqlite`.

Gold returns 1 row(s), 1 column(s):

    11dVZOO

Returned query gives 1 row(s), 1 column(s):

    nQxjD

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C097  (question 251, database `battle_death`)

- Returned by: kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Class mass: 49/50, 50/50, 50/50
- Instances disagreeing: 22 of 28 (79%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the ids and names of the battles that led to more than 10 people died.

**Gold.**
```sql
SELECT T1.id ,  T1.name FROM battle AS T1 JOIN ship AS T2 ON T1.id  =  T2.lost_in_battle JOIN death AS T3 ON T2.id  =  T3.caused_by_ship_id GROUP BY T1.id HAVING sum(T3.killed)  >  10
```

**Returned.**
```sql
SELECT T1.id, T1.name
FROM battle AS T1
INNER JOIN ship AS T2 ON T1.id = T2.lost_in_battle
INNER JOIN death AS T3 ON T2.id = T3.caused_by_ship_id
WHERE T3.killed > 10
```

**First disagreeing instance** `battle_deathv5080.sqlite`.

Gold returns 61 row(s), 2 column(s):

    -8146471391 | k8HK0o2
    -3057138174 | Kaloyan
    -2519651209 | 226
    -797862848 | ZPYCapturedwFa
    -540009472 | 226
    0 | 0)p
    3 | Battle of Philippopolis
    4 | WorBattle of Philippopolis6dU
    10 | Captured
    11 | 2
    225 | Battle of Philippopolis
    226 | hZDqJBattle of Serres
    ... (61 rows total)

Returned query gives 124 row(s), 2 column(s):

    9070468346 | VJfwR5)BU83AWD 0787LFzn
    7936890329 | Baldwin I
    3810850516 | Captured
    6826520359 | cv5JOY7tkH(q
    8576269272 | 226
    1111358172 | HMS Atlanta
    10 | Captured
    1 | Kaloyan
    8196806012 | English Channe
    -2519651209 | 226
    9724008145 | 0
    -540009472 | 226
    ... (124 rows total)

Difference: values differ; 58 row(s) in common, 3 only in the gold, 1 only in the returned result.

### C098  (question 366, database `world_1`)

- Returned by: kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Class mass: 50/50, 50/50, 50/50
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

### C099  (question 368, database `world_1`)

- Returned by: kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Class mass: 50/50, 50/50, 50/50
- Instances disagreeing: 3 of 46 (7%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** How many official languages does Afghanistan have?

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

### C100  (question 393, database `world_1`)

- Returned by: kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Class mass: 41/50, 36/50, 41/50
- Instances disagreeing: 39 of 46 (85%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** How many people live in countries that do not speak English?

**Gold.**
```sql
SELECT sum(Population) FROM country WHERE Name NOT IN (SELECT T1.Name FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code  =  T2.CountryCode WHERE T2.Language  =  "English")
```

**Returned.**
```sql
SELECT SUM(Population)
FROM country
WHERE Code NOT IN (
  SELECT CountryCode
  FROM countrylanguage
  WHERE Language = 'English'
)
```

**First disagreeing instance** `world_1v5080.sqlite`.

Gold returns 1 row(s), 1 column(s):

    268945194457

Returned query gives 1 row(s), 1 column(s):

    273514308785

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C101  (question 429, database `world_1`)

- Returned by: kwai-autosql-14b/seed101, kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Class mass: 50/50, 50/50, 50/50
- Instances disagreeing: 38 of 46 (83%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the cities who have more than 160000 people and less than 900000 people?

**Gold.**
```sql
SELECT name FROM city WHERE Population BETWEEN 160000 AND 900000
```

**Returned.**
```sql
SELECT Name FROM city WHERE Population > 160000 AND Population < 900000
```

**First disagreeing instance** `world_1v5080.sqlite`.

Gold returns 3 row(s), 1 column(s):

    vsgTbpN
    Jql900001MwW
    930

Returned query gives 1 row(s), 1 column(s):

    Jql900001MwW

Difference: rep_subset_of_gold; 1 row(s) in common, 2 only in the gold, 0 only in the returned result.

### C102  (question 468, database `dog_kennels`)

- Returned by: kwai-autosql-14b/seed101, kwai-autosql-14b/seed202
- Class mass: 50/50, 49/50
- Instances disagreeing: 22 of 48 (46%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Which person has the most dogs? List the id, first name and last name.

**Gold.**
```sql
SELECT T1.owner_id ,  T2.first_name ,  T2.last_name FROM Dogs AS T1 JOIN Owners AS T2 ON T1.owner_id  =  T2.owner_id GROUP BY T1.owner_id ORDER BY count(*) DESC LIMIT 1
```

**Returned.**
```sql
SELECT O.owner_id, O.first_name, O.last_name
FROM Owners O
INNER JOIN Dogs D ON O.owner_id = D.owner_id
GROUP BY O.owner_id, O.first_name, O.last_name
ORDER BY COUNT(D.dog_id) DESC
LIMIT 1
```

**First disagreeing instance** `dog_kennelsv5080.sqlite`.

Gold returns 1 row(s), 3 column(s):

    7994075702 | 501 | qwM)4Jaclyn

Returned query gives 1 row(s), 3 column(s):

    999 | bPG%West%CRw | 0

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C103  (question 469, database `dog_kennels`)

- Returned by: kwai-autosql-14b/seed101, kwai-autosql-14b/seed303
- Class mass: 47/50, 50/50
- Instances disagreeing: 22 of 48 (46%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Return the id, first name and last name of the person who has the most dogs.

**Gold.**
```sql
SELECT T1.owner_id ,  T2.first_name ,  T2.last_name FROM Dogs AS T1 JOIN Owners AS T2 ON T1.owner_id  =  T2.owner_id GROUP BY T1.owner_id ORDER BY count(*) DESC LIMIT 1
```

**Returned.**
```sql
SELECT O.owner_id, O.first_name, O.last_name
FROM Owners O
INNER JOIN Dogs D ON O.owner_id = D.owner_id
GROUP BY O.owner_id, O.first_name, O.last_name
ORDER BY COUNT(D.dog_id) DESC
LIMIT 1
```

**First disagreeing instance** `dog_kennelsv5080.sqlite`.

Gold returns 1 row(s), 3 column(s):

    7994075702 | 501 | qwM)4Jaclyn

Returned query gives 1 row(s), 3 column(s):

    999 | bPG%West%CRw | 0

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C104  (question 24, database `concert_singer`)

- Returned by: kwai-autosql-14b/seed202
- Class mass: 50/50
- Instances disagreeing: 29 of 32 (91%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the names and number of concerts for each person?

**Gold.**
```sql
SELECT T2.name ,  count(*) FROM singer_in_concert AS T1 JOIN singer AS T2 ON T1.singer_id  =  T2.singer_id GROUP BY T2.singer_id
```

**Returned.**
```sql
SELECT T1.Name, COUNT(T2.concert_ID)
FROM singer AS T1
INNER JOIN singer_in_concert AS T2 ON T1.Singer_ID = T2.Singer_ID
GROUP BY T1.Name
```

**First disagreeing instance** `concert_singertest0.sqlite`.

Gold returns 105 row(s), 2 column(s):

    19 | 2
    Rose White | 1
    2 | 1
    TRcZXxHKP | 1
    IDpR8 | 1
    19 | 3
    20 | 3
    France | 1
    l1Ua98Vy | 1
    K | 2
    0 | 1
    Timbaland | 1
    ... (105 rows total)

Returned query gives 45 row(s), 2 column(s):

     | 4
    0 | 9
    0Yjt87 | 2
    1 | 8
    19 | 10
    19ky90n | 1
    2 | 4
    20 | 13
    21 | 3
    2tN | 2
    5 | 3
    5c  | 2
    ... (45 rows total)

Difference: values differ; 34 row(s) in common, 26 only in the gold, 11 only in the returned result.

### C105  (question 56, database `pets_1`)

- Returned by: kwai-autosql-14b/seed202
- Class mass: 50/50
- Instances disagreeing: 10 of 27 (37%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the last name of the student who has a cat that is 3 years old?

**Gold.**
```sql
SELECT T1.lname FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid  =  T2.stuid JOIN pets AS T3 ON T3.petid  =  T2.petid WHERE T3.pet_age  =  3 AND T3.pettype  =  'cat'
```

**Returned.**
```sql
SELECT DISTINCT S.LName
FROM Student S
INNER JOIN Has_Pet HP ON S.StuID = HP.StuID
INNER JOIN Pets P ON HP.PetID = P.PetID
WHERE P.PetType = 'cat' AND P.pet_age = 3
```

**First disagreeing instance** `pets_1v5083.sqlite`.

Gold returns 10 row(s), 1 column(s):

    1003
    2
    0
    ONgJgQVyw
    rwds6
    rwds6
    Andreou
    10
    gppH4e
    cat

Returned query gives 9 row(s), 1 column(s):

    1003
    2
    0
    ONgJgQVyw
    rwds6
    Andreou
    10
    gppH4e
    cat

Difference: duplicate_multiplicity_only; 9 row(s) in common, 0 only in the gold, 0 only in the returned result.

### C106  (question 104, database `car_1`)

- Returned by: kwai-autosql-14b/seed202
- Class mass: 21/50
- Instances disagreeing: 17 of 60 (28%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** For a volvo , how many cylinders does the version with least accelerate have?

**Gold.**
```sql
SELECT T1.cylinders FROM CARS_DATA AS T1 JOIN CAR_NAMES AS T2 ON T1.Id  =  T2.MakeId WHERE T2.Model  =  'volvo' ORDER BY T1.accelerate ASC LIMIT 1;
```

**Returned.**
```sql
SELECT T4.Cylinders
FROM car_makers AS T1
INNER JOIN model_list AS T2 ON T1.Id = T2.Maker
INNER JOIN car_names AS T3 ON T2.Model = T3.Model
INNER JOIN cars_data AS T4 ON T3.MakeId = T4.Id
WHERE T1.Maker = 'volvo'
ORDER BY T4.Accelerate ASC
LIMIT 1
```

**First disagreeing instance** `car_1v50811.sqlite`.

Gold returns 0 row(s), None column(s):

    (no rows)

Returned query gives 1 row(s), 1 column(s):

    1969

Difference: gold_empty; 0 row(s) in common, 0 only in the gold, 1 only in the returned result.

### C107  (question 137, database `flight_2`)

- Returned by: kwai-autosql-14b/seed202
- Class mass: 50/50
- Instances disagreeing: 1 of 56 (2%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** How many flights depart from Aberdeen and arrive at Ashley?

**Gold.**
```sql
SELECT count(*) FROM FLIGHTS AS T1 JOIN AIRPORTS AS T2 ON T1.DestAirport  =  T2.AirportCode JOIN AIRPORTS AS T3 ON T1.SourceAirport  =  T3.AirportCode WHERE T2.City  =  "Ashley" AND T3.City  =  "Aberdeen"
```

**Returned.**
```sql
SELECT COUNT(*)
FROM flights
WHERE SourceAirport = (SELECT AirportCode FROM airports WHERE City = 'Aberdeen')
  AND DestAirport = (SELECT AirportCode FROM airports WHERE City = 'Ashley')
```

**First disagreeing instance** `flight_2v50814.sqlite`.

Gold returns 1 row(s), 1 column(s):

    1

Returned query gives 1 row(s), 1 column(s):

    0

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C108  (question 248, database `wta_1`)

- Returned by: kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Class mass: 50/50, 50/50
- Instances disagreeing: 6 of 33 (18%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** How many different winners both participated in the WTA Championships and were left handed?

**Gold.**
```sql
SELECT count(DISTINCT winner_name) FROM matches WHERE tourney_name  =  'WTA Championships' AND winner_hand  =  'L'
```

**Returned.**
```sql
SELECT COUNT(DISTINCT T1.winner_id)
FROM matches AS T1
INNER JOIN players AS T2 ON T1.winner_id = T2.player_id
WHERE T1.tourney_name = 'WTA Championships' AND T2.hand = 'L'
```

**First disagreeing instance** `wta_1v50815.sqlite`.

Gold returns 1 row(s), 1 column(s):

    4

Returned query gives 1 row(s), 1 column(s):

    0

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C109  (question 367, database `world_1`)

- Returned by: kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Class mass: 50/50, 50/50
- Instances disagreeing: 26 of 46 (57%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** How many languages are spoken in Aruba?

**Gold.**
```sql
SELECT COUNT(T2.Language) FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code  =  T2.CountryCode WHERE T1.Name  =  "Aruba"
```

**Returned.**
```sql
SELECT COUNT(Language)
FROM countrylanguage
WHERE CountryCode = (SELECT Code FROM country WHERE Name = 'Aruba')
```

**First disagreeing instance** `world_1v50811.sqlite`.

Gold returns 1 row(s), 1 column(s):

    33

Returned query gives 1 row(s), 1 column(s):

    15

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C110  (question 372, database `world_1`)

- Returned by: kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Class mass: 50/50, 50/50
- Instances disagreeing: 3 of 46 (7%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Which continent has the most diverse languages?

**Gold.**
```sql
SELECT T1.Continent FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code  =  T2.CountryCode GROUP BY T1.Continent ORDER BY COUNT(*) DESC LIMIT 1
```

**Returned.**
```sql
SELECT T1.Continent
FROM country AS T1
INNER JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode
GROUP BY T1.Continent
ORDER BY COUNT(DISTINCT T2.Language) DESC
LIMIT 1
```

**First disagreeing instance** `world_1v5082.sqlite`.

Gold returns 1 row(s), 1 column(s):

    2

Returned query gives 1 row(s), 1 column(s):

    North America

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C111  (question 392, database `world_1`)

- Returned by: kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Class mass: 29/50, 26/50
- Instances disagreeing: 39 of 46 (85%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the total number of people living in the nations that do not use English?

**Gold.**
```sql
SELECT sum(Population) FROM country WHERE Name NOT IN (SELECT T1.Name FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code  =  T2.CountryCode WHERE T2.Language  =  "English")
```

**Returned.**
```sql
SELECT SUM(Population)
FROM country
WHERE Code NOT IN (
  SELECT CountryCode
  FROM countrylanguage
  WHERE Language = 'English'
)
```

**First disagreeing instance** `world_1v5080.sqlite`.

Gold returns 1 row(s), 1 column(s):

    268945194457

Returned query gives 1 row(s), 1 column(s):

    273514308785

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C112  (question 484, database `dog_kennels`)

- Returned by: kwai-autosql-14b/seed202, kwai-autosql-14b/seed303
- Class mass: 49/50, 48/50
- Instances disagreeing: 47 of 48 (98%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** How many dogs younger than average?

**Gold.**
```sql
SELECT count(*) FROM Dogs WHERE age  <  ( SELECT avg(age) FROM Dogs )
```

**Returned.**
```sql
SELECT COUNT(*)
FROM Dogs
WHERE CAST(age AS REAL) < (SELECT AVG(CAST(age AS REAL)) FROM Dogs)
```

**First disagreeing instance** `dog_kennelsv5080.sqlite`.

Gold returns 1 row(s), 1 column(s):

    43

Returned query gives 1 row(s), 1 column(s):

    86

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C113  (question 21, database `concert_singer`)

- Returned by: kwai-autosql-14b/seed303
- Class mass: 50/50
- Instances disagreeing: 29 of 32 (91%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the names of all stadiums that did not have a concert in 2014?

**Gold.**
```sql
SELECT name FROM stadium EXCEPT SELECT T2.name FROM concert AS T1 JOIN stadium AS T2 ON T1.stadium_id  =  T2.stadium_id WHERE T1.year  =  2014
```

**Returned.**
```sql
SELECT Name
FROM stadium
WHERE Stadium_ID NOT IN (
  SELECT Stadium_ID
  FROM concert
  WHERE Year = '2014'
)
```

**First disagreeing instance** `concert_singertest0.sqlite`.

Gold returns 14 row(s), 1 column(s):

    )uFP
    03RZUfj(bwx UE
    19
    2h52O0
    Be(
    Recreation Par
    RvI8xFrance
    V2z20hJn
    cmrzmn3fEIv4v2)r
    kHG1vmsN
    lJojzlh5tVtfoa)
    mC
    ... (14 rows total)

Returned query gives 38 row(s), 1 column(s):

    Recreation Park
    20
    2
    20
    France
    Glebe Park
    2
    Recreation Park
    2h52O0
    0
    2
    )uFP
    ... (38 rows total)

Difference: gold_subset_of_rep; 14 row(s) in common, 0 only in the gold, 9 only in the returned result.

### C114  (question 104, database `car_1`)

- Returned by: kwai-autosql-14b/seed303
- Class mass: 16/50
- Instances disagreeing: 17 of 60 (28%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** For a volvo , how many cylinders does the version with least accelerate have?

**Gold.**
```sql
SELECT T1.cylinders FROM CARS_DATA AS T1 JOIN CAR_NAMES AS T2 ON T1.Id  =  T2.MakeId WHERE T2.Model  =  'volvo' ORDER BY T1.accelerate ASC LIMIT 1;
```

**Returned.**
```sql
SELECT T1.Cylinders
FROM cars_data AS T1
INNER JOIN car_names AS T2 ON T1.Id = T2.MakeId
INNER JOIN model_list AS T3 ON T2.Model = T3.Model
INNER JOIN car_makers AS T4 ON T3.Maker = T4.Id
WHERE T4.Maker = 'volvo'
ORDER BY T1.Accelerate ASC
LIMIT 1
```

**First disagreeing instance** `car_1v50811.sqlite`.

Gold returns 0 row(s), None column(s):

    (no rows)

Returned query gives 1 row(s), 1 column(s):

    1969

Difference: gold_empty; 0 row(s) in common, 0 only in the gold, 1 only in the returned result.

### C115  (question 105, database `car_1`)

- Returned by: kwai-autosql-14b/seed303
- Class mass: 24/50
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
HAVING COUNT(T2.Maker) > 2
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

### C116  (question 111, database `car_1`)

- Returned by: kwai-autosql-14b/seed303
- Class mass: 47/50
- Instances disagreeing: 20 of 60 (33%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the id and names of the countries which have more than 3 car makers or produce the 'fiat' ?

**Gold.**
```sql
SELECT T1.countryId ,  T1.CountryName FROM Countries AS T1 JOIN CAR_MAKERS AS T2 ON T1.CountryId  =  T2.Country GROUP BY T1.countryId HAVING count(*)  >  3 UNION SELECT T1.countryId ,  T1.CountryName FROM Countries AS T1 JOIN CAR_MAKERS AS T2 ON T1.CountryId  =  T2.Country JOIN MODEL_LIST AS T3 ON T2.Id  =  T3.Maker WHERE T3.Model  =  'fiat';
```

**Returned.**
```sql
SELECT DISTINCT T2.CountryId, T2.CountryName
FROM car_makers AS T1
INNER JOIN countries AS T2 ON T1.Country = T2.CountryId
GROUP BY T2.CountryId, T2.CountryName
HAVING COUNT(T1.Id) > 3 OR SUM(CASE WHEN T1.Maker = 'fiat' THEN 1 ELSE 0 END) > 0
```

**First disagreeing instance** `car_1v5080.sqlite`.

Gold returns 8 row(s), 2 column(s):

    -4076741865 | us
    10 | Om
    12 | 400
    19 | ford
    151 | buick
    1981 | asia
    8210699449 | 3499
    9236429507 | mc

Returned query gives 9 row(s), 2 column(s):

    -4076741865 | us
    10 | Om
    12 | 400
    19 | ford
    151 | buick
    1969 | france
    1981 | asia
    8210699449 | 3499
    9236429507 | mc

Difference: gold_subset_of_rep; 8 row(s) in common, 0 only in the gold, 1 only in the returned result.

### C117  (question 149, database `flight_2`)

- Returned by: kwai-autosql-14b/seed303
- Class mass: 50/50
- Instances disagreeing: 5 of 56 (9%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are airlines that have flights arriving at AHD?

**Gold.**
```sql
SELECT T1.Airline FROM AIRLINES AS T1 JOIN FLIGHTS AS T2 ON T1.uid  =  T2.Airline WHERE T2.DestAirport  =  "AHD"
```

**Returned.**
```sql
SELECT DISTINCT T1.Airline
FROM airlines AS T1
INNER JOIN flights AS T2 ON T1.uid = T2.Airline
WHERE T2.DestAirport = 'AHD'
```

**First disagreeing instance** `flight_2v50814.sqlite`.

Gold returns 5 row(s), 1 column(s):

    ABR
    199ZSJuF
    5UBp(Hl( 
    2
    5UBp(Hl( 

Returned query gives 4 row(s), 1 column(s):

    ABR
    199ZSJuF
    5UBp(Hl( 
    2

Difference: duplicate_multiplicity_only; 4 row(s) in common, 0 only in the gold, 0 only in the returned result.

### C118  (question 475, database `dog_kennels`)

- Returned by: kwai-autosql-14b/seed303
- Class mass: 20/50
- Instances disagreeing: 1 of 48 (2%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Find the id and zip code of the person who spent the most money in total for his or her dogs.

**Gold.**
```sql
SELECT T1.owner_id ,  T1.zip_code FROM Owners AS T1 JOIN Dogs AS T2 ON T1.owner_id  =  T2.owner_id JOIN Treatments AS T3 ON T2.dog_id  =  T3.dog_id GROUP BY T1.owner_id ORDER BY sum(T3.cost_of_treatment) DESC LIMIT 1
```

**Returned.**
```sql
SELECT T1.owner_id, T1.zip_code
FROM Owners T1
INNER JOIN Dogs T2 ON T1.owner_id = T2.owner_id
INNER JOIN Treatments T3 ON T2.dog_id = T3.dog_id
GROUP BY T1.owner_id, T1.zip_code
ORDER BY SUM(T3.cost_of_treatment) DESC
LIMIT 1
```

**First disagreeing instance** `dog_kennelsv508557.sqlite`.

Gold returns 1 row(s), 2 column(s):

    3501605851 | %West%

Returned query gives 1 row(s), 2 column(s):

    348300858 | 90RK2Uq

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C119  (question 3, database `concert_singer`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed303
- Class mass: 27/50, 29/50
- Instances disagreeing: 3 of 32 (9%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Show the name and the release year of the song by the youngest singer.

**Gold.**
```sql
SELECT song_name ,  song_release_year FROM singer ORDER BY age LIMIT 1
```

**Returned.**
```sql
SELECT Song_Name, Song_release_year
FROM singer
WHERE Age = (SELECT MIN(Age) FROM singer)
```

**First disagreeing instance** `concert_singerv515patch4.sqlite`.

Gold returns 1 row(s), 2 column(s):

    Hey | %Hey%

Returned query gives 2 row(s), 2 column(s):

    Hey | %Hey%
    Love | lKJ)2AjFjp

Difference: gold_subset_of_rep; 1 row(s) in common, 0 only in the gold, 1 only in the returned result.

### C120  (question 15, database `concert_singer`)

- Returned by: omnisql-32b/seed101
- Class mass: 41/50
- Instances disagreeing: 7 of 32 (22%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Show the stadium name and capacity with most number of concerts in  2014 or after.

**Gold.**
```sql
SELECT T2.name ,  T2.capacity FROM concert AS T1 JOIN stadium AS T2 ON T1.stadium_id  =  T2.stadium_id WHERE T1.year  >=  2014 GROUP BY T2.stadium_id ORDER BY count(*) DESC LIMIT 1
```

**Returned.**
```sql
SELECT 
    stadium.Name, 
    stadium.Capacity
FROM 
    concert
INNER JOIN 
    stadium
ON 
    concert.Stadium_ID = stadium.Stadium_ID
WHERE 
    concert.Year >= 2014
GROUP BY 
    concert.Stadium_ID
ORDER BY 
    COUNT(*) DESC
LIMIT 1
```

**First disagreeing instance** `concert_singertest0.sqlite`.

Gold returns 1 row(s), 2 column(s):

    0 | 0

Returned query gives 1 row(s), 2 column(s):

    20 | 8774077902

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C121  (question 16, database `concert_singer`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed202
- Class mass: 49/50, 49/50
- Instances disagreeing: 7 of 32 (22%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What is the name and capacity of the stadium  with the most concerts after 2013?

**Gold.**
```sql
select t2.name ,  t2.capacity from concert as t1 join stadium as t2 on t1.stadium_id  =  t2.stadium_id where t1.year  >  2013 group by t2.stadium_id order by count(*) desc limit 1
```

**Returned.**
```sql
SELECT 
    s.Name, 
    s.Capacity
FROM 
    concert c
INNER JOIN 
    stadium s
ON 
    c.Stadium_ID = s.Stadium_ID
WHERE 
    c.Year > 2013
GROUP BY 
    c.Stadium_ID
ORDER BY 
    COUNT(c.concert_ID) DESC
LIMIT 1
```

**First disagreeing instance** `concert_singertest0.sqlite`.

Gold returns 1 row(s), 2 column(s):

    0 | 0

Returned query gives 1 row(s), 2 column(s):

    20 | 8774077902

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C122  (question 23, database `concert_singer`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed202, omnisql-32b/seed303
- Class mass: 50/50, 49/50, 50/50
- Instances disagreeing: 29 of 32 (91%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** List singer names and number of concerts for each person.

**Gold.**
```sql
SELECT T2.name ,  count(*) FROM singer_in_concert AS T1 JOIN singer AS T2 ON T1.singer_id  =  T2.singer_id GROUP BY T2.singer_id
```

**Returned.**
```sql
SELECT 
    singer.Name, 
    COUNT(singer_in_concert.concert_ID) AS Number_of_Concerts
FROM 
    singer
INNER JOIN 
    singer_in_concert 
ON 
    singer.Singer_ID = singer_in_concert.Singer_ID
GROUP BY 
    singer.Name
```

**First disagreeing instance** `concert_singertest0.sqlite`.

Gold returns 105 row(s), 2 column(s):

    19 | 2
    Rose White | 1
    2 | 1
    TRcZXxHKP | 1
    IDpR8 | 1
    19 | 3
    20 | 3
    France | 1
    l1Ua98Vy | 1
    K | 2
    0 | 1
    Timbaland | 1
    ... (105 rows total)

Returned query gives 45 row(s), 2 column(s):

     | 4
    0 | 9
    0Yjt87 | 2
    1 | 8
    19 | 10
    19ky90n | 1
    2 | 4
    20 | 13
    21 | 3
    2tN | 2
    5 | 3
    5c  | 2
    ... (45 rows total)

Difference: values differ; 34 row(s) in common, 26 only in the gold, 11 only in the returned result.

### C123  (question 24, database `concert_singer`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed202, omnisql-32b/seed303
- Class mass: 50/50, 50/50, 50/50
- Instances disagreeing: 29 of 32 (91%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the names and number of concerts for each person?

**Gold.**
```sql
SELECT T2.name ,  count(*) FROM singer_in_concert AS T1 JOIN singer AS T2 ON T1.singer_id  =  T2.singer_id GROUP BY T2.singer_id
```

**Returned.**
```sql
SELECT 
    singer.Name, 
    COUNT(singer_in_concert.concert_ID) AS Number_of_Concerts
FROM 
    singer
INNER JOIN 
    singer_in_concert 
ON 
    singer.Singer_ID = singer_in_concert.Singer_ID
GROUP BY 
    singer.Name
```

**First disagreeing instance** `concert_singertest0.sqlite`.

Gold returns 105 row(s), 2 column(s):

    19 | 2
    Rose White | 1
    2 | 1
    TRcZXxHKP | 1
    IDpR8 | 1
    19 | 3
    20 | 3
    France | 1
    l1Ua98Vy | 1
    K | 2
    0 | 1
    Timbaland | 1
    ... (105 rows total)

Returned query gives 45 row(s), 2 column(s):

     | 4
    0 | 9
    0Yjt87 | 2
    1 | 8
    19 | 10
    19ky90n | 1
    2 | 4
    20 | 13
    21 | 3
    2tN | 2
    5 | 3
    5c  | 2
    ... (45 rows total)

Difference: values differ; 34 row(s) in common, 26 only in the gold, 11 only in the returned result.

### C124  (question 43, database `pets_1`)

- Returned by: omnisql-32b/seed101
- Class mass: 50/50
- Instances disagreeing: 23 of 27 (85%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find the name of students who have both cat and dog.

**Gold.**
```sql
select t1.fname from student as t1 join has_pet as t2 on t1.stuid  =  t2.stuid join pets as t3 on t3.petid  =  t2.petid where t3.pettype  =  'cat' intersect select t1.fname from student as t1 join has_pet as t2 on t1.stuid  =  t2.stuid join pets as t3 on t3.petid  =  t2.petid where t3.pettype  =  'dog'
```

**Returned.**
```sql
SELECT S.Fname, S.LName
FROM Student S
JOIN Has_Pet HP ON S.StuID = HP.StuID
JOIN Pets P ON HP.PetID = P.PetID
WHERE P.PetType = 'cat'

INTERSECT

SELECT S.Fname, S.LName
FROM Student S
JOIN Has_Pet HP ON S.StuID = HP.StuID
JOIN Pets P ON HP.PetID = P.PetID
WHERE P.PetType = 'dog'
```

**First disagreeing instance** `pets_1v5080.sqlite`.

Gold returns 5 row(s), 1 column(s):

    0
    003
    10
    David
    Oy01U(d

Returned query gives 4 row(s), 2 column(s):

    0 | 9
    003 | 10
    David | Linda
    Oy01U(d | AilCTbfL

Difference: col_count_differs, disjoint; 0 row(s) in common, 5 only in the gold, 4 only in the returned result.

### C125  (question 52, database `pets_1`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed202, omnisql-32b/seed303
- Class mass: 50/50, 50/50, 50/50
- Instances disagreeing: 3 of 27 (11%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What type of pet is the youngest animal, and how much does it weigh?

**Gold.**
```sql
SELECT pettype ,  weight FROM pets ORDER BY pet_age LIMIT 1
```

**Returned.**
```sql
SELECT PetType, weight
FROM Pets
WHERE pet_age = (SELECT MIN(pet_age) FROM Pets)
```

**First disagreeing instance** `pets_1v5080.sqlite`.

Gold returns 1 row(s), 2 column(s):

    3 | 10.0

Returned query gives 7 row(s), 2 column(s):

    3 | 10.0
    (iKpD | 10.0
    2 | 9.0
    9)jcatFEl | 1.0
    20 | 10.0
    0 | 1.0
    cat | 1003.0

Difference: gold_subset_of_rep; 1 row(s) in common, 0 only in the gold, 6 only in the returned result.

### C126  (question 69, database `car_1`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed202, omnisql-32b/seed303
- Class mass: 49/50, 48/50, 48/50
- Instances disagreeing: 42 of 60 (70%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Which of the nations has the most car makers? List the country name.

**Gold.**
```sql
SELECT T2.CountryName FROM CAR_MAKERS AS T1 JOIN COUNTRIES AS T2 ON T1.Country  =  T2.CountryId GROUP BY T1.Country ORDER BY Count(*) DESC LIMIT 1;
```

**Returned.**
```sql
SELECT c.CountryName
FROM car_makers cm
JOIN countries c ON cm.Country = c.CountryId
GROUP BY c.CountryName
ORDER BY COUNT(cm.Id) DESC
LIMIT 1
```

**First disagreeing instance** `car_1v5080.sqlite`.

Gold returns 1 row(s), 1 column(s):

    us

Returned query gives 1 row(s), 1 column(s):

    asia

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C127  (question 70, database `car_1`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed202, omnisql-32b/seed303
- Class mass: 48/50, 46/50, 45/50
- Instances disagreeing: 42 of 60 (70%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What is the name of the nation with the most car makers?

**Gold.**
```sql
SELECT T2.CountryName FROM CAR_MAKERS AS T1 JOIN COUNTRIES AS T2 ON T1.Country  =  T2.CountryId GROUP BY T1.Country ORDER BY Count(*) DESC LIMIT 1;
```

**Returned.**
```sql
SELECT c.CountryName
FROM car_makers cm
JOIN countries c ON cm.Country = c.CountryId
GROUP BY c.CountryName
ORDER BY COUNT(cm.Id) DESC
LIMIT 1
```

**First disagreeing instance** `car_1v5080.sqlite`.

Gold returns 1 row(s), 1 column(s):

    us

Returned query gives 1 row(s), 1 column(s):

    asia

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C128  (question 71, database `car_1`)

- Returned by: omnisql-32b/seed101
- Class mass: 50/50
- Instances disagreeing: 57 of 60 (95%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** How many car models are produced by each manufacturer? List the count and the maker full name.

**Gold.**
```sql
select count(*) ,  t2.fullname from model_list as t1 join car_makers as t2 on t1.maker  =  t2.id group by t2.id;
```

**Returned.**
```sql
SELECT 
    COUNT(T1.Model) AS Count, 
    T2.FullName
FROM 
    model_list T1
INNER JOIN 
    car_makers T2 ON T1.Maker = T2.Id
GROUP BY 
    T2.FullName
```

**First disagreeing instance** `car_1v5080.sqlite`.

Gold returns 32 row(s), 2 column(s):

    1 | WgId2j2tiOKXNbJE)
    1 | 19.0
    1 | 4
    1 | 3
    1 | 5
    1 | eugeaut
    2 | ER5Km8gHv9Mtc9w6Jlv
    1 | General Motors
    2 | JS8WGkUpkQNRnwpw
    1 | 9
    2 | 151
    1 | fia
    ... (32 rows total)

Returned query gives 28 row(s), 2 column(s):

    3 | 
    2 | 0qSpYywiWEZMmhE9zCeNGcUo5Y
    1 | 0xIjVZ
    1 | 1
    2 | 151
    1 | 19.0
    1 | 1975
    2 | 3
    1 | 3499
    1 | 4
    1 | 4000N1f3g
    3 | 5
    ... (28 rows total)

Difference: values differ; 24 row(s) in common, 6 only in the gold, 4 only in the returned result.

### C129  (question 74, database `car_1`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed202
- Class mass: 35/50, 35/50
- Instances disagreeing: 7 of 60 (12%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** How many car makers are there in france?

**Gold.**
```sql
SELECT count(*) FROM CAR_MAKERS AS T1 JOIN COUNTRIES AS T2 ON T1.Country  =  T2.CountryId WHERE T2.CountryName  =  'france';
```

**Returned.**
```sql
SELECT COUNT(*) 
FROM car_makers 
WHERE Country = (SELECT CountryId FROM countries WHERE CountryName = 'france')
```

**First disagreeing instance** `car_1v5081.sqlite`.

Gold returns 1 row(s), 1 column(s):

    6

Returned query gives 1 row(s), 1 column(s):

    4

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C130  (question 90, database `car_1`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed303
- Class mass: 32/50, 25/50
- Instances disagreeing: 18 of 60 (30%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the average edispl of the cars of  volvo?

**Gold.**
```sql
SELECT avg(T2.edispl) FROM CAR_NAMES AS T1 JOIN CARS_DATA AS T2 ON T1.MakeId  =  T2.Id WHERE T1.Model  =  'volvo';
```

**Returned.**
```sql
SELECT AVG(cars_data.Edispl) AS Average_Edispl
FROM car_makers
INNER JOIN model_list ON car_makers.Id = model_list.Maker
INNER JOIN car_names ON model_list.Model = car_names.Model
INNER JOIN cars_data ON car_names.MakeId = cars_data.Id
WHERE car_makers.Maker = 'volvo'
```

**First disagreeing instance** `car_1v50811.sqlite`.

Gold returns 1 row(s), 1 column(s):

    NULL

Returned query gives 1 row(s), 1 column(s):

    436889768.3333333

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C131  (question 96, database `car_1`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed202
- Class mass: 44/50, 47/50
- Instances disagreeing: 8 of 60 (13%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the number of car models created by American Motor Company?

**Gold.**
```sql
SELECT count(*) FROM CAR_MAKERS AS T1 JOIN MODEL_LIST AS T2 ON T1.Id  =  T2.Maker WHERE T1.FullName  =  'American Motor Company';
```

**Returned.**
```sql
SELECT COUNT(*) 
FROM model_list 
WHERE Maker = (SELECT Id FROM car_makers WHERE FullName = 'American Motor Company')
```

**First disagreeing instance** `car_1v5081.sqlite`.

Gold returns 1 row(s), 1 column(s):

    4

Returned query gives 1 row(s), 1 column(s):

    0

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C132  (question 103, database `car_1`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed303
- Class mass: 26/50, 34/50
- Instances disagreeing: 17 of 60 (28%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** For  volvo, how many cylinders does the car with the least accelerate have?

**Gold.**
```sql
SELECT T1.cylinders FROM CARS_DATA AS T1 JOIN CAR_NAMES AS T2 ON T1.Id  =  T2.MakeId WHERE T2.Model  =  'volvo' ORDER BY T1.accelerate ASC LIMIT 1;
```

**Returned.**
```sql
SELECT c.Cylinders
FROM cars_data c
JOIN car_names cn ON c.Id = cn.MakeId
JOIN model_list ml ON cn.Model = ml.Model
JOIN car_makers cm ON ml.Maker = cm.Id
WHERE cm.Maker = 'volvo'
ORDER BY c.Accelerate ASC
LIMIT 1
```

**First disagreeing instance** `car_1v50811.sqlite`.

Gold returns 0 row(s), None column(s):

    (no rows)

Returned query gives 1 row(s), 1 column(s):

    1969

Difference: gold_empty; 0 row(s) in common, 0 only in the gold, 1 only in the returned result.

### C133  (question 104, database `car_1`)

- Returned by: omnisql-32b/seed101
- Class mass: 23/50
- Instances disagreeing: 17 of 60 (28%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** For a volvo , how many cylinders does the version with least accelerate have?

**Gold.**
```sql
SELECT T1.cylinders FROM CARS_DATA AS T1 JOIN CAR_NAMES AS T2 ON T1.Id  =  T2.MakeId WHERE T2.Model  =  'volvo' ORDER BY T1.accelerate ASC LIMIT 1;
```

**Returned.**
```sql
SELECT 
    cars_data.Cylinders
FROM 
    cars_data
INNER JOIN 
    car_names ON cars_data.Id = car_names.MakeId
INNER JOIN 
    model_list ON car_names.Model = model_list.Model
INNER JOIN 
    car_makers ON model_list.Maker = car_makers.Id
WHERE 
    car_makers.Maker = 'volvo'
ORDER BY 
    cars_data.Accelerate ASC
LIMIT 1
```

**First disagreeing instance** `car_1v50811.sqlite`.

Gold returns 0 row(s), None column(s):

    (no rows)

Returned query gives 1 row(s), 1 column(s):

    1969

Difference: gold_empty; 0 row(s) in common, 0 only in the gold, 1 only in the returned result.

### C134  (question 111, database `car_1`)

- Returned by: omnisql-32b/seed101
- Class mass: 34/50
- Instances disagreeing: 20 of 60 (33%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the id and names of the countries which have more than 3 car makers or produce the 'fiat' ?

**Gold.**
```sql
SELECT T1.countryId ,  T1.CountryName FROM Countries AS T1 JOIN CAR_MAKERS AS T2 ON T1.CountryId  =  T2.Country GROUP BY T1.countryId HAVING count(*)  >  3 UNION SELECT T1.countryId ,  T1.CountryName FROM Countries AS T1 JOIN CAR_MAKERS AS T2 ON T1.CountryId  =  T2.Country JOIN MODEL_LIST AS T3 ON T2.Id  =  T3.Maker WHERE T3.Model  =  'fiat';
```

**Returned.**
```sql
SELECT c.CountryId, c.CountryName
FROM countries c
JOIN car_makers cm ON c.CountryId = cm.Country
GROUP BY c.CountryId, c.CountryName
HAVING COUNT(cm.Id) > 3
UNION
SELECT c.CountryId, c.CountryName
FROM countries c
JOIN car_makers cm ON c.CountryId = cm.Country
WHERE cm.Maker = 'fiat'
```

**First disagreeing instance** `car_1v5080.sqlite`.

Gold returns 8 row(s), 2 column(s):

    -4076741865 | us
    10 | Om
    12 | 400
    19 | ford
    151 | buick
    1981 | asia
    8210699449 | 3499
    9236429507 | mc

Returned query gives 9 row(s), 2 column(s):

    -4076741865 | us
    10 | Om
    12 | 400
    19 | ford
    151 | buick
    1969 | france
    1981 | asia
    8210699449 | 3499
    9236429507 | mc

Difference: gold_subset_of_rep; 8 row(s) in common, 0 only in the gold, 1 only in the returned result.

### C135  (question 112, database `car_1`)

- Returned by: omnisql-32b/seed101
- Class mass: 28/50
- Instances disagreeing: 16 of 60 (27%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the ids and names of all countries that either have more than 3 car makers or produce fiats?

**Gold.**
```sql
select t1.countryid ,  t1.countryname from countries as t1 join car_makers as t2 on t1.countryid  =  t2.country group by t1.countryid having count(*)  >  3 union select t1.countryid ,  t1.countryname from countries as t1 join car_makers as t2 on t1.countryid  =  t2.country join model_list as t3 on t2.id  =  t3.maker where t3.model  =  'fiat';
```

**Returned.**
```sql
SELECT 
    C.CountryId, 
    C.CountryName
FROM 
    countries C
JOIN 
    car_makers CM ON C.CountryId = CM.Country
GROUP BY 
    C.CountryId, 
    C.CountryName
HAVING 
    COUNT(*) > 3

UNION

SELECT 
    C.CountryId, 
    C.CountryName
FROM 
    countries C
JOIN 
    car_makers CM ON C.CountryId = CM.Country
JOIN 
    model_list ML ON CM.Id = ML.Maker
WHERE 
    CM.Maker = 'fiat'
```

**First disagreeing instance** `car_1v5080.sqlite`.

Gold returns 8 row(s), 2 column(s):

    -4076741865 | us
    10 | Om
    12 | 400
    19 | ford
    151 | buick
    1981 | asia
    8210699449 | 3499
    9236429507 | mc

Returned query gives 9 row(s), 2 column(s):

    -4076741865 | us
    10 | Om
    12 | 400
    19 | ford
    151 | buick
    1969 | france
    1981 | asia
    8210699449 | 3499
    9236429507 | mc

Difference: gold_subset_of_rep; 8 row(s) in common, 0 only in the gold, 1 only in the returned result.

### C136  (question 137, database `flight_2`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed303
- Class mass: 50/50, 50/50
- Instances disagreeing: 1 of 56 (2%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** How many flights depart from Aberdeen and arrive at Ashley?

**Gold.**
```sql
SELECT count(*) FROM FLIGHTS AS T1 JOIN AIRPORTS AS T2 ON T1.DestAirport  =  T2.AirportCode JOIN AIRPORTS AS T3 ON T1.SourceAirport  =  T3.AirportCode WHERE T2.City  =  "Ashley" AND T3.City  =  "Aberdeen"
```

**Returned.**
```sql
SELECT COUNT(*)
FROM flights
WHERE SourceAirport = (SELECT AirportCode FROM airports WHERE City = 'Aberdeen')
AND DestAirport = (SELECT AirportCode FROM airports WHERE City = 'Ashley')
```

**First disagreeing instance** `flight_2v50814.sqlite`.

Gold returns 1 row(s), 1 column(s):

    1

Returned query gives 1 row(s), 1 column(s):

    0

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C137  (question 147, database `flight_2`)

- Returned by: omnisql-32b/seed101
- Class mass: 50/50
- Instances disagreeing: 4 of 56 (7%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are airlines that have some flight departing from AHD?

**Gold.**
```sql
SELECT T1.Airline FROM AIRLINES AS T1 JOIN FLIGHTS AS T2 ON T1.uid  =  T2.Airline WHERE T2.SourceAirport  =  "AHD"
```

**Returned.**
```sql
SELECT DISTINCT airlines.Airline
FROM flights
JOIN airlines ON flights.Airline = airlines.uid
WHERE flights.SourceAirport = 'AHD'
```

**First disagreeing instance** `flight_2v5081.sqlite`.

Gold returns 2 row(s), 1 column(s):

    Virgin America
    Virgin America

Returned query gives 1 row(s), 1 column(s):

    Virgin America

Difference: duplicate_multiplicity_only; 1 row(s) in common, 0 only in the gold, 0 only in the returned result.

### C138  (question 148, database `flight_2`)

- Returned by: omnisql-32b/seed101
- Class mass: 50/50
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
JOIN airlines ON flights.Airline = airlines.uid
WHERE flights.SourceAirport = 'AHD'
```

**First disagreeing instance** `flight_2v5081.sqlite`.

Gold returns 2 row(s), 1 column(s):

    Virgin America
    Virgin America

Returned query gives 1 row(s), 1 column(s):

    Virgin America

Difference: duplicate_multiplicity_only; 1 row(s) in common, 0 only in the gold, 0 only in the returned result.

### C139  (question 149, database `flight_2`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed303
- Class mass: 50/50, 50/50
- Instances disagreeing: 5 of 56 (9%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are airlines that have flights arriving at AHD?

**Gold.**
```sql
SELECT T1.Airline FROM AIRLINES AS T1 JOIN FLIGHTS AS T2 ON T1.uid  =  T2.Airline WHERE T2.DestAirport  =  "AHD"
```

**Returned.**
```sql
SELECT DISTINCT airlines.Airline
FROM flights
JOIN airlines ON flights.Airline = airlines.uid
WHERE flights.DestAirport = 'AHD'
```

**First disagreeing instance** `flight_2v50814.sqlite`.

Gold returns 5 row(s), 1 column(s):

    ABR
    199ZSJuF
    5UBp(Hl( 
    2
    5UBp(Hl( 

Returned query gives 4 row(s), 1 column(s):

    ABR
    199ZSJuF
    5UBp(Hl( 
    2

Difference: duplicate_multiplicity_only; 4 row(s) in common, 0 only in the gold, 0 only in the returned result.

### C140  (question 151, database `flight_2`)

- Returned by: omnisql-32b/seed101
- Class mass: 50/50
- Instances disagreeing: 4 of 56 (7%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find all airlines that have flights from both APG and CVO.

**Gold.**
```sql
SELECT T1.Airline FROM AIRLINES AS T1 JOIN FLIGHTS AS T2 ON T1.uid  =  T2.Airline WHERE T2.SourceAirport  =  "APG" INTERSECT SELECT T1.Airline FROM AIRLINES AS T1 JOIN FLIGHTS AS T2 ON T1.uid  =  T2.Airline WHERE T2.SourceAirport  =  "CVO"
```

**Returned.**
```sql
SELECT Airline 
FROM flights 
WHERE SourceAirport = 'APG'
INTERSECT
SELECT Airline 
FROM flights 
WHERE SourceAirport = 'CVO'
```

**First disagreeing instance** `flight_2v50814.sqlite`.

Gold returns 1 row(s), 1 column(s):

    5UBp(Hl( 

Returned query gives 1 row(s), 1 column(s):

    11

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C141  (question 152, database `flight_2`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed202, omnisql-32b/seed303
- Class mass: 50/50, 48/49, 49/50
- Instances disagreeing: 4 of 56 (7%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Which airlines have departing flights from both APG and CVO ?

**Gold.**
```sql
SELECT T1.Airline FROM AIRLINES AS T1 JOIN FLIGHTS AS T2 ON T1.uid  =  T2.Airline WHERE T2.SourceAirport  =  "APG" INTERSECT SELECT T1.Airline FROM AIRLINES AS T1 JOIN FLIGHTS AS T2 ON T1.uid  =  T2.Airline WHERE T2.SourceAirport  =  "CVO"
```

**Returned.**
```sql
SELECT Airline
FROM flights
WHERE SourceAirport = 'APG'
INTERSECT
SELECT Airline
FROM flights
WHERE SourceAirport = 'CVO'
```

**First disagreeing instance** `flight_2v50814.sqlite`.

Gold returns 1 row(s), 1 column(s):

    5UBp(Hl( 

Returned query gives 1 row(s), 1 column(s):

    11

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C142  (question 223, database `wta_1`)

- Returned by: omnisql-32b/seed101
- Class mass: 32/50
- Instances disagreeing: 7 of 33 (21%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the names of players who won in both 2013 and 2016?

**Gold.**
```sql
SELECT winner_name FROM matches WHERE YEAR  =  2013 INTERSECT SELECT winner_name FROM matches WHERE YEAR  =  2016
```

**Returned.**
```sql
SELECT p.first_name || ' ' || p.last_name AS player_name
FROM players p
JOIN matches m ON p.player_id = m.winner_id
WHERE m.year = 2013

INTERSECT

SELECT p.first_name || ' ' || p.last_name AS player_name
FROM players p
JOIN matches m ON p.player_id = m.winner_id
WHERE m.year = 2016
```

**First disagreeing instance** `wta_1v5080.sqlite`.

Gold returns 1 row(s), 1 column(s):

    3

Returned query gives 0 row(s), None column(s):

    (no rows)

Difference: rep_empty; 0 row(s) in common, 1 only in the gold, 0 only in the returned result.

### C143  (question 229, database `wta_1`)

- Returned by: omnisql-32b/seed101
- Class mass: 34/50
- Instances disagreeing: 7 of 33 (21%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What is the first name and country code of the oldest player?

**Gold.**
```sql
SELECT first_name ,  country_code FROM players ORDER BY birth_date LIMIT 1
```

**Returned.**
```sql
SELECT first_name, country_code
FROM players
WHERE birth_date = (SELECT MIN(birth_date) FROM players)
```

**First disagreeing instance** `wta_1v50815.sqlite`.

Gold returns 1 row(s), 2 column(s):

    40 | IND

Returned query gives 4 row(s), 2 column(s):

    40 | IND
    Gsb8 | 24.626967830300003vQMaC
    3500 | RCNsvGw
    Ji Su | L

Difference: gold_subset_of_rep; 1 row(s) in common, 0 only in the gold, 3 only in the returned result.

### C144  (question 234, database `wta_1`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed303
- Class mass: 7/50, 14/50
- Instances disagreeing: 32 of 33 (97%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Find the name and rank points of the person who won the most times.

**Gold.**
```sql
SELECT winner_name ,  winner_rank_points FROM matches GROUP BY winner_name ORDER BY count(*) DESC LIMIT 1
```

**Returned.**
```sql
SELECT winner_name, winner_rank_points
FROM matches
GROUP BY winner_id
ORDER BY COUNT(*) DESC
LIMIT 1
```

**First disagreeing instance** `wta_1v5080.sqlite`.

Gold returns 1 row(s), 2 column(s):

    1 | 2841

Returned query gives 1 row(s), 2 column(s):

    2017 | 9

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C145  (question 236, database `wta_1`)

- Returned by: omnisql-32b/seed101
- Class mass: 39/50
- Instances disagreeing: 9 of 33 (27%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Find the name of the winner who has the highest rank points and participated in the Australian Open.

**Gold.**
```sql
SELECT winner_name FROM matches WHERE tourney_name  =  'Australian Open' ORDER BY winner_rank_points DESC LIMIT 1
```

**Returned.**
```sql
SELECT p.first_name || ' ' || p.last_name AS winner_name
FROM matches m
JOIN players p ON m.winner_id = p.player_id
JOIN rankings r ON p.player_id = r.player_id
WHERE m.tourney_name = 'Australian Open'
ORDER BY r.ranking_points DESC
LIMIT 1
```

**First disagreeing instance** `wta_1v5080.sqlite`.

Gold returns 1 row(s), 1 column(s):

    11dVZOO

Returned query gives 1 row(s), 1 column(s):

    R 19

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C146  (question 237, database `wta_1`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed303
- Class mass: 43/50, 41/50
- Instances disagreeing: 9 of 33 (27%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What is the name of the winner with the most rank points who participated in the Australian Open?

**Gold.**
```sql
SELECT winner_name FROM matches WHERE tourney_name  =  'Australian Open' ORDER BY winner_rank_points DESC LIMIT 1
```

**Returned.**
```sql
SELECT p.first_name || ' ' || p.last_name AS winner_name
FROM matches m
JOIN players p ON m.winner_id = p.player_id
WHERE m.tourney_name = 'Australian Open'
ORDER BY m.winner_rank_points DESC
LIMIT 1
```

**First disagreeing instance** `wta_1v5080.sqlite`.

Gold returns 1 row(s), 1 column(s):

    11dVZOO

Returned query gives 1 row(s), 1 column(s):

    200001 10

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C147  (question 248, database `wta_1`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed202, omnisql-32b/seed303
- Class mass: 50/50, 50/50, 49/50
- Instances disagreeing: 6 of 33 (18%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** How many different winners both participated in the WTA Championships and were left handed?

**Gold.**
```sql
SELECT count(DISTINCT winner_name) FROM matches WHERE tourney_name  =  'WTA Championships' AND winner_hand  =  'L'
```

**Returned.**
```sql
SELECT COUNT(DISTINCT m.winner_id)
FROM matches m
JOIN players p ON m.winner_id = p.player_id
WHERE m.tourney_name = 'WTA Championships' AND p.hand = 'L'
```

**First disagreeing instance** `wta_1v50815.sqlite`.

Gold returns 1 row(s), 1 column(s):

    4

Returned query gives 1 row(s), 1 column(s):

    0

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C148  (question 249, database `wta_1`)

- Returned by: omnisql-32b/seed101
- Class mass: 34/50
- Instances disagreeing: 2 of 33 (6%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find the number of left handed winners who participated in the WTA Championships.

**Gold.**
```sql
SELECT count(DISTINCT winner_name) FROM matches WHERE tourney_name  =  'WTA Championships' AND winner_hand  =  'L'
```

**Returned.**
```sql
SELECT COUNT(DISTINCT winner_id) AS left_handed_winners
FROM matches
WHERE tourney_name = 'WTA Championships' AND winner_hand = 'L'
```

**First disagreeing instance** `wta_1v5085.sqlite`.

Gold returns 1 row(s), 1 column(s):

    6

Returned query gives 1 row(s), 1 column(s):

    7

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C149  (question 253, database `battle_death`)

- Returned by: omnisql-32b/seed101
- Class mass: 31/50
- Instances disagreeing: 16 of 28 (57%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** List the name and date the battle that has lost  Lettice and HMS Atalanta

**Gold.**
```sql
SELECT T1.name ,  T1.date FROM battle AS T1 JOIN ship AS T2 ON T1.id  =  T2.lost_in_battle WHERE T2.name  =  'Lettice' INTERSECT SELECT T1.name ,  T1.date FROM battle AS T1 JOIN ship AS T2 ON T1.id  =  T2.lost_in_battle WHERE T2.name  =  'HMS Atalanta'
```

**Returned.**
```sql
SELECT DISTINCT battle.name, battle.date
FROM battle
INNER JOIN ship ON battle.id = ship.lost_in_battle
WHERE ship.name IN ('Lettice', 'HMS Atalanta')
```

**First disagreeing instance** `battle_deathv5080.sqlite`.

Gold returns 0 row(s), None column(s):

    (no rows)

Returned query gives 11 row(s), 2 column(s):

    1SjnDEnglish Channel | Boril
    %East% | TKJ
    hZDqJBattle of Serres | %East%
    5VU7TUgfOgqy79 | X
    Baldwin I | 1235
    English Channe | C1pIqw(
    2 | 2
    Kaloyan | English Channel
    224 | 8zV0f11
    June 1205 | vSDpp0WuPy51oJz5
    Battle of Boruy | June 1205

Difference: gold_empty; 0 row(s) in common, 0 only in the gold, 11 only in the returned result.

### C150  (question 254, database `battle_death`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed202, omnisql-32b/seed303
- Class mass: 26/50, 24/50, 25/50
- Instances disagreeing: 17 of 28 (61%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Show names, results and bulgarian commanders of the battles with no ships lost in the 'English Channel'.

**Gold.**
```sql
SELECT name ,  RESULT ,  bulgarian_commander FROM battle EXCEPT SELECT T1.name ,  T1.result ,  T1.bulgarian_commander FROM battle AS T1 JOIN ship AS T2 ON T1.id  =  T2.lost_in_battle WHERE T2.location  =  'English Channel'
```

**Returned.**
```sql
SELECT 
    name, 
    result, 
    bulgarian_commander 
FROM 
    battle 
WHERE 
    id NOT IN (
        SELECT 
            lost_in_battle 
        FROM 
            ship 
        WHERE 
            location = 'English Channel'
    )
```

**First disagreeing instance** `battle_deathv5083735.sqlite`.

Gold returns 217 row(s), 3 column(s):

     | (HQyWVu58Kg | oY7KaloyanbWa
     | East% | Kaloyan
     | USYHTLatin victory | Unknown
     nqqY0tt4ldRt | East | EPs%East%lSA
    %East% | Brig | jT43P3Q
    %East% | Bulgarian victory | 
    %East% | East | Brig
    %East% | Latin victory | %East%
    %East% | Latin victory | t
    %East% | Pp1t(Ub | %East%
    %East% | Two Year Truce | Brig
    %East% | Two Year Truce | Unknown
    ... (217 rows total)

Returned query gives 225 row(s), 3 column(s):

    Battle of Adrianople | Bulgarian victory | Kaloyan
    East | wo Year Truce | Kaloyan
    Battle of Adrianople | t | East
    ymM7A | Bulgarian victory | East
    East | Eas | RezWT
    zr4Battle of SerresA 3 | 3Cm96bVBQ0GUb | Kaloyan
    Battle of Boruy | Bulgarian victory | Kaloyan
    Battle of Adrianople | Bulgarian victory | (Pf
    Battle of Messinopolis | Brig | Kaloyan
    ZNp1 7dlN 0aKhDewen2w)y( | 0 da)sqf4Q D8s4 | bNCKaloyang6y
    Brig | Latin victory | L0I)
    RNQOdgPlRkGEFZLdQbw | Latin victory | jG3 Bgh
    ... (225 rows total)

Difference: duplicate_multiplicity_only; 217 row(s) in common, 0 only in the gold, 0 only in the returned result.

### C151  (question 307, database `tvshow`)

- Returned by: omnisql-32b/seed101
- Class mass: 50/50
- Instances disagreeing: 11 of 25 (44%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** which countries' tv channels are playing some cartoon  Todd Casey writes?

**Gold.**
```sql
SELECT T1.country FROM TV_Channel AS T1 JOIN cartoon AS T2 ON T1.id = T2.Channel WHERE T2.written_by  =  'Todd Casey'
```

**Returned.**
```sql
SELECT DISTINCT TV_Channel.Country
FROM TV_Channel
INNER JOIN Cartoon ON TV_Channel.id = Cartoon.Channel
WHERE Cartoon.Written_by = 'Todd Casey'
```

**First disagreeing instance** `tvshowv5081.sqlite`.

Gold returns 8 row(s), 1 column(s):

    Todd Casey neY1
    Italy
    Todd Casey
    Italy
    yes
    Italy
    zk9GuItaly
    Italy

Returned query gives 5 row(s), 1 column(s):

    Todd Casey neY1
    Italy
    Todd Casey
    yes
    zk9GuItaly

Difference: duplicate_multiplicity_only; 5 row(s) in common, 0 only in the gold, 0 only in the returned result.

### C152  (question 308, database `tvshow`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed202, omnisql-32b/seed303
- Class mass: 50/50, 50/50, 50/50
- Instances disagreeing: 11 of 25 (44%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the countries that have cartoons on TV that Todd Casey writes?

**Gold.**
```sql
SELECT T1.country FROM TV_Channel AS T1 JOIN cartoon AS T2 ON T1.id = T2.Channel WHERE T2.written_by  =  'Todd Casey'
```

**Returned.**
```sql
SELECT DISTINCT TV_Channel.Country
FROM Cartoon
INNER JOIN TV_Channel ON Cartoon.Channel = TV_Channel.id
WHERE Cartoon.Written_by = 'Todd Casey'
```

**First disagreeing instance** `tvshowv5081.sqlite`.

Gold returns 8 row(s), 1 column(s):

    Todd Casey neY1
    Italy
    Todd Casey
    Italy
    yes
    Italy
    zk9GuItaly
    Italy

Returned query gives 5 row(s), 1 column(s):

    Todd Casey neY1
    Italy
    Todd Casey
    yes
    zk9GuItaly

Difference: duplicate_multiplicity_only; 5 row(s) in common, 0 only in the gold, 0 only in the returned result.

### C153  (question 374, database `world_1`)

- Returned by: omnisql-32b/seed101
- Class mass: 45/50
- Instances disagreeing: 9 of 46 (20%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the names of nations speak both English and French?

**Gold.**
```sql
SELECT T1.Name FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code  =  T2.CountryCode WHERE T2.Language  =  "English" INTERSECT SELECT T1.Name FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code  =  T2.CountryCode WHERE T2.Language  =  "French"
```

**Returned.**
```sql
SELECT Name
FROM country
WHERE Code IN (
    SELECT CountryCode
    FROM countrylanguage
    WHERE Language = 'English'
    INTERSECT
    SELECT CountryCode
    FROM countrylanguage
    WHERE Language = 'French'
)
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

### C154  (question 375, database `world_1`)

- Returned by: omnisql-32b/seed101
- Class mass: 49/49
- Instances disagreeing: 9 of 46 (20%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Give the names of nations that speak both English and French.

**Gold.**
```sql
SELECT T1.Name FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code  =  T2.CountryCode WHERE T2.Language  =  "English" INTERSECT SELECT T1.Name FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code  =  T2.CountryCode WHERE T2.Language  =  "French"
```

**Returned.**
```sql
SELECT Name
FROM country
WHERE Code IN (
    SELECT CountryCode
    FROM countrylanguage
    WHERE Language = 'English'
    INTERSECT
    SELECT CountryCode
    FROM countrylanguage
    WHERE Language = 'French'
)
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

### C155  (question 392, database `world_1`)

- Returned by: omnisql-32b/seed101
- Class mass: 32/50
- Instances disagreeing: 39 of 46 (85%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the total number of people living in the nations that do not use English?

**Gold.**
```sql
SELECT sum(Population) FROM country WHERE Name NOT IN (SELECT T1.Name FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code  =  T2.CountryCode WHERE T2.Language  =  "English")
```

**Returned.**
```sql
SELECT SUM(Population) 
FROM country 
WHERE Code NOT IN (
    SELECT CountryCode 
    FROM countrylanguage 
    WHERE Language = 'English'
)
```

**First disagreeing instance** `world_1v5080.sqlite`.

Gold returns 1 row(s), 1 column(s):

    268945194457

Returned query gives 1 row(s), 1 column(s):

    273514308785

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C156  (question 393, database `world_1`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed202, omnisql-32b/seed303
- Class mass: 33/49, 31/50, 31/50
- Instances disagreeing: 39 of 46 (85%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** How many people live in countries that do not speak English?

**Gold.**
```sql
SELECT sum(Population) FROM country WHERE Name NOT IN (SELECT T1.Name FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code  =  T2.CountryCode WHERE T2.Language  =  "English")
```

**Returned.**
```sql
SELECT SUM(Population)
FROM country
WHERE Code NOT IN (
    SELECT CountryCode
    FROM countrylanguage
    WHERE Language = 'English'
)
```

**First disagreeing instance** `world_1v5080.sqlite`.

Gold returns 1 row(s), 1 column(s):

    268945194457

Returned query gives 1 row(s), 1 column(s):

    273514308785

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C157  (question 429, database `world_1`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed202, omnisql-32b/seed303
- Class mass: 50/50, 50/50, 50/50
- Instances disagreeing: 38 of 46 (83%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the cities who have more than 160000 people and less than 900000 people?

**Gold.**
```sql
SELECT name FROM city WHERE Population BETWEEN 160000 AND 900000
```

**Returned.**
```sql
SELECT Name 
FROM city 
WHERE Population > 160000 AND Population < 900000
```

**First disagreeing instance** `world_1v5080.sqlite`.

Gold returns 3 row(s), 1 column(s):

    vsgTbpN
    Jql900001MwW
    930

Returned query gives 1 row(s), 1 column(s):

    Jql900001MwW

Difference: rep_subset_of_gold; 1 row(s) in common, 2 only in the gold, 0 only in the returned result.

### C158  (question 455, database `network_1`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed202, omnisql-32b/seed303
- Class mass: 50/50, 48/50, 49/50
- Instances disagreeing: 22 of 29 (76%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Show the names of all of Kyle's friends.

**Gold.**
```sql
SELECT T3.name FROM Friend AS T1 JOIN Highschooler AS T2 ON T1.student_id  =  T2.id JOIN Highschooler AS T3 ON T1.friend_id  =  T3.id WHERE T2.name  =  "Kyle"
```

**Returned.**
```sql
SELECT name
FROM Highschooler
WHERE ID IN (
    SELECT friend_id
    FROM Friend
    WHERE student_id = (
        SELECT ID
        FROM Highschooler
        WHERE name = 'Kyle'
    )
)
```

**First disagreeing instance** `network_1v5080.sqlite`.

Gold returns 19 row(s), 1 column(s):

    1
    pN
    
    1709
    2
    Haley
    168
    KMV
    1542A1510
    Gabrie
    8
    We
    ... (19 rows total)

Returned query gives 1 row(s), 1 column(s):

    3

Difference: rep_subset_of_gold; 1 row(s) in common, 18 only in the gold, 0 only in the returned result.

### C159  (question 457, database `network_1`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed303
- Class mass: 45/50, 42/50
- Instances disagreeing: 22 of 29 (76%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** How many friends does Kyle have?

**Gold.**
```sql
SELECT count(*) FROM Friend AS T1 JOIN Highschooler AS T2 ON T1.student_id  =  T2.id WHERE T2.name  =  "Kyle"
```

**Returned.**
```sql
SELECT COUNT(*) AS friend_count
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

### C160  (question 458, database `network_1`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed202, omnisql-32b/seed303
- Class mass: 49/50, 43/50, 42/50
- Instances disagreeing: 22 of 29 (76%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Count the number of friends Kyle has.

**Gold.**
```sql
SELECT count(*) FROM Friend AS T1 JOIN Highschooler AS T2 ON T1.student_id  =  T2.id WHERE T2.name  =  "Kyle"
```

**Returned.**
```sql
SELECT COUNT(*) 
FROM Friend 
WHERE student_id = (SELECT ID FROM Highschooler WHERE name = 'Kyle')
```

**First disagreeing instance** `network_1v5080.sqlite`.

Gold returns 1 row(s), 1 column(s):

    19

Returned query gives 1 row(s), 1 column(s):

    1

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C161  (question 459, database `network_1`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed303
- Class mass: 50/50, 49/50
- Instances disagreeing: 24 of 29 (83%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** How many likes does Kyle have?

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

### C162  (question 460, database `network_1`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed202
- Class mass: 50/50, 49/50
- Instances disagreeing: 24 of 29 (83%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Return the number of likes Kyle has.

**Gold.**
```sql
SELECT count(*) FROM Likes AS T1 JOIN Highschooler AS T2 ON T1.student_id  =  T2.id WHERE T2.name  =  "Kyle"
```

**Returned.**
```sql
SELECT COUNT(*) 
FROM Likes 
WHERE liked_id = (SELECT ID FROM Highschooler WHERE name = 'Kyle')
```

**First disagreeing instance** `network_1v5080.sqlite`.

Gold returns 1 row(s), 1 column(s):

    21

Returned query gives 1 row(s), 1 column(s):

    4

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C163  (question 468, database `dog_kennels`)

- Returned by: omnisql-32b/seed101
- Class mass: 26/50
- Instances disagreeing: 22 of 48 (46%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Which person has the most dogs? List the id, first name and last name.

**Gold.**
```sql
SELECT T1.owner_id ,  T2.first_name ,  T2.last_name FROM Dogs AS T1 JOIN Owners AS T2 ON T1.owner_id  =  T2.owner_id GROUP BY T1.owner_id ORDER BY count(*) DESC LIMIT 1
```

**Returned.**
```sql
SELECT o.owner_id, o.first_name, o.last_name
FROM Owners o
JOIN Dogs d ON o.owner_id = d.owner_id
GROUP BY o.owner_id, o.first_name, o.last_name
ORDER BY COUNT(d.dog_id) DESC
LIMIT 1
```

**First disagreeing instance** `dog_kennelsv5080.sqlite`.

Gold returns 1 row(s), 3 column(s):

    7994075702 | 501 | qwM)4Jaclyn

Returned query gives 1 row(s), 3 column(s):

    999 | bPG%West%CRw | 0

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C164  (question 469, database `dog_kennels`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed202, omnisql-32b/seed303
- Class mass: 40/50, 42/50, 43/50
- Instances disagreeing: 22 of 48 (46%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Return the id, first name and last name of the person who has the most dogs.

**Gold.**
```sql
SELECT T1.owner_id ,  T2.first_name ,  T2.last_name FROM Dogs AS T1 JOIN Owners AS T2 ON T1.owner_id  =  T2.owner_id GROUP BY T1.owner_id ORDER BY count(*) DESC LIMIT 1
```

**Returned.**
```sql
SELECT o.owner_id, o.first_name, o.last_name
FROM Owners o
JOIN Dogs d ON o.owner_id = d.owner_id
GROUP BY o.owner_id, o.first_name, o.last_name
ORDER BY COUNT(d.dog_id) DESC
LIMIT 1
```

**First disagreeing instance** `dog_kennelsv5080.sqlite`.

Gold returns 1 row(s), 3 column(s):

    7994075702 | 501 | qwM)4Jaclyn

Returned query gives 1 row(s), 3 column(s):

    999 | bPG%West%CRw | 0

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C165  (question 472, database `dog_kennels`)

- Returned by: omnisql-32b/seed101
- Class mass: 49/50
- Instances disagreeing: 4 of 48 (8%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What is the description of the treatment type that is the cheapest overall?

**Gold.**
```sql
SELECT T1.treatment_type_description FROM Treatment_types AS T1 JOIN Treatments AS T2 ON T1.treatment_type_code  =  T2.treatment_type_code GROUP BY T1.treatment_type_code ORDER BY sum(cost_of_treatment) ASC LIMIT 1
```

**Returned.**
```sql
SELECT
    tt.treatment_type_description
FROM
    Treatments t
JOIN
    Treatment_Types tt ON t.treatment_type_code = tt.treatment_type_code
GROUP BY
    t.treatment_type_code, tt.treatment_type_description
ORDER BY
    AVG(t.cost_of_treatment) ASC
LIMIT 1
```

**First disagreeing instance** `dog_kennelsv5082.sqlite`.

Gold returns 1 row(s), 1 column(s):

    Vaccination

Returned query gives 1 row(s), 1 column(s):

    999

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C166  (question 473, database `dog_kennels`)

- Returned by: omnisql-32b/seed101
- Class mass: 48/50
- Instances disagreeing: 17 of 48 (35%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Give me the description of the treatment type that is least expensive.

**Gold.**
```sql
SELECT T1.treatment_type_description FROM Treatment_types AS T1 JOIN Treatments AS T2 ON T1.treatment_type_code  =  T2.treatment_type_code GROUP BY T1.treatment_type_code ORDER BY sum(cost_of_treatment) ASC LIMIT 1
```

**Returned.**
```sql
SELECT tt.treatment_type_description
FROM Treatment_Types tt
JOIN Treatments t ON tt.treatment_type_code = t.treatment_type_code
WHERE t.cost_of_treatment = (
    SELECT MIN(cost_of_treatment)
    FROM Treatments
)
```

**First disagreeing instance** `dog_kennelsv5081.sqlite`.

Gold returns 1 row(s), 1 column(s):

    QOY2(500

Returned query gives 4 row(s), 1 column(s):

    2
    North
    QOY2(500
    Virginia

Difference: gold_subset_of_rep; 1 row(s) in common, 0 only in the gold, 3 only in the returned result.

### C167  (question 474, database `dog_kennels`)

- Returned by: omnisql-32b/seed101
- Class mass: 19/50
- Instances disagreeing: 1 of 48 (2%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Who has paid the largest amount of money in total for their dogs? Show the id and zip code.

**Gold.**
```sql
SELECT T1.owner_id ,  T1.zip_code FROM Owners AS T1 JOIN Dogs AS T2 ON T1.owner_id  =  T2.owner_id JOIN Treatments AS T3 ON T2.dog_id  =  T3.dog_id GROUP BY T1.owner_id ORDER BY sum(T3.cost_of_treatment) DESC LIMIT 1
```

**Returned.**
```sql
SELECT o.owner_id, o.zip_code
FROM Owners o
JOIN Dogs d ON o.owner_id = d.owner_id
JOIN Treatments t ON d.dog_id = t.dog_id
GROUP BY o.owner_id, o.zip_code
ORDER BY SUM(t.cost_of_treatment) DESC
LIMIT 1
```

**First disagreeing instance** `dog_kennelsv508557.sqlite`.

Gold returns 1 row(s), 2 column(s):

    3501605851 | %West%

Returned query gives 1 row(s), 2 column(s):

    348300858 | 90RK2Uq

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C168  (question 475, database `dog_kennels`)

- Returned by: omnisql-32b/seed101, omnisql-32b/seed202, omnisql-32b/seed303
- Class mass: 35/50, 35/50, 30/50
- Instances disagreeing: 1 of 48 (2%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Find the id and zip code of the person who spent the most money in total for his or her dogs.

**Gold.**
```sql
SELECT T1.owner_id ,  T1.zip_code FROM Owners AS T1 JOIN Dogs AS T2 ON T1.owner_id  =  T2.owner_id JOIN Treatments AS T3 ON T2.dog_id  =  T3.dog_id GROUP BY T1.owner_id ORDER BY sum(T3.cost_of_treatment) DESC LIMIT 1
```

**Returned.**
```sql
SELECT o.owner_id, o.zip_code
FROM Owners o
JOIN Dogs d ON o.owner_id = d.owner_id
JOIN Treatments t ON d.dog_id = t.dog_id
GROUP BY o.owner_id, o.zip_code
ORDER BY SUM(t.cost_of_treatment) DESC
LIMIT 1
```

**First disagreeing instance** `dog_kennelsv508557.sqlite`.

Gold returns 1 row(s), 2 column(s):

    3501605851 | %West%

Returned query gives 1 row(s), 2 column(s):

    348300858 | 90RK2Uq

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C169  (question 15, database `concert_singer`)

- Returned by: omnisql-32b/seed202
- Class mass: 40/50
- Instances disagreeing: 7 of 32 (22%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Show the stadium name and capacity with most number of concerts in  2014 or after.

**Gold.**
```sql
SELECT T2.name ,  T2.capacity FROM concert AS T1 JOIN stadium AS T2 ON T1.stadium_id  =  T2.stadium_id WHERE T1.year  >=  2014 GROUP BY T2.stadium_id ORDER BY count(*) DESC LIMIT 1
```

**Returned.**
```sql
SELECT 
    stadium.Name, 
    stadium.Capacity
FROM 
    concert
INNER JOIN 
    stadium 
ON 
    concert.Stadium_ID = stadium.Stadium_ID
WHERE 
    concert.Year >= 2014
GROUP BY 
    concert.Stadium_ID
ORDER BY 
    COUNT(*) DESC
LIMIT 1
```

**First disagreeing instance** `concert_singertest0.sqlite`.

Gold returns 1 row(s), 2 column(s):

    0 | 0

Returned query gives 1 row(s), 2 column(s):

    20 | 8774077902

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C170  (question 20, database `concert_singer`)

- Returned by: omnisql-32b/seed202
- Class mass: 48/50
- Instances disagreeing: 29 of 32 (91%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Show names for all stadiums except for stadiums having a concert in  2014.

**Gold.**
```sql
SELECT name FROM stadium EXCEPT SELECT T2.name FROM concert AS T1 JOIN stadium AS T2 ON T1.stadium_id  =  T2.stadium_id WHERE T1.year  =  2014
```

**Returned.**
```sql
SELECT Name
FROM stadium
WHERE Stadium_ID NOT IN (
    SELECT Stadium_ID
    FROM concert
    WHERE Year = 2014
)
```

**First disagreeing instance** `concert_singertest0.sqlite`.

Gold returns 14 row(s), 1 column(s):

    )uFP
    03RZUfj(bwx UE
    19
    2h52O0
    Be(
    Recreation Par
    RvI8xFrance
    V2z20hJn
    cmrzmn3fEIv4v2)r
    kHG1vmsN
    lJojzlh5tVtfoa)
    mC
    ... (14 rows total)

Returned query gives 38 row(s), 1 column(s):

    Recreation Park
    20
    2
    20
    France
    Glebe Park
    2
    Recreation Park
    2h52O0
    0
    2
    )uFP
    ... (38 rows total)

Difference: gold_subset_of_rep; 14 row(s) in common, 0 only in the gold, 9 only in the returned result.

### C171  (question 43, database `pets_1`)

- Returned by: omnisql-32b/seed202
- Class mass: 49/50
- Instances disagreeing: 23 of 27 (85%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find the name of students who have both cat and dog.

**Gold.**
```sql
select t1.fname from student as t1 join has_pet as t2 on t1.stuid  =  t2.stuid join pets as t3 on t3.petid  =  t2.petid where t3.pettype  =  'cat' intersect select t1.fname from student as t1 join has_pet as t2 on t1.stuid  =  t2.stuid join pets as t3 on t3.petid  =  t2.petid where t3.pettype  =  'dog'
```

**Returned.**
```sql
SELECT S.Fname, S.LName
FROM Student S
INNER JOIN Has_Pet HP ON S.StuID = HP.StuID
INNER JOIN Pets P ON HP.PetID = P.PetID
WHERE P.PetType = 'cat'

INTERSECT

SELECT S.Fname, S.LName
FROM Student S
INNER JOIN Has_Pet HP ON S.StuID = HP.StuID
INNER JOIN Pets P ON HP.PetID = P.PetID
WHERE P.PetType = 'dog'
```

**First disagreeing instance** `pets_1v5080.sqlite`.

Gold returns 5 row(s), 1 column(s):

    0
    003
    10
    David
    Oy01U(d

Returned query gives 4 row(s), 2 column(s):

    0 | 9
    003 | 10
    David | Linda
    Oy01U(d | AilCTbfL

Difference: col_count_differs, disjoint; 0 row(s) in common, 5 only in the gold, 4 only in the returned result.

### C172  (question 71, database `car_1`)

- Returned by: omnisql-32b/seed202
- Class mass: 50/50
- Instances disagreeing: 57 of 60 (95%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** How many car models are produced by each manufacturer? List the count and the maker full name.

**Gold.**
```sql
select count(*) ,  t2.fullname from model_list as t1 join car_makers as t2 on t1.maker  =  t2.id group by t2.id;
```

**Returned.**
```sql
SELECT COUNT(model_list.Model) AS ModelCount, car_makers.FullName
FROM car_makers
JOIN model_list ON car_makers.Id = model_list.Maker
GROUP BY car_makers.FullName
```

**First disagreeing instance** `car_1v5080.sqlite`.

Gold returns 32 row(s), 2 column(s):

    1 | WgId2j2tiOKXNbJE)
    1 | 19.0
    1 | 4
    1 | 3
    1 | 5
    1 | eugeaut
    2 | ER5Km8gHv9Mtc9w6Jlv
    1 | General Motors
    2 | JS8WGkUpkQNRnwpw
    1 | 9
    2 | 151
    1 | fia
    ... (32 rows total)

Returned query gives 28 row(s), 2 column(s):

    3 | 
    2 | 0qSpYywiWEZMmhE9zCeNGcUo5Y
    1 | 0xIjVZ
    1 | 1
    2 | 151
    1 | 19.0
    1 | 1975
    2 | 3
    1 | 3499
    1 | 4
    1 | 4000N1f3g
    3 | 5
    ... (28 rows total)

Difference: values differ; 24 row(s) in common, 6 only in the gold, 4 only in the returned result.

### C173  (question 90, database `car_1`)

- Returned by: omnisql-32b/seed202
- Class mass: 19/50
- Instances disagreeing: 18 of 60 (30%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the average edispl of the cars of  volvo?

**Gold.**
```sql
SELECT avg(T2.edispl) FROM CAR_NAMES AS T1 JOIN CARS_DATA AS T2 ON T1.MakeId  =  T2.Id WHERE T1.Model  =  'volvo';
```

**Returned.**
```sql
SELECT AVG(cars_data.Edispl) AS AverageEdispl
FROM car_makers
INNER JOIN model_list ON car_makers.Id = model_list.Maker
INNER JOIN car_names ON model_list.Model = car_names.Model
INNER JOIN cars_data ON car_names.MakeId = cars_data.Id
WHERE car_makers.Maker = 'volvo'
```

**First disagreeing instance** `car_1v50811.sqlite`.

Gold returns 1 row(s), 1 column(s):

    NULL

Returned query gives 1 row(s), 1 column(s):

    436889768.3333333

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C174  (question 103, database `car_1`)

- Returned by: omnisql-32b/seed202
- Class mass: 27/50
- Instances disagreeing: 17 of 60 (28%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** For  volvo, how many cylinders does the car with the least accelerate have?

**Gold.**
```sql
SELECT T1.cylinders FROM CARS_DATA AS T1 JOIN CAR_NAMES AS T2 ON T1.Id  =  T2.MakeId WHERE T2.Model  =  'volvo' ORDER BY T1.accelerate ASC LIMIT 1;
```

**Returned.**
```sql
SELECT cd.Cylinders
FROM car_makers cm
JOIN model_list ml ON cm.Id = ml.Maker
JOIN car_names cn ON ml.Model = cn.Model
JOIN cars_data cd ON cn.MakeId = cd.Id
WHERE cm.Maker = 'volvo'
ORDER BY cd.Accelerate ASC
LIMIT 1
```

**First disagreeing instance** `car_1v50811.sqlite`.

Gold returns 0 row(s), None column(s):

    (no rows)

Returned query gives 1 row(s), 1 column(s):

    1969

Difference: gold_empty; 0 row(s) in common, 0 only in the gold, 1 only in the returned result.

### C175  (question 104, database `car_1`)

- Returned by: omnisql-32b/seed202, omnisql-32b/seed303
- Class mass: 26/50, 30/50
- Instances disagreeing: 17 of 60 (28%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** For a volvo , how many cylinders does the version with least accelerate have?

**Gold.**
```sql
SELECT T1.cylinders FROM CARS_DATA AS T1 JOIN CAR_NAMES AS T2 ON T1.Id  =  T2.MakeId WHERE T2.Model  =  'volvo' ORDER BY T1.accelerate ASC LIMIT 1;
```

**Returned.**
```sql
SELECT 
    cars_data.Cylinders
FROM 
    car_makers
INNER JOIN 
    model_list ON car_makers.Id = model_list.Maker
INNER JOIN 
    car_names ON model_list.Model = car_names.Model
INNER JOIN 
    cars_data ON car_names.MakeId = cars_data.Id
WHERE 
    car_makers.Maker = 'volvo'
ORDER BY 
    cars_data.Accelerate ASC
LIMIT 1
```

**First disagreeing instance** `car_1v50811.sqlite`.

Gold returns 0 row(s), None column(s):

    (no rows)

Returned query gives 1 row(s), 1 column(s):

    1969

Difference: gold_empty; 0 row(s) in common, 0 only in the gold, 1 only in the returned result.

### C176  (question 111, database `car_1`)

- Returned by: omnisql-32b/seed202
- Class mass: 40/50
- Instances disagreeing: 20 of 60 (33%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the id and names of the countries which have more than 3 car makers or produce the 'fiat' ?

**Gold.**
```sql
SELECT T1.countryId ,  T1.CountryName FROM Countries AS T1 JOIN CAR_MAKERS AS T2 ON T1.CountryId  =  T2.Country GROUP BY T1.countryId HAVING count(*)  >  3 UNION SELECT T1.countryId ,  T1.CountryName FROM Countries AS T1 JOIN CAR_MAKERS AS T2 ON T1.CountryId  =  T2.Country JOIN MODEL_LIST AS T3 ON T2.Id  =  T3.Maker WHERE T3.Model  =  'fiat';
```

**Returned.**
```sql
SELECT c.CountryId, c.CountryName
FROM countries c
JOIN car_makers cm ON c.CountryId = cm.Country
GROUP BY c.CountryId, c.CountryName
HAVING COUNT(cm.Id) > 3

UNION

SELECT c.CountryId, c.CountryName
FROM countries c
JOIN car_makers cm ON c.CountryId = cm.Country
WHERE cm.Maker = 'fiat'
```

**First disagreeing instance** `car_1v5080.sqlite`.

Gold returns 8 row(s), 2 column(s):

    -4076741865 | us
    10 | Om
    12 | 400
    19 | ford
    151 | buick
    1981 | asia
    8210699449 | 3499
    9236429507 | mc

Returned query gives 9 row(s), 2 column(s):

    -4076741865 | us
    10 | Om
    12 | 400
    19 | ford
    151 | buick
    1969 | france
    1981 | asia
    8210699449 | 3499
    9236429507 | mc

Difference: gold_subset_of_rep; 8 row(s) in common, 0 only in the gold, 1 only in the returned result.

### C177  (question 112, database `car_1`)

- Returned by: omnisql-32b/seed202
- Class mass: 30/50
- Instances disagreeing: 20 of 60 (33%)
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
JOIN 
    car_makers cm ON c.CountryId = cm.Country
GROUP BY 
    c.CountryId, 
    c.CountryName
HAVING 
    COUNT(cm.Id) > 3
UNION
SELECT 
    c.CountryId, 
    c.CountryName 
FROM 
    countries c
JOIN 
    car_makers cm ON c.CountryId = cm.Country
WHERE 
    cm.Maker = 'fiat'
```

**First disagreeing instance** `car_1v5080.sqlite`.

Gold returns 8 row(s), 2 column(s):

    -4076741865 | us
    10 | Om
    12 | 400
    19 | ford
    151 | buick
    1981 | asia
    8210699449 | 3499
    9236429507 | mc

Returned query gives 9 row(s), 2 column(s):

    -4076741865 | us
    10 | Om
    12 | 400
    19 | ford
    151 | buick
    1969 | france
    1981 | asia
    8210699449 | 3499
    9236429507 | mc

Difference: gold_subset_of_rep; 8 row(s) in common, 0 only in the gold, 1 only in the returned result.

### C178  (question 133, database `flight_2`)

- Returned by: omnisql-32b/seed202
- Class mass: 50/50
- Instances disagreeing: 43 of 56 (77%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** How many flights depart from Aberdeen?

**Gold.**
```sql
SELECT count(*) FROM FLIGHTS AS T1 JOIN AIRPORTS AS T2 ON T1.SourceAirport  =  T2.AirportCode WHERE T2.City  =  "Aberdeen"
```

**Returned.**
```sql
SELECT COUNT(*) 
FROM flights 
WHERE SourceAirport = (SELECT AirportCode FROM airports WHERE City = 'Aberdeen')
```

**First disagreeing instance** `flight_2v5080.sqlite`.

Gold returns 1 row(s), 1 column(s):

    22

Returned query gives 1 row(s), 1 column(s):

    0

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C179  (question 137, database `flight_2`)

- Returned by: omnisql-32b/seed202
- Class mass: 50/50
- Instances disagreeing: 1 of 56 (2%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** How many flights depart from Aberdeen and arrive at Ashley?

**Gold.**
```sql
SELECT count(*) FROM FLIGHTS AS T1 JOIN AIRPORTS AS T2 ON T1.DestAirport  =  T2.AirportCode JOIN AIRPORTS AS T3 ON T1.SourceAirport  =  T3.AirportCode WHERE T2.City  =  "Ashley" AND T3.City  =  "Aberdeen"
```

**Returned.**
```sql
SELECT COUNT(*) 
FROM flights 
WHERE SourceAirport = (SELECT AirportCode FROM airports WHERE City = 'Aberdeen') 
  AND DestAirport = (SELECT AirportCode FROM airports WHERE City = 'Ashley')
```

**First disagreeing instance** `flight_2v50814.sqlite`.

Gold returns 1 row(s), 1 column(s):

    1

Returned query gives 1 row(s), 1 column(s):

    0

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C180  (question 138, database `flight_2`)

- Returned by: omnisql-32b/seed202, omnisql-32b/seed303
- Class mass: 50/50, 50/50
- Instances disagreeing: 1 of 56 (2%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** How many flights fly from Aberdeen to Ashley?

**Gold.**
```sql
SELECT count(*) FROM FLIGHTS AS T1 JOIN AIRPORTS AS T2 ON T1.DestAirport  =  T2.AirportCode JOIN AIRPORTS AS T3 ON T1.SourceAirport  =  T3.AirportCode WHERE T2.City  =  "Ashley" AND T3.City  =  "Aberdeen"
```

**Returned.**
```sql
SELECT COUNT(*) 
FROM flights 
WHERE SourceAirport = (SELECT AirportCode FROM airports WHERE City = 'Aberdeen') 
AND DestAirport = (SELECT AirportCode FROM airports WHERE City = 'Ashley')
```

**First disagreeing instance** `flight_2v50814.sqlite`.

Gold returns 1 row(s), 1 column(s):

    1

Returned query gives 1 row(s), 1 column(s):

    0

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C181  (question 139, database `flight_2`)

- Returned by: omnisql-32b/seed202, omnisql-32b/seed303
- Class mass: 49/50, 50/50
- Instances disagreeing: 4 of 56 (7%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** How many flights does 'JetBlue Airways' have?

**Gold.**
```sql
SELECT count(*) FROM FLIGHTS AS T1 JOIN AIRLINES AS T2 ON T1.Airline  =  T2.uid WHERE T2.Airline = "JetBlue Airways"
```

**Returned.**
```sql
SELECT COUNT(*) 
FROM flights 
WHERE Airline = (SELECT uid FROM airlines WHERE Airline = 'JetBlue Airways')
```

**First disagreeing instance** `flight_2v50810.sqlite`.

Gold returns 1 row(s), 1 column(s):

    9

Returned query gives 1 row(s), 1 column(s):

    0

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C182  (question 147, database `flight_2`)

- Returned by: omnisql-32b/seed202
- Class mass: 50/50
- Instances disagreeing: 4 of 56 (7%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are airlines that have some flight departing from AHD?

**Gold.**
```sql
SELECT T1.Airline FROM AIRLINES AS T1 JOIN FLIGHTS AS T2 ON T1.uid  =  T2.Airline WHERE T2.SourceAirport  =  "AHD"
```

**Returned.**
```sql
SELECT DISTINCT airlines.Airline
FROM airlines
INNER JOIN flights ON airlines.uid = flights.Airline
WHERE flights.SourceAirport = 'AHD'
```

**First disagreeing instance** `flight_2v5081.sqlite`.

Gold returns 2 row(s), 1 column(s):

    Virgin America
    Virgin America

Returned query gives 1 row(s), 1 column(s):

    Virgin America

Difference: duplicate_multiplicity_only; 1 row(s) in common, 0 only in the gold, 0 only in the returned result.

### C183  (question 149, database `flight_2`)

- Returned by: omnisql-32b/seed202
- Class mass: 50/50
- Instances disagreeing: 5 of 56 (9%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are airlines that have flights arriving at AHD?

**Gold.**
```sql
SELECT T1.Airline FROM AIRLINES AS T1 JOIN FLIGHTS AS T2 ON T1.uid  =  T2.Airline WHERE T2.DestAirport  =  "AHD"
```

**Returned.**
```sql
SELECT DISTINCT airlines.Airline
FROM airlines
JOIN flights ON airlines.uid = flights.Airline
WHERE flights.DestAirport = 'AHD'
```

**First disagreeing instance** `flight_2v50814.sqlite`.

Gold returns 5 row(s), 1 column(s):

    ABR
    199ZSJuF
    5UBp(Hl( 
    2
    5UBp(Hl( 

Returned query gives 4 row(s), 1 column(s):

    ABR
    199ZSJuF
    5UBp(Hl( 
    2

Difference: duplicate_multiplicity_only; 4 row(s) in common, 0 only in the gold, 0 only in the returned result.

### C184  (question 151, database `flight_2`)

- Returned by: omnisql-32b/seed202, omnisql-32b/seed303
- Class mass: 48/50, 49/50
- Instances disagreeing: 4 of 56 (7%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find all airlines that have flights from both APG and CVO.

**Gold.**
```sql
SELECT T1.Airline FROM AIRLINES AS T1 JOIN FLIGHTS AS T2 ON T1.uid  =  T2.Airline WHERE T2.SourceAirport  =  "APG" INTERSECT SELECT T1.Airline FROM AIRLINES AS T1 JOIN FLIGHTS AS T2 ON T1.uid  =  T2.Airline WHERE T2.SourceAirport  =  "CVO"
```

**Returned.**
```sql
SELECT Airline
FROM flights
WHERE SourceAirport = 'APG'
INTERSECT
SELECT Airline
FROM flights
WHERE SourceAirport = 'CVO'
```

**First disagreeing instance** `flight_2v50814.sqlite`.

Gold returns 1 row(s), 1 column(s):

    5UBp(Hl( 

Returned query gives 1 row(s), 1 column(s):

    11

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C185  (question 153, database `flight_2`)

- Returned by: omnisql-32b/seed202
- Class mass: 48/50
- Instances disagreeing: 21 of 56 (38%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find all airlines that have flights from 'CVO' but not from 'APG'.

**Gold.**
```sql
SELECT T1.Airline FROM AIRLINES AS T1 JOIN FLIGHTS AS T2 ON T1.uid  =  T2.Airline WHERE T2.SourceAirport  =  "CVO" EXCEPT SELECT T1.Airline FROM AIRLINES AS T1 JOIN FLIGHTS AS T2 ON T1.uid  =  T2.Airline WHERE T2.SourceAirport  =  "APG"
```

**Returned.**
```sql
SELECT Airline
FROM flights
WHERE SourceAirport = 'CVO'
EXCEPT
SELECT Airline
FROM flights
WHERE SourceAirport = 'APG'
```

**First disagreeing instance** `flight_2v5080.sqlite`.

Gold returns 1 row(s), 1 column(s):

    Aberdeen

Returned query gives 5 row(s), 1 column(s):

    6
    7
    27
    30998003
    9103079609

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 5 only in the returned result.

### C186  (question 154, database `flight_2`)

- Returned by: omnisql-32b/seed202
- Class mass: 50/50
- Instances disagreeing: 21 of 56 (38%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Which airlines have departures from CVO but not from APG?

**Gold.**
```sql
SELECT T1.Airline FROM AIRLINES AS T1 JOIN FLIGHTS AS T2 ON T1.uid  =  T2.Airline WHERE T2.SourceAirport  =  "CVO" EXCEPT SELECT T1.Airline FROM AIRLINES AS T1 JOIN FLIGHTS AS T2 ON T1.uid  =  T2.Airline WHERE T2.SourceAirport  =  "APG"
```

**Returned.**
```sql
SELECT Airline
FROM flights
WHERE SourceAirport = 'CVO'
EXCEPT
SELECT Airline
FROM flights
WHERE SourceAirport = 'APG'
```

**First disagreeing instance** `flight_2v5080.sqlite`.

Gold returns 1 row(s), 1 column(s):

    Aberdeen

Returned query gives 5 row(s), 1 column(s):

    6
    7
    27
    30998003
    9103079609

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 5 only in the returned result.

### C187  (question 223, database `wta_1`)

- Returned by: omnisql-32b/seed202
- Class mass: 33/50
- Instances disagreeing: 7 of 33 (21%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the names of players who won in both 2013 and 2016?

**Gold.**
```sql
SELECT winner_name FROM matches WHERE YEAR  =  2013 INTERSECT SELECT winner_name FROM matches WHERE YEAR  =  2016
```

**Returned.**
```sql
SELECT p.first_name || ' ' || p.last_name AS player_name
FROM players p
JOIN matches m ON p.player_id = m.winner_id
WHERE m.year = 2013
INTERSECT
SELECT p.first_name || ' ' || p.last_name AS player_name
FROM players p
JOIN matches m ON p.player_id = m.winner_id
WHERE m.year = 2016
```

**First disagreeing instance** `wta_1v5080.sqlite`.

Gold returns 1 row(s), 1 column(s):

    3

Returned query gives 0 row(s), None column(s):

    (no rows)

Difference: rep_empty; 0 row(s) in common, 1 only in the gold, 0 only in the returned result.

### C188  (question 228, database `wta_1`)

- Returned by: omnisql-32b/seed202
- Class mass: 36/50
- Instances disagreeing: 7 of 33 (21%)
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
WHERE birth_date = (SELECT MIN(birth_date) FROM players)
```

**First disagreeing instance** `wta_1v50815.sqlite`.

Gold returns 1 row(s), 2 column(s):

    40 | IND

Returned query gives 4 row(s), 2 column(s):

    40 | IND
    Gsb8 | 24.626967830300003vQMaC
    3500 | RCNsvGw
    Ji Su | L

Difference: gold_subset_of_rep; 1 row(s) in common, 0 only in the gold, 3 only in the returned result.

### C189  (question 249, database `wta_1`)

- Returned by: omnisql-32b/seed202
- Class mass: 28/50
- Instances disagreeing: 6 of 33 (18%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find the number of left handed winners who participated in the WTA Championships.

**Gold.**
```sql
SELECT count(DISTINCT winner_name) FROM matches WHERE tourney_name  =  'WTA Championships' AND winner_hand  =  'L'
```

**Returned.**
```sql
SELECT COUNT(DISTINCT m.winner_id) AS number_of_left_handed_winners
FROM matches m
JOIN players p ON m.winner_id = p.player_id
WHERE m.tourney_name = 'WTA Championships' AND p.hand = 'L'
```

**First disagreeing instance** `wta_1v50815.sqlite`.

Gold returns 1 row(s), 1 column(s):

    4

Returned query gives 1 row(s), 1 column(s):

    0

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C190  (question 251, database `battle_death`)

- Returned by: omnisql-32b/seed202
- Class mass: 49/50
- Instances disagreeing: 22 of 28 (79%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the ids and names of the battles that led to more than 10 people died.

**Gold.**
```sql
SELECT T1.id ,  T1.name FROM battle AS T1 JOIN ship AS T2 ON T1.id  =  T2.lost_in_battle JOIN death AS T3 ON T2.id  =  T3.caused_by_ship_id GROUP BY T1.id HAVING sum(T3.killed)  >  10
```

**Returned.**
```sql
SELECT 
    battle.id, 
    battle.name
FROM 
    battle
INNER JOIN 
    ship ON battle.id = ship.lost_in_battle
INNER JOIN 
    death ON ship.id = death.caused_by_ship_id
WHERE 
    death.killed > 10
```

**First disagreeing instance** `battle_deathv5080.sqlite`.

Gold returns 61 row(s), 2 column(s):

    -8146471391 | k8HK0o2
    -3057138174 | Kaloyan
    -2519651209 | 226
    -797862848 | ZPYCapturedwFa
    -540009472 | 226
    0 | 0)p
    3 | Battle of Philippopolis
    4 | WorBattle of Philippopolis6dU
    10 | Captured
    11 | 2
    225 | Battle of Philippopolis
    226 | hZDqJBattle of Serres
    ... (61 rows total)

Returned query gives 124 row(s), 2 column(s):

    9070468346 | VJfwR5)BU83AWD 0787LFzn
    7936890329 | Baldwin I
    3810850516 | Captured
    6826520359 | cv5JOY7tkH(q
    8576269272 | 226
    1111358172 | HMS Atlanta
    10 | Captured
    1 | Kaloyan
    8196806012 | English Channe
    -2519651209 | 226
    9724008145 | 0
    -540009472 | 226
    ... (124 rows total)

Difference: values differ; 58 row(s) in common, 3 only in the gold, 1 only in the returned result.

### C191  (question 253, database `battle_death`)

- Returned by: omnisql-32b/seed202, omnisql-32b/seed303
- Class mass: 35/50, 37/50
- Instances disagreeing: 16 of 28 (57%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** List the name and date the battle that has lost  Lettice and HMS Atalanta

**Gold.**
```sql
SELECT T1.name ,  T1.date FROM battle AS T1 JOIN ship AS T2 ON T1.id  =  T2.lost_in_battle WHERE T2.name  =  'Lettice' INTERSECT SELECT T1.name ,  T1.date FROM battle AS T1 JOIN ship AS T2 ON T1.id  =  T2.lost_in_battle WHERE T2.name  =  'HMS Atalanta'
```

**Returned.**
```sql
SELECT DISTINCT battle.name, battle.date
FROM ship
INNER JOIN battle ON ship.lost_in_battle = battle.id
WHERE ship.name IN ('Lettice', 'HMS Atalanta')
```

**First disagreeing instance** `battle_deathv5080.sqlite`.

Gold returns 0 row(s), None column(s):

    (no rows)

Returned query gives 11 row(s), 2 column(s):

    1SjnDEnglish Channel | Boril
    %East% | TKJ
    hZDqJBattle of Serres | %East%
    5VU7TUgfOgqy79 | X
    Baldwin I | 1235
    English Channe | C1pIqw(
    2 | 2
    Kaloyan | English Channel
    224 | 8zV0f11
    June 1205 | vSDpp0WuPy51oJz5
    Battle of Boruy | June 1205

Difference: gold_empty; 0 row(s) in common, 0 only in the gold, 11 only in the returned result.

### C192  (question 307, database `tvshow`)

- Returned by: omnisql-32b/seed202, omnisql-32b/seed303
- Class mass: 49/49, 50/50
- Instances disagreeing: 11 of 25 (44%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** which countries' tv channels are playing some cartoon  Todd Casey writes?

**Gold.**
```sql
SELECT T1.country FROM TV_Channel AS T1 JOIN cartoon AS T2 ON T1.id = T2.Channel WHERE T2.written_by  =  'Todd Casey'
```

**Returned.**
```sql
SELECT DISTINCT TV_Channel.Country
FROM Cartoon
INNER JOIN TV_Channel ON Cartoon.Channel = TV_Channel.id
WHERE Cartoon.Written_by = 'Todd Casey'
```

**First disagreeing instance** `tvshowv5081.sqlite`.

Gold returns 8 row(s), 1 column(s):

    Todd Casey neY1
    Italy
    Todd Casey
    Italy
    yes
    Italy
    zk9GuItaly
    Italy

Returned query gives 5 row(s), 1 column(s):

    Todd Casey neY1
    Italy
    Todd Casey
    yes
    zk9GuItaly

Difference: duplicate_multiplicity_only; 5 row(s) in common, 0 only in the gold, 0 only in the returned result.

### C193  (question 310, database `tvshow`)

- Returned by: omnisql-32b/seed202
- Class mass: 40/50
- Instances disagreeing: 22 of 25 (88%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the countries that are not playing cartoons  Todd Casey writes?

**Gold.**
```sql
SELECT country FROM TV_Channel EXCEPT SELECT T1.country FROM TV_Channel AS T1 JOIN cartoon AS T2 ON T1.id = T2.Channel WHERE T2.written_by  =  'Todd Casey'
```

**Returned.**
```sql
SELECT Country
FROM TV_Channel
WHERE Country NOT IN (
    SELECT TV_Channel.Country
    FROM TV_Channel
    INNER JOIN Cartoon ON TV_Channel.id = Cartoon.Channel
    WHERE Cartoon.Written_by = 'Todd Casey'
)
```

**First disagreeing instance** `tvshowv5080.sqlite`.

Gold returns 42 row(s), 1 column(s):

    0
    1
    2
    2.0
    2RVcO3
    3
    A Love of a Lifetime
    AmQVA41fzq
    AqaP9Todd Casey
    Day of the Dark Knight!
    Double Down
    Emily
    ... (42 rows total)

Returned query gives 54 row(s), 1 column(s):

    Sky Radio
    Michael Jeleni
    2RVcO3
    Fall of the Blue Beetle!
    Todd Casey
    FnYV1Q4Mv5cAp
    Joseph Kuhr
    0
    qyX6OLOuH(jr)e uhitYkQcmbrWj
    sQF2cbb
    oRAhExYtgAGXhKgINzSGtRFEzn1eO7
    yInDdPZGzLS(NjeelAdU YYifYpRe7
    ... (54 rows total)

Difference: duplicate_multiplicity_only; 42 row(s) in common, 0 only in the gold, 0 only in the returned result.

### C194  (question 366, database `world_1`)

- Returned by: omnisql-32b/seed202, omnisql-32b/seed303
- Class mass: 50/50, 50/50
- Instances disagreeing: 13 of 46 (28%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the total number of languages used in Aruba?

**Gold.**
```sql
SELECT COUNT(T2.Language) FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code  =  T2.CountryCode WHERE T1.Name  =  "Aruba"
```

**Returned.**
```sql
SELECT COUNT(DISTINCT T2.Language) AS TotalLanguages
FROM country AS T1
INNER JOIN countrylanguage AS T2
ON T1.Code = T2.CountryCode
WHERE T1.Name = 'Aruba'
```

**First disagreeing instance** `world_1v50811.sqlite`.

Gold returns 1 row(s), 1 column(s):

    33

Returned query gives 1 row(s), 1 column(s):

    31

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C195  (question 392, database `world_1`)

- Returned by: omnisql-32b/seed202, omnisql-32b/seed303
- Class mass: 18/50, 23/50
- Instances disagreeing: 39 of 46 (85%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the total number of people living in the nations that do not use English?

**Gold.**
```sql
SELECT sum(Population) FROM country WHERE Name NOT IN (SELECT T1.Name FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code  =  T2.CountryCode WHERE T2.Language  =  "English")
```

**Returned.**
```sql
SELECT SUM(Population)
FROM country
WHERE Code NOT IN (
    SELECT CountryCode
    FROM countrylanguage
    WHERE Language = 'English'
)
```

**First disagreeing instance** `world_1v5080.sqlite`.

Gold returns 1 row(s), 1 column(s):

    268945194457

Returned query gives 1 row(s), 1 column(s):

    273514308785

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C196  (question 457, database `network_1`)

- Returned by: omnisql-32b/seed202
- Class mass: 44/50
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
WHERE student_id = (SELECT ID FROM Highschooler WHERE name = 'Kyle')
```

**First disagreeing instance** `network_1v5080.sqlite`.

Gold returns 1 row(s), 1 column(s):

    19

Returned query gives 1 row(s), 1 column(s):

    1

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C197  (question 459, database `network_1`)

- Returned by: omnisql-32b/seed202
- Class mass: 50/50
- Instances disagreeing: 24 of 29 (83%)
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
WHERE liked_id = (SELECT ID FROM Highschooler WHERE name = 'Kyle')
```

**First disagreeing instance** `network_1v5080.sqlite`.

Gold returns 1 row(s), 1 column(s):

    21

Returned query gives 1 row(s), 1 column(s):

    4

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C198  (question 473, database `dog_kennels`)

- Returned by: omnisql-32b/seed202
- Class mass: 49/50
- Instances disagreeing: 15 of 48 (31%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Give me the description of the treatment type that is least expensive.

**Gold.**
```sql
SELECT T1.treatment_type_description FROM Treatment_types AS T1 JOIN Treatments AS T2 ON T1.treatment_type_code  =  T2.treatment_type_code GROUP BY T1.treatment_type_code ORDER BY sum(cost_of_treatment) ASC LIMIT 1
```

**Returned.**
```sql
SELECT treatment_type_description
FROM Treatment_Types
WHERE treatment_type_code = (
  SELECT treatment_type_code
  FROM Treatments
  WHERE cost_of_treatment = (
    SELECT MIN(cost_of_treatment)
    FROM Treatments
  )
)
```

**First disagreeing instance** `dog_kennelsv5081.sqlite`.

Gold returns 1 row(s), 1 column(s):

    QOY2(500

Returned query gives 1 row(s), 1 column(s):

    2

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C199  (question 15, database `concert_singer`)

- Returned by: omnisql-32b/seed303
- Class mass: 35/50
- Instances disagreeing: 17 of 32 (53%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Show the stadium name and capacity with most number of concerts in  2014 or after.

**Gold.**
```sql
SELECT T2.name ,  T2.capacity FROM concert AS T1 JOIN stadium AS T2 ON T1.stadium_id  =  T2.stadium_id WHERE T1.year  >=  2014 GROUP BY T2.stadium_id ORDER BY count(*) DESC LIMIT 1
```

**Returned.**
```sql
SELECT 
    T2.Name, 
    T2.Capacity
FROM 
    concert AS T1
INNER JOIN 
    stadium AS T2 
ON 
    T1.Stadium_ID = T2.Stadium_ID
WHERE 
    T1.Year >= 2014
GROUP BY 
    T2.Name, T2.Capacity
ORDER BY 
    COUNT(T1.concert_ID) DESC
LIMIT 1
```

**First disagreeing instance** `concert_singerv5083.sqlite`.

Gold returns 1 row(s), 2 column(s):

    mpr5T0V | 2600364897

Returned query gives 1 row(s), 2 column(s):

    Bayview Stadium | 19

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C200  (question 43, database `pets_1`)

- Returned by: omnisql-32b/seed303
- Class mass: 50/50
- Instances disagreeing: 23 of 27 (85%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find the name of students who have both cat and dog.

**Gold.**
```sql
select t1.fname from student as t1 join has_pet as t2 on t1.stuid  =  t2.stuid join pets as t3 on t3.petid  =  t2.petid where t3.pettype  =  'cat' intersect select t1.fname from student as t1 join has_pet as t2 on t1.stuid  =  t2.stuid join pets as t3 on t3.petid  =  t2.petid where t3.pettype  =  'dog'
```

**Returned.**
```sql
SELECT S.Fname, S.LName
FROM Student AS S
JOIN Has_Pet AS HP ON S.StuID = HP.StuID
JOIN Pets AS P ON HP.PetID = P.PetID
WHERE P.PetType = 'cat'

INTERSECT

SELECT S.Fname, S.LName
FROM Student AS S
JOIN Has_Pet AS HP ON S.StuID = HP.StuID
JOIN Pets AS P ON HP.PetID = P.PetID
WHERE P.PetType = 'dog'
```

**First disagreeing instance** `pets_1v5080.sqlite`.

Gold returns 5 row(s), 1 column(s):

    0
    003
    10
    David
    Oy01U(d

Returned query gives 4 row(s), 2 column(s):

    0 | 9
    003 | 10
    David | Linda
    Oy01U(d | AilCTbfL

Difference: col_count_differs, disjoint; 0 row(s) in common, 5 only in the gold, 4 only in the returned result.

### C201  (question 51, database `pets_1`)

- Returned by: omnisql-32b/seed303
- Class mass: 49/50
- Instances disagreeing: 3 of 27 (11%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Find the type and weight of the youngest pet.

**Gold.**
```sql
SELECT pettype ,  weight FROM pets ORDER BY pet_age LIMIT 1
```

**Returned.**
```sql
SELECT PetType, weight
FROM Pets
WHERE pet_age = (SELECT MIN(pet_age) FROM Pets)
```

**First disagreeing instance** `pets_1v5080.sqlite`.

Gold returns 1 row(s), 2 column(s):

    3 | 10.0

Returned query gives 7 row(s), 2 column(s):

    3 | 10.0
    (iKpD | 10.0
    2 | 9.0
    9)jcatFEl | 1.0
    20 | 10.0
    0 | 1.0
    cat | 1003.0

Difference: gold_subset_of_rep; 1 row(s) in common, 0 only in the gold, 6 only in the returned result.

### C202  (question 71, database `car_1`)

- Returned by: omnisql-32b/seed303
- Class mass: 50/50
- Instances disagreeing: 57 of 60 (95%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** How many car models are produced by each manufacturer? List the count and the maker full name.

**Gold.**
```sql
select count(*) ,  t2.fullname from model_list as t1 join car_makers as t2 on t1.maker  =  t2.id group by t2.id;
```

**Returned.**
```sql
SELECT
    COUNT(M.Model) AS ModelCount,
    CM.FullName AS MakerFullName
FROM
    model_list M
JOIN
    car_makers CM ON M.Maker = CM.Id
GROUP BY
    CM.FullName
```

**First disagreeing instance** `car_1v5080.sqlite`.

Gold returns 32 row(s), 2 column(s):

    1 | WgId2j2tiOKXNbJE)
    1 | 19.0
    1 | 4
    1 | 3
    1 | 5
    1 | eugeaut
    2 | ER5Km8gHv9Mtc9w6Jlv
    1 | General Motors
    2 | JS8WGkUpkQNRnwpw
    1 | 9
    2 | 151
    1 | fia
    ... (32 rows total)

Returned query gives 28 row(s), 2 column(s):

    3 | 
    2 | 0qSpYywiWEZMmhE9zCeNGcUo5Y
    1 | 0xIjVZ
    1 | 1
    2 | 151
    1 | 19.0
    1 | 1975
    2 | 3
    1 | 3499
    1 | 4
    1 | 4000N1f3g
    3 | 5
    ... (28 rows total)

Difference: values differ; 24 row(s) in common, 6 only in the gold, 4 only in the returned result.

### C203  (question 91, database `car_1`)

- Returned by: omnisql-32b/seed303
- Class mass: 19/50
- Instances disagreeing: 18 of 60 (30%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the average edispl for all volvos?

**Gold.**
```sql
SELECT avg(T2.edispl) FROM CAR_NAMES AS T1 JOIN CARS_DATA AS T2 ON T1.MakeId  =  T2.Id WHERE T1.Model  =  'volvo';
```

**Returned.**
```sql
SELECT AVG(cars_data.Edispl) AS Average_Edispl
FROM cars_data
JOIN car_names ON cars_data.Id = car_names.MakeId
JOIN model_list ON car_names.Model = model_list.Model
JOIN car_makers ON model_list.Maker = car_makers.Id
WHERE car_makers.Maker = 'volvo'
```

**First disagreeing instance** `car_1v50811.sqlite`.

Gold returns 1 row(s), 1 column(s):

    NULL

Returned query gives 1 row(s), 1 column(s):

    436889768.3333333

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C204  (question 95, database `car_1`)

- Returned by: omnisql-32b/seed303
- Class mass: 47/50
- Instances disagreeing: 8 of 60 (13%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** How many car models were produced by American Motor Company?

**Gold.**
```sql
SELECT count(*) FROM CAR_MAKERS AS T1 JOIN MODEL_LIST AS T2 ON T1.Id  =  T2.Maker WHERE T1.FullName  =  'American Motor Company';
```

**Returned.**
```sql
SELECT COUNT(*) 
FROM model_list 
WHERE Maker = (SELECT Id FROM car_makers WHERE FullName = 'American Motor Company')
```

**First disagreeing instance** `car_1v5081.sqlite`.

Gold returns 1 row(s), 1 column(s):

    4

Returned query gives 1 row(s), 1 column(s):

    0

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C205  (question 111, database `car_1`)

- Returned by: omnisql-32b/seed303
- Class mass: 30/50
- Instances disagreeing: 20 of 60 (33%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the id and names of the countries which have more than 3 car makers or produce the 'fiat' ?

**Gold.**
```sql
SELECT T1.countryId ,  T1.CountryName FROM Countries AS T1 JOIN CAR_MAKERS AS T2 ON T1.CountryId  =  T2.Country GROUP BY T1.countryId HAVING count(*)  >  3 UNION SELECT T1.countryId ,  T1.CountryName FROM Countries AS T1 JOIN CAR_MAKERS AS T2 ON T1.CountryId  =  T2.Country JOIN MODEL_LIST AS T3 ON T2.Id  =  T3.Maker WHERE T3.Model  =  'fiat';
```

**Returned.**
```sql
SELECT c.CountryId, c.CountryName
FROM car_makers cm
JOIN countries c ON cm.Country = c.CountryId
GROUP BY c.CountryId, c.CountryName
HAVING COUNT(cm.Id) > 3

UNION

SELECT c.CountryId, c.CountryName
FROM car_makers cm
JOIN countries c ON cm.Country = c.CountryId
WHERE cm.Maker = 'fiat'
```

**First disagreeing instance** `car_1v5080.sqlite`.

Gold returns 8 row(s), 2 column(s):

    -4076741865 | us
    10 | Om
    12 | 400
    19 | ford
    151 | buick
    1981 | asia
    8210699449 | 3499
    9236429507 | mc

Returned query gives 9 row(s), 2 column(s):

    -4076741865 | us
    10 | Om
    12 | 400
    19 | ford
    151 | buick
    1969 | france
    1981 | asia
    8210699449 | 3499
    9236429507 | mc

Difference: gold_subset_of_rep; 8 row(s) in common, 0 only in the gold, 1 only in the returned result.

### C206  (question 112, database `car_1`)

- Returned by: omnisql-32b/seed303
- Class mass: 26/50
- Instances disagreeing: 20 of 60 (33%)
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
JOIN 
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
JOIN 
    car_makers cm ON c.CountryId = cm.Country
WHERE 
    cm.Maker = 'fiat'
```

**First disagreeing instance** `car_1v5080.sqlite`.

Gold returns 8 row(s), 2 column(s):

    -4076741865 | us
    10 | Om
    12 | 400
    19 | ford
    151 | buick
    1981 | asia
    8210699449 | 3499
    9236429507 | mc

Returned query gives 9 row(s), 2 column(s):

    -4076741865 | us
    10 | Om
    12 | 400
    19 | ford
    151 | buick
    1969 | france
    1981 | asia
    8210699449 | 3499
    9236429507 | mc

Difference: gold_subset_of_rep; 8 row(s) in common, 0 only in the gold, 1 only in the returned result.

### C207  (question 147, database `flight_2`)

- Returned by: omnisql-32b/seed303
- Class mass: 49/50
- Instances disagreeing: 4 of 56 (7%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are airlines that have some flight departing from AHD?

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

### C208  (question 148, database `flight_2`)

- Returned by: omnisql-32b/seed303
- Class mass: 50/50
- Instances disagreeing: 4 of 56 (7%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Which airlines have a flight from  AHD?

**Gold.**
```sql
SELECT T1.Airline FROM AIRLINES AS T1 JOIN FLIGHTS AS T2 ON T1.uid  =  T2.Airline WHERE T2.SourceAirport  =  "AHD"
```

**Returned.**
```sql
SELECT DISTINCT a.Airline
FROM flights f
JOIN airlines a ON f.Airline = a.uid
WHERE f.SourceAirport = 'AHD'
```

**First disagreeing instance** `flight_2v5081.sqlite`.

Gold returns 2 row(s), 1 column(s):

    Virgin America
    Virgin America

Returned query gives 1 row(s), 1 column(s):

    Virgin America

Difference: duplicate_multiplicity_only; 1 row(s) in common, 0 only in the gold, 0 only in the returned result.

### C209  (question 150, database `flight_2`)

- Returned by: omnisql-32b/seed303
- Class mass: 50/50
- Instances disagreeing: 5 of 56 (9%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Which airlines have a flight to  AHD?

**Gold.**
```sql
SELECT T1.Airline FROM AIRLINES AS T1 JOIN FLIGHTS AS T2 ON T1.uid  =  T2.Airline WHERE T2.DestAirport  =  "AHD"
```

**Returned.**
```sql
SELECT DISTINCT airlines.Airline
FROM flights
JOIN airlines ON flights.Airline = airlines.uid
WHERE flights.DestAirport = 'AHD'
```

**First disagreeing instance** `flight_2v50814.sqlite`.

Gold returns 5 row(s), 1 column(s):

    ABR
    199ZSJuF
    5UBp(Hl( 
    2
    5UBp(Hl( 

Returned query gives 4 row(s), 1 column(s):

    ABR
    199ZSJuF
    5UBp(Hl( 
    2

Difference: duplicate_multiplicity_only; 4 row(s) in common, 0 only in the gold, 0 only in the returned result.

### C210  (question 153, database `flight_2`)

- Returned by: omnisql-32b/seed303
- Class mass: 50/50
- Instances disagreeing: 21 of 56 (38%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find all airlines that have flights from 'CVO' but not from 'APG'.

**Gold.**
```sql
SELECT T1.Airline FROM AIRLINES AS T1 JOIN FLIGHTS AS T2 ON T1.uid  =  T2.Airline WHERE T2.SourceAirport  =  "CVO" EXCEPT SELECT T1.Airline FROM AIRLINES AS T1 JOIN FLIGHTS AS T2 ON T1.uid  =  T2.Airline WHERE T2.SourceAirport  =  "APG"
```

**Returned.**
```sql
SELECT DISTINCT Airline
FROM flights
WHERE SourceAirport = 'CVO'
EXCEPT
SELECT DISTINCT Airline
FROM flights
WHERE SourceAirport = 'APG'
```

**First disagreeing instance** `flight_2v5080.sqlite`.

Gold returns 1 row(s), 1 column(s):

    Aberdeen

Returned query gives 5 row(s), 1 column(s):

    6
    7
    27
    30998003
    9103079609

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 5 only in the returned result.

### C211  (question 236, database `wta_1`)

- Returned by: omnisql-32b/seed303
- Class mass: 34/50
- Instances disagreeing: 9 of 33 (27%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Find the name of the winner who has the highest rank points and participated in the Australian Open.

**Gold.**
```sql
SELECT winner_name FROM matches WHERE tourney_name  =  'Australian Open' ORDER BY winner_rank_points DESC LIMIT 1
```

**Returned.**
```sql
SELECT p.first_name || ' ' || p.last_name AS winner_name
FROM matches m
JOIN players p ON m.winner_id = p.player_id
WHERE m.tourney_name = 'Australian Open'
ORDER BY m.winner_rank_points DESC
LIMIT 1
```

**First disagreeing instance** `wta_1v5080.sqlite`.

Gold returns 1 row(s), 1 column(s):

    11dVZOO

Returned query gives 1 row(s), 1 column(s):

    200001 10

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C212  (question 267, database `student_transcripts_tracking`)

- Returned by: omnisql-32b/seed303
- Class mass: 40/50
- Instances disagreeing: 31 of 55 (56%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What is the id, line 1, and line 2 of the place with the most students?

**Gold.**
```sql
SELECT T1.address_id ,  T1.line_1 ,  T1.line_2 FROM Addresses AS T1 JOIN Students AS T2 ON T1.address_id  =  T2.current_address_id GROUP BY T1.address_id ORDER BY count(*) DESC LIMIT 1
```

**Returned.**
```sql
SELECT a.address_id, a.line_1, a.line_2
FROM Addresses a
JOIN Students s ON a.address_id = s.current_address_id
GROUP BY a.address_id, a.line_1, a.line_2
ORDER BY COUNT(s.student_id) DESC
LIMIT 1
```

**First disagreeing instance** `student_transcripts_trackingv5080.sqlite`.

Gold returns 1 row(s), 3 column(s):

    9700166583 | 10 | 6

Returned query gives 1 row(s), 3 column(s):

    -7035591255 | 09700166582 | Apt. 335

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C213  (question 375, database `world_1`)

- Returned by: omnisql-32b/seed303
- Class mass: 49/50
- Instances disagreeing: 9 of 46 (20%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Give the names of nations that speak both English and French.

**Gold.**
```sql
SELECT T1.Name FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code  =  T2.CountryCode WHERE T2.Language  =  "English" INTERSECT SELECT T1.Name FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code  =  T2.CountryCode WHERE T2.Language  =  "French"
```

**Returned.**
```sql
SELECT c.Name
FROM country AS c
WHERE c.Code IN (
    SELECT cl1.CountryCode
    FROM countrylanguage AS cl1
    WHERE cl1.Language = 'English'
    INTERSECT
    SELECT cl2.CountryCode
    FROM countrylanguage AS cl2
    WHERE cl2.Language = 'French'
)
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

### C214  (question 460, database `network_1`)

- Returned by: omnisql-32b/seed303
- Class mass: 49/50
- Instances disagreeing: 22 of 29 (76%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Return the number of likes Kyle has.

**Gold.**
```sql
SELECT count(*) FROM Likes AS T1 JOIN Highschooler AS T2 ON T1.student_id  =  T2.id WHERE T2.name  =  "Kyle"
```

**Returned.**
```sql
SELECT COUNT(*) AS like_count
FROM Highschooler AS H
INNER JOIN Likes AS L ON H.ID = L.liked_id
WHERE H.name = 'Kyle'
```

**First disagreeing instance** `network_1v5080.sqlite`.

Gold returns 1 row(s), 1 column(s):

    21

Returned query gives 1 row(s), 1 column(s):

    30

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C215  (question 473, database `dog_kennels`)

- Returned by: omnisql-32b/seed303
- Class mass: 50/50
- Instances disagreeing: 17 of 48 (35%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Give me the description of the treatment type that is least expensive.

**Gold.**
```sql
SELECT T1.treatment_type_description FROM Treatment_types AS T1 JOIN Treatments AS T2 ON T1.treatment_type_code  =  T2.treatment_type_code GROUP BY T1.treatment_type_code ORDER BY sum(cost_of_treatment) ASC LIMIT 1
```

**Returned.**
```sql
SELECT tt.treatment_type_description
FROM Treatments t
JOIN Treatment_Types tt ON t.treatment_type_code = tt.treatment_type_code
WHERE t.cost_of_treatment = (
    SELECT MIN(cost_of_treatment)
    FROM Treatments
)
```

**First disagreeing instance** `dog_kennelsv5081.sqlite`.

Gold returns 1 row(s), 1 column(s):

    QOY2(500

Returned query gives 4 row(s), 1 column(s):

    2
    North
    QOY2(500
    Virginia

Difference: gold_subset_of_rep; 1 row(s) in common, 0 only in the gold, 3 only in the returned result.

### C216  (question 21, database `concert_singer`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed202, xiyansql-32b/seed303
- Class mass: 50/50, 50/50, 50/50
- Instances disagreeing: 29 of 32 (91%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the names of all stadiums that did not have a concert in 2014?

**Gold.**
```sql
SELECT name FROM stadium EXCEPT SELECT T2.name FROM concert AS T1 JOIN stadium AS T2 ON T1.stadium_id  =  T2.stadium_id WHERE T1.year  =  2014
```

**Returned.**
```sql
SELECT name FROM stadium WHERE stadium_id NOT IN (SELECT stadium_id FROM concert WHERE YEAR = 2014)
```

**First disagreeing instance** `concert_singertest0.sqlite`.

Gold returns 14 row(s), 1 column(s):

    )uFP
    03RZUfj(bwx UE
    19
    2h52O0
    Be(
    Recreation Par
    RvI8xFrance
    V2z20hJn
    cmrzmn3fEIv4v2)r
    kHG1vmsN
    lJojzlh5tVtfoa)
    mC
    ... (14 rows total)

Returned query gives 38 row(s), 1 column(s):

    Recreation Park
    20
    2
    20
    France
    Glebe Park
    2
    Recreation Park
    2h52O0
    0
    2
    )uFP
    ... (38 rows total)

Difference: gold_subset_of_rep; 14 row(s) in common, 0 only in the gold, 9 only in the returned result.

### C217  (question 43, database `pets_1`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed202
- Class mass: 50/50, 50/50
- Instances disagreeing: 23 of 27 (85%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find the name of students who have both cat and dog.

**Gold.**
```sql
select t1.fname from student as t1 join has_pet as t2 on t1.stuid  =  t2.stuid join pets as t3 on t3.petid  =  t2.petid where t3.pettype  =  'cat' intersect select t1.fname from student as t1 join has_pet as t2 on t1.stuid  =  t2.stuid join pets as t3 on t3.petid  =  t2.petid where t3.pettype  =  'dog'
```

**Returned.**
```sql
SELECT T1.fname , T1.lname FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid = T2.stuid JOIN pets AS T3 ON T2.petid = T3.petid WHERE T3.pettype = 'cat' INTERSECT SELECT T1.fname , T1.lname FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid = T2.stuid JOIN pets AS T3 ON T2.petid = T3.petid WHERE T3.pettype = 'dog'
```

**First disagreeing instance** `pets_1v5080.sqlite`.

Gold returns 5 row(s), 1 column(s):

    0
    003
    10
    David
    Oy01U(d

Returned query gives 4 row(s), 2 column(s):

    0 | 9
    003 | 10
    David | Linda
    Oy01U(d | AilCTbfL

Difference: col_count_differs, disjoint; 0 row(s) in common, 5 only in the gold, 4 only in the returned result.

### C218  (question 69, database `car_1`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed202, xiyansql-32b/seed303
- Class mass: 50/50, 50/50, 50/50
- Instances disagreeing: 42 of 60 (70%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Which of the nations has the most car makers? List the country name.

**Gold.**
```sql
SELECT T2.CountryName FROM CAR_MAKERS AS T1 JOIN COUNTRIES AS T2 ON T1.Country  =  T2.CountryId GROUP BY T1.Country ORDER BY Count(*) DESC LIMIT 1;
```

**Returned.**
```sql
SELECT T1.CountryName FROM COUNTRIES AS T1 JOIN CAR_MAKERS AS T2 ON T1.CountryId = T2.Country GROUP BY T1.CountryName ORDER BY Count(*) DESC LIMIT 1
```

**First disagreeing instance** `car_1v5080.sqlite`.

Gold returns 1 row(s), 1 column(s):

    us

Returned query gives 1 row(s), 1 column(s):

    asia

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C219  (question 70, database `car_1`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed202, xiyansql-32b/seed303
- Class mass: 50/50, 50/50, 50/50
- Instances disagreeing: 42 of 60 (70%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What is the name of the nation with the most car makers?

**Gold.**
```sql
SELECT T2.CountryName FROM CAR_MAKERS AS T1 JOIN COUNTRIES AS T2 ON T1.Country  =  T2.CountryId GROUP BY T1.Country ORDER BY Count(*) DESC LIMIT 1;
```

**Returned.**
```sql
SELECT T1.CountryName FROM COUNTRIES AS T1 JOIN CAR_MAKERS AS T2 ON T1.CountryId = T2.Country GROUP BY T1.CountryName ORDER BY Count(*) DESC LIMIT 1
```

**First disagreeing instance** `car_1v5080.sqlite`.

Gold returns 1 row(s), 1 column(s):

    us

Returned query gives 1 row(s), 1 column(s):

    asia

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C220  (question 71, database `car_1`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed202
- Class mass: 50/50, 50/50
- Instances disagreeing: 57 of 60 (95%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** How many car models are produced by each manufacturer? List the count and the maker full name.

**Gold.**
```sql
select count(*) ,  t2.fullname from model_list as t1 join car_makers as t2 on t1.maker  =  t2.id group by t2.id;
```

**Returned.**
```sql
SELECT count(*) , T1.FullName FROM CAR_MAKERS AS T1 JOIN MODEL_LIST AS T2 ON T1.Id = T2.Maker GROUP BY T1.FullName
```

**First disagreeing instance** `car_1v5080.sqlite`.

Gold returns 32 row(s), 2 column(s):

    1 | WgId2j2tiOKXNbJE)
    1 | 19.0
    1 | 4
    1 | 3
    1 | 5
    1 | eugeaut
    2 | ER5Km8gHv9Mtc9w6Jlv
    1 | General Motors
    2 | JS8WGkUpkQNRnwpw
    1 | 9
    2 | 151
    1 | fia
    ... (32 rows total)

Returned query gives 28 row(s), 2 column(s):

    3 | 
    2 | 0qSpYywiWEZMmhE9zCeNGcUo5Y
    1 | 0xIjVZ
    1 | 1
    2 | 151
    1 | 19.0
    1 | 1975
    2 | 3
    1 | 3499
    1 | 4
    1 | 4000N1f3g
    3 | 5
    ... (28 rows total)

Difference: values differ; 24 row(s) in common, 6 only in the gold, 4 only in the returned result.

### C221  (question 84, database `car_1`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed202
- Class mass: 26/50, 35/50
- Instances disagreeing: 9 of 60 (15%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Which countries in europe have at least 3 car manufacturers?

**Gold.**
```sql
SELECT T1.CountryName FROM COUNTRIES AS T1 JOIN CONTINENTS AS T2 ON T1.Continent  =  T2.ContId JOIN CAR_MAKERS AS T3 ON T1.CountryId  =  T3.Country WHERE T2.Continent  =  'europe' GROUP BY T1.CountryName HAVING count(*)  >=  3;
```

**Returned.**
```sql
SELECT T1.CountryName FROM countries AS T1 JOIN car_makers AS T2 ON T1.CountryId = T2.Country WHERE T1.Continent = (SELECT ContId FROM continents WHERE Continent = 'europe') GROUP BY T1.CountryName HAVING count(*) >= 3
```

**First disagreeing instance** `car_1v50813.sqlite`.

Gold returns 3 row(s), 1 column(s):

    1969
    2
    volvo

Returned query gives 0 row(s), None column(s):

    (no rows)

Difference: rep_empty; 0 row(s) in common, 3 only in the gold, 0 only in the returned result.

### C222  (question 90, database `car_1`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed202, xiyansql-32b/seed303
- Class mass: 50/50, 50/50, 50/50
- Instances disagreeing: 18 of 60 (30%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the average edispl of the cars of  volvo?

**Gold.**
```sql
SELECT avg(T2.edispl) FROM CAR_NAMES AS T1 JOIN CARS_DATA AS T2 ON T1.MakeId  =  T2.Id WHERE T1.Model  =  'volvo';
```

**Returned.**
```sql
SELECT avg(T1.edispl) FROM CARS_DATA AS T1 JOIN CAR_NAMES AS T2 ON T1.Id = T2.MakeId JOIN MODEL_LIST AS T3 ON T2.Model = T3.Model JOIN CAR_MAKERS AS T4 ON T3.Maker = T4.Id WHERE T4.Maker = 'volvo'
```

**First disagreeing instance** `car_1v50811.sqlite`.

Gold returns 1 row(s), 1 column(s):

    NULL

Returned query gives 1 row(s), 1 column(s):

    436889768.3333333

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C223  (question 91, database `car_1`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed303
- Class mass: 47/50, 50/50
- Instances disagreeing: 16 of 60 (27%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the average edispl for all volvos?

**Gold.**
```sql
SELECT avg(T2.edispl) FROM CAR_NAMES AS T1 JOIN CARS_DATA AS T2 ON T1.MakeId  =  T2.Id WHERE T1.Model  =  'volvo';
```

**Returned.**
```sql
SELECT avg(T1.edispl) FROM CARS_DATA AS T1 JOIN CAR_NAMES AS T2 ON T1.Id = T2.MakeId WHERE T2.Make LIKE "%volvo%"
```

**First disagreeing instance** `car_1v5080.sqlite`.

Gold returns 1 row(s), 1 column(s):

    NULL

Returned query gives 1 row(s), 1 column(s):

    6400658707.0

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C224  (question 99, database `car_1`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed303
- Class mass: 50/50, 50/50
- Instances disagreeing: 19 of 60 (32%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Which distinctive models are produced by General Motors or heavier than 3500?

**Gold.**
```sql
SELECT DISTINCT T2.Model FROM CAR_NAMES AS T1 JOIN MODEL_LIST AS T2 ON T1.Model  =  T2.Model JOIN CAR_MAKERS AS T3 ON T2.Maker  =  T3.Id JOIN CARS_DATA AS T4 ON T1.MakeId  =  T4.Id WHERE T3.FullName  =  'General Motors' OR T4.weight  >  3500;
```

**Returned.**
```sql
SELECT DISTINCT T1.Model FROM CAR_NAMES AS T1 JOIN CARS_DATA AS T2 ON T1.MakeId = T2.Id JOIN MODEL_LIST AS T3 ON T1.Model = T3.Model JOIN CAR_MAKERS AS T4 ON T3.Maker = T4.Id WHERE T4.Maker = 'gm' OR T2.weight > 3500
```

**First disagreeing instance** `car_1v50812.sqlite`.

Gold returns 14 row(s), 1 column(s):

    (sC6vTf2LiQMjE9kLIj
    8
    1974
    europe
    1973
    ZIU3500RsB
    2Zcyey
    MuecQscion
    1979
    299
    bmw
    9
    ... (14 rows total)

Returned query gives 16 row(s), 1 column(s):

    299
    (sC6vTf2LiQMjE9kLIj
    8
    volvo
    1974
    europe
    1973
    ZIU3500RsB
    9
    Ford Motor Company
    2Zcyey
    MuecQscion
    ... (16 rows total)

Difference: gold_subset_of_rep; 14 row(s) in common, 0 only in the gold, 2 only in the returned result.

### C225  (question 103, database `car_1`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed202, xiyansql-32b/seed303
- Class mass: 50/50, 50/50, 50/50
- Instances disagreeing: 17 of 60 (28%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** For  volvo, how many cylinders does the car with the least accelerate have?

**Gold.**
```sql
SELECT T1.cylinders FROM CARS_DATA AS T1 JOIN CAR_NAMES AS T2 ON T1.Id  =  T2.MakeId WHERE T2.Model  =  'volvo' ORDER BY T1.accelerate ASC LIMIT 1;
```

**Returned.**
```sql
SELECT T1.cylinders FROM CARS_DATA AS T1 JOIN CAR_NAMES AS T2 ON T1.Id = T2.MakeId JOIN MODEL_LIST AS T3 ON T2.Model = T3.Model JOIN CAR_MAKERS AS T4 ON T3.Maker = T4.Id WHERE T4.Maker = 'volvo' ORDER BY T1.accelerate ASC LIMIT 1
```

**First disagreeing instance** `car_1v50811.sqlite`.

Gold returns 0 row(s), None column(s):

    (no rows)

Returned query gives 1 row(s), 1 column(s):

    1969

Difference: gold_empty; 0 row(s) in common, 0 only in the gold, 1 only in the returned result.

### C226  (question 104, database `car_1`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed303
- Class mass: 50/50, 50/50
- Instances disagreeing: 17 of 60 (28%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** For a volvo , how many cylinders does the version with least accelerate have?

**Gold.**
```sql
SELECT T1.cylinders FROM CARS_DATA AS T1 JOIN CAR_NAMES AS T2 ON T1.Id  =  T2.MakeId WHERE T2.Model  =  'volvo' ORDER BY T1.accelerate ASC LIMIT 1;
```

**Returned.**
```sql
SELECT T1.cylinders FROM CARS_DATA AS T1 JOIN CAR_NAMES AS T2 ON T1.Id = T2.MakeId WHERE T2.Make LIKE "%volvo%" ORDER BY T1.accelerate ASC LIMIT 1
```

**First disagreeing instance** `car_1v5080.sqlite`.

Gold returns 0 row(s), None column(s):

    (no rows)

Returned query gives 1 row(s), 1 column(s):

    5

Difference: gold_empty; 0 row(s) in common, 0 only in the gold, 1 only in the returned result.

### C227  (question 111, database `car_1`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed202, xiyansql-32b/seed303
- Class mass: 50/50, 50/50, 50/50
- Instances disagreeing: 20 of 60 (33%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the id and names of the countries which have more than 3 car makers or produce the 'fiat' ?

**Gold.**
```sql
SELECT T1.countryId ,  T1.CountryName FROM Countries AS T1 JOIN CAR_MAKERS AS T2 ON T1.CountryId  =  T2.Country GROUP BY T1.countryId HAVING count(*)  >  3 UNION SELECT T1.countryId ,  T1.CountryName FROM Countries AS T1 JOIN CAR_MAKERS AS T2 ON T1.CountryId  =  T2.Country JOIN MODEL_LIST AS T3 ON T2.Id  =  T3.Maker WHERE T3.Model  =  'fiat';
```

**Returned.**
```sql
SELECT T1.CountryId , T1.CountryName FROM COUNTRIES AS T1 JOIN CAR_MAKERS AS T2 ON T1.CountryId = T2.Country GROUP BY T1.CountryId HAVING count(*) > 3 UNION SELECT T1.CountryId , T1.CountryName FROM COUNTRIES AS T1 JOIN CAR_MAKERS AS T2 ON T1.CountryId = T2.Country WHERE T2.Maker = 'fiat'
```

**First disagreeing instance** `car_1v5080.sqlite`.

Gold returns 8 row(s), 2 column(s):

    -4076741865 | us
    10 | Om
    12 | 400
    19 | ford
    151 | buick
    1981 | asia
    8210699449 | 3499
    9236429507 | mc

Returned query gives 9 row(s), 2 column(s):

    -4076741865 | us
    10 | Om
    12 | 400
    19 | ford
    151 | buick
    1969 | france
    1981 | asia
    8210699449 | 3499
    9236429507 | mc

Difference: gold_subset_of_rep; 8 row(s) in common, 0 only in the gold, 1 only in the returned result.

### C228  (question 112, database `car_1`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed202, xiyansql-32b/seed303
- Class mass: 45/50, 41/50, 40/50
- Instances disagreeing: 20 of 60 (33%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What are the ids and names of all countries that either have more than 3 car makers or produce fiats?

**Gold.**
```sql
select t1.countryid ,  t1.countryname from countries as t1 join car_makers as t2 on t1.countryid  =  t2.country group by t1.countryid having count(*)  >  3 union select t1.countryid ,  t1.countryname from countries as t1 join car_makers as t2 on t1.countryid  =  t2.country join model_list as t3 on t2.id  =  t3.maker where t3.model  =  'fiat';
```

**Returned.**
```sql
SELECT T1.CountryId , T1.CountryName FROM COUNTRIES AS T1 JOIN CAR_MAKERS AS T2 ON T1.CountryId = T2.Country GROUP BY T1.CountryId HAVING count(*) > 3 UNION SELECT T1.CountryId , T1.CountryName FROM COUNTRIES AS T1 JOIN CAR_MAKERS AS T2 ON T1.CountryId = T2.Country WHERE T2.Maker = 'fiat'
```

**First disagreeing instance** `car_1v5080.sqlite`.

Gold returns 8 row(s), 2 column(s):

    -4076741865 | us
    10 | Om
    12 | 400
    19 | ford
    151 | buick
    1981 | asia
    8210699449 | 3499
    9236429507 | mc

Returned query gives 9 row(s), 2 column(s):

    -4076741865 | us
    10 | Om
    12 | 400
    19 | ford
    151 | buick
    1969 | france
    1981 | asia
    8210699449 | 3499
    9236429507 | mc

Difference: gold_subset_of_rep; 8 row(s) in common, 0 only in the gold, 1 only in the returned result.

### C229  (question 383, database `world_1`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed202, xiyansql-32b/seed303
- Class mass: 27/50, 35/50, 28/50
- Instances disagreeing: 26 of 46 (57%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Which language is the most popular on Asian ?

**Gold.**
```sql
SELECT T2.Language FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code  =  T2.CountryCode WHERE T1.Continent  =  "Asia" GROUP BY T2.Language ORDER BY COUNT (*) DESC LIMIT 1
```

**Returned.**
```sql
SELECT T2.Language FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code = T2.CountryCode WHERE T1.Continent = "Asia" GROUP BY T2.Language ORDER BY SUM(T2.Percentage) DESC LIMIT 1
```

**First disagreeing instance** `world_1v5080.sqlite`.

Gold returns 1 row(s), 1 column(s):

    wVT6wDgbpLbVxdY CjOQ

Returned query gives 1 row(s), 1 column(s):

    Anguilla

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C230  (question 456, database `network_1`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed202, xiyansql-32b/seed303
- Class mass: 38/50, 34/50, 34/50
- Instances disagreeing: 22 of 29 (76%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Return the names of friends of  Kyle.

**Gold.**
```sql
SELECT T3.name FROM Friend AS T1 JOIN Highschooler AS T2 ON T1.student_id  =  T2.id JOIN Highschooler AS T3 ON T1.friend_id  =  T3.id WHERE T2.name  =  "Kyle"
```

**Returned.**
```sql
SELECT T2.name FROM Friend AS T1 JOIN Highschooler AS T2 ON T1.friend_id = T2.id WHERE T1.student_id = (SELECT id FROM Highschooler WHERE name = "Kyle")
```

**First disagreeing instance** `network_1v5080.sqlite`.

Gold returns 19 row(s), 1 column(s):

    1
    pN
    
    1709
    2
    Haley
    168
    KMV
    1542A1510
    Gabrie
    8
    We
    ... (19 rows total)

Returned query gives 1 row(s), 1 column(s):

    3

Difference: rep_subset_of_gold; 1 row(s) in common, 18 only in the gold, 0 only in the returned result.

### C231  (question 472, database `dog_kennels`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed202
- Class mass: 50/50, 50/50
- Instances disagreeing: 4 of 48 (8%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What is the description of the treatment type that is the cheapest overall?

**Gold.**
```sql
SELECT T1.treatment_type_description FROM Treatment_types AS T1 JOIN Treatments AS T2 ON T1.treatment_type_code  =  T2.treatment_type_code GROUP BY T1.treatment_type_code ORDER BY sum(cost_of_treatment) ASC LIMIT 1
```

**Returned.**
```sql
SELECT T1.treatment_type_description FROM Treatment_Types AS T1 JOIN Treatments AS T2 ON T1.treatment_type_code = T2.treatment_type_code GROUP BY T1.treatment_type_code ORDER BY avg(cost_of_treatment) LIMIT 1
```

**First disagreeing instance** `dog_kennelsv5082.sqlite`.

Gold returns 1 row(s), 1 column(s):

    Vaccination

Returned query gives 1 row(s), 1 column(s):

    999

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C232  (question 473, database `dog_kennels`)

- Returned by: xiyansql-32b/seed101, xiyansql-32b/seed303
- Class mass: 50/50, 50/50
- Instances disagreeing: 15 of 48 (31%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Give me the description of the treatment type that is least expensive.

**Gold.**
```sql
SELECT T1.treatment_type_description FROM Treatment_types AS T1 JOIN Treatments AS T2 ON T1.treatment_type_code  =  T2.treatment_type_code GROUP BY T1.treatment_type_code ORDER BY sum(cost_of_treatment) ASC LIMIT 1
```

**Returned.**
```sql
SELECT T1.treatment_type_description FROM Treatment_Types AS T1 JOIN Treatments AS T2 ON T1.treatment_type_code = T2.treatment_type_code ORDER BY T2.cost_of_treatment ASC LIMIT 1
```

**First disagreeing instance** `dog_kennelsv5081.sqlite`.

Gold returns 1 row(s), 1 column(s):

    QOY2(500

Returned query gives 1 row(s), 1 column(s):

    2

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C233  (question 91, database `car_1`)

- Returned by: xiyansql-32b/seed202
- Class mass: 49/50
- Instances disagreeing: 16 of 60 (27%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** What is the average edispl for all volvos?

**Gold.**
```sql
SELECT avg(T2.edispl) FROM CAR_NAMES AS T1 JOIN CARS_DATA AS T2 ON T1.MakeId  =  T2.Id WHERE T1.Model  =  'volvo';
```

**Returned.**
```sql
SELECT avg(T1.edispl) FROM CARS_DATA AS T1 JOIN CAR_NAMES AS T2 ON T1.Id = T2.MakeId WHERE T2.Make LIKE '%volvo%'
```

**First disagreeing instance** `car_1v5080.sqlite`.

Gold returns 1 row(s), 1 column(s):

    NULL

Returned query gives 1 row(s), 1 column(s):

    6400658707.0

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C234  (question 99, database `car_1`)

- Returned by: xiyansql-32b/seed202
- Class mass: 50/50
- Instances disagreeing: 19 of 60 (32%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Which distinctive models are produced by General Motors or heavier than 3500?

**Gold.**
```sql
SELECT DISTINCT T2.Model FROM CAR_NAMES AS T1 JOIN MODEL_LIST AS T2 ON T1.Model  =  T2.Model JOIN CAR_MAKERS AS T3 ON T2.Maker  =  T3.Id JOIN CARS_DATA AS T4 ON T1.MakeId  =  T4.Id WHERE T3.FullName  =  'General Motors' OR T4.weight  >  3500;
```

**Returned.**
```sql
SELECT DISTINCT T1.Model FROM CAR_NAMES AS T1 JOIN CARS_DATA AS T2 ON T1.MakeId = T2.Id JOIN MODEL_LIST AS T3 ON T1.Model = T3.Model JOIN CAR_MAKERS AS T4 ON T3.Maker = T4.Id WHERE T4.Maker = 'gm' OR T2.Weight > 3500
```

**First disagreeing instance** `car_1v50812.sqlite`.

Gold returns 14 row(s), 1 column(s):

    (sC6vTf2LiQMjE9kLIj
    8
    1974
    europe
    1973
    ZIU3500RsB
    2Zcyey
    MuecQscion
    1979
    299
    bmw
    9
    ... (14 rows total)

Returned query gives 16 row(s), 1 column(s):

    299
    (sC6vTf2LiQMjE9kLIj
    8
    volvo
    1974
    europe
    1973
    ZIU3500RsB
    9
    Ford Motor Company
    2Zcyey
    MuecQscion
    ... (16 rows total)

Difference: gold_subset_of_rep; 14 row(s) in common, 0 only in the gold, 2 only in the returned result.

### C235  (question 104, database `car_1`)

- Returned by: xiyansql-32b/seed202
- Class mass: 50/50
- Instances disagreeing: 17 of 60 (28%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** For a volvo , how many cylinders does the version with least accelerate have?

**Gold.**
```sql
SELECT T1.cylinders FROM CARS_DATA AS T1 JOIN CAR_NAMES AS T2 ON T1.Id  =  T2.MakeId WHERE T2.Model  =  'volvo' ORDER BY T1.accelerate ASC LIMIT 1;
```

**Returned.**
```sql
SELECT T1.cylinders FROM CARS_DATA AS T1 JOIN CAR_NAMES AS T2 ON T1.Id = T2.MakeId WHERE T2.Make LIKE '%volvo%' ORDER BY T1.accelerate ASC LIMIT 1
```

**First disagreeing instance** `car_1v5080.sqlite`.

Gold returns 0 row(s), None column(s):

    (no rows)

Returned query gives 1 row(s), 1 column(s):

    5

Difference: gold_empty; 0 row(s) in common, 0 only in the gold, 1 only in the returned result.

### C236  (question 473, database `dog_kennels`)

- Returned by: xiyansql-32b/seed202
- Class mass: 50/50
- Instances disagreeing: 15 of 48 (31%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** Give me the description of the treatment type that is least expensive.

**Gold.**
```sql
SELECT T1.treatment_type_description FROM Treatment_types AS T1 JOIN Treatments AS T2 ON T1.treatment_type_code  =  T2.treatment_type_code GROUP BY T1.treatment_type_code ORDER BY sum(cost_of_treatment) ASC LIMIT 1
```

**Returned.**
```sql
SELECT T1.treatment_type_description FROM Treatment_Types AS T1 JOIN Treatments AS T2 ON T1.treatment_type_code = T2.treatment_type_code ORDER BY T2.cost_of_treatment LIMIT 1
```

**First disagreeing instance** `dog_kennelsv5081.sqlite`.

Gold returns 1 row(s), 1 column(s):

    QOY2(500

Returned query gives 1 row(s), 1 column(s):

    2

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C237  (question 43, database `pets_1`)

- Returned by: xiyansql-32b/seed303
- Class mass: 50/50
- Instances disagreeing: 23 of 27 (85%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** Find the name of students who have both cat and dog.

**Gold.**
```sql
select t1.fname from student as t1 join has_pet as t2 on t1.stuid  =  t2.stuid join pets as t3 on t3.petid  =  t2.petid where t3.pettype  =  'cat' intersect select t1.fname from student as t1 join has_pet as t2 on t1.stuid  =  t2.stuid join pets as t3 on t3.petid  =  t2.petid where t3.pettype  =  'dog'
```

**Returned.**
```sql
SELECT T1.fname , T1.lname FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid = T2.stuid JOIN pets AS T3 ON T3.petid = T2.petid WHERE T3.pettype = 'cat' INTERSECT SELECT T1.fname , T1.lname FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid = T2.stuid JOIN pets AS T3 ON T3.petid = T2.petid WHERE T3.pettype = 'dog'
```

**First disagreeing instance** `pets_1v5080.sqlite`.

Gold returns 5 row(s), 1 column(s):

    0
    003
    10
    David
    Oy01U(d

Returned query gives 4 row(s), 2 column(s):

    0 | 9
    003 | 10
    David | Linda
    Oy01U(d | AilCTbfL

Difference: col_count_differs, disjoint; 0 row(s) in common, 5 only in the gold, 4 only in the returned result.

### C238  (question 71, database `car_1`)

- Returned by: xiyansql-32b/seed303
- Class mass: 50/50
- Instances disagreeing: 57 of 60 (95%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** How many car models are produced by each manufacturer? List the count and the maker full name.

**Gold.**
```sql
select count(*) ,  t2.fullname from model_list as t1 join car_makers as t2 on t1.maker  =  t2.id group by t2.id;
```

**Returned.**
```sql
SELECT count(*) , t1.FullName FROM CAR_MAKERS AS t1 JOIN MODEL_LIST AS t2 ON t1.Id = t2.Maker GROUP BY t1.FullName
```

**First disagreeing instance** `car_1v5080.sqlite`.

Gold returns 32 row(s), 2 column(s):

    1 | WgId2j2tiOKXNbJE)
    1 | 19.0
    1 | 4
    1 | 3
    1 | 5
    1 | eugeaut
    2 | ER5Km8gHv9Mtc9w6Jlv
    1 | General Motors
    2 | JS8WGkUpkQNRnwpw
    1 | 9
    2 | 151
    1 | fia
    ... (32 rows total)

Returned query gives 28 row(s), 2 column(s):

    3 | 
    2 | 0qSpYywiWEZMmhE9zCeNGcUo5Y
    1 | 0xIjVZ
    1 | 1
    2 | 151
    1 | 19.0
    1 | 1975
    2 | 3
    1 | 3499
    1 | 4
    1 | 4000N1f3g
    3 | 5
    ... (28 rows total)

Difference: values differ; 24 row(s) in common, 6 only in the gold, 4 only in the returned result.

### C239  (question 365, database `world_1`)

- Returned by: xiyansql-32b/seed303
- Class mass: 50/50
- Instances disagreeing: 37 of 46 (80%)
- Row order compared: no (the gold has no ORDER BY)

**Question.** How many different forms of governments are there in Africa?

**Gold.**
```sql
SELECT count(DISTINCT GovernmentForm) FROM country WHERE Continent  =  "Africa"
```

**Returned.**
```sql
SELECT count(DISTINCT GovernmentForm) FROM country WHERE Region LIKE "%Africa%"
```

**First disagreeing instance** `world_1v5080.sqlite`.

Gold returns 1 row(s), 1 column(s):

    6

Returned query gives 1 row(s), 1 column(s):

    18

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.

### C240  (question 472, database `dog_kennels`)

- Returned by: xiyansql-32b/seed303
- Class mass: 50/50
- Instances disagreeing: 4 of 48 (8%)
- Row order compared: yes (the gold has ORDER BY)

**Question.** What is the description of the treatment type that is the cheapest overall?

**Gold.**
```sql
SELECT T1.treatment_type_description FROM Treatment_types AS T1 JOIN Treatments AS T2 ON T1.treatment_type_code  =  T2.treatment_type_code GROUP BY T1.treatment_type_code ORDER BY sum(cost_of_treatment) ASC LIMIT 1
```

**Returned.**
```sql
SELECT T1.treatment_type_description FROM Treatment_Types AS T1 JOIN Treatments AS T2 ON T1.treatment_type_code = T2.treatment_type_code GROUP BY T1.treatment_type_code ORDER BY avg(T2.cost_of_treatment) LIMIT 1
```

**First disagreeing instance** `dog_kennelsv5082.sqlite`.

Gold returns 1 row(s), 1 column(s):

    Vaccination

Returned query gives 1 row(s), 1 column(s):

    999

Difference: disjoint; 0 row(s) in common, 1 only in the gold, 1 only in the returned result.


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

### `employee_hire_evaluation`
```
  employee(Employee_ID, Name, Age, City)
  evaluation(Employee_ID, Year_awarded, Bonus)
  hiring(Shop_ID, Employee_ID, Start_from, Is_full_time)
  shop(Shop_ID, Name, Location, District, Number_products, Manager_name)
```

### `flight_2`
```
  airlines(uid, Airline, Abbreviation, Country)
  airports(City, AirportCode, AirportName, Country, CountryAbbrev)
  flights(Airline, FlightNo, SourceAirport, DestAirport)
```

### `network_1`
```
  Friend(student_id, friend_id)
  Highschooler(ID, name, grade)
  Likes(student_id, liked_id)
```

### `pets_1`
```
  Has_Pet(StuID, PetID)
  Pets(PetID, PetType, pet_age, weight)
  Student(StuID, LName, Fname, Age, Sex, Major, Advisor, city_code)
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
