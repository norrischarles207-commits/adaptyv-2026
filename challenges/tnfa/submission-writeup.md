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
gate (shape complementarity ≥ 0.58). Six carry the pre-registered pH mechanism
on AlphaFold2. Three of those were then re-tested on a second, independent
predictor against a bar fixed before the run: **one passes in 10 of 10 samples
and is now our lead; two fail.**

| | status |
|---|---|
| **Objective 3 — pH selectivity** (ranked 1st) | Mechanism present in 6 of 12 designs by a rule fixed in advance, on AlphaFold2 (2 of 2 samples). Three were re-tested on an independent predictor (Boltz-2) at 10 diffusion samples against a ≥7-of-10 bar **fixed before that run** (Amendment 4): **`l69_mpnn1` passes 10/10 on human and 8/10 on mouse**; `l69_mpnn2` fails at 4/10 and `l91_mpnn2` at 3/10. The mechanism is therefore independently supported for one design and unsupported for two. We do not convert that into a reproducibility rate: three designs is too few to estimate one (1 of 3 is a 95% interval of 0.06–0.79). The nine untested designs should be read as untested, not as confirmed. No predictor models protonation. |
| **Objective 2 — mouse cross-reactivity** (ranked 2nd) | Rests on **structural** evidence: the epitope is anchored on **7KP7**, a solved 2.65 Å structure of *human* TNFR1 bound to *mouse* TNF-α, and 30 of 32 human receptor contacts are also mouse contacts. The computational comparison, re-run at 10 samples, now goes **against** us: both `l69` designs show a real human preference (diff 0.26 / 0.25 against noise floors 0.14 / 0.19), and only `l91_mpnn2` is indistinguishable under the pre-registered test. Amendment 4 pre-committed that a REAL verdict at n=10 is the *more* conservative reading, so we report a species gap rather than noise — and we also report that the pre-registered test is biased toward the answer objective 2 wants: an exact permutation test on the same data finds a species difference for **all three** designs, `l91_mpnn2` included (p = 0.004). Objective 2 has no computational support here. The pH anchor itself is satisfied in both species for the lead; what differs is predicted interface confidence. |
| **Objective 1 — affinity** (ranked 3rd) | 12 designs over 8 independent backbones. Lead (`l69_mpnn1`): SC 0.62, dG −61.6, 2131 Å² buried, 12 interface H-bonds, 7.8% unsatisfied — the best binding energy and the cleanest H-bond satisfaction in the set. Its sibling `l69_mpnn2` is higher on SC alone (0.66). Better than our EGFR submission on every axis. |

**The honest summary:** affinity is solid. The pH mechanism is, for one design,
confirmed on two independent predictors by a rule and a bar both fixed in
advance — the strongest result in this submission — while still resting on
predictors that cannot represent protonation at all. Cross-reactivity is
well-grounded in an experimental structure and **not** supported by our own
computation: the design that passes the pH test shows a species gap, and the
design that looks cross-reactive fails the pH test. We have not found one that
does both, and we say so rather than ranking around it.

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

### Result: confirmed on two predictors for one design, not for the other two

`[measured]` Six of 12 submitted designs satisfy the rule on AlphaFold2 models
in 2 of 2 samples:

| design | His | anchor | distance (Å) |
|---|---|---|---|
| l69_mpnn1 | H4 | R32 | 4.6, 5.7 |
| l69_mpnn2 | H4 | R32 | 3.0, 5.4 |
| l91_mpnn2 | H15 / H16 | R32 / K65 | 5.3–5.9 / 4.7 |
| l91_mpnn1 | H15 | R32 | 4.8, 5.4 |
| l66_mpnn2 | H32 | R32 | 5.6, 5.7 |
| l87_mpnn1 | H27 | R32 | 3.8, 4.9 |

`[measured]` The three top-ranked designs were then co-folded with Boltz-2
against the full human and mouse **trimers** at **10 diffusion samples** per
species. The bar — `≥7 of 10`, the proportional translation of the
pre-registered `≥2 of 3` — was fixed in Amendment 4 (`8a68de1`) **before any
10-sample fold existed**, so it could not be chosen to fit the result.

