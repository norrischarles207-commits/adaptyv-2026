#!/usr/bin/env python3
"""Generate the writeup's result tables from the raw run data, so no number in
submission-writeup.md is ever hand-transcribed."""
import json, math, re, itertools, statistics as st

R1 = {x["design"]: x for x in json.load(open("challenges/tnfa/crossreact-n10.json"))["rows"]}
R2 = json.load(open("challenges/tnfa/crossreact-all12-n10.json.partial"))["raw_rows"]
R3 = {x["design"]: x for x in json.load(open("challenges/tnfa/crossreact-rep2.json"))["rows"]}
SHORT = lambda d: re.sub(r"_s\d+", "", d.replace("tnfa_", ""))
BAR, P0 = 7, 2/3

def wilson(k, n, z=1.96):
    if n == 0: return (0., 1.)
    ph = k/n; d = 1+z*z/n; c = (ph+z*z/(2*n))/d
    h = z*math.sqrt(ph*(1-ph)/n + z*z/(4*n*n))/d
    return (max(0., c-h), min(1., c+h))
def tge(k, n, p): return sum(math.comb(n,i)*p**i*(1-p)**(n-i) for i in range(k, n+1))
def phc(ifa): return sum(1 for x in ifa if x.get("ph_rule_hits"))
def anch(ifa):
    hs = [h for x in ifa for h in (x.get("ph_rule_hits") or [])]
    return (sorted({h["his_resnum"] for h in hs}), sorted({h["anchor_resnum"] for h in hs}),
            (round(min(h["distance_A"] for h in hs), 2), round(max(h["distance_A"] for h in hs), 2)) if hs else None)
def perm_p(a, b):
    if len(a) < 2 or len(b) < 2: return None
    pool = a+b; n = len(a); tot = sum(pool)
    obs = abs(sum(a)/n - (tot-sum(a))/(len(pool)-n)); hit = c = 0
    for comb in itertools.combinations(pool, n):
        sa = sum(comb)
        if abs(sa/n - (tot-sa)/(len(pool)-n)) >= obs-1e-12: hit += 1
        c += 1
    return hit/c

runs = {}   # short -> {species: [counts per run]}
for d in R2:
    s = SHORT(d); runs[s] = {"human": [], "mouse": []}
    for sp in ("human", "mouse"):
        if d in R1: runs[s][sp].append(phc(R1[d]["%s_interface" % sp]))
        runs[s][sp].append(phc(R2[d][sp]["interface_per_sample"]))
        if d in R3: runs[s][sp].append(phc(R3[d]["%s_interface" % sp]))

out = []
out.append("#### pH rule across every independent run (bar: >= 7 of 10)\n")
out.append("| design | human, per run | human pooled | mouse, per run | mouse pooled | status |")
out.append("|---|---|---|---|---|---|")
order = sorted(runs, key=lambda s: (-sum(runs[s]["human"])/len(runs[s]["human"]), s))
for s in order:
    h, m = runs[s]["human"], runs[s]["mouse"]
    hk, hn = sum(h), 10*len(h); mk, mn = sum(m), 10*len(m)
    nclear = sum(1 for x in h if x >= BAR)
    if len(h) >= 2 and nclear == len(h): stat = "**CONFIRMED** (human, %d runs)" % len(h)
    elif len(h) >= 2 and nclear >= 1:    stat = "cleared %d of %d runs" % (nclear, len(h))
    elif h[0] >= BAR:                    stat = "provisional"
    else:                                stat = "below bar"
    lo, hi = wilson(hk, hn)
    out.append("| %s | %s | %d/%d [%.2f–%.2f] | %s | %d/%d | %s |"
               % (s, ", ".join("%d/10" % x for x in h), hk, hn, lo, hi,
                  ", ".join("%d/10" % x for x in m), mk, mn, stat))

