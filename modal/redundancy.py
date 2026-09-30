"""redundancy.py -- target-agnostic 2-model cross-validation for BindCraft designs.

Independent second opinion on BindCraft/AF2-accepted designs, using Boltz-2 as
a structurally- and MSA-independent predictor. For each design we re-predict the
binder-target complex with Boltz and score the interface with the metrics that
actually track wet-lab binding on real-world Adaptyv/meta-analysis data.

Every entrypoint here takes --target <slug>, matching the slug used by
run_bindcraft.py's --target so a challenge's designs, under
/designs/<target>/attempts/..., are found and cross-validated without any
per-target code change.

Calibration (see notes/calibration.md for full sourcing):
  - ipTM (AUC 0.52) and pDockQ (0.50) do not predict real binding on the
    ~2,600-design Adaptyv set; a 3,766-binder bioRxiv meta-analysis
    (2025.08.14.670059) independently agrees.
  - Shape complementarity (AUC 0.68) and ipSAE_min (0.615) do. The recommended
    recipe is: pre-filter on SC, then rank by ipSAE_min.

Metric roles here:
  - SC (BindCraft's shape complementarity, 0-100): PRE-FILTER. Pass at ~58.
    Reused from BindCraft's final_design_stats.csv when present; otherwise a
    biopython buried-SASA proxy is computed and clearly flagged as `computed`
    so a reader never mistakes the proxy for the pyrosetta SC value.
  - ipSAE_min: PRIMARY DECISION + RANKING metric. Pass at ~0.60. Computed from
    Boltz's full PAE matrix + per-residue pLDDT using the reference formulation
    (Dunbrack 2025, `ipsae` on GitHub) -- interface residues by PAE + pLDDT,
    d0 from TM-score's length formula, min across the two chain directions.
    Not a homemade normalized-PAE proxy.
  - ipTM: kept in the output as INFORMATIONAL. Not used to pass or rank.

`cross_val_pass` == (SC >= SC_PASS) AND (ipsae_min >= IPSAE_MIN_PASS). Anything
else (missing SC, missing pLDDT, one metric failing) is NOT a pass.

Ranking: composite = ipsae_min * min(SC / SC_PASS, 1.0). Rewards clearing the
SC bar but does not double-count SC beyond it; ipSAE_min is the primary signal.

Run (--target is required in every case; --smoke needs --smoke-design-id too):
    # cheap single-design validation (Boltz run + score):
    modal run --detach modal/redundancy.py::main --target vegf --smoke --smoke-design-id VEGF_l95_s144661_mpnn18
    # rescore already-run designs from cached Boltz outputs (no GPU):
    modal run modal/redundancy.py::rescore_saved --target vegf
    # full shortlist:
    modal run --detach modal/redundancy.py::main --target vegf
"""
import modal

app = modal.App("adaptyv-binders")

# adaptyv-designs holds every challenge's accepted designs (namespaced by
# target slug), and is where we write each challenge's crossval table.
designs = modal.Volume.from_name("adaptyv-designs", create_if_missing=True)
# New persistent volume for Boltz's model weights + CCD/mols data (~a few GB),
# so they download once and are reused -- same pattern as the AF2 weights volume.
boltz_weights = modal.Volume.from_name("boltz-weights", create_if_missing=True)

# BOLTZ_CACHE must be an ABSOLUTE path (boltz asserts this); it is the mount point
# of the boltz-weights volume, so all downloaded checkpoints/data land on the volume.
BOLTZ_CACHE = "/boltz-cache"

BOLTZ_VERSION = "2.2.1"

image = (
    modal.Image.debian_slim(python_version="3.11")
    .apt_install("git", "wget")
    .pip_install(
        f"boltz[cuda]=={BOLTZ_VERSION}",
        "biopython",
        "pandas",
        "numpy<2",
        "pyyaml",
    )
)

# --- Calibration thresholds (notes/calibration.md) --------------------------
# Pre-filter: BindCraft's shape complementarity (pyrosetta ShapeComplementarity
# Filter). BindCraft's Average_ShapeComplementarity column is on the pyrosetta
# 0-1 scale (Lawrence & Colman convention), verified against the smoke run
# (VEGF_l95_s144661_mpnn18 reports 0.67). The Adaptyv calibration point ~58
# in 0-100 units is 0.58 here.
SC_PASS = 0.58

# Primary decision + rank metric: Dunbrack 2025 ipSAE_min. 0.60 is the
# published operating point (matches the bioRxiv 2025.08.14.670059 recipe).
IPSAE_MIN_PASS = 0.60

# ipSAE interface-residue selection (Dunbrack ipsae defaults).
IPSAE_PAE_CUTOFF = 10.0    # angstroms; a residue is "in interface" if any cross-chain PAE <= this
IPSAE_PLDDT_CUTOFF = 70.0  # per-residue pLDDT on the 0-100 scale (Boltz emits 0-1; we rescale)

# ipTM is kept for the record but is not used in the pass/rank decision (AUC 0.52
# on the Adaptyv set). Same threshold BindCraft's default_filters.json uses so
# the informational column is directly comparable to the design-time value.
IPTM_INFO = 0.50

# AF2 PAE reporting normalization (colabdesign/af/loss.py: get_pae()/31.0).
PAE_NORM = 31.0

# Split a merged multi-subchain target (BindCraft labels a multi-chain target
# passed as one PDB chain -- e.g. the VEGF V+W dimer in the original VEGF
# challenge -- as a single chain A with a large artificial numbering gap at
# each subchain boundary) back into separate chains. A gap this large never
# occurs inside a real folded chain.
GAP_SPLIT = 30


@app.function(
    image=image,
    volumes={BOLTZ_CACHE: boltz_weights},
    timeout=3600,
)
def download_boltz_weights():
    """Download Boltz-2 weights + data to the boltz-weights volume, once."""
    import os
    from pathlib import Path

    marker = f"{BOLTZ_CACHE}/done.txt"
    if os.path.exists(marker):
        print("boltz weights already present")
        return

    os.makedirs(BOLTZ_CACHE, exist_ok=True)
    from boltz.main import download_boltz2

    download_boltz2(Path(BOLTZ_CACHE))
    open(marker, "w").close()
    boltz_weights.commit()
    print("boltz weights committed to volume")


# --------------------------------------------------------------------------- #
# Chain / sequence helpers
# --------------------------------------------------------------------------- #

