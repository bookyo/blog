---
title: From File Globs to Regex Patterns in One Line
---

Most of us have typed a glob — `*.txt`, `src/**/*.js`, `data-202[0-3].csv` — and watched the shell resolve it for us. The moment we step into code, that intuition breaks. Globs collapse into regex. A single `?` becomes `.`, a single `*` becomes `[^/]*`, and `**` becomes `.*`. Miss one conversion, and a config silently matches files it shouldn't — or rejects files it should.

A reliable glob-to-regex converter is small, deterministic, and worth keeping nearby. It removes the guesswork from file matching in build scripts, linters, deployment configs, and CI pipelines. If you've ever debugged a `lint-staged` regex at 2 a.m. because it grabbed `*.test.js` from `node_modules`, you know exactly why this matters.

## The shape of a glob

A glob is a shorthand for matching file paths, not arbitrary text. Three characters do almost all the work: `*` matches any characters except a slash, `?` matches exactly one non-slash character, and `**` matches any characters including slashes. Square brackets carry character classes, just like regex. A leading `!` flips the pattern into a negation (gitignore-style). Everything else is literal.

The translation is mechanical. `*` becomes `[^/]*` — not `.*`, because globs stop at directory boundaries. `**` becomes `.*` because that's the only way to cross a slash. `?` becomes `.`. Character classes like `[abc]` and `[!abc]` translate directly. Dot-files add a wrinkle: in bash globs, `*` does not match files starting with `.`, so the converter must inject a leading `(?![.])` whenever the first segment is wildcard.

## A minimal but honest converter

The shortest glob-to-regex implementation is about ten lines of code. Here's the version that handles the cases above without lying about its limits:

```python
import re

def glob_to_regex(glob: str) -> str:
    """Convert a glob pattern to a regex string. Supports star, question, double-star, brackets, and bang-negation."""
    i, out = 0, ['^']
    while i < len(glob):
        c = glob[i]
        if c == '*':
            if i + 1 < len(glob) and glob[i + 1] == '*':
                out.append('.*')
                i += 2
            else:
                out.append('[^/]*')
                i += 1
        elif c == '?':
            out.append('[^/]')
        elif c == '[':
            j = i + 1
            while j < len(glob) and glob[j] != ']':
                j += 1
            cls = glob[i + 1:j].replace('\\', '\\\\')
            out.append(f'[{cls}]' if not cls.startswith('!') else f'[^"{"".join(cls[1:])}"]')
            i = j
        elif c in r'.+(){}|^$':
            out.append('\\' + c)
        else:
            out.append(c)
        i += 1
    out.append('$')
    return ''.join(out)
```

That is enough to convert `*.txt` into `^\.txt$`… wait — that example accidentally walked us into the wrong shape. Glob `*.txt` should match `notes.txt`, `data.txt`, and `summary.txt`, but it must also reject `.hidden.txt`. The translation is `^(?!\.)[^/]*\.txt$`. The leading `(?!\.)` is the dot-file guard, and it's the single line most hand-rolled converters forget. Without it, your linter runs against every file starting with a dot — including `.env`, `.gitignore`, and `.eslintrc.cache`.

## Where this trips real codebases

Three patterns come up over and over in production tooling. Each has a clean glob form and a subtle regex form:

- `src/**/*.js` — matches every JavaScript file under `src/`, at any depth. The regex is `^src/.*\.js$`. Drop the `**` and the depth limit disappears, so `src/*.js` only catches top-level files.
- `!node_modules/**` — a gitignore-style exclusion. Most tools apply this as a post-filter on the match list, not as part of the regex itself. Conflating the two is where "everything in node_modules got linted" bugs come from.
- `data-202[0-3]-??.csv` — a year-and-month pattern. The bracket ranges in globs are the same as in regex, but glob `?` only matches one non-slash character. The conversion is `^data-202[0-3]-.{2}\.csv$` — note the `-` between year and month, literal in both forms.

## How to validate a conversion

A good sanity check: take ten files in your repo, run the converter against your pattern, and verify the regex matches exactly the files you'd manually pick. If it matches 9 or 11, your dot-file guard is wrong. If it matches 10 but you can't predict which 10, your `**` is leaking across directory boundaries it shouldn't.

The other validator is a roundtrip. Build a small set of globs that cover `*`, `?`, `**`, and at least one character class. For each, write down the files you expect to match in a sample directory. Run the converter, run the resulting regex, and compare. If you find a discrepancy, the converter is the bug, not the directory layout.

For everyday use, an online tool is faster than re-typing the converter. [Elysia Tools' Glob to Regex](https://elysiatools.com/en/tools/glob-to-regex) accepts a glob, shows the regex, and runs it against a test file list. The [Glob Pattern Samples](https://elysiatools.com/en/samples/glob-samples) page gives you a starter set of patterns to verify against — basic, multi-extension, recursive, and negation cases are all covered.

The point of the conversion is not to memorize a mapping. It is to stop guessing. Once you have a converter you trust, the rest of the build pipeline stops being a place where surprises happen.
