**An NTP packet is not 48 random bytes — it is a 384-bit structure where the first 8 bits alone tell a client whether the world just learned about a leap second, the next 2 bits betray which protocol version is in play, and the last 32 bits encode an absolute UTC timestamp using an epoch that predates Unix by 70 years.** If you have ever stared at a hexdump from `tcpdump -ni eth0 'udp port 123'` and tried to make sense of `24 01 0c fa 000005e4 0000059c 47505300 ...`, this guide is for you. We will walk through the NTPv4 packet (RFC 5905) and its SNTP cousin (RFC 4330) field by field, then see how the [NTP RFC 5905 / SNTP Leap Second & Epoch Decoder](https://elysiatools.com/en/tools/ntp-rfc-5905-sntp-leap-second-epoch-decoder) renders the same numbers into a panel your watch can compare to wall-clock time.

## Why NTP packets look so strange

The NTP wire format was frozen in 1985 and has barely moved since. It uses the **NTP epoch** of 1900-01-01 00:00:00 — seventy years before the Unix epoch of 1970-01-01. By the time you read this, the NTP timestamp for "right now" is a 64-bit unsigned integer around `0xec5e0d0000000000` (about 4.0 billion seconds since 1900). Every modern NTP client converts this to Unix time by subtracting the well-known `0x83aa7e80` (2,208,988,800 seconds) offset.

The first 32 bits of every NTP packet are a **status octet cascade** — Leap Indicator (2 bits), Version Number (3 bits), Mode (3 bits), then Stratum (8), Poll (8), Precision (8), and Root Delay (32). That is a lot of dense semantics before you even reach a timestamp. A single bit flip in the right place can change a packet's meaning from "sync to me" to "drop your association, do not respond".

## The first 8 bits tell three stories at once

`0x24` in the canonical stratum-1 packet from a GPS-disciplined server reads as binary `0010 0100`. Reading the bits left-to-right:

- **Leap Indicator (LI) = 0** (`00`) — no warning. A value of `01` would mean "last minute has 61 seconds", `10` would mean "last minute has 59 seconds", and `11` means "clock unsynchronized" (often kiss-o'-death).
- **Version Number (VN) = 4** (`100`) — this is NTPv4, RFC 5905. SNTPv4 uses the same version field.
- **Mode = 4** (`100`) — the server is responding to a client. Mode 3 is client, mode 4 is server, mode 5 is broadcast, mode 7 is symmetric active for NTP peer exchanges.

That is exactly what a decoded panel shows in the LI/VN/Mode row — the bit triplets in their natural reading order, plus a textual legend so you do not have to memorize that `011` in Mode means a symmetric-peer packet rather than a unicast client.

## From raw bytes to a UTC timestamp

The four timestamps (Reference, Origin, Receive, Transmit) each occupy 64 bits — 32 bits of seconds since 1900 and 32 bits of fractional second. The fractional field is **not** a millisecond; it is a fixed-point denominator of `2^32`, which gives roughly 233 picosecond resolution. A value of `0x80000000` therefore represents exactly 0.5 seconds.

Conversion to UTC is a three-step recipe:

1. Read the seconds field as an unsigned 32-bit integer.
2. Subtract `2208988800` to move from the 1900 epoch to the Unix epoch.
3. Add the current TAI-UTC offset to get UTC. As of 2026-01-01, that offset is **37 seconds** (the leap-second insertion at the end of 2016, plus the 27 added earlier). The decoder shows this offset explicitly so the result can be sanity-checked against `date -u` on the host.

The fractional part is left as raw `0.xxxxxxxx` seconds unless you round it to milliseconds, which is almost always enough for log correlation.

## Stratum, reference ID, and the kiss codes

Stratum is the hop count from a primary reference clock. Stratum 0 means "this device is itself the reference" (a GPS receiver, an atomic clock). Stratum 1 means "directly synchronized to a stratum-0 device". Stratum 2 synchronizes to stratum 1, and so on, with a hard ceiling of 15 — anything beyond that is considered unusable.

The Reference ID is four ASCII characters when the stratum is low (`47505300` reads `GPS\0`, identifying a GPS source) and a four-character **kiss-o'-death code** when stratum is 0 or unsynchronized. The codes are unkind by design:

- `DENY`, `RSTR`, `CRYP` — the server refuses to serve you, often because of access controls or cryptographic failure.
- `RATE` — you are polling too often; back off.
- `STEP` — the server's time changed by more than the step threshold; a client should reset its association.

A `CRYP` from your upstream is the NTP equivalent of a stern letter from your bank: do not ignore it.

## What SNTPv4 leaves on the table

SNTPv4 (RFC 4330) deliberately drops the stateful parts of NTP — the filtering, selection, and clock-discipline algorithms — and keeps only the wire format. A pure SNTP client reads one packet, computes one offset, and applies it. For a single-server setup this is exactly what you want; for a multi-peer mesh it is not, because SNTP does not perform Marzullo's algorithm or intersection to filter out a falseticker.

The decoder handles both modes transparently because the on-wire format is identical. If you feed it a packet that has only the Transmit timestamp populated and zeros in the other three, it will decode the LI/VN/Mode, the stratum, and the precision while flagging the missing Reference, Origin, and Receive fields. That is exactly the SNTP broadcast packet a server would emit from `ntpdate -q`.

## Verifying against a live capture

The fastest way to see a real packet is `tcpdump -ni lo0 -X 'udp port 123'`. After kicking `sntp -sS pool.ntppool.org`, you will see a 48-byte UDP datagram from a stratum-2 or stratum-3 server. Drop the bytes into the decoder in the same order they appeared in the dump (the first byte in the hexdump is the high byte of the LI/VN/Mode field). You should see UTC timestamps within a few milliseconds of your host's `date -u`, and a Reference ID like `132.163.xx.xx` if the upstream is a US pool node, or `GOOG` if you happen to be synced to Google's anycast NTP service.

For deterministic offline testing, the decoder ships with a built-in GPS-synced sample (`24 01 0c fa 000005e4 0000059c 47505300 eb5c3a80 ...`) that produces a fully-populated stratum-1 panel. Working through the bytes against the sample is the fastest way to internalize the bit layout.

## When the leap-second indicator finally fires

LI values of `01` and `10` are vanishingly rare — IERS announces leap seconds about six months in advance, and only 27 have been inserted since 1972. When the next one is announced, the world's NTP daemons will start emitting LI=1 packets at the end of the last day. If you are building any system that consumes NTP, the decoder is the quickest way to confirm your parser agrees with a reference implementation on what `01` and `10` actually mean — they are easy to swap if you read them as "minute has 61 seconds" vs "minute has 59 seconds" without checking the spec.

For a hands-on walk-through, paste a captured packet (or the canonical sample) into the [NTP / SNTP decoder](https://elysiatools.com/en/tools/ntp-rfc-5905-sntp-leap-second-epoch-decoder). The panel will resolve every field, including the bit triplets, the four timestamps in UTC, and the TAI-UTC offset in play at the moment the packet was generated. From there, comparing to `date -u` on the same host is a one-line sanity check — and the easiest way to catch a clock-skew bug before it bites a downstream log search.

## Common decoding mistakes worth flagging

A few pitfalls show up repeatedly when teams ship a custom NTP parser:

- **Byte order.** The 32-bit seconds fields are big-endian. Reading them as little-endian silently shifts the timestamp by 4.0 billion seconds — exactly enough to land in 2076 and immediately look like a clock-skew bug from the future.
- **Signed vs unsigned.** The Stratum, Poll, and Precision fields are all **signed** 8-bit integers in the spec, even though their natural values are small positive integers. A precision of `0xfa` decodes to `-6` and means "the system clock ticks every 64 ms", not "250 ticks per second". A parser that treats it as unsigned will report nonsense poll intervals.
- **Fractional truncation.** Rounding the 32-bit fractional seconds to a 16-bit integer for storage loses ~16 bits of precision and turns a sub-microsecond offset into a multi-second one. Keep the full 64 bits if your downstream cares about phase, not just wall-clock.

For each of these, the decoder renders the field the way the spec actually defines it, and a quick eyeball comparison against the raw input tells you whether your parser agrees.

Explore more protocol and timestamp tools at [elysiatools.com](https://elysiatools.com/en/tools).
