# EGFR literature pass — hand-back

The block below is the step-6 hand-back **verbatim**, as reviewed in the working thread on 2026-09-28. Three items were flagged for follow-up after review; their resolutions are in the **Addendum** at the end, not edited into the block. All residue numbers are precursor / UniProt P00533 numbering.

```text
===== EGFR LIT PASS — HAND-BACK =====

Scope note: Prompts 1–5 are done. Numbers marked [computed] are mine, from the raw data or sequences. Numbers marked [summ] passed through a page summarizer and were not checked against the original tables. Most primary pages (PMC, PubMed, Cell, RCSB via shell) were blocked. Every residue number below is precursor/UniProt P00533 numbering (precursor = mature + 24) unless I say otherwise.

CONFIRMED
- Precursor = mature + 24. The Li cetuximab residues, converted to precursor, match the 6ARU chain A sequence with no identity mismatches (mature S468 = precursor S492) [computed] — PDB 6ARU https://www.rcsb.org/structure/6ARU ; PDB 1YY9 https://www.rcsb.org/structure/1YY9
- Cetuximab domain III contacts (precursor): 377, 408, 432, 433, 436, 442, 464, 467, 489, 491, 492, 497. This is from Li 2005 (1YY9), secondhand through the patent text — https://patents.google.com/patent/US9540450B2/en
- Panitumumab domain III contacts (precursor): 408, 442, 444, 464, 467, 489, 490, 492, 493. Panitumumab resistance-site mutants: 464, 465, 467, 491. Both from Sickmier 2016, structures 5SX4 and 5SX5 (S468R mature = S492R). Read secondhand; I did not read the paper — https://www.rcsb.org/structure/5SX4 ; https://www.rcsb.org/structure/5SX5
- Voigt 2012 (secondhand) adds 373, 379, 436, 462. Only 379 is outside your 24.
- Mouse conservation: 17 of your 24 contacts are conserved and 7 diverge. The divergent ones are 377 R→K, 442 S→G, 467 K→R, 491 I→M, 492 S→N, 495 G→A, 497 N→K. This is my index-wise alignment of P00533 vs Q01279 over the first 660 residues (85.5% identity) [computed] — https://www.uniprot.org/uniprotkb/P00533 ; https://www.uniprot.org/uniprotkb/Q01279
- Mouse also lacks the N361 sequon (N361Y). The other divergent domain III positions (334–538) are all outside your contacts [computed] (same UniProt entries).
- Genuine de novo hit rate in the prior Adaptyv round was low, and the best de novo binder was about 82 nM (details under PRECEDENT) — https://www.biorxiv.org/content/10.1101/2025.04.17.648362v2 ; https://github.com/adaptyvbio/egfr_competition_2

CORRECTIONS
- The 6ARU chain A range "4–612, mature numbering" was NOT verified independently. SIFTS, PDBsum, PDBe and the deposition paper were all blocked or rate-limited. The +24 offset is supported only by the sequence identity checks above. The 1YY9 range is also unverified — not found in literature (as reachable here).
- Sickmier text anomalies: it says N384 but the sequence has Q384; D420 is the engineered N420D; "Ser404" is really G404. I excluded or caveated all three [computed] — PDB 5SX4 / 6ARU sequence.
- Your contacts 374, 406, 435, 439, 441, 495, 496 are not in the literature union. They look like peripheral 4.5 Å contacts, and the literature lists are H-bond-centric. I found no literature support for them, and I did not remove any.
- Literature residues not in your list: N444 (panitumumab) and 379 (Voigt only) — Sickmier 2016 via 5SX4; Voigt 2012, secondhand.
- Attribution gap: I did not find a primary source that names these seven residues as the reason cetuximab doesn't cross-react with mouse. Panitumumab mouse cross-reactivity is also not directly evidenced. Both are not found in literature. The mouse-divergence result is sequence-level only.
- Prompt 5 premise mismatches:
  - The Baker preprint (bioRxiv 2025.09.29.678932) describes His-to-cation geometry and buried His networks, not His-to-acid geometry. All its designs weaken at low pH, and it reports no His-to-carboxylate distances [summ] — https://www.biorxiv.org/content/10.1101/2025.09.29.678932v1.full
  - "Sarkar et al. 2019 anti-CD20" was not found. The likely intended paper is Sarkar 2002 on G-CSF — https://www.nature.com/articles/nbt725
  - Igawa 2010 gives endosomal pH 6.0, not 5.8 (abstract only) — https://www.nature.com/articles/nbt.1691
  - "Strop 2012 J Mol Biol" was not found. The pH-sensitive anti-PCSK9 paper is Chaparro-Riggers 2012, JBC — https://pmc.ncbi.nlm.nih.gov/articles/PMC3322827
  - The preLights His–Arg distances (5.7 and 7.8 Å) and "10^8-fold at pH 6.4" conflict with or are absent from the preprint text. The preprint gives 3.7, 7.6 and 4.9 Å [summ]. I don't treat either set as established — https://prelights.biologists.com/highlights/computational-design-of-ph-sensitive-binders/
- Adaptyv numbers differ by source. The best de novo KD is 82 nM in the raw data and the preprint, but 91.5 nM in the Adaptyv blog [summ]. The BindCraft hit rate is 6 of 65 in the blog and 6 of 49 by my count of the results file's design-method labels. I did not reconcile these — https://www.adaptyvbio.com/blog/po104/
- The headline "14% hit rate" (53 of 378) is not a de novo rate, because it includes EGF/TGFα variants and antibody-derived designs. This classification is my sequence heuristic, not the organisers'.
- Your "ipTM is noise" premise is only partly supported (details under PRECEDENT).

EPITOPE (precursor numbering)
- Final contact-residue list (add/remove vs the measured 24):
  - Keep all 24: 373, 374, 377, 406, 408, 432, 433, 435, 436, 439, 441, 442, 462, 464, 465, 467, 489, 490, 491, 492, 493, 495, 496, 497.
  - Add optionally: 444 (panitumumab; mouse-conserved).
  - 379 is Voigt-only, so I treat it as low confidence and would not add it.
  - Remove: none.
  - Your five resistance-linked sites are 464, 465, 467, 491 and 492 (Sickmier 2016 via 5SX5, secondhand). Three of your planned "avoid" sites, 467, 491 and 492, are mouse-divergent.
- Mouse-conserved (17): 373, 374, 406, 408, 432, 433, 435, 436, 439, 441, 462, 464, 465, 489, 490, 493, 496.
- Mouse-divergent (7): 377, 442, 467, 491, 492, 495, 497. Non-contact His differences: H383R and H507N.
- Mouse-conserved histidines in domain III: 358, 370, 418, 433 [computed] (UniProt entries above).

pH STRATEGY
- Best-supported mechanism from the literature:
  - The best-supported mechanism for acid-preferring binding is an Asp/Glu on the binder pairing with an antigen histidine, so binding strengthens when the histidine is protonated at pH 6.5. This is the design logic of the EGFR domain III antibody G532. It came from structure-guided Asp/Glu substitution against antigen histidines, not His scanning — Liu et al. 2022, Mol Ther Oncolytics [summ] https://www.sciencedirect.com/science/article/pii/S237277052200136X ; patent https://patents.google.com/patent/WO2024109709A1/en
  - Supporting mechanism: the FcRn His–carboxylate salt bridges — Martin 2001 https://pubmed.ncbi.nlm.nih.gov/11336709/ ; Ying 2014 (Å distances 2.70–2.91, unverified) https://www.frontiersin.org/journals/immunology/articles/10.3389/fimmu.2014.00146/full
  - The His–Arg/Lys repulsion and buried-network mechanisms produce acid-releasing designs, the wrong direction. Sulea 2020 (HER2) and La Sala 2026 (CD3, Asp/Glu without His) are the other acid-preferring examples — https://pmc.ncbi.nlm.nih.gov/articles/PMC6927761 ; https://www.dora.lib4ri.ch/psi/dload/psi:86933/PDF/La_Sala-2026-Engineering_of_acidic_pH-responsive_anti-CD3-(published_version).pdf
  - No de novo or computationally designed acid-preferring binder was found in literature (search not exhaustive).
- Which acidic anchor residue on EGFR you'd design toward:
  - Design toward H433 (in your epitope, and the Li cetuximab contact mature H409) and H370 (just outside your 24). G532 is reported to engage both. Both histidines are also mouse-conserved by my alignment.
  - The His-numbering inference is mine: H370 and H433 are histidines only under precursor numbering, since mature 370 is I and mature 433 is S in the 6ARU sequence [computed]. So Liu 2022 appears to use precursor numbering, but I did not confirm this from the paper.
  - Do not anchor on H383 or H507, which are lost in mouse.
  - The binder-side acidic residue would be Asp or Glu placed to reach the histidine. The literature gives no numeric His-to-carboxylate design window or burial threshold — not found in literature.
- Realistic pH-selectivity ratio for a 6.5-vs-7.4 window based on published work:
  - Expect about 2–10x monovalent. The best EGFR precedent is G532 at a KD(7.4)/KD(6.5) of 13.26 on human EGFR and 3.31 on mouse, as a bivalent IgG [summ] (Liu 2022 link above).
  - A single His with pKa 6.0–6.4 caps at about 5–6x by Henderson–Hasselbalch (my arithmetic, not from a paper).
  - Ratios above 10x in narrow windows mostly come from cell or functional assays. Examples: Sulea 2020 HER2 cells at pH 6.8 vs 7.3 (over 10x) and the acid-Fc paper (about 2x binding vs about 20x ADCC) — https://pubmed.ncbi.nlm.nih.gov/35248534/
  - No paper found reports a monovalent KD ratio above about 10 at 6.5 vs 7.4 (search not exhaustive).
  - The lower mouse ratio for G532 (3.31) suggests mouse cross-reactivity may cost selectivity. The cause is unknown.

PRECEDENT (prior Adaptyv EGFR round + Proteinbase)
- De novo hit rate and best de novo KD reported:
  - Round 1: 5 binders from 201 designs (2.5%); the best was a BindCraft helical design at 491 nM [summ]. Round 2: 53 binders from 378 expressed designs (about 14% overall) [summ]. The best de novo binder was a BindCraft β-sheet miniprotein at 82 nM [summ; matches the raw data] — https://www.biorxiv.org/content/10.1101/2025.04.17.648362v2
  - After excluding EGF/TGFα-like and antibody-like designs, about 12 of 206 designs bound (about 6%), on my sequence heuristic [computed] — https://github.com/adaptyvbio/egfr_competition_2
  - The tighter short "binders" (52–55 nM) are EGF-like. The 1.21 nM Cradle winner is a cetuximab-CDR scFv, not de novo.
  - The assay was BLI against the EGFR ectodomain at one condition, HBS-T, pH not stated in what I read (README above).
- Which metrics separated binders from non-binders:
  - I reproduced the preprint's AUCs on 378 designs. ipTM: 0.64. pLDDT: 0.66. The pAE_interaction AUC is 0.61 [computed] — https://github.com/adaptyvbio/egfr_competition_2
  - On the strict de novo subset, ipTM is 0.67 (95% CI 0.51–0.81), pAE_interaction 0.61 (0.46–0.75), and pLDDT 0.65 [computed]. All are weak, with wide CIs, since only 12 binders.
  - Among binders, ipTM correlates with KD in the wrong direction (Spearman +0.15 to +0.28, not significant) [computed]. The preprint says the same. So ipTM is a weak filter and a poor ranker.
  - The preprint reports ESM2 log-likelihood as the top metric. I could not reproduce that with the raw sum (AUC 0.55); the Adaptyv blog quotes a normalised 0.72 [summ] (blog link above).
  - Expression predictors: Glu 0.77 and Lys 0.73 (matches the preprint; mine are 0.74 and 0.71 overall), and low Aggrescan3D. They predict expression, not binding [computed].
  - ipSAE and shape complementarity were not analysed in the preprint or the public tables, so your ranking on them is untested — not found in literature.
- Notable prior EGFR de novo designs to learn from (as reference, not scaffold):
  - The Nickel/Pacesa BindCraft β-sheet binder (179 aa, 82 nM). Its epitope is not stated in what I read — not found in literature.
  - Two shorter BindCraft binders, begonia l88 (264 nM) and chuh Seg2 l58 (394 nM) [computed from the results table above].
  - Two BindCraft designs aimed at 6ARU domain III (deepsatflow) bound only weakly (3.5 µM and ≥10 µM). That suggests hotspot choice matters [computed].
  - Cao 2022 designed binders to the native ligand sites on domain I (EGFRn_mb, optimised to about 20 nM) and domain III (EGFRc_mb) — https://www.nature.com/articles/s41586-022-04654-9
  - A competitor design note (composite GB1–minibinder constructs, 6ARU domain III hotspots A348, A350, A382, A412, A417, A438; no binding data) — https://github.com/ccalia/EGFR_Binders_Adaptyv_Round2
  - Epitope of the successful de novo binders: not found in literature. Adaptyv's blog says domain III was the most-targeted region (46–62%) and quotes an organiser-advised epitope "11-13, 15-18, 356, 440-441" with numbering unstated [summ] (blog link above). The neutralisation zip, which would localise epitopes, was on a host my sandbox could not reach.
  - Proteinbase: I read only the competition page, which had no metrics or epitope data — https://proteinbase.com/competitions/adaptyv-egfr-binder2. Per-design pages were not mined.
  - This is the 2024 competition, which may differ from Track 3.

SOURCES (full annotated list)
1. RCSB PDB 1YY9, cetuximab Fab:sEGFR (Li 2005) https://www.rcsb.org/structure/1YY9 — cetuximab contacts (list read secondhand).
2. RCSB PDB 6ARU, cetuximab Fab variant with wild-type EGFR https://www.rcsb.org/structure/6ARU — reference structure and the sequence used for identity and numbering checks.
3. RCSB PDB 5SX4 and 5SX5, panitumumab:domain III (Sickmier 2016) https://www.rcsb.org/structure/5SX4 ; https://www.rcsb.org/structure/5SX5 — panitumumab contacts and the S492R resistance structure (paper itself not read).
4. US 9,540,450 https://patents.google.com/patent/US9540450B2/en — secondhand source for the Li 2005 residue list.
5. UniProt P00533 (human EGFR) and Q01279 (mouse EGFR) https://www.uniprot.org/uniprotkb/P00533 ; https://www.uniprot.org/uniprotkb/Q01279 — sequences behind my alignment and mouse-conservation calls [computed].
6. Liu et al. 2022, cross-reactive pH-dependent EGFR antibody G532, Mol Ther Oncolytics https://www.sciencedirect.com/science/article/pii/S237277052200136X — acid-preferring EGFR precedent, H370/H433, 13.26 vs 3.31 (summarizer only).
7. WO2024109709A1 https://patents.google.com/patent/WO2024109709A1/en — patent for the same antibody, about 13-fold (secondary).
8. Ahn … Baker 2025 preprint, computational design of pH-sensitive binders https://www.biorxiv.org/content/10.1101/2025.09.29.678932v1.full — His–cation and buried-network mechanisms; release-type only.
9. Martin 2001, FcRn/Fc structure https://pubmed.ncbi.nlm.nih.gov/11336709/ — FcRn salt-bridge precedent (abstract only).
10. Ying 2014, Front Immunol https://www.frontiersin.org/journals/immunology/articles/10.3389/fimmu.2014.00146/full — His–carboxylate distances (summarizer; residue numbering inconsistent).
11. Sulea 2020, mAbs (HER2) https://pmc.ncbi.nlm.nih.gov/articles/PMC6927761 — acid-preferring HER2, narrow-window cell ratios (summarizer).
12. La Sala 2026, mAbs (anti-CD3) https://www.dora.lib4ri.ch/psi/dload/psi:86933/PDF/La_Sala-2026-Engineering_of_acidic_pH-responsive_anti-CD3-(published_version).pdf — Asp/Glu acid-preferring example without His (summarizer).
13. Acid-Fc, JBC 2022 https://pubmed.ncbi.nlm.nih.gov/35248534/ — narrow-window ratio: about 2x binding vs about 20x ADCC (abstract only).
14. Chaparro-Riggers 2012, JBC https://pmc.ncbi.nlm.nih.gov/articles/PMC3322827 — pH-sensitive anti-PCSK9; corrects the "Strop 2012" citation.
15. Sarkar 2002 https://www.nature.com/articles/nbt725 and Igawa 2010 https://www.nature.com/articles/nbt.1691 — foundational histidine-switching and recycling papers (abstracts only).
16. preLights https://prelights.biologists.com/highlights/computational-design-of-ph-sensitive-binders/ — conflicting distances noted as unreliable.
17. Crowdsourced Protein Design: Lessons From the Adaptyv EGFR Binder Competition, bioRxiv 2025.04.17.648362 https://www.biorxiv.org/content/10.1101/2025.04.17.648362v2 — hit rates, best KD, metric AUCs (summarizer only; title and abstract not returned).
18. adaptyvbio/egfr_competition_2 (raw data) https://github.com/adaptyvbio/egfr_competition_2 — source for all [computed] precedent numbers.
19. Adaptyv blogs https://www.adaptyvbio.com/blog/po102/ and https://www.adaptyvbio.com/blog/po104/ — 91.5 nM, 6/65, the domain III share, the organiser-advised epitope (summarizer).
20. Proteinbase https://proteinbase.com/competitions/adaptyv-egfr-binder2 — competition page only, no per-design data.
21. Cao et al. 2022, Nature https://www.nature.com/articles/s41586-022-04654-9 — earlier EGFR domain I and III binders (about 20 nM domain I).
22. ccalia Round 2 notes https://github.com/ccalia/EGFR_Binders_Adaptyv_Round2 — a competitor's design method and hotspots (no binding data).

===== END =====
```

