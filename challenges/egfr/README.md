# Challenge 1 — EGFR pH-conditional binder

Track 3, submitted 2026-10-05. Five de novo designs: two complementary leads
plus three declared near-misses.

> **Numbering.** Every residue number in this directory is **precursor /
> UniProt P00533** numbering (signal peptide counted; mature L1 = precursor
> L25, so precursor = mature + 24) unless a line says "mature". The literature
> on EGFR mixes the two freely, which is exactly why the convention is stated
> here and repeated at the top of every file in `lit/`.

## The mechanism, and how it differs from Challenge 2

This challenge asked for binding **at** acidic pH. The switch is placed on
**EGFR's own His409** rather than engineered into the binder, following Liu et
al. 2022 on antibody G532: a binder-side carboxylate raises that histidine's
pKa, so the contact converts from hydrogen bond to salt bridge as pH falls
toward 6.5.

Challenge 2 inverts this in both directions — it asks for *loss* of binding at
low pH, and puts the histidine in the **binder** rather than the target. The
two challenges are therefore not variations on one trick; see
[`../tnfa/README.md`](../tnfa/README.md).

## Start here

| file | what it is |
|---|---|
| [`submission-writeup.md`](submission-writeup.md) | The submitted document — rationale, every measurement, eight limitations. |
| [`methods.md`](methods.md) | Dated run log, including corrections to its own earlier claims. Long; skim the latest entries first. |
| [`submission.csv`](submission.csv) | The five submitted sequences. |
| [`brief.md`](brief.md) | The challenge brief as issued. |
| [`lit/`](lit/) | The literature pass (see below). |

## The result in one paragraph

`egfr_l93_s713816` clears both pre-registered thresholds against the full
621-residue receptor and is cleanly cross-reactive with mouse. A single
substitution on that same backbone, `l93_H36E`, places a carboxylate 3.21 Å
from His409 in 3 of 3 predictions but fails the mouse threshold on the
pre-registered statistic. The two sequences in `submission.csv` differ at
exactly one position — H36 versus E36 — which is the whole point: **no single
molecule meets both criteria.** The two properties conflict at one residue, and
the submission reports that rather than picking a winner.

## `lit/` — the literature pass

Every number in these files carries a provenance label, because they were not
all established the same way:

- `[computed]` — our own calculation from raw data.
- `[summ]` / `[SUMMARY]` — read through a page summarizer, **not** seen as raw
  text; flagged as needing a spot-check against the primary source before
  anything relies on it.
- `[BLOG]` — Adaptyv's own published statements.

| file | scope |
|---|---|
| `epitope-verification.md` | Epitope selection, numbering reconciliation, mouse follow-ups. |
| `ph-strategy-notes.md` | The pH-switch literature, including the G532 precedent. |
| `precedent-adaptyv-egfr.md` | The 2024 Adaptyv EGFR competition (Rounds 1–2) — what the released outcome data actually show. Recomputed from the raw Round 2 data where labelled. |
| `hand-back.md` | The literature hand-back verbatim as reviewed, with follow-ups resolved in an addendum rather than edited into the original text. |
| `sources.md` | Annotated source list. |

## Runs and data

The campaign ran in stages; each stage's raw results are kept as JSON next to
the writeup that cites them.

| file | stage |
|---|---|
| `v3c-core-designs.csv`, `v3c-core-filters.csv` | BindCraft design round: accepted designs and the filter outcomes. |
| `v3c-crossreact-stage1.json` | Stage 1 — human/mouse cross-reactivity screen. |
| `v3c-fulllength-stage2.json` | Stage 2 — the surviving designs against the full-length receptor. |
| `l93-variants.json` | The pre-registered variant round on the `l93` backbone. |
| `l93-species-fulllength.json`, `l93_H36E-mouse-6sample.json` | Species checks on the pH-switch lead. |
| `egf-control.json` | EGF positive control. |
| `v3c-core.log`, `v3c-q408.log` | Raw BindCraft run logs (trajectory stats live here). |

## Structures

- `6aru.cif` — the source complex. **6ARU is a cetuximab–EGFR complex and was
  used solely to identify surface epitope residues**; no backbone here is
  derived from it. All binder backbones are hallucinated.
- `structures/v3c-core/` — the seven core designs.
- `l93_H36E/`, `species-mouse/` — the pH-switch lead, human and mouse, 3 Boltz
  models each.
- `fulllength-v3c/`, `fulllength-cofold/` — full-length receptor complexes.
- `h36e_his409_saltbridge.png` — the H36E carboxylate against His409.

A note on `*.npz` confidence matrices: four (`pae_*`, `plddt_*` under
`fulllength-cofold/`) are tracked, because they were committed before the
ignore rule for them was added and `.gitignore` does not untrack
retroactively. The rest are ignored as regenerable. They are the inputs
`redundancy.py::rescore_saved` reads to re-score a design without paying for a
GPU re-prediction, so the tracked ones are usable, not merely residual.
