import re, math

text = open('article.md').read()

def words(t): return re.findall(r'[A-Za-z0-9]+', t)
def get_paragraphs(t):
    blocks = re.split(r'\n\s*\n', t.strip())
    return [b.strip() for b in blocks if b.strip() and not b.strip().startswith('#')]
def get_sentences(t):
    rough = re.split(r'(?<=[.!?])\s+', t.strip())
    return [s.strip() for s in rough if words(s)]

lines = text.splitlines()
for line in lines:
    if line.strip() and line.startswith('# '):
        title = line[2:].strip()
        body = '\n'.join(lines[lines.index(line)+1:]).strip()
        break
else:
    title, body = '', text

paragraphs = get_paragraphs(body)
sentences = get_sentences(body)
body_word_count = len(words(body))

print(f"Word count: {body_word_count}")
print(f"Paragraphs: {len(paragraphs)}")
print(f"Sentences: {len(sentences)}")
avg_sent = body_word_count/len(sentences) if sentences else 0
print(f"Avg sentence length: {avg_sent:.1f}")
print(f"Title: {title}")

# Check filler/hedges/strong verbs
STRONG_VERBS = {"build","ship","break","change","force","show","prove","cut","remove","clarify","reshape","unlock","increase","reduce","create","design","replace","fix","improve","matter"}
FILLER = {"very","really","actually","basically","generally","clearly","obviously","simply","just"}
HEDGES = {"maybe","perhaps","sort of","kind of","somewhat","arguably","possibly","it seems","it appears","in some ways","quite","rather"}

body_lower = body.lower()
strong_count = sum(1 for v in STRONG_VERBS if v in body_lower)
filler_count = sum(1 for v in FILLER if v in body_lower)
hedge_count = sum(1 for v in HEDGES if v in body_lower)
print(f"Strong verbs: {strong_count}")
print(f"Filler: {filler_count}")
print(f"Hedges: {hedge_count}")

# Check evidence
EVIDENCE = {"for example","for instance","according to","data","study","research","measured","observed","case","benchmark","reported"}
evidence_count = sum(body_lower.count(e) for e in EVIDENCE)
print(f"Evidence markers: {evidence_count}")

# Title words
title_words = words(title)
print(f"Title words: {len(title_words)}")