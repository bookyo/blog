<strong>Sum forty weighted risk factors, and a 40-year-old same-day surgery patient looks nothing like a 75-year-old hip-fracture patient.</strong> The 2005 Caprini Risk Assessment Model collapses ~40 patient, surgical, and thrombophilia variables into a single integer, then maps that integer onto one of four VTE-prophylaxis tiers. This guide walks through every weighted item, the four management bands, the edge cases the score chart glosses over, and the two structural failures (tier-mismatch and missing thrombophilia audit) that show up most often when the calculator is used as a checklist rather than a stratification tool.

## What the 2005 Caprini Score Actually Weighs

The Caprini Risk Assessment Model is a single-integer sum of roughly 40 weighted risk factors. Each factor contributes 1, 2, 3, or 5 points depending on how strongly it predicts venous thromboembolism in the published 2005 derivation cohort. The weights are not arbitrary: 1-point items are common baseline factors (age 41-60, BMI >25, swollen legs, COPD, OCP/HRT use), 2-point items are moderate surgical or oncologic exposures, 3-point items are personal and family thrombophilia plus age ≥75, and 5-point items are the catastrophic exposures that almost guarantee VTE in the absence of prophylaxis (stroke <1 month, hip/pelvis/leg fracture <1 month, elective major lower-extremity arthroplasty, acute spinal cord injury <1 month, multiple trauma <1 month).

