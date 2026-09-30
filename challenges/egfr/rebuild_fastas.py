#!/usr/bin/env python3
"""
Regenerate every FASTA the v3c pipeline consumed, deterministically from
UniProt, and commit them. The originals were written to scratch and lost;
Stage 1 and Stage 2 results currently have no input artifact in the repo.

Writes into challenges/egfr/fasta/:
    egfr_human_ecd_full.fasta     mature 1-621    (Stage 2 target)
    egfr_human_domIII.fasta       mature 311-514  (Stage 1 human target)
    egfr_mouse_domIII.fasta       mature 311-514, mouse residues at divergent
                                  positions (Stage 1 mouse target)
    egf_control.fasta             mature EGF, 53 aa (control binder)

NUMBERING
    precursor (P00533) = mature + 24 ; signal peptide = precursor 1-24
    mature ECD          = precursor 25-645   = 621 aa
    domain III slice    = mature 311-514     = 204 aa

Every derived sequence is asserted against an independently known fact
before anything is written. A failed assert means the numbering moved or
UniProt changed the canonical isoform -- stop and re-derive, do not patch
the assert.

Usage:  python3 challenges/egfr/rebuild_fastas.py
        python3 challenges/egfr/rebuild_fastas.py --dry-run
Needs:  biopython (already installed for species_align.py)
"""

import hashlib
import os
import sys
import urllib.request

OUTDIR = "challenges/egfr/fasta"
DRY = "--dry-run" in sys.argv

SIG = 24                      # signal peptide length, human
ECD_MATURE = (1, 621)         # mature ECD used as the Stage 2 target
DOM3_MATURE = (311, 514)      # domain III slice used for design and Stage 1


def die(m):
    sys.exit("FAIL: " + m)


def fetch(url):
    with urllib.request.urlopen(url, timeout=40) as r:
        return r.read().decode()


def fetch_fasta(acc):
    lines = fetch("https://rest.uniprot.org/uniprotkb/%s.fasta" % acc).splitlines()
    if not lines or not lines[0].startswith(">"):
        die("unexpected FASTA for %s" % acc)
    return "".join(x.strip() for x in lines[1:])


def mature(seq, lo, hi):
    """Slice by MATURE numbering, inclusive, 1-based."""
    return seq[lo + SIG - 1: hi + SIG]


def egf_from_flatfile():
    """Extract mature EGF from P01133's feature table. Coordinates are read
    from the FT CHAIN record, never hardcoded."""
    txt = fetch("https://rest.uniprot.org/uniprotkb/P01133.txt")
    lines = txt.splitlines()
    span = None
    for i, ln in enumerate(lines):
        if not ln.startswith("FT   CHAIN"):
            continue
        rng = ln.split()[-1]
        note = ""
        for j in range(i + 1, min(i + 4, len(lines))):
            if "/note=" in lines[j]:
                note = lines[j].split("/note=", 1)[1].strip().strip('"')
                break
        if note.lower() == "epidermal growth factor":
            try:
                a, b = rng.split("..")
                span = (int(a), int(b))
            except ValueError:
                die("could not parse CHAIN range %r" % rng)
            break
    if span is None:
        die("no CHAIN record named 'Epidermal growth factor' in P01133")
    full = fetch_fasta("P01133")
    seq = full[span[0] - 1: span[1]]
    print("  EGF chain from feature table: precursor %d..%d" % span)
    return seq


def write(name, header, seq, records):
    records.append((name, header, seq))


