"""Generate every LaTeX table of the paper from the result files. One file per table under figures/.

Tables are written as complete table environments (booktabs) so the writer only \\input{}s them.
Captions carry the standing qualifiers where the table reports AI labels or a census.
"""
import collections
import json
import math
import os
import numpy as np
from paper_plot_style import load, ROOT, FIG_DIR, CHECKPOINTS, CHECKPOINT_LABEL, SCORES, SCORE_LABEL

SEEDS = [101, 202, 303]
LINEAGE = {"kwai-autosql-32b": "Qwen3-32B", "kwai-autosql-14b": "Qwen3-14B", "xiyansql-32b": "Qwen2.5 family", "omnisql-32b": "Qwen2.5-Coder-32B"}
FULLNAME = {"kwai-autosql-32b": "Kwai-AutoSQL-32B", "kwai-autosql-14b": "Kwai-AutoSQL-14B",
            "xiyansql-32b": "XiYanSQL-QwenCoder-32B-2504", "omnisql-32b": "OmniSQL-32B"}
SHORT = {"kwai-autosql-32b": "Kwai-32B", "kwai-autosql-14b": "Kwai-14B", "xiyansql-32b": "XiYan-32B", "omnisql-32b": "Omni-32B"}
NOTE_TIE = "File-order recomputation (\\cref{app:tie})."
NOTE_AI = "Labels were assigned by the two-pass adjudicated AI audit."
NOTE_SHORT = "Labels are AI-assigned."
_NUMBER_WORDS = ("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen "
                 "sixteen seventeen eighteen nineteen twenty").split()


def _words(n):
    """Numbers up to twenty are spelled out in the prose of the tables, as in the text."""
    return _NUMBER_WORDS[n] if 0 <= n < len(_NUMBER_WORDS) else f"{n:,}"


APPENDIX_TABLES = {"TABLE_4_labels.tex", "TABLE_6_gap_ladder.tex", "TABLE_7_sixscores.tex", "TABLE_8_auroc.tex",
                   "TABLE_9_robustness.tex", "TABLE_10_tie.tex", "TABLE_11_blind_audit.tex",
                   "TABLE_12_dma_decomposition.tex"}
def write(name, body):
    if name in APPENDIX_TABLES:
        body = body.replace("\\begin{table}[t]", "\\begin{table}[htbp]")
    path = os.path.join(FIG_DIR, name)
    with open(path, "w") as f:
        f.write(body)
    print("Saved: figures/" + name)


def pts(x, d=2, sign=True):
    v = x * 100
    return (f"{v:+.{d}f}" if sign else f"{v:.{d}f}")


# ---------------- Table 1: panel ----------------
panel = load("experiments/c4_panel_summary.json")
entry = {c["tag"]: c for c in load("experiments/panel_entry_3.json")["candidates"]}
rows = []
for t in CHECKPOINTS:
    m = panel["models"][t]
    top1 = [s["question"]["top1_strong"] for s in m["seeds"]]
    parse = [s["parse_rate"] for s in m["seeds"]]
    trunc = [s["truncation_rate"] for s in m["seeds"]]
    rows.append(f"{FULLNAME[t]} ({SHORT[t]}) & {LINEAGE[t]} & {entry[t]['top1_strong']:.3f} & {min(top1):.3f}--{max(top1):.3f} & {min(parse):.4f} & {max(trunc):.4f} \\\\")
excl = [c for c in load("experiments/panel_entry_3.json")["candidates"] if c["status"] != "ENTER"]
t1 = r"""\begin{table}[t]
\centering
\caption{The checkpoint panel. Entry was decided by a frozen rule on a disjoint 200-question pilot of Spider dev (parse rate at least 0.98, truncation rate at most 0.01, top-1 accuracy under the multi-instance suite oracle at least 0.75). Main pools are 508 Spider-Realistic questions with 50 samples each at temperature 1.0 and top-$p$ 0.95, three generation seeds per checkpoint; main-pool top-1 is the range over seeds, parse rate the minimum over seeds and truncation rate the maximum. The short names in parentheses are used in the other tables and figures. The panel spans two Qwen lineages, Qwen3 and Qwen2.5. SQLCoder-70B-alpha (0.67 on the pilot) and llama-3-sqlcoder-8b (no parseable output) were excluded.}
\label{tab:panel}
\small
\setlength{\tabcolsep}{4pt}
\begin{tabular}{p{0.34\linewidth}lcccc}
\toprule
Checkpoint & Base model & Pilot top-1 & Main-pool top-1 & Parse rate & Truncation \\
\midrule
""" + "\n".join(rows) + r"""
\bottomrule
\end{tabular}
\end{table}
"""
write("TABLE_1_panel.tex", t1)

# ---------------- Table 2: preregistered main result ----------------
rows = []
for t in CHECKPOINTS:
    m = panel["models"][t]
    for split in ("question", "database"):
        seeds = [s[split] for s in m["seeds"]]
        A_fit = np.mean([s["A_risk_fit"] for s in seeds]); A_str = np.mean([s["A_risk_strong"] for s in seeds])
        D_str = np.mean([s["D_risk_strong"] for s in seeds]); gap = m[split]["gap_mean"]; rep = m[split]["repair_mean"]
        ans = m[split]["answer_rate_change_mean"]
        verdict = ("pass" if m[split]["repair_pass"] else "fail")
        if m[split]["repair_pass"] and m[split].get("repair_robust"): verdict = "pass (robust)"
        name = SHORT[t] if split == "question" else ""
        rows.append(f"{name} & {split} & {A_fit:.4f} & {A_str:.4f} & {pts(gap)} & {D_str:.4f} & {pts(rep)} & {pts(ans, 1)} & {'yes' if m[split]['gap_positive'] else 'no'} & {verdict} \\\\")
