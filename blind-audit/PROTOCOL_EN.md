# Blinded review of benchmark reference queries: protocol

**Version**: 2026-09-06, built in the same batch as `ITEMS.md` and `RESPONSES.csv`
**Audience**: the invited SQL experts. This package is all the material you need.
**Effort**: 153 items at 2 to 4 minutes each, so roughly 5 to 10 hours. It can be split over several sittings.

## 1. What you are judging

Each item gives you a natural language question, the database it belongs to, and the
**reference query the benchmark ships as the correct answer**.

**Your task is one judgement: does this reference query correctly answer this question?**

Not whether it is elegant, not whether you would write it differently. Whether what it
returns is the answer the question asks for.

## 2. What you will not see, and should not go looking for

- **No model output.** There is no second candidate query anywhere in this package. That is
  deliberate: you judge the reference query on its own, without an alternative pulling your
  reading of the question in some direction.
- **No earlier judgements.** Some of these questions were flagged as suspect by an automated
  process and some were not. **Which are which is not disclosed here**, the item order is
  shuffled, the numbering carries no information, and the proportions are not published.
- **Please do not consult the project repository or any earlier labels.** The entire value of
  this review is that it is independent of that process. If you happen to see an earlier
  judgement, say so in the `note` column for that item and it will be reported separately.

## 3. How to judge: execute, do not only read

**Run the reference query against the given database and look at what it actually returns.**
The package ships the databases, and `run.py` will do it for you:

```
python3 run.py Q001                 # show item Q001 and execute its reference query
python3 run.py --schema world_1     # tables, columns and row counts of one database
python3 run.py --db world_1 --sql "select distinct Continent from country"
python3 run.py --check              # confirm the package is complete before you start
```

`sqlite3` on the command line works equally well; the databases are plain SQLite files
under `data/spider/test_suite_database/`, opened read only.

Many problems are visible only once the query runs. For example:

- a string literal whose case does not match what is stored, so a condition never holds and
  the result is empty
- a number stored in a TEXT column, so `ORDER BY` sorts lexicographically and `'9'` lands
  after `'100'`
- a question asking for the youngest, answered with `MAX(age)`
- a `JOIN` with no `ON`, producing a cross product
- a filter condition that is negated
- a question asking for all of X where the query returns only some columns of X
- a set operation (`INTERSECT` or `EXCEPT`) applied to names rather than keys, so distinct
  entities that share a name are merged

These are shapes that can occur. They are not a checklist, and none of them is claimed to be
present in this batch. Use your own judgement.

## 4. Verdicts (the `verdict` column, choose one)

| Value | Meaning |
|---|---|
| `gold_correct` | the reference query correctly answers the question |
| `gold_defective` | the question has a determinate answer and the reference query computes something else |
| `question_underspecified` | the question itself leaves the contested point open, several readings are defensible, and the reference query is one of them |
| `cannot_judge` | you cannot decide; say in `note` what stops you |

**The boundary between `gold_defective` and `question_underspecified` is the most consequential
call in this review. Use this test:**

> Can you state, uniquely, what the question is asking for?
> If yes, and the reference query does not return that, the verdict is `gold_defective`.
> If no, and reasonable people would write different queries each faithful to the question,
> the verdict is `question_underspecified`.

**An illustration of the boundary** (constructed, not from this batch): a question asking for
the names of all employees, answered by a reference query that returns only surnames, is
`gold_defective`, because "name" has a determinate referent in that schema. A question asking
for the major departments, answered by taking the three largest by headcount, is
`question_underspecified`, because "major" was never defined.

## 5. The other two columns

- **`defect_type`**: fill in only when the verdict is `gold_defective`, choosing the single
  most important one: `case_sensitivity`, `text_column_numeric_or_ordering`, `wrong_extremum`,
  `missing_join_condition`, `wrong_or_negated_filter`, `incomplete_projection`,
  `wrong_set_operation_key`, `wrong_grouping`, `other`. Explain `other` in `note`.
- **`borderline`**: `yes` or `no`. **This column matters, please fill it honestly.** If you
  think another reviewer might reasonably land on a different verdict, mark `yes`. The
  analysis reports the non-borderline subset separately, so marking `yes` does not discount
  your judgement, it makes the result more credible.
- **`note`**: one sentence of reasoning. Required for `gold_defective` and `cannot_judge`,
  optional otherwise.

## 6. Two experts, independent, then adjudication

The intended setup is **two experts, each completing all 153 items independently**, without
consulting each other. Then:

1. agreement and Cohen's kappa between the two are computed, as the reliability figure for
   this review itself;
2. a third pass adjudicates **only the items where the two disagree**, either by a third
   person or by the two discussing; items they agreed on **are not revised**;
3. the analysis runs on the adjudicated labels.

With only one expert the review is still valid, but kappa cannot be computed, and that is
recorded in the paper as a limitation.

## 7. What to return

The filled `RESPONSES.csv`, and nothing else. Keep the `item_id` column as it is and do not
reorder the rows.

## 8. What this result is used for

It tests whether a judgement previously made by an automated process holds up. **It may
confirm that judgement and it may overturn it.** The analysis, including what counts as an
overturn, was written and committed before you started, and any later change to it has to be
recorded as a documented deviation.

**The preregistration document is deliberately not in this package**, because it states the
size of each stratum, and reading it would tell you the proportion of suspect items in this
batch. It is in the project repository, and you are welcome to read it **after** you return
`RESPONSES.csv`. If you want assurance that it really was frozen beforehand, ask the project
lead for its commit hash and timestamp, which establishes that it predates your judgements
without your having to read it.

Please judge as your expertise tells you. Which direction is convenient for the project is
not your concern.
