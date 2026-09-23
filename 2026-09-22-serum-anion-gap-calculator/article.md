## Article: Serum Anion Gap (AG) Calculator — Field Guide

### Working title

Serum Anion Gap (AG) Calculator — Field Guide: When Sodium, Chloride, and Bicarbonate Decide Whether Your Patient Has Lactic Acidosis, DKA, or Just Diarrhea

### Slug

serum-anion-gap-calculator-field-guide-when-sodium-chloride-bicarbonate-and-the-gold-mark-mnemonic-decide-whether-your-metabolic-acidosis-is-hagma-or-nagma

### Article body (Markdown source — will go through md_to_html)

<strong>Serum anion gap is the fastest triage signal in metabolic acidosis — but only if you pick the right formula and read the four downstream branches in the right order.</strong> The standard serum anion gap — AG = Na⁺ − Cl⁻ − HCO₃⁻ — looks like three electrolyte values you already have on every BMP. It is. The interpretation is what changes everything: a gap above 12 mmol/L (or above 20 if you count potassium) puts the patient in a high-anion-gap metabolic acidosis (HAGMA), and the list of what fills that gap collapses to a single mnemonic. A normal gap during acidosis points elsewhere entirely. A low gap points somewhere else again.

This guide walks through the four decisions that decide whether your metabolic acidosis reads as HAGMA, NAGMA, hypoalbuminemia, or a mixed picture — and where the [Serum Anion Gap (AG) Calculator](https://elysiatools.com/en/tools/anion-gap-calculator) sits in each branch.

## The formula itself is two lines; the choice of which two is the first decision

The canonical equation is AG = Na⁺ − Cl⁻ − HCO₃⁻, expressed in mmol/L. Most clinical chemistry panels report Na⁺, Cl⁻, and total CO₂ (a usable proxy for HCO₃⁻ in the steady state, off by roughly 1–2 mmol/L in acute settings). A useful extended form adds potassium: AG = Na⁺ + K⁺ − Cl⁻ − HCO₃⁻. The two are NOT interchangeable. The potassium-included form shifts the reference range upward by about 4 mmol/L; the cutoff for HAGMA moves from 12 to roughly 20. Labs that report potassium as 3.5–5.0 mmol/L almost always run the potassium-included form; labs that default to 140 / 105 / 24 use the three-ion form.

The tool lets you toggle between them at the input level. Pick the form your lab actually reports. Mixing the two silently moves borderline patients from one category to another, and the category is what triggers the next branch.

## The reference range has three zones, and the low zone is the most underread

The textbook reference is 8–12 mmol/L for the three-ion form, 12–20 mmol/L for the potassium-included form. Three clinical zones follow:

- **Normal (8–12)**: Standard value, no unmeasured anions of clinical concern at this moment.
- **High (>12 or >20 with K⁺)**: HAGMA. Unmeasured anions are accumulating. The differential is finite and mnemonic-friendly.
- **Low (<3–6)**: Hypoalbuminemia is by far the most common cause. Each 1 g/dL drop in serum albumin lowers the gap by roughly 2.5–3 mmol/L. Hypercalcemia, hypermagnesemia, lithium toxicity, and IgG paraproteinemia also produce low gaps but are far less common.

The low-gap zone is the one clinicians most often wave through. A patient with cirrhosis, nephrotic syndrome, or any chronic albumin loss may present with a gap of 4–6 mmol/L on routine labs. That is NOT normal — it is the diagnostic signal that something has been slowly depleting anionic protein. The calculator's output explicitly flags the low zone and suggests the albumin correction branch.

## Albumin correction turns a normal gap into HAGMA more often than you expect

Hypoalbuminemia masks HAGMA. A patient with serum albumin 2.0 g/dL (normal 4.0) has lost roughly 5–6 mmol/L of anionic contribution to the gap. Their measured gap of 10 mmol/L is actually a corrected gap of 15–16 mmol/L — HAGMA territory. The correction is simple: corrected_AG = measured_AG + 2.5 × (4.0 − serum_albumin). For every 1 g/dL below 4.0, add 2.5 mmol/L.

This correction matters most in ICU, sepsis, and elderly patients — exactly the populations where metabolic acidosis is most likely and most consequential. Skip it and you miss HAGMA roughly 20–30 percent of the time in hypoalbuminemic cohorts. The tool accepts albumin as an optional fourth input and reports both the measured and corrected gap side-by-side.

## GOLD-MARK is the mnemonic for the high-gap differential

Once you have a corrected AG above the cutoff, the differential is the seven-item set every intern learns: G — glycols (ethylene glycol, propylene glycol), O — oxoproline (chronic acetaminophen use, especially in elderly women on acetaminophen), L — L-lactate (sepsis, shock, hypoperfusion, metformin), D — D-lactate (short bowel syndrome, post-gastric bypass), M — methanol, A — aspirin (salicylates), R — renal failure (sulfate, phosphate, urate retention), K — ketoacids (DKA, alcoholic ketoacidosis, starvation). The order is unimportant; the completeness is. Missing one (most often propylene glycol from IV lorazepam or oxoproline from chronic APAP) means missing the diagnosis.

The calculator does not pick from this list for you — no calculator can — but it does confirm whether the gap is high enough that the differential should be on your mind at all. A gap of 13 mmol/L is a soft prompt. A gap of 24 mmol/L is a hard one.

## Normal-gap acidosis means the bicarbonate is being lost, not titrated

A gap of 8–12 mmol/L in a patient with metabolic acidosis (low pH, low HCO₃⁻) means the acidosis is NOT from unmeasured anions — it is from HCO₃⁻ loss with chloride retention to maintain electroneutrality. The differential is shorter: diarrhea (GI bicarbonate loss), renal tubular acidosis (type 1, 2, or 4 — each with its own urine anion gap and potassium signature), saline resuscitation (chloride-rich fluid diluting bicarbonate), and ureteroenteric diversions. The workup is urine chloride, urine anion gap, and urine pH — NOT the GOLD-MARK list.

A normal-gap acidosis with a high urine chloride and high urine anion gap points at RTA. A normal-gap acidosis with a low urine chloride points at diarrhea. The tool does not run the urine workup, but it correctly classifies the gap as normal and routes the differential toward the NAGMA branch.

## Mixed pictures need both branches run

Many real patients have a HAGMA from one cause (lactic acidosis from sepsis) layered on top of a chronic NAGMA (diarrhea from tube feeds, RTA from longstanding disease) layered on top of hypoalbuminemia. The measured gap may be 14 mmol/L, but the corrected gap may be 19, and the urine chloride may be elevated. The treatment of the HAGMA branch (restore perfusion, source control) does not fix the NAGMA branch (replace bicarbonate, stop offending agent).

The tool returns the gap, the corrected gap, the classification (HAGMA / NAGMA / mixed / normal / low), and the four flags that feed the next branch. Read all four before treating. The most expensive mistake in metabolic acidosis is to chase one branch and miss the other.

## Where this fits in the rest of the electrolyte panel

The anion gap is one of four classical acid-base calculations that share the same electrolyte inputs. The other three are the delta gap (Δ-delta), the Winters formula (expected pCO₂ compensation in metabolic acidosis), and the strong ion difference (SID, the Stewart approach). Each catches a different failure mode. A patient with a clear HAGMA but a pCO₂ that does NOT match the Winters prediction has a concurrent respiratory acidosis — a missed second diagnosis.

The [Serum Anion Gap (AG) Calculator](https://elysiatools.com/en/tools/anion-gap-calculator) is built for the first branch and stops there on purpose. Pair its output with the delta-delta and Winters checks on the same lab draw to catch the mixed disorders. Most modern EMRs will compute the first two inline; the calculator is the place to go when you want to verify the correction explicitly or walk through the logic at the bedside.

## What to do next

Pick the form your lab reports, run the calculation, and read the classification before you chase the differential. The mnemonic works only when the gap is correctly categorized. Explore more tools at [elysiatools.com](https://elysiatools.com/en/tools).