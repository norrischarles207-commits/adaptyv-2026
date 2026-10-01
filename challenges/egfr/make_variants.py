#!/usr/bin/env python3
"""
Build pH-switch variants of egfr_l93_s713816.

Rationale (measured, ChimeraX 2026-10-01, all three Stage 2 models):
    Ser32 OG -> His409 NE2 = 3.332 / 3.397 / 3.628 A   (mean 3.45)
    Ser33 OG -> His409 NE2 = 4.452 A                   (model_0)
    His36 NE2 -> His409 NE2 = 4.971 A                  (model_0)
    Lys40 NZ -> His409 NE2 = 8.402 A   (too far to matter; not targeted)

Ser OG and Asp OD sit at essentially the same distance from CB (~2.4-2.5 A),
so S32D should place a carboxylate where the hydroxyl currently sits. A
Ser-His hydrogen bond is pH-insensitive; an Asp-His pair is not.

Writes challenges/egfr/fasta/l93_variants.fasta

Usage:  python3 challenges/egfr/make_variants.py
        python3 challenges/egfr/make_variants.py --dry-run
"""

import csv
import os
import sys

SRC = "challenges/egfr/v3c-core-designs.csv"
OUT = "challenges/egfr/fasta/l93_variants.fasta"
PARENT = "egfr_l93_s713816"
PARENT_LEN = 93
DRY = "--dry-run" in sys.argv

# 1-based position -> residue we REQUIRE to be there before mutating.
# If any of these fail the structure numbering does not match the sequence
# and every variant below would be wrong.
ANCHORS = {32: "S", 33: "S", 36: "H"}

# name -> list of (1-based position, new residue)
VARIANTS = [
    ("l93_S32D",       [(32, "D")]),
    ("l93_S32D_S33D",  [(32, "D"), (33, "D")]),
    ("l93_S32E",       [(32, "E")]),
    ("l93_H36E",       [(36, "E")]),
]

STANDARD_AA = set("ACDEFGHIKLMNPQRSTVWY")


def die(m):
    sys.exit("FAIL: " + m)


def load_parent():
    if not os.path.exists(SRC):
        die("%s not found. Run from the repo root." % SRC)
    with open(SRC, newline="") as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        die("%s is empty" % SRC)

    low = {c.lower().strip(): c for c in rows[0].keys()}
    ncol = next((low[c] for c in ("name", "design", "design_name", "id") if c in low), None)
    scol = next((low[c] for c in ("sequence", "seq", "binder_sequence") if c in low), None)
    if not ncol or not scol:
        die("no name/sequence column; header = " + ", ".join(rows[0].keys()))

    for r in rows:
        if (r.get(ncol) or "").strip() == PARENT:
            return (r.get(scol) or "").strip().upper()
    die("%s not found in %s" % (PARENT, SRC))


def main():
    seq = load_parent()
    print("parent : %s" % PARENT)
    print("length : %d" % len(seq))

    if len(seq) != PARENT_LEN:
        die("parent is %d aa, expected %d" % (len(seq), PARENT_LEN))
    bad = sorted(set(seq) - STANDARD_AA)
    if bad:
        die("parent has non-standard residues: %s" % " ".join(bad))

    print("\nANCHOR CHECK (sequence position vs structure)")
    for pos, want in sorted(ANCHORS.items()):
        got = seq[pos - 1]
        flag = "ok" if got == want else ">> MISMATCH <<"
        print("  position %-3d expected %s, found %s   %s" % (pos, want, got, flag))
        if got != want:
            die("position %d is %s, not %s. The structure residue numbering does\n"
                "      not line up with the sequence -- every variant below would\n"
                "      target the wrong residue. Stop and re-check before running."
                % (pos, got, want))

    records = [(PARENT + "_parent", seq)]
    print("\nVARIANTS")
    for name, muts in VARIANTS:
        s = list(seq)
        desc = []
        for pos, new in muts:
            old = s[pos - 1]
            s[pos - 1] = new
            desc.append("%s%d%s" % (old, pos, new))
        v = "".join(s)
        if len(v) != PARENT_LEN:
            die("%s changed length -- impossible, abort" % name)
        if set(v) - STANDARD_AA:
            die("%s has non-standard residues" % name)
        if v == seq:
            die("%s is identical to parent -- mutation did not apply" % name)
        ndiff = sum(1 for a, b in zip(seq, v) if a != b)
        if ndiff != len(muts):
            die("%s differs at %d positions, expected %d" % (name, ndiff, len(muts)))
        print("  %-18s %-14s  %d substitution(s)" % (name, ",".join(desc), ndiff))
        records.append((name, v))

    names = [n for n, _ in records]
    seqs = [s for _, s in records]
    if len(set(names)) != len(names):
        die("duplicate variant names")
    if len(set(seqs)) != len(seqs):
        die("two variants produced identical sequences")

    print("\n%d records (parent + %d variants)" % (len(records), len(records) - 1))

    if DRY:
        print("--dry-run: not writing %s" % OUT)
        return

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        for name, s in records:
            fh.write(">%s\n" % name)
            for i in range(0, len(s), 60):
                fh.write(s[i:i + 60] + "\n")

    with open(OUT) as fh:
        lines = fh.read().splitlines()
    back, cur, buf = [], None, []
    for ln in lines:
        if ln.startswith(">"):
            if cur:
                back.append((cur, "".join(buf)))
            cur, buf = ln[1:], []
        else:
            buf.append(ln.strip())
    if cur:
        back.append((cur, "".join(buf)))
    if back != records:
        die("round-trip mismatch on %s" % OUT)

    print("round-trip verified. wrote %s" % OUT)


if __name__ == "__main__":
    main()
