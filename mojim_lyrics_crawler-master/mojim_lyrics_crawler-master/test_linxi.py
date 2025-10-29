"""
测试林夕的前两首歌 - 验证清洁版爬虫
"""

import requests
from bs4 import BeautifulSoup
import re
import time
import os
from urllib.parse import urljoin

base_url = "https://www.kugeci.com"
output_dir = "test_linxi"
os.makedirs(output_dir, exist_ok=True)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

def safe_filename(name):
    return re.sub(r'[<>:"/\\|?*]', '_', name)[:100]

def clean_lyrics(raw_text):
    """智能清理歌词"""
    lines = raw_text.split('\n')
    clean_lines = []
    
    skip_keywords = [
        'English Version', '日本語版', '首页', '今日热门', '热门歌曲', 
        '最新歌曲', '歌手', 'lrc/lyrics', 'txt 文档', '下载lyrics', 
        '下载txt', '更多', '歌手最新歌曲', '歌手热门歌曲', '最近30天', 
        '点击:', '收录:', '演唱：', 'Get it on', 'Google Play',
        'Copyright', '联系我们', 'Privacy Policy'
    ]
    
    for line in lines:
        clean_line = re.sub(r'\[\d{2}:\d{2}\.\d{2,3}\]', '', line).strip()
        
        if not clean_line or clean_line.isdigit() or len(clean_line) == 1:
            continue
        
        if any(keyword in clean_line for keyword in skip_keywords):
            continue
        
        if len(clean_line) > 2:
            clean_lines.append(clean_line)
    
    return '\n'.join(clean_lines)

print("=== 测试林夕作词人 ===\n")

# 林夕的页面
writer_url = "https://www.kugeci.com/writer/Tb1woIQI"
writer_name = "林夕"

print(f"1. 访问林夕的作词人页面")
print(f"   URL: {writer_url}\n")

time.sleep(2)

try:
    r = requests.get(writer_url, headers=headers, timeout=15)
    print(f"   状态码: {r.status_code}\n")
    
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'lxml')
        
        # 从表格提取歌曲
        print("2. 提取歌曲列表")
        table = soup.find('table', {'class': 'table'}) or soup.find('table', {'id': 'tablesort'})
        
        if table:
            songs = []
            rows = table.find_all('tr')[1:][:2]  # 只取前2行
            
            for row in rows:
                cells = row.find_all('td')
                if len(cells) >= 4:
                    date = cells[0].get_text(strip=True)
                    song_link = cells[1].find('a')
                    singer = cells[2].get_text(strip=True)
                    composer = cells[3].get_text(strip=True)
                    
                    if song_link:
                        songs.append({
                            'date': date,
                            'song_name': song_link.get_text(strip=True),
                            'singer': singer,
                            'composer': composer,
                            'url': urljoin(base_url, song_link['href'])
                        })
            
            print(f"   找到 {len(songs)} 首歌曲（前2首）\n")
            
            # 下载歌词
            writer_dir = os.path.join(output_dir, safe_filename(writer_name))
            os.makedirs(writer_dir, exist_ok=True)
            
            for idx, song in enumerate(songs, 1):
                full_title = f"{song['singer']} - {song['song_name']}"
                print(f"{idx}. 下载: {full_title}")
                print(f"   发布: {song['date']}")
                print(f"   作曲: {song['composer']}")
                
                time.sleep(2)
                
                # 获取歌词
                sr = requests.get(song['url'], headers=headers, timeout=10)
                ssoup = BeautifulSoup(sr.text, 'lxml')
                
                raw_lyrics = ""
                for elem in ssoup.find_all(['div', 'pre']):
                    text = elem.get_text(strip=False)
                    if '[00:' in text and len(text) > 100:
                        if len(text) > len(raw_lyrics):
                            raw_lyrics = text
                
                if raw_lyrics:
                    # 清理歌词
                    clean = clean_lyrics(raw_lyrics)
                    
                    # 统计
                    lines_before = len(raw_lyrics.split('\n'))
                    lines_after = len(clean.split('\n'))
                    
                    # 保存
                    filename = os.path.join(writer_dir, f"{safe_filename(full_title)}.txt")
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(clean)
                    
                    print(f"   ✓ 已保存")
                    print(f"   原始: {lines_before}行 → 清理后: {lines_after}行")
                    print(f"   文件: {filename}")
                else:
                    print(f"   ✗ 未找到歌词")
                
                print()
        else:
            print("   ✗ 未找到歌曲表格")
    else:
        print(f"   ✗ 请求失败")
        
except Exception as e:
    print(f"   ✗ 错误: {e}")

print("=== 测试完成 ===")
print(f"\n输出目录: {output_dir}/{writer_name}/")

