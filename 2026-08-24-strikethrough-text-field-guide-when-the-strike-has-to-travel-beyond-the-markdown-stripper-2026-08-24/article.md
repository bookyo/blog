<strong>Strike-through that survives the chat app's markdown stripper.</strong> Strikethrough text is a small Unicode trick that punches above its weight. The tool inserts the combining mark `U+0336` after every character of your input, which the renderer paints as a horizontal line directly through the previous glyph. The result looks like `~~strikethrough~~`, but it is just characters — no markdown processor, no rich-text engine, no `<s>` tag required.

The plain-text trick matters because most platforms silently strip formatting on paste. Slack removes markdown asterisks on quick-edit; many chat clients rewrite double-tilde spans; CMS sanitizers drop `<s>` tags wholesale. A pasted `~~cancelled~~` becomes `cancelled` and the visual cue is gone. The Unicode combining-mark version, by contrast, is a sequence of code points your application has no reason to rewrite, so the strike survives end-to-end.

## How the combining mark actually attaches

Each output character is a two-code-point sequence: a base glyph followed by `U+0336` (COMBINING LONG STROKE OVERLAY). The mark has zero width and zero advance — it draws on top of the previous glyph without shifting the layout. That is why `t̶o̶t̶a̶l̶l̶y̶` still occupies the same horizontal footprint as `totally`. The line is per-character, drawn exactly where the previous base character sits.

Because the mark is purely visual, the rendering depends on the font. All modern OS fonts (Helvetica, Segoe, Roboto, Noto, PingFang) render it correctly; legacy bitmap fonts and some terminal emulators may show a missing-glyph box for the mark itself. When in doubt, copy the output into a browser tab and inspect — if it strikes there, it will strike on every mainstream chat app and CMS the recipient uses.

## Why plain text beats markdown here

Markdown's `~~strike~~` is a presentation-layer feature: a parser sees the double-tilde, decides "strikethrough intent," wraps the run in `<del>` or `<s>`, and forgets it. Three failure modes follow.

First, parser dialect. GitHub Flavored Markdown renders `~~`; CommonMark before v0.30 did not; many lightweight parsers (the kind embedded in chat and CMS preview panes) still don't. Second, sanitization. Most HTML sanitizers strip `<del>` and `<s>` from user-submitted content by default, so even when the parser succeeds, downstream rendering throws the tag away. Third, copy-paste: the rendered DOM carries the tag, but a `cmd+c` on the rendered text returns the original `~~word~~` source which, pasted into a plain-text field, is just literal tildes around the word.

Unicode combining marks sidestep all three. There is no parser step — `̶` is a single code point the application is supposed to render. There is no tag to sanitize — the mark is plain text by every sanitizer's definition. And on copy, the actual character copies, so the strike travels with the text into the next application.

## The escape hatch that almost isn't

To remove a strikethrough later, you delete the combining characters. A find-and-replace on the literal `̶` glyph returns the original text. This is also the audit recipe — a quick `grep` over a corpus for `U+0336` tells you exactly which strings have been struck, even when the rest of the document is plain ASCII. Try that with `<del>` markup: it requires a DOM walk and an attribute-aware parser.

The one caveat: screen readers handle struck text inconsistently. Some narrate the mark ("struck through"), some skip it, some pause awkwardly. For accessibility-critical content — alt-text descriptions, formal corrections in published docs — prefer real `<del>` tags with proper ARIA labelling. For informal use — chat banter, sarcasm in social posts, struck-out items in personal notes — the combining mark is the right tool.

## What survives the markdown stripper

Five everyday text situations where `U+0336` works and `~~word~~` does not.

<ul>
<li><strong>Sarcastic corrections in chat.</strong> "I l̶o̶v̶e̶d̶ hated the meeting." Markdown double-tildes get eaten by Slack's quick-edit preview; combining marks survive.</li>
<li><strong>Crossed-out items in shared notes.</strong> Collaborative notes often render as plain text only. Real strikethrough lets you strike a TODO without losing the line.</li>
<li><strong>Social media posts without rich-text fields.</strong> Twitter's composer strips `<s>` tags; the Unicode mark posts as struck text and renders correctly in every modern feed.</li>
<li><strong>Filenames and CLI snippets.</strong> The shell renders `U+0336` as a struck-out string — useful for diagrams showing a renamed file.</li>
<li><strong>Filename announcements in commit messages.</strong> GitHub renders the combining mark in commit views; markdown `~~` does not always render consistently on the web view.</li>
</ul>

All five need plain-text fidelity. None of them need a renderable `<del>` tag.

## Letters, digits, emoji, CJK — the mark is universal

The combining mark applies to whatever character it follows. That means letters strike, digits strike, punctuation strikes, spaces strike (the mark sits to the right of the space — usually invisible but present), emoji strike, and CJK characters strike. There is no font subset that hides the line because the mark is drawn on top, not as a separate glyph.

The one exception is combining-character chains. If you apply the strikethrough to text that already contains combining marks (accents, diacritics, emoji variation selectors), the renderer composes them in a defined order and the strikethrough generally still paints correctly — but the visual alignment can drift if the base character has unusual metrics. Test on a sample before you ship.

## When to use it (and when not to)

Use it for: sarcasm, corrections, struck-out items in notes, social posts without rich-text fields, anywhere plain-text fidelity matters. Use it sparingly — a wall of struck text is hard to read. Prefer markdown `~~` when you control the renderer (your own blog, a docs site that respects `<del>`) because the markup is semantic and accessibility tools handle it better. Use real `<del>` tags with proper labelling for accessible documents.

## Try it and the wider Text Processing toolkit

Try the full tool at [Elysia Tools](https://elysiatools.com/en/tools/strikethrough-text) — paste any string, copy the output, paste it into Slack, Twitter, or a notes app and watch the strike survive. For more text-style transforms (underline, small caps, superscript), explore the broader Text Processing collection at [elysiatools.com](https://elysiatools.com/en/tools).

## Five keep-in-mind rules

A short checklist for working with `U+0336` day-to-day.

- The mark is `U+0336` (COMBINING LONG STROKE OVERLAY) — zero width, zero advance, drawn on top of the previous base character.
- Every character gets the mark — letters, digits, punctuation, spaces, emoji, CJK.
- Find-and-replace on the literal `̶` glyph strips the strike and restores the original.
- Modern OS fonts render the mark correctly; legacy bitmap fonts may show a missing-glyph box.
- Screen readers handle struck text inconsistently — prefer `<del>` for accessibility-critical content.

The combining mark is one of the few Unicode tricks that is universally supported, syntax-free, and survives every sanitizer you are likely to hit. Use it when the strike has to land.
