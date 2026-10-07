"""TNF-alpha residues contacting its receptor, computed from coordinates.

Usage:  python3 -I tnfr_contacts.py <pdb> <ligand_chains> <receptor_chains> [cutoff]
e.g.    python3 -I tnfr_contacts.py structures/3ALQ.pdb ABCDEF RSTUVW 4.5

Reports every TNF residue with a heavy atom within <cutoff> A of any heavy atom
of a receptor chain, per TNF protomer, in mature TNF numbering (the numbering
1TNF/2TNF/3ALQ/7KPB all use).

Contacts only. No ranking, no hotspot call -- those need energetic data.
"""
import sys, collections
import numpy as np

pdb, lig_ch, rec_ch = sys.argv[1], set(sys.argv[2]), set(sys.argv[3])
cutoff = float(sys.argv[4]) if len(sys.argv) > 4 else 4.5

# 3ALQ ships a lysine-deficient TNF variant; flag any contact at these sites.
ENGINEERED = {11: "K11M", 65: "K65S", 90: "K90P", 98: "K98R",
              112: "K112N", 128: "K128P"}

atoms = collections.defaultdict(list)   # (chain,resseq,resname) -> [xyz]
for line in open(pdb, encoding="utf-8", errors="replace"):
    if not line.startswith("ATOM"):
        continue                         # ATOM only: no HETATM, no waters
    if line[76:78].strip() == "H" or line[12:16].strip().startswith("H"):
        continue                         # heavy atoms only
    if line[16] not in (" ", "A"):
        continue                         # first altloc only
    ch = line[21]
    if ch not in lig_ch and ch not in rec_ch:
        continue
    atoms[(ch, int(line[22:26]), line[17:20].strip())].append(
        (float(line[30:38]), float(line[38:46]), float(line[46:54])))

lig = {k: np.array(v) for k, v in atoms.items() if k[0] in lig_ch}
rec = {k: np.array(v) for k, v in atoms.items() if k[0] in rec_ch}
if not lig or not rec:
    sys.exit(f"ERROR: ligand atoms={len(lig)} receptor atoms={len(rec)} -- check chain IDs")

rec_xyz = np.vstack([v for v in rec.values()])
print(f"{pdb}  ligand chains {''.join(sorted(lig_ch))}  "
      f"receptor chains {''.join(sorted(rec_ch))}  cutoff {cutoff} A")
print(f"ligand residues {len(lig)}   receptor heavy atoms {len(rec_xyz)}\n")

hits = []
for (ch, num, name), xyz in lig.items():
    d = np.sqrt(((xyz[:, None, :] - rec_xyz[None, :, :]) ** 2).sum(-1))
    m = d.min()
    if m <= cutoff:
        hits.append((ch, num, name, round(float(m), 2), int((d <= cutoff).sum())))

by_chain = collections.defaultdict(list)
for h in hits:
    by_chain[h[0]].append(h)

for ch in sorted(by_chain):
    rows = sorted(by_chain[ch], key=lambda r: r[1])
    print(f"--- TNF chain {ch}: {len(rows)} contact residues ---")
    print(f"{'res':>5} {'aa':>4} {'min d':>7} {'atom pairs':>11}   note")
    for _, num, name, mind, n in rows:
        # wild-type is LYS at all six; flag only where this structure differs
        note = (f"<-- ENGINEERED HERE ({ENGINEERED[num]})"
                if num in ENGINEERED and name != "LYS" else "")
        print(f"{num:>5} {name:>4} {mind:>7} {n:>11}   {note}")
    print()

union = sorted({h[1] for h in hits})
print("=" * 62)
print(f"UNION of contact positions across all TNF chains ({len(union)}):")
print("  " + ", ".join(str(u) for u in union))
obs = {h[1]: h[2] for h in hits}
flagged = [u for u in union if u in ENGINEERED and obs.get(u) != "LYS"]
if flagged:
    print(f"\n  WARNING: {len(flagged)} contact position(s) are engineered here: "
          + ", ".join(ENGINEERED[f] for f in flagged))
    print("  Those contacts do not describe wild-type TNF-alpha.")
