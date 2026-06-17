---
title: "Glob to Regex: 12 Lines That Expose How File Matching Actually Works"
description: "Glob and regex look like unrelated formats, but a small converter reveals they are dialects of the same language. The judgment calls inside that converter are where file matching actually gets understood."
---

Every file matcher in your stack — ripgrep, ESLint, webpack, jest — quietly picks a side in a 50-year argument about how to describe patterns. Globs won the file-system war. Regex won the text war. The two formats look unrelated: `*.js` versus `^[a-z]+\\d+$`. But a small converter can prove they are dialects, not languages, with one caveat most tutorials skip. That converter is the [Glob to Regex](https://elysiatools.com/en/tools/glob-to-regex) tool on Elysia Tools — and the 12 lines inside it are where the real understanding lives.

## Why two matching languages exist at all

Globs and regex both answer the same question — "does this string match this pattern?" — but they made different tradeoffs. Globs were designed for shell users in 1969. They had to be readable by people who were not programmers. So `*.js` beats `^[^/]*\\.js$` every time on the command line. Globs are tiny, fixed-shape, and almost impossible to misread.

Regex came out of formal-language theory in the 1950s. It was designed for people who needed to describe the shape of text precisely, including things globs cannot express: alternation with repetition (`a{2,5}`), lookahead, character classes with arithmetic (`[a-z&&[^aeiou]]`). Regex is more powerful than globs but reads like a substitution cipher.

The split was not technical. It was ergonomic. Files live in shells; text lives in code. Each format was optimized for the audience that touched it most. Once that split happened, it calcified: 50 years later, your shell and your editor still speak different matching languages, and every tool that bridges the two implements the same small lookup table.

## The translation rules that fit on a sticky note

A glob-to-regex converter is roughly 12 lines. The full translation table looks like this:

| Glob | Regex | Why this mapping |
|------|-------|------------------|
| `*` | `[^/]*` | any chars except `/` (a single directory level) |
| `**` | `.*` | any chars including `/` (multiple directories) |
| `?` | `[^/]` | exactly one char, no slash |
| `.` | `\\.` | literal dot, not "any char" |
| `[abc]` | `[abc]` | character class, mostly identical |
| `{a,b}` | `(a\\|b)` | alternation, the only non-trivial case |
| `\\` | `/\\\\` | escape the next char |

That table is the entire translation. Most of it is one-to-one. The interesting cases — the ones where the table looks wrong — are the ones that expose how matching actually works.

## Where simple globs break: dotfiles, anchors, and `**`

Three judgment calls hide inside those 12 lines, and each one will bite a beginner eventually.

**Dotfiles.** Glob `*` does not match `.env` or `.gitignore`. That is not a convention — it is a hard rule in every major shell. If your regex converter translates `*` to `.*` instead of `[^/]*`, you silently start matching dotfiles and your test suite breaks. The tool must convert `*` to `[^/]*`, never to `.*`, even though `.*` is "more general." Glob semantics are stricter than regex semantics, and the converter must preserve that strictness.

**Anchors.** Glob `*.js` matches `package.js` anywhere it appears. The natural regex translation `[^/]*\\.js` matches the same. But `path/to/foo.js` — does it match? Yes, because regex has no implicit anchor. Most glob tools DO anchor the result, producing `^[^/]*\\.js$`. A converter that forgets the anchor will over-match and a converter that adds the wrong anchor will under-match. The right answer depends on what the consuming tool expects.

**Double star.** Glob `**` means "any number of directories." The regex is `.*` — but that also matches the empty string, the leading slash, and the trailing slash. A clean converter produces something like `(?:.*/)?foo(?:/.*)?` to handle the edge cases. Most tools settle for `.*` because the extra precision is rarely worth the readability hit.

## A worked example: turning `src/**/*.{ts,tsx}` into a regex

Take the glob `src/**/*.{ts,tsx}`. This is what a TypeScript project uses to find every component file. Walk through the translation:

1. `src/` becomes `src/`. Literal characters become escaped literals.
2. `**` becomes `.*`. Any number of directories.
3. `/` becomes `/`. Still a literal.
4. `*` becomes `[^/]*`. Single-level filename body, no slashes.
5. `.` becomes `\\.`. Escape the dot.
6. `{ts,tsx}` becomes `(ts|tsx)`. Alternation, parenthesized.
7. Anchor with `^` and `$` at the boundaries.

Result: `^src/.*/[^/]*\\.(ts|tsx)$`. Test it mentally:

- `src/components/Button.tsx` matches.
- `src/lib/util.ts` matches.
- `src/components/Button.ts` does NOT match (`tsx` required).
- `src/.env` does NOT match (`*` excludes dotfiles if the converter is correct).
- `lib/util.ts` does NOT match (requires `src/` prefix).

Every test passes for the right reason. The 12 lines of translation forced every judgment call — dotfiles, anchors, double star, alternation — to be made explicitly rather than left to the matcher.

## What this tells you about every file matcher you use

Once you can write this converter by hand, the boundary between globs and regex stops being mystical. ESLint's `.eslintignore`, jest's `testMatch`, webpack's `module.rules.test`, prettier's `*.{js,ts}` config — they all consume one of these two formats. When one of them surprises you with a match you did not expect, the surprise comes from one of those three judgment calls: dotfiles, anchors, or double-star semantics. Knowing the translation table means you can predict the surprise before it happens.

The opposite is also true: if you cannot write this converter, you have probably lost hours to a matcher that did something you did not expect. The cost of not understanding is paid in debugging time, slowly, one bug at a time.

Try the [Glob to Regex](https://elysiatools.com/en/tools/glob-to-regex) tool on Elysia Tools to see the translation in action. It is the cleanest way to confirm your mental model — paste a glob, read the regex, and check it against your files. Explore more matching and pattern tools at [elysiatools.com/en/tools](https://elysiatools.com/en/tools).
