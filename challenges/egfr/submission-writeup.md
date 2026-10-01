# EGFR pH-conditional binder — design rationale and validation

**Challenge 1, Anthropic × Adaptyv Bio 2026 · Track 3**
Complete — hallucination round 2026-09-30, pre-registered variant round 2026-10-01.

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
| Designs submitted | 5 (2 complementary leads, 3 declared near-misses) — allowance is 20, deliberately unused |
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

**The hallucination round produced no pH mechanism in its best binder.**
`[measured]` No pH restraint was applied during hallucination, so any
acid–histidine geometry would have been incidental. Structural inspection of
all seven full-length Stage 2 models showed five of seven carried an acidic
residue within 6 Å of H409 — **but the only design that passed the binding
thresholds, `egfr_l93_s713816`, was one of the two that did not.** Its epitope
instead presented His36 at 4.97 Å from H409: two histidines that both gain
positive charge as pH falls, which opposes selectivity rather than creating it.

`[measured]` Proximity is also not geometry. Of the designs that did carry
acids, only one of each adjacent pair actually faced H409 — in `l64`, Asp34 sits
at 4.44 Å while Glu35 points away at 10.9 Å; in `l91`, Asp28 at 3.66 Å against
Glu29 at 10.6 Å.

**A pre-registered variant round fixed this.** `[measured]` Four single
substitutions on the `l93` backbone, acceptance criteria and submission rule
committed before the co-folds ran (commit `25bbfb3`): unchanged ipSAE_min ≥
0.60 and SC ≥ 0.58, plus a new requirement that a carboxylate oxygen sit within
4.0 Å of H409's NE2 or ND1 in at least 2 of 3 samples.

| variant | ipSAE_min | SC | verdict |
|---|---|---|---|
| parent (control) | 0.639 [0.072] | 0.671 [0.116] | pass |
| **l93_H36E** | **0.666 [0.048]** | **0.641 [0.083]** | **pass** |
| l93_S32D | 0.407 [0.443] | 0.554 [0.148] | fail |
| l93_S32D_S33D | 0.449 [0.491] | 0.545 [0.170] | fail |
| l93_S32E | 0.272 [0.009] | 0.423 [0.041] | fail |

`[measured]` The parent re-ran as an internal control and reproduced within
sampling noise (0.639 vs 0.651 at Stage 2), so these sit on the Stage 2 scale.

**The predicted-best variant failed and the predicted-worst succeeded.**
`[measured]` S32D was the primary hypothesis on geometric grounds — Ser32's
hydroxyl sits 3.45 Å from H409 across all three parent models, and Asp's
carboxylate reaches the same distance from CB. It collapsed to 0.407 with a
sample range of 0.443. S32E failed harder with a range of 0.009 — confidently
broken. Ser32's hydroxyl is evidently load-bearing for the pose, not merely
decorative. H36E, ranked last a priori, was the only variant to pass: it adds
the acid without disturbing Ser32, removes the like-charge histidine pair, and
relieves a His8–His36 intra-binder clash that reproduced in all three parent
models.

**Measured geometry of the designed switch.** `[measured]`

| model | contact | distance |
|---|---|---|
| model_0 | Glu36 OE1 → H409 NE2 | 3.305 Å |
| model_1 | Glu36 OE1 → H409 NE2 | 3.117 Å |
| model_2 | Glu36 OE1 → H409 ND1 | 3.205 Å |

Mean **3.21 Å**, spread 0.19 Å, present in 3 of 3 models against a
pre-registered bar of 2 of 3. That is canonical salt-bridge distance. The
engaged imidazole nitrogen differs between models; the interaction does not.

`[inferred]` Mechanistically: at pH 7.4 H409 is largely neutral and the
Glu36–His409 contact is an ordinary hydrogen bond. At pH 6.5 a larger fraction
is protonated and the same contact becomes a charged salt bridge. Binding
strengthens as pH falls. This is the first design in the project where that
mechanism is present by design rather than by accident.

**Expected magnitude.** `[literature]` A single ionisable group caps the Kd
ratio at 10^0.9 = 7.9× across pH 7.4→6.5. G532 achieves 13.26× (SPR, monovalent
analyte geometry) at 294 nM affinity. Published de novo fold-changes are mostly
measured over a 2.0 pH-unit window against our 0.9, so literature headline
numbers scale down substantially here. We are not claiming to exceed G532, and
a single engineered salt bridge is at the modest end of what is achievable.

