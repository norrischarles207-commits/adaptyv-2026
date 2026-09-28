# EGFR Challenge Brief

**Challenge 01 · Anthropic × Adaptyv Bio protein binder competition (Track 3)**
*v2 — 6ARU parsed, primary hotspots on conserved cetuximab core, pH anchor = E496*

One epitope can serve all three objectives. The cetuximab site on domain III is a validated functional epitope, its measured 24-residue contact patch is ~71% identical in mouse, and it contains a conserved in-patch acidic residue — E496 — that anchors a pH switch. This v2 replaces the literature-inferred hotspots with residues measured directly from the 6ARU coordinates and updates the pH anchor to the one that's actually in the Fab footprint.

---

## The three objectives, at a glance

| # | Objective | Verdict |
|---|-----------|---------|
| **01** | **Human affinity** — bind human EGFR ECD at a functional epitope (domain III recommended). | Designable · precedent exists |
| **02** | **Mouse cross-reactivity** — same sequence binds mouse EGFR too. | Favorable · pick conserved residues |
| **03 ★ ranked first** | **pH-selective binding** — bind at pH 6.5, no detectable binding at 7.4. | Hard · but highest impact |

**Strategic read:** pH-selectivity is ranked first and Adaptyv says explicitly that a *weak but clearly pH-sensitive* binder beats a strong one that isn't. So the play isn't three separate campaigns — it's **one conserved, functional epitope patch** that lets us layer mouse-conservation and a pH switch onto the same affinity scaffolds. Design for affinity + cross-reactivity on the conserved cetuximab core, then install pH-sensitivity onto the best scaffolds rather than co-optimizing from scratch.

---

## Target & epitope

**EGFR (ErbB1/HER1), UniProt P00533.** Receptor tyrosine kinase; its extracellular region (four domains, I–IV) binds EGF-family ligands in a cleft between domains I and III, which drives receptor dimerization (via the domain II arm) and downstream proliferative signalling. Cetuximab (Erbitux) and panitumumab (Vectibix) are approved antibodies, both binding **domain III** and blocking ligand engagement.

The challenge's reference structure, **PDB 6ARU**, is a cetuximab Fab–EGFR extracellular domain complex — so the challenge points us straight at the cetuximab epitope on domain III as the functional site to design against. Domain III (the L2 leucine-rich β-solenoid, ~residues 334–504 in precursor numbering) presents a moderately convex, mixed polar/charged face — not a deep hydrophobic pocket, but a validated, bindable, druggable epitope.

### Numbering — resolved from the deposited coordinates

Charles parsed the 6ARU mmCIF directly:

- Chain A is EGFR (609 residues, author 4–612), chains B/C are the cetuximab Fab.
- **Author numbering = MATURE EGFR numbering** (signal peptide removed).
- The challenge spec and Charles's provided sequence use **precursor / UniProt numbering** (starts at L25).
- **Precursor = mature + 24.**
- Every residue in this brief is in precursor numbering with mature in parentheses; all 10 previously-cited literature residues were sequence-verified at that offset.
- S468R (mature) = S492R (precursor) — same residue.

---

## The measured cetuximab contact patch

Twenty-four EGFR residues sit within 4.5 Å of the cetuximab Fab in 6ARU. These are the real structural epitope, not a literature-inferred list. Mouse conservation is 17/24 (71%). Divergent residues cluster in two spots — the "resistance corner" 467/491/492 (K→R, I→M, S→N) and 377/442/495/497 at the periphery — which is exactly why cetuximab itself does not cross-react with mouse.

