import csv, glob, re, subprocess, os, sys
os.chdir(os.path.expanduser('~/mnt/adaptyv-2026'))
W=open('challenges/tnfa/submission-writeup.md').read()
sub=list(csv.DictReader(open('challenges/tnfa/submission.csv')))
src={}
for fp in glob.glob('challenges/tnfa/v2-core*/**/final_design_stats.csv',recursive=True):
    for r in csv.DictReader(open(fp)):
        if r.get('Design') and r.get('Sequence') and r['Design'] not in src: src[r['Design']]=r
fails=[]
def chk(ok,msg):
    print(("  ok   " if ok else "  FAIL ")+msg)
    if not ok: fails.append(msg)

print("=== 1. CSV <-> writeup: identity, order, length ===")
tbl=re.findall(r'^\|\s*(\d+)\s*\|\s*(tnfa_\S+)\s*\|\s*(\d+)\s*\|', W, re.M)
chk(len(tbl)==len(sub), "writeup lists %d designs, csv has %d" % (len(tbl),len(sub)))
for (idx,name,ln),row in zip(tbl,sub):
    chk(name==row['name'], "#%s %s == csv %s" % (idx,name,row['name']))
    chk(int(ln)==len(row['sequence']), "#%s %s len %s == seq %d" % (idx,name,ln,len(row['sequence'])))

print("\n=== 2. histidine claims vs submitted sequences ===")
claims={'tnfa_l69_s930894_mpnn2':[4],'tnfa_l69_s930894_mpnn1':[4],
        'tnfa_l91_s990274_mpnn2':[15,16],'tnfa_l91_s990274_mpnn1':[15,16],
        'tnfa_l66_s937529_mpnn2':[32],'tnfa_l87_s136696_mpnn1':[27],
        'tnfa_l66_s937529_mpnn1':[32],'tnfa_l60_s347619_mpnn2':[17],
        'tnfa_l60_s347619_mpnn1':[17],'tnfa_l62_s149973_mpnn20':[30,34,35],
        'tnfa_l97_s762214_mpnn2':[72]}
seqs={r['name']:r['sequence'] for r in sub}
for n,ps in claims.items():
    s=seqs.get(n)
    chk(s is not None and all(p<=len(s) and s[p-1]=='H' for p in ps), "%s His%s present" % (n,ps))
chk(seqs['tnfa_l84_s861729_mpnn1'].count('H')==0, "l84_mpnn1 has no histidine, as claimed")

print("\n=== 3. metrics in writeup table vs source CSVs ===")
rows=re.findall(r'^\|\s*(l\d+_mpnn\d+)\s*\|\s*(\d+)\s*\|\s*([\d.]+)\s*\|\s*\*{0,2}([\d.]+)\*{0,2}\s*\|\s*\*{0,2}(−?-?[\d.]+)\*{0,2}\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*\*{0,2}([\d.]+)\*{0,2}\s*\|', W, re.M)
print("  parsed %d metric rows" % len(rows))
for short,ln,iptm,sc,dg,ds,hb,uns in rows:
    m2=re.match(r'l(\d+)_mpnn(\d+)', short)
    full=[k for k in src if re.fullmatch(r'tnfa_l%s_s\d+_mpnn%s' % (m2.group(1),m2.group(2)), k)] if m2 else []
    if not full: chk(False,"%s: no source row"%short); continue
    r=src[full[0]]
    def cl(a,b,t=0.011): return abs(float(a)-float(b))<=t
    chk(int(ln)==len(r['Sequence']), "%s len %s" % (short,ln))
    chk(cl(iptm,r['Average_i_pTM']), "%s i_pTM %s vs %.4f" % (short,iptm,float(r['Average_i_pTM'])))
    chk(cl(sc,r['Average_ShapeComplementarity']), "%s SC %s vs %.4f" % (short,sc,float(r['Average_ShapeComplementarity'])))
    chk(cl(dg.replace('−','-'),r['Average_dG'],0.06), "%s dG %s vs %.2f" % (short,dg,float(r['Average_dG'])))
    chk(abs(int(ds)-float(r['Average_dSASA']))<1.0, "%s dSASA %s vs %.1f" % (short,ds,float(r['Average_dSASA'])))
    chk(abs(int(hb)-float(r['Average_n_InterfaceHbonds']))<0.51, "%s Hb %s vs %s" % (short,hb,r['Average_n_InterfaceHbonds']))
    chk(cl(uns,r['Average_InterfaceUnsatHbondsPercentage'],0.06), "%s unsat %s vs %.2f" % (short,uns,float(r['Average_InterfaceUnsatHbondsPercentage'])))

