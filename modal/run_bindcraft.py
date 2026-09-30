"""run_bindcraft.py -- target-agnostic parallel BindCraft on Modal.

Each `main` invocation designs binders against ONE target (--target <slug>).
The target's identity + PDB + chains + hotspots are supplied at the CLI --
this file has no per-target constants, so a new challenge is a new
--target/--pdb-id/--target-chains/--hotspots combination, not a code edit.

Output convention on the `adaptyv-designs` volume:
    /designs/<target-slug>/attempts/<run-tag>/<seed>/    (BindCraft's own tree)
    /designs/<target-slug>/targets/<target-slug>.pdb     (cleaned target copy)

Weights volumes (af2-weights, boltz-weights) are shared across challenges and
NOT prefixed by target, so alphafold params download once for the account.
"""
import modal

app = modal.App("adaptyv-binders")
weights = modal.Volume.from_name("af2-weights", create_if_missing=True)
designs = modal.Volume.from_name("adaptyv-designs", create_if_missing=True)

# Image: mirrors BindCraft's Colab install, on a controlled Python 3.11
image = (
    modal.Image.debian_slim(python_version="3.11")
    # ffmpeg: ColabDesign's animate() ends in to_html5_video(), which shells out
    # to the ffmpeg binary. Without it every trajectory dies after the design work
    # is done but before its stats row is written.
    .apt_install("git", "wget", "aria2", "dssp", "ffmpeg")
    .run_commands(
        "git clone https://github.com/martinpacesa/BindCraft /opt/bindcraft",
        "chmod +x /opt/bindcraft/functions/dssp || true",
        "chmod +x /opt/bindcraft/functions/DAlphaBall.gcc || true",
    )
    # jax, colabdesign and numpy resolve together so ColabDesign can't upgrade
    # jax past the CUDA 12 plugin that ships with 0.4.35
    .pip_install(
        "jax[cuda12]==0.4.35",
        "colabdesign @ git+https://github.com/sokrypton/ColabDesign.git",
        "numpy<2",
        # 12.9.x ships as a namespace package (__file__ is None), which breaks
        # jax 0.4.35's CUDA path probe at import time
        "nvidia-cuda-nvcc-cu12==12.6.85",
        # 0.0.17 needs jax.core APIs that don't exist in 0.4.35
        "dm-haiku==0.0.13",
    )
    # matplotlib 3.9 removed cm.get_cmap (deprecated in 3.7); ColabDesign's
    # shared/plot.py still calls it, so animate() dies mid-trajectory and the
    # run loses an otherwise-good design before its stats row is written
    .pip_install("biopython", "pandas", "scipy", "matplotlib<3.9")
    .pip_install(
        "pyrosetta",
        find_links="https://west.rosettacommons.org/pyrosetta/quarterly/release.cxx11thread.serialization",
    )
)

AF2_PARAMS_URL = (
    "https://storage.googleapis.com/alphafold/alphafold_params_2022-12-06.tar"
)


@app.function(image=image, volumes={"/weights": weights}, timeout=3600)
def download_weights():
    import os
    import subprocess

    done = "/weights/params/done.txt"
    if os.path.exists(done):
        print("already present")
        return

    os.makedirs("/weights/params", exist_ok=True)
    tar_path = "/weights/alphafold_params_2022-12-06.tar"

    subprocess.run(
        ["aria2c", "-x", "16", "-d", "/weights", AF2_PARAMS_URL],
        check=True,
    )
    subprocess.run(
        ["tar", "-xf", tar_path, "-C", "/weights/params"],
        check=True,
    )

    open(done, "w").close()
    os.remove(tar_path)

    print(subprocess.run(["ls", "-la", "/weights/params"], capture_output=True, text=True).stdout)
    weights.commit()
    print("weights committed")


@app.function(gpu="T4", image=image, volumes={"/weights": weights}, timeout=1800)
def verify():
    import subprocess, jax
    print("JAX devices:", jax.devices())
    import colabdesign; print("colabdesign import OK")
    try:
        import pyrosetta; print("pyrosetta import OK")
    except Exception as e:
        print("pyrosetta FAILED:", e)
    print(subprocess.run(["ls", "/opt/bindcraft"], capture_output=True, text=True).stdout)


