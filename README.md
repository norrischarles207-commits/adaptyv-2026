# Adaptyv 2026 — binder design pipeline

Target-agnostic pipeline for designing de novo protein binders and cross-
validating them, built for repeated use across Adaptyv 2026 weekly
challenges. Every stage takes a target slug and target-specific parameters
at the command line — no per-challenge code changes.

Extracted from an earlier VEGF-A-specific project; see
[`notes/calibration.md`](notes/calibration.md) for the scoring calibration
that project produced, which this pipeline inherits.

## Challenges

| # | target | submitted | designs | where it landed |
|---|---|---|---|---|
| 1 | EGFR — pH-conditional binding | 2026-10-05 | 5 | Two complementary leads; no single molecule meets both criteria, and the submission says so. |
| 2 | TNF-α — pH-conditional + mouse cross-reactive | 2026-10-16 | 12 | Two designs confirmed on the pH objective under replication; neither confirmed on mouse. |
| 3 | GLP1R — agonist (binding **and** receptor activation) | in progress | — | — |

**Challenge 1 — pH-conditional EGFR binder.** Track 3, submitted 2026-10-05.
Five de novo designs: two complementary leads plus three declared near-misses.
The pH switch is placed on EGFR's own His409 rather than engineered into the
binder, following Liu et al. 2022 on antibody G532 — a binder-side carboxylate
raises that histidine's pKa, so the contact converts from hydrogen bond to
salt bridge as pH falls toward 6.5.

The result, stated as it stands: `egfr_l93_s713816` clears both pre-registered
thresholds against the full 621-residue receptor and is cleanly cross-reactive
with mouse. A single substitution on that backbone, `l93_H36E`, places a
carboxylate 3.21 Å from His409 in 3 of 3 predictions but fails the mouse
threshold on the pre-registered statistic. **No single molecule meets both
criteria** — the two properties conflict at one residue, and the submission
says so rather than picking a winner.

- [`challenges/egfr/submission-writeup.md`](challenges/egfr/submission-writeup.md)
  — the submitted document: rationale, every measurement, eight limitations.
- [`challenges/egfr/methods.md`](challenges/egfr/methods.md) — the dated run
  log, including corrections to its own earlier claims.
- [`challenges/egfr/submission.csv`](challenges/egfr/submission.csv) — the five
  submitted sequences.

**Challenge 2 — pH-conditional, cross-species TNF-α binder.** Track 3,
submitted 2026-10-16. Twelve de novo designs, 60–97 aa, over eight independent
backbones. The organisers **number** the objectives 1 = affinity, 2 = mouse
cross-reactivity, 3 = pH selectivity but **rank** them in reverse; every
document for this challenge is organised in ranked order and labelled with the
organisers' number, so the two cannot be confused.

The mechanism inverts Challenge 1. There the binder had to *acquire* an
interaction as pH fell; here it must *lose* one. A binder histidine sits against
a conserved cationic residue on the target — R32, with K65 as a second anchor —
neutral and tolerated at pH 7.4, positively charged at 6.0, where the like
charges repel. All of the pH machinery is in the binder: the conserved
cross-species epitope contains no histidine, so a target-side switch would have
traded objective 3 against objective 2.

The result, stated as it stands: **two designs clear the pre-registered pH bar
on the human arm under replication** — `l69_mpnn1` at 30 of 30 diffusion samples
across three independent runs, `l91_mpnn1` at 19 of 20 across two, both anchored
on R32 at hydrogen-bond distance. **Neither is confirmed on mouse.** The
AlphaFold2 screen that selected them is itself validated against the second
predictor (permutation p = 0.015). No predictor models protonation, so this is
geometric availability, not demonstrated pH-dependent binding.

Cross-reactivity is the weak objective and is reported as one. It rests on 7KP7
— a 2.65 Å structure of human TNFR1 bound to *mouse* TNF-α, sharing 30 of 32
receptor contacts — but our own computation does not corroborate it for any
design and contradicts it for the lead, which carries the largest species gap in
the set. The two properties pull apart, and the submission reports both rather
than ranking around the problem.

- [`challenges/tnfa/submission-writeup.md`](challenges/tnfa/submission-writeup.md)
  — the submitted document: ranked-order rationale, machine-generated result
  tables, sixteen limitations.
- [`challenges/tnfa/methods.md`](challenges/tnfa/methods.md) — the
  pre-registration and Amendments 1–7. Each amendment is dated and tied to the
  commit that fixed it *before* the run it governs, including the two that
  tightened the rules against us.
- [`challenges/tnfa/submission.csv`](challenges/tnfa/submission.csv) — the
  twelve submitted sequences.

## Pipeline, end to end

