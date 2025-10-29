"""
酷歌词爬虫 - 小规模测试版
测试：第1页的前2个作词人，每人最多3首歌
"""

import requests
from bs4 import BeautifulSoup
import time
import os
import re
from urllib.parse import urljoin

base_url = "https://www.kugeci.com"
output_dir = "test_lyrics"
os.makedirs(output_dir, exist_ok=True)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

def safe_filename(name):
    """创建安全的文件名"""
    return re.sub(r'[<>:"/\\|?*]', '_', name)[:100]

print("=== 测试爬取 ===\n")

# 1. 获取第1页作词人
print("1. 获取第1页作词人列表...")
r = requests.get(f"{base_url}/writers?page=1", headers=headers, timeout=10)
soup = BeautifulSoup(r.text, 'lxml')

writers = []
for link in soup.find_all('a', href=True):
    if '/writer/' in link.get('href', ''):
        name = link.get_text(strip=True)
        if name:
            writers.append({
                'name': name,
                'url': urljoin(base_url, link['href'])
            })

# 去重并只取前2个
unique_writers = list({w['url']: w for w in writers}.values())[:2]
print(f"   找到 {len(unique_writers)} 个作词人（测试）\n")

# 2. 遍历作词人
for writer in unique_writers:
    writer_name = safe_filename(writer['name'])
    writer_dir = os.path.join(output_dir, f"page_1/{writer_name}")
    os.makedirs(writer_dir, exist_ok=True)
    
    print(f"2. 处理作词人: {writer['name']}")
    time.sleep(1.5)
    
    # 获取歌曲列表
    r = requests.get(writer['url'], headers=headers, timeout=10)
    soup = BeautifulSoup(r.text, 'lxml')
    
    songs = []
    for link in soup.find_all('a', href=True):
        if '/song/' in link.get('href', ''):
            title = link.get_text(strip=True)
            if title and ' - ' in title:
                songs.append({
                    'title': title,
                    'url': urljoin(base_url, link['href'])
                })
    
    # 去重并只取前3首
    unique_songs = list({s['url']: s for s in songs}.values())[:3]
    print(f"   找到 {len(unique_songs)} 首歌曲（测试）\n")
    
    # 3. 下载歌词
    for song in unique_songs:
        print(f"   下载: {song['title']}")
        time.sleep(1.5)
        
        r = requests.get(song['url'], headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, 'lxml')
        
        # 查找歌词
        lyrics_text = ""
        for elem in soup.find_all(['div', 'pre']):
            text = elem.get_text(strip=False)
            if '[00:' in text and len(text) > 100:
                lyrics_text = text
                break
        
        if lyrics_text:
            # 清理并保存
            lines = [re.sub(r'\[\d{2}:\d{2}\.\d{2}\]', '', line).strip() 
                     for line in lyrics_text.split('\n')]
            clean_lyrics = '\n'.join(line for line in lines if line)
            
            filename = os.path.join(writer_dir, f"{safe_filename(song['title'])}.txt")
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(clean_lyrics)
            print(f"      ✓ 已保存到: {filename}")
        else:
            print(f"      ✗ 未找到歌词")
    
    print()

print("=== 测试完成 ===")
print(f"输出目录: {output_dir}/page_1/")