## Addendum (2026-09-28, after review; resolves the three follow-up items)

1. **Liu 2022 numbering: precursor / UniProt.** Liu's H433 is our precursor H433 (mature H409), inside the contact patch. It is not H457 (precursor 457 is S). Evidence: the paper gives the ECR as Leu25–Ser645 and domain III as "Lys335–Lys538" (both terminal residues are lysines in precursor P00533); the patent WO2024109709A1 lists "H370, H433, R377, L406, Q435, K489" and P00533 has exactly H, H, R, L, Q, K at those precursor positions (four of these six are in the measured 24). Under mature numbering, mature 370 is I and mature 433 is S. Correction to the wording above: the engineered change is LCDR1 **Y32→E/D/H** (Kabat), not a native E32; the non-pH control is LCDR1 K31N; G5V2 LCDR2 D52/D53 face H370. Read through two summarizers that agree with each other and with the sequence; no figure legend was seen. https://www.sciencedirect.com/science/article/pii/S237277052200136X ; https://patents.google.com/patent/WO2024109709A1/en
2. **Domain III identity is 87.3%, not 92%.** Identical residues, human vs mouse: 178/204 (K335–K538), 179/205 (334–538), 156/181 (358–538) = 86.2%. BLOSUM62-positive similarity is 93.1% (335–538) and 92.3% (358–538), so the brief's 92% may be a similarity figure (a guess). Whole ECD (25–645) is 87.8%; first 660 residues 85.5% [computed, P00533 vs Q01279].
3. **Adaptyv's advised epitope "11-13, 15-18, 356, 440-441" is almost certainly mature numbering** (precursor 11–18 is signal peptide). In precursor numbering it is 35–37, 39–42 (domain I), 380 and 464–465 (domain III; S464 and G465 are in the measured 24 and are resistance sites). The blog states it is "at the interaction between Domains I and III of EGFR"; no numbering convention or PDB ID is given (likely 1IVO-style, an inference). https://www.adaptyvbio.com/blog/po104/
