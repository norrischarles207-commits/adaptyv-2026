# pH strategy notes (literature pass, Prompts 4–5)

**Residue numbers are precursor / UniProt P00533 numbering.** Labels: **[summ]** read through a page summarizer, **[computed]** our own calculation. Every number in the review body below passed through a summarizer unless it says otherwise and needs spot-checking against the primary source before anyone relies on it.

## Bottom line (updated after the numbering check in `epitope-verification.md`)

- **Best-supported mechanism for acid-preferring (bind harder at pH 6.5) binding:** a protonated histidine paired with a carboxylate. Two directions have precedent:
  - *Antigen His, binder Asp/Glu.* EGFR antibody G532 was engineered this way against EGFR domain III histidines **H433 and H370** (precursor numbering, confirmed) — Liu et al. 2022 [summ] https://www.sciencedirect.com/science/article/pii/S237277052200136X ; patent https://patents.google.com/patent/WO2024109709A1/en
  - *Binder His, target Asp/Glu.* The FcRn–Fc benchmark (Fc histidines pair with FcRn Glu/Asp) — Martin 2001 https://pubmed.ncbi.nlm.nih.gov/11336709/ ; Ying 2014 https://www.frontiersin.org/journals/immunology/articles/10.3389/fimmu.2014.00146/full
  - The working brief's E496 anchor uses the second direction. The literature does not compare the two on EGFR.
- **The Baker 2025 preprint (bioRxiv 2025.09.29.678932) describes His-to-cation (Arg/Lys/His) repulsion and buried His networks, not His-to-acid geometry. All its designs weaken at low pH.** Its 3.7 / 7.6 / 4.9 Å values are protonated-His to cationic-residue distances in one EphA2 release design [summ]. They are not a His-to-carboxylate design window. https://www.biorxiv.org/content/10.1101/2025.09.29.678932v1.full
- **Realistic selectivity at pH 6.5 vs 7.4:** about 2–10x monovalent. A single His with pKa 6.0–6.4 caps at about 5–6x by Henderson–Hasselbalch (our arithmetic). The best EGFR precedent is G532: KD(7.4)/KD(6.5) of **13.26 on human EGFR and 3.31 on mouse EGFR**, as a bivalent IgG [summ]. No paper found reports a monovalent KD ratio above about 10 at 6.5 vs 7.4. Larger narrow-window ratios come from cell or functional assays.
- **Tension between objectives 2 and 3:** the one EGFR precedent lost most of its selectivity on mouse EGFR (13.26 vs 3.31), even though H370 and H433 are mouse-conserved. The cause is unknown.
- **No de novo or computationally designed acid-preferring binder was found in the literature** (search not exhaustive, about ten queries, several databases blocked).
- **Not tested anywhere we could find:** scoring designs on ΔΔG_elec between pH 7 and pH 6, in either sign. The preprint used a release-direction electrostatic filter (ddG elec ≥ 0 at low pH); inverting the sign for our direction is a reasonable inference, not a validated method.

## Full literature review

The literature on pH-dependent protein-protein binding rests on three named mechanisms: histidine-carboxylate salt bridges (the FcRn benchmark), desolvation of a His buried at an interface, and His-driven electrostatic repulsion. Only the first two are supported by sources retrieved here. Most published engineering has aimed at weaker binding at acidic pH (recycling, lysosomal release), but a smaller set of acid-preferring binders exists: HER2, CTLA-4, VISTA, CD3, AXL, ROR2 and, for EGFR, antibody G532. The single EGFR-specific finding is Liu et al. 2022, with a pH 7.4/pH 6.5 KD ratio of **13.26** on human EGFR and **3.31** on mouse EGFR. No de novo or computationally designed acid-preferring binder was found, although the search was not exhaustive. Reported selectivity depends heavily on the pH pair and the assay. Wide-window (pH 5.4 to 6.0 vs 7.4) ratios run from about 2x to about 1000x. Narrow-window (pH 6.5 to 6.8 vs 7.3 to 7.4) ratios are mostly about 2 to 20x, and the larger ones come from avidity-containing cell or functional assays. The Baker-lab preprint (bioRxiv 2025.09.29.678932) does not describe histidine-to-acidic-residue geometry. It describes His next to Arg/Lys/His, and all of its designs weaken at low pH. Nearly every number below passed through a page-summarizing fetch tool and needs re-checking against the source (see next section).

## How much to trust this

Primary pages were largely blocked (PMC, PubMed, Europe PMC, Wiley, Taylor & Francis, PNAS and Cell returned 403 or CAPTCHA responses). Content came through WebFetch, which returns a model-generated summary rather than raw text. No number here was checked against a downloaded PDF. The labels used throughout are as follows.

