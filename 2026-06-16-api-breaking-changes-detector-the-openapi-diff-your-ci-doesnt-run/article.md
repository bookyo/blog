---
title: "The OpenAPI Diff Your CI Does Not Run: Why Two Specs Can Look Compatible and Still Break Every Client"
slug: api-breaking-changes-detector-the-openapi-diff-your-ci-doesnt-run
date: 2026-06-16T15:47:00
tool: api-breaking-changes-detector-migration-planner
category: Development
---

The breaking change you ship to production is almost never the one a human reviews. It is the one a generated SDK picks up automatically. It is the one a downstream team re-generated at midnight and merged without reading the changelog. It is the one that looked like a tightening — `required: true` added to a request field, a `default` value flipped, a response property renamed, a `minimum` increased from 0 to 1 — and looked, on paper, like a reasonable thing for a backend team to do. The PR passed code review. The CI pipeline said green. The OpenAPI spec linter was happy. But somewhere, a client that was sending `{ "name": "Alice" }` is now sending a payload the new server rejects with a 422 and an error message that names a field the client does not know it has to send.

A breaking-change detector is the smallest piece of machinery that catches the structural change before it ships. You hand it the old spec and the new spec. It walks every path, every method, every parameter, every request body, every response code, and tells you which contract changed and which side of the contract is now unhappy. That is the whole job. The reason it matters is that a generated SDK, a typed client, and a contract test are all downstream consumers of the spec, and all of them silently inherit every change the spec carries — including the ones the spec author did not mean to be breaking.

