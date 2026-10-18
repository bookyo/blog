> **Lead phrase.** When the pulse oximeter reads 88% and the ABG comes back, every clinician at the bedside eventually asks the same question: *is this hypoventilation, or is something in the lung actually broken?* The A-a gradient — the difference between alveolar and arterial PO₂ — answers that in one equation.

The alveolar gas equation predicts how much oxygen *should* be in the alveolus given the FiO₂ and the barometric pressure, and arterial PaO₂ measures how much actually crossed into the blood. A normal gap means the lung is transferring oxygen as expected, so hypoxemia must be coming from somewhere else (low ventilation, low inspired oxygen, or low atmospheric pressure at altitude). A widened gap means there is a real intrapulmonary problem — V/Q mismatch, shunt, diffusion block, or low mixed-venous O₂. The [A-a Gradient calculator](https://elysiatools.com/en/tools/a-a-gradient-calculator) runs the math and labels the result against the age-adjusted normal so the answer shows up before the next set of vitals does.

## Why the A-a Gradient Matters at the Bedside

The ABG prints three numbers an intern actually needs: PaO₂, PaCO₂, FiO₂. Alone, they tell you the patient is hypoxemic but not *why*. The A-a gradient closes the loop. If the gap is normal, the clinician can skip a pulmonary workup, look at the drive to breathe (opioids, neuromuscular weakness, severe metabolic alkalosis), and treat accordingly. If the gap is widened, the differential narrows to V/Q mismatch (pneumonia, COPD, asthma, PE, pulmonary edema), shunt (ARDS, hepatopulmonary syndrome, intracardiac right-to-left), diffusion limitation (interstitial lung disease), or low mixed-venous O₂ (sepsis, shock, low cardiac output). One number, four destinations.

## The Alveolar Gas Equation Walkthrough

The math behind the gradient is short enough to do at the whiteboard.

> `PAO₂ = FiO₂ × (P_atm − 47) − PaCO₂ / 0.8`

The first term is the inspired oxygen partial pressure: 21% of dry barometric pressure at sea level, 47 mmHg subtracted for the water vapor pressure in the trachea. The second term is the alveolar dilution by CO₂ — the respiratory quotient (default 0.8) assumes the patient is burning a mixed diet of carbohydrate, fat, and protein. Lower the barometric pressure and PAO₂ drops. Lower the PaCO₂ and PAO₂ rises (hyperventilation packs more oxygen into each alveolar space). Lower the FiO₂ and PAO₂ falls in proportion.

Subtracting the measured PaO₂ gives the gradient:

> `A-a = PAO₂ − PaO₂`

## The Age-Adjusted Normal Range

A "normal" A-a gradient is not 0 — small mismatches always exist between alveolar and arterial sides, and the gap widens with age. The canonical teaching rule is:

> `Normal A-a ≈ (Age + 10) / 4`

A 20-year-old patient breathing room air should have a gradient under about 7-8 mmHg. A 60-year-old can run up to ~17 mmHg and still be physiologically normal. A 90-year-old can hit 25 mmHg. The age cutoff matters because the alternative — a single fixed threshold like "<15 mmHg" — produces false positives on every elderly patient and false negatives on every teenager. The calculator uses `(Age + 10) / 4` as its denominator and reports the gradient as a multiple of normal (e.g. "3.1× expected normal"), which keeps the interpretation scale-invariant across decades.

## The Hypoxemia Decision Tree

Once the gradient is computed, the bedside logic follows two branches.

**Normal gradient.** Hypoxemia is *not* in the lung. Think hypoventilation (PaCO₂ > 45 mmHg suggests opioid, neuromuscular weakness, severe CNS depression); think high altitude (P_atm < 760 mmHg — Denver, Leadville, Mexico City); think low inspired oxygen (rebreather mask malfunction, hypoxic mix on a ventilator, sealed environment). Treat by correcting the drive (naloxone, BiPAP, ventilatory support) or the FiO₂ (supplemental oxygen, descent from altitude).

**Widened gradient.** Hypoxemia *is* in the lung. The next move is the response to supplemental oxygen. If PaO₂ jumps when FiO₂ goes from 0.21 to 1.0, the cause is V/Q mismatch — pneumonia, asthma, COPD exacerbation, pulmonary edema, early PE. If PaO₂ barely budges, the cause is true shunt — ARDS, hepatopulmonary syndrome, complete airway obstruction, large right-to-left intracardiac shunt. Diffusion limitation (interstitial fibrosis, ILD) sits in between — usually responds to high FiO₂ but never normalizes. Low mixed-venous O₂ (sepsis, cardiac arrest, severe anemia) shows up as a widened gradient too, because the deoxygenated blood returning to the lung cannot catch up no matter how good the alveolar side is.

## The Worked Examples

Two ABGs illustrate the wide range of conclusions the gradient drives.

**Example 1 — elevated A-a, V/Q mismatch.** A 60-year-old patient on room air with PaO₂ 55, PaCO₂ 32, FiO₂ 0.21. Alveolar calculation: 0.21 × (760 − 47) − 32 / 0.8 = 109.7 mmHg. Gradient = 109.7 − 55 = **54.7 mmHg**, against an expected normal of (60 + 10) / 4 = 17.5. Ratio 3.1×. Mildly low PaCO₂ (the patient is hyperventilating to compensate) with a markedly widened gradient points at V/Q mismatch — pneumonia, asthma, PE, early pulmonary edema. The right next move is a chest film and a CT-angiogram, not a BiPAP ramp.

**Example 2 — normal A-a, pure hypoventilation.** A 40-year-old with PaO₂ 60, PaCO₂ 70, FiO₂ 0.21. Alveolar: 0.21 × 713 − 70 / 0.8 = 62.2 mmHg. Gradient = 62.2 − 60 = **2.2 mmHg**, against an expected 12.5. Ratio 0.2× — far below normal, but the patient is hypoxemic because the PaCO₂ is so high that oxygen is being displaced from the alveolus. Classic opioid overdose, neuromuscular weakness, or severe CNS depression. Treat the drive (naloxone, BiPAP, intubation), not the lung.

## Common Pitfalls at the Bedside

Three mistakes show up over and over.

**1. Forgetting to adjust atmospheric pressure.** At 5,000 feet (Denver is ~5,280 ft, P_atm ≈ 630 mmHg), the alveolar term drops by ~17%, and the gradient narrows in absolute terms even when the physiology is the same as sea level. Always pass the actual P_atm when the patient is not at sea level; otherwise you under-call severity at altitude and over-call it on FiO₂ 1.0 patients coming back from altitude.

**2. Trusting a single FiO₂ without checking the device.** Ventilator FiO₂ is supposed to match the dial but only after calibration. Nasal cannula "3 L" is not FiO₂ 0.30 — actual inspired fraction is closer to 0.32 plus a dilution term from the patient's inspiratory flow. Use the calculator's FiO₂ field as documented, but cross-check the ABG's PaO₂/FiO₂ ratio (P/F) whenever intubation is in play — a P/F below 300 is mild ARDS, below 100 is severe.

**3. Treating a "normal" gradient as normal physiology.** A young 25-year-old with A-a = 5 mmHg is fine. A 70-year-old with A-a = 12 mmHg looks normal but is significantly above that patient's expected 20 — still abnormal for them. Always use the age-adjusted expected, not the population range, when calling the gradient "normal".

## When the Number Doesn't Fit

Two clinical situations routinely confuse the gradient interpretation.

**On 100% oxygen.** A patient on FiO₂ 1.0 (post-intubation) has a normal PaO₂ target of ~500 mmHg at sea level (about 5× the FiO₂ 0.21 baseline). Anything below ~300 mmHg on FiO₂ 1.0 is intrapulmonary shunt. The A-a gradient still widens here, but the P/F ratio is the more useful bedside number — under 300 maps onto mild ARDS, under 100 onto severe. Both can be derived from the same ABG inputs.

**White-out lungs.** A patient with diffuse bilateral infiltrates and a PaO₂ of 50 on BiPAP with FiO₂ 0.6 has a PAO₂ of roughly 0.6 × 713 − PaCO₂/0.8 ≈ 400, gradient ≥ 350. That is severe shunt physiology, and the gradient calculation quantifies it — but the bedside eye often catches the trend before the lab does. Use the gradient to *confirm* what you already suspected, not to *replace* clinical judgement.

## Closing the Loop

The A-a gradient is one of the few bedside numbers that survives direct inspection: you can see the algebra, age-adjust it, and decide whether the lung is failing or the drive to breathe is failing. The [A-a Gradient calculator](https://elysiatools.com/en/tools/a-a-gradient-calculator) automates the alveolar gas equation, normalizes the result against `(Age + 10) / 4`, and prints the gap as a multiple of normal — keeping the patient's full ABG and altitude in scope. Pair it with the rest of the [Health calculator family](https://elysiatools.com/en/tools) for adjacent arterial blood gas interpretations (PaO₂/FiO₂ ratio, oxygenation index, lactate clearance) and the surrounding critical-care math.

For more guided field guides on respiratory acid-base, oxygenation indices, and bedside triage numbers, browse the rest of the [Elysia Tools catalog](https://elysiatools.com/en/tools) — every calculator returns both the equation and the age or unit-adjusted reference range, so the next ABG never has to wait for an interpreter.
