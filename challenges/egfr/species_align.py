#!/usr/bin/env python3
"""
Human vs mouse EGFR domain III conservation.

Pulls UniProt P00533 (human EGFR) and Q01279 (mouse Egfr), globally aligns
the full precursors, and reports conservation at positions of interest.

NUMBERING
  POSITIONS below are MATURE numbering.
  precursor = mature + 24   (signal peptide = precursor 1-24)
  Domain III = mature 310-514 = precursor 334-538
  Full precursors are aligned, so mouse signal-peptide length is irrelevant.
"""

import sys
import urllib.request

try:
    from Bio import Align
except ImportError:
    sys.exit("Need biopython:  pip3 install --user biopython")

SIG = 24
DOM3 = (310, 514)

POSITIONS = {
    408: "Arm A hotspot - cetuximab contact, NOT a G5V2 contact",
    409: "Arm A hotspot - pH anchor His; cetuximab AND G5V2",
    411: "Arm A hotspot - G5V2 contact",
    412: "Arm A hotspot",
    384: "dropped for glycan risk",
    465: "dropped; G5V2 + cetuximab contact",
    466: "dropped",
    346: "G5V2 second histidine",
    353: "G5V2 + cetuximab contact",
    382: "G5V2 contact",
    467: "mouse-divergent per earlier analysis",
    468: "mouse-divergent per earlier analysis; cetuximab contact",
}


def fetch(acc):
    url = "https://rest.uniprot.org/uniprotkb/%s.fasta" % acc
    with urllib.request.urlopen(url, timeout=30) as r:
        lines = r.read().decode().splitlines()
    return lines[0], "".join(x.strip() for x in lines[1:])


def main():
    h_hdr, human = fetch("P00533")
    m_hdr, mouse = fetch("Q01279")
    print("human: %s\n       %d aa" % (h_hdr, len(human)))
    print("mouse: %s\n       %d aa\n" % (m_hdr, len(mouse)))

    if len(human) != 1210:
        print("!! WARNING: human precursor %d aa, expected 1210." % len(human))
        print("   Canonical isoform may have changed. Verify before trusting.\n")

    al = Align.PairwiseAligner()
    al.mode = "global"
    al.open_gap_score = -11
    al.extend_gap_score = -1
    try:
        from Bio.Align import substitution_matrices
        al.substitution_matrix = substitution_matrices.load("BLOSUM62")
    except Exception:
        al.match_score, al.mismatch_score = 2, -1

    aln = al.align(human, mouse)[0]

    # map human 1-based precursor position -> aligned mouse residue
    partner = {}
    bh, bm = aln.aligned
    for (hs, he), (ms, _me) in zip(bh, bm):
        for off in range(he - hs):
            partner[hs + off + 1] = mouse[ms + off]

    lo, hi = DOM3[0] + SIG, DOM3[1] + SIG
    same = tot = 0
    diffs = []
    for p in range(lo, hi + 1):
        hr, mr = human[p - 1], partner.get(p, "-")
        tot += 1
        if hr == mr:
            same += 1
        else:
            diffs.append((p - SIG, p, hr, mr))

    print("Domain III (mature %d-%d = precursor %d-%d), %d positions"
          % (DOM3[0], DOM3[1], lo, hi, tot))
    print("identity: %d/%d = %.1f%%\n" % (same, tot, 100.0 * same / tot))

    print("POSITIONS OF INTEREST")
    print("%7s %6s %6s %6s  %-9s %s"
          % ("mature", "prec", "human", "mouse", "same?", "note"))
    print("-" * 90)
    for mat in sorted(POSITIONS):
        pr = mat + SIG
        hr, mr = human[pr - 1], partner.get(pr, "-")
        print("%7d %6d %6s %6s  %-9s %s"
              % (mat, pr, hr, mr, "yes" if hr == mr else ">> NO <<",
                 POSITIONS[mat]))

    print("\nALL %d DIVERGENT POSITIONS IN DOMAIN III" % len(diffs))
    print("%7s %6s %6s %6s" % ("mature", "prec", "human", "mouse"))
    print("-" * 32)
    for mat, pr, hr, mr in diffs:
        print("%7d %6d %6s %6s" % (mat, pr, hr, mr))

    print("\nSANITY CHECKS - if any FAIL, numbering is wrong, discard the above")
    ok = True
    for mat, exp, desc in [(409, "H", "pH anchor = precursor H433"),
                           (346, "H", "G5V2 second His = precursor H370"),
                           (353, "R", "= precursor R377"),
                           (465, "K", "= precursor K489")]:
        got = human[mat + SIG - 1]
        ok &= (got == exp)
        print("  %-4s mature %d = %s (expected %s)  %s"
              % ("PASS" if got == exp else "FAIL", mat, got, exp, desc))
    if not ok:
        print("\n  !! NUMBERING IS OFF. Do not use the table above.")


if __name__ == "__main__":
    main()
