#!/usr/bin/env python3
"""How far the two experts of the independent-yardstick audit agree with each other.

Section 7 reports agreement on the four-way verdict over every item, and agreement on correct
against wrong over the items both experts judged one way or the other, each with Cohen's kappa.
Both are read off the two answer sheets as the experts returned them, before any adjudication.
"""
import argparse, collections, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c15_alignment_audit_analyse import read_verdicts  # noqa: E402

USABLE = ("answers", "does_not_answer")


def agreement(pairs):
    """Observed agreement and Cohen's kappa over (first expert, second expert) verdict pairs."""
    n = len(pairs)
    po = sum(a == b for a, b in pairs) / n
    first = collections.Counter(a for a, _ in pairs)
    second = collections.Counter(b for _, b in pairs)
    pe = sum(first[k] * second[k] for k in first) / (n * n)
    return {"items": n, "agreement": round(po, 4), "kappa": round((po - pe) / (1 - pe), 4)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--responses", nargs=2,
                    default=["experiments/alignment-audit/RESPONSES_E1.csv",
                             "experiments/alignment-audit/RESPONSES_E2.csv"])
    ap.add_argument("--out", default="experiments/c21_expert_agreement.json")
    a = ap.parse_args()

    first, second = read_verdicts(a.responses)
    if set(first) != set(second):
        raise SystemExit("the two sheets do not cover the same items")
    ids = sorted(first)
    four_way = agreement([(first[i], second[i]) for i in ids])
    binary = agreement([(first[i], second[i]) for i in ids
                        if first[i] in USABLE and second[i] in USABLE])
    json.dump({"note": "agreement between the two experts of the independent-yardstick audit, on "
                       "their own sheets before adjudication. The binary reading is correct against "
                       "wrong, over the items both experts judged answers or does_not_answer.",
               "responses": a.responses,
               "verdicts": {"first": dict(collections.Counter(first.values())),
                            "second": dict(collections.Counter(second.values()))},
               "four_way": four_way, "binary": binary},
              open(a.out, "w"), indent=1)
    print(f"four-way verdict: {100 * four_way['agreement']:.1f} percent of {four_way['items']} "
          f"items, kappa {four_way['kappa']:.3f}")
    print(f"correct against wrong: {100 * binary['agreement']:.1f} percent of {binary['items']} "
          f"items, kappa {binary['kappa']:.3f}")
    print(f"written {a.out}")


if __name__ == "__main__":
    main()
