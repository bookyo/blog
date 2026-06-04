---
title: "Why Every Modern API Hides a Tiny Contract in Its JSON"
description: "JSON Schema looks like overhead. Then one of your clients sends a number where a string was promised, and everything breaks at 2am. Here's the validation grammar that prevents that."
---

A 2 a.m. page lights up your phone. A client integration has been failing for nine minutes. You open the logs, and the failing request is a JSON document with a perfectly innocent-looking `"price": "$49.99"` where the schema — which you wrote — asked for a number. A string slipped into a number field, a check fired, a webhook cascaded, and the dashboard that the customer's CEO watches at 8 a.m. is now full of red. The bug is not in the handler. The bug is that you trusted the data before you read the contract.

JSON Schema exists to make that trust earned. It is a separate, machine-checkable grammar that sits next to your data and refuses anything that does not match. Tools like the [JSON Schema Validator](https://elysiatools.com/en/tools/json-schema-validator) run that grammar in milliseconds, before your handler executes, and they turn that 2 a.m. page into a 400 the client can read and fix.

JSON looked, when it arrived in the early 2000s, like a syntax with no opinions. Curly braces, square brackets, commas, and a handful of literal values — `null`, `true`, `false`, and a number. That was the whole language. No required fields. No types. No rules about whether a key was a number, a string, or a string that *happened* to look like a number. JSON trusted you. JSON was wrong to trust you.

By 2009, when the first draft of **JSON Schema** circulated, every team that shipped an API had learned the same lesson: a free-form document at the boundary of two systems is not data. It is a *promise* in clothing, and promises break. The schema — originally proposed by Kris Zyp, refined through drafts 03, 04, 06, 07, 2019-09, 2020-12 — was a way to write that promise down. Not in prose. Not in a wiki page nobody reads. In a strict, machine-checkable grammar that sits next to the data and refuses anything that does not match.

## What the schema actually does

A JSON Schema is itself a JSON document. Its job is to describe another JSON document: which keys are required, what types each value must have, what range of numbers is acceptable, which string patterns are valid, whether a value is allowed to be `null`. The current draft, **2020-12**, has been the stable recommendation since late 2020. Older drafts are still everywhere in the wild, which is why most validators — including the [Ajv](https://ajv.js.org/)-based engine behind the [JSON Schema Validator](https://elysiatools.com/en/tools/json-schema-validator) — accept `schemaDraft` as an explicit input rather than guessing.

The simplest schema does almost nothing: `{}` accepts any JSON value, including the empty object. That is a *trivially true* schema, and it is also the one most teams accidentally write. The interesting schemas do four things at once: they declare the *type* of the root value, they list the *required* keys for an object, they constrain the *type* of each value, and they add a *format* hint that goes beyond the JSON type system (an `email` format, a `uri` format, a `date-time` format). Ajv with `ajv-formats` activated — which is exactly the configuration this tool uses — enforces those formats as if they were types.

A real example. Suppose your API accepts a signup payload. The schema is the file you wish your clients had read before posting. It is small, it is precise, and it is the single source of truth for what `POST /signup` will and will not accept:

```json
{
  "type": "object",
  "required": ["email", "password", "plan"],
  "properties": {
    "email":    { "type": "string", "format": "email" },
    "password": { "type": "string", "minLength": 12 },
    "plan":     { "enum": ["free", "pro", "team"] },
    "age":      { "type": "integer", "minimum": 13 }
  },
  "additionalProperties": false
}
```

A 19-year-old posting a `plan: "enterprise"` does not get a friendly 500. They get a 400. The 400 explains, in order, that `plan` was not in the enum, that `email` was missing a top-level domain, that no other properties are allowed. The handler never runs. The database never gets called. The 2 a.m. page does not happen.

## Why `additionalProperties: false` is the most important line in the file

That last line — `additionalProperties: false` — is the one most teams leave out, and it is the one that saves the most incidents. Without it, a client can send `{ "email": "...", "password": "...", "plan": "free", "isAdmin": true }` and your handler has to decide what to do with `isAdmin`. With it, the schema rejects the request at the door, and your handler can trust the rest of the document. The reason this matters more than the type checks is that *untyped extras are the entry point for privilege escalation bugs*. A client who can set fields you did not know existed is a client who has found an undocumented API surface. JSON Schema with `additionalProperties: false` closes that surface.

## Why types alone are not enough

This is the part that surprises people who have only seen JSON Schema used for type checking. JSON Schema can express: regex patterns on strings (`"pattern": "^[A-Z]{2}\\d{4}$"`), numeric ranges (`"exclusiveMinimum": 0`), array length (`"minItems": 1, "maxItems": 10`), array item types (`"items": { "type": "string" }`), and oneOf/anyOf/allOf composition. The 2020-12 draft added `prefixItems` for tuple-typed arrays, which is the kind of detail that makes the difference between a schema that mostly works and a schema that survives contact with your mobile team's edge cases. None of these are types. They are *constraints on values*, and the union of all of them is what makes the contract enforceable.

## What a validation error actually looks like

When validation fails, Ajv returns a structured error per failure. The tool surfaces these in plain text, prefixed with the `instancePath` (the JSON Pointer to the bad value) and the validation keyword that fired (e.g. `required`, `enum`, `type`, `format`). A failure for a missing required field looks like `/email must have required property 'email'`. A wrong-type error looks like `/age must be integer`. A failed format check looks like `/email must match format "email"`. The path is the *line number* of the contract. The keyword is the *rule* that was violated. Together they make a 400 response that a developer can fix without reading the docs. Try the [JSON Schema Validator](https://elysiatools.com/en/tools/json-schema-validator) against a deliberately broken payload and the output reads like a checklist of what to change.

## Where to put the validation in your stack

There are three places, and the right answer is all three. The first is at the API gateway — a request that does not match the schema never reaches your service. The second is inside the service itself, as a guard at the top of the handler. The third is in your tests, where a fixture library of valid and invalid payloads is replayed against the schema on every commit. This last one is the cheapest insurance you will ever buy. A schema that is not tested is a schema that has rotted. The validator tool is useful for all three layers because it accepts the schema and the data as plain text inputs and returns a structured pass/fail plus a list of errors, which is exactly what your test framework wants to assert against.

## The contract is the test

The reason this matters — and the reason the schema has survived a dozen drafts and a 20-year span of API styles — is that the schema *is* the test. There is no separate specification document. There is no separate test suite. There is no separate stub server. The schema is the only file the producer and the consumer have to agree on, and once they do, every other piece of the system can be generated from it: client types in TypeScript, server types in Go, documentation in OpenAPI, fake data for local development, contract tests for CI. The schema is a small file. It is the seed of an entire system.

If your API still uses hand-rolled validation — a long chain of `if` statements checking field by field, each one slightly different, each one missing an edge case — the path forward is shorter than you think. Pick a draft. Pick a tool. Write the schema once.

Then the next time a client sends the wrong type, you will not be debugging at 2 a.m. You will be reading a 400 that tells you exactly which line of which contract was broken. That is the whole game. The schema is not overhead. It is the line between systems that hold up and systems that fail in production. Write the contract down. Reject the rest. Sleep through the night.
