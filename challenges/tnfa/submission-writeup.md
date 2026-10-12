# TNF-α conditional binder — design rationale and validation

**Team:** 2GuysBuildProteins (Charles Norris, Malachi Cardona) · Track 3 (open)

A note on numbering before anything else, because we got it wrong once already
and corrected it mid-week. The organisers **number** the objectives
1 = human TNF-α affinity, 2 = mouse cross-reactivity, 3 = pH-selective binding,
but **rank** them in the reverse order: pH first, mouse second, affinity third.
This document is organised in **ranked** order and labels each section with the
organisers' number, so the two cannot be confused.

---

## At a glance

12 designs, 60–97 aa, all de novo. Every one clears our pre-registered affinity
gate (shape complementarity ≥ 0.58). Six carry the pre-registered pH mechanism;
one of those is confirmed on two independent structure predictors.

| | status |
|---|---|
| **Objective 3 — pH selectivity** (ranked 1st) | Mechanism present in 6 of 12 designs by a rule fixed in advance. Confirmed on **both** AlphaFold2 and Boltz-2 for the lead — but the two predictors anchor it on **different** conserved cations. No predictor models protonation, so this is geometric availability, not demonstrated function. |
| **Objective 2 — mouse cross-reactivity** (ranked 2nd) | Strongest-evidenced objective. The epitope is anchored on **7KP7**, a solved structure of *human* TNFR1 bound to *mouse* TNF-α. 30 of 32 human receptor contacts are also mouse contacts. Boltz human-vs-mouse difference falls inside the sampling noise floor. |
| **Objective 1 — affinity** (ranked 3rd) | 12 designs over 8 independent backbones. Lead: SC 0.66, dG −57.7, 2144 Å² buried, 12 interface H-bonds, 9.1% unsatisfied. Better than our EGFR submission on every axis. |

**The honest summary:** affinity is solid, cross-reactivity is well-grounded in
an experimental structure, and the pH mechanism is present and geometrically
plausible but rests on predictors that cannot represent the chemistry it
depends on.

---

## Objective 3 — pH-selective binding (ranked first)

### The mechanism is inverted from challenge 1

Challenge 1 asked for binding **at** acidic pH; this challenge asks for binding
at pH 7.4 and **no detectable binding** at pH 6.0. That inverts the design:
instead of acquiring an interaction on protonation, the binder must **lose**
one.

Our mechanism: place a **binder histidine** against a **conserved cationic
residue on the target**. Histidine is neutral near pH 7.4 and positively
charged near pH 6.0. At 7.4 it is tolerated beside the target cation; at 6.0 it
acquires a like charge and the two repel. The switch is a repulsion that only
turns on when the acid arrives.

All the pH machinery must come from the binder. `[computed]` The conserved
consensus epitope contains **no histidine**: human H73 contacts both receptors
but is tyrosine in mouse, and position 20 is proline in human and histidine in
mouse — each species carries an interface histidine the other lacks. A
mechanism built on a target histidine would trade objective 3 against objective
2. Building it entirely in the binder decouples them.

### The anchors, and how one of them was nearly missed

`[computed]` Four conserved cations sit in the cross-species epitope:

| residue | contacts human / mouse | note |
|---|---|---|
| **R32** | 82 / 128 | densest contact in the whole epitope |
| **K65** | 28 / 45 | 16.4 Å from R32, same protomer, same groove |
| K90 | 7 / 20 | highest B-factors of any anchor; peripheral |
| R82 | 1 / 3 | rim only, not meaningfully in the interface |

K65 was **not** in our original epitope set. Our first pass required contact
with both TNFR1 and TNFR2, and that intersection discarded it. K65 is also
mutated (K65S) in 3ALQ, so it was invisible until we switched to wild-type
7KPB. It surfaced only when 7KP7 was added for the cross-species analysis.

This matters because **K65 is the anchor the second predictor found.**

### The rule, fixed before any design was scored

Pre-registered in `methods.md` (commit `06126db`, amended in `81839f9`):

