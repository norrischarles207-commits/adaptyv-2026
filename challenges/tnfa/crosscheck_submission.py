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

print("\n=== 7. writeup tables vs raw run data (regenerated, not trusted) ===")
import subprocess as _sp
_r = _sp.run([sys.executable, "-I", "challenges/tnfa/make_tables.py"],
             capture_output=True, text=True)
chk(_r.returncode == 0, "make_tables.py regenerates from raw data"
    + ("" if _r.returncode == 0 else ": " + _r.stderr.strip()[-300:]))
if _r.returncode == 0:
    _T = open("challenges/tnfa/generated-tables.md").read()
    _rows = [l.rstrip() for l in _T.splitlines()
             if l.startswith("| ") and set(l.strip()) - set("|- ")]
    _miss = [l for l in _rows if l not in W]
    chk(not _miss, "all %d generated table rows appear verbatim in the writeup%s"
        % (len(_rows), "" if not _miss else "  MISSING e.g. %r" % _miss[0]))
    _sent = [l for l in _T.splitlines()
             if l.startswith("Exact permutation test on the group difference")]
    chk(bool(_sent) and _sent[0] in W, "AF2 screen permutation sentence verbatim")

    # independent invariants that do not come from the generated tables
    import json as _json, re as _re
    _R2 = _json.load(open("challenges/tnfa/crossreact-all12-n10.json.partial"))["raw_rows"]
    _R3 = {x["design"]: x for x in _json.load(open("challenges/tnfa/crossreact-rep2.json"))["rows"]}
    _R1 = {x["design"]: x for x in _json.load(open("challenges/tnfa/crossreact-n10.json"))["rows"]}
    def _ph(ifa): return sum(1 for x in ifa if x.get("ph_rule_hits"))
    _conf = []
    for _d in _R2:
        _runs = []
        if _d in _R1: _runs.append(_ph(_R1[_d]["human_interface"]))
        _runs.append(_ph(_R2[_d]["human"]["interface_per_sample"]))
        if _d in _R3: _runs.append(_ph(_R3[_d]["human_interface"]))
        if len(_runs) >= 2 and all(x >= 7 for x in _runs):
            _conf.append(_re.sub(r"_s\d+", "", _d.replace("tnfa_", "")))
    chk(sorted(_conf) == ["l69_mpnn1", "l91_mpnn1"],
        "designs confirmed on >=2 runs = %s" % sorted(_conf))
    for _n, _slot in (("tnfa_l69_s930894_mpnn1", 1), ("tnfa_l91_s990274_mpnn1", 2)):
        chk(sub[_slot-1]["name"] == _n,
            "csv slot %d is %s (got %s)" % (_slot, _n, sub[_slot-1]["name"]))
        chk("| %d | %s |" % (_slot, _n) in W, "writeup slot %d is %s" % (_slot, _n))
    _neg = _ph(_R2["tnfa_l84_s861729_mpnn1"]["human"]["interface_per_sample"]) \
         + _ph(_R2["tnfa_l84_s861729_mpnn1"]["mouse"]["interface_per_sample"])
    chk(_neg == 0, "negative control l84_mpnn1 scores 0 on both arms (got %d)" % _neg)
    _eng = sum(1 for _d in _R2 for _sp2 in ("human","mouse")
               for x in _R2[_d][_sp2]["interface_per_sample"] if x.get("contacts_both_protomers"))
    _tot = sum(len(_R2[_d][_sp2]["interface_per_sample"]) for _d in _R2 for _sp2 in ("human","mouse"))
    chk(_eng == _tot == 240, "engagement %d/%d both protomers" % (_eng, _tot))
    chk("240 of 240" in W, "writeup states the 240/240 engagement figure")

print("\n"+"="*60)
print("ALL CHECKS PASS" if not fails else "%d FAILURES" % len(fails))
for f in fails: print("  - "+f)
sys.exit(1 if fails else 0)
