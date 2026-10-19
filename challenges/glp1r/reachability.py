#!/usr/bin/env python3
"""Which GLP1R activation-epitope residues are actually reachable by a soluble binder?

Two measures, both on the receptor with the peptide and G protein REMOVED
(i.e. the surface a designed binder would actually see):

  depth  - position along the extracellular<->intracellular axis, defined by the
           vector from the Galpha centroid (intracellular) to the ECD centroid
           (extracellular). Higher = more extracellular = more accessible.
  SASA   - Shrake-Rupley solvent accessible surface area of the residue in the
           apo receptor. A pocket-lining residue that is buried once the peptide
           is gone cannot be gripped from outside.

Usage: python3 -I reachability.py <structure.pdb>
"""
import sys
from collections import defaultdict
import numpy as np
from Bio.PDB import PDBParser
from Bio.PDB.SASA import ShrakeRupley
from Bio.PDB.Polypeptide import protein_letters_3to1 as T31

CUTOFF, MESSAGE_END, ECD_MAX = 4.5, 15, 145


def one(res):
    n = res.get_resname()
    return T31.get(n.capitalize(), T31.get(n, "?"))


def main(path):
    p = PDBParser(QUIET=True)
    m = p.get_structure("s", path)[0]
    R, P, A = m["R"], m["P"], m["A"]
    rres = {r.id[1]: r for r in R if r.id[0] == " "}
    pres = {r.id[1]: r for r in P if r.id[0] == " "}

    # --- contacts, split message/address ------------------------------------
    msg, adr = defaultdict(int), defaultdict(int)
    for pnum, pr in pres.items():
        tgt = msg if pnum <= MESSAGE_END else adr
        pa = np.array([a.coord for a in pr if a.element != "H"])
        for rnum, rr in rres.items():
            ra = np.array([a.coord for a in rr if a.element != "H"])
            d = np.linalg.norm(pa[:, None, :] - ra[None, :, :], axis=-1)
            n = int((d <= CUTOFF).sum())
            if n:
                tgt[rnum] += n

    # --- axis: Galpha centroid (in) -> ECD centroid (out) -------------------
    ga = np.array([a.coord for a in A.get_atoms() if a.element != "H"]).mean(0)
    ecd = np.array([rres[k]["CA"].coord for k in rres
                    if k <= ECD_MAX and "CA" in rres[k]]).mean(0)
    axis = ecd - ga
    axis /= np.linalg.norm(axis)

    # membrane reference: project all TM-region CAs, call the extracellular
    # boundary the 90th percentile of the TM bundle (approximate but consistent)
    tm = [rres[k]["CA"].coord for k in rres if k > ECD_MAX and "CA" in rres[k]]
    tm_proj = np.array([np.dot(c - ga, axis) for c in tm])
    outer = np.percentile(tm_proj, 90)

    # --- SASA on the APO receptor (peptide + G protein stripped) ------------
    apo = p.get_structure("apo", path)[0]
    for ch in [c.id for c in apo]:
        if ch != "R":
            apo.detach_child(ch)
    ShrakeRupley().compute(apo, level="R")
    sasa = {r.id[1]: r.sasa for r in apo["R"] if r.id[0] == " "}

    print(f"{'res':<8}{'role':<10}{'pairs':>6}{'depth':>8}{'vs_outer':>10}{'SASA':>8}  verdict")
    print("-" * 74)
    rows = []
    allhits = set(msg) | set(adr)
    for rnum in sorted(allhits, key=lambda k: -(msg.get(k, 0))):
        role = "message" if msg.get(rnum, 0) >= adr.get(rnum, 0) else "address"
        if msg.get(rnum) and adr.get(rnum):
            role = "both"
        ca = rres[rnum]["CA"].coord
        d = np.dot(ca - ga, axis)
        rel = d - outer                      # >0 above the bundle top
        s = sasa.get(rnum, 0.0)
        if s >= 40:
            v = "exposed"
        elif s >= 15:
            v = "partial"
        else:
            v = "BURIED"
        rows.append((rnum, role, msg.get(rnum, 0), d, rel, s, v))

    for rnum, role, n, d, rel, s, v in rows:
        if role == "address" and n == 0:
            continue
        print(f"{one(rres[rnum])}{rnum:<7}{role:<10}{n:>6}{d:>8.1f}{rel:>+10.1f}{s:>8.1f}  {v}")

    print("\n=== reachable activation surface (message contact, SASA >= 15 A^2) ===")
    good = [(r, n, s) for r, role, n, d, rel, s, v in rows
            if n > 0 and s >= 15]
    good.sort(key=lambda t: -t[1])
    for r, n, s in good:
        print(f"   {one(rres[r])}{r:<6} {n:>4} pairs  SASA {s:>6.1f}")
    print(f"\n   count: {len(good)} of {len([r for r in rows if r[2] > 0])} message residues")
    print("   hotspot string:", ",".join(f"R{r}" for r, _, _ in good[:10]))

    print("\n=== buried message residues (cannot be gripped from solvent) ===")
    bad = [(r, n, s) for r, role, n, d, rel, s, v in rows if n > 0 and s < 15]
    bad.sort(key=lambda t: -t[1])
    print("  ", ", ".join(f"{one(rres[r])}{r}({s:.0f})" for r, n, s in bad) or "  none")


if __name__ == "__main__":
    main(sys.argv[1])