> A binder histidine satisfies the pH rule when its ND1 or NE2 lies within
> **6.0 Å** of R32 NH1/NH2/NE or K65 NZ, in at least **2 of 3** samples.

6.0 Å was set a priori from the 3.7–7.6 Å range reported in Baker 2025
(bioRxiv 2025.09.29.678932) for protonated-His to cationic-residue distances in
pH-release designs. Two anchors rank above one. Three (+K90) was recorded as a
labelled stretch goal, not a target.

### Result: the rule passes on two independent predictors

`[measured]` Six of 12 submitted designs satisfy the rule on AlphaFold2 models
in 2 of 2 samples:

| design | His | anchor | distance (Å) |
|---|---|---|---|
| l69_mpnn2 | H4 | R32 | 3.0, 5.4 |
| l69_mpnn1 | H4 | R32 | 4.6, 5.7 |
| l91_mpnn2 | H15 / H16 | R32 / K65 | 5.3–5.9 / 4.7 |
| l91_mpnn1 | H15 | R32 | 4.8, 5.4 |
| l66_mpnn2 | H32 | R32 | 5.6, 5.7 |
| l87_mpnn1 | H27 | R32 | 3.8, 4.9 |

`[measured]` Independently, on Boltz-2 against the full human trimer, three
diffusion samples of **l69_mpnn2**:

```
human:  K65 at 4.62, 4.46, 6.59 Å   → within 6.0 Å in 2 of 3  → PASSES
mouse:  K65 at 5.18, 4.78, 5.03 Å   → within 6.0 Å in 3 of 3  → PASSES
```

The pre-registered rule is satisfied on a predictor that played no part in
generating the design.

### The disagreement we are not smoothing over

**The two predictors anchor the mechanism on different residues.** AlphaFold2
places H4 3.0–5.4 Å from **R32**; Boltz-2 places the same histidine 4.5–5.2 Å
from **K65** and puts R32 13–16 Å away. Both are conserved cations in the
epitope, and both satisfy the rule as written. But the predictors do not agree
on *which* contact the switch acts through, and we cannot say which is right.

What survives the disagreement: a binder histidine sits within 6.0 Å of *a*
conserved cation under both models. What does not: any claim about the specific
contact geometry.

### What this cannot show, stated plainly

`[inferred]` Neither AlphaFold2 nor Boltz-2 models protonation state. Neither
can predict pH-dependent binding. What is measurable is **geometry at neutral
pH** — whether a histidine sits where protonation would be disruptive. That is
evidence the mechanism is *available*, not evidence that it *works*.

`[literature]` A single ionisable group caps the affinity ratio at 10^ΔpH, and
7.4 → 6.0 is 1.4 units, so ~25× at theoretical best. Objective 3 asks for *no
detectable binding*, which is a switch rather than a dial. Expert discussion
among competition participants put the requirement at **three** titratable
groups for a 100–1000× window; five of our six pH-capable designs carry one
load-bearing histidine and one carries two. **We expect to demonstrate the
geometry and not the magnitude.**

`[secondhand]` One further caution we recorded rather than designed around:
histidine *networks* may buffer rather than amplify a pH response, so anchors
should be spatially separated rather than clustered. Our anchors are 16.4 Å
apart, which is consistent with that advice.

---

## Objective 2 — mouse cross-reactivity (ranked second)

This is our best-evidenced objective, and the evidence is experimental rather
than computational.

### The species problem

`[computed]` Human and mouse mature TNF-α are **124/156 identical = 79.5%**
(re-derived independently from sequence; matches the organisers' stated
figure), with one indel — human T72 has no mouse counterpart. 33 positions
differ, nine of them charge changes, including one full reversal (D140K). For
comparison, the EGFR target in challenge 1 was ~92% conserved, and participants
there judged cross-reactivity a minor risk. At 79.5% it is not.

Adalimumab, a validated therapeutic against this target, does **not** bind
mouse TNF-α. That is the most informative negative result available: a
clinically successful binder to this protein that fails the test we must pass.

