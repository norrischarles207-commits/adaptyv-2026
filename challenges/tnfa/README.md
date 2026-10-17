# Challenge 2 — TNF-α conditional binder

Track 3, submitted 2026-10-16. Twelve de novo designs, 60–97 aa, over eight
independent backbones.

The organisers **number** the objectives 1 = human affinity, 2 = mouse
cross-reactivity, 3 = pH selectivity, but **rank** them in the reverse order.
Every document in this directory is organised in **ranked** order and labels
each section with the organisers' number, so the two cannot be confused.

## Start here

| file | what it is |
|---|---|
| [`submission-writeup.md`](submission-writeup.md) | The submitted document — rationale, every measurement, sixteen limitations. |
| [`methods.md`](methods.md) | Pre-registration plus Amendments 1–7. Each amendment is dated and names the commit that fixed it *before* the run it governs. |
| [`submission.csv`](submission.csv) | The twelve submitted sequences, in submitted order. |
| [`generated-tables.md`](generated-tables.md) | Every result table, regenerated from raw run JSON by `make_tables.py`. |
| [`epitope-analysis.md`](epitope-analysis.md) | Cross-species epitope intersection and the four conserved cation anchors. |
| [`target-prep.md`](target-prep.md) | Which PDB, which chains kept, what was stripped. |

## The cross-species runs — and why the primary file ends in `.partial`

Three independent Boltz-2 co-folding runs back the pH result. Each folds
designs against the full human and mouse TNF-α **trimers** at 10 diffusion
samples per species.

| file | run | scope |
|---|---|---|
| `crossreact-n10.json` | 1 | top 3 designs only |
| `crossreact-all12-n10.json.partial` | 2 | **all 12 designs — the primary dataset** |
| `crossreact-rep2.json` | 3 | replication of the two confirmed designs (Amendment 5) |

**Run 2's file is a checkpoint, and that is not a defect.** The run folded all
12 designs on both arms, then crashed inside its own summary step on a `None`
mean — the exact bug Amendment 6 was written to fix — before the final
`json.dump` ran. What survived is the per-design checkpoint the run writes
after every fold, and it holds all 12 designs, both species, 10 samples each.
It is complete data from an incomplete program, not a truncated run.

`make_tables.py`, `analyze_all12.py` and `crosscheck_submission.py` all read it
directly. The filename is left as the run wrote it rather than tidied, because
what happened to that run is part of the record — and the failure itself is
what motivated the checkpointing fix in `modal/redundancy.py`.

Smoke and development runs (`crossreact-smoke`, `-trimer-smoke`, `-patchsmoke`)
are kept for provenance and feed no table.

## Reproducing the numbers

No number in the writeup is hand-transcribed. From the repository root:

```
python3 challenges/tnfa/make_tables.py            # regenerate every result table
python3 challenges/tnfa/crosscheck_submission.py  # verify writeup <-> CSV <-> raw JSON
```

`crosscheck_submission.py` exits non-zero if any stated figure disagrees with
the raw data. It *parses the numbers out of the writeup* and recomputes them
from the run JSON, rather than comparing against constants held inside the
checker — so a wrong number in the writeup fails the check instead of passing
it. That distinction was the point: an earlier version compared three figures
against literals hardcoded in the checker, which would have let a wrong writeup
value pass. It also caught a real transcription error (a standard deviation
written as 0.031 when the data said 0.030).

## Structures

- `structures/` — reference PDBs. **7KP7** is human TNFR1 bound to *mouse*
  TNF-α at 2.65 Å and is the structural basis of the cross-reactivity argument;
  **7KPB** is the wild-type structure used for target prep; **3ALQ** carries
  K65S, which is why the K65 anchor was invisible until 7KPB and 7KP7 were
  added; **1TNF** and **2TNF** are human TNF-α references.
- `structures/confirmed/` — predicted complexes for the two designs that
  cleared the pH bar under replication (`l69_mpnn1`, `l91_mpnn1`), pulled from
  the Modal volume. These are the structures behind the headline claim.

## Logs

`tnfa-v*-core*.log` are BindCraft design-run logs; `crossreact-*.log` are the
Boltz-2 cross-species runs. They are the raw provenance behind the `methods.md`
entries and are kept deliberately rather than pruned.