| design | human | mouse | verdict |
|---|---|---|---|
| **l69_mpnn1** | **10 / 10** — H4 → R32, 2.55–5.68 Å | **8 / 10** — H4 → K65, 4.04–5.64 Å | **passes both arms** |
| l69_mpnn2 | 4 / 10 | 4 / 10 | fails |
| l91_mpnn2 | 3 / 10 | 2 / 10 | fails |

**`l69_mpnn1` satisfies the pre-registered pH rule in every one of ten
independent samples on human TNF-α, and in eight of ten on mouse.** It carries
exactly one histidine, H4, so the contact is unambiguous — there is no second
histidine that could be supplying the hit. One human sample places H4 2.55 Å
from an R32 guanidinium nitrogen, which is hydrogen-bond distance: neutral
imidazole at pH 7.4, and a like-charge contact at van der Waals range once
protonated at 6.0. That is the designed mechanism, found by a predictor that
played no part in the design.

`[measured]` Two results that go the other way, reported with equal weight.
**l69_mpnn2 fails at 4 of 10.** At n=3 it had given 2/3 (pass) then 1/3 (fail);
ten samples resolve it decisively below the bar. The two designs differ by a
handful of MPNN substitutions and share the same backbone and the same H4 —
yet one positions that histidine reliably and the other does not. **l91_mpnn2
fails at 3 of 10**, which retires the two-anchor hypothesis for it: its H15 and
H16 do reach R32 and K65, but only in 3 of 10 samples.

`[computed]` **How strong is each of these three results, exactly?** The bar is
a proportion, so the right reading is binomial. Against the implied
per-sample rate the bar encodes (p₀ = 2/3):

| arm | hits | Wilson 95% CI | P(≤ observed \| p₀) | reading |
|---|---|---|---|---|
| l69_mpnn1 human | 10/10 | 0.72–1.00 | — | **strong**: P(≥10 \| p₀) = 0.017 |
| l69_mpnn1 mouse | 8/10 | 0.49–0.94 | — | clears the bar, but P(≥8 \| p₀) = 0.30 — **weak** |
| l69_mpnn2 human | 4/10 | 0.17–0.69 | 0.077 | below the bar, **not a rejection** |
| l69_mpnn2 mouse | 4/10 | 0.17–0.69 | 0.077 | below the bar, **not a rejection** |
| l91_mpnn2 human | 3/10 | 0.11–0.60 | 0.020 | below the bar, and a rejection |
| l91_mpnn2 mouse | 2/10 | 0.06–0.51 | 0.003 | below the bar, and a rejection |

Three distinctions this forces, which an earlier revision of this document
blurred by calling all three outcomes "confirmed" or "refuted":

1. **Only the human arm of `l69_mpnn1` is strongly supported.** Its mouse arm
   clears the ≥7-of-10 bar but is statistically consistent with p₀ — passing
   our bar is not the same as beating it. We report the pass, and we report
   that it is a weak pass.
2. **`l69_mpnn2` is not refuted, it is unsupported.** At 4 of 10 the
   one-sided probability under p₀ is 0.077 — below our bar, but not a
   rejection of the mechanism. Earlier wording that called it refuted was
   stronger than the data.
3. **`l91_mpnn2` is genuinely rejected**, on both arms (p = 0.020 and 0.003).
   The two-anchor hypothesis for it does not survive.

`[inferred]` We deliberately do **not** turn "1 of 3" into a reproducibility
rate for the untested nine. One success in three designs carries a 95%
interval of 0.06–0.79, which is no information. The honest statement is that
six designs carry an AlphaFold2 ✓, one of them has independent support, two
have been tested and did not get it, and nine are untested.

### The anchor disagreement, and how 10 samples resolved it

An earlier revision of this document reported that the two predictors anchored
the mechanism on **different** residues — AF2 on R32, Boltz-2 on K65 — and
treated that as an unresolved conflict. **Ten samples show that conclusion was
an artefact of three samples on the wrong design.**

| arm | anchor at n=10 | agrees with AF2? |
|---|---|---|
| l69_mpnn1, human | **R32 in 10 of 10** | **yes** |
| l69_mpnn1, mouse | K65 in 8 of 8 hits | no — switches anchor |
| l69_mpnn2, human | mixed R32 / K65, 4 hits | n/a, below bar |

