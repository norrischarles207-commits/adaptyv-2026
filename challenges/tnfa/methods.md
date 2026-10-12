# TNF-α — methods log

Challenge 2, Anthropic × Adaptyv Bio 2026 · Track 3.
Mature TNF-α numbering 1–157 throughout (human UniProt P01375 = mature + 76;
mouse P06804 = mature + 79).

---

## 2026-10-10 — PRE-REGISTRATION, recorded before any design result exists

Nothing has been generated against this target. The probe run
(`tnfa-probe-v1`) tested memory only, was cancelled mid-trajectory, produced
no accepted design, and **nothing from it is eligible for submission**.

### Target

**PDB 7KPB, chains B + C.** Chain B presents the conserved face of the
receptor groove (143–146); chain C presents the dense face (86/87). Grooves in
7KPB run B→C (3.89 Å) and A→B (3.92 Å).

**Why 7KPB and not 1TNF or 3ALQ.** Checked every structure's sequence against
the sequence in the challenge brief:

| structure | mismatches |
|---|---|
| 1TNF | 1 — **L143 where wild-type is D143, inside the epitope** |
| 3ALQ | 6 — engineered lysines K11M, K65S, K90P, K98R, K112N, K128P; two inside the epitope |
| **7KPB** | **0** |

7KPB is the only sequence-exact structure available and is receptor-bound,
which is the conformation a receptor-blocking binder must complement.

### Hotspots — fixed now

```
B32, B143, B146, C86, C87, C90
```

Rationale, all from `epitope-analysis.md`:
- **B32 (Arg32)** and **C90 (Lys90)** are the only two conserved cationic
  residues in the consensus epitope, 13.7 Å apart in this groove. They are the
  pH-switch anchors (see below).
- **B143, B146** anchor the 143–146 run: the only four-long conserved stretch
  in the consensus epitope, independently supported by mutagenesis.
- **C86, C87** are the densest contacts in the entire site, 42 and 45 atom
  pairs against a typical 5–20, and both conserved.

Deliberately excluded: **31, 71, 72, 73, 85, 89, 97** — every divergent
position in the epitope, including the indel at 72, the human-only histidine
at 73, and the charge changes at 31 and 89.

Binder lengths **60–100 aa**. Preset `default_4stage_multimer_hardtarget`,
filters unmodified.

### Acceptance thresholds — unchanged from challenge 1

- **ipSAE_min ≥ 0.60**, minimum over chain-pair directions
- **SC ≥ 0.58** (pyrosetta Lawrence–Colman). Reviewed between challenges and
  deliberately kept; see `notes/calibration.md`, "SC gate reviewed and kept".
- Scored as the **mean of 3 diffusion samples, never best-of-N**
- Sample range > 0.15 on either metric = "poorly determined", flagged
- ipTM recorded, not used for selection

### pH-release variant rule — fixed before any variant is run

The mechanism is **binder histidine against a conserved target cation**. At
pH 7.4 the histidine is neutral and binding is intact; at pH 6.0 it protonates
and repels R32 or K90, and the complex releases. Both anchors are conserved
human/mouse, so the switch does not trade against objective 2.

A variant is accepted only if **all three** hold:

1. ipSAE_min ≥ 0.60 against human, unchanged
2. SC ≥ 0.58, unchanged
3. **a binder histidine side-chain nitrogen (ND1 or NE2) within 6.0 Å of
   R32 NH1/NH2/NE or K90 NZ in at least 2 of 3 samples**

The 6.0 Å bar is set a priori from the only published range we have for this
mechanism class — protonated-His to cationic-residue distances of 3.7–7.6 Å
in the Baker 2025 release designs (bioRxiv 2025.09.29.678932, read through a
summarizer, not yet verified against the primary text). It is a judgement
call, recorded as one.

**Two histidines are preferred over one.** A single ionisable group caps the
affinity ratio at 10^ΔpH, and pH 7.4→6.0 is 1.4 units, so ~25× at theoretical
best — probably short of "no detectable binding". Variants satisfying (3) at
**both** R32 and K90 rank above variants satisfying it at one.

### What this cannot show, stated now

`[inferred]` Neither Boltz-2 nor AF2 models protonation state. No prediction
here can show pH-dependent binding. What is measurable is **geometry at
neutral pH**: whether a histidine sits where protonation would be disruptive.
That is evidence the mechanism is *available*, not evidence it *works*. Every
pH claim in the writeup must be stated at that strength.

