<strong>Cellular IoT packets look like noise until you crack open the right layer.</strong> NB-IoT and LTE-M Cat-M1 devices speak CoAP, LwM2M, and CoAP-over-SMS over radio bearers that drop below 200 kbps — and when a fleet debugging session lands a hex dump on your desk, knowing which RFC header to peel first turns an hour of guessing into ten seconds of parsing. The [NB-IoT LTE-M Cat-M1 CoAP LwM2M Cellular IoT Packet Analyzer](https://elysiatools.com/en/tools/nb-iot-lte-m-cat-m1-coap-lwm2m-cellular-iot-packet-analyzer) is purpose-built for exactly that workflow: hex in, decoded protocol tree out, with the corner-case handling (block-wise reassembly, Observe cancellation, SMS bearer unwrap) already wired up.

## Why cellular IoT traffic needs a different decoder

A laptop running Wireshark will happily show you the bytes, but it won't decode the application layer the way a fleet engineer needs. CoAP options with delta-encoded option numbers, LwM2M TLV-encoded resource trees with object IDs from the OMA registry, and SMS-DELIVER TPDUs carrying a CoAP message wrapped inside a 3GPP TS 23.040 UDH application-port addressing field — each layer has its own grammar, and the layers nest. A hex dump from a [popular firmware's AT-command log](https://elysiatools.com/en/tools/nb-iot-lte-m-cat-m1-coap-lwm2m-cellular-iot-packet-analyzer) is rarely a single protocol: it's CoAP-over-SMS-over-UDP-or-non-IP, with DTLS in front and a registration payload at the back.

The analyzer handles all of those in one pass. Paste the hex, pick the framing (raw CoAP, CoAP-over-SMS, LwM2M TLV), and the decoded tree shows the option numbers, the ETag, the block1/block2 offset, the LwM2M Object ID and Resource ID, and — if the registration link-format is present — the resource paths the device is announcing.

## Why a dedicated CoAP decoder matters on a battery radio

Before diving into the byte layout, it's worth naming the constraint that drives every design choice in cellular IoT: the radio. NB-IoT devices spend most of their lives in deep sleep, waking for a few milliseconds to transmit, then sleeping again for hours or days. Every byte on the wire costs energy; every retransmit costs ten times as much. This is why the protocols are so compact, why headers fit in twelve bytes, why option deltas exist, and why `NON` confirmables are favored over `CON` even though `CON` is more reliable. When a decoder shows you the option structure, it's showing you a series of decisions the device firmware made to stay alive.

## The CoAP header, decoded in twelve bytes

CoAP's compactness is its defining feature. A GET request fits in four header bytes plus a token, with all method semantics carried in option deltas. The analyzer's CoAP decoder surfaces:

- **Version (2 bits)** — must be `01`; a different value is a malformed packet that won't route.
- **Type (2 bits)** — `CON` (confirmable), `NON` (non-confirmable), `ACK`, `RST`. Cellular IoT lean heavily on `NON` to save battery; the retransmission logic that `CON` triggers is hostile to duty-cycled radio.
- **Token Length (4 bits, 0–8)** — TKL=0 means no token; TKL=8 is the upper bound.
- **Code** — class.detail, where `0.01` is GET, `0.02` is POST, `2.04` is Changed. The analyzer decodes this against the standard [IANA CoAP code registry](https://elysiatools.com/en/tools/nb-iot-lte-m-cat-m1-coap-lwm2m-cellular-iot-packet-analyzer).
- **Message ID (16 bits)** — for `CON`/`ACK` matching.
- **Token (TKL bytes)** — client-generated correlation ID.
- **Options** — delta-encoded, with delta over 12 needing the 13/14 extended-delta bytes, and length over 268 needing the 15 marker followed by a 16-bit length.
- **Payload marker (`0xFF`)** — separates options from the optional payload, prefixed by a Content-Format option.

For a debugging session, the most useful fields are the **URI-Path options** (which LwM2M resource is being touched), the **Observe option** (delta 6, length 0–3 bytes for the sequence number), and **Block1 / Block2** (delta 13/14, length encoded). The analyzer lifts these into a tree so you don't have to chase option-number arithmetic by hand.

## Block-wise transfers (RFC 7959) — the part that catches everyone

A CoAP message has a UDP datagram budget. On NB-IoT the radio link's maximum payload is 15–35 bytes in the downlink direction depending on coverage enhancement level, and even LTE-M tops out well below 1 KB per datagram. Anything bigger has to be split across block-wise transfers, and the option encoding is where most manual decoding goes off the rails.

The analyzer tracks:

- **Block1** (delta 13) — request-side fragmentation. The `NUM` field is the block number; `M` (more-bit) tells you whether another block follows; `SZX` is the block size exponent (2^(SZX+4) bytes).
- **Block2** (delta 14) — response-side fragmentation, same encoding but used for the server's reply.

The cumulative message ID and the M-bit together let you reconstruct the full payload. If you see `Block2: NUM=3, M=1, SZX=3` in a response, the device is asking for the next 1 KB slice of a payload the server is splitting across blocks 0, 1, 2, and 3.

## LwM2M TLV — the actual protocol your device speaks

LwM2M sits on top of CoAP. Every resource read or write is a CoAP GET, POST, PUT, or DELETE against a URI like `/3/0/9` (Object 3, Instance 0, Resource 9 — the device's battery level on OMA's standard object). The body is TLV-encoded: each entry is a Type-Length-Value triple where the Type encodes the 16-bit Object/Instance/Resource ID, the Length is the byte count, and the Value carries the actual data.

The analyzer reads TLV according to OMA-TS-LightweightM2M §7.4.4 and resolves Object IDs against the standard OMA registry:

- `/3/0/9` → Device Object, battery level (%)
- `/4/0/0` → Connectivity Monitoring, IP address
- `/3300/0/5700` → Sensor Value, "Sensor Value" resource

When a device bootstraps, it POSTs a registration message in RFC 6690 link-format to the LwM2M server. The analyzer decodes the registration's `<…>;rt="oma.lwm2m"` payload and shows you exactly which objects the device is announcing.

## SMS as a bearer: when CoAP travels over 3GPP control plane

In coverage-extension scenarios or when a device is outside data-bearer coverage, CoAP is sometimes carried over SMS-DELIVER. The 3GPP TS 23.040 TPDU has its own header (UDH, originating address, service-center timestamp) and inside the UDH the **application port addressing** (IEI 0x04 / 0x05) tells the device which socket to deliver the inner payload to. A CoAP message inside an SMS arrives as the user-data portion after the UDH; the analyzer transparently unwraps it so the same CoAP decoder runs against the inner bytes.

This is the part of the protocol stack where the analyzer earns its keep: a hex string that starts with `0791...` (an SMS-DELIVER PDU) and ends with a `40 01 00 01` CoAP header would be unreadable in a generic hex viewer. The analyzer walks the TPDU, extracts the user-data, identifies the CoAP framing, and gives you a single decoded tree.

## DTLS 1.3 (RFC 9147) record headers and session resumption

Cellular IoT devices are heavily constrained, so a full DTLS handshake on every reconnect is expensive. The analyzer decodes DTLS record headers — content type, version, epoch, sequence number, length — and shows whether the handshake is a fresh full handshake (HelloVerifyRequest cookie exchange, ECDHE key share) or a **session resumption** (PSK-based, with the session ticket embedded in the NewSessionTicket message). On resumption, the epoch in the record header is the giveaway: a fresh handshake starts at epoch 0 and bumps to 1 once the cipher suite activates; resumption jumps straight to the resumed epoch without a new handshake roundtrip on the wire.

## Putting it together: a real hex dump

Paste `40 02 00 01 8b fb 6b 32 39 2f 33 2f 30 2f 39 84 09 65 6e 64 65 76 69 63 65` and the analyzer returns: CoAP POST, MID 0x0001, token 0x8bfb, URI-Path `/3/0/9` (Device / Instance 0 / Resource 9 — battery level), Content-Format `application/octet-stream` (delta 12, length 1), payload `endevice` (8 bytes — the manufacturer identifier). Knowing the structure tells you exactly why a fleet manager might be seeing `2.04 Changed` from a hundred devices but `4.04 Not Found` from a few — the malformed ones are sending `4.00` instead of `4.01` in the URI-Path option, and that's the difference between `Path` (a single resource) and a path that the server couldn't resolve.

Try your own hex dumps against the [NB-IoT LTE-M Cat-M1 CoAP LwM2M Cellular IoT Packet Analyzer](https://elysiatools.com/en/tools/nb-iot-lte-m-cat-m1-coap-lwm2m-cellular-iot-packet-analyzer), and explore more protocol tools at [elysiatools.com/en/tools](https://elysiatools.com/en/tools).
