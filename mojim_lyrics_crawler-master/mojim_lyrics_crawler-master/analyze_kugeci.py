import requests
from bs4 import BeautifulSoup
import json

base_url = "https://www.kugeci.com"

print("=== 分析酷歌词网站结构 ===\n")

# 1. 分析首页
print("1. 首页分析")
r = requests.get(base_url, timeout=10)
soup = BeautifulSoup(r.text, 'lxml')
print(f"   状态: {r.status_code}")
print(f"   标题: {soup.find('title').text if soup.find('title') else 'No title'}\n")

# 2. 测试不同的列表页面
print("2. 测试各种列表页面")
test_pages = [
    '/songs/new',      # 最新歌曲
    '/songs/hot',      # 热门歌曲
    '/songs/today',    # 今日热门
    '/writers',        # 作词人列表
    '/composers',      # 作曲人列表
    '/artists',        # 歌手列表
    '/singers',        # 歌手列表（另一种可能）
]

available_pages = []
for page in test_pages:
    try:
        r = requests.get(base_url + page, timeout=5)
        if r.status_code == 200:
            print(f"   ✓ {page} - 可访问")
            available_pages.append(page)
        else:
            print(f"   ✗ {page} - {r.status_code}")
    except Exception as e:
        print(f"   ✗ {page} - Error: {type(e).__name__}")

# 3. 分析作词人页面
print("\n3. 分析作词人页面结构")
r = requests.get(f"{base_url}/writers", timeout=10)
soup = BeautifulSoup(r.text, 'lxml')

# 查找作词人链接
writer_links = []
for link in soup.find_all('a', href=True):
    href = link.get('href', '')
    if '/writer/' in href:
        text = link.get_text(strip=True)
        writer_links.append({'name': text, 'url': href})

print(f"   找到 {len(writer_links)} 个作词人链接")
if writer_links:
    print("   前5个作词人:")
    for i, writer in enumerate(writer_links[:5]):
        print(f"     {i+1}. {writer['name']}: {writer['url']}")

# 4. 测试具体作词人页面
if writer_links:
    print("\n4. 测试具体作词人页面")
    test_writer = writer_links[0]
    writer_url = base_url + test_writer['url'] if not test_writer['url'].startswith('http') else test_writer['url']
    print(f"   测试: {test_writer['name']} - {writer_url}")
    
    r = requests.get(writer_url, timeout=10)
    soup = BeautifulSoup(r.text, 'lxml')
    
    # 查找歌曲列表
    song_links = []
    for link in soup.find_all('a', href=True):
        href = link.get('href', '')
        if '/song/' in href or '/lyric/' in href:
            text = link.get_text(strip=True)
            if text and len(text) > 1:
                song_links.append({'title': text, 'url': href})
    
    print(f"   找到 {len(song_links)} 个歌曲链接")
    if song_links:
        print("   前5首歌曲:")
        for i, song in enumerate(song_links[:5]):
            print(f"     {i+1}. {song['title']}: {song['url']}")

# 5. 测试歌曲页面
if song_links:
    print("\n5. 测试歌曲页面结构")
    test_song = song_links[0]
    song_url = base_url + test_song['url'] if not test_song['url'].startswith('http') else test_song['url']
    print(f"   测试: {test_song['title']} - {song_url}")
    
    try:
        r = requests.get(song_url, timeout=10)
        soup = BeautifulSoup(r.text, 'lxml')
        print(f"   状态: {r.status_code}")
        
        # 查找歌词容器
        for selector in ['lyrics', 'lyric-content', 'song-lyrics', 'content']:
            elem = soup.find(class_=selector) or soup.find(id=selector)
            if elem:
                print(f"   ✓ 找到歌词容器: class/id='{selector}'")
                lyrics_preview = elem.get_text(strip=True)[:100]
                print(f"   歌词预览: {lyrics_preview}")
                break
    except Exception as e:
        print(f"   ✗ 错误: {e}")

print("\n=== 分析完成 ===")