t2 = r"""\begin{table}[t]
\centering
\caption{Preregistered main result at nominal risk $\alpha=0.10$, three-seed means. The current-practice cell A is calibrated on labels from the shipped database and evaluated under the multi-instance suite oracle; GAP is its suite-oracle risk minus the risk it reports on its own labels; D minus A is the suite-oracle risk of the fully multi-instance cell D minus that of cell A, negative meaning D carries less. Answer-rate change is D minus A. The last two columns are the frozen-rule verdicts (GAP positive: every seed above zero and mean at least one point; D minus A pass: every seed below zero and mean at most $-3$ points; robust: every seed at most $-3$ points). All risks are under the suite oracle unless marked reported.}
\label{tab:main}
\footnotesize
\setlength{\tabcolsep}{3.5pt}
\begin{tabular}{llcccccccc}
\toprule
Checkpoint & Split & A reported & A suite & GAP (pts) & D suite & $\DmA$ (pts) & $\Delta$answer (pts) & GAP$>0$ & $\DmA$ rule \\
\midrule
""" + "\n".join(rows) + r"""
\bottomrule
\end{tabular}
\end{table}
"""
write("TABLE_2_main.tex", t2)

# ---------------- Table 3: agreement ----------------
c6 = load("experiments/c6_semantic_audit.json"); c7 = load("experiments/c7_semantic_audit.json")
carried = {c["case_id"] for c in load("experiments/c7_repair_cases.json")["cases"] if c.get("carried_over_from")}


def agreement(cases):
    a = [c["label_a"] for c in cases]; b = [c["label_b"] for c in cases]
    def kappa(x, y):
        n = len(x); obs = sum(p == q for p, q in zip(x, y)) / n
        cx, cy = collections.Counter(x), collections.Counter(y)
        exp = sum(cx[k] * cy[k] for k in set(cx) | set(cy)) / (n * n)
        return obs, (obs - exp) / (1 - exp)
    o5, k5 = kappa(a, b)
    o2, k2 = kappa([x == "semantic_error" for x in a], [x == "semantic_error" for x in b])
    return o5, k5, o2, k2


ag6 = agreement(c6["cases"]); ag7 = agreement(c7["cases"]); ag7new = agreement([c for c in c7["cases"] if c["case_id"] not in carried])
n7new = sum(1 for c in c7["cases"] if c["case_id"] not in carried)
p6, p7 = c6["population"], c7["population"]
l6, l7 = c6["labelling"], c7["labelling"]
t3 = r"""\begin{table}[t]
\centering
\caption{The two censuses and the agreement of the two independent labelling passes, computed from the case-level labels. """ + NOTE_AI + r""" Binary agreement collapses the five labels to semantic error versus not. In the four agreement and $\kappa$ rows, the full-census value is over all 742 cases and the parenthesised value is over the """ + f"{n7new}" + r""" cases labelled for the first time in that census, the other 240 being carried over from the disagreement census with their labels.}
\label{tab:agreement}
\small
\begin{tabular}{p{0.36\linewidth}>{\raggedright\arraybackslash}p{0.27\linewidth}>{\raggedright\arraybackslash}p{0.27\linewidth}}
\toprule
 & Disagreement census & Full census \\
\midrule
Population & weak-accepted, suite-rejected A-cell answers & any A- or D-cell answer the suite rejects \\
Answers & """ + f"{p6['weak_correct_strong_wrong_answers']:,}" + " & " + f"{p7['wrong_answers']:,}" + r""" \\
Distinct cases & """ + f"{p6['distinct_cases']}" + " & " + f"{p7['distinct_cases']}" + r""" \\
Questions & """ + f"{p6['distinct_questions']}" + " & " + f"{p7['distinct_questions']}" + r""" \\
Five-label agreement & """ + f"{ag6[0]*100:.1f}\\%" + " & " + f"{ag7[0]*100:.1f}\\% ({ag7new[0]*100:.1f}\\%)" + r""" \\
Binary agreement & """ + f"{ag6[2]*100:.1f}\\%" + " & " + f"{ag7[2]*100:.1f}\\% ({ag7new[2]*100:.1f}\\%)" + r""" \\
Cohen's $\kappa$, binary & """ + f"{ag6[3]:.3f}" + " & " + f"{ag7[3]:.3f} ({ag7new[3]:.3f})" + r""" \\
Cohen's $\kappa$, five-label & """ + f"{ag6[1]:.3f}" + " & " + f"{ag7[1]:.3f} ({ag7new[1]:.3f})" + r""" \\
Cases with a borderline flag in either pass & """ + f"{c6['headline']['borderline_in_either_pass']} ({c6['headline']['borderline_in_either_pass']/p6['distinct_cases']*100:.1f}\\%)" + " & " + f"{c7['headline']['borderline_in_either_pass']} ({c7['headline']['borderline_in_either_pass']/p7['distinct_cases']*100:.1f}\\%)" + r""" \\
Adjudicated disagreements & """ + f"{l6['adjudicated']}" + " & " + f"{l7['adjudicated']}" + r""" \\
Unresolved after adjudication & """ + f"{l6['unresolved']}" + " & " + f"{l7['unresolved']}" + r""" \\
\bottomrule
\end{tabular}
\end{table}
"""
write("TABLE_3_agreement.tex", t3)

# ---------------- Table 4: label distributions ----------------
LABEL_TEXT = {"semantic_error": "semantic error", "gold_defect": "suspected reference-query defect", "underspecified": "underspecified question",
              "instance_defect": "synthetic-instance defect", "comparator_artifact": "comparator artefact"}
