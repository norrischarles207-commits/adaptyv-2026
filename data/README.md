# data/

Shared, cross-challenge reference data — not any single challenge's target or
results. Examples of what belongs here:

- Cached RCSB downloads reused across challenges (rare; most challenge PDBs
  are challenge-specific and live under `challenges/<slug>/`).
- Reference datasets used to calibrate scoring, e.g. an exported copy of the
  Adaptyv outcome data or the bioRxiv meta-analysis supplementary table that
  `notes/calibration.md` cites (only if small enough to check in; link out
  instead of committing anything large).
- Any lookup table (e.g. a conservation-score cache) meant to be reused by
  more than one challenge's `find_hotspots.py` run.

Per-challenge inputs (target PDBs, hotspot picks, designs) belong under
`challenges/<slug>/`, not here — this directory is for things that don't
belong to one challenge.
