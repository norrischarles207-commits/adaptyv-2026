#!/usr/bin/env python3
"""
Build and validate submission.csv for Adaptyv Challenge 1 / Track 3.

Reads sequences from challenges/egfr/v3c-core-designs.csv, selects the
pre-registered submission set, and writes challenges/egfr/submission.csv
with columns: name,sequence,molecule_class

Refuses to write anything if ANY validation fails. Loud failure by design —
a silently malformed submission is worse than no submission.

Usage:
    python3 challenges/egfr/build_submission.py
    python3 challenges/egfr/build_submission.py --dry-run
"""

import argparse
import csv
import os
import sys

# ---------------------------------------------------------------- config

SOURCE = "challenges/egfr/v3c-core-designs.csv"
DEST = "challenges/egfr/submission.csv"

# Pre-registered submission set: the single Stage 2 passer plus the two
# next-best by composite. Order is submission order.
SUBMISSION_SET = [
    "egfr_l93_s713816",
    "egfr_l75_s674224_mpnn14",
    "egfr_l64_s902794_mpnn2",
]

MOLECULE_CLASS = "protein"

MIN_LEN, MAX_LEN = 10, 250
STANDARD_AA = set("ACDEFGHIKLMNPQRSTVWY")

# Expected lengths from the Stage 2 run, as an independent cross-check.
# If the CSV disagrees with these, we pulled the wrong sequence.
EXPECTED_LEN = {
    "egfr_l93_s713816": 93,
    "egfr_l75_s674224_mpnn14": 75,
    "egfr_l64_s902794_mpnn2": 64,
}

# Candidate column names, checked case-insensitively.
NAME_COLS = ("design", "name", "design_name", "id")
SEQ_COLS = ("sequence", "seq", "binder_sequence", "aa_sequence")

# ---------------------------------------------------------------- helpers


def die(msg):
    print("FAIL: %s" % msg, file=sys.stderr)
    sys.exit(1)


def pick_column(fieldnames, candidates, what):
    lowered = {f.lower().strip(): f for f in fieldnames}
    for c in candidates:
        if c in lowered:
            return lowered[c]
    die("no %s column in %s.\n      looked for: %s\n      found: %s"
        % (what, SOURCE, ", ".join(candidates), ", ".join(fieldnames)))


def load_source():
    if not os.path.exists(SOURCE):
        die("%s not found. Run from the repo root." % SOURCE)

    with open(SOURCE, newline="") as fh:
        reader = csv.DictReader(fh)
        if not reader.fieldnames:
            die("%s has no header row." % SOURCE)
        name_col = pick_column(reader.fieldnames, NAME_COLS, "design-name")
        seq_col = pick_column(reader.fieldnames, SEQ_COLS, "sequence")
        rows = list(reader)

    print("source:  %s" % SOURCE)
    print("columns: name=%r sequence=%r" % (name_col, seq_col))
    print("rows:    %d\n" % len(rows))

    table = {}
    for r in rows:
        key = (r.get(name_col) or "").strip()
        seq = (r.get(seq_col) or "").strip().upper()
        if not key:
            continue
        if key in table and table[key] != seq:
            die("design %r appears twice in %s with different sequences."
                % (key, SOURCE))
        table[key] = seq
    return table


def validate(name, seq):
    """Return list of problems; empty list means clean."""
    problems = []

    if not seq:
        problems.append("empty sequence")
        return problems

    bad = sorted(set(seq) - STANDARD_AA)
    if bad:
        problems.append("non-standard residues: %s" % " ".join(bad))

    if not (MIN_LEN <= len(seq) <= MAX_LEN):
        problems.append("length %d outside [%d, %d]"
                        % (len(seq), MIN_LEN, MAX_LEN))

    want = EXPECTED_LEN.get(name)
    if want is not None and len(seq) != want:
        problems.append("length %d but Stage 2 recorded %d — WRONG SEQUENCE"
                        % (len(seq), want))

    return problems


# ---------------------------------------------------------------- main


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true",
                    help="validate and print, write nothing")
    args = ap.parse_args()

    table = load_source()

    missing = [n for n in SUBMISSION_SET if n not in table]
    if missing:
        print("designs present in source:", file=sys.stderr)
        for k in sorted(table):
            print("    %s" % k, file=sys.stderr)
        die("submission set names not found in %s: %s"
            % (SOURCE, ", ".join(missing)))

    records = []
    failed = False
    print("VALIDATION")
    print("%-28s %6s  %s" % ("design", "len", "status"))
    print("-" * 68)
    for name in SUBMISSION_SET:
        seq = table[name]
        problems = validate(name, seq)
        if problems:
            failed = True
            print("%-28s %6d  FAIL: %s" % (name, len(seq), "; ".join(problems)))
        else:
            print("%-28s %6d  ok" % (name, len(seq)))
            records.append((name, seq))

    seqs = [s for _, s in records]
    if len(set(seqs)) != len(seqs):
        failed = True
        print("\nFAIL: duplicate sequences in submission set.")

    names = [n for n, _ in records]
    if len(set(names)) != len(names):
        failed = True
        print("\nFAIL: duplicate names in submission set.")

    if failed:
        die("validation failed. Nothing written.")

    print("\n%d designs validated." % len(records))

    if args.dry_run:
        print("\n--dry-run: not writing %s" % DEST)
        return

    with open(DEST, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["name", "sequence", "molecule_class"])
        for name, seq in records:
            w.writerow([name, seq, MOLECULE_CLASS])

    # Round-trip: read back what we wrote and compare to the source table.
    with open(DEST, newline="") as fh:
        back = list(csv.DictReader(fh))

    if len(back) != len(records):
        die("round-trip row count mismatch: wrote %d, read %d"
            % (len(records), len(back)))

    for row, (name, seq) in zip(back, records):
        if row["name"] != name:
            die("round-trip name mismatch: %r != %r" % (row["name"], name))
        if row["sequence"] != seq:
            die("round-trip sequence mismatch for %s" % name)
        if row["sequence"] != table[name]:
            die("round-trip lost fidelity against source for %s" % name)
        if row["molecule_class"] != MOLECULE_CLASS:
            die("round-trip molecule_class mismatch for %s" % name)

    print("round-trip verified against source: %d/%d exact.\n"
          % (len(back), len(records)))
    print("wrote %s" % DEST)
    print("\n%-28s %6s  %s" % ("name", "len", "molecule_class"))
    print("-" * 56)
    for name, seq in records:
        print("%-28s %6d  %s" % (name, len(seq), MOLECULE_CLASS))


if __name__ == "__main__":
    main()
