import requests
from bs4 import BeautifulSoup
import re

base_url = "https://mojigeci.com"

# 获取页面源代码
print("=== Analyzing page source ===")
r = requests.get(f"{base_url}/list?sort=latest", timeout=10)
html = r.text

# 查找可能的API端点
print("\n=== Looking for API endpoints ===")
api_patterns = [
    r'api[./][a-zA-Z0-9/_.-]+',
    r'/data/[a-zA-Z0-9/_.-]+',
    r'fetch\(["\']([^"\']+)["\']',
    r'axios\.[a-z]+\(["\']([^"\']+)["\']',
]

for pattern in api_patterns:
    matches = re.findall(pattern, html, re.IGNORECASE)
    if matches:
        print(f"Pattern '{pattern}' found {len(set(matches))} unique matches:")
        for match in list(set(matches))[:5]:
            print(f"  - {match}")

# 查找JSON数据
print("\n=== Looking for embedded JSON data ===")
json_patterns = [
    r'<script[^>]*>.*?window\.__INITIAL_STATE__\s*=\s*({.*?});',
    r'<script[^>]*>.*?var\s+data\s*=\s*({.*?});',
    r'<script type="application/json"[^>]*>(.*?)</script>',
]

for pattern in json_patterns:
    matches = re.findall(pattern, html, re.DOTALL)
    if matches:
        print(f"Found embedded JSON data:")
        for match in matches[:2]:
            print(f"  Length: {len(match)} chars")
            print(f"  Preview: {match[:200]}...")

# 查看script标签
print("\n=== Analyzing script tags ===")
soup = BeautifulSoup(html, 'lxml')
scripts = soup.find_all('script', src=True)
print(f"Found {len(scripts)} external scripts:")
for script in scripts[:10]:
    src = script.get('src', '')
    print(f"  - {src}")

# 尝试查找特定的URL模式
print("\n=== Looking for song URL patterns ===")
url_patterns = re.findall(r'href=["\']([^"\']*(?:song|lyric|tw)[^"\']*)["\']', html, re.IGNORECASE)
unique_patterns = list(set(url_patterns))
if unique_patterns:
    print(f"Found {len(unique_patterns)} unique URL patterns with 'song/lyric/tw':")
    for url in unique_patterns[:15]:
        print(f"  - {url}")