out.append("\n#### Mouse arm of the two confirmed designs\n")
out.append("| design | per run | pooled | P(>= k \\| p0 = 2/3) | reading |")
out.append("|---|---|---|---|---|")
for s in ("l69_mpnn1", "l91_mpnn1"):
    m = runs[s]["mouse"]; mk, mn = sum(m), 10*len(m)
    nclear = sum(1 for x in m if x >= BAR)
    out.append("| %s | %s | %d/%d | %.3f | cleared the bar in %d of %d runs |"
               % (s, ", ".join("%d/10" % x for x in m), mk, mn, tge(mk, mn, P0), nclear, len(m)))

out.append("\n#### Anchor reproducibility (human arm)\n")
out.append("| design | run 2 | run 3 |")
out.append("|---|---|---|")
for s, d in (("l69_mpnn1","tnfa_l69_s930894_mpnn1"), ("l91_mpnn1","tnfa_l91_s990274_mpnn1")):
    h2, a2, _ = anch(R2[d]["human"]["interface_per_sample"])
    h3, a3, _ = anch(R3[d]["human_interface"])
    out.append("| %s | His%s → %s | His%s → %s |" % (s, h2, a2, h3, a3))

out.append("\n#### Species comparison, 12 designs at n=10 (Amendments 5 and 6)\n")
out.append("| design | human mean [range] | mouse mean [range] | diff | pre-registered verdict | exact permutation p |")
out.append("|---|---|---|---|---|---|")
for d in sorted(R2, key=lambda x: SHORT(x)):
    h, m = R2[d]["human"], R2[d]["mouse"]
    hs = [x for x in (h.get("ipsae_min_samples") or []) if x is not None]
    ms = [x for x in (m.get("ipsae_min_samples") or []) if x is not None]
    if len(hs) < 2 or len(ms) < 2:
        out.append("| %s | n=%d usable | n=%d usable | — | **NOT MEASURABLE** (Am. 6) | — |"
                   % (SHORT(d), len(hs), len(ms))); continue
    hm, mm = sum(hs)/len(hs), sum(ms)/len(ms)
    hr, mr = max(hs)-min(hs), max(ms)-min(ms)
    diff = hm-mm; floor = max(hr, mr)
    out.append("| %s | %.4f [%.4f] | %.4f [%.4f] | %+.4f | %s | %.2e |"
               % (SHORT(d), hm, hr, mm, mr, diff,
                  "**REAL**" if abs(diff) > floor else "indistinguishable", perm_p(hs, ms)))

AF2 = ["l69_mpnn2","l69_mpnn1","l91_mpnn2","l91_mpnn1","l66_mpnn2","l87_mpnn1"]
y = [runs[s]["human"][-1] if s not in ("l69_mpnn1",) else runs[s]["human"][1] for s in AF2]
y = [phc(R2["tnfa_"+[d for d in R2 if SHORT(d)==s][0].split("tnfa_")[1]]["human"]["interface_per_sample"]) for s in AF2]
n = [phc(R2[d]["human"]["interface_per_sample"]) for d in R2 if SHORT(d) not in AF2]
pool = y+n; obs = abs(sum(y)/len(y)-sum(n)/len(n)); tot = sum(pool); k = len(y)
hit = c = 0
for comb in itertools.combinations(pool, k):
    sa = sum(comb)
    if abs(sa/k-(tot-sa)/(len(pool)-k)) >= obs-1e-12: hit += 1
    c += 1
out.append("\n#### Did the AlphaFold2 screen predict the independent predictor?\n")
out.append("| AF2 call | Boltz human counts (12-design run) | mean |")
out.append("|---|---|---|")
out.append("| pH-positive (6 designs) | %s | **%.2f/10** |" % (", ".join(str(x) for x in sorted(y, reverse=True)), sum(y)/len(y)))
out.append("| pH-negative (6 designs) | %s | **%.2f/10** |" % (", ".join(str(x) for x in sorted(n, reverse=True)), sum(n)/len(n)))
out.append("\nExact permutation test on the group difference: **p = %.4f** (%d of %d splits)." % (hit/c, hit, c))

txt = "\n".join(out) + "\n"
open("challenges/tnfa/generated-tables.md", "w").write(txt)
print(txt)
