import sys
from collections import defaultdict
def load(p):
    at=defaultdict(list)
    for l in open(p):
        if l.startswith('ATOM') and l[76:78].strip()!='H':
            at[l[21]].append((int(l[22:26]),l[17:20].strip(),
                float(l[30:38]),float(l[38:46]),float(l[46:54])))
    return at
def pairs(at,c1,c2,cut=4.5):
    n=0; res=set()
    B=at[c2]
    for r,rn,x,y,z in at[c1]:
        for _,_,X,Y,Z in B:
            if abs(X-x)<cut and abs(Y-y)<cut and abs(Z-z)<cut and (X-x)**2+(Y-y)**2+(Z-z)**2<cut*cut:
                n+=1; res.add(r); break
    return n,sorted(res)
f=sys.argv[1]; at=load(f)
tnf=[c for c in 'ABC' if c in at]
rec=[c for c in sys.argv[2] if c in at]
other=[c for c in sys.argv[3] if c in at] if len(sys.argv)>3 else []
print(f"### {f}  TNF={tnf} receptor={rec} other={other}")
print("\n--- which TNF protomers does each receptor chain engage? ---")
for rc in rec:
    tot=[]
    for tc in tnf:
        n,res=pairs(at,tc,rc)
        if n: tot.append((n,tc,res))
    tot.sort(reverse=True)
    desc="  ".join(f"{tc}:{n}res" for n,tc,_ in tot)
    groove="+".join(tc for n,tc,_ in tot if n>=5)
    print(f"  receptor {rc}: {desc}      -> groove {groove}")
    for n,tc,res in tot:
        if n>=5: print(f"        {tc} contacts: {res}")
if other:
    print("\n--- does the Fab touch our epitope on B or C? ---")
    for oc in other:
        for tc in tnf:
            n,res=pairs(at,tc,oc)
            if n: print(f"  Fab {oc} <-> TNF {tc}: {n} residues {res}")
