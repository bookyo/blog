import importlib.util
for mod in ['requests', 'httpx', 'urllib3', 'aiohttp']:
    spec = importlib.util.find_spec(mod)
    print(f"{mod}: {'available' if spec else 'NOT available'}")
