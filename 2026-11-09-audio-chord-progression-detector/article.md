---
title: Your Chord Chart Disagrees With Your Ears. The Grid Is the Reason.
---

<strong>A chord detector does not fail on the chords you hear.</strong> It fails on the boundaries between them. On the four-chord loop half of pop music borrows, a template matcher agrees with your ears almost one second at a time. The disagreements cluster in the 200 to 700 milliseconds where two chords touch, and that is where the interesting harmony lives.

## The Easy Eighty Percent Was Solved Before You Arrived

Name a chord and you can score it. That is the whole trick behind [the Audio Chord Progression Detector](https://elysiatools.com/en/tools/audio-chord-progression-detector), and it explains why these tools look magical on a clean loop and argumentative on a real recording.

The vocabulary is tiny. Twelve roots times nine qualities gives 108 named chords: major, minor, diminished, augmented, sus2, sus4, dominant seventh, major seventh, minor seventh. Each name is a weighted set of pitch classes — the root at 1.0, the third at 0.92, the fifth at 0.78, a seventh at 0.72. Match a measured pitch-class profile against all 108 and take the best fit. There is no search, no model and no training set. It is arithmetic over twelve numbers.

The measurement side is equally plain. Audio is decoded to mono at 11,025 Hz, sliced into 4,096-sample frames of 371 milliseconds with a 2,048-sample hop, so consecutive frames overlap by half. Each frame gets a Hann window, a power spectrum on 2.69 Hz bins, and a peak-pick across the 55 to 2,500 Hz band. Those observed peaks fold into twelve pitch classes, the vector is normalised, and the data that leaves the frame is twelve numbers. One frame in, one chroma vector out.

This works because harmony is coarse. A triad occupies three of twelve pitch classes, so the score question is never ambiguous when the audio is clean. The gap between a good chart and a bad one never sits in the naming step.

## One Second of Audio Is Often Three Chords in a Trench Coat

Here is the mechanism that decides whether your chart matches your ears, and it is not a chord question at all.

Frames are pooled into segments of 1.5, 1.0 or 0.5 seconds — the tool's quick, balanced and detailed resolutions. The chroma vectors inside a segment are summed, normalised once, and classified once. One label per segment. A segment spanning a chord change reports whichever harmony dominates the pooled energy, and the boundary itself is not approximated. It is cut.

Set the grid to 1.5 seconds and a 0.4-second passing chord does not get mislabelled. It gets absorbed into its neighbours. Set the grid to 0.5 seconds and the same passage usually splits into three segments, which is where the passing chord appears for the first time. A twelve-bar blues, for example, changes harmony roughly twice a second — exactly the rate a 1.0-second grid handles worst.

Two settings therefore decide what your chart can show: segment duration and minimum chord duration. Neither one is about chord names.

That reframes the resolution control. It is not a quality slider. It is a claim about how often the song changes harmony, and a wrong claim produces a chart that is internally consistent and audibly wrong.

## What 108 Templates Cannot Name

The vocabulary constraint is worth stating plainly, because most of the disappointment in chord detection traces to a name that was never on the list. A first inversion, for instance, is not a rare edge case; it is in the first bar of a thousand songs.

A first inversion does not exist here. C/E is reported as C, with the bass contributing a 0.06 bonus to the root score — evidence that nudges a decision, not a label. Slash chords, added-note chords, ninths, elevenths, thirteenths, altered dominants and power chords sit outside the 108. A distorted guitar playing root and fifth has no third for the template to find, so the fit falls under the 0.57 floor and the segment reports N: no chord.

That floor is the honest part of the design. When nothing fits well enough, the tool reports nothing instead of guessing. You will see N on the intro swell, on the drum break, and on the overdriven chorus.

## The Confidence Number Is a Margin, Not a Probability

A confidence of 0.55 does not mean "55 percent likely to be right". Read the formula and the number stops pretending.

Confidence is 2.2 times the margin between the best and the runner-up score, plus 0.72 times whatever the best fit exceeds 0.45 by, clamped to the 0..1 range. Both terms reward separation. A clean C major with no rival scores high. A C major sitting next to an A minor seventh — same pitch classes, one rotation apart — scores low even when the fit is excellent, because the margin collapsed.

The practical consequence is not intuitive. Raising the threshold from the 0.2 default toward 0.8 mostly converts ambiguous frames into N. It does not make the ambiguous frames correct. You are choosing how much silence you want in the chart, not how much accuracy.

## The Smoothing Pass Nobody Lists in the Spec

Raw per-segment labels flicker. Sixty seconds of a live take can produce dozens of one-segment anomalies, so the tool runs three passes before you see a chart.

The first fills islands: when the previous and next segments agree and the current one differs, the current label is replaced by the neighbours and its confidence becomes their average. The second collapses sevenths to triads when a seventh does not continue on either side and a neighbouring segment carries the plain triad — protection against a stray seventh element ringing through one window. The third merges segments shorter than the minimum chord duration, from 0.5 up to 4 seconds, defaulting to 0.7.

Each pass encodes a prior. Islands are assumed to be noise. Sevenths without support are assumed to be overtones. Short segments are assumed to be flicker. Those priors remove most of the flicker you would otherwise read as harmony, and they are exactly what erases a genuine passing chord shorter than 0.7 seconds when you leave the default in place.

## A Worked Example: C, Am, F, G at Two Speeds

The tool ships with a four-chord fixture and two documented runs over it, and the pair is the cleanest data on what resolution does and does not change. It is a benchmark, not a hard case.

At balanced — one-second segments, 0.7-second minimum chord, 0.2 confidence — the observable output is C, Am, F, G: four chords, reported as a ZIP holding chords.csv, chords.json, timeline.svg and README.md. At detailed — half-second segments, 0.5-second minimum — the same ordered progression comes back with finer transition boundaries and a reported resolution field of 0.5 seconds.

Hold those two results side by side. The sequence is stable. The boundaries are not. The chord names are the durable part of the output; the timestamps are the arguable part, and any downstream system that keys off bar positions inherits that ambiguity. The observed shift in boundary times between the two runs is the whole resolution argument in one comparison.

If you want to hear the difference before running your own file, the [FLAC sample pages](https://elysiatools.com/en/samples/flac-samples) and [MP3 samples](https://elysiatools.com/en/samples/mp3-samples) carry comparable fixtures.

## Where This Method Breaks

I ran the failure modes against the implementation and three of them are structural, not fixable by tuning.

The first is harmonic confusion under distortion. Heavy overdrive adds harmonics that land on other pitch classes, so the profile stops resembling a triad and the fit floor starts rejecting real chords. The second is sustain. A piano with the pedal down holds the previous chord's tones into the next segment, so the pooled chroma of segment two contains segment one, and the island-filling pass then protects the wrong label. The third is the absence of musical structure in the output: there is no tempo, no downbeat, no bar count and no key. The SVG timeline is drawn in seconds, because seconds are all the analysis knows.

In each case the measured profile is a fair description of the audio and a poor description of the music. That gap is documented, not accidental. MIR research treats chroma-based chord estimation as a baseline for exactly this reason: it shows what plain pitch-class energy can do before any model is added.

The bounded input matters too. Files cap at 100 MB and 180 seconds, the downmix is mono, and the analysis band stops at 2,500 Hz on an 11,025 Hz sampler. That is a deliberate trade for pitch-class energy: it costs you nothing on a string quartet and a great deal on a cymbal-heavy mix. The tool's own documentation is blunt about the scope — "an approximate MIR guide for listening and annotation, not score-level ground truth" — and that sentence should travel with each chart you export.

## What to Do With a Chart You Do Not Trust

Treat the first chart as a hypothesis, not a deliverable. The workflow that survives contact with real audio is short.

Run detailed resolution with the minimum chord duration at 0.5 seconds and confidence at 0.2, so you see the maximum number of borders the analysis is willing to draw. Then look at the segments shorter than a second and ask what the harmony is doing there — those segments are where the grid and the song disagree, and they are the only place a second pass can help. Re-run at higher confidence to prove which chords are load-bearing: the ones that survive a 0.4 threshold are the ones you can safely chart. Accept C/E as C by design, and read N as "the audio did not support a name", not as an error.

Then check the result against a metronome, not against your memory of the song. A chart that agrees with the recording to within one grid step, at a grid you chose deliberately, is a result you can defend. Two runs at different resolutions will show you the stable sequence and the unstable borders in one comparison. You can run the whole loop in the browser at [Elysia Tools](https://elysiatools.com/en/tools/audio-chord-progression-detector), and the wider set of [media tools](https://elysiatools.com/en/categories/media) covers the rest of the audio pipeline — or browse the full catalog at [elysiatools.com](https://elysiatools.com/en/tools).

For a while I read chord detection as a naming problem. Widen the vocabulary, tune the templates, and the chart falls out. It is not a naming problem. Nearly all detectors agree about C, Am, F and G, and almost none of them agrees about the half-second where those chords touch.

So the next time a chart and your ears part ways, do not widen the vocabulary. Move the border. Ask what the harmony is doing in the 500 milliseconds the grid hid, and then answer honestly: is that passing chord the song, or is it your tool's frame rate? That is a music question, and no sample rate can answer it for you.
