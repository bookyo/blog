<strong>The corrected-QT interval is not a measurement; it is a choice.</strong> The same raw QT value gives you three different numbers depending on which formula you pick — Bazett's square-root correction, Fridericia's cube-root, or Framingham's linear regression — and the one your calculator returns tells your reader whether the patient looks fine, borderline, or prolonged. That is the entire point of [the Corrected QT (QTc) Calculator](https://elysiatools.com/en/tools/corrected-qt-bazett-fridericia): one input, three formulae, side-by-side output, with the threshold tables that turn a number into a clinical decision.

## Why Three Formulae for the Same Number

The raw QT interval changes with heart rate. A 380 ms QT is normal at 60 bpm and abnormal at 120 bpm. To compare QT values across patients — or across time in one patient — you need a heart-rate–corrected version, and the correction is where the disagreement lives.

**Bazett (1920)** divides QT by the square root of the RR interval: `QTc = QT / sqrt(RR)`. It is the most cited formula because it appears in textbooks, but it over-corrects at high heart rates and under-corrects at low ones — exactly the regions where the ECG is most clinically interesting (tachyarrhythmia workup, bradyarrhythmia drug studies).

**Fridericia (1920)** divides QT by the cube root of RR: `QTc = QT / RR^(1/3)`. The exponent is shallower than Bazett's, which means the correction is gentler at the extremes. Modern ICH E14 regulatory studies and most QT-prolonging drug development use Fridericia as the primary endpoint because the curve hugs the data better across the 40–120 bpm range.

**Framingham (1992)** uses a simple linear regression: `QTc = QT + 0.154 * (1 - RR)`. No roots, no fractions, no power-function gotchas. It is robust at typical adult heart rates (60–90 bpm) and behaves reasonably at extremes, which makes it a sensible default when the heart rate is normal.

The calculator computes all three. When the three disagree — and they will, especially outside 60–90 bpm — the discrepancy is information, not noise.

## Anatomy of the Input

The input panel takes three fields. **QT (ms)** is the uncorrected interval measured from the start of the Q wave to the end of the T wave on lead II or V5, ideally averaged over 3–5 beats. **Heart rate (bpm)** drives RR via the inverse `RR = 60 / HR`, so the calculator does not require you to type RR separately; if you do provide RR directly, the calculator uses that and skips the derivation. **RR (s)** is optional.

All three formulae converge when heart rate sits near 60 bpm. The interesting behavior lives at the edges: at 45 bpm (sleep, athletes, beta-blocker effect), Bazett under-corrects and reports a smaller QTc than Fridericia does; at 130 bpm (sepsis, SVT, exercise), Bazett over-corrects and inflates the QTc. Reporting only Bazett in those settings makes a normal patient look borderline, or a borderline patient look normal.

## Reading the Output: The Three QTc Numbers

The output panel displays the three QTc values side by side in milliseconds, plus a derived flag against the AHA/ACC/HRS 2009 thresholds:

- **< 450 ms (men) / < 460 ms (women)** — normal
- **450–480 ms (men) / 460–480 ms (women)** — borderline; review QT-prolonging drugs, check K+/Mg2+/Ca2+
- **> 480 ms** — prolonged
- **> 500 ms** — markedly prolonged; high torsades-de-pointes risk

A ΔQTc increase of more than 30 ms from baseline is concerning in drug studies; more than 60 ms is clearly abnormal under ICH E14. The calculator returns the absolute QTc and the ΔQTc when you provide a baseline.

## When Bazett Misleads You

Bazett is the default in many EMRs and bedside references, which is a problem at the extremes. Two cases illustrate the trap:

**Case A: a 28-year-old presenting with palpitations at 130 bpm, raw QT 320 ms.** Bazett returns 470 ms (prolonged). Fridericia returns 446 ms (normal-borderline). Framingham returns 437 ms (normal). The patient is on no QT-prolonging drugs, electrolytes are normal. Bazett is alarming the clinician; the other two formulae disagree. The right move is to repeat the ECG at a lower heart rate after a beta-blocker — Bazett's over-correction at 130 bpm is the noise, not the signal.

