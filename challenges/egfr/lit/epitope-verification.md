# EGFR epitope verification (literature pass, Prompt 1 + numbering/mouse follow-ups)

**All residue numbers are precursor / UniProt P00533 numbering (signal peptide counted; L25 = mature L1) unless labelled "mature".** Precursor = mature + 24.

Verification labels used below:
- **[computed]** recomputed by us from sequences (P00533, Q01279, the 6ARU chain A sequence). Scripts: `xref.py`, `mouse.py` (session scratchpad, not committed).
- **[secondhand]** taken from a patent or secondary text, not the primary paper.
- **[summ]** read through a page summarizer, not raw text.

## 1. Numbering

- Precursor = mature + 24. Li cetuximab residues converted at this offset match the 6ARU chain A sequence with no identity mismatches (mature S468 = precursor S492) [computed].
- **Not verified:** the brief's claim that 6ARU chain A spans author residues 4–612 in mature numbering, and the 1YY9 range. SIFTS, PDBsum, PDBe and the deposition paper were all blocked or rate-limited. The offset is supported only by sequence identity checks, not by an independent structural-database mapping. Please confirm the range from the mmCIF `_struct_ref_seq` / `_pdbx_poly_seq_scheme` records directly.
- Liu et al. 2022 (EGFR antibody G532) uses **precursor** numbering. Evidence: the paper gives the ECR as Leu25–Ser645 and domain III as "Lys335–Lys538"; K335 and K538 are lysines in P00533 precursor numbering. The patent WO2024109709A1 lists "H370, H433, R377, L406, Q435, K489"; at these precursor numbers P00533 has H, H, R, L, Q, K. Under mature numbering those positions would be I370 (mature) and S433 (mature). Precursor 457 is S, so "H433 = precursor H457" is ruled out [summ; two independent summarized sources agree; sequence check computed].
- Adaptyv's advised epitope "residues 11-13, 15-18, 356, 440-441" is almost certainly **mature** (1IVO-style) numbering: precursor 11–18 lies inside the signal peptide. In precursor numbering it is 35–37, 39–42 (domain I), 380, and **464–465** (domain III) [computed; the numbering convention itself is an inference, the blog does not state it].

## 2. Cetuximab domain III contacts (Li 2005, PDB 1YY9)

Source: Li et al. 2005, Cancer Cell, via the patent text [secondhand]. Mature numbers as published; precursor = +24.

| Mature | Precursor | Residue (6ARU seq) | In measured 24? | Mouse |
|---|---|---|---|---|
| 353 | 377 | R | yes | K (divergent) |
| 384 | 408 | Q | yes | conserved |
| 408 | 432 | Q | yes | conserved |
| 409 | 433 | H | yes | conserved |
| 412 | 436 | F | yes | conserved |
| 418 | 442 | S | yes | G (divergent) |
| 440 | 464 | S | yes | conserved |
| 443 | 467 | K | yes | R (divergent) |
| 465 | 489 | K | yes | conserved |
| 467 | 491 | I | yes | M (divergent) |
| 468 | 492 | S | yes | N (divergent) |
| 473 | 497 | N | yes | K (divergent) |

All 12 Li residues are in the measured 24.

## 3. Panitumumab domain III contacts (Sickmier et al. 2016; PDB 5SX4, resistance-mutant 5SX5)

Sickmier and colleagues describe the panitumumab–domain III structure. I did not read the paper directly; residue lists are from secondary text [secondhand].

| Mature | Precursor | Residue | In measured 24? |
|---|---|---|---|
| 384 | 408 | Q (text says N384, see anomalies) | yes |
| 418 | 442 | S | yes |
| 420 | 444 | N (text says D420, see anomalies) | **no** |
| 440 | 464 | S | yes |
| 443 | 467 | K | yes |
| 465 | 489 | K | yes |
| 466 | 490 | I | yes |
| 468 | 492 | S | yes |
| 469 | 493 | N | yes |

Sickmier resistance-site mutation positions (5SX5): mature 440, 441, 443, 467 = precursor **464, 465, 467, 491**. S468R (mature) = S492R (precursor).

**Text anomalies excluded or caveated:** "N384" (the sequence and Li both have Q384); "D420" (an engineered N420D; native is N444 in precursor); "Ser404" (the sequence has G404 mature, precursor 428).

## 4. Other literature residues

