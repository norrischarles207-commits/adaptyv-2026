#!/usr/bin/env python3
"""Map the GLP1R activation epitope from 6X18.

Splits the bound GLP-1 peptide into its 'message' (N-terminal, drives
activation) and 'address' (C-terminal, drives affinity) halves and reports
which receptor residues each one touches.

Usage: python3 -I epitope_6x18.py <structure.pdb> <construct.fasta-seq-or-->
"""
import sys
from collections import defaultdict
import numpy as np
from Bio.PDB import PDBParser

CUTOFF = 4.5          # heavy-atom contact, same convention as the TNF-a work
MESSAGE_END = 15      # GLP-1 7..15 = message; 16..36 = address
ECD_MAX = 145         # approx. end of the extracellular domain

# literature anchors (UniProt numbering) with expected identity
ANCHORS = {
    190: "R", 152: "Y", 148: "Y", 364: "E", 387: "E",
    310: "R", 306: "W", 241: "Y", 313: "I", 234: "Q",
}


def heavy(res):
    return [a for a in res if a.element != "H"]


def main(path):
    st = PDBParser(QUIET=True).get_structure("s", path)
    m = st[0]
    R, P = m["R"], m["P"]
    rres = {r.id[1]: r for r in R if r.id[0] == " "}
    pres = {r.id[1]: r for r in P if r.id[0] == " "}

    print("=== 1. literature anchor verification (expected vs 6X18 chain R) ===")
    from Bio.PDB.Polypeptide import protein_letters_3to1 as T31
    ok = bad = miss = 0
    for num, exp in sorted(ANCHORS.items()):
        if num not in rres:
            print(f"  {exp}{num}: NOT RESOLVED in 6X18")
            miss += 1
            continue
        got = T31.get(rres[num].get_resname().capitalize(),
                      T31.get(rres[num].get_resname(), "?"))
        mark = "OK " if got == exp else "MISMATCH"
        if got == exp:
            ok += 1
        else:
            bad += 1
        print(f"  {exp}{num}: 6X18 has {got}{num}  [{mark}]")
    print(f"  -> {ok} match, {bad} mismatch, {miss} unresolved")

    print("\n=== 2. peptide contacts on the receptor (heavy atom <= 4.5 A) ===")
    msg_hits, adr_hits = defaultdict(int), defaultdict(int)
    for pnum, pr in sorted(pres.items()):
        tgt = msg_hits if pnum <= MESSAGE_END else adr_hits
        pa = np.array([a.coord for a in heavy(pr)])
        for rnum, rr in rres.items():
            ra = np.array([a.coord for a in heavy(rr)])
            d = np.linalg.norm(pa[:, None, :] - ra[None, :, :], axis=-1)
            n = int((d <= CUTOFF).sum())
            if n:
                tgt[rnum] += n

    def show(title, hits, limit=24):
        print(f"\n-- {title}: {len(hits)} receptor residues --")
        for rnum, n in sorted(hits.items(), key=lambda kv: -kv[1])[:limit]:
            aa = T31.get(rres[rnum].get_resname().capitalize(),
                         T31.get(rres[rnum].get_resname(), "?"))
            dom = "ECD" if rnum <= ECD_MAX else "TMD/ECL"
            star = " <-- anchor" if rnum in ANCHORS else ""
            print(f"   {aa}{rnum:<5} {n:>4} atom-pairs   {dom}{star}")

    show(f"MESSAGE (GLP-1 7-{MESSAGE_END}) -> ACTIVATION epitope", msg_hits)
    show(f"ADDRESS (GLP-1 {MESSAGE_END+1}-36) -> affinity epitope", adr_hits)

    print("\n=== 3. domain split ===")
    for nm, hits in (("message", msg_hits), ("address", adr_hits)):
        ecd = sum(1 for k in hits if k <= ECD_MAX)
        tmd = sum(1 for k in hits if k > ECD_MAX)
        print(f"  {nm:<8} ECD:{ecd:>3}  TMD/ECL:{tmd:>3}")

    print("\n=== 4. geometry: how far the message reaches ===")
    his7 = pres[7]["CA"].coord
    ecd_ca = np.array([rres[k]["CA"].coord for k in rres
                       if k <= ECD_MAX and "CA" in rres[k]])
    adr_ca = np.array([rres[k]["CA"].coord for k in adr_hits
                       if "CA" in rres[k]])
    print(f"  His7 CA -> ECD centroid:            {np.linalg.norm(his7 - ecd_ca.mean(0)):.1f} A")
    print(f"  His7 CA -> address-epitope centroid:{np.linalg.norm(his7 - adr_ca.mean(0)):.1f} A")
    deep = max(msg_hits, key=lambda k: np.linalg.norm(rres[k]["CA"].coord - ecd_ca.mean(0)))
    print(f"  deepest message contact: residue {deep} "
          f"({np.linalg.norm(rres[deep]['CA'].coord - ecd_ca.mean(0)):.1f} A from ECD centroid)")

    print("\n=== 5. candidate BindCraft hotspot strings (chain R) ===")
    for nm, hits, k in (("activation-only", msg_hits, 8),
                        ("activation+rim", {**msg_hits, **{a: b for a, b in adr_hits.items() if a > ECD_MAX}}, 10)):
        top = [f"R{n}" for n, _ in sorted(hits.items(), key=lambda kv: -kv[1])[:k]]
        print(f"  {nm:<16} {','.join(top)}")


if __name__ == "__main__":
    main(sys.argv[1])