On the human arm of the design that actually passes, Boltz-2 and AlphaFold2
**agree**: the anchor is R32, in all ten samples. The K65-only picture came
from `l69_mpnn2` at three samples, a design that we now know does not clear the
bar on either predictor-sample budget.

What remains genuinely open is the **species** switch: in mouse, the same
histidine anchors on **K65** rather than R32, in 8 of 8 hits. Both are
conserved cations inside our pre-registered anchor set `{R32, K65}`, and the
rule as written does not require the same one in both species — but it means
the switch may act through a different contact in the two orthologues. We
record that as a finding, not a problem solved.

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

### Computational cross-reactivity — the result goes against us

`[measured]` Boltz-2, binder co-folded against the full human and mouse
**trimers** at **10 diffusion samples** per species, on the three top-ranked
designs. The verdict form — `|human − mouse|` against a noise floor of the
larger per-species range — was fixed before the run, and Amendment 4
(`8a68de1`) pre-committed the reading that at n=10 this test is *more*
conservative than at n=3, because the observed range grows with sample size. A
REAL verdict here is therefore harder to obtain than the one we previously
declined to report.

Pre-registered `ipsae_min` (minimum over all binder↔protomer pairs):

| design | human mean [range] | mouse mean [range] | diff | floor | verdict |
|---|---|---|---|---|---|
| l69_mpnn1 | 0.5486 [0.1340] | 0.2933 [0.1390] | +0.2553 | 0.1390 | **REAL** |
| l69_mpnn2 | 0.5192 [0.0920] | 0.2673 [0.1945] | +0.2519 | 0.1945 | **REAL** |
| l91_mpnn2 | 0.5237 [0.2027] | 0.4150 [0.2357] | +0.1087 | 0.2357 | indistinguishable |

Restricted to the protomers the binder actually contacts — a post-hoc
diagnostic, not the pre-registered quantity — the same three verdicts hold
(0.6711/0.4061 REAL; 0.6465/0.3659 REAL; 0.6717/0.5552 indistinguishable). The
two metrics differ because on a trimer one protomer is *correctly* never
engaged, and its pair sets the all-pairs minimum; this is the effect Amendment
3 (`ca6393b`) anticipated when it ruled that trimer `ipsae_min` is **not** to
be compared against our 0.60 threshold. We do not compare it.

**So we report a species gap, not cross-reactivity.** Both `l69` designs
predict more confidently against human than mouse by a margin that clears its
own noise floor. The one design the pre-registered test calls indistinguishable,
`l91_mpnn2`, is also the one that fails the pH rule at 3 of 10 — and, as the
next section shows, its indistinguishability does not survive a stronger test
either. We did not find a design that satisfies both of the top-two objectives,
and we are not going to present the ranking as though we had.

### The pre-registered test is conservative in the direction that flatters us

`[computed]` Our pre-registered verdict compares a **difference of means**
against the **range of single samples**. That is a heuristic, not a
significance test, and it is underpowered: the range grows with sample size
while the precision of a mean improves, so at n=10 the floor inflates for a
reason unrelated to the difference being tested. Amendment 4 noted this and
called it "more conservative". That is true, and incomplete — **it is
conservative toward declaring no species difference, which is the answer
objective 2 wants.** The bias runs in our favour, so we are obliged to check
what a better test says.

An exact two-sided permutation test on the same 10-versus-10 samples,
enumerating all 184,756 splits, reported as a **post-hoc sensitivity analysis
and not as a re-gate**:

| design | diff | pre-registered verdict | exact permutation p |
|---|---|---|---|
| l69_mpnn1 | 0.2553 | REAL | 1.1 × 10⁻⁵ |
| l69_mpnn2 | 0.2519 | REAL | 1.1 × 10⁻⁵ |
| l91_mpnn2 | 0.1087 | **indistinguishable** | **4.4 × 10⁻³** |

**The two REAL verdicts are confirmed emphatically, and the one favourable
verdict does not survive.** `l91_mpnn2` — the only design our pre-registered
test called indistinguishable between species, and the design we would
otherwise have pointed to as our cross-reactivity candidate — shows a species
difference at p = 0.004 under an exact test.

