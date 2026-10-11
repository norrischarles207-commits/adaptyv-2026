"""Design-level metrics from BindCraft final_design_stats blocks in a run log.
Data rows carry a pandas index, so each field sits one token right of its header."""
import re, sys
want=['Average_i_pTM','Average_ShapeComplementarity','Average_dG','Average_dSASA',
      'Average_Relaxed_Clashes','Average_n_InterfaceHbonds',
      'Average_InterfaceUnsatHbondsPercentage','Average_Surface_Hydrophobicity']
rows=[]; seen=set()
for path in sys.argv[1:]:
    hdr=None
    for l in open(path):
        s=l.split()
        if s[:3]==['Rank','Design','Protocol']: hdr=s; continue
        if hdr and len(s)>12 and re.fullmatch(r'tnfa_l\d+_s\d+_mpnn\d+', s[2]):
            if s[2] in seen: continue
            seen.add(s[2])
            r={'Design':s[2],'Length':s[4],'src':path.split('-')[-1].replace('.log','')}
            for w in want:
                if w in hdr:
                    i=hdr.index(w)+1
                    if i<len(s): r[w]=s[i]
            rows.append(r)
def g(r,k):
    try: return float(r.get(k,'nan'))
    except: return float('nan')
rows.sort(key=lambda r:-g(r,'Average_i_pTM'))
print(f"  {'DESIGN':26}{'blk':>6}{'len':>4}{'i_pTM':>7}{'SC':>6}{'dG':>8}{'dSASA':>7}{'Hb':>4}{'uns%':>6}  SC gate")
npass=0; backbones=set()
for r in rows:
    sc=g(r,'Average_ShapeComplementarity'); ok=sc>=0.58; npass+=ok
    if ok: backbones.add(re.match(r'(tnfa_l\d+_s\d+)',r['Design']).group(1))
    print(f"  {r['Design']:26}{r['src']:>6}{r['Length']:>4}{g(r,'Average_i_pTM'):>7.2f}{sc:>6.2f}"
          f"{g(r,'Average_dG'):>8.1f}{g(r,'Average_dSASA'):>7.0f}"
          f"{g(r,'Average_n_InterfaceHbonds'):>4.0f}"
          f"{g(r,'Average_InterfaceUnsatHbondsPercentage'):>6.1f}  {'PASS' if ok else 'fail'}")
print(f"\n  designs scored: {len(rows)}   passing SC>=0.58: {npass}")
print(f"  distinct passing backbones: {len(backbones)}  {sorted(backbones)}")
print(f"  v1 best reference: SC 0.65  dG -33.5  dSASA 1444  Hb 8")
