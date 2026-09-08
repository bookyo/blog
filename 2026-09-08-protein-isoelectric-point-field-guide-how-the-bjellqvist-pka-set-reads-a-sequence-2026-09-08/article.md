Theoretical protein pI numbers look academic until a separation fails. A basic peptide that refuses to bind a cation-exchange column at pH 7, or an acidic band that disappears off the acidic end of an IEF strip, usually comes back to one quiet mistake: someone trusted the average pI from a database without checking how many acidic versus basic residues the chain actually carries.

<strong>A sequence-first pI calculation collapses eight textbook pages into a single number you can plan a buffer around.</strong> The [Protein Isoelectric Point Calculator (pI by Composition)](https://elysiatools.com/en/tools/protein-isoelectric-point) takes an amino-acid sequence and returns the pH where the net charge crosses zero, the net charge at pH 7.4, and the molecular weight, all from the simplified ExPASy (Bjellqvist) pKa set. The same algorithm Biopython ships with; results match Biopython's `IsoelectricPoint` exactly.

This field guide walks through what the numbers actually mean, when they break, and how to read the calculator's output without re-reading Gasteiger's chapter on ionizable groups.

## What "pI by composition" actually computes

Every ionizable group on the peptide has a pKa. At pH values below its pKa, the group is protonated; above, it deprotonates. The net charge at any pH is the sum of partial charges across every Asp, Glu, Cys, Tyr, His, Lys, Arg, plus the alpha-amino N-terminus and alpha-carboxyl C-terminus.

The Bjellqvist set the calculator uses assigns:

- N-terminus 7.5, Lys 10.0, Arg 12.0, His 5.98
- C-terminus 3.55, Asp 4.05, Glu 4.45, Cys 9.0, Tyr 10.0

Bisection sweeps pH and reports the value where net charge crosses zero. That crossing is the pI. A chain with four Glu and zero Lys/Arg/His will cross zero deep in the acidic range; a chain with three Arg and one Asp will cross deep in the basic range.

This is composition, not structure. Folded-state pKa shifts from hydrogen bonds, salt bridges, or buried residues are not modeled. PTMs (phosphorylation, acetylation) are not modeled. For 95 percent of bench-planning work, that simplification is exactly what you want.

## A worked pair: an acidic peptide and a basic peptide

Two real sequences from the calculator's example library illustrate the range. Insulin A-chain (`GIVEQCCTSICSLYQLENYCN`, 21 residues) carries 2 Glu, 4 Cys, and 2 Tyr against no Lys, no Arg, and no His. Net charge is already negative at neutral pH, and the bisection settles at **pI ≈ 3.79**, with a net charge of −2.54 at pH 7.4 and a molecular weight of 2383.71 Da.

Bradykinin (`RPPGFSPFR`, 9 residues) has 2 Arg and zero acidic residues beyond the C-terminus. The chain's only easy way to lose positive charge is to deprotonate the two Arg guanidinium groups, which does not finish until pH 12. The calculator returns **pI = 12**, net charge +1.56 at pH 7.4, MW 1060.22 Da.

These two outputs are the right shape for the lab work each predicts:

- **Insulin A-chain at pI 3.79** elutes early on an anion-exchange column at pH 7.4 (it's already negative) and focuses toward the acidic end of an IEF strip.
- **Bradykinin at pI 12** binds tightly to cation-exchange resin at any working pH below about 9 and co-migrates with lysozyme-class basic proteins in IEF.

If your bench result contradicts that prediction, the peptide is not behaving as a random coil. Something else is going on: a PTM, a folded conformation, a cofactor, or a sample problem.

## Reading the calculator's output

The result block returns three numbers plus a classification tag.

`isoelectricPoint` is the pH where net charge crosses zero. For neutral peptides this is the middle of the physiological range; for charged peptides it can fall anywhere from below 3 to above 12.

`netChargePh74` is the net elementary charge at pH 7.4. Sign tells you which exchange resin binds the chain at physiological pH; magnitude roughly tracks binding strength. Insulin A-chain's −2.54 predicts firm anion-exchange binding; bradykinin's +1.56 predicts firm cation-exchange binding.

`molecularWeightDa` is the residue-mass sum from the ProtParam table plus water (18.015 Da). Compare against an intact-mass spec to catch missed residues, missed disulfides (each reduces two H), or unexpected modifications.

`classification` is `acidic` when pI is below about 6, `basic` above about 8, and `neutral` in between. Use it as a quick sanity check before picking a buffer pH.

## When the algorithm and your experiment disagree

Three common failure modes:

- **Composition surprises.** A "neutral" 100-residue enzyme with 12 Lys and 12 Glu reads pI near 7 on paper but the actual folded pI may sit near 5 if a lysine is buried in a salt bridge with a glutamate. The calculator cannot see this; neither can any sequence-only tool. Verify with IEF before trusting the buffer choice.
- **PTMs.** Phosphorylation adds roughly one negative charge per phosphate group. Acetylation of the N-terminus removes the pKa-7.5 group entirely and shifts the calculated pI by 0.5-1.0 units toward acidic. If your sample is phosphorylated, the calculator's number is the unmodified chain, not your real analyte.
- **Cysteine state.** The Bjellqvist set treats Cys as pKa 9.0 (thiol/thiolate). At pH 7 a free Cys is mostly protonated and neutral; at pH 8.5 it is half-thiolate and contributes roughly −0.5. If your chain forms disulfides, those two Cys residues are no longer titratable in the physiological range. The calculator still counts them at pKa 9.0 because the sequence input does not specify redox state. Subtract roughly one pKa-9 contribution per disulfide when reasoning about a cross-linked chain.

## A quick-start recipe for the calculator

For most lab-planning calls you only need three inputs: the one-letter sequence, the number of decimal places you care about (2 is the default for buffer work), and a sense of what counts as an acidic, basic, or neutral result.

A workflow that takes about 30 seconds:

1. Paste the sequence with no spaces and no FASTA header.
2. Set `decimalPlaces` to 2.
3. Read `isoelectricPoint` for the buffer-pH direction, `netChargePh74` for the exchange-resin choice and binding strength, and `molecularWeightDa` to verify the chain length.
4. Compare against any intact-mass spec; a discrepancy larger than 2-3 Da usually means a missed PTM or a missed disulfide.

If the sequence contains non-standard residues (selenocysteine, pyrrolysine, modified amino acids), the calculator falls back to a neutral contribution for those positions — fine for pI estimation, less fine for MW. Re-run with the standard residue substituted in for an upper-bound estimate.

## Picking a buffer pH from the output

A practical rule:

- **pI < 6:** use an anion-exchange column at pH 7-8 (the protein is already negative). Buffer: 20 mM Tris-HCl pH 8.0.
- **pI > 8:** use a cation-exchange column at pH 6-7 (the protein is already positive). Buffer: 20 mM MES pH 6.0 or 20 mM phosphate pH 6.5.
- **pI 6-8:** the chain is too close to neutral to bind either resin cleanly at pH 7.4. Drop anion-exchange pH to 7.0 or cation-exchange pH to 6.5, or pick a buffer that adds a binding handle (add 5 mM NaCl to screen weak binding; or run a pH-gradient IEF instead of ion exchange).

Keep 0.5 pH units of headroom between the buffer pH and the pI. Insulin A-chain's pI 3.79 leaves no room at all on the cation side; you would never pick a cation column for it.

## Where the Bjellqvist approximation breaks

The calculator uses the simplified Bjellqvist set with terminal pKas of 7.5 and 3.55. ExPASy's `Compute pI/Mw` tool uses a more nuanced terminal-residue-specific table and may differ from this calculator by 0.1-0.3 pH units for short peptides where the termini dominate. For most workflows the difference does not matter; for analytical-grade work where you are claiming a pI to two decimal places, run the same sequence through ExPASy and Biopython and average.

Folded-state pKa shifts, histidine microenvironments, and PTM-driven charge changes are out of scope. If your protein is folded and active, treat the calculated pI as a planning estimate, then measure.

## Running the calculation

The calculator takes a one-letter amino-acid sequence and an optional decimal-place count. Paste the sequence, set decimal places to 2 for most lab work, and the result block returns pI, net charge at pH 7.4, MW, and the acidic/basic tag in a single JSON.

Try the two worked sequences from this guide:

- `GIVEQCCTSICSLYQLENYCN` returns pI ≈ 3.79, charge −2.54 at pH 7.4, MW 2383.71 Da.
- `RPPGFSPFR` returns pI = 12, charge +1.56 at pH 7.4, MW 1060.22 Da.

Then paste your own sequence and plan the buffer around the three numbers. For more composition-driven protein properties (extinction coefficient, instability index, aliphatic index), the same Bjellqvist framework extends cleanly to most ProtParam-style tools.

Explore the full tool at [Elysia Tools](https://elysiatools.com/en/tools/protein-isoelectric-point), and try your own sequence in the calculator before committing to a buffer pH or an IEF range.