rows = []
for lab in ["semantic_error", "gold_defect", "underspecified", "instance_defect", "comparator_artifact"]:
    c6c = c6["label_distribution_cases"].get(lab, 0); c6a = c6["label_distribution_answers"].get(lab, 0)
    c7c = c7["label_distribution_cases"].get(lab, 0); c7a = c7["label_distribution_answers"].get(lab, 0)
    rows.append(f"{LABEL_TEXT[lab]} & {c6c} ({c6c/240*100:.1f}\\%) & {c6a} ({c6a/521*100:.1f}\\%) & {c7c} ({c7c/742*100:.1f}\\%) & {c7a:,} ({c7a/2779*100:.1f}\\%) \\\\")
et6 = c6["error_type_distribution"]; et7 = c7["error_type_distribution"]
ET = {"wrong_filter": "wrong filter", "wrong_grouping": "wrong grouping", "wrong_join": "wrong join", "wrong_aggregate": "wrong aggregate",
      "wrong_set_operation": "wrong set operation", "wrong_order_or_limit": "wrong order or limit", "wrong_projection": "wrong projection"}
erows = [f"\\quad {ET[k]} & {et6.get(k, 0)} & & {et7.get(k, 0)} & \\\\" for k in ET]
t4 = r"""\begin{table}[t]
\centering
\caption{Labels assigned to the two censuses, by distinct case and by answer occurrence. """ + NOTE_SHORT + r""" The lower block gives the error type of the cases labelled semantic error.}
\label{tab:labels}
\small
\begin{tabular}{lcccc}
\toprule
 & \multicolumn{2}{c}{Disagreement census} & \multicolumn{2}{c}{Full census} \\
\cmidrule(lr){2-3}\cmidrule(lr){4-5}
Label & cases (240) & answers (521) & cases (742) & answers (2,779) \\
\midrule
""" + "\n".join(rows) + r"""
\midrule
Error type of semantic-error cases & & & & \\
""" + "\n".join(erows) + r"""
\bottomrule
\end{tabular}
\end{table}
"""
write("TABLE_4_labels.tex", t4)

# ---------------- Table 5: D-minus-A ladder ----------------
rep = load("experiments/c7_repair_audited.json")["summary"]
CONV = ["preregistered", "wide", "narrow", "agreed", "unanimous"]
rows = []
for t in CHECKPOINTS:
    for split in ("question", "database"):
        r = rep[f"{t}|{split}"]
        name = SHORT[t] if split == "question" else ""
        vals = " & ".join(pts(r[c]) for c in CONV)
        neg = " & ".join(f"{r[c + '_negative_splits']:.3f}" for c in CONV)
        rows.append(f"{name} & {split} & {vals} & {neg} \\\\")
counts = {}
for c in ["wide", "narrow", "agreed", "unanimous"]:
    d = load(f"experiments/c8_baselines_audited_{c}.json")["summary"]
    n = 0
    for key, v in d.items():
        for sc in SCORES:
            if v.get(f"{sc}|REPAIR", 0) <= -0.03: n += 1
    counts[c] = n
t5 = r"""\begin{table}[t]
\centering
\caption{The D minus A contrast (points, negative means cell D carries less risk under the named yardstick) at $\alpha=0.10$ under the preregistered suite labels and under four nested relabelling conventions of the full census that exculpate rejected answers labelled as not semantic errors: wide (semantic error and synthetic-instance defect count as wrong), narrow (only semantic error counts as wrong), agreed (narrow, restricted to cases both passes agreed on), unanimous (agreed and neither pass flagged the case as borderline). The suite oracle stays the intervention; only the yardstick changes. The right block is the three-seed mean share of the 200 splits in which the contrast is negative, a resplit-stability statistic. Over the six scores of Section~\ref{sec:sixscores}, the number of the 48 score-by-checkpoint-by-split cells that clear the preregistered three-point bar is """ + f"{counts['wide']}, {counts['narrow']}, {counts['agreed']} and {counts['unanimous']}" + r""" under the four conventions. """ + NOTE_SHORT + " " + NOTE_TIE + r"""}
\label{tab:repair_ladder}
\footnotesize
\setlength{\tabcolsep}{3pt}
\begin{tabular}{llccccc ccccc}
\toprule
 & & \multicolumn{5}{c}{$\DmA$ (points)} & \multicolumn{5}{c}{share of splits negative} \\
\cmidrule(lr){3-7}\cmidrule(lr){8-12}
Checkpoint & Split & prereg. & wide & narrow & agreed & unanim. & prereg. & wide & narrow & agreed & unanim. \\
\midrule
""" + "\n".join(rows) + r"""
\bottomrule
\end{tabular}
\end{table}
"""
write("TABLE_5_repair_ladder.tex", t5)

# ---------------- Table 6: GAP ladder + stress ----------------
g6 = load("experiments/c6_gap_audited.json")["summary"]; g7 = load("experiments/c7_gap_audited_full.json")["summary"]; gs = load("experiments/c7_gap_stress.json")["summary"]
rows = []
for t in CHECKPOINTS:
    for split in ("question", "database"):
        name = SHORT[t] if split == "question" else ""
        k = f"{t}|{split}"
        rows.append(f"{name} & {split} & {pts(g7[k]['preregistered'])} & {pts(g6[k]['narrow'])} & {pts(g7[k]['narrow'])} & {pts(g7[k]['unanimous'])} & {pts(gs[k]['narrow'])} \\\\")