```
                      ┌──────────────────────────────────────────────────┐
                      │ 1. Target intake      challenges/<slug>/         │
                      │    Pick a target/partner complex (the natural    │
                      │    binding partner gives you the real interface).│
                      └──────────────────────────────────────────────────┘
                                          │
                      ┌──────────────────────────────────────────────────┐
                      │ 2. Hotspot picking   modal/find_hotspots.py      │
                      │    Rank target residues by contact-count with    │
                      │    the natural partner. Optional conservation    │
                      │    overlay. Runs locally, no GPU/Modal needed.   │
                      └──────────────────────────────────────────────────┘
                                          │
                      ┌──────────────────────────────────────────────────┐
                      │ 3. Design            modal/run_bindcraft.py      │
                      │    BindCraft on A10G: AlphaFold hallucination    │
                      │    → SolubleMPNN redesign → AF2 re-prediction    │
                      │    → filters: BindCraft's default set, or        │
                      │      --gate-mode prereg, which nulls those and   │
                      │      defers acceptance to our pre-registered     │
                      │      gate downstream (used for TNF-α).           │
                      │    Fan out N attempts in parallel; one           │
                      │    trajectory per call. Every MPNN               │
                      │    re-prediction is logged (pass or fail).       │
                      └──────────────────────────────────────────────────┘
                                          │
                      ┌──────────────────────────────────────────────────┐
                      │ 4. Cross-validation  modal/redundancy.py         │
                      │    Re-predict the binder-target complex with     │
                      │    Boltz-2 (independent MSA + model), score on   │
                      │    the calibrated metrics (see below). CPU-only  │
                      │    rescore path reuses cached Boltz outputs      │
                      │    when thresholds change.                       │
                      └──────────────────────────────────────────────────┘
                                          │
                      ┌──────────────────────────────────────────────────┐
                      │ 5. Selection & writeup  challenges/<slug>/       │
                      │    Ranked candidates → the accepted shortlist.   │
                      │    One dated entry per run in that challenge's   │
                      │    methods.md.                                   │
                      └──────────────────────────────────────────────────┘
```

## Current selection criteria

The selection rule is calibrated against real wet-lab outcomes (Adaptyv
N ≈ 2,600) with independent literature agreement (bioRxiv 2025.08.14.670059,
3,766 binders). Full sourcing, AUCs, and thresholds live in
[`notes/calibration.md`](notes/calibration.md) — that file is the live spec,
shared across every challenge, and is edited in place whenever thresholds
move.

Short version:

- **Shape complementarity ≥ 0.58** (Lawrence–Colman, 0–1 scale). Measured at
  two stages: at design time from BindCraft's `Average_ShapeComplementarity`,
  and again at cross-validation, where `redundancy.py` runs pyrosetta's
  `ShapeComplementarityFilter` on the Boltz complex itself. **The
  cross-validation value is the one that decides.** A biopython
  burial-fraction proxy exists as a flagged fallback and is never compared
  against the 0.58 bar — it is not Lawrence–Colman SC.
- **Primary rank + decision:** Boltz `ipSAE_min` ≥ 0.60 (Dunbrack 2025
  formulation — interface residues by PAE + pLDDT, TM-score `d0`, min across
  binder ↔ target chain directions).
- **`cross_val_pass`** = SC-pass AND ipSAE-pass. Both required.
- **Composite rank:** `ipsae_min * min(SC / 0.58, 1.0)`.
- **ipTM** and **pDockQ** are kept in the output as **informational only**
  (AUC 0.52 and 0.50 on Adaptyv respectively — at chance). They do not gate
  or rank.

## How to run it

Prerequisites: a Modal workspace (`pip install modal && modal token new`),
Python 3.11 for the design/cross-val paths, `biopython` for the local
hotspot tool.

Every command below takes `--target <slug>` — pick one per challenge
(`egfr` and `tnfa` are the two run so far) and use it consistently; it
namespaces outputs both in `challenges/` and on the Modal volume.

**Hotspot picking (local, no GPU):**
```
python3 modal/find_hotspots.py --pdb 1FLT --target V,W --partner X,Y --top-n 8
```
(Here `--target`/`--partner` are `find_hotspots.py`'s own chain-selection
flags, not the challenge slug — see `--help` for the full option set.)

**Design run on Modal (parallel, GPU):**
```
python3 -m modal run --detach modal/run_bindcraft.py::main \
  --target <slug> --pdb-id <PDBID> --target-chains <A,B> \
  --hotspots <A21,A25,A48,A63> --n 30 --run-tag hardtarget-focused4
```
Override any knob at the CLI (`--advanced-preset`, `--lengths`,
`--i-ptm-threshold`). Only run one detached app at a time — two concurrent
detached `python3 -m modal run` sessions from one client cancel each other.

**Cross-validation on Modal (Boltz-2, GPU):**
```
# smoke test on one accepted design:
python3 -m modal run --detach modal/redundancy.py::main --target <slug> --smoke

# full accepted shortlist:
python3 -m modal run --detach modal/redundancy.py::main --target <slug>
```

