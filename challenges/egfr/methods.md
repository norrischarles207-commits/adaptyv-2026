# EGFR — methods log

Append-only historical log, one dated entry per run or pass (see `../README.md`). Entries are never rewritten. The design-run entries from `brief.md` ("Methods-log seed") have not been added yet; this file starts with the literature pass.

---

## 2026-09-28 — Literature pass (M. lit review)

Files: `lit/hand-back.md` (structured hand-back plus post-review addendum), `lit/epitope-verification.md`, `lit/ph-strategy-notes.md`, `lit/precedent-adaptyv-egfr.md`, `lit/sources.md`. All residue numbers are precursor / UniProt P00533 numbering. Most primary pages were blocked; numbers marked "summarizer" were read through a page summarizer and none were checked against a downloaded PDF. This pass does not edit `brief.md`; where it disagrees with the brief the conflicts are raised in the PR.

What changed vs the working brief (five points; detail in the `lit/` files):

(1) The measured 24-residue patch is consistent with the Li (1YY9) and Sickmier (5SX4/5SX5) contact lists and 17 of 24 residues are mouse-conserved (our P00533 vs Q01279 alignment); N444 is an optional add and domain III identity is 87.3%, not 92% (BLOSUM62 similarity 93.1%), while the 6ARU author range "4–612, mature" remains unverified beyond sequence-identity checks. (2) The only EGFR acid-preferring precedent, antibody G532 (Liu 2022; WO2024109709A1, both summarizer-read), pairs binder Asp/Glu with EGFR histidines H433 and H370 (precursor numbering confirmed), the reverse of the brief's binder-His / E496 anchor; FcRn–Fc supports the brief's direction, so both are literature-supported and neither has been compared on EGFR. (3) The brief's 3.7–7.6 Å His placement window comes from His-to-cation distances in one acid-releasing design of bioRxiv 2025.09.29.678932, not a His-to-carboxylate rule (none was found), and realistic monovalent selectivity at pH 6.5 vs 7.4 is about 2–10x (G532: 13.26 human, 3.31 mouse), so the mouse and pH objectives may trade off. (4) In Adaptyv's prior round the 82 nM best de novo KD is Round 2 (Round 1 was 491 nM), the strict de novo hit rate is about 6% (12 of 206, our heuristic on github.com/adaptyvbio/egfr_competition_2), and ipTM is a weak filter (AUC 0.64–0.67) that does not rank affinity, while ipSAE and shape complementarity were never analysed and the epitope of the 82 nM binder is not stated. (5) Open for the team: choose the pH anchor(s), test ipSAE_min plus shape complementarity on the released AF2 structures and neutralisation data (unreachable from our sandbox), and confirm the 6ARU range from the mmCIF.

---

## 2026-09-29 — Literature pass follow-ups

Corrections and additions to the 2026-09-28 entry (see `lit/hand-back.md`, Addendum 2): Liu 2022 lists six EGFR interface residues and five of them (H433, R377, L406, Q435, K489) are in the measured 24, not four; that overlap is expected because the G5V2 model was docked on the cetuximab 1YY9 template, so it is not independent evidence. G532 is G5V2 Y32E plus unspecified HCDR2 mutations (paper, summarizer-read), not Y32E alone. Whether EGFR is among the 15 targets of the Overath 2025 ipSAE_min meta-analysis is unresolved (Table 1 unreachable; Zenodo 15722219 `final_dataset.csv` would answer it). The Round 2 BLI assay pH remains unstated in every source we could read.

---

## 2026-09-29 — Phase 1 probe runs, full-length validation, structural measurements

Covers: the v3 AF2 OOM and the domain III slicer that fixed it, the v3b probe run and
its two accepted designs, an independent full-length co-fold check of both, and a
geometry pass over 6ARU / 3NJP / 1NQL that motivates the v3c two-arm hotspot split.

Every number below was measured in this session unless it is explicitly attributed to
the literature pass. Geometry was computed with Biopython (Shrake-Rupley SASA,
`NeighborSearch` for contacts) on the deposited coordinates; scripts were run
ad hoc and are not checked in. Values are quoted as measured, not rounded.

### 1. NUMBERING

**Offset: precursor = mature + 24.** UniProt P00533 is a 1210-residue precursor with a
24-residue signal peptide; mature numbering drops it.

Verified three independent ways, not assumed:

- **Hotspot identity match.** All seven v3 hotspots have the expected residue identity
  at mature = precursor − 24: precursor 408→mature 384 GLN, 432→408 GLN, 433→409 HIS,
  435→411 GLN, 436→412 PHE, 489→465 LYS, 490→466 ILE. The 433→409 HIS match is the
  load-bearing one — it confirms the H433 pH anchor in `f596f6f` is mature H409.
- **Whole-chain sequence identity.** 6ARU chain A SEQRES is 622 aa; stripping the
  trailing `HHHHHH` purification tag leaves 616 aa = mature 1-616 = precursor 25-640.
  That matches P00533 precursor 25-640 exactly except at two positions, **N540K and
  E634R** (precursor numbering), both far from the 408-490 epitope region.