### Submission rule — fixed now

- Up to 20 designs permitted. **Do not pad.**
- If fewer than three designs pass full-length validation, submit the passers
  plus the next-best by composite, labelled as near-misses.
- Designs whose only merit is a pH geometry, without clearing (1) and (2), are
  **not** submitted — mechanism without binding is not a candidate.
- Any design added after results are seen is disclosed as post-hoc.

### Known risk, recorded in advance

Objective 3 asks for *no detectable binding* at pH 6.0, not a ratio. That is a
switch, not a dial, and a harder bar than challenge 1's. We expect to be able
to demonstrate the geometry and not the magnitude.

---

## Amendment 1 — 2026-10-11, written before the v2 run

Everything below supersedes the hotspot set at line 36, the anchor rationale
at lines 40-41, and the pH variant rule at lines 68, 76 and 87. The original
text is left in place unedited: this file's value is that each claim provably
predates its result, and silently rewriting a superseded line would destroy
that. No compute has been spent against the revised set at the time of this
commit.

### Correction: the 13.7 A figure was wrong

The original recorded **R32 and K90 as "13.7 A apart in this groove."**
Remeasured from 7KPB coordinates, closest cationic nitrogen to closest
cationic nitrogen:

| pair | side-chain N-N | Ca-Ca |
|---|---|---|
| R32(B) - K90(C) | **21.5 A** | 15.9 A |
| R32(B) - R82(C) | **13.9 A** | - |
| R32(B) - K65(B) | **16.4 A** | - |

`[computed]` The 13.7 A figure matches **R82**, not K90. The original was
never attributed to a named atom pair, so this is recorded as a mismeasurement
rather than a transcription slip. Our pre-registered anchor pair is ~8 A
further apart than written down -- the difference between "one binder face
reaches both" and "marginal."

### New evidence: 7KP7 (mouse TNF-alpha + human TNFR1)

`[computed]` 7KP7, 2.65 A, is human TNFR1 bound to **mouse** TNF-alpha. Both
7KPB and 7KP7 have **wild-type TNF** (all SEQADV entries are on the receptor
or are expression tags) and carry the **identical** receptor construct
(N54D, C182S), so species is the only variable between them.

- 30 of 32 human TNFR1 contacts are also mouse TNFR1 contacts.
- **All six original hotspots are contacted in both species.**
- Author numbering in 7KP7 is mouse-mature + 1; with the indel at human T72,
  author N maps to human mature N for N>=73 and N-1 below. Validated by
  residue identity at **148/148 residues, zero mismatches**.
- Divergence re-derived from sequence independently: 33 positions,
  124/156 = 79.5%, matching the organisers' stated figure.

Objective 2 therefore rests on a solved complex of a protein that binds this
site in both species, not on an inference from global sequence identity.

### Correction: the TNFR1-and-TNFR2 consensus discarded two conserved cations

`[computed]` Requiring contact with **both** receptors was conservative but
unjustified -- the challenge asks us to bind TNF-alpha, not to block both
receptors. Against the cross-species TNFR1 standard there are **four**
conserved cations in the epitope, not two:

| | contacts hum/mou | note |
|---|---|---|
| R32 | 82 / 128 | densest contact in the epitope; face-1 |
| K65 | 28 / 45 | face-1, 16.4 A from R32; TNFR1-only, so the old intersect dropped it |
| K90 | 7 / 20 | face-2; highest B-factors of any anchor (68-75) |
| R82 | 1 / 3 | face-2; rim only, not meaningfully in the interface |

K65 is also mutated (K65S) in 3ALQ, so it only became visible after the switch
to wild-type 7KPB.

`[computed]` Receptor F in 7KPB occupies the B+C groove and contacts chain B
at 20, 21, 31, **32**, 33, **65**, 67, 113, 115, 143-147, 149. R32 and K65 are
therefore contacted by the same receptor molecule in the same groove -- not
merely close in space. Both side chains are fully modelled (B = 50-66 and
48-62). **C32's side chain is absent** (residue mean B = 99) and was never a
usable target.

### Revised hotspots — fixed now

```
B32, B65, B145, C86, C87
```

