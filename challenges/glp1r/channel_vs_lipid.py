#!/usr/bin/env python3
"""Separate channel-facing surface from lipid-facing surface.

A residue can look 'exposed' in an apo calculation simply because the membrane
is absent -- i.e. its area faces lipid, not the peptide channel. Targeting such
a residue would mean designing against a surface that is covered by detergent
in the real assay.

dSASA = SASA(receptor alone) - SASA(receptor + peptide).  Area that the native
peptide actually buries is, by construction, channel-facing and available to a
competing binder. Area that stays exposed with the peptide bound is either
lipid-facing or bulk solvent.

Usage: python3 -I channel_vs_lipid.py <structure.pdb>
"""
import sys
import numpy as np
from Bio.PDB import PDBParser
from Bio.PDB.SASA import ShrakeRupley
from Bio.PDB.Polypeptide import protein_letters_3to1 as T31

CUTOFF, MESSAGE_END, ECD_MAX = 4.5, 15, 145


def one(r):
    n = r.get_resname()
    return T31.get(n.capitalize(), T31.get(n, "?"))


def sasa_of_R(path, keep):
    p = PDBParser(QUIET=True)
    m = p.get_structure("x", path)[0]
    for ch in [c.id for c in m]:
        if ch not in keep:
            m.detach_child(ch)
    ShrakeRupley().compute(m, level="R")
    return {r.id[1]: r.sasa for r in m["R"] if r.id[0] == " "}


def main(path):
    apo = sasa_of_R(path, {"R"})
    holo = sasa_of_R(path, {"R", "P"})

    m = PDBParser(QUIET=True).get_structure("s", path)[0]
    rres = {r.id[1]: r for r in m["R"] if r.id[0] == " "}
    pres = {r.id[1]: r for r in m["P"] if r.id[0] == " "}

    msg = {}
    for pnum, pr in pres.items():
        if pnum > MESSAGE_END:
            continue
        pa = np.array([a.coord for a in pr if a.element != "H"])
        for rnum, rr in rres.items():
            ra = np.array([a.coord for a in rr if a.element != "H"])
            d = np.linalg.norm(pa[:, None, :] - ra[None, :, :], axis=-1)
            n = int((d <= CUTOFF).sum())
            if n:
                msg[rnum] = msg.get(rnum, 0) + n

    print(f"{'res':<8}{'pairs':>6}{'apo':>8}{'holo':>8}{'dSASA':>8}{'%buried':>9}  verdict")
    print("-" * 70)
    keep = []
    for rnum in sorted(msg, key=lambda k: -msg[k]):
        a, h = apo.get(rnum, 0.0), holo.get(rnum, 0.0)
        d = a - h
        pct = (d / a * 100) if a > 1e-6 else 0.0
        if d >= 20 and pct >= 40:
            v = "CHANNEL (good target)"
            keep.append((rnum, msg[rnum], d))
        elif d >= 10:
            v = "channel, partial"
            keep.append((rnum, msg[rnum], d))
        elif a >= 40:
            v = "lipid/solvent-facing -- AVOID"
        else:
            v = "buried"
        print(f"{one(rres[rnum])}{rnum:<7}{msg[rnum]:>6}{a:>8.1f}{h:>8.1f}{d:>8.1f}{pct:>8.0f}%  {v}")

    keep.sort(key=lambda t: -t[2])
    print(f"\n=== channel-facing activation hotspots ({len(keep)}) ===")
    for rnum, n, d in keep:
        print(f"   {one(rres[rnum])}{rnum:<6} {n:>4} pairs  dSASA {d:>6.1f}")
    print("\n   BindCraft hotspot string (top 8 by buried area):")
    print("   " + ",".join(f"R{r}" for r, _, _ in keep[:8]))
    print("\n   NOTE: 'R306' = chain R residue 306, which is TRP306, not Arg.")


if __name__ == "__main__":
    main(sys.argv[1])
