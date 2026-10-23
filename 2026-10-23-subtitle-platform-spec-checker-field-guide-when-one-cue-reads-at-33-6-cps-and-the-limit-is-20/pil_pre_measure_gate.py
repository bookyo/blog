"""PIL pre-measure GATE for the Subtitle Platform Spec Checker post (2026-10-23 ~23:0x UTC).

Measures every string against each template's REAL budget before a single PNG is
written. Exits non-zero on overflow so no render cycle is wasted.

Template budgets re-derived from the template source (not from a remembered table):
  render_poster            W=1080; title/subtitle/eyebrow centered -> budget W
                           callout box inner width -> budget W-160
  render_card_4tile_compact tile_w=360; label LEFT-ALIGNED at x+30 -> budget tile_w-60
                           count auto-shrinks 150 -> 84 -> 64 -> budget tile_w-60
                           body/sub wrapped at tile_w-60
  render_card_5tile        tile_w=290; label centered -> budget tile_w
                           value F_MONO_BIG -> budget tile_w-24 (pre-measure the
                           longest \\n-split line)
                           note F_MONO_SM -> budget tile_w
                           requires EXACTLY 5 items (WP 6436)
  render_card_input_output_2col  col_w=700; header -> budget col_w
                           rows F_MONO -> budget col_w-60
"""
import sys
from PIL import Image, ImageDraw

SKILL = '/Users/quyue/.hermes/skills/wordpress-rest-api-publishing'
sys.path.insert(0, SKILL + '/templates')
import pil_poster_and_cards_network_theme as pil

W = 1080
CARD_W = 1600
TILE_W_5 = 290
TILE_W_4 = 360
COL_W = 700
CALLOUT_W = W - 160

fails = []
_d = ImageDraw.Draw(Image.new('RGB', (10, 10)))


def check(label, text, font, budget, hard=True):
	tw = pil.text_w(_d, text, font)
	ok = tw <= budget
	print(f'  [{"ok " if ok else "OVER"}] {label:<34} {tw:>5}px / {budget:>5}px   {text[:52]!r}')
	if not ok and hard:
		fails.append((label, tw, budget, text))
	return tw


print('=' * 78)
print('POSTER  (render_poster: W=1080 H=800)')
print('=' * 78)
EYEBROW = 'MEDIA  .  SUBTITLE DELIVERY QA'
TITLE = ('One File, Four Specs,', 'One Number That Fails')
SUBTITLE = 'Why CPS decides the delivery, not your taste'
CALLOUT = ('84 characters over 2.5 seconds', 'is 33.6 CPS against a 20 CPS limit')
URLBAR = 'elysiatools.com/en/tools/subtitle-platform-spec-checker'

check('poster eyebrow', EYEBROW, pil.F_MED, W)
check('poster title line 0', TITLE[0], pil.F_TITLE, W)
check('poster title line 1', TITLE[1], pil.F_TITLE, W)
check('poster subtitle', SUBTITLE, pil.F_MED, W)
check('poster callout 0', CALLOUT[0], pil.F_MED, CALLOUT_W)
check('poster callout 1', CALLOUT[1], pil.F_MED, CALLOUT_W)
check('poster url bar', URLBAR, pil.F_SMALL, W)

print()
print('=' * 78)
print('CARD 1 — render_card_4tile_compact  (tile_w=360, label budget tile_w-60=300)')
print('=' * 78)
C1_TITLE = 'Four Profiles, Four Headline Limits'
C1_SUB = 'The thresholds each rulebook applies to every cue'
C1_TILES = (
	('NETFLIX ADULT', '20', 'CPS limit for adult programs', 'children drop to 17'),
	('NETFLIX KIDS', '17', 'CPS limit for children', 'same 42-char line'),
	('BBC TV', '37', 'characters per line, teletext', '160-180 wpm pace'),
	('YOUTUBE', 'UTF-8', 'plain text, markup ignored', 'reported as warning'),
)
C1_TAKE = 'Only one profile can be the delivery target for a given file'
check('card1 title', C1_TITLE, pil.F_H2, CARD_W)
check('card1 subtitle', C1_SUB, pil.F_MED, CARD_W)
for i, (label, count, body, sub) in enumerate(C1_TILES):
	check(f'card1 tile{i} label', label, pil.F_H3, TILE_W_4 - 60)
	eff = pil.text_w(_d, count, pil.F_HUGE)
	eff_font = '150'
	if eff > TILE_W_4 - 60:
		eff = pil.text_w(_d, count, pil.load(pil.HELV_NEU, 0, 84))
		eff_font = '84'
	if eff > TILE_W_4 - 60:
		eff = pil.text_w(_d, count, pil.load(pil.HELV_NEU, 0, 64))
		eff_font = '64'
	print(f'  [{"ok " if eff <= TILE_W_4 - 60 else "OVER"}] card1 tile{i} count@{eff_font:<4}'
	      f' {eff:>5}px / {TILE_W_4 - 60:>5}px   {count!r}')
	if eff > TILE_W_4 - 60:
		fails.append((f'card1 tile{i} count', eff, TILE_W_4 - 60, count))
	for b in pil.wrap_text(_d, body, pil.F_SMALL, TILE_W_4 - 60)[:2]:
		check(f'card1 tile{i} body', b, pil.F_SMALL, TILE_W_4 - 60)
	for s in pil.wrap_text(_d, sub, pil.F_MONO_SM, TILE_W_4 - 60)[:2]:
		check(f'card1 tile{i} sub', s, pil.F_MONO_SM, TILE_W_4 - 60)
