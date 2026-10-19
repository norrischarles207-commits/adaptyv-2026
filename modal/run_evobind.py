"""run_evobind.py -- EvoBind2 de novo peptide design on Modal (GLP1R, Challenge 3).

SUPERSEDED 2026-10-17 -- NOT used for Challenge 3 design.
This ran once as a cost probe and was stopped. The measurement it produced
(92.5 s per mutation step on an A10G against the 409-residue receptor, about
$0.0283/iteration, i.e. $4.25-28 per design) is precisely why
challenges/glp1r/methods.md selects BindCraft instead. The file is kept so that
measurement is checkable -- not because the pipeline below is in use. EvoBind
ran correctly; it is the budget that does not fit, not the method that failed.

EvoBind2 (Li, Vlachos & Bryant, Commun Chem 2025; github.com/patrickbryant1/EvoBind)
designs peptide binders from a receptor SEQUENCE alone, by in-silico directed
evolution against a modified AlphaFold2. It is the method behind the only
published *de novo* GLP1R agonist (the dual GCGR/GLP1R cyclic-agonist paper),
and was the first tool tried for Ch3. We design LINEAR peptides (the
Adaptyv cell-free system expresses a linear chain: Met + our sequence + C-tag),
not cyclic -- so --cyclic_offset is never set here.

WHY THIS FILE IS STAGED
-----------------------
I cannot run Modal from the agent sandbox (no egress to modal.com), so Charles
runs each command in his own terminal and pastes the output back. To keep a
plumbing bug from ever burning GPU-hours on a real design, the work is split
into cheap gates you run in order:

  1) modal run modal/run_evobind.py::verify          # ~1-2 min on a T4, ~$0.01
        image builds? jax sees the GPU? EvoBind + its AF2 import?
  2) modal run modal/run_evobind.py::download_weights # CPU, one-time, ~$0
        AF2 2021-07-14 params -> evobind-af2-weights volume (sentinel: skip if present)
  3) modal run modal/run_evobind.py::get_msa          # CPU, one-time, ~$0
        GLP1R MSA via ColabFold API -> /designs/glp1r/msa/glp1r.a3m
  4) modal run modal/run_evobind.py::probe --single-seq   # cheapest real design
        proves mc_design.py runs end-to-end; LOWER-BOUND timing (no MSA)
  5) modal run modal/run_evobind.py::probe            # realistic timing w/ MSA
        the number we size the fan-out budget against

Everything before step 4 is CPU or a ~2-min T4, so the first time we spend real
A10G minutes is a single, deliberate design -- never a blind fan-out.

COST: A10G is billed at ~$0.000306/s (~$1.10/h) per your BindCraft app. `probe`
prints measured GPU-seconds and dollars so we extrapolate the fan-out honestly.
"""
import modal

app = modal.App("adaptyv-evobind")

# EvoBind needs AF2 params 2021-07-14 (its bundled AF2 expects that release);
# this is a DIFFERENT set from BindCraft's 2022-12-06, so it gets its own volume
# rather than colliding on af2-weights.
ev_weights = modal.Volume.from_name("evobind-af2-weights", create_if_missing=True)
# Reuse the shared designs volume so Ch3 outputs sit beside egfr/tnfa.
designs = modal.Volume.from_name("adaptyv-designs", create_if_missing=True)

# GLP1R assay target: wild-type UniProt P43220 segment 24-432 (the sequence
# Proteinbase publishes). The real construct carries unlisted thermostabilising
# mutations, but we design against WT, as agreed. 409 residues.
GLP1R_24_432 = (
    "RPQGATVSLWETVQKWREYRRQCQRSLTEDPPPATDLFCNRTFDEYACWPDGEPGSFVNVSCPWYLPWASSVPQGH"
    "VYRFCTAEGLWLQKDNSSLPWRDLSECEESKRGERSSPEEQLLFLYIIYTVGYALSFSALVIASAILLGFRHLHCT"
    "RNYIHLNLFASFILRALSVFIKDAALKWMYSTAAQQHQWDGLLSYQDSLSCRLVFLLMQYCVAANYYWLLVEGVYLY"
    "TLLAFSVLSEQWIFRLYVSIGWGVPLLFVVPWGIVKYLYEDEGCWTRNSNMNYWLIIRLPILFAIGVNFLIFVRVIC"
    "IVVSKLKANLMCKTDIKCRLAKSTLTLIPLLGTHEVIFAFVMDEHARGTLRFIKLFTELSFTSFQGLMVAILYCFVN"
    "NEVQLEFRKSWERWRLEHLHIQRDSS"
)

