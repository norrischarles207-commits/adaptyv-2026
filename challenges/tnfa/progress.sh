#!/bin/sh
# Progress + verdict for a BindCraft fan-out log. Usage: sh progress.sh <log>
L="${1:-tnfa-v2-core.log}"
[ -f "$L" ] || { echo "no such log: $L"; exit 1; }
echo "=== $L   $(wc -c < "$L" | tr -d ' ') bytes   last write $(date -r "$L" '+%H:%M:%S')   now $(date '+%H:%M:%S')"
echo "trajectories started : $(grep -c 'Starting trajectory:' "$L")"
echo "severe clashes       : $(grep -c 'Severe clashes' "$L")"
echo "no accepted MPNN     : $(grep -c 'No accepted MPNN' "$L")"
echo "passed all filters   : $(grep -c 'passed all filters' "$L")"
echo "accepted PDBs written: $(grep -c 'Accepted/Ranked/' "$L")"
echo
echo "--- re-predicted i_pTM (THE number: post-MPNN, independent AF2) ---"
grep -E "^[0-9]+ +2026-" "$L" | awk '{print $7}' | sort -rn | awk '
  {v[NR]=$1; s+=$1}
  END{ if(NR==0){print "  none yet"; exit}
       printf "  n=%d  best=%.2f  median=%.2f  worst=%.2f\n", NR, v[1], v[int((NR+1)/2)], v[NR]
       c=0; for(i=1;i<=NR;i++) if(v[i]>=0.70) c++
       printf "  >= 0.70 (v1-quality): %d of %d\n", c, NR }'
echo
echo "--- top 8 variants ---"
grep -E "^[0-9]+ +2026-" "$L" | sort -k7 -rn | head -8 | awk '{printf "  %-28s model%s  pLDDT %s  i_pTM %s  i_pAE %s\n",$3,$4,$5,$7,$9}'
echo
echo "--- trajectory-stage i_ptm (IGNORE for quality; shown only for contrast) ---"
echo "  max: $(grep -oE 'i_ptm 0\.[0-9]+' "$L" | sort -t. -k2 -rn | head -1)"
echo
echo "--- cost so far ---"
grep -E "total cost:|accepted designs:|timed out:" "$L" | tail -4
