import sys, itertools
from collections import defaultdict
CAT={'ARG':('NH1','NH2','NE'),'LYS':('NZ',),'HIS':('ND1','NE2')}
want={32:'ARG',65:'LYS',82:'ARG',90:'LYS'}
at=defaultdict(dict)
for l in open(sys.argv[1]):
    if l.startswith('ATOM'):
        n=int(l[22:26]); c=l[21]; rn=l[17:20].strip(); an=l[12:16].strip()
        if n in want and rn==want[n] and an in CAT.get(rn,()):
            at[c].setdefault(n,[]).append((float(l[30:38]),float(l[38:46]),float(l[46:54])))
def d(p,q): return min(((a[0]-b[0])**2+(a[1]-b[1])**2+(a[2]-b[2])**2)**.5 for a in p for b in q)
print("conserved cations present per TNF chain:", {c:sorted(v) for c,v in sorted(at.items()) if c in 'ABC'})
print("\n=== pairwise min distance between cationic N atoms, ACROSS the B+C groove ===")
print("   (binder sits in one groove; it can only reach anchors that are mutually close)")
rows=[]
for (c1,c2) in (('B','C'),('C','B'),('B','B'),('C','C')):
    for n1 in sorted(at.get(c1,{})):
        for n2 in sorted(at.get(c2,{})):
            if (c1,n1)>=(c2,n2): continue
            dd=d(at[c1][n1],at[c2][n2]); rows.append((dd,f"{c1}{n1}",f"{c2}{n2}"))
for dd,a,b in sorted(rows):
    reach="BOTH REACHABLE by one binder face" if dd<=20 else ("marginal" if dd<=28 else "too far apart")
    print(f"   {a:>5} <-> {b:<5}  {dd:6.1f} A   {reach}")
