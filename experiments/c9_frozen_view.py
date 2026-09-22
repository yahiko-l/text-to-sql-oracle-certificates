#!/usr/bin/env python3
"""Rewrite an archived per-question file into the frozen analyser's own tie convention.

The per-question files list classes by (-count, str(class_key)) but do not carry class_key, so a
recomputation reading one of them takes the earliest listed class among a tie while the frozen
analyser took the largest key. That is the whole difference between the two conventions, and it
touches 53 of 12,192 top-class decisions.

The files themselves are not edited: each results file records the sha256 of its per-question
sibling, and rewriting one in place would break that pin. This script emits a separate frozen view
instead, moving the frozen top class to the front of its class list on the tied decisions only.
Counts and masses are untouched, because tied classes have equal counts; what moves is which class
is answered, and therefore its correctness labels.

The frozen choices come from c9_tie_reconstruction.json, which rebuilt them by re-running the
union-find on the tied questions. Analyser runs from now on emit class_key directly and need none
of this.

  python3 experiments/c9_frozen_view.py experiments/c4_kwai-autosql-14b_seed101_results_official_per_question.json
  python3 experiments/c9_frozen_view.py --all --out-dir experiments/frozen_view
"""
import argparse
import copy
import glob
import hashlib
import json
import os
import re

RECON = "experiments/c9_tie_reconstruction.json"


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def frozen_map():
    return {(x["tag"], x["seed"], x["qid"], x["part"]): x
            for x in json.load(open(RECON))["decisions"]}


def tag_seed(path):
    """The pool identity the reconstruction keys on, read off the file name."""
    m = re.search(r"c4_([a-z0-9.-]+)_seed(\d+)_results", os.path.basename(path))
    return (m.group(1), int(m.group(2))) if m else (None, None)


def recorded_hash(pq_path):
    """The sha256 the sibling results file pinned for this per-question file, if there is one."""
    for cand in glob.glob(re.sub(r"_per_question\.json$", ".json", pq_path)):
        try:
            p = json.load(open(cand)).get("provenance", {})
        except (ValueError, OSError):
            continue
        if p.get("per_question_file", "").endswith(os.path.basename(pq_path)):
            return p.get("per_question_sha256")
    return None


def convert(pq_path, fm, out_dir, strict=True):
    tag, seed = tag_seed(pq_path)
    want = recorded_hash(pq_path)
    got = sha256(pq_path)
    if want and want != got:
        msg = (f"{pq_path}: hashes to {got}, its results file pinned {want}. The archived file has "
               f"changed since the run that produced it; refusing to convert.")
        if strict:
            raise SystemExit(msg)
        print("  " + msg)
        return None
    d = json.load(open(pq_path))
    out = copy.deepcopy(d)
    moved = 0
    if tag is not None:
        for q in out["questions"]:
            for part in ("single", "multi"):
                f = fm.get((tag, seed, q["qid"], part))
                if not f or f["same_rep"]:
                    continue
                cls = q[part]
                i = next((j for j, c in enumerate(cls)
                          if c["representative"] == f["frozen_rep"]), None)
                if i is None:
                    raise SystemExit(f"{pq_path} q{q['qid']} {part}: the frozen representative is "
                                     f"not in the class list")
                cls.insert(0, cls.pop(i))
                moved += 1
    out["tie_convention"] = "frozen-analyser"
    out["note"] = ("the frozen analyser's convention: on a tie for the top class it took the "
                   "largest class_key, and that class has been moved to the front of its list "
                   "here. Counts and masses are exactly as the analyser wrote them, because tied "
                   "classes have equal counts. The archived file this was built from uses file "
                   "order instead. " + d.get("note", ""))
    out["built_from"] = {"file": pq_path, "sha256": got,
                         "reconstruction": RECON, "reconstruction_sha256": sha256(RECON)}
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, os.path.basename(pq_path))
    json.dump(out, open(dst, "w"), indent=1, ensure_ascii=False)
    return dst, moved, tag


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("per_question", nargs="*")
    ap.add_argument("--all", action="store_true",
                    help="convert the files the reconstruction covers: the official question-split "
                         "and database-split per-question files of the twelve main pools")
    ap.add_argument("--out-dir", default="experiments/frozen_view")
    a = ap.parse_args()

    fm = frozen_map()
    # The reconstruction was built for the official question-split and database-split files of
    # the twelve main pools. The other variants (cross-fit folds, candidates-only, gold-free, the
    # budget denominator) build their classes from a different instance subset, so the same
    # decisions do not apply to them and are not offered here.
    paths = a.per_question or (sorted(glob.glob("experiments/c4_*_results_official_per_question.json")
                                      + glob.glob("experiments/c4_*_results_official_dbsplit_per_question.json"))
                               if a.all else [])
    if not paths:
        raise SystemExit("give a per-question file, or --all")

    total_moved = converted = skipped = 0
    for p in paths:
        r = convert(p, fm, a.out_dir, strict=not a.all)
        if r is None:
            skipped += 1
            continue
        dst, moved, tag = r
        converted += 1
        total_moved += moved
        if moved or not a.all:
            print(f"  {os.path.basename(p)}: {moved} tied decision(s) moved"
                  f"{'' if tag else ', pool not in the reconstruction, copied unchanged'}")
    print(f"\n{converted} file(s) written to {a.out_dir}, {total_moved} tied decision(s) moved"
          + (f", {skipped} skipped on a hash mismatch" if skipped else ""))


if __name__ == "__main__":
    main()