| Precursor | Mature | AA | Human → Mouse | Role |
|-----------|--------|----|---------------| ---- |
| 373 | 349 | P | P → P (cons) | pani |
| 374 | 350 | V | V → V (cons) | |
| 377 | 353 | R | R → K (div) | periphery |
| 406 | 382 | L | L → L (cons) | |
| **408** | **384** | **Q** | **Q → Q (cons)** | **★ primary hotspot · cetux** |
| **432** | **408** | **Q** | **Q → Q (cons)** | **★ primary hotspot · cetux + EGF site** |
| **433** | **409** | **H** | **H → H (cons)** | **★ primary hotspot · native His · EGF site** |
| **435** | **411** | **Q** | **Q → Q (cons)** | **★ primary hotspot** |
| **436** | **412** | **F** | **F → F (cons)** | **★ primary hotspot · pani** |
| 439 | 415 | A | A → A (cons) | |
| 441 | 417 | V | V → V (cons) | |
| 442 | 418 | S | S → G (div) | periphery |
| 462 | 438 | I | I → I (cons) | pani |
| 464 | 440 | S | S → S (cons) | |
| 465 | 441 | G | G → G (cons) | |
| 467 | 443 | K | K → R (div) | ⚠ resistance corner · EGF site |
| **489** | **465** | **K** | **K → K (cons)** | **★ primary hotspot · cetux** |
| **490** | **466** | **I** | **I → I (cons)** | **★ primary hotspot** |
| 491 | 467 | I | I → M (div) | ⚠ resistance corner |
| 492 | 468 | S | S → N (div) | ⚠ resistance corner (S468R) |
| 493 | 469 | N | N → N (cons) | |
| 495 | 471 | G | G → A (div) | periphery |
| **496** | **472** | **E** | **E → E (cons)** | **★★ pH-switch anchor (in-patch, conserved)** |
| 497 | 473 | N | N → K (div) | periphery |

**Design rule for Obj 2:** center the binder footprint on the **conserved core** (373, 374, 406, 408, 432, 433, 435, 436, 439, 441, 462, 464, 465, 489, 490, 493, 496) and **steer away from** 377, 442, 467, 491, 492, 495, 497. A binder gripping the conserved core has a real shot at binding both species from one sequence — exactly the objective.

---

## Objective 3 — the pH switch (bind at 6.5, silent at 7.4)

Tumour interstitium sits at ~pH 6.5; blood at 7.4. Histidine is the only side chain with a pKa (~6.0–6.5) in that window, so it's the switch. Note the direction: most published pH-binders are engineered to *release* at low pH (for receptor recycling / LYTACs). **We need the opposite — bind harder at low pH.** That inverts the mechanism cleanly:

- **Mechanism:** place a *binder* histidine adjacent to a *conserved acidic* residue on the target. At pH 6.5 the His is protonated (+) and forms a salt bridge / H-bond to the target carboxylate → binding. At pH 7.4 the His is neutral → the salt bridge is absent → weak/no binding.
- **Primary anchor: E496 (mature 472).** This is the acidic residue that (a) sits directly in the measured cetuximab contact patch — 4.5 Å from the Fab — and (b) is conserved in mouse. Any binder that occupies the cetuximab footprint has E496 within its interface by construction. This is the pH anchor to design toward.
- **Secondary anchors** (near the patch but not in the 4.5 Å footprint): D379 (mature 355) at 8.8 Å from the Fab, and D460 (mature 436) at 8.6 Å. Both conserved. Useful if the binder's reach differs from cetuximab or as multi-His secondary contacts. Not primary — E496 is.
- **Placement geometry** (from the Sept-2025 pH-binder paper): position binder His imidazole **3.7–7.6 Å** from the target carboxylate; aim for **≥2** His↔anion contacts across the interface; specify His H-bond donor/acceptor state explicitly in ProteinMPNN rather than just raising overall His frequency (their key finding — naive "more histidines" fails).
- **Scoring:** fold each design at both protonation states and rank on the *electrostatic delta* (Rosetta `fa_elec` only, ΔΔG_elec between pH 7 and pH 6). For our direction we want electrostatics to *improve* at low pH (opposite sign to their release-designs). This becomes the Obj-3 ranking column on top of shape complementarity + ipSAE_min.

**Honest caveat:** our window (6.5 vs 7.4, ΔpH ≈ 0.9) is narrower than the 5.4-vs-7.4 gap where the literature got 100–1000× switching, so expect a smaller ratio. That's fine — Adaptyv weights a clear-but-modest pH ratio above raw affinity here. Target a measurable ratio with retained 6.5 binding rather than a huge ratio that kills affinity everywhere.

---

## Objective 1 & designability — what the prior EGFR round tells us

Adaptyv already ran an EGFR binder competition; the post-analysis (bioRxiv 2025.04.17.648362) is direct precedent:

- **~2.5%** de novo hit rate, Round 1 (5/201)
- **82 nM** best de novo K_D (BindCraft, β-sheet interface)
- **0.64** ipTM ROC-AUC — near useless, as expected

Findings:

