# 从这里开始 / Start here

参考查询盲审的第三轮裁定。13 项，预计 1 到 2 小时。
Third-pass adjudication for the blinded review of reference queries. 13 items, 1 to 2 hours.

---

## 中文

> **这是一次独立重裁。** 这 13 项此前有人裁定过，但那位裁定人是项目负责人，与被检验的主张有利害关系，
> 因此那一轮不作数。你的判断将取代它。请不要去找那一轮的结果，也不要向项目组打听。

### 你在这一轮的位置

两位专家各自独立判完了全部 153 项，互不通气。其中 140 项两人一致，按协议**不得改动**，也不在本包里。
剩下 13 项两人不一致，由你来定。这一轮不再盲：你会看到两位的判定和他们各自的理由，这是设计如此。

你仍然看不到、也请不要去找的：哪些题曾被一个自动流程标记为可疑、各类题目的比例、项目仓库里的任何先前标注。

### 三步

1. **读简报** `ADJUDICATION_BRIEF.md`。13 项逐条给出：自然语言问题、基准自带的参考查询、
   **这条查询实际返回什么**，以及两位专家的判定与理由。
2. **要自己验就跑一下。** 5 个数据库随包附带：

       python3 run.py --schema world_1
       python3 run.py --db world_1 --sql "select ... "

   需要 Python 3.8 以上，不需要装任何东西。（本包不含完整条目表，所以 `run.py Q003` 这种按编号取题的用法在这里不适用，
   13 项的查询和结果简报里都有。）
3. **填** `ADJUDICATION.csv`，13 行，只填前四列：`verdict`、`defect_type`、`borderline`、`note`。
   后面 6 列是两位专家的原判与理由，供你阅读，不要改。`item_id` 保持原样，行序不要动，存回 UTF-8。

### 判定值

| 值 | 含义 |
|---|---|
| `gold_correct` | 参考查询正确回答了这个问题 |
| `gold_defective` | 问题有确定的答案，而参考查询算的不是它 |
| `question_underspecified` | 问题本身没把争议点说死，多种写法都站得住 |
| `cannot_judge` | 无法判断，在 `note` 里写清卡在哪里 |

`gold_defective` 时 `defect_type` 必填，从九个类型里取最主要的一个：
`case_sensitivity`、`text_column_numeric_or_ordering`、`wrong_extremum`、`missing_join_condition`、
`wrong_or_negated_filter`、`incomplete_projection`、`wrong_set_operation_key`、`wrong_grouping`、`other`。

`borderline` 填 `yes` 或 `no`。`note` 一句话理由，`gold_defective` 与 `cannot_judge` 必填。

### 两条要紧的

- **你不必在两位给出的答案里二选一。** 如果你认为两位都不对，就填第三个值。裁定不是投票。
- **`gold_defective` 与 `question_underspecified` 的分界**是本次复核最关键的一条，13 项里有好几项卡在这里。
  判据是：你能不能把这个问题**唯一确定地**说成"它要的是什么"？能，而参考查询返回的不是那个，就是 `gold_defective`；
  不能，几个讲道理的人会写出不同的查询且都忠实于问题，就是 `question_underspecified`。

### 交回

只需要填好的 `ADJUDICATION.csv`。

---

## English

> **This is an independent re-adjudication.** These 13 items were adjudicated once before, by the
> project lead, who has a stake in the claim under test, so that pass does not count. Yours replaces
> it. Please do not look for its result or ask the project team about it.

### Where this pass sits

Two experts each completed all 153 items independently, without consulting each other. They agree
on 140 items, which **must not be revised** and are not in this package. The remaining 13 are
where they disagree, and you decide those. This pass is not blinded: you see both verdicts and
both lines of reasoning, by design.

What you still do not see, and should not go looking for: which items an automated process flagged
as suspect, the proportions of each category, and any earlier labels in the project repository.

### Three steps

1. **Read the brief**, `ADJUDICATION_BRIEF.md`. For each of the 13 items it gives the natural
   language question, the reference query the benchmark ships, **what that query actually
   returns**, and each expert's verdict and reasoning.
2. **Run things yourself if you want to.** The 5 databases involved ship with this package:

       python3 run.py --schema world_1
       python3 run.py --db world_1 --sql "select ... "

   Python 3.8 or later, nothing to install. (This package does not carry the full item sheet, so
   looking an item up by number is not available here; the 13 queries and their results are all in
   the brief.)
3. **Fill in** `ADJUDICATION.csv`, 13 rows, only the first four columns: `verdict`, `defect_type`,
   `borderline`, `note`. The six columns after them are the experts' verdicts and notes, for you to
   read, not to change. Keep `item_id` as it is, do not reorder rows, save as UTF-8.

### Verdicts

| Value | Meaning |
|---|---|
| `gold_correct` | the reference query correctly answers the question |
| `gold_defective` | the question has a determinate answer and the reference query computes something else |
| `question_underspecified` | the question leaves the contested point open and several readings are defensible |
| `cannot_judge` | you cannot decide; say in `note` what stops you |

`defect_type` is required when the verdict is `gold_defective`, one of: `case_sensitivity`,
`text_column_numeric_or_ordering`, `wrong_extremum`, `missing_join_condition`,
`wrong_or_negated_filter`, `incomplete_projection`, `wrong_set_operation_key`, `wrong_grouping`,
`other`. `borderline` is `yes` or `no`. `note` is one sentence, required for `gold_defective` and
`cannot_judge`.

### Two things that matter

- **You are not restricted to the two verdicts on offer.** If you think both experts are wrong,
  enter a third value. This is adjudication, not a vote.
- **The boundary between `gold_defective` and `question_underspecified`** is the most consequential
  call in this review, and several of the 13 turn on it. The test: can you state, uniquely, what
  the question is asking for? If yes, and the reference query does not return that, it is
  `gold_defective`. If no, and reasonable people would write different queries each faithful to the
  question, it is `question_underspecified`.

### Returning it

The filled `ADJUDICATION.csv`, and nothing else.