def _chain_segments(chain, gap_split):
    """Yield (sequence, resnums) segments of a chain, split at numbering gaps
    larger than gap_split (to separate merged subchains)."""
    from Bio.SeqUtils import seq1

    residues = [r for r in chain if r.id[0] == " "]
    seg_seq, seg_nums = [], []
    prev = None
    for r in residues:
        num = r.id[1]
        if prev is not None and (num - prev) > gap_split:
            yield "".join(seg_seq), seg_nums
            seg_seq, seg_nums = [], []
        seg_seq.append(seq1(r.resname))
        seg_nums.append(num)
        prev = num
    if seg_seq:
        yield "".join(seg_seq), seg_nums


def _extract_chains(pdb_path, gap_split=GAP_SPLIT):
    """Return (target_seqs, binder_seq). Chain A = target (may be a merged
    multimer -> split into several sequences); chain B = binder."""
    from Bio.PDB import PDBParser

    model = PDBParser(QUIET=True).get_structure("x", pdb_path)[0]
    target_seqs, binder_seq = [], None
    for ch in model:
        if ch.id == "B":
            binder_seq = "".join(s for s, _ in _chain_segments(ch, gap_split))
        else:
            for seq, _ in _chain_segments(ch, gap_split):
                if seq:
                    target_seqs.append(seq)
    if binder_seq is None:
        raise RuntimeError(f"no chain B (binder) found in {pdb_path}")
    if not target_seqs:
        raise RuntimeError(f"no target chain found in {pdb_path}")
    return target_seqs, binder_seq


# --------------------------------------------------------------------------- #
# ipSAE (Dunbrack 2025, https://github.com/DunbrackLab/IPSAE)
# --------------------------------------------------------------------------- #

def _tm_d0(n):
    """TM-score d0 with the standard n>=27 floor (Zhang & Skolnick 2004).
    ipsae.py uses this same formula on the interface-residue count."""
    n_eff = max(int(n), 27)
    return 1.24 * (n_eff - 15) ** (1.0 / 3.0) - 1.8


def _compute_ipsae(
    pae,
    plddt_0_100,
    chain_slices,
    pae_cutoff=IPSAE_PAE_CUTOFF,
    plddt_cutoff=IPSAE_PLDDT_CUTOFF,
):
    """Compute ipSAE per chain pair, per Dunbrack 2025.

    Args:
      pae: (N, N) PAE matrix in angstroms (Boltz's native scale).
      plddt_0_100: (N,) per-residue pLDDT on 0-100 scale.
      chain_slices: list of (chain_id, slice) covering the token axis in order.
      pae_cutoff: interface PAE threshold in angstroms (default 10).
      plddt_cutoff: interface pLDDT threshold on 0-100 (default 70).

    For each ordered chain pair (A, B) A != B:
      1. Interface residues in A wrt B = { i in A : plddt_i >= cutoff AND
         min_{j in B} PAE[i, j] <= pae_cutoff }.
      2. n_int = |interface_A| + |interface_B| (aligned-residue proxy).
      3. d0 = TM-score d0(n_int).
      4. For each interface residue i in A, mean over j in interface_B of
         1 / (1 + (PAE[i, j] / d0)^2). Average over interface_A -> ipSAE(A->B).
      5. ipSAE(B->A) symmetrically, using PAE[j, i].
    Return {"ipsae_min": min over ordered pairs, "pairs": per-pair details}.

    Two-chain systems here always have exactly one binder chain and one or more
    target chains. We compute ipSAE for every (binder <-> target-subchain) pair
    and ipsae_min is the minimum over those directional scores, capturing the
    weakest side of the interface.
    """
    import numpy as np

    N = pae.shape[0]
    if pae.shape != (N, N):
        raise ValueError(f"PAE matrix not square: {pae.shape}")
    if plddt_0_100.shape != (N,):
        raise ValueError(
            f"pLDDT length {plddt_0_100.shape} != PAE dim {N}"
        )

    # Only inter-chain pairs. Same-chain pairs are excluded from ipsae by construction.
    pairs = []
    for a_id, a_slice in chain_slices:
        for b_id, b_slice in chain_slices:
            if a_id == b_id:
                continue

            pae_ab = pae[a_slice, b_slice]                     # (nA, nB), PAE A->B
            plddt_a = plddt_0_100[a_slice]
            plddt_b = plddt_0_100[b_slice]

            # interface residues in A wrt B
            min_pae_a = pae_ab.min(axis=1) if pae_ab.size else np.array([])
            int_a_mask = (plddt_a >= plddt_cutoff) & (min_pae_a <= pae_cutoff)
            # interface residues in B wrt A (using the transpose direction)
            min_pae_b = pae[b_slice, a_slice].min(axis=1) if pae_ab.size else np.array([])
            int_b_mask = (plddt_b >= plddt_cutoff) & (min_pae_b <= pae_cutoff)

            n_int_a = int(int_a_mask.sum())
            n_int_b = int(int_b_mask.sum())
            n_int = n_int_a + n_int_b

            if n_int_a == 0 or n_int_b == 0:
                pairs.append({
                    "a": a_id, "b": b_id, "n_int_a": n_int_a, "n_int_b": n_int_b,
                    "d0": None, "ipsae": None,
                })
                continue

            d0 = _tm_d0(n_int)
            # ipsae(A->B): for each interface residue i in A, mean over
            # interface residues j in B of 1/(1 + (PAE[i,j]/d0)^2). Then avg over i.
            pae_int = pae_ab[np.ix_(int_a_mask, int_b_mask)]
            per_pair = 1.0 / (1.0 + (pae_int / d0) ** 2)
            per_i = per_pair.mean(axis=1)          # shape (n_int_a,)
            ipsae_ab = float(per_i.mean())

            pairs.append({
                "a": a_id, "b": b_id,
                "n_int_a": n_int_a, "n_int_b": n_int_b,
                "d0": round(d0, 3),
                "ipsae": round(ipsae_ab, 4),
            })

    scored = [p["ipsae"] for p in pairs if p["ipsae"] is not None]
    return {
        "ipsae_min": (round(min(scored), 4) if scored else None),
        "pairs": pairs,
    }


# --------------------------------------------------------------------------- #
# Shape complementarity: read BindCraft's value; fall back to a computed proxy.
# --------------------------------------------------------------------------- #

