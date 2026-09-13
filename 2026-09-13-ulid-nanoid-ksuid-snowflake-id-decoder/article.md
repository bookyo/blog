# ULID / NanoID / KSUID / Snowflake ID Decoder — Field Guide: When Five ID Families, Three Bit-Field Layouts, and One Birthday Paradox Decide Whether Your Sortable Identifier Is a Timestamp or a Mystery

## Why Your Database Has Five Different "UUID-Like" Columns

Pick a modern backend codebase and grep its schema migration history. You will find `id UUID`, `id BIGINT`, `id CHAR(26)`, `id CHAR(12)`, `id CHAR(21)` — five column shapes living next to each other, all of them supposedly "the primary key." Each one was added by a different engineer at a different time, and each one made a different trade-off between sortability, randomness, footprint, and inspectability. When a row from one of those tables shows up in a Slack thread at 3 a.m. as `01ARZ3NDEKTSV4RRFFQ69G5FAV`, nobody on the team can tell whether that is a UUID, a Snowflake, a ULID, or a typo of the customer name.

The five ID families that show up over and over — **ULID, KSUID, NanoID, MongoDB ObjectId, and Discord / Twitter / Sonyflake Snowflakes** — solve the same problem (uniquely identify a row, ideally without coordination) with five different answers. They share enough structure that a single decoder tool can crack all five, but the bit layouts are different enough that copy-pasting from one family into another produces silently-wrong timestamps. This guide walks through what each format actually stores, how to read it, and where the decoder at [Elysia Tools](https://elysiatools.com/en/tools/ulid-nanoid-ksuid-snowflake-id-decoder) saves the hour you would otherwise spend parsing Crockford Base32 by hand.

## ULID: 48-Bit Millisecond Timestamp + 80 Random Bits, Encoded as 26 Crockford Base32 Chars

The **ULID** (Universally Unique Lexicographically Sortable Identifier) spec, published in 2016, is the cleanest expression of "I want a UUID I can sort by time." A ULID is 128 bits, laid out as:

| Bits | Field         | Source                                                  |
| ---- | ------------- | ------------------------------------------------------- |
| 0–47 | `time_ms`     | Unix milliseconds, big-endian                           |
| 48–79 | `random_1`   | 32 bits from CSPRNG                                     |
| 80–127 | `random_2` | 48 bits from CSPRNG                                     |

Encoded with Crockford Base32 (no `I`, `L`, `O`, `U` — the alphabet that excludes look-alikes), the 128 bits become a 26-character string. The first 10 characters are the timestamp; the remaining 16 are randomness. Because the timestamp is the most-significant half, sorting 10,000 ULIDs lexicographically is equivalent to sorting them by creation time.

The decoder pulls the timestamp half out with a 5-byte slice, converts to ISO-8601 with millisecond precision, and computes the **birthday-bound collision probability** at the requested entropy level. For a single-process CSPRNG emitting ULIDs at 1000/sec, the birthday bound is reached at roughly 2<sup>32</sup> items — 4.29 billion — which is why the spec recommends the 80-bit random half: it is generous enough that any realistic single-table workload will not collide within the lifetime of the universe.

Example input that the decoder handles:

```
01ARZ3NDEKTSV4RRFFQ69G5FAV
```

The first ten characters decode to `2080-04-20T07:53:20.768Z`, and the random half is the value the spec reserves for per-row uniqueness.

## KSUID: 32-Bit Second Timestamp + 128-Bit Payload, Base62

**KSUID** (K-Sortable Unique Identifier) is Segment's 2014 answer to the same problem, with two deliberate differences. The timestamp is **seconds**, not milliseconds, so a KSUID fits in a smaller window before the high bits repeat. The payload is **128 bits** of randomness, all of it allocated to uniqueness rather than split across a counter. The encoding is Base62 (alphanumeric, case-sensitive), which packs more entropy per character than Crockford Base32 at the cost of being URL-hostile on systems that lowercase path segments.

KSUID layout:

| Bits  | Field        | Notes                                                  |
| ----- | ------------ | ------------------------------------------------------ |
| 0–31  | `time_sec`   | Seconds since 2014-05-13 (custom epoch)               |
| 32–159 | `payload`    | 128 bits from CSPRNG                                  |

Total length is 27 characters in Base62. The custom epoch means timestamps stay compact: a KSUID generated in 2030 still fits in 10 characters of base-62 timestamp representation, leaving 17 for randomness. Sort order matches creation order to within one second.

Example:

```
1dH6TkQqgG8Y4gH7gX8wJ6qRYZM
```

Decodes to `2026-09-12T14:37:57Z` plus the payload. The decoder shows both ISO timestamp and raw hex.

## NanoID: 21 URL-Safe Characters From a Custom Alphabet

**NanoID** is a 2019 minimalist alternative. Instead of cramming a timestamp into the ID, NanoID gives you pure randomness at whatever length you choose. The default is 21 characters from an alphabet of 64 URL-safe characters (`A–Z`, `a–z`, `0–9`, `_`, `-`), which yields **126 bits of entropy** — collision-resistant for any practical workload. The trade-off: NanoIDs are not sortable by creation time. They are also not timestamp-bearing at all; if you need to know when a row was created from its ID alone, you need a separate column.

NanoID layout (variable):

| Chars  | Bits (default 64-alphabet) | Notes                                          |
| ------ | -------------------------- | ---------------------------------------------- |
| 21     | 126                        | Default; collision-safe for billions of rows |

The decoder treats NanoID as alphabet + entropy: it checks that every character is in the 64-symbol alphabet, counts the entropy in bits, and computes the birthday bound. For 21 chars from a 64-alphabet that is 2<sup>42.5</sup> items at 50% collision probability — a number so large that real-world workloads never approach it.

If you need both timestamp and NanoID-style brevity, the answer is usually ULID or KSUID, not a longer NanoID.

## MongoDB ObjectId: 4-Byte Seconds + 5-Byte Random + 3-Byte Counter

The **ObjectId** predates ULID by seven years (introduced in MongoDB 1.0, 2009), and it is the grandfather of every "sortable-by-time ID in 24 hex characters" pattern. ObjectId is 96 bits laid out as:

| Bits  | Field       | Source                                       |
| ----- | ----------- | -------------------------------------------- |
| 0–31  | `time_sec`  | Unix seconds, big-endian                     |
| 32–71  | `random_5`  | 5 bytes per-process random                   |
| 72–95  | `counter`   | 3-byte auto-increment, big-endian           |

The 3-byte counter is the load-bearing detail. MongoDB guarantees that two ObjectIds generated inside the same process during the same second will differ by at least 1 in the counter field, even if the random half collides. That is what lets MongoDB issue a million inserts per second per shard without collision. The decoder breaks the 24-char hex string into the three fields, prints the timestamp, and surfaces both the per-process random and the counter — useful when debugging duplicate-key errors that look impossible until you realize two writer processes had been seeded with the same `random_5`.

Example:

```
507f1f77bcf86cd799439011
```

Decodes to `2012-10-17T20:46:31Z`, per-process random `f1f77bcf86`, counter `799439011` — note the counter starts at a non-zero value because each driver process seeds itself differently.

## Discord / Twitter / Sonyflake Snowflakes: Bit-Field Layouts by Use Case

The **Snowflake** family is a class of ID schemes popularized by Twitter (2010) and copied by Discord, Sonyflake, Instagram, and the Mastodon / Pleroma forks. The unifying idea: a 64-bit integer split into timestamp + worker + sequence, packed tightly enough that you can fit a year of millisecond-resolution IDs into 41 bits and still leave room for thousands of workers.

Twitter Snowflake layout:

| Bits  | Field       | Source                                       |
| ----- | ----------- | -------------------------------------------- |
| 63    | sign        | Always 0 (reserved)                          |
| 22–62 | `time_ms`   | Custom epoch, 41 bits                        |
| 12–21 | `worker_id` | 10 bits — datacenter + worker                |
| 0–11  | `sequence`  | 12 bits — per-process counter                |

The decoder flags whether the high bit is set (which would make the value negative as a signed int — a common bug when comparing Snowflakes to signed-BIGINT columns). Discord uses the same layout but with a different epoch (2015-01-01) and a 42-bit timestamp field, which the decoder detects via the auto-detect path.

Sonyflake (Sony's Go implementation) flips the layout: 39-bit timestamp, 8-bit sequence, 16-bit machine ID, packed into 63 bits. The decoder checks for Sonyflake's distinct sequence bit-position when auto-detect fails.

## Why the Birthday Bound Matters More Than the Format

Every one of these formats uses randomness to break ties. The **birthday paradox** says the probability of a collision in `n` items from `k` bits of entropy is roughly `n² / 2k`. The decoder prints this number next to each decoded row so you can answer "is my entropy enough?" without doing the math by hand.

For ULID at 80 bits of randomness, the birthday bound is 2<sup>40</sup> items (~1 trillion). For KSUID at 128 bits, 2<sup>64</sup> items. For MongoDB ObjectId at 40 bits of randomness + counter, the bound depends on the counter's overflow rate — a runaway counter can produce duplicates faster than randomness would predict, which is exactly the failure mode the decoder surfaces when the counter field is non-monotonic across two consecutive IDs in the same second.

## Closing (read this first)

Pick one ID family and stick with it for a single table. The decoder at [Elysia Tools](https://elysiatools.com/en/tools/ulid-nanoid-ksuid-snowflake-id-decoder) handles all five formats with auto-detect, so you can paste an unknown ID from a log file and see its timestamp, entropy, and birthday bound without deciding the format in advance. If you are designing a new schema today, ULID is the safest default: timestamp-bearing, sortable, collision-safe for trillions of rows, 26 characters long, and URL-safe. KSUID if you want the same idea with a smaller timestamp window. NanoID if you do not need timestamp ordering and want the smallest possible ID. ObjectId only if you are inside MongoDB. Snowflakes only if you have thousands of writer processes and need 64-bit integers in your primary key.

For more tooling that turns opaque identifiers into inspectable structure, browse the rest of the catalog at [elysiatools.com/en/tools](https://elysiatools.com/en/tools).
