# TNF-α epitope analysis — computed from coordinates

2026-10-07. All numbers **mature TNF-α 1–157** (UniProt P01375 = mature + 76;
P06804 = mature + 79). Scripts: `tnfr_contacts.py`, `epitope_intersect.py`,
alignment from `tnf_align.py`. Contacts are any heavy atom within **4.5 Å**.

`[measured]` unless marked otherwise.

## Structures used, and what is wrong with each

| PDB | contents | res. | defect |
|---|---|---|---|
| 3ALQ | TNF **A–F**, TNFR2 **R–W** | 3.00 Å | TNF is a lysine-deficient variant: K11M, K65S, K90P, K98R, K112N, K128P |
| 7KPB | TNF **A,B,C**, TNFR1 **E,F**, Fab1974 **H,L** | 3.00 Å | wild-type TNF; third receptor groove occupied by the Fab |
| 1TNF | human trimer | 2.60 Å | apo |
| 2TNF | mouse trimer | 1.40 Å | apo; best resolution in the set |

**Chain IDs corrected.** TNFR2 in 3ALQ is **R–W**, not G–L. The RCSB summary
page gave G–L and was wrong; a script using it finds zero contacts.

**Fab1974 is not a confound.** In 7KPB the two TNFR1 chains contact protomers
A/B/C across two grooves and the Fab spans A and C — the third groove. It is a
receptor-site blocker occupying the same epitope, so its footprint is a third
independent read, not a perturbation.

## Contact sets

- **TNFR2** (3ALQ): 32 positions — 20, 21, 23, 31, 32, 33, 63, 67, 71, 72, 73,
  75, 77, 85, 86, 87, 88, 89, 90, 91, 92, 97, 111, 113, 115, 128, 137, 143,
  144, 145, 146, 149
- **TNFR1** (7KPB): 32 positions — 20, 21, 23, 30, 31, 32, 33, 65, 66, 67, 73,
  75, 77, 82, 85, 86, 87, 89, 90, 91, 97, 110, 113, 115, 135, 137, 143, 144,
  145, 146, 147, 149
- **Shared by both receptors: 25 positions.**

Receptor-selective: TNFR2-only 63, 71, 72, 88, 92, 111, 128 · TNFR1-only 30,
65, 66, 82, 110, 135, 147.

## The decision

Of the 25 consensus positions, **19 are conserved human/mouse**:

```
21, 23, 32, 33, 67, 75, 77, 86, 87, 90, 91, 113, 115, 137, 143, 144, 145, 146, 149
```

Contiguous runs: **143–146**, 86–87, 90–91, 32–33, and singletons.

Six are divergent: 20 (P→H), 31 (R→Q), 73 (H→Y), 85 (V→I), 89 (T→E), 97 (I→V).
Two of those (85, 97) are conservative hydrophobic swaps. The real species
liabilities inside the epitope are **20, 31, 73, 89**, of which 31 and 89 are
charge changes.

`[measured]` **D140K, the only full charge reversal in the alignment, is not in
either receptor contact set.** The worst species difference does not touch the
epitope.

## The histidine result

`[measured]` **The conserved consensus epitope contains no histidine.** Human
H15 and H78 are conserved but neither contacts a receptor; H73 contacts both
receptors but is tyrosine in mouse.

`[measured]` Each species carries an interface histidine the other lacks, at
different positions:
- **73** — His in human, Tyr in mouse
- **20** — Pro in human, **His** in mouse

`[inferred]` Two consequences. First, any pH mechanism built on a *target*
histidine is species-specific by construction and would trade objective 3
against objective 2 — the same trap that cost us a combined lead in Challenge 1,
visible here before any compute. Second, because the conserved surface carries
no titratable residue, **all pH machinery has to come from the binder**, which
means objectives 2 and 3 do not compete at the target level. That is the
opposite of the EGFR round and it is good news.

## Candidate anchor

`[inferred]` **143–146** is the strongest starting point: the only four-residue
conserved run in the consensus epitope, contacts both receptors, and is
independently supported by mutagenesis — the literature pass reports 143–145 as
TNFR1-weighted and E146K as activity-reducing (Van Ostade 1991, PMID 2009860).
Convergence of a structural result and a functional one on the same stretch is
worth more than either alone.

Not a decision. The epitope is not chosen until the hotspot set is pre-registered.

## Caveats

- 3ALQ contacts at **90** and **128** are to engineered residues (K90P, K128P),
  not wild-type lysine. 7KPB shows wild-type Lys90 in contact, so position 90 is
  corroborated; 128 is TNFR2-only and rests on the mutant alone.
- Both complexes are 3.00 Å. Side-chain positions at that resolution carry real
  uncertainty; the contact *set* is more reliable than any individual distance.
- Contacts are geometric. Which of them carry binding energy is not answerable
  from structure — that is the open literature-pass item.
