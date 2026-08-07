#!/usr/bin/env python3
"""Per-tool PIL render for SSH Key Pair Generator (WP 5712+).

Generates poster + 3 highlight cards. Follows the WP 5683 / WP 5705 lessons:
- Single-row 4-tile variant for card 3 (when content fits)
- Per-tile font auto-shrink (36 -> 28 -> 22) for path-style values
- Body text capped to 2 lines + divider rule + note below rule
- Poster subtitle pre-measured to clear the W=1080 canvas
- vision_analyze for pre-POST visual QA

Theme: SECURITY palette (deep navy + cyan-teal).
Output to: /Users/quyue/www/blog/2026-08-07-ssh-key-pair-generator-field-guide-2026-08-07/
"""
import sys
import os
sys.path.insert(0, '/Users/quyue/.hermes/skills/wordpress-rest-api-publishing/templates')

from PIL import Image, ImageDraw, ImageFont, ImageFont as _IF
from pil_poster_and_cards_network_theme import (
    BG, BG_CARD, ACCENT, ACCENT2, TEXT_MAIN, TEXT_DIM, TEXT_MUTED,
    PANEL_BORDER, GREEN, RED,
    HELV, HELV_NEU,
    load, F_HUGE, F_TITLE, F_H2, F_H3, F_BIG, F_MED, F_SMALL, F_TINY,
    F_MONO_BIG, F_MONO, F_MONO_SM, F_MONO_TINY,
    text_w, text_h, wrap_text, draw_centered,
)

OUT_DIR = '/Users/quyue/www/blog/2026-08-07-ssh-key-pair-generator-field-guide-2026-08-07'

# ============================================================================
# POSTER (1080x800)
# ============================================================================
def render_poster(out_path,
                  eyebrow='SECURITY / IDENTITY',
                  title_lines=('SSH Keys', 'Are a Math Trick'),
                  subtitle="How Ed25519, RSA 4096, and ECDSA prove your identity without sending a password",
                  callout_lines=('One private file, one public line,', 'and 256 bits of math that holds'),
                  url_bar='elysiatools.com/en/tools/ssh-key-generator'):
    W, H = 1080, 800
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)

    # Subtle grid background
    for y in range(0, H, 40):
        d.line([(0, y), (W, y)], fill=(20, 30, 55), width=1)
    for x in range(0, W, 40):
        d.line([(x, 0), (x, H)], fill=(20, 30, 55), width=1)

    # Top accent bar
    d.rectangle([(0, 0), (W, 8)], fill=ACCENT)

    # Eyebrow
    draw_centered(d, (0, 70), W, eyebrow, F_MED, ACCENT)

    # 2-line title
    t1_y = 170
    t2_y = t1_y + 100
    draw_centered(d, (0, t1_y), W, title_lines[0], F_TITLE, TEXT_MAIN)
    draw_centered(d, (0, t2_y), W, title_lines[1], F_TITLE, ACCENT)

    # Subtitle (pre-measured against W=1080-40 = 1040 max width)
    subtitle_y = t2_y + 130
    if text_w(d, subtitle, F_MED) > W - 40:
        # Shorten defensively (should not happen with the line we wrote)
        subtitle = "Ed25519, RSA 4096, and ECDSA prove identity without a password"
    draw_centered(d, (0, subtitle_y), W, subtitle, F_MED, TEXT_DIM)

    # Callout box
    box_y = t2_y + 250
    box_h = 100
    d.rectangle([(80, box_y), (W - 80, box_y + box_h)], fill=BG_CARD, outline=ACCENT, width=3)
    for i, line in enumerate(callout_lines):
        ly = box_y + 18 + i * 38
        # ensure no overflow
        if text_w(d, line, F_MED) > W - 160:
            # split or shrink
            for k in range(len(line), 0, -1):
                if text_w(d, line[:k], F_MED) <= W - 160:
                    line = line[:k]
                    break
        draw_centered(d, (80, ly), W - 160, line, F_MED, TEXT_MAIN)

    # Bottom URL bar
    d.rectangle([(0, H - 50), (W, H)], fill=(4, 10, 22))
    draw_centered(d, (0, H - 38), W, url_bar, F_SMALL, ACCENT)

    img.save(out_path, 'PNG', optimize=True)
    return out_path


