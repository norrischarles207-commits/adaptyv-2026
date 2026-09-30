# Sources — EGFR literature pass (annotated)

**Numbering:** every residue number in this directory is precursor / UniProt P00533 numbering unless labelled "mature".
**Verification labels:** *summarizer* = read through a page summarizer, not raw text; *abstract only* = no body text seen; *secondhand* = via a patent or review; *computed* = our own calculation. Most primary pages (PMC, PubMed, Cell, Europe PMC, RCSB via shell, SIFTS/PDBsum/PDBe) were blocked, so **no numeric claim in this pass was checked against a downloaded PDF**.

## A. Epitope, numbering, mouse conservation, Adaptyv precedent (items 1–22, from the hand-back)

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

Additional items from the follow-up checks:

23. Voigt et al., functional dissection of the cetuximab / panitumumab epitopes (as linked in `brief.md`) https://www.tandfonline.com/doi/pdf/10.4161/mabs.28915 — Voigt-only contacts (mature 349, 355, 412, 438 = precursor 373, 379, 436, 462); the publication year is unresolved (my notes say 2012, the brief says 2014) and the paper was not read directly.
24. Adaptyv, Protein Optimization 102 https://www.adaptyvbio.com/blog/po102/ — Round 1 hit rate (5/201), iPAE correlation with KD (Pearson −0.25), Round 1 residue examples "18, 39, 41, 108, 131" (summarizer).
25. Pacesa et al. 2025, BindCraft, Nature https://www.nature.com/articles/s41586-025-09429-6 — method behind the Round 1 and Round 2 de novo winners; whether it reports EGFR was not verified.

## B. pH-dependent binding (from the pH review; see `ph-strategy-notes.md` for how each was used and its verification label)

1. Sarkar 2002, Nat Biotechnol (G-CSF histidine switching): https://www.nature.com/articles/nbt725
2. Igawa 2010, Nat Biotechnol (recycling antibodies): https://www.nature.com/articles/nbt.1691
3. Chaparro-Riggers 2012, JBC (pH-sensitive anti-PCSK9): https://pmc.ncbi.nlm.nih.gov/articles/PMC3322827
4. Martin 2001, Mol Cell (FcRn/Fc structure): https://pubmed.ncbi.nlm.nih.gov/11336709/
5. Ying 2014, Front Immunol (Fc-FcRn interactions): https://www.frontiersin.org/journals/immunology/articles/10.3389/fimmu.2014.00146/full
6. Strauch, Fleishman, Baker 2014, PNAS: https://www.bakerlab.org/wp-content/uploads/2015/12/Strauch-1313605111_PNAS_13W.pdf
7. Sulea et al. 2020, mAbs (HER2): https://pmc.ncbi.nlm.nih.gov/articles/PMC6927761
8. Sulea et al. 2023, Proteins: https://onlinelibrary.wiley.com/doi/10.1002/prot.26340
9. Wei and Sulea 2024, mAbs (SIpHAB): https://doaj.org/article/bd1f5d5978474d8ab00891f2829d0515
10. Murtaugh 2011, Protein Sci: https://onlinelibrary.wiley.com/doi/10.1002/pro.696
11. Schröter 2015, mAbs: https://www.tandfonline.com/doi/full/10.4161/19420862.2014.985993
12. Edgcomb and Murphy 2002, Proteins: https://onlinelibrary.wiley.com/doi/10.1002/prot.10177
13. Grimsley, Scholtz, Pace 2009, Protein Sci: https://onlinelibrary.wiley.com/doi/abs/10.1002/pro.19
14. Stepwise His plus acidic mutagenesis, 3 Biotech 2021: https://doi.org/10.1007/s13205-021-03079-x
15. Ahn ... Baker 2025, bioRxiv preprint (record): https://api.biorxiv.org/details/biorxiv/10.1101/2025.09.29.678932
16. Ahn ... Baker 2025, bioRxiv full text: https://www.biorxiv.org/content/10.1101/2025.09.29.678932v1.full
17. Ahn ... Baker 2025, bioRxiv PDF: https://www.biorxiv.org/content/10.1101/2025.09.29.678932v1.full.pdf
18. preLights summary (unreliable for distances and "ILVBP"): https://prelights.biologists.com/highlights/computational-design-of-ph-sensitive-binders/
19. Chang 2021, PNAS (CTLA-4 CAB): https://www.pnas.org/doi/10.1073/pnas.2020606118
20. Lee 2022, mAbs (acidic pH-selective anti-CTLA-4): https://www.tandfonline.com/doi/full/10.1080/19420862.2021.2024642
21. La Sala 2026, mAbs (acidic pH anti-CD3): https://www.dora.lib4ri.ch/psi/dload/psi:86933/PDF/La_Sala-2026-Engineering_of_acidic_pH-responsive_anti-CD3-(published_version).pdf
22. Chang 2025, Antibody Therapeutics (BA3011, AXL): https://www.bioatla.com/wp-content/uploads/2025/04/Chang-2025-Preclinical-development-of-mecbotam.pdf and https://academic.oup.com/abt/article/8/2/145/8110027
23. Chang 2025, mAbs (BA3021, ROR2): https://www.bioatla.com/wp-content/uploads/2025/04/Preclinical-development-of-ozuriftamab-vedotin-BA3021-a-novel-ROR2-specific-conditionally-active-biologic-antibody-drug-conjugate.pdf
24. Gera 2024, Mol Cancer Ther (MYTX-011, c-Met): https://aacrjournals.org/mct/article/23/9/1282/747349/MYTX-011-A-pH-Dependent-Anti-c-MET-Antibody-Drug
25. Traxlmayr 2014, Biotechnol J (HER2 Fcab): https://pmc.ncbi.nlm.nih.gov/articles/PMC4314675/
26. Liu et al. 2022, Mol Ther Oncolytics (EGFR G532): https://www.sciencedirect.com/science/article/pii/S237277052200136X and https://pubmed.ncbi.nlm.nih.gov/36458200/
27. WO2024109709A1 (Huahui Health, EGFR): https://patents.google.com/patent/WO2024109709A1/en
28. WO2020214748A1 (ipilimumab variants): https://patents.google.com/patent/WO2020214748A1/en
29. Acid-Fc, JBC 2022: https://pubmed.ncbi.nlm.nih.gov/35248534/
30. Vaccaro et al. 2005, Nat Biotechnol (MST-HN Fc): https://www.nature.com/articles/nbt1143
31. PMC5627591 (pH-dependent anti-PCSK9/CTGF antibodies): https://pmc.ncbi.nlm.nih.gov/articles/PMC5627591/
32. CEACAM5 x CEACAM6 bispecific, Front Immunol 2019: https://www.frontiersin.org/journals/immunology/articles/10.3389/fimmu.2019.01892/full
33. PD-L1 mAbs, Signal Transduct Target Ther 2020: https://www.nature.com/articles/s41392-020-00254-z
34. Review, J Biomed Sci 2021: https://link.springer.com/article/10.1186/s12929-021-00709-7
35. Review, Antibodies 2023: https://www.mdpi.com/2073-4468/12/3/55
36. eLife 2019, pH-sensitive EGFR reporter: https://elifesciences.org/articles/46135