- **De novo EGFR is achievable but not easy** — a few-percent base hit rate. The winning de novo binder (BindCraft) targeted a β-sheeted interface of EGFR and reached 82 nM. Domain III is a validated site.
- **Their metric findings match our calibration:** ipTM and iPAE were weak (AUC ~0.64); pDockQ/interface-area and ESM2 pseudo-log-likelihood (AUC 0.71) carried more signal. Consistent with our stance — **rank on shape complementarity + ipSAE_min, treat ipTM as noise**, and add ESM2-LL as a cheap secondary filter.
- **Expression predictors:** smaller designs, lower Aggrescan3D aggregation, higher NetSolP, and Glu/Lys content were the strongest separators of expressed/functional designs (AUC 0.73–0.77). Bake these into filtering.
- **Gotcha:** EGFR domain III has N-glycosylation sites and disulfide-rich structure; keep the designed epitope patch on the clean β-face away from glycans, and design against the domain III sub-structure rather than the whole flexible ECD.

**Rule reminder:** the prior round's *best* results came from optimizing cetuximab — **which is banned this round** (de novo, zero-shot only). Cetuximab is our *epitope map*, never a scaffold. Everything we submit must be generated from scratch with adequate sequence/structural diversity from known binders.

---

## Recommended hotspots → for the pipeline

Target residues on 6ARU chain A. Given below in **author/mature numbering to match the deposited coordinates** (this is what the hotspot script indexes into). Precursor numbering shown in the note for cross-reference against the challenge spec.

### Primary — conserved cetuximab-contact core (Obj 1 + Obj 2)

```
A384, A408, A409, A411, A412, A465, A466
```

= precursor Q408, Q432, H433, Q435, F436, K489, I490. All measured as direct cetuximab contacts (any-atom <4.5 Å from Fab), all conserved in mouse. Tight spatial cluster within the true Fab footprint (max Cα-Cα ~14 Å). Native H433 contributes a conserved His at the interface. **This is the affinity + cross-reactivity target for BindCraft.**

### pH-switch anchor — for Phase 3 His-biased redesign

```
A472
```

= precursor E496. In-patch, conserved acidic residue. Bias ProteinMPNN to place binder histidines within 3.7–7.6 Å of the E496 side-chain carboxylate on the top affinity scaffolds; then score on ΔΔG_elec(pH 7 − pH 6). Not a design target for the base affinity run — layered on afterward.

### Optional secondary pH anchors (near patch, not in Fab contact)

```
A355, A436
```

= precursor D379, D460. Both conserved acidic residues 8–9 Å off the direct contact patch. Useful for a second binder-His if the design has geometry that reaches them, or as backup anchors if E496-focused designs underperform on pH ratio.

**Do NOT target:** mature `A443, A467, A468` (= precursor K467, I491, S492) — the resistance corner where human and mouse diverge (K→R, I→M, S→N). Also steer clear of the periphery divergent residues at precursor 377, 442, 495, 497.

---

## Budget & sequencing call

- **Phase 1 — conserved-core affinity (biggest batch).** Run BindCraft against the primary hotspot set `A384, A408, A409, A411, A412, A465, A466` on the domain III sub-structure of 6ARU chain A. At a ~2–5% expected hit rate, budget the bulk of trajectories here. Filter on shape complementarity + ipSAE_min (+ ESM2-LL, Aggrescan3D, size). These designs satisfy Obj 1 and, because the patch is conserved, are Obj-2 candidates by construction.
- **Phase 2 — verify mouse in silico (cheap).** Re-fold the top affinity designs against mouse EGFR (AF-Q01279-F1) and keep those with retained interface metrics. No new design compute — just scoring.
- **Phase 3 — install pH switch onto winners (targeted).** Take the best Phase-1/2 scaffolds and do His-biased ProteinMPNN redesign near **E496** (mature A472), then the dual-protonation ΔΔG_elec screen. Cheapest route to Obj 3 — layered onto proven scaffolds rather than co-optimizing pH from scratch.
- **Submission mix (up to 20):** lead with the pH-sensitive designs (ranked objective), then cross-reactive high-affinity, then pure high-affinity human as the floor. Rank the CSV in that order — Adaptyv's Claude-based selection reads our ranking.

---

## Methods-log seed

