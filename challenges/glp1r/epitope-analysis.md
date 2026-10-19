# GLP1R activation epitope — analysis and hotspot selection

All numbers in this file are recomputed from `6X18.pdb` by the scripts in this
directory; the raw output is in [`generated-epitope.txt`](generated-epitope.txt).
The figures quoted in the prose below **are** transcribed from that output, so
[`crosscheck_epitope.py`](crosscheck_epitope.py) re-derives each one from the
structure and compares it against what this document actually says. It parses
the claimed figure out of the markdown rather than holding a constant, so a
wrong number here fails the check instead of passing it, and it exits non-zero
on any disagreement.

> **Numbering.** 6X18 chain R author numbering **equals UniProt P43220
> numbering** — verified, not assumed: chain R residue 29 is Thr, and our
> submitted construct (P43220 24–432) has Thr at 29. The assay construct's
> sequence position is therefore `UniProt − 23`.

## What is in 6X18

| chain | contents | residues |
|---|---|---|
| R | GLP1R | 29–423 (2 gaps) |
| P | GLP-1 | 7–36, `HAEGTFTSDVSSYLEGQAAKEFIAWLVKGR` |
| A / B / G | Gαs / Gβ / Gγ | — |
| N | Nb35 (complex-stabilising nanobody) | 1–126 |

The receptor is captured in the **active, G-protein-coupled state**. That is
the whole reason this structure is the design target.

## The two-domain split, measured

Splitting the bound peptide at residue 15 and taking heavy-atom contacts at
4.5 Å (the same convention as the TNF-α work):

| peptide segment | receptor residues contacted | ECD | TMD/ECL |
|---|---|---|---|
| **message**, GLP-1 7–15 | 27 | 3 | **24** |
| **address**, GLP-1 16–36 | 29 | **20** | 9 |

Activation lives in the transmembrane bundle; affinity lives in the
extracellular domain. This is our own measurement of the two-domain model
rather than a citation of it.

All ten literature anchors (Y148, Y152, R190, Q234, Y241, W306, R310, I313,
E364, E387) are **present and identity-matched** in chain R: 10 match, 0
mismatch, 0 unresolved.

## The geometric problem, and why it is avoidable

His7 Cα sits **43.2 Å** from the ECD centroid; the deepest message contact
(Y241) is **52.1 Å** out. A binder anchored in the ECD groove would have to
project ~30–43 Å to touch the activation site — roughly twenty residues of
uninterrupted helix. This is the most likely reason de novo miniproteins
published against class B receptors came back as **antagonists**: they grip
the ECD and cannot reach.

**The reach problem is an artefact of anchoring in the ECD.** Measured against
the bundle top instead, the best activation residues sit **0.8–13 Å** below it.
Targeting the transmembrane mouth directly removes the 43 Å span entirely.

## Is that surface actually grippable?

Two filters were applied to the 27 message residues.

**Accessibility.** On the apo receptor (peptide and G protein stripped, ECD
retained), 22 of 27 have SASA ≥ 15 Å². The peptide channel opens when vacated,
which is unsurprising — it is how the hormone enters.

**Channel-facing vs lipid-facing.** Apo SASA alone is misleading: a residue can
look exposed only because the calculation has no membrane, meaning its area
faces lipid and would be detergent-covered in the real assay. Computing
ΔSASA = SASA(receptor) − SASA(receptor + peptide) isolates the area the native
peptide actually buries, which is channel-facing by construction.

Result: **only Y145 is lipid/solvent-facing** (8% buried by the peptide) and it
is a low-contact residue. Every other candidate is 54–100% buried by the
peptide. The activation surface is genuinely channel-facing.

## Selected hotspots

```
R141,R201,R298,R299,R300,R306,R380,R384
```

> **Read this carefully: `R306` means chain R residue 306, which is TRP306 —
> not an arginine.** BindCraft hotspots are `<chainID><number>`, and this
> target's chain happens to be R, so every hotspot begins with R regardless of
> the residue's identity. The set above is Leu141, Leu201, Thr298, Arg299,
> Asn300, Trp306, Arg380, Leu384.

Chosen for high message-contact count **and** high buried area **and** shallow
depth (0 to −10 Å below the bundle top). Deeper high-scoring residues (L388 at
−13 Å, V237 −16 Å, R190 −16 Å) are held in reserve: they are channel-facing,
but deep enough to sit inside the detergent belt.

## Contraindications

1. **Designing for the active state may cost measured affinity.** The binder is
   built to be complementary to the Gs-coupled conformation, because that is
   the mechanism available for agonism — stabilise the active state. But
   objective 1 is measured on a detergent-solubilised construct carrying
   *unlisted* thermostabilising mutations, which may not populate that
   conformation. A design optimised for activation can therefore under-perform
   on the binding assay. This tension is inherent to the strategy, not a bug in
   it, and should be stated in the submission.
2. **Do not truncate the ECD away.** The ECD is part of chain R and caps the
   channel in the active state. The accessibility numbers above already include
   that occlusion. Removing it would design against a surface that is partly
   blocked in reality.
3. **Depth versus detergent.** Hotspots below roughly −10 Å likely sit within
   the DDM/CHS micelle. The native peptide does insert there, but a folded
   binder has a harder time; hence the shallow weighting.
4. **No tool available to us predicts agonism.** Targeting the activation
   epitope is a mechanistic bet. Structural engagement of the message site is
   *geometric evidence of the right binding mode*, not demonstrated receptor
   activation — the same distinction the TNF-α submission drew for pH.
5. **Expression format.** The cell-free system prepends Met and appends a
   C-terminal polyhistidine tag (confirmed with the organisers). Both termini
   must be modelled and kept clear of the channel.
