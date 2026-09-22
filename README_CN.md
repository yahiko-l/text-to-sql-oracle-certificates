# Certified Against Which Oracle?

[English](README.md) | 简体中文

论文 *Certified Against Which Oracle? Execution Labels Set the Reported Risk of Conformal
Abstention for Text-to-SQL* 的实验代码：采样、评测与分析脚本，都在 `experiments/` 下。

## 分析流程

| 脚本 | 作用 |
| --- | --- |
| `e0_sample.py` | 按声明的策略用 vLLM 采样 SQL 候选（需要 GPU） |
| `e0_analyse.py` | oracle 干预的 2x2 |
| `c3_aggregate.py` | 汇总模型面板并套用冻结规则 |
| `c4_recompute.py` | 从每题充分统计量重算候选池 |
| `c4_exhaustive_splits.py` | 穷举全部 schema 不相交的数据库划分，而非随机抽取 |
| `c5_summarise.py` | 由分析器输出重建紧凑汇总表 |
| `c6_classify.py` | 对审计案例分层，并并入评审标签 |
| `c7_repair_audited.py` | 用审计后的语义标签重算 repair 指标 |
| `c8_baselines.py` | 已发表的不确定性基线在同一 oracle 干预下的表现 |
| `c9_tie_audit.py` | 测量并列规则代理实际付出的代价 |
| `c10_blind_audit_analyse.py` | 盲审专家审计的预注册分析 |
| `c11_dma_decomposition.py` | 把对比量分解到能承载它的事件上 |
| `c15_alignment_audit_analyse.py` | 独立标尺审计的冻结分析 |
| `c18_human_gap.py` | 用专家标签重新给证书打分 |
| `c20_matched_suite_contrast.py` | 在专家估计所用的同一批问题上重算 suite 标签下的对比 |

`figures/` 下是从这些结果文件排出论文十四张生成表、画出九张生成图的脚本。

脚本写出的结果文件命名为 `<步骤>_<checkpoint>_<条件>_results_<划分>[_per_question].json`。带
`_per_question` 的是每题充分统计量，论文报告的每个量都由它算出；其余是聚合结果。

## 运行

采样候选的脚本需要 GPU 与 vLLM；执行 SQL 的脚本需要基准数据集及其 test-suite 数据库，它们属于
第三方、由其作者自行分发，请自行取一份放到 `data/spider/`。其余脚本在笔记本上就能跑，只需
Python 3.11 或更高版本与 NumPy（`pip install -r requirements.txt`）。分析脚本读取前面各步写出的
结果文件，普查与两份审计的分析还要读取 AI 评审与专家的标注表。

## 引用

    @misc{liu2026certified,
      title  = {Certified Against Which Oracle? Execution Labels Set the
                Reported Risk of Conformal Abstention for Text-to-SQL},
      author = {Liu, Jiamiao and Qiao, Dewen and Zhang, Yu and Chen, Xuetao},
      year   = {2026},
      note   = {Preprint}
    }

## 许可证

代码采用 MIT 许可证（`LICENSE`）。