- **SEQRES ↔ author numbering.** `SEQRES[i-1]` equals author residue `i` for **0
  mismatches over all 609 observed residues**. This closes the open item raised in the
  2026-09-28 lit entry ("the 6ARU author range 4–612, mature remains unverified beyond
  sequence-identity checks") — chain A observed span is **mature 4-612, 609 standard
  residues**, i.e. precursor 28-636.

**Which convention each artifact uses:**

| Artifact | Convention | Note |
|---|---|---|
| 6ARU deposited coords (`6aru.cif`) | **mature** | author/`auth_seq_id`; observed 4-612 |
| 3NJP, 1NQL deposited coords | **mature** | same as 6ARU, offset +0 (below) |
| Challenge spec / Adaptyv brief | **precursor** | P00533, e.g. H433, E496 |
| Literature (`lit/`, Liu 2022, patent) | **precursor** | per the lit-pass header |
| Pipeline `--hotspots` strings | **mature** | must match the loaded PDB's numbering |
| Pipeline `--target-residue-range` | **mature** | 311-514 = precursor 335-538 |
| BindCraft output complex PDBs | **renumbered 1-N** | see the trap below |
| Boltz co-fold output chain A | **1-621** | precursor = i + 24 |

**Trap, recorded because it produced a wrong result once.** The slicer writes
`egfr.pdb` preserving mature numbering (311-514), but **BindCraft renumbers the target
to 1-204 in the complex PDB it writes**. Mapping contacts with the input numbering gave
a spurious "0/7 hotspots contacted". The correct map for v3b accepted designs is
**precursor = 334 + slice index**, verified by 204/204 exact residue-identity matches
against P00533. For the Boltz full-length co-folds the map is precursor = chain-A index
+ 24, verified at **0/621 mismatches in both predictions**.

**All three structures share mature numbering, offset +0.** Established by scanning
offsets −30…+30 and taking the one maximising global sequence identity over shared
numbering, then confirming the ±10 window around 409 and requiring the mapped residue
to be HIS:

| Structure | chain | offset | shared | global identity | ±10 window | res @409 |
|---|---|---|---|---|---|---|
| 6ARU | A | +0 | 609 | 1.000 | 1.000 | 409 H |
| 3NJP | A | +0 | 609 | 0.998 | 1.000 | 409 H |
| 3NJP | B | +0 | 609 | 0.998 | 1.000 | 409 H |
| 1NQL | A | +0 | 609 | 0.998 | 1.000 | 409 H |

Convention: `6ARU_number = target_number + offset`. No renumbering was needed between
the three; this was confirmed by alignment, not inferred from a His happening to sit at
409.

### 2. EPITOPE DERIVATION

**The cetuximab contact patch, measured from 6ARU.** Chain A residues with any heavy
atom within 4.5 Å of the Fab (chains B+C): **24 residues**, independently reproducing
the count in the lit pass. Mature numbering, span 349-473 (precursor 373-497):

```
349P 350V 353R 382L 384Q 408Q 409H 411Q 412F 415A 417V 418S
438I 440S 441G 443K 465K 466I 467I 468S 469N 471G 472E 473N
```

Split by Fab chain — light chain B contacts 10, heavy chain C contacts 19:

- **C (heavy) only:** 349P 350V 353R 382L 384Q 408Q 409H 411Q 412F 415A 417V 418S 438I 440S
- **B (light) only:** 466I 469N 471G 472E 473N
- **both:** 441G 443K 465K 467I 468S

**All 7 of the v3 hotspots are cetuximab contacts (7/7).** The epitope choice is
therefore anchored on measured Fab contacts, not inference.

**Hotspot set history**

| Version | Hotspots | Change and reason |
|---|---|---|
| **v3** | `A384,A408,A409,A411,A412,A465,A466` | Conserved cetuximab core + H409 (precursor H433) as the pH anchor. All 7 verified as Fab contacts. |
| **v3b** | same | No hotspot change. Added `--target-residue-range 311-514` (domain III) after AF2 OOM'd on the full 609-residue ECD — see §9. |
| **v3c** | two arms, §7 | A466 and A465 dropped; set split into a 4-residue core and a 5-residue variant. |

**Why A466 was dropped.** Never contacted by any design produced so far. In the
full-length co-fold of seed 1 its closest heavy-atom approach to the binder is
**8.65 Å** (seed 6: 7.68 Å) — not a borderline miss. It was also uncontacted at design
time on the domain III slice, so both accepted designs scored 6/7 rather than 7/7 with
A466 as the sole miss. A hotspot no design will touch adds nothing to the restraint.

**Why A465 was dropped.** It is the route by which the mouse-divergent positions enter
the patch. With A465 present (SET3), **I467 is in-patch at 3.85 Å and S468 at 7.32 Å**
(criterion in §3). Removing A465 pushes both out: against the 5-residue set I467 is
8.53 Å and S468 12.66 Å, and against the 4-residue core 8.53 Å and 13.08 Å. Since
mouse cross-reactivity is an objective, steering the interface away from divergent
positions is worth more than the extra contact.

### 3. STRUCTURAL MEASUREMENTS

All SASA below is **chain A alone — free-receptor exposure**, with the Fab, glycans and
waters excluded. This matters: see §5 for how much drops in the complexes. Relative
SASA uses a Gly-X-Gly reference built computationally from each residue's own observed
backbone and rotamer (flanking residues stripped to backbone), not a published table.

**Histidines**

| Res | SC SASA | GlyXGly ref | rel SC | total | ring↔surface normal | direction |
|---|---|---|---|---|---|---|
| **H409** (precursor H433) | 99.1 Å² | 147.1 Å² | **0.67** | 145.1 Å² | 72.8° | ALONG |
| **H346** (precursor H370) | 30.0 Å² | 145.8 Å² | **0.21** | 30.0 Å² | 93.7° | ALONG |

H346 is largely buried — about a third the relative exposure of H409, and its backbone
is fully occluded (total SASA equals side-chain SASA). Both imidazoles lie *along* the
surface rather than projecting out of it. This bears directly on lit-pass point (2):
Liu 2022 pairs binder acid with **both** H433 and H370, but H370/H346 is poorly
accessible on the free receptor.

**H409 ↔ H346 geometry** — they are on the same face but too far apart to act as a
coupled pair:

| Measurement | Value |
|---|---|
| CA-CA | 12.84 Å |
| closest heavy-atom approach | 7.72 Å (409 N ↔ 346 NE2) |
| **ring-to-ring closest approach** | **8.52 Å** |
| ring-centroid separation | 9.73 Å |
| imidazole interplanar angle | 77.8° |
| angle between surface normals | 47.7° → **same exposed face** (<60°) |

**Patch spans, centroids, planarity, curvature**

| Set | Members | Max span | Centroid RMS | Plane RMS | H (/Å) | \|1/H\| | Shape |
|---|---|---|---|---|---|---|---|
| 4-res core | 408,409,411,412 | **6.93 Å** (409-412) | **3.14 Å** | **0.45 Å** | −0.02069 | 48.3 Å | flat (see below) |
| 5-res | 384,408,409,411,412 | 15.77 Å (384-411) | 6.12 Å | 0.96 Å | **+0.08311** | 12.0 Å | **CONCAVE** |
| SET3 | 384,408,409,411,412,465 | 15.77 Å (384-411) | 7.20 Å | 1.34 Å | +0.03320 | 30.1 Å | not resolvable |
| SET4 | 346,384,408,409,411,412 | 15.77 Å (384-411) | 6.71 Å | 1.86 Å | −0.06558 | 15.2 Å | **CONVEX** |

CA centroids: 4-res (33.35, 31.35, 63.25); 5-res (35.12, 33.16, 62.24);
SET3 (34.04, 34.79, 62.78); SET4 (36.11, 33.23, 60.91).

**Curvature method and its noise floor.** A 6-parameter quadric cannot be fitted to 4-6
CA points (exactly determined or underdetermined, zero residual, meaningless), so
curvature is fitted to the **solvent-exposed heavy atoms** (SASA > 1 Å²) of the patch
residues, with z along the outward normal so H>0 is concave. Resolvability test:
compare the predicted sag `|H|·r²/2` over the patch radius against the quadric fit RMS.

| Set | r | \|H\| | sag | fit RMS | resolvable? |
|---|---|---|---|---|---|
| 4-res | 3.5 Å | 0.02069 | 0.13 Å | 1.68 Å | **NO** — 13× below noise |
| 5-res | 7.9 Å | 0.08311 | 2.59 Å | 1.77 Å | yes |
| SET3 | 7.9 Å | 0.03320 | 1.04 Å | 1.82 Å | **NO** |
| SET4 | 7.9 Å | 0.06558 | 2.05 Å | 1.91 Å | yes |

**Correction to an earlier statement in this session.** SET3 was first reported as
"mildly concave at 30 Å radius". That is **not supported**: its sag (1.04 Å) is below
its own fit RMS (1.82 Å). SET3 should be treated as **flat**, as should the 4-residue
core, whose nominal "convex" sign is arbitrary. Only the 5-residue set and SET4 have
resolvable curvature. Signs were stable to atom selection (an all-heavy-atom fit gave
+0.0696 for SET3 and −0.0145 for SET4, same signs), so it is the *magnitude*, not the
direction, that fails the noise test.

**Neither 6-residue set is one compact patch.** Nearest-neighbour CA distance within
each set: the core is tight (408↔409 = 3.80 Å, 411↔412 = 3.80 Å) but **A384 is 12.29 Å
from its nearest set member and A465 is 10.10 Å** — two detached satellites, which is
what inflates the centroid RMS to 7.20 Å. In SET4, A346 sits 7.95 Å from A384 and
bridges the gap, lowering the RMS to 6.71 Å.

**H409's local environment is unusually sparse.** Residues with CA within 10 Å of the
H409 CA: only **8**, and they are purely its own sequence neighbours 406-413 — no
tertiary contacts at all. Within 12 Å: 17 residues (344, 379, 380, 382, 404, 406-415,
435, 436). H409 sits on a protruding loop tip.

**Mouse-divergent positions** (criterion: **in-patch = minHD ≤ 8 Å AND normal angle
< 90° AND solvent exposed**; minHD is closest heavy-atom distance to any patch member):

| Res | rel SASA | vs SET3 | vs 5-res | vs 4-res core |
|---|---|---|---|---|
| **467 I** | 0.55 SC | **3.85 Å → IN** | 8.53 Å → out | 8.53 Å → out |
| **468 S** | 0.83 SC | **7.32 Å → IN** | 12.66 Å → out | 13.08 Å → out |
| 471 G | 0.39 total | 13.53 Å → out | 18.54 Å → out | 20.19 Å → out |
| 473 N | 0.93 SC | 15.72 Å → out | 23.13 Å → out | 23.13 Å → out |

Gly471 has no side chain, so it is reported on a total-residue basis. A first attempt
at "contiguous patch" used a 5 Å connectivity graph over all exposed residues; that
percolates across the whole surface (395-residue component) and called everything
contiguous, so it was discarded in favour of the local criterion above.

**Acidic residues near H409 and near the patch.** Only three ASP and no GLU lie within
14 Å of the H409 imidazole (ring atoms CG/ND1/CD2/CE1/NE2):

| Res | dist to imidazole | rel SC | carboxylate vs normal | minHD → 5-res | in-patch |
|---|---|---|---|---|---|
| **D436** | 10.24 Å | 0.30 | 27.6° **OUT** | 3.00 Å (411) | YES |
| **D344** | 10.58 Å | 0.19 | 95.1° ALONG | 6.05 Å (408) | YES (face 88.7°, marginal) |
| D434 | 13.54 Å | 0.43 | 47.4° ALONG | 5.84 Å (412) | YES |

Nearest *carboxyl oxygen* to the imidazole: D344 10.58 Å, D436 10.68 Å, D434 14.31 Å,
D323 16.07 Å, D355 17.98 Å. Other exposed acids (rel SASA > 0.3) within 20 Å of the
5-res centroid: **E431** (0.57, carboxylate 125.0° **IN**, minHD 11.56 Å, out),
**D323** (0.83, 23.9° OUT, minHD 14.37 Å, out), **E400** (0.64, 131.7° **IN**,
minHD 14.78 Å, out). E431 and E400 look exposed on side-chain SASA but their
carboxylates point *into* the protein, so the functional group is unavailable.

D436 is the only well-oriented acid in the patch: outward carboxylate, same face
(47.7°), and genuine contact distance (3.00 Å to Q411, 3.38 Å to F412).

### 4. GLYCOSYLATION

**Sequon inventory.** 11 N-X-S/T sequons (X ≠ Pro) in chain A, derived from the SEQRES
construct (so gaps in observed density cannot create or hide one); all 11 are observed
in the coordinates. Distances are closest heavy atom to the 5-residue patch centroid:

| Asn | motif | d to centroid | within 25 Å |
|---|---|---|---|
| 104 | NKT | 70.26 Å | no |
| 151 | NMS | 71.08 Å | no |
| 172 | NGS | 87.40 Å | no |
| **328** | NAT | **17.93 Å** | YES |
| **337** | NCT | 24.83 Å | YES |
| **389** | NRT | 24.16 Å | YES |
| **420** | NIT | **18.77 Å** | YES |
| 504 | NVS | 36.01 Å | no |
| 544 | NIT | 53.87 Å | no |
| 579 | NNT | 65.87 Å | no |
| 599 | NCT | 75.51 Å | no |

The four within 25 Å, with per-member distances:

| Asn | motif | rel SC | →384 | →408 | →409 | →411 | →412 | side chain points |
|---|---|---|---|---|---|---|---|---|
| 328 | NAT | 0.19 | **11.89** | 14.99 | 18.44 | 21.87 | 18.51 | LATERAL (96.5°) |
| 337 | NCT | 0.70 | 21.47 | 23.42 | 26.22 | 26.66 | 22.90 | AWAY (167.3°) |
| 389 | NRT | 0.84 | 12.33 | 21.59 | 25.12 | 27.50 | 23.95 | LATERAL (119.6°) |
| **420** | NIT | 0.32 | **7.76** | 16.58 | 19.62 | 21.83 | 18.28 | AWAY (163.1°) |

**Key finding: every sequon reaches the patch only through A384.** N420 is the closest
at 7.76 Å from A384, and the **408-412 core is ≥ 14.99 Å from any sequon Asn** (the
minimum being N328→A408). The glycan liability is therefore a property of A384
specifically, not of the core.

**Carbohydrate present.** 13 carbohydrate residues, traced to their root Asn by actual
bond distance (≤1.8 Å), not nearest-neighbour guessing — a first pass using
nearest-ASN wrongly split the chain-D octasaccharide across three different residues.

| Root Asn | tree | first-NAG distance to patch | nearest member |
|---|---|---|---|
| **A/ASN328** | 8 sugars (chain D: NAG1-2, BMA3, MAN4-8) | **11.93 Å** | 384 |
| **A/ASN420** | 2 sugars (chain E: NAG1-2) | **13.15 Å** | 384 |
| A/ASN389 | 1 sugar (A NAG710) | 16.66 Å | 384 |
| A/ASN337 | 1 sugar (A NAG709) | 25.11 Å | 384 |
| C/ASN88 | 1 sugar (C NAG301) | 30.13 Å | 384 (Fab glycan) |

Closest carbohydrate atom to the patch is **D/NAG1 at 11.93 Å**. The closest any sugar
atom comes to the *core* is 16.79 Å (MAN4, nearest member 409). Note both nearest
glycans again arrive via A384.

### 5. LIGAND OVERLAP

H409's 0.67 relative exposure is a **free-receptor** figure. In complex it is buried in
every structure measured except one. Burial attributed per chain:

| Structure | chain A alone | with partner | buries | closest approach | rel SC alone → complex |
|---|---|---|---|---|---|
| **6ARU** (cetuximab Fab) | 99.1 Å² | 26.3 Å² | **72.8 Å² by chain C** (heavy) | 3.47 Å | 0.67 → **0.18** |
| 6ARU | — | 99.1 Å² | 0.0 Å² by chain B (light) | 13.52 Å | — |
| **3NJP A** (EGF) | 104.8 Å² | 17.0 Å² | **87.8 Å² by chain C** (EGF) | 3.10 Å | 0.70 → **0.11** |
| **3NJP B** (EGF) | 108.1 Å² | 15.7 Å² | **92.4 Å² by chain D** (EGF) | 3.37 Å | 0.73 → **0.11** |
| **1NQL A** (EGF) | 113.5 Å² | 113.5 Å² | **0.0 Å² by chain B** | **29.21 Å** | 0.77 → **0.77** |

So H409 lies in **both** the cetuximab epitope and the EGF-binding site. A binder
anchored there competes with the natural ligand — a consequence worth stating
explicitly, since EGF competition may be desirable (antagonism) but also means
endogenous ligand will compete in any cell assay.

**1NQL asymmetric-unit caveat.** 1NQL is the apparent exception, and the reason is
probably crystallographic rather than biological: its asymmetric unit holds one
receptor plus one EGF (chain A 612 residues, chain B 48; chains C/D/E have no standard
residues), and its EGF sits 29.21 Å from H409. The biological 2:2 dimer is generated by
symmetry, so contacts formed only in the symmetry-completed assembly do not appear in
the deposited coordinates. **The 0.77 should be read as asymmetric-unit exposure, not
as evidence that EGF leaves H409 free.** The symmetry mate was not built or checked.

**H409 rotamer is conserved across all three structures.**

| Structure | chi1 | bin | chi2 | SC RMSD vs 6ARU (10 Å shell) | flip-corrected |
|---|---|---|---|---|---|
| 6ARU A | −57.4° | m (−65) | −63.6° | — | — |
| 3NJP A | −44.8° | m (−65) | −51.9° | 0.79 Å | 1.64 Å |
| 3NJP B | −47.9° | m (−65) | +134.8° | 1.58 Å | **0.80 Å** |
| 1NQL A | −58.9° | m (−65) | −55.8° | 0.74 Å | 1.63 Å |

chi1 is in the m(−65) bin in all four copies. 3NJP chain B's chi2 is a **180° imidazole
ring flip**: it comes within 18.4° of 6ARU after the flip and its side-chain RMSD drops
from 1.58 Å to 0.80 Å under ND1↔CD2 / CE1↔NE2 correspondence. Since the ND1/CD2
assignment is often unresolved at X-ray resolution, this is an atom-labelling
difference between two copies in one crystal, not a conformational one. Superposition
used backbone N/CA/C/O of the shell around H409; results were unchanged between a 10 Å
shell (8 residues, 32 atoms, bb RMSD 0.20-0.31 Å) and a 12 Å shell (17 residues,
bb RMSD 0.25-0.33 Å). Because the 10 Å shell is a single contiguous loop segment
(406-413), the fit is local by construction.

### 6. pH STRATEGY

**Anchor is H409 (precursor H433).** This supersedes the brief v2 anchor of E496.
Measured basis: **mature 472 (= precursor E496) is 25.85 Å from the H409 imidazole**
and 28.89 Å CA-CA. E496 and H433 cannot participate in the same interface, so the
brief's binder-His/E496 scheme and the H433 anchor are mutually exclusive, and the
lit-pass precedent (Liu 2022 G532 pairing binder acid with EGFR H433/H370) points to
H433. This resolves lit-pass contradiction (2) on geometry, independent of the
summarizer-read sourcing.

**Single-ionization ceiling.** For one ionizable group fully coupled to binding, the
maximum achievable selectivity is `10^ΔpH`. Over pH 7.4 → 6.5, ΔpH = 0.9, so
**Kd(7.4)/Kd(6.5) saturates at 10^0.9 = 7.94×** (computed here). The G532 figure of
**13.26×** reported in the lit pass (Liu 2022, summarizer-read, not verified against a
PDF) **exceeds that ceiling**, which implies more than one coupled ionizable group — or
that the reported value includes avidity, since G532 is an IgG and the lit pass records
a monovalent expectation of roughly 2-10×. Practical consequence: a single binder-side
histidine cannot reach 13×, and a design brief that targets it should plan for ≥2
coupled groups rather than one.

**No target carboxylate is within salt-bridge range of H409.** Closest carboxyl oxygen
is **D344 at 10.58 Å** and **D436 at 10.68 Å** — roughly 2-3× beyond H-bond/salt-bridge
range (~2.7-4.0 Å). H346 (precursor H370), the second Liu anchor, is 8.52 Å ring-to-ring
from H409, so the two target histidines do not couple to each other either. D344 and
D436 remain live candidates for pairing with a **binder-side** histidine rather than
with H409: both are in-patch, D436 with an outward carboxylate at 3.00 Å from Q411.
**This is a Phase 3 question** — Phase 1 (§7) does not attempt pH coupling and uses no
pH-specific restraint.

### 7. PHASE 1 TWO-ARM DESIGN (v3c)

Two arms, **10 seeds each, run sequentially** (not concurrently — two detached
`modal run` sessions from one client cancel each other, per the `run_bindcraft.py`
docstring), both on the domain III slice `--target-residue-range 311-514`:

| Arm | Run tag | Hotspots |
|---|---|---|
| **A** | `phase1-v3c-core` | `A408,A409,A411,A412` |
| **B** | `phase1-v3c-q408` | `A384,A408,A409,A411,A412` |

**Rationale — the two arms trade off three measured properties that cannot all be
satisfied at once.** The split exists because A384 is simultaneously the best and worst
residue in the set:

- **The core (Arm A) is glycan-free but flat.** The 408-412 core is ≥ 14.99 Å from any
  sequon Asn and ≥ 16.79 Å from any modelled sugar atom, so it carries no glycan
  liability. But it is the flattest surface measured (plane RMS 0.45 Å) with no
  resolvable curvature, and its span is only 6.93 Å — a small, flat epitope is a harder
  target for a high-affinity interface.
- **A384 is the only source of concavity (Arm B).** Adding it takes the patch from
  unresolvable curvature to a resolvable **concave** surface (H = +0.08311 /Å, radius
  12.0 Å) and widens the span to 15.77 Å. Concavity generally helps a designed binder
  get shape complementarity.
- **But A384 is also the glycan-adjacent residue.** Every one of the four near sequons
  reaches the patch through A384 and nothing else — N420 at 7.76 Å, N328 at 11.89 Å —
  and the two nearest first-NAGs (11.93 Å, 13.15 Å) are both nearest to A384. A384 is
  additionally 12.29 Å from its nearest other set member, so the concavity it creates
  depends on a spatially detached residue.

Running both is the only way to find out whether the concavity is worth the glycan risk;
neither arm is a priori correct on the measurements.

### 8. ASSAY CONDITIONS

Neutral condition: **10 mM HEPES, 150 mM NaCl, 0.2% Tween-20, 3 mM EDTA, pH 7.4.**
The acidic condition swaps HEPES for a low-pH buffer species (**species TBC** — see
§10), with **ionic strength matched at ~170 mM** so the two conditions differ in pH
alone and not in electrostatic screening.

**Screening consequence.** At I = 0.170 M the Debye length is
`0.304/√I nm = 0.737 nm = 7.37 Å` (computed here, 25 °C). A solvent-exposed salt bridge
is therefore screened over roughly the length of a single residue-residue contact, so a
pH-coupled ion pair placed on the open surface will contribute little free energy at
this ionic strength. **The pH-coupled pair should be buried at the interface core**,
where the local dielectric is lower and the interaction is shielded from bulk
counterions. This argues against relying on H409's own exposure (0.67 free-receptor)
and in favour of a pair that becomes occluded on binding.

**Conflict to reconcile.** An earlier note recorded the buffer as **"HBS-T + 0.5% BSA"**,
which is not the same as the above — it omits EDTA, implies a different detergent
concentration, and adds BSA as a carrier. The two records need reconciling against the
actual Adaptyv assay sheet before any pH-dependent claim is made, since 0.5% BSA in
particular changes the effective free-ligand concentration. **Not resolved here.**

### 9. VALIDATION SO FAR

**The v3 OOM and the fix.** The v3 probe loaded the full 609-residue chain A. AF2
activation memory scales ~N², and `design_logits` requested **29.26-42.59 GiB** across
seeds against a 24 GB A10G, giving `RESOURCE_EXHAUSTED` on every seed before any design
completed. Slicing to domain III (**311-514, 204 residues**, verified 609 → 204 on both
`6aru.cif` and the RCSB `6ARU.pdb` that `design_one` actually fetches, all 7 hotspots
retained) eliminated it: the v3b run logged **0 `RESOURCE_EXHAUSTED` and 0 XLA
rematerialization warnings**, versus one rematerialization warning per seed within 10 s
in v3.

**v3b outcome: 2 accepted from 10 seeds.** Only 10 of the requested 100 seeds ever got
a container — the run was killed mid-flight by
`GRPCError FAILED_PRECONDITION 'workspace ac-3KZ86ww6Oyuet9trAefaYa is disabled'`, an
account-level event, not a code fault. Every seed's last write is timestamped 10:53 PDT.
Seeds 3/5/8 failed on their own merits (Clashing, LowConfidence); seeds 2/4/7/9 were
interrupted mid-MPNN with trajectories in hand; seed 0 never wrote a trajectory. So the
2/10 accept rate understates the true rate. Partial outputs preserved in
`challenges/egfr/phase1-probe-v3b-partial/` (125 files).

| | seed 1 | seed 6 |
|---|---|---|
| design | `egfr_l61_s802791_mpnn5` | `egfr_l73_s214385_mpnn3` |
| length | 61 | 73 |
| sequence | `SAEEEERIRDIVLTTDPHIKRWHEEYEKHPDLPERDKELYEEVMGHHLFLASVVLEDEKAA` | `MKVKDLVGLFRDFVEGKKPEGISEDEFWVIHFEFMVVDPRDPEMVEEFAKKYGISIEEVEEVFRIVKWHPYHR` |
| AF2 design-time i_pTM | 0.90 | 0.80 |
| AF2 pLDDT / i_pAE | 0.94 / 0.12 | 0.90 / 0.21 |
| BindCraft SC | 0.67 | 0.64 |
| binder energy | −148.92 | −183.31 |
| interface H-bonds | 8.0 | 3.5 |

**Full-length co-fold against P00533 precursor 25-645 (621 aa).** Boltz-2 2.2.1 on
A100-40GB. Canonical P00533 was used rather than the 6ARU construct because the
construct stops at precursor 640 and carries a His6 tag. Decision thresholds from
`notes/calibration.md`: **ipSAE_min ≥ 0.60, SC ≥ 0.58; ipTM informational only**
(AUC 0.52 on the Adaptyv set).

| | seed 1 | seed 6 |
|---|---|---|
| iPTM *(informational)* | 0.9293 | 0.7191 |
| pTM | 0.6603 | 0.8090 |
| **ipSAE_min** | **0.5659** ✗ narrow fail | **0.2880** ✗ hard fail |
| ipSAE directional (A→B / B→A) | 0.625 / 0.5659 | 0.3285 / 0.2880 |
| **SC** (pyrosetta Lawrence-Colman) | **0.6451** ✓ pass | **0.3883** ✗ fail |
| complex pLDDT | 0.8873 | 0.8302 |
| binder mean pLDDT | 85.375 | 69.888 |
| interface residues (4.5 Å, heavy) | 27 | 38 |
| target residues flagged interface by PAE | 239 / 621 | **331 / 621** |
| **hotspot recovery** | **6/7** | **3/7** |
| epitope Jaccard vs design-time | **0.77** (88% retained) | **0.32** (70% retained) |
| contacts by ECD domain | **27 domain III** | **19 domain I / 19 domain III** |
| receptor fold, domIII CA RMSD vs 6ARU | 0.58 Å | 0.66 Å |
| receptor fold, domI CA RMSD | 0.72 Å | 0.68 Å |

Per-hotspot closest heavy-atom distance (precursor numbering):

| Hotspot | seed 1 | seed 6 |
|---|---|---|
| Q408 | 3.25 Å ✓ | 3.03 Å ✓ |
| Q432 | 2.97 Å ✓ | 2.81 Å ✓ |
| **H433** | 3.00 Å ✓ | 3.16 Å ✓ |
| Q435 | 2.80 Å ✓ | 7.49 Å ✗ |
| F436 | 3.73 Å ✓ | 4.96 Å ✗ |
| K489 | 2.21 Å ✓ | 4.61 Å ✗ |
| I490 | 8.65 Å ✗ | 7.68 Å ✗ |

**Seed 1 passes; seed 6 fails.** Seed 1 keeps its epitope entirely within domain III
with six hotspots at genuine contact distance (2.21-3.73 Å), passes SC, and misses
ipSAE_min by 0.034 — the shortfall is on the binder side (B→A 0.5659 vs A→B 0.625), not
in interface geometry. Seed 6 bridges domain I and domain III on the full receptor,
fails both decision metrics, and its binder pLDDT of 69.888 sits at ipSAE's 70 cutoff,
which is why 331 of 621 target residues register as "interface" — a diffuse,
low-confidence prediction. **Seed 6 was an artifact of the domain III slice**, which is
the failure mode the slice was expected to risk. Receptor folds are sound in both
(domain III CA RMSD 0.58/0.66 Å vs 6ARU), so the contact analysis is trustworthy.

Contact counts use **heavy atoms only on both sides**: BindCraft's relaxed outputs carry
hydrogens and Boltz's do not, so including H inflates the design-time counts to 29/26
instead of 26/20 and makes the comparison unfair.

**Tools built, and why each was needed** (both additive; no existing behaviour changed):

- **`--target-residue-range` in `run_bindcraft.py`** (commit `155971a`) — the pipeline
  had no way to load a sub-range of a target chain, so a large ECD could only be run
  whole, which OOM'd. 17 insertions / 2 deletions, reusing the existing
  `ChainSelect.accept_residue` hook. Empty string preserves prior behaviour exactly.
- **`cofold_seqs` in `redundancy.py`** (commit `1362da3`) — the existing
  `crossval_boltz` derives its target from the design PDB via `_extract_chains`, so it
  can *only* re-predict against the same sliced target the design was built on. That
  makes it structurally incapable of the check needed here. `cofold_seqs` takes the
  target as an explicit sequence.
- **`sc_and_contacts` + `sc_image`** (same commit) — two problems with reusing `_get_sc`.
  First, `SC_PASS = 0.58` is calibrated on pyrosetta Lawrence-Colman SC, but
  `redundancy.py`'s image has no pyrosetta and falls back to a **burial-fraction proxy**,
  a different quantity that cannot be compared to that threshold. Second, `_get_sc`
  prefers BindCraft's CSV value, which for a re-prediction is the *original* target's
  number. `sc_image` adds pyrosetta so the real `ShapeComplementarityFilter` runs on the
  new structure. `sc_and_contacts` also reports contacts with a `--resnum-offset` so
  output lands in the caller's numbering.

Artifacts: `challenges/egfr/fulllength-cofold/` (predicted complexes, PAE/pLDDT arrays,
confidence JSON).

### 10. OPEN ITEMS

1. **Which ipSAE convention the pipeline uses.** `_compute_ipsae` implements Dunbrack
   2025 with PAE ≤ 10 Å and pLDDT ≥ 70 interface selection and `d0` from the TM-score
   length formula, taking the **minimum over ordered chain pairs**. Whether that matches
   the convention behind the 0.60 operating point (and the Overath 2025 meta-analysis)
   is unconfirmed — the lit pass records that ipSAE and SC "were never analysed in the
   preprint or public tables", so the ranking recipe is untested on this data. Seed 1
   fails by 0.034, which is inside the plausible spread between conventions, so this
   directly decides whether seed 1 advances.
2. **Adaptyv submission cap.** Number of sequences submittable is not recorded anywhere
   in the repo; it sets how many seeds each v3c arm can contribute.
3. **Low-pH buffer species.** §8 — the acidic condition's buffer is TBC, and the
   "HBS-T + 0.5% BSA" vs "HEPES/NaCl/Tween/EDTA" conflict is unresolved.
4. **D344 / D436 exposure.** Both are in-patch but modestly exposed (0.19 and 0.30 rel
   SC) and D344's same-face call is marginal (88.7°, 1.3° inside the cutoff) and would
   flip under a slightly different normal-estimation radius. If either is to carry a
   pH-coupled pair with a binder histidine, its exposure should be checked in the
   *bound* state rather than on the free receptor.
5. **Mouse model confidence over domain III.** Domain III identity is 87.3% per the lit
   pass (not the 92% in brief v2; BLOSUM62 similarity 93.1%). I467 and S468 are the
   divergent positions that sit closest to the epitope, and dropping A465 in v3c is what
   moves them out of patch — but the mouse cross-reactivity of the resulting interface
   has not been modelled, only argued from distance.
6. **`I490` (mature A466) is uncontacted by construction now.** It was dropped from the
   hotspot set, but if the Adaptyv epitope definition requires it, no design so far
   touches it and none is being steered to.

---

## 2026-09-29 — Pre-registered v3c acceptance criteria

Written **before any v3c results exist**, so the bar cannot be moved to fit the
outcome. Both arms (`phase1-v3c-core` = A408,A409,A411,A412; `phase1-v3c-q408` =
A384,A408,A409,A411,A412) are judged by **identical** criteria. A design must
meet all of the following to advance:

1. **ipSAE ≥ 0.60**, using the **min reduction** over the two chain-pair
   directions (min of A→B and B→A), measured on the **full-length co-fold**
   against P00533 precursor 25-645 — **not** on the domain III complex.
2. **Shape complementarity ≥ 0.58**, pyrosetta Lawrence-Colman
   (`ShapeComplementarityFilter`), computed on the **full-length** structure.
3. **pH anchor engaged:** at least one binder side-chain heavy atom within
   **6 Å** of the HIS409 imidazole (ring atoms CG/ND1/CD2/CE1/NE2), on the
   full-length co-fold.
4. **Mouse-divergent positions avoided:** **no** interface contact (any heavy
   atom ≤ 4.5 Å) with mature **467, 468, 471, or 473**.

**Why min, not max.** The 0.60 threshold's source convention is unresolved
(open item #1): the code attributes the ipSAE *formula* to Dunbrack 2025 but the
min reduction to the bioRxiv 2025.08.14.670059 meta-analysis, and neither has
been checked against the reference implementation. The min reduction is the
**conservative** choice — it scores the weaker of the two interface directions,
so a design cannot pass on the strength of one side alone. This convention was
fixed **before v3c results existed**; it is recorded here so it cannot be
reconsidered in light of the numbers. (For reference, under min the v3b survivor
seed 1 scored 0.5659 — a fail; under max it would have been 0.625, a pass. That
0.034 gap is exactly what this pre-registration refuses to relitigate after the
fact.)

---

## 2026-09-30 — Phase 1 v3c — core arm

First real two-arm launch. Arm A (the 4-residue core) completed enough to answer
the question the split was built for; Arm B never started. Full per-design metrics
for all 7 completed designs are in `challenges/egfr/v3c-core-designs.csv` (36
columns); the key columns are tabulated below.

### Run configuration

- Launched **2026-09-29 23:16 MDT** from `main`, plain terminal, foreground,
  `caffeinate` active.
- Arm A, tag `phase1-v3c-core`: hotspots **A408,A409,A411,A412**.
- Arm B, tag `phase1-v3c-q408`: hotspots **A384,A408,A409,A411,A412** — **NOT RUN**.
- Both arms: `--target-residue-range 311-514`, `--lengths 60,100`, `--n 10`.
- Chained with `&&` so Arm B would start only on a clean Arm A exit.
- Confirmed at launch: `chains A=204res`, lengths `[60,100]`, correct hotspot string.

### Outcome

- All 10 containers started **23:29**, terminated **23:53 MDT** — ~24 minutes of runtime.
- **Termination cause: Modal workspace spend limit.** The limit was set to **$20.00**
  personal spend; **$30.00** of credits had already been consumed, so apps stopped at
  **$50.16** total usage.
- **Cost: $6.86** (Modal usage breakdown, Ephemeral Apps, Sep 30 UTC).
- Arm B never started — correct behaviour of the `&&` guard. Nothing to undo.

### Results

**7 designs completed** (one per seed for seeds 0,1,2,3,5,6,7). Of these, **only 5
(seeds 1, 2, 3, 5, 7) have `Accepted/Ranked` directories on the volume.**
`egfr_l93_s713816` (seed 6) and `egfr_l67_s528267` (seed 0) **completed scoring but
were not written to Accepted before termination — they exist only in `v3c-core.log`**,
so a volume listing misses them. For those two, no interface metrics (SC, dG, etc.)
were dumped to the log (only trajectory + AF2 re-prediction values), so those cells are
blank in the CSV.

Metrics for accepted designs are the Rank-1 row of each seed's `final_design_stats.csv`
(AF2 i_pTM/pLDDT are Average over the 2 predicted models; SC/dG/Hbonds are pyrosetta on
the domain III complex). For the two rejected designs, i_pTM/pLDDT are the best-model
AF2 re-prediction from `mpnn_reprediction_log.csv`.

| Seed | Design | Len | Accepted | AF2 i_pTM | SC | dG | Interface Hbonds |
|---|---|---|---|---|---|---|---|
| 0 | egfr_l67_s528267 | 67 | **no** (log only) | 0.85 | — | — | — |
| 1 | egfr_l89_s399498_mpnn2 | 89 | yes | 0.86 | 0.63 | −43.88 | 5.5 |
| 2 | egfr_l75_s674224_mpnn14 | 75 | yes | 0.86 | 0.72 | −52.14 | 6.5 |
| 3 | egfr_l91_s124145_mpnn1 | 91 | yes | 0.81 | 0.73 | −56.73 | 5.0 |
| 5 | egfr_l64_s902794_mpnn2 | 64 | yes | 0.86 | 0.68 | −43.60 | 7.0 |
| 6 | egfr_l93_s713816 | 93 | **no** (log only) | 0.90 | — | — | — |
| 7 | egfr_l79_s846567_mpnn5 | 79 | yes | 0.85 | 0.70 | −51.91 | 10.5 |

Sequences (also in the CSV):

```
seed 0  egfr_l67_s528267        SWTPAQKAHRVDVFYEDMMEIVEKVYRNSGEAKPSPKKFDKEVKMMMPNWVFEWYKEVEPVRKARGA
seed 1  egfr_l89_s399498_mpnn2  MWLSREELMERARKVADPNDPERDAFWIMLDNTLAIIESRRKKAEETGDWEGAKEAIKKEVDDLRKHAPKSLLEKVFGEVLEEALKIPE
seed 2  egfr_l75_s674224_mpnn14 MSVQQRYLFRMIEKNKELVEKGEISPEEAKEVLERYFKEHVEKYDTEFFLPHLNEEEKEKTLKAVEEIKERIESI
seed 3  egfr_l91_s124145_mpnn1  HMTPELEKVMDALYKEKVWHEITWKLYDEFFKAHVDYDEKKVEEIQKVMQEIDEAVKNGDLERFVKVLTEYMKKYFGEELVKKLLEVVEKA
seed 5  egfr_l64_s902794_mpnn2  MKVSEEEFMTLMWKLDDHYMFNPPPGKTIREVHDEVWSKVSNYFDGKYTPTDEDVAEAKKILSS
seed 6  egfr_l93_s713816        MELARRIHKRMVELVLEAYEKDQMDPYFFVISSIGHISYKHLGGKFHPWFMEHWPTFVEIGMKTFKNDPEAMAKVREFRSLMEVYVEETARNS
seed 7  egfr_l79_s846567_mpnn5  EIPKNWTLHHWGEFFRHELHFFRTVYTKEEYEKLKPEFLEKLEKIFEEYVKPVLEKASEEEREAFFKLYSEAMAEFESR
```

### Interpretation

- **7 designs is a FLOOR, not a yield rate.** Seeds 4, 8, and 9 had not finished when
  the run was killed (no report block in the log); seed 0 finished but rejected. The
  denominator is incomplete, so no accept-rate should be quoted from this run.
- **~$1 per accepted design** at this configuration ($6.86 / ~7 completed, 5 accepted).
- **The 4-residue core epitope is designable without A384.** This is the open question
  the two-arm design was built to answer, and Arm A answers it on its own: **7 completed
  / 5 accepted from the 4-residue core, versus 2 accepted from v3b's 7-hotspot set.** The
  concavity that A384 contributes is not required to get BindCraft-accepted designs on
  this epitope. (Whether it improves *full-length* survival is still open — see below.)

### Correction to the record

An earlier assessment in this project attributed the run's termination to unbounded
trajectory looping and estimated the cost at roughly **$57**. **Both were wrong.** The
run cost **$6.86** and was stopped by a **$20 spend-limit setting after 24 minutes**, not
by a runaway loop. This correction is recorded explicitly rather than silently replacing
the earlier figure.

**Correction 2 — the `&&` guard did not guard, and Arm B *did* launch.** The Run
configuration and Outcome sections above state that Arm B was "**NOT RUN**", that it
"never started", and that this was "correct behaviour of the `&&` guard." All three are
wrong. The launch piped Arm A through `tee`
(`modal run … | tee v3c-core.log && modal run … --run-tag phase1-v3c-q408`); in zsh a
pipeline exits with the status of its **last** stage (`tee`), not `modal`, so `&&` fired
on `tee`'s success regardless of Arm A's exit code. Arm B therefore launched, hit the
already-disabled workspace, and died immediately: `v3c-q408.log` (793 bytes) contains
only `Workspace ac-3KZ86ww6Oyuet9trAefaYa has exceeded its spend limit`. No Arm B
designs were produced and nothing was written to the volume, so "nothing to undo" still
holds — but it was the spend limit that stopped Arm B, **not** the guard. **Fix for next
time:** `set -o pipefail` before the chain, or redirect (`> v3c-core.log 2>&1`) instead
of piping to `tee`, so `&&` sees `modal`'s real exit status.

### Still pending

- **Full-length co-fold of all 7 against the pre-registered criteria (`d94a8d4`)** —
  none of these have been scored against that bar yet. The design-time SC/i_pTM above are
  domain III numbers, not the full-length decision metrics.
- **Arm B** (`phase1-v3c-q408`, the +A384 arm).
- **Mouse cross-reactivity refold.**
- **pH-biased redesign near H409.**

All of the above require the Modal workspace, which is currently over its spend limit.

## 2026-09-30 — AMENDMENT to pre-registered v3c criteria: C-terminal paratope clearance

**Reason.** Adaptyv confirmed in Slack (Tudor-Stefan Cotet) that submitted
binders are expressed and immobilised with C-terminal tags, in the construct
`design–linker–GFP11–linker–TwinStrep`, and recommended keeping the paratope
near the N terminus, noting this matters more for smaller binders. Our v3c
designs are 64–93 aa, so the C-terminal fusion is comparable in size to the
binder itself, and a paratope sitting near the binder's C terminus risks
steric occlusion by the fusion.

**New reported metric (all candidates).** *C-terminal clearance* =
(binder length − highest-numbered binder interface residue), reported in
residues and as a fraction of length. Larger clearance = paratope further
from the tagged C terminus. The interface residue set is the binder-chain
(chain B) interface-residue list from BindCraft.

**Status — ranking factor / tiebreaker, NOT a pass/fail threshold.** No cutoff
is set. The metric was defined *after* the v3c results were already in view,
so any threshold chosen now would be fitted to those results. Clearance is
recorded to rank and break ties among otherwise-comparable candidates, not to
accept or reject them.

**Provenance caveat.** For the 5 accepted designs (seeds 1, 2, 3, 5, 7) the
interface set is the MPNN-variant-specific, AF2-repredicted, interface-scored
list. For the 2 non-accepted designs (seed 0 `egfr_l67_s528267`, seed 6
`egfr_l93_s713816`) no MPNN variant passed the base AF2 filters, so no
interface scoring was run on any variant; their clearance is derived from the
**trajectory-backbone** interface set instead (same fold, so paratope location
is essentially unchanged) and is a reference value only — these designs are
not accepted and will not be submitted.

**Values recorded** (new columns `Cterm_clearance_res`, `Cterm_clearance_frac`
in `v3c-core-designs.csv`):

| seed | design | length | max interface res (chain B) | clearance (res) | clearance (frac) | source |
|------|--------|--------|-----------------------------|-----------------|------------------|--------|
| 1 | egfr_l89_s399498_mpnn2  | 89 | B67 | 22 | 0.247 | mpnn |
| 3 | egfr_l91_s124145_mpnn1  | 91 | B64 | 27 | 0.297 | mpnn |
| 5 | egfr_l64_s902794_mpnn2  | 64 | B45 | 19 | 0.297 | mpnn |
| 7 | egfr_l79_s846567_mpnn5  | 79 | B61 | 18 | 0.228 | mpnn |
| 2 | egfr_l75_s674224_mpnn14 | 75 | B61 | 14 | 0.187 | mpnn |
| 0 | egfr_l67_s528267        | 67 | B54 | 13 | 0.194 | trajectory |
| 6 | egfr_l93_s713816        | 93 | B49 | 44 | 0.473 | trajectory |

Among the 4 accepted MPNN designs with the largest clearance, seeds 3 and 5
lead (0.297), then seed 7 (0.228) and seed 1 (0.247); seed 2 has the tightest
paratope-to-C-terminus spacing of the accepted set (0.187).

**Robustness to MPNN redesign.** The chain-B interface list differs between the
trajectory backbone and the final MPNN-redesigned sequence, but the *highest-numbered*
interface residue — the only quantity clearance depends on — agrees on **6 of the 7**
designs; only seed 1 differs, and by a single residue (trajectory B68 vs MPNN B67, i.e.
clearance 21 vs 22). C-terminal clearance is therefore insensitive to MPNN redesign,
which is why the trajectory-derived values for seeds 0 and 6 (no MPNN variant was
interface-scored) are trustworthy. The committed MPNN-derived values stand unchanged.

**Additional constraints and caveats recorded (2026-09-30).**

- **Linear designs only.** Adaptyv confirmed that only linear designs are
  supported this round; cyclic and disulfide-constrained peptides are not.
  Our designs are linear by construction, so this is satisfied by default.
- **Immobilisation is on the C-terminus.** Confirmed twice in Slack by
  Tudor-Stefan Cotet, in two separate threads. This is the basis for the
  C-terminal clearance metric above.
- **Sequence clearance is a proxy, not the quantity of interest.** The
  clearance metric above is a 1-D sequence-distance proxy. The intended
  metric is the *spatial* distance and angle between the C-terminal residue
  and the paratope centroid in the design structure, which captures whether
  the paratope actually faces the immobilisation surface. That structural
  metric is deferred until the design structures are retrievable from the
  Modal volume (currently over its spend limit).

## 2026-09-30 — Finding: MPNN strips non-interface histidines (pH-machinery risk)

Quantifying ISSUE C — whether the MPNN redesign step deletes histidines that a
pH-responsive design would depend on. For each of the 5 accepted v3c core designs,
trajectory sequence (from `v3c-core.log`) vs the MPNN variant (from
`v3c-core-designs.csv`), His positions 1-indexed from the binder N-terminus. "Interface
His" = a His whose position is in that design's chain-B interface-residue list.

| Seed | Design | traj His | MPNN His | lost | gained | interface His (traj → MPNN) |
|---|---|---|---|---|---|---|
| 1 | egfr_l89_s399498_mpnn2  | 4: 20,41,50,67 | 1: 67 | 20,41,50 | — | [67] → [67] |
| 2 | egfr_l75_s674224_mpnn14 | 2: 40,52 | 2: 40,52 | — | — | [40,52] → [40,52] |
| 3 | egfr_l91_s124145_mpnn1  | 5: 16,20,34,72,75 | 3: 1,20,34 | 16,72,75 | 1 | [20,34] → [20,34] |
| 5 | egfr_l64_s902794_mpnn2  | 3: 18,27,33 | 2: 18,33 | 27 | — | [33] → [33] |
| 7 | egfr_l79_s846567_mpnn5  | 5: 9,10,17,20,49 | 4: 9,10,17,20 | 49 | — | [9,10,17,20] → [9,10,17,20] |

**Totals: 19 trajectory His → 12 MPNN His (8 lost, 1 gained, net −7).** MPNN reduced His
count in 3 of 5 designs, left it unchanged in 1, and in seed 3 traded three surface His
for one N-terminal His.

**The strip is selective, and in a reassuring direction.** Every one of the 8 lost His
was a **non-interface** residue; every one of the 8 **interface** His (across all 5
designs) was **conserved**. The single gained His (seed 3, position 1) is also
non-interface. So on this run MPNN is behaving as ProteinMPNN usually does — disfavouring
solvent-exposed His on the scaffold surface — while preserving every His that sits in the
binder–target contact set. No interface His was lost.

**Caveats — why this is recorded as a risk, not a resolved concern.**

1. **This run carried no pH restraint.** The v3c core arm used no pH-specific term (§6,
   §7: "Phase 1 does not attempt pH coupling and uses no pH-specific restraint"). The
   trajectory His here are therefore *incidental scaffold His*, not deliberately placed
   pH machinery. The framing "we select for pH-responsive designs and then hand them to
   MPNN" does **not** literally apply to this run — nothing here was selected for pH.
2. **But it is a real risk for the planned pH-biased arm.** The pending "pH-biased
   redesign near H409" step (§ Still pending) is exactly the case where a functional His
   would be introduced and then handed to the same MPNN step. This finding says that
   step will strip any pH His that is **not** inside the ≤4.5 Å interface contact set.
3. **Interface-set membership is a coarse proxy for "pH-relevant".** A titratable His
   can act at slightly longer range than the 4.5 Å heavy-atom contact cutoff, so
   "interface His conserved" guarantees protection only for His that happen to coincide
   with a contact residue. A His positioned to titrate against target H409 but sitting
   6–8 Å away could be both pH-relevant and MPNN-strippable.
4. **We cannot yet say which trajectory His sat near target H409.** That needs the design
   structures, which are not retrievable while the Modal volume is over its spend limit.

**Not fixed here, by instruction — quantified only.** If the pH-biased arm goes ahead,
the fix is to fix (`--fixed-residues`, or the BindCraft omit-AA / bias mechanism) any
deliberately placed pH histidine so MPNN cannot mutate it, and to re-check His retention
against the trajectory as done above.

## 2026-09-30 — Species alignment reproduced; two filters pre-registered; pipeline audit

### Task 1 — domain III conservation reproduced in-repo (`species_align.py`)

`challenges/egfr/species_align.py` fetches UniProt P00533 (human) and Q01279 (mouse),
globally aligns the full precursors (BLOSUM62, gap −11/−1), and reports domain III
conservation; output in `species_align.out`. All four numbering sanity checks **PASS**
(mature 409=H, 346=H, 353=R, 465=K), so the table is trusted.

- **Domain III identity 179/205 = 87.3%**, now reproduced by a live in-repo alignment
  rather than attributed to the lit pass — confirms 87.3% (not brief v2's 92%).
- **All four Arm A core hotspots are mouse-conserved:** mature 408 Q, 409 H, 411 Q,
  412 F. Both pH histidines are conserved: **H409 and H346**.
- **Hypothesis that Q408 is a species liability: TESTED and REJECTED.** Mature Q408
  (precursor Q432) is glutamine in both species.
- Epitope-adjacent divergences confirmed: **467 I→M, 468 S→N** (cetuximab region) and
  **353 R→K**. Full 26-position divergence list is in `species_align.out`.

### Tasks 2 & 3 — two new filters, PRE-REGISTERED and DEFERRED (blocked on coordinates)

Both require the v3c per-design **complex coordinates**, which are on the Modal volume
(over its spend limit) and not retrievable. Neither can be computed now: `v3c-core.log`
records only *binder*-side interface residues (chain B), not target-side contacts, and
**no v3c complex PDB exists locally**. Definitions are fixed here, before the numbers
exist, so they cannot be tuned to the outcome. Both run against each design's complex PDB,
in which BindCraft renumbers the target 1-204 over the mature 311-514 slice
(**mature = index + 310**; verification gate: **index 99 must be HIS = mature 409**, else
stop and do not trust the mapping).

**Filter 2 — interface species conservation.** Conserved *hotspots* do not imply a
conserved *interface*. For each design: take the binder–target interface residue list
(4.5 Å heavy-atom), map each **target** residue to mature numbering, and report total
target interface residues; count mouse-conserved vs divergent (against the 26 divergent
positions in `species_align.out`); and which divergent positions are contacted, by mature
number. **Flag as a cross-reactivity risk any design contacting mature 418, 443, 467,
468, or 353**, regardless of its hotspot set.

**Filter 3 — acidic-residue-to-target-histidine (Liu 2022 / G532 mechanism, PMC9703009).**
The G532 pH switch comes from EGFR's *own* histidines paired with binder **acidic**
residues (H433=H409 ↔ LCDR1 Glu32; H370=H346 ↔ LCDR2 Asp52/Asp53; mutating that Glu→His
destroyed the pH dependence). Our binders need Asp/Glu positioned against the target
histidines, not histidines of their own. For each design report: min distance from any
binder Asp/Glu carboxylate O to the **H409** imidazole N (ND1/NE2); same for **H346**;
and counts of binder Asp/Glu within **4.0 Å** and within **6.0 Å** of either. Target
positions in the renumbered complex: **H409 = index 99, H346 = index 36.**

### Task 4 — pipeline audit (CHECK only; nothing changed)

(a) **MPNN variant — UNCONFIRMED from this repo.** `run_bindcraft.py` loads BindCraft's
shipped `settings_advanced/default_4stage_multimer_hardtarget.json` (on the image at
`/opt/bindcraft`, **not** in this repo) and overrides only `af_params_dir`,
`save_design_animations`, `save_design_trajectory_plots`, and `max_trajectories`. It does
**not** set `mpnn_weights`, so the SolubleMPNN-vs-ProteinMPNN choice is whatever that JSON
ships. BindCraft's documented default for this preset is SolubleMPNN, but the value is not
verifiable from the repo — it must be read off the image. Given the Adaptyv expression gap
(0% ProteinMPNN vs 93.1% SolubleMPNN), **confirm this before the next run.**
(b) **ipSAE — YES, min reduction.** `redundancy.py::_compute_ipsae` (Dunbrack 2025):
interface residues by PAE ≤ 10 Å and pLDDT ≥ 70, d0 from the TM-score length formula,
reduced as **ipsae_min** (minimum over the two ordered chain directions).
`IPSAE_MIN_PASS = 0.60`.
(c) **Interface dG / dSASA / shape complementarity — YES.** SC via pyrosetta
ShapeComplementarityFilter (pre-filter, pass 0.58); dG, dSASA, and Binder_Energy_Score
are computed by BindCraft (present in `v3c-core.log`).
(d) **Exposed-hydrophobic-patch metric — NO.** No SAP / spatial-aggregation-propensity /
exposed-patch score anywhere in the pipeline. Only BindCraft's scalar
`Surface_Hydrophobicity` and `Interface_Hydrophobicity` columns exist (fractions, not a
patch score). Adding a real exposed-hydrophobic-patch metric is an open item if
aggregation / expression liability is a concern.

### Task 5 — `set -o pipefail` fix

No launch script existed to patch: the v3c two-arm launch was an ad-hoc **interactive**
`modal run … | tee … && modal run …` command (README's `modal run` commands are single
detached runs, no `tee`, no chain). Added **`modal/run_logged.sh`**, a `set -euo pipefail`
wrapper that tees a command's combined output to a log **and** exits with the command's
real status, so an `&&`-chained launch cannot advance on `tee`'s success after `modal`
failed. Tested: failing command → non-zero exit, and a failing first arm blocks the
second. Use it for any future chained/logged launch.

## 2026-09-30 — Filters 2 & 3 computed on retrieved v3c complexes

**Retrieval (read-only, no container, no compute spend).** The v3c complex PDBs were
pulled with `modal volume get` (CLI, control-plane copy from the `adaptyv-designs`
volume) — **not** by invoking a Modal function, which would start a GPU container.
**Total pulled: 2,545,668 bytes (~2.6 MB), 7 files.** They live in the session scratch
(not committed, as with `phase1-probe-v3b-partial/`); exact volume paths are recorded
below for reproducibility.

**Inventory (Task B).** Every one of the 7 designs has both a trajectory complex
(`<seed>/Trajectory/Relaxed/egfr_l*.pdb`) and MPNN-variant complexes
(`<seed>/MPNN/Relaxed/…`). The 5 accepted designs additionally have Rank-1 accepted
complexes (`<seed>/Accepted/Ranked/1_*.pdb`); seeds 0 and 6 have MPNN complexes (32 and
4) but none accepted. **Accepted designs all have MPNN-variant complexes, so no STOP.**

**Provenance (Task C) — exact structure measured per design.** MPNN Rank-1 complex for
the 5 accepted; trajectory complex for seeds 0 and 6 (no accepted MPNN variant). Per-row
`pdb_file` and numbers are in `challenges/egfr/v3c-core-filters.csv`. Numbering gate
(target chain A residue 99 = HIS = mature 409, residue 36 = HIS = mature 346;
mature = A_resnum + 310) **PASSED on all 7**.

| Seed | Structure measured | src |
|---|---|---|
| 0 | `…/0/Trajectory/Relaxed/egfr_l67_s528267.pdb` | trajectory |
| 1 | `…/1/Accepted/Ranked/1_egfr_l89_s399498_mpnn2_model2.pdb` | mpnn |
| 2 | `…/2/Accepted/Ranked/1_egfr_l75_s674224_mpnn14_model2.pdb` | mpnn |
| 3 | `…/3/Accepted/Ranked/1_egfr_l91_s124145_mpnn1_model2.pdb` | mpnn |
| 5 | `…/5/Accepted/Ranked/1_egfr_l64_s902794_mpnn2_model2.pdb` | mpnn |
| 6 | `…/6/Trajectory/Relaxed/egfr_l93_s713816.pdb` | trajectory |
| 7 | `…/7/Accepted/Ranked/1_egfr_l79_s846567_mpnn5_model2.pdb` | mpnn |

### Filter 2 — interface species conservation (4.5 Å heavy-atom, target mapped to mature)

| Seed | target iface res | conserved | divergent | divergent contacted (mature) | RISK (418/443/467/468/353) |
|---|---|---|---|---|---|
| 0 | 21 | 17 | 4 | 353, 418, 443, 468 | 353, 418, 443, 468 |
| 1 | 23 | 19 | 4 | 353, 418, 467, 468 | 353, 418, 467, 468 |
| 2 | 25 | 22 | 3 | 324, 418, 467 | 418, 467 |
| 3 | 26 | 20 | 6 | 324, 353, 359, 418, 467, 468 | 353, 418, 467, 468 |
| 5 | 23 | 18 | 5 | 324, 353, 418, 467, 468 | 353, 418, 467, 468 |
| 6 | 28 | 24 | 4 | 324, 418, 467, 468 | 418, 467, 468 |
| 7 | 23 | 19 | 4 | 324, 353, 418, 467 | 353, 418, 467 |

**Finding — conserved hotspots did NOT buy a conserved interface.** Although all four
Arm A core hotspots are mouse-conserved (previous entry), **every one of the 7 designs
contacts mouse-divergent positions, and every one contacts both mature 418 (S→G) and 467
(I→M)**; most also contact 353 (R→K) and 468 (S→N). The as-built paratopes reach beyond
the conserved core into divergent territory in all cases, so **mouse cross-reactivity is
a live risk across the whole v3c core arm**, not something the hotspot choice secured.
This is exactly the gap the filter was meant to expose: hotspot conservation is necessary
but not sufficient.

### Filter 3 — binder acid → target histidine (6.0 Å primary; see caveat)

Min distance from any binder Asp/Glu carboxylate O to the target His imidazole N
(ND1/NE2). **Per Task E the 6.0 Å shell is the primary readout**: AF2 surface-polar
rotamers are unreliable, so a sub-4 Å carboxylate–imidazole distance is *not* evidence of
a hydrogen bond. The 4.0 Å column is reported but not interpreted as bonding.

| Seed | src | d(acid→H409) | d(acid→H346) | acids ≤4.0Å | acids ≤6.0Å | H409 in iface? | H409 min-acid (any atom) | H409 rank | iface frac w/ acid ≤6Å |
|---|---|---|---|---|---|---|---|---|---|
| 0 | traj | 9.00 | 9.41 | 0 | 0 | yes | 8.77 | 10/21 | 0.19 |
| 1 | mpnn | 4.19 | 7.79 | 0 | 1 | yes | 3.52 | 6/23 | **0.65** |
| 2 | mpnn | 2.59 | 9.32 | 1 | 1 | yes | 2.59 | **1/25** | 0.16 |
| 3 | mpnn | 2.68 | 8.05 | 1 | 1 | yes | 2.68 | **1/26** | 0.42 |
| 5 | mpnn | 2.97 | 9.89 | 1 | 1 | yes | 2.97 | 4/23 | 0.43 |
| 6 | traj | 10.91 | 17.99 | 0 | 0 | yes | 10.13 | 14/28 | 0.17 |
| 7 | mpnn | 2.69 | 6.53 | 1 | 1 | yes | 2.69 | **1/23** | 0.48 |

**Null control (Task D) — and what it means.** The five MPNN designs each place a binder
acid within 6 Å of H409; the two trajectory designs (0, 6) do not. But the null control
shows this is only *partly* H409-specific:

- In **seed 2** (only 16% of interface residues have an acid within 6 Å, yet H409 is rank
  1/25) the acid proximity to H409 is genuinely distinctive.
- In **seeds 3 and 7** H409 is also rank 1, but 42–48% of *all* interface residues have
  an acid within 6 Å, so the interface is broadly acid-rich; H409 leading is meaningful
  but partly a composition effect.
- In **seed 1** H409 is rank 6/23 and **65%** of interface residues have an acid within
  6 Å — here "acid near H409" carries essentially **no** information; the filter is
  measuring interface packing density and the binder's overall acidity, not H409-specific
  design intent.

**Because the v3c core arm used no pH restraint, every acid-near-H409 here is incidental,
not intent.** The null control confirms the filter's raw form (count acids within 6 Å of
H409) largely measures packing density / binder acidity in acid-rich designs, and is only
informative where the interface-wide acid fraction is low (seed 2). H346 is essentially
unengaged in all designs (≥6.5 Å; only seed 7 marginal at 6.53 Å), consistent with its
poor free-receptor accessibility (§3). The proper use of Filter 3 is therefore on the
*pH-biased* redesign arm, where an acid is deliberately placed, and always read against
this null (H409's rank among interface residues), not as an absolute distance.

## 2026-09-30 — Operational notes and pre-registered submission decisions

### Structures vendored into the repo

The 7 v3c core complex PDBs used for Filters 2 & 3 are now committed under
`challenges/egfr/structures/v3c-core/`, with filenames matching the `pdb_file`
column of `v3c-core-filters.csv` so that column resolves locally. Reason: the
Modal volume has been unreachable twice today (spend-limit stops), and every
downstream structural analysis depends on these files — they should not live
only in ephemeral session scratch or behind a volume that can disappear.

### Modal volume / target naming (recorded to avoid a recurring dead end)

The design outputs live on the Modal **volume named `adaptyv-designs`**, not
`designs`. Running `modal volume ls designs …` (e.g. against environment `main`)
returns **`Volume 'designs' not found`**, which reads like a missing/empty volume
but is actually a **wrong-name (wrong-target) error** — the data is fine, the
name is wrong. Always use `adaptyv-designs`. Confirmed working:
`python3 -m modal volume ls adaptyv-designs /egfr/attempts/phase1-v3c-core`.

### PRE-COMMITMENT — submission decisions (recorded BEFORE Stage 1 & Stage 2 results)

**Pre-registered. Written before any co-fold cross-reactivity or full-length
pass/fail numbers are seen, so the decision cannot be reverse-fitted to the
outcome.** Two contingencies:

**(a) If Stage 1 shows a real human-vs-mouse ipSAE_min gap across all 7 designs**
(a "real" gap being one larger than the per-complex diffusion-sample range, per
the fixed interpretation rule): **we submit anyway rather than redesigning.**
Reasoning: (i) mouse cross-reactivity is Adaptyv's *second-ranked* criterion of
three, a ranking factor, not a pass/fail gate; (ii) the Challenge 1 deadline is
**2026-10-04**, and (iii) redesigning against a mouse-variant target would leave
no time to validate the redesign. The cross-reactivity weakness will be **stated
explicitly in the submission**, not hidden.

**(b) If fewer than 3 designs pass the d94a8d4 criteria at Stage 2**
(ipSAE_min ≥ 0.60 AND SC ≥ 0.58): **we submit the passers plus the next-best by
the composite ranking, each labelled pass or sub-threshold, and we do NOT fill
all 20 slots.** Reasoning: an unused slot scores zero, so *some* padding beyond
the strict passers is rational — but Track 2 and Track 3 share a single 384-well
plate allocated by a workflow that reads the submissions, so a large tail of
weakly justified designs plausibly costs more in selection than it gains in
coverage. Submit the defensible set, labelled honestly; do not pad to 20.
