# The Hidden Standard That Decides How Loud Everything You Hear Actually Sounds

When you raise the volume on a podcast and it sounds fine, then flip to a Netflix trailer and it blasts you off the couch — even though both are at what your phone calls "100%" — something strange is happening. Your ears are not broken. Your speaker is not defective. You are experiencing the invisible war over loudness that has been fought in audio engineering for a century.

The weapon is called **LUFS**.

## What LUFS Actually Measures

LUFS stands for **Loudness Units relative to Full Scale**. It is not a volume knob. It is not decibels. It is a *perceptual* measurement — a way of quantifying how loud something *sounds* to a human ear, accounting for the fact that our hearing is not equally sensitive to all frequencies.

The human ear is most sensitive to frequencies between 2kHz and 5kHz — roughly the range of a baby's cry or a whistle. It is less sensitive to very low frequencies (a 50Hz bass note can be 15dB louder than a 1kHz tone and sound equally loud). LUFS incorporates this frequency weighting, which is why two audio files with identical dB readings can feel dramatically different in perceived loudness.

This is why LUFS matters: it measures what you *hear*, not just what the physics say is happening.

## The Loudness Wars: A Brief and Damaging History

For most of the 20th century, the audio industry competed on a simple metric: who could make their recordings the loudest? Louder sounded better — or at least, louder was perceived as more exciting, more impactful, more *professional*. Record labels demanded increasingly hot masters. Radios boosted their signals to compete. By the 1990s, albums were being compressed and limited to the point where the dynamic range — the difference between the quietest and loudest moments — had essentially collapsed.

The result was called the **loudness wars**, and the damage was real. Music that was slammed to -3 dBFS on a peak meter might actually sound *quieter* perceptually than a classical recording sitting at -20 dBFS, because the classical piece had enormous dynamic range and the pop track had zero quiet moments to contrast against.

The consumer suffered most. Turning up the quiet classical piece to match the loud pop track meant the crescendos became painful. Playing the pop track at a comfortable level meant the verses were nearly inaudible.

## The Standard That Finally Fixed It

The solution came from broadcast engineers who needed a way to ensure that a TV commercial didn't blast viewers into seizures when it followed a quiet drama. The **EBU R128** standard, developed by the European Broadcasting Union and now adopted worldwide, established LUFS as the universal language of audio loudness.

The key insight was simple: instead of measuring peak levels (which tell you almost nothing about perceived loudness), measure *integrated loudness* — the average loudness of an entire program, weighted by human perception, measured in LUFS.

Here are the target loudness standards that govern everything you watch and listen to:

| Platform / Standard | Target Integrated LUFS | Loudness Range (LRA) |
|---------------------|----------------------|---------------------|
| Spotify | -14 LUFS | — |
| YouTube | -14 LUFS | — |
| Netflix | -27 LUFS | 20 LU |
| Apple Music | -16 LUFS | — |
| Podcasts (Apple) | -16 LUFS | — |
| European TV (EBU R128) | -23 LUFS | 18 LU |
| US TV (ATSC A/85) | -24 LUFS | 20 LU |

Notice that Spotify and YouTube target -14 LUFS, while Netflix sits at -27. A Netflix production and a Spotify track are calibrated to sound dramatically different in absolute loudness — but perceptually *consistent* within their own ecosystem. When you switch from a Spotify track to a Netflix film, the platform handles the gain staging automatically so the perceived loudness feels similar.

This is why your phone's volume percentage is a lie. It is applying a simple gain multiplier, not a LUFS-normalized adjustment. A -14 LUFS Spotify track at "50% volume" is not perceptually equivalent to a -24 LUFS film at "50% volume."

## The Three Numbers That Tell You Everything

When you run the **Audio LUFS Meter** on an audio file, it returns three key measurements that together give you a complete picture of the loudness landscape:

**Integrated Loudness** is the big-picture average — the loudness of the entire file averaged over its full duration, weighted for human perception. Think of it as the overall "felt loudness" someone would experience if they listened to the whole thing. If your podcast sits at -16 LUFS integrated, that is its loudness identity.

**Short-Term Loudness** measures loudness over a rolling 3-second window. It tells you what the loudness is *right now*. If the integrated is -16 but the short-term is spiking to -8, you have a hot section that is pushing the overall average up. In mixing, you watch short-term to avoid momentary overloads.

**Momentary Loudness** is the loudest snapshot over a 400-millisecond window — the loudest fraction of a second. In practice, this tracks the transient peaks: a drum hit, a cymbal crash, a scream. Broadcast standards often set true-peak limits based on momentary readings.

The fourth number, **Loudness Range (LRA)**, tells you about dynamics — the difference between the quietest and loudest sections. A film score with lots of quiet passages and sudden fortissimos will have a high LRA. A heavily compressed pop song will have a low LRA. For music, LRA is a creative choice. For broadcast, it is a compliance requirement.

## Why This Matters for Podcasters, Streamers, and Content Creators

If you upload a podcast episode without measuring LUFS, you are flying blind. Listeners may find your episode too quiet compared to other shows, or if you have errant loud sections, they may clip and distort on platforms that normalize to a target LUFS.

Spotify, Apple Music, and YouTube all apply their own loudness normalization at playback. If your track is mastered to -10 LUFS (louder than the -14 target), Spotify will turn it *down* at playback. If it is mastered to -20 LUFS, Spotify will turn it *up*. Your hard work and loudness decisions are being undone at the listener's end — which is why hitting the right target upstream matters.

For podcasters specifically, Apple's Podcast Hosting platform recommends -16 LUFS with a true-peak maximum of -1 dBTP. Going louder does not make your show stand out — it makes it sound amateur, because platforms will normalize it anyway and the listeners who have normalization enabled will hear it at the target level regardless of how hot you baked it.

## How the LUFS Meter Works Under the Hood

The **Audio LUFS Meter** at ElysiaTools runs **FFmpeg's ebur128 filter** — the industry-standard implementation of ITU-R BS.1770 and EBU R128. When you drop an audio file into the tool, FFmpeg processes it through the ebur128 filter, which performs a frequency-weighted loudness analysis aligned with human hearing models.

The tool parses the verbose FFmpeg output to extract:
- The integrated loudness (I value in LUFS)
- The loudness range (LRA in LU)
- The maximum short-term loudness over any 3-second window
- The maximum momentary loudness over any 400ms window

These four numbers give a mastering engineer everything they need to diagnose a mix and give a content creator everything they need to verify platform compliance.

## The Quiet Revolution

The loudness wars are over. The industry settled on LUFS not because artists stopped wanting their music to sound powerful, but because engineers realized that *perceived* power comes from dynamics, not from loudness maximization. A well-mastered track at -14 LUFS with 12 LU of loudness range will sound more impactful and alive than a brick-walled track at -8 LUFS with 2 LU of range.

LUFS normalized the battlefield. Now the competition is not about who can be loudest — it is about who can make the most of the loudness budget they are given.

That is a far more interesting problem. And it all starts with knowing the numbers.

**Try the [Audio LUFS Meter](https://elysiatools.com/en/tools/audio-lufs-meter) to analyze your audio files against broadcast standards — and see exactly what your ears have been guessing at for years.**