# Advanced-settings preset. _hardtarget == plain default + predict_initial_guess:
# True (the MPNN complex is re-predicted from the trajectory's docked pose rather
# than from scratch) -- the recommended mode for hard targets. It was adopted
# after VEGF runs (0 accepted in plain-default sweeps) but the rationale is
# target-agnostic; override with --advanced-preset default_4stage_multimer for
# easier targets.
DEFAULT_ADVANCED_PRESET = "default_4stage_multimer_hardtarget"

# Binder length range [min, max]. 60-180 is a reasonable default for hard-target
# mode (longer binders can wrap more interface); tighten for specific targets.
DEFAULT_LENGTHS = "60,180"

# af_params_dir is handed to ColabDesign as data_dir, and ColabDesign does
# os.path.join(data_dir, "params") -- so it is the PARENT of params/, not params/ itself.
AF_PARAMS_DIR = "/weights"

# Leave room inside the 3600s function timeout to commit partial results:
# a hard timeout kills the container before anything is persisted.
DESIGN_BUDGET_S = 3300

# Launcher that monkey-patches BindCraft's predict_binder_complex() to log the
# post-MPNN AF2 re-prediction metrics (i_pTM / i_pAE / pLDDT / pTM / pAE) for
# EVERY redesigned sequence -- pass or fail -- to a CSV on the /designs volume.
#
# Why a launcher rather than editing the library: BindCraft/ColabDesign live at
# /opt/bindcraft, baked into the image, and vanish on every image rebuild. This
# script is written to /tmp at runtime from THIS file and wraps the function at
# import time, so the patch survives rebuilds and never touches library files.
#
# Why it must run in the subprocess (not design_one's process): design_one runs
# bindcraft.py as a subprocess, so a monkey-patch applied in design_one's own
# process would not reach it. The launcher IS the subprocess entrypoint: it
# imports `functions`, replaces functions.predict_binder_complex with a logging
# wrapper, THEN runpy's bindcraft.py -- whose `from functions import *` binds the
# wrapper (functions/__init__.py re-exports the name; the only call site,
# bindcraft.py, calls it unqualified). BindCraft never saves raw metrics for a
# failed candidate (only pass/fail tallies), which is exactly the missing signal.
PATCHED_LAUNCHER = r'''
import os, sys, csv, time

# The launcher lives in /tmp, so /opt/bindcraft is not on sys.path by default.
sys.path.insert(0, "/opt/bindcraft")

import functions  # triggers `from .colabdesign_utils import *`, defining functions.predict_binder_complex

_orig_predict_binder_complex = functions.predict_binder_complex


def _logged_predict_binder_complex(*args, **kwargs):
    # Run the real function untouched, then log whatever it computed.
    result = _orig_predict_binder_complex(*args, **kwargs)
    try:
        prediction_stats, pass_af2 = result
        # Call site is all-positional: mpnn_design_name is arg 3, design_paths arg 11.
        mpnn_design_name = args[2] if len(args) > 2 else kwargs.get("mpnn_design_name")
        design_paths = args[10] if len(args) > 10 else kwargs.get("design_paths")
        # design_paths["MPNN"] == <design_path>/MPNN, so its parent is the run dir.
        design_path = os.path.dirname(design_paths["MPNN"])
        log_csv = os.path.join(design_path, "mpnn_reprediction_log.csv")
        write_header = not os.path.exists(log_csv)
        with open(log_csv, "a", newline="") as fh:
            w = csv.writer(fh)
            if write_header:
                w.writerow(["timestamp", "mpnn_design_name", "model",
                            "pLDDT", "pTM", "i_pTM", "pAE", "i_pAE",
                            "pass_af2_filters"])
            ts = time.strftime("%Y-%m-%dT%H:%M:%S")
            # prediction_stats == {model_num: {pLDDT,pTM,i_pTM,pAE,i_pAE}}. It may
            # hold fewer models than requested: the real function breaks after the
            # first model that fails, so we log exactly what was actually scored.
            for model_num, s in sorted(prediction_stats.items()):
                w.writerow([ts, mpnn_design_name, model_num,
                            s.get("pLDDT"), s.get("pTM"), s.get("i_pTM"),
                            s.get("pAE"), s.get("i_pAE"), pass_af2])
    except Exception as e:  # logging must NEVER break a design run
        print("[mpnn-log] WARNING: failed to log re-prediction stats:", e, flush=True)
    return result


functions.predict_binder_complex = _logged_predict_binder_complex

import runpy
# run_name="__main__" so bindcraft.py executes its top-level design loop; its
# `from functions import *` now binds the wrapper above.
runpy.run_path("/opt/bindcraft/bindcraft.py", run_name="__main__")
'''


