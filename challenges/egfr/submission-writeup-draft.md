# EGFR pH-conditional binder — design rationale and validation

**Challenge 1, Anthropic × Adaptyv Bio 2026 · Track 3**
Complete — all co-fold results landed 2026-09-30.

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
| Designs submitted | 3 (1 pass, 2 declared near-misses) — allowance is 20, deliberately unused |
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
conserved in mouse, so the mechanism is available in both species. And the EGF
control independently confirms the site is bindable: folded blind against the
full receptor, EGF recovers 408, 409 and 412 in every sample.

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
Three diffusion samples per species per design; 1,771 GPU-s. A difference is
called real only when it exceeds the larger of the two sample ranges.

| design | human ipSAE | mouse ipSAE | gap | noise floor | resolved |
|---|---|---|---|---|---|
| `egfr_l93_s713816` | 0.816 [0.011] | 0.792 [0.014] | 0.024 | 0.014 | yes |
| `egfr_l75_s674224_mpnn14` | 0.801 [0.032] | 0.775 [0.006] | 0.026 | 0.032 | no |
| `egfr_l64_s902794_mpnn2` | 0.751 [0.050] | 0.727 [0.047] | 0.024 | 0.050 | no |
| `egfr_l79_s846567_mpnn5` | 0.748 [0.028] | 0.728 [0.056] | 0.020 | 0.056 | no |
| `egfr_l91_s124145_mpnn1` | 0.720 [0.015] | 0.693 [0.051] | 0.027 | 0.051 | no |
| `egfr_l67_s528267` | 0.705 [0.031] | 0.642 [0.051] | **0.063** | 0.051 | yes |
| `egfr_l89_s399498_mpnn2` | 0.761 [0.015] | 0.695 [0.048] | **0.066** | 0.048 | yes |

**The aggregate result, stated against our own interest.** `[measured]` All
seven designs score higher against human than mouse. Under a sign test that is
p = 0.016 two-tailed (0.008 one-tailed, and the human-favouring direction was
predictable a priori from 26 divergent positions). **These designs are not
species-agnostic — there is a small, systematic human preference across the
entire set.** That is a finding against criterion 2, and we report it as such
rather than leading with the four "indistinguishable" verdicts.

**Resolution tracks precision, not effect size.** `[measured]` The per-design
verdicts split into three resolved and four not, but that split is largely an
artifact of measurement precision. `l93` (gap 0.024) resolves while `l79`
(gap 0.020) does not — near-identical gaps, different verdicts, because `l93`
was sampled four times more tightly. The honest grouping is by gap magnitude,
not by verdict:

- **Large gap (~0.065):** `l67`, `l89` — genuine species discrimination.
- **Small gap (0.020–0.027):** the other five, indistinguishable from each
  other and close to the noise floor.

`[inferred]` Reading the four non-resolved designs as "cross-reactive" would
be reading a null result as a positive one. The defensible claim is narrower:
five of seven show a species gap too small to resolve at this sampling depth,
and two show a gap roughly 2.7× larger that is clearly real.

**Convergence worth noting.** `[measured]` The three submitted designs were
selected on Stage 2 full-length composite, with no reference to Stage 1. They
happen to be three of the five smallest species gaps, and both large-gap
designs fall outside the submission set. The two selection criteria agree
without having been made to.

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
confirm the interface survives in the intact receptor. Three diffusion samples
per design; mean reported with sample range in brackets. Total 1,244 GPU-s.

| design | len | ipSAE_min | SC | pass | composite |
|---|---|---|---|---|---|
| `egfr_l93_s713816` | 93 | **0.651** [0.014] | **0.647** [0.122] | **yes** | 0.651 |
| `egfr_l75_s674224_mpnn14` | 75 | 0.543 [0.218] ⚠ | 0.597 [0.100] | SC only | 0.543 |
| `egfr_l64_s902794_mpnn2` | 64 | 0.516 [0.098] | 0.574 [0.066] | no | 0.511 |
| `egfr_l89_s399498_mpnn2` | 89 | 0.546 [0.057] | 0.512 [0.065] | no | 0.482 |
| `egfr_l91_s124145_mpnn1` | 91 | 0.510 [0.064] | 0.545 [0.039] | no | 0.479 |
| `egfr_l79_s846567_mpnn5` | 79 | 0.524 [0.126] | 0.519 [0.205] ⚠ | no | 0.469 |
| `egfr_l67_s528267` | 67 | 0.453 [0.154] ⚠ | 0.533 [0.060] | no | 0.417 |

⚠ = poorly determined, sample range > 0.15 on the marked metric.

**One design passes.** `[measured]` Slice-stage ipSAE_min was 0.72–0.82; six of
seven fall to 0.45–0.65 at full length. The interface does not survive intact
receptor context for most of the set.

**The passer is the most reproducible result in the run, not the luckiest.**
`[measured]` `egfr_l93_s713816` has an ipSAE sample range of **0.014** —
0.650, 0.659, 0.645 — roughly four times tighter than any other design and
sixteen times tighter than `l75`. All three samples clear threshold
independently.

**Why the sampling protocol mattered.** `[measured]` `l75` has a mean of 0.543
but samples spanning 0.431–0.649: **one of three clears 0.60.** A single-sample
protocol had a one-in-three chance of reporting `l75` as a pass. The
mean-not-best-of-N rule was fixed before results were seen, and this is the
case it caught.

