title: "Snowflake / Discord ID Bit Decoder Field Guide: When Six Platforms Share One 64-Bit Layout but Five Different Epochs Decide Whether the Timestamp Points Anywhere Useful"

<strong>When a Snowflake-style ID like `109580041603153152` lands on your screen, the question is not which platform minted it — the question is which 42-bit timestamp block, which 5-bit worker slot, and which 12-bit increment within that slot you are reading, because the wrong epoch turns a perfectly good number into a date in the year 48,817.</strong>

Discord IDs, Twitter Snowflakes, Mastodon IDs, Sonyflake, Instagram, and a hundred internal custom schemes all hang their 64-bit identity on a single `BigInt`. The numbers look identical on screen — sixteen decimal digits, no dashes, no separators — and the wrong epoch silently maps a Discord message from `2017-04-13` into the Stone Age or the Heat Death. Each platform chose its own starting instant, and the difference between Discord's `2015-01-01T00:00:00Z` epoch and Sonyflake's `2014-11-04T01:42:54.657Z` is the difference between a timestamp that lands where you expect and one that does not.

This field guide walks through what the [Snowflake / Discord ID Bit Decoder](https://elysiatools.com/en/tools/snowflake-discord-id-bit-decoder) actually decodes when you paste a 64-bit ID, how the six default platforms reconcile at the bitfield level, where the custom-profile path lets you describe a layout the defaults cannot, and how the shard calculation turns a worker slot into a `bucket = ID >> 22 % shardCount` lookup. The goal is not to enumerate every Snowflake variant ever shipped — it is to make the five decisions that any 64-bit ID decoder has to make explicit enough that you can debug the wrong-output case without trial-and-error.

## A Snowflake is just a 64-bit integer split into three fields — and the split is platform-specific

Every Snowflake-style ID fits the same template: a most-significant timestamp block, a middle worker/process/machine block, and a least-significant sequence/increment block. The template is the same; the bit allocation is not. Discord uses `(42-bit ms timestamp) | (5-bit worker) | (5-bit process) | (12-bit increment)`. Twitter Snowflake uses `(41-bit ms timestamp) | (10-bit machine) | (12-bit sequence)`. Sonyflake reverses the order and uses `(39-bit 10ms units since local epoch) | (8-bit machine) | (16-bit counter)`. Instagram uses `(41-bit second-resolution timestamp since 2011) | (13-bit shard) | (10-bit sequence)`. Mastodon holds Snowflake layout `(48-bit ms timestamp | 16-bit random)` for its internal IDs, but the public posts use `OStatus` Snowflake with the same 42-bit / 5 / 5 / 12 layout as Discord.

The [Snowflake / Discord ID Bit Decoder](https://elysiatools.com/en/tools/snowflake-discord-id-bit-decoder) accepts all six preset platforms and parses the same 64-bit number against each preset's bit layout. The same `109580041603153152` decodes as `2017-04-13T11:42:28.064Z` under the Discord preset, as the same instant under the Twitter preset (the two presets share the `2010-11-04T01:42:54.657Z` epoch... actually they do not, see below), or as something wildly outside the expected range under the Sonyflake preset, depending on which bit layout and epoch the decoder picks. The output is three numbers plus an inferred shard — and each one comes from a different slice of the same 64 bits.

## Epoch is where the five default platforms diverge, and where most decoder bugs hide

The bit layout determines *which* bits represent the timestamp; the epoch determines what those bits *mean*. The six default platforms picked six different starting instants:

- **Discord** uses the Twitter epoch `2015-01-01T00:00:00Z` for the official public IDs (modern Discord migrated to a custom epoch in 2024 for some internal IDs, but legacy public IDs all use the Twitter instant).
- **Twitter Snowflake** uses `2010-11-04T01:42:54.657Z` (the Twitter founding second, modulo a millisecond to keep ms representation friendly).
- **Mastodon** uses Twitter's epoch as well for OStatus IDs, but some Mastodon forks shipped with `2014-02-24T17:30:00Z` or other locally chosen instants.
- **Sonyflake** uses `2014-11-04T01:42:54.657Z` — close to Twitter's epoch but not identical, and crucially uses 10-millisecond granularity instead of 1-millisecond, so a Sonyflake timestamp's unit conversion differs.
- **Instagram** uses `2011-01-01T00:00:00Z` with **second-resolution** timestamps, so its 41-bit block holds seconds since 2011 rather than milliseconds since 2010.
- **Custom** lets you supply your own epoch and unit, because every internal Snowflake scheme at every company uses a different starting instant — the default six are conveniences, not a complete list.

For an ID like `109580041603153152`, the timestamp block is bits `(63..22)` at 42 bits wide. Under Discord's preset the math is `(109580041603153152 >> 22) + discord_epoch_ms = 1492081348064 ms since Unix epoch` which is `2017-04-13T11:42:28.064Z`. Under Twitter's preset the same 42-bit block yields the same ms timestamp, but the epoch is different — `+ twitter_epoch_ms`, where `twitter_epoch_ms = 1288834974657`. Wait — that comparison only works once you notice that Discord's public epoch and Twitter's Snowflake epoch are *different* even though both are sometimes called "the Twitter epoch". There are at least three different "Twitter epoch" timestamps in the wild: `2010-11-04T01:42:54.657Z` (the canonical Snowflake epoch), `2015-01-01T00:00:00Z` (the Discord public ID epoch), and `2010-11-04T01:42:54.657Z` referenced by some libraries as their anchor.

The decoder picks one canonical epoch per platform. If your real-world ID came from a fork that picked a non-default epoch — and almost every internal Snowflake has done this — the timestamp will be off by exactly that fork's epoch delta. The custom-epoch input is the escape hatch.

## Bit-layout mapping: where the shift and mask constants come from for each platform

Once the epoch is settled, the next question is which bits carry the timestamp, which carry the worker, and which carry the sequence. The shift-and-mask constants that any runtime Snowflake library computes once at startup are:

- **Discord** — `(42, 5, 5, 12)` bits in order `(timestamp, worker, process, increment)`, with the timestamp at `(63..22)`, worker at `(21..17)`, process at `(16..12)`, increment at `(11..0)`. The shifts are `(>>22, >>17, >>12, & 0xFFF)`.
- **Twitter Snowflake** — `(41, 10, 12)` bits in order `(timestamp, machine, sequence)`, with the timestamp at `(63..22)`, machine at `(21..12)`, sequence at `(11..0)`. The shifts are `(>>22, >>12, & 0xFFF)`.
- **Sonyflake** — `(39-bit 10ms-units timestamp, 8-bit machine, 16-bit counter)` in `(63..24, 23..16, 15..0)`. The shifts are `(>>24, >>16, & 0xFFFF)` and the unit-multiplier is `10ms` not `1ms`.
- **Instagram** — `(41-bit second-resolution timestamp, 13-bit shard, 10-bit sequence)` in `(63..22, 21..10, 9..0)`. The shifts are `(>>22, >>10, & 0x3FF)` and the unit-multiplier is `s` not `ms`.
- **Mastodon (Snowflake family)** — `(48-bit ms timestamp, 16-bit random)` in `(63..16, 15..0)`. The shifts are `(>>16, & 0xFFFF)` for the random half.
- **Custom** — whatever bit widths you specify, in the order you list them in the custom-fields JSON (least-significant-field-first).

The mask constant for each field is `(1 << field_bits) - 1`, and the shift constant is the sum of all field widths below that field. A decoder that hardcodes Discord's `(>>22, >>17, >>12, & 0xFFF)` will silently produce a wrong worker and a wrong sequence on Twitter, Instagram, or Sonyflake. The shift triples `(timestamp_shift, worker_shift, sequence_shift)` vary by exactly the field-width sum below each field, which is why the same 64-bit integer parsed against five different layouts yields five different decoded triples.

## Worker slots and the shard calculation are usually `>> (seq_bits) & worker_mask`, but the ordering matters

Once the timestamp is extracted, the next 10-or-so bits encode the worker, process, machine, or shard, and the last 12-or-so bits encode the sequence within the worker's tick. The decode for Discord is:

```
worker_id  = (snowflake >> 17) & 0x1F   # 5 bits, bits 17-21
process_id = (snowflake >> 12) & 0x1F   # 5 bits, bits 12-16
increment  = snowflake & 0xFFF         # 12 bits, bits 0-11
```

For Twitter:

```
machine_id = (snowflake >> 12) & 0x3FF  # 10 bits, bits 12-21
sequence   = snowflake & 0xFFF          # 12 bits, bits 0-11
```

For Instagram:

```
shard_id   = (snowflake >> 10) & 0x1FFF  # 13 bits, bits 10-22
sequence   = snowflake & 0x3FF          # 10 bits, bits 0-9
```

The shifts move because the bit layout moves. A decoder that hardcodes Discord's `(>>22, >>17, >>12, & 0xFFF)` will silently produce a wrong worker and a wrong sequence on Twitter, Instagram, or Sonyflake. The [Snowflake / Discord ID Bit Decoder](https://elysiatools.com/en/tools/snowflake-discord-id-bit-decoder) reuses one Rust/SQL/JS-style bitfield parser across all six presets — it reads the platform's per-field bit widths at the top of the parse, then issues a uniform `(field_offset, field_width, field_mask)` triple per field.

The shard calculation is a separate, optional step that only runs when you supply a `shardCount`. Discord's official shard routing uses `bucket = (snowflake >> 22) % shardCount` — bucket the ID, not the decoded timestamp, and route by bitwise reduction rather than by date. The decoder reports `bucket = (snowflake >> 22) % shardCount` alongside the worker/process/increment so you can see which shard "owns" the ID at the moment of inquiry. This is the calculation the gateway uses to decide which shard-process receives the next message event, and it is independent of the timestamp block — the shard routing only cares about the upper bits of the 64-bit integer.

## Three worked examples across Discord, Twitter, and Sonyflake on the same 18-digit number — and how the verification step catches the wrong-platform case

Take `109580041603153152`. Under Discord:

```
(ms_timestamp, worker, process, increment) =
  (1492081348064, 26, 0, 384)
(2017-04-13T11:42:28.064Z, worker_id=26, process_id=0, sequence=384)
```

Under Twitter (same bit layout, wrong epoch):

```
ms_timestamp = 1492081348064 - (twitter_epoch - discord_epoch) ms
            = 1492081348064 - (discord_epoch has ts 1422748800000 ms, twitter has 1288834974657 ms)
            ⇒ wrong by exactly the epoch delta
```

Under Sonyflake (different layout — 39-bit timestamp at 10ms units plus 16-bit counter):

```
(sf_10ms_units, machine_id, counter) =
  (sf_bits >> 24, (sf_bits >> 16) & 0xFF, sf_bits & 0xFFFF)
date = sonyflake_epoch + (sf_10ms_units * 10)ms
```

The same 18-digit decimal number, parsed against three different bit layouts and three different epochs, produces three different decoded dates — and only one of them is the right answer for any given system. The decoder does not warn when the platform and the bit layout disagree; the output is whatever the chosen preset says it is.

## Verifying the decoded date against an external timestamp source is the only way to catch a misclassified platform

The verification step is to take the inferred date and check it against an external timestamp source — the message timestamp in Discord's `MESSAGE_CREATE` gateway event, the tweet creation time in Twitter's Snowflake response payload, the post creation time in Mastodon's `status.created_at`. If the inferred date and the external timestamp disagree by more than one resolution tick (1ms for Discord/Twitter/Mastodon, 10ms for Sonyflake, 1s for Instagram), the platform classification is wrong — the ID was minted by a platform whose bit layout and epoch the preset you chose does not match. The fix is either to switch to a different preset or to set up a custom profile that matches the real-world system.

The most common mismatches in practice: a Discord ID parsed under the Mastodon preset (which uses Twitter's epoch) will report the timestamp as roughly 4-5 years too late; an Instagram ID parsed under the Discord preset will report the timestamp as a number of milliseconds before the Unix epoch (because Instagram's epoch is `2011-01-01T00:00:00Z` but its 41-bit block is seconds since 2011, not ms since 2015). Once you have seen one of these mismatches you can usually classify the platform by the timestamp magnitude alone — but the custom-profile path is the right answer when the platform is unknown or proprietary.

## When the custom profile is the only path that works

The six default presets cover the publicly documented platforms. Internal Snowflake schemes at every company pick their own `(timestamp_bits, worker_bits, sequence_bits)` triple, and often their own epoch. A few common custom shapes you will encounter in production:

- `(48-bit ms timestamp) | (8-bit worker) | (8-bit sequence)` — used by several Erlang/OTP-based systems and some Go services with `sonyflake`-inspired layouts.
- `(41-bit ms timestamp) | (5-bit datacenter) | (3-bit worker) | (5-bit sequence)` — common in older Twitter-internal tooling that needed more datacenter granularity than the public 10-bit machine slot.
- `(40-bit 100ns timestamp since Windows epoch) | (24-bit sequence)` — anything using `.NET`'s `Guid` generation has this layout, though the resulting UUID structure is 128-bit rather than 64-bit.
- `(46-bit second-resolution timestamp) | (16-bit shard) | (2-bit reserved)` — Stripe-style internal IDs with second resolution and 16-bit shard capacity.

The decoder's "Custom" preset asks for the bit layout as a JSON list of `{name, bits}` objects (least-significant-field-first), the timestamp unit (ms / 10ms / s), and the epoch in either ISO format or Unix ms. For an internal Snowflake with `(47-bit ms timestamp | 8-bit worker | 9-bit sequence)` and epoch `2020-01-01T00:00:00Z`, the custom fields JSON is:

```json
[{"name":"sequence","bits":9},{"name":"worker","bits":8},{"name":"timestamp","bits":47}]
```

And the parsed output follows the same three-tuple pattern: `(ts, worker, sequence)`. The custom-epoch input also accepts ISO format (`2020-01-01T00:00:00Z`) or Unix ms (`1577836800000`); both are normalized to ms internally so the per-platform bitfield parsing does not have to care which format you supplied.

## Closing

The five decisions a Snowflake decoder has to make — bit layout, epoch, timestamp unit, worker slot, sequence increment — combine into one parsed triple: `(date, worker, increment)`. Pick the wrong bit layout and the sequence becomes the worker; pick the wrong epoch and the date lands in the year 48,817 or the year 1970; pick the wrong timestamp unit and the date lands a factor of 1000 off. The decoder bakes the canonical six platforms into one parser and lets you describe any other layout through the custom-profile path.

If you want to see the failure modes side by side, the [Snowflake / Discord ID Bit Decoder](https://elysiatools.com/en/tools/snowflake-discord-id-bit-decoder) runs the same 18-digit `109580041603153152` through Discord, Twitter, Mastodon, Sonyflake, Instagram, and a custom-profile variant in one pass, and prints the decoded timestamp, worker/process slots, sequence, and shard bucket side by side. The math behind each output is the same bitfield-arithmetic that any runtime ID generation library does internally — the difference is that you can see all of them at once and pick the one that matches the system you are debugging.

For more tools that translate raw binary layouts into inspectable numeric output, the [Elysia Tools collection](https://elysiatools.com/en/tools) catalogs the full set.