def _read_bindcraft_sc(design_dir):
    """Try to read BindCraft's ShapeComplementarity value for this design.

    Returns (sc_value, column_name) or (None, None) if not present. BindCraft's
    final_design_stats.csv uses per-model + Average columns for each metric.
    Column names vary slightly by BindCraft revision -- we search for any
    column whose name contains 'shape' and 'complement' (case-insensitive),
    preferring the Average_* column.
    """
    import os

    p = os.path.join(design_dir, "final_design_stats.csv")
    if not os.path.exists(p):
        return None, None
    import pandas as pd
    df = pd.read_csv(p)
    if not len(df):
        return None, None
    row = df.iloc[0]

    def looks_like_sc(col):
        c = col.lower()
        return ("shape" in c and "complement" in c) or c in ("sc", "sc_all")

    # Prefer Average_*; then any per-model.
    sc_cols = [c for c in df.columns if looks_like_sc(c)]
    avg_first = sorted(sc_cols, key=lambda c: (0 if c.lower().startswith("average") else 1, c))
    for col in avg_first:
        if pd.notna(row[col]):
            try:
                return float(row[col]), col
            except (TypeError, ValueError):
                continue
    return None, None


def _compute_sc_proxy(pdb_path):
    """Fallback SC proxy: interface burial from biopython's SASA calculator.

    Not true Lawrence-Colman SC (which needs surface-curvature matching).
    Reported on the same 0-1 scale as pyrosetta SC (fraction of binder SASA
    lost on complex formation), so it drops into the same column position,
    but the value is a burial fraction, not shape complementarity. Flagged
    as source='computed_burial_proxy' so a reader never confuses it with
    the real pyrosetta SC number.
    """
    from Bio.PDB import PDBParser
    from Bio.PDB.SASA import ShrakeRupley

    parser = PDBParser(QUIET=True)
    complex_struct = parser.get_structure("cx", pdb_path)
    binder_alone = parser.get_structure("bd", pdb_path)

    # SASA of full complex
    ShrakeRupley().compute(complex_struct, level="R")
    binder_sasa_in_complex = 0.0
    for ch in complex_struct[0]:
        if ch.id == "B":
            for r in ch:
                if r.id[0] == " ":
                    binder_sasa_in_complex += float(r.sasa)

    # SASA of the binder chain in isolation
    model_alone = binder_alone[0]
    for ch_id in [c.id for c in model_alone]:
        if ch_id != "B":
            model_alone.detach_child(ch_id)
    ShrakeRupley().compute(binder_alone, level="R")
    binder_sasa_alone = 0.0
    for ch in binder_alone[0]:
        if ch.id == "B":
            for r in ch:
                if r.id[0] == " ":
                    binder_sasa_alone += float(r.sasa)

    if binder_sasa_alone <= 0:
        return None
    buried_frac = 1.0 - (binder_sasa_in_complex / binder_sasa_alone)
    # Report on 0-1 to match pyrosetta SC's scale; sc_source is the load-bearing
    # signal that this is a burial-fraction proxy, not real ShapeComplementarity.
    return round(max(0.0, min(1.0, buried_frac)), 4)


def _get_sc(design_dir, pdb_path):
    """Return {'value': float|None, 'source': 'bindcraft'|'computed_burial_proxy'|'missing', 'column': str|None}."""
    sc_bc, col = _read_bindcraft_sc(design_dir)
    if sc_bc is not None:
        return {"value": round(float(sc_bc), 4), "source": "bindcraft", "column": col}
    try:
        v = _compute_sc_proxy(pdb_path)
    except Exception as e:
        print(f"[warn] sc proxy failed on {pdb_path}: {e}")
        v = None
    if v is None:
        return {"value": None, "source": "missing", "column": None}
    return {"value": v, "source": "computed_burial_proxy", "column": None}


# --------------------------------------------------------------------------- #
# AF2 scores (informational only from here on)
# --------------------------------------------------------------------------- #

def _read_af2_scores(design_dir):
    """Pull AF2 i_pTM / i_pAE from BindCraft's final_design_stats.csv."""
    import os

    p = os.path.join(design_dir, "final_design_stats.csv")
    if not os.path.exists(p):
        return None, None
    import pandas as pd
    df = pd.read_csv(p)
    if not len(df):
        return None, None
    row = df.iloc[0]

    def g(col):
        return float(row[col]) if col in row and pd.notna(row[col]) else None

    return g("Average_i_pTM"), g("Average_i_pAE")


# --------------------------------------------------------------------------- #
# Boltz driver + scorer
# --------------------------------------------------------------------------- #

def _load_boltz_arrays(out_dir):
    """Return (pae A, plddt 0-100, conf dict, pred_dir) from a Boltz predict tree.

    Boltz 2.x nests outputs under out_dir/boltz_results_<stem>/predictions/<stem>/,
    so glob recursively for the artifacts rather than hardcoding the path.
    plddt is loaded from the plddt npz when present; otherwise from the PDB's
    B-factor column (per-residue pLDDT is what Boltz writes to that column).
    """
    import glob
    import json
    import os

    import numpy as np

    conf_matches = glob.glob(
        os.path.join(out_dir, "**", "confidence_*_model_0.json"), recursive=True
    )
    if not conf_matches:
        raise RuntimeError(f"no confidence_*_model_0.json under {out_dir}")
    conf_path = conf_matches[0]
    pred_dir = os.path.dirname(conf_path)
    with open(conf_path) as fh:
        conf = json.load(fh)

    pae_matches = glob.glob(
        os.path.join(out_dir, "**", "pae_*_model_0.npz"), recursive=True
    )
    if not pae_matches:
        raise FileNotFoundError("no pae_*_model_0.npz found (need --write_full_pae)")
    pae_data = np.load(pae_matches[0])
    pae = pae_data["pae"] if "pae" in pae_data.files else pae_data[pae_data.files[0]]

    plddt = None
    plddt_matches = glob.glob(
        os.path.join(out_dir, "**", "plddt_*_model_0.npz"), recursive=True
    )
    if plddt_matches:
        pl = np.load(plddt_matches[0])
        arr = pl["plddt"] if "plddt" in pl.files else pl[pl.files[0]]
        arr = np.asarray(arr).ravel()
        # Boltz emits plddt on 0-1; ipsae thresholds are on the 0-100 scale.
        plddt = arr * 100.0 if arr.max() <= 1.0 else arr

    if plddt is None:
        # fall back to the predicted PDB's B-factor column (per-CA)
        pdb_matches = glob.glob(os.path.join(pred_dir, "*.pdb"))
        if not pdb_matches:
            raise FileNotFoundError("no Boltz-predicted PDB found for pLDDT fallback")
        plddt = _plddt_from_pdb(pdb_matches[0])

    return pae, plddt, conf, pred_dir