B145 (52/81) replaces D143 (13/29) on contact density; C90 is dropped as an
aiming point. All five are conserved and contacted in both species. Target
remains 7KPB chains B,C: face-1 of B is a groove *wall*, so designing against
isolated chain B would yield binders that clash with C in the real trimer.

### Revised pH variant rule

- **Required:** binder His ND1/NE2 within **6.0 A** of R32 NH1/NH2/NE **or**
  K65 NZ, in at least 2 of 3 samples. Threshold unchanged and still set a
  priori from Baker 2025's 3.7-7.6 A range.
- **Two anchors (R32 and K65) rank above one.** This replaces the R32/K90
  pairing at line 87.
- **Three anchors (+K90) is a stretch goal, labelled as such.** R32/K65/K90
  are mutually 16-21 A, so it is reachable in a 60-100 aa binder, but we are
  not pre-registering a target we cannot reliably hit.

### Declared asymmetry: the mouse His tag

`[inferred]` The mouse assay construct TNA-M52H3 carries a C-terminal
polyhistidine tag; human TNA-H4211 is tag-free. Objectives 2 and 3 are
measured on tagged protein, objective 1 on untagged. A His tag is itself a
cluster of titratable histidines, i.e. the same chemistry as our switch.

`[computed]` Nearest approach from any modelled C-terminus (157) to any
revised hotspot is **21.0 A**, with all distances 21-34 A. Thresholds were set
before measuring: >25 A unreachable, <15 A real risk. A fully extended His6
spans roughly 21 A, so this is **low risk but not zero.** K65 is the most
tag-remote hotspot in the set (33.5 A); C90/C86/C87 are the closest (21-24 A),
which independently favours the face-1 anchoring above.

### Acceptance gate — disclosure

Our pre-registered gate is **ipSAE_min >= 0.60 and SC >= 0.58**. BindCraft's
stock `default_filters.json` is a *separate, stricter, uncalibrated* gate that
we never pre-registered and never derived. In run tnfa-v1-core it returned
**0 accepted designs from 22 trajectories** while six MPNN variants passed the
AF2 filters (best i_pTM 0.78, SC 0.65 -- above our threshold). Stated plainly
because it matters: v2 applies our pre-registered criteria and relaxes the
stock filter. This is not a threshold loosened after seeing results -- the
stock filter was never our criterion, and the evidence is that it was
discarding designs that pass the criterion we did commit to.

### Declared unknowns — not resolved, recorded

1. **Does TNF-alpha itself change between pH 7.4 and 6.0?** Trimer stability
   or dissociation at the acidic condition would confound objective 3's
   readout for every entrant. Unanswered. Largest open risk and not ours to
   fix; recorded so it cannot be invoked post-hoc.
2. **propka is not relied upon.** Jacobson et al. 2025 report predicted pKa
   was *not* predictive of which pH bin a design fell into. `[secondhand]`,
   from the authors' own account. Our geometric rule above is the instrument.
3. Calibration AUCs in notes/calibration.md still have no recorded source.

### Independent corroboration

`[secondhand]` Two expert panel discussions (Adaptyv competitor calls, video 1
and 2) independently support three pre-registered positions: that one
histidine is insufficient and more than one titratable group is needed; that
structure predictors do not model protonation, so neutral-pH geometry shows
availability and not function; and that **charge clash is more predictive of
pH sensitivity than pH-sensitive hydrogen bonding** -- which is the mechanism
class this file already specified. One panellist proposed binder-His against
target-cation unprompted, which is the design recorded here. A counterpoint is
also recorded: histidine *networks* may buffer rather than amplify pH
response, so the anchors should stay spatially separated rather than clustered.

---

## Amendment 1a — 2026-10-11, after the v2 smoke (n=2), before the fan-out

### Record-keeping note

Amendment 1's content (this file's revision, 7KP7.pdb, and the five analysis
scripts) was committed in **81839f9**, whose message describes only the
i_pTM-floor change to run_bindcraft.py. Files left staged were swept in by a
later `git commit`. The commit is already pushed and is not being rewritten.
The substance is unaffected -- 81839f9 predates every v2 result -- but the
message under-describes its contents, and this note is the correction.

### The revised hotspot set underperformed at n=2; reverting it

`[measured]` Run tnfa-v2-smoke, hotspots B32,B65,B145,C86,C87, gate-mode
prereg, 2 attempts, $1.06. Both trajectories completed and both produced
accepted designs *only because the stock thresholds were nulled*. MPNN
variants after AF2 re-prediction:

