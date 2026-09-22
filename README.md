# Certified Against Which Oracle?

English | [简体中文](README_CN.md)

Experiment code for *Certified Against Which Oracle? Execution Labels Set the Reported Risk of
Conformal Abstention for Text-to-SQL*: the sampling, evaluation and analysis scripts, all in
`experiments/`.

## The analysis, step by step

| Script | What it does |
| --- | --- |
| `e0_sample.py` | samples SQL candidates with vLLM under a declared policy (needs a GPU) |
| `e0_analyse.py` | the oracle-intervention 2x2 |
| `c3_aggregate.py` | aggregates the model panel and applies the frozen rules |
| `c4_recompute.py` | re-analyses the pools from their per-question sufficient statistics |
| `c4_exhaustive_splits.py` | every schema-disjoint database split, exactly, instead of random draws |
| `c5_summarise.py` | rebuilds the compact summary tables from the analyser outputs |
| `c6_classify.py` | stratifies the audit cases and folds in the reviewer labels |
| `c7_repair_audited.py` | recomputes the repair metric with audited semantic labels |
| `c8_baselines.py` | published uncertainty baselines under the same oracle intervention |
| `c9_tie_audit.py` | measures what the tie-rule proxy costs |
| `c10_blind_audit_analyse.py` | the preregistered analysis of the blinded expert audit |
| `c11_dma_decomposition.py` | decomposes the contrast into the events that can carry it |
| `c15_alignment_audit_analyse.py` | the frozen analysis of the independent-yardstick audit |
| `c18_human_gap.py` | the certificate re-scored against the expert labels |
| `c20_matched_suite_contrast.py` | the suite-label contrast on the questions the expert estimate is built from |

`figures/` holds the scripts that typeset the paper's fourteen generated tables and draw its nine
generated figures from those result files.

The scripts name their result files `<step>_<checkpoint>_<condition>_results_<partition>[_per_question].json`.
The `_per_question` files are the sufficient statistics every reported quantity is computed from;
the others are the aggregates.

## Running the code

Scripts that sample candidates need a GPU and vLLM, and scripts that execute SQL need the benchmark
and its test-suite databases, which are third party and distributed by their own authors: place a
copy at `data/spider/`. Everything else runs on a laptop with Python 3.11 or newer and NumPy
(`pip install -r requirements.txt`). The analysis scripts read the result files the earlier steps
write, and the census and audit analyses also read the label sheets of the AI reviewer and of the
experts.

## Citing this work

    @misc{liu2026certified,
      title  = {Certified Against Which Oracle? Execution Labels Set the
                Reported Risk of Conformal Abstention for Text-to-SQL},
      author = {Liu, Jiamiao and Qiao, Dewen and Zhang, Yu and Chen, Xuetao},
      year   = {2026},
      note   = {Preprint}
    }

## License

The code is under the MIT License (`LICENSE`).