check('card1 takeaway', C1_TAKE, pil.F_MED, CARD_W)

print()
print('=' * 78)
print('CARD 2 — render_card_5tile  (tile_w=290, EXACTLY 5 items required)')
print('=' * 78)
C2_TITLE = 'Five Checks That Run on Every Profile'
C2_SUB = 'What the checker measures before it grades a cue'
C2_ITEMS = (
	('01', 'READING SPEED', '20 CPS'),
	('02', 'LINE WIDTH', '42 chars'),
	('03', 'LINE COUNT', '2 lines'),
	('04', 'DURATION', '7 s max'),
	('05', 'FRAME GAP', '2 frames'),
)
C2_NOTES = ('adult profile', 'BBC says 37', 'per cue', 'min 20 frames', 'at any fps')
C2_TAKE = 'Overlap, negative duration and empty cues fail under every profile'
assert len(C2_ITEMS) == 5, 'render_card_5tile requires exactly 5 items'
check('card2 title', C2_TITLE, pil.F_H2, CARD_W)
check('card2 subtitle', C2_SUB, pil.F_MED, CARD_W)
for i, (num, label, body) in enumerate(C2_ITEMS):
	check(f'card2 item{i} label', label, pil.F_MED, TILE_W_5)
	# WP 8523: pre-measure the LONGEST \n-split line, not the whole string
	for line in body.split('\n'):
		check(f'card2 item{i} value', line, pil.F_MONO_BIG, TILE_W_5 - 24)
	check(f'card2 item{i} note', C2_NOTES[i], pil.F_MONO_SM, TILE_W_5)
check('card2 takeaway', C2_TAKE, pil.F_MED, CARD_W)

print()
print('=' * 78)
print('CARD 3 — render_card_input_output_2col  (col_w=700, row budget 640, header 700)')
print('=' * 78)
C3_TITLE = 'The One Number That Fails a File'
C3_SUB = 'Characters per second is characters over duration, spaces counted'
C3_LH = 'CUE -> READ -> CPS -> GRADE'
C3_RH = 'WHAT THE REPORT NAMES'
C3_LEFT = (
	'84 chars / 2.5 s',
	'  = 33.6 CPS',
	'  limit 20 CPS',
	'',
	'84 chars / 4.2 s',
	'  = 20.0 CPS  PASS',
)
C3_RIGHT = (
	'cue 3 reading speed',
	'fail against adult limit',
	'needs 4200 ms on screen',
	'',
	'verdict: pass',
	'fastest cue 20.0 CPS',
)
C3_TAKE = 'Extend the cue to 4200 ms and the file becomes compliant unchanged'
check('card3 title', C3_TITLE, pil.F_H2, CARD_W)
check('card3 subtitle', C3_SUB, pil.F_MED, CARD_W)
check('card3 left header', C3_LH, pil.F_MED, COL_W)
check('card3 right header', C3_RH, pil.F_MED, COL_W)
for r in C3_LEFT:
	if r:
		check('card3 left row', r, pil.F_MONO, COL_W - 60)
for r in C3_RIGHT:
	check('card3 right row', r, pil.F_MONO, COL_W - 60)
check('card3 takeaway', C3_TAKE, pil.F_MED, CARD_W)

print()
print('=' * 78)
if fails:
	print(f'GATE: FAIL -- {len(fails)} overflow(s), no PNG written')
	for f in fails:
		print('   ', f)
	sys.exit(1)
print('GATE: PASS -- every string fits its real budget')

print()
print('=' * 78)
print('TOFU PRE-FLIGHT (memory pitfall #82: build ranges with chr(), self-test)')
print('=' * 78)
bad_ranges = [(0x2460, 0x24FF), (0x2776, 0x2793), (0x1F150, 0x1F1FF),
              (0x1D00, 0x1D5A), (0x2100, 0x2BFF), (0x0378, 0x037F),
              (0xFEFF, 0xFEFF), (0x2E80, 0x9FFF)]
BAD = ''.join(chr(cp) for lo, hi in bad_ranges for cp in range(lo, hi + 1))
_TOFU_RE = __import__('re').compile('[' + BAD + ']')
assert _TOFU_RE.findall('<ascii probe ABC 123 ~!@#>') == [], 'tofu class matches ASCII -> broken'
print('  [ok ] tofu class self-test (ASCII probe returns [])')
ALL_TEXT = ' '.join([EYEBROW, ' '.join(TITLE), SUBTITLE, ' '.join(CALLOUT), URLBAR,
                      C1_TITLE, C1_SUB, ' '.join(x for t in C1_TILES for x in t), C1_TAKE,
                      C2_TITLE, C2_SUB, ' '.join(x for t in C2_ITEMS for x in t), ' '.join(C2_NOTES), C2_TAKE,
                      C3_TITLE, C3_SUB, C3_LH, C3_RH, ' '.join(C3_LEFT), ' '.join(C3_RIGHT), C3_TAKE])
hits = sorted(set(_TOFU_RE.findall(ALL_TEXT)))
print(f'  [{"ok " if not hits else "TOFU"}] tofu glyphs in asset text: {len(hits)} {hits if hits else ""}')
if hits:
	sys.exit(1)
print('GATE: ALL PASS')
