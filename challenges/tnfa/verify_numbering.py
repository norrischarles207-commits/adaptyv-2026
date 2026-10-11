import sys
from collections import defaultdict
aa3={'ALA':'A','ARG':'R','ASN':'N','ASP':'D','CYS':'C','GLN':'Q','GLU':'E','GLY':'G','HIS':'H',
 'ILE':'I','LEU':'L','LYS':'K','MET':'M','PHE':'F','PRO':'P','SER':'S','THR':'T','TRP':'W','TYR':'Y','VAL':'V'}
HUM='VRSSSRTPSDKPVAHVVANPQAEGQLQWLNRRANALLANGVELRDNQLVVPSEGLYLIYSQVLFKGQGCPSTHVLLTHTISRIAVSYQTKVNLLSAIKSPCQRETPEGAEAKPWYEPIYLGGVFQLEKGDRLSAEINRPDYLDFAESGQVYFGIIAL'
MOU='LRSSSQNSSDKPVAHVVANHQVEEQLEWLSQRANALLANGMDLKDNQLVVPADGLYLVYSQVLFKGQGCPDYVLLTHTVSRFAISYQEKVNLLSAVKSPCPKDTPEGAELKPWYEPIYLGGVFQLEKGDQLSAEVNLPKYLDFAESGQVYFGVIAL'
# 1) re-derive divergence from scratch: human i <-> mouse i (i<=71), human i <-> mouse i-1 (i>=73), 72 = indel
def mouse_at(h):
    if h==72: return None
    return MOU[h-1] if h<=71 else MOU[h-2]
DIV=set(); 
for h in range(1,158):
    m=mouse_at(h)
    if m is None or m!=HUM[h-1]: DIV.add(h)
print(f"1) DIVERGENCE RE-DERIVED FROM SEQUENCE: {len(DIV)} positions (expected 33)")
print(f"   {sorted(DIV)}")
print(f"   identical: {157-len(DIV)}/156 aligned = {(157-len(DIV))/156*100:.1f}%  (brief says 124/156 = 79.5%)")
print(f"\n2) KEY RESIDUES — conservation verified from sequence, not a stored list:")
for h in (32,65,82,86,87,90,113,115,143,145,146):
    m=mouse_at(h)
    print(f"   {h:>4}: human {HUM[h-1]}  mouse {m}   {'CONSERVED' if h not in DIV else '*** DIVERGENT'}")

# 3) validate numbering conversion against 7KP7 coordinates by identity
at=defaultdict(dict)
for l in open(sys.argv[1]):
    if l.startswith('ATOM') and l[12:16].strip()=='CA':
        at[l[21]][int(l[22:26])]=aa3.get(l[17:20].strip(),'X')
def to_human(n): return n if n>=73 else n-1
ok=bad=0; mism=[]
for n,a in sorted(at['B'].items()):
    h=to_human(n); exp=mouse_at(h)
    if exp is None: continue
    if exp==a: ok+=1
    else: bad+=1; mism.append((n,h,a,exp))
print(f"\n3) NUMBERING CONVERSION VALIDATED BY IDENTITY (7KP7 chain B):")
print(f"   author->human-mature mapping agrees with mouse sequence at {ok}/{ok+bad} residues")
if mism: print(f"   MISMATCHES: {mism[:12]}")
else: print("   zero mismatches -- conversion is correct")
