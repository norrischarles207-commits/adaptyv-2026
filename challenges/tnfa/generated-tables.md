#### pH rule across every independent run (bar: >= 7 of 10)

| design | human, per run | human pooled | mouse, per run | mouse pooled | status |
|---|---|---|---|---|---|
| l69_mpnn1 | 10/10, 10/10, 10/10 | 30/30 [0.89–1.00] | 8/10, 5/10, 7/10 | 20/30 | **CONFIRMED** (human, 3 runs) |
| l91_mpnn1 | 9/10, 10/10 | 19/20 [0.76–0.99] | 4/10, 3/10 | 7/20 | **CONFIRMED** (human, 2 runs) |
| l66_mpnn2 | 6/10 | 6/10 [0.31–0.83] | 3/10 | 3/10 | below bar |
| l69_mpnn2 | 4/10, 6/10 | 10/20 [0.30–0.70] | 4/10, 6/10 | 10/20 | below bar |
| l91_mpnn2 | 3/10, 4/10 | 7/20 [0.18–0.57] | 2/10, 3/10 | 5/20 | below bar |
| l66_mpnn1 | 2/10 | 2/10 [0.06–0.51] | 3/10 | 3/10 | below bar |
| l60_mpnn1 | 0/10 | 0/10 [0.00–0.28] | 0/10 | 0/10 | below bar |
| l60_mpnn2 | 0/10 | 0/10 [0.00–0.28] | 0/10 | 0/10 | below bar |
| l62_mpnn20 | 0/10 | 0/10 [0.00–0.28] | 0/10 | 0/10 | below bar |
| l84_mpnn1 | 0/10 | 0/10 [0.00–0.28] | 0/10 | 0/10 | below bar |
| l87_mpnn1 | 0/10 | 0/10 [0.00–0.28] | 0/10 | 0/10 | below bar |
| l97_mpnn2 | 0/10 | 0/10 [0.00–0.28] | 0/10 | 0/10 | below bar |

#### Mouse arm of the two confirmed designs

| design | per run | pooled | P(>= k \| p0 = 2/3) | reading |
|---|---|---|---|---|
| l69_mpnn1 | 8/10, 5/10, 7/10 | 20/30 | 0.585 | cleared the bar in 2 of 3 runs |
| l91_mpnn1 | 4/10, 3/10 | 7/20 | 0.999 | cleared the bar in 0 of 2 runs |

#### Anchor reproducibility (human arm)

| design | run 2 | run 3 |
|---|---|---|
| l69_mpnn1 | His[4] → [32] | His[4] → [32] |
| l91_mpnn1 | His[15, 16] → [32, 65] | His[15] → [32] |

#### Species comparison, 12 designs at n=10 (Amendments 5 and 6)

| design | human mean [range] | mouse mean [range] | diff | pre-registered verdict | exact permutation p |
|---|---|---|---|---|---|
| l60_mpnn1 | n=1 usable | n=0 usable | — | **NOT MEASURABLE** (Am. 6) | — |
| l60_mpnn2 | n=1 usable | n=1 usable | — | **NOT MEASURABLE** (Am. 6) | — |
| l62_mpnn20 | 0.2762 [0.2705] | 0.1709 [0.2264] | +0.1053 | indistinguishable | 4.49e-03 |
| l66_mpnn1 | 0.3834 [0.1438] | 0.3820 [0.1694] | +0.0014 | indistinguishable | 9.46e-01 |
| l66_mpnn2 | 0.3542 [0.0686] | 0.3935 [0.1116] | -0.0393 | indistinguishable | 1.43e-02 |
| l69_mpnn1 | 0.5684 [0.1138] | 0.3185 [0.2127] | +0.2499 | **REAL** | 1.08e-05 |
| l69_mpnn2 | 0.5023 [0.1597] | 0.3149 [0.1959] | +0.1874 | indistinguishable | 1.08e-05 |
| l84_mpnn1 | 0.3563 [0.2520] | 0.4172 [0.1790] | -0.0609 | indistinguishable | 7.82e-02 |
| l87_mpnn1 | 0.3789 [0.0981] | 0.3221 [0.2479] | +0.0568 | indistinguishable | 3.63e-02 |
| l91_mpnn1 | 0.5325 [0.1468] | 0.4472 [0.1984] | +0.0853 | indistinguishable | 3.00e-03 |
| l91_mpnn2 | 0.5089 [0.1722] | 0.4358 [0.2275] | +0.0732 | indistinguishable | 1.48e-02 |
| l97_mpnn2 | 0.3110 [0.1401] | 0.2645 [0.1231] | +0.0466 | indistinguishable | 2.40e-02 |

#### Did the AlphaFold2 screen predict the independent predictor?

| AF2 call | Boltz human counts (12-design run) | mean |
|---|---|---|
| pH-positive (6 designs) | 10, 9, 6, 6, 4, 0 | **5.83/10** |
| pH-negative (6 designs) | 2, 0, 0, 0, 0, 0 | **0.33/10** |

Exact permutation test on the group difference: **p = 0.0152** (14 of 924 splits).

#### Are the hotspots themselves species-conserved?

| hotspot | human | mouse | identical? |
|---|---|---|---|
| R32 (anchor) | R32 | R32 | **yes** |
| K65 (anchor) | K65 | K65 | **yes** |
| D143 | D143 | D142 | **yes** |
| E146 | E146 | E145 | **yes** |
| S86 | S86 | S85 | **yes** |
| Y87 | Y87 | Y86 | **yes** |
| K90 | K90 | K89 | **yes** |

All 7 of 7 hotspots are identical between human and mouse TNF-α (indel at human T72 accounted for).

#### Species-divergent residues inside the epitope (none are hotspots)

| position | human → mouse | note |
|---|---|---|
| 20 | P→H |  |
| 31 | R→Q | adjacent to anchor R32 |
| 73 | H→Y |  |
| 85 | V→I |  |
| 89 | T→E | near hotspot K90 |
| 97 | I→V |  |

#### Contact-pattern asymmetry against the species gap (exploratory)

| design | species gap | contact asymmetry |
|---|---|---|
| l69_mpnn1 | +0.2499 | 11.60 |
| l69_mpnn2 | +0.1874 | 7.50 |
| l62_mpnn20 | +0.1053 | 5.00 |
| l91_mpnn1 | +0.0853 | 4.80 |
| l91_mpnn2 | +0.0732 | 2.90 |
| l87_mpnn1 | +0.0568 | 4.00 |
| l97_mpnn2 | +0.0466 | 7.80 |
| l66_mpnn1 | +0.0014 | 3.20 |
| l66_mpnn2 | -0.0393 | 2.50 |
| l84_mpnn1 | -0.0609 | 5.20 |

Pearson r = **0.742**, Spearman rho = **0.467**, across the 10 measurable designs. Leave-one-out: dropping **l69_mpnn1** takes r to **0.487**; no other single design moves it below 0.697.