t6 = r"""\begin{table}[t]
\centering
\caption{GAP (points) at $\alpha=0.10$: the risk of the current-practice cell under the named yardstick minus the risk it reports on its own labels; only the preregistered column uses the unmodified suite oracle as the yardstick. Columns: under the preregistered suite labels, after relabelling the rejected side with the disagreement census (narrow convention), after relabelling it with the full census (narrow and unanimous conventions), and under the reverse stress test that additionally counts as wrong the 259 accepted answers that fall on questions with a suspected defective reference query. The stress test is an extreme assumption, not an estimate; the 1,580 distinct accepted outputs were never examined. """ + NOTE_SHORT + " " + NOTE_TIE + r"""}
\label{tab:gap_ladder}
\footnotesize
\setlength{\tabcolsep}{4pt}
\begin{tabular}{llccccc}
\toprule
Checkpoint & Split & preregistered & disagreement census & full census, narrow & full census, unanimous & reverse stress \\
\midrule
""" + "\n".join(rows) + r"""
\bottomrule
\end{tabular}
\end{table}
"""
write("TABLE_6_gap_ladder.tex", t6)

# ---------------- Table 7: six scores ----------------
S = load("experiments/c8_baselines.json")["summary"]
heads = " & ".join(SHORT[t] for t in CHECKPOINTS)
blocks = []
for metric, title in (("GAP", "GAP (points)"), ("REPAIR", r"$\DmA$ (points)")):
    rows = []
    for sc in SCORES:
        cells = [pts(S[f"{t}|{split}"][f"{sc}|{metric}"], 1) for split in ("question", "database") for t in CHECKPOINTS]
        rows.append(f"{SCORE_LABEL[sc]} & " + " & ".join(cells) + " \\\\")
    blocks.append(r"""\multicolumn{9}{l}{\emph{""" + title + r"""}} \\
""" + "\n".join(rows))
t7 = r"""\begin{table}[t]
\centering
\caption{GAP and D minus A (points) for six confidence scores under one certificate, one answer rule, the same pools and the same 200 splits, at $\alpha=0.10$ under the preregistered suite labels. The top-class-mass row is the pipeline of the main text; the four consistency scores share the execution-equivalence relation under test; the two likelihood scores never read any oracle. All 48 GAP cells are positive and all 48 D minus A cells are negative. """ + NOTE_TIE + r"""}
\label{tab:sixscores}
\small
\setlength{\tabcolsep}{2.5pt}
\begin{tabular}{l cccc cccc}
\toprule
 & \multicolumn{4}{c}{question splits} & \multicolumn{4}{c}{database splits} \\
\cmidrule(lr){2-5}\cmidrule(lr){6-9}
Score & """ + heads + " & " + heads + r""" \\
\midrule
""" + ("\n\\midrule\n".join(blocks)) + r"""
\bottomrule
\end{tabular}
\end{table}
"""
write("TABLE_7_sixscores.tex", t7)

# ---------------- Table 8: AUROC ----------------
same = load("experiments/c8_baselines.json")["same_answer_auroc"]
def auroc_block(tags):
    rows = []
    for sc in SCORES:
        cells = []
        for t in tags:
            r = S[f"{t}|question"]
            cells.append(f"{r[f'{sc}|auroc_weak']:.3f} / {r[f'{sc}|auroc_strong']:.3f}")
            cells.append(f"{r[f'{sc}|auroc_weak_D']:.3f} / {r[f'{sc}|auroc_strong_D']:.3f}")
            cells.append(f"{r[f'{sc}|auroc_drop']*100:+.1f} / {r[f'{sc}|auroc_drop_D']*100:+.1f}")
            sm = same[t]["scores"][sc]
            cells.append(f"{sm['drop_A']*100:+.1f} / {sm['drop_D']*100:+.1f}")
        rows.append(f"{SCORE_LABEL[sc]} & " + " & ".join(cells) + " \\\\")
    head = " & ".join(f"\\multicolumn{{4}}{{c}}{{{SHORT[t]}}}" for t in tags)
    return r""" & """ + head + r""" \\
\cmidrule(lr){2-5}\cmidrule(lr){6-9}
Score & A w/s & D w/s & drop A/D & sameSQL A/D & A w/s & D w/s & drop A/D & sameSQL A/D \\
\midrule
""" + "\n".join(rows)
def auroc_rows():
    rows = []
    for t in CHECKPOINTS:
        r = S[f"{t}|question"]; first = True
        for sc in SCORES:
            sm = same[t]["scores"][sc]
            cells = [f"{r[f'{sc}|auroc_weak']:.3f}", f"{r[f'{sc}|auroc_strong']:.3f}",
                     f"{r[f'{sc}|auroc_weak_D']:.3f}", f"{r[f'{sc}|auroc_strong_D']:.3f}",
                     f"{r[f'{sc}|auroc_drop']*100:+.1f}", f"{r[f'{sc}|auroc_drop_D']*100:+.1f}",
                     f"{sm['drop_A']*100:+.1f}", f"{sm['drop_D']*100:+.1f}"]
            rows.append((SHORT[t] if first else "") + f" & {SCORE_LABEL[sc]} & " + " & ".join(cells) + " \\\\")
            first = False
        rows.append("\\addlinespace")
    return "\n".join(rows[:-1])