Voigt et al. (functional epitope dissection, secondhand; the publication year is unresolved between my notes and the brief's 2014 mAbs link, please check against https://www.tandfonline.com/doi/pdf/10.4161/mabs.28915): mature 349, 355, 412, 438 = precursor **373, 379, 436, 462**. Of these only 379 (D379) is outside the measured 24.

## 5. Union, and diff against the measured 6ARU contact list

Union of the Li and Sickmier text lists (precursor): 377, 408, 432, 433, 436, 442, 444, 464, 467, 489, 490, 491, 492, 493, 497 (plus 465 as a Sickmier resistance site).

**Measured 24 (any atom within 4.5 Å of the Fab, from the brief):** 373 P, 374 V, 377 R, 406 L, 408 Q, 432 Q, 433 H, 435 Q, 436 F, 439 A, 441 V, 442 S, 462 I, 464 S, 465 G, 467 K, 489 K, 490 I, 491 I, 492 S, 493 N, 495 G, 496 E, 497 N.

- **Literature epitope not in the measured list:** N444 (panitumumab); D379 (Voigt-only). Optional add: 444 (mouse-conserved). 379 is low confidence.
- **In the measured list but not in the literature union:** 374, 406, 435, 439, 441, 495, 496. These look like peripheral 4.5 Å contacts, since the literature lists are H-bond-centric. We found no literature support. **No residue should be removed on this evidence.**
- **Voigt-supported members of the measured 24:** 373, 436, 462.

## 6. Mouse conservation

Index-wise alignment of P00533 vs Q01279, first 660 residues [computed]: 85.5% identity. **Domain III identity, by window [computed]:**

| Window (precursor) | Identical | Identity |
|---|---|---|
| Domain III K335–K538 (Liu 2022 boundaries) | 178/204 | 87.3% |
| Domain III 334–538 | 179/205 | 87.3% |
| Domain III 358–538 | 156/181 | 86.2% |
| ECD 25–645 | 545/621 | 87.8% |
| First 660 residues | 564/660 | 85.5% |

The working brief's "92% domain III identity" does not reconcile with these identity figures. BLOSUM62-positive similarity over 335–538 is 93.1% (358–538: 92.3%), so the brief's number may be similarity, not identity. This is a guess; we do not know how the brief computed it.

**Measured 24 contacts, mouse status [computed]:**
- Conserved (17): 373, 374, 406, 408, 432, 433, 435, 436, 439, 441, 462, 464, 465, 489, 490, 493, 496.
- Divergent (7): 377 R→K, 442 S→G, 467 K→R, 491 I→M, 492 S→N, 495 G→A, 497 N→K.

**All 26 human→mouse differences in domain III (334–538):** S348T, N361Y, S364A, R377K, H383R, Q390R, D393E, E412D, R414W, S442G, K467R, S484P, G485N, I491M, S492N, G495A, N497K, S498D, T502V, G503N, Q504H, H507N, A508P, P512S, R527Q, D537E (26 of 205 positions). Non-contact differences: 348, 361, 364, 383, 390, 393, 412, 414, 484, 485, 498, 502, 503, 504, 507, 508, 512, 527, 537.

**N-glycan sequons (N-X-S/T, positions 1–640) [computed]:** human 128, 175, 196, 352, 361, 413, 444, 528, 568, 603, 623; mouse lacks 361 (N361Y). N444 is a panitumumab contact and its sequon is conserved.

**Histidines in domain III:** human 358, 370, 383, 418, 433, 507. Mouse-conserved: 358, 370, 418, 433. Lost in mouse: 383 (H383R), 507 (H507N).

**What we did NOT find:** a primary source that attributes cetuximab's lack of mouse cross-reactivity to these specific seven residues. The brief's statement that the divergent residues are "exactly why cetuximab does not cross-react with mouse" is a sequence-level inference only. Panitumumab mouse cross-reactivity was not directly evidenced. Both are "not found in literature".

## 7. Sources

- PDB 1YY9 (cetuximab Fab:sEGFR, Li 2005): https://www.rcsb.org/structure/1YY9
- PDB 6ARU (cetuximab Fab variant with wild-type EGFR): https://www.rcsb.org/structure/6ARU
- PDB 5SX4, 5SX5 (panitumumab:domain III, Sickmier 2016): https://www.rcsb.org/structure/5SX4 , https://www.rcsb.org/structure/5SX5
- US 9,540,450 (secondhand source for Li 2005 residues): https://patents.google.com/patent/US9540450B2/en
- UniProt P00533: https://www.uniprot.org/uniprotkb/P00533 ; Q01279: https://www.uniprot.org/uniprotkb/Q01279
- Liu et al. 2022, Mol Ther Oncolytics (numbering evidence): https://www.sciencedirect.com/science/article/pii/S237277052200136X
- WO2024109709A1 (numbering evidence): https://patents.google.com/patent/WO2024109709A1/en
- Adaptyv blog po104 (organiser-advised epitope): https://www.adaptyvbio.com/blog/po104/

## 8. Liu 2022 interface residues vs the measured 24 (added 2026-09-29)

Liu et al. 2022 / WO2024109709A1 name H370, H433, R377, L406, Q435 and K489 as EGFR interface residues in the G5V2 model (precursor numbering, confirmed in section 1). **Five of the six (H433, R377, L406, Q435, K489) are in the measured 24; H370 is not.** This is weak convergent evidence only: the model was manually docked using cetuximab:EGFR (1YY9) as template, so overlap with the cetuximab contact set is expected by construction, and it is not an independent epitope measurement [summ]. Source: https://www.sciencedirect.com/science/article/pii/S237277052200136X ; https://patents.google.com/patent/WO2024109709A1/en