| Label | Meaning |
|---|---|
| **FT-summ** | Full-text page fetched, read via summarizer. Numbers are probably right but unchecked against the original tables. |
| **ABS** | Abstract only. No body text seen. |
| **Secondary** | Number comes from a review or patent, not the primary paper. |
| **Snippet / unverified** | Search-result title only, or from background knowledge. Not asserted as a finding. |

Volume and page numbers marked "from memory" in the notes are not verified and are omitted here where possible. Specific items that need a source check before anyone relies on them: every Å distance (Ying 2014 and the preprint), the Sulea HER2 KD values (three different pH pairs appear across sources), the Chang 2021 CTLA-4 EC50 statement, all BA3011 and BA3021 figures, the patent CAPBP values, and the preprint fold-changes (whether "1000-fold" is a measured value or a bound is unknown).

## Premise mismatches to reconcile before use

Five items in the request do not match what the sources show.

**(a) The preprint reports His-to-cation geometry, not His-to-acid.** The Ahn ... Baker preprint, "Computational design of pH-sensitive binders," describes two principles: histidines placed adjacent to positively charged residues at the interface so that protonation causes electrostatic repulsion, and buried His-containing charged hydrogen-bond networks in the binder core that destabilize the protein at acid pH ([bioRxiv record](https://api.biorxiv.org/details/biorxiv/10.1101/2025.09.29.678932)). All designs dissociate at low pH. Asp/Glu appears only in the Introduction as the natural FcRn example, with no distances ([bioRxiv PDF](https://www.biorxiv.org/content/10.1101/2025.09.29.678932v1.full.pdf), FT-summ).

**(b) "Sarkar et al. 2019 anti-CD20" was not found.** A targeted search returned only generic anti-CD20 literature. The likely intended paper is Sarkar et al. 2002 on G-CSF "histidine switching" ([Nature](https://www.nature.com/articles/nbt725), ABS). A negative search is not proof of non-existence.

**(c) Igawa 2010 acidic pH.** The fetched abstract page gives the endosomal pH as **6.0**, not 5.8 ([Nature](https://www.nature.com/articles/nbt.1691), ABS). Check against the paper.

**(d) "Strop 2012 J Mol Biol" was not found.** Searches returned Chaparro-Riggers et al. 2012 in J Biol Chem, which is the pH-sensitive anti-PCSK9 paper ([PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC3322827), FT-summ). Do not cite it as Strop.

**(e) Two preLights-only claims are unreliable.** preLights gives His-to-Arg distances of 5.7 and 7.8 Å, and a "10^8-fold reduction at pH 6.4" for a target labeled "ILVBP" ([preLights](https://prelights.biologists.com/highlights/computational-design-of-ph-sensitive-binders/)). Neither appeared in the preprint text retrieved, and they are not presented here as findings.

## 1. Mechanisms: salt bridges, desolvation and repulsion

**Histidine-carboxylate interactions.** The canonical case is IgG-FcRn. The 2.8 Å FcRn/Fc structure reports conformational changes in Fc and "three titratable salt bridges that confer pH-dependent binding" ([Martin et al. 2001, Mol Cell](https://pubmed.ncbi.nlm.nih.gov/11336709/), ABS). A review-level source lists candidate pairs: His310 (CH2) with FcRn Glu, and His433 (CH3) with Asp126 ([Ying et al. 2014, Front Immunol](https://www.frontiersin.org/journals/immunology/articles/10.3389/fimmu.2014.00146/full), FT-summ). Its listed distances are GLU111 OE2-HIS310 ND1 2.77 Å and 2.70 Å (two complexes), GLU111 OE2-HIS310 N 2.85 Å, and ASP126 OD1-HIS433 ND1 2.91 Å. The fetched text has a Glu111/Glu112 numbering inconsistency, so these values need checking. In engineered antibodies, the anti-PCSK9 antibody J17 carries S30H, S50H and S52H; modeling suggests His30 pairs with PCSK9 Asp374 ([Chaparro-Riggers et al. 2012, JBC](https://pmc.ncbi.nlm.nih.gov/articles/PMC3322827), FT-summ). The reported effect is 3.8-, 2.6- and 9.2-fold weaker binding at pH 6 vs 7.4 for mouse, cynomolgus and human PCSK9, mostly through the off-rate. No distance was reported. A stepwise His-plus-acidic-residue mutagenesis paper exists ([3 Biotech 2021](https://doi.org/10.1007/s13205-021-03079-x)), but only its title was seen (snippet).

**Buried histidine and desolvation.** Strauch, Fleishman and Baker designed a pH-sensitive IgG-binding protein around Fc His433, which "forms a buried hydrogen bond to Ser-134 of FcB6.1 and is shielded from solvent by R135 and V138." Protonation raises the desolvation cost of the charged residue, removes the H-bond and adds repulsion with Arg135; measured Kd was 4.0 ± 2.5 nM at pH 8.2 vs 3.78 ± 3.2 µM at the lower pH, about 500-fold ([Strauch et al. 2014, PNAS](https://www.bakerlab.org/wp-content/uploads/2015/12/Strauch-1313605111_PNAS_13W.pdf), FT-summ). The summarizer also returned "A135 and E138" as beneficial mutations, which conflicts with the R135/V138 wording, so residue-level details are unconfirmed. This is a His-Ser hydrogen bond, not a His-acid one. Sulea et al. state that surface His pKa is about 6.4 and that the design principle is placing "a positively charged and highly solvated His residue...into [a] desolvated environment"; they also excluded His mutants with no direct antigen contacts ([Sulea et al. 2020, mAbs](https://pmc.ncbi.nlm.nih.gov/articles/PMC6927761/), FT-summ). The link between burial and His pKa variability is the subject of Edgcomb and Murphy 2002 ([Proteins](https://onlinelibrary.wiley.com/doi/10.1002/prot.10177)), and measured pKa compilations exist ([Grimsley et al. 2009](https://onlinelibrary.wiley.com/doi/abs/10.1002/pro.19)); both were located by title only (snippet), so no pKa-shift numbers can be given.

**Electrostatic repulsion and protonation-coupled change.** The 2025 preprint's interface mechanism is His placed near Arg/Lys/His so that the protonated imidazole repels the target cation. Its buried-network mechanism destabilizes the binder itself at low pH ([bioRxiv](https://www.biorxiv.org/content/10.1101/2025.09.29.678932v1.full), FT-summ). Martin 2001 adds protonation-coupled conformational change in Fc. For an acid-preferring CD3 antibody, La Sala et al. report pH sensitivity that does not rely on histidine: two Asp/Glu mutations distant from the antigen peptide were proposed, from molecular dynamics, to act through CDR-L1/L3 rigidification and VH-VL reorientation at pH 6.0 ([La Sala et al. 2026, mAbs](https://www.dora.lib4ri.ch/psi/dload/psi:86933/PDF/La_Sala-2026-Engineering_of_acidic_pH-responsive_anti-CD3-(published_version).pdf), FT-summ). These are simulation-based proposals.

**Foundational engineering papers.** Sarkar 2002 used computationally predicted His substitutions in G-CSF, giving an order-of-magnitude increase in medium half-life and enhanced potency ([Nature](https://www.nature.com/articles/nbt725), ABS). Igawa 2010 engineered tocilizumab variants to dissociate from IL-6R at endosomal pH while retaining plasma-pH affinity ([Nature](https://www.nature.com/articles/nbt.1691), ABS). Combinatorial His-scanning libraries appear in Murtaugh et al. 2011 ([Protein Sci](https://onlinelibrary.wiley.com/doi/10.1002/pro.696)) and Schröter et al. 2015 ([mAbs](https://www.tandfonline.com/doi/full/10.4161/19420862.2014.985993)). Both were located by title only (snippet), and no mechanism or number was read for either. Sulea et al. 2023 (large-scale computation of low-pH-favoring mutations) and Wei and Sulea 2024 (the SIpHAB sequence-based tool, trained on 3,490 structures) exist but were not read beyond abstract level ([Proteins](https://onlinelibrary.wiley.com/doi/10.1002/prot.26340); [DOAJ](https://doaj.org/article/bd1f5d5978474d8ab00891f2829d0515)).

**Not supported by retrieved sources.** No source was retrieved for cation-pi, His-aromatic, His-backbone or long-range net-charge electrostatics as named mechanisms. The interface His pKa shifts themselves were not quantified in any retrieved text.

## 2. Directionality: acid-preferring binders are rarer and mostly antibodies

The natural benchmark for acid-preferring binding is IgG-FcRn, which binds near pH 6.0 and negligibly at 7.4; no KD table was retrieved ([Vaccaro et al. 2005](https://www.nature.com/articles/nbt1143), ABS, whose Fc variants show "reduced pH dependence"). The engineered examples are in the table. Metrics differ (SPR KD, cell EC50, ELISA EC50), so ratios are not comparable across rows.

| Paper | Target | pH pair | Metric and value | Verification | Link |
|---|---|---|---|---|---|
| Sulea 2020 | HER2 (bH1 variants) | 5.6 vs 7.3 | KD 6.6 nM vs 290 nM, about 44x (arithmetic on review figures); active in spheroids at pH 6.4, not 7.4 | Secondary (review) | [J Biomed Sci review](https://link.springer.com/article/10.1186/s12929-021-00709-7) |
| Chang 2021 (BioAtla) | CTLA-4, clone 87CAB3 | 6.0 vs 7.4 | EC50 at pH 7.4 "reduced to 0.5% of" pH 6.0; direction of phrase ambiguous | Secondary (review) | [PNAS](https://www.pnas.org/doi/10.1073/pnas.2020606118); [MDPI review](https://www.mdpi.com/2073-4468/12/3/55) |
| SNS-101 (Sensei/Adimab) | VISTA | 6.0 vs 7.4 | KD 0.218 nM vs 132 nM, ">600-fold" | Secondary (review) | [MDPI review](https://www.mdpi.com/2073-4468/12/3/55) |
| VISTA.18 (BMS) | VISTA (His-rich epitope) | acidic vs neutral | Blood residence 717 h vs 7.6 h for parental; no KD ratio | Secondary (review) | [MDPI review](https://www.mdpi.com/2073-4468/12/3/55) |
| La Sala 2026 | CD3 | 6.0 vs 7.4 | SPR KD: Q90L(E) 101 vs 743 nM (7.4x); I93L(H) 53.5 vs 114 nM (2.1x); T89L(D) 177 nM vs no detectable binding; parental 29.8 vs 31.9 nM. Cell EC50 fold: 53x (T89L(D)), 789x (Q90L(E)) | FT-summ | [DORA PDF](https://www.dora.lib4ri.ch/psi/dload/psi:86933/PDF/La_Sala-2026-Engineering_of_acidic_pH-responsive_anti-CD3-(published_version).pdf) |
| Chang 2025 (BA3011) | AXL | 6.0 vs 7.4 | SPR KD 62 pM vs 218 pM (about 3.5x); ELISA EC50 4.78 ng/mL at 6.0, none meaningful at 7.4 | PDF-summ | [BioAtla PDF](https://www.bioatla.com/wp-content/uploads/2025/04/Chang-2025-Preclinical-development-of-mecbotam.pdf) |
| Chang 2025 (BA3021) | ROR2 | 6.0 vs 7.4 | Affinity about 5.7x lower at 7.4; ELISA EC50 56.3 ng/mL at 6.0, none meaningful at 7.4 | PDF-summ | [BioAtla PDF](https://www.bioatla.com/wp-content/uploads/2025/04/Preclinical-development-of-ozuriftamab-vedotin-BA3021-a-novel-ROR2-specific-conditionally-active-biologic-antibody-drug-conjugate.pdf) |
| Lee 2022 | CTLA-4 (Ipi.105/106) | acidic-selective | Five acidic-residue substitutions plus CDR histidines; no KD obtained | Unverified (blocked) | [mAbs](https://www.tandfonline.com/doi/full/10.1080/19420862.2021.2024642) |

CAB-CAR-T anti-AXL and anti-ROR2 scFvs with higher affinity at pH 6.7 than 7.4 are mentioned only in a review, with no numbers ([J Biomed Sci review](https://link.springer.com/article/10.1186/s12929-021-00709-7), secondary).

The recycling-direction comparison set (weaker at acid pH) is larger. Examples include a Fab-level anti-PCSK9 antibody with a KD shift of "as high as ~33" and an anti-CTGF antibody at about 5 ([PMC5627591](https://pmc.ncbi.nlm.nih.gov/articles/PMC5627591/), FT-summ, author names not confirmed), and a CEACAM5 arm with off-rate gains of 15x, 25x and 52x at pH 6.0, 5.5 and 5.0 ([Front Immunol 2019](https://www.frontiersin.org/journals/immunology/articles/10.3389/fimmu.2019.01892/full), FT-summ; the summarizer was unclear whether these are relative to wild type or to pH 7.4). The MST-HN Fc variants are pH-independent, not acid-preferring, so they are a contrast case only ([Vaccaro 2005](https://www.nature.com/articles/nbt1143), ABS).

On rarity, La Sala et al. state that pH-engineering "frequently results in affinity loss" and requires "a tremendous engineering effort," and that the ten-fold proton-concentration difference across the window limits dynamic range ([DORA PDF](https://www.dora.lib4ri.ch/psi/dload/psi:86933/PDF/La_Sala-2026-Engineering_of_acidic_pH-responsive_anti-CD3-(published_version).pdf), FT-summ). No source quantified how often acid-gain designs succeed relative to acid-release designs. Note that the La Sala variants lose absolute affinity at pH 6.0 relative to the parent (101 to 304 nM vs 29.8 nM). Searches for de novo or computational acid-preferring binders, nanobodies and peptides were not run in this pass, so their absence is unconfirmed.

## 3. Placement geometry: sparse numbers, mostly qualitative

**What the antibody and Fc literature gives.** Explicit imidazole-to-carboxylate distances appear only in the Fc-FcRn structural summary above (2.70 to 2.91 Å; [Ying et al. 2014](https://www.frontiersin.org/journals/immunology/articles/10.3389/fimmu.2014.00146/full), FT-summ). That range is consistent with direct N-to-O hydrogen-bond or salt-bridge distances, but this is a reading of the numbers, not a rule stated by the authors. Sulea et al. give a design filter (acidic-pH loss of no more than 2.7 kcal/mol relative to parent) and a requirement for direct antigen contact, and note that for heavy-chain R58H a favorable interaction with antigen E558 might persist at acidic pH; they reported no Å distances and no burial or SASA quantification ([PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC6927761/), FT-summ). Strauch describes burial qualitatively (His433 more surface-exposed than His310; shielded by neighbors), with computed-energy (< -10) and shape-complementarity (> 0.63) filters ([Baker lab PDF](https://www.bakerlab.org/wp-content/uploads/2015/12/Strauch-1313605111_PNAS_13W.pdf), FT-summ). No retrieved paper states a design rule for number of acid contacts per His, imidazole-carboxylate cutoffs, burial depth or SASA thresholds.

**Key geometric findings of bioRxiv 2025.09.29.678932.** All values below are His-to-cation, all from the full-text summary ([bioRxiv](https://www.biorxiv.org/content/10.1101/2025.09.29.678932v1.full), FT-summ), and need checking against the PDF.

| Item | Reported value or rule | Verification |
|---|---|---|
| EphA2_pH_1 interface repulsion | His15, His19, His22 near target Arg at **3.7, 7.6 and 4.9 Å** (imidazole ε2 N to guanidinium terminal N) | FT-summ |
| Contact criterion | All pH-dependent binders had **two or more** protonated-His to cationic (His/Lys/Arg) contacts; up to **11** in the EphA2 binder, up to **8** in the TNFR2 binder | FT-summ |
| Interface selection filter | Predicted increase in repulsion at low pH (ddG elec ≥ 0) and at least one His accepting an H-bond from a positively charged residue | FT-summ |
| Buried-network filter | Primary His-His/Arg/Lys H-bond energy below **-0.5 kcal/mol**; AF2 pae_interaction and interface RMSD similar to or better than the parent complex | FT-summ |
| Sequence redesign shell | Residues within **5, 5.5 or 6 Å** of buried His | FT-summ (Methods) |
| Burial measure | Depth of the H-bond below the molecular surface via Rosetta AtomicDepth; **no numeric threshold** and no SASA values returned | FT-summ (Methods) |
| Low-pH modeling | Rosetta pH mode, pH value 0 vs 7, His repacked | FT-summ (Methods) |

The 3.7, 7.6 and 4.9 Å values conflict with the preLights figures (5.7 and 7.8 Å) noted above; the resolution is unknown without the raw PDF, and the paper does not state a target distance window. Supplementary figures (for example Fig. S6) were not accessed.

## 4. Narrow-window ratios are smaller and assay-dependent

A single isolated His caps the protonation contrast within a narrow window. By Henderson-Hasselbalch (the review author's own calculation, not from a paper), a His with pKa 6.4 is 44% protonated at pH 6.5 and 9% at 7.4, a maximum contrast of about 4.9x; pKa 6.0 gives about 6.3x. Across pH 5.8 vs 7.4 the same calculation gives about 8.8x (pKa 6.4) to 16x (pKa 6.0). Reported binding ratios need not track protonation ratios, because avidity, cooperativity and shifted local pKa can raise them. Sources make the qualitative point: surface His pKa about 6.4 with tumor pH 6.0 to 6.8 ([Sulea 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC6927761), FT-summ); a therapeutic window of about pH 5.9 vs 7.4 that "complicates engineering" ([J Biomed Sci review](https://link.springer.com/article/10.1186/s12929-021-00709-7), secondary); and His as "the only residue with a sidechain pKa near neutral pH" ([bioRxiv](https://www.biorxiv.org/content/10.1101/2025.09.29.678932v1.full), FT-summ). No retrieved paper performs an explicit narrow-window protonation analysis.

| Paper | Target, format | pH pair | Metric | Value | Verification | Link |
|---|---|---|---|---|---|---|
| Sulea 2020, bH1-P5P8 IgG | HER2, SKOV3 cells | 6.8 vs 7.3 | Cell-binding KD | About 21.7 nM vs about 290 nM; text ">10-fold" | FT-summ; approximate (Bmax not reached) | [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC6927761) |
| Sulea 2020, bH1-P5P8 Fab | HER2, recombinant | 5.0 vs 7.4 | SPR KD | 50 ± 20 nM vs 290 ± 50 nM, about 6x (P5 Fab about 3x); parental bH1 3 vs 13 nM, about 4x in the wrong direction | FT-summ | [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC6927761) |
| Acid-Fc paper (JBC 2022) | Human IgG1 Fc, FcγRIIIa | 6.5 vs 7.4 | Kd ratio; ADCC EC50 ratio | About 2x; ADCC about 20x | ABS | [PubMed](https://pubmed.ncbi.nlm.nih.gov/35248534/) |
| Chang 2025 (BA3011) | AXL, CAB-ADC | 6.0 vs 7.4 (inflection at 6.6) | SPR KD; ELISA EC50 | About 3.5x; ELISA no meaningful EC50 at 7.4 | FT-summ | [OUP](https://academic.oup.com/abt/article/8/2/145/8110027) |
| WO2020214748A1 (patent) | CTLA-4, ipilimumab variants | 5.5 to 6.8 vs 7.0 to 7.5 | CAPBP (normalized) | ipi.25 6.3; ipi.57 5.5; ipi.64 27.2 | Patent summary; pH pairs per variant not reported | [Google Patents](https://patents.google.com/patent/WO2020214748A1/en) |
| Ahn ... Baker preprint | Neo2, buried network | 6.0 vs 7.4 (also 6.4) | Fold weaker | Greater than 2x at 6.0; two designs dissociated faster at 6.4; no value returned for 6.4 | FT-summ | [bioRxiv](https://www.biorxiv.org/content/10.1101/2025.09.29.678932v1.full) |
| Ahn ... Baker preprint | EphA2, TNFR2, TNFα, IL-6, PCSK9 | 5.4 vs 7.4 | Fold weaker | Up to 1000x; 122x; 79x; 6x; 3.5x | FT-summ; not per-design KDs | [bioRxiv PDF](https://www.biorxiv.org/content/10.1101/2025.09.29.678932v1.full.pdf) |
| Igawa 2010 | IL-6R, tocilizumab variants | 6.0 vs 7.4 | Dissociation vs pH | Numbers not retrieved | ABS | [Nature](https://www.nature.com/articles/nbt.1691) |
| PD-L1 mAbs (STTT 2020) | JS003 | 6.0, 5.5 vs 7.4 | koff ratio | 3.4x (6.0); 8.7x (5.5) | FT-summ | [Nature](https://www.nature.com/articles/s41392-020-00254-z) |
| Traxlmayr 2014 | HER2 Fcab, weaker at acid | 6.0 vs 7.4 | KD | P1 152 nM (7.4) vs 1201 nM (6.0), ratio 7.9 | FT-summ | [PMC4314675](https://pmc.ncbi.nlm.nih.gov/articles/PMC4314675/) |

Two patterns emerge. Within one paper, the wide-window ratio is larger: for Sulea the SPR ratio at 5.0 vs 7.4 is about 3 to 6x, the cell-binding ratio at 6.8 vs 7.3 is above 10x, and the review-quoted figure at 5.6 vs 7.3 is about 44x. Cell binding plateaus between pH 6.8 and 5.2 (KD roughly 10 to 22 nM against about 290 nM at 7.3), so by the review's arithmetic on approximate values most of the achievable selectivity is already present at 6.8. Second, the same molecule gives very different ratios by readout: about 3.5x by SPR against near-absent ELISA and flow binding at 7.4 for BA3011, and about 2x binding vs about 20x ADCC for acid-Fc. Narrow-window ratios above 10x therefore come from cell-based or functional assays that can amplify a modest monovalent difference. No retrieved paper reports monovalent KD at both pH 6.5 and 7.4 with a ratio above about 10, and no de novo paper was found with a numeric 6.5 vs 7.4 ratio. The preprint itself notes that pH 7.4 vs 5.4 or 5.5 is the most common comparison ([bioRxiv](https://www.biorxiv.org/content/10.1101/2025.09.29.678932v1.full), FT-summ). Its inconsistent counts (PCSK9 "7 of 40" vs "7/32") and the unclear meaning of "1000-fold" should be checked.

## 5. EGFR and other receptor tyrosine kinases

### EGFR: Liu et al. 2022, antibody G532 (Mol Ther Oncolytics)

Liu, Tian, Hao, Zhang, Wang, Wei, Wei, Li and Sui describe "a cross-reactive pH-dependent EGFR antibody with improved tumor selectivity and penetration obtained by structure-guided engineering" (DOI 10.1016/j.omto.2022.11.001; [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S237277052200136X), FT-summ; also [PubMed 36458200](https://pubmed.ncbi.nlm.nih.gov/36458200/), not readable). **Verification status: full-text page read only through a summarizer; absolute KD values at each pH, the number of mutations and the cetuximab head-to-head numbers were not obtained. All figures below need checking against the paper.**

| Attribute | Reported | 
|---|---|
| Format and lineage | Full-length IgG; parent 14C07 from phage display, then G5V2, then G532 |
| Engineering | Structure-guided, not His scanning. The patent summary describes identifying antigen (EGFR) histidines that contribute to binding and replacing interacting antibody residues with Asp/Glu; the paper summary mentions His-Asp/Glu interactions |
| Direction and pH pair | Acid-preferring: strong binding at pH 6.5, weak at 7.4 |
| Selectivity | KD ratio (pH 7.4 / pH 6.5) **13.26 human EGFR, 3.31 mouse EGFR**; non-pH-dependent control G532Ctrl 0.599 (human), 0.586 (mouse) |
| Epitope | EGFR domain III, histidines **H370 and H433** engaged; patent describes competition with EGF |
| In vivo | Better tumor penetration than the non-pH-dependent variant; about 9-fold lower human IgG signal in mouse liver; tumor/liver ratio above 1 for G532 and below 1 for controls; xenograft tumor growth inhibition comparable to cetuximab |

The related patent WO2024109709A1 (Huahui Health, published 30 May 2024) claims about 13-fold pH-dependent binding over G5V2, matching the paper's figure; this is secondary evidence ([Google Patents](https://patents.google.com/patent/WO2024109709A1/en)). Note that the 13.26 value is a narrow-window ratio (6.5 vs 7.4) and is 4x higher on human than on mouse EGFR.

### Other RTKs

Acid-preferring examples are AXL (BA3011, above) and ROR2 (BA3021, above), plus HER2 (Sulea 2020, secondary). Release-at-acid examples are c-Met and the HER2 Fcab. For c-Met, Gera et al. 2024 (MYTX-011, an antibody-drug conjugate) report cell-binding IC50 of 0.4 nM at pH 7.4 and 0.5 nM at pH 6.4, so no tumor-pH selectivity, with rapid dissociation at pH 5.4 for endolysosomal release ([Mol Cancer Ther](https://aacrjournals.org/mct/article/23/9/1282/747349/MYTX-011-A-pH-Dependent-Anti-c-MET-Antibody-Drug), FT-summ; DOI and author list not returned). The HER2 Fcab (Traxlmayr) is listed in Section 4. In the preprint, EphA2 is the only de novo RTK target; interface-His designs from about 12,000 screened yielded 4 pH-sensitive designs with up to 1000-fold weaker binding at pH 5.4, and a first histidine-biased approach showed little or no sensitivity ([bioRxiv](https://www.biorxiv.org/content/10.1101/2025.09.29.678932v1.full), FT-summ). Those designs are release-type, not acid-preferring.

### What was not found

No de novo, nanobody, peptide or EGF/TGF-α ligand-variant EGFR binder with pH selectivity was found, and no de novo acid-preferring RTK binder of any kind. The eLife 2019 pH-sensitive EGFR reporter is a tagging tool, not a binder ([eLife](https://elifesciences.org/articles/46135), snippet). No BioAtla CAB-EGFR data and no pH-selective binders for HER3, VEGFR, IGF-1R or FGFR were found. Whether EGFR is among the nine test systems in Wei and Sulea 2024 was not confirmed. A 2025 AXL phage-display paper ([Antibodies 2025](https://www.mdpi.com/2073-4468/14/4/83)) and the CAB-CAR-T anti-EGFR mention (review, no kinetics) were seen by title only. These are limits of search coverage (about ten queries, several databases blocked), not evidence of absence.

## Conclusion

Read together, the sources describe two largely separate literatures. Acid-release designs (recycling, LYTAC-type) carry the mechanistic detail: buried-His desolvation, His-cation repulsion, and computational filters. Acid-preferring designs cluster among antibodies aimed at tumor microenvironment, with the mechanistic rationale sometimes His-acid, sometimes Asp/Glu-based without His (La Sala 2026), and the most explicit EGFR case (G532) obtained by structure-guided Asp/Glu substitution against antigen histidines rather than by His scanning. The retrieved sources do not connect the preprint's His-cation geometry to the acid-preferring designs.

Two evidence gaps stand out. No retrieved paper states a numeric His-to-carboxylate design window, contact-count rule or burial threshold for engineered binders; the only such distances are FcRn structural contacts. And narrow-window selectivity is reported almost entirely through cell-based or functional readouts, so the monovalent affinity contrast at pH 6.5 vs 7.4 remains poorly documented outside G532 and acid-Fc. Everything numeric above should be spot-checked against the primary sources before use.

## Sources

- Sarkar 2002, Nat Biotechnol (G-CSF histidine switching): https://www.nature.com/articles/nbt725
- Igawa 2010, Nat Biotechnol (recycling antibodies): https://www.nature.com/articles/nbt.1691
- Chaparro-Riggers 2012, JBC (pH-sensitive anti-PCSK9): https://pmc.ncbi.nlm.nih.gov/articles/PMC3322827
- Martin 2001, Mol Cell (FcRn/Fc structure): https://pubmed.ncbi.nlm.nih.gov/11336709/
- Ying 2014, Front Immunol (Fc-FcRn interactions): https://www.frontiersin.org/journals/immunology/articles/10.3389/fimmu.2014.00146/full
- Strauch, Fleishman, Baker 2014, PNAS: https://www.bakerlab.org/wp-content/uploads/2015/12/Strauch-1313605111_PNAS_13W.pdf
- Sulea et al. 2020, mAbs (HER2): https://pmc.ncbi.nlm.nih.gov/articles/PMC6927761
- Sulea et al. 2023, Proteins: https://onlinelibrary.wiley.com/doi/10.1002/prot.26340
- Wei and Sulea 2024, mAbs (SIpHAB): https://doaj.org/article/bd1f5d5978474d8ab00891f2829d0515
- Murtaugh 2011, Protein Sci: https://onlinelibrary.wiley.com/doi/10.1002/pro.696
- Schröter 2015, mAbs: https://www.tandfonline.com/doi/full/10.4161/19420862.2014.985993
- Edgcomb and Murphy 2002, Proteins: https://onlinelibrary.wiley.com/doi/10.1002/prot.10177
- Grimsley, Scholtz, Pace 2009, Protein Sci: https://onlinelibrary.wiley.com/doi/abs/10.1002/pro.19
- Stepwise His plus acidic mutagenesis, 3 Biotech 2021: https://doi.org/10.1007/s13205-021-03079-x
- Ahn ... Baker 2025, bioRxiv preprint (record): https://api.biorxiv.org/details/biorxiv/10.1101/2025.09.29.678932
- Ahn ... Baker 2025, bioRxiv full text: https://www.biorxiv.org/content/10.1101/2025.09.29.678932v1.full
- Ahn ... Baker 2025, bioRxiv PDF: https://www.biorxiv.org/content/10.1101/2025.09.29.678932v1.full.pdf
- preLights summary (unreliable for distances and "ILVBP"): https://prelights.biologists.com/highlights/computational-design-of-ph-sensitive-binders/
- Chang 2021, PNAS (CTLA-4 CAB): https://www.pnas.org/doi/10.1073/pnas.2020606118
- Lee 2022, mAbs (acidic pH-selective anti-CTLA-4): https://www.tandfonline.com/doi/full/10.1080/19420862.2021.2024642
- La Sala 2026, mAbs (acidic pH anti-CD3): https://www.dora.lib4ri.ch/psi/dload/psi:86933/PDF/La_Sala-2026-Engineering_of_acidic_pH-responsive_anti-CD3-(published_version).pdf
- Chang 2025, Antibody Therapeutics (BA3011, AXL): https://www.bioatla.com/wp-content/uploads/2025/04/Chang-2025-Preclinical-development-of-mecbotam.pdf and https://academic.oup.com/abt/article/8/2/145/8110027
- Chang 2025, mAbs (BA3021, ROR2): https://www.bioatla.com/wp-content/uploads/2025/04/Preclinical-development-of-ozuriftamab-vedotin-BA3021-a-novel-ROR2-specific-conditionally-active-biologic-antibody-drug-conjugate.pdf
- Gera 2024, Mol Cancer Ther (MYTX-011, c-Met): https://aacrjournals.org/mct/article/23/9/1282/747349/MYTX-011-A-pH-Dependent-Anti-c-MET-Antibody-Drug
- Traxlmayr 2014, Biotechnol J (HER2 Fcab): https://pmc.ncbi.nlm.nih.gov/articles/PMC4314675/
- Liu et al. 2022, Mol Ther Oncolytics (EGFR G532): https://www.sciencedirect.com/science/article/pii/S237277052200136X and https://pubmed.ncbi.nlm.nih.gov/36458200/
- WO2024109709A1 (Huahui Health, EGFR): https://patents.google.com/patent/WO2024109709A1/en
- WO2020214748A1 (ipilimumab variants): https://patents.google.com/patent/WO2020214748A1/en
- Acid-Fc, JBC 2022: https://pubmed.ncbi.nlm.nih.gov/35248534/
- Vaccaro et al. 2005, Nat Biotechnol (MST-HN Fc): https://www.nature.com/articles/nbt1143
- PMC5627591 (pH-dependent anti-PCSK9/CTGF antibodies): https://pmc.ncbi.nlm.nih.gov/articles/PMC5627591/
- CEACAM5 x CEACAM6 bispecific, Front Immunol 2019: https://www.frontiersin.org/journals/immunology/articles/10.3389/fimmu.2019.01892/full
- PD-L1 mAbs, Signal Transduct Target Ther 2020: https://www.nature.com/articles/s41392-020-00254-z
- Review, J Biomed Sci 2021: https://link.springer.com/article/10.1186/s12929-021-00709-7
- Review, Antibodies 2023: https://www.mdpi.com/2073-4468/12/3/55
- eLife 2019, pH-sensitive EGFR reporter: https://elifesciences.org/articles/46135