t8 = r"""\begin{table}[t]
\centering
\caption{AUROC of each score for predicting the correctness of the returned answer, computed on all 508 questions of each seed and averaged over the three seeds; the value does not depend on the split scheme. The score is built once on the original-database partition (cell A) and once on the suite partition (cell D), and each is evaluated under weak labels (correctness on the shipped database) and under suite labels. The drop is the weak-minus-suite change in AUROC in points for each cell; the same-SQL drop restricts the computation to the questions on which both cells return the same SQL, 477 to 508 per seed. The two likelihood scores use the same oracle-independent formula in both cells.}
\label{tab:auroc}
\footnotesize
\setlength{\tabcolsep}{4.5pt}
\begin{tabular}{ll cc cc cc cc}
\toprule
 & & \multicolumn{2}{c}{Built on A} & \multicolumn{2}{c}{Built on D} & \multicolumn{2}{c}{Drop} & \multicolumn{2}{c}{Same-SQL drop} \\
\cmidrule(lr){3-4}\cmidrule(lr){5-6}\cmidrule(lr){7-8}\cmidrule(lr){9-10}
Checkpoint & Score & weak & suite & weak & suite & A & D & A & D \\
\midrule
""" + auroc_rows() + r"""
\bottomrule
\end{tabular}
\end{table}
"""
write("TABLE_8_auroc.tex", t8)

# ---------------- Table 9: robustness ----------------
cf = load("experiments/c4_crossfit_summary.json")["models"]; gf = load("experiments/c4_gold_free_summary.json")["models"]
co = load("experiments/c4_candidates_only_summary.json")["models"]
ex = load("experiments/c4_exhaustive_db_splits.json")["models"]; c5 = load("experiments/c5_matched_control_summary.json")
lodo = load("experiments/c4_cluster_analysis.json")["leave_one_database_out"]
def lodo_range(t, metric):
    vals = {k.split("drop=")[1]: v[metric] for k, v in lodo.items() if k.startswith(t + "|") and "<none>" not in k}
    lo = min(vals.items(), key=lambda kv: kv[1]); hi = max(vals.items(), key=lambda kv: kv[1])
    return lo, hi
def tex(db):
    return db.replace("_", "\\_")
def row(label, f):
    return label + " & " + " & ".join(f(t) for t in CHECKPOINTS) + " \\\\"
lines = [
    row("instance cross-fit GAP / $\\DmA$ (24 runs)", lambda t: f"{pts(np.mean([r['GAP'] for r in cf[t]['runs']]))} / {pts(np.mean([r['REPAIR'] for r in cf[t]['runs']]))}"),
    row("instance cross-fit, held-out D risk (range)", lambda t: f"{min(r['D_risk_strong'] for r in cf[t]['runs']):.3f}--{max(r['D_risk_strong'] for r in cf[t]['runs']):.3f}"),
    row("candidates-only partition GAP / $\\DmA$", lambda t: f"{pts(co[t]['GAP_candidates_only'])} / {pts(co[t]['REPAIR_candidates_only'])}"),
    row("gold-free construction GAP / $\\DmA$", lambda t: f"{pts(gf[t]['GAP_gold_free'])} / {pts(gf[t]['REPAIR_gold_free'])}"),
    row("exhaustive database splits, mean GAP / $\\DmA$", lambda t: f"{pts(ex[t + '|tie=first']['GAP_mean'])} / {pts(ex[t + '|tie=first']['REPAIR_mean'])}"),
    row("exhaustive splits, share with GAP $>0$ (range over seeds)", lambda t: f"{ex[t + '|tie=first']['GAP_positive_fraction_range'][0]*100:.1f}--{ex[t + '|tie=first']['GAP_positive_fraction_range'][1]*100:.1f}\\%"),
    row("exhaustive splits, share with $\\DmA$ $<0$ (range over seeds)", lambda t: f"{ex[t + '|tie=first']['REPAIR_negative_fraction_range'][0]*100:.1f}--{ex[t + '|tie=first']['REPAIR_negative_fraction_range'][1]*100:.1f}\\%"),
    row("leave-one-out GAP, min / max", lambda t: f"{pts(lodo_range(t, 'GAP')[0][1])} / {pts(lodo_range(t, 'GAP')[1][1])}"),
    row("leave-one-out GAP, schema whose removal gives the min", lambda t: tex(lodo_range(t, 'GAP')[0][0])),
    row("leave-one-out $\\DmA$, weakest (schema removed)", lambda t: f"{pts(lodo_range(t, 'REPAIR')[1][1])} ({tex(lodo_range(t, 'REPAIR')[1][0])})"),
]
mc = {r["split"]: r for r in c5 if r["set"].startswith("matched")}
t9 = r"""\begin{table}[t]
\centering
\caption{Post-hoc robustness checks of the preregistered measurement (points, three-seed means, $\alpha=0.10$, question splits unless stated). Instance cross-fit: classes and calibration labels from one half of each schema's suite instances plus the shipped database, correctness judged on the other half plus the shipped database, both directions (24 runs); the held-out D-cell risk row is its range. Candidates-only: partition built from the sampled candidates alone, the reference query used only to label a class afterwards. Gold-free: candidates-only with the row-order convention taken from the compared pair. Exhaustive database splits: mean over all 92,378 schema-disjoint 9/10 splits, with the range over seeds of the share of splits carrying the reported sign given in the two rows below. Leave-one-database-out: the preregistered question-split analysis with one schema removed. The matched original-Spider control (Kwai-14B, 508 one-to-one paired original questions) gives GAP """ + f"{pts(mc['question']['GAP'])} / {pts(mc['database']['GAP'])}" + r""" and D minus A """ + f"{pts(mc['question']['REPAIR'])} / {pts(mc['database']['REPAIR'])}" + r""" under question / database splits.}
\label{tab:robustness}
\scriptsize
\setlength{\tabcolsep}{3pt}
\begin{tabular}{p{0.36\linewidth}cccc}
\toprule
Check & """ + " & ".join(SHORT[t] for t in CHECKPOINTS) + r""" \\
\midrule
""" + "\n".join(lines) + r"""
\bottomrule
\end{tabular}
\end{table}
"""
write("TABLE_9_robustness.tex", t9)