We are **not** substituting this test for the pre-registered one. The verdict
column above is the verdict; swapping in a better statistic after seeing
results is precisely the move this document's audit trail exists to prevent.
But reporting only the pre-registered heuristic, while knowing that a stronger
test on the same data contradicts its one favourable result, would be
reporting selectively. **Under the stronger test, all three designs predict
more confidently against human than mouse.** Objective 2 has no computational
support in this submission, for any design we tested.

`[measured]` Two things do survive on the positive side, and they are narrow:

- **The pH anchor is satisfied in both species for the lead** — 10/10 human,
  8/10 mouse. Whatever the confidence gap, the switch geometry is not
  human-specific.
- **Groove engagement is clean in all 60 samples.** Every sample contacted
  exactly 2 of the 3 protomers, and `contacts_both_protomers` was true 10/10
  for all six folds. The binder is in the inter-protomer groove, in both
  species, every time. The orientational ambiguity that forced Amendment 2 on
  the two-protomer target is absent on the trimer.

`[measured]` **What this supersedes.** An earlier revision reported the
3-sample comparison for `l69_mpnn2` as `human 0.6309 / mouse 0.5092`,
indistinguishable, and reported the partial 12-design run as **indeterminate**
on the grounds that 3 of its 4 comparisons exceeded our
`sample range > 0.15 = poorly determined` threshold. Amendment 4 fixed in
advance that the 0.15 threshold does **not** transfer to n=10, since a range
over ten draws is not comparable to one over three. The n=10 measurement is the
one we report. It is less favourable to us than the measurement it replaces.

The objective-2 claim therefore rests entirely on the **structural** evidence
above — 7KP7, and 30 of 32 human receptor contacts shared with mouse — which
does not move between runs. Our own computation does not corroborate it for the
lead design.

---

## Objective 1 — human TNF-α affinity (ranked third)

### The submitted designs

`[measured]` All values are Rosetta/AF2 metrics on the design models, averaged
over 5 AF2 models.

| design | len | i_pTM | SC | dG | dSASA | H-bonds | unsat % | pH |
|---|---|---|---|---|---|---|---|---|
| l69_mpnn1 | 69 | 0.86 | 0.62 | **−61.6** | 2131 | 12 | **7.8** | ✓✓ |
| l69_mpnn2 | 69 | 0.86 | **0.66** | −57.7 | 2144 | 12 | 9.1 | ✗ |
| l87_mpnn1 | 87 | 0.72 | 0.62 | −44.1 | 1883 | 6 | 7.6 | ✓ |
| l66_mpnn2 | 66 | 0.77 | 0.61 | −53.2 | 1814 | 10 | 10.3 | ✓ |
| l91_mpnn2 | 91 | 0.80 | 0.59 | −54.2 | 2224 | 15 | 23.3 | ✗ |
| l91_mpnn1 | 91 | 0.80 | 0.59 | −52.0 | 2154 | 12 | 29.1 | ✓ |
| l84_mpnn1 | 84 | 0.84 | 0.60 | −46.9 | 1910 | 11 | 24.1 | — |
| l66_mpnn1 | 66 | 0.77 | 0.64 | −48.6 | 1695 | 8 | 7.4 | — |
| l60_mpnn2 | 60 | 0.71 | **0.68** | −47.9 | 1937 | 8 | 28.9 | — |
| l60_mpnn1 | 60 | 0.69 | 0.64 | −43.9 | 1825 | 7 | 19.6 | — |
| l62_mpnn20 | 62 | 0.63 | **0.68** | −38.3 | 1636 | 7 | 18.4 | — |
| l97_mpnn2 | 97 | 0.45 | 0.64 | −41.7 | 1381 | 10 | 8.0 | — |

**✓✓** = pH rule satisfied on AlphaFold2 (2 of 2) **and** on Boltz-2 at the
pre-registered ≥7-of-10 bar, in **both** species · **✓** = AlphaFold2 2 of 2,
not tested at n=10 · **✗** = AlphaFold2 2 of 2 but tested at n=10 and **below**
the bar · **—** = no binder histidine within the pre-registered 6.0 Å of R32 or
K65. Exactly one design is claimed as confirmed on two predictors; two were
tested on the second and did not clear the bar, and nine were not tested at
all. The strength of each result is quantified in Objective 3.

