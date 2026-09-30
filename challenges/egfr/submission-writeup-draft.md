# EGFR pH-conditional binder — design rationale and validation

**Challenge 1, Anthropic × Adaptyv Bio 2026 · Track 3**
Draft — values marked `[PENDING]` land from the Stage 1/2 co-folds.

---

## At a glance

| | |
|---|---|
| Approach | De novo minibinder, BindCraft (AF2 hallucination → SolubleMPNN → AF2 validation) |
| Starting point | None. PDB 6ARU used for epitope selection only; all backbones hallucinated |
| Target region | Human EGFR domain III, mature 311–514 |
| Epitope (hotspots) | Q408, H409, Q411, F412 — **mature** numbering |
| Molecule class | protein (single chain, linear) |
| Lengths | 64–93 aa |
| Designs submitted | `[PENDING]` |
| Selection criteria | Pre-registered before results, commit `d94a8d4` |

**Numbering convention.** Mature EGFR numbering throughout. Precursor
(UniProt P00533) = mature + 24. EGFR ECD crystal structures use mature
numbering (1YY9 DBREF maps PDB residue 1 → UniProt 25). Every residue number
in this document is mature unless explicitly marked otherwise.

**Epistemic labels.** Claims below are marked `[measured]` (computed in this
project, artifact in repo), `[literature]` (published, cited), `[inferred]`
(our reasoning from sourced facts), or `[unverified]` (assumed, not confirmed).

---

## Criterion 1 — pH-selective binding (6.5 over 7.4)

