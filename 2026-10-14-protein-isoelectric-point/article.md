<strong>A single substitution can swing a protein's pI by a full pH unit.</strong> That's the practical fact behind every 2D-gel smear, every failed ion-exchange column, and every weird western-blot band that refuses to transfer at pH 8.3. The [Protein Isoelectric Point Calculator](https://elysiatools.com/en/tools/protein-isoelectric-point) computes the theoretical pI by summing net charge across every ionizable group, then using bisection to land on the pH of zero net charge — the same Bjellqvist pKa set and the same bisection routine used by Biopython's IsoelectricPoint. This field guide unpacks which pKa values do the most work, where bisection converges or oscillates, and why the result drifts when you ignore N-terminal and C-terminal residues.

## What the Calculator Actually Sums

Every amino acid has zero, one, or two titratable groups in the physiological range, and the calculator treats each one as an independent Henderson-Hasselbalch site with its own pKa. The default Bjellqvist set used here is the simplified ExPASy table: **N-terminus 7.5**, **C-terminus 3.55**, **Lys 10.0**, **Arg 12.0**, **His 5.98**, **Asp 4.05**, **Glu 4.45**, **Cys 9.0**, **Tyr 10.0**. All other residues (Ala, Gly, Val, Leu, Ile, Pro, Phe, Trp, Met, Ser, Thr, Asn, Gln) contribute their residue mass for the molecular-weight sum but no net charge at any pH between 0 and 14.

The net-charge formula at pH `p` is therefore:

```
Q(p) = sum_over_basic( 1 / (1 + 10^(pKa - p)) )
     - sum_over_acidic( 1 / (1 + 10^(p - pKa)) )
     + (N_term_charge - C_term_charge)
```

At pH 7.4 a typical 300-residue soluble protein will have a net charge of ±5 to ±20, and the pI is the pH where Q(p) crosses zero. Bisection between pH 0 and pH 14 with a 0.001 tolerance usually converges in 30-40 iterations.

## Why the Bisection Sometimes Lands on the Wrong Plateau

The mathematical pI is unique — Q(p) is monotonic across any single ionization step, so there is exactly one crossing between pH 0 and 14. The practical hazard is that the calculator reports a **single pI value rounded to two decimals**, and that single value can land on the **truncated plateau** at the edge of the convergence band. Two cases trip the truncation:

1. **Polyamphoridine proteins** — sequences with extreme charge asymmetry where the basic and acidic groups are clustered in different domains. The net-charge curve flattens near pI and bisection can spend 50+ iterations oscillating inside a 0.01-pH band before the tolerance triggers exit. The reported pI is correct, but the convergence log will show no early-exit — if you re-run with a 0.0001 tolerance you'll get the same answer to four decimals, and the 0.001 answer was already within rounding noise.

2. **Disulfide-bonded Cys pairs** — the calculator treats each Cys independently with pKa 9.0, but a real disulfide drops the thiolate form entirely. If your sequence has 4 Cys in two disulfide bonds, the calculator will over-count by 4 negative charges near pH 9, pushing the pI down by 0.2 to 0.5 pH units. The Bjellqvist set has no built-in disulfide detection, so the practical fix is to substitute the paired Cys with Ser (which contributes no charge) for the theoretical pI calculation, then add back the residue mass for the molecular-weight sum.

## The Three pKa Values That Decide the pI

For 90% of soluble proteins the pI is determined by just three pKa values: **Glu 4.45**, **Asp 4.05**, and **Lys 10.0**. Here's why:

- The acidic plateau (pH 3 to 5) is dominated by Glu and Asp deprotonation. A protein that has 15 Glu and 12 Asp will have a strong acidic shoulder centered around pH 4.2, and any basic residues contribute their protonated form throughout this band.
- The basic plateau (pH 9 to 12) is dominated by Lys (pKa 10.0) and Arg (pKa 12.0). His (pKa 5.98) and Tyr (pKa 10.0) are too weak to influence the basic side once Lys kicks in.
- The crossing happens where the cumulative acidic deprotonation equals the cumulative basic protonation. For the 15-Glu/12-Asp/20-Lys/10-Arg protein above, that's around pH 8.4.

If your protein's pI prediction is off by more than 0.5 pH units from a published experimental value, the first thing to check is the Glu/Asp count — even a single misread residue can swing the answer by 0.3.

## How N-Terminal and C-Terminal Residues Move the Answer

The N-terminus (pKa 7.5) and C-terminus (pKa 3.55) are treated as **fixed charges that don't depend on the chain length**, which means their contribution to the net charge sum is constant per molecule, not per residue. For a 50-residue peptide that's a 2% contribution; for a 500-residue protein it's 0.2%. The simplification works because the Bjellqvist set averages the pKa shift across N-terminal residue identity — ExPASy's Compute pI tool uses a fuller terminal-residue-specific table that swings the answer by ±0.1 pH depending on whether the N-terminus is Lys (pKa 7.7) or Pro (pKa 6.7).

The practical takeaway: for routine lab planning (column buffer pH, IEF strip pH range), the simplified Bjellqvist set is correct to ±0.3 pH units against ExPASy Compute pI. For a publication-grade citation, run the same sequence through Biopython's `IsoelectricPoint` class or ExPASy's web tool and report both values.

## Net Charge at Physiological pH and Why It Matters for Solubility

The calculator reports the net charge at pH 7.4 alongside the pI, and that single number is the best predictor of solubility at neutral pH. A protein with Q(7.4) > +10 will be highly soluble at pH 7.4; a protein with Q(7.4) < -10 will be borderline and may precipitate. The His contribution (pKa 5.98) is the only pH-7.4-relevant group that swings steeply across the physiological band — moving from pH 6.5 to pH 7.5 changes a 30-His protein's net charge by about +3.

For ion-exchange chromatography planning, the rule is:

- **Anion exchange (DEAE, Q)**: bind at pH 0.5 above pI, elute with a salt gradient. The protein is net negative and binds tightly.
- **Cation exchange (SP, CM)**: bind at pH 0.5 below pI, elute with a salt gradient. The protein is net positive and binds tightly.
- **At pH = pI**: the protein has zero net charge, does not bind either column, and may precipitate. Always buffer at least 0.5 pH units away from pI for any ion-exchange step.

The calculator's Q(7.4) output lets you skip the guesswork and pick the buffer pH directly from the predicted charge curve.

## Average Molecular Weight from Residue Masses

The molecular-weight sum uses the standard ProtParam residue masses plus water (18.015 Da), which is the same approach as Biopython's `ProteinAnalysis.molecular_weight()`. The calculator does NOT average isotopic compositions — every residue is treated as the monoisotopic-average mass from the standard residue table. That means the reported MW is the **average MW**, not the monoisotopic MW you'd see on a high-res mass spec.

For most lab-planning uses (gel electrophoresis, sizing columns, concentration calculations), the average MW is what you want. For mass-spec interpretation, run the sequence through ExPASy's ProtParam or Biopython's `ProteinAnalysis.molecular_weight()` with the monoisotopic flag and compare.

The charged-residue composition output (count of each ionizable residue) is also useful for picking the right IEF strip pH range: a protein with 30 Lys and 25 Arg will have a broad pI plateau near pH 10.5, so a pH 9-11 IEF strip is appropriate. A protein with 20 Glu and 15 Asp will plateau near pH 4.5, so a pH 3-5 strip is the right call.

## Acidic / Basic Reading and Its Limitations

The calculator labels the protein as "acidic", "basic", or "neutral" based on the pI:

- pI < 7.0: acidic
- pI > 7.0: basic
- pI = 7.0: neutral

This is a coarse label — most published proteins fall outside the strict pH-7 cutoff, and the "neutral" bucket is rarely populated. For a finer classification, use the Q(7.4) reading: a protein with Q(7.4) > +5 is strongly basic at physiological pH, Q(7.4) < -5 is strongly acidic, and anything in between is mild. The pI and Q(7.4) values together give you a complete picture of the protein's charge behavior across the physiological pH range.

The label is most useful for at-a-glance triage: if you're scanning 50 sequences from a proteomics study and need to bucket them for ion-exchange fractionation, the acidic/basic reading plus pI bucket (pH 4-5, 5-6, 6-7, 7-8, 8-9, 9-10) is enough to plan the column strategy.

## When the Calculator Is and Isn't the Right Tool

Use the calculator when:

- You have a clean amino-acid sequence (no unknown residues, no non-standard modifications).
- You need a fast theoretical pI for lab-planning purposes (column buffer, IEF strip, 2D-gel pH range).
- You want a Biopython-equivalent answer without installing the Python stack.
- You're comparing multiple sequence variants and need a relative pI shift rather than a publication-grade absolute value.

Don't use the calculator when:

- The protein has post-translational modifications (phosphorylation, acetylation, glycosylation) that change the ionizable groups. PTMs are NOT modeled.
- The protein has folded-state pKa shifts — a buried His in a hydrophobic pocket can have a pKa shifted by 1-2 pH units from the Bjellqvist set. The calculator assumes fully solvent-exposed residues.
- You need a publication-grade absolute pI to four decimals. Run ExPASy Compute pI or Biopython directly and cite the tool.

The closing rule for the field guide is that **a single substitution can swing the pI by a full pH unit**, but only if it changes the charge balance at the convergence point. Most substitutions move it by 0.1-0.3 — and that's exactly the regime where the simplified Bjellqvist set is most accurate. When you're planning an ion-exchange step, the calculator's output is more reliable than the textbook rule of thumb, and when you're debugging a 2D-gel smear, the residue-by-residue breakdown tells you which substitution is the culprit.

For more on protein charge analysis, see the [Bjellqvist 1993 pKa derivation paper](https://pubmed.ncbi.nlm.nih.gov/8268772/) and the [Gasteiger 2003 ExPASy tools review](https://pubmed.ncbi.nlm.nih.gov/12824417/). To run the same calculation on your own sequence, head to the [Protein Isoelectric Point Calculator](https://elysiatools.com/en/tools/protein-isoelectric-point). For a wider tour of molecular-biology lab calculators, browse the [Elysia Tools Education category](https://elysiatools.com/en/tools/education).