**Artifacts:** `challenges/egfr/l93-variants.json`, `challenges/egfr/l93_H36E/`
(three output structures), methods log entries 2026-10-01.

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

**Full-length measurement for the two lead designs.** `[measured]` Stage 1
above was run on the domain III slice, before `l93_H36E` existed. Both leads
were therefore re-measured against human and mouse **full-length** ECD in a
single run, under an interpretation rule committed beforehand (commit
`4e656f4`). The mouse target was built by substituting mouse residues at every
divergent position of mature 1–621 in the human numbering frame — 70 of 621
divergent, 88.7% identity, H409/H346 and all four hotspots conserved.

| design | human | mouse | gap | noise floor |
|---|---|---|---|---|
| `egfr_l93_s713816` | 0.653 [0.009] | **0.648** [0.032] | +0.005 | 0.032 |
| `l93_H36E` | 0.672 [0.022] | **0.593** [0.423] ⚠ | +0.079 | 0.423 |

H36E's mouse value is from a 6-sample re-measurement (below); every other cell
in this table is 3 samples.

`[measured]` Validity check: `l93_H36E` against human reads 0.672 here against
0.666 in the variant round; the parent reads 0.653 against 0.639 and 0.651 in
two earlier runs. Both reproduce, so these gaps are interpretable.

**The parent is cross-reactive. This is the project's one clean criterion-2
result.** `[measured]` Human 0.653 and mouse 0.648 both clear the 0.60
threshold, the gap is 0.005 against a noise floor of 0.032, and both arms are
tightly determined. Unlike the slice-stage verdicts above, this is a positive
result rather than an unresolved one.

**The lead design does not meet criterion 2, and the reason is worth stating
precisely.** `[measured]` H36E's first mouse measurement gave samples 0.670,
0.424, 0.301 — range 0.369, the largest spread in the project and 2.5× the
0.15 precision bar used elsewhere. Because the trigger was the *range* and not
the unfavourable mean, the same rule would have fired on a favourable result
with that spread, so it was re-measured at 6 samples. The rule, all three
outcome branches, and a stop rule were committed before the run
(`methods.md` 2026-10-01, commit `92206e1`).

Six samples: **0.6746, 0.6588, 0.6729, 0.6538, 0.6451, 0.2513.** Mean 0.5927,
range 0.4233, median 0.6563. **The pre-registered statistic is the mean, the
mean is 0.5927, and it fails the 0.60 threshold by 0.0073. Criterion 2 is not
met for `l93_H36E`.** The stop rule was applied and no third measurement was
taken.

`[measured]` **Post-hoc observation, labelled as such and not used to rescue
the result.** The distribution is bimodal rather than scattered: five samples
span 0.645–0.675, one sits at 0.2513. Per-sample hotspot recovery separates
them objectively — each of the five clustered samples recovered **4/4**
hotspots (SC 0.649–0.750); the outlier recovered **0/4** (SC 0.426). The
outlier is a docking failure, not a weaker pose. This makes the mean a poor
summary statistic here, which is a statement about the statistic and **not**
grounds for substituting the median. The median is reported above so a reader
can see the difference; the verdict stands on the mean.

`[inferred]` What this does and does not license. It supports: *when H36E
engages the mouse epitope it does so comparably to human (0.645–0.675 vs
0.672), and it engages less reliably than any other pairing measured here.*
It does not support a failure rate — n = 6 cannot separate a real ~15%
failure from one unlucky draw — and it does not support calling H36E
cross-reactive.

`[measured]` **Symmetry check, so outlier structure is not invoked only where
it helps.** No other measured pairing shows it: parent/mouse range 0.032,
H36E/human range 0.022 and 0.048. The instability is specific to H36E against
mouse, which is at least consistent with the H→E substitution having removed a
histidine that contributed to initial recognition — an untested hypothesis, not
a conclusion.

**The two leads are complementary, and neither is complete.** `[measured]`

| | pH mechanism | cross-reactivity | human binding |
|---|---|---|---|
| `l93_H36E` | **yes**, 3.21 Å | **no** | yes, 0.67 |
| `egfr_l93_s713816` | no | **yes**, clean | yes, 0.65 |

`[inferred]` These differ by a single residue, position 36. His gives
cross-reactivity without a mechanism; Glu gives the mechanism and costs mouse
binding. The two properties are coupled at one position rather than being
independently optimisable, and every alternative position we tested (S32D,
S32D/S33D, S32E) destroyed human binding outright. We submit both and state
plainly that the submission as a set addresses criteria 1 and 2 while no single
design in it does.

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