def _plddt_from_pdb(pdb_path):
    """Extract per-residue CA pLDDT from a Boltz-predicted PDB (B-factor col).
    Returns a numpy array in Boltz token order (target chain(s) then binder)."""
    import numpy as np
    from Bio.PDB import PDBParser

    model = PDBParser(QUIET=True).get_structure("p", pdb_path)[0]
    vals = []
    for ch in sorted(model, key=lambda c: c.id):
        for r in ch:
            if r.id[0] != " ":
                continue
            ca = r["CA"] if "CA" in r else None
            if ca is None:
                continue
            vals.append(float(ca.get_bfactor()))
    arr = np.array(vals, dtype=float)
    return arr * 100.0 if arr.size and arr.max() <= 1.0 else arr


def _chain_slices_for(target_seqs, binder_seq):
    """Return [(chain_id, slice), ...] in Boltz's token order: targets, then binder."""
    slices = []
    cursor = 0
    letters = [chr(ord("A") + i) for i in range(len(target_seqs) + 1)]
    for i, s in enumerate(target_seqs):
        slices.append((letters[i], slice(cursor, cursor + len(s))))
        cursor += len(s)
    slices.append((letters[len(target_seqs)], slice(cursor, cursor + len(binder_seq))))
    return slices


def _score_from_boltz_outputs(design_id, pdb_path, out_dir, sc_info):
    """Compute all metrics + decisions from cached Boltz outputs. CPU-only."""
    import json

    target_seqs, binder_seq = _extract_chains(pdb_path)
    pae, plddt, conf, pred_dir = _load_boltz_arrays(out_dir)

    n_expected = sum(len(s) for s in target_seqs) + len(binder_seq)
    if pae.shape[0] != n_expected:
        raise RuntimeError(
            f"PAE dim {pae.shape[0]} does not match sequence length {n_expected}; "
            f"Boltz token order may differ from the design PDB"
        )

    slices = _chain_slices_for(target_seqs, binder_seq)
    ipsae = _compute_ipsae(pae, plddt, slices)

    boltz_iptm = float(conf.get("iptm")) if conf.get("iptm") is not None else None
    boltz_ptm = float(conf.get("ptm")) if conf.get("ptm") is not None else None
    boltz_plddt = float(conf.get("complex_plddt")) if conf.get("complex_plddt") is not None else None

    # legacy raw interface PAE (kept in output for transparency, not for decisions)
    import numpy as np
    n_target = sum(len(s) for s in target_seqs)
    inter = np.concatenate([
        pae[:n_target, n_target:].ravel(),
        pae[n_target:, :n_target].ravel(),
    ])
    boltz_ipae_A = float(inter.mean())
    boltz_ipae_norm = boltz_ipae_A / PAE_NORM

    # AF2 side (informational; not part of the pass decision)
    design_dir = pdb_path
    for _ in range(2):
        design_dir = _dirname(design_dir)      # <design_dir>/Accepted/<pdb> -> <design_dir>
    af2_iptm, af2_ipae = _read_af2_scores(design_dir)

    # --- decision + rank -----------------------------------------------------
    sc_val = sc_info["value"]
    ipsae_min = ipsae["ipsae_min"]

    sc_pass = sc_val is not None and sc_val >= SC_PASS
    ipsae_pass = ipsae_min is not None and ipsae_min >= IPSAE_MIN_PASS
    cross_val_pass = bool(sc_pass and ipsae_pass)

    if ipsae_min is not None and sc_val is not None:
        composite = round(ipsae_min * min(sc_val / SC_PASS, 1.0), 4)
    else:
        composite = None

    result = {
        "design_id": design_id,
        # decision metrics
        "sc": sc_val,
        "sc_source": sc_info["source"],           # bindcraft / computed_burial_proxy / missing
        "sc_column": sc_info["column"],
        "sc_pass": sc_pass,
        "ipsae_min": ipsae_min,
        "ipsae_pass": ipsae_pass,
        "cross_val_pass": cross_val_pass,
        "composite_rank": composite,
        # informational
        "boltz_iptm": round(boltz_iptm, 3) if boltz_iptm is not None else None,
        "boltz_iptm_info_pass": (boltz_iptm is not None and boltz_iptm >= IPTM_INFO),
        "boltz_ptm": round(boltz_ptm, 3) if boltz_ptm is not None else None,
        "boltz_plddt": round(boltz_plddt, 3) if boltz_plddt is not None else None,
        "boltz_ipae_A": round(boltz_ipae_A, 2),
        "boltz_ipae_norm": round(boltz_ipae_norm, 3),
        "af2_iptm": af2_iptm,
        "af2_ipae": af2_ipae,
        # diagnostics
        "ipsae_pairs": ipsae["pairs"],
    }
    return result, pred_dir


def _dirname(p):
    import os
    return os.path.dirname(p)


