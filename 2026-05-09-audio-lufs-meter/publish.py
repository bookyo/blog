import re, json, requests

work_dir = "/Users/quyue/www/blog/2026-05-09-audio-lufs-meter"
auth = ("bted2k@gmail.com", "zVlf aCkm vB79 GjXc zVrJ dSuH")
wp_url = "https://blog.flowrust.com"

# Disable proxy to avoid 127.0.0.1:1081 connection issues
session = requests.Session()
session.trust_env = False

# ─── Upload images ─────────────────────────────────────────────────────────────
def upload_image(filename, display_name):
    with open(filename, "rb") as f:
        response = session.post(
            f"{wp_url}/wp-json/wp/v2/media",
            auth=auth,
            headers={
                "Content-Type": "image/png",
                "Content-Disposition": f"attachment; filename={display_name}",
            },
            data=f.read(),
            timeout=30
        )
    return response.json()["id"], response.json()["source_url"]

print("Uploading poster...")
cover_id, cover_url = upload_image(f"{work_dir}/poster.png", "poster.png")
print(f"  cover_id={cover_id}, url={cover_url}")

print("Uploading card 01...")
card1_id, card1_url = upload_image(f"{work_dir}/card-01.png", "card-01.png")
print(f"  card1_id={card1_id}, url={card1_url}")

print("Uploading card 02...")
card2_id, card2_url = upload_image(f"{work_dir}/card-02.png", "card-02.png")
print(f"  card2_id={card2_id}, url={card2_url}")

print("Uploading card 03...")
card3_id, card3_url = upload_image(f"{work_dir}/card-03.png", "card-03.png")
print(f"  card3_id={card3_id}, url={card3_url}")

# ─── Read HTML ────────────────────────────────────────────────────────────────
with open(f"{work_dir}/article_raw.html") as f:
    html_original = f.read()

# ─── Find insertion points ────────────────────────────────────────────────────
def find_para_end_after(html, phrase):
    idx = html.find(phrase)
    if idx == -1:
        return None
    end_para = html.find('</p>', idx)
    return end_para + 4

def find_h2_section_insert(html, h2_text_contains):
    """Insert after the first paragraph following an h2 heading containing h2_text_contains (partial match, case-insensitive)."""
    search_start = 0
    while True:
        h2_open = html.find('<h2>', search_start)
        if h2_open == -1:
            return None
        h2_close = html.find('</h2>', h2_open)
        if h2_close == -1:
            return None
        heading_text = html[h2_open + 4:h2_close]
        if h2_text_contains.lower() in heading_text.lower():
            first_p = html.find('<p>', h2_open)
            if first_p == -1:
                return None
            end_p = html.find('</p>', first_p)
            return end_p + 4
        search_start = h2_open + 1

positions = {
    'card1': find_h2_section_insert(html_original, 'What LUFS Actually Measures'),
    'card2': find_h2_section_insert(html_original, 'The Loudness Wars'),
    'card3': find_h2_section_insert(html_original, 'The Three Numbers'),
}

print("\nInsert positions:", positions)

positions = {k: v for k, v in positions.items() if v is not None}
missing = set(['card1','card2','card3']) - set(positions.keys())
if missing:
    print(f"WARNING: phrases not found: {missing}")

sorted_cards = sorted(positions.items(), key=lambda x: x[1], reverse=True)
print("Sorted (bottom-to-top):", sorted_cards)

card_imgs = {
    'card1': f'<br/><img src="{card1_url}" alt="Card 1: Perceived Loudness" style="width:100%;max-width:1080px;margin:2rem 0;display:block;"/><br/>',
    'card2': f'<br/><img src="{card2_url}" alt="Card 2: Loudness Wars" style="width:100%;max-width:1080px;margin:2rem 0;display:block;"/><br/>',
    'card3': f'<br/><img src="{card3_url}" alt="Card 3: Platform Standards" style="width:100%;max-width:1080px;margin:2rem 0;display:block;"/><br/>',
}

html = html_original
for name, pos in sorted_cards:
    html = html[:pos] + '\n' + card_imgs[name] + html[pos:]
    print(f"Inserted {name} at position {pos}")

with open(f"{work_dir}/article_with_cards.html", "w") as f:
    f.write(html)
print(f"\nSaved: {work_dir}/article_with_cards.html")

# ─── Create post ───────────────────────────────────────────────────────────────
slug = "audio-lufs-meter-hidden-standard-loudness"
title = "The Hidden Standard That Decides How Loud Everything You Hear Actually Sounds"
# Use date 7th of month to avoid "future" status
create_data = {
    "title": title,
    "slug": slug,
    "status": "publish",
    "content": html,
    "date_gmt": "2026-05-07T04:00:00",
    "featured_media": cover_id,
}

resp = session.post(
    f"{wp_url}/wp-json/wp/v2/posts",
    auth=auth,
    headers={"Content-Type": "application/json"},
    json=create_data,
    timeout=30
)
print("\nCreate response status:", resp.status_code)
result = resp.json()
print("Post ID:", result.get("id"))
print("Status:", result.get("status"))
post_id = result.get("id")

if result.get("status") == "future":
    print("Post is future — forcing publish with PATCH...")
    update_data = {
        "status": "publish",
        "date_gmt": "2026-05-07T04:00:00"
    }
    resp2 = session.post(
        f"{wp_url}/wp-json/wp/v2/posts/{post_id}",
        auth=auth,
        headers={"Content-Type": "application/json"},
        json=update_data,
        timeout=30
    )
    print("PATCH response:", resp2.status_code, resp2.json().get("status"))

print(f"\nPost URL: {result.get('link')}")
print(f"Featured image URL: {cover_url}")
print(f"Card URLs: {card1_url}, {card2_url}, {card3_url}")
