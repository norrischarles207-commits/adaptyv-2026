# Onboarding

For a new collaborator joining the project. You should be able to be useful
within a day of reading the docs below and picking a role.

## Read these, in order

1. [`../README.md`](../README.md) — what the project is, the end-to-end
   pipeline, how to run each stage, where things live. ~10 minutes.
2. [`calibration.md`](calibration.md) — the live selection criteria and why
   they are what they are (Adaptyv N ≈ 2,600 real-outcome data + the 2025
   bioRxiv meta-analysis). Shared across every challenge; this is where
   thresholds actually get changed. ~10 minutes.
3. [`../challenges/README.md`](../challenges/README.md) — the per-challenge
   folder convention, then whichever `challenges/<slug>/methods.md` you're
   picking up. Skim latest entries first. Some early entries in a mature
   challenge may be marked `superseded` and annotated; that's intentional,
   don't rewrite them — the honest history of what we tried and why we
   changed course *is* the value. ~15 minutes.
4. The code path you'll actually work in — usually `modal/redundancy.py`
   (scoring / cross-val) or `modal/run_bindcraft.py` (design stage). ~30
   minutes.

If you've never used Modal: `pip install modal && modal token new`, then
run `python -m modal token current` to confirm the workspace shows up.

## Workflow when a new challenge target drops

Each new target (a weekly Adaptyv challenge, or a research target picked
independently) runs through the same 5-stage loop, under its own
`challenges/<slug>/` and its own `--target <slug>` on every pipeline command.
Time-box each stage — the loop is useful only if it turns.

1. **Target intake (~1 hour).** Find the best available complex structure
   (target + a natural partner: receptor, ligand, antibody, whatever gives
   the biological interface). Create `challenges/<slug>/`, add the cleaned
   target PDB, and write `challenges/<slug>/README.md`: which chains you
   kept, why, whether the crystal is bound or apo. If you drop chains or
   waters, say so.

2. **Epitope research (~2–4 hours).** Read enough of the target's
   literature to know *which face matters biologically*. Then run
   `modal/find_hotspots.py` against the complex to get contact-ranked
   residues on the target chain. Don't just take the top-N blindly —
   pick from the ones that both contact the partner **and** matter in
   the biology (surface accessibility, known mutagenesis, functional
   annotation). Record the hotspot string and the reason for each residue
   in `challenges/<slug>/epitope.md`.

3. **Design (~a few hours of wall time, budget dependent).** Kick off a
   BindCraft run on Modal against `--target <slug>`, with `--pdb-id`,
   `--target-chains`, and `--hotspots` matching what you decided in step 2.
   Start small — one attempt to sanity-check plumbing (`--n 1`), then a
   batch (say `--n 30`). The `--run-tag` flag namespaces the output further;
   use something readable like `hardtarget-focused4`. Only one detached
   `modal run` at a time from the same client — two cancel each other.

4. **Triage (~1 hour).** For the accepted designs, run cross-validation:
   `modal run --detach modal/redundancy.py::main --target <slug>`. Look at
   `crossval.csv` on the volume, under `/<slug>/redundancy/`. Anything that
   passes `cross_val_pass` is worth deeper inspection. Anything that clears
   ipSAE but not SC (or vice versa) is worth a second look — it usually
   points at the design's actual weakness. If thresholds move after this,
   edit `calibration.md` (shared across all challenges) and re-run
   `rescore_saved --target <slug>` (CPU-only, cheap).

5. **Writeup (~30 minutes).** One dated entry in `challenges/<slug>/methods.md`
   per run. Copy the previous block and fill it out honestly.
   `superseded` and `caveat` are first-class fields; use them freely. If you
   got 0 accepted, that's still an entry — the interesting part is *why*.

## Roles

Pick one to lead per target. All four roles overlap — nobody works in
isolation — but somebody should own each.

### Literature deep dive
Read the primary literature on the target: what it does, what binds it
natively, what's been tried therapeutically, which surfaces have known
mutagenesis, which are cryptic. Output: a one-page brief that answers
"if we can only grip one face of this thing, which face and why?"
Feeds directly into epitope research.

### Epitope research
Takes the literature brief and picks the actual hotspot residues. Runs
`find_hotspots.py` on the complex. Decides on focused-N vs broad
coverage. Sanity-checks the picks against surface accessibility and
conservation. Output: a hotspot string and a rationale line for
`challenges/<slug>/epitope.md`.

### Designability triage
Owns the design → cross-val loop for a given challenge. Kicks off
BindCraft runs, watches the funnel (gate-pass, MPNN, accepted), diagnoses
where designs die. Reads `mpnn_reprediction_log.csv` to distinguish
"near-miss" from "far-off." Runs `redundancy.py` on accepted designs.
Decides whether to oversample, switch to hard-target mode, adjust hotspots,
or move on. Output: a shortlist of designs that cleared `cross_val_pass`,
with a one-line reason for each.

### Methods writeup
Owns each challenge's `methods.md` and the eventual publication draft.
Makes sure every run — successful or not — gets a compact honest entry.
Watches for calibration drift across challenges (if the same failure mode
keeps showing up in more than one challenge, that's a `calibration.md`
change, not a per-run note in one challenge's log). Output: a methods
section that a reviewer or a competition judge can read end-to-end and
reproduce.

## Things worth knowing early

- **Never rewrite past `methods.md` entries**, in any challenge. If we
  changed our mind about something, mark the old entry `superseded` with a
  pointer to the new entry. The history is load-bearing.
- **Thresholds go in `calibration.md`, not in code comments**, and apply to
  every challenge. When a threshold moves, edit that file and re-run
  `rescore_saved --target <slug>` for any challenge you want re-scored.
- **`--target` is required on every pipeline command** and must be
  consistent across `run_bindcraft.py`, `redundancy.py`, and the
  `challenges/<slug>/` folder name for a given challenge — it's the only
  thing that ties a challenge's repo notes to its Modal volume state
  together.
- **Modal Starter plan is 10-wide.** N=30 runs in three waves, not
  all at once.
- **BindCraft's own CSV writers have no locking.** Each parallel
  worker writes to its own `design_path` (namespaced by seed +
  run_tag) — do not point two workers at the same directory.
- **The Boltz cross-val step persists `pae_*.npz` / `plddt_*.npz`**
  alongside each design's predicted PDB. That's what makes
  `rescore_saved` a CPU-only re-run — don't delete those files.
- **`af2-weights` and `boltz-weights` are shared across every challenge**
  and are never namespaced by target — they download once for the whole
  account and every challenge reuses them.
- **`ipTM` is informational, not a decision metric.** On real Adaptyv
  outcomes it's at chance (AUC 0.52). `calibration.md` is the current spec;
  don't rank or gate on it even if an old methods.md entry does (those
  were written before the calibration was done).