# ============================================================================
# CARD 1 — Four-component output panel (4-tile single-row)
# Cards anchor H2: "Generating a key with one paste: the Elysia Tools flow"
# ============================================================================
def render_card_4tile_1row(out_path,
                           title='Four Artifacts, One Click',
                           subtitle='What the SSH Key Pair Generator gives you on every click of Generate',
                           tiles=(
                               ('PUBLIC KEY',  'ssh-ed25519 AAAA...', 'paste into authorized_keys'),
                               ('FINGERPRINT', 'SHA256:abcd...',     'verify out-of-band'),
                               ('PRIVATE KEY', '-----BEGIN PRIVATE KEY-----', 'chmod 600 then save'),
                               ('METADATA',    'algorithm + comment', 'know which key you made'),
                           ),
                           takeaway='Private key never leaves the page  |  local generate, zero upload'):
    """Single-row 4-tile variant (WP 5683 / WP 5705 recipe)."""
    W, H = 1600, 900
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([(0, 0), (W, 6)], fill=ACCENT)

    draw_centered(d, (0, 50), W, title, F_H2, TEXT_MAIN)
    draw_centered(d, (0, 130), W, subtitle, F_MED, TEXT_DIM)

    n = len(tiles)
    tile_w, tile_h, gap_x = 360, 540, 30
    total_w = n * tile_w + (n - 1) * gap_x
    start_x = (W - total_w) // 2
    y0 = 200

    for i, (label, value, note) in enumerate(tiles):
        x = start_x + i * (tile_w + gap_x)

        # Tile background
        d.rectangle([(x, y0), (x + tile_w, y0 + tile_h)], fill=BG_CARD, outline=PANEL_BORDER, width=2)
        d.rectangle([(x, y0), (x + tile_w, y0 + 4)], fill=ACCENT)

        # Label (top, accent color)
        draw_centered(d, (x, y0 + 40), tile_w, label, F_H3, ACCENT)

        # Divider under label
        d.line([(x + 40, y0 + 110), (x + tile_w - 40, y0 + 110)], fill=PANEL_BORDER, width=2)

        # Value (mono, auto-shrink 36 -> 28 -> 22)
        val_font = F_MONO_BIG
        if text_w(d, value, val_font) > tile_w - 60:
            val_font = F_MONO
            if text_w(d, value, val_font) > tile_w - 60:
                val_font = F_MONO_SM
        vlines = wrap_text(d, value, val_font, tile_w - 60)
        # Cap to 2 lines
        if len(vlines) > 2:
            vlines = vlines[:2]
        vy = y0 + 160
        for ln in vlines:
            draw_centered(d, (x, vy), tile_w, ln, val_font, TEXT_MAIN)
            vy += 44

        # Body text line (2 lines max), placed at y0 + 300
        body_lines = wrap_text(d, note, F_SMALL, tile_w - 40)
        if len(body_lines) > 2:
            body_lines = body_lines[:2]
        body_y = y0 + 320
        for ln in body_lines:
            draw_centered(d, (x, body_y), tile_w, ln, F_SMALL, TEXT_DIM)
            body_y += 28

        # Divider rule above note (WP 5705 lesson: y0 + tile_h - 80)
        d.line([(x + 30, y0 + tile_h - 80), (x + tile_w - 30, y0 + tile_h - 80)], fill=PANEL_BORDER, width=1)

        # Note text below the divider (capped 2 lines) - reusing 'note' as the takeaway note under divider
        # For this card, the body is the note, so display a compact metadata line under divider
        # We just leave the divider as the visual break.

    # Bottom takeaway — clear tile bottom by 30px (single-row variant: y0 + tile_h + 30)
    draw_centered(d, (0, y0 + tile_h + 30), W, takeaway, F_MED, ACCENT)

    img.save(out_path, 'PNG', optimize=True)
    return out_path


