#!/usr/bin/env python3
"""Build and validate challenges/tnfa/submission.csv. Writes nothing unless
every check passes.

Sequences come from the BindCraft final_design_stats.csv files pulled off the
Modal volume -- never retyped. Submission order follows the pre-registered
priority in methods.md: the affinity gate (SC >= 0.58) is a hard filter, then
designs carrying the pre-registered pH mechanism rank above those that do not,
because objective 3 (pH selectivity) is ranked first by the organisers.

Checks: declared length == name length == actual sequence length; standard
residues only; no duplicate names or sequences; and every histidine position
asserted in the writeup is present in the sequence actually submitted.
"""
import csv, glob, os, re, sys

DST = "challenges/tnfa/submission.csv"
SRC_GLOB = "challenges/tnfa/v2-core*/**/final_design_stats.csv"
SC_PASS = 0.58
AA = set("ACDEFGHIKLMNPQRSTVWY")
DRY = "--dry-run" in sys.argv

# (name, tier, His positions the writeup relies on).
#
# TIER 1 WAS REDEFINED ON 2026-10-12, AND THE CHANGE IS POST-HOC.
# The original definition was: AF2 (2/2) AND Boltz-2 at the Amendment-4 bar of
# >=7 of 10 diffusion samples, ON BOTH SPECIES. After 12 designs x n=10 plus
# two replication runs, **no design meets that definition** -- the best mouse
# result is l69_mpnn1 at 2 of 3 runs (pooled 20/30, exactly the bar's implied
# rate). Keeping it would leave tier 1 empty and discard the fact that two
# designs are now confirmed on the human arm across independent runs.
# Tier 1 therefore now means: AF2 (2/2) AND Boltz-2 >=7 of 10 on the HUMAN arm
# in TWO OR MORE independent runs (Amendment 5's replication standard).
# This is a loosened criterion applied after seeing that nothing passed the
# original. It is disclosed as such in submission-writeup.md, and the
# both-species result is reported there for every design so a reader can apply
# the original definition unaided.
#
# Tier 2: anchor on AF2 in 2/2 samples; Boltz-2 tested and below the bar, or
#         not replicated.
# Tier 3: clears the affinity gate, no anchor within the pre-registered 6.0 A.
# Ordering is POST-HOC throughout and disclosed; the bars themselves
# (Amendments 4, 5) were fixed before the runs that produced these results.
ORDER = [
    ("tnfa_l69_s930894_mpnn1",  1, [4]),      # human 10/10 x3 runs = 30/30; mouse 2 of 3 runs (20/30)
    ("tnfa_l91_s990274_mpnn1",  1, [15, 16]), # human 9/10 then 10/10 = 19/20; mouse 7/20
    ("tnfa_l69_s930894_mpnn2",  2, [4]),      # human 4/10 then 6/10 -> below bar both runs
    ("tnfa_l87_s136696_mpnn1",  2, [27]),     # human 0/10 -- AF2 anchor does not reproduce
    ("tnfa_l66_s937529_mpnn2",  2, [32]),     # human 6/10 -- one sample short, NOT re-run (Am.7)
    ("tnfa_l91_s990274_mpnn2",  2, [15, 16]), # human 3/10 then 4/10 -> below bar both runs
    ("tnfa_l84_s861729_mpnn1",  3, []),
    ("tnfa_l66_s937529_mpnn1",  3, [32]),
    ("tnfa_l60_s347619_mpnn2",  3, [17]),
    ("tnfa_l60_s347619_mpnn1",  3, [17]),
    ("tnfa_l62_s149973_mpnn20", 3, [30, 34, 35]),
    ("tnfa_l97_s762214_mpnn2",  3, [72]),
]

def die(m): sys.exit("FAIL: " + m)

rows = {}
for fp in glob.glob(SRC_GLOB, recursive=True):
    for r in csv.DictReader(open(fp)):
        d = r.get("Design")
        if d and r.get("Sequence") and d not in rows:
            rows[d] = r
if not rows: die("no final_design_stats.csv rows found; run from the repo root")

out, seen_seq = [], {}
for name, tier, his in ORDER:
    if name not in rows: die(f"{name} not found in any final_design_stats.csv")
    r = rows[name]
    seq = r["Sequence"].strip().upper()

    m = re.search(r"_l(\d+)_", name)
    if not m: die(f"{name}: cannot parse length from name")
    if not (int(m.group(1)) == len(seq) == int(float(r["Length"]))):
        die(f"{name}: length disagreement name={m.group(1)} seq={len(seq)} csv={r['Length']}")
    bad = set(seq) - AA
    if bad: die(f"{name}: non-standard residues {bad}")
    if not (10 <= len(seq) <= 250): die(f"{name}: length {len(seq)} outside the permitted 10-250")

    sc = r.get("Average_ShapeComplementarity")
    if sc in (None, "", "nan"): die(f"{name}: no ShapeComplementarity")
    if float(sc) < SC_PASS:
        die(f"{name}: SC {float(sc):.3f} < {SC_PASS} -- fails the pre-registered affinity gate")

    for p in his:
        if p > len(seq) or seq[p - 1] != "H":
            die(f"{name}: writeup claims His{p} but sequence has "
                f"{seq[p-1] if p <= len(seq) else 'nothing'} there")
    if seq.count("H") != len(set(his)) and his:
        print(f"  note {name}: {seq.count('H')} His in sequence, {len(set(his))} load-bearing")

    if seq in seen_seq: die(f"{name} duplicates the sequence of {seen_seq[seq]}")
    seen_seq[seq] = name
    out.append((name, seq, "single_chain", tier, float(sc)))

if len({n for n, *_ in out}) != len(out): die("duplicate names")
print(f"validated {len(out)} designs")
for n, s, _, t, sc in out:
    print(f"  T{t}  {n:28} {len(s):>3} aa  SC={sc:.3f}  His={[i+1 for i,c in enumerate(s) if c=='H']}")
if DRY:
    print("\n--dry-run: nothing written"); sys.exit(0)
os.makedirs(os.path.dirname(DST), exist_ok=True)
with open(DST, "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["name", "sequence", "molecule_class"])
    for n, s, c, _, _ in out: w.writerow([n, s, c])
print(f"\nwrote {DST} ({len(out)} designs)")