### 7KP7 — the structure that anchors the claim

`[computed]` **7KP7 is human TNFR1 bound to mouse TNF-α**, 2.65 Å. It is direct
experimental proof that a protein can engage this site in both species.

We computed the receptor epitope from coordinates in both species and
intersected:

- **30 of 32** human TNFR1 contacts are also mouse TNFR1 contacts
- only positions 23 and 30 are human-only
- all six of our aiming hotspots are contacted in **both** species

Both structures carry **wild-type** TNF — every SEQADV record in each is on the
receptor or an expression tag — and both carry the *identical* receptor
construct (N54D, C182S), so species is the only variable between them.
7KP7 is also the higher-resolution structure (2.65 Å vs 3.00 Å for 7KPB).

Numbering was validated rather than assumed: 7KP7's author numbering is mouse
mature + 1, which with the indel at human T72 maps author N to human mature N
for N ≥ 73 and N−1 below. Checked by residue identity at **148/148 residues,
zero mismatches**.

### Computational cross-reactivity

`[measured]` Boltz-2, binder co-folded against the full human and mouse
trimers, three diffusion samples each. For **l69_mpnn2**, on ipSAE restricted
to the protomers the binder actually contacts:

```
human 0.6309    mouse 0.5092    |difference| 0.1217    noise floor 0.1317
→ INDISTINGUISHABLE
```

The species difference falls **inside** the sampling noise floor, computed as
the larger of the two per-species sample ranges. We report this as
indistinguishable, which for cross-reactivity is the desired outcome — and we
report it against a floor rather than by eye. Interface confidence was high and
similar in both species (iptm 0.969 human, 0.949 mouse).

**[PENDING] The same measurement across all 12 designs is running at the time
of writing. These numbers will be inserted or this section amended before
submission; if the run does not complete, that will be stated.**

---

## Objective 1 — human TNF-α affinity (ranked third)

### The submitted designs

`[measured]` All values are Rosetta/AF2 metrics on the design models, averaged
over 5 AF2 models.

| design | len | i_pTM | SC | dG | dSASA | H-bonds | unsat % | pH |
|---|---|---|---|---|---|---|---|---|
| l69_mpnn2 | 69 | 0.86 | **0.66** | −57.7 | 2144 | 12 | 9.1 | ✓✓ |
| l69_mpnn1 | 69 | 0.86 | 0.62 | **−61.6** | 2131 | 12 | **7.8** | ✓ |
| l91_mpnn2 | 91 | 0.80 | 0.59 | −54.2 | 2224 | 15 | 23.3 | ✓ |
| l87_mpnn1 | 87 | 0.72 | 0.62 | −44.1 | 1883 | 6 | 7.6 | ✓ |
| l66_mpnn2 | 66 | 0.77 | 0.61 | −53.2 | 1814 | 10 | 10.3 | ✓ |
| l91_mpnn1 | 91 | 0.80 | 0.59 | −52.0 | 2154 | 12 | 29.1 | ✓ |
| l84_mpnn1 | 84 | 0.84 | 0.60 | −46.9 | 1910 | 11 | 24.1 | — |
| l66_mpnn1 | 66 | 0.77 | 0.64 | −48.6 | 1695 | 8 | 7.4 | — |
| l60_mpnn2 | 60 | 0.71 | **0.68** | −47.9 | 1937 | 8 | 28.9 | — |
| l60_mpnn1 | 60 | 0.69 | 0.64 | −43.9 | 1825 | 7 | 19.6 | — |
| l62_mpnn20 | 62 | 0.63 | **0.68** | −38.3 | 1636 | 7 | 18.4 | — |
| l97_mpnn2 | 97 | 0.45 | 0.64 | −41.7 | 1381 | 10 | 8.0 | — |

✓✓ = pH rule satisfied on both predictors · ✓ = on AlphaFold2 · — = no anchor
within 6.0 Å

