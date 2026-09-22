#!/usr/bin/env python3
"""What the outstanding adjudication can and cannot change in the PREREGISTRATION_4 endpoint.

Two experts judged every item independently. Where they disagree the protocol sends the item to a
third pass, which may return any verdict. Rather than wait on that pass to know what the round
found, this bounds it: for each checkpoint, search over assignments of the disagreed items for the
resolution that maximises the contrast and the one that minimises it. If the preregistered verdict
is the same at both ends, the adjudication cannot decide the result, and the round can be reported
with the bound in place of a point estimate it does not have.

The search is a greedy hill climb over one item at a time, so the interval it returns is attainable
and is reported as the widest we could construct, not as a proof of the extremes.
"""
import argparse, csv, json, math, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c15_alignment_audit_analyse import delong, two_sided_p, cells_for

USABLE = ("answers", "does_not_answer")
CANDIDATES = ("answers", "does_not_answer", "question_underspecified")


def endpoint(tag, by, data, verdict):
    pos, neg = [], []
    for i, r in by.items():
        if not any(u["tag"] == tag and u["same_sql"] for u in r["uses"]):
            continue
        v = verdict.get(i)
        if v not in USABLE:
            continue
        row = data[tag][r["qid"]]
        (pos if v == "answers" else neg).append([row["score_a"], row["score_d"]])
    auc, S = delong(pos, neg)
    var = S[0][0] + S[1][1] - 2 * S[0][1]
    d = auc[1] - auc[0]
    return {"auroc_a": auc[0], "auroc_d": auc[1], "delta": d,
            "se": math.sqrt(var) if var > 0 else 0.0,
            "p": two_sided_p(d / math.sqrt(var)) if var > 0 else 1.0,
            "n_correct": len(pos), "n_wrong": len(neg)}


def extreme(tag, by, data, base, disagreed, sign):
    v = dict(base)
    moved = True
    while moved:
        moved = False
        cur = endpoint(tag, by, data, v)["delta"]
        for i in disagreed:
            for cand in CANDIDATES:
                if cand == v.get(i):
                    continue
                old = v.get(i)
                v[i] = cand
                new = endpoint(tag, by, data, v)["delta"]
                if sign * (new - cur) > 1e-9:
                    cur, moved = new, True
                else:
                    v[i] = old
    return endpoint(tag, by, data, v)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--key", default="experiments/c15_alignment_audit_key.json")
    ap.add_argument("--sheets", nargs="*", default=["E1", "E2"])
    ap.add_argument("--out", default="experiments/c17_alignment_adjudication_bound.json")
    a = ap.parse_args()

    key = json.load(open(a.key))
    by = {r["item_id"]: r for r in key["key"]}
    tags = key["checkpoints"]
    data = {t: cells_for(t) for t in tags}
    S = {e: {r["item_id"].strip(): (r.get("verdict") or "").strip()
             for r in csv.DictReader(open(f"experiments/alignment-audit/RESPONSES_{e}.csv",
                                          encoding="utf-8-sig"))} for e in a.sheets}
    e1, e2 = a.sheets
    disagreed = [i for i in by if S[e1][i] != S[e2][i]]
    agreed = {i: S[e1][i] for i in by if S[e1][i] == S[e2][i]}

    report = {"note": __doc__.strip().splitlines()[0], "items": len(by),
              "disagreed": len(disagreed), "agreed": len(agreed), "checkpoints": {}}
    print(f"items {len(by)}   two experts disagree on {len(disagreed)}   agreed subset {len(agreed)}\n")
    for tag in tags:
        d = [i for i in disagreed
             if any(u["tag"] == tag and u["same_sql"] for u in by[i]["uses"])]
        rows = {"agreed_only": endpoint(tag, by, data, agreed),
                e1: endpoint(tag, by, data, S[e1]),
                e2: endpoint(tag, by, data, S[e2]),
                "max": extreme(tag, by, data, agreed, d, +1),
                "min": extreme(tag, by, data, agreed, d, -1)}
        report["checkpoints"][tag] = {"disagreed_items": len(d),
                                      **{k: {kk: round(vv, 4) for kk, vv in v.items()}
                                         for k, v in rows.items()}}
        sig = {k: v["p"] < 0.05 for k, v in rows.items()}
        report["checkpoints"][tag]["verdict_invariant"] = len(set(sig.values())) == 1
        print(f"{tag}   disagreed items {len(d)}")
        for k in ("agreed_only", e1, e2, "min", "max"):
            v = rows[k]
            print(f"  {k:<12} AUROC A {v['auroc_a']:.3f}  D {v['auroc_d']:.3f}  "
                  f"delta {v['delta']:+.4f}  se {v['se']:.4f}  p {v['p']:.4f}"
                  f"{'  significant' if v['p'] < 0.05 else ''}")
        print(f"  significance is the same at both extremes: "
              f"{report['checkpoints'][tag]['verdict_invariant']}\n")

    json.dump(report, open(a.out, "w"), indent=1)
    print("Saved: " + a.out)


if __name__ == "__main__":
    main()
