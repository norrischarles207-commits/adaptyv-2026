#!/usr/bin/env python3
"""Analyze crossreact-n10.json.

Three quantities, kept strictly separate:
  A. PRE-REG ipsae_min  -- min over ALL binder<->target ordered pairs.
     This is what methods.md defines. On a TRIMER target one protomer is
     correctly never engaged, and its pair sets the min -- which is why
     Amendment 3 says the trimer ipsae_min is NOT compared to 0.60.
  B. RESTRICTED ipsae_min -- min over binder<->target pairs for protomers
     the binder actually touches (atom_pairs > 0). POST-HOC diagnostic.
  C. pH rule (Amendment 4) -- proportion of samples with a binder His
     ND1/NE2 within 6.0 A of R32 NH1/NH2/NE or K65 NZ. Bar: >= 7 of 10.
"""
import json, sys, statistics as st

path = sys.argv[1]
data = json.load(open(path))
rows = data["rows"]
print("stage=%s  diffusion_samples=%s  gpu_s=%.1f  aborted=%s  designs=%d"
      % (data.get("stage"), data.get("diffusion_samples"),
         data.get("total_gpu_seconds"), data.get("aborted"), len(rows)))

def agg(xs):
    if not xs:
        return (None, None, None)
    return (round(sum(xs)/len(xs), 4),
            round(st.stdev(xs), 4) if len(xs) > 1 else 0.0,
            round(max(xs)-min(xs), 4))

def fold(row, sp):
    pairs = row["%s_ipsae_pairs" % sp]
    iface = row["%s_interface" % sp]
    n = min(len(pairs), len(iface))
    raw, restr = [], []
    ph, both, nch, detail, eng_counts = [], [], [], [], []
    for i in range(n):
        ps, ifc = pairs[i], iface[i]
        bid = ifc["binder_chain"]
        per = ifc["per_chain"]
        engaged = {c for c, d in per.items() if d.get("atom_pairs", 0) > 0}
        eng_counts.append(len(engaged))
        bp = [p for p in ps if bid in (p["a"], p["b"])]
        if bp:
            raw.append(min(p["ipsae"] for p in bp))
        eng = [p for p in bp
               if (p["b"] if p["a"] == bid else p["a"]) in engaged]
        if eng:
            restr.append(min(p["ipsae"] for p in eng))
        hits = ifc.get("ph_rule_hits") or []
        ph.append(1 if hits else 0)
        for h in hits:
            detail.append((i, h.get("his_resnum"), h.get("anchor_chain"),
                           h.get("anchor_resnum"), h.get("distance_A")))
        both.append(1 if ifc.get("contacts_both_protomers") else 0)
        nch.append(ifc.get("n_target_chains_contacted"))
    return dict(n=n, raw=agg(raw), restr=agg(restr), raw_list=raw,
                restr_list=restr, ph=sum(ph), both=sum(both),
                nch=sorted(set(nch)), eng=sorted(set(eng_counts)),
                detail=detail)

res = {}
for row in rows:
    for sp in ("human", "mouse"):
        res[(row["design"], sp)] = fold(row, sp)
        res[(row["design"], sp)]["stored_mean"] = row["%s_mean" % sp]
        res[(row["design"], sp)]["stored_range"] = row["%s_range" % sp]

print()
print("=" * 118)
print("PER-FOLD (n=10 diffusion samples each)")
print("=" * 118)
print("%-30s %-6s %-26s %-26s %-12s %s"
      % ("design", "sp", "A. PRE-REG (all pairs)", "B. RESTRICTED (engaged)",
         "C. pH rule", "engagement"))
for (d, sp), v in res.items():
    a, b = v["raw"], v["restr"]
    chk = "" if abs(a[0] - v["stored_mean"]) < 5e-4 else "  <<MISMATCH vs stored %.4f>>" % v["stored_mean"]
    print("%-30s %-6s m %.4f sd %.4f r %.4f  m %.4f sd %.4f r %.4f  %2d/%-2d %-4s  both %d/%d eng%s%s"
          % (d.replace("tnfa_", ""), sp, a[0], a[1], a[2], b[0], b[1], b[2],
             v["ph"], v["n"], "PASS" if v["ph"] >= 7 else "fail",
             v["both"], v["n"], v["eng"], chk))

print()
print("pH rule hits (sample#, His, anchor, distance):")
for (d, sp), v in res.items():
    tag = "%s %s" % (d.replace("tnfa_", ""), sp)
    if not v["detail"]:
        print("  %-36s -- none in 10 samples" % tag)
        continue
    anchors = sorted({t[3] for t in v["detail"]})
    hiss = sorted({t[1] for t in v["detail"]})
    print("  %-36s %d hits  His%s -> anchor%s" % (tag, len(v["detail"]), hiss, anchors))
    for t in v["detail"]:
        print("      s%-2d His%-4s %s%-4s %.2f A" % (t[0], t[1], t[2], t[3], t[4]))

print()
print("=" * 118)
print("SPECIES COMPARISON  (verdict: |diff| > max(range_h, range_m) -> REAL)")
print("=" * 118)
designs = sorted({d for d, _ in res})
for metric, label in (("raw", "A. PRE-REG"), ("restr", "B. RESTRICTED")):
    print(" --", label)
    print("    %-24s %-20s %-20s %-10s %-9s %s"
          % ("design", "human", "mouse", "diff", "floor", "verdict"))
    for d in designs:
        h, m = res[(d, "human")][metric], res[(d, "mouse")][metric]
        diff = h[0] - m[0]
        floor = max(h[2], m[2])
        print("    %-24s %.4f[%.4f]      %.4f[%.4f]      %+.4f    %.4f    %s"
              % (d.replace("tnfa_", ""), h[0], h[2], m[0], m[2], diff, floor,
                 "REAL" if abs(diff) > floor else "indistinguishable"))

print()
print("=" * 118)
print("AMENDMENT 4 SUMMARY -- pH rule, human arm, bar = >= 7 of 10")
print("=" * 118)
for d in designs:
    v = res[(d, "human")]
    vm = res[(d, "mouse")]
    print("  %-24s human %2d/10 %-4s   mouse %2d/10 %-4s"
          % (d.replace("tnfa_", ""), v["ph"], "PASS" if v["ph"] >= 7 else "fail",
             vm["ph"], "PASS" if vm["ph"] >= 7 else "fail"))
