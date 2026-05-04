#!/usr/bin/env python3
import re
import json
import requests

AUTH = ("bted2k@gmail.com", "zVlf aCkm vB79 GjXc zVrJ dSuH")
BLOG_URL = "https://blog.flowrust.com"

# Card image URLs
card_urls = {
    'card1': 'https://blog.flowrust.com/wp-content/uploads/2026/05/card-01-8.png',
    'card2': 'https://blog.flowrust.com/wp-content/uploads/2026/05/card-02-8.png',
    'card3': 'https://blog.flowrust.com/wp-content/uploads/2026/05/card-03-8.png',
}

# Read HTML
with open("article.html") as f:
    html = f.read()

# Find insertion positions on ORIGINAL html (before ANY insertions)
def find_para_end_after(html, phrase):
    idx = html.find(phrase)
    if idx == -1:
        return None
    end_para = html.find('</p>', idx)
    return end_para + 4

positions = {}
positions['card1'] = find_para_end_after(html, 'The atoms in your fingertip')
positions['card2'] = find_para_end_after(html, 'At any point in space, the electric field has exactly one direction')
positions['card3'] = find_para_end_after(html, "A water molecule is a dipole")

print("Insert positions:", positions)

# Filter None, sort descending
positions = {k: v for k, v in positions.items() if v is not None}
sorted_cards = sorted(positions.items(), key=lambda x: x[1], reverse=True)

missing = set(['card1','card2','card3']) - set(positions.keys())
if missing:
    print(f"WARNING: phrases not found: {missing}")

# Card HTML
card_imgs = {
    'card1': f'<br/><img src="{card_urls["card1"]}" alt="You Never Actually Touch Anything" style="width:100%;max-width:1080px;margin:2rem 0;"/><br/>',
    'card2': f'<br/><img src="{card_urls["card2"]}" alt="Field Lines Never Cross" style="width:100%;max-width:1080px;margin:2rem 0;"/><br/>',
    'card3': f'<br/><img src="{card_urls["card3"]}" alt="The Dipole Is Everywhere" style="width:100%;max-width:1080px;margin:2rem 0;"/><br/>',
}

# Insert from bottom to top
for name, pos in sorted_cards:
    html = html[:pos] + '\n' + card_imgs[name] + html[pos:]

# Save final HTML
with open("article_with_cards.html", "w") as f:
    f.write(html)

print(f"Final HTML length: {len(html)}")
print("Saved article_with_cards.html")
