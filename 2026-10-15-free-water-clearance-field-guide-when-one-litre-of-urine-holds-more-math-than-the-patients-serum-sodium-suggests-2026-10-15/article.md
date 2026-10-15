# Free Water Clearance Calculator Field Guide: When One Litre of Urine Holds More Math Than the Patient's Serum Sodium Suggests

## Overview

This field guide explains how to use the Free Water Clearance Calculator on Elysia Tools, when the two related formulas (solute-free and electrolyte-free water clearance) answer different questions, and how the calculator's three output bands help a clinician or trainee spot the dilution-vs-concentration split that decides whether hyponatremia is renal or extrarenal. By the end, you will understand why a single 24-hour urine volume and three osmolality numbers tell you more about a sodium disturbance than five serum electrolytes do, and how to plug those numbers into the calculator without losing the units.

The Free Water Clearance Calculator ([elysiatools.com](https://elysiatools.com/en/tools/free-water-clearance)) takes four routine inputs — 24-hour urine volume (mL or L), urine osmolality (U_osm, mOsm/kg), plasma osmolality (P_osm, mOsm/kg), and an optional pair of urine and plasma sodium with potassium — and returns the two clearance values that nephrologists use to classify hypo- and hypernatremia: solute-free water clearance (C_H₂O) and electrolyte-free water clearance (eC_H₂O). It runs in the browser, does not phone home, and is designed for the workflow where the resident has the morning labs in one tab and the calculator open in another.

## The two clearance formulas and what each one actually measures

Solute-free water clearance (C_H₂O) is the volume of pure water the kidney excretes or retains per unit time, after stripping out the water that was obligated to carry the solutes in the urine. The classic formula is:

  C_H₂O = V × (1 − U_osm / P_osm)

where V is the urine flow rate in mL/min (or the total 24-hour volume divided by 1440 if you prefer the day's accounting).

When U_osm is lower than P_osm, the ratio is less than 1 and the term in parentheses is positive: the kidney excreted free water. When U_osm is higher than P_osm, the ratio exceeds 1, the term turns negative, and the kidney reabsorbed free water. C_H₂O is positive in diabetes insipidus and primary polydipsia (the urine is dilute and the kidney is dumping water), negative in dehydration and SIADH (the urine is concentrated and the kidney is conserving water), and approximately zero in healthy adults whose kidneys are simply matching plasma osmolality.

Electrolyte-free water clearance (eC_H₂O) refines C_H₂O by ignoring urea and glucose (which contribute to U_osm but do not drive the free-water balance in a clinically meaningful way) and using only urinary sodium plus potassium against plasma sodium. The simplified version is:

  eC_H₂O = V × (1 − (U_Na + U_K) / P_Na)

eC_H₂O is the value you want when you are asking whether the kidney is excreting or retaining the sodium-bearing water that is driving the serum sodium disturbance — the part of the urine volume that the kidney could have used to correct the sodium if it had been willing to. Negative eC_H₂O is the hallmark of SIADH and other hyponatremic states where the kidney is inappropriately retaining free water; positive eC_H₂O in a hyponatremic patient means the kidney is dumping free water and the problem is somewhere upstream (adrenal insufficiency, hypothyroidism, or — most commonly — too much oral water).

The calculator handles both formulas because the clinical question that triggered the calculation changes the answer you want.

## The three input pairs and the order you should enter them

The calculator takes its four to six inputs in a single panel. The order matters less than the units, and the units matter more than the order.

The first pair is **urine volume (V)** and **time window**. If you enter the total 24-hour collection, the calculator divides by 1440 internally to get the mL/min flow rate that the formulas expect; if you enter an eight-hour collection, it divides by 480; if you enter a per-minute catheter reading, it uses the value as-is. The calculator accepts the volume in mL or L — toggle the unit selector and the conversion happens before the multiplication, so the answer does not change.

The second pair is **U_osm** and **P_osm** in mOsm/kg. U_osm is measured by freezing-point depression on a spot urine sample, ideally from the same 24-hour collection as the volume; P_osm is the morning serum osmolality from the BMP plus a glucose correction (the calculator accepts glucose as a sixth optional input and adds 1 mOsm/kg per 18 mg/dL above the lab's normal range). When you enter both osmolalities, the ratio U_osm / P_osm is computed and the C_H₂O term (1 − ratio) is shown before you finish typing the electrolytes.

The third pair is **U_Na + U_K** and **P_Na**, all in mmol/L. U_Na and U_K come from the urine electrolytes panel; P_Na is the morning serum sodium. If your patient is on a lot of intravenous normal saline, the urine electrolytes from a sample collected during the infusion will not reflect baseline renal handling — pause the drip for 30 minutes before drawing the urine panel or accept that the answer is the answer under current therapy.

The five-input version (urine volume, U_osm, P_osm, U_Na, U_K, P_Na) is the one you actually want at the bedside; the four-input version (drop the electrolytes) gives you only C_H₂O, which is enough when you are ruling in or out diabetes insipidus in a patient with hypernatremia and polyuria.

## A worked example: hyponatremia on the morning labs

A 68-year-old patient is admitted overnight with confusion. Morning labs: serum sodium 119 mmol/L, BUN 8 mg/dL, serum osmolality 256 mOsm/kg, urine osmolality 612 mOsm/kg. The team has ordered a 24-hour urine collection; the volume comes back at 880 mL over 22 hours (so V = 880 / (22 × 60) = 0.667 mL/min), with U_Na 56 mmol/L and U_K 28 mmol/L.

Plug the four numbers into the calculator. The C_H₂O term reads 1 − 612 / 256 = 1 − 2.39 = −1.39, and multiplied by 0.667 mL/min gives **C_H₂O = −0.93 mL/min** — about −1336 mL/day of free water being reabsorbed. The electrolyte-free term reads 1 − (56 + 28) / 119 = 1 − 0.706 = 0.294, and multiplied by 0.667 gives **eC_H₂O = +0.196 mL/min** — about +282 mL/day of electrolyte-free water being excreted.

The two numbers tell different stories. C_H₂O is negative because the urine is markedly concentrated relative to the dilute serum (the kidney is doing its job of conserving water); eC_H₂O is mildly positive because, once you strip out the urea and glucose contribution, the kidney is dumping a small amount of electrolyte-free water. The clinical interpretation is that the serum sodium disturbance is being driven by something other than inappropriate renal water retention — the differential opens up toward hypothyroidism, adrenal insufficiency, or beer potomania, with SIADH less likely because eC_H₂O is not strongly negative.

This is exactly the case where having both formulas side by side in one calculator saves a second round of arithmetic, a second source of rounding error, and the five minutes it would take to do the second formula by hand and decide whether it agrees with the first.

## The three output bands and what each one tells you

The calculator surfaces its result in three visual bands, each corresponding to one of the standard interpretations of free-water clearance.

**Positive C_H₂O (band 1)** — the kidney is excreting free water. In a hyponatremic patient this is the reassuring band: the kidney is not the cause of the serum sodium problem. Common causes for a positive C_H₂O with hyponatremia are primary polydipsia, beer potomania, low solute intake (tea-and-toast diet), and reset osmostat. In a hypernatremic patient a positive C_H₂O is the diagnostic for diabetes insipidus — the kidney is dumping water it should be conserving.

**Negative C_H₂O (band 2)** — the kidney is reabsorbing free water. In a hypernatremic patient this is reassuring (the kidney is appropriately conserving water; the problem is water access or insensible losses). In a hyponatremic patient a negative C_H₂O is the SIADH-shaped alarm — combine with a urine sodium above 40 mmol/L and a low serum uric acid for the strongest signal. SIADH is a diagnosis of exclusion, but a strongly negative C_H₂O in a euvolemic hyponatremic patient is one of the two most useful confirmatory numbers (the other is the urine:plasma electrolyte ratio you get from eC_H₂O).

**Near-zero C_H₂O (band 3)** — the kidney is matching plasma osmolality without meaningful free-water gain or loss. This is the healthy-adult band and the band you expect to see in patients whose sodium disturbance is driven by volume status, not by free-water balance. A near-zero C_H₂O in a hyponatremic patient with low effective circulating volume (CHF, cirrhosis) tells you the kidney is appropriately retaining both sodium and water to defend perfusion, and the treatment is to fix the perfusion problem, not to fluid-restrict.

The eC_H₂O band on the right side of the calculator output follows the same sign convention but with one important caveat: eC_H₂O can read as positive even when C_H₂O is strongly negative, because the urea and glucose contributions to U_osm are masking a small amount of electrolyte-free water excretion. The two side-by-side bands let you see both signals at once and decide which one is clinically dominant.

## The pitfalls that change the answer without changing the inputs

Five failure modes hit the calculator often enough that they are worth a paragraph each.

**Failure 1: spot urine instead of timed collection.** If the urine osmolality comes from a one-time catheter sample but the volume comes from the nursing intake-and-output sheet, the V in the formula is the day's volume while the U_osm is one snapshot. In a patient whose urine osmolality swings by 200 mOsm/kg between morning and afternoon (a real pattern in reset osmostat), the formula returns nonsense. The calculator does not enforce that the volume and the osmolality come from the same window — that is a clinical judgment.

**Failure 2: mannitol or contrast dye in the urine.** Both raise U_osm by 20–50 mOsm/kg per dose without contributing to free-water balance. A patient who got a contrast CT four hours before the urine osmolality was drawn will have a falsely concentrated U_osm, the ratio U_osm / P_osm will be falsely high, and C_H₂O will be falsely negative. The calculator's eC_H₂O band is more robust against this error because it ignores the non-electrolyte osmolality contributions.

**Failure 3: glycosuria.** Glucose in the urine raises U_osm by 1 mOsm/kg per 18 mg/dL of glucose above normal. The calculator's optional glucose input lets you subtract the glucose contribution from U_osm before applying the formula. If you skip the glucose input and the patient has 400 mg/dL glucose spilling into the urine, C_H₂O will be falsely negative by 0.2–0.4 mL/min.

**Failure 4: diuretics.** Loop diuretics blunt the kidney's ability to concentrate or dilute urine by 50–80% within two hours of dosing. A urine osmolality drawn one hour after a furosemide dose will look falsely dilute. The calculator cannot see the medication list — the user has to hold the diuretic or wait at least four hours after the dose before drawing the urine panel.

**Failure 5: glucosuria and a urine sodium drawn from the same catheter stay.** The urine sodium reading on a lab slip is the sum of the sodium and the sodium-equivalent of the glucose's osmotic effect on water distribution. The calculator does not correct for this; if the patient's serum sodium is also low, the urine sodium reading is unreliable and eC_H₂O is unreliable downstream. Treat the answer as a starting point, not a verdict.

## When to use the calculator versus a textbook table

The calculator's job is to do the arithmetic without rounding errors and to present both formulas side by side. It does not replace the clinical reasoning that decides which formula is the right one for the question.

For a hyponatremic euvolemic patient, the right formula is eC_H₂O — the urea-and-glucose-corrected version — because you want to know whether the kidney is dumping or retaining the sodium-bearing water that is driving the serum disturbance. For a hypernatremic polyuric patient, the right formula is C_H₂O — the osmolality-based version — because you want to know whether the kidney can concentrate urine at all.

The calculator presents both for the cases where the clinical picture is not yet committed to one question. A morning labs round where the patient has a serum sodium of 124 but the urine sodium has not yet resulted is exactly the moment to open the calculator with the four inputs you have (V, U_osm, P_osm, and the plasma electrolytes) and let the right side of the output sit blank until the urine electrolytes come back.

## Where this fits in a clinical workflow

In an admission workflow, the free-water clearance pair goes into the chart on day 1 for any patient whose serum sodium is below 130 or above 150 mmol/L on the initial BMP. The pair is small — two numbers, two bands — and stays relevant through the correction phase because the formulas track response to fluid restriction, hypertonic saline, or D5W administration. The electrolyte-free water clearance number in particular tracks the SIADH response to fluid restriction almost in real time: as the kidney ramps down its free-water retention, eC_H₂O swings from strongly negative to mildly positive, often over 12–24 hours.

For trainees, the calculator's two-band display is a quick way to internalize the difference between the two formulas. After running a half-dozen admitted patients through it, the sign convention (positive = excreting, negative = retaining) becomes reflexive, and the next time a confused hyponatremic patient shows up in the ED, the differential workup shortens by a step.

The Free Water Clearance Calculator ([elysiatools.com/en/tools/free-water-clearance](https://elysiatools.com/en/tools/free-water-clearance)) is part of the broader Elysia Tools health calculator family. For hyponatremia workups that need a serum anion gap alongside the free-water calculation, the [Serum Anion Gap Calculator](https://elysiatools.com/en/tools/anion-gap-calculator) answers the next question the labs raise. For renal-dose adjustment in the same patient, the [Renal Dose Adjustment Calculator](https://elysiatools.com/en/tools/renal-dose-adjustment) handles the medication side of the same workup. And for the related sodium-disturbance differential that splits hypo from hyper, the [Serum Osmolality Calculator](https://elysiatools.com/en/tools/serum-osmolality-calculator) provides the P_osm reference value that anchors the formula. Explore more health calculators in the [Elysia Tools health category](https://elysiatools.com/en/tools) — and remember: every litre of urine carries an arithmetic, and the calculator just makes the arithmetic visible.
