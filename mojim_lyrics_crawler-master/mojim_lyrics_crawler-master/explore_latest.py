import requests
from bs4 import BeautifulSoup
import json

base_url = "https://mojigeci.com"

# 探索最新歌曲页面
print("=== Exploring /list?sort=latest page ===")
r = requests.get(f"{base_url}/list?sort=latest", timeout=10)
soup = BeautifulSoup(r.text, 'lxml')
print(f"Status: {r.status_code}")
print(f"Title: {soup.find('title').text if soup.find('title') else 'No title'}")

# 查看页面中的歌曲信息
print("\n=== Looking for song entries ===")

# 常见的歌曲信息容器标签
containers = ['div', 'article', 'li', 'tr', 'section']
for tag_name in containers:
    items = soup.find_all(tag_name, class_=True, limit=5)
    if items:
        print(f"\nFound {tag_name} elements:")
        for i, item in enumerate(items[:3]):
            classes = ' '.join(item.get('class', []))
            text = item.get_text(strip=True)[:100]
            print(f"  [{i}] class='{classes}' text='{text}'")

# 查找所有歌曲链接
print("\n=== Song links ===")
links = soup.find_all('a', href=True)
song_links = []
for link in links[:50]:
    href = link.get('href', '')
    text = link.get_text(strip=True)
    # 歌词页面通常包含特定模式
    if href and text and len(text) > 2:
        song_links.append({'text': text, 'href': href})

print(f"Found {len(song_links)} potential song links (showing first 10):")
for link in song_links[:10]:
    print(f"  {link['text']}: {link['href']}")

# 查看是否有日期/年份筛选
print("\n=== Looking for date filters ===")
selects = soup.find_all('select')
for select in selects:
    print(f"Select element: {select.get('name', 'no-name')}")
    options = select.find_all('option')
    for opt in options[:10]:
        print(f"  - {opt.get_text(strip=True)}: {opt.get('value', '')}")

