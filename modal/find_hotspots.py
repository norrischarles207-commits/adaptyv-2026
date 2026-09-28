#!/usr/bin/env python3
"""find_hotspots.py -- structural hotspot finder, target-agnostic.

Given a target/partner complex structure, ranks the target chain's residues
by how much they contact the partner chain(s), and (optionally) flags which
of those are also evolutionarily conserved -- the combination BindCraft
hotspots should usually be picked from.

Plain local script, no Modal/GPU dependency: this is a CPU-only Biopython
NeighborSearch over a few thousand atoms, done in milliseconds. It lives in
modal/ as a companion tool to run_bindcraft.py (which it feeds hotspots
into), not because it needs Modal's infrastructure. Does not import or
modify run_bindcraft.py.

Usage
-----
    python3 modal/find_hotspots.py --pdb 1FLT --target V,W --partner X,Y

    # local file instead of an RCSB fetch
    python3 modal/find_hotspots.py --pdb ./my_complex.pdb --target A --partner B

    # with a conservation file (see --help for the two-column format)
    python3 modal/find_hotspots.py --pdb 1FLT --target V,W --partner X,Y \\
        --conservation consurf_scores.tsv --conserved-threshold 7

Requires: biopython (`pip install biopython`).
"""
from __future__ import annotations

import argparse
import csv
import os
import sys
import urllib.request
from dataclasses import dataclass, field


def fetch_or_load_pdb(pdb_arg: str, cache_dir: str) -> str:
    """Return a local path to the structure. `pdb_arg` is either an existing
    file path or a 4-character PDB ID to fetch from RCSB."""
    if os.path.exists(pdb_arg):
        return pdb_arg

    pdb_id = pdb_arg.strip().upper()
    if len(pdb_id) != 4:
        raise SystemExit(
            f"'{pdb_arg}' is neither an existing file nor a 4-character PDB ID"
        )
    os.makedirs(cache_dir, exist_ok=True)
    dest = os.path.join(cache_dir, f"{pdb_id}.pdb")
    if not os.path.exists(dest):
        url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
        print(f"fetching {url} ...", file=sys.stderr)
        urllib.request.urlretrieve(url, dest)
    return dest


@dataclass
class ResidueContact:
    chain: str
    resnum: int
    resname: str
    contact_residues: int = 0   # distinct partner residues within cutoff
    atom_pairs: int = 0         # total atom-atom pairs within cutoff (tiebreak)
    min_dist: float = field(default=float("inf"))  # closest heavy-atom contact
    conservation: float | None = None
    conserved: bool = False

    @property
    def hotspot_id(self) -> str:
        return f"{self.chain}{self.resnum}"


def find_contacts(
    structure_path: str,
    target_chains: list[str],
    partner_chains: list[str],
    cutoff: float,
) -> list[ResidueContact]:
    from Bio.PDB import NeighborSearch, PDBParser

    parser = PDBParser(QUIET=True)
    structure = parser.get_structure("target", structure_path)
    model = structure[0]

    present_chains = {c.id for c in model}
    for c in target_chains + partner_chains:
        if c not in present_chains:
            raise SystemExit(
                f"chain '{c}' not found in structure (present: {sorted(present_chains)})"
            )

    partner_atoms = [
        atom
        for chain in model
        if chain.id in partner_chains
        for residue in chain
        if residue.id[0] == " "  # skip waters/heteroatoms
        for atom in residue
    ]
    if not partner_atoms:
        raise SystemExit(f"no atoms found in partner chain(s) {partner_chains}")

    ns = NeighborSearch(partner_atoms)

    results: dict[tuple[str, int], ResidueContact] = {}
    for chain in model:
        if chain.id not in target_chains:
            continue
        for residue in chain:
            if residue.id[0] != " ":
                continue
            key = (chain.id, residue.id[1])
            rc = ResidueContact(chain.id, residue.id[1], residue.resname)
            contact_residue_keys = set()
            for atom in residue:
                for partner_atom in ns.search(atom.coord, cutoff):
                    d = atom - partner_atom
                    rc.atom_pairs += 1
                    rc.min_dist = min(rc.min_dist, d)
                    p_res = partner_atom.get_parent()
                    contact_residue_keys.add((p_res.get_parent().id, p_res.id[1]))
            rc.contact_residues = len(contact_residue_keys)
            if rc.contact_residues > 0:
                results[key] = rc

    return sorted(
        results.values(),
        key=lambda r: (-r.contact_residues, -r.atom_pairs, r.min_dist),
    )


