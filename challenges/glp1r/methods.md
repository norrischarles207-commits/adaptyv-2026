# GLP1R — methods log

Challenge 3, Anthropic × Adaptyv Bio 2026 · Track 3.
UniProt **P43220** numbering throughout. `[computed]` 6X18 chain R author
numbering **equals** UniProt numbering (verified, not assumed: chain R residue
29 is Thr, and P43220 residue 29 is Thr). The assay construct is P43220
24–432, so **construct position = UniProt − 23**.

---

## 2026-10-17 — PRE-REGISTRATION, recorded before any design result exists

Nothing has been generated against this target. One EvoBind trajectory was run
today as a **cost probe**; it was stopped before completion, produced no
accepted design, and **nothing from it is eligible for submission**.

### The objective that drives everything else

This challenge has two objectives: **binding affinity** and **receptor
activation**. A design that binds but does not activate fails objective 2
outright — activation is measured only on confirmed binders, and a non-agonist
scores nothing on it.

Objective 2 therefore drives target and epitope selection, and **we knowingly
accept a cost to objective 1 to serve it.** That trade is recorded here, before
any result exists, because it is the decision most likely to look wrong in
hindsight.

### Target

**PDB 6X18, chain R.** GLP-1 bound to GLP1R in complex with Gs — the **active,
G-protein-coupled conformation**.

Why the active state specifically: the only mechanism for agonism available to
a designed binder is to **stabilise the active conformation**. A binder built
to be shape-complementary to an inactive or apo structure has no reason to
activate anything. This is the same reasoning under which published de novo
miniprotein agonists for class A receptors were obtained.

`[computed]` **Sequence check against the assay construct**, the same check run
on 7KPB in challenge 2:

| structure | mismatches vs the construct sequence in the brief |
|---|---|
| **6X18 chain R** | **1 — L260F**, outside both contact sets and outside the hotspot set below |

384 resolved residues compared. L260F is the only deviation and does not touch
the designed interface.

**What is kept:** chain R only, resolved range 29–423. Gαs, Gβ, Gγ and Nb35 are
dropped. The GLP-1 peptide is dropped — its site *is* the design target.

`[computed]` Two numbering gaps exist in the deposit: **130–135** (an ECD loop)
and **339–343** (ICL3, intracellular). Neither lies in the epitope.

**The ECD is not truncated.** It caps the channel in the active state, and
every accessibility number below already includes that occlusion. Removing it
would design against a surface that is partly blocked in reality.

### Hotspots — fixed now

```
R141,R201,R298,R299,R300,R306,R380,R384
```

> **Notation.** The chain is called R, so *every* hotspot begins with `R`
> regardless of residue identity. This set is **Leu141, Leu201, Thr298,
> Arg299, Asn300, Trp306, Arg380, Leu384**. `R306` is a tryptophan.

Rationale, all `[computed]` in `epitope-analysis.md`:

- All eight are **message** contacts (GLP-1 7–15) — the activation epitope, not
  the affinity epitope. `[computed]` The message touches 27 receptor residues,
  24 of them TMD/ECL; the address touches 29, 20 of them ECD.
- All eight are **channel-facing, not lipid-facing**: ΔSASA on peptide binding
  of 38–74 Å², i.e. 54–100% of their apo area is buried by the native peptide.
- All eight sit **0 to −10 Å** below the top of the TM bundle — shallow enough
  to be approached without deep penetration of the DDM/CHS micelle.

**Deliberately excluded:**

- **The entire ECD affinity epitope** (W39, E68, Y69, W91, S31, L32, …).
  `[computed]` His7 is **43.2 Å** from the ECD centroid; a binder anchored
  there would need to project ~30–43 Å to reach the activation site. This is
  the most likely reason published de novo binders to class B receptors came
  back as **antagonists**.
- **Deep message contacts** — L388 (−13 Å), V237 (−16 Å), R190 (−16 Å), I313
  (−19 Å), Y241 (−22 Å). Channel-facing, but probably inside the detergent
  belt. Held in reserve, not targeted.
- **Y145** — apo-exposed but only 8% buried by the peptide, i.e.
  lipid/solvent-facing rather than channel-facing.

Binder lengths **55–130 aa**. Preset `default_4stage_multimer_hardtarget`.

### Tool choice — fixed now, with the reason

**BindCraft, not EvoBind.** `[measured]` EvoBind re-folds the 409-residue
receptor once per mutation step: **92.5 s/iteration on an A10G = $0.0283 per
iteration**, i.e. **$4.25–28 per design** depending on iteration count, against
roughly **$58 remaining across three challenges**. BindCraft takes the receptor
coordinates as fixed and its per-attempt cost is already calibrated from
challenge 2.

This is a **budget decision, not a claim that EvoBind is the worse method.** It
ran correctly and was optimising when stopped.

### Acceptance thresholds — unchanged from challenges 1 and 2

- **ipSAE_min ≥ 0.60**, minimum over chain-pair directions
- **SC ≥ 0.58** (pyrosetta Lawrence–Colman)
- Scored as the **mean of diffusion samples, never best-of-N**
- Sample range > 0.15 on either metric = "poorly determined", flagged
- ipTM recorded, not used for selection

### Activation-mode rule — fixed before any design is scored

> A design satisfies the activation-mode rule when its binder chain makes
> heavy-atom contact (**≤ 4.5 Å**) with at least **4 of the 8** pre-registered
> hotspot residues, in at least **2 of 3** diffusion samples.

If sampling is later raised to 10 per design, the bar translates
proportionally to **≥ 7 of 10**, by the same rule used in challenge 2
(Amendment 4), and that translation is fixed here rather than chosen later.

**This rule is geometric and nothing more.** No predictor available to us
models receptor activation. Satisfying it is evidence that a design engages the
*message* site rather than the *address* site — the binding mode associated
with agonism — and is **not** a prediction that the design is an agonist.

### What this design cannot establish

1. **No tool here predicts agonism.** See above. Any claim of activation must
   come from Adaptyv's cell-based reporter assay, not from us.
2. **Designing for the active state may cost measured affinity.** Objective 1
   is measured on a detergent-solubilised construct carrying *unlisted*
   thermostabilising mutations, which may not populate the conformation we
   designed against. Accepted deliberately; recorded now, not after the result.
3. **6X18 is one conformational snapshot** of a receptor that is dynamic.
4. **Expression format.** The cell-free system prepends **Met** and appends a
   **C-terminal polyhistidine tag** (confirmed with the organisers). Both
   termini are modelled. A design whose termini land in the channel is rejected
   regardless of score.

### Budget, flagged before spending

~$58 remains across challenges 3–5. **Challenge 3 is capped at $25.** A
single-attempt smoke test runs first (~$1) to confirm target prep and A10G
memory; the fan-out is sized from the *measured* per-attempt cost, not an
assumed one.

### What we are deliberately NOT doing

- **Not targeting the ECD peptide-binding groove, although the brief
  recommends it.** The brief also states that a groove-only binder may not
  switch the receptor on, and says that is what the organisers would like to
  find out. Our own measurements say the same thing quantitatively. We are
  testing the harder hypothesis on purpose, and if every design fails objective
  1 as a result, that is the cost of this choice and not a surprise.
- **Not designing a cyclic peptide.** The expression system is linear.
- **Not deriving any sequence from GLP-1, exendin-4, semaglutide, dulaglutide
  or any other known agonist.** The organisers' prescreen rejects modified
  known binders; every backbone here is hallucinated de novo. Reproducing the
  native *binding mode* is intended; reusing native *sequence* is not.