print("\n=== 4. funnel vs committed logs ===")
logs={'v1-core':'challenges/tnfa/tnfa-v1-core.log','v2-smoke':'challenges/tnfa/tnfa-v2-smoke.log',
      'v2-core':'challenges/tnfa/tnfa-v2-core.log','v2-core2':'challenges/tnfa/tnfa-v2-core2.log'}
tot=cl2=nm=0
for k,p in logs.items():
    t=open(p,errors='replace').read()
    a=t.count('Starting trajectory:'); b=t.count('Severe clashes'); c=t.count('No accepted MPNN')
    print("    %-9s traj=%3d clashes=%2d no-MPNN=%2d" % (k,a,b,c)); tot+=a; cl2+=b; nm+=c
print("    TOTAL     traj=%d clashes=%d no-MPNN=%d" % (tot,cl2,nm))
def claim(pat):
    m=re.search(pat,W); return int(m.group(1)) if m else None
pairs=[(r'BindCraft trajectories started \| (\d+)',tot,'trajectories'),
       (r'severe clashes \| (\d+)',cl2,'clashes'),
       (r'no accepted MPNN variant \| (\d+)',nm,'no-MPNN'),
       (r'production runs \| (\d+)',len(logs),'runs'),
       (r'full interface scoring \| (\d+)',len(src),'scored')]
for pat,actual,label in pairs:
    c=claim(pat); chk(c==actual, "%s: writeup %s vs actual %s" % (label,c,actual))
npass=sum(1 for r in src.values() if r.get('Average_ShapeComplementarity') not in (None,'','nan') and float(r['Average_ShapeComplementarity'])>=0.58)
c=claim(r'clearing SC . 0\.58 \| \*\*(\d+)\*\*'); chk(c==npass,"SC-passers: writeup %s vs actual %s"%(c,npass))
bb={re.match(r'(tnfa_l\d+_s\d+)',k).group(1) for k,r in src.items() if r.get('Average_ShapeComplementarity') not in (None,'','nan') and float(r['Average_ShapeComplementarity'])>=0.58}
c=claim(r'independent backbones among those \| \*\*(\d+)\*\*'); chk(c==len(bb),"backbones: writeup %s vs actual %s"%(c,len(bb)))

print("\n=== 5. every submitted design clears SC 0.58 ===")
for r in sub:
    sc=float(src[r['name']]['Average_ShapeComplementarity']); chk(sc>=0.58,"%s SC %.3f"%(r['name'],sc))

print("\n=== 6. provenance commits exist ===")
for h in sorted(set(re.findall(r'\| `([0-9a-f]{7})` \|', W))):
    ok=subprocess.run(['git','cat-file','-t',h],capture_output=True,text=True).stdout.strip()=='commit'
    chk(ok,"commit %s"%h)

print("\n=== 7. n=10 claims vs crossreact-n10.json ===")
import json as _json, statistics as _st
_NJ = "challenges/tnfa/crossreact-n10.json"
if not os.path.exists(_NJ):
    chk(False, "missing %s" % _NJ)