## Funnel — every denominator, not a hit rate

`[measured]` Reporting a single success rate hides which denominator it was
computed on. Counts for every stage, including the runs that failed:

Generation, by arm — four arms were launched, two produced nothing:

| arm | seeds requested | containers started | trajectories completed | accepted | fate |
|---|---|---|---|---|---|
| `phase1-probe-v3` | not logged | ≥1, all failed | 0 | 0 | `RESOURCE_EXHAUSTED` in `design_logits` on every seed — 29.26–42.59 GiB requested against a 24 GB A10G, on the untruncated 609-residue chain |
| `phase1-probe-v3b` | 100 | 10 | 9 | 2 | killed at 10 seeds; arm later retired on the glycan argument, never validated |
| `phase1-v3c-core` | 10 | 10 | 7 | 5 | every completed design carried forward |
| `phase1-v3c-q408` | 10 | 0 | 0 | 0 | launched, but the workspace was already disabled; the app died on the spend limit with no container ever running |
| **total** | **≥120** | **≥20** | **16** | **7** | |

The v3 probe's seed count was not recorded at run time and is not reconstructed
here, so the request and container totals are lower bounds. The two numbers
that matter for it — trajectories and accepted designs — are both zero and are
recorded: it contributed nothing downstream.

Validation, on the `v3c-core` set:

| stage | count | note |
|---|---|---|
| Carried to validation | 7 | 5 accepted, plus seeds 0 and 6 which BindCraft **rejected** and we retained deliberately |
| Variants designed | 4 | single substitutions on the `l93` backbone |
| Computationally screened | 11 | all 7 originals and all 4 variants, full-length co-fold |
| Passed pre-registered criteria | 2 | `egfr_l93_s713816`, `l93_H36E` |
| **Submitted** | **5** | 2 passing, 3 labelled near-misses — out of **20 permitted** per team |
| Selected and expressed | — | sponsor-determined |
| Experimentally positive | — | sponsor-determined |

The two `v3b` accepted designs are counted in the generation table and excluded
from validation: the arm was retired before any full-length check was run on
them, so there is no validation number to report. Neither is submitted.

`[measured]` **Five of twenty permitted slots are used.** Three further designs
completed and were computationally screened but are not submitted
(`egfr_l67_s528267`, `egfr_l89_s399498_mpnn2`, `egfr_l79_s846567_mpnn5`), as are
the three failed variants. Filling the remaining fifteen slots was available and
declined: the selection rule was fixed before the results existed, and
submitting everything that ran would discard the only thing that makes the
five-design set meaningful.

**No yield rate is quoted from these numbers, deliberately.** `[measured]`
Both arms that produced designs were terminated by **account-level compute
events** rather than by designs failing: v3b by
`GRPCError FAILED_PRECONDITION: workspace ... is disabled`, and the v3c pair by
the workspace spend limit, which stopped arm 1 partway and killed arm 2 at
launch. In v3b, 10 of 100 requested seeds reached a container at all;
of those, seeds 3/5/8 failed on their own merits (Clashing, LowConfidence)
while seeds 2/4/7/9 were interrupted mid-MPNN holding completed trajectories.
In v3c-core, seeds 4, 8 and 9 never produced a report block. **The
denominators are truncated by infrastructure, not by biology**, so dividing
accepted by requested would produce a number that understates the method and
means nothing. The counts are reported; the ratio is not.

`[measured]` All four arms are in the table, including the two that produced
nothing: the 100-seed v3 probe that OOM'd before writing a trajectory, and the
`v3c-q408` arm that never got a container because the spend limit was reached
while arm 1 was still running. Each is dated in `methods.md` with its failure
reason and whatever partial output survived.

`[measured]` Note the asymmetry in the "carried to validation" row: `l93`,
which became a submitted lead and passed both pre-registered thresholds, is one
of the two designs BindCraft's own default filters **rejected**. Retaining
rejected designs was a decision made before the validation results existed.

**Reviewer attestation.** `[measured]` Every submitted design was individually
inspected by the submitting researcher, not accepted on score alone. For the
two leads this covered: pose reproducibility across three independent
predictions (domain III RMSD 0.35–0.37 Å), buried interface area measured
against domain III rather than the flexible full receptor (1124 Å², 3.0%
spread), per-residue confidence at the epitope (90.3–95.7, top band of the
structure), binder-restricted clash counts with severities, and the identity
and geometry of every residue within 5–6 Å of H409. Dates, commands and
outputs are in `methods.md` under 2026-10-01; the structures inspected are
committed under `challenges/egfr/fulllength-v3c/` and
`challenges/egfr/l93_H36E/`.

