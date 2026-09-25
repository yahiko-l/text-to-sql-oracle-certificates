# Certified Against Which Oracle?

[English](README.md) | 简体中文

论文 *Certified Against Which Oracle? Execution Labels Set the Reported Risk of Conformal
Abstention for Text-to-SQL* 的代码与数据：采样、评测与分析脚本，排版论文表格、绘制论文图的脚本，
以及这些脚本读写的、由本研究产生的全部文件。每个文件都放在脚本所写的路径上，克隆下来即可直接运行。

`supplementary.pdf` 是论文的补充材料：论文中以字母编号的章节、表和图都在其中。

## 快速开始

    pip install -r requirements.txt
    gunzip -k experiments/*.jsonl.gz
    python figures/gen_tables.py

`gen_tables.py` 把论文的十四张生成表写进 `figures/`，与论文中的表逐字节相同。
`figures/gen_fig2_cells.py` 到 `figures/gen_fig9_negative_control.py` 把其余八张生成图画进
`figures/`，`figures/gen_fig1_hero.py` 把第一张画在当前目录。以上在笔记本上几秒钟就能跑完。

## 内容

| 路径 | 内容 |
| --- | --- |
| `experiments/*.py` | 采样、评测与分析脚本 |
| `experiments/prereg3_run.sh`、`prereg3_lane.sh`、`c5_run.sh` | 每个 checkpoint 的采样配置 |
| `experiments/*_prompts*.jsonl.gz` | prompt，每题一条 |
| `experiments/*_candidates.jsonl.gz` | 候选池：每条采样 SQL 及其原始输出与对数概率 |
| `experiments/*_results_*.json` | 每题充分统计量（`_per_question`）及其聚合结果 |
| `experiments/c6_*`、`experiments/c7_*` | 两次普查：AI 标注者读的卷宗、两轮标注与裁定 |
| `experiments/c10_*`、`experiments/blind_audit/`、`blind-audit/` | 参考查询审计：专家收到的材料包、密钥、专家答卷与裁定 |
| `experiments/c15_*`、`experiments/alignment-audit/`、`alignment-audit/` | 独立标尺审计：材料包、密钥与专家答卷 |
| `experiments/spider_dev_*` | Spider dev 上的两项预实验：不同题目在基准自带数据库上的结果碰撞，以及参考查询的近似变异 |
| 其余 `experiments/*.json` | 面板汇总与全部事后分析 |
| `experiments/c4_manifest.json` | 面板每个候选池与每个 checkpoint 各权重分片的 SHA-256 |
| `data/spider_realistic/spider-realistic-matched-original.json` | Spider-Realistic 各题对应的 Spider dev 原始问法，供匹配对照使用 |
| `figures/` | 表格与图的脚本 |
| `supplementary.pdf` | 论文的补充材料 |

结果文件命名为 `<步骤>_<checkpoint>_<条件>_results_<划分>[_per_question].json`。带
`_per_question` 的是每题充分统计量，论文报告的每个量都由它算出；其余是聚合结果。`c4` 是预注册面板，
生成种子为 101、202、303，另有错误 schema 阴性对照；`c5` 是匹配原始 Spider 的对照；`e0`、`c1`、
`c2`、`c3` 与 `pilot` 是最终预注册之前的各阶段，其历程见补充材料；两个 `spider_dev_*` 文件是
促成这项干预的两项预实验。

## 第三方输入

执行 SQL 与重建 prompt 需要基准、test suite 与官方评测器。它们由各自作者分发，脚本在以下路径查找：

| 输入 | 来源 | 路径 |
| --- | --- | --- |
| Spider-Realistic，508 题 | Deng 等，[doi:10.5281/zenodo.5205322](https://doi.org/10.5281/zenodo.5205322) | `data/spider_realistic/spider-realistic.json` |
| Spider dev，1,034 题 | 同一记录，或 [Spider](https://yale-lily.github.io/spider) | `data/spider/dev.json` |
| distilled test suite | [test-suite-sql-eval](https://github.com/taoyds/test-suite-sql-eval)，下载链接见其 README | `data/spider/test_suite_database/<db_id>/` |
| 官方评测器 `exec_eval.py` 与 `parse.py` | 同一仓库 | `data/spider/` |
| `classical_test.pkl` | 同一仓库 | `data/classical/` |

## Checkpoint

| 标签 | Checkpoint |
| --- | --- |
| `xiyansql-32b` | [XGenerationLab/XiYanSQL-QwenCoder-32B-2504](https://huggingface.co/XGenerationLab/XiYanSQL-QwenCoder-32B-2504) |
| `omnisql-32b` | [seeklhy/OmniSQL-32B](https://huggingface.co/seeklhy/OmniSQL-32B) |
| `kwai-autosql-32b` | [Kwai-AutoSQL/Kwai-AutoSQL-32B](https://huggingface.co/Kwai-AutoSQL/Kwai-AutoSQL-32B) |
| `kwai-autosql-14b` | [Kwai-AutoSQL/Kwai-AutoSQL-14B](https://huggingface.co/Kwai-AutoSQL/Kwai-AutoSQL-14B) |
| `sqlcoder-70b` | [defog/sqlcoder-70b-alpha](https://huggingface.co/defog/sqlcoder-70b-alpha) |
| `llama3-sqlcoder-8b` | [defog/llama-3-sqlcoder-8b](https://huggingface.co/defog/llama-3-sqlcoder-8b) |

运行脚本从 `$MODEL_ROOT` 下按脚本列出的目录名读取各 checkpoint。`experiments/c4_manifest.json`
记录了所用每个权重分片的 SHA-256，下载的权重可据此核对。最终面板之前试过的通用模型写在各自的
`experiments/pilot_*_candidates_meta.json` 里。

## 复现

研究分四层，每层的产出都已发布，任何一层都可以单独重跑。所有命令都在仓库根目录运行。

**表格与图**：由结果文件生成，见快速开始。

**分析**：由每题充分统计量与标注文件算出。下表每条命令重写它对应的已发布文件，都只需 CPU，
多数几秒钟完成。

| 命令 | 写出 |
| --- | --- |
| `python experiments/c3_aggregate.py` | `c3_panel_summary.json` |
| `python experiments/c4_aggregate.py` | `c4_panel_summary.json` |
| `python experiments/c4_recompute.py --alphas 0.05 0.1 0.15 0.2 --out experiments/c4_alpha_curve.json` | alpha 曲线 |
| `python experiments/c4_recompute.py --pareto --out experiments/c4_frontier.json` | 风险-覆盖前沿 |
| `python experiments/c4_recompute.py --per-db --out experiments/c4_cluster_analysis.json` | 逐 schema 与留一 schema 的数值 |
| `python experiments/c4_crossfit_summary.py` | `c4_crossfit_summary.json` |
| `python experiments/c4_exhaustive_splits.py` | `c4_exhaustive_db_splits.json` |
| `python experiments/c4_gap_source.py` | `c4_gap_source_descriptive.json` |
| `python experiments/c5_summarise.py` | candidates-only、gold-free 与匹配对照的汇总 |
| `python experiments/c6_classify.py` | `c6_semantic_audit.json` |
| `python experiments/c6_classify.py --cases experiments/c7_repair_cases.json --pass-a experiments/c7_labels_pass_a.json --pass-b experiments/c7_labels_pass_b.json --adjudication experiments/c7_labels_adjudicated.json --carry-over experiments/c6_semantic_audit.json --date 2026-09-06 --out experiments/c7_semantic_audit.json` | `c7_semantic_audit.json` |
| `python experiments/c6_gap_audited.py` | `c6_gap_audited.json` |
| `python experiments/c7_accepted_side.py` | `c7_accepted_side.json` |
| `python experiments/c7_repair_audited.py` | `c7_repair_audited.json` |
| `python experiments/c8_baselines.py --check-crc 5000 --rank-decomposition --same-answer-auroc --grid-sensitivity --verify` | `c8_baselines.json` |
| `python experiments/c8_baselines.py --audited agreed --out experiments/c8_baselines_audited_agreed.json` | 四种审计口径之一，`narrow`、`unanimous` 与 `wide` 同理 |
| `python experiments/c9_tie_audit.py --enumerate --populations --recompute --six-scores --gap-ladder` | `c9_tie_audit.json`、`c9_tied_decisions.json` |
| `python experiments/c10_blind_audit_analyse.py --responses experiments/blind_audit/RESPONSES_专家1.clean.csv experiments/blind_audit/RESPONSES_专家2.clean.csv --adjudicated experiments/blind_audit/ADJUDICATION_标注.clean.csv` | `c10_blind_audit_result.json` |
| `python experiments/c10_blind_audit_sensitivity.py` | `c10_blind_audit_sensitivity.json` |
| `python experiments/c11_dma_decomposition.py` | `c11_dma_decomposition.json` |
| `python experiments/c12_sample_budget.py` | `c12_sample_budget.json` |
| `python experiments/c13_blind_audit_weighted.py` | `c13_blind_audit_weighted.json` |
| `python experiments/c14_alignment_power.py` | `c14_alignment_power.json` |
| `python experiments/c15_alignment_audit_analyse.py --responses experiments/alignment-audit/RESPONSES_E1.csv --out experiments/c15_alignment_audit_result_E1.json` | 第一位专家的结果，`E2` 同理 |
| `python experiments/c16_alignment_secondary.py` 至 `python experiments/c21_expert_agreement.py` | 各写一个文件 |
| `python experiments/panel_entry.py kwai-autosql-32b kwai-autosql-14b xiyansql-32b omnisql-32b sqlcoder-70b llama3-sqlcoder-8b --prefix experiments/pilot3 --out experiments/panel_entry_3.json` | 最终面板的准入判定 |

`panel_entry_3.json` 中 `llama3-sqlcoder-8b` 的记录用文字说明了排除原因：它的试跑没有产出任何可解析
的输出，而脚本的状态词表没有对应这种情况的条目。`c4_cluster_analysis.json` 另外保留了一段标为已被取代的
早期 schema bootstrap，它已由穷举划分取代。

**执行**：把候选池在两个 oracle 下执行，需要第三方输入。`e0_analyse.py` 把一个候选池变成一种划分的
结果文件；每个结果文件都在 `provenance` 下记录了生成它所用的候选池、选项与评测器，据此可以读出对应的
命令。`c6_semantic_cases.py` 与 `c7_repair_cases.py` 抽取普查案例；`c9_tie_reconstruct.py`、
`c10_blind_audit_build.py` 与 `c15_alignment_audit_build.py` 重建并列重构结果与两份审计条目表，
条目表逐字节相同。Spider dev 上的两项预实验不需要候选池，只需要基准及其 test suite：
`spider_dev_collision_census.py` 与 `spider_dev_near_miss_census.py` 各自在 CPU 上一分钟内重写同名文件。

**采样**：需要 GPU 与 vLLM。论文的候选池用 vLLM 0.22.1、bfloat16 在 H100 80GB 上采样；
张量并行数等于可见卡数：

    MODEL_ROOT=/path/to/checkpoints CUDA_VISIBLE_DEVICES=0,1 \
      bash experiments/prereg3_run.sh xiyansql-32b main 101

## 记录

结果文件记录了生成它的候选池、评测器与脚本的 SHA-256。解压后的候选池与记录逐字节一致，
test-suite 仓库中的评测器也一致。脚本以最新版本发布：预注册之后新增的选项默认保持预注册的行为，
注释与帮助文字也有改动，所以脚本的哈希可能与记录不同，而计算内容相同。
研究所用机器上的 checkpoint 路径已替换为 checkpoint 目录名。

## 引用

    @misc{liu2026certified,
      title  = {Certified Against Which Oracle? Execution Labels Set the
                Reported Risk of Conformal Abstention for Text-to-SQL},
      author = {Liu, Jiamiao and Qiao, Dewen and Zhang, Yu and Chen, Xuetao},
      year   = {2026},
      note   = {Preprint}
    }

## 许可证

代码采用 MIT 许可证（`LICENSE`）。数据采用 CC BY-SA 4.0（`LICENSE-DATA`），因为 prompt 与候选池
包含来自 Spider 的问题与参考查询，而 Spider 以该许可证分发。
