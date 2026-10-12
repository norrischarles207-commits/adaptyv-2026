#!/usr/bin/env python3
"""Adversarial audit of the n=10 result and the claims made from it."""
import json, sys, math, itertools, statistics as st
from collections import Counter

d = json.load(open(sys.argv[1]))
rows = d["rows"]
fail = []
def chk(c, m):
    print(("  ok   " if c else "  FAIL ") + m)
    if not c: fail.append(m)

print("=== A. anchor residue identity (every anchor, every sample) ===")
bad_id = Counter(); seen = 0
for r in rows:
    for sp in ("human", "mouse"):
        for ic in r["%s_interface" % sp]:
            for a in ic["anchors"]:
                seen += 1
                if not a.get("identity_as_expected"):
                    bad_id[(sp, a["chain"], a["resnum"], a["resname"])] += 1
chk(not bad_id, "all %d anchor records have identity_as_expected=True%s"
    % (seen, "" if not bad_id else " -- VIOLATIONS: %s" % dict(bad_id)))

print("\n=== B. cation atoms actually present (R32 needs 3, K65 needs 1) ===")
wrong_atoms = Counter()
for r in rows:
    for sp in ("human", "mouse"):
        for ic in r["%s_interface" % sp]:
            for a in ic["anchors"]:
                want = 3 if a["resnum"] == 32 else 1
                if a.get("cation_atoms_present") != want:
                    wrong_atoms[(sp, a["resnum"], a.get("cation_atoms_present"))] += 1
chk(not wrong_atoms, "every anchor exposes its full cation tip set%s"
    % ("" if not wrong_atoms else " -- %s" % dict(wrong_atoms)))

print("\n=== C. does any pH hit sit on a protomer the binder never touches? ===")
offchain = []
for r in rows:
    for sp in ("human", "mouse"):
        for i, ic in enumerate(r["%s_interface" % sp]):
            eng = {c for c, v in ic["per_chain"].items() if v.get("atom_pairs", 0) > 0}
            for h in (ic.get("ph_rule_hits") or []):
                if h["anchor_chain"] not in eng:
                    offchain.append((r["design"], sp, i, h))
chk(not offchain, "every pH hit is on an ENGAGED protomer%s"
    % ("" if not offchain else " -- %d spurious: %s" % (len(offchain), offchain[:3])))

print("\n=== D. ph_rule_hits <-> ph_anchors_satisfied agree ===")
mismatch = []
for r in rows:
    for sp in ("human", "mouse"):
        for i, ic in enumerate(r["%s_interface" % sp]):
            a = bool(ic.get("ph_rule_hits"))
            b = bool(ic.get("ph_anchors_satisfied"))
            if a != b: mismatch.append((r["design"], sp, i, a, b))
chk(not mismatch, "the two pH fields agree in all 60 samples%s"
    % ("" if not mismatch else " -- %s" % mismatch))

print("\n=== E. distance_A reproducible from nearest_binder_his ===")
bad_d = []
for r in rows:
    for sp in ("human", "mouse"):
        for i, ic in enumerate(r["%s_interface" % sp]):
            amap = {(a["chain"], a["resnum"]): a for a in ic["anchors"]}
            for h in (ic.get("ph_rule_hits") or []):
                a = amap.get((h["anchor_chain"], h["anchor_resnum"]))
                nb = dict((bn, dd) for dd, bn in (a or {}).get("nearest_binder_his", []))
                if nb.get(h["his_resnum"]) != h["distance_A"]:
                    bad_d.append((r["design"], sp, i, h["distance_A"], nb))
chk(not bad_d, "every hit distance matches the anchor's own nearest-His table%s"
    % ("" if not bad_d else " -- %s" % bad_d[:3]))

print("\n=== F. hits per sample (>1 would make 'N of N hits' wording wrong) ===")
for r in rows:
    for sp in ("human", "mouse"):
        per = [len(ic.get("ph_rule_hits") or []) for ic in r["%s_interface" % sp]]
        nz = [x for x in per if x]
        print("    %-26s %-6s samples_with_hit=%2d  hits_per_hitting_sample=%s"
              % (r["design"].replace("tnfa_", ""), sp, len(nz), sorted(set(nz)) or "-"))

print("\n=== G. every anchor hit ALSO within 6.0 A, and <= cutoff ===")
over = [h["distance_A"] for r in rows for sp in ("human", "mouse")
        for ic in r["%s_interface" % sp] for h in (ic.get("ph_rule_hits") or [])
        if h["distance_A"] > 6.0]
chk(not over, "no recorded hit exceeds the 6.0 A cutoff%s" % ("" if not over else " -- %s" % over))

print("\n=== H. exact permutation test on the species difference (assumption-free) ===")
print("    the pre-registered test compares a difference of MEANS to a RANGE of")
print("    single samples. that is a heuristic, not a significance test. this is")
print("    the same data under an exact test, for contrast only -- NOT a re-gate.")
for r in rows:
    h, m = r["human_samples"], r["mouse_samples"]
    obs = abs(st.mean(h) - st.mean(m))
    pool = h + m
    n = len(h)
    cnt = tot = 0
    for combo in itertools.combinations(range(len(pool)), n):
        cs = set(combo)
        a = [pool[i] for i in combo]
        b = [pool[i] for i in range(len(pool)) if i not in cs]
        tot += 1
        if abs(st.mean(a) - st.mean(b)) >= obs - 1e-12: cnt += 1
    p = cnt / tot
    print("    %-26s diff=%.4f  exact two-sided p=%.2e  (%d/%d)"
          % (r["design"].replace("tnfa_", ""), obs, p, cnt, tot))

print("\n=== I. binomial reading of the pH proportions (bar = >=7/10, p0 = 2/3) ===")
def wilson(k, n, z=1.96):
    if n == 0: return (0.0, 1.0)
    ph = k / n; d = 1 + z*z/n
    c = (ph + z*z/(2*n)) / d
    hw = z*math.sqrt(ph*(1-ph)/n + z*z/(4*n*n)) / d
    return (max(0.0, c-hw), min(1.0, c+hw))
def tail_le(k, n, p):
    return sum(math.comb(n, i)*p**i*(1-p)**(n-i) for i in range(0, k+1))
def tail_ge(k, n, p):
    return sum(math.comb(n, i)*p**i*(1-p)**(n-i) for i in range(k, n+1))
p0 = 2/3
for r in rows:
    for sp in ("human", "mouse"):
        k = sum(1 for ic in r["%s_interface" % sp] if ic.get("ph_rule_hits"))
        lo, hi = wilson(k, 10)
        print("    %-26s %-6s %2d/10  Wilson95=[%.2f,%.2f]  P(<=k|p=2/3)=%.3f  P(>=k|p=2/3)=%.3f"
              % (r["design"].replace("tnfa_", ""), sp, k, lo, hi,
                 tail_le(k, 10, p0), tail_ge(k, 10, p0)))
print("\n    'one design in three reproduces' -- 1 of 3 designs, Wilson95 = [%.2f, %.2f]"
      % wilson(1, 3))

print("\n" + "="*64)
print("AUDIT CLEAN" if not fail else "%d AUDIT FAILURES" % len(fail))
for f in fail: print("  - " + f)