# ---------------- Table 10: tie audit ----------------
tie = load("experiments/c9_tie_audit.json")
# Top-class mass: the preregistered labels and every column of both ladders, which the recompute,
# the six-score run and the GAP-ladder run cover between them; the six-score run and the ladder run
# hold disjoint cells, so their counts add. The other five scores: the six-score run alone.
tcm = [tie["impact_bounds"], tie["six_scores"]["impact_bounds_top_class_mass"],
       tie["gap_ladder"]["impact_bounds"]]
tcm_cells = tcm[1:]
five = tie["six_scores"]["impact_bounds_other_scores"]
worst = lambda key: max(b[key] for b in tcm)
count = lambda key: sum(b[key] for b in tcm_cells)
t10 = r"""\begin{table}[t]
\centering
\caption{The tie-rule audit. The frozen analyser breaks a top-class tie by the largest integer union-find key; the per-question files sort by the stringified key, so every recomputation from them takes the first-listed class. Impact bounds are over the GAP and D minus A cells of top-class mass under the preregistered labels and in every column of both audit ladders, and of the other five scores of the six-score comparison under the preregistered labels and the four census conventions, after recomputing under the frozen rule and bracketing the never-labelled answers in both directions.}
\label{tab:tie}
\small
\begin{tabular}{lc}
\toprule
Top-class decisions examined & """ + f"{tie['tied']['decisions_examined']:,}" + r""" \\
Tied decisions & """ + f"{tie['tied']['tied']}" + r""" \\
Tied decisions whose representative differs under the frozen rule & """ + f"{tie['reconstruction']['representative_differs']}" + r""" \\
Tied decisions whose correctness label differs & """ + f"{tie['reconstruction']['correctness_label_differs']}" + r""" \\
Disagreement census: archived / frozen answers & """ + f"{tie['populations']['c6']['stored_answers']} / {tie['populations']['c6']['frozen_answers']}" + r""" \\
Full census: archived / frozen answers (cases) & """ + f"{tie['populations']['c7']['stored_answers']:,} / {tie['populations']['c7']['frozen_answers']:,} ({tie['populations']['c7']['cases_labelled']} / {tie['populations']['c7']['cases_under_frozen']})" + r""" \\
Largest change of a GAP or D minus A, top-class mass / other five scores (points) & """ + f"{worst('largest_change_points'):.4f} / {five['largest_change_points']:.4f}" + r""" \\
Largest bracket width from never-labelled answers, top-class mass / other five scores (points) & """ + f"{worst('largest_bracket_width_points'):.4f} / {five['largest_bracket_width_points']:.4f}" + r""" \\
Sign changes, top-class mass / other five scores & """ + f"{count('sign_changes')} / {five['sign_changes']}" + r""" \\
Cells crossing the three-point line, top-class mass / other five scores & """ + f"{count('crossings_of_the_three_point_line')} / {five['crossings_of_the_three_point_line']}" + r""" \\
\bottomrule
\end{tabular}
\end{table}
"""
write("TABLE_10_tie.tex", t10)

# ---------------- Table 11: blind audit design ----------------
key = load("experiments/c10_blind_audit_key.json")
bench = key["strata_sizes_in_the_benchmark"]; samp = key["sampled"]
t11 = r"""\begin{table}[t]
\centering
\caption{Design of the preregistered blinded human audit of the reference queries. Experts see the question, the schema and the reference query only, must execute the query, and return one of four verdicts per item. The decision rule was fixed and committed before any human label existed. No human label exists at the time of writing.}
\label{tab:blind}
\small
\begin{tabular}{p{0.30\linewidth}p{0.60\linewidth}}
\toprule
Stratum & Items \\
\midrule
flagged (AI audit assigned at least one suspected reference defect) & all """ + f"{samp['flagged']}" + r""" questions \\
examined but not flagged (a rejected answer was labelled, no reference defect assigned) & """ + f"{samp['examined']} of {bench['examined']}" + r""", random \\
never examined (no answer of these questions was ever rejected by the suite) & """ + f"{samp['unexamined']} of {bench['unexamined']}" + r""", random \\
\midrule
Verdicts & reference correct; reference defective; question underspecified; cannot judge \\
Support & $D(\text{flagged}) - D(\text{examined}) \ge 25$ points and $D(\text{flagged}) \ge 40\%$ \\
Refute & $D(\text{flagged}) - D(\text{examined}) < 10$ points; the suspected-defect interpretation is withdrawn \\
Partial support & otherwise \\
Secondary & background defect rate on the never-examined stratum with an exact binomial interval; human-versus-AI agreement and $\kappa$; per-strength confirmation rates; borderline sensitivity \\
\bottomrule
\end{tabular}
\end{table}
"""
write("TABLE_11_blind_audit.tex", t11)

