---
title: A Normal RPP Can Hide a Collapsing Circulation
---

<strong>Your chart already holds the two numbers.</strong> Multiply them, a heart rate of 72 against a systolic pressure of 120 giving 8,640, and you have the rate-pressure product, the cheapest index of how much oxygen your heart is asking for. The arithmetic takes one second, but the reading takes judgement, because a product cannot tell you which factor did the work.

## Two Numbers Multiply Into a Demand Estimate

Cardiac muscle extracts oxygen near its maximum even at rest, so demand has to be met by raising flow. Two levers set that flow: how often the ventricle ejects, and the pressure it ejects against. The rate-pressure product wraps both into one scalar with units of beats per minute times millimetres of mercury, which is why clinicians also call it the double product.

A resting adult charted at 120 over 72 returns 8,640. Written as 8.64 times ten to the third it sits inside the 6,000 to 10,000 band that Gobel's 1978 Circulation paper tied to directly measured myocardial oxygen consumption in the catheterization laboratory. That validation is why the number survives six decades of alternatives: it is not a scoring heuristic assembled from expert opinion, it is a product that tracked measured oxygen consumption closely enough to be useful at the bedside. The study's own title states the claim plainly: the product indexes oxygen consumption during exercise in patients with angina.

What makes it useful is also what makes it risky. There is no arithmetic error to catch. A wrong band label still multiplies correctly.

You can run the two-factor version at [Elysia Tools](https://elysiatools.com/en/tools/rate-pressure-product); it returns the product, the thousands-scaled value, and the band label in one pass.

## Why Heart Rate Is the Cheaper Lever

Both factors raise demand. They do not raise it equally per unit of clinical effort.

A 20 mmHg rise in systolic pressure, starting from 120, lifts demand by 16.7 percent. Doubling the heart rate doubles it outright, and doubling is easy to do by accident with fever, pain, hypovolaemia or anxiety. That asymmetry forces a stenosed coronary artery to fail sooner under tachycardia than under mild hypertension: the rate multiplies the number of pressure-time ejections per minute, and each ejection must squeeze past the same fixed narrowing.

Beta blockade exploits the asymmetry. One drug class cuts rate and pressure together, and the two reductions compound instead of adding.

## Where the Bands Fall, and Where the Label Slips

The calculator breaks a result into three bands using strict inequalities:

<ul><li>Below 6,000 returns Low RPP</li><li>6,000 through 12,000 returns Normal RPP</li><li>Above 12,000 returns High RPP</li></ul>

Read the edges carefully, because they are not where the prose suggests. For example, a systolic of 100 against a rate of 120 lands on exactly 12,000 and returns Normal. One extra beat per minute returns High. The 12,000 line is exclusive, so the angina threshold named in the same output begins at 12,001.

The wider gap sits between the label and the interpretation string. According to the tool's own prose, 6,000 to 10,000 is normal at rest and 10,000 to 12,000 is typical for light exertion, yet both print the single word Normal. A patient at 135 over 88 returns 11,880, labelled Normal, while the sentence beside it describes light exertion. Neither statement is false. The label is coarser than the prose, and a reader who scans only the label inherits that coarseness.

## The Case Ladder: Four Patients, One Formula

Start simple and let the formula do the work.

A treated hypertensive on a beta blocker, 120 over 49, returns 5,880: Low RPP. Demand is genuinely low, the drug is doing its job, and nothing needs fixing.

A healthy adult at rest, 120 over 72, returns 8,640: Normal RPP, and the number matches the physiology.

A patient at peak treadmill effort, 150 over 110, returns 16,500: High RPP. In this case high is not a defect, it is the point of the test. Demand above 12,000 with a reversible ST change marks a positive study, not a crisis.

Now the case that breaks the reading. A patient in circulatory shock, systolic 60, compensatory tachycardia of 155, returns 9,300: Normal RPP, a mere 8 percent above the resting adult in the second case. Those two patients share a band and share nothing else. One heart asks for 8,640 units of oxygen at a normal pressure; the other asks for 9,300 while delivering a fraction of the perfusion. The product forces two opposite errors into one reassuring number.

## Stress Testing Wants the Product, Not the Parts

Exercise physiology is where the scalar earns its keep. During a graded protocol the workload rises until demand outstrips a fixed supply, and the product rises with it: 90 over 180 returns 16,200, and 105 over 200 returns 21,000, roughly 2.4 times the resting figure.

Because peak demand is reproducible, the observed value works as a workload receipt. Two tests on the same patient months apart can be compared on the number reached at the ischemic threshold, and a threshold falling from 18,000 to 14,000 shows something the reported stage labels hide. Cardiology guidelines lean on the same product when they express exercise intensity as a multiple of resting demand.

The trap is comparing peak values across patients. A young athlete reaching 21,000 and a patient with aortic stenosis reaching 21,000 hold the same demand number and completely different supply. The product measures the bill, not the bank balance; it is measured, not modelled.

## Titrating a Beta-Blocker With One Multiplication

Two flows run through the same decision.

Success flow. After a myocardial infarction the target is a resting rate near 55 to 60. At 130 over 58 the product returns 7,540, comfortably inside the normal band, and the dose holds while the number improves. The number moves in the direction the pharmacology predicts and the patient is asymptomatic, so up-titration gets judged against a target, not a feeling.

Failure flow. Push the same patient one step further and the rate falls to 52 while systolic sags to 95, returning 4,940. Low RPP, and a patient who is dizzy on standing. The number is excellent; the circulation is not. A low product cannot separate demand successfully reduced from pressure too low to perfuse, because a product of two small numbers is small either way.

## What One Multiplication Cannot See

The limit is structural. The product carries the rate and pressure components of myocardial oxygen demand and drops the rest:

<ul><li>Contractility, since catecholamines and inotropes raise demand with no change in the two inputs</li><li>Wall stress and ventricular radius, since for instance a dilated ventricle spends more oxygen at an identical product</li><li>Ejection time, since a longer systole raises the pressure-time integral the product ignores</li><li>Oxygen-carrying capacity, since anaemia lowers supply while the demand number stays flat</li><li>The supply side entirely, since no input describes a stenosis, a spasm, or a collateral bed</li></ul>

Two refinements were designed to fix the contractility gap: the tension-time index, and the triple product, which scales the product by ejection time. Neither has displaced the two-factor version at the bedside, and the reason is not accuracy. A number a nurse can compute from the chart in one second and reproduce exactly on the next shift beats a better model nobody calculates.

## How to Read the Number Without Overreading It

Three checks, in order.

Compute the product and its band, then ask which factor carries it. A high value driven by rate and a high value driven by pressure point at different interventions. Next ask whether the inputs agree with the patient in front of you: a normal product with a systolic of 60 and a rate of 155 is a warning, not a clearance. Last, check the supply side, because the arithmetic holds no data about it.

The calculator accepts systolic pressures from 40 to 300 mmHg and heart rates from 20 to 250 bpm, which covers all physiologic values you will chart and rejects typos. Run it at [Elysia Tools](https://elysiatools.com/en/tools/rate-pressure-product), browse the wider cardiology set at [the Health category](https://elysiatools.com/en/categories/health), and find related bedside indices in the full catalog at [elysiatools.com](https://elysiatools.com/en/tools). It is a labelled arithmetic assistant, not a diagnostic.

I began by treating 8,640 as a reassuring number. I no longer do. It is a product, and products hide their factors, so a rate of 155 against a systolic of 60 lands in the same band as a runner at rest. The question worth asking is not whether your rate-pressure product is normal. It is which of the two numbers you would move, and what moving it would cost.