@app.function(
    gpu="A10G",
    image=image,
    volumes={"/designs": designs, BOLTZ_CACHE: boltz_weights},
    timeout=3600,
)
def crossval_boltz(design_id: str, pdb_path: str):
    """Re-predict one binder-target complex with Boltz-2 and apply the new
    calibration-driven scoring (SC pre-filter + ipSAE_min ranking; ipTM info)."""
    import json
    import os
    import subprocess

    import yaml

    os.environ["BOLTZ_CACHE"] = BOLTZ_CACHE

    target_seqs, binder_seq = _extract_chains(pdb_path)
    print(f"{design_id}: target chains {[len(s) for s in target_seqs]}, binder {len(binder_seq)}")

    # --- build Boltz YAML: each target subchain + the binder as protein chains ---
    letters = [chr(ord("A") + i) for i in range(len(target_seqs) + 1)]
    yaml_doc = {"version": 1, "sequences": []}
    for i, s in enumerate(target_seqs):
        yaml_doc["sequences"].append({"protein": {"id": letters[i], "sequence": s}})
    binder_id = letters[len(target_seqs)]
    yaml_doc["sequences"].append({"protein": {"id": binder_id, "sequence": binder_seq}})

    work = f"/tmp/{design_id}"
    os.makedirs(work, exist_ok=True)
    yaml_path = f"{work}/{design_id}.yaml"
    with open(yaml_path, "w") as fh:
        yaml.safe_dump(yaml_doc, fh, sort_keys=False)
    print("boltz input yaml:\n" + open(yaml_path).read())

    out_dir = f"{work}/out"
    cmd = [
        "boltz", "predict", yaml_path,
        "--out_dir", out_dir,
        "--cache", BOLTZ_CACHE,
        "--use_msa_server",
        "--write_full_pae",
        "--accelerator", "gpu",
        "--devices", "1",
        "--override",
        "--output_format", "pdb",
    ]
    print("running:", " ".join(cmd))
    subprocess.run(cmd, check=True, env={**os.environ, "BOLTZ_CACHE": BOLTZ_CACHE})

    # --- SC + score from cached outputs (SC needs the design_dir + pdb) --------
    design_dir = os.path.dirname(os.path.dirname(pdb_path))  # .../<seed> (parent of Accepted)
    sc_info = _get_sc(design_dir, pdb_path)
    result, pred_dir = _score_from_boltz_outputs(design_id, pdb_path, out_dir, sc_info)

    # --- persist Boltz predictions + PAE/pLDDT for CPU-only rescoring later ---
    save_dir = os.path.join(design_dir, "boltz_crossval")
    os.makedirs(save_dir, exist_ok=True)
    try:
        import glob
        import shutil
        for f in os.listdir(pred_dir):
            if f.endswith(".pdb") or f.startswith("confidence_"):
                shutil.copy(os.path.join(pred_dir, f), os.path.join(save_dir, f))
        # persist the PAE + pLDDT arrays so rescore_saved can rerun the scorer
        # without paying for a GPU/Boltz re-prediction.
        for pattern in ("pae_*_model_0.npz", "plddt_*_model_0.npz"):
            for src in glob.glob(os.path.join(out_dir, "**", pattern), recursive=True):
                shutil.copy(src, os.path.join(save_dir, os.path.basename(src)))
        with open(os.path.join(save_dir, "crossval_result.json"), "w") as fh:
            json.dump(result, fh, indent=2)
        designs.commit()
    except Exception as e:
        print(f"[warn] could not persist boltz outputs for {design_id}: {e}")

    print("RESULT:", json.dumps({k: v for k, v in result.items() if k != "ipsae_pairs"}))
    return result


# --------------------------------------------------------------------------- #
# Table + output formatting
# --------------------------------------------------------------------------- #

def _yn(v):
    return "?" if v is None else ("Y" if v else "N")


def _consensus_table(results):
    """Format the cross-validation table. Ranked by composite (ipsae_min * SC/threshold).
    ipTM shown as an informational column, not used for the pass decision."""
    def fmt(v, nd=3):
        return "n/a" if v is None else f"{v:.{nd}f}"

    header = (
        f"{'design_id':30s} {'SC':>6s} {'SC_src':>16s} "
        f"{'ipSAE_min':>10s} {'composite':>10s} "
        f"{'Boltz_ipTM*':>12s} {'AF2_ipTM*':>10s} "
        f"{'SC_pass':>8s} {'ipSAE_pass':>11s} {'crossval':>9s}"
    )
    lines = [
        header,
        "-" * len(header),
        "* ipTM columns are informational only (AUC 0.52 on Adaptyv N=2600); "
        "cross-val decision uses SC AND ipSAE_min. See notes/calibration.md.",
    ]
    for r in sorted(results, key=lambda x: -(x.get("composite_rank") or 0)):
        lines.append(
            f"{r['design_id']:30s} {fmt(r['sc'], 3):>6s} {(r['sc_source'] or ''):>16s} "
            f"{fmt(r['ipsae_min']):>10s} {fmt(r['composite_rank']):>10s} "
            f"{fmt(r['boltz_iptm']):>12s} {fmt(r['af2_iptm']):>10s} "
            f"{_yn(r['sc_pass']):>8s} {_yn(r['ipsae_pass']):>11s} {_yn(r['cross_val_pass']):>9s}"
        )
    return "\n".join(lines)


def _find_accepted_designs(target):
    """Walk this target's tree on the adaptyv-designs volume for accepted
    design PDBs. Returns list of (design_id, pdb_path). Runs inside a Modal
    function (needs the mount)."""
    import os

    root = f"/designs/{target}/attempts"
    found = []
    for dirpath, _, files in os.walk(root):
        if os.path.basename(dirpath) != "Accepted":
            continue
        for f in sorted(files):
            if f.endswith(".pdb"):
                design_id = f.rsplit("_model", 1)[0]
                found.append((design_id, os.path.join(dirpath, f)))
    return found


@app.function(image=image, volumes={"/designs": designs}, timeout=600)
def list_accepted(target: str):
    return _find_accepted_designs(target)


# --------------------------------------------------------------------------- #
# CPU-only rescore of already-run designs (no Boltz, no GPU)
# --------------------------------------------------------------------------- #

@app.function(image=image, volumes={"/designs": designs}, timeout=600)
def rescore_one(design_id: str, pdb_path: str):
    """Re-score a design from its saved boltz_crossval/ files (pae/plddt/conf).
    Skipped with a clear reason if the earlier run did not persist the arrays."""
    import glob
    import json
    import os

    design_dir = os.path.dirname(os.path.dirname(pdb_path))
    save_dir = os.path.join(design_dir, "boltz_crossval")

    if not (glob.glob(os.path.join(save_dir, "pae_*_model_0.npz"))
            and glob.glob(os.path.join(save_dir, "confidence_*_model_0.json"))):
        return {
            "design_id": design_id,
            "error": "cached boltz outputs missing (rerun crossval_boltz on GPU once "
                     "to populate save_dir with pae/plddt/confidence files)",
        }

    sc_info = _get_sc(design_dir, pdb_path)
    result, _ = _score_from_boltz_outputs(design_id, pdb_path, save_dir, sc_info)

    with open(os.path.join(save_dir, "crossval_result.json"), "w") as fh:
        json.dump(result, fh, indent=2)
    designs.commit()
    return result


