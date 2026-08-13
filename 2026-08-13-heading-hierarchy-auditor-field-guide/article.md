---
slug: heading-hierarchy-auditor-field-guide-2026-08-13
date_gmt: 2026-08-13T01:34:47
tool_id: heading-hierarchy-auditor
---

<strong>The right way to think about heading hierarchy is that visual weight is a side effect, not the goal.</strong> Search engines, screen readers, and accessibility audits all read your document in a tree, not a column. The Heading Hierarchy Auditor at [Elysia Tools](https://elysiatools.com/en/tools/heading-hierarchy-auditor) inspects that tree: it flags skipped levels, multiple h1 nodes, likely style-only heading abuse, and drift between the main h1 and your document title. This field guide walks through what the tool reports, how to read the report, and how to translate the report into fixes that survive real publishing pipelines.

## What the Heading Hierarchy Auditor actually checks

The auditor accepts two input modes. Paste raw HTML and you get a deterministic parse of the markup; provide a page URL and the tool fetches the rendered document and runs the same checks on whatever the browser sees. Both modes walk the h1 through h6 nodes in source order, build a hierarchy tree, then run five pattern detectors against that tree:

<ul>
<li>Multiple h1 nodes — a page is supposed to have exactly one top-level heading per WAI-ARIA and HTML5 outlines</li>
<li>Skipped levels — jumping from h1 to h3 without an h2 in between breaks the document outline</li>
<li>Likely style-only headings — h2 or h3 used purely for visual size, with no content section beneath it</li>
<li>Empty headings — nodes with no text content, usually a CMS artifact</li>
<li>h1 vs title drift — the primary heading text does not match the <code>&lt;title&gt;</code> or <code>og:title</code></li>
</ul>

Two toggles reshape the report. <strong>Compare With Metadata Titles</strong> cross-references the main h1 against your document title and Open Graph title; <strong>Show Fix Suggestions</strong> appends a suggested replacement level or replacement strategy to each flagged node. Both are off by default because they make the report noisier on a quick scan.

## Reading the hierarchy tree output

The first section of every report is a tree view that mirrors the rendered outline. Each node carries its level, its text content, and a severity chip:

<ul>
<li>Green: clean node, no findings</li>
<li>Amber: minor issue (empty heading, style-only marker)</li>
<li>Red: structural issue (multiple h1, skipped level)</li>
</ul>

Work top to bottom. A red chip at the top of the tree is almost always the root cause of every red chip below it, because skipping levels cascades. Fix the topmost red node first, re-run the audit, and the rest of the tree tends to fall in line. The [Heading Hierarchy Auditor](https://elysiatools.com/en/tools/heading-hierarchy-auditor) re-runs are free and idempotent, so use that loop aggressively.

## Common patterns the report catches

Four patterns account for the bulk of real findings across the wild web. Knowing them lets you predict the report before you run it:

<ul>
<li>The CMS heading picker — content editors reach for h3 when they want larger text, regardless of section depth. Every CMS-driven blog has at least one h3 floating without a parent h2.</li>
<li>The SEO h1 — designers and SEO plugins both inject an h1 in the page chrome (logo, page title) that the editor never sees. Two h1s, no warning, instant audit fail.</li>
<li>The accessibility h1 — a hero banner with <code>&lt;h1&gt;Welcome&lt;/h1&gt;</code> at the top of every page. The h1 is decorative, but screen readers still announce it before the article title.</li>
<li>The orphaned h2 — an h2 that ends a section with no content under it, often a leftover from a CMS split.</li>
</ul>

Pair this with a broader accessibility scan via the [Accessibility Checker](https://elysiatools.com/en/tools/accessibility-checker) — heading hierarchy is one slice of WCAG, but the audit catches patterns that the broader checker attributes to other rules.

## How the report translates to fixes

The Show Fix Suggestions toggle produces a fix table that pairs each flagged node with a recommended action. Three fix recipes cover most cases:

<ul>
<li><strong>Demote a style-only heading</strong> — change the h3 to a styled <code>&lt;p&gt;</code> (or use a CSS class). The hierarchy becomes cleaner and the visual weight stays.</li>
<li><strong>Promote an orphaned parent</strong> — if you have a stray h3 followed by h4s but no h2, lift the surrounding <code>&lt;section&gt;</code> and rename the orphan to an h2.</li>
<li><strong>Remove the decorative h1</strong> — wrap a hero h1 in <code>aria-hidden="true"</code> if it is purely visual, or move it to a <code>&lt;div role="heading" aria-level="1"&gt;</code> so it does not compete with the document h1 in the accessibility tree.</li>
</ul>

For the SEO h1 case, the fix is almost always structural rather than stylistic: your page template should not be injecting an h1 in the chrome. The audit gives you the evidence to push back on the template.

## When to skip the report

There are three situations where the audit's findings are not worth acting on:

<ul>
<li>Single-page apps with virtual DOMs — the auditor sees whatever HTML you paste or fetch. If your headings are rendered client-side from JavaScript, you need a pre-render snapshot to get a real read.</li>
<li>Email templates and PDF exports — heading rules in WCAG target web documents. Use the audit on the web version of the same content.</li>
<li>Legacy pages under a deprecation notice — if the page is marked for retirement, do not invest in the fix; redirect it and move on.</li>
</ul>

The auditor is a guidance tool, not a policy enforcer. Use it as input to the migration plan rather than as a checklist.

## Pairing with the rest of an SEO workflow

Heading hierarchy is one input to on-page SEO and accessibility, not the whole picture. Three other tools at [Elysia Tools](https://elysiatools.com/en/tools) complement it without overlap:

<ul>
<li>[Accessibility Checker](https://elysiatools.com/en/tools/accessibility-checker) — broader WCAG scan; covers heading-adjacent rules like landmark structure, color contrast, and form labels</li>
<li>Heading Hierarchy Auditor — what we are covering now</li>
<li>Heading Hierarchy Auditor on a URL — same tool, URL input mode; useful for spot-checking competitor pages or partner sites that link to yours</li>
</ul>

The heading audit is the cheapest of the three to run, so make it the first gate in any content-quality pipeline. Anything that fails it should not move on to the slower audits.

## Putting it together

Run the [Heading Hierarchy Auditor](https://elysiatools.com/en/tools/heading-hierarchy-auditor) on your top ten pages by traffic, then sort the findings by severity. The top three findings almost always share a root cause — a CMS template, a hero pattern, an SEO plugin. Fix that root cause, and you have fixed the audit for the whole site at once.

If you only have time for one habit, run the audit after every theme change. Theme updates are the single most common cause of new heading issues, because they reset the chrome (logo h1, hero h1, sidebar h2s) without warning content editors. Five minutes of audit after every theme update is worth more than ten hours of post-launch cleanup.

## Where to look next

Two follow-up reads extend what this guide covers. The first is the [Accessibility Checker](https://elysiatools.com/en/tools/accessibility-checker) for the rest of the WCAG surface area; the second is the Heading Hierarchy Auditor's URL-input mode for spot-checking any page without copy-pasting markup. Both live at [elysiatools.com/en/tools](https://elysiatools.com/en/tools).