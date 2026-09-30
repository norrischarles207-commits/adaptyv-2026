# EGFR Phase 1 hotspot targets (6ARU chain A, author/mature numbering)
# Precursor equivalents: Q408, Q432, H433, Q435, F436, K489, I490
# All measured cetuximab contacts, all mouse-conserved.
# H433 (A409) is BOTH a design target AND the Phase 3 pH-switch anchor
# (native mouse-conserved histidine engaged by Liu 2022 G532 antibody).
# Reference structure: challenges/egfr/6aru.cif, chain A.

TARGET_PDB = "challenges/egfr/6aru.cif"
TARGET_CHAIN = "A"
HOTSPOTS = ["A384", "A408", "A409", "A411", "A412", "A465", "A466"]

# pH switch details for Phase 3 (not used in Phase 1 BindCraft):
# - Primary target-His anchor: A409 (H433) — already in HOTSPOTS above
# - Secondary target-His anchor: A346 (H370) — outside 4.5 A patch,
#   engaged by G532's second CDR
# - Binder-side residue: Asp or Glu, placed via ProteinMPNN in Phase 3