---

## Limitations

1. **The pH mechanism and cross-reactivity are coupled, and we could not have
   both.** `[measured]` The single substitution that creates the acid–H409
   salt bridge (H36E) takes mouse binding from 0.648 (tight, range 0.032) to a
   mean of 0.593 at 6 samples, below the 0.60 threshold. The failure is one of
   *reliability* rather than of pose quality: five of six predictions land on
   the epitope at 0.645–0.675 with 4/4 hotspot recovery, one misses entirely.
   Every alternative acid position tested (32, 33, 32+33) destroyed human
   binding, so within this scaffold position 36 is the only site that can carry
   the mechanism and it is the same site that carries cross-reactivity. **No
   design in this submission satisfies criteria 1 and 2 simultaneously; the set
   does, the individual molecules do not.**
2. **Interface-level mouse divergence, and a systematic slice-stage gap.** All
   designs contact ≥2 species-divergent positions, and all seven scored higher
   against human than mouse at slice stage (sign test p = 0.016 two-tailed).
   The full-length parent result is the one clean exception.
3. **Flat epitope.** Dropping A384 removed the only measurable concavity;
   the remaining surface is flat within fit error.
4. **The pH switch is a single engineered salt bridge, not a designed
   interface.** `[measured]` Hallucination applied no pH restraint; the
   mechanism in `l93_H36E` comes from one post-hoc substitution, not from
   designing the interface for pH from the start. One ionisable pair caps the
   achievable ratio at 7.9× before window scaling. A trajectory-stage pH
   restraint remains the right approach and was not implemented.
   `[inferred]` The substitution is also unvalidated beyond structure
   prediction — Boltz placing a carboxylate at 3.21 Å is evidence, not proof,
   that the real sidechain adopts that rotamer.
5. **Small sample, and no base rate for this problem type.** `[literature]`
   Two independent anchors: the de novo hallucination hit rate in Adaptyv's
   EGFR Round 2 was 9% (6/65); a prior Proteinbase challenge ran 1,196 tested
   → 1,028 expressed → 111 bound, i.e. 10.8% among expressed designs. Neither
   round required pH-switching or cross-species reactivity, so there is no
   base rate for a problem with three stacked criteria. We expect below both
   figures.
6. **SC criterion is probably mis-set.** `[measured]` The EGF control scores
   SC = 0.499 at our own epitope, below our 0.58 cutoff — the criterion would
   reject a known ligand. Left unchanged because it was pre-registered and
   changing it rescues nothing, but it should not be reused as-is.
7. **The passer was rejected by BindCraft's own filters.** `[measured]`
   `egfr_l93_s713816` is a trajectory sequence that BindCraft's default filter
   set declined. It passes our independent full-length criteria with the
   tightest sampling spread in the run. We report the disagreement rather than
   resolving it: either our criteria admit something BindCraft correctly
   rejected, or BindCraft's defaults are miscalibrated for this target. The
   wet-lab result decides.
8. **Both leads share one scaffold, and it is the least solubility-optimised in
   the set.** `[measured]` Designs 1 and 2 differ by a single residue, so any
   expression or aggregation failure takes both. That scaffold has the highest
   surface hydrophobicity of the four submitted (0.43 vs 0.22–0.34) because it
   is the only submitted sequence that never passed through SolubleMPNN — all
   twenty MPNN variants of `l93` failed AF2 re-prediction. With 0.2% Tween-20
   in the buffer and a split-GFP expression readout, that risk reads as failed
   expression rather than failed binding, and it is **not independently
   mitigable within the two leads**. Designs 3–5 are the mitigation.

---

## Designs submitted

**Five, not twenty.** `[measured]` The original selection rule was
pre-registered: if fewer than three designs pass full-length validation, submit
the passer plus the next-best by composite, labelled, and **do not pad to the
20-sequence allowance.** One design passed, and that rule fired as written,
giving three. Two were added afterwards, each for a stated reason, and both
additions are disclosed below as post-hoc.