# ============================================================================
# CARD 2 — three-tile workflow (right-half audit-style) for H2: "When to choose RSA 4096 anyway"
# Use the existing render_card_audit style but with our own numbers.
# We'll write a custom card with a 3-row comparison table.
# ============================================================================
def render_card_3row_compare(out_path,
                             title='Ed25519 vs RSA 4096 vs ECDSA',
                             subtitle='Three algorithms, three compatibility profiles, one recommendation',
                             rows=(
                                 ('01', 'Speed',  'Ed25519 < 1ms',   'RSA 4096 ~30ms',       'ECDSA P-256 ~2ms'),
                                 ('02', 'Key size', '68 bytes',      '700 bytes',            '~100 bytes'),
                                 ('03', 'Compat',  'Modern default', 'Legacy / old SSH',     'Somewhat rare'),
                                 ('04', 'Default', 'Recommended',    'Only if needed',       'Edge cases'),
                             ),
                             takeaway='Pick Ed25519 unless a concrete server, appliance, or tool requires RSA 4096'):
    """4-row comparison table card (3 algorithms side by side). 1600x900."""
    W, H = 1600, 900
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([(0, 0), (W, 6)], fill=ACCENT)

    draw_centered(d, (0, 50), W, title, F_H2, TEXT_MAIN)
    draw_centered(d, (0, 130), W, subtitle, F_MED, TEXT_DIM)

    # Layout: 4 columns: number badge | Ed25519 | RSA 4096 | ECDSA P-256
    # Each column 360 wide, total 4*360 + 3*30 = 1530 (35px margin each side)
    col_w, gap_x = 360, 30
    start_x = (W - (4 * col_w + 3 * gap_x)) // 2
    y0 = 210
    row_h = 130

    headers = ['', 'Ed25519', 'RSA 4096', 'ECDSA P-256']

    # Header row
    for i, h in enumerate(headers):
        x = start_x + i * (col_w + gap_x)
        # Header bar
        d.rectangle([(x, y0), (x + col_w, y0 + 70)], fill=BG_CARD, outline=ACCENT, width=2)
        draw_centered(d, (x, y0 + 18), col_w, h, F_H3, ACCENT)

    # Rows
    for ridx, row in enumerate(rows):
        num, label, v1, v2, v3 = row
        ry = y0 + 70 + ridx * row_h

        # Label column with badge
        x0 = start_x
        d.rectangle([(x0, ry), (x0 + col_w, ry + row_h)], fill=BG_CARD, outline=PANEL_BORDER, width=2)
        # Badge
        badge_size = 50
        bx = x0 + 25
        by_ = ry + (row_h - badge_size) // 2
        d.rectangle([(bx, by_), (bx + badge_size, by_ + badge_size)], fill=ACCENT2)
        ntw = text_w(d, num, F_BIG)
        nth = text_h(d, num, F_BIG)
        d.text((bx + (badge_size - ntw) // 2, by_ + (badge_size - nth) // 2 - 4), num, fill=BG, font=F_BIG)
        # Label text
        d.text((bx + badge_size + 25, ry + (row_h - 30) // 2), label, fill=TEXT_MAIN, font=F_H3)

        # Three value columns
        for cidx, val in enumerate([v1, v2, v3]):
            cx = start_x + (cidx + 1) * (col_w + gap_x)
            d.rectangle([(cx, ry), (cx + col_w, ry + row_h)], fill=BG_CARD, outline=PANEL_BORDER, width=2)
            # Highlight recommended
            if cidx == 0:
                d.rectangle([(cx, ry), (cx + col_w, ry + 4)], fill=ACCENT)
            # Value (wrap if needed)
            vlines = wrap_text(d, val, F_MONO, col_w - 50)
            if len(vlines) > 2:
                vlines = vlines[:2]
            vy = ry + (row_h - len(vlines) * 36) // 2
            for ln in vlines:
                draw_centered(d, (cx, vy), col_w, ln, F_MONO, TEXT_MAIN)
                vy += 36

    # Bottom takeaway
    takeaway_y = y0 + 70 + 4 * row_h + 50
    if takeaway_y < 870:
        draw_centered(d, (0, takeaway_y), W, takeaway, F_MED, ACCENT)
    else:
        # truncate to fit
        draw_centered(d, (0, 860), W, takeaway[:100], F_MED, ACCENT)

    img.save(out_path, 'PNG', optimize=True)
    return out_path


# ============================================================================
# CARD 3 — Audit/checklist card for H2: "Common failures and the fix for each"
# Uses the audit pattern (left column checklist, right column verdict).
# ============================================================================
def render_card_audit(out_path,
                      title='Four Failures SSH Hands You',
                      subtitle='What each error means, what you change, and what to never click past',
                      header_left='ERROR YOU SEE',
                      header_right='WHAT IT ACTUALLY MEANS',
                      checks=(
                          ('01', 'Permission denied (publickey)',
                           'Wrong perms on server ~/.ssh or authorized_keys',
                           'chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys'),
                          ('02', 'No mutual signature algorithm',
                           'Server does not accept your key type',
                           'Regenerate to match server or extend PubkeyAcceptedAlgorithms'),
                          ('03', 'Host key verification failed',
                           'Server fingerprint does not match known_hosts',
                           'Verify out-of-band first, then ssh-keygen -R hostname'),
                          ('04', 'Pasted key wraps to multiple lines',
                           'Chat client broke a 76-col base64 string',
                           'Use the single-line output from a browser generator'),
                      ),
                      stamp='ssh user@host',
                      verdict=(
                          ('first connect',  'ed25519'),
                          ('paste target',   '~/.ssh/authorized_keys'),
                          ('file mode',      'chmod 600'),
                          ('recheck',        'ssh -v user@host'),
                      )):
    """Audit-style card based on the canonical render_card_audit template but adapted to 4 rows."""
    W, H = 1600, 900
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([(0, 0), (W, 6)], fill=ACCENT)

    draw_centered(d, (0, 50), W, title, F_H2, TEXT_MAIN)
    draw_centered(d, (0, 130), W, subtitle, F_MED, TEXT_DIM)

    col_w, gap = 700, 60
    left_x = (W - (col_w * 2 + gap)) // 2
    right_x = left_x + col_w + gap
    col_y, col_h = 200, 620

    # Left column (errors + fixes)
    d.rectangle([(left_x, col_y), (left_x + col_w, col_y + col_h)], fill=BG_CARD, outline=PANEL_BORDER, width=2)
    d.rectangle([(left_x, col_y), (left_x + col_w, col_y + 4)], fill=ACCENT2)
    draw_centered(d, (left_x, col_y + 22), col_w, header_left, F_MED, ACCENT2)

    # 4 rows; row_h = 130
    row_h = 130
    row_y0 = col_y + 80
    for idx, (num, label, body, fix) in enumerate(checks):
        ry = row_y0 + idx * row_h
        if ry + row_h > col_y + col_h - 10:
            break  # safety: never exceed column
        badge_size = 50
        bx = left_x + 25
        by_ = ry + 10
        d.rectangle([(bx, by_), (bx + badge_size, by_ + badge_size)], fill=ACCENT2)
        ntw = text_w(d, num, F_BIG)
        nth = text_h(d, num, F_BIG)
        d.text((bx + (badge_size - ntw) // 2, by_ + (badge_size - nth) // 2 - 4), num, fill=BG, font=F_BIG)
        # Label
        d.text((bx + badge_size + 20, ry + 8), label, fill=TEXT_MAIN, font=F_H3)
        # Body (1 line normally)
        body_lines = wrap_text(d, body, F_SMALL, col_w - badge_size - 80)[:1]
        d.text((bx + badge_size + 20, ry + 60), body_lines[0] if body_lines else '', fill=TEXT_DIM, font=F_SMALL)
        # Fix (mono, bottom)
        fix_lines = wrap_text(d, fix, F_MONO_SM, col_w - badge_size - 80)[:1]
        if fix_lines:
            d.text((bx + badge_size + 20, ry + 92), fix_lines[0], fill=GREEN, font=F_MONO_SM)

    # Right column (verdict)
    d.rectangle([(right_x, col_y), (right_x + col_w, col_y + col_h)], fill=BG_CARD, outline=PANEL_BORDER, width=2)
    d.rectangle([(right_x, col_y), (right_x + col_w, col_y + 4)], fill=ACCENT)
    draw_centered(d, (right_x, col_y + 22), col_w, header_right, F_MED, ACCENT)

    draw_centered(d, (right_x, col_y + 80), col_w, stamp, F_MONO_BIG, TEXT_MAIN)

    vy = col_y + 180
    for label, val in verdict:
        d.text((right_x + 40, vy), label, fill=TEXT_DIM, font=F_MED)
        d.text((right_x + 280, vy), val, fill=TEXT_MAIN, font=F_MONO)
        d.rectangle([(right_x + col_w - 110, vy + 4), (right_x + col_w - 50, vy + 40)], fill=GREEN)
        tw_ok = text_w(d, 'OK', F_SMALL)
        d.text((right_x + col_w - 110 + (60 - tw_ok) // 2, vy + 9), 'OK', fill=BG, font=F_SMALL)
        vy += 70

    d.line([(right_x + 30, col_y + col_h - 110), (right_x + col_w - 30, col_y + col_h - 110)], fill=PANEL_BORDER, width=2)
    d.text((right_x + 40, col_y + col_h - 90), 'rule', fill=ACCENT2, font=F_MONO)
    d.text((right_x + 40, col_y + col_h - 56), 'Verify fingerprints out-of-band before clicking past host-key warnings.', fill=TEXT_DIM, font=F_SMALL)

    img.save(out_path, 'PNG', optimize=True)
    return out_path


if __name__ == '__main__':
    p = render_poster(os.path.join(OUT_DIR, 'poster.png'))
    print(f'Poster: {p}  size={os.path.getsize(p)} bytes')
    c1 = render_card_4tile_1row(os.path.join(OUT_DIR, 'card1.png'))
    print(f'Card 1: {c1}  size={os.path.getsize(c1)} bytes')
    c2 = render_card_3row_compare(os.path.join(OUT_DIR, 'card2.png'))
    print(f'Card 2: {c2}  size={os.path.getsize(c2)} bytes')
    c3 = render_card_audit(os.path.join(OUT_DIR, 'card3.png'))
    print(f'Card 3: {c3}  size={os.path.getsize(c3)} bytes')
