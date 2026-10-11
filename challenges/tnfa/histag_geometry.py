import sys
from collections import defaultdict
rows=[]
for l in open(sys.argv[1]):
    if l.startswith('ATOM') and l[76:78].strip()!='H':
        rows.append((l[21],int(l[22:26]),l[17:20].strip(),l[12:16].strip(),
                     float(l[30:38]),float(l[38:46]),float(l[46:54]),float(l[60:66])))
print("1) SIDE-CHAIN QUALITY of the two proposed pH anchors (7KPB, 3.00 A)")
print("   if a guanidinium/ammonium is missing or has a high B-factor, the distance is soft")
for c in 'ABC':
    for n,tgt in ((32,('NH1','NH2','NE','CZ')),(65,('NZ','CE')),(90,('NZ','CE'))):
        got=[(a,b) for cc,nn,rn,a,x,y,z,b in rows if cc==c and nn==n and a in tgt]
        bb=[b for _,b in got]
        allb=[b for cc,nn,rn,a,x,y,z,b in rows if cc==c and nn==n]
        if not allb: continue
        state = "side chain MISSING" if not got else f"B={min(bb):.0f}-{max(bb):.0f}"
        print(f"   chain {c} res {n:>3}: {len(got)}/{len(tgt)} tip atoms  {state}   (res mean B={sum(allb)/len(allb):.0f})")

print("\n2) *** THE HIS-TAG CONTRAINDICATION ***")
print("   mouse assay construct TNA-M52H3 carries a C-TERMINAL POLYHISTIDINE TAG.")
print("   A His tag is itself a cluster of titratable histidines. If the C-terminus")
print("   sits near the receptor groove, it lands on top of our pH mechanism --")
print("   and it is present ONLY in the mouse arm (human TNA-H4211 is tag-free).")
ca={(c,n):(x,y,z) for c,n,rn,a,x,y,z,b in rows if a=='CA'}
cterm={}
for c in 'ABC':
    ns=[n for (cc,n) in ca if cc==c]
    if ns: cterm[c]=max(ns)
print(f"   last modelled residue per TNF chain: {cterm}")
def d(p,q): return ((p[0]-q[0])**2+(p[1]-q[1])**2+(p[2]-q[2])**2)**.5
print(f"\n   distance from each C-terminus to the B+C groove hotspots (Ca-Ca):")
print(f"   {'':>12} " + " ".join(f"{'B'+str(h):>7}" for h in (32,65,143,145,146)) + " " + " ".join(f"{'C'+str(h):>7}" for h in (86,87,90)))
for c,last in sorted(cterm.items()):
    p=ca[(c,last)]
    cells=[]
    for ch,h in [('B',32),('B',65),('B',143),('B',145),('B',146),('C',86),('C',87),('C',90)]:
        q=ca.get((ch,h)); cells.append(f"{d(p,q):7.1f}" if q else "    n/a")
    print(f"   {c}-term ({last}) " + " ".join(cells))
print("\n   >25 A = tag cannot reach the groove even extended; <15 A = real confound risk")
