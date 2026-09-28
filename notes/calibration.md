# Cross-validation scoring calibration

Sourcing for the confidence thresholds `modal/redundancy.py` uses to decide which
Boltz-cross-validated designs pass. Written so the choice is reproducible and so
a future reader can tell why we stopped ranking on ipTM.

## Empirical AUCs on real binding data

Analysis of ~2,600 Adaptyv designs with known wet-lab binding outcomes:

| metric                     | AUC   | uses it? |
| -------------------------- | ----- | -------- |
| ipTM                       | 0.52  | no (informational only) |
| pDockQ                     | 0.50  | no |
| shape complementarity (SC) | 0.68  | **yes — pre-filter** (0-1 scale) |
| ipSAE_min                  | 0.615 | **yes — primary rank + decision** |

Interpretation: on real binding outcomes ipTM is at chance (0.52) and pDockQ is
literally chance (0.50). Ranking or thresholding on them cannot separate binders
from non-binders on this dataset, so we log them but do not decide on them.

## Independent literature agreement

- **bioRxiv 2025.08.14.670059** — meta-analysis of 3,766 binders across multiple
  campaigns. Same finding: ipSAE_min is the best single confidence predictor,
  and the recommended selection recipe is:
    1. Pre-filter on shape complementarity.
    2. Rank the survivors by ipSAE_min.

So the recipe below is the recipe the meta-analysis independently arrived at.

## Thresholds used in `modal/redundancy.py`

| constant           | value | rationale                                                              |
| ------------------ | ----- | ---------------------------------------------------------------------- |
| `SC_PASS`          | 0.58  | Adaptyv calibration point (often reported as ~58 in 0-100 units); on pyrosetta's native 0-1 SC scale, that's 0.58. Verified against the smoke run: BindCraft's `Average_ShapeComplementarity` for VEGF_l95_s144661_mpnn18 is 0.67, matching pyrosetta convention. |
| `IPSAE_MIN_PASS`   | 0.60  | The bioRxiv 2025.08.14.670059 operating point; consistent with the Adaptyv AUC=0.615 crossover. |
| `IPSAE_PAE_CUTOFF` | 10.0 Å | Dunbrack 2025 default for identifying interface residues. |
| `IPSAE_PLDDT_CUTOFF` | 70   | Dunbrack 2025 default (pLDDT on 0-100). |
| `IPTM_INFO`        | 0.50  | BindCraft's default_filters.json value; kept only so the informational column is directly comparable to design-time ipTM, not because we use it for decisions. |

## Decision rule

```
cross_val_pass = (SC >= SC_PASS) AND (ipSAE_min >= IPSAE_MIN_PASS)
```

Both conditions required. If SC is missing (BindCraft didn't emit one and the
biopython burial proxy also failed) the design is not passable — an unknown SC
is not a passing SC.

## Ranking

```
composite = ipsae_min * min(SC / SC_PASS, 1.0)
```

- Rewards clearing SC but does not double-count SC beyond the bar.
- ipSAE_min is the primary signal (AUC 0.615, best single confidence metric on
  the meta-analysis).
- ipTM and pDockQ are deliberately absent from the composite.

## ipSAE implementation

Reference: Dunbrack lab `IPSAE` on GitHub (Dunbrack 2025). Our version reproduces
the same core algorithm:

1. For an ordered chain pair (A, B), interface residues in A are those with
   min-over-B PAE ≤ `IPSAE_PAE_CUTOFF` **and** per-residue pLDDT ≥
   `IPSAE_PLDDT_CUTOFF`. Symmetric definition for B.
2. `n_int` = |interface_A| + |interface_B|, used as the aligned-residue count.
3. `d0` = TM-score's d0 formula with the standard `n >= 27` floor:
   `d0 = 1.24 * (max(n_int, 27) - 15) ** (1/3) - 1.8`.
4. `ipSAE(A → B) = mean over interface_A of mean over interface_B of
   1 / (1 + (PAE[i, j] / d0) ** 2)`.
5. `ipSAE_min = min(ipSAE(A → B), ipSAE(B → A))` across all binder ↔ target
   directional pairs, capturing the weaker side of the interface.

Not a homemade normalized-PAE proxy — same d0-tempered pTM aggregation the
reference script uses, only restricted to inter-chain pairs.

## Shape complementarity source

- Preferred: BindCraft's `final_design_stats.csv` (any column matching
  case-insensitive `shape.*complement`; `Average_*` preferred). This is the
  pyrosetta `ShapeComplementarityFilter` value — same scale used at design time.
- Fallback: a biopython Shrake–Rupley buried-SASA proxy (fraction of binder
  SASA lost on complex formation), reported on the same 0-1 scale as pyrosetta
  SC and flagged in `SC_source` as `computed_burial_proxy` so a reader never
  mistakes the proxy for pyrosetta SC.
- If both are missing, `SC_source == "missing"` and `cross_val_pass == False`.

## What changed vs the previous cross-val

- Old decision: ipTM ≥ 0.50 AND normalized ipAE ≤ 0.35 on both models.
- New decision: SC ≥ 0.58 AND ipSAE_min ≥ 0.60 on the Boltz prediction.
- ipTM stays in the output as an informational column so a change from the old
  regime is legible, but it does not gate or rank.