AF2_PARAMS_URL = (
    "https://storage.googleapis.com/alphafold/alphafold_params_2021-07-14.tar"
)

# EvoBind's conda env, replicated as pip pins (environment.yml). We skip hh-suite
# and uniclust30 entirely because we supply a precomputed .a3m, so the image is
# just: EvoBind repo + its bundled AF2 + a CUDA-12 jax that matches the pins.
image = (
    modal.Image.debian_slim(python_version="3.11")
    .apt_install("git", "wget", "aria2")
    .run_commands(
        "git clone https://github.com/patrickbryant1/EvoBind.git /opt/EvoBind",
    )
    .pip_install(
        # jax + CUDA 12 plugin, pinned exactly as EvoBind ships them
        "jax==0.4.30",
        "jaxlib==0.4.30",
        "jax-cuda12-pjrt==0.4.30",
        "jax-cuda12-plugin==0.4.30",
        "nvidia-cublas-cu12==12.5.3.2",
        "nvidia-cuda-cupti-cu12==12.5.82",
        "nvidia-cuda-nvcc-cu12==12.5.82",
        "nvidia-cuda-runtime-cu12==12.5.82",
        "nvidia-cudnn-cu12==9.1.1.17",
        "nvidia-cufft-cu12==11.2.3.61",
        "nvidia-cusolver-cu12==11.6.3.83",
        "nvidia-cusparse-cu12==12.5.1.3",
        "nvidia-nccl-cu12==2.22.3",
        "nvidia-nvjitlink-cu12==12.5.82",
    )
    .pip_install(
        "jax[cuda12]==0.4.30",  # keep jax+plugin matched; this layer re-resolves
        "dm-haiku==0.0.12",
        "dm-tree==0.1.8",
        "chex==0.1.86",
        "optax==0.2.2",
        "flax==0.8.5",
        "ml-collections==0.1.1",
        "ml-dtypes==0.3.2",
        "numpy==1.26.4",
        "scipy==1.14.0",
        "pandas==2.2.2",
        "biopython==1.81",
        "absl-py==2.1.0",
        "tensorflow-cpu==2.16.2",  # AF2 feature pipeline imports tf
        "requests==2.32.3",
    )
)

# AF2 wants data_dir to be the PARENT of params/ (it does os.path.join(data_dir,
# "params")), so we mount the weights volume at /weights and point --data_dir there.
DATA_DIR = "/weights"
EVOBIND = "/opt/EvoBind"

# Modal A10G list price (matches your BindCraft app's constant).
A10G_USD_PER_SEC = 0.000306
T4_USD_PER_SEC = 0.000164


@app.function(image=image, volumes={"/weights": ev_weights}, timeout=3600)
def download_weights():
    """One-time: fetch AF2 2021-07-14 params to the evobind-af2-weights volume."""
    import os, subprocess

    done = "/weights/params/done.txt"
    if os.path.exists(done):
        print("params already present -- skipping")
        return
    os.makedirs("/weights/params", exist_ok=True)
    tar_path = "/weights/af2_2021-07-14.tar"
    subprocess.run(["aria2c", "-x", "16", "-o", os.path.basename(tar_path),
                    "-d", "/weights", AF2_PARAMS_URL], check=True)
    subprocess.run(["tar", "-xf", tar_path, "-C", "/weights/params"], check=True)
    os.remove(tar_path)
    open(done, "w").close()
    print(subprocess.run(["ls", "-la", "/weights/params"],
                         capture_output=True, text=True).stdout)
    ev_weights.commit()
    print("weights committed")