# When the expert labels have come back, Table 11 reports the result instead of the design.
_bl = "experiments/c10_blind_audit_result.json"
# ROOT-relative, like load(): a cwd-relative test here silently reverts the table to its
# pre-results design version whenever the script is run from anywhere but the repository root.
if os.path.exists(os.path.join(ROOT, _bl)):
    R = load(_bl)
    _name = {"flagged": "flagged", "examined": "examined, not flagged",
             "unexamined": "never examined"}

    def _cp(k, n):
        """The stored interval is rounded to four decimals; displaying it to one decimal
        would round twice and move an endpoint. Recompute from the counts instead, by the
        same definition the analysis uses."""
        if n == 0:
            return 0.0, 1.0
        def cdf(p, upto):
            return sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(upto + 1))
        def solve(target, upto):
            lo, hi = 0.0, 1.0
            for _ in range(200):
                mid = (lo + hi) / 2
                if cdf(mid, upto) > target:
                    lo = mid
                else:
                    hi = mid
            return (lo + hi) / 2
        return (0.0 if k == 0 else solve(0.975, k - 1),
                1.0 if k == n else solve(0.025, k))

    _rows = []
    for _s in ("flagged", "examined", "unexamined"):
        r = R["rates"][_s]
        lo, hi = _cp(r["defective"], r["n"])
        _rows.append(f"{_name[_s]} & {r['n']} & {r['defective']} & {100 * r['D']:.1f} & "
                     f"[{100 * lo:.1f}, {100 * hi:.1f}] & {r['underspecified']} \\\\")
    d, db = R["decision"], R["decision_excluding_borderline"]
    hv, bg = R["human_vs_ai"], R["background_gold_defect_rate"]
    _lines = [
        f"Preregistered verdict & \\multicolumn{{5}}{{p{{0.70\\linewidth}}}}{{{d['verdict'].replace('_', ' ')}, "
        f"margin {100 * d['margin']:.1f} points}} \\\\",
        f"Excluding borderline & \\multicolumn{{5}}{{p{{0.70\\linewidth}}}}{{{db['verdict'].replace('_', ' ')}, "
        f"margin {100 * db['margin']:.1f} points on the first expert's marks, "
        f"60.2 if either expert's mark excludes}} \\\\",
        f"Never-examined stratum & \\multicolumn{{5}}{{p{{0.70\\linewidth}}}}{{{100 * bg['estimate']:.1f}\\% "
        f"of its 40 sampled questions, 95\\% CI "
        f"{100 * _cp(R['rates']['unexamined']['defective'], R['rates']['unexamined']['n'])[0]:.1f} to "
        f"{100 * _cp(R['rates']['unexamined']['defective'], R['rates']['unexamined']['n'])[1]:.1f}}} \\\\",
        f"Human versus AI flag & \\multicolumn{{5}}{{p{{0.70\\linewidth}}}}{{agreement {100 * hv['agreement']:.1f}\\%, "
        f"$\\kappa = {hv['kappa']:.3f}$, over all 153 items}} \\\\"]
    if "expert_agreement" in R:
        e = R["expert_agreement"]
        _nfour = len(e["disagreements"])
        _nbin = round((1 - e["binary_agreement"]) * e["n"])
        _lines.append(
            f"Between experts & \\multicolumn{{5}}{{p{{0.70\\linewidth}}}}{{binary agreement "
            f"{100 * e['binary_agreement']:.1f}\\%, $\\kappa = {e['binary_kappa']:.3f}$; "
            f"{_words(_nfour)} four-way verdict disagreements adjudicated, {_words(_nbin)} of them binary}} \\\\")
    t11 = (r"""\begin{table}[t]
\centering
\caption{Result of the preregistered blinded human audit of the reference queries. Experts saw the question, the schema and the reference query only, executed the query, and returned one of four verdicts per item. $D$ is the share judged a defective reference query, with an exact binomial interval. The flagged stratum is a complete enumeration of the 73 flagged questions, so its interval describes uncertainty about a wider population of questions the flag could select rather than sampling error inside this set, while the two control intervals are sampling intervals for their own finite strata. The decision rule and its thresholds were committed before any human label existed.}
\label{tab:blind}
\small
\begin{tabular}{lrrrrr}
\toprule
Stratum & Items & Defective & $D$ (\%) & 95\% CI & Underspecified \\
\midrule
""" + "\n".join(_rows) + r"""
\midrule
""" + "\n".join(_lines) + r"""
\bottomrule
\end{tabular}
\end{table}
""")
    write("TABLE_11_blind_audit.tex", t11)

# ---------------- Table 12: where D minus A comes from ----------------
_dd = load("experiments/c11_dma_decomposition.json")["three_seed_means"]
_drows = []
for _c in CHECKPOINTS:
    for _j, _how in enumerate(("question", "database")):
        _m = _dd[f"{_c}|{_how}"]
        _name = SHORT[_c] if _j == 0 else ""
        _drows.append(f"{_name} & {_how} & {pts(_m['dma'], 3)} & {pts(_m['contrib_both_changed_sql'], 3)} & "
                      f"{pts(_m['contrib_only_d'], 3)} & {pts(_m['contrib_only_a'], 3)} & "
                      f"{pts(_m['share_both_same_sql'], 1, False)} \\\\")
    if _c != CHECKPOINTS[-1]:
        _drows.append(r"\addlinespace")

t12 = (r"""\begin{table}[t]
\centering
\caption{Where the D minus A contrast comes from, at $\alpha=0.10$, three-seed means over 200 splits. Both cells are judged by the same oracle, so a held-out question both cells answer with the same SQL contributes exactly zero and the three remaining events sum to the contrast; the identity is asserted on every split. The last column is the share of held-out questions on which both cells answer and the SQL is unchanged, which is not the 97.1 percent of Section~\ref{sec:populations}: that share counts the representative of every question, answered or not. Post hoc. """ + NOTE_TIE + r"""}
\label{tab:dma_decomposition}
\footnotesize
\setlength{\tabcolsep}{5pt}
\begin{tabular}{llccccc}
\toprule
 & & & \multicolumn{3}{c}{contribution (pts)} & both answer, \\
\cmidrule(lr){4-6}
Checkpoint & Split & $\DmA$ (pts) & changed SQL & only D & only A & same SQL (\%) \\
\midrule
""" + "\n".join(_drows) + r"""
\bottomrule
\end{tabular}
\end{table}
""")
write("TABLE_12_dma_decomposition.tex", t12)