@app.local_entrypoint()
def rescore_saved(target: str, smoke: bool = False, smoke_design_id: str = None):
    """CPU-only rescore of a target's accepted shortlist from cached Boltz outputs.

    Use after a change to scoring thresholds or the ipSAE math -- no Boltz
    re-prediction, no GPU. Designs whose earlier run didn't save PAE/pLDDT
    arrays are reported as skipped rather than silently missing.

    --target is required (e.g. "vegf") and must match the slug run_bindcraft.py
    was given via --target, since that's what namespaces /designs/<target>/.
    """
    accepted = list_accepted.remote(target)
    if not accepted:
        print(f"no accepted designs found for target={target!r}; nothing to rescore")
        return

    if smoke:
        shortlist = (
            ([d for d in accepted if d[0] == smoke_design_id][:1] if smoke_design_id else [])
            or accepted[:1]
        )
        print(f"SMOKE rescore: {shortlist[0][0]}")
    else:
        shortlist = accepted
        print(f"rescoring {len(shortlist)} designs for target={target!r}")

    results = list(rescore_one.starmap(shortlist, return_exceptions=True))
    ok, skipped, errors = [], [], []
    for spec, r in zip(shortlist, results):
        if isinstance(r, Exception):
            errors.append((spec[0], repr(r)))
        elif isinstance(r, dict) and r.get("error"):
            skipped.append((spec[0], r["error"]))
        else:
            ok.append(r)

    print("\n=== Boltz cross-validation (rescore) ===")
    if ok:
        print(_consensus_table(ok))
    for did, msg in skipped:
        print(f"  SKIP {did}: {msg}")
    for did, err in errors:
        print(f"  ERROR {did}: {err}")

    _write_outputs(target, ok, errors, smoke=smoke, skipped=skipped, mode="rescore")


@app.local_entrypoint()
def main(target: str, smoke: bool = False, smoke_design_id: str = None):
    """Run Boltz cross-validation on a target's accepted shortlist (GPU).

    --target is required (e.g. "vegf") and must match the slug run_bindcraft.py
    was given via --target. --smoke restricts the run to one design: pass
    --smoke-design-id to pin a specific one, otherwise any one accepted design
    for this target is used.
    """
    print("ensuring Boltz weights ...")
    download_boltz_weights.remote()

    accepted = list_accepted.remote(target)
    if not accepted:
        print(f"no accepted designs found for target={target!r}; nothing to cross-validate")
        return

    if smoke:
        shortlist = (
            ([d for d in accepted if d[0] == smoke_design_id][:1] if smoke_design_id else [])
            or accepted[:1]
        )
        print(f"SMOKE mode: 1 design -> {shortlist[0][0]}")
    else:
        shortlist = accepted
        print(f"full run: {len(shortlist)} accepted designs for target={target!r}")

    results = list(crossval_boltz.starmap(shortlist, return_exceptions=True))

    ok, errors = [], []
    for spec, r in zip(shortlist, results):
        if isinstance(r, Exception):
            errors.append((spec[0], repr(r)))
        else:
            ok.append(r)

    print("\n=== Boltz cross-validation ===")
    if ok:
        print(_consensus_table(ok))
    for did, err in errors:
        print(f"  ERROR {did}: {err}")

    _write_outputs(target, ok, errors, smoke=smoke)


@app.function(image=image, volumes={"/designs": designs}, timeout=600)
def _persist_table(target: str, csv_text: str, md_text: str, filename_prefix: str = "crossval"):
    import os
    out_dir = f"/designs/{target}/redundancy"
    os.makedirs(out_dir, exist_ok=True)
    csv_path = f"{out_dir}/{filename_prefix}.csv"
    md_path = f"{out_dir}/{filename_prefix}_methods_block.md"
    with open(csv_path, "w") as fh:
        fh.write(csv_text)
    with open(md_path, "w") as fh:
        fh.write(md_text)
    designs.commit()
    return csv_path


def _write_outputs(target, ok, errors, smoke, skipped=None, mode="run"):
    """Persist a CSV + methods.md-appendable markdown block."""
    import csv
    import io

    skipped = skipped or []

    buf = io.StringIO()
    w = csv.writer(buf)
    # Decision columns first (SC, ipSAE_min, cross_val_pass), then informational.
    w.writerow([
        "design_id",
        "SC", "SC_source", "SC_pass",
        "ipSAE_min", "ipSAE_pass",
        "cross_val_pass", "composite_rank",
        # informational -- do NOT use for decisions:
        "Boltz_ipTM_info", "AF2_ipTM_info", "AF2_ipAE_info",
        "Boltz_pLDDT", "Boltz_ipAE_A", "Boltz_ipAE_norm",
    ])
    for r in sorted(ok, key=lambda x: -(x.get("composite_rank") or 0)):
        w.writerow([
            r["design_id"],
            r["sc"], r["sc_source"], _yn(r["sc_pass"]),
            r["ipsae_min"], _yn(r["ipsae_pass"]),
            _yn(r["cross_val_pass"]), r["composite_rank"],
            r["boltz_iptm"], r["af2_iptm"], r["af2_ipae"],
            r["boltz_plddt"], r["boltz_ipae_A"], r["boltz_ipae_norm"],
        ])

    n_pass = sum(1 for r in ok if r["cross_val_pass"])
    n_sc_pass = sum(1 for r in ok if r["sc_pass"])
    n_ipsae_pass = sum(1 for r in ok if r["ipsae_pass"])
    tag = " (SMOKE, 1 design)" if smoke else ""
    if mode == "rescore":
        tag = f"{tag} [rescore, CPU-only]" if tag else " [rescore, CPU-only]"

    md = [
        f"## {target} — Boltz cross-validation{tag}",
        "Second model: Boltz-2. Decision metrics (calibrated on Adaptyv N~2600 + bioRxiv",
        "2025.08.14.670059): shape complementarity as PRE-FILTER, then ipSAE_min (Dunbrack",
        f"2025) as PRIMARY RANK metric. Thresholds: SC >= {SC_PASS}, ipSAE_min >= {IPSAE_MIN_PASS}.",
        "ipTM is INFORMATIONAL only (AUC 0.52 on Adaptyv, does not predict real binding).",
        "See notes/calibration.md for AUCs, thresholds, and sources.",
        f"SC pass: {n_sc_pass}/{len(ok)}. ipSAE_min pass: {n_ipsae_pass}/{len(ok)}. "
        f"cross_val_pass (both): {n_pass}/{len(ok)}"
        + (f"; {len(errors)} errored" if errors else "")
        + (f"; {len(skipped)} skipped" if skipped else "")
        + ".",
        "Ranked by composite = ipsae_min * min(SC/SC_PASS, 1.0).",
        "",
        "```",
        _consensus_table(ok) if ok else "(no successful predictions)",
        "```",
    ]
    md_text = "\n".join(md) + "\n"

    prefix = "crossval_rescore" if mode == "rescore" else "crossval"
    path = _persist_table.remote(target, buf.getvalue(), md_text, prefix)
    print(f"\nwrote cross-validation table to {path} (on adaptyv-designs volume)")
    print("\n--- methods.md-appendable block ---\n" + md_text)


