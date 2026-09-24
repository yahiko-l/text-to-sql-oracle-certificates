# Certified Against Which Oracle?

English | [简体中文](README_CN.md)

Code and data for *Certified Against Which Oracle? Execution Labels Set the Reported Risk of
Conformal Abstention for Text-to-SQL*: the sampling, evaluation and analysis scripts, the scripts
that typeset the paper's tables and draw its figures, and every file those scripts read or write
that the study produced. Each file sits at the path the scripts name, so the scripts run on a clone
as they are.

`supplementary.pdf` is the paper's supplementary material: the sections, tables and figures the
paper numbers with a letter.

## Quick start

    pip install -r requirements.txt
    gunzip -k experiments/*.jsonl.gz
    python figures/gen_tables.py

`gen_tables.py` writes the paper's fourteen generated tables into `figures/`, byte for byte the
tables in the paper. `figures/gen_fig2_cells.py` to `figures/gen_fig9_negative_control.py` draw the
other eight generated figures into `figures/`, and `figures/gen_fig1_hero.py` draws the first into
the working directory. All of this runs on a laptop in seconds.

## What is here

| Path | Contents |
| --- | --- |
| `experiments/*.py` | sampling, evaluation and analysis scripts |
| `experiments/prereg3_run.sh`, `prereg3_lane.sh`, `c5_run.sh` | the sampling configuration of each checkpoint |
| `experiments/*_prompts*.jsonl.gz` | prompts, one record per question |
| `experiments/*_candidates.jsonl.gz` | candidate pools: every sampled SQL with its raw output and log-probability |
| `experiments/*_results_*.json` | per-question sufficient statistics (`_per_question`) and their aggregates |
| `experiments/c6_*`, `experiments/c7_*` | the two censuses: the dossiers the AI labeller read, both labelling passes, the adjudications |
| `experiments/c10_*`, `experiments/blind_audit/`, `blind-audit/` | the reference-query audit: the package the experts received, its key, their answer sheets, the adjudication |
| `experiments/c15_*`, `experiments/alignment-audit/`, `alignment-audit/` | the independent-yardstick audit: the package, its key, the answer sheets |
| `experiments/spider_dev_*` | the two pilot measurements on Spider dev: collisions between questions on the shipped database, and near-miss mutants of reference queries |
| other `experiments/*.json` | panel summaries and every post-hoc analysis |
| `experiments/c4_manifest.json` | SHA-256 of every panel pool and of each checkpoint's weight shards |
| `data/spider_realistic/spider-realistic-matched-original.json` | the Spider-Realistic items with their original Spider dev wording, for the matched control |
| `figures/` | table and figure scripts |
| `supplementary.pdf` | the paper's supplementary material |

Result files are named `<step>_<checkpoint>_<condition>_results_<partition>[_per_question].json`.
The `_per_question` files are the sufficient statistics every reported quantity is computed from;
the others are aggregates. `c4` is the preregistered panel, with generation seeds 101, 202 and 303
and the false-schema negative control; `c5` is the matched original-Spider control; `e0`, `c1`,
`c2`, `c3` and `pilot` are the stages before the final preregistration, whose history the
supplementary material gives; the two `spider_dev_*` files are the pilot measurements that
motivated the intervention.

## Third-party inputs

Executing SQL and rebuilding prompts need the benchmark, its test suites and the official
evaluator. They are distributed by their authors, and the scripts look for them at these paths:

| Input | Source | Path |
| --- | --- | --- |
| Spider-Realistic, 508 questions | Deng et al., [doi:10.5281/zenodo.5205322](https://doi.org/10.5281/zenodo.5205322) | `data/spider_realistic/spider-realistic.json` |
| Spider dev split, 1,034 questions | the same record, or [Spider](https://yale-lily.github.io/spider) | `data/spider/dev.json` |
| distilled test suites | [test-suite-sql-eval](https://github.com/taoyds/test-suite-sql-eval), download link in its README | `data/spider/test_suite_database/<db_id>/` |
| official evaluator, `exec_eval.py` and `parse.py` | the same repository | `data/spider/` |
| `classical_test.pkl` | the same repository | `data/classical/` |

## Checkpoints

| Tag | Checkpoint |
| --- | --- |
| `xiyansql-32b` | [XGenerationLab/XiYanSQL-QwenCoder-32B-2504](https://huggingface.co/XGenerationLab/XiYanSQL-QwenCoder-32B-2504) |
| `omnisql-32b` | [seeklhy/OmniSQL-32B](https://huggingface.co/seeklhy/OmniSQL-32B) |
| `kwai-autosql-32b` | [Kwai-AutoSQL/Kwai-AutoSQL-32B](https://huggingface.co/Kwai-AutoSQL/Kwai-AutoSQL-32B) |
| `kwai-autosql-14b` | [Kwai-AutoSQL/Kwai-AutoSQL-14B](https://huggingface.co/Kwai-AutoSQL/Kwai-AutoSQL-14B) |
| `sqlcoder-70b` | [defog/sqlcoder-70b-alpha](https://huggingface.co/defog/sqlcoder-70b-alpha) |
| `llama3-sqlcoder-8b` | [defog/llama-3-sqlcoder-8b](https://huggingface.co/defog/llama-3-sqlcoder-8b) |

The run scripts read each checkpoint from `$MODEL_ROOT` under the directory names they list.
`experiments/c4_manifest.json` records the SHA-256 of every weight shard used, so a download can
be checked against it. The general-purpose models piloted before the final panel are named in
their `experiments/pilot_*_candidates_meta.json`.

## Reproducing the results

The study runs in four layers, and each layer's output is released, so any layer can be rerun on
its own. Run every command from the repository root.

**Tables and figures** from the result files: see Quick start.

**Analyses** from the per-question sufficient statistics and the label files. Each script below
rewrites the released file it names; all of them run on a CPU, most in seconds.

| Command | Writes |
| --- | --- |
| `python experiments/c3_aggregate.py` | `c3_panel_summary.json` |
| `python experiments/c4_aggregate.py` | `c4_panel_summary.json` |
| `python experiments/c4_recompute.py --alphas 0.05 0.1 0.15 0.2 --out experiments/c4_alpha_curve.json` | alpha curves |
| `python experiments/c4_recompute.py --pareto --out experiments/c4_frontier.json` | risk-coverage frontier |
| `python experiments/c4_recompute.py --per-db --out experiments/c4_cluster_analysis.json` | per-schema and leave-one-schema-out values |
| `python experiments/c4_crossfit_summary.py` | `c4_crossfit_summary.json` |
| `python experiments/c4_exhaustive_splits.py` | `c4_exhaustive_db_splits.json` |
| `python experiments/c4_gap_source.py` | `c4_gap_source_descriptive.json` |
| `python experiments/c5_summarise.py` | candidates-only, gold-free and matched-control summaries |
| `python experiments/c6_classify.py` | `c6_semantic_audit.json` |
| `python experiments/c6_classify.py --cases experiments/c7_repair_cases.json --pass-a experiments/c7_labels_pass_a.json --pass-b experiments/c7_labels_pass_b.json --adjudication experiments/c7_labels_adjudicated.json --carry-over experiments/c6_semantic_audit.json --date 2026-09-06 --out experiments/c7_semantic_audit.json` | `c7_semantic_audit.json` |
| `python experiments/c6_gap_audited.py` | `c6_gap_audited.json` |
| `python experiments/c7_accepted_side.py` | `c7_accepted_side.json` |
| `python experiments/c7_repair_audited.py` | `c7_repair_audited.json` |
| `python experiments/c8_baselines.py --check-crc 5000 --rank-decomposition --same-answer-auroc --grid-sensitivity --verify` | `c8_baselines.json` |
| `python experiments/c8_baselines.py --audited agreed --out experiments/c8_baselines_audited_agreed.json` | the four audited conventions; `narrow`, `unanimous` and `wide` likewise |
| `python experiments/c9_tie_audit.py --enumerate --populations --recompute` | `c9_tie_audit.json`, `c9_tied_decisions.json` |
| `python experiments/c10_blind_audit_analyse.py --responses experiments/blind_audit/RESPONSES_专家1.clean.csv experiments/blind_audit/RESPONSES_专家2.clean.csv --adjudicated experiments/blind_audit/ADJUDICATION_标注.clean.csv` | `c10_blind_audit_result.json` |
| `python experiments/c10_blind_audit_sensitivity.py` | `c10_blind_audit_sensitivity.json` |
| `python experiments/c11_dma_decomposition.py` | `c11_dma_decomposition.json` |
| `python experiments/c12_sample_budget.py` | `c12_sample_budget.json` |
| `python experiments/c13_blind_audit_weighted.py` | `c13_blind_audit_weighted.json` |
| `python experiments/c14_alignment_power.py` | `c14_alignment_power.json` |
| `python experiments/c15_alignment_audit_analyse.py --responses experiments/alignment-audit/RESPONSES_E1.csv --out experiments/c15_alignment_audit_result_E1.json` | the first expert's result; `E2` likewise |
| `python experiments/c16_alignment_secondary.py` to `python experiments/c20_matched_suite_contrast.py` | one file each |
| `python experiments/panel_entry.py kwai-autosql-32b kwai-autosql-14b xiyansql-32b omnisql-32b sqlcoder-70b llama3-sqlcoder-8b --prefix experiments/pilot3 --out experiments/panel_entry_3.json` | the entry decision of the final panel |

In `panel_entry_3.json` the record of `llama3-sqlcoder-8b` states why it was excluded in words:
its pilot produced no parsable output, a case the script's status vocabulary has no entry for.
`c4_cluster_analysis.json` also keeps, marked superseded, an earlier schema bootstrap that the
exhaustive split enumeration replaced.

**Execution** of the candidate pools against both oracles, which needs the third-party inputs.
`e0_analyse.py` turns one pool into the result files of one partition. Every result file records
under `provenance` the pool, the options and the evaluator it was produced with, so the command
behind it can be read off the file. `c6_semantic_cases.py` and `c7_repair_cases.py` extract the
census cases, and `c9_tie_reconstruct.py`, `c10_blind_audit_build.py` and
`c15_alignment_audit_build.py` rebuild the tie reconstruction and the two audit item sheets, the
sheets byte for byte. The two pilot measurements on Spider dev need no candidate pool, only the
benchmark and its test suites: `spider_dev_collision_census.py` and `spider_dev_near_miss_census.py`
each rewrite the file of the same name in under a minute on a CPU.

**Sampling** needs GPUs and vLLM. The paper's pools were drawn with vLLM 0.22.1 in bfloat16 on
H100 80GB cards; tensor parallelism is the number of visible cards:

    MODEL_ROOT=/path/to/checkpoints CUDA_VISIBLE_DEVICES=0,1 \
      bash experiments/prereg3_run.sh xiyansql-32b main 101

## Records

Result files record the SHA-256 of the pool, the evaluator and the script that produced them.
Decompressed, the pools here are byte for byte the recorded ones, and so is the evaluator of the
test-suite repository. The scripts are released in their latest version: options added after the
preregistration default to the preregistered behaviour, and comments and help texts have been
edited, so a script's hash can differ from the recorded one while it computes the same thing.
Checkpoint paths on the machine that ran the study are replaced by the checkpoint directory name.

## Citing this work

    @misc{liu2026certified,
      title  = {Certified Against Which Oracle? Execution Labels Set the
                Reported Risk of Conformal Abstention for Text-to-SQL},
      author = {Liu, Jiamiao and Qiao, Dewen and Zhang, Yu and Chen, Xuetao},
      year   = {2026},
      note   = {Preprint}
    }

## License

The code is under the MIT License (`LICENSE`). The data is under CC BY-SA 4.0 (`LICENSE-DATA`),
because the prompts and pools carry questions and reference queries from Spider, which is
distributed under that license.
