import requests
from bs4 import BeautifulSoup
import urllib.parse

base_url = "https://mojigeci.com"

# 测试一个歌词页面
song_url = f"{base_url}/lyrics/%E5%86%8D%E8%A6%8B%20Rainy%20Days"

print(f"=== Testing lyrics page ===")
print(f"URL: {song_url}")

r = requests.get(song_url, timeout=10)
soup = BeautifulSoup(r.text, 'lxml')

print(f"Status: {r.status_code}")
print(f"Title: {soup.find('title').text if soup.find('title') else 'No title'}")

# 查找歌词内容
print("\n=== Looking for lyrics content ===")

# 常见的歌词容器ID和class
lyrics_selectors = [
    {'id': 'lyrics'},
    {'id': 'fsZx3'},  # 旧网站使用的ID
    {'class': 'lyrics'},
    {'class': 'lyric-content'},
    {'class': 'song-lyrics'},
]

found_lyrics = False
for selector in lyrics_selectors:
    if 'id' in selector:
        element = soup.find(id=selector['id'])
    else:
        element = soup.find(class_=selector['class'])
    
    if element:
        print(f"Found lyrics in {selector}:")
        lyrics = element.get_text(strip=False)
        print(lyrics[:300])
        found_lyrics = True
        break

if not found_lyrics:
    # 查看所有div和pre标签
    print("Lyrics not found in common selectors. Checking all containers...")
    for tag in ['div', 'pre', 'p']:
        elements = soup.find_all(tag, class_=True)
        for elem in elements[:10]:
            text = elem.get_text(strip=True)
            if len(text) > 100 and '歌' in text:  # 可能是歌词
                classes = ' '.join(elem.get('class', []))
                print(f"\nPotential lyrics in <{tag} class='{classes}'>:")
                print(text[:200])

# 查找歌手和歌曲信息
print("\n=== Song metadata ===")
meta_tags = soup.find_all('meta')
for meta in meta_tags:
    if meta.get('property') or meta.get('name'):
        print(f"{meta.get('property') or meta.get('name')}: {meta.get('content', '')[:100]}")

