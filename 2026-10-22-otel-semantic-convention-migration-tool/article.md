**A semantic-convention rename is a one-line diff; a semantic-convention migration is a codebase-wide search across five file types you may not know you own.** When OpenTelemetry spans move from semantic conventions v1.20 to v1.27, roughly thirty attribute names change. The rename table is public, complete, and boring. What is not boring is discovering that half of your usages live inside a Grafana dashboard JSON, a collector transform block, and a Java service maintained by a team you never met. The <a href="https://elysiatools.com/en/tools/otel-semantic-convention-migration-tool">OpenTelemetry Semantic-Convention Migration Tool</a> exists to make that search one operation instead of a week, and to tell you honestly which parts it refuses to automate.

## What Actually Changed Between v1.20 and v1.27

Semantic conventions version independently of the SDKs and collectors that consume them. v1.20 was effectively the last revision where HTTP span attributes still carried experimental status. v1.23.1 promoted HTTP to stable and renamed most of the group in the same release, because stable status is the moment a name stops moving — a rename at the exact point it is allowed to stop. v1.24.0 carried the database group forward. v1.27.0 finished the messaging group.

That produces a migration surface with a shape nobody expects. There is no single v1.20 to v1.27 jump in practice, because teams upgrade their SDKs on their own schedule and their collector on another. What you actually face is a matrix: three plausible source revisions, three plausible target revisions, and a different attribute delta for each pair. A migration tool that only knows the endpoints will quietly produce the wrong answer for the middle of the matrix, so the useful input is the version pair, not a single dropdown.

## The Five Renames That Break Every Dashboard

Five one-to-one renames account for the overwhelming majority of broken panels after a convention upgrade.

- `http.method` becomes `http.request.method`
- `http.status_code` becomes `http.response.status_code`
- `http.url` becomes `url.full`
- `db.system` becomes `db.system.name`
- `messaging.destination` becomes `messaging.destination.name`

Each of these is trivially mechanical. The damage does not come from the rename itself. It comes from lag. A Grafana panel written against `http.method` keeps rendering happily for months after the SDK upgrade, because a missing attribute in a Prometheus-style query usually evaluates to an empty series rather than an error. You find out during an incident, or during a capacity review, or from a colleague asking why the service-latency panel is flat at zero.

The second structural point is that `url.full` is not a rename in spirit at all. The old `http.url` carried the full request URL including query string. `url.full` carries the absolute URL without the query string and fragment, which is a deliberate data-leak fix. Any dashboard or recording rule that was relying on a query parameter embedded in that attribute changes behaviour even though the rename succeeds.

## Read the Diff Before You Write the Fix

The order of operations matters more than it sounds. Run the migration, then read the per-attribute diff statistics before touching a single file. The statistics answer a question you cannot answer by inspection: how many usages does each renamed attribute actually have.

A high count on `http.method` is comfortable news — it means one mechanical pass fixes it and the review is trivial. A count of zero is more interesting than a high count, because it usually means the attribute name is buried somewhere the scraper does not reach by default, such as a Grafana JSON string or a collector YAML block that is not part of the pasted source.

The unmapped-attribute report is the real deliverable. It lists every attribute you used that has no automatic mapping, split into the three outcomes described further down. Most teams discover that this list, not the rename table, is where the actual engineering work is.

## The Collector Transform Is Not a Find and Replace

There is a collector-side answer to every rename, and it is a trap if you reach for it first. An OpenTelemetry Collector `transform` statement can rename attributes at ingest with a `rename_attribute` action inside a `trace_statements` entry scoped to span context. It works on the first try, it needs no application deploy, and it produces exactly the wrong mental model.

Attributes renamed in the collector are new names wearing old data. Your application source still emits `http.method`, your local debugging sessions still show `http.method`, and the next person to read a trace in a terminal or a profiler sees a name that no longer appears anywhere in the shipped code. Worse, the collector config becomes load-bearing for correctness, so a collector rollback silently restores the old names everywhere downstream.

Use the collector transform as a bridge for services you do not own, not as a destination. Generate it, apply it to the third-party service, and schedule the source-side fix.

## Unmapped Attributes Are the Actual Work

Everything the tool will not do automatically falls into three classes, and the class determines how much of your afternoon it costs.

The first class is the removal. Some v1.20 attributes have no v1.27 equivalent because the convention authors decided the concept was ill-defined or privacy-unsafe. `http.host` is the common example: it conflated the server name with the port, and the replacement splits the concept. There is no single correct answer here, so a warning is the only honest output, and you have to decide per service whether the attribute was load-bearing.

The second class is the manual split. One old attribute becomes two new ones, and no automatic tool can know which half belongs in which name without knowing your topology. `net.peer.name` splitting into client and server addresses is the canonical case: whether it is the client or the server depends on the direction of the call, which is context the scraper does not have.

The third class is the dashboard string. An attribute name embedded inside a JSON value is text, not code, so a source-level rename cannot reach it. That is a separate pass over a separate set of files, and it is the pass most often skipped.

## Dashboards Are JSON Too, and They Are Worse

Grafana dashboards store the attribute name in at least four distinct places, and a migration that only rewrites the query text will still leave a broken panel behind.

The panel query is the obvious one. The second is the datasource override block, where a legacy name appears as a key rather than as a value. The third is the templating variable, which usually contains a regular expression matching attribute names, so it fails silently when the match set goes empty. The fourth is the annotation definition, which is easy to miss because it is rarely opened during a migration.

The tool handles this as an explicit opt-in that applies the same rename map inside JSON string values, because rewriting JSON structurally and rewriting attribute names textually are two different operations with different failure modes. Turn it on when your dashboards are checked in. Leave it off when they live only in a shared Grafana workspace, where a scripted edit is a permissions problem rather than a parsing problem.

## A Migration Checklist That Survives a Code Review

A review-ready migration has a shape, and the shape is mostly about ordering and evidence rather than cleverness.

1. Run the migration against the version pair you are actually moving between, not the endpoints.
2. Read the diff statistics and confirm the high-count attributes match your expectation of where the code lives.
3. Triage the unmapped report into removal, split, and dashboard-string before editing anything.
4. Apply source-side renames in the services you own, one service per commit so a bisect stays meaningful.
5. Generate the collector transform for third-party services you cannot deploy, and mark it as temporary in the config file itself.
6. Re-run the migration on the merged tree and confirm the unmapped list is empty or explicitly waived.
7. Update dashboard JSON in the same pull request as the dashboards that consume it, never in a follow-up ticket.

Step seven is the one that gets skipped, and it is the one that produces a migration that is green on every CI check and still wrong in production for a month.

## Where to Take the Numbers Next

The migration is the boring half of an observability upgrade. The interesting half is what your spans look like once the names are correct and the unmapped attributes are gone. Once attribute names are stable, the same span data starts working with tools built for structured telemetry, including the <a href="https://elysiatools.com/en/tools/logfmt-to-json-structured-log-bridge">logfmt to JSON structured-log bridge</a> for flat log lines that carry the same attribute vocabulary. When you need to verify that a propagated context header survived your service hop, the <a href="https://elysiatools.com/en/tools/opentelemetry-w3c-traceparent-tracestate-baggage-and-otlp-protobuf-headers-propagation-validator">W3C traceparent and OTLP header propagation validator</a> checks the wire format directly. And when a rename does land wrong in a shared dashboard, a <a href="https://elysiatools.com/en/tools/json-diff-visualizer">JSON diff visualizer</a> shows you exactly which query changed. Run the migration, close the unmapped report, then explore more tools at <a href="https://elysiatools.com/en/tools">elysiatools.com</a>.