def _colabfold_msa(seq: str, out_a3m: str):
    """Build a single-chain MSA for `seq` via the public ColabFold MMseqs2 API
    and write it to out_a3m (query first). CPU-only, no local database.

    Mirrors ColabFold's run_mmseqs2 submit/poll/download protocol. Runs on
    Modal (open egress), not in the agent sandbox.
    """
    import os, time, tarfile, requests

    host = "https://api.colabfold.com"
    ua = {"User-Agent": "colabfold/1.5.5 adaptyv-evobind"}
    query = f">101\n{seq}\n"

    r = requests.post(f"{host}/ticket/msa",
                      data={"q": query, "mode": "env"}, headers=ua, timeout=120)
    r.raise_for_status()
    sub = r.json()
    tid = sub["id"]
    print(f"[msa] ticket {tid} status={sub.get('status')}")

    # Explicit status handling: RATELIMIT/MAINTENANCE/UNKNOWN used to fall
    # through to the generic poll and burn the full timeout instead of saying
    # what went wrong.
    deadline = time.time() + 1800
    while True:
        if time.time() > deadline:
            raise RuntimeError("ColabFold MSA timed out after 30 min")
        r = requests.get(f"{host}/ticket/{tid}", headers=ua, timeout=120)
        r.raise_for_status()
        st = r.json().get("status")
        if st == "COMPLETE":
            break
        if st in ("ERROR", "UNKNOWN", "MAINTENANCE"):
            raise RuntimeError(f"ColabFold MSA failed with status {st}")
        if st == "RATELIMIT":
            print("[msa] rate limited -- backing off 30s")
            time.sleep(30)
            continue
        time.sleep(3)

    tgz = "/tmp/msa_result.tar.gz"
    with requests.get(f"{host}/result/download/{tid}", headers=ua,
                      stream=True, timeout=600) as resp:
        resp.raise_for_status()
        with open(tgz, "wb") as fh:
            for chunk in resp.iter_content(chunk_size=1 << 20):
                fh.write(chunk)

    with tarfile.open(tgz, "r:gz") as tar:
        names = tar.getnames()
        print(f"[msa] archive: {names}")
        pick = next((n for n in names if n.endswith("uniref.a3m")), None) \
            or next((n for n in names if n.endswith(".a3m")), None)
        if not pick:
            raise RuntimeError(f"no .a3m in MSA archive: {names}")
        tar.extract(pick, "/tmp/msa_out")
        extracted = os.path.join("/tmp/msa_out", pick)

    # ColabFold a3m can lead with '#' cardinality/comment lines. Drop them so
    # the query really is the first record -- otherwise the startswith('>')
    # test below fails and we prepend a DUPLICATE query.
    lines = open(extracted).read().splitlines()
    while lines and lines[0].startswith("#"):
        lines.pop(0)
    if not lines or not lines[0].startswith(">"):
        lines = [">101", seq] + lines

    # Hard guard: the first record MUST be our receptor. If the API ever hands
    # back a different job's result, designing against it would silently poison
    # every downstream design -- fail loudly here instead.
    first = []
    for ln in lines[1:]:
        if ln.startswith(">"):
            break
        first.append(ln)
    first_seq = "".join(first).replace("-", "").upper()
    if first_seq != seq.upper():
        raise RuntimeError(
            f"MSA query mismatch: first record is {len(first_seq)} aa, "
            f"expected the {len(seq)} aa GLP1R receptor -- refusing to cache")

    os.makedirs(os.path.dirname(out_a3m), exist_ok=True)
    with open(out_a3m, "w") as fh:
        fh.write("\n".join(lines) + "\n")
    n_seqs = sum(1 for ln in lines if ln.startswith(">"))
    print(f"[msa] wrote {out_a3m} ({n_seqs} sequences)")
    return n_seqs


