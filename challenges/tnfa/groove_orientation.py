"""Which chain pair of the apo trimer forms a receptor groove, and which face
each chain presents.

In 3ALQ the two faces of one TNFR2 site are:
  face 1 (143-146, 32-33, 113, 115, 149)   -- 87% conserved
  face 2 (86, 87, 90, 91, 75, 77)          -- 60% conserved
A groove exists where one chain's face-1 residues sit against another chain's
face-2 residues. Checks every ordered chain pair.

Usage: python3 -I groove_orientation.py <pdb> <chains>
"""
import sys, collections, itertools
import numpy as np

pdb, chains = sys.argv[1], list(sys.argv[2])
FACE1 = [143, 144, 145, 146, 32, 33, 113, 115, 149]
FACE2 = [86, 87, 90, 91, 75, 77]

at = collections.defaultdict(list)
for line in open(pdb, encoding="utf-8", errors="replace"):
    if not line.startswith("ATOM"):
        continue
    if line[76:78].strip() == "H" or line[12:16].strip().startswith("H"):
        continue
    if line[16] not in (" ", "A"):
        continue
    if line[21] in chains:
        at[(line[21], int(line[22:26]))].append(
            (float(line[30:38]), float(line[38:46]), float(line[46:54])))

def face_xyz(ch, nums):
    pts = [p for n in nums for p in at.get((ch, n), [])]
    return np.array(pts) if pts else None

print(f"{pdb}  chains {''.join(chains)}\n")
print(f"{'pair':>8}  {'min dist':>9}  {'<5A pairs':>10}   reading")
rows = []
for a, b in itertools.permutations(chains, 2):
    f1, f2 = face_xyz(a, FACE1), face_xyz(b, FACE2)
    if f1 is None or f2 is None:
        continue
    d = np.sqrt(((f1[:, None, :] - f2[None, :, :]) ** 2).sum(-1))
    rows.append((a, b, float(d.min()), int((d <= 5.0).sum())))

for a, b, mind, n in sorted(rows, key=lambda r: r[2]):
    verdict = "GROOVE" if mind < 6 else ""
    print(f"  {a}->{b}  {mind:>9.2f}  {n:>10}   {verdict}")

best = min(rows, key=lambda r: r[2])
print(f"\nClosest: chain {best[0]} presents face 1 (conserved, 143-146) and "
      f"chain {best[1]} presents face 2 (86/87).")
print(f"So a two-chain target of {best[0]}+{best[1]} contains one complete "
      f"receptor site,\nwith hotspots prefixed {best[0]} for face-1 residues "
      f"and {best[1]} for face-2.")
