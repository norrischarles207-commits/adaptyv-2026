#!/usr/bin/env python3
"""
Build the mouse full-length ECD target, and a two-record binder FASTA
(l93 parent + l93_H36E) for the species comparison.

Mouse target is built the same way rebuild_fastas.py builds the mouse domain
III slice: align the full human and mouse precursors, then read the mouse
partner residue at every position of mature 1-621. This keeps the mouse
target in the human numbering frame, so H409 stays at index 408 and
fulllength_pass's assert still applies.

Writes:
    challenges/egfr/fasta/egfr_mouse_ecd_full.fasta     621 aa
    challenges/egfr/fasta/l93_species_pair.fasta        parent + H36E

Usage:  python3 challenges/egfr/build_mouse_fulllength.py [--dry-run]
Needs:  biopython
"""

import hashlib
import os
import sys
import urllib.request

OUTDIR = "challenges/egfr/fasta"
VARIANTS = "challenges/egfr/fasta/l93_variants.fasta"
DRY = "--dry-run" in sys.argv

SIG = 24                 # human signal peptide
ECD = (1, 621)           # mature ECD range

PAIR = ["egfr_l93_s713816_parent", "l93_H36E"]


def die(m):
    sys.exit("FAIL: " + m)


def fetch_fasta(acc):
    url = "https://rest.uniprot.org/uniprotkb/%s.fasta" % acc
    with urllib.request.urlopen(url, timeout=40) as r:
        lines = r.read().decode().splitlines()
    if not lines or not lines[0].startswith(">"):
        die("unexpected FASTA for " + acc)
    return "".join(x.strip() for x in lines[1:])


def read_fasta(path):
    if not os.path.exists(path):
        die(path + " not found")
    tbl, name, buf = {}, None, []
    for ln in open(path):
        ln = ln.strip()
        if ln.startswith(">"):
            if name:
                tbl[name] = "".join(buf)
            name, buf = ln[1:], []
        elif ln:
            buf.append(ln)
    if name:
        tbl[name] = "".join(buf)
    return tbl


def write_fasta(path, records):
    with open(path, "w") as fh:
        for n, s in records:
            fh.write(">%s\n" % n)
            for i in range(0, len(s), 60):
                fh.write(s[i:i + 60] + "\n")
    back = read_fasta(path)
    for n, s in records:
        if back.get(n) != s:
            die("round-trip mismatch in " + path)


def main():
    print("fetching UniProt ...")
    human = fetch_fasta("P00533")
    mouse = fetch_fasta("Q01279")
    print("  P00533 human %d aa" % len(human))
    print("  Q01279 mouse %d aa" % len(mouse))
    if len(human) != 1210:
        die("human precursor is %d aa, expected 1210" % len(human))

    try:
        from Bio import Align
        from Bio.Align import substitution_matrices
    except ImportError:
        die("biopython not available")

    al = Align.PairwiseAligner()
    al.mode = "global"
    al.open_gap_score = -11
    al.extend_gap_score = -1
    al.substitution_matrix = substitution_matrices.load("BLOSUM62")
    aln = al.align(human, mouse)[0]

    partner = {}
    bh, bm = aln.aligned
    for (hs, he), (ms, _me) in zip(bh, bm):
        for off in range(he - hs):
            partner[hs + off + 1] = mouse[ms + off]

    seq, ndiff = [], 0
    for mat in range(ECD[0], ECD[1] + 1):
        prec = mat + SIG
        h = human[prec - 1]
        m = partner.get(prec, h)        # unaligned -> keep human
        if m != h:
            ndiff += 1
        seq.append(m)
    mecd = "".join(seq)

    print("\nmouse ECD (mature %d-%d, human numbering frame)" % ECD)
    print("  length     : %d" % len(mecd))
    print("  divergent  : %d of %d (%.1f%% identity)"
          % (ndiff, len(mecd), 100.0 * (len(mecd) - ndiff) / len(mecd)))

    if len(mecd) != 621:
        die("mouse ECD is %d aa, expected 621" % len(mecd))
    if mecd[408] != "H":
        die("mouse ECD index 408 (mature 409) = %r, expected H.\n"
            "      fulllength_pass asserts this and would refuse the target."
            % mecd[408])
    if mecd[345] != "H":
        die("mouse ECD index 345 (mature 346) = %r, expected H" % mecd[345])
    if not 50 <= ndiff <= 200:
        die("mouse ECD differs at %d positions; expected roughly 90-130 for\n"
            "      this receptor. Check the alignment before using." % ndiff)
    print("  409=H ok, 346=H ok")

    # hotspots must be conserved -- species_align.out recorded all four as such
    for mat, want in ((408, "Q"), (409, "H"), (411, "Q"), (412, "F")):
        got = mecd[mat - 1]
        if got != want:
            die("mouse mature %d = %r, expected %r (hotspots are conserved "
                "per species_align.out)" % (mat, got, want))
    print("  hotspots QHQF conserved in mouse: ok")

    tbl = read_fasta(VARIANTS)
    pair = []
    for n in PAIR:
        if n not in tbl:
            die("%r not in %s" % (n, VARIANTS))
        pair.append((n, tbl[n]))
    a, b = pair[0][1], pair[1][1]
    if len(a) != len(b):
        die("pair sequences differ in length")
    diff = [(i + 1, a[i], b[i]) for i in range(len(a)) if a[i] != b[i]]
    if [(p, o, nw) for p, o, nw in diff] != [(36, "H", "E")]:
        die("pair does not differ by exactly H36E; got %s" % diff)
    print("\nbinder pair: %s and %s, single substitution H36E confirmed"
          % (PAIR[0], PAIR[1]))

    print("\nRECORDS")
    for n, s in [("egfr_mouse_ecd_full.fasta", mecd)] + \
                [("l93_species_pair.fasta", a + b)]:
        print("  %-30s sha256[:16] %s"
              % (n, hashlib.sha256(s.encode()).hexdigest()[:16]))

    if DRY:
        print("\n--dry-run: nothing written")
        return

    os.makedirs(OUTDIR, exist_ok=True)
    write_fasta(os.path.join(OUTDIR, "egfr_mouse_ecd_full.fasta"),
                [("EGFR_MOUSE_ECD_mature_1_621|Q01279_on_P00533_frame", mecd)])
    write_fasta(os.path.join(OUTDIR, "l93_species_pair.fasta"), pair)
    print("\nwrote 2 files to %s/ (round-trip verified)" % OUTDIR)


if __name__ == "__main__":
    main()