@app.function(
    gpu="A10G",
    image=image,
    volumes={"/weights": weights, "/designs": designs},
    timeout=3600,
)
def design_one(
    seed: int,
    target: str,
    pdb_id: str,
    target_chains: str,
    hotspots: str,
    i_ptm_threshold: float = 0.0,
    run_tag: str = "default",
    advanced_preset: str = DEFAULT_ADVANCED_PRESET,
    lengths: str = DEFAULT_LENGTHS,
    target_residue_range: str = "",
):
    """Run exactly one BindCraft trajectory attempt against `target`.

    Args:
      seed: identifies this call (used to give it a private design_path so
        parallel workers never write to the same file on the shared volume --
        BindCraft's own CSV writers do a naive read/append/write with no
        locking, so concurrent commits from multiple containers to one path
        lose rows).
      target: challenge slug used to namespace outputs on the volume. Every
        artifact for this challenge lives under /designs/<target>/.
      pdb_id: either a 4-char RCSB code (fetched at runtime) or a URL. The
        current implementation assumes RCSB.
      target_chains: comma-separated chain IDs to keep from the source PDB
        (e.g. "V,W" for the VEGF dimer in 1FLT). Everything else is stripped.
      target_residue_range: optional "START-END" of author residue numbers
        (e.g. "311-514") to keep from every kept chain. AF2 memory scales
        ~N^2, so a full receptor ECD can OOM an A10G -- slicing to the one
        domain the hotspots sit in is what makes the run fit.
      hotspots: comma-separated chain-prefixed hotspot residues in
        ColabDesign's prep_pos() format (e.g. "V21,V25,V48"). Must all be
        present in the cleaned target; a missing hotspot fails fast.
      run_tag: namespaces the design_path further so two differently-configured
        sweeps (different hotspots/thresholds) never collide even if they
        reuse the same seed range.
      advanced_preset: settings_advanced/<preset>.json BindCraft ships.
        Default is the _hardtarget preset (predict_initial_guess: True).
      lengths: "min,max" for the binder length range.
      i_ptm_threshold: 0.0 (default) means DO NOT touch the filters -- run
        BindCraft's stock default_filters.json unchanged. A positive value
        overrides Average_/1_/2_i_pTM to that value.

    BindCraft has no CLI hook for an external RNG seed (only
    --settings/--filters/--advanced; the trajectory's own seed and length are
    drawn internally). `seed` is not wired into that -- it's this call's
    identity, not BindCraft's hallucination seed. The real internal seed is
    recorded in the trajectory row.

    "One trajectory per call" is enforced via advanced_settings["max_trajectories"]
    = 1: BindCraft's loop stops as soon as one trajectory reaches the Relaxed
    stage (i.e. gets a trajectory_stats.csv row and one MPNN pass), whether or
    not that MPNN pass yields an accepted design.
    """
    import json
    import os
    import subprocess
    import time
    import urllib.request

    t0 = time.time()

    from Bio.PDB import PDBIO, PDBParser, Select

    keep_chains = tuple(c.strip() for c in target_chains.split(",") if c.strip())
    if not keep_chains:
        raise RuntimeError(f"--target-chains yielded no chains: {target_chains!r}")

    res_lo, res_hi = None, None
    if target_residue_range:
        res_lo, res_hi = (int(x) for x in target_residue_range.split("-"))

    design_path = f"/designs/{target}/attempts/{run_tag}/{seed}"
    targets_dir = f"/designs/{target}/targets"
    os.makedirs(design_path, exist_ok=True)
    os.makedirs(targets_dir, exist_ok=True)

    # --- prepare the target -------------------------------------------------
    raw_pdb = f"/tmp/{pdb_id}.pdb"
    urllib.request.urlretrieve(
        f"https://files.rcsb.org/download/{pdb_id}.pdb", raw_pdb
    )

    class ChainSelect(Select):
        def accept_chain(self, chain):
            return chain.id in keep_chains

        def accept_residue(self, residue):
            # drop waters and heteroatoms, keep standard residues
            if residue.id[0] != " ":
                return False
            if res_lo is not None and not (res_lo <= residue.id[1] <= res_hi):
                return False
            return True

    structure = PDBParser(QUIET=True).get_structure(pdb_id, raw_pdb)
    io = PDBIO()
    io.set_structure(structure)
    target_pdb = os.path.join(design_path, f"{target}.pdb")
    io.save(target_pdb, ChainSelect())
    # keep a copy outside the design dir so the cleaned target survives re-runs
    io.save(os.path.join(targets_dir, f"{target}.pdb"), ChainSelect())

    kept = PDBParser(QUIET=True).get_structure(target, target_pdb)[0]
    print(f"target {target_pdb}: chains " + ", ".join(
        f"{c.id}={len(list(c.get_residues()))}res" for c in kept
    ))

    # fail fast if a hotspot does not exist -- cheaper than an hour of GPU
    present = {f"{c.id}{r.id[1]}" for c in kept for r in c}
    missing = [h for h in hotspots.split(",") if h not in present]
    if missing:
        raise RuntimeError(f"hotspots not found in target: {missing}")
    print(f"hotspots OK: {hotspots}")

    length_min, length_max = (int(x) for x in lengths.split(","))

    # --- settings JSON ------------------------------------------------------
    # Schema mirrors BindCraft's settings_target/PDL1.json exactly. The file's
    # basename is what BindCraft prints as the target name.
    settings = {
        "design_path": design_path,
        "binder_name": target,
        "starting_pdb": target_pdb,
        "chains": ",".join(keep_chains),
        "target_hotspot_residues": hotspots,
        "lengths": [length_min, length_max],
        "number_of_final_designs": 1,
    }
    settings_json = f"/tmp/{target}_{seed}.json"
    with open(settings_json, "w") as fh:
        json.dump(settings, fh, indent=4)
    print("settings:", json.dumps(settings, indent=4))

    # Filters + advanced preset, with af_params_dir pointed at the weights volume.
    bc = "/opt/bindcraft"
    filters_src = f"{bc}/settings_filters/default_filters.json"
    advanced_src = f"{bc}/settings_advanced/{advanced_preset}.json"
    if not os.path.exists(advanced_src):
        raise RuntimeError(f"advanced preset not found: {advanced_src}")

    if i_ptm_threshold and i_ptm_threshold > 0:
        # Relaxed-filter mode: override the three i_pTM keys BindCraft checks.
        with open(filters_src) as fh:
            filters = json.load(fh)
        for key in ("Average_i_pTM", "1_i_pTM", "2_i_pTM"):
            filters[key]["threshold"] = i_ptm_threshold
        filters_json = f"/tmp/filters_{seed}.json"
        with open(filters_json, "w") as fh:
            json.dump(filters, fh, indent=4)
        print(f"filters: relaxed i_pTM -> {i_ptm_threshold} (Average_/1_/2_)")
    else:
        # Default-filter mode (i_ptm_threshold == 0): use BindCraft's stock file
        # unchanged -- no relaxation. This is the hard-target config's setting.
        filters_json = filters_src
        print("filters: BindCraft default_filters.json, unchanged")

    with open(advanced_src) as fh:
        advanced = json.load(fh)
    advanced["af_params_dir"] = AF_PARAMS_DIR
    # Cosmetic HTML animation of the hallucination trajectory. It runs inside
    # binder_hallucination() *before* the stats row is written, so any failure
    # there discards a finished design -- it killed two runs already. Off.
    advanced["save_design_animations"] = False
    # Same story: plot_trajectory() also runs before the stats row is written.
    # (Key is save_design_trajectory_plots, not save_trajectory_pics.)
    advanced["save_design_trajectory_plots"] = False
    # check_n_trajectories() counts files in Trajectory/Relaxed/, which only
    # get written by a trajectory that clears the initial confidence gate.
    # This is what makes the call stop after exactly one such trajectory.
    advanced["max_trajectories"] = 1
    advanced_json = f"/tmp/advanced_{seed}.json"
    with open(advanced_json, "w") as fh:
        json.dump(advanced, fh, indent=4)

    # --- run ----------------------------------------------------------------
    # Run bindcraft.py through the monkey-patch launcher (see PATCHED_LAUNCHER)
    # so post-MPNN re-prediction metrics get logged. cwd stays /opt/bindcraft so
    # bindcraft.py's relative paths resolve exactly as before; the timeout +
    # commit-partial behaviour is unchanged (the launcher is just the entrypoint).
    launcher = f"/tmp/patched_run_{seed}.py"
    with open(launcher, "w") as fh:
        fh.write(PATCHED_LAUNCHER)

    timed_out = False
    try:
        subprocess.run(
            ["python", launcher,
             "--settings", settings_json,
             "--filters", filters_json,
             "--advanced", advanced_json],
            cwd=bc,
            check=True,
            timeout=DESIGN_BUDGET_S,
            env={**os.environ, "PYTHONUNBUFFERED": "1"},
        )
    except subprocess.TimeoutExpired:
        timed_out = True
        print(f"\n!! hit the {DESIGN_BUDGET_S}s budget -- committing partial results")
    finally:
        designs.commit()

    # --- report ---------------------------------------------------------
    # Only this worker's own private tree -- with N parallel workers on a
    # shared volume, walking all of /designs here would print every other
    # worker's files too (whatever the snapshot happened to catch).
    print(f"\n=== files under {design_path} ===")
    for root, _, files in os.walk(design_path):
        for f in sorted(files):
            p = os.path.join(root, f)
            print(f"  {p}  ({os.path.getsize(p)} bytes)")

    import pandas as pd

    def first_row_or_none(name):
        p = os.path.join(design_path, name)
        if not os.path.exists(p):
            return None
        df = pd.read_csv(p)
        print(f"\n=== {name} ({len(df)} rows) ===")
        if len(df):
            with pd.option_context("display.max_columns", None, "display.width", 250):
                print(df.to_string())
            # max_trajectories=1 caps this at one row; take it as a plain dict
            # so the launcher can aggregate without re-reading the volume.
            return df.iloc[0].to_dict()
        return None

    trajectory_row = first_row_or_none("trajectory_stats.csv")
    accepted_row = first_row_or_none("final_design_stats.csv")

    # Post-MPNN re-prediction log written by the monkey-patch launcher: one row
    # per (redesigned sequence x AF2 model), pass or fail -- the near-miss vs
    # far-off signal BindCraft otherwise discards.
    reprediction_rows = 0
    repred_csv = os.path.join(design_path, "mpnn_reprediction_log.csv")
    if os.path.exists(repred_csv):
        repred_df = pd.read_csv(repred_csv)
        reprediction_rows = len(repred_df)
        print(f"\n=== mpnn_reprediction_log.csv ({reprediction_rows} rows) ===")
        if reprediction_rows:
            with pd.option_context("display.max_columns", None, "display.width", 250):
                print(repred_df.to_string())

    return {
        "seed": seed,
        "target": target,
        "run_tag": run_tag,
        "hotspots": hotspots,
        "i_ptm_threshold": i_ptm_threshold,
        "timed_out": timed_out,
        "design_path": design_path,
        # wall clock inside the container; Modal bills from container start, so
        # this slightly understates the billed time (image pull is not counted)
        "gpu_seconds": round(time.time() - t0, 1),
        "trajectory": trajectory_row,
        "accepted": accepted_row,
        "reprediction_rows": reprediction_rows,
    }