# --------------------------------------------------------------------------- #
# Full-length co-fold: re-predict a binder against an arbitrary target SEQUENCE
# --------------------------------------------------------------------------- #
# crossval_boltz() takes its target from the design PDB, so it can only ever
# re-predict against whatever target the design was made on. When a design was
# built against a SLICED target (see run_bindcraft.py --target-residue-range),
# the honest check is a co-fold against the untruncated receptor: the slice's
# cut faces are artificial exposed surface a binder can score well against.
# These entrypoints take the target as an explicit sequence so that check is
# possible without touching the design-time path.

# pyrosetta is not in `image`, and the burial-fraction proxy in _compute_sc_proxy
# is NOT Lawrence-Colman SC, so it cannot be compared to SC_PASS. This image adds
# pyrosetta so the real ShapeComplementarityFilter value is available.
sc_image = (
    modal.Image.debian_slim(python_version="3.11")
    .apt_install("wget")
    .pip_install("biopython", "numpy<2")
    .pip_install(
        "pyrosetta",
        find_links="https://west.rosettacommons.org/pyrosetta/quarterly/release.cxx11thread.serialization",
    )
)


@app.function(
    gpu="A100-40GB",
    image=image,
    volumes={"/designs": designs, BOLTZ_CACHE: boltz_weights},
    timeout=7200,
)
def cofold_seqs(run_id: str, target_seq: str, binder_seq: str, save_rel: str):
    """Co-fold `binder_seq` against `target_seq` with Boltz-2; score iPTM + ipSAE_min.

    Args:
      run_id: label for logs and the output filenames.
      target_seq: the target chain, as one gapless sequence -> Boltz chain A.
      binder_seq: the binder -> Boltz chain B.
      save_rel: path under /designs to persist the predicted PDB + arrays to,
        so SC/contacts can be scored later on CPU without re-paying for a GPU.

    Returns the metric dict. SC is deliberately NOT computed here (no pyrosetta
    in this image) -- sc_and_contacts() does that on the persisted PDB.
    """
    import glob
    import json
    import os
    import shutil
    import subprocess

    import yaml

    os.environ["BOLTZ_CACHE"] = BOLTZ_CACHE

    yaml_doc = {"version": 1, "sequences": [
        {"protein": {"id": "A", "sequence": target_seq}},
        {"protein": {"id": "B", "sequence": binder_seq}},
    ]}
    work = f"/tmp/{run_id}"
    os.makedirs(work, exist_ok=True)
    yaml_path = f"{work}/{run_id}.yaml"
    with open(yaml_path, "w") as fh:
        yaml.safe_dump(yaml_doc, fh, sort_keys=False)
    print(f"{run_id}: target {len(target_seq)} aa (chain A), binder {len(binder_seq)} aa (chain B)")

    out_dir = f"{work}/out"
    cmd = [
        "boltz", "predict", yaml_path,
        "--out_dir", out_dir,
        "--cache", BOLTZ_CACHE,
        "--use_msa_server",
        "--write_full_pae",
        "--accelerator", "gpu",
        "--devices", "1",
        "--override",
        "--output_format", "pdb",
    ]
    print("running:", " ".join(cmd))
    subprocess.run(cmd, check=True, env={**os.environ, "BOLTZ_CACHE": BOLTZ_CACHE})

    pae, plddt, conf, pred_dir = _load_boltz_arrays(out_dir)
    n_expected = len(target_seq) + len(binder_seq)
    if pae.shape[0] != n_expected:
        raise RuntimeError(
            f"PAE dim {pae.shape[0]} != {n_expected} (target+binder); token order unexpected"
        )

    slices = _chain_slices_for([target_seq], binder_seq)
    ipsae = _compute_ipsae(pae, plddt, slices)
    iptm = float(conf["iptm"]) if conf.get("iptm") is not None else None

    save_dir = f"/designs/{save_rel}"
    os.makedirs(save_dir, exist_ok=True)
    saved_pdb = None
    for f in os.listdir(pred_dir):
        if f.endswith(".pdb") or f.startswith("confidence_"):
            dst = os.path.join(save_dir, f)
            shutil.copy(os.path.join(pred_dir, f), dst)
            if f.endswith(".pdb"):
                saved_pdb = dst
    for pattern in ("pae_*_model_0.npz", "plddt_*_model_0.npz"):
        for src in glob.glob(os.path.join(out_dir, "**", pattern), recursive=True):
            shutil.copy(src, os.path.join(save_dir, os.path.basename(src)))

    result = {
        "run_id": run_id,
        "target_len": len(target_seq),
        "binder_len": len(binder_seq),
        "iptm": round(iptm, 4) if iptm is not None else None,
        "ptm": round(float(conf["ptm"]), 4) if conf.get("ptm") is not None else None,
        "complex_plddt": (round(float(conf["complex_plddt"]), 4)
                          if conf.get("complex_plddt") is not None else None),
        "ipsae_min": ipsae["ipsae_min"],
        "ipsae_pass": (ipsae["ipsae_min"] is not None
                       and ipsae["ipsae_min"] >= IPSAE_MIN_PASS),
        "ipsae_pairs": ipsae["pairs"],
        "saved_pdb": saved_pdb,
    }
    with open(os.path.join(save_dir, "cofold_result.json"), "w") as fh:
        json.dump(result, fh, indent=2)
    designs.commit()
    print("RESULT:", json.dumps({k: v for k, v in result.items() if k != "ipsae_pairs"}))
    return result


