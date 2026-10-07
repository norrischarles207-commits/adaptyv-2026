"""Where the receptor epitope, species conservation and histidines intersect.

Inputs are hard-coded from upstream results so this is reproducible without
re-running anything:
  - TNFR2 contacts: tnfr_contacts.py structures/3ALQ.pdb ABCDEF RSTUVW 4.5
  - TNFR1 contacts: tnfr_contacts.py structures/7KPB.pdb ABC EF 4.5
  - divergence:     tnf_align.py (human P01375 77-233 vs mouse P06804 80-235)
All numbers are mature TNF-alpha 1-157.
"""
TNFR2 = {20,21,23,31,32,33,63,67,71,72,73,75,77,85,86,87,88,89,90,91,92,97,
         111,113,115,128,137,143,144,145,146,149}
TNFR1 = {20,21,23,30,31,32,33,65,66,67,73,75,77,82,85,86,87,89,90,91,97,110,
         113,115,135,137,143,144,145,146,147,149}
FAB   = {47,63,65,67,77,79,83,88,89,90,91,92,93,94,95,96,97,98,113,115,117,
         131,133,135,136,137,138,143,145,146,149}

DIV = {1:"V>L",6:"R>Q",7:"T>N",8:"P>S",20:"P>H",22:"A>V",24:"G>E",27:"Q>E",
       30:"N>S",31:"R>Q",41:"V>M",42:"E>D",44:"R>K",52:"S>A",53:"E>D",
       58:"I>V",71:"S>D",72:"T>indel",73:"H>Y",80:"I>V",83:"I>F",85:"V>I",
       89:"T>E",97:"I>V",102:"Q>P",103:"R>K",104:"E>D",111:"A>L",131:"R>Q",
       136:"I>V",138:"R>L",140:"D>K",154:"I>V"}
CHARGE = {6,24,27,31,71,89,131,138,140}
HIS_HUMAN = {15,73,78}
ENGINEERED_3ALQ = {11,65,90,98,112,128}

both = TNFR2 & TNFR1
print(f"TNFR2 contacts {len(TNFR2)} | TNFR1 contacts {len(TNFR1)} | "
      f"shared by both receptors {len(both)}\n")

print("=" * 70)
print("CONSENSUS EPITOPE  (contacts both TNFR1 and TNFR2)")
print("=" * 70)
cons, div_hits = [], []
for r in sorted(both):
    tags = []
    if r in DIV:
        tags.append(f"DIVERGENT {DIV[r]}")
        if r in CHARGE: tags.append("charge change")
    if r in HIS_HUMAN: tags.append("human His")
    if r in ENGINEERED_3ALQ: tags.append("engineered in 3ALQ")
    if r in FAB: tags.append("in Fab1974 footprint")
    (div_hits if r in DIV else cons).append(r)
    print(f"  {r:>4}  {'; '.join(tags) if tags else 'conserved'}")

print("\n" + "=" * 70)
print("THE DECISION")
print("=" * 70)
print(f"Consensus epitope positions          : {len(both)}")
print(f"  conserved human/mouse              : {len(cons)}  <- usable surface")
print(f"  divergent                          : {len(div_hits)}  {sorted(div_hits)}")
print(f"  of those, charge changes           : {sorted(set(div_hits) & CHARGE)}")
print(f"\nCONSERVED CONSENSUS SET ({len(cons)}):\n  {sorted(cons)}")

runs, start, prev = [], None, None
for r in sorted(cons):
    if prev is None or r != prev + 1:
        if start is not None: runs.append((start, prev))
        start = r
    prev = r
runs.append((start, prev))
print("\n  contiguous stretches: " +
      ", ".join(f"{a}-{b}" if a != b else str(a) for a, b in runs))

print(f"\nTNFR2-only contacts : {sorted(TNFR2 - TNFR1)}")
print(f"TNFR1-only contacts : {sorted(TNFR1 - TNFR2)}")
print(f"\nFab1974 overlaps the consensus epitope at: {sorted(both & FAB)}")
print("  (7KPB has Fab1974 bound alongside TNFR1; overlap means the TNFR1")
print("   contact set from that structure may be perturbed at those sites.)")
