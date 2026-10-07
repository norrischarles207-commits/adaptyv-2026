# TNF-α target preparation — decisions needed before any run

2026-10-07. Mature TNF numbering 1–157 throughout.

## Pipeline supports this without code changes

`[measured]` `run_bindcraft.py` already takes comma-separated `--target-chains`
and filters by membership, so a two-chain target works as-is. The residue range
applies uniformly to every kept chain, which is correct here because TNF is
1–157 on all protomers. Hotspots are already chain-prefixed in the interface
(`A21,A25,…`). **No code change required.**

Note the function fetches the PDB from RCSB itself, inside Modal. Our local
copies under `structures/` are for analysis only; the run does not use them.

## Groove orientation `[measured]`

`groove_orientation.py` on 1TNF: grooves run **B→A, C→B, A→C** at 3.25, 3.44
and 3.65 Å. The reverse pairings are 17.7–18.4 Å apart — no site. Three-fold
symmetry, as expected.

For a two-chain slice of 1TNF:

| chain | presents | residues |
|---|---|---|
| **B** | face 1 — 87% conserved | 143, 144, 145, 146, 32, 33, 113, 115, 149 |
| **A** | face 2 — 60% conserved, densest contacts | 86, 87, 90, 91, 75, 77 |

Chain IDs are per-structure: in 3ALQ the same faces fall on A and B
respectively. Only the relationship transfers, not the letters.

## Decision 1 — which structure

| option | for | against |
|---|---|---|
| **1TNF, chains B+A** | wild-type sequence; 2.60 Å; apo, nothing to strip | apo conformation, not the receptor-bound one |
| 3ALQ, chains A+B | receptor-bound conformation, which is what a blocker must complement | six engineered lysine substitutions; 3.00 Å |

`[inferred]` Recommend **1TNF**. Sequence fidelity matters more than the
conformational difference, which the literature describes as small — individual
protomers keep their fold on receptor binding, and the site is formed by
inter-protomer geometry rather than intra-protomer change. Using a six-fold
mutant as the design target would also put an asterisk on every downstream
number.

## Decision 2 — hotspot set, needs pre-registering

Size: the EGFR round used 4 hotspots in the arm that produced every submitted
design; the 7-hotspot arm was retired. Treat 4–6 as the working range.

Candidate, weighted toward the conserved face and keeping the two densest
conserved contacts from the other:

```
B143, B145, B146, A86, A87
```

`[inferred]` Rationale: 143–146 is the only four-long conserved run in the
consensus epitope, is on the 87%-conserved face, and is independently supported
by mutagenesis (143–145 TNFR1-weighted; E146K activity-reducing, Van Ostade
1991). 86 and 87 are the densest contacts in the entire site — 42 and 45 atom
pairs against a typical 5–20 — and both are conserved. 144 is omitted to keep
the set at five; it can be swapped for 145 if the energetic data favour it.

Deliberately excluded: **71, 72, 73, 89** — the indel, the human-only histidine
and both charge changes. Steering a binder onto those trades objective 2 away.

**Open and blocking:** which of these contacts carry binding energy. Structure
cannot answer it. If the mutagenesis item from the literature pass does not land
in time, pre-register on contact density plus conservation and say so
explicitly, rather than waiting past the point where a failed probe can still be
redone.

## Decision 3 — binder length

EGFR used `--lengths 60,100` and the submitted designs came out 64–93 aa. This
challenge allows 10–250. No reason to change; a groove-binding minibinder in the
same range is the proven configuration.

## Memory risk, untested

`[measured]` EGFR: a 204-residue target ran fine on the 24 GB A10G; the
untruncated 609-residue chain requested 29.26–42.59 GiB and OOM'd on every seed.

`[inferred]` Two TNF protomers is **314 residues** — between the two, closer to
the one that worked, but not tested. **Run a single seed before any fan-out.**
