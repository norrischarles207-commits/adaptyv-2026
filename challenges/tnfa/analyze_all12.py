#!/usr/bin/env python3
"""Full analysis of the 12-design n=10 run, under Amendments 4, 5 and 6.

Reads the CHECKPOINT (.partial) because the run's final json.dump was never
reached -- the summary crashed on a None mean (the very bug Amendment 6
addresses). The checkpoint holds all 12 designs, both arms, 10 samples each.
"""
import json, sys, math, itertools, statistics as st, re

P1 = "challenges/tnfa/crossreact-n10.json"            # run 1, top-3 only
P2 = "challenges/tnfa/crossreact-all12-n10.json.partial"  # run 2, all 12
BAR, P0, NS = 7, 2/3, 10

def wilson(k, n, z=1.96):
    if n == 0: return (0.0, 1.0)
    ph = k/n; d = 1 + z*z/n
    c = (ph + z*z/(2*n))/d
    h = z*math.sqrt(ph*(1-ph)/n + z*z/(4*n*n))/d
    return (max(0., c-h), min(1., c+h))
def tle(k, n, p): return sum(math.comb(n,i)*p**i*(1-p)**(n-i) for i in range(0, k+1))
def tge(k, n, p): return sum(math.comb(n,i)*p**i*(1-p)**(n-i) for i in range(k, n+1))

def perm_p(a, b):
    """Exact two-sided permutation test on the difference of means."""
    if len(a) < 2 or len(b) < 2: return None
    pool = a + b; n = len(a); tot = sum(pool)
    obs = abs(sum(a)/len(a) - sum(b)/len(b))
    hit = cnt = 0
    for combo in itertools.combinations(pool, n):
        sa = sum(combo)
        if abs(sa/n - (tot-sa)/(len(pool)-n)) >= obs - 1e-12: hit += 1
        cnt += 1
    return hit/cnt

def fold(v):
    ifa = v.get("interface_per_sample") or []
    samp = [x for x in (v.get("ipsae_min_samples") or []) if x is not None]
    hits = [h for x in ifa for h in (x.get("ph_rule_hits") or [])]
    return dict(
        ph=sum(1 for x in ifa if x.get("ph_rule_hits")),
        n_iface=len(ifa), eff=len(samp), samples=samp,
        mean=round(sum(samp)/len(samp), 4) if samp else None,
        rng=round(max(samp)-min(samp), 4) if samp else None,
        both=sum(1 for x in ifa if x.get("contacts_both_protomers")),
        anchors=sorted({h["anchor_resnum"] for h in hits}),
        dmin=round(min(h["distance_A"] for h in hits), 2) if hits else None,
        dmax=round(max(h["distance_A"] for h in hits), 2) if hits else None,
        his=sorted({h["his_resnum"] for h in hits}))

r2 = json.load(open(P2))["raw_rows"]
F2 = {re.sub(r"_s\d+", "", d.replace("tnfa_","")): {sp: fold(v) for sp, v in pr.items()}
      for d, pr in r2.items()}
r1 = {re.sub(r"_s\d+", "", x["design"].replace("tnfa_","")): x
      for x in json.load(open(P1))["rows"]}
F1 = {}
for k, x in r1.items():
    F1[k] = {}
    for sp in ("human","mouse"):
        ifa = x["%s_interface" % sp]
        F1[k][sp] = dict(ph=sum(1 for y in ifa if y.get("ph_rule_hits")),
                         mean=x["%s_mean" % sp], rng=x["%s_range" % sp],
                         samples=[s for s in x["%s_samples" % sp] if s is not None])

