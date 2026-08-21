If you have ever tried to load a folder of `application.log` files into a spreadsheet and gotten back a wall of timestamp prefixes, varying severity keys, and `Apache combined log format` lines creeping in alongside `{"level":"info"}` JSON lines, you already know why a log analyzer that does format detection, field inference, and structured export belongs in every backend &amp; ops pipeline. The [Structured Log Analyzer](https://elysiatools.com/en/tools/structured-log-analyzer) turns a pasted log blob into a typed table that exports to JSON, CSV, or SQL inserts without you writing a parser per format. This guide walks through how to use it on the shapes you actually see in production &mdash; mixed JSON lines, Apache access logs, syslog fragments, custom regex patterns, and the multi-line stack traces that hide between single-line records.

<h2>Why A Mixed-Log Detector Earns Its Slot</h2>

Production logs are never one shape. A single tenant typically runs an application that emits JSON lines, a reverse proxy that writes Apache combined-log format, an OS that writes syslog, and a hand-rolled service whose only contract is "follow this regex." The naive fix is to write one parser per format and merge the rows downstream &mdash; which is fine until the third format lands and the merge logic eats a Friday. The analyzer's auto-detect path inspects each line, classifies it into a known shape, extracts the core fields, infers column types from the values, and emits a single unified table. The whole loop runs in the browser, so nothing leaves the tab.

The gain is bigger than it looks. Field inference means a column of timestamps becomes a real `datetime` instead of a string column, a column of HTTP status codes becomes an integer you can `GROUP BY` on, and a column of durations becomes a number you can plot. Export to JSON keeps the type fidelity, export to CSV flattens to a spreadsheet-friendly form, and SQL inserts get a typed `CREATE TABLE` that mirrors the inferred schema. The [Data Processing](https://elysiatools.com/en/tools/data-processing) hub on Elysia Tools lists other field-detection utilities worth pairing with this one when you have JSONL or CSV inputs that are already clean but need a quick shape check.

<h2>Five Output Bands The Analyzer Tags On Every Row</h2>

When the analyzer finishes a parse, it tags each row with one of five output bands that describe where the row came from and what type fidelity it carries. Knowing the bands lets you pick the export target deliberately instead of letting the auto-export guess for you.

<ul>
<li>`01 PARSED` &mdash; the line matched a known format, every named field extracted, type inferred.</li>
<li>`02 INFERRED` &mdash; the line did not match a known format but a custom regex caught it; field names come from your `(?<name>...)` group labels.</li>
<li>`03 PARTIAL` &mdash; only some fields matched; missing columns filled with `null` and flagged in the report.</li>
<li>`04 SKIPPED` &mdash; the line was a comment, blank, or pure-noise (e.g. a `---` separator); recorded for audit but excluded from exports.</li>
<li>`05 RAW` &mdash; the line could not be parsed at all; surfaced verbatim in the report with the auto-detect verdict attached.</li>
</ul>

The bands travel with the row into every export target, so a CSV export keeps a `band` column you can filter on, and a SQL export gets a `band` enum you can `WHERE` against. This is what makes the tool useful as the first step of an audit pass &mdash; you always know which rows were confidently parsed and which ones need a human.

<h2>Four Log Format Families The Detector Auto-Classifies</h2>

The auto-classifier knows four format families out of the box, and it picks the family per line rather than per file. A pasted blob with one line of each format gets four correct parses, not one guess.

<ul>
<li>`JSONL` &mdash; JSON-per-line. Detected by leading `{` and parseable JSON. Fields are the keys, types inferred from the values.</li>
<li>`Apache CLF` &mdash; Apache "combined" access log format. Detected by the `host - - [timestamp] "METHOD path HTTP/x" status size` shape. Fields: `remote_host`, `timestamp`, `method`, `path`, `status`, `size`, `referer`, `user_agent`.</li>
<li>`Syslog` &mdash; `Mar 10 14:03:02 host app[pid]: message` shape (RFC 3164 ish, lenient on the year). Fields: `timestamp`, `host`, `process`, `pid`, `message`.</li>
<li>`Custom Regex` &mdash; any line that matches the user-supplied `customRegex` field with `(?<name>...)` named groups.</li>
</ul>

If you want to see what the [JSON to Go Struct Converter](https://elysiatools.com/en/tools/json-to-go) does with a JSONL line you parsed out, paste the inferred schema in and let it spit out a typed struct. For diff workflows (which line format shifted last Tuesday), the [CSV/Excel Diff Tool](https://elysiatools.com/en/tools/csv-excel-diff-tool) reads the exported CSV and surfaces the drift between two days of the same log source.

<h2>Five Reasons A Custom Regex Beats Auto-Detection</h2>

Auto-detection is good enough for the common four formats and brittle for anything custom. Reach for the custom-regex path when any of these five conditions hold.

<ul>
<li>`01 NAMING` &mdash; your service writes structured logs but with field names like `evt` and `src` instead of `event` and `service`; a regex with `(?<event>...) (?<service>...)` renames them.</li>
<li>`02 TYPES` &mdash; the default inference sees `1234` as a number when you want it as a string; a custom `(?<code>\d+)` group captures it as text.</li>
<li>`03 SHAPE` &mdash; your lines have variable-tail fields (a JSON blob embedded in a syslog message); regex with `(?<ctx>\{.*\})` peels off the blob for a nested parse pass.</li>
<li>`04 MIXING` &mdash; one file contains four services with different layouts; a per-service regex dispatch (set the `source` field first, then dispatch) maps them correctly.</li>
<li>`05 STABILITY` &mdash; the format is unlikely to change but the auto-detect heuristics occasionally misfire on edge cases; locking the format with a regex removes the guessing.</li>
</ul>

The custom regex field takes any standard JS-flavored regex with named groups. Use single-line mode by default; flip the `aggregateMultiline` flag on when your lines wrap across newlines (Java stack traces, multi-line JSON values).

<h2>The Pre-Publish Sanity Loop &mdash; Three Audit Checks That Catch Most Mistakes</h2>

Before you click export, run three audit checks on the inferred table. These are the same checks the [Data Processing](https://elysiatools.com/en/tools/data-processing) tools apply to their outputs, distilled to the log-analyser case.

<ul>
<li>**Row-count delta** &mdash; the parsed row count plus the skipped row count plus the raw row count should equal the input line count. Off-by-one usually means a multi-line block collided with a single-line parse.</li>
<li>**Type sanity** &mdash; every numeric column should have at least 95% values that parse to a number in the chosen export format; below that, the column is a string masquerading as a number.</li>
<li>**Null density** &mdash; any column with more than 50% null values is a signal the regex or the format detection is misaligned with your real shape.</li>
</ul>

If a row lands in the `RAW` band after this loop, you have two options: tighten the custom regex or accept the verbatim row in the report and exclude it from the SQL export.

<h2>How The Export Bands Map To Real Downstream Pipelines</h2>

Export target choice is not cosmetic &mdash; each one carries type fidelity differently.

<ul>
<li>`JSON` keeps the inferred types. Use this when the next stage is a JSON-aware pipeline (a Node service, a Python `json.loads` call, a Logstash `json` filter).</li>
<li>`CSV` flattens every value to a string. Use this when the next stage is a spreadsheet, a `pandas.read_csv` call, or a SQL `COPY FROM` against a `TEXT` column.</li>
<li>`SQL` emits typed `CREATE TABLE` plus `INSERT` statements. Use this when you want the inferred schema to become a real table in Postgres or MySQL.</li>
<li>`HTML` is the report view &mdash; the same data rendered for a human, with band tags, format verdicts, and the original line side-by-side.</li>
</ul>

If your downstream is a Postgres-and-dbt stack, the SQL export saves you the `dbt seed` step entirely &mdash; paste the `CREATE TABLE` into a migration, run the inserts, and the rows are typed columns.

<h2>Pairing The Analyzer With The Rest Of The Elysia Tools Stack</h2>

The analyzer sits at the front of a log-handling pipeline. The middle (validation, normalization, diff) and the back (presentation, archival) have their own Elysia Tools that wire up cleanly.

<ul>
<li>For input cleanup before parsing, the [JSON Key Extractor](https://elysiatools.com/en/tools/json-key-extractor) lifts a subset of fields out of JSONL blobs &mdash; useful when you only care about five of twenty keys.</li>
<li>For trace reconstruction across services, the [Distributed Trace Decoder &amp; Waterfall Visualizer](https://elysiatools.com/en/tools/distributed-trace-decoder-waterfall-visualizer) reads JSONL spans and renders the timing chart.</li>
<li>For pattern matching against arbitrary log shapes (no parser required), the [Regex Cheat Sheet](https://elysiatools.com/en/tools/regex-cheat-sheet) is the reference table for the named-group syntax used in the custom regex field.</li>
<li>For data-URI inline embedding (handy when you want to share a parsed report in a chat message), the [Data URI Generator](https://elysiatools.com/en/tools/data-uri-generator) base64-encodes the report HTML.</li>
</ul>

Browse the full tool catalog at [elysiatools.com](https://elysiatools.com/en/tools). The analyzer is one of about thirty log-and-data utilities in the Data Processing hub, and it pairs well with the Format Conversion category when the next step is "ship the parsed CSV into a customer-facing XLSX."

<h2>The One-Sentence Mental Model</h2>

> Paste a mixed log blob, get back a typed table whose rows are tagged by parse band and whose columns are inferred from the values, with an export target that preserves the types you actually need.

That sentence is the entire workflow. The seven sections above are the audit and pairing notes that turn "works on one log file" into "trust it across an SRE rotation." Browse the full tool catalog at [elysiatools.com](https://elysiatools.com/en/tools), or jump straight back to the [Structured Log Analyzer](https://elysiatools.com/en/tools/structured-log-analyzer) to run this guide against your own log blob.