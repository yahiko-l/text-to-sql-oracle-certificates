# 裁定用简报

两位专家在以下 13 项上不一致，其余各项一致，按协议不得改动。
每项给出问题、参考查询、查询实际返回的结果，以及两位专家的判定与理由。
读完在 `ADJUDICATION.csv` 里填 `verdict`、`defect_type`、`borderline`、`note` 四列。

## Q003

数据库：`tvshow`

**问题.** Find the series name and country of the tv channel that is playing some cartoons  Ben Jones and Michael Chang directs?

**参考查询.**

```sql
SELECT T1.series_name ,  T1.country FROM TV_Channel AS T1 JOIN cartoon AS T2 ON T1.id = T2.Channel WHERE T2.directed_by  =  'Michael Chang' INTERSECT SELECT T1.series_name ,  T1.country FROM TV_Channel AS T1 JOIN cartoon AS T2 ON T1.id = T2.Channel WHERE T2.directed_by  =  'Ben Jones'
```

**它返回什么.**

```
series_name | Country
---------------------
MTV Dance | United Kingdom
1 row(s)
```

**专家一** `gold_correct`：按频道分别核验两位导演的作品后，唯一同时满足条件的频道为707，输出MTV Dance及United Kingdom正确。

**专家二** `question_underspecified`（难判）：题目未明确两位导演是分别有作品在同一频道播出还是共同执导作品，金标采用前一种解释并返回MTV Dance、United Kingdom。

---

## Q022

数据库：`world_1`

**问题.** What is the official language used in the country the name of whose chief of state is Beatrix.

**参考查询.**

```sql
SELECT T2.Language FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code  =  T2.CountryCode WHERE T1.HeadOfState  =  "Beatrix" AND T2.IsOfficial  =  "T"
```

**它返回什么.**

```
Language
--------
Dutch
Dutch
Papiamento
Dutch
4 row(s)
```

**专家一** `gold_correct`（难判）：正确限定HeadOfState=Beatrix且IsOfficial=T，四行语言对应三个国家／地区的官方语言记录，重复Dutch来自不同实体。

**专家二** `question_underspecified`（难判）：库中Aruba、Netherlands Antilles和Netherlands的元首都为Beatrix，题目未确定单一国家或去重口径，金标返回三地官方语言并重复Dutch。

---

## Q033

数据库：`pets_1`

**问题.** Find the weight of the youngest dog.

**参考查询.**

```sql
SELECT weight FROM pets ORDER BY pet_age LIMIT 1
```

**它返回什么.**

```
weight
------
9.3
1 row(s)
```

**专家一** `gold_defective`（难判）：题目限定dog但金标在全部pets中取最小年龄，缺少PetType过滤；当前最年轻宠物恰好是dog，输出9.3与正确答案偶合。

**专家二** `gold_correct`（难判）：本库最年轻宠物恰是唯一1岁犬，重量9.3，与限定dog后的答案一致，但金标没有显式犬类过滤，不能据此认定对其他数据也正确。

---

## Q034

数据库：`world_1`

**问题.** Which continent has the most diverse languages?

**参考查询.**

```sql
SELECT T1.Continent FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code  =  T2.CountryCode GROUP BY T1.Continent ORDER BY COUNT(*) DESC LIMIT 1
```

**它返回什么.**

```
Continent
---------
Africa
1 row(s)
```

**专家一** `gold_defective`（难判）：按语言种类多样性应对Language去重，金标却计国家—语言记录数；非洲310条记录实际为215种语言，两种计数当前恰均使Africa居首。

**专家二** `gold_correct`（难判）：金标数的是国家—语言记录而非不同语言，但当前Africa同时以310条记录及215种不同语言居首，实际返回大陆正确。

---

## Q058

数据库：`car_1`

**问题.** What are the different models created by either General Motors or over 3500 lbs?

**参考查询.**

```sql
SELECT DISTINCT T2.Model FROM CAR_NAMES AS T1 JOIN MODEL_LIST AS T2 ON T1.Model  =  T2.Model JOIN CAR_MAKERS AS T3 ON T2.Maker  =  T3.Id JOIN CARS_DATA AS T4 ON T1.MakeId  =  T4.Id WHERE T3.FullName  =  'General Motors' OR T4.weight  >  3500;
```

**它返回什么.**

```
Model
-----
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
... 13 rows in total
```

**专家一** `gold_defective`：OR中的重量条件不要求有制造商记录，但对CAR_MAKERS的内连接先删掉制造商缺失且重量>3500的hi车型，金标13种而独立求两条件并集应为14种。

**专家二** `gold_correct`：制造商FullName为General Motors或车辆重量大于3500的OR条件及四表连接均正确，去重后得到13个车型。

---

## Q070

数据库：`pets_1`

**问题.** How much does the youngest dog weigh?

**参考查询.**

```sql
SELECT weight FROM pets ORDER BY pet_age LIMIT 1
```

**它返回什么.**

```
weight
------
9.3
1 row(s)
```

**专家一** `gold_defective`（难判）：缺少PetType=dog条件，实际计算最年轻宠物的体重而不是限定狗类；当前两者恰同为PetID=2003、体重9.3，属结果偶合。

**专家二** `gold_correct`（难判）：本库年龄最小的全部宠物就是1岁犬2003，重量9.3，金标实际答案正确，但未限定dog使其正确性依赖当前数据。

---

## Q080

数据库：`world_1`

**问题.** Which continent speaks the most languages?

**参考查询.**

```sql
SELECT T1.Continent FROM country AS T1 JOIN countrylanguage AS T2 ON T1.Code  =  T2.CountryCode GROUP BY T1.Continent ORDER BY COUNT(*) DESC LIMIT 1
```

**它返回什么.**