# Modal's pricing page lists "A10" at this rate and has no separate A10G entry,
# so treat it as approximate and correct it here if the invoice disagrees.
A10G_USD_PER_SEC = 0.000306


def calibration_summary(results):
    """Print run economics for the caller. Does not write to any log file:
    challenge-specific writeups live under challenges/<target>/ and are owned
    by the human running the sweep, not by this launcher.
    """
    attempts = len(results)
    trajectories = sum(1 for r in results if r["trajectory"] is not None)
    accepted = sum(1 for r in results if r["accepted"] is not None)
    timed_out = sum(1 for r in results if r["timed_out"])
    gpu_seconds = sum(r["gpu_seconds"] for r in results)
    cost = gpu_seconds * A10G_USD_PER_SEC

    def per(n):
        return f"${cost / n:.2f}" if n else "n/a"

    traj_rate = f"{trajectories / attempts:.1%}" if attempts else "n/a"
    accept_rate = f"{accepted / trajectories:.1%}" if trajectories else "n/a"
    print(
        "\n=== calibration ===\n"
        f"  attempts (calls made):     {attempts}\n"
        f"  timed out:                 {timed_out}\n"
        f"  reached a trajectory row:  {trajectories} ({traj_rate} of attempts)\n"
        f"  accepted designs:          {accepted} ({accept_rate} of trajectories)\n"
        f"  GPU time:                  {gpu_seconds:.0f} s ({gpu_seconds / 3600:.2f} h)\n"
        f"  A10G rate:                 ${A10G_USD_PER_SEC:.6f}/s "
        "(Modal list price for A10)\n"
        f"  total cost:                ${cost:.2f}\n"
        f"  cost per attempt:          {per(attempts)}\n"
        f"  cost per accepted design:  {per(accepted)}"
    )


