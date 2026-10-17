# challenges/

One subdirectory per challenge, named with the same slug you pass to
`--target` on `modal/run_bindcraft.py` and `modal/redundancy.py`. All the
per-challenge intellectual work — epitope selection, methods log, cross-val
results — lives here; the bulk design PDBs and Boltz outputs live on the
`adaptyv-designs` Modal volume under `/designs/<slug>/`, namespaced the same
way.

## What's here

| challenge | target | status |
|---|---|---|
| [`egfr/`](egfr/) | EGFR — pH-conditional binding | submitted 2026-10-05 |
| [`tnfa/`](tnfa/) | TNF-α — pH-conditional + mouse cross-reactive | submitted 2026-10-16 |
| `glp1r/` | GLP1R — agonist: binding **and** receptor activation | in progress |

Each challenge directory opens with its own `README.md` mapping that
challenge's files and flagging anything a reader would otherwise misread.
Start there rather than in `methods.md`, which is long by design.

## The shape a challenge takes

There is no template scaffold here on purpose — a new challenge shouldn't be
forced into a shape that doesn't fit it. In practice each has grown the same
four files:

```
challenges/<slug>/
├── README.md              # file map + anything a reader would misread
├── methods.md             # append-only dated log; entries are never
│                          #   rewritten, only marked `superseded`
├── submission-writeup.md  # the document submitted to Proteinbase
└── submission.csv         # the submitted sequences
```

Past that the two completed challenges diverge, and the divergence is
deliberate rather than drift:

- **`egfr/`** keeps its literature pass in [`lit/`](egfr/lit/), where every
  number carries a provenance label (`[computed]` from raw data vs read
  through a summarizer and still needing a spot-check) and the residue
  numbering convention is restated at the top of every file — the EGFR
  literature mixes precursor and mature numbering freely, so an unlabelled
  number is a trap.
- **`tnfa/`** splits the same work into `epitope-analysis.md` and
  `target-prep.md`, and generates every result table from raw run JSON via
  `make_tables.py`, so no number in the writeup is hand-transcribed.
  `crosscheck_submission.py` then verifies writeup ↔ CSV ↔ raw JSON agree and
  exits non-zero if they don't.

Cross-challenge pipeline code (`modal/*.py`) and the live scoring spec
(`notes/calibration.md`) stay at the repo root — they're shared. Only
target-specific decisions and results go under `challenges/<slug>/`.

See [`../notes/onboarding.md`](../notes/onboarding.md) for the full workflow
that runs when a new challenge target drops.