**Case B: a 72-year-old on sotalol, heart rate 50 bpm, raw QT 480 ms.** Bazett returns 411 ms (normal — under-correction at low HR). Fridericia returns 444 ms (normal-borderline). Framingham returns 459 ms (borderline). All three say "do not escalate sotalol," but the spread from 411 to 459 is itself a clinical finding — the borderline Framingham reading is closer to the truth than the reassuring Bazett number.

This is the case for always reporting all three.

## Common Precipitants of QT Prolongation

A prolonged QTc is rarely idiopathic in adults. The calculator pairs the output with the precipitants list to keep the differential in view:

<ul><li><strong>QT-prolonging drugs</strong>: macrolides (azithromycin, erythromycin), fluoroquinolones (especially moxifloxacin), class IA and class III antiarrhythmics (quinidine, sotalol, dofetilide), antipsychotics (haloperidol IV, ziprasidone), methadone, ondansetron at high doses, and many others. CredibleMeds maintains the canonical list.</li><li><strong>Electrolyte disturbance</strong>: hypokalemia, hypomagnesemia, hypocalcemia.</li><li><strong>Congenital LQTS</strong> — consider if the patient is young, has a family history of sudden cardiac death, or presents with syncope on auditory triggers.</li><li><strong>Bradycardia, acute ischemia, hypothermia</strong> — all prolong QT independently of drugs.</li></ul>

The calculator does not adjudicate which of these is operative — that is a clinician's call — but it surfaces the list so the next step is obvious.

## Why the Three Thresholds for Men vs Women

The AHA/ACC/HRS 2009 thresholds are sex-specific: women tolerate slightly longer QT intervals at baseline because the repolarization reserve is smaller (testosterone shortens QT; estrogen and progesterone lengthen it). Reporting a single threshold hides this. The calculator applies the sex-specific threshold you select and flags borderline vs prolonged accordingly. A 470 ms QTc in a man is borderline; in a woman, it is approaching prolonged.

## How to Use the Calculator in Practice

Three workflows that come up repeatedly in cardiology and emergency-medicine practice:

<ol><li><strong>Triage ECG with QT-prolonging symptoms</strong> — enter the measured QT and the rhythm-strip heart rate, read the three QTc values, apply the threshold for the patient's sex, and decide whether to hold the next dose of the offending drug.</li><li><strong>Drug-initiation baseline and follow-up</strong> — measure QTc before starting sotalol, methadone, or dofetilide, then re-measure after the loading dose. The calculator returns ΔQTc when you provide the baseline.</li><li><strong>Syncope workup</strong> — when the cause is unclear, a borderline QTc in a young patient with a suggestive family history shifts the differential toward congenital LQTS and warrants a cardiology referral.</li></ol>

The tool lives at [elysiatools.com/en/tools/corrected-qt-bazett-fridericia](https://elysiatools.com/en/tools/corrected-qt-bazett-fridericia) — paste the QT and HR, read the three numbers, apply the threshold.

## Limitations and a Note on Medical Advice

The calculator is derived from Bazett 1920, Fridericia 1920, Sagie/Framingham 1992, AHA 2009, and ICH E14. It is not medical advice. It does not adjudicate measurement quality — a poorly-measured QT (T-wave flattening, lead misplacement, U-wave inclusion) propagates straight through. It does not store data, does not call the EMR, and does not replace clinical judgment. Use it as a sanity check on your own arithmetic and as a fast second opinion when the bedside number does not match the clinical picture.

<strong>Sources.</strong> Bazett HC. *Heart* 1920;7:353–370. Fridericia LS. *Acta Med Scand* 1920;53:469–486. Sagie A et al. *Am J Cardiol* 1992;70:797–801. AHA/ACC/HRS 2009 recommendations. ICH E14 guidance. MDCalc reference values.

Explore more tools at [elysiatools.com](https://elysiatools.com/en/tools).