| # | design | len | ipSAE_min | acid–H409 | basis |
|---|---|---|---|---|---|
| 1 | **`l93_H36E`** | 93 | **0.666** [0.048] | **3.21 Å, 3/3** | Pre-registered variant round; meets criteria 1 and 3. Mouse 0.593 at 6 samples — fails criterion 2 on the mean, 5/6 samples on-epitope |
| 2 | **`egfr_l93_s713816`** | 93 | 0.651 [0.014] | none | Original pre-registered passer. **Cross-reactive** (mouse 0.648, clean) |
| 3 | `egfr_l75_s674224_mpnn14` | 75 | 0.543 [0.218] | Asp45 present | Next-best by composite; poorly determined |
| 4 | `egfr_l64_s902794_mpnn2` | 64 | 0.516 [0.098] | Asp34 at 4.44 Å | Next-best by composite |
| 5 | `egfr_l91_s124145_mpnn1` | 91 | 0.510 [0.064] | **Asp28 at 3.66 Å** | **Post-hoc addition** — best acid geometry among the original seven |

**Two disclosures.** `[measured]` Design 1 came from a variant round run after
the original set was locked, under criteria committed in advance of the result.
Design 5 was added after seeing results, on a criterion — acid–H409 geometry —
that had not been used for selection because no full-length measurement of it
existed at the time. It was then measured uniformly across all seven original
designs, and `l91` ranked first on it despite ranking fifth on binding. Neither
addition is claimed as pre-registered.

`[inferred]` Designs 3–5 are submitted as declared near-misses on binding, not
as candidates we expect to bind well. We did not pad the remaining 15 slots.

**Designs 3–5 also carry an unplanned function: they are scaffold insurance
against a correlated failure in designs 1 and 2.** `[measured]` The two leads
are the same backbone one residue apart, so every property governing whether
the molecule is physically obtainable — fold stability, aggregation propensity,
surface hydrophobicity — is shared. If that scaffold does not express, both
leads are lost in the same well. Designs 3–5 are three independent backbones at
64, 75 and 91 residues.

`[measured]` **Surface hydrophobicity of the submitted sequences, and why the
leads are highest.** The assay buffer carries 0.2% Tween-20, which competes for
exposed nonpolar surface, and expression is quantified by split-GFP
complementation, so an aggregation-prone design reads as failed expression
rather than as failed binding.

| submitted design | surface hydrophobicity | sequence origin |
|---|---|---|
| `egfr_l93_s713816` / `l93_H36E` | **0.43** † | AF2 trajectory — **never SolubleMPNN-redesigned** |
| `egfr_l64_s902794_mpnn2` | 0.34 | SolubleMPNN |
| `egfr_l91_s124145_mpnn1` | 0.26 | SolubleMPNN |
| `egfr_l75_s674224_mpnn14` | 0.22 | SolubleMPNN |

† **Provenance differs and is marked rather than smoothed over.** The three
MPNN figures are `Average_Surface_Hydrophobicity` from
`challenges/egfr/v3c-core-designs.csv`. `l93` has no value in that column —
no MPNN variant of it was ever accepted — so its figure is
`Surface_Hydrophobicity` from the trajectory stats table in `v3c-core.log`.
Same metric and same code, each computed on the molecule actually submitted,
but trajectory and MPNN statistics are not interchangeable in general and
conflating them produced a documented error earlier in this project
(`methods.md`, 2026-09-30, correction 2).

`[inferred]` The gap is not coincidence. All twenty SolubleMPNN variants of
`l93` failed AF2 re-prediction filters, so the submitted `l93` sequence is the
raw hallucinated trajectory — the only design in the set that never received
the sequence-design step whose explicit purpose is lowering surface
hydrophobicity. The same fact that made `l93` unusual enough to survive
full-length validation when its MPNN children did not is the fact that leaves
it least optimised for solubility. **This is a stated expression risk on both
leads, not a prediction of failure**, and it is the reason the three remaining
slots went to other scaffolds rather than to more `l93` variants.

`[measured]` **Designs 1 and 2 are the two we would defend, and they are
complementary rather than ranked.** `l93_H36E` is the only design carrying a
measured pH-switch geometry and has the highest human ipSAE in the project, but
fails the threshold against mouse. Its parent is the only design with clean
full-length cross-reactivity, but carries no pH mechanism. They differ by one
residue, and that residue is where the two properties conflict.

---

## Provenance

Methods log, per-design metrics, alignment script and output, and all complex
structures are version-controlled, including dated corrections to analyses that
proved wrong — a broken shell guard, a confounded run comparison, and a
sequence analysis run on the wrong sequence set. The pre-registration commit
`d94a8d4` predates all v3c results.
