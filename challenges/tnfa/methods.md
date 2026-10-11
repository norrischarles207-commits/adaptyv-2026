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
