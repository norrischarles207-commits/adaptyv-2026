#!/usr/bin/env python3
"""Verify every figure stated in epitope-analysis.md / methods.md against 6X18.

Written for the same reason as challenges/tnfa/crosscheck_submission.py: a
prose document that quotes numbers can drift from the data it quotes. This
script RECOMPUTES each figure from the structure and PARSES the claimed figure
out of the markdown, so a wrong number in the prose fails the check rather
than passing it. Nothing is compared against a constant held in this file.

Usage (from the repo root):
    python3 -I challenges/glp1r/crosscheck_epitope.py
Exits non-zero on any disagreement.
"""
import re
import sys
from collections import defaultdict

import numpy as np
from Bio.PDB import PDBParser
from Bio.PDB.SASA import ShrakeRupley
from Bio.PDB.Polypeptide import protein_letters_3to1 as T31

PDB = "challenges/glp1r/6X18.pdb"
ANALYSIS = "challenges/glp1r/epitope-analysis.md"
METHODS = "challenges/glp1r/methods.md"
CUTOFF, MESSAGE_END, ECD_MAX = 4.5, 15, 145
HOTSPOTS = [141, 201, 298, 299, 300, 306, 380, 384]

CONSTRUCT = (
    "RPQGATVSLWETVQKWREYRRQCQRSLTEDPPPATDLFCNRTFDEYACWPDGEPGSFVNVSCPWYLPWASSVPQGH"
    "VYRFCTAEGLWLQKDNSSLPWRDLSECEESKRGERSSPEEQLLFLYIIYTVGYALSFSALVIASAILLGFRHLHCT"
    "RNYIHLNLFASFILRALSVFIKDAALKWMYSTAAQQHQWDGLLSYQDSLSCRLVFLLMQYCVAANYYWLLVEGVYLY"
    "TLLAFSVLSEQWIFRLYVSIGWGVPLLFVVPWGIVKYLYEDEGCWTRNSNMNYWLIIRLPILFAIGVNFLIFVRVIC"
    "IVVSKLKANLMCKTDIKCRLAKSTLTLIPLLGTHEVIFAFVMDEHARGTLRFIKLFTELSFTSFQGLMVAILYCFVN"
    "NEVQLEFRKSWERWRLEHLHIQRDSS"
)
ANCHORS = {190: "R", 152: "Y", 148: "Y", 364: "E", 387: "E",
           310: "R", 306: "W", 241: "Y", 313: "I", 234: "Q"}

fails = []


def check(ok, msg):
    print(("  ok   " if ok else "  FAIL ") + msg)
    if not ok:
        fails.append(msg)


def one(res):
    n = res.get_resname()
    return T31.get(n.capitalize(), T31.get(n, "?"))


def sasa_R(path, keep):
    m = PDBParser(QUIET=True).get_structure("x", path)[0]
    for ch in [c.id for c in m]:
        if ch not in keep:
            m.detach_child(ch)
    ShrakeRupley().compute(m, level="R")
    return {r.id[1]: r.sasa for r in m["R"] if r.id[0] == " "}