@app.function(image=image, volumes={"/designs": designs}, timeout=3600)
def get_msa(depth_cap: int = 256):
    """One-time: build the GLP1R MSA and cache it on the designs volume.

    depth_cap caps the MSA at query + N sequences. This is a COST and MEMORY
    knob, not cosmetic: AF2's Evoformer scales with MSA depth, and EvoBind
    re-runs AF2 once per optimisation iteration against a 409-residue receptor.
    An uncapped MSA (often thousands deep) both inflates $/design -- the number
    this whole probe exists to measure -- and risks OOM on a 24 GB A10G. AF2
    gains little past ~30 sequences, so 256 is already generous.
    Pass --depth-cap 0 to keep the full MSA.
    """
    import os

    out = "/designs/glp1r/msa/glp1r.a3m"
    if os.path.exists(out):
        with open(out) as fh:
            n = fh.read().count(">")
        print(f"MSA already present at {out} ({n} sequences) -- skipping")
        return
    n = _colabfold_msa(GLP1R_24_432, out)

    if depth_cap and depth_cap > 0 and n > depth_cap:
        lines = open(out).read().splitlines()
        kept, seqs = [], 0
        for ln in lines:
            if ln.startswith(">"):
                seqs += 1
                if seqs > depth_cap:
                    break
            kept.append(ln)
        with open(out, "w") as fh:
            fh.write("\n".join(kept) + "\n")
        print(f"[msa] capped {n} -> {depth_cap} sequences")

    designs.commit()
    print("MSA committed")


@app.function(gpu="T4", image=image, volumes={"/weights": ev_weights}, timeout=1200)
def verify():
    """Cheap gate: image built, GPU visible to jax, EvoBind + AF2 import, params present."""
    import os, subprocess, sys
    import jax
    print("JAX devices:", jax.devices())
    sys.path.insert(0, f"{EVOBIND}/src")
    sys.path.insert(0, f"{EVOBIND}/src/AF2")
    try:
        from alphafold.model import model  # noqa: F401
        print("EvoBind AF2 import OK")
    except Exception as e:
        print("AF2 import FAILED:", e)
    print("mc_design.py present:", os.path.exists(f"{EVOBIND}/src/mc_design.py"))
    params_ok = os.path.exists("/weights/params/done.txt")
    print("params present:", params_ok)
    if params_ok:
        print(subprocess.run(["ls", "/weights/params"], capture_output=True, text=True).stdout)