Two structural points matter when reading any [Caprini Score](https://elysiatools.com/en/tools/caprini-score) calculator. First, the score is a *sum*, not a list of flags — a patient with twelve 1-point items scores 12, the same way a patient with three 3-point items plus three 1-point items scores 12, and both belong in the same management tier. Second, the 3-point and 5-point items dominate the arithmetic: any single 5-point exposure pushes the patient into the highest-risk tier regardless of everything else. The score rewards clinicians who actually screen for personal thrombophilia and recent orthopedic/neurologic catastrophe.

## The Four Management Tiers and Where Most Errors Cluster

The 2005 Caprini paper maps the integer score onto four prophylaxis tiers:

- **Score 0** — lowest risk. Mechanical prophylaxis only (early ambulation, intermittent pneumatic compression).
- **Score 1-4** — low to moderate risk. Mechanical prophylaxis is the default; pharmacologic prophylaxis is optional and depends on bleeding risk.
- **Score 5-6** — high risk. Consider LMWH for 7-10 days post-operatively.
- **Score 7-8** — high risk. LMWH for 7-10 days, often extended to discharge plus 7-10 days.
- **Score ≥9** — highest risk. LMWH for 30 days is the published recommendation.

Most calculator errors cluster around the **tier boundary** between 4 and 5, and between 8 and 9. A patient who scores 4 is in mechanical-only territory; one who scores 5 jumps to consider-LMWH. The single missing factor that flips the tier most often is the personal-VTE-history item (3 points), followed by the family-VTE-history item (also 3 points) and the 5-point orthopedic/neurologic exposures. The calculator catches these when used as a checklist; the typical clinical error is omitting one because the clinician "didn't think to ask."

## The 3-Point Thrombophilia Cluster Is Where the Audit Breaks

The 3-point cluster — factor V Leiden, prothrombin 20210A, lupus anticoagulant, anticardiolipin antibodies, elevated homocysteine, heparin-induced thrombocytopenia (HIT), and other thrombophilia — is the failure mode of the chart-based Caprini score. Most clinicians default to "no known thrombophilia" because they have not ordered the workup. The structural fix is to either (a) explicitly state "thrombophilia workup not performed" and treat the 3-point cluster as "unknown = score 0", or (b) order the relevant labs pre-operatively and score them in. Both are defensible, but only one should be documented.

A second audit failure mode in the same cluster is the *family history* item. Family VTE history in a first-degree relative is a 3-point exposure; it is the single highest-yield item to ask about, because it changes the management tier in roughly one in twenty pre-operative patients without a personal history. Run the [Caprini Score field guide](https://elysiatools.com/en/tools/caprini-score) tool with an explicit "ask every patient about family VTE" workflow before scoring.

## The 5-Point Orthopedic and Trauma Exposures Override Everything

Five items in the model are worth 5 points each: stroke <1 month, elective major lower-extremity arthroplasty, hip/pelvis/leg fracture <1 month, acute spinal cord injury <1 month, and multiple trauma <1 month. Any one of these alone pushes the patient into the highest-risk tier (≥9 combined with any baseline factor, or ≥5 on its own with no other items). These are also the items that *should* trigger automatic extended-duration LMWH — typically 30 days for total hip or knee arthroplasty, 28-35 days for hip fracture surgery.

The common calculator failure mode here is double-counting: a patient with a hip fracture who also has age ≥75 (3 points) plus recent major surgery (2 points) may end up at 10, when the 5-point fracture exposure already covers most of the VTE risk. The published Caprini paper does not subtract overlap; the score is additive by design, and a 10 is still a 10 in terms of prophylaxis tier. The clinical lesson: do not "discount" the 5-point exposure because other items also score high — every item counts.

## The Pediatric and Pregnancy Edges

The 2005 derivation cohort is adult surgical patients. Two edges are worth flagging:

- **Pediatric patients**: the published model is not validated for children under 18; do not score pediatric patients against Caprini and treat the output as clinically actionable.
- **Pregnancy and postpartum (≤1 month)**: this is a 1-point item in the model. Pregnancy-related VTE risk is much higher in the immediate postpartum period than during pregnancy itself; some institutions use a *modified* Caprini score that bumps postpartum to 3 points and adds cesarean delivery as a 2-point item. If the calculator returns 1-2 for a postpartum patient, treat that as a floor, not a ceiling.

The published [calculator](https://elysiatools.com/en/tools/caprini-score) tool flags both edges in the output, but the clinical decision still belongs to the treating team.

## When Caprini and Bleeding Risk Disagree

Caprini scores VTE risk. It does not score bleeding risk. A patient with active GI bleed, intracranial hemorrhage, or platelet count <50,000 should not receive pharmacologic prophylaxis regardless of Caprini tier — the LMWH 7-10 day or 30-day recommendations assume the patient is not actively bleeding. The published model pairs Caprini with a separate bleeding-risk assessment (often IMPROVE-B or similar); the calculator is silent on this by design.

The typical workflow is: run Caprini first, identify the target prophylaxis tier, then run a bleeding-risk tool, and reconcile. If bleeding risk is high and Caprini tier is ≥5, the patient still gets mechanical prophylaxis (intermittent pneumatic compression, graduated compression stockings) but pharmacologic prophylaxis is held or shortened. Document the reconciliation — "Caprini 7, IMPROVE-B 5, holding LMWH pending GI consult" is the kind of note that survives an audit.

## Where the Calculator Adds the Most Value

Three clinical situations benefit most from a structured Caprini calculation:

- **Pre-operative clearance** for elective general, oncologic, gynecologic, or urologic surgery — the score drives the discharge prophylaxis plan.
- **Same-day surgery decision support** — patients scoring ≥5 on intake should not be sent home without a documented prophylaxis plan.
- **Extended prophylaxis planning** for total hip or knee arthroplasty, hip fracture surgery, and major cancer surgery — the calculator maps directly onto the 30-day LMWH recommendation.

In each case the value is not the integer but the *checklist*: the score forces a thrombophilia audit, a family-history ask, and an orthopedic-exposure check that are easy to skip in a busy pre-op clinic. Use the [Caprini Score tool](https://elysiatools.com/en/tools/caprini-score) with that workflow in mind.

## Limitations and When to Step Outside the Model

The 2005 Caprini derivation cohort is non-randomized and weighted toward general, vascular, and urologic surgery. The model is less validated for trauma, neurosurgical, and obstetric populations, and the published management tiers were derived from 2005-era LMWH dosing regimens. Newer direct oral anticoagulants and extended-duration protocols are not in the original model.

Two practical off-model situations:

- **Trauma patients**: many institutions use the modified Greenfield risk profile or the Parkland protocol instead. Caprini is a fallback.
- **Medical inpatients with prolonged immobility**: the Padua Prediction Score or the IMPROVE score are the published tools, not Caprini. Do not score a medical patient against Caprini and call it the same assessment.

Use the calculator where it is validated, supplement with the bleeding-risk tool, and document the prophylaxis plan in the chart. The score is one input to a decision; it is not the decision itself.

---

*Not medical advice. The 2005 Caprini Risk Assessment Model is a published risk-stratification tool; clinical decisions remain with the treating clinician.* For more tools, browse the [full elysia-tools library](https://elysiatools.com/en/tools).