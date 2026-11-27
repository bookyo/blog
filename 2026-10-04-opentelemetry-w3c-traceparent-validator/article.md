<strong>Propagation bugs hide in byte positions your mocks never visit.</strong> W3C trace context headers travel in every span you ship, and every one of them has at least three places where a byte flip silently breaks distributed traces: a missing version prefix, a tracestate list with 33 members instead of 32, or a baggage value whose percent-encoding lost a delimiter. The OpenTelemetry W3C traceparent / tracestate / baggage + OTLP Header Propagation Validator catches each of those break modes in a single parse, then runs the two-header correlation round-trip that finds child span-id collisions your unit tests never reach. This is the field guide that walks the propagation contract as a contract — every byte position, every list-member ceiling, every encoding edge — and shows how to fold the validator into a CI gate so broken traces stop being a Monday-morning surprise.

The validator sits between your HTTP client and your collector's first hop. Paste a traceparent, a tracestate, or a baggage header and it returns the parsed fields, the version compliance flag, the W3C rule violations, and a propagation matrix that walks traceparent → tracestate → baggage → OTLP Content-Type → gRPC `grpc-trace-context-bin` so you can see how a single-byte edit in one header cascades into the next. The two-header correlation round-trip is the part most teams skip; it generates a child span-id, validates that the child fits inside the parent's trace-id namespace, and flags the case where two children collide on the same parent. For full end-to-end testing, run headers through the [OpenTelemetry W3C traceparent / tracestate / baggage + OTLP Header Propagation Validator](https://elysiatools.com/en/tools/opentelemetry-w3c-traceparent-tracestate-baggage-and-otlp-protobuf-headers-propagation-validator) alongside your existing unit suite — the validator catches what your mocks missed because mocks only test the happy path, and propagation bugs only show up on the broken path.

## How the W3C Trace Context Headers Are Structured

The W3C Trace Context spec defines two HTTP headers that travel with every request: `traceparent` and `tracestate`. Each one has a fixed byte layout, a fixed length budget, and a fixed set of allowed characters. Most propagation bugs come from a sloppy edit to one of those layouts.

A `traceparent` header is a four-field ASCII string in this exact order:

```
traceparent: 00-<32 hex trace-id>-<16 hex parent-id>-<2 hex trace-flags>
```

- `00` is the version. `ff` is reserved as "invalid" — anything else is future-version.
- `<32 hex trace-id>` is the 16-byte trace identifier. All zeros (`00000000000000000000000000000000`) is invalid.
- `<16 hex parent-id>` is the 8-byte parent span identifier. All zeros is also invalid.
- `<2 hex trace-flags>` is the bitfield (`01` = sampled, `02` = unknown, plus reserved bits).

Total length is exactly 55 ASCII characters. Any deviation is a parse failure. Most services accept lowercase or uppercase hex; the validator normalizes both.

A `tracestate` header is a list of up to 32 members, each shaped as `<vendor-key>=<value>`, comma-separated. The validator enforces:

- ≤ 32 list members (the W3C ceiling).
- Vendor key length ≤ 256 characters, must match `[a-z][a-z0-9_\-*/]{0,255}`.
- Value length ≤ 256 characters, must match <code>[!#$%&amp;'()*+\-.^_&#96;|~0-9a-zA-Z/]+</code> (RFC 7230 quoted-string with restrictions).
- Total header length ≤ 512 characters once the propagation header is split across multiple `tracestate` lines.

A `baggage` header is a similar list with percent-encoded values. Members use `key=value` pairs joined by `,`, with percent-encoding for reserved characters. The validator checks each value against the percent-encoding grammar and rejects values whose decoded length exceeds 4096 bytes.

## Why Your Mocks Miss Propagation Bugs

Three propagation bugs survive most unit suites:

1. **A version byte that doesn't exist yet.** If you write `01-...` thinking `01` is "the next version", the validator flags it as a future-version header and marks the parse as non-compliant. Most code silently accepts unknown versions and forwards them, which means downstream consumers treat the header as `00`-compatible and lose the version semantics the sender intended.

2. **A tracestate list that grew past 32 members.** The W3C spec lets vendors add list members freely, but if the total exceeds 32, downstream consumers are required to drop the overflow. The validator shows which members would be dropped and flags the line so you can see which vendor over-allocated.

3. **A baggage value whose percent-encoding is malformed.** A stray `+` in a percent-encoded string can be either literal or space-encoded depending on the encoder. The validator normalizes both, but flags the case where a value decoded to a reserved character (e.g. `=` inside a key segment) that breaks the `key=value` grammar.

For end-to-end propagation testing, the validator's two-header correlation round-trip is the missing test: feed it a parent traceparent and a child traceparent that share the trace-id but differ on parent-id, then ask whether the child-id collides with any sibling span-id in the tracestate list. Most propagation bugs hide in that intersection.

## What the Validator Parses and What It Rejects

The validator's parser walks each header character by character and rejects anything outside the W3C grammar. For `traceparent` it enforces: total length 55, version byte in `[0-9a-f]{2}` excluding `ff`, trace-id and parent-id in `[0-9a-f]{32}` and `[0-9a-f]{16}` excluding all-zeros, and trace-flags in `[0-9a-f]{2}`. For `tracestate` it enforces the ≤ 32 list members, vendor-key grammar, value grammar, and total length budget. For `baggage` it enforces the percent-encoding grammar and 4096-byte value ceiling.

The parser outputs a structured object with one field per rule, plus a top-level `compliance` boolean that flips to `false` on the first violation. CI tests can assert on either the structured object or the boolean; the structured object gives you the byte offset when a test fails.

## The Propagation Matrix: From traceparent to gRPC Binary Context

The validator walks five propagation channels in order:

```
HTTP traceparent (ASCII, 55 chars)
  → HTTP tracestate (list, ≤32 members)
    → HTTP baggage (percent-encoded)
      → OTLP/HTTP Content-Type (application/json or application/protobuf)
        → gRPC grpc-trace-context-bin (25-byte binary: 1 flag + 16 trace-id + 8 span-id)
```

Each hop has its own parser. The validator checks:

- `traceparent` matches the four-field grammar above.
- `tracestate` parses to ≤ 32 members with valid vendor keys.
- `baggage` percent-decodes without throwing and each value fits the 4096-byte budget.
- OTLP `Content-Type` is one of `application/json`, `application/protobuf`, or `application/x-protobuf` (legacy alias).
- gRPC `grpc-trace-context-bin` is exactly 25 bytes when decoded.

If any hop fails, the validator returns the failing hop's byte offset and the offending character. This is the part that's most useful in CI: a test that fails on byte 47 of a 55-byte header tells you exactly which character to fix.

## Two-Header Correlation Round-Trip

The validator's standout feature is the correlation test, which catches span-id collisions your unit tests never see:

```
Input:
  parent:    00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01
  child:     00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b8-01
Output:
  child_id:    00f067aa0ba902b8
  collision:   false
  parent_id:   00f067aa0ba902b7
  trace_id:    4bf92f3577b34da6a3ce929d0e0e4736
  sampled:     true
```

The collision check works by walking every `tracestate` member and every baggage key, computing the hash of the candidate child-id, and flagging any match. A collision means two spans in the same trace share a parent-id — your collector will dedupe them and you'll lose one of the spans.

For teams that want to add this check to CI, the simplest integration is to take a real trace from your staging environment, paste the headers into the validator, save the parsed output as a fixture, then assert in CI that the fixture matches the new parse. If anyone edits the propagation code and the parse drifts, CI fails with the byte offset of the changed character. To see how this pattern fits into a full HTTP trace pipeline, browse other Development tools at [Elysia Tools](https://elysiatools.com/en/tools).

## OTLP Content-Type Edge Cases

OTLP defines two wire formats for HTTP export:

- `application/json` — JSON-encoded request and response bodies.
- `application/protobuf` — protobuf-encoded request and response bodies. `application/x-protobuf` is the legacy alias and should be treated as equivalent.

The validator catches three common Content-Type bugs:

1. **`application/x-protobuf` rejected by a downstream that only knows `application/protobuf`.** Treat both as the same wire format — the validator normalizes them and emits a warning when the legacy alias is used.

2. **A missing `Content-Type` header on the OTLP export.** Some HTTP clients omit it when the body is empty. The validator flags the export as "no wire format declared" and treats the body as protobuf by default.

3. **A `charset=utf-8` parameter on the Content-Type.** OTLP doesn't define charset for binary wire formats; the validator strips charset before the comparison.

For teams shipping OTLP exports to multiple backends (one collector with JSON, another with protobuf), the validator's Content-Type assertion is the single source of truth. If you also want to see how this fits into a generic HTTP header inspection pipeline, browse the related [Elysia Tools samples](https://elysiatools.com/en/samples) for header parse patterns.

## Where the Validator Fits in a CI Gate

The pattern that works in practice:

1. Pull a real trace from staging (any span, any service).
2. Extract the `traceparent`, `tracestate`, `baggage`, and OTLP Content-Type from the wire format.
3. Run each header through the validator.
4. Assert the parsed output matches a stored fixture.
5. Run the two-header correlation round-trip on the parent + child pair.
6. Block the merge if any assertion fails.

The fixture is the load-bearing piece. Most teams skip the fixture and end up with a test that always passes because the test reads its own output. A stored fixture forces the test to detect drift, which is the whole point.

For teams that want to extend the pattern beyond HTTP, the validator's gRPC `grpc-trace-context-bin` parser is the entry point: it accepts the 25-byte binary context, decodes it to the same `traceparent` fields, and runs the same compliance checks. The propagation matrix becomes a single regex across both wire formats.

## Closing: Treat Propagation as a Contract

Most teams treat `traceparent` and `tracestate` as opaque strings their HTTP library sets. That's fine until a vendor adds a new tracestate key, a future version byte ships, or a baggage value over-allocates. The validator turns propagation from an implicit assumption into an explicit contract you can test against.

The minimum viable test set is small — one parse of a well-formed traceparent, one parse of a tracestate list at exactly 32 members, one parse of a baggage value at exactly 4096 bytes, and one two-header correlation round-trip that includes a deliberate collision. Add a fixture for each, run them in CI on every merge, and your propagation layer stops being a source of midnight pages.

To fold this into your own pipeline, start at the [OpenTelemetry W3C traceparent / tracestate / baggage + OTLP Header Propagation Validator](https://elysiatools.com/en/tools/opentelemetry-w3c-traceparent-tracestate-baggage-and-otlp-protobuf-headers-propagation-validator), pull a real trace, and walk the propagation matrix from your code side. The byte offsets in the parse output are the same byte offsets in your HTTP client. From there, treat every propagation layer as a contract you can pin to a fixture and you'll catch the next byte-flip bug before it reaches production.