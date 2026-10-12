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
gate (shape complementarity ≥ 0.58). **All twelve have now been tested on a
second, independent structure predictor at 10 diffusion samples per species,
and the two that clear the pre-registered pH bar have each held it under
replication.**

| | status |
|---|---|
| **Objective 3 — pH selectivity** (ranked 1st) | Rule and bar both fixed before the runs that tested them (Amendments 4, 5). **Two designs are confirmed on the human arm across independent runs: `l69_mpnn1` at 30 of 30 samples over three runs, and `l91_mpnn1` at 19 of 20 over two.** Both anchor on R32 at hydrogen-bond distance. **Neither is confirmed on mouse** — `l69_mpnn1` cleared the bar in 2 of 3 mouse runs (pooled 20/30, exactly the bar's implied rate) and `l91_mpnn1` in 0 of 2. Six of twelve designs score a flat 0/10. The AlphaFold2 screen that selected the candidates is itself validated: AF2-positive designs average 5.83/10 on the second predictor against 0.33/10 for AF2-negative, permutation p = 0.015. No predictor models protonation, so this is geometric availability, not demonstrated pH-dependent binding. |
| **Objective 2 — mouse cross-reactivity** (ranked 2nd) | Rests on **structural** evidence: 7KP7, a solved 2.65 Å structure of *human* TNFR1 bound to *mouse* TNF-α, with 30 of 32 human receptor contacts also mouse contacts. **Our own computation does not corroborate it for any design, and contradicts it for the lead**, which carries the largest species gap in the set (+0.2499, reproduced at +0.2359). The pre-registered test returns `indistinguishable` for 9 of 10 measurable designs while an exact permutation test rejects 8 of 10 — neither is usable alone, so Amendment 6 fixes effect size as the reading rule and a sub-0.10 ipSAE difference is not called a species preference. `l91_mpnn1` is the better of the confirmed pair at +0.0853 / +0.0938. |
| **Objective 1 — affinity** (ranked 3rd) | 12 designs over 8 independent backbones, all clearing SC ≥ 0.58. Lead (`l69_mpnn1`): SC 0.62, dG −61.6, 2131 Å² buried, 12 interface H-bonds, 7.8% unsatisfied — the best binding energy and the cleanest H-bond satisfaction in the set. Better than our EGFR submission on every axis. |

**The honest summary:** the pH mechanism is the strongest part of this
submission — two designs confirmed on a second predictor, under a bar and a
replication rule both fixed in advance, with 30 of 30 on the lead. Affinity is
solid. Cross-reactivity is the weak objective: well-grounded in an experimental
structure, **unsupported by our own computation**, and the tension is not
resolvable from where we stand — the design with the strongest pH evidence
carries the largest species gap, and the design with the smallest species gap
has the weaker pH evidence. We report both rather than ranking around the
problem.

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

### Result: two designs confirmed, and the screen that found them validated

`[measured]` Six of 12 submitted designs satisfy the rule on AlphaFold2 models
in 2 of 2 samples:

| design | His | anchor | distance (Å) |
|---|---|---|---|
| l69_mpnn1 | H4 | R32 | 4.6, 5.7 |
| l91_mpnn1 | H15 | R32 | 4.8, 5.4 |
| l69_mpnn2 | H4 | R32 | 3.0, 5.4 |
| l91_mpnn2 | H15 / H16 | R32 / K65 | 5.3–5.9 / 4.7 |
| l66_mpnn2 | H32 | R32 | 5.6, 5.7 |
| l87_mpnn1 | H27 | R32 | 3.8, 4.9 |

`[measured]` **All 12 designs** were then co-folded with Boltz-2 against the
full human and mouse **trimers** at **10 diffusion samples** per species. The
bar — `≥7 of 10`, the proportional translation of the pre-registered
`≥2 of 3` — was fixed in Amendment 4 (`8a68de1`) before any 10-sample fold
existed. The requirement that a first-time pass be **replicated** in a second
independent run was fixed in Amendment 5 (`2d58faa`) before the run that
produced these results.

| design | human, per run | human pooled | mouse, per run | mouse pooled | status |
|---|---|---|---|---|---|
| l69_mpnn1 | 10/10, 10/10, 10/10 | 30/30 [0.89–1.00] | 8/10, 5/10, 7/10 | 20/30 | **CONFIRMED** (human, 3 runs) |
| l91_mpnn1 | 9/10, 10/10 | 19/20 [0.76–0.99] | 4/10, 3/10 | 7/20 | **CONFIRMED** (human, 2 runs) |
| l66_mpnn2 | 6/10 | 6/10 [0.31–0.83] | 3/10 | 3/10 | below bar |
| l69_mpnn2 | 4/10, 6/10 | 10/20 [0.30–0.70] | 4/10, 6/10 | 10/20 | below bar |
| l91_mpnn2 | 3/10, 4/10 | 7/20 [0.18–0.57] | 2/10, 3/10 | 5/20 | below bar |
| l66_mpnn1 | 2/10 | 2/10 [0.06–0.51] | 3/10 | 3/10 | below bar |
| l60_mpnn1 | 0/10 | 0/10 [0.00–0.28] | 0/10 | 0/10 | below bar |
| l60_mpnn2 | 0/10 | 0/10 [0.00–0.28] | 0/10 | 0/10 | below bar |
| l62_mpnn20 | 0/10 | 0/10 [0.00–0.28] | 0/10 | 0/10 | below bar |
| l84_mpnn1 | 0/10 | 0/10 [0.00–0.28] | 0/10 | 0/10 | below bar |
| l87_mpnn1 | 0/10 | 0/10 [0.00–0.28] | 0/10 | 0/10 | below bar |
| l97_mpnn2 | 0/10 | 0/10 [0.00–0.28] | 0/10 | 0/10 | below bar |

**Two designs clear the bar on the human arm and hold it under replication.**
`l69_mpnn1` satisfied the rule in **every one of thirty samples across three
independent runs**; it carries exactly one histidine, H4, so the contact is
unambiguous. `l91_mpnn1` gave 9/10 then 10/10. Both anchor on **R32**, and the
closest approaches (2.55 Å and 3.10 Å in different runs) are hydrogen-bond
distance — neutral imidazole at pH 7.4, a like-charge contact at van der Waals
range once protonated at 6.0. That is the designed mechanism, found by a
predictor that played no part in the design.

**Neither design is confirmed on mouse**, and we are explicit about it:

| design | per run | pooled | P(>= k \| p0 = 2/3) | reading |
|---|---|---|---|---|
| l69_mpnn1 | 8/10, 5/10, 7/10 | 20/30 | 0.585 | cleared the bar in 2 of 3 runs |
| l91_mpnn1 | 4/10, 3/10 | 7/20 | 0.999 | cleared the bar in 0 of 2 runs |

`l69_mpnn1`'s mouse arm pools to **exactly the bar's own implied rate**
(20/30 = 0.667, p₀ = 2/3), which is why it oscillates either side of the
threshold run to run. Amendment 7 fixed in advance that a result like this is
reported as "cleared the bar in 2 of 3 runs" and may not be dropped as an
outlier. It isn't.

`[measured]` **Six of the twelve designs score a flat 0 of 10**, including
three that carry an AlphaFold2 ✓. The negative control behaves: `l84_mpnn1`
contains no histidine at all and returns 0/10 on both arms in every run, so
the detector is not manufacturing hits.

### The AlphaFold2 screen is itself validated

`[computed]` An earlier revision of this document said our AF2 pH geometry
"reproduces roughly one time in three", then withdrew that as an overclaim
from three designs. With all twelve tested, the picture is the opposite in
spirit:

| AF2 call | Boltz human counts (12-design run) | mean |
|---|---|---|
| pH-positive (6 designs) | 10, 9, 6, 6, 4, 0 | **5.83/10** |
| pH-negative (6 designs) | 2, 0, 0, 0, 0, 0 | **0.33/10** |

Exact permutation test on the group difference: **p = 0.0152** (14 of 924 splits).

Individual AF2 calls do **not** all reproduce — `l87_mpnn1` went from a clean
AF2 anchor to 0/10 — but AF2 positivity strongly predicts Boltz positivity.
The screen is a real filter, and that is the single most useful methodological
result we have.

`[computed]` **How strong is each confirmed result?** The bar is a proportion,
so the reading is binomial, against the per-sample rate the bar encodes
(p₀ = 2/3):

| arm | pooled | Wilson 95% CI | P(≥ k \| p₀) | reading |
|---|---|---|---|---|
| l69_mpnn1 human | 30/30 | 0.89–1.00 | 0.0000 | **very strong** |
| l91_mpnn1 human | 19/20 | 0.76–0.99 | 0.003 | **strong** |
| l69_mpnn1 mouse | 20/30 | 0.49–0.81 | 0.585 | indistinguishable from p₀ |
| l91_mpnn1 mouse | 7/20 | 0.18–0.57 | 0.999 | below the bar |
| l69_mpnn2 human | 10/20 | 0.30–0.70 | 0.962 | below the bar |
| l91_mpnn2 human | 7/20 | 0.18–0.57 | 0.999 | below the bar |

`l66_mpnn2` sits at **6 of 10** — one sample short of the bar. Amendment 7
states before the fact that near-miss designs are **not** re-run, because
re-running narrow misses until one crosses is the multiplicity error the
replication rule exists to prevent. It has not been re-run.

### Anchors: one claim resolved, one retracted

**Resolved.** An earlier revision reported that the two predictors anchored the
mechanism on **different** residues — AF2 on R32, Boltz-2 on K65 — and treated
it as an unresolved conflict. That was an artefact of three samples on a design
that does not clear the bar. On the human arm of both confirmed designs the
predictors **agree on R32**, and it reproduces across runs:

| design | run 2 | run 3 |
|---|---|---|
| l69_mpnn1 | His[4] → [32] | His[4] → [32] |
| l91_mpnn1 | His[15, 16] → [32, 65] | His[15] → [32] |

**Retracted.** A later revision described `l91_mpnn1` as carrying the
**two-anchor** geometry that methods.md pre-registered as ranking above one
anchor, on the strength of a single run in which its H15 and H16 reached both
R32 and K65. **The replication run shows only H15 → R32.** The K65 contact is
sporadic, not structural. `l91_mpnn1` is a single-anchor design against R32 —
architecturally the same as `l69_mpnn1` — and the two-anchor advantage we
briefly attributed to it does not exist. The claim stood for roughly one hour
and is recorded here because replication is what removed it.

**Still open: the species switch.** In mouse, `l69_mpnn1`'s H4 anchors on
**K65** rather than R32. Both are conserved cations inside our pre-registered
anchor set `{R32, K65}`, and the rule does not require the same one in both
species — but the switch may act through a different contact in the two
orthologues. Given that the mouse arm does not clear the bar reproducibly, we
record this as an observation rather than a mechanism.

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

### Computational cross-reactivity — our own computation does not support it

`[measured]` All 12 designs were co-folded with Boltz-2 against the full human
and mouse **trimers** at 10 diffusion samples per species. The verdict form —
`|human − mouse|` against a noise floor of the larger per-species range — was
fixed before the run. Amendment 5 requires the exact permutation p to be
reported **alongside** it, never instead of it. Amendment 6 withholds a verdict
entirely where fewer than two samples yield a usable ipSAE value.

| design | human mean [range] | mouse mean [range] | diff | pre-registered verdict | exact permutation p |
|---|---|---|---|---|---|
| l60_mpnn1 | n=1 usable | n=0 usable | — | **NOT MEASURABLE** (Am. 6) | — |
| l60_mpnn2 | n=1 usable | n=1 usable | — | **NOT MEASURABLE** (Am. 6) | — |
| l62_mpnn20 | 0.2762 [0.2705] | 0.1709 [0.2264] | +0.1053 | indistinguishable | 4.49e-03 |
| l66_mpnn1 | 0.3834 [0.1438] | 0.3820 [0.1694] | +0.0014 | indistinguishable | 9.46e-01 |
| l66_mpnn2 | 0.3542 [0.0686] | 0.3935 [0.1116] | -0.0393 | indistinguishable | 1.43e-02 |
| l69_mpnn1 | 0.5684 [0.1138] | 0.3185 [0.2127] | +0.2499 | **REAL** | 1.08e-05 |
| l69_mpnn2 | 0.5023 [0.1597] | 0.3149 [0.1959] | +0.1874 | indistinguishable | 1.08e-05 |
| l84_mpnn1 | 0.3563 [0.2520] | 0.4172 [0.1790] | -0.0609 | indistinguishable | 7.82e-02 |
| l87_mpnn1 | 0.3789 [0.0981] | 0.3221 [0.2479] | +0.0568 | indistinguishable | 3.63e-02 |
| l91_mpnn1 | 0.5325 [0.1468] | 0.4472 [0.1984] | +0.0853 | indistinguishable | 3.00e-03 |
| l91_mpnn2 | 0.5089 [0.1722] | 0.4358 [0.2275] | +0.0732 | indistinguishable | 1.48e-02 |
| l97_mpnn2 | 0.3110 [0.1401] | 0.2645 [0.1231] | +0.0466 | indistinguishable | 2.40e-02 |

**Three readings, and none of them helps objective 2.**

1. **The pre-registered test almost never rejects.** It returns
   `indistinguishable` for 9 of the 10 measurable designs. Amendment 4 called
   it "conservative"; at n=10 across twelve designs it is closer to inert,
   because the observed range grows with sample size while the precision of a
   mean improves. It is conservative toward "no species difference" — which is
   the answer objective 2 wants — so the bias runs in our favour.
2. **The exact test rejects almost everything.** Permutation p < 0.05 for 8 of
   the 10 measurable designs. But it detects differences as small as 0.04
   ipSAE, which is statistically real and biologically uninformative. Neither
   statistic answers the question on its own.
3. **On effect size, which is what Amendment 6 fixes as the reading rule, only
   the two `l69` designs show a large gap** (+0.2499 and +0.1874). Everything
   else is below 0.11, and two designs (`l66_mpnn2`, `l84_mpnn1`) lean mildly
   toward *mouse*. A difference below 0.10 ipSAE is not described here as a
   species preference whatever its p-value.

`[measured]` **The uncomfortable part: our lead has the largest species gap in
the set.** `l69_mpnn1` sits at +0.2499, reproduced at +0.2359 in a third
independent run — the only design to draw a REAL verdict under the
pre-registered test, in both runs it appeared in. The design with the smallest
gap among the confirmed pair is `l91_mpnn1` at +0.0853, reproduced at +0.0938:
indistinguishable under the pre-registered test both times, and below the 0.10
effect-size threshold both times. That is the main reason it occupies slot 2.

`[measured]` **Two narrow things survive on the positive side.**

- **Groove engagement is perfect.** All **240 of 240** samples in the
  12-design run contacted exactly two of the three protomers, with
  `contacts_both_protomers` true every time. The binders are in the
  inter-protomer groove, in both species, without exception. The orientational
  ambiguity that forced Amendment 2 on a two-protomer target is absent on the
  trimer.
- **`l91_mpnn1` binds mouse substantially better than the lead** — mouse ipSAE
  0.4472 and 0.4196 across two runs, against `l69_mpnn1`'s 0.3185 and 0.3239.

`[measured]` **What this supersedes.** An earlier revision reported the
3-sample comparison for `l69_mpnn2` as indistinguishable, and the partial
12-design run at n=3 as **indeterminate** because 3 of 4 comparisons exceeded
our `sample range > 0.15 = poorly determined` threshold. Amendment 4 fixed in
advance that the 0.15 threshold does not transfer to n=10. The n=10 numbers
above are the ones we report, and they are less favourable to us than the ones
they replace.

The objective-2 claim therefore rests **entirely** on the structural evidence
above — 7KP7, and 30 of 32 human receptor contacts shared with mouse. Our own
computation does not corroborate it for any design, and contradicts it for the
lead.

---

## Objective 1 — human TNF-α affinity (ranked third)

### The submitted designs

`[measured]` All values are Rosetta/AF2 metrics on the design models, averaged
over 5 AF2 models.

| design | len | i_pTM | SC | dG | dSASA | H-bonds | unsat % | pH |
|---|---|---|---|---|---|---|---|---|
| l69_mpnn1 | 69 | 0.86 | 0.62 | **−61.6** | 2131 | 12 | **7.8** | ✓✓ |
| l91_mpnn1 | 91 | 0.80 | 0.59 | −52.0 | 2154 | 12 | 29.1 | ✓✓ |
| l69_mpnn2 | 69 | 0.86 | **0.66** | −57.7 | 2144 | 12 | 9.1 | ✗ |
| l87_mpnn1 | 87 | 0.72 | 0.62 | −44.1 | 1883 | 6 | 7.6 | ✗ |
| l66_mpnn2 | 66 | 0.77 | 0.61 | −53.2 | 1814 | 10 | 10.3 | ✗ |
| l91_mpnn2 | 91 | 0.80 | 0.59 | −54.2 | 2224 | 15 | 23.3 | ✗ |
| l84_mpnn1 | 84 | 0.84 | 0.60 | −46.9 | 1910 | 11 | 24.1 | — |
| l66_mpnn1 | 66 | 0.77 | 0.64 | −48.6 | 1695 | 8 | 7.4 | — |
| l60_mpnn2 | 60 | 0.71 | **0.68** | −47.9 | 1937 | 8 | 28.9 | — |
| l60_mpnn1 | 60 | 0.69 | 0.64 | −43.9 | 1825 | 7 | 19.6 | — |
| l62_mpnn20 | 62 | 0.63 | **0.68** | −38.3 | 1636 | 7 | 18.4 | — |
| l97_mpnn2 | 97 | 0.45 | 0.64 | −41.7 | 1381 | 10 | 8.0 | — |

**✓✓** = pH rule satisfied on AlphaFold2 (2 of 2) **and** on Boltz-2 at the
pre-registered ≥7-of-10 bar, on the **human** arm, in **two or more independent
runs** · **✗** = AlphaFold2 2 of 2 but below the bar on Boltz-2 · **—** = no
binder histidine within the pre-registered 6.0 Å of R32 or K65 and below the
bar. **All twelve designs were tested on the second predictor.** Note that ✓✓
is a *redefinition*: the original tier-1 criterion required clearing the bar on
**both species**, and no design meets it. That change is post-hoc and is set
out under "Designs submitted". The strength of every result is quantified in
Objective 3.

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

Seven. The first four were committed with the correction timestamped ahead of
any result that depended on it. The last three are claims made in earlier
revisions of this document that later measurements showed to be wrong; we have
left each retraction visible rather than quietly editing the claim away. Two of
the three were removed by **replication**, which is the argument for having
required it. We list them because the audit trail is the point.

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

**6. We credited a design with a two-anchor geometry it does not have.** A
revision of this document described `l91_mpnn1` as carrying the **two-anchor**
configuration that methods.md pre-registered as ranking above one anchor, on
the strength of a single run in which H15 and H16 reached both R32 and K65. The
replication run returned **H15 → R32 only**: the K65 contact is sporadic, not
structural. `l91_mpnn1` is a single-anchor design, architecturally the same as
`l69_mpnn1`. The claim survived about an hour and was removed by the
replication requirement, not by argument.

**7. We understated our own screen, then overstated the pessimism.** After
three designs we wrote that the AlphaFold2 pH geometry "reproduces roughly one
time in three", then withdrew it as an overclaim from too small a sample. With
all twelve designs tested the correct statement runs the other way: AF2-positive
designs average **5.83 of 10** on the independent predictor against **0.33 of
10** for AF2-negative, exact permutation p = 0.015. Individual AF2 calls do not
all reproduce, but AF2 positivity strongly predicts Boltz positivity. Both the
original figure and its withdrawal were wrong in opposite directions, and the
data that settled it only existed once we tested all twelve.

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
8. **The mouse pH arm is not reproducible, and that is now measured rather
   than suspected.** `l69_mpnn1` returned 8/10, 5/10 and 7/10 across three
   independent runs — cleared the bar in 2 of 3, pooling to 20/30 = 0.667,
   which is exactly the rate the bar encodes. A design sitting on its own
   threshold will cross it about half the time. We report the mouse arm as
   unconfirmed for every design. The earlier 3-sample protocol was worse still
   (l69_mpnn2 moved 0.509 → 0.385 and 2/3 → 1/3 on identical input, amid 48
   MSA-server errors); it was replaced by n=10 under Amendment 4 and its
   numbers are not reported.
9. **propka is not relied upon.** The Proton-PottsMPNN authors report predicted
   pKa was not predictive of which pH bin a design fell into.
10. **Calibration provenance.** The AUC figures underlying our metric choices
   (SC 0.68, ipSAE_min 0.615) have no recorded primary source in our notes.
11. **The challenge brief was not committed to the repository** — it was
    supplied in conversation. Objective definitions in this document are as we
    understood them.
12. **Individual AlphaFold2 pH calls do not all reproduce, even though the
    screen as a whole does.** `l87_mpnn1` carried a clean AF2 anchor (H27 → R32
    at 3.8 and 4.9 Å) and returned **0 of 10** on the independent predictor.
    Group-level prediction (5.83/10 against 0.33/10, p = 0.015) does not license
    a per-design claim, and a ✓ in the AF2 column is evidence, not a result.
13. **Our pre-registered species test is biased toward the answer we wanted.**
    Comparing a difference of means to the range of single samples inflates the
    rejection threshold as sample size grows. It is conservative toward
    "no species difference", which is objective 2's desired outcome. An exact
    permutation test on the same data gives p = 1.1 × 10⁻⁵, 1.1 × 10⁻⁵ and
    4.4 × 10⁻³ for the three designs — so the one favourable pre-registered
    verdict is not robust. We report the pre-registered verdict as the verdict
    and the permutation test as a disclosed sensitivity analysis, because the
    error here would be to keep the flattering statistic quietly.
14. **The submission order was changed post-hoc, twice.** The bars themselves
    were pre-registered; their consequences for ordering were not. Disclosed
    under "Designs submitted"; no sequence was ever changed.
15. **The tier-1 criterion was loosened after nothing passed the original.**
    It required clearing the bar on both species; no design does. We redefined
    it to the human arm rather than publish an empty tier. This is disclosed
    under "Designs submitted", and the mouse data is given for every design so
    the original criterion can be applied by any reader.
16. **Two designs could not be measured for cross-reactivity at all.** The
    60-aa binders yielded 1 and 0 usable ipSAE samples of 10, because the
    metric's interface selection admits too few residues for a binder that
    small. Amendment 6 reports them as NOT MEASURABLE. That rule removes two
    verdicts that would have read as evidence *against* cross-reactivity, so it
    happens to favour us, and it is recorded in methods.md for that reason.

---

## Designs submitted

12 designs in `submission.csv`, in submission order. All 12 clear the affinity
gate and **all 12 were tested on the second predictor** at n=10 per species.

**The tier-1 definition was changed on 2026-10-12, and the change is post-hoc.**
It originally required clearing the ≥7-of-10 bar on AlphaFold2 **and** Boltz-2
**in both species**. After twelve designs at n=10 plus two replication runs,
**no design meets that definition** — the best mouse result is `l69_mpnn1` at 2
of 3 runs, pooling to exactly the bar's implied rate. Rather than publish an
empty tier, we redefined tier 1 as clearing the bar on the **human** arm in
**two or more independent runs** (Amendment 5's replication standard). This is
a criterion loosened after seeing that nothing passed the original, which is
the kind of move the rest of this document exists to prevent, so: the original
definition is stated here, and the mouse result is reported for every design in
Objective 3 so a reader can apply it unaided and find tier 1 empty.

| # | design | len | tier | pH evidence (human arm unless stated) |
|---|---|---|---|---|
| 1 | tnfa_l69_s930894_mpnn1 | 69 | **1** | H4 → R32; **10/10, 10/10, 10/10 = 30/30 over three runs**; mouse 2 of 3 runs |
| 2 | tnfa_l91_s990274_mpnn1 | 91 | **1** | H15 → R32; **9/10 then 10/10 = 19/20**; mouse 0 of 2 runs |
| 3 | tnfa_l69_s930894_mpnn2 | 69 | 2 | H4 → R32, AF2 2/2; Boltz 4/10 then 6/10 — **below bar both runs** |
| 4 | tnfa_l87_s136696_mpnn1 | 87 | 2 | H27 → R32, AF2 2/2; Boltz **0/10** — anchor does not reproduce |
| 5 | tnfa_l66_s937529_mpnn2 | 66 | 2 | H32 → R32, AF2 2/2; Boltz **6/10** — one short of the bar, not re-run (Am. 7) |
| 6 | tnfa_l91_s990274_mpnn2 | 91 | 2 | H15/H16, AF2 2/2; Boltz 3/10 then 4/10 — **below bar both runs** |
| 7 | tnfa_l84_s861729_mpnn1 | 84 | 3 | none — no histidine; 0/10 both arms (negative control) |
| 8 | tnfa_l66_s937529_mpnn1 | 66 | 3 | His32 present; Boltz 2/10 |
| 9 | tnfa_l60_s347619_mpnn2 | 60 | 3 | His17 present; Boltz 0/10 |
| 10 | tnfa_l60_s347619_mpnn1 | 60 | 3 | His17 present; Boltz 0/10 |
| 11 | tnfa_l62_s149973_mpnn20 | 62 | 3 | 3 His present; Boltz 0/10 |
| 12 | tnfa_l97_s762214_mpnn2 | 97 | 3 | His72 present; Boltz 0/10 |

**Ordering is post-hoc and disclosed.** The bars themselves (Amendments 4, 5)
were fixed before the runs that produced these results; their consequence for
submission order was not. `l91_mpnn1` rose from slot 6 to slot 2 on confirming
at 19/20 with the smallest species gap of the confirmed pair. `l69_mpnn1` was
kept at slot 1 rather than yielding to it: the two are statistically tied on
objective 3 (30/30 against 19/20), `l91_mpnn1` is clearly better on objective 2
(+0.09 against +0.25), but `l69_mpnn1` is clearly better on objective 1
(dG −61.6 against −52.0, 7.8% unsatisfied against 29.1%) — and binding is a
prerequisite for a pH switch mattering at all. A reader who weights the ranked
objectives strictly lexicographically would put `l91_mpnn1` first, and that
reading is defensible. No sequence was altered in any reorder.

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
| `b088b94` | n=10 result on the top 3; three overclaims walked back; permutation sensitivity analysis disclosed |
| `2d58faa` | Amendment 5: **replication required for a first-time pass**, run ordering and paired species reporting fixed **before** the 12-design run; crossreact made failure-tolerant |
| `efb841c` | 12-design n=10 results; Amendment 6 (effective-n rule, with its favourable direction disclosed); Amendment 7: **the l91_mpnn1 replication, the control rule and the no-re-running-near-misses commitment, all fixed before the replication run** |

Analysis scripts are in `challenges/tnfa/`: `tnfr_contacts.py`,
`crossspecies_epitope.py`, `cation_anchors.py`, `groove_occupancy.py`,
`verify_numbering.py`, `histag_geometry.py`, `parse_designs.py`,
`build_submission.py`, `analyze_n10.py`. Run logs for every production run are
committed, including `crossreact-n10.log` and the full per-sample record in
`crossreact-n10.json` — every ipSAE pair, every interface contact list and
every pH-anchor distance behind the tables above, so the n=10 claims can be
recomputed from source with `analyze_n10.py`.