# ---------------- Table 13: the independent-yardstick audit ----------------
_al = load("experiments/c17_alignment_adjudication_bound.json")
_alrows = []
_ALNAME = {"agreed_only": "both experts agree", "E1": "first expert alone", "E2": "second expert alone"}
for _c in ("xiyansql-32b", "kwai-autosql-32b"):
    _b = _al["checkpoints"][_c]
    for _j, _k in enumerate(("agreed_only", "E1", "E2")):
        _r = _b[_k]
        _alrows.append(f"{SHORT[_c] if _j == 0 else ''} & {_ALNAME[_k]} & {_r['n_correct']}/{_r['n_wrong']} & "
                       f"{_r['auroc_a']:.3f} & {_r['auroc_d']:.3f} & {pts(_r['delta'])} & {_r['p']:.3f} \\\\")
    _lo, _hi = _b["min"], _b["max"]
    _alrows.append(f" & searched assignments & & & & {pts(_lo['delta'])} to {pts(_hi['delta'])} & "
                   f"{min(_lo['p'], _hi['p']):.3f} to {max(_lo['p'], _hi['p']):.3f} \\\\")
    if _c != "kwai-autosql-32b":
        _alrows.append(r"\addlinespace")

t13 = (r"""\begin{table}[t]
\centering
\caption{The preregistered independent-yardstick audit. Two SQL experts, blind to the cell, the score and every oracle label, judged whether each returned query answers its question, on the """ + f"{_al['items']:,}" + r""" distinct answers of two checkpoints; they were required to execute rather than read. AUROC is for predicting a correct answer, for the score built on the original-database partition and for the same score built on the suite partition, against the same expert labels on the same questions. The contrast is paired and tested by DeLong. The experts agree on """ + f"{_al['agreed']}" + r""" of the items; the last row of each block is the widest range a hill-climbing search over assignments of the remaining """ + f"{_al['disagreed']}" + r""" attained; significance does not change anywhere inside it. The decision rule was fixed before any label existed and returns MIXED.}
\label{tab:alignment_audit}
\footnotesize
\setlength{\tabcolsep}{5pt}
\begin{tabular}{llccccc}
\toprule
Checkpoint & Labels & correct/wrong & AUROC on A & AUROC on D & $\Delta$ (pts) & $p$ \\
\midrule
""" + "\n".join(_alrows) + r"""
\bottomrule
\end{tabular}
\end{table}
""")
write("TABLE_13_alignment_audit.tex", t13)

# ---------------- Table 14: the certificate under the expert yardstick ----------------
_hg = load("experiments/c18_human_gap.json")
_FB = {"suite": "the suite label", "weak": "the shipped-database label", "drop": "dropped"}
_hrows = []
for _c in ("xiyansql-32b", "kwai-autosql-32b"):
    for _j, _fb in enumerate(("suite", "weak", "drop")):
        _v = _hg["certificate"]["agreed"][_fb][_c]
        _hrows.append(f"{SHORT[_c] if _j == 0 else ''} & {_FB[_fb]} & "
                      f"{_v['gap']:+.2f} & {_v['dma']:+.2f} \\\\")
    _g = [_hg["certificate"][_e][_f][_c]["gap"] for _e in ("E1", "E2") for _f in ("suite", "weak", "drop")]
    _d = [_hg["certificate"][_e][_f][_c]["dma"] for _e in ("E1", "E2") for _f in ("suite", "weak", "drop")]
    _hrows.append(f" & either expert alone & {min(_g):+.2f} to {max(_g):+.2f} & "
                  f"{max(_d):+.2f} to {min(_d):+.2f} \\\\")
    _s = _hg["sides"][_c]
    _hrows.append(f" & \\multicolumn{{3}}{{l}}{{\\footnotesize experts call wrong "
                  f"{_s['suite_accepted']['share']*100:.1f}\\% of the {_s['suite_accepted']['n']} answers the suite accepts, "
                  f"{_s['suite_rejected']['share']*100:.1f}\\% of the {_s['suite_rejected']['n']} it rejects}} \\\\")
    if _c != "kwai-autosql-32b":
        _hrows.append(r"\addlinespace")

t14 = (r"""\begin{table}[t]
\centering
\caption{The certificate re-scored against the expert labels of \cref{app:yardstick}, at $\alpha=0.10$ under question splits, generation seed 101. Unlike every earlier relabelling, these labels cover both sides of the suite oracle, so the sign is read off rather than bracketed. GAP is the risk the current-practice cell carries under the experts minus the risk it reports on its own labels; D minus A is the expert-judged risk of the fully multi-instance cell minus that of the current-practice cell, each cell answering at the threshold its own calibration selected. Rows differ in what is done with the questions the experts called underspecified or could not judge. Post hoc: the preregistration for this audit fixed the alignment endpoint and declined to preregister a claim about the sign.}
\label{tab:human_gap}
\footnotesize
\setlength{\tabcolsep}{5pt}
\begin{tabular}{llcc}
\toprule
Checkpoint & Unjudged verdicts & GAP (pts) & $\DmA$ (pts) \\
\midrule
""" + "\n".join(_hrows) + r"""
\bottomrule
\end{tabular}
\end{table}
""")
write("TABLE_14_human_gap.tex", t14)

print("pass counts by convention:", counts)
print("all tables written")
