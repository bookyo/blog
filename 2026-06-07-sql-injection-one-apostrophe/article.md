---
title: Why One Apostrophe Can Wipe Out Your Entire Database
---

A junior developer pastes a login form into production. A user types `' OR '1'='1` into the username field. By the time anyone notices, every user record in the database has been exfiltrated — passwords, emails, addresses, all of it. This is not a hypothetical. The first documented SQL injection attack dates back to 1998, and 27 years later it still appears in the OWASP Top 10. The pattern has not changed; only the methods of detection have.

The first line of defense is not a framework or an ORM. It is the moment you read a payload and think: *this string should not be in a username field*. A tool built for that exact recognition step can save a deployment — and a database — from the simplest, oldest attack on the open web.

## How a 7-character payload becomes a full table dump

The most common SQL injection is also the most elegant. A login form expects a username and password, and the backend runs something like:

```sql
SELECT * FROM users WHERE username = 'INPUT' AND password = 'HASH'
```

When a user types `' OR '1'='1` into the username box, the final query becomes:

```sql
SELECT * FROM users WHERE username = '' OR '1'='1' AND password = 'HASH'
```

The first part of the WHERE clause — `username = ''` — is false for any real user. But the OR clause is **always true**: `'1'='1'` evaluates identically on both sides, so the database returns the first row in the table. In most login flows, that first row is the admin account. The attacker is now logged in as the highest-privileged user in the system.

The `' OR '1'='1` payload is just 11 characters. The catastrophic outcomes it produces — full database reads, credential theft, in some cases total server takeover — are why SQL injection has been the number one web vulnerability for over two decades.

## The 5 families of injection every detector needs to know

Modern injection patterns fall into roughly five families, each with its own signature:

**Tautology attacks** rely on conditions that are always true. `' OR 1=1--`, `' OR 'a'='a`, and the original `' OR '1'='1` are all tautologies. The trailing `--` (or `#` for MySQL, `/*...*/` for block comments) cuts off the rest of the query so the malicious clause is the only thing the database evaluates.

**UNION-based attacks** append a second `SELECT` statement to the original query, allowing the attacker to pull arbitrary data from any table in the same database. `' UNION SELECT username, password FROM users--` is a textbook example. Defenders can spot these by looking for the word `UNION` followed by `SELECT` or `ALL SELECT`.

**Stacked-query attacks** try to chain a second statement onto the first using semicolons: `'; DROP TABLE users;--`. Most modern database drivers disallow stacked queries, but the patterns still appear in legacy code, in admin tools, and in the payloads attackers try first to map the system's defenses.

**Time-based blind attacks** don't return visible data at all. Instead, they trigger a measurable delay: `'; WAITFOR DELAY '00:00:05'--` (SQL Server) or `'; SELECT SLEEP(5)--` (MySQL). If the response takes five seconds longer, the attacker knows the injection succeeded — even if the page shows nothing useful. The signatures `WAITFOR DELAY` and `SLEEP(` are reliable indicators.

**Boolean-based blind attacks** probe the database with conditional logic: `' AND 1=1--` versus `' AND 1=2--`. The first returns the page normally, the second returns a different page or an error. By iterating over conditions, the attacker reconstructs data one bit at a time. Patterns like `AND 1=1` and `AND 1=2` are the tell.

A detector that recognizes all five families — not just tautologies — catches the attacks that show up in real incident reports.

## Why a quick scan misses the dangerous half

The trade-off in any detector is speed versus coverage. A quick scan looks for the obvious patterns: bare apostrophes followed by SQL keywords, the most common tautologies, a handful of comment styles. It runs in milliseconds and catches the low-effort probes that automated scanners fire off first.

A full scan runs a deeper pattern set — stacked queries, hex-encoded payloads (`0x73656C656374`), the full UNION family, time-based functions, and conditional errors. It is what you run on a code review, a log audit, or any time a user-submitted value is about to be logged or stored.

The difference is not just about more patterns. The full scan also reports each match with its line number and the specific pattern that triggered — so the reviewer can see *why* the string was flagged, not just that it was. That detail is what turns a detection into a fix.

## Reading a finding, not just a count

A detector that returns "1 match found" is barely better than no detector at all. The useful output shows each finding individually: the exact line of code or log entry, the substring that matched, and the pattern family. When the report says `line 47: ' OR 1=1-- — pattern: tautology`, the developer knows where to look and what to fix.

The [SQL Injection Detector](https://elysiatools.com/en/tools/sql-injection-detector) at Elysia Tools produces exactly that output — line numbers, matched substrings, and the pattern that fired. For code review and log forensics, this is the difference between a 30-second triage and a 30-minute hunt.

## The honest limit of pattern matching

A regex-based detector catches the payloads that look like payloads. It does not catch a clever attacker who splits a keyword with a comment, uses Unicode lookalikes, or hides the injection inside a binary blob that the database decodes at execution time. Those are caught by parameterized queries, by database firewalls, and by reviews of the data flow — not by string matching.

But every modern attack still begins with a string. The trick is recognizing it before it reaches the database. That is what a detector is for.

## The first line of code that should be in any review

If you are reviewing a login form, a search box, or any endpoint that takes user input, run the inputs through a detector before you run the deploy. The cost is seconds. The cost of skipping it is a database.

For a working set of detection patterns to use as a starting point, the [SQL Injection Samples](https://elysiatools.com/en/samples/sql-injections) collection includes classic tautologies, UNION chains, blind-injection probes, and time-based payloads at three difficulty levels. Paste them into your own inputs during a review and see what your detector catches — and what it misses.

The fix for SQL injection has been known for 20 years: parameterized queries, escaped inputs, ORMs that do the work for you. The detection step is faster than the fix, and it belongs before the fix, not after. A tool that flags the payload is not a substitute for safe code — but it is the moment you find out whether your safe code is, in fact, safe. For a wider set of defenders, including log auditors and security engineers, browse more [security tools at Elysia Tools](https://elysiatools.com/en/tools).

The next breach will not start with a novel payload. It will start with a string your team has seen a hundred times before — a string that someone, this time, did not look at closely enough.
