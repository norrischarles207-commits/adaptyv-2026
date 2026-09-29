# EGFR — methods log

Append-only historical log, one dated entry per run or pass (see `../README.md`). Entries are never rewritten. The design-run entries from `brief.md` ("Methods-log seed") have not been added yet; this file starts with the literature pass.

---

## 2026-09-28 — Literature pass (M. lit review)

Files: `lit/hand-back.md` (structured hand-back plus post-review addendum), `lit/epitope-verification.md`, `lit/ph-strategy-notes.md`, `lit/precedent-adaptyv-egfr.md`, `lit/sources.md`. All residue numbers are precursor / UniProt P00533 numbering. Most primary pages were blocked; numbers marked "summarizer" were read through a page summarizer and none were checked against a downloaded PDF. This pass does not edit `brief.md`; where it disagrees with the brief the conflicts are raised in the PR.

What changed vs the working brief (five points; detail in the `lit/` files):

(1) The measured 24-residue patch is consistent with the Li (1YY9) and Sickmier (5SX4/5SX5) contact lists and 17 of 24 residues are mouse-conserved (our P00533 vs Q01279 alignment); N444 is an optional add and domain III identity is 87.3%, not 92% (BLOSUM62 similarity 93.1%), while the 6ARU author range "4–612, mature" remains unverified beyond sequence-identity checks. (2) The only EGFR acid-preferring precedent, antibody G532 (Liu 2022; WO2024109709A1, both summarizer-read), pairs binder Asp/Glu with EGFR histidines H433 and H370 (precursor numbering confirmed), the reverse of the brief's binder-His / E496 anchor; FcRn–Fc supports the brief's direction, so both are literature-supported and neither has been compared on EGFR. (3) The brief's 3.7–7.6 Å His placement window comes from His-to-cation distances in one acid-releasing design of bioRxiv 2025.09.29.678932, not a His-to-carboxylate rule (none was found), and realistic monovalent selectivity at pH 6.5 vs 7.4 is about 2–10x (G532: 13.26 human, 3.31 mouse), so the mouse and pH objectives may trade off. (4) In Adaptyv's prior round the 82 nM best de novo KD is Round 2 (Round 1 was 491 nM), the strict de novo hit rate is about 6% (12 of 206, our heuristic on github.com/adaptyvbio/egfr_competition_2), and ipTM is a weak filter (AUC 0.64–0.67) that does not rank affinity, while ipSAE and shape complementarity were never analysed and the epitope of the 82 nM binder is not stated. (5) Open for the team: choose the pH anchor(s), test ipSAE_min plus shape complementarity on the released AF2 structures and neutralisation data (unreachable from our sandbox), and confirm the 6ARU range from the mmCIF.