| trajectory | i_pTM (re-predicted) |
|---|---|
| tnfa_l79_s137625 | 0.38, 0.49, 0.51, 0.53 |
| tnfa_l90_s948572 | 0.11, 0.11, 0.18, 0.19 |
| **v1, old set, for comparison** | **0.71 - 0.78** |

`[measured]` l90 reached i_pTM 0.86 during trajectory optimisation and
collapsed to 0.11-0.19 after MPNN redesign and independent re-prediction.
**Trajectory-stage confidence is not evidence of a real interface** and is not
used as such anywhere in this project from here on.

`[computed]` Hotspot-set dispersion, side-chain centroids:

| set | max pair | Rg |
|---|---|---|
| v1 B32,B143,B146,C86,C87,C90 | 26.7 A | 10.7 A |
| v2 B32,B65,B145,C86,C87 | **30.4 A** | 12.0 A |
| B32,B145,C86,C87 | 24.1 A | 10.0 A |

Adding B65 widened the aiming set by ~4 A, with B65-C86 the widest pair at
30.4 A. For a 79-90 aa binder that is close to its full long dimension.

**Caveat, stated plainly:** v1's 0.71-0.78 is from the single trajectory of 22
whose variants were logged, so it is a best-of-22 against v2's both-of-2. n=2
cannot establish that the new set is worse. The decision rests on asymmetry,
not proof: there is no evidence the revised set is better, there is a
mechanistic reason to expect it to be worse, and the proven set costs the same
to run.

**Decision: revert the hotspot set to the v1 configuration for the fan-out**
and keep the i_pTM-floor and prereg-gate fixes. Two variables were changed at
once (gate and hotspots) and the result was confounded; the gate fix is
confirmed working, so the hotspot change is the one to withdraw. This isolates
one variable per run.

**K65 remains a pH anchor.** Dropping B65 as a BindCraft *aiming point* does
not remove it as a histidine target: hotspots steer where the binder lands,
and the variant round places histidines against whichever conserved cations
fall within reach of the realised interface. R32 and K65 are 16.4 A apart
(closest cationic nitrogens), so a binder landing on B32 will very likely have
K65 in reach. The revised pH variant rule in Amendment 1 is unchanged.

**Distance conventions, to stop these being conflated:** 16.4 A (R32-K65) is
closest-cationic-nitrogen to closest-cationic-nitrogen and governs histidine
placement. 19.6 A for the same pair is side-chain centroid to centroid and
governs binder footprint. Both are correct for their purpose; neither
substitutes for the other.

---

## Amendment 2 — 2026-10-11, before any cross-reactivity result exists

Written while the first Boltz fold is still running. No human-vs-mouse number
has been seen for any design.

### ipSAE_min is a harsher test on this target than where it was calibrated

`[computed]` ipSAE_min is defined as the minimum over (binder <-> target
subchain) directional pairs -- deliberately, "the weakest side of the
interface". On challenge 1 the target was a **single chain**, so ipSAE_min was
the weakest direction of one interface.

TNF-alpha's receptor site exists only in the groove between two protomers, so
our target is **two chains**, and the epitope is lopsided by design: the
protomer-1 face carries 32/143/145/146 and the protomer-2 face carries
86/87/90. ipSAE_min is therefore set by whichever protomer contributes the
*thinner* contact, even when total binding is strong.

`[literature]` The 0.60 operating point comes from bioRxiv 2025.08.14.670059
and is consistent with the AUC 0.615 crossover on the Adaptyv N~2600 set --
both single-chain-target data. **Applying 0.60 to a two-protomer groove is not
a like-for-like application of the calibration.** It is stricter, by an amount
we have not quantified and cannot quantify before the deadline.

### Decision, fixed now: the threshold does not change

**ipSAE_min >= 0.60 stands, unchanged.** We are recording that it is strict
here, not relaxing it. A threshold loosened after seeing which designs it
excludes is not a threshold, and this project's only real asset is that its
criteria predate its results.

What changes is **reporting, not gating**: alongside ipSAE_min we report the
per-pair ipSAE values (binder<->protomer-1 and binder<->protomer-2, both
directions), which `_compute_ipsae` already returns in `pairs`. That lets a
near-miss be diagnosed as "thin second-protomer contact" rather than "weak
interface", which is information a reader needs and which the single number
hides. It does not promote any design.