For scale, our EGFR submission's best design scored SC 0.65, dG −33.5,
dSASA 1444, 8 H-bonds. The lead here buries 48% more surface with 84% more
binding energy and 50% more interface H-bonds, at slightly lower shape
complementarity (0.62 against 0.65).

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

Five. The first four were committed with the correction timestamped ahead of
any result that depended on it. The fifth is a claim in an earlier revision of
this document that a later measurement showed to be wrong, and we have left the
retraction visible rather than quietly editing the claim away. We list them
because the audit trail is the point.

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

**5. We reported a predictor disagreement that was really a sampling artefact.**
An earlier revision of this document stated that AlphaFold2 and Boltz-2
anchored the pH mechanism on **different** residues — R32 and K65 respectively
— and listed that as an unresolved conflict in both Objective 3 and the
limitations. That conclusion came from three diffusion samples on `l69_mpnn2`.
At ten samples, on `l69_mpnn1` — the design that actually clears the
pre-registered bar — Boltz-2 places H4 against **R32 in 10 of 10 human
samples**, which *agrees* with AlphaFold2. The disagreement was an artefact of
too few samples on a design that does not pass. What remains is a narrower and
real finding: the anchor differs between **species** (R32 in human, K65 in
mouse), not between predictors. Corrected in this revision; the superseded
numbers are quoted in place so the change is checkable.

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
| designs with the pH rule met on Boltz-2 in >=2 of 3 samples | **1 of 4 attempted** (not reproducible between runs; 8 of 12 designs never folded — MSA server failure) |
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
2. **The anchor differs between species, not between predictors.** At 10
   samples the two predictors agree on R32 for the lead's human arm (10/10),
   retracting a disagreement we previously reported — see correction 5. But in
   mouse the same histidine anchors on **K65** in 8 of 8 hits. Both are
   conserved cations inside our pre-registered anchor set and the rule does not
   require the same one in both species, so the switch may act through
   different contacts in the two orthologues. Unresolved.
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
8. **The 3-sample Boltz protocol was not reproducible, and the 10-sample
   replacement covers only 3 of 12 designs.** At three samples the 12-design
   run stalled after 4 designs (48 ColabFold MSA-server errors, one 1800 s
   timeout), and the measurement did not repeat on identical input:
   l69_mpnn2's mouse score moved 0.509 → 0.385 and its human pH-anchor count
   2/3 → 1/3, flipping the pre-registered verdict. Boltz is deterministic
   without a seed, so the likely cause is differing MSAs from a failing server.
   We replaced that protocol with 10 samples on the three top-ranked designs
   (Amendment 4, fixed in advance), where the human arm is tight (SD
   0.030–0.065) and the mouse arm looser (SD 0.041–0.079). The n=10 numbers are
   what we report. **The cost is coverage: nine designs have no second-predictor
   evidence at all**, and of the three that do, one clears the bar, one falls
   below it without being rejected, and one is rejected.
9. **propka is not relied upon.** The Proton-PottsMPNN authors report predicted
   pKa was not predictive of which pH bin a design fell into.
10. **Calibration provenance.** The AUC figures underlying our metric choices
   (SC 0.68, ipSAE_min 0.615) have no recorded primary source in our notes.
11. **The challenge brief was not committed to the repository** — it was
    supplied in conversation. Objective definitions in this document are as we
    understood them.
12. **We cannot estimate how often our AlphaFold2 pH geometry reproduces.**
    Of the three designs re-tested on an independent predictor, one cleared the
    pre-registered bar and two did not. An earlier revision of this document
    turned that into "roughly one time in three"; that was an overclaim, since
    1 of 3 carries a 95% interval of 0.06–0.79. Six designs carry an AF2 ✓, one
    has independent support, and nine are untested — which is all we can say.