**Target:** Human EGFR ECD (P00533), domain III; mouse ortholog Q01279
**Requirement:** affinity + mouse cross-reactivity + pH-selective (6.5 vs 7.4)
**Epitope:** measured cetuximab contact patch on 6ARU chain A (24 EGFR residues within 4.5 Å of Fab); primary conserved core = precursor Q408, Q432, H433, Q435, F436, K489, I490 (mature 384, 408, 409, 411, 412, 465, 466); pH-switch anchor = precursor E496 (mature 472), in-patch and mouse-conserved; derivation = direct BioPython interface analysis of the deposited 6ARU coordinates + human/mouse alignment of provided sequences (domain III 92% id); numbering: author = mature, precursor = author + 24, all 10 literature residues sequence-verified
**Pipeline:** BindCraft (Modal) on 6ARU chain A domain III → ProteinMPNN (His-biased redesign near E496 for pH) → AF2/Boltz-2 re-fold at pH 6.5/7.4 protonation states
**Selection:** shape complementarity + ipSAE_min (primary); ESM2-LL, Aggrescan3D, NetSolP, size (developability); ΔΔG_elec(pH7−pH6) for pH ranking; ipTM excluded (AUC 0.64 on prior EGFR round)
**Cross-check:** re-fold top designs vs mouse EGFR (AF-Q01279-F1), require retained interface
**Decisions:** de novo/zero-shot only — cetuximab used as epitope map, never scaffold; avoid divergent resistance corner (precursor K467/I491/S492) and periphery (377/442/495/497)
**Result:** *(fill run numbers)*

---

## Confirmed from the 6ARU coordinates

The v1 "open item to confirm in-pipeline" is now closed. Findings from the deposited mmCIF (BioPython NeighborSearch, 4.5 Å any-atom cutoff):

- **Chain A = EGFR**, author residues 4–612 (609 residues), covers ECD domains I–IV. Chains B/C = cetuximab Fab light + heavy.
- **Numbering:** author = mature; precursor = author + 24. Sequence-verified at all 10 literature epitope positions against the provided human sequence.
- **Cetuximab contact patch:** 24 EGFR residues at 4.5 Å (26 at 5.0 Å). Full list in the epitope table above.
- **Mouse conservation of contact patch:** 17/24 = 71%. Divergent residues cluster in the resistance corner (467/491/492) + periphery (377/442/495/497).
- **Primary patch geometry:** Q408/Q432/H433/Q435/F436/K489/I490 max Cα-Cα ~14 Å — tight, contiguous cluster inside the Fab footprint. (Contrast: the v1 patch including D379 spanned 23 Å — D379 was 15+ Å from the other three.)
- **pH-anchor correction (v1 → v2):** D379 is *not* a direct cetuximab contact — closest atom is 8.77 Å from the Fab. E496 is the correct primary pH anchor (in-patch + conserved). D379 and D460 retained as optional secondary anchors.

---

## Sources

- [PDB 6ARU](https://www.rcsb.org/structure/6ARU) — Cetuximab Fab mutant + EGFR extracellular domain (challenge reference structure; parsed directly for this brief)
- [PDB 1YY9](https://www.rcsb.org/structure/1YY9) — EGFR ECD + cetuximab Fab (Li et al. 2005, original epitope structure)
- [Voigt et al. 2014, mAbs](https://www.tandfonline.com/doi/pdf/10.4161/mabs.28915) — functional dissection of cetuximab & panitumumab EGFR epitopes (contact residues)
- [Sickmier / Frontiers Oncology 2019](https://www.frontiersin.org/articles/10.3389/fonc.2019.00849/full) — cetuximab vs panitumumab epitope residues & EGF-site overlap
- [Adaptyv EGFR competition post-analysis (bioRxiv 2025.04.17.648362)](https://www.biorxiv.org/content/10.1101/2025.04.17.648362v2) — de novo hit rates, metric performance, best designs
- [Computational design of pH-sensitive binders (bioRxiv 2025.09.29.678932)](https://www.biorxiv.org/content/10.1101/2025.09.29.678932v1.full) — His-switch mechanism, placement geometry, ΔΔG_elec scoring
- [PDB 1NQL](https://www.rcsb.org/structure/1NQL) — EGFR ECD in inactive low-pH complex with EGF (pH-conformational context)
- UniProt [P00533](https://www.uniprot.org/uniprotkb/P00533/entry) (human) · [Q01279](https://www.uniprot.org/uniprotkb/Q01279/entry) (mouse) — sequences, domain annotations, signal-peptide boundary

---

*v2 · 6ARU coordinates parsed · Companion to the Binder Design Playbook, Competition Readiness, and Malachi's Research Kit + Literature Pass · all designs de novo / zero-shot · residue numbers in precursor (UniProt) numbering unless noted "mature" (for coordinate/pipeline handoff).*