Designs landing at 0.55-0.59 are **failures** under the pre-registered gate.
They may enter the submission only under the rule already written in this file
-- if fewer than three designs pass, submit the passers plus the next-best by
composite, explicitly labelled as near-misses. No new rule is created here.

### Code correction that affects this metric (commit 1850f24)

`[measured]` `_compute_ipsae` scored **every** ordered inter-chain pair. With a
multi-protomer target that silently included the **protomer-protomer**
interface in ipSAE_min. Because a dimer is not TNF-alpha's native state, a
poorly modelled protomer-protomer packing could have set ipSAE_min for every
design identically -- presenting as "no binder works" when it in fact meant
"the target multimer was modelled badly". Pairs are now restricted to those
involving the binder chain.

`[computed]` This does **not** change any challenge-1 number. With a
single-chain target every inter-chain pair already involved the binder, so the
fix is a verified no-op there (2-chain: A->B, B->A both retained; 3-chain:
A->B, B->A excluded). The EGFR submission's reported metrics stand as
submitted.

### Target multimer state — decision recorded in advance

We co-fold the binder against **two** protomers, matching the two-chain slice
the designs were made against. TNF-alpha's biological unit is a **trimer**, so
this is a known approximation.

Rule fixed now: if the smoke fold shows the two protomers failing to pack into
the groove geometry seen in 7KPB, the two-protomer result is **discarded, not
reported**, and the comparison is re-run against three protomers. We do not
report a mouse-vs-human difference computed on a target that did not fold into
the right state, in either direction.

### Significance, not eyeballing

Cross-reactivity is scored as `|human_mean - mouse_mean|` against a noise floor
of `max(human_range, mouse_range)` over diffusion samples, with the verdict
`REAL` only when the difference exceeds that floor. Means over samples, never
best-of-N. A difference inside the noise floor is reported as
**indistinguishable** -- which, for objective 2, is the outcome we want and is
not the same as "no difference measured".

---

## Amendment 3 — 2026-10-11, before the trimer run

Written after three dimer folds and before any trimer fold. Prompted by
checking the code rather than by a result we disliked.

### Measured: ipSAE's interface selection is over-inclusive on this target

`[measured]` Dunbrack's interface rule (cross-chain PAE <= 10 A and pLDDT >= 70)
classifies **104-136 of 157 target residues** as interface on our dimer folds.
Our own heavy-atom contact analysis puts the real interface at ~15-20 residues
per protomer. Boltz is confident about the whole rigid complex, so most of each
protomer qualifies, and ipSAE is then averaged over ~130 residues of which ~20
are contacts. The score is diluted by construction.

This is not a defect in the implementation -- it is the published definition
meeting a target type it was not calibrated on. The calibration (bioRxiv
2025.08.14.670059; Adaptyv N~2600) is single-chain-target data.

`[measured]` The metric is not uniformly broken here: tnfa_l69_s930894_mpnn1's
strong groove wall reaches ipSAE **0.58-0.66** (C->A 0.6236, 0.6553), clearing
0.60. The weak wall (0.21-0.41) sets ipsae_min.

### Measured: a two-protomer target is orientationally ambiguous

`[measured]` A dimer has one interface and Boltz builds it in either
orientation. Across three diffusion samples of l69_mpnn2 the binder's H4 sat
8.3 A from A65 (sample 0), 8.2 A from B65 (sample 1), 10.0 A from A65 (sample
2) -- the protomers swapping which plays the face-1 role. ipsae_min samples
were [0.2783, 0.2219, 0.0789], **range 0.1994**, which fails our own
"sample range > 0.15 = poorly determined" convention.