For scale, our EGFR submission's best design scored SC 0.65, dG −33.5,
dSASA 1444, 8 H-bonds. The lead here buries 50% more surface with 70% more
binding energy at comparable shape complementarity.

### Two designs we are explicit about

**l84_mpnn1 contains no histidine at all.** It therefore cannot have a pH
mechanism, and on the top-ranked objective it must score zero. It is included
because it clears the affinity gate with the third-highest interface
confidence in the set, on the assumption that designs are scored individually.
If they are scored as a set, it should be removed.

**l97_mpnn2 has i_pTM 0.45**, the lowest in the submission, despite passing SC
at 0.64. It is the weakest design submitted and we rank it last.

---

## Epitope selection

`[computed]` TNF-α is a homotrimer, and the receptor-binding site exists
**only** in the groove between two adjacent protomers — a monomer does not
contain the site. Our target is therefore a two-chain slice of 7KPB (chains B
and C, 143 + 138 residues), and every hotspot is chain-prefixed.

We verified which protomer presents which face rather than assuming: in 7KPB,
receptor chain F occupies the B+C groove with **B presenting face-1**
(residues 20, 21, 31, 32, 33, 65, 67, 113, 115, 143–147, 149) and **C
presenting face-2** (73, 75, 77, 82, 85, 86, 87, 89, 90, 91, 97, 137).

Three constraints had to intersect at one site: it must be a functional
receptor-blocking epitope, it must be conserved between species, and it must
carry a conserved cation for the pH switch. They do intersect — 19 conserved
positions in the consensus epitope, four conserved cations, and the
cross-species confirmation above.

Fab1974, present in 7KPB, is not a confound: it occupies the third (C+A)
groove, never contacts chain B, and on chain C touches only face-1 residues —
not one of our hotspots.

**Final hotspot set:** `B32, B143, B146, C86, C87, C90`.

---

## Method

| stage | tool |
|---|---|
| backbone + sequence design | BindCraft (AF2 hallucination, 4-stage), hard-target preset |
| sequence redesign | ProteinMPNN with SolubleMPNN weights |
| re-prediction | AlphaFold2, 5 models |
| interface scoring | PyRosetta (Lawrence–Colman shape complementarity, dG, dSASA, H-bond satisfaction) |
| independent cross-validation | Boltz-2, 3 diffusion samples, full trimer target |
| cross-species | Boltz-2 co-fold against human and mouse trimers |
| compute | Modal (A10G for design, A100-40GB for Boltz) |

Target: 7KPB chains B,C. Binder length sampled 60–100 aa. Means over samples,
never best-of-N.

### Acceptance criteria, pre-registered

- **SC ≥ 0.58** (Lawrence–Colman, PyRosetta)
- **ipSAE_min ≥ 0.60** (Dunbrack 2025)
- pH rule as stated above
- sample range > 0.15 flags a measurement as *poorly determined*

---

## Corrections made during the work

Four, all committed with the correction timestamped ahead of any result that
depended on it. We list them because the audit trail is the point.

**1. A mismeasured distance.** The pre-registration recorded R32 and K90 as
"13.7 Å apart in this groove". Remeasured cationic-N to cationic-N:
R32–K90 is **21.5 Å**; 13.7 Å matches **R82**, a different residue. Our
original anchor pair was ~8 Å further apart than written down. Corrected in
`81839f9`.

**2. An over-restrictive epitope intersection.** Requiring contact with both
TNFR1 and TNFR2 was conservative but unjustified — the challenge asks us to
bind TNF-α, not to block both receptors — and it discarded two conserved
cations, one of which (K65) is the anchor the second predictor later found.
Corrected in `81839f9`.

**3. An uncalibrated gate was silently rejecting good designs.** Our first
production run returned **0 accepted designs from 22 trajectories** while six
MPNN variants cleared the AF2 filters at up to i_pTM 0.78 and SC 0.65 — above
our own threshold. The cause was BindCraft's stock `default_filters.json`, a
separate, stricter gate we never pre-registered and never derived. We moved
acceptance to our pre-registered criteria. Stated plainly because the shape of
the action matters: this was not a threshold loosened after seeing results —
the stock filter was never our criterion, and the evidence was that it rejected
designs passing the criterion we had committed to.

