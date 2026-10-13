# Corrected QT (QTc) Field Guide: When Three Formulae on the Same Strip Disagree by 80 ms

When the ECG printer says **QT 380 ms** and the cardiologist's note says **QTc 460 ms**, every formula on the strip picks its own RR denominator — and on the same patient the **Bazett, Fridericia, and Framingham** QTc values can sit 30 to 80 ms apart. The Corrected QT (QTc) Calculator at [Elysia Tools](https://elysiatools.com/en/tools/corrected-qt-bazett-fridericia) runs all three formulas against the same QT and HR inputs, so the variation is transparent instead of hidden inside a single-channel printout. This field guide explains why three formulae on the same strip give three different QTc values, which one the drug-trial literature prefers, and how to read the calculator's output against the AHA/ACC and ICH E14 thresholds without re-deriving the arithmetic on a sticky note.

## The Three Formulae on One Strip

Bazett (1920): `QTc = QT / sqrt(RR)`. The classic — but it **over-corrects at high heart rate** and **under-corrects at low heart rate**, so a 100-bpm patient gets a QTc that runs hot and a 50-bpm patient gets one that runs cold. Fridericia (1920): `QTc = QT / RR^(1/3)`. The cube-root exponent spreads the penalty more evenly across the heart-rate range and is what most modern drug-QT studies report. Framingham (1992): `QTc = QT + 0.154 * (1 - RR)`. A simple linear regression that holds up at typical adult resting rates (60-90 bpm) but was not designed for the extremes.

The calculator takes two inputs: **QT (ms)** and **HR (bpm)**. When RR is not supplied directly, it derives `RR = 60 / HR` so the same QT string produces three comparable QTc values. Open the tool at [Elysia Tools](https://elysiatools.com/en/tools/corrected-qt-bazett-fridericia) and watch a 380 ms QT at 80 bpm produce **QTc Bazett ≈ 439**, **QTc Fridericia ≈ 422**, and **QTc Framingham ≈ 430** — a 17 ms spread that you can hand a colleague without context.

## Reading the Prolongation Thresholds

The AHA/ACC/HRS 2009 statement and the ICH E14 guidance set the same adult cut-offs: **men > 450 ms borderline** and **> 480 ms prolonged**; **women > 460 ms borderline** and **> 480 ms prolonged**; **> 500 ms is markedly prolonged** and triggers a review of QT-prolonging drugs plus K⁺ / Mg²⁺ / Ca²⁺. The calculator's interpretive band prints the threshold trip for each formula, so a single QTc Bazett of 472 puts the patient in "borderline" under Bazett but "normal" under Fridericia — and you decide which exponent earns the call.

## When the Three Disagree Most

The disagreement peaks at the rate extremes. At HR 120 bpm (RR = 0.5 s), Bazett's sqrt denominator penalizes the QT aggressively; at HR 40 bpm (RR = 1.5 s), Fridericia's cube-root falls faster than Bazett's. The calculator's side-by-side layout makes this real: a 420 ms QT at HR 50 bpm returns **Bazett ≈ 514**, **Fridericia ≈ 462**, **Framingham ≈ 446** — a 68 ms range that would never fit on a single ECG label. For drug studies, ΔQTc > 30 ms is concerning and ΔQTc > 60 ms is a regulatory signal — the calculator shows the delta against a baseline alongside the absolute value.

## Worked Example: 50-Year-Old on Sotalol

Input: **QT = 440 ms**, **HR = 60 bpm** (`RR = 1.0 s`). Output: **QTc Bazett = 440 ms** (borderline but normal), **QTc Fridericia = 440 ms**, **QTc Framingham = 440 ms**. Because `RR = 1.0 s`, every formula's correction factor equals 1 — the three formulae agree by construction. Now change HR to 90 bpm (RR = 0.667 s), QT stays 440 ms: **QTc Bazett ≈ 538 ms** (markedly prolonged — red flag), **QTc Fridericia ≈ 487 ms** (prolonged), **QTc Framingham ≈ 472 ms** (prolonged). The same QT string, the same patient, three different verdicts. Use the [QTc Calculator](https://elysiatools.com/en/tools/corrected-qt-bazett-fridericia) to walk this example before clinic.

## Why the Drug-Trial Literature Picks Fridericia (Usually)

ICH E14 doesn't mandate one formula, but the consensus in thorough-QT studies is to **report Fridericia as the primary endpoint** and Bazett as a sensitivity analysis. The reason is the rate-correction bias: Bazett's sqrt exaggerates QTc at high rates (where β-agonists and SVTS push patients during a washout) and compresses it at low rates (where β-blockade and atrial pacing land them). Fridericia's cube-root tracks drug-induced changes more linearly. The calculator's three-format output lets the same clinical visit produce both a Bazett number (for the chart) and a Fridericia number (for the trial report) without re-entering data.

## Edge Cases the Calculator Handles

When the user enters HR but no RR, the tool derives `RR = 60 / HR` — fine for sinus rhythm. For atrial fibrillation the RR varies beat-to-beat; the calculator flags that and asks for an averaged RR or an averaged QT over 10 beats. Pacemaker-dependent rhythms at fixed 60-bpm pacing produce RR = 1.0 s by definition, so all three formulae collapse to the raw QT. The calculator exposes each case as a label under the result so the interpretation follows the rhythm strip, not just the rate.

## When to Escalate Beyond the Calculator

Any **QTc > 500 ms** on any formula is markedly prolonged — review the medication list (antiarrhythmics, macrolides, fluoroquinolones, ondansetron, methadone, antipsychotics), check K⁺ / Mg²⁺ / Ca²⁺, and hold the next dose of any QT-prolonging agent until the electrolyte panel returns. **ΔQTc > 60 ms** from baseline is a regulatory signal in a trial setting and a clinical signal on the ward. The calculator rounds to the nearest millisecond and prints the delta next to the threshold so the call does not depend on mental math.

## Closing

Three formulae on the same strip disagree by tens of milliseconds — that's not a bug, that's the math. The [Corrected QT (QTc) Calculator](https://elysiatools.com/en/tools/corrected-qt-bazett-fridericia) runs Bazett, Fridericia, and Framingham against the same QT and HR inputs so the disagreement is visible instead of buried. Pick the formula the trial or the institutional protocol requires, report all three when the rate sits at the extremes, and treat **> 500 ms** or **Δ > 60 ms** as a stop-and-review line. Explore more cardiology and measurement tools at [elysiatools.com](https://elysiatools.com/en/tools).
