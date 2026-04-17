#!/bin/bash
# Test connectivity
echo "=== Testing dev.to connectivity ==="
curl -s --max-time 10 -I "https://dev.to" 2>&1 | head -5
echo ""
echo "=== Testing API GET ==="
curl -s --max-time 10 "https://api.dev.to/articles?username=elysiatools&per_page=1" 2>&1 | head -100
echo ""
echo "=== Testing API POST (should fail auth) ==="
curl -s --max-time 10 -X POST "https://api.dev.to/articles" \
  -H "Content-Type: application/json" \
  -H "Api-Key: YLAoSq6MdnbmRk26QZkvc2mx" \
  -d '{"article":{"title":"test"}}' 2>&1 | head -100
