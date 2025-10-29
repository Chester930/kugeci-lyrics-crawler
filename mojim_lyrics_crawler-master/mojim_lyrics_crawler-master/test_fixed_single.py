"""
测试修复后的爬虫 - 直接测试李奎页面
"""

import requests
from bs4 import BeautifulSoup
import time
import os
import re
from urllib.parse import urljoin

base_url = "https://www.kugeci.com"
output_dir = "test_fixed"
os.makedirs(output_dir, exist_ok=True)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

def safe_filename(name):
    return re.sub(r'[<>:"/\\|?*]', '_', name)[:100]

print("=== 测试修复后的爬虫 ===\n")

# 直接测试李奎的页面
writer_url = "https://www.kugeci.com/writer/N3vdNEOq"
writer_name = "李奎"

print(f"1. 访问作词人页面: {writer_name}")
print(f"   URL: {writer_url}\n")

time.sleep(2)  # 等待2秒

try:
    r = requests.get(writer_url, headers=headers, timeout=15)
    print(f"   状态码: {r.status_code}")
    
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'lxml')
        
        # 从表格中提取歌曲
        print("\n2. 从表格中提取歌曲列表")
        table = soup.find('table', {'class': 'table'}) or soup.find('table', {'id': 'tablesort'})
        
        if table:
            print("   ✓ 找到歌曲表格")
            songs = []
            
            rows = table.find_all('tr')[1:]  # 跳过表头
            print(f"   表格行数: {len(rows)}")
            
            for row in rows:
                cells = row.find_all('td')
                if len(cells) >= 4:
                    # 提取信息
                    date = cells[0].get_text(strip=True)
                    song_link = cells[1].find('a')
                    singer = cells[2].get_text(strip=True)
                    composer = cells[3].get_text(strip=True)
                    
                    if song_link:
                        song_name = song_link.get_text(strip=True)
                        song_url = urljoin(base_url, song_link['href'])
                        
                        songs.append({
                            'date': date,
                            'song_name': song_name,
                            'singer': singer,
                            'composer': composer,
                            'url': song_url
                        })
                        
                        print(f"\n   歌曲 {len(songs)}:")
                        print(f"     发布日期: {date}")
                        print(f"     歌名: {song_name}")
                        print(f"     歌手: {singer}")
                        print(f"     作曲: {composer}")
                        print(f"     URL: {song_url}")
            
            print(f"\n   总计: {len(songs)} 首歌曲")
            
            # 下载歌词
            if songs:
                print("\n3. 下载歌词")
                writer_dir = os.path.join(output_dir, safe_filename(writer_name))
                os.makedirs(writer_dir, exist_ok=True)
                
                for song in songs:
                    print(f"\n   处理: {song['singer']} - {song['song_name']}")
                    time.sleep(2)
                    
                    # 获取歌词
                    sr = requests.get(song['url'], headers=headers, timeout=10)
                    ssoup = BeautifulSoup(sr.text, 'lxml')
                    
                    lyrics_text = ""
                    for elem in ssoup.find_all(['div', 'pre']):
                        text = elem.get_text(strip=False)
                        if '[00:' in text and len(text) > 100:
                            lyrics_text = text
                            break
                    
                    if lyrics_text:
                        # 清理歌词
                        lines = [re.sub(r'\[\d{2}:\d{2}\.\d{2,3}\]', '', line).strip() 
                                 for line in lyrics_text.split('\n')]
                        clean_lyrics = '\n'.join(line for line in lines if line)
                        
                        # 添加元数据
                        metadata = f"歌名: {song['song_name']}\n"
                        metadata += f"演唱: {song['singer']}\n"
                        metadata += f"作词: {writer_name}\n"
                        metadata += f"作曲: {song['composer']}\n"
                        metadata += f"发布: {song['date']}\n"
                        metadata += f"\n{'='*40}\n\n"
                        
                        full_content = metadata + clean_lyrics
                        
                        # 保存
                        filename = os.path.join(writer_dir, f"{safe_filename(song['singer'])} - {safe_filename(song['song_name'])}.txt")
                        with open(filename, 'w', encoding='utf-8') as f:
                            f.write(full_content)
                        print(f"     ✓ 已保存: {filename}")
                    else:
                        print(f"     ✗ 未找到歌词")
        else:
            print("   ✗ 未找到歌曲表格")
            
    else:
        print(f"   ✗ 请求失败: {r.status_code}")
        
except Exception as e:
    print(f"   ✗ 错误: {e}")

print("\n=== 测试完成 ===")

