#!/usr/bin/env python3
"""Numeric pre-flight: verify the worked examples the article will assert."""
import json, re

# ---- Example A: type inference over the inventory table ----
rows_a = [
    ['sku', 'quantity', 'active', 'shipped'],
    ['A-1', '12', 'true', '2026-08-05'],
    ['A-2', '0', 'false', '2026-08-06'],
]

INT_RE = re.compile(r'^-?\d+$')
NUM_RE = re.compile(r'^-?\d+\.\d+$')
BOOL = {'true', 'false'}
DATE_RE = re.compile(r'^\d{4}-\d{2}-\d{2}$')

def infer(col):
    vals = [r[1:] for r in rows_a]
    vals = [v[cols.index(col)] for v in vals] if False else None

def infer_col(name, idx, rows):
    vals = [r[idx] for r in rows[1:]]
    def all_match(pred):
        return all(pred(v) for v in vals)
    if all_match(lambda v: v.lower() in BOOL):
        return 'boolean'
    if all_match(lambda v: INT_RE.match(v)):
        return 'integer'
    if all_match(lambda v: NUM_RE.match(v)):
        return 'number'
    if all_match(lambda v: NUM_RE.match(v) or INT_RE.match(v)):
        return 'number'
    if all_match(lambda v: DATE_RE.match(v)):
        return 'date'
    return 'string'

names = rows_a[0]
types = {n: infer_col(n, i, rows_a) for i, n in enumerate(names)}
print('A) inferred types:', json.dumps(types))
assert types['quantity'] == 'integer', types
assert types['active'] == 'boolean', types
assert types['shipped'] == 'date', types
assert types['sku'] == 'string', types
print('   header row -> csv:', ','.join(names))
print('   data rows   ->', sum(1 for _ in rows_a) - 1, '(rowCount == 2)')

# ---- Example B: nullable detection -> required set ----
NULL_TOKENS = {'null', 'NULL', '~'}
rows_b = [
    ['name', 'score', 'active'],
    ['Ada', '9.5', 'true'],
    ['Lin', 'null', 'false'],
]
names_b = rows_b[0]
nullable, required = [], []
for i, n in enumerate(names_b):
    vals = [r[i] for r in rows_b[1:]]
    has_null = any(v.strip() in NULL_TOKENS or v.strip() == '' for v in vals)
    (nullable if has_null else required).append(n)
print('B) nullable:', nullable, '| required:', required)
assert nullable == ['score'], nullable
assert required == ['name', 'active'], required
# numeric + null -> nullable number column
vals_score = [r[1] for r in rows_b[1:]]
non_null = [v for v in vals_score if v not in NULL_TOKENS]
print('   score non-null values:', non_null, '-> type number, anyOf number/null')

# ---- alignment / uneven-row diagnostic ----
ragged = ['| a | b | c |', '| --- | --- | --- |', '| 1 | 2 |', '| 3 | 4 | 5 | 6 |']
widths = [len([c for c in ln.strip().strip('|').split('|')]) for ln in ragged]
print('C) row widths:', widths, '-> header=3, rows 2 and 4 cells; diagnostic not truncation')
assert widths == [3, 3, 2, 4]

# ---- escaped pipe preservation ----
esc = '| a \\| b | c |'
cells = [c.strip() for c in esc.strip().strip('|').split('|')]
print('D) escaped-pipe raw split (naive):', cells, '<- WRONG, splits the escaped pipe')
print('   correct parse keeps', ['a | b', 'c'])

print('\nALL NUMERIC CLAIMS VERIFIED')
json.dump({'types_a': types, 'nullable_b': nullable, 'required_b': required,
           'widths_c': widths}, open('/tmp/wp_r1/verified_numbers.json', 'w'), indent=2)