# 3 NDJSON Sample Files Every Developer Needs for ETL and Streaming Tests

Your JSON parser breaks the moment you feed it a 500MB file. That's not a bug — it's a design limitation. Standard JSON loads everything into memory. NDJSON (Newline-Delimited JSON) doesn't.

NDJSON is one valid JSON object per line. No brackets, no commas between records, no memory explosion. It's the format behind Kafka topics, Cloud Dataflow inputs, and every serious ETL pipeline that can't afford to choke on a 10GB dataset.

[ElysiaTools](https://elysiatools.com) offers **three free, downloadable NDJSON sample files** — simple users, orders, and analytics events — ready for ingestion tests, stream processing experiments, and pipeline benchmarking. No sign-up, no rate limits.

---

## 1. Simple Users NDJSON — Baseline Identity Data

The starting point for any data pipeline test.

```ndjson
{"id":1,"name":"Alice","active":true}
{"id":2,"name":"Bob","active":false}
{"id":3,"name":"Carol","active":true}
```

**What this file tests:** Data ingestion speed, schema validation, identity deduplication, and basic record parsing. It has 4 fields per record (id, name, active, and an implicit timestamp). If your ETL tool can't handle 10,000 lines of this, it won't handle anything.

**Real-world use case:** Onboarding a new data warehouse and you need synthetic user records to test your JSON → SQL mapper. Point your pipeline at this file and watch it fly.

[Try Simple Users NDJSON →](https://elysiatools.com/en/samples/ndjson)

---

## 2. Intermediate Orders NDJSON — Transactional Data with Context

A step up. Each record carries a customer ID, timestamp, currency, amount, and status — the full anatomy of a commerce event.

```ndjson
{"order_id":1001,"customer_id":501,"order_date":"2026-01-10T08:30:00.000Z","amount":1280.5,"currency":"USD","status":"paid","items_count":3}
{"order_id":1002,"customer_id":502,"order_date":"2026-01-12T10:45:00.000Z","amount":98.2,"currency":"EUR","status":"shipped","items_count":1}
```

**What this file tests:** Multi-field schema validation, currency normalization, date parsing across time zones, and status-enum handling. The mixed currencies (USD, EUR, CNY) force your pipeline to confront real data heterogeneity.

**Real-world use case:** Building a revenue reconciliation pipeline. Feed this into your stream processor and validate that orders aggregate correctly by customer, currency, and date range.

[Try Intermediate Orders NDJSON →](https://elysiatools.com/en/samples/ndjson)

---

## 3. Complex Events NDJSON — Analytics Streams with Nested Payloads

This is where most pipelines fall apart.

```ndjson
{"event_id":"evt-0001","event_time":"2026-02-01T03:00:00.000Z","user_id":90001,"session_id":"sess-a1","event_type":"page_view","page":"/products/1001","country":"US","device":"mobile","browser":"Chrome","revenue":0,"latency_ms":123,"payload_json":"{\"referrer\":\"google\",\"ab_bucket\":\"B\",\"experiments\":[\"hero_v2\",\"checkout_copy_a\"]}"}
```

**What this file tests:** Nested JSON-in-JSON handling, A/B test attribution parsing, session grouping by session_id, latency outlier detection, and multi-dimension event categorization. The `payload_json` field contains escaped JSON that needs a second parse pass — exactly the kind of thing that silently corrupts data in naive implementations.

**Real-world use case:** Validating a real-time analytics dashboard. Parse the event stream, extract `payload_json` fields, and compute per-session conversion rates. If your parser drops events or double-counts sessions, you'll see it immediately.

[Try Complex Events NDJSON →](https://elysiatools.com/en/samples/ndjson)

---

## Why NDJSON Wins Over JSON for Pipeline Testing

| Feature | JSON | NDJSON |
|---------|------|--------|
| Partial read | ❌ Load entire file | ✅ Read line by line |
| Stream processing | ❌ Needs SAX parser | ✅ Native streaming |
| Unix tooling (grep, wc) | ❌ Full parse required | ✅ Works out of the box |
| Append-only writes | ❌ Rewrite full file | ✅ Append a line |
| Error isolation | ❌ One bad char breaks all | ✅ One bad line, rest continue |

The key insight: NDJSON is **line-oriented by design**, which means every line is an independent, valid JSON blob. Your parser can process line 1, encounter a malformed line 2, skip it, and continue with line 3. Try doing that with a JSON array.

---

## What Nobody Tells You About NDJSON at Scale

At high throughput — think millions of events per hour — the framing between records matters more than the records themselves. Newline-delimited means your consumer needs to know where one record ends and the next begins. At 1M records/hour, a single malformed line with a newline character inside a string field will silently desynchronize your entire stream.

This is exactly why testing with these sample files matters. You catch the edge cases before they hit production.

---

## Get Started

All three NDJSON sample files are free, downloadable, and ready to use on [ElysiaTools](https://elysiatools.com/en/samples/ndjson):

- **[Simple Users NDJSON](https://elysiatools.com/en/samples/ndjson)** — 4 fields, basic identity records. Start here.
- **[Intermediate Orders NDJSON](https://elysiatools.com/en/samples/ndjson)** — multi-currency transactions. Tests schema and currency handling.
- **[Complex Events NDJSON](https://elysiatools.com/en/samples/ndjson)** — nested payloads, analytics dimensions. The real pipeline stress test.

No sign-up. No rate limits. Just free, realistic data for your next ETL experiment.