Per Amendment 2 this result is therefore **discarded, not reported**, and the
comparison moves to three protomers, whose packing is directional and
unambiguous (in 7KPB protomer A contacts B with 248 atom pairs and C with 166 --
asymmetric, so each protomer's role is fixed).

### Fixed now: how trimer ipSAE will and will not be used

`[inferred]` On a trimer the binder occupies one groove and touches two of three
protomers. A pair with no interface residues is excluded from ipsae_min
(n_int == 0 -> None), but given that 104-136 residues qualify under the
permissive rule above, the **uncontacted** protomer may still register
n_int > 0, score spuriously low, and dominate ipsae_min for every design.

Decisions, fixed before the run:

1. **Trimer ipsae_min is NOT compared to the 0.60 operating point.** Not
   because 0.60 is inconvenient -- Amendment 2 already refused to move it --
   but because a trimer-derived value is not on the scale the threshold was
   calibrated on. A number that is not comparable is not evidence either way,
   and we will say so rather than quietly pass or fail designs on it.
2. **The trimer run is used for objective 2 only: the human-vs-mouse
   difference.** Any artefact that deflates the absolute value deflates both
   species identically, so a paired comparison survives what would destroy an
   absolute threshold. This is the whole reason the run is still worth doing.
3. **Per-pair ipSAE is reported restricted to protomers the binder actually
   contacts** (atom_pairs > 0, from the interface report). Pairs to an
   uncontacted protomer are reported separately and excluded from any summary
   statistic, because a chain that is not touched is not a side of the
   interface.
4. **The affinity gate is unchanged and is carried by SC >= 0.58** (Rosetta, on
   the design models) plus the AF2 interface metrics, exactly as already
   recorded. Boltz contributes the species comparison and a qualitative
   sanity check on binding mode, not the affinity decision.

### Consequence for objective 3, stated plainly

`[measured]` In all three dimer samples **no binder histidine came within
6.0 A of R32 or K65** -- H4's closest approach to any anchor was 8.2-10.0 A,
against the 3.0-5.4 A that AF2 reported for H4->R32. Some of that is the
orientation ambiguity, which the trimer should remove.

But if the trimer also shows no anchor within 6.0 A, then **our objective-3
evidence rests on AlphaFold2 alone**, and the writeup will say that in those
words. It will not describe the pH mechanism as independently confirmed, and it
will not report the AF2 geometry without noting that a second predictor did not
reproduce it. Recorded now, while the trimer result is unknown.

---

## Amendment 4 — 2026-10-11, before the 10-sample run

Written after the 3-sample run proved non-reproducible and before any 10-sample
fold exists.

### Why the sampling changes

`[measured]` The 3-sample protocol does not repeat. On identical input, across
two independent runs of **l69_mpnn2**:

| | run 1 | run 2 |
|---|---|---|
| mouse ipSAE (contacted-restricted) | 0.509 | **0.385** |
| human pH anchors satisfied | 2 of 3 | **1 of 3** |
| pre-registered >=2-of-3 verdict (human) | **passes** | **fails** |

Three of four completed species comparisons also exceeded our own
`sample range > 0.15 = poorly determined` threshold. Boltz is deterministic
without a seed, so the most likely cause is differing MSAs from a ColabFold
server that returned 48 errors during the run.

The defect is **precision, not coverage**. Folding the remaining 8 designs at
3 samples would yield twelve unreliable numbers instead of four. Raising the
sample count on the designs that matter addresses the actual problem.

### What changes, fixed now

**diffusion_samples 3 -> 10**, on the three top-ranked designs only
(l69_mpnn2, l69_mpnn1, l91_mpnn2). This is a change toward more precision; no
threshold is being moved.

**The pH rule translates as a proportion, not a count.** ">=2 of 3 samples"
is 66.7%, so at n=10 it becomes **>=7 of 10**. Stated before results so the
bar cannot be chosen to fit them.

**The 0.15 range threshold does NOT transfer to n=10.** The observed range of a
sample grows with sample size even from an identical distribution, so a range
computed over 10 draws is not comparable to one computed over 3. We will:

- report mean, SD and range at n=10, and the range **without** comparing it to
  the n=3 threshold;
- keep the species verdict in its existing form -- `|human - mouse|` against a
  noise floor of the larger per-species range -- noting that at n=10 this is
  **more** conservative than at n=3, because the floor grows. A REAL verdict
  under this test at n=10 is therefore harder to obtain, not easier.

### What this run cannot fix

`[inferred]` If the MSA server is still degraded, a 10-sample run inherits the
same instability at higher cost. The run is therefore capped and time-boxed: if
it has not completed by 02:30 PDT, it is abandoned and the submission goes
forward on the evidence already recorded, with objective 2's computational
comparison reported as indeterminate exactly as currently written.

Nothing in the submission depends on this run succeeding. It is upside over a
writeup that is already complete and already honest about what it lacks.