print("="*104)
print("OBJECTIVE 3 -- pH rule, bar >= %d of %d  (Amendment 4 bar; Amendment 5 replication rule)" % (BAR, NS))
print("="*104)
print("%-14s %-9s %-9s %-9s %-9s %-26s %s" % ("design","run1 hum","run2 hum","run1 mou","run2 mou","status","anchor/dist (run2 human)"))
status = {}
for d in sorted(F2, key=lambda k: -F2[k]["human"]["ph"]):
    h2, m2 = F2[d]["human"]["ph"], F2[d]["mouse"]["ph"]
    h1 = F1.get(d, {}).get("human", {}).get("ph")
    m1 = F1.get(d, {}).get("mouse", {}).get("ph")
    runs_h = [x for x in (h1, h2) if x is not None]
    if len(runs_h) == 2 and all(x >= BAR for x in runs_h): s = "CONFIRMED (human, 2 runs)"
    elif h2 >= BAR and h1 is None:                          s = "PROVISIONAL (1 run)"
    elif len(runs_h) == 2 and any(x >= BAR for x in runs_h): s = "FAILED REPLICATION"
    else:                                                    s = "below bar"
    status[d] = s
    f = F2[d]["human"]
    det = ("His%s->%s  %.2f-%.2f A" % (f["his"], f["anchors"], f["dmin"], f["dmax"])) if f["dmin"] else "-"
    print("%-14s %-9s %-9s %-9s %-9s %-26s %s"
          % (d, h1 if h1 is not None else "-", "%d/10"%h2,
             m1 if m1 is not None else "-", "%d/10"%m2, s, det))

print()
print("Pooled across both runs, where a design was tested twice:")
for d in sorted(F2):
    if d not in F1: continue
    for sp in ("human","mouse"):
        k = F1[d][sp]["ph"] + F2[d][sp]["ph"]; n = 20
        lo, hi = wilson(k, n)
        print("  %-14s %-6s %2d/20  Wilson95=[%.2f,%.2f]  P(>=k|p0)=%.3f" % (d, sp, k, lo, hi, tge(k, n, P0)))

print()
print("="*104)
print("OBJECTIVE 2 -- species comparison (Amendment 5: pre-registered verdict AND permutation p together)")
print("           (Amendment 6: no verdict when effective n < 2 on either arm)")
print("="*104)
print("%-14s %-17s %-17s %-8s %-8s %-22s %s" % ("design","human mean[rng]","mouse mean[rng]","diff","floor","pre-reg verdict","exact perm p"))
suppressed = []
for d in sorted(F2):
    h, m = F2[d]["human"], F2[d]["mouse"]
    if h["eff"] < 2 or m["eff"] < 2:
        naive = None
        if h["mean"] is not None and m["mean"] is not None:
            nd = round(h["mean"]-m["mean"], 4); nf = round(max(h["rng"] or 0, m["rng"] or 0), 4)
            naive = "REAL" if abs(nd) > nf else "indistinguishable"
            suppressed.append((d, h["eff"], m["eff"], h["mean"], m["mean"], nd, nf, naive))
        else:
            suppressed.append((d, h["eff"], m["eff"], h["mean"], m["mean"], None, None, "uncomputable"))
        print("%-14s %-17s %-17s %-8s %-8s %-22s %s"
              % (d, "n=%d"%h["eff"], "n=%d"%m["eff"], "-", "-", "NOT MEASURABLE (Am.6)", "-"))
        continue
    diff = round(h["mean"]-m["mean"], 4); floor = round(max(h["rng"], m["rng"]), 4)
    verdict = "REAL" if abs(diff) > floor else "indistinguishable"
    p = perm_p(h["samples"], m["samples"])
    print("%-14s %-17s %-17s %+8.4f %-8.4f %-22s %.2e"
          % (d, "%.4f[%.4f]"%(h["mean"],h["rng"]), "%.4f[%.4f]"%(m["mean"],m["rng"]),
             diff, floor, verdict, p))

print()
print("SUPPRESSED BY AMENDMENT 6 -- disclosed, not discarded:")
for d, he, me, hm, mm, nd, nf, nv in suppressed:
    print("  %-14s effective n human=%d mouse=%d | naive mean %s vs %s -> would have read %s"
          % (d, he, me, hm, mm, nv))
print("  Direction of this rule's effect on our own case: a REAL verdict is")
print("  evidence AGAINST cross-reactivity, so suppressing these REMOVES")
print("  unfavourable evidence. Stated explicitly for that reason.")

print()
print("="*104)
print("ENGAGEMENT (sanity)")
print("="*104)
tot = ok = 0
for d in sorted(F2):
    for sp in ("human","mouse"):
        tot += F2[d][sp]["n_iface"]; ok += F2[d][sp]["both"]
print("  samples contacting both protomers: %d / %d" % (ok, tot))
print("  negative control l84_mpnn1 (zero histidines): human %d/10, mouse %d/10"
      % (F2["l84_mpnn1"]["human"]["ph"], F2["l84_mpnn1"]["mouse"]["ph"]))
