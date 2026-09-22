#!/usr/bin/env python3
"""Frozen analysis for PREREGISTRATION_4: does the suite partition build a better score under a
yardstick neither oracle produced?

The endpoint is a paired comparison of two scores predicting one binary outcome on the questions
where both cells return the same SQL. One human verdict serves both cells there, so the only thing
that differs between them is the score. The test is DeLong's for two correlated ROC curves.

Committed with PREREGISTRATION_4.md and before any human label exists. Any change to this file
after that point is a deviation and goes in section 8 of that document.

  --simulate   run the whole pipeline against the suite oracle's own labels instead of human ones.
               This is a self-test of the code path, NOT a result: the suite labels are one of the
               two oracles whose circularity is the thing under test.
"""
import argparse, collections, csv, json, math, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c4_recompute import load, pool_files
from c11_dma_decomposition import top_reps

SCORES = ("top_class_mass",)          # primary; the other five enter as a secondary
PRIMARY = "top_class_mass"
GEN_SEED = 101


def psi(a, b):
    return 1.0 if a > b else 0.5 if a == b else 0.0


def delong(pos, neg):
    """AUCs, variances and covariance for K correlated scores. pos/neg are lists of K-vectors."""
    m, n, K = len(pos), len(neg), len(pos[0])
    v10 = [[sum(psi(p[k], q[k]) for q in neg) / n for p in pos] for k in range(K)]
    v01 = [[sum(psi(p[k], q[k]) for p in pos) / m for q in neg] for k in range(K)]
    auc = [sum(v10[k]) / m for k in range(K)]

    def cov(v, a, b, mean_a, mean_b, size):
        return sum((v[a][i] - mean_a) * (v[b][i] - mean_b) for i in range(size)) / (size - 1)

    S = [[cov(v10, i, j, auc[i], auc[j], m) / m + cov(v01, i, j, auc[i], auc[j], n) / n
          for j in range(K)] for i in range(K)]
    return auc, S


def two_sided_p(z):
    return math.erfc(abs(z) / math.sqrt(2))


def cells_for(tag):
    """Per question: the two cells' top-class mass and the SQL each returns."""
    qs = load(pool_files(tag, GEN_SEED, "question"))
    ra, rd = top_reps(qs, "single"), top_reps(qs, "multi")
    out = {}
    for q in qs:
        i = q["qid"]
        if i not in ra or i not in rd:
            continue
        row = {"sql_a": ra[i], "sql_d": rd[i], "same_sql": ra[i] == rd[i]}
        for key, part in (("a", "single"), ("d", "multi")):
            cls = q[part]
            n = sum(c["count"] for c in cls)
            masses = [c["count"] / n for c in cls]
            top = cls[[j for j, mm in enumerate(masses) if mm == max(masses)][0]]
            row["score_" + key] = max(masses)
            row["suite_ok_" + key] = top["strong_ok"]
        out[i] = row
    return out


def read_verdicts(paths):
    """item_id -> verdict, from one adjudicated sheet or from several to be compared."""
    out = []
    for p in paths:
        d = {}
        # utf-8-sig: a sheet returned from Excel carries a BOM, which turns the first column
        # name into "\ufeffitem_id" and makes the whole file unreadable.
        with open(p, encoding="utf-8-sig") as f:
            for r in csv.DictReader(f):
                v = (r.get("verdict") or "").strip()
                if v:
                    d[r["item_id"].strip()] = v
        out.append(d)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--key", default="experiments/c15_alignment_audit_key.json")
    ap.add_argument("--responses", nargs="*", default=[],
                    help="adjudicated sheet; several are reported as agreement only")
    ap.add_argument("--simulate", action="store_true")
    ap.add_argument("--out", default="experiments/c15_alignment_audit_result.json")
    a = ap.parse_args()

    key = json.load(open(a.key))
    by_item = {r["item_id"]: r for r in key["key"]}
    tags = key["checkpoints"]
    data = {t: cells_for(t) for t in tags}

    verdict = {}
    if a.simulate:
        for iid, r in by_item.items():
            u = r["uses"][0]
            row = data[u["tag"]][r["qid"]]
            verdict[iid] = "answers" if row["suite_ok_" + u["cell"].lower()] else "does_not_answer"
    else:
        sheets = read_verdicts(a.responses)
        if not sheets:
            raise SystemExit("no responses given; pass --responses <adjudicated.csv> or --simulate")
        verdict = sheets[-1]

    report = {"source": "SIMULATED on suite labels, not a result" if a.simulate else a.responses,
              "items_sha256": key["items_sha256"], "checkpoints": {}}
    verdicts_seen = collections.Counter(verdict.values())
    report["verdict_counts"] = dict(verdicts_seen)

    for tag in tags:
        pos, neg, skipped = [], [], 0
        for iid, r in by_item.items():
            uses = [u for u in r["uses"] if u["tag"] == tag and u["same_sql"]]
            if not uses:
                continue
            v = verdict.get(iid)
            if v is None:
                skipped += 1
                continue
            if v not in ("answers", "does_not_answer"):
                continue
            row = data[tag][r["qid"]]
            vec = [row["score_a"], row["score_d"]]
            (pos if v == "answers" else neg).append(vec)
        if not pos or not neg:
            report["checkpoints"][tag] = {"error": "a class is empty", "unlabelled": skipped}
            continue
        auc, S = delong(pos, neg)
        var = S[0][0] + S[1][1] - 2 * S[0][1]
        delta = auc[1] - auc[0]
        z = delta / math.sqrt(var) if var > 0 else 0.0
        p = two_sided_p(z)
        report["checkpoints"][tag] = {
            "score": PRIMARY, "n_correct": len(pos), "n_wrong": len(neg), "unlabelled": skipped,
            "auroc_built_on_A": round(auc[0], 4), "auroc_built_on_D": round(auc[1], 4),
            "delta": round(delta, 4), "se": round(math.sqrt(var), 4),
            "z": round(z, 3), "p_two_sided": round(p, 5), "significant_05": p < 0.05}
        print(f"{tag:<20} A {auc[0]:.3f}  D {auc[1]:.3f}  delta {delta:+.3f}  "
              f"se {math.sqrt(var):.4f}  p {p:.4f}")

    # the preregistered three-way rule, section 3
    rows = [v for v in report["checkpoints"].values() if "delta" in v]
    if len(rows) == len(tags):
        if all(r["delta"] > 0 and r["significant_05"] for r in rows):
            verdict_label = "SUBSTANTIVE"
        elif all(r["delta"] <= 0 for r in rows) or \
             (not any(r["significant_05"] for r in rows) and all(r["delta"] < 0.02 for r in rows)):
            verdict_label = "CIRCULAR"
        else:
            verdict_label = "MIXED"
        report["preregistered_verdict"] = verdict_label
        print(f"\npreregistered verdict: {verdict_label}"
              + ("   [SIMULATED, not a result]" if a.simulate else ""))

    json.dump(report, open(a.out, "w"), indent=1)
    print("Saved: " + a.out)


if __name__ == "__main__":
    main()