@app.local_entrypoint()
def main(
    target: str,
    pdb_id: str,
    target_chains: str,
    hotspots: str,
    n: int = 1,
    i_ptm_threshold: float = 0.0,
    run_tag: str = "default",
    advanced_preset: str = DEFAULT_ADVANCED_PRESET,
    lengths: str = DEFAULT_LENGTHS,
    target_residue_range: str = "",
):
    """Fan out N independent design_one attempts in parallel across A10Gs.

    Required per-challenge args:
      --target         slug for this challenge (namespaces outputs on the volume)
      --pdb-id         4-char RCSB code of the target complex
      --target-chains  comma-separated chain IDs to keep (e.g. "V,W")
      --hotspots       ColabDesign prep_pos() format hotspots (e.g. "V21,V25,V48,V63")

    Example:
      modal run --detach modal/run_bindcraft.py::main \\
        --target vegf --pdb-id 1FLT --target-chains V,W \\
        --hotspots V21,V25,V48,V63 --n 30 --run-tag hardtarget-focused4

    Any knob can still be overridden per run, e.g. --i-ptm-threshold 0.45 to
    relax filters, or --advanced-preset default_4stage_multimer for plain mode.
    Run one detached app at a time -- two concurrent detached `modal run`
    sessions from one client cancel each other.
    """
    seeds = list(range(n))
    # order_outputs=False: results stream back in COMPLETION order, not seed
    # order, so a slow seed 0 no longer blocks seeing the ones that finished
    # first. Attempts are independent and calibration_summary aggregates over
    # the whole list, so ordering has no effect on correctness -- only on how
    # early each result surfaces.
    results = list(design_one.starmap(
        [(s, target, pdb_id, target_chains, hotspots,
          i_ptm_threshold, run_tag, advanced_preset, lengths,
          target_residue_range) for s in seeds],
        order_outputs=False,
    ))
    for r in results:
        print(r)
    calibration_summary(results)