@app.function(image=sc_image, volumes={"/designs": designs}, timeout=1800)
def sc_and_contacts(
    run_id: str,
    pdb_rel: str,
    resnum_offset: int,
    hotspots: str,
    contact_cutoff: float = 4.5,
):
    """Real pyrosetta SC + any-atom interface contacts on a co-folded complex.

    Args:
      pdb_rel: path under /designs to the predicted complex (chain A target,
        chain B binder).
      resnum_offset: added to chain A's residue numbers to report them in the
        caller's numbering scheme (e.g. +24 to turn a target chain that starts
        at EGFR precursor 25 into precursor numbering).
      hotspots: comma-separated intended hotspots, already in the OUTPUT
        numbering scheme, checked for contact.
      contact_cutoff: any-atom heavy-atom distance in angstroms.
    """
    import json
    import os

    import pyrosetta
    from Bio.PDB import NeighborSearch, PDBParser
    from Bio.PDB.Polypeptide import protein_letters_3to1 as t31

    pdb = f"/designs/{pdb_rel}"
    if not os.path.exists(pdb):
        raise RuntimeError(f"no such pdb on volume: {pdb}")

    # --- real Lawrence-Colman SC across the A|B interface --------------------
    pyrosetta.init("-mute all -ignore_unrecognized_res", silent=True)
    pose = pyrosetta.pose_from_pdb(pdb)
    sc_filter = pyrosetta.rosetta.protocols.simple_filters.ShapeComplementarityFilter()
    sc_filter.jump_id(1)
    sc_filter.quick(False)
    try:
        sc = float(sc_filter.score(pose))
    except Exception as e:
        print(f"[warn] SC filter failed: {e}")
        sc = None

    # --- interface contacts --------------------------------------------------
    model = PDBParser(QUIET=True).get_structure("cx", pdb)[0]
    tgt_atoms = [a for a in model["A"].get_atoms()
                 if a.get_parent().id[0] == " " and a.element != "H"]
    bnd_atoms = [a for a in model["B"].get_atoms()
                 if a.get_parent().id[0] == " " and a.element != "H"]
    ns = NeighborSearch(tgt_atoms)
    contacts = {}
    for a in bnd_atoms:
        for t in ns.search(a.coord, contact_cutoff):
            r = t.get_parent()
            num = r.id[1] + resnum_offset
            contacts.setdefault(num, t31.get(r.get_resname(), "X"))

    hot = [int(h) for h in hotspots.split(",") if h.strip()]
    recovered = [h for h in hot if h in contacts]
    result = {
        "run_id": run_id,
        "sc": round(sc, 4) if sc is not None else None,
        "sc_source": "pyrosetta_ShapeComplementarityFilter",
        "sc_pass": (sc is not None and sc >= SC_PASS),
        "n_interface_residues": len(contacts),
        "interface_residues": {str(k): contacts[k] for k in sorted(contacts)},
        "hotspots_checked": hot,
        "hotspots_recovered": recovered,
        "hotspot_recovery": f"{len(recovered)}/{len(hot)}",
    }
    print("SC/CONTACTS:", json.dumps(
        {k: v for k, v in result.items() if k != "interface_residues"}))
    return result


@app.local_entrypoint()
def fulllength_check(
    target_fasta: str,
    binders_fasta: str,
    hotspots: str,
    resnum_offset: int = 0,
    save_prefix: str = "fulllength",
):
    """Co-fold every binder in `binders_fasta` against the single target in
    `target_fasta`, then report iPTM / ipSAE_min / SC / hotspot recovery.

    --resnum-offset shifts chain A's residue numbers into the numbering scheme
    --hotspots is written in (the target sequence is fed to Boltz gaplessly, so
    chain A always comes back numbered from 1).

    Example:
      modal run --detach modal/redundancy.py::fulllength_check \\
        --target-fasta /tmp/egfr_25_645.fasta \\
        --binders-fasta /tmp/binders.fasta \\
        --hotspots 408,432,433,435,436,489,490 --resnum-offset 24 \\
        --save-prefix egfr/fulllength
    """
    import json

    def read_fasta(p):
        recs, name, buf = [], None, []
        for line in open(p):
            line = line.strip()
            if line.startswith(">"):
                if name:
                    recs.append((name, "".join(buf)))
                name, buf = line[1:].split()[0], []
            elif line:
                buf.append(line)
        if name:
            recs.append((name, "".join(buf)))
        return recs

    tgt = read_fasta(target_fasta)
    if len(tgt) != 1:
        raise SystemExit(f"--target-fasta must hold exactly one record, got {len(tgt)}")
    target_name, target_seq = tgt[0]
    bnds = read_fasta(binders_fasta)
    print(f"target {target_name}: {len(target_seq)} aa")
    for n, s in bnds:
        print(f"  binder {n}: {len(s)} aa")

    folds = list(cofold_seqs.starmap(
        [(n, target_seq, s, f"{save_prefix}/{n}") for n, s in bnds],
        order_outputs=True,
    ))

    scored = list(sc_and_contacts.starmap(
        [(f["run_id"], f["saved_pdb"].replace("/designs/", ""), resnum_offset, hotspots)
         for f in folds if f.get("saved_pdb")],
        order_outputs=True,
    ))
    by_id = {s["run_id"]: s for s in scored}

    print("\n" + "=" * 72)
    print(f"FULL-LENGTH CO-FOLD vs {target_name} ({len(target_seq)} aa)")
    print(f"thresholds: ipSAE_min >= {IPSAE_MIN_PASS}, SC >= {SC_PASS} (ipTM informational)")
    print("=" * 72)
    for f in folds:
        s = by_id.get(f["run_id"], {})
        print(f"\n--- {f['run_id']} (binder {f['binder_len']} aa) ---")
        print(f"  iPTM               {f['iptm']}   (informational)")
        print(f"  ipSAE_min          {f['ipsae_min']}   pass={f['ipsae_pass']}")
        print(f"  SC                 {s.get('sc')}   pass={s.get('sc_pass')}  [{s.get('sc_source')}]")
        print(f"  complex pLDDT      {f['complex_plddt']}")
        print(f"  interface residues {s.get('n_interface_residues')}")
        print(f"  hotspot recovery   {s.get('hotspot_recovery')}  "
              f"recovered={s.get('hotspots_recovered')}")
        print(f"  ipsae pairs: {json.dumps(f['ipsae_pairs'])}")
        if s.get("interface_residues"):
            ir = s["interface_residues"]
            print("  interface: " + ", ".join(f"{k}{v}" for k, v in ir.items()))
    return {"folds": folds, "scored": scored}
