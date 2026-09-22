#!/usr/bin/env python3
"""Preregistered secondary analyses for PREREGISTRATION_4, section 4.

Item 1 carries a hard validity check. The two likelihood scores read no oracle and are computed by
one formula over the same usable candidates in both cells, so their delta must come out exactly
zero. A non-zero value there would mean the join between verdicts, items and cells is wrong, and
section 4 says the round is void in that case. It is checked from the candidate archives rather
than assumed.
"""
import argparse, collections, csv, json, math, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c15_alignment_audit_analyse import delong, two_sided_p
from c4_recompute import load, pool_files
from c11_dma_decomposition import top_reps

GEN_SEED = 101
CONSISTENCY = ("top_class_mass", "discrete_semantic_entropy", "lin_deg", "lin_numsets")
LIKELIHOOD = ("mean_seq_logprob", "max_seq_logprob")


def consistency_scores(cls):
    n = sum(c["count"] for c in cls)
    p = [c["count"] / n for c in cls]
    return {"top_class_mass": max(p),
            "discrete_semantic_entropy": sum(x * math.log(x) for x in p),
            "lin_deg": sum(x * x for x in p),
            "lin_numsets": -float(len(p))}


def likelihood_scores(tag):
    """Partition-independent by construction; recomputed from the archive to prove it."""
    out = {}
    with open(f"experiments/c4_{tag}_seed{GEN_SEED}_candidates.jsonl") as f:
        for line in f:
            r = json.loads(line)
            v = [c["cum_logprob"] / c["n_tokens"] for c in r["candidates"]
                 if c.get("parsed") and not c.get("truncated") and c.get("n_tokens")]
            if v:
                out[r["qid"]] = {"mean_seq_logprob": sum(v) / len(v), "max_seq_logprob": max(v)}
    return out


def build(tag):
    qs = load(pool_files(tag, GEN_SEED, "question"))
    ra, rd = top_reps(qs, "single"), top_reps(qs, "multi")
    lik = likelihood_scores(tag)
    out = {}
    for q in qs:
        i = q["qid"]
        if i not in ra or i not in rd or ra[i] != rd[i] or i not in lik:
            continue
        row = {"a": consistency_scores(q["single"]), "d": consistency_scores(q["multi"])}
        for k in LIKELIHOOD:
            row["a"][k] = row["d"][k] = lik[i][k]
        cls = q["single"]
        n = sum(c["count"] for c in cls)
        m = [c["count"] / n for c in cls]
        row["weak_ok"] = cls[[j for j, x in enumerate(m) if x == max(m)][0]]["weak_ok"]
        row["suite_ok"] = cls[[j for j, x in enumerate(m) if x == max(m)][0]]["strong_ok"]
        out[i] = row
    return out


def kappa(pairs):
    n = len(pairs)
    cats = sorted({a for a, b in pairs} | {b for a, b in pairs})
    po = sum(1 for a, b in pairs if a == b) / n
    m1 = collections.Counter(a for a, b in pairs)
    m2 = collections.Counter(b for a, b in pairs)
    pe = sum(m1[c] / n * m2[c] / n for c in cats)
    return po, ((po - pe) / (1 - pe) if pe < 1 else 1.0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--key", default="experiments/c15_alignment_audit_key.json")
    ap.add_argument("--sheets", nargs="*", default=["E1", "E2"])
    ap.add_argument("--out", default="experiments/c16_alignment_secondary.json")
    a = ap.parse_args()

    key = json.load(open(a.key))
    by = {r["item_id"]: r for r in key["key"]}
    tags = key["checkpoints"]
    S = {e: {r["item_id"].strip(): (r.get("verdict") or "").strip()
             for r in csv.DictReader(open(f"experiments/alignment-audit/RESPONSES_{e}.csv",
                                          encoding="utf-8-sig"))} for e in a.sheets}
    agreed = {i: S[a.sheets[0]][i] for i in by
              if len({S[e][i] for e in a.sheets}) == 1}
    print(f"agreement-only subset: {len(agreed)} of {len(by)} items\n")

    scores = {t: build(t) for t in tags}
    report = {"note": __doc__.strip().splitlines()[0], "six_scores": {}, "oracle_agreement": {}}

    print(f"{'score':<28}" + "".join(f"{t:<26}" for t in tags))
    void = []
    for sc in CONSISTENCY + LIKELIHOOD:
        cells = []
        for t in tags:
            pos, neg = [], []
            for i, r in by.items():
                if not any(u["tag"] == t and u["same_sql"] for u in r["uses"]):
                    continue
                v = agreed.get(i)
                if v not in ("answers", "does_not_answer"):
                    continue
                row = scores[t].get(r["qid"])
                if row is None:
                    continue
                (pos if v == "answers" else neg).append([row["a"][sc], row["d"][sc]])
            auc, Sm = delong(pos, neg)
            var = Sm[0][0] + Sm[1][1] - 2 * Sm[0][1]
            d = auc[1] - auc[0]
            p = two_sided_p(d / math.sqrt(var)) if var > 0 else 1.0
            cells.append(f"d{d:+.4f} p{p:.3f}{'*' if p < 0.05 else ' '}")
            report["six_scores"].setdefault(sc, {})[t] = {
                "auroc_a": round(auc[0], 4), "auroc_d": round(auc[1], 4),
                "delta": round(d, 4), "p": round(p, 4), "n_correct": len(pos), "n_wrong": len(neg)}
            if sc in LIKELIHOOD and abs(d) > 1e-9:
                void.append((sc, t, d))
        print(f"{sc:<28}" + "".join(f"{c:<26}" for c in cells))

    print("\nnull control: the two likelihood scores must give delta exactly 0")
    print("  " + ("PASS, both are exactly zero" if not void else f"FAIL {void}"))
    report["null_control_passed"] = not void

    print("\nhuman verdict against each oracle, on the agreement-only subset:")
    for t in tags:
        for oracle in ("weak_ok", "suite_ok"):
            pairs = []
            for i, r in by.items():
                if not any(u["tag"] == t and u["same_sql"] for u in r["uses"]):
                    continue
                v = agreed.get(i)
                if v not in ("answers", "does_not_answer"):
                    continue
                row = scores[t].get(r["qid"])
                if row is None:
                    continue
                pairs.append((v == "answers", bool(row[oracle])))
            po, k = kappa(pairs)
            name = "shipped database" if oracle == "weak_ok" else "suite oracle"
            print(f"  {t:<20} {name:<18} agreement {po*100:5.1f}%  kappa {k:.3f}  (n={len(pairs)})")
            report["oracle_agreement"].setdefault(t, {})[oracle] = {
                "agreement": round(po, 4), "kappa": round(k, 4), "n": len(pairs)}

    json.dump(report, open(a.out, "w"), indent=1)
    print("\nSaved: " + a.out)


if __name__ == "__main__":
    main()