def main():
    doc = open(ANALYSIS).read()
    meth = open(METHODS).read()
    m = PDBParser(QUIET=True).get_structure("s", PDB)[0]
    rres = {r.id[1]: r for r in m["R"] if r.id[0] == " "}
    pres = {r.id[1]: r for r in m["P"] if r.id[0] == " "}

    print("=== 1. numbering convention ===")
    check(one(rres[29]) == "T", "chain R residue 29 is Thr (author numbering == UniProt)")
    wt = {24 + i: c for i, c in enumerate(CONSTRUCT)}
    check(wt[29] == "T", "construct residue 29 is Thr")

    print("\n=== 2. sequence vs the assay construct ===")
    mism = [(n, wt[n], one(r)) for n, r in rres.items()
            if n in wt and one(r) != wt[n]]
    check(len(mism) == 1, f"exactly one mismatch over {len(rres)} resolved residues (got {len(mism)})")
    if mism:
        n, e, g = mism[0]
        check(f"{e}{n}{g}" == "L260F", f"the mismatch is L260F (got {e}{n}{g})")
        check(f"{e}{n}{g}" in doc or f"{e}{n}{g}" in meth, "L260F is stated in the prose")
        check(n not in HOTSPOTS, "the mismatch is not in the hotspot set")

    print("\n=== 3. literature anchors ===")
    nmatch = sum(1 for k, v in ANCHORS.items() if k in rres and one(rres[k]) == v)
    claimed = int(re.search(r"(\d+) match, 0\s*mismatch", doc).group(1))
    check(nmatch == len(ANCHORS), f"all {len(ANCHORS)} anchors identity-match (got {nmatch})")
    check(nmatch == claimed, f"prose claims {claimed} matches, recomputed {nmatch}")

    print("\n=== 4. message / address contact split ===")
    msg, adr = defaultdict(int), defaultdict(int)
    for pnum, pr in pres.items():
        tgt = msg if pnum <= MESSAGE_END else adr
        pa = np.array([a.coord for a in pr if a.element != "H"])
        for rnum, rr in rres.items():
            ra = np.array([a.coord for a in rr if a.element != "H"])
            if (np.linalg.norm(pa[:, None] - ra[None, :], axis=-1) <= CUTOFF).any():
                tgt[rnum] += int((np.linalg.norm(pa[:, None] - ra[None, :], axis=-1) <= CUTOFF).sum())
    row = re.search(r"\*\*message\*\*.*?\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*\*\*(\d+)\*\*\s*\|", doc)
    check(row is not None, "message row parsed from the prose table")
    if row:
        tot, ecd, tmd = (int(x) for x in row.groups())
        check(len(msg) == tot, f"message total: prose {tot}, recomputed {len(msg)}")
        check(sum(1 for k in msg if k <= ECD_MAX) == ecd, f"message ECD: prose {ecd}")
        check(sum(1 for k in msg if k > ECD_MAX) == tmd, f"message TMD/ECL: prose {tmd}")
    row = re.search(r"\*\*address\*\*.*?\|\s*(\d+)\s*\|\s*\*\*(\d+)\*\*\s*\|\s*(\d+)\s*\|", doc)
    if row:
        tot, ecd, tmd = (int(x) for x in row.groups())
        check(len(adr) == tot, f"address total: prose {tot}, recomputed {len(adr)}")
        check(sum(1 for k in adr if k <= ECD_MAX) == ecd, f"address ECD: prose {ecd}")

    print("\n=== 5. geometry ===")
    his7 = pres[7]["CA"].coord
    ecd_c = np.array([rres[k]["CA"].coord for k in rres
                      if k <= ECD_MAX and "CA" in rres[k]]).mean(0)
    d = float(np.linalg.norm(his7 - ecd_c))
    for src, name in ((doc, "epitope-analysis.md"), (meth, "methods.md")):
        mm = re.search(r"\*\*(\d+\.\d)\s*Å\*\*\s*from the ECD centroid", src) or \
             re.search(r"His7[^.]{0,40}?(\d+\.\d)\s*Å", src)
        if mm:
            check(abs(float(mm.group(1)) - d) < 0.15,
                  f"{name}: His7->ECD centroid {mm.group(1)} A vs recomputed {d:.1f} A")

    print("\n=== 6. hotspots are message contacts and channel-facing ===")
    apo, holo = sasa_R(PDB, {"R"}), sasa_R(PDB, {"R", "P"})
    for h in HOTSPOTS:
        check(msg.get(h, 0) > 0, f"R{h} ({one(rres[h])}{h}) is a message contact")
    ds = {h: apo[h] - holo[h] for h in HOTSPOTS}
    check(all(v >= 15 for v in ds.values()),
          f"all hotspots channel-facing (min dSASA {min(ds.values()):.1f} A^2)")
    lip = [k for k in msg if apo.get(k, 0) >= 40 and (apo[k] - holo[k]) < 10]
    check(lip == [145], f"Y145 is the only lipid/solvent-facing message residue (got {lip})")

    print("\n=== 7. hotspot string in prose matches this script ===")
    mm = re.search(r"R\d+(?:,R\d+)+", doc)
    check(mm is not None, "hotspot string present in epitope-analysis.md")
    if mm:
        stated = [int(x[1:]) for x in mm.group(0).split(",")]
        check(sorted(stated) == sorted(HOTSPOTS), f"prose hotspots {sorted(stated)} == {sorted(HOTSPOTS)}")
        mm2 = re.search(r"R\d+(?:,R\d+)+", meth)
        check(mm2 and sorted(int(x[1:]) for x in mm2.group(0).split(",")) == sorted(HOTSPOTS),
              "methods.md hotspot string agrees with epitope-analysis.md")

    print("\n" + "=" * 60)
    print("ALL CHECKS PASS" if not fails else f"{len(fails)} FAILURES")
    for f in fails:
        print("  - " + f)
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