else:
    _JS = _json.load(open(_NJ))
    chk(_JS.get("diffusion_samples") == 10, "json diffusion_samples=%s" % _JS.get("diffusion_samples"))
    chk(_JS.get("aborted") is False, "json aborted=%s" % _JS.get("aborted"))
    _f = {}
    for _row in _JS["rows"]:
        for _sp in ("human", "mouse"):
            _ps, _if = _row["%s_ipsae_pairs" % _sp], _row["%s_interface" % _sp]
            _raw, _res, _ph, _dist, _anch, _both, _eng = [], [], 0, [], set(), 0, set()
            for _i in range(min(len(_ps), len(_if))):
                _ic = _if[_i]; _b = _ic["binder_chain"]
                _e = {c for c, v in _ic["per_chain"].items() if v.get("atom_pairs", 0) > 0}
                _eng.add(len(_e))
                _bp = [q for q in _ps[_i] if _b in (q["a"], q["b"])]
                if _bp: _raw.append(min(q["ipsae"] for q in _bp))
                _ep = [q for q in _bp if (q["b"] if q["a"] == _b else q["a"]) in _e]
                if _ep: _res.append(min(q["ipsae"] for q in _ep))
                _h = _ic.get("ph_rule_hits") or []
                if _h: _ph += 1
                for _x in _h:
                    _dist.append(_x["distance_A"]); _anch.add(_x["anchor_resnum"])
                if _ic.get("contacts_both_protomers"): _both += 1
            _key = (_row["design"].replace("tnfa_", "").replace("_s930894", "").replace("_s990274", ""), _sp)
            _f[_key] = dict(n=len(_raw),
                raw_m=round(sum(_raw)/len(_raw), 4), raw_r=round(max(_raw)-min(_raw), 4),
                raw_sd=round(_st.stdev(_raw), 4),
                res_m=round(sum(_res)/len(_res), 4),
                ph=_ph, both=_both, eng=sorted(_eng),
                dmin=round(min(_dist), 2) if _dist else None,
                dmax=round(max(_dist), 2) if _dist else None,
                anch=sorted(_anch))
    # pH proportions asserted in the writeup
    for _k, _want in ((("l69_mpnn1","human"),10), (("l69_mpnn1","mouse"),8),
                      (("l69_mpnn2","human"),4), (("l69_mpnn2","mouse"),4),
                      (("l91_mpnn2","human"),3), (("l91_mpnn2","mouse"),2)):
        _g = _f[_k]["ph"]
        chk(_g == _want, "pH %s %s: writeup %d/10 vs json %d/10" % (_k[0], _k[1], _want, _g))
    # parse the pH table out of the writeup so a typo there cannot pass
    # EVERY writeup row quoting an "N / 10" for a design must agree with the JSON.
    # Rows naming a bare design carry human then mouse; rows naming "<design>
    # <species>" carry that one arm. Both forms are checked, and an unparseable
    # row is a failure rather than a skip.
    for _dn in ("l69_mpnn1", "l69_mpnn2", "l91_mpnn2"):
        _jh, _jm = _f[(_dn, "human")]["ph"], _f[(_dn, "mouse")]["ph"]
        _rows = [l for l in W.splitlines()
                 if re.match(r"^\|\s*\*{0,2}%s\b" % re.escape(_dn), l)
                 and re.search(r"\d+\s*/\s*10", l)]
        chk(len(_rows) >= 1, "%s: at least one pH row present in writeup" % _dn)
        for _l in _rows:
            _sp = ("human" if re.match(r"^\|\s*\*{0,2}%s\*{0,2}\s+human" % re.escape(_dn), _l)
                   else "mouse" if re.match(r"^\|\s*\*{0,2}%s\*{0,2}\s+mouse" % re.escape(_dn), _l)
                   else None)
            _nums = [int(x) for x in re.findall(r"(\d+)\s*/\s*10", _l)]
            if _sp is None:
                chk(len(_nums) >= 2 and _nums[0] == _jh and _nums[1] == _jm,
                    "%s both-arm pH row %s vs json %d/%d" % (_dn, _nums, _jh, _jm))
            else:
                _wantv = _jh if _sp == "human" else _jm
                chk(len(_nums) >= 1 and _nums[0] == _wantv,
                    "%s %s pH row %s vs json %d" % (_dn, _sp, _nums, _wantv))

    # the >=7 bar decides tier 1 for exactly one design
    _pass = sorted({d for (d, sp) in _f if _f[(d, "human")]["ph"] >= 7 and _f[(d, "mouse")]["ph"] >= 7})
    chk(_pass == ["l69_mpnn1"], "both-arm pass set = %s (expected ['l69_mpnn1'])" % _pass)
    chk("| 1 | tnfa_l69_s930894_mpnn1 |" in W, "l69_mpnn1 occupies writeup slot 1")
    # Objective 2 table numbers
    for _d, _hm, _hr, _mm, _mr, _df, _fl in (
            ("l69_mpnn1", 0.5486, 0.1340, 0.2933, 0.1390, 0.2553, 0.1390),
            ("l69_mpnn2", 0.5192, 0.0920, 0.2673, 0.1945, 0.2519, 0.1945),
            ("l91_mpnn2", 0.5237, 0.2027, 0.4150, 0.2357, 0.1087, 0.2357)):
        _h, _m = _f[(_d, "human")], _f[(_d, "mouse")]
        chk(abs(_h["raw_m"] - _hm) < 5e-4, "%s human mean %s vs json %s" % (_d, _hm, _h["raw_m"]))
        chk(abs(_h["raw_r"] - _hr) < 5e-4, "%s human range %s vs json %s" % (_d, _hr, _h["raw_r"]))
        chk(abs(_m["raw_m"] - _mm) < 5e-4, "%s mouse mean %s vs json %s" % (_d, _mm, _m["raw_m"]))
        chk(abs(_m["raw_r"] - _mr) < 5e-4, "%s mouse range %s vs json %s" % (_d, _mr, _m["raw_r"]))
        chk(abs((_h["raw_m"] - _m["raw_m"]) - _df) < 1e-3, "%s diff %s" % (_d, _df))
        chk(abs(max(_h["raw_r"], _m["raw_r"]) - _fl) < 5e-4, "%s floor %s" % (_d, _fl))
        _verdict_real = abs(_h["raw_m"] - _m["raw_m"]) > max(_h["raw_r"], _m["raw_r"])
        _want_real = _d.startswith("l69")
        chk(_verdict_real == _want_real, "%s verdict REAL=%s as written" % (_d, _want_real))
        for _tok in ("%.4f" % _hm, "%.4f" % _mm):
            chk(_tok in W, "%s token %s present in writeup" % (_d, _tok))
    # restricted (post-hoc) values quoted in prose
    for _d, _rh, _rm in (("l69_mpnn1", 0.6711, 0.4061), ("l69_mpnn2", 0.6465, 0.3659),
                         ("l91_mpnn2", 0.6717, 0.5552)):
        chk(abs(_f[(_d,"human")]["res_m"] - _rh) < 5e-4, "%s restricted human %s vs json %s" % (_d, _rh, _f[(_d,"human")]["res_m"]))
        chk(abs(_f[(_d,"mouse")]["res_m"] - _rm) < 5e-4, "%s restricted mouse %s vs json %s" % (_d, _rm, _f[(_d,"mouse")]["res_m"]))
    # parse the objective-2 table out of the writeup (same gap class as the pH table)
    for _dn in ("l69_mpnn1", "l69_mpnn2", "l91_mpnn2"):
        _m = re.search(r"^\|\s*%s\s*\|\s*([\d.]+)\s*\[([\d.]+)\]\s*\|\s*([\d.]+)\s*\[([\d.]+)\]"
                       % re.escape(_dn), W, re.M)
        if not _m:
            chk(False, "%s: objective-2 table row not found in writeup" % _dn); continue
        _wh, _whr, _wm, _wmr = (float(x) for x in _m.groups())
        _h, _mo = _f[(_dn, "human")], _f[(_dn, "mouse")]
        chk(abs(_wh - _h["raw_m"]) < 5e-5 and abs(_whr - _h["raw_r"]) < 5e-5
            and abs(_wm - _mo["raw_m"]) < 5e-5 and abs(_wmr - _mo["raw_r"]) < 5e-5,
            "%s writeup obj-2 row %s/%s %s/%s vs json %s/%s %s/%s"
            % (_dn, _wh, _whr, _wm, _wmr, _h["raw_m"], _h["raw_r"], _mo["raw_m"], _mo["raw_r"]))

    # binomial figures quoted in objective 3
    import math as _math
    import math
    def _tle(k, n, p):
        return sum(_math.comb(n, i) * p**i * (1-p)**(n-i) for i in range(0, k+1))
    def _tge(k, n, p):
        return sum(_math.comb(n, i) * p**i * (1-p)**(n-i) for i in range(k, n+1))
    import itertools as _it, statistics as _sst
    _p0 = 2/3
    # parse EVERY "P(>=k | p0) = x" / "P(<=k | p0) = x" claim out of the writeup
    # and recompute it, rather than comparing against a literal duplicated here.
    _pc = re.findall(r"P\((\u2265|\u2264)\s*(\d+)\s*\\?\|\s*p\u2080\)\s*=\s*([\d.]+)", W)
    chk(len(_pc) >= 2, "found %d prose binomial P(...) claims in writeup" % len(_pc))
    for _rel, _k, _q in _pc:
        _k = int(_k); _got = _tge(_k, 10, _p0) if _rel == "\u2265" else _tle(_k, 10, _p0)
        _dp = len(_q.split(".")[1]) if "." in _q else 0
        chk(("%%.%df" % _dp) % _got == _q,
            "writeup P(%s%d|p0)=%s vs computed %s" % (_rel, _k, _q, ("%%.%df" % _dp) % _got))

    # the binomial table itself: every k, every Wilson bound, every P(<=k) cell
    def _wil(k, n, z=1.96):
        ph = k / n; dd = 1 + z*z/n
        cc = (ph + z*z/(2*n)) / dd
        hw = z * math.sqrt(ph*(1-ph)/n + z*z/(4*n*n)) / dd
        return (max(0.0, cc-hw), min(1.0, cc+hw))
    _brows = re.findall(
        r"^\|\s*(l\d+_mpnn\d+)\s+(human|mouse)\s*\|\s*(\d+)/10\s*\|\s*"
        r"([\d.]+)\s*[\u2013-]\s*([\d.]+)\s*\|\s*([^|]*?)\s*\|", W, re.M)
    chk(len(_brows) == 6, "binomial table has %d parsed rows (expected 6)" % len(_brows))
    for _bd, _bsp, _bk, _blo, _bhi, _bp in _brows:
        _bk = int(_bk)
        chk(_bk == _f[(_bd, _bsp)]["ph"],
            "binomial table %s %s k=%d vs json %d" % (_bd, _bsp, _bk, _f[(_bd, _bsp)]["ph"]))
        _wl, _wh2 = _wil(_bk, 10)
        chk(("%.2f" % _wl) == _blo and ("%.2f" % _wh2) == _bhi,
            "binomial table %s %s Wilson %s-%s vs computed %.2f-%.2f"
            % (_bd, _bsp, _blo, _bhi, _wl, _wh2))
        _bps = _bp.strip().strip("*")
        if re.fullmatch(r"[\d.]+", _bps):
            _dp2 = len(_bps.split(".")[1]) if "." in _bps else 0
            _exp2 = ("%%.%df" % _dp2) % _tle(_bk, 10, _p0)
            chk(_exp2 == _bps, "binomial table %s %s P(<=%d)=%s vs computed %s"
                % (_bd, _bsp, _bk, _bps, _exp2))

    # exact permutation counts behind the sensitivity analysis
    _want = {"l69_mpnn1": 2, "l69_mpnn2": 2, "l91_mpnn2": 814}
    for _row in _JS["rows"]:
        _k = _row["design"].replace("tnfa_", "").replace("_s930894", "").replace("_s990274", "")
        _hs, _ms = _row["human_samples"], _row["mouse_samples"]
        _obs = abs(_sst.mean(_hs) - _sst.mean(_ms)); _pool = _hs + _ms; _n = len(_hs)
        _cnt = _tot = 0
        for _combo in _it.combinations(range(len(_pool)), _n):
            _cs = set(_combo)
            _a = [_pool[i] for i in _combo]
            _b = [_pool[i] for i in range(len(_pool)) if i not in _cs]
            _tot += 1
            if abs(_sst.mean(_a) - _sst.mean(_b)) >= _obs - 1e-12: _cnt += 1
        chk(_tot == 184756, "%s permutation space %d vs 184756" % (_k, _tot))
        chk(_cnt == _want[_k], "%s permutation count %d vs quoted %d" % (_k, _cnt, _want[_k]))
    _SUP = str.maketrans("\u207b\u2070\u00b9\u00b2\u00b3\u2074\u2075\u2076\u2077\u2078\u2079",
                         "-0123456789")
    _pp = re.findall(r"\|\s*(l\d+_mpnn\d+)\s*\|[^|]*\|[^|]*\|\s*\*{0,2}\s*([\d.]+)\s*\u00d7\s*10([\u207b\u2070-\u2079\u00b9\u00b2\u00b3]+)\s*\*{0,2}\s*\|", W)
    chk(len(_pp) == 3, "found %d permutation-p table rows (expected 3)" % len(_pp))
    for _dn2, _mant, _exp in _pp:
        _claim = float(_mant) * 10 ** int(_exp.translate(_SUP))
        _row = next(r for r in _JS["rows"] if _dn2.split("_")[0] in r["design"]
                    and r["design"].endswith(_dn2.split("_")[1]))
        _hs, _ms = _row["human_samples"], _row["mouse_samples"]
        _obs = abs(_sst.mean(_hs) - _sst.mean(_ms)); _pool = _hs + _ms; _n = len(_hs)
        _cnt = _tot = 0
        for _combo in _it.combinations(range(len(_pool)), _n):
            _cs = set(_combo)
            _a2 = [_pool[i] for i in _combo]
            _b2 = [_pool[i] for i in range(len(_pool)) if i not in _cs]
            _tot += 1
            if abs(_sst.mean(_a2) - _sst.mean(_b2)) >= _obs - 1e-12: _cnt += 1
        _true = _cnt / _tot
        chk(abs(_claim - _true) / _true < 0.06,
            "%s writeup permutation p=%.2e vs computed %.2e" % (_dn2, _claim, _true))
    chk("184,756" in W, "writeup states the permutation space size")
    chk(W.count("0.06\u20130.79") >= 1, "writeup states the 1-of-3 Wilson interval")

    # engagement claim: all 60 samples, exactly 2 of 3 protomers, both-protomer true
    _tot = sum(v["n"] for v in _f.values())
    chk(_tot == 60, "total samples 60 vs %d" % _tot)
    chk(all(v["eng"] == [2] for v in _f.values()), "every sample engaged exactly 2 protomers")
    chk(all(v["both"] == v["n"] for v in _f.values()), "contacts_both_protomers true in every sample")
    # anchor identity and distance span for the lead
    chk(_f[("l69_mpnn1","human")]["anch"] == [32], "lead human anchor is R32 only, got %s" % _f[("l69_mpnn1","human")]["anch"])
    chk(_f[("l69_mpnn1","mouse")]["anch"] == [65], "lead mouse anchor is K65 only, got %s" % _f[("l69_mpnn1","mouse")]["anch"])
    chk("2.55\u20135.68" in W or "2.55-5.68" in W, "lead human distance span 2.55-5.68 in writeup")
    chk(abs(_f[("l69_mpnn1","human")]["dmin"] - 2.55) < 1e-9 and abs(_f[("l69_mpnn1","human")]["dmax"] - 5.68) < 1e-9,
        "lead human distances %s-%s" % (_f[("l69_mpnn1","human")]["dmin"], _f[("l69_mpnn1","human")]["dmax"]))
    chk(abs(_f[("l69_mpnn1","mouse")]["dmin"] - 4.04) < 1e-9 and abs(_f[("l69_mpnn1","mouse")]["dmax"] - 5.64) < 1e-9,
        "lead mouse distances %s-%s" % (_f[("l69_mpnn1","mouse")]["dmin"], _f[("l69_mpnn1","mouse")]["dmax"]))
    # SD spans quoted in limitation 8
    _hsd = sorted(_f[(d,"human")]["raw_sd"] for d in {k[0] for k in _f})
    _msd = sorted(_f[(d,"mouse")]["raw_sd"] for d in {k[0] for k in _f})
    for _label, _pat, _got in (
            ("human", r"human arm is tight \(SD\s+([\d.]+)[\u2013-]([\d.]+)\)", _hsd),
            ("mouse", r"mouse arm looser \(SD\s+([\d.]+)[\u2013-]([\d.]+)\)", _msd)):
        _m = re.search(_pat, W)
        if not _m:
            chk(False, "%s SD span not found in writeup" % _label); continue
        _lo, _hi = _m.group(1), _m.group(2)
        chk(_lo == "%.3f" % _got[0] and _hi == "%.3f" % _got[-1],
            "%s SD span: writeup %s-%s vs json %.3f-%.3f"
            % (_label, _lo, _hi, _got[0], _got[-1]))

print("\n"+"="*60)
print("ALL CHECKS PASS" if not fails else "%d FAILURES" % len(fails))
for f in fails: print("  - "+f)
sys.exit(1 if fails else 0)
