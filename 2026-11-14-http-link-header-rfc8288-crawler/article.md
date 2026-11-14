---
title: Your Link Header Parses. Your Crawler Stops Before Page 2.
---

Four link relations, zero warnings, one page fetched. That is what a GitHub-style pagination header looks like to a parser that implements RFC 8288 Appendix B correctly — but it is also exactly what a crawler that never reaches page two looks like. A Link header is not a field you read. It is an instruction you execute, and the parser is far more forgiving than the crawler.

## A clean parse is not a correct chain

I pasted a GitHub-style pagination header into the [Link header analyser](https://elysiatools.com/en/tools/http-link-header-rfc8288-parser-and-pagination-crawler-preview) with a local API base URL. According to the report, 4 links parsed, the pagination set was complete, 0 warnings fired, and the crawl chain measured 1 page.

Three of those numbers say ship it. The fourth says the crawler stopped before it started, and it is the only one that describes what a client does.

Two numbers measure two different things: `linkCount` counts what your header advertises, and `chainLength` counts what a crawler reaches when it follows `rel="next"` from one response to the next. A header can score perfectly on the first and reach nothing on the second, because parsing is a per-response act and crawling is a sequence. The tool reports both because neither substitutes for the other, and an audit that only asks whether the header parses will pass headers no client can walk.

## Each response is read in the context of the page before it

This is the detail that quietly breaks real crawlers, and it is a design decision in the spec, not a bug.

A relative target like `</api/items?page=2>` is a URI-reference. RFC 3986 §5.2 resolves it against a context URL — and in the crawl simulation, page 2's context is the resolved `rel="next"` of page 1, not the base URL you typed into the form. The base URL sets the context for one line only: Page 1 reads your base, and each line after it reads the previous page's `next`.

For example, a three-line paste resolves like this: Page 1's context is your base, page 1's `next` becomes page 2's context, and page 2's header is then read against page 2's address. Paste those same three headers in reverse order and each relative target lands somewhere else, with no warning and no error. The crawl table prints the context URL in its own column for exactly this reason, so read that column before the resolved links.

The corollary is that a response body's own `<base>` element never enters the calculation. RFC 8288 links are resolved with `URL()` semantics against the response URL, which is why an API that works in a browser can break in a crawler that never parses HTML at all.

## Two rel="next" values is a silent coin flip

Appendix B is a deliberately permissive parser, and permissive parsers convert typos into routing decisions.

Write `; rel="next"; rel="last"` and the second `rel` is ignored. The parse succeeds, the first relation wins, and `last` disappears with no error. The analyser checks the case that hurts most — a response carrying more than one `rel="next"` — and reports that crawlers follow only the first. Two competing next links are not a tie. They force a choice, and your client may have made a different one than you did.

The same permissiveness shows up in an empty reference. A bare `<>` resolves to the response URL with its fragment stripped, per RFC 3986 §5.2.2, so a link that looks truncated can be perfectly valid and point at the page you are already on. That is the shape a pagination loop is built out of, and it is the one clue a naive audit never sees.

## A complete pagination set is a property of page one

The analyser's `paginationComplete` flag asks one narrow question: does the first response expose all four of `first`, `prev`, `next`, and `last`? It reads the relation set of line 1 only.

That matters when you are auditing a paged API, because completeness is an entry-point claim. Page 3 carrying a tidy `first/prev/next/last` set proves nothing about page 1, and a client that discovers pagination by reading the first page will never see it. If the badge is green, your entry point advertises a full navigation set. If it is red and page 1 still has a working `next`, you have a walkable chain with an incomplete map — two different defects that need two different fixes. I observed exactly that split in the first test header: A complete set on line 1, and a chain that ended after one page because there was no second response to walk.

## The permissive parser shrugs in five specific places

The report's warning panel is where the spec's advisory language becomes something you can act on, and it will show you which of the five you hit. Five checks carry most of the value:

<ul>
<li><strong>Non-ASCII targets.</strong> A target with raw international characters is an IRI, and Link header targets must be URI-encoded per RFC 3986. Percent-encode it or the client decides whether to guess.</li>
<li><strong>Unquoted values containing whitespace.</strong> A parameter value with a space that is not wrapped in quotes is technically invalid. Senders must quote values that are not valid tokens, and the parser only tolerates it.</li>
<li><strong>Extension relation types that are not absolute URIs.</strong> The registry the analyser checks against holds 133 IANA-registered relation names, which is why `rel="previous"` is understood and `rel="prev-page"` is not. A private relation must look like `acme:widget` — a bare custom word is neither registered nor a URI, so it lands in the warning list. The rest of the header-focused tooling sits under the same [Network catalogue](https://elysiatools.com/en/categories/network).</li>
<li><strong>The deprecated rev parameter.</strong> RFC 8288 §3.3 retired it. The reverse relation belongs in a dedicated rel type, and `rev` now ships as a plain attribute that clients may ignore.</li>
<li><strong>Anchor parameters.</strong> A link carrying `anchor` is interpreted in the context of the anchor, not the response URL, and §3.2 permits applications to ignore such links entirely. If your pagination target sits on a link with an anchor, you have made the most important relation in your header optional.</li>
</ul>

## Preload without as is a priority request you cannot make

Resource hints share the header with pagination, and they fail differently: a hint does not break a crawl, it never earns the optimisation you asked for.

`rel="preload"` without an `as` parameter triggers a warning, because the browser cannot classify the fetch and cannot prioritise it against the resources it already knows about. Twelve destinations are valid: Audio, document, embed, fetch, font, image, object, script, style, track, video, worker. A `type` parameter is expected to look like a MIME type unless `as="fetch"`, otherwise the preload can be discarded quietly. For instance, a font preload missing its `crossorigin` attribute can fetch the file twice.

The analyser tracks six hint relations — preload, prefetch, preconnect, dns-prefetch, modulepreload and prerender — and prints a table of `as`, `type`, `crossorigin` and `fetchpriority` per hint. In the three-page crawl example the final response carries a single preload for a hashed script, which raises the hint count to 1 and leaves the documentation of that asset exactly where a human can find it.

## Termination is the only diagnostic that means anything

A chain report is only useful if it tells you why the walk stopped, because the termination state changes what you fix. The tool names seven termination states, and four of them are the ones you will meet:

<ul>
<li><strong>no-next</strong> — a response has no rel="next", so pagination ends. Usually correct; in the three-page example, page 3 exposes a preload and nothing else, and the crawl terminates there with a chain length of 3.</li>
<li><strong>cycle</strong> — rel="next" points back at a URL already visited. The visited set is seeded with the base URL and compared with fragments stripped, so an appended #top does not hide the loop, and a next that points at your base is a cycle on page 1.</li>
<li><strong>end</strong> — all supplied responses were walked and the chain would continue at the last resolved URL. This is the one that tells you your paste set is incomplete, not your API.</li>
<li><strong>depth</strong> — the cap was reached. The default is 10 and the input is clamped between 1 and 100, and the state only fires when you supplied more responses than the cap allows. Give it exactly ten lines and you get end, which reads like progress.</li>
</ul>

The remaining three are input problems, not API problems: Needs-base, no-input and no-base. Needs-base is the honest one — a relative `rel="next"` with no base URL cannot be simulated at all, so the tool reports that instead of inventing a URL.

## Paste the headers, then read the chain

The workflow that works is small. Paste one response per line — a leading `Link:` prefix is stripped automatically, so a `curl -sI` dump goes in as-is — then set the base URL, then read the chain table before the link table. When a warning appears, replace the duplicate `next` with one link, confirm the four-relation set sits on line 1, then check each hint's `as` value. The [analyser](https://elysiatools.com/en/tools/http-link-header-rfc8288-parser-and-pagination-crawler-preview) accepts the whole dump at once, so a four-hour debugging session becomes one paste. For example, the reported warning count drops to zero as soon as those three things hold. Explore more tools at [elysiatools.com](https://elysiatools.com/en/tools).

One honest limit: this is a reference implementation of the walk, and no major crawler implements RFC 8288 exactly. Googlebot, Bingbot and your own HTTP client each bring their own tolerance for duplicate relations and relative targets. What the test proves is whether your header is internally consistent — whether the page you claim is next is the page your own links resolve to — not whether a specific crawler will behave the way you hope. The metadata numbers are the data worth diffing between two API releases, because a chain length that improves from 1 to 5 is progress you can measure.

I used to check that the header parsed. Now I check what the chain does after the first page, because that is the part a reader never sees and the part where a correct header and a broken crawl look identical. If your pagination crawler stopped at page one, would your Link header tell you why?