**Mechanism targeted.** `[literature]` The pH switch is placed on *EGFR's own*
histidine rather than engineered into the binder. Liu et al. 2022 (Mol Ther
Oncolytics, [PMC9703009](https://pmc.ncbi.nlm.nih.gov/articles/PMC9703009/))
showed that the cross-reactive, pH-dependent anti-EGFR antibody G532 derives
its pH dependence from receptor histidines paired with antibody-side acidic
residues: LCDR1 Glu32 against H433 (precursor) = **H409** (mature), and LCDR2
Asp52/Asp53 facing H370 = **H346**. The effect is supported bidirectionally —
Y32E created it (~13× gain, Fab format), reverting E32→His destroyed it
(~5× loss), H433A abolishes binding, H370A reduces both affinity and pH
dependence.

**Why this epitope.** H409 is in the hotspot set. `[measured]` It is also
conserved in mouse, so the mechanism is available in both species.

**What was achieved this round — stated plainly.** `[measured]` This round
applied **no pH restraint during hallucination**. Any favourable acid–histidine
geometry is incidental. We measured it anyway: all five MPNN designs place a
binder carboxylate 2.6–4.2 Å from H409's imidazole. Run against a null control
— the same measurement to every other contacted target residue — that result
largely dissolves: for most designs acidic residues sit near most target
residues, so proximity to H409 carries no information. One design is
distinctive: 16% of its interface residues have an acid within 6 Å while H409
ranks first. **The raw filter without the null would have reported five
successes instead of one.**

**Expected magnitude.** `[literature]` A single ionisable group caps the Kd
ratio at 10^0.9 = 7.9× across pH 7.4→6.5. G532 achieves 13.26× (SPR, monovalent
analyte geometry) at 294 nM affinity. Published de novo fold-changes are mostly
measured over a 2.0 pH-unit window against our 0.9, so literature headline
numbers scale down substantially here. We are not claiming to exceed G532.

**Artifacts:** `challenges/egfr/v3c-core-filters.csv` (per-design acid–H409
distances, null ranks), methods log entry 2026-09-30.

---

## Criterion 2 — mouse cross-reactivity

**Measured per design, not inferred.** `[measured]` Rather than assume
cross-reactivity from hotspot conservation, we built the mouse domain III
sequence by substituting all 26 divergent positions and co-folded every design
against both species under identical tool, length, and sampling settings.
`[PENDING — Stage 1 table]`

**Epitope-level conservation.** `[measured]` Global alignment of P00533 against
mouse Q01279, computed in-repo against live UniProt. Domain III identity
179/205 = **87.3%**. All four hotspots conserved: 408 Q, 409 H, 411 Q, 412 F.
Both histidines H346 and H409 conserved.

**A hypothesis we tested and rejected.** `[measured]` We predicted Q408 would
be a species liability, since it is a cetuximab contact but not a contact of
the cross-reactive G5V2 epitope. The alignment shows it conserved. The
prediction was wrong and is recorded as such.

**Why A465/A466 were dropped.** `[measured]` They were the route by which
mouse-divergent I467 (I→M) and S468 (S→N) entered the contact patch. Removing
them pushes both beyond contact range.

**Known weakness — interface-level divergence.** `[measured]` Conserved
hotspots do not imply a conserved interface. Mapping each design's full 4.5 Å
contact set against the alignment shows **all seven designs contact divergent
418 (S→G) and 467 (I→M)**; most also contact 353 (R→K) and 468 (S→N).
S418→G is the most consequential, since mouse deletes the side chain entirely.
This is a real limitation of the current designs.

**Context.** `[literature]` Cetuximab does not functionally bind mouse EGFR;
necitumumab, on an overlapping domain III epitope, loses ~3,000× from human to
mouse (FDA BLA 125547 pharmacology review). Domain III cross-reactivity is
achievable but not automatic — G532 manages it, and its own pH selectivity on
mouse is 3.3× against 13.26× on human.

**Artifacts:** `challenges/egfr/species_align.py`, `species_align.out`.

---

## Criterion 3 — human EGFR affinity

**Pre-registered acceptance thresholds.** `[measured]` Committed to the
repository **before** any v3c results existed (commit `d94a8d4`), specifically
to prevent the min/max ipSAE convention being chosen after the fact to rescue a
borderline design.

- **ipSAE_min ≥ 0.60**, minimum over chain-pair directions
- **Shape complementarity ≥ 0.58** (PyRosetta, Lawrence–Colman)
- ipTM recorded, not used for selection

`[literature]` The threshold was chosen independently and subsequently found to
match the published optimum: a meta-analysis of 3,766 experimentally
characterised binders reports AF3 ipSAE_min > 0.61 as the max-F1 threshold and
the best single predictor of wet-lab binding, at 1.4× the average precision of
AF2 ipAE (bioRxiv 2025.08.14.670059).

**Full-length validation.** `[measured]` Designs were scored against the
complete 621-residue ECD, not only the domain III slice used for design, to
confirm the interface survives in the intact receptor. `[PENDING — Stage 2]`

---

## Epitope selection — the glycan decision

`[measured]` A384 was dropped late in design despite being the **only**
resolvable source of surface concavity (mean curvature H = +0.083/Å). It is
also the sole route by which the N420 sequon reaches the patch, at 7.8 Å.

`[literature]` N420 is occupied — chitobiose resolved in both 1YY9 and 6ARU —
and the chitobiose core alone extends 10–12 Å from the attachment asparagine.
The epitope therefore sat inside the rigid, crystallographically ordered stem,
not under a mobile distal antenna.

`[inferred]` Since the assay antigen is HEK293-expressed with full human
glycans while our template is a crystal structure with glycans truncated to
stubs, the design model could not see the obstruction.

`[literature]` Domain III glycan shielding is measured, not hypothetical:
PNGase F deglycosylation improves cetuximab KD from 4.66 nM to 0.017 nM and
151 nM to 0.15 nM (270× and 1000×), with trastuzumab/HER2 unaffected
(Glycobiology 2025, cwaf066).

**Decision:** a flat epitope with validated accessibility over a concave one
with unvalidated accessibility. The cost is acknowledged — flat surfaces are
harder to bind tightly.

---

## Method

BindCraft, `default_4stage_multimer_hardtarget` preset, filters unmodified.
Target sliced to mature 311–514 (204 residues) to fit AF2 activation memory.
Sequence design by SolubleMPNN with `mpnn_fix_interface` enabled. All designs
single-chain and linear.

**De novo declaration.** `[measured]` No existing binder was used as a starting
point. 6ARU is a cetuximab–EGFR complex and was used solely to identify surface
residues for the hotspot set. No antibody sequence, CDR, or scaffold was
grafted, copied, or optimised. Backbones are hallucinated de novo.

---

## Additional validation

**Sampling noise quantified.** `[measured]` Every co-fold ran three diffusion
samples; scores are the mean with sample range reported. A human-vs-mouse
difference is called real only when it exceeds the larger of the two sample
ranges. The scoring rule — mean, not best-of-three — was fixed before results
were seen, since best-of-N biases toward whichever side draws a lucky sample
and the bias is not symmetric. `[inferred]` Boltz is deterministic without a
seed, so diffusion sampling is the only measurable repeat-variance; this bounds
sampling noise only and says nothing about systematic model error.

**C-terminal clearance.** `[inferred]` Expression is quantified by split-GFP
complementation and the construct linker is short, so a C-terminus occluded by
the binding interface would read as failed expression rather than as a
construct problem. Clearance was measured per design and used in ranking.

**Assay-condition filters.** `[inferred]` 3 mM EDTA rules out metal-coordinating
designs. `[unverified]` The stated 0.2% Tween-20 is roughly ten times a typical
BLI kinetics buffer; if correct, it penalises designs relying on broad exposed
hydrophobic surface, and we weighted against those.

---

## Limitations

1. **Interface-level mouse divergence.** All designs contact ≥2 species-divergent
   positions. Quantified above.
2. **Flat epitope.** Dropping A384 removed the only measurable concavity;
   the remaining surface is flat within fit error.
3. **pH mechanism is incidental, not designed.** No pH restraint was applied
   during hallucination. `mpnn_fix_interface` means MPNN preserves an interface
   acid the trajectory placed but never introduces one, so a *designed* pH
   switch requires intervention at the hallucination stage. Planned, not done.
4. **Small sample.** `[literature]` The de novo hallucination hit rate in
   Adaptyv's EGFR Round 2 was 9% (6/65), and no prior round required
   pH-switching or cross-species reactivity, so there is no base rate for this
   problem type. We expect below 9%.

---

## Designs submitted

`[PENDING — table: name, length, ipSAE_min human (mean ± range), ipSAE_min
mouse (mean ± range), difference vs noise floor, SC, C-terminal clearance,
H409 acid rank, pass / sub-threshold]`

---

## Provenance

Methods log, per-design metrics, alignment script and output, and all complex
structures are version-controlled, including dated corrections to analyses that
proved wrong — a broken shell guard, a confounded run comparison, and a
sequence analysis run on the wrong sequence set. The pre-registration commit
`d94a8d4` predates all v3c results.
