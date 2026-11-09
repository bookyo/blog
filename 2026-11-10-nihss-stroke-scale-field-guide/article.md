---
title: Your NIHSS Total Is a Handoff, Not a Diagnosis
---

<strong>A stroke score you cannot unpack is a number with a hospital attached.</strong> The NIH Stroke Scale squeezes a full neurological exam into a single integer between 0 and 42, and clinicians hand that integer to each other across shifts, units and hospitals as though it were the patient. It is useful. But two patients who both score 16 can need opposite plans.

## The total is a compression, and compression drops the useful part

A sum is commutative. Sixteen points arrived at through dense hemiparesis and sixteen arrived at through drowsiness, mutism, and a missing gaze are the same sixteen as far as addition is concerned. As far as the patient is concerned, they are different diseases.

The scale cuts a long bedside exam into fifteen checkboxes and then adds them up. Here is the smallest case. Give one patient a completely paralyzed leg, and item 6 scores 4. Now take another patient who is drowsy (1a = 1), gets one of two orientation questions wrong (1b = 1), follows one of two commands (1c = 1), and has mild slurring (10 = 1). That is also 4.

Both land in the 1 to 4 band, and both get read as a minor stroke. One cannot walk. The other cannot reliably tell you what year it is.

The calculator at [Elysia Tools](https://elysiatools.com/en/tools/nihss-score) returns the component scores alongside the total for exactly this reason. The breakdown is the part you can act on.

## Fifteen scored items do not carry equal weight

The four limb items, 5a, 5b, 6a and 6b, contribute 16 of the 42 available points. That is 38.1% of the whole scale, and the other eleven items share the remaining 26. Language maxes out at 3. Facial palsy maxes out at 3. Ataxia maxes out at 2.

This weighting is structural, not a bug in the implementation. For example, a patient whose only deficit is global aphasia scores 3 and lands in the band labeled "Minor stroke (1–4)". A patient with moderate weakness in all four limbs scores 16 and lands in "Moderate to severe stroke (16–20)". Both numbers are arithmetically right and clinically misleading, in opposite directions.

The weighting is not folklore. The original derivation is a 1989 Stroke paper by Brott and colleagues, and the NINDS instructions that ship with the scale define what each grade means. Inter-rater agreement on the instrument has been reported to vary by item, which is the practical reason to record components instead of only a total.

<ul><li><strong>Motor dominates.</strong> Four items carry 38.1% of the range, so limb weakness drives most of the total.</li><li><strong>Cortical signs are cheap.</strong> Language, neglect and visual fields together cap at 8 points.</li><li><strong>The top of the range is theoretical.</strong> A 42 requires coma plus total bilateral motor loss, and real acute scores cluster far lower.</li></ul>

## A 16 and an 18 can be clinically opposite

The tool ships a worked example that scores a right middle cerebral artery syndrome at 16: drowsy, forced gaze, complete hemianopia, partial facial palsy, arm and leg weakness on one side, mild sensory loss, mild dysarthria, partial neglect.

Now build a different patient. Bilateral arm and leg weakness at grade 4 across all four limb items scores 16 before you add another finding. The arithmetic is short: 4+4+4+4. Toss in severe dysarthria for 2 more, and the total is 18. Consciousness is normal and language is intact. This is the locked-in picture, and it produces a higher number than the MCA syndrome while being far easier to miss on a score sheet, because the two heaviest groups of items are already spent.

Two points apart, opposite clinical posture. One patient forces a reperfusion decision. The other forces a reliable communication channel and a low threshold for recognizing that mute and quadriparetic is not the same as unarousable.

## Where the scale goes quiet

There is no item for gait, stance, trunk control or vertigo. A vertebrobasilar or cerebellar stroke can present with unsteady walking, double vision and nausea and still score 1 or 2, because nothing on the form asks about any of it. Ataxia exists as item 7, but it caps at 2 and only counts after you find it.

This is a known limitation, not a hidden defect, and it is why a low NIHSS in a patient who reports only dizziness is not reassuring. When the history points to the posterior circulation, the score is the wrong instrument, and the exam you do with your hands outranks the number.

## Zero is not the same as fine

A score of 0 means no measurable deficit on these fifteen items. It does not mean the patient is well. The form does not test standing, walking or fine dexterity. Someone can score 0, be unable to cross a room without holding a wall, and still be counted under a band labeled no stroke symptoms.

The band text the tool returns is precise about the limit: "No measurable neurologic deficit on the scale. Clinical context still guides workup." The clause after the period is doing the real work, and it is the line most readers skip.

## The tool's text disagrees with itself in two places

Both are visible in the data the calculator ships with, which makes them worth flagging.

<strong>The motor summing rule.</strong> The English description states that both left and right limb motor scores are summed into the total. All six localized descriptions say the more affected side enters the total. Those cannot both hold, and only one describes the standard scale, which sums both sides.

<strong>The worked example's lateralization.</strong> The arithmetic is correct: 1+1+1+2+2+2+0+2+0+2+0+1+0+1+1 does equal 16. The narrative breaks down under inspection. Right hemiparesis points at a left hemisphere lesion, and leftward gaze deviation points the same way, because the eyes are driven toward the damaged frontal eye field. The partial neglect points the other way. The label says right MCA.

Neither observation changes what the calculator computes. Both are reasons to read the components and not the summary line.

## Score the same arm as the last person

Inter-rater reliability on this scale is examiner-dependent, and the manifest states that plainly. The practical version: use the same item order, read the same instructions, score the first attempt, not the best one, and do not round a 3 up to a 4.

The usual disagreement points are two: 1a, because drowsy and stuporous are judgment calls, and item 9, because scoring language in a patient who is intubated, deaf or a non-native speaker of the language you are testing is a different task than the item describes. Score before the imaging comes back. The value of the number lies in the rule it was collected under, not in the collecting.

## What the number is for

Three jobs, and none of them is diagnosis. It sets a conversation about reperfusion eligibility. It tracks change, and a meaningful shift in the total over hours tells you something the absolute value cannot. It stratifies patients so research and quality reporting compare like with like.

What it cannot do is tell you what is wrong or what will happen. A 21 in a 92-year-old with a large completed infarct and a 21 in a 45-year-old four hours into symptoms are the same number with sharply different conversations attached.

Explore the calculator at [Elysia Tools](https://elysiatools.com/en/tools/nihss-score); it reports the more-affected motor side next to the total, which is the detail hand-written notes tend to drop. The rest of the catalog sits at [elysiatools.com](https://elysiatools.com/en/tools).

The score is a handoff, not a verdict. Two patients can share a 16 and need completely different phone calls, and the number alone will never tell anyone which one is on the table. So write the sixteen down, with the arm and the gaze and the words that went missing, because the total will outlive your shift and nobody downstream can re-examine an exam you did not record. The scale measures the stroke. What makes the measurement matter is all that you choose to write beside it. If the next clinician cannot unpack your number, what did it buy them?
