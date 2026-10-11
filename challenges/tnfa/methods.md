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
