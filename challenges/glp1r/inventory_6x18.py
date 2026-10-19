#!/usr/bin/env python3
"""Inventory a PDB: chains, lengths, author numbering ranges, sequences.

Usage: python3 -I inventory_6x18.py <path/to/structure.pdb>
Reads the structure as data only; nothing is executed from its directory.
"""
import sys
from Bio.PDB import PDBParser

AA3 = {
    "ALA": "A", "ARG": "R", "ASN": "N", "ASP": "D", "CYS": "C", "GLN": "Q",
    "GLU": "E", "GLY": "G", "HIS": "H", "ILE": "I", "LEU": "L", "LYS": "K",
    "MET": "M", "PHE": "F", "PRO": "P", "SER": "S", "THR": "T", "TRP": "W",
    "TYR": "Y", "VAL": "V", "MSE": "M", "SEP": "S", "TPO": "T",
}


def main(path):
    st = PDBParser(QUIET=True).get_structure("s", path)
    models = list(st)
    print(f"models: {len(models)}")
    m = models[0]
    print(f"{'chain':<6}{'nres':>6}{'first':>8}{'last':>8}  {'gaps':>5}  sequence (first 60)")
    print("-" * 100)
    for ch in m:
        res = [r for r in ch if r.id[0] == " " and r.get_resname() in AA3]
        if not res:
            het = [r.get_resname() for r in ch if r.id[0] != " "]
            print(f"{ch.id:<6}{0:>6}{'-':>8}{'-':>8}  {'-':>5}  (non-polymer: {sorted(set(het))[:6]})")
            continue
        nums = [r.id[1] for r in res]
        seq = "".join(AA3.get(r.get_resname(), "X") for r in res)
        # count numbering discontinuities (unresolved stretches)
        gaps = sum(1 for a, b in zip(nums, nums[1:]) if b != a + 1)
        print(f"{ch.id:<6}{len(res):>6}{nums[0]:>8}{nums[-1]:>8}  {gaps:>5}  {seq[:60]}")


if __name__ == "__main__":
    main(sys.argv[1])
