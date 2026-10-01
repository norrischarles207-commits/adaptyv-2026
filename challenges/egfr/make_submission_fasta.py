#!/usr/bin/env python3
"""
Emit submission.fasta from submission.csv, so the entry can be uploaded in
whichever format the portal actually wants.

Adaptyv's prior EGFR round was submitted as FASTA; the CSV schema this repo
assumes is not corroborated by any public template. This makes the FASTA a
derived artifact of the CSV rather than a second hand-maintained list, so the
two cannot drift.

Usage:  python3 challenges/egfr/make_submission_fasta.py [--dry-run]
"""
import csv
import os
import sys

SRC = "challenges/egfr/submission.csv"
DST = "challenges/egfr/submission.fasta"
DRY = "--dry-run" in sys.argv

AA = set("ACDEFGHIKLMNPQRSTVWY")


def die(m):
    sys.exit("FAIL: " + m)


def main():
    if not os.path.exists(SRC):
        die(SRC + " not found. Run build_submission.py first.")

    with open(SRC, newline="") as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        die(SRC + " has no data rows")

    for col in ("name", "sequence"):
        if col not in rows[0]:
            die("%s has no %r column; header = %s"
                % (SRC, col, ", ".join(rows[0].keys())))

    recs = []
    print("%-26s %5s  %s" % ("design", "len", "status"))
    print("-" * 52)
    for r in rows:
        n = (r["name"] or "").strip()
        s = (r["sequence"] or "").strip().upper()
        if not n:
            die("a row has an empty name")
        if not s:
            die("design %r has an empty sequence" % n)
        bad = sorted(set(s) - AA)
        if bad:
            die("design %r has non-standard residues: %s" % (n, " ".join(bad)))
        print("%-26s %5d  ok" % (n, len(s)))
        recs.append((n, s))

    names = [n for n, _ in recs]
    seqs = [s for _, s in recs]
    if len(set(names)) != len(names):
        die("duplicate names")
    if len(set(seqs)) != len(seqs):
        die("duplicate sequences")

    print("\n%d records" % len(recs))
    if DRY:
        print("--dry-run: not writing %s" % DST)
        return

    with open(DST, "w") as fh:
        for n, s in recs:
            fh.write(">%s\n" % n)
            for i in range(0, len(s), 60):
                fh.write(s[i:i + 60] + "\n")

    # read back and compare against the CSV, not against our in-memory copy
    tbl, name, buf = {}, None, []
    for ln in open(DST):
        ln = ln.strip()
        if ln.startswith(">"):
            if name:
                tbl[name] = "".join(buf)
            name, buf = ln[1:], []
        elif ln:
            buf.append(ln)
    if name:
        tbl[name] = "".join(buf)

    with open(SRC, newline="") as fh:
        for r in csv.DictReader(fh):
            n = r["name"].strip()
            s = r["sequence"].strip().upper()
            if tbl.get(n) != s:
                die("round-trip mismatch on %r" % n)
    if len(tbl) != len(recs):
        die("round-trip count: wrote %d read %d" % (len(recs), len(tbl)))

    print("round-trip verified against %s: %d/%d exact." % (SRC, len(tbl), len(recs)))
    print("wrote %s" % DST)


if __name__ == "__main__":
    main()