@app.function(
    gpu="A10G",
    image=image,
    volumes={"/weights": ev_weights, "/designs": designs},
    timeout=5400,
)
def _design(
    seed: int,
    peptide_length: int,
    num_iterations: int,
    max_recycles: int,
    single_seq: bool,
    receptor_if_residues: str,
    run_tag: str,
):
    """Run ONE EvoBind design trajectory against GLP1R and report wall time + cost."""
    import os, time, subprocess, glob

    t0 = time.time()
    out_dir = f"/designs/glp1r/evobind/{run_tag}/{seed}"
    os.makedirs(out_dir, exist_ok=True)

    # EvoBind RESUMES: optimise_binder() does `if os.path.exists(output_dir +
    # "metrics.csv"): df = pd.read_csv(...)` and continues from that history.
    # Re-running the same --run-tag/--seed would therefore pick up mid-trajectory
    # and report gpu_seconds for a PARTIAL run -- silently corrupting the $/iter
    # number this probe exists to produce. Fail fast instead.
    if os.path.exists(os.path.join(out_dir, "metrics.csv")):
        raise RuntimeError(
            f"{out_dir} already holds metrics.csv -- EvoBind would RESUME it and "
            f"the timing would be wrong. Use a fresh --run-tag (or --seed).")

    # receptor fasta
    fasta = f"{out_dir}/glp1r.fasta"
    with open(fasta, "w") as fh:
        fh.write(f">glp1r_24_432\n{GLP1R_24_432}\n")

    # MSA: real (cached) or single-sequence (plumbing test / lower-bound timing)
    if single_seq:
        a3m = f"{out_dir}/glp1r_singleseq.a3m"
        with open(a3m, "w") as fh:
            fh.write(f">glp1r_24_432\n{GLP1R_24_432}\n")
        print("MSA: single-sequence (query only) -- LOWER-BOUND timing")
    else:
        a3m = "/designs/glp1r/msa/glp1r.a3m"
        if not os.path.exists(a3m):
            raise RuntimeError(f"MSA not found at {a3m} -- run get_msa first")
        with open(a3m) as fh:
            print(f"MSA: {a3m} (~{fh.read().count('>')} sequences)")

    cmd = [
        "python3", f"{EVOBIND}/src/mc_design.py",
        f"--receptor_fasta_path={fasta}",
        f"--peptide_length={peptide_length}",
        f"--msas={a3m}",
        f"--output_dir={out_dir}/",
        "--model_names=model_1",
        f"--data_dir={DATA_DIR}/",
        f"--max_recycles={max_recycles}",
        f"--num_iterations={num_iterations}",
        "--predict_only=False",
        f"--random_seed={seed}",
    ]
    if receptor_if_residues:
        cmd.append(f"--receptor_if_residues={receptor_if_residues}")

    print("CMD:", " ".join(cmd))
    timed_out = False
    try:
        subprocess.run(cmd, cwd=EVOBIND, check=True, timeout=5100,
                       env={**os.environ, "PYTHONUNBUFFERED": "1"})
    except subprocess.TimeoutExpired:
        timed_out = True
        print("!! hit time budget -- committing partial output")
    finally:
        designs.commit()

    print(f"\n=== files under {out_dir} ===")
    for p in sorted(glob.glob(f"{out_dir}/**/*", recursive=True)):
        if os.path.isfile(p):
            print(f"  {p} ({os.path.getsize(p)} bytes)")

    secs = round(time.time() - t0, 1)
    return {
        "seed": seed,
        "run_tag": run_tag,
        "peptide_length": peptide_length,
        "num_iterations": num_iterations,
        "max_recycles": max_recycles,
        "single_seq": single_seq,
        "timed_out": timed_out,
        "gpu_seconds": secs,
        "usd_a10g": round(secs * A10G_USD_PER_SEC, 3),
        "usd_per_iter": round(secs * A10G_USD_PER_SEC / max(num_iterations, 1), 5),
        "out_dir": out_dir,
    }


@app.local_entrypoint()
def probe(
    single_seq: bool = False,
    peptide_length: int = 18,
    num_iterations: int = 150,
    max_recycles: int = 3,
    receptor_if_residues: str = "",
    run_tag: str = "probe",
    seed: int = 0,
):
    """One design, measured. Defaults: 18-mer, 150 iters, 3 recycles, A10G,
    site-agnostic (as the EvoBind GLP1R-agonist precedent ran). Pass
    --single-seq for the cheapest plumbing check (no MSA).

      modal run modal/run_evobind.py::probe --single-seq
      modal run modal/run_evobind.py::probe

    Reports measured GPU-seconds, dollars, and $/iteration so we can extrapolate
    a full run (e.g. 300-500 iters) and size the fan-out against the Ch3 cap."""
    r = _design.remote(seed, peptide_length, num_iterations, max_recycles,
                        single_seq, receptor_if_residues, run_tag)
    print("\n=== probe result ===")
    for k, v in r.items():
        print(f"  {k}: {v}")
    iters = r["num_iterations"]
    per_iter = r["usd_per_iter"]
    print("\n=== extrapolation (A10G) ===")
    for full in (300, 500, 1000):
        print(f"  {full} iters  ~= ${per_iter * full:.2f}/design"
              f"  -> 40 designs ~= ${per_iter * full * 40:.0f}")
    if r["single_seq"]:
        print("NOTE: single-seq is a LOWER bound; real MSA runs somewhat slower.")