If you only do one thing after reading this, run the [API Breaking Changes Detector](https://elysiatools.com/en/tools/api-breaking-changes-detector-migration-planner) against the last two versions of your own OpenAPI spec and read the report. You will find at least one change that "looks fine" and is in fact a tightening that forces every client to update. Every team I have watched do this exercise has discovered either a request field that quietly became required, a response property that was renamed in place, or a default value that flipped semantics for the long tail of clients that do not pass it explicitly. The cost of finding that out after release is a sev-2 incident. The cost of finding it out at PR time is a single line in the bot comment.

---

## The CI that says green and the CI that should say red

Most teams run a spec linter in CI. The linter checks that the OpenAPI document parses, that the references resolve, that every operation has a 2xx and a 4xx response, that the security schemes are declared, and that the operation IDs are unique. This is good. It is not the same as a breaking-change check.

A linter compares one document against a static rule set. A breaking-change detector compares two documents against each other. The information the linter has access to — "is this a valid OpenAPI document" — is a single-document question. The information the breaking-change detector needs — "is the second document compatible with what the first document promised" — is a relational question, and it cannot be answered without both sides.

This is the gap that ships breaking changes. The linter is happy because the new spec is structurally valid. The review is happy because the diff in the PR is small. The CI is green because the contract tests against the staging environment pass. But the contract tests are running against a server that has been updated to the new spec. They are not running against a client that was generated from the old spec — which is the one that is going to break in production, six hours after release, when a downstream team's nightly regen picks up the change and pushes a typed client that no longer matches what its callers send.

The fix is not a better linter. The fix is a second pass in CI that has access to both spec versions and is allowed to fail the build. The detector can run as a post-merge job on the spec repo, a pre-merge check on the spec PR, a pre-release gate on the SDK repo, or a scheduled job that diffs the deployed spec against the previous deploy. The exact placement matters less than the fact that the job runs at all.

## The four shapes of a breaking change

Most breaking changes in OpenAPI specs fall into one of four shapes. None of them are caught by a single-document linter. All of them are caught by a two-document diff.

**A required field appears.** The request schema adds a property and marks it `required: true`. The server, on the next deploy, starts rejecting requests that omit it. Every client that was sending a payload without that field is now broken. The new spec is valid. The change is intentional. The breakage is silent until a 422 lands.

**A response field disappears.** The response schema removes a property that the old spec declared. Any client that was reading that field is now reading `undefined`. Typed clients in TypeScript or Go see the field as missing from the type definition. The generated client compiles. The runtime behavior is "the field I expect is not there." This is the most insidious shape because the change is invisible in the spec diff — a removed line in a YAML file — and visible only when the client tries to read the field.

**A type tightens.** A field that was `type: integer` becomes `type: string` and a format annotation. A field that was a free-form `string` becomes an `enum` with two values. A `minimum` increases. A `maxLength` decreases. A `pattern` is added. The new spec is more strict. The new server now rejects payloads the old server accepted. The breakage is conditional on which subset of the old payload space the new spec no longer accepts.

**An endpoint disappears.** A path is removed. A method is removed. A path is renamed. A path is moved from one server to another. The endpoint is gone. Any client that was calling it is now hitting a 404. The new spec does not declare the path, so the SDK regen produces a client that does not have the method. The client compile fails — that part is loud. The clients that have not been regenerated yet are the ones that break in production.

A breaking-change detector classifies each diff into one of these shapes, names the field, names the path, and tags the severity. The [API Breaking Changes Detector](https://elysiatools.com/en/tools/api-breaking-changes-detector-migration-planner) walks the spec, finds these patterns, and reports them grouped by impact.

## The case the detector saves

Take a real worked example. The spec for `POST /users` declares a request body with one optional property:

```yaml
paths:
  /users:
    post:
      requestBody:
        required: false
        content:
          application/json:
            schema:
              type: object
              properties:
                name: { type: string }
      responses:
        "200":
          description: ok
          content:
            application/json:
              schema:
                type: object
                properties:
                  id: { type: string }
                  name: { type: string }
```

The new spec tightens this. `requestBody.required` flips from `false` to `true`. The schema adds a `role` property and marks both `name` and `role` as required. The response schema removes the `name` property.

```yaml
paths:
  /users:
    post:
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [name, role]
              properties:
                name: { type: string }
                role: { type: string }
      responses:
        "200":
          description: ok
          content:
            application/json:
              schema:
                type: object
                properties:
                  id: { type: string }
```

Read those two specs side by side. Both are valid OpenAPI. Both pass the linter. The diff in the PR is six lines. None of the changes is a typo. The author intended all of them. And every client that was calling `POST /users` with `{ "name": "Alice" }` is now broken in three different ways: the request body is now required, the new required field `role` is missing, and the response no longer includes the `name` field the client was reading.

A breaking-change detector flags all three. The request tightening is a "request contract tightened" finding with a client impact grade. The new required field is a "new required field" finding. The response field removal is a "response field removed" finding. Each finding cites the path, the method, the field, the old shape, the new shape, and a migration strategy.

The migration strategy is the part that turns the detector from a critic into a tool. A detector that only says "you broke the contract" is something the team will silence. A detector that says "you broke the contract; here is the compatibility shim, here is the deprecation path, here is the SDK regeneration command, here is the migration window" is something the team will keep.

## What the detector is not

A breaking-change detector does not check whether the server behaves correctly. It does not catch a backend that ignores the schema and accepts a payload the spec rejects. It does not catch a backend that returns a 200 with an error body. It does not catch race conditions in the handler. It does not substitute for contract tests, integration tests, or end-to-end tests. It checks the structural contract between two OpenAPI documents and nothing else.

This is the scope that makes it fast and embeddable. The detector runs in seconds, in CI, without a deployed environment, without a test database, without a network round trip. The output is a static report — a list of findings, each with a path, a field, a severity, and a migration note. The report is small enough to read in a PR review. The report is structured enough to gate a release.

The decision to keep the detector offline and structural is the same decision that makes the detector worth running on every PR. You can run it on any commit, any branch, any pull request, without a staging environment, without rate limits, and without the false confidence that comes from a "valid" verdict when the API is in fact unreachable. The detector is the contract check, not the behavior check. The contract check is the part that catches spec drift before it becomes a client outage.

## Where to put it in the pipeline

The detector fits naturally in three places. The first is a pre-merge check on the spec repository — every PR that changes the spec runs the detector against the merged result and the previous main, and the bot comments with the report. The second is a post-merge job that runs on every commit to main, archives the report, and alerts if the severity count crosses a threshold. The third is a pre-release gate in the SDK repository — before the SDK regen job publishes a new version, the detector diffs the old published spec against the new spec, and the release is blocked if the report is not empty.

The exact placement is less important than the fact that the job runs at all. The shape of a breaking change is structural, and the structural check is fast. The cost of running it is small. The cost of not running it is the sev-2 incident that ships at 4 p.m. on a Friday and rolls into a sev-1 by Monday morning.

A spec is a contract. A contract that changes without a record is not a contract — it is a guess. The detector is the record. It is small. It is offline. It is the smallest piece of machinery that turns "we think this is compatible" into "we know what changed and who needs to update." That is the whole job. The reason it matters is that every typed client, every generated SDK, and every contract test is downstream of the spec, and all of them silently inherit every change the spec carries.

Explore more tools at [Elysia Tools](https://elysiatools.com/en/tools).