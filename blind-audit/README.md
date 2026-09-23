# 从这里开始 / Start here

基准参考查询的盲审。153 项，预计 5 到 10 小时，可以分次做。
A blinded review of benchmark reference queries. 153 items, 5 to 10 hours, can be split over sittings.

---

## 中文

### 五步

1. **读协议**：`PROTOCOL.md`。特别是第 4 节的四个判定值，以及 `gold_defective` 与
   `question_underspecified` 的分界，那是本次复核最关键的一条。
2. **验包**：`python3 run.py --check`。应当显示 153 项、17 个数据库、153 条查询全部可执行。
   需要 Python 3.8 以上，不需要安装任何第三方库。
3. **逐项判**：`python3 run.py Q001`，它会显示问题与参考查询，并把查询在数据库上跑一遍打出结果。
   接着 `Q002`、`Q003`，一直到 `Q153`。想自己查数据用
   `python3 run.py --schema <库名>` 和 `python3 run.py --db <库名> --sql "..."`。
4. **填答卷**：`RESPONSES.csv`，一行一项，五列：`item_id`、`verdict`、`defect_type`、
   `borderline`、`note`。`item_id` 保持原样，不要重排行序。用文本编辑器或表格软件都可以，
   **存回来时请确认是 UTF-8 编码的 CSV**。
5. **交回**：把文件名改成 `RESPONSES_你的姓名.csv` 再发回。只需要这一个文件。

### 判定值

| 值 | 含义 |
|---|---|
| `gold_correct` | 参考查询正确回答了这个问题 |
| `gold_defective` | 问题有确定的答案，而参考查询算的不是它 |
| `question_underspecified` | 问题本身没把争议点说死，多种写法都站得住 |
| `cannot_judge` | 无法判断，在 `note` 里写清卡在哪里 |

`borderline` 填 `yes` 或 `no`：只要觉得换个人可能判成另一个值，就填 `yes`。
标 `yes` 不会让你的判断被打折，分析会把非难判的部分单独报一遍。

### 三条要紧的

- **请执行，不要只读。** 很多缺陷只有跑起来才看得见，比如字面量大小写对不上导致返回空表，
  或者数字存在 TEXT 列里、排序按字典序。
- **本包里没有任何模型输出**，也不会告诉你哪些题曾被自动流程标记过。这是刻意的。
- **请不要去查项目仓库或先前的标注结果。** 本次复核的全部价值就在于它独立于那个流程。

有疑问先看 `PROTOCOL.md`，那里有完整说明。

---

## English

### Five steps

1. **Read the protocol**: `PROTOCOL_EN.md`. In particular section 4, the four verdicts, and the
   boundary between `gold_defective` and `question_underspecified`, which is the most
   consequential call in this review.
2. **Check the package**: `python3 run.py --check`. It should report 153 items, 17 databases and
   153 queries that run. Python 3.8 or later, no third-party libraries.
3. **Work through the items**: `python3 run.py Q001` shows the question and the reference query
   and executes it against the database. Then `Q002`, `Q003`, through `Q153`. To look at the data
   yourself, `python3 run.py --schema <db>` and `python3 run.py --db <db> --sql "..."`.
4. **Fill in the sheet**: `RESPONSES.csv`, one row per item, five columns: `item_id`, `verdict`,
   `defect_type`, `borderline`, `note`. Keep `item_id` as it is and do not reorder the rows. A
   text editor or a spreadsheet both work; **save it back as UTF-8 CSV**.
5. **Return it**: rename to `RESPONSES_<yourname>.csv` and send that one file back.

### Verdicts

| Value | Meaning |
|---|---|
| `gold_correct` | the reference query correctly answers the question |
| `gold_defective` | the question has a determinate answer and the reference query computes something else |
| `question_underspecified` | the question leaves the contested point open and several readings are defensible |
| `cannot_judge` | you cannot decide; say in `note` what stops you |

`borderline` is `yes` or `no`: mark `yes` whenever another reviewer might reasonably land on a
different verdict. It does not discount your judgement; the analysis reports the non-borderline
subset separately.

### Three things that matter

- **Execute, do not only read.** Many defects are visible only when the query runs, such as a
  string literal whose case does not match what is stored, or a number kept in a TEXT column and
  sorted lexicographically.
- **There is no model output anywhere in this package**, and which items an automated process
  flagged is not disclosed. That is deliberate.
- **Please do not consult the project repository or any earlier labels.** The value of this review
  is that it is independent of that process.

`PROTOCOL_EN.md` has the full instructions.