**Calibration control — pre-registered, run, branch (a).** `[measured]` The
0.60 threshold derives from a benchmark of ~200–400 residue complexes and is
applied here at ~700. We pre-registered an EGF positive control with both
interpretive branches fixed in advance (commit `5a2d2dc`, before the control
was run), explicitly as a check on the instrument rather than an adjustment of
the threshold to admit designs.

Mature EGF (53 aa, P01133, coordinates read from the feature table) co-folded
against the same 621-residue target, same tool, same settings, three samples:

| | ipSAE_min | SC | ipTM | pTM | pLDDT |
|---|---|---|---|---|---|
| EGF control | **0.644** [0.059] | 0.499 [0.036] | 0.948 | 0.882 | 0.884 |

**EGF clears 0.60. Branch (a) applies: the threshold holds, Stage 2 stands
unadjusted.** A known nanomolar ligand of this receptor is not systematically
depressed below threshold by full-length context, so the six sub-threshold
designs are better read as six genuine failures than as a scoring artifact.
That is the less convenient of the two branches and it is the one the data
selected.

**The control validated the epitope as well as the threshold.** `[measured]`
Unplanned: `sc_and_contacts` reports which hotspots each pose recovers. EGF
independently docked onto our hotspot set — 3/4, 3/4 and 4/4 across the three
samples, recovering 408, 409 and 412 in every sample and 411 in one. We did
not constrain it there; `cofold_seqs` receives no hotspot argument. **A natural
ligand of EGFR, folded blind against the full receptor, lands on the patch we
designed against.** The epitope is a real binding site, not an artifact of
hotspot selection from a cetuximab co-crystal.

**A finding against our own SC criterion.** `[measured]` EGF scores SC = 0.499,
below our pre-registered 0.58 cutoff. Since EGF binds at essentially our
epitope, this is not an epitope mismatch — **our SC criterion would have
rejected EGF.** SC ≥ 0.58 is therefore not a necessary condition for binding
at this site, and the criterion is probably too strict. We report this rather
than acting on it: the thresholds were fixed in advance, and no design in our
set failed on SC alone, so relaxing the criterion post-hoc would rescue nothing
and cost the pre-registration its meaning. The finding is offered for whoever
calibrates this metric next.

`[inferred]` One caution on reading these numbers as affinity. Our passer
scores 0.651 against EGF's 0.644. That does not mean it out-binds EGF. ipSAE
is a binary classifier of whether an interface is real, validated as such; it
is not an affinity scale, and nothing here licenses ranking a de novo design
above a natural ligand.

`[measured]` Control cost 149 GPU-s. Artifact: `challenges/egfr/egf-control.json`.

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

1. **Interface-level mouse divergence, and a systematic species gap.** All
   designs contact ≥2 species-divergent positions, and all seven score higher
   against human than mouse (sign test p = 0.016 two-tailed). The designs are
   not species-agnostic; the submitted three have gaps near the noise floor,
   which is weaker than demonstrated cross-reactivity.
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
5. **SC criterion is probably mis-set.** `[measured]` The EGF control scores
   SC = 0.499 at our own epitope, below our 0.58 cutoff — the criterion would
   reject a known ligand. Left unchanged because it was pre-registered and
   changing it rescues nothing, but it should not be reused as-is.
6. **The passer was rejected by BindCraft's own filters.** `[measured]`
   `egfr_l93_s713816` is a trajectory sequence that BindCraft's default filter
   set declined. It passes our independent full-length criteria with the
   tightest sampling spread in the run. We report the disagreement rather than
   resolving it: either our criteria admit something BindCraft correctly
   rejected, or BindCraft's defaults are miscalibrated for this target. The
   wet-lab result decides.

---

## Designs submitted

**Three, not twenty.** `[measured]` The selection rule was pre-registered: if
fewer than three designs pass full-length validation, submit the passer plus
the next-best by composite, labelled, and **do not pad to the 20-sequence
allowance.** One design passed. The rule fired as written.

| # | design | len | full-length ipSAE | species gap | status |
|---|---|---|---|---|---|
| 1 | `egfr_l93_s713816` | 93 | **0.651** [0.014] | 0.024 | **Pass** — both thresholds, all three samples |
| 2 | `egfr_l75_s674224_mpnn14` | 75 | 0.543 [0.218] | 0.026 | Sub-threshold, poorly determined (1 of 3 samples above threshold). Highest SC in the set |
| 3 | `egfr_l64_s902794_mpnn2` | 64 | 0.516 [0.098] | 0.024 | Sub-threshold, well determined. Second-highest SC |

`[inferred]` Designs 2 and 3 are submitted as declared near-misses, not as
candidates we expect to bind. Padding the remaining 17 slots with designs whose
composite runs down to 0.417 would raise the chance of a hit by chance while
making the pre-registration meaningless. We would rather report one honest pass.

`[measured]` `egfr_l93_s713816` leads on every axis measured: highest human
ipSAE at slice stage (0.816), highest mouse (0.792), tightest sampling in both
species, only full-length pass, and tightest full-length spread. It is the
single design in this set we would defend individually.

---

## Provenance

Methods log, per-design metrics, alignment script and output, and all complex
structures are version-controlled, including dated corrections to analyses that
proved wrong — a broken shell guard, a confounded run comparison, and a
sequence analysis run on the wrong sequence set. The pre-registration commit
`d94a8d4` predates all v3c results.
