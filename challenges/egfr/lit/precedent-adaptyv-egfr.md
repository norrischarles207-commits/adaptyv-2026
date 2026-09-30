# Adaptyv EGFR binder competition: what the data say (Round 2 raw data + preprint + blog)

Scope: the **2024 Adaptyv EGFR competition (Rounds 1–2)**, not the current Track 3. Numbers labelled **[COMPUTED]** were recomputed by me from the raw Round 2 data. Numbers labelled **[SUMMARY]** came from a WebFetch summary of a page and were not seen as raw text. Numbers labelled **[BLOG]** are Adaptyv's own statements, read through a summarizer.

## 0. Sources and verification status

| Source | Status |
|---|---|
| Raw Round 2 data, [adaptyvbio/egfr_competition_2](https://github.com/adaptyvbio/egfr_competition_2) (`result_summary.csv`, DE-STRESS tables, `replicate_summary.csv`) | Read directly. All **[COMPUTED]** numbers come from here. |
| Preprint, [Crowdsourced Protein Design: Lessons From the Adaptyv EGFR Binder Competition, bioRxiv 2025.04.17.648362](https://www.biorxiv.org/content/10.1101/2025.04.17.648362v2) | Summaries only. Title and abstract were never returned. |
| Adaptyv blogs [po102](https://www.adaptyvbio.com/blog/po102/) and [po104](https://www.adaptyvbio.com/blog/po104/) | Summaries only. The two fetches of po104 gave slightly different wording, so treat the domain III statistic as soft. |
| [Proteinbase competition page](https://proteinbase.com/competitions/adaptyv-egfr-binder2) | The page loaded but had no metrics or epitope data. Per-design Proteinbase pages were not mined. |
| Neutralisation zip and AF2 structure zips (api.adaptyvbio.com) | **Blocked** by the sandbox proxy (HTTP 403). I did not retry or work around it. Your teammate can download them; see section 6. |

My reproduction of the preprint's numbers: ipTM AUC 0.64, pLDDT 0.66, Glu composition 0.74–0.77, Lys composition 0.71–0.73, and 53 binders from 378 expressed designs all match. The raw data and the paper therefore agree.

## 1. Hit rate and best de novo KD

**Headline figures (paper, [SUMMARY]).**
- Round 1: 5 novel binders from 201 designs (2.5%); 146 (73%) expressed.
- Round 2: 53 binders from 378 expressed designs (about 14%); 378 of 400 expressed (95%).

**Why the headline hit rate does not describe de novo design.** A large share of the binders are natural-ligand (EGF or TGFα) variants or antibody-derived. I classified the 378 designs by sequence [COMPUTED]:

| Class (my heuristic) | Binders / designs |
|---|---|
| Antibody-like (scFv or nanobody, "WGQGT" motif) | 14 / 61 (23%) |
| EGF/TGFα-like (≥35% identity to EGF or TGFα, or a shared 6-mer with EGF) | 23 / 94 among designs ≤80 aa |
| Everything else, which I call **de novo-ish** | **12 / 206 (5.8%)** |

- The Adaptyv blog confirms the EGF-like effect. One TGFα-optimising participant had 8 of her submissions bind, an 80% hit rate.
- Adaptyv reports hallucination (BindCraft) at 6 of 65 designs (9%) [BLOG]. In the results file, entries labelled BindCraft gave 6 binders from 49 designs [COMPUTED]. The denominators differ, probably because of labelling, and I did not reconcile them.
- Caveat: my EGF-like filter is a sequence-identity heuristic, not the organisers' classification.

**Best de novo KD.**
- Round 2: **82 nM** for the BindCraft β-sheet miniprotein `lennart.nickel.EGFR_l179_s82283_mpnn1` (179 aa, ipTM 0.89) [COMPUTED]. The preprint says the same (82 nM). The blog says 91.5 nM, probably a different replicate summary.
- Round 1: 491 nM for the BindCraft helical design [SUMMARY].
- The tighter "de novo" hits below 82 nM are EGF-like sequences: Aurelia Bustos variants at 52–55 nM and 50 aa long, about 50% identical to EGF. **Do not treat them as de novo.**
- Nothing tighter than 82 nM was de novo by my classification.
- The non-de-novo winner, Cradle (1.21 nM), is a cetuximab-derived scFv with the CDRs preserved and framework mutations. It is not de novo. Cetuximab scFv control: 6.6 nM in the raw data, 9.94 nM in the paper.

**Every strict de novo binder [COMPUTED]:**

| Design | KD | Length | Method label |
|---|---|---|---|
| Nickel, l179 | 82 nM | 179 | BindCraft |
| Blakely, 12_6 / 12_3 / 16_2 | 217–322 nM | 228–236 | RFdiffusion+MPNN (unverified as de novo; a two-domain linked construct) |
| Begonia, l88 | 264 nM | 88 | BindCraft |
| Kurumida, mg_05 | 272 nM | 48 | RFdiffusion+MPNN |
| chuh, Seg2_l58 | 394 nM | 58 | BindCraft |
| deepsatflow, 6aru domain 3 l142 | 3.5 µM | 142 | BindCraft |
| gitter, yolo48 | ≥10 µM | 63 | BindCraft |
| deepsatflow, 6aru domain 3 l147 | ≥10 µM | 147 | BindCraft |
| cotimed_egf | 8.3 µM | 47 | TIMED, EGF-derived name, so questionable |
| colby | ≥10 µM | 250 | Fv-like EvoDiff, so questionable |

The large majority of designs across all methods did not bind.

## 2. Epitope

- **What the data show:** nothing directly. The public tables have no epitope column. The neutralisation assay (EGF competition) would say whether binders block the ligand site, but I could not download it.
- **What organisers advised.** Adaptyv's post says: "We advised you to select a specific EGFR epitope (residues 11-13, 15-18, 356, 440-441)" [BLOG]. This is the EGF-binding surface across domains I and III. The numbering convention is not stated, and residue 440 overlaps the cetuximab footprint (mature 440). This is **not** the cetuximab site as a whole.
- **Domain III share.** The blog says domain III accounted for 46–62% of binding sites, and that de novo binders preferred it at 62% [BLOG]. How epitopes were assigned is not stated. It is probably from predicted complexes, but that is my guess.
- **Domain-III-only attempts.** The two `deepsatflow.6aru_final_chain_A_domain_3` designs (BindCraft on 6ARU domain III) bound only weakly (3.5 µM and ≥10 µM). The one Round 2 method write-up I found targeted domain III residues 312–470 of 6ARU with hotspots A348, A350, A382, A412, A417 and A438 (a [GitHub](https://github.com/ccalia/EGFR_Binders_Adaptyv_Round2) design description, no binding data).
- **Winner epitope.** The winning β-sheet BindCraft binder's epitope is not stated in anything I could read.
- **Verdict.** I cannot say which surface the successful de novo binders used, and I would not claim it is the cetuximab site.

## 3. Which metrics separated binders from non-binders [COMPUTED]

AUC = probability that a random binder scores better than a random non-binder. Bootstrap 95% CIs are wide because there are only 12 strict de novo binders.

| Metric | All 378 | Strict de novo (12 / 206) | Note |
|---|---|---|---|
| ipTM (high = binder) | 0.64 (0.55–0.72) | 0.67 (0.51–0.81) | Preprint: 0.64 |
| pAE_interaction (low = binder) | 0.61 (0.53–0.70) | 0.61 (0.46–0.75) | |
| pLDDT | 0.66 (0.58–0.73) | 0.65 (0.51–0.78) | Preprint: 0.66 |
| ESM2 PLL (raw, unnormalised) | 0.55 | 0.36 | Preprint says it was the top metric; I could not reproduce that with the unnormalised value, and the blog says length-normalised PLL reached 0.72 |
| Length (shorter = binder) | 0.43 | 0.36 | Longer designs bound more often among de novo |

- **Among binders, ipTM and pAE do not track affinity.** Spearman correlation of ipTM with KD is +0.15 for all binders (n=53) and +0.28 for strict de novo binders (n=12). A positive value means a higher ipTM goes with a weaker KD. Neither is significant. This matches the paper's "opposite trend" remark.
- **ipTM as a coarse filter:** among strict de novo designs, ipTM ≥ 0.9 gave 6 binders from 63 (9.5%), ipTM ≥ 0.8 gave 8 from 98 (8.2%), and ipTM < 0.8 gave 4 from 108 (3.7%). The signal is weak and the counts are small.

**Your ranking (shape complementarity + ipSAE_min, ipTM ignored):**
- **The EGFR data neither support nor refute it.** ipSAE and shape complementarity were not analysed in the paper or in the public tables. I did not compute them because the AF2 structures were behind the blocked host, and ipSAE also needs the PAE matrices.
- **The data do not show that ipTM is pure noise.** It carries a weak signal (AUC about 0.6–0.7). It fails as an affinity ranker among binders. "Weak binary filter, useless ranker" is what the data actually show.
- **Caveat on all of this.** Classes are confounded. Antibody-like designs have low ipTM but a higher hit rate (23%), and EGF-like designs have high ipTM and a high hit rate. That is why I report the strict subset alongside "all".

## 4. Lengths, classes, expression, developability

**Lengths and classes [COMPUTED, strict de novo binders / designs by length bin]:** ≤60 aa: 3 / 72; 61–100: 2 / 47; 101–150: 2 / 46; >150: 5 / 41. Longer designs did as well or better, and the shortest de novo class was mostly EGF mimics. Classes that produced binders: BindCraft miniproteins (6 / 49 by label), RFdiffusion+MPNN (4 / 61), EGF/TGFα variants, and scFv/nanobodies. Peptides were overrepresented among submissions.

**Expression [COMPUTED; AUC for "high" expression versus the rest]:**
- Glu composition: 0.74 all, 0.77 strict. Preprint: 0.77.
- Lys composition: 0.71 all, 0.73 strict.
- Aggrescan3D average: 0.27 all, 0.25 strict. That means lower aggregation propensity goes with higher expression (equivalent AUC of about 0.73–0.75).
- Helix fraction: 0.63 all, 0.71 strict. β-strand fraction: 0.35 all (lower for expressed).
- ipTM and pLDDT are near chance for expression (0.54–0.65), which matches the paper.
- **Round 2 expression rose from 73% to 95%** after ProteinMPNN with soluble weights plus SoluProt/NetSolP filters [SUMMARY].

**Do Glu/Lys and Aggrescan3D predict binding?** Barely: Glu 0.47 (all) and 0.58 (strict), Lys 0.42 and 0.66, Aggrescan3D average 0.59 (all) and 0.43 (strict), all with wide CIs. Treat them as expression features, not binding features. Note the cell-free expression assay and BLI setup (see the README) differ from a cell-based track.

## 5. Published EGFR binders and methods (reference only, no copying)

- **[Cao et al. 2022, Nature](https://www.nature.com/articles/s41586-022-04654-9)** (Rosetta/hallucination-era, pre-RFdiffusion): designed binders to the native ligand-binding sites of EGFR on domain I (EGFRn_mb) and domain III (EGFRc_mb). The optimised domain I binder reached about 20 nM. The domain III binder's affinity was not stated numerically in what I read. Signalling inhibition (pERK in HUVECs) was shown for the domain I binder. The preprint cites this as the source of the earlier hit-rate benchmark ("0.01%"), though I did not verify that number in Cao itself.
- **[Pacesa et al. 2025, BindCraft, Nature](https://www.nature.com/articles/s41586-025-09429-6):** the method behind the Round 1 and Round 2 de novo winners. I did not verify whether BindCraft's own paper included EGFR.
- **Method write-ups from competitors** (e.g. [ccalia](https://github.com/ccalia/EGFR_Binders_Adaptyv_Round2): composite GB1–linker–minibinder constructs, ipTM ≥ 0.8, NetSolP ranking, domain III hotspots on 6ARU) illustrate design choices only. No binding data are attached.
- **Not found:** a published de novo binder to EGFR domain III with structural confirmation of the cetuximab epitope. Chai-2 and Germinal papers came up in search, but I did not confirm any EGFR result in them.

## 6. What transfers to your three-objective design (domain III + mouse cross-reactivity + pH selectivity)

1. **Base rates are low.** Genuine de novo hit rate was about 6% (or 9% for BindCraft) at ≤10 µM, with only about 1 in 200 reaching under 100 nM. Plan for a small number of binders among many designs.
2. **Domain III appears to have been the most-targeted region, and it is plausible for de novo design.** Domain-III-specific BindCraft on 6ARU gave only weak binders here. That suggests hotspot choice matters.
3. **Ligand-site vs cetuximab-site.** The winning epitope is unknown. Check your epitope face against both EGF-contact residues and the cetuximab footprint before committing.
4. **Do not use ipTM as an affinity ranker.** It is a mild filter at best. The paper's "opposite trend" among binders holds in my recomputation. Whether ipSAE_min and shape complementarity do better is untested here. Your teammate can test it on the released AF2 structures (below).
5. **Expression is worth designing for explicitly.** Soluble-weight MPNN, Glu/Lys-rich surfaces and low Aggrescan3D are supported by this dataset. A Glu/Lys-rich surface may or may not sit comfortably with a His-based pH switch. That is my inference, not something this dataset tests.
6. **Nothing here informs mouse cross-reactivity or pH selectivity.** The competition tested human EGFR ectodomain by BLI at one pH (HBS-T, pH not stated in what I read, 25 °C).
7. **A cheap test for you:** with the AF2 zip and the neutralisation zip, your teammate can (a) compute ipSAE and shape complementarity for all 400 designs and check AUC against the same labels, and (b) see which binders block EGF, which localises the epitope.

## Sources

- [adaptyvbio/egfr_competition_2 (raw data)](https://github.com/adaptyvbio/egfr_competition_2)
- [Crowdsourced Protein Design: Lessons From the Adaptyv EGFR Binder Competition (bioRxiv v2)](https://www.biorxiv.org/content/10.1101/2025.04.17.648362v2)
- [Adaptyv: Protein Optimization 102](https://www.adaptyvbio.com/blog/po102/)
- [Adaptyv: Has binder design been solved? (po104)](https://www.adaptyvbio.com/blog/po104/)
- [Proteinbase: Adaptyv EGFR Binder Design Competition 2](https://proteinbase.com/competitions/adaptyv-egfr-binder2)
- [Cao et al. 2022, Nature](https://www.nature.com/articles/s41586-022-04654-9)
- [Pacesa et al. 2025, BindCraft, Nature](https://www.nature.com/articles/s41586-025-09429-6)
- [ccalia Round 2 design notes](https://github.com/ccalia/EGFR_Binders_Adaptyv_Round2)
