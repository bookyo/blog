<strong>The osmolar gap is one of the most reliable single numbers in toxicology — but only if you compute it, correct it for ethanol, and read it next to the anion gap.</strong> An osmolar gap of 38.9 mOsm/kg with a credible toxic alcohol story changes the next hour of care. A normal gap with a strong ingestion history does not.

## What the Osmolar Gap Calculator Actually Computes

The osmolar gap (often written osm gap or osmolal gap, OG) is one of the most reliable single numbers in toxicology. The arithmetic is simple: subtract calculated osmolality from measured osmolality. The interpretation, however, is where most clinicians get into trouble. A normal gap rules out almost nothing. An elevated gap can mean ethanol on a Saturday night or ethylene glycol on a Sunday morning. The decision to dialyze, to start fomepizole, or to send a sample for ethylene glycol testing usually rides on whether you can compute this number correctly and read it in context.

This field guide walks through the conventional formula, the SI variant, the ethanol correction, the seven common unmeasured osmoles, and the three failure modes that send normal-looking results to the wrong bedside. For a tool that runs the calculation across both unit systems, see the [Osmolar Gap Calculator](https://elysiatools.com/en/tools/osmolar-gap-calculator).

## The Conventional Formula (mg/dL Inputs)

The classic formula uses US customary units:

```
Osm_calculated = 2 × Na + Glucose / 18 + BUN / 2.8
```

The factors 18 and 2.8 are molar mass conversions (glucose 180 g/mol → 180 / 10 = 18 mg/dL per mmol/L; BUN 28 g/mol → 28 / 10 = 2.8 mg/dL per mmol/L). The doubling of sodium reflects sodium's two accompanying anions (chloride and bicarbonate).

A worked example: measured osmolality 330 mOsm/kg, sodium 140 mmol/L, glucose 110 mg/dL, BUN 14 mg/dL. Calculated = 2 × 140 + 110/18 + 14/2.8 = 280 + 6.1 + 5.0 = 291.1. The gap is 330 − 291.1 = **38.9 mOsm/kg**, well above the normal −10 to +10 band, flagging an unmeasured osmole.

## The SI Formula (mmol/L Inputs)

Outside the United States, glucose and urea arrive in mmol/L rather than mg/dL. The formula collapses to:

```
Osm_calculated_SI = 2 × Na + Glucose + Urea
```

No division factors, no molar-mass gymnastics. A 6.1 mmol/L glucose reading is glucose 6.1; a 5.0 mmol/L urea reading is urea 5.0. The tool's `unitSystem` toggle switches the formula in place — pick the convention that matches your lab report, because mixing the two produces gaps of 20 mOsm/kg from a pure unit conversion error.

## The Ethanol-Corrected Gap

Ethanol is itself an unmeasured osmole. A patient with ethanol 200 mg/dL shows up with an OG around 43 mOsm/kg (200 / 4.6 ≈ 43). If the only story is acute intoxication, the corrected gap should fall back into the normal band:

```
OG_corr = OG − Ethanol / 4.6
```

For the ethanol 200 case, OG_corr = 43 − 43 = 0 — clean. For ethanol 100 mg/dL with a measured OG of 60, the corrected gap is 60 − 21.7 = 38.3, still elevated, and you should keep hunting for methanol or ethylene glycol. This is the move that separates "drunk and discharged" from "drunk and dialyzed."

## The Seven Unmeasured Osmoles You Will See

An elevated OG points to one of these, roughly in order of frequency in the US:

<ol>
<li><strong>Ethanol</strong> — subtract it; if the corrected gap falls, you are done.</li>
<li><strong>Methanol</strong> — windshield washer fluid, illicit spirits; metabolized to formic acid.</li>
<li><strong>Ethylene glycol</strong> — antifreeze; metabolized to oxalic acid.</li>
<li><strong>Diethylene glycol</strong> — contaminated medication; pediatric outbreaks.</li>
<li><strong>Propylene glycol</strong> — IV lorazepam, diazepam carrier; usually a small gap.</li>
<li><strong>Mannitol, sorbitol, glycerol</strong> — osmotic diuretics and bowel preps.</li>
<li><strong>Severe DKA, sepsis, end-stage renal disease</strong> — ketoacids, lactate, and other small solutes accumulate when clearance fails.</li>
</ol>

A gap above 25 mOsm/kg without a clear ethanol story is the textbook trigger for toxic alcohols workup: anion gap, blood gas, ethylene glycol level, and the call to the poison center.

## The Three Normal-Gap Failure Modes

A normal OG does NOT exclude toxic alcohol poisoning. Three situations produce a falsely normal result:

<ul>
<li><strong>Late presentation after metabolism.</strong> Methanol and ethylene glycol are parent alcohols with high osmolality; their metabolites (formic, oxalic, glycolic acids) have low osmolality but high anion gap. A patient who arrives 18 hours after ingestion has converted most of the parent alcohol and now shows a normal OG with an elevated AG.</li>
<li><strong>Massive ethanol with low baseline osmolality.</strong> Some chronic alcoholics run a measured osmolality near the calculated baseline, so an acute methanol co-ingestion is masked. Always pair OG with AG and a careful history.</li>
<li><strong>Laboratory error.</strong> A point-of-care glucose strip and a sodium from an old sample can each swing the calculated osmolality by 10+ mOsm/kg. Repeat the draw before dialing a dialysis team.</li>
</ul>

The takeaway: a normal OG buys you an anion gap and a clock, not a discharge.

## When to Dialyze (And When Not To)

The osmolar gap is a screening tool, not a treatment threshold. Hemodialysis decisions for toxic alcohols depend on the anion gap, the pH, the ethylene glycol or methanol level, the renal function, and the hemodynamic status. OG > 25 mOsm/kg with a credible toxic alcohol story is the typical trigger for fomepizole or ethanol therapy; the actual dialysis call comes from the toxicologist with the level in hand. Document the OG calculation and the unit system explicitly, because the receiving team will want to re-derive it themselves.

## A Closing Checklist for the Bedside

Before you trust an OG:

<ul>
<li>Pick the formula that matches the lab's unit system; never mix.</li>
<li>If ethanol is positive, subtract it before interpreting.</li>
<li>Pair OG with anion gap, blood gas, and a clock from ingestion.</li>
<li>A normal OG with a strong history is not a discharge — call poison control.</li>
<li>For reproducible arithmetic and dual-unit toggling, the [Osmolar Gap Calculator](https://elysiatools.com/en/tools/osmolar-gap-calculator) handles the conversion in both directions and surfaces the ethanol-corrected gap automatically. Explore more toxicology tools at [elysiatools.com/en/tools](https://elysiatools.com/en/tools).</li>
</ul>