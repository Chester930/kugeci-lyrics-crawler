import requests
from bs4 import BeautifulSoup
import json

base_url = "https://www.kugeci.com"

# 测试一个歌曲页面
song_url = f"{base_url}/song/a64WYn9U"

print("=== 分析酷歌词歌曲页面 ===")
print(f"URL: {song_url}\n")

r = requests.get(song_url, timeout=10)
soup = BeautifulSoup(r.text, 'lxml')

print(f"状态码: {r.status_code}")
print(f"页面标题: {soup.find('title').text if soup.find('title') else 'No title'}\n")

# 1. 查找歌曲元数据
print("1. 歌曲元数据")
meta_tags = soup.find_all('meta')
metadata = {}
for meta in meta_tags:
    prop = meta.get('property') or meta.get('name')
    content = meta.get('content')
    if prop and content:
        print(f"   {prop}: {content[:100]}")
        metadata[prop] = content

# 2. 查找歌曲信息（标题、歌手、作词、作曲等）
print("\n2. 页面中的歌曲信息")
# 查找所有文本较长的元素
info_elements = soup.find_all(['h1', 'h2', 'h3', 'div', 'p', 'span'])
for elem in info_elements[:30]:
    text = elem.get_text(strip=True)
    classes = ' '.join(elem.get('class', []))
    if text and len(text) > 3 and len(text) < 100:
        if any(keyword in text for keyword in ['作词', '作曲', '演唱', '歌手', '专辑']):
            print(f"   <{elem.name} class='{classes}'>: {text}")

# 3. 查找歌词内容
print("\n3. 查找歌词内容")
found_lyrics = False

# 尝试常见的选择器
selectors = [
    ('id', 'lyrics'),
    ('class', 'lyrics'),
    ('class', 'lyric-content'),
    ('class', 'song-lyrics'),
    ('class', 'lyrics-container'),
    ('class', 'content'),
]

for selector_type, selector_value in selectors:
    if selector_type == 'id':
        element = soup.find(id=selector_value)
    else:
        element = soup.find(class_=selector_value)
    
    if element:
        lyrics = element.get_text(strip=False)
        if len(lyrics) > 50:
            print(f"   ✓ 在 {selector_type}='{selector_value}' 找到歌词")
            print(f"   歌词长度: {len(lyrics)} 字符")
            print(f"   歌词预览:\n{lyrics[:300]}\n")
            found_lyrics = True
            break

if not found_lyrics:
    print("   未在常见选择器中找到歌词，分析所有文本块...")
    # 查找包含大量文本的元素
    text_blocks = []
    for elem in soup.find_all(['div', 'pre', 'p']):
        text = elem.get_text(strip=True)
        if len(text) > 100:
            text_blocks.append({
                'tag': elem.name,
                'class': ' '.join(elem.get('class', [])),
                'id': elem.get('id', ''),
                'length': len(text),
                'preview': text[:150]
            })
    
    text_blocks.sort(key=lambda x: x['length'], reverse=True)
    print(f"   找到 {len(text_blocks)} 个大文本块（前3个）:")
    for i, block in enumerate(text_blocks[:3]):
        print(f"\n   [{i+1}] <{block['tag']} class='{block['class']}' id='{block['id']}'>")
        print(f"       长度: {block['length']} 字符")
        print(f"       预览: {block['preview']}")

# 4. 查找相关歌曲链接
print("\n4. 页面中的其他链接")
links = soup.find_all('a', href=True)
song_links = [link for link in links if '/song/' in link.get('href', '')]
writer_links = [link for link in links if '/writer/' in link.get('href', '')]
singer_links = [link for link in links if '/singer/' in link.get('href', '')]

print(f"   歌曲链接: {len(song_links)} 个")
print(f"   作词人链接: {len(writer_links)} 个")
print(f"   歌手链接: {len(singer_links)} 个")

print("\n=== 分析完成 ===")