def main():
    print("fetching UniProt ...")
    human = fetch_fasta("P00533")
    print("  P00533 human EGFR precursor: %d aa" % len(human))
    if len(human) != 1210:
        die("human precursor is %d aa, expected 1210. UniProt may have changed\n"
            "      the canonical isoform -- every number downstream is suspect."
            % len(human))

    mouse = fetch_fasta("Q01279")
    print("  Q01279 mouse Egfr precursor: %d aa" % len(mouse))

    records = []

    # ---- Stage 2 target: full mature ECD -------------------------------
    ecd = mature(human, *ECD_MATURE)
    if len(ecd) != 621:
        die("mature ECD is %d aa, expected 621" % len(ecd))
    if ecd[408] != "H":
        die("ECD index 408 (mature 409) = %r, expected H. fulllength_pass\n"
            "      asserts this -- numbering is wrong." % ecd[408])
    if ecd[345] != "H":
        die("ECD index 345 (mature 346) = %r, expected H" % ecd[345])
    print("  mature ECD 1-621: %d aa, 409=H ok, 346=H ok" % len(ecd))
    write("egfr_human_ecd_full.fasta",
          "EGFR_HUMAN_ECD_mature_1_621|P00533|precursor_25_645", ecd, records)

    # ---- Stage 1 human target: domain III slice ------------------------
    d3h = mature(human, *DOM3_MATURE)
    if len(d3h) != 204:
        die("domain III slice is %d aa, expected 204" % len(d3h))
    for mat, want in ((409, "H"), (408, "Q"), (411, "Q"), (412, "F")):
        got = d3h[mat - DOM3_MATURE[0]]
        if got != want:
            die("domain III mature %d = %r, expected %r" % (mat, got, want))
    print("  domain III 311-514: %d aa, hotspots QHQF ok" % len(d3h))
    write("egfr_human_domIII.fasta",
          "EGFR_HUMAN_domIII_mature_311_514|P00533", d3h, records)

    # ---- Stage 1 mouse target: same slice, mouse residues --------------
    try:
        from Bio import Align
        from Bio.Align import substitution_matrices
    except ImportError:
        die("biopython not available; needed to rebuild the mouse target")

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

    d3m = []
    ndiff = 0
    for mat in range(DOM3_MATURE[0], DOM3_MATURE[1] + 1):
        prec = mat + SIG
        h = human[prec - 1]
        m = partner.get(prec, h)     # unaligned -> keep human
        if m != h:
            ndiff += 1
        d3m.append(m)
    d3m = "".join(d3m)
    if len(d3m) != 204:
        die("mouse domain III slice is %d aa, expected 204" % len(d3m))
    print("  mouse domain III: %d aa, %d positions differ from human" % (len(d3m), ndiff))
    if not 20 <= ndiff <= 30:
        die("mouse slice differs at %d positions; species_align.out recorded 26\n"
            "      over mature 310-514. Something moved -- check before using." % ndiff)
    for mat, want in ((409, "H"), (408, "Q"), (411, "Q"), (412, "F")):
        got = d3m[mat - DOM3_MATURE[0]]
        if got != want:
            die("mouse domain III mature %d = %r, expected %r (hotspots are\n"
                "      conserved per species_align.out)" % (mat, got, want))
    print("    hotspots conserved in mouse slice: ok")
    write("egfr_mouse_domIII.fasta",
          "EGFR_MOUSE_domIII_mature_311_514|Q01279_on_P00533_frame", d3m, records)

    # ---- control binder: mature EGF ------------------------------------
    egf = egf_from_flatfile()
    if len(egf) != 53:
        die("mature EGF is %d aa, expected 53" % len(egf))
    if not egf.startswith("N"):
        print("  note: EGF starts with %r, not N -- verify against P01133" % egf[0])
    print("  mature EGF: %d aa" % len(egf))
    write("egf_control.fasta", "EGF_HUMAN_mature|P01133", egf, records)

    # ---- write ---------------------------------------------------------
    print("\nRECORDS")
    print("%-30s %6s  %s" % ("file", "len", "sha256[:16]"))
    print("-" * 62)
    for fn, hdr, seq in records:
        h = hashlib.sha256(seq.encode()).hexdigest()[:16]
        print("%-30s %6d  %s" % (fn, len(seq), h))

    if DRY:
        print("\n--dry-run: nothing written")
        return

    os.makedirs(OUTDIR, exist_ok=True)
    for fn, hdr, seq in records:
        p = os.path.join(OUTDIR, fn)
        with open(p, "w") as fh:
            fh.write(">%s\n" % hdr)
            for i in range(0, len(seq), 60):
                fh.write(seq[i:i + 60] + "\n")

    # read back and compare
    for fn, hdr, seq in records:
        p = os.path.join(OUTDIR, fn)
        with open(p) as fh:
            ln = fh.read().splitlines()
        got = "".join(x.strip() for x in ln[1:])
        if got != seq:
            die("round-trip mismatch in %s" % p)

    print("\nwrote %d files to %s/ (round-trip verified)" % (len(records), OUTDIR))


if __name__ == "__main__":
    main()
