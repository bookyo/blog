WP 6197 asset URL pattern (2026-08-20):
- Uploaded: poster.png → poster-23.png (auto rename by WordPress)
- Actual URL: https://blog.flowrust.com/wp-content/uploads/2026/08/poster-23.png
- Initial HTML src: https://blog.flowrust.com/wp-content/uploads/poster-23.png (returns 404!)
- After PATCH: https://blog.flowrust.com/wp-content/uploads/2026/08/poster-23.png (200)

Defense for future runs:
- Use full source_url from media upload response, not just filename
- The WordPress REST API POST returns source_url with the date folder prefix
- HTML must use the full URL, not just /uploads/FILENAME