def load_conservation(path: str) -> dict[int, float]:
    """Two-column format: resnum, score (whitespace or comma separated).
    Matches a simplified export of ConSurf's per-residue grades -- ConSurf
    itself requires an MSA-based web job, which this script does not run;
    supply its output (or any per-residue conservation score) as this file.
    """
    scores: dict[int, float] = {}
    with open(path) as fh:
        sample = fh.read(2048)
        fh.seek(0)
        delim = "," if sample.count(",") > sample.count("\t") else None
        reader = csv.reader(fh, delimiter=delim) if delim else (
            line.split() for line in fh
        )
        for row in reader:
            if not row or row[0].strip().lstrip("-").isdigit() is False:
                continue  # skip header / blank lines
            try:
                resnum = int(row[0])
                score = float(row[1])
            except (ValueError, IndexError):
                continue
            scores[resnum] = score
    if not scores:
        raise SystemExit(f"no (resnum, score) rows parsed from {path}")
    return scores


def format_table(contacts: list[ResidueContact], show_conservation: bool) -> str:
    header = f"{'residue':10s} {'resname':8s} {'contacts':>8s} {'atom_pairs':>10s} {'min_dist':>9s}"
    if show_conservation:
        header += f" {'conserv':>8s} {'flag':>6s}"
    lines = [header, "-" * len(header)]
    for rc in contacts:
        line = (
            f"{rc.hotspot_id:10s} {rc.resname:8s} {rc.contact_residues:8d} "
            f"{rc.atom_pairs:10d} {rc.min_dist:9.2f}"
        )
        if show_conservation:
            cons = f"{rc.conservation:.2f}" if rc.conservation is not None else "n/a"
            flag = "HOT" if rc.conserved else ""
            line += f" {cons:>8s} {flag:>6s}"
        lines.append(line)
    return "\n".join(lines)


def main() -> None:
    p = argparse.ArgumentParser(
        description="Rank a target chain's residues by contact with a partner "
        "chain, for picking BindCraft hotspots. Target-agnostic -- works for "
        "any PDB ID or local structure.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument("--pdb", required=True, help="PDB ID (e.g. 1FLT) or path to a local .pdb file")
    p.add_argument("--target", required=True, help="Target chain(s), comma-separated (e.g. V,W)")
    p.add_argument("--partner", required=True, help="Partner/receptor chain(s), comma-separated (e.g. X,Y)")
    p.add_argument("--cutoff", type=float, default=5.0, help="Heavy-atom contact distance cutoff, angstroms")
    p.add_argument("--top-n", type=int, default=8, help="Number of residues in the output hotspot string")
    p.add_argument("--conservation", default=None, help="Optional path to a (resnum, score) conservation file")
    p.add_argument(
        "--conserved-threshold", type=float, default=7.0,
        help="Minimum conservation score to flag a residue as conserved "
        "(default matches ConSurf's 1-9 scale, where 9 is most conserved)",
    )
    p.add_argument("--cache-dir", default="targets", help="Where to cache a fetched PDB file")
    args = p.parse_args()

    target_chains = [c.strip() for c in args.target.split(",")]
    partner_chains = [c.strip() for c in args.partner.split(",")]

    structure_path = fetch_or_load_pdb(args.pdb, args.cache_dir)
    contacts = find_contacts(structure_path, target_chains, partner_chains, args.cutoff)

    if not contacts:
        raise SystemExit(
            f"no contacts found between target {target_chains} and partner "
            f"{partner_chains} within {args.cutoff}A -- check chain IDs and cutoff"
        )

    show_conservation = args.conservation is not None
    if show_conservation:
        scores = load_conservation(args.conservation)
        missing = 0
        for rc in contacts:
            rc.conservation = scores.get(rc.resnum)
            if rc.conservation is None:
                missing += 1
            else:
                rc.conserved = rc.conservation >= args.conserved_threshold
        if missing:
            print(
                f"warning: {missing}/{len(contacts)} contact residues had no "
                f"conservation score in {args.conservation}",
                file=sys.stderr,
            )

    print(f"target chain(s) {target_chains} vs partner chain(s) {partner_chains}, "
          f"cutoff {args.cutoff}A -- {len(contacts)} contacting residues found\n")
    print(format_table(contacts, show_conservation))

    top = contacts[: args.top_n]
    hotspot_string = ",".join(rc.hotspot_id for rc in top)
    print(f"\ntop {len(top)} by contact count -- ready to paste as BindCraft hotspots:")
    print(f"  {hotspot_string}")

    if show_conservation:
        hot_and_conserved = [rc for rc in contacts if rc.conserved]
        hot_and_conserved.sort(key=lambda r: (-r.contact_residues, -r.atom_pairs))
        if hot_and_conserved:
            top_hc = hot_and_conserved[: args.top_n]
            hc_string = ",".join(rc.hotspot_id for rc in top_hc)
            print(
                f"\nhigh-contact AND conserved (>= {args.conserved_threshold}), "
                f"{len(hot_and_conserved)} total -- alternative hotspot string:"
            )
            print(f"  {hc_string}")
        else:
            print(
                f"\nno residues were both contacting and >= {args.conserved_threshold} "
                "conserved -- top-N by contact count above is the only option"
            )


if __name__ == "__main__":
    main()