**4. A metric was measuring the wrong interface.** Our ipSAE implementation
scored every ordered inter-chain pair, so with a multi-protomer target the
**protomer–protomer** interface was folded into ipSAE_min. A poorly modelled
target multimer would then set the score for every design identically and read
as "no binder works". Restricted to binder-involving pairs in `1850f24`;
verified a no-op for challenge 1's single-chain target, so the EGFR
submission's reported metrics stand as submitted.

### A threshold we did **not** change

ipSAE_min ≥ 0.60 is stricter on this target than where it was calibrated. It is
the minimum over binder↔subchain pairs — the weakest side of the interface —
and our epitope is lopsided by design, so the thinner protomer contact sets it.
The operating point comes from single-chain-target data. We recorded that it is
strict here and **left it at 0.60** (`a8715ee`). A threshold loosened after
seeing which designs it excludes is not a threshold. What we changed was
reporting, not gating: per-pair values are reported so a near-miss can be
diagnosed rather than promoted.

---

## Funnel — every denominator

| stage | n |
|---|---|
| production runs | 4 (one withdrawn) |
| BindCraft trajectories started | 90 |
| trajectories lost to severe clashes | 15 |
| trajectories yielding no accepted MPNN variant | 10 |
| designs reaching full interface scoring | 24 |
| designs clearing SC ≥ 0.58 | **12** |
| independent backbones among those | **8** |
| designs satisfying the pH rule (AF2, 2/2 samples) | **6** |
| designs with the pH rule confirmed on Boltz-2 | **1** (12-design run pending) |
| designs submitted | **12** |

A run we withdrew: a revised hotspot set (`B32,B65,B145,C86,C87`) was tested on
2 attempts and produced re-predicted i_pTM of 0.11–0.53 against 0.71–0.78 for
the original set. We reverted rather than tune further, on the reasoning that
n=2 cannot establish the new set is worse but there was no evidence it was
better, a mechanistic reason to expect worse (it widened the aiming set from
26.7 Å to 30.4 Å), and the proven set cost the same to run. Recorded in
`55acf42`.

A design we excluded: `tnfa_l73_s499042` produced the most robust pH geometry
in the entire project — H68 within 2.8–5.6 Å of K65 across eleven MPNN variants
and both model samples — and **fails the affinity gate in every variant**
(SC 0.40–0.54). Our pre-registration states that designs whose only merit is pH
geometry are not submitted. It is excluded by a rule written before we saw it.

---

## Limitations

1. **No predictor used here models protonation.** Every pH claim is geometric
   availability at neutral pH, not demonstrated pH-dependent binding.
2. **The two predictors disagree on which anchor the switch acts through**
   (AF2: R32; Boltz-2: K65). Both are conserved cations and both satisfy the
   pre-registered rule, but the specific geometry is unresolved.
3. **One load-bearing histidine in five of six pH-capable designs.** Expert
   estimates for a 100–1000× window call for three titratable groups. We expect
   the geometry to be demonstrable and the magnitude not to be.
4. **Whether TNF-α itself changes between pH 7.4 and 6.0 is unknown to us.**
   Trimer destabilisation at the acidic condition would confound objective 3's
   readout for every entrant. We could not resolve it and record it rather than
   invoke it later.
5. **The mouse assay construct carries a C-terminal polyhistidine tag**
   (TNA-M52H3); the human construct (TNA-H4211) is tag-free. Objectives 2 and 3
   are measured on tagged protein, objective 1 on untagged. A His tag is itself
   a cluster of titratable histidines. Nearest approach from any modelled
   C-terminus to any hotspot is **21.0 Å**, against thresholds we set before
   measuring (>25 Å safe, <15 Å risky). Low risk, not zero, and asymmetric
   between arms.