13. **Our pre-registered species test is biased toward the answer we wanted.**
    Comparing a difference of means to the range of single samples inflates the
    rejection threshold as sample size grows. It is conservative toward
    "no species difference", which is objective 2's desired outcome. An exact
    permutation test on the same data gives p = 1.1 × 10⁻⁵, 1.1 × 10⁻⁵ and
    4.4 × 10⁻³ for the three designs — so the one favourable pre-registered
    verdict is not robust. We report the pre-registered verdict as the verdict
    and the permutation test as a disclosed sensitivity analysis, because the
    error here would be to keep the flattering statistic quietly.
14. **The submission order was changed post-hoc.** The ≥7-of-10 bar was
    pre-registered before the run that produced it; the decision to let that
    result reorder slots 1, 2, 3 and 5 was made after seeing it. Disclosed
    under "Designs submitted"; no sequence was changed.

---

## Designs submitted

12 designs in `submission.csv`, in submission order. Tier reflects pH evidence;
all 12 clear the affinity gate. **Tier 1** is satisfied on AlphaFold2 (2 of 2)
*and* on Boltz-2 at the pre-registered ≥7-of-10 bar in both species. **Tier 2**
is AlphaFold2-supported at 2 of 2; where it was also tested at n=10 and fell
below the bar, that is stated. **Tier 3** clears the affinity gate with no
anchor inside 6.0 Å.

| # | design | len | tier | pH evidence |
|---|---|---|---|---|
| 1 | tnfa_l69_s930894_mpnn1 | 69 | **1** | H4 → R32, AF2 2/2; **Boltz 10/10 human, 8/10 mouse** |
| 2 | tnfa_l69_s930894_mpnn2 | 69 | 2 | H4 → R32, AF2 2/2; Boltz **4/10 — below bar** |
| 3 | tnfa_l87_s136696_mpnn1 | 87 | 2 | H27 → R32, AF2 2/2; not tested at n=10 |
| 4 | tnfa_l66_s937529_mpnn2 | 66 | 2 | H32 → R32, AF2 2/2; not tested at n=10 |
| 5 | tnfa_l91_s990274_mpnn2 | 91 | 2 | H15 → R32 + H16 → K65, AF2 2/2; Boltz **3/10 — below bar** |
| 6 | tnfa_l91_s990274_mpnn1 | 91 | 2 | H15 → R32, AF2 2/2; not tested at n=10 |
| 7 | tnfa_l84_s861729_mpnn1 | 84 | 3 | none — no histidine |
| 8 | tnfa_l66_s937529_mpnn1 | 66 | 3 | His32 present, >6.0 Å |
| 9 | tnfa_l60_s347619_mpnn2 | 60 | 3 | His17 present, >6.0 Å |
| 10 | tnfa_l60_s347619_mpnn1 | 60 | 3 | His17 present, >6.0 Å |
| 11 | tnfa_l62_s149973_mpnn20 | 62 | 3 | 3 His present, all >6.0 Å |
| 12 | tnfa_l97_s762214_mpnn2 | 97 | 3 | His72 present, >6.0 Å |

**This order was changed after the n=10 run, and the change is post-hoc.** The
≥7-of-10 bar was pre-registered; its consequence for submission order was not.
Slots 1 and 2 were swapped because objective 3 is ranked first by the
organisers and `l69_mpnn1` is the only design with two-predictor support for
it. `l91_mpnn2` fell from slot 3 to slot 5 because the pre-registered rule that
put it there — *"two anchors (R32 and K65) rank above one"*, methods.md — was
applied on a premise that n=10 then tested and rejected (3 of 10). No sequence
was altered; the file is byte-identical in length to the previous revision.

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
| `8a68de1` | Amendment 4: diffusion sampling 3 → 10 on the top 3 designs; **≥7-of-10 pH bar and the n=10 verdict form fixed before any 10-sample fold existed** |

Analysis scripts are in `challenges/tnfa/`: `tnfr_contacts.py`,
`crossspecies_epitope.py`, `cation_anchors.py`, `groove_occupancy.py`,
`verify_numbering.py`, `histag_geometry.py`, `parse_designs.py`,
`build_submission.py`, `analyze_n10.py`. Run logs for every production run are
committed, including `crossreact-n10.log` and the full per-sample record in
`crossreact-n10.json` — every ipSAE pair, every interface contact list and
every pH-anchor distance behind the tables above, so the n=10 claims can be
recomputed from source with `analyze_n10.py`.
