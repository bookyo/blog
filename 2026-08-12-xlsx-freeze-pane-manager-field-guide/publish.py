"""Substitute placeholders with real WP media URLs, then publish."""
import sys, json
sys.path.insert(0, '/Users/quyue/.hermes/skills/wordpress-rest-api-publishing')
from templates.cron_publish_driver import publish_post

WORKDIR = '/Users/quyue/www/blog/2026-08-12-xlsx-freeze-pane-manager-field-guide'

media_urls = {
    'poster.png': 'https://blog.flowrust.com/wp-content/uploads/2026/08/jarvis-poster-xlsx-freeze-pane-manager-field-guide-2026-08-12.png',
    'card1.png':  'https://blog.flowrust.com/wp-content/uploads/2026/08/jarvis-card1-xlsx-freeze-pane-manager-field-guide-2026-08-12.png',
    'card2.png':  'https://blog.flowrust.com/wp-content/uploads/2026/08/jarvis-card2-xlsx-freeze-pane-manager-field-guide-2026-08-12.png',
    'card3.png':  'https://blog.flowrust.com/wp-content/uploads/2026/08/jarvis-card3-xlsx-freeze-pane-manager-field-guide-2026-08-12.png',
}

html = open(f'{WORKDIR}/article_with_figures.html').read()
html = html.replace('POSTER_URL', media_urls['poster.png'])
html = html.replace('CARD1_URL',  media_urls['card1.png'])
html = html.replace('CARD2_URL',  media_urls['card2.png'])
html = html.replace('CARD3_URL',  media_urls['card3.png'])

open(f'{WORKDIR}/article_final.html', 'w').write(html)
print('Final HTML length:', len(html))

# publish via driver
res = publish_post(
    html=html,
    slug='xlsx-freeze-pane-manager-field-guide-2026-08-12',
    title='XLSX Freeze Pane Manager Field Guide: Lock the Headers Without Clicking View 47 Times',
)
print('Publish result:')
print(json.dumps(res, indent=2))
