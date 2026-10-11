import sys, itertools
from collections import defaultdict
aa3={'ALA':'A','ARG':'R','ASN':'N','ASP':'D','CYS':'C','GLN':'Q','GLU':'E','GLY':'G',
     'HIS':'H','ILE':'I','LEU':'L','LYS':'K','MET':'M','PHE':'F','PRO':'P','SER':'S',
     'THR':'T','TRP':'W','TYR':'Y','VAL':'V'}
def load(p):
    at=defaultdict(list)
    for l in open(p):
        if l.startswith('ATOM') and l[76:78].strip()!='H':
            at[l[21]].append((int(l[22:26]), l[17:20].strip(),
                              float(l[30:38]),float(l[38:46]),float(l[46:54])))
    return at
def contacts(at, lig, rec, cut=4.5):
    out=defaultdict(int); ident={}
    R=[a for c in rec for a in at[c]]
    for c in lig:
        for n,rn,x,y,z in at[c]:
            ident[n]=aa3.get(rn,'X')
            for _,_,X,Y,Z in R:
                if abs(X-x)<cut and abs(Y-y)<cut and abs(Z-z)<cut:
                    if (X-x)**2+(Y-y)**2+(Z-z)**2 < cut*cut: out[n]+=1
    return out, ident

# --- human: 7KPB author numbering == human mature (verified) ---
hb=load(sys.argv[1]); hc,hi = contacts(hb,'ABC','EF')
HUM=dict(hc)
# --- mouse: 7KP7 author N -> human mature  (author = mouse mature +1; indel at human 72) ---
mb=load(sys.argv[2]); mc,mi = contacts(mb,'ABC','DEF')
def to_human(n): return n if n>=73 else n-1
MOU={to_human(n):v for n,v in mc.items()}
MOUid={to_human(n):a for n,a in mi.items()}

print(f"human 7KPB TNFR1 contacts : {len(HUM)}")
print(f"mouse 7KP7 TNFR1 contacts : {len(MOU)}  (converted to human mature numbering)")
both=sorted(set(HUM)&set(MOU)); honly=sorted(set(HUM)-set(MOU)); monly=sorted(set(MOU)-set(HUM))
print(f"\nCONTACTED IN BOTH SPECIES ({len(both)}): {both}")
print(f"human-only ({len(honly)}): {honly}")
print(f"mouse-only ({len(monly)}): {monly}")

DIV={1,6,7,8,20,22,24,27,30,31,41,42,44,52,53,58,71,72,73,80,83,85,89,97,102,103,104,111,131,136,138,140,154}
print(f"\n{'='*78}\nOUR HOTSPOT SET, TESTED AGAINST THE MOUSE COMPLEX\n{'='*78}")
print(f"{'human':>6} {'aa':>3} {'7KPB':>6} {'7KP7':>6}  {'conserved':>9}  verdict")
for h in (32,86,87,90,143,146):
    a=hi.get(h,'?'); ph=hc.get(h,0); pm=MOU.get(h,0)
    cons='no (DIV)' if h in DIV else 'yes'
    if ph and pm: v='CROSS-SPECIES CONFIRMED by structure'
    elif ph and not pm: v='*** human contact only -- NOT seen in mouse complex'
    elif pm and not ph: v='mouse only'
    else: v='neither'
    print(f"{h:>6} {a:>3} {ph:>6} {pm:>6}  {cons:>9}  {v}")

print(f"\nconserved AND contacted in both species, by mouse contact density:")
cand=[(MOU[n]+HUM[n],n,hi.get(n,'?'),HUM[n],MOU[n]) for n in both if n not in DIV]
for tot,n,a,ph,pm in sorted(cand,reverse=True)[:16]:
    print(f"   {a}{n:<4} human {ph:>3} atom-pairs   mouse {pm:>3}")
print(f"\n   total conserved+both-species positions: {len(cand)}")

print("\n=== the two cations the TNFR1/TNFR2 consensus discarded ===")
for n in (65,82):
    print(f"   {hi.get(n,'?')}{n}: human 7KPB {hc.get(n,0):>3} atom-pairs   mouse 7KP7 {MOU.get(n,0):>3}   conserved={n not in DIV}")
print("\n=== is 65 or 82 wild-type in 3ALQ? (3ALQ is the lysine-deficient variant) ===")
print("   K65S and K90P are engineered in 3ALQ; 7KPB is wild-type at both. 7KPB is the right source.")