**Rescore already-run designs (CPU-only, no Boltz re-prediction):**
```
python3 -m modal run modal/redundancy.py::rescore_saved --target <slug> --smoke   # one design
python3 -m modal run modal/redundancy.py::rescore_saved --target <slug>           # full shortlist
```
Uses the cached `pae_*.npz` / `plddt_*.npz` / `confidence_*.json` that
`crossval_boltz` writes next to each design. Use this after a threshold
change in `calibration.md` so you don't pay for a GPU re-prediction just to
re-apply the scorer.

## Where things live

```
adaptyv-2026/
├── README.md               # this file — start here
├── .gitignore
├── modal/
│   ├── run_bindcraft.py      # target-agnostic parallel BindCraft on Modal (design stage)
│   ├── find_hotspots.py      # target-agnostic hotspot finder (local, no GPU)
│   └── redundancy.py         # target-agnostic Boltz-2 cross-validation + scoring
├── data/                    # shared, cross-challenge reference data (see data/README.md)
├── challenges/
│   ├── README.md             # per-challenge layout convention
│   ├── egfr/                 # Challenge 1 — complete, submitted 2026-10-05
│   │   ├── methods.md          # dated run log, including corrections to its own record
│   │   ├── submission-writeup.md  # the document submitted to Proteinbase
│   │   ├── submission.csv      # the 5 submitted designs
│   │   ├── lit/                # literature brief, epitope verification, sources
│   │   ├── l93_H36E/           # the pH-switch lead, 3 Boltz models
│   │   ├── fulllength-v3c/     # Stage 2 complexes, all 7 designs
│   │   └── v3c-core.log        # BindCraft run log (trajectory stats live here)
│   └── tnfa/                 # Challenge 2 — complete, submitted 2026-10-16
│       ├── methods.md          # pre-registration + Amendments 1–7, each dated
│       ├── submission-writeup.md  # the document submitted to Proteinbase
│       ├── submission.csv      # the 12 submitted designs
│       ├── generated-tables.md # result tables, regenerated from raw run JSON
│       ├── make_tables.py      # generates them — no hand-transcribed numbers
│       ├── crosscheck_submission.py  # verifies writeup ↔ CSV ↔ raw JSON agree
│       ├── epitope-analysis.md # cross-species epitope + cation anchor picks
│       ├── structures/         # reference PDBs (1TNF, 2TNF, 3ALQ, 7KP7, 7KPB)
│       └── crossreact-*.json   # Boltz-2 cross-species runs (raw results)
└── notes/
    ├── calibration.md        # LIVE thresholds + calibration sources, shared across challenges
    └── onboarding.md         # what a new collaborator reads first + role notes
```

Modal-side state that doesn't live in the repo, namespaced by `<slug>`:

- **`adaptyv-designs`** volume: BindCraft runs
  (`/<slug>/attempts/<run-tag>/<seed>/`), accepted designs,
  `mpnn_reprediction_log.csv`, `boltz_crossval/` output per design, and the
  aggregate `crossval.csv` / `crossval_rescore.csv` under `/<slug>/redundancy/`.
- **`af2-weights`** volume: AlphaFold2 params — shared across every
  challenge and this pipeline's predecessor project; fetched once via
  `download_weights`, never re-downloaded.
- **`boltz-weights`** volume: Boltz-2 checkpoints + CCD/mol data — same
  sharing story, fetched once via `download_boltz_weights`.

## Reading order

**If you're evaluating the work** rather than joining it, the two submission
writeups are the shortest path to what was done and how it was reported:
[`challenges/tnfa/submission-writeup.md`](challenges/tnfa/submission-writeup.md)
is the more developed of the two, and
[`challenges/egfr/submission-writeup.md`](challenges/egfr/submission-writeup.md)
is the first. Then
[`challenges/tnfa/methods.md`](challenges/tnfa/methods.md) if you want to check
that the rules really were fixed before the runs they govern — each amendment
names the commit that fixed it.

**If you're picking the work up:**

1. This README.
2. [`notes/calibration.md`](notes/calibration.md) — why the selection rule is what it is.
3. [`notes/onboarding.md`](notes/onboarding.md) — if you're joining, what to do first.
4. `challenges/<slug>/methods.md` for whichever challenge you're picking up — skim latest first.

## License

[MIT](LICENSE), covering everything in this repository.

The written record — `challenges/*/methods.md`, the submission writeups, and
`notes/calibration.md` — is additionally offered under
[CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/) for anyone who would
rather cite it under a content licence than a software one. Either is fine;
both ask only for attribution.

Designed sequences and predicted structures under `challenges/` are published
so the work can be checked and built on. If you use a design, please cite the
repository and the relevant `methods.md` entry — predictions here are
computational and, as of this writing, none has been validated at the bench.
