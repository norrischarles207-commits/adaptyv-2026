# challenges/

One subdirectory per challenge, named with the same slug you pass to
`--target` on `modal/run_bindcraft.py` and `modal/redundancy.py`. All the
per-challenge intellectual work — epitope selection, methods log, cross-val
results — lives here; the actual design PDBs and Boltz outputs live on the
`adaptyv-designs` Modal volume under `/designs/<slug>/`, namespaced the same
way.

Suggested layout for a new challenge (copy this shape, not literal files —
there's no template scaffold here on purpose, so a new challenge's structure
isn't forced into a shape that doesn't fit it):

```
challenges/<slug>/
├── README.md          # target intake: PDB source, chains kept, why
├── methods.md          # append-only historical log, same convention as
│                        # notes/methods.md used in the VEGF project this
│                        # pipeline was extracted from -- one dated entry
│                        # per run, never rewritten
├── epitope.md          # hotspot picks + rationale (literature + find_hotspots.py output)
└── target.pdb           # cleaned target structure (small enough to check in)
```

Cross-challenge pipeline code (`modal/*.py`) and the live scoring spec
(`notes/calibration.md`) stay at the repo root — they're shared. Only
target-specific decisions and results go under `challenges/<slug>/`.

See [`../notes/onboarding.md`](../notes/onboarding.md) for the full workflow
that runs when a new challenge target drops.
