"""
测试最终优化版 - 林夕的第一首歌
验证：
1. 去除重复元数据
2. 去除演唱会对话
3. 格式化输出
"""

import requests
from bs4 import BeautifulSoup
import re
import time
import os
from urllib.parse import urljoin

def extract_metadata(raw_text):
    """提取元数据（避免重复）"""
    metadata = {}
    lines = raw_text.split('\n')
    
    for line in lines[:30]:
        line = line.strip()
        if re.match(r'(作词|词)\s*[:：]\s*(.+)', line):
            match = re.match(r'(作词|词)\s*[:：]\s*(.+)', line)
            if '作词' not in metadata:
                metadata['作词'] = match.group(2).strip()
        elif re.match(r'(作曲|曲)\s*[:：]\s*(.+)', line):
            match = re.match(r'(作曲|曲)\s*[:：]\s*(.+)', line)
            if '作曲' not in metadata:
                metadata['作曲'] = match.group(2).strip()
        elif re.match(r'编曲\s*[:：]\s*(.+)', line):
            match = re.match(r'编曲\s*[:：]\s*(.+)', line)
            if '编曲' not in metadata:
                metadata['编曲'] = match.group(1).strip()
    
    return metadata

def clean_lyrics(raw_text):
    """清理歌词 - 去除重复和演唱会对话"""
    lines = raw_text.split('\n')
    lyrics_lines = []
    
    skip_keywords = [
        'English Version', '日本語版', '首页', '今日热门', '热门歌曲',
        'lrc/lyrics', 'txt 文档', '下载', '更多', '演唱：'
    ]
    
    skip_patterns = [
        r'观众[：:]',
        r'哥哥[：:]',
        r'我今天.*开心',
        r'不是因为',
    ]
    
    for line in lines:
        clean_line = re.sub(r'\[\d{2}:\d{2}\.\d{2,3}\]', '', line).strip()
        
        if not clean_line or clean_line.isdigit() or len(clean_line) == 1:
            continue
        
        if re.match(r'(作词|词|作曲|曲|编曲|后期)\s*[:：]', clean_line):
            continue
        
        if any(keyword in clean_line for keyword in skip_keywords):
            continue
        
        if any(re.search(pattern, clean_line) for pattern in skip_patterns):
            break
        
        if len(clean_line) >= 2:
            lyrics_lines.append(clean_line)
    
    return '\n'.join(lyrics_lines)

def format_output(song_name, singer, writer_name, metadata, lyrics):
    """格式化输出"""
    output = []
    output.append(f"歌名：{song_name}")
    output.append(f"演唱：{singer}")
    output.append(f"作词：{writer_name}")
    
    if '作曲' in metadata:
        output.append(f"作曲：{metadata['作曲']}")
    if '编曲' in metadata:
        output.append(f"编曲：{metadata['编曲']}")
    
    output.append('')
    output.append('='*40)
    output.append('')
    output.append(lyrics)
    
    return '\n'.join(output)

# 测试
print("=== 测试最终优化版 ===\n")

song_url = "https://www.kugeci.com/writer/Tb1woIQI"
print("1. 获取林夕的第一首歌...\n")

time.sleep(2)
r = requests.get(song_url, timeout=10)
soup = BeautifulSoup(r.text, 'lxml')

table = soup.find('table', {'id': 'tablesort'})
if table:
    row = table.find_all('tr')[1]
    cells = row.find_all('td')
    
    song_name = cells[1].find('a').get_text(strip=True)
    singer = cells[2].get_text(strip=True)
    href = cells[1].find('a')['href']
    song_url = href if href.startswith('http') else f"https://www.kugeci.com{href}"
    
    print(f"歌曲：{singer} - {song_name}")
    print(f"URL：{song_url}\n")
    
    time.sleep(2)
    sr = requests.get(song_url, timeout=10)
    ssoup = BeautifulSoup(sr.text, 'lxml')
    
    # 提取原始内容
    raw_lyrics = ""
    for elem in ssoup.find_all(['div', 'pre']):
        text = elem.get_text(strip=False)
        if '[00:' in text and len(text) > 100:
            raw_lyrics = text
            break
    
    if raw_lyrics:
        print("2. 处理结果对比\n")
        
        # 统计
        lines_before = len(raw_lyrics.split('\n'))
        
        # 处理
        metadata = extract_metadata(raw_lyrics)
        clean = clean_lyrics(raw_lyrics)
        final = format_output(song_name, singer, "林夕", metadata, clean)
        
        lines_after = len(final.split('\n'))
        
        print(f"原始行数：{lines_before}")
        print(f"处理后行数：{lines_after}")
        print(f"减少比例：{(lines_before-lines_after)/lines_before*100:.1f}%\n")
        
        print("3. 元数据提取")
        for key, value in metadata.items():
            print(f"   {key}：{value}")
        
        # 保存
        output_dir = "test_final_output"
        os.makedirs(output_dir, exist_ok=True)
        filename = os.path.join(output_dir, f"{singer} - {song_name}.txt")
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(final)
        
        print(f"\n✓ 已保存到：{filename}")
        print("\n4. 文件预览（前15行）")
        print("-" * 40)
        for i, line in enumerate(final.split('\n')[:15], 1):
            print(f"{i:2}. {line}")
        print("   ...")

print("\n=== 测试完成 ===")

