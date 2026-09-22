#!/usr/bin/env python3
"""The two secondary analyses of PREREGISTRATION_4 that the first pass left unrun.

Section 4.2, the reversal count recomputed under the expert labels. The reversal of Section 6.4 is
a sign that flips between the two cells when the labels switch from the shipped database to the
suite. Substituting the expert labels for the suite's asks whether the flip needed the suite to be
the D-built score's own oracle: expert labels are nobody's own oracle, so a reversal that survives
the substitution is not an artefact of the score being scored by its own instances.

Section 4.6, instance cross-fit alignment. The archived cross-fit pools build the suite partition
and its labels from one half of each schema's suite instances and judge correctness on the other
half, so each class carries both. Comparing a score's AUROC under the instances that built it with
its AUROC under instances it never saw isolates the instance-level part of the alignment. It cannot
reach a defect in the reference query, which both halves share, so it bounds one component and not
the whole; the expert audit is what reaches the rest.
"""
import argparse, csv, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c4_recompute import load, pool_files
from c11_dma_decomposition import top_reps

GEN_SEED = 101
USABLE = ("answers", "does_not_answer")
TAGS4 = ("kwai-autosql-32b", "kwai-autosql-14b", "omnisql-32b", "xiyansql-32b")


def auroc(pairs):
    pos = [s for s, y in pairs if y]
    neg = [s for s, y in pairs if not y]
    if not pos or not neg:
        return None
    order = sorted({s for s, _ in pairs})
    rank = {s: i for i, s in enumerate(order)}
    tot = sum(1.0 if rank[p] > rank[n] else 0.5 if rank[p] == rank[n] else 0.0
              for p in pos for n in neg)
    return tot / (len(pos) * len(neg))


def top_of(cls):
    n = sum(c["count"] for c in cls)
    m = [c["count"] / n for c in cls]
    return max(m), cls[[j for j, x in enumerate(m) if x == max(m)][0]]


def reversal_under_experts(key, sheets):
    by = {r["item_id"]: r for r in key["key"]}
    agreed = {i: sheets["E1"][i] for i in by if sheets["E1"][i] == sheets["E2"][i]}
    out, survived, total = {}, 0, 0
    for tag in key["checkpoints"]:
        qs = load(pool_files(tag, GEN_SEED, "question"))
        hv = {c: {} for c in ("A", "D")}
        for i, r in by.items():
            for u in r["uses"]:
                if u["tag"] == tag:
                    hv[u["cell"]][r["qid"]] = agreed.get(i)
        rows = {"A": [], "D": []}
        for q in qs:
            i = q["qid"]
            for cell, part in (("A", "single"), ("D", "multi")):
                if hv[cell].get(i) not in USABLE:
                    continue
                mass, top = top_of(q[part])
                rows[cell].append({"mass": mass, "weak": top["weak_ok"],
                                   "human": hv[cell][i] == "answers"})
        cells = {}
        for cell in ("A", "D"):
            r = rows[cell]
            a_weak = auroc([(x["mass"], x["weak"]) for x in r])
            a_hum = auroc([(x["mass"], x["human"]) for x in r])
            cells[cell] = {"n": len(r), "auroc_weak": round(a_weak, 4),
                           "auroc_human": round(a_hum, 4),
                           "drop_weak_minus_human": round(a_weak - a_hum, 4)}
        rev = cells["A"]["drop_weak_minus_human"] > 0 > cells["D"]["drop_weak_minus_human"]
        cells["reversal"] = rev
        survived += rev
        total += 1
        out[tag] = cells
        print(f"  {tag:<20} drop on A {cells['A']['drop_weak_minus_human']:+.4f}   "
              f"drop on D {cells['D']['drop_weak_minus_human']:+.4f}   "
              f"reversal {'yes' if rev else 'no'}")
    print(f"  reversal survives the substitution in {survived} of {total} audited checkpoints")
    return {"per_checkpoint": out, "survived": survived, "of": total}


def crossfit_alignment():
    out = {}
    print(f"  {'checkpoint':<20}{'fold':>5}{'drop A':>10}{'drop D':>10}   instance-level alignment")
    for tag in TAGS4:
        for fold in (0, 1):
            path = (f"experiments/c4_{tag}_seed{GEN_SEED}_results_crossfit2_f{fold}"
                    f"_per_question.json")
            if not os.path.isfile(path):
                continue
            qs = json.load(open(path))["questions"]
            cells = {}
            for cell, part in (("A", "single"), ("D", "multi")):
                rows = []
                for q in qs:
                    cls = q[part]
                    if not cls or sum(c["count"] for c in cls) == 0:
                        continue
                    mass, top = top_of(cls)
                    rows.append((mass, top["constr_ok"], top["strong_ok"]))
                a_own = auroc([(m, c) for m, c, _ in rows])
                a_held = auroc([(m, h) for m, _, h in rows])
                cells[cell] = {"n": len(rows), "auroc_own_instances": round(a_own, 4),
                               "auroc_held_out": round(a_held, 4),
                               "drop": round(a_own - a_held, 4)}
            aligned = cells["D"]["drop"] > cells["A"]["drop"]
            cells["d_drops_more"] = aligned
            out[f"{tag}|f{fold}"] = cells
            print(f"  {tag:<20}{fold:>5}{cells['A']['drop']:>+10.4f}{cells['D']['drop']:>+10.4f}"
                  f"   {'yes' if aligned else 'no'}")
    n = sum(1 for v in out.values() if v["d_drops_more"])
    print(f"  the suite-partition score loses more on unseen instances in {n} of {len(out)} pools")
    return {"per_pool": out, "d_drops_more": n, "of": len(out)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--key", default="experiments/c15_alignment_audit_key.json")
    ap.add_argument("--out", default="experiments/c19_prereg4_secondaries.json")
    a = ap.parse_args()
    key = json.load(open(a.key))
    sheets = {e: {r["item_id"].strip(): (r.get("verdict") or "").strip()
                  for r in csv.DictReader(open(f"experiments/alignment-audit/RESPONSES_{e}.csv",
                                               encoding="utf-8-sig"))} for e in ("E1", "E2")}
    print("section 4.2: the reversal recomputed with expert labels in place of the suite's\n")
    rev = reversal_under_experts(key, sheets)
    print("\nsection 4.6: instance cross-fit alignment, no new labels\n")
    cf = crossfit_alignment()
    json.dump({"note": __doc__.strip().splitlines()[0], "reversal_under_experts": rev,
               "instance_crossfit": cf}, open(a.out, "w"), indent=1)
    print("\nSaved: " + a.out)


if __name__ == "__main__":
    main()