```
Continent
---------
Africa
1 row(s)
```

**专家一** `gold_defective`（难判）：最多语言应统计不同Language而非国家—语言记录数，非洲实际215种语言却被COUNT(*)计成310；当前输出Africa与去重结果恰一致。

**专家二** `gold_correct`（难判）：COUNT(*)计算国家—语言记录而不是不同语言种数，但Africa在两种算法下都唯一居首（310条／215种），本库返回结果正确。

---

## Q108

数据库：`pets_1`

**问题.** What are the students' first names who have both cats and dogs?

**参考查询.**

```sql
SELECT T1.Fname FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid  =  T2.stuid JOIN pets AS T3 ON T3.petid  =  T2.petid WHERE T3.pettype  =  'cat' INTERSECT SELECT T1.Fname FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid  =  T2.stuid JOIN pets AS T3 ON T3.petid  =  T2.petid WHERE T3.pettype  =  'dog'
```

**它返回什么.**

```
Fname
-----
(zero rows)
0 row(s)
```

**专家一** `gold_defective`（难判）：猫主人与狗主人应先按StuID取交集再投影Fname，按Fname取交集可能拼接同名不同学生；当前按主键核验也为空，未出现实际误配，故标边界。

**专家二** `gold_correct`（难判）：按student_id核验确无同时养猫狗的学生，金标空集在本库正确；按Fname而非主键求交存在同名学生误配风险，但当前未触发。

---

## Q137

数据库：`world_1`

**问题.** Return the names of the 3 countries with the fewest people.

**参考查询.**

```sql
SELECT Name FROM country ORDER BY Population ASC LIMIT 3
```

**它返回什么.**

```
Name
----
Antarctica
French Southern territories
Bouvet Island
3 row(s)
```

**专家一** `question_underspecified`（难判）：有七个国家／地区人口均为0并列最少，题目要求三个却未指定并列选择规则，金标返回其中三个，其他三元组合也同样符合人口排序。

**专家二** `gold_correct`（难判）：当前有7个国家人口并列为0，题目明确要3个，金标返回其中3个最低人口国家，未规定并列项内部的选择次序。

---

## Q138

数据库：`car_1`

**问题.** What car has the most different versions?

**参考查询.**

```sql
SELECT Model FROM CAR_NAMES GROUP BY Model ORDER BY count(*) DESC LIMIT 1;
```

**它返回什么.**

```
Model
-----
ford
1 row(s)
```

**专家一** `question_underspecified`（难判）：different versions未定义为MakeId记录数还是不同Make名称，金标按记录数计ford为53而按不同名称为37，两个合理口径当前均由ford居首。

**专家二** `gold_correct`（难判）：按车型记录数ford以53条最多，按不同Make核验也以37款最多，虽然versions可有去重口径差异，本库返回ford在两种口径下都正确。

---

## Q139

数据库：`car_1`

**问题.** Which distinctive models are produced by General Motors or heavier than 3500?

**参考查询.**

```sql
SELECT DISTINCT T2.Model FROM CAR_NAMES AS T1 JOIN MODEL_LIST AS T2 ON T1.Model  =  T2.Model JOIN CAR_MAKERS AS T3 ON T2.Maker  =  T3.Id JOIN CARS_DATA AS T4 ON T1.MakeId  =  T4.Id WHERE T3.FullName  =  'General Motors' OR T4.weight  >  3500;
```

**它返回什么.**

```
Model
-----
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
... 13 rows in total
```

**专家一** `gold_defective`：制造商内连接错误限制了OR的重量分支，车型hi虽有重量>3500车辆但其制造商外键无对应记录而被丢弃，金标13种而完整条件并集为14种。

**专家二** `gold_correct`：经车型、制造商和车辆数据连接，以General Motors或重量大于3500作OR筛选并去重，正确返回13个不同车型。

---

## Q145

数据库：`student_transcripts_tracking`

**问题.** Find the last name of the students who currently live in North Carolina but have not registered in any degree program.

**参考查询.**

```sql
SELECT T1.last_name FROM Students AS T1 JOIN Addresses AS T2 ON T1.current_address_id  =  T2.address_id WHERE T2.state_province_county  =  'NorthCarolina' EXCEPT SELECT DISTINCT T3.last_name FROM Students AS T3 JOIN Student_Enrolment AS T4 ON T3.student_id  =  T4.student_id
```

**它返回什么.**

```
last_name
---------
Gleichner
Weimann
2 row(s)
```

**专家一** `gold_defective`（难判）：排除已入学学生应按student_id而不是last_name做集合差，同姓不同人会相互排除；当前姓氏无重复且主键核验同为Gleichner、Weimann，故标边界。

**专家二** `gold_correct`（难判）：按student_id排除入学记录后确为Gleichner、Weimann两人，当前15名学生的姓均唯一，按姓EXCEPT结果正确但存在同姓误排的潜在风险。

---

## Q146

数据库：`world_1`

**问题.** What are the cities who have more than 160000 people and less than 900000 people?

**参考查询.**

```sql
SELECT name FROM city WHERE Population BETWEEN 160000 AND 900000
```

**它返回什么.**

```
Name
----
Qandahar
Herat
Amsterdam
Rotterdam
Haag
Utrecht
Eindhoven
Tilburg
Groningen
Breda
Tirana
Oran
... 1860 rows in total
```

**专家一** `gold_defective`（难判）：more than和less than要求严格开区间，BETWEEN却包含160000和900000两个端点；当前恰无端点记录，因此1860行输出暂与严格条件相同。

**专家二** `gold_correct`（难判）：BETWEEN包含边界而题目用严格大于和小于，但本库没有人口恰为160000或900000的城市，金标与严格条件实际均返回1860行。

---
