# CSV Flavor to SQL INSERT Emitter Field Guide: When Four Dialects, Six NULL Tokens, and Twelve Quoting Rules Decide Whether Your 200-MB Load Hits Production or Hits a Syntax Error

<strong>Loading 200 MB of CSV straight into MySQL usually ends one of two ways: a clean 38-second import, or a 38-minute cleanup of bracketed identifiers, backslash-doubling, and TIMESTAMP literals that the driver quietly rewrote.</strong> Most teams reach the same conclusion after their third failed `LOAD DATA INFILE` attempt: hand-written CSV-to-SQL converters are correct on a single dialect and brittle on the other three, and the dialect-switch cost is paid by whoever is on call when the next dataset arrives. The CSV Flavor to SQL INSERT Emitter ([Elysia Tools](https://elysiatools.com/en/tools/csv-flavor-to-sql-insert-emitter)) closes that gap by auto-detecting the CSV dialect, inferring column types per row scan, and emitting correct INSERT batches for MySQL, PostgreSQL, SQLite, and SQL Server — including the four ON CONFLICT / IGNORE / DUPLICATE KEY / MERGE variants that determine whether a re-run is idempotent or destructive. This field guide walks through the eight decisions the emitter makes on every load, and where each one shows up as a silent bug in a hand-rolled script.

## How the emitter reads the CSV before it writes a single INSERT

The first pass is dialect detection, not parsing. A four-byte probe decides whether the file is RFC 4180 comma, semicolon (Excel-CSV), tab (TSV), or pipe. A UTF-8 BOM is consumed and discarded before the first record. Quoted fields are then handled with full RFC 4180 semantics: a doubled quote inside a quoted field escapes correctly, and a field may contain a literal newline, delimiter, or both — none of those terminate the record.

A hand-written splitter almost always breaks here. The most common bug is `str.split(',')` followed by a `.replace('"', '')`, which collapses `"line one\nline two"` into two malformed rows. The emitter keeps state across newlines and only emits a record when the quote count for the current row is even. That single decision is the reason a 50,000-row file with embedded newlines parses in one pass instead of producing 53,402 rows.

## Why column-type inference is the load-or-stall moment

After dialect detection, the emitter scans every row to assign a column type from BIGINT, DOUBLE, BOOLEAN, DATE, TIMESTAMP, or TEXT. The order matters: a column that parses as BIGINT on row 1 and as a phone-number string on row 4,582 collapses to TEXT, not to a NULL-bomb at INSERT time.

The hand-rolled equivalent is a `CREATE TABLE ... TEXT` block followed by `INSERT INTO ... VALUES (...)`, which works until the first query tries to filter `WHERE amount > 100` and Postgres refuses because `amount` is a string. Inference also catches TIMESTAMP versus DATE — a `2026-09-13` cell becomes DATE, while `2026-09-13 09:00:00` becomes TIMESTAMP, and the two are never collapsed. For loads that include a timestamp column emitted by a legacy system, this distinction is what determines whether your analytics queries need a cast on every line.

## Four SQL dialects, four identifier-quoting conventions

MySQL quotes identifiers with backticks: `INSERT INTO \`orders\` (\`id\`, \`name\`) VALUES (...)`. PostgreSQL uses ANSI double-quotes. SQLite accepts either but emits double-quotes by default. SQL Server uses brackets. Get the wrong one and the parser either rejects every identifier (Postgres on backticks) or interprets the backtick as a stray token (MySQL on brackets).

The emitter picks the convention from the dialect selector, not from inference, because the convention is a property of the destination database, not of the data. The most common silent bug in a hand-rolled converter is emitting Postgres double-quoted identifiers into a MySQL target — MySQL accepts them as string literals and stores the column names with literal double-quote characters, which then fail every downstream ORM lookup. The emitter avoids this by tying the quoting convention to the dialect selector in the same code path that chooses the statement terminator.

## ON CONFLICT, ON DUPLICATE KEY, MERGE — which idempotent variant to choose

Every re-runnable load needs an idempotency clause, and the dialect determines the clause. Postgres and SQLite emit `INSERT ... ON CONFLICT (id) DO NOTHING` or `ON CONFLICT (id) DO UPDATE SET ...`. MySQL emits `INSERT ... ON DUPLICATE KEY UPDATE column = VALUES(column)`. SQL Server has no native INSERT-time upsert and is documented with a `MERGE` note.

The choice between DO NOTHING and DO UPDATE is a business decision, not a syntax decision. A staging table that should always reflect the source gets DO UPDATE. A fact table where late-arriving rows should be ignored gets DO NOTHING. The emitter exposes both per dialect, and the same source CSV emits a different statement depending on which mode is selected. A hand-written converter almost always hardcodes one variant and ignores the other, which is the cause of the recurring "why does the second run drop rows" bug.

## NULL-token recognition: the six strings that mean "no value"

CSV dialects disagree on which token represents a missing field. RFC 4180 says empty. Excel often emits `N/A` or a literal dash. Postgres `COPY` uses `\N`. SPSS exports `.`. Stata uses empty. The emitter accepts any of those as NULL via a selector, and emits the dialect-appropriate NULL representation: unquoted `NULL` in Postgres and SQLite, backticked `` `NULL` `` is never used, and the standard `NULL` keyword in MySQL and SQL Server.

The bug this prevents is the silent-string-load: a column where every empty value landed as the literal string `"NA"` or `""`, which then fails `IS NULL` filters downstream. A pass over the source column with a configurable null-token selector is the difference between a clean fact table and a column that needs a four-hour scrub on every load.

## Batch sizing and the multi-row VALUES clause

The emitter can emit a single `INSERT INTO orders VALUES (...), (...), (...);` with N rows per statement, or one INSERT per row. Multi-row VALUES is roughly 3x faster on MySQL and Postgres because it halves the parser overhead and lets the planner batch the executor path. The trade-off is that a single malformed row aborts the entire batch.

For staging loads where every row has already been validated, multi-row VALUES is the default. For untrusted input where you want to localize a parse failure to a single row, one-statement-per-row is the safer default. The batch size is exposed as a selector — the canonical pattern is 100 to 500 rows per statement for staging, and 1 row per statement for production loads on untrusted input.

## CREATE TABLE emission and the schema-bundled payload

A optional selector emits a `CREATE TABLE IF NOT EXISTS orders (...)` block ahead of the INSERTs, with column types copied from the inference pass. This is the difference between a hand-typed CREATE TABLE that drifts from the inferred columns over time, and a self-contained payload that runs identically on a fresh database or an existing schema.

The most common bug this prevents is column-order drift: a hand-written CREATE TABLE adds `created_at` at position 8, while the hand-written INSERT emits it at position 5 because the CSV dialect reordered it. The schema bundle ties the two together and re-emits them as one atomic payload.

## Worked example: a 12-row orders CSV to four dialects in 4 statements

A minimal orders file with id, name, amount, and created_at columns produces four different outputs from one source. Postgres gets `INSERT INTO "orders" ("id", "name", "amount", "created_at") VALUES (1, 'Alice', 99.50, '2026-09-13'), (2, 'Bob', NULL, '2026-09-13');` with `ON CONFLICT (id) DO NOTHING`. MySQL gets the same VALUES list with backtick-quoted identifiers and an `ON DUPLICATE KEY UPDATE` clause. SQLite emits ANSI double-quotes and `INSERT OR IGNORE`. SQL Server emits brackets and a `MERGE` example in a comment block. All four share the same inferred schema: BIGINT, TEXT, DOUBLE, TIMESTAMP.

The load it directly handles is the [CSV Flavor to SQL INSERT Emitter](https://elysiatools.com/en/tools/csv-flavor-to-sql-insert-emitter) — paste a CSV in, pick the dialect, set the conflict mode, and ship the resulting script to the destination database. For related work in the same conversion family, the [xlsx-sql-insert-generator](https://elysiatools.com/en/tools/xlsx-sql-insert-generator) covers the Excel workbook case, and the broader tool index is at [elysiatools.com](https://elysiatools.com/en/tools).

The hand-rolled equivalent of this emitter is roughly 300 lines of dialect-specific code per target, and the bug count is roughly proportional to the number of times it has been copy-pasted across an ETL codebase. A single typed CSV in, four correct dialects out, and idempotent re-runs by default — that is the whole pitch.