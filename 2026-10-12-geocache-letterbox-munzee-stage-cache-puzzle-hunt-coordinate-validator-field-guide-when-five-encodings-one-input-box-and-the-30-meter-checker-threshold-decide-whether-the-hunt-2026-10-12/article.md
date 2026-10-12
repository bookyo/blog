<strong>A field-stamped geocache is not a problem you can solve with a single math call.</strong> The puzzle-hunt hobby hides five different encodings behind one hobby: a six-character GC-code that decodes to a numeric ID, a 1-to-5 D/T grid that lives on a separate 81-cell scale from the rating, a multi-stage projection that walks WGS84 waypoints through bearing and distance offsets, a 31-character alphabet that resists parsing with standard regex, and a "checker" coordinate that the puzzle author plants in plain text and trusts you to compare against. The Geocache Letterbox Munzee Stage-Cache Puzzle-Hunt Coordinate Validator at [Elysia Tools](https://elysiatools.com/en/tools/geocache-letterbox-munzee-stage-cache-puzzle-hunt-coordinate-validator) puts all five on a single page and tells you which type your cache is before it tells you whether your answer is right.

## What the GC-Code Encoding Is Really Doing

The GC-code on a geocaching.com cache page looks like a four-or-five character hex string — `GC1ABC`, `GC12345`, `GC4F7Z` — but the older format is hexadecimal and the post-2005 format is a custom base-31 encoding with a quirky +411120 offset. A naive `parseInt(code, 16)` returns 127 for `GC1ABC2` on the modern era and a number that wraps to negative for `GCABC` on the legacy era. The validator takes a single string, detects which era it belongs to, normalizes the prefix, and emits the numeric ID along with the cache type label. If the encoding falls outside the expected range the tool flags the input as malformed and prints the expected character set rather than failing silently.

This matters more than it sounds. A puzzle cache whose GC-code has been transcribed wrong on a forum post will return a "valid" hex number that points at a different cache — the solver checks the wrong coordinates, the cache-owner emails you about your mistake, and a 30-minute hunt turns into a half-day. The validator's encoding check is the cheap pre-flight that costs two seconds and saves the rest.

## The D/T Grid Is Two Numbers, Not One

Geocachers rate caches with two numbers: Difficulty (1 to 5) and Terrain (1 to 5), printed as `D3.5/T4`. The Fizzy grid the community uses to visualize them is an 81-cell (9×9) matrix, but the rating you see on a cache page is half-step — 1.0, 1.5, 2.0, 2.5, 3.0 — which means half the cells in the grid are unreachable from the published rating scheme. The validator plots the cache's D/T on a 9×9 grid that respects the half-step boundary and color-codes the cell to make the actual cognitive load of the hunt obvious at a glance.

What the D/T really tells a solver is whether the cache needs climbing gear, a long walk, a kayak, or just street shoes. A `D2/T5` is a trivial puzzle with a hard physical approach — common for letterbox hybrids in remote parks — and a `D5/T1` is a brutally hard puzzle solved from a parking lot. The validator's grid view makes that asymmetry impossible to miss.

## Multi-Stage Projections: Bearings, Distances, and WGS84

Puzzle caches and multi-caches walk the solver through a chain of "stage" coordinates. Stage 1's waypoint is the published coordinate, stage 2 is a bearing-and-distance offset from stage 1 (`bearing 47° for 0.6 miles`), stage 3 is another offset from stage 2, and the final is where the cache sits. A naive solver projects the first offset on a flat plane, gets a coordinate 200 meters off, and concludes the puzzle is wrong.

The projection math is haversine on a sphere (WGS84), not a flat-plane transform. The validator walks each stage, applies the bearing and distance on the spherical surface, emits the decimal-degree coordinate and the `N 47° 36.600' W 122° 19.450'` DMS format side by side, and labels each as stage N. When the final waypoint differs from the checker coordinate by more than 30 meters the validator flags the cache as a puzzle — that's the radius at which GPS noise still leaves a real answer, and below which the solver is searching inside a parking-lot radius.

## The 31-Character Base-31 Alphabet

The base-31 encoding behind modern GC-codes skips digits that look like letters (0/O, 1/I/L) and uses exactly 31 characters. That makes the encoding regex `^[0-9A-HJ-NP-Z]+$` — not the obvious `^[0-9A-Z]+$` your first try will write. The validator enforces this alphabet on the parsed value and refuses to interpret an input that contains I, O, or 0 in the wrong position, which is the most common transcription error on old forum posts that lost the original formatting.

A pre-65536 cache uses the legacy hexadecimal era and decodes as `parseInt(code, 16)`; a post-65536 cache uses base-31 with the +411120 offset that maps the encoded value back into the cache ID space. The validator handles both with one parser and a single `era` flag in the output, so the solver does not have to know which era the cache was published in.

## Checker Coordinates and Puzzle-Cache Reality

Puzzle-cache authors usually embed the answer in the puzzle — a hidden coordinate that the solver has to extract from a series of clues, a coded message, or a physical artifact. The author almost always publishes a "checker" coordinate on the cache page that lets the solver confirm their derived answer before going outside. The validator's checker input takes the solver's derived coordinate, takes the published checker, and emits a distance-and-bearing result. Under 30 meters: the solver's math is right. Over 30 meters: something is off and the validator prints a sanity-check warning rather than a clean pass.

The 30-meter threshold is the real-world GPS noise floor. A handheld GPS in tree cover is good to about 10 meters, a phone GPS is good to about 5 meters in open sky, and a cache hidden in a cliff face is good to about 30. The validator's threshold matches the noise floor so a clean pass really means clean.

## Letterbox Hybrids and Munzees Need Different Defaults

Letterbox hybrids use a rubber-stamp and a logbook instead of a trackable, and the cache page is usually missing the typical geocaching fields. Munzees use a QR code on a virtual or physical location and the validation rules are different. The validator detects the cache type from the GC-code prefix and the input shape, then applies the type-specific tolerance and grid placement. A munzee virtual at a city fountain with no physical container is not "found" the way a letterbox is, and the validator's output reflects that.

This is the part the geocaching forums skip. The community assumes every cache is a geocache, and the tools that grew up around that assumption treat letterbox and munzee caches as a special case. The validator's type detection is a single check, but it changes which fields the output cares about.

## The Five-Check Output Format

A clean validator run prints five labeled fields in order: parsed cache type (geocache / letterbox hybrid / munzee / multi-cache / mystery cache), GC-code era flag (legacy hex or modern base-31), the D/T grid cell with the half-step enforced, the multi-stage chain as `stage 1 → stage 2 → ... → final` with the bearing and distance between each pair, and the checker-coordinate distance with the green-or-red 30-meter threshold. The five fields are the minimum a solver needs to trust the output; anything less and the tool is forcing a manual cross-check downstream.

## Why a Single Validator Page Beats a Stack of Scripts

A solver who is debugging a puzzle cache typically runs a regex over the GC-code, then a base-conversion, then a haversine, then a D/T-grid plot, then a checker compare, and then debugs whichever step the chain broke in. The validator runs all five in one input box and prints the disambiguated output, which means a solver can paste a forum-posted code, see whether the transcription is the bug or the puzzle is the bug, and skip the half-hour of setup. The tool is free, runs in the browser, and saves the alternative — opening five tabs and re-entering the same input in each.

For puzzle-hunt organizers, the same tool validates the chain before publication: a multi-stage cache with a broken projection never reaches the page because the validator caught it during authoring. The checker-coordinate distance is the last field in the output and the first field a serious organizer checks.

Run the validator at [Elysia Tools](https://elysiatools.com/en/tools/geocache-letterbox-munzee-stage-cache-puzzle-hunt-coordinate-validator) when the next puzzle-cache page arrives in your feed. The tool is the difference between a half-day of frustration and a clean pass at the published coordinates.

Explore more puzzle-solving and projection tools at [elysiatools.com/en/tools](https://elysiatools.com/en/tools).