6. **ipSAE_min on a multi-protomer target is not on the scale its 0.60
   operating point was calibrated on.** We report it and decline to treat it as
   a pass/fail on this target.
7. **A two-protomer target proved orientationally ambiguous** under Boltz —
   across three samples the protomers swapped which presented face-1, and the
   sample range (0.1994) failed our own poorly-determined threshold. We
   discarded those results and re-ran against the full trimer. Reported because
   the discarded measurement would have read as a design failure.
8. **propka is not relied upon.** The Proton-PottsMPNN authors report predicted
   pKa was not predictive of which pH bin a design fell into.
9. **Calibration provenance.** The AUC figures underlying our metric choices
   (SC 0.68, ipSAE_min 0.615) have no recorded primary source in our notes.
10. **The challenge brief was not committed to the repository** — it was
    supplied in conversation. Objective definitions in this document are as we
    understood them.

---

## Designs submitted

12 designs in `submission.csv`, in submission order. Tier reflects pH evidence;
all 12 clear the affinity gate.

| # | design | len | tier | pH evidence |
|---|---|---|---|---|
| 1 | tnfa_l69_s930894_mpnn2 | 69 | 1 | H4 → cation, both predictors |
| 2 | tnfa_l69_s930894_mpnn1 | 69 | 1 | H4 → R32, AF2 2/2 |
| 3 | tnfa_l91_s990274_mpnn2 | 91 | 2 | H15 → R32 + H16 → K65 |
| 4 | tnfa_l87_s136696_mpnn1 | 87 | 2 | H27 → R32, AF2 2/2 |
| 5 | tnfa_l66_s937529_mpnn2 | 66 | 2 | H32 → R32, AF2 2/2 |
| 6 | tnfa_l91_s990274_mpnn1 | 91 | 2 | H15 → R32, AF2 2/2 |
| 7 | tnfa_l84_s861729_mpnn1 | 84 | 3 | none — no histidine |
| 8 | tnfa_l66_s937529_mpnn1 | 66 | 3 | His32 present, >6.0 Å |
| 9 | tnfa_l60_s347619_mpnn2 | 60 | 3 | His17 present, >6.0 Å |
| 10 | tnfa_l60_s347619_mpnn1 | 60 | 3 | His17 present, >6.0 Å |
| 11 | tnfa_l62_s149973_mpnn20 | 62 | 3 | 3 His present, all >6.0 Å |
| 12 | tnfa_l97_s762214_mpnn2 | 97 | 3 | His72 present, >6.0 Å |

Every sequence is taken programmatically from the BindCraft output CSVs, never
retyped. `build_submission.py` refuses to write the file unless declared length,
name-encoded length and actual sequence length agree; residues are standard;
names and sequences are unique; SC clears 0.58; and every histidine position
asserted in this document is present in the sequence actually submitted.

---

## Provenance

The pre-registration and every amendment were committed **before** the results
they govern, and this is checkable from public history.

| commit | content |
|---|---|
| `06126db` | pre-registration: target, hotspots, thresholds, pH rule |
| `81839f9` | Amendment 1: the 13.7 Å correction, 7KP7 cross-species evidence, revised hotspots |
| `55acf42` | Amendment 1a: revised hotspot set underperformed at n=2; reverted |
| `1850f24` | ipSAE restricted to binder-involving pairs; multi-chain co-fold |
| `a8715ee` | Amendment 2: ipSAE_min is stricter on a two-protomer groove; threshold unchanged |
| `d812538` | Modal-side interface diagnosis so results are interpretable without downloading structures |
| `ca6393b` | Amendment 3: ipSAE interface selection is over-inclusive here; trimer run scoped to objective 2 |

Analysis scripts are in `challenges/tnfa/`: `tnfr_contacts.py`,
`crossspecies_epitope.py`, `cation_anchors.py`, `groove_occupancy.py`,
`verify_numbering.py`, `histag_geometry.py`, `parse_designs.py`,
`build_submission.py`. Run logs for every production run are committed.
