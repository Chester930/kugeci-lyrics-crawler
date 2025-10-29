import requests
from bs4 import BeautifulSoup

# 测试新网站结构
base_url = "https://mojigeci.com"

# 测试首页
print("=== Testing Homepage ===")
r = requests.get(base_url, timeout=10)
soup = BeautifulSoup(r.text, 'lxml')
print(f"Status: {r.status_code}")
print(f"Title: {soup.find('title').text if soup.find('title') else 'No title'}")

# 查找主要链接
print("\n=== Finding main navigation links ===")
links = soup.find_all('a', href=True)
relevant_links = []
for link in links[:50]:  # 只看前50个链接
    href = link.get('href', '')
    text = link.get_text(strip=True)
    if 'list' in href.lower() or '2024' in href or '2023' in href:
        relevant_links.append(f"{text}: {href}")

for link in relevant_links[:10]:
    print(link)

# 尝试不同的URL格式
print("\n=== Testing different URL formats ===")
test_urls = [
    f"{base_url}/twzlist2024-01.htm",
    f"{base_url}/twlist2024-01.htm",
    f"{base_url}/tw/zlist2024-01.htm",
    f"{base_url}/songlist-2024-01.htm",
    f"{base_url}/zlist/2024-01",
    f"{base_url}/new/2024-01",
]

for url in test_urls:
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            print(f"✓ FOUND: {url} - {r.status_code}")
        else:
            print(f"✗ {url} - {r.status_code}")
    except Exception as e:
        print(f"✗ {url} - Error: {type(e).__name__}")

