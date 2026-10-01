#!/usr/bin/env python3
"""
Build and validate submission.csv. Writes nothing unless everything passes.

Five designs, two sources: four parents from the v3c designs CSV, and the
H36E variant from the variant FASTA. Order is submission order, lead first.
"""
import csv, os, sys

CSV_SRC = "challenges/egfr/v3c-core-designs.csv"
FASTA_SRC = "challenges/egfr/fasta/l93_variants.fasta"
DST = "challenges/egfr/submission.csv"
DRY = "--dry-run" in sys.argv

# (submission name, source, key in that source, expected length)
ORDER = [
    ("l93_H36E",                "fasta", "l93_H36E",                93),
    ("egfr_l93_s713816",        "csv",   "egfr_l93_s713816",        93),
    ("egfr_l75_s674224_mpnn14", "csv",   "egfr_l75_s674224_mpnn14", 75),
    ("egfr_l64_s902794_mpnn2",  "csv",   "egfr_l64_s902794_mpnn2",  64),
    ("egfr_l91_s124145_mpnn1",  "csv",   "egfr_l91_s124145_mpnn1",  91),
]

AA = set("ACDEFGHIKLMNPQRSTVWY")


def die(m):
    sys.exit("FAIL: " + m)


def load_csv():
    if not os.path.exists(CSV_SRC):
        die(CSV_SRC + " not found. Run from the repo root.")
    with open(CSV_SRC, newline="") as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        die(CSV_SRC + " is empty or headerless")
    low = {c.lower().strip(): c for c in rows[0].keys()}
    ncol = next((low[c] for c in ("name", "design", "design_name", "id") if c in low), None)
    scol = next((low[c] for c in ("sequence", "seq", "binder_sequence") if c in low), None)
    if not ncol or not scol:
        die("no name/sequence column in %s; header = %s"
            % (CSV_SRC, ", ".join(rows[0].keys())))
    print("csv    : %s  (name=%r seq=%r, %d rows)" % (CSV_SRC, ncol, scol, len(rows)))
    tbl = {}
    for r in rows:
        k = (r.get(ncol) or "").strip()
        v = (r.get(scol) or "").strip().upper()
        if not k:
            continue
        if k in tbl and tbl[k] != v:
            die("design %r appears twice in the CSV with different sequences" % k)
        tbl[k] = v
    return tbl


def load_fasta():
    if not os.path.exists(FASTA_SRC):
        die(FASTA_SRC + " not found. Run make_variants.py first.")
    tbl, name, buf = {}, None, []
    for ln in open(FASTA_SRC):
        ln = ln.strip()
        if ln.startswith(">"):
            if name:
                tbl[name] = "".join(buf)
            name, buf = ln[1:], []
        elif ln:
            buf.append(ln)
    if name:
        tbl[name] = "".join(buf)
    print("fasta  : %s  (%d records)" % (FASTA_SRC, len(tbl)))
    return tbl


def main():
    csv_tbl = load_csv()
    fa_tbl = load_fasta()
    print()

    out, bad = [], False
    print("%-26s %-6s %5s  %s" % ("design", "source", "len", "status"))
    print("-" * 72)
    for name, src, key, want in ORDER:
        tbl = csv_tbl if src == "csv" else fa_tbl
        if key not in tbl:
            print("%-26s %-6s %5s  FAIL: not present in source" % (name, src, "-"))
            bad = True
            continue
        s = tbl[key]
        errs = []
        if not s:
            errs.append("empty sequence")
        if set(s) - AA:
            errs.append("non-standard residues: " + "".join(sorted(set(s) - AA)))
        if not 10 <= len(s) <= 250:
            errs.append("length %d outside [10,250]" % len(s))
        if len(s) != want:
            errs.append("length %d but expected %d -- WRONG SEQUENCE" % (len(s), want))
        if errs:
            print("%-26s %-6s %5d  FAIL: %s" % (name, src, len(s), "; ".join(errs)))
            bad = True
        else:
            print("%-26s %-6s %5d  ok" % (name, src, len(s)))
            out.append((name, s))

    names = [n for n, _ in out]
    seqs = [s for _, s in out]
    if len(set(names)) != len(names):
        die("duplicate names in submission set")
    if len(set(seqs)) != len(seqs):
        die("duplicate sequences in submission set")
    if bad:
        die("validation failed. Nothing written.")

    # H36E must differ from its parent at exactly one position.
    d = dict(out)
    if "l93_H36E" in d and "egfr_l93_s713816" in d:
        a, b = d["egfr_l93_s713816"], d["l93_H36E"]
        if len(a) != len(b):
            die("H36E and parent differ in length")
        diff = [(i + 1, a[i], b[i]) for i in range(len(a)) if a[i] != b[i]]
        if len(diff) != 1:
            die("H36E differs from parent at %d positions, expected 1" % len(diff))
        p, old, new = diff[0]
        if (p, old, new) != (36, "H", "E"):
            die("H36E substitution is %s%d%s, expected H36E" % (old, p, new))
        print("\nparent/variant check: single substitution H36E confirmed")

    print("\n%d designs validated." % len(out))
    if DRY:
        print("--dry-run: not writing %s" % DST)
        return

    with open(DST, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["name", "sequence", "molecule_class"])
        for n, s in out:
            w.writerow([n, s, "protein"])

    with open(DST, newline="") as fh:
        back = list(csv.DictReader(fh))
    if len(back) != len(out):
        die("round-trip row count: wrote %d read %d" % (len(out), len(back)))
    for b_, (n, s) in zip(back, out):
        if b_["name"] != n or b_["sequence"] != s:
            die("round-trip mismatch on " + n)
        if b_["molecule_class"] != "protein":
            die("round-trip molecule_class mismatch on " + n)

    print("round-trip verified against source: %d/%d exact." % (len(back), len(out)))
    print("wrote %s" % DST)


if __name__ == "__main__":
    main()
