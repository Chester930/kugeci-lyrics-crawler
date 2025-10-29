"""
测试完美版 - 验证格式标准
标准：
1. 第一行：歌名
2. 第二行：作词（或词）
3. 继续内容
4. 遇到第二次"作词"或"词"停止
"""

import requests
from bs4 import BeautifulSoup
import re
import time
import os

def clean_perfect(raw_text, song_name, singer, writer_name):
    """根据用户标准清理"""
    lines = raw_text.split('\n')
    output = []
    metadata_count = 0
    in_metadata = True
    
    # 第一行：歌名
    output.append(f"歌名：{song_name}")
    output.append(f"演唱：{singer}")
    
    for line in lines:
        clean_line = re.sub(r'\[\d{2}:\d{2}\.\d{2,3}\]', '', line).strip()
        
        if not clean_line:
            continue
        
        # 检查"作词"或"词："
        if re.search(r'(作词|^词)\s*[:：]', clean_line):
            metadata_count += 1
            if metadata_count > 1:
                print(f"   ⚠️  检测到第{metadata_count}次出现'作词'，停止处理")
                break
            output.append(clean_line)
            continue
        
        # 其他元数据
        if in_metadata and re.match(r'(作曲|曲|编曲|后期|监制|制作)\s*[:：]', clean_line):
            output.append(clean_line)
            continue
        
        # 跳过网页元素
        skip = ['English Version', '日本語版', '首页', '热门歌曲', 
                'txt 文档', '下载', '演唱：', '歌手：']
        if any(k in clean_line for k in skip):
            continue
        
        if clean_line.isdigit() or len(clean_line) == 1:
            continue
        
        if clean_line == song_name:
            continue
        
        # 进入歌词部分
        if not re.match(r'(作词|词|作曲|曲|编曲)\s*[:：]', clean_line):
            if in_metadata and len(clean_line) > 5:
                if output and not output[-1].startswith('='):
                    output.append('')
                    output.append('='*40)
                    output.append('')
                in_metadata = False
        
        if not in_metadata and len(clean_line) >= 2:
            output.append(clean_line)
    
    return '\n'.join(output)

# 测试林夕的第一首歌
print("=== 测试完美版格式 ===\n")

writer_url = "https://www.kugeci.com/writer/Tb1woIQI"
print("1. 获取林夕的第一首歌\n")

time.sleep(2)
r = requests.get(writer_url, timeout=10)
soup = BeautifulSoup(r.text, 'lxml')

table = soup.find('table', {'id': 'tablesort'})
if table:
    row = table.find_all('tr')[1]
    cells = row.find_all('td')
    
    song_name = cells[1].find('a').get_text(strip=True)
    singer = cells[2].get_text(strip=True)
    href = cells[1].find('a')['href']
    song_url = href if href.startswith('http') else f"https://www.kugeci.com{href}"
    
    print(f"歌曲：{singer} - {song_name}\n")
    
    time.sleep(2)
    sr = requests.get(song_url, timeout=10)
    ssoup = BeautifulSoup(sr.text, 'lxml')
    
    raw_lyrics = ""
    for elem in ssoup.find_all(['div', 'pre']):
        text = elem.get_text(strip=False)
        if '[00:' in text and len(text) > 100:
            raw_lyrics = text
            break
    
    if raw_lyrics:
        print("2. 处理结果\n")
        
        lines_before = len(raw_lyrics.split('\n'))
        result = clean_perfect(raw_lyrics, song_name, singer, "林夕")
        lines_after = len(result.split('\n'))
        
        print(f"原始行数：{lines_before}")
        print(f"处理后：{lines_after}")
        print(f"减少：{(lines_before-lines_after)/lines_before*100:.1f}%\n")
        
        # 保存
        os.makedirs("test_perfect", exist_ok=True)
        filename = f"test_perfect/{singer} - {song_name}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(result)
        
        print(f"✓ 已保存：{filename}\n")
        print("3. 文件格式验证（前15行）")
        print("-" * 40)
        for i, line in enumerate(result.split('\n')[:15], 1):
            print(f"{i:2}. {line}")
        print(f"\n   ...（共{lines_after}行）")

print("\n=== 测试完成 ===")

