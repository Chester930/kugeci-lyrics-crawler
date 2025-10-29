"""
测试方文山的第一首歌 - 验证清理效果
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
        elif re.match(r'制作人\s*[:：]\s*(.+)', line):
            match = re.match(r'制作人\s*[:：]\s*(.+)', line)
            if '制作人' not in metadata:
                metadata['制作人'] = match.group(1).strip()
    
    return metadata

def clean_lyrics(raw_text):
    """清理歌词"""
    lines = raw_text.split('\n')
    lyrics_lines = []
    
    skip_keywords = [
        'English Version', '日本語版', '首页', '今日热门', '热门歌曲',
        'lrc/lyrics', 'txt 文档', '下载', '更多', '演唱：', '歌手：',
        'Get it on', 'Google Play', 'Copyright', '最新歌曲'
    ]
    
    skip_patterns = [
        r'观众[：:]',
        r'哥哥[：:]',
    ]
    
    for line in lines:
        clean_line = re.sub(r'\[\d{2}:\d{2}\.\d{2,3}\]', '', line).strip()
        
        if not clean_line or clean_line.isdigit() or len(clean_line) == 1:
            continue
        
        # 跳过元数据行
        if re.match(r'(作词|词|作曲|曲|编曲|后期|监制|制作)\s*[:：]', clean_line):
            continue
        
        # 跳过网页元素
        if any(keyword in clean_line for keyword in skip_keywords):
            continue
        
        # 跳过演唱会对话
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
    if '制作人' in metadata:
        output.append(f"制作人：{metadata['制作人']}")
    
    output.append('')
    output.append('='*40)
    output.append('')
    output.append(lyrics)
    
    return '\n'.join(output)

# 测试
print("=== 测试方文山作词人 ===\n")

# 方文山的页面 URL
writer_url = "https://www.kugeci.com/writer/WQY6QJC3"
writer_name = "方文山"

print(f"1. 访问方文山的作词人页面")
print(f"   URL: {writer_url}\n")

time.sleep(2)

try:
    r = requests.get(writer_url, timeout=15)
    print(f"   状态码: {r.status_code}\n")
    
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'lxml')
        
        # 从表格提取第一首歌
        print("2. 提取第一首歌曲")
        table = soup.find('table', {'class': 'table'}) or soup.find('table', {'id': 'tablesort'})
        
        if table:
            row = table.find_all('tr')[1]  # 第一首歌（跳过表头）
            cells = row.find_all('td')
            
            if len(cells) >= 4:
                date = cells[0].get_text(strip=True)
                song_link = cells[1].find('a')
                singer = cells[2].get_text(strip=True)
                composer = cells[3].get_text(strip=True)
                
                if song_link:
                    song_name = song_link.get_text(strip=True)
                    href = song_link['href']
                    song_url = href if href.startswith('http') else f"https://www.kugeci.com{href}"
                    
                    full_title = f"{singer} - {song_name}"
                    print(f"   歌曲：{full_title}")
                    print(f"   发布：{date}")
                    print(f"   作曲：{composer}")
                    print(f"   URL：{song_url}\n")
                    
                    time.sleep(2)
                    
                    # 下载歌词
                    print("3. 下载并处理歌词")
                    sr = requests.get(song_url, timeout=10)
                    ssoup = BeautifulSoup(sr.text, 'lxml')
                    
                    raw_lyrics = ""
                    for elem in ssoup.find_all(['div', 'pre']):
                        text = elem.get_text(strip=False)
                        if '[00:' in text and len(text) > 100:
                            if len(text) > len(raw_lyrics):
                                raw_lyrics = text
                    
                    if raw_lyrics:
                        # 处理
                        lines_before = len(raw_lyrics.split('\n'))
                        metadata = extract_metadata(raw_lyrics)
                        clean = clean_lyrics(raw_lyrics)
                        final = format_output(song_name, singer, writer_name, metadata, clean)
                        lines_after = len(final.split('\n'))
                        
                        print(f"   原始行数：{lines_before}")
                        print(f"   处理后行数：{lines_after}")
                        print(f"   减少比例：{(lines_before-lines_after)/lines_before*100:.1f}%\n")
                        
                        print("4. 元数据提取")
                        print(f"   作词：{writer_name}")
                        for key, value in metadata.items():
                            if key != '作词':
                                print(f"   {key}：{value}")
                        
                        # 保存
                        output_dir = "test_fangwenshan"
                        os.makedirs(output_dir, exist_ok=True)
                        filename = os.path.join(output_dir, f"{singer} - {song_name}.txt")
                        
                        with open(filename, 'w', encoding='utf-8') as f:
                            f.write(final)
                        
                        print(f"\n✓ 已保存到：{filename}")
                        print(f"\n5. 文件格式验证")
                        print("-" * 40)
                        header_lines = final.split('\n')[:10]
                        for i, line in enumerate(header_lines, 1):
                            print(f"{i:2}. {line}")
                        print("   ...")
                        print(f"\n   总行数：{lines_after}")
                    else:
                        print("   ✗ 未找到歌词")
        else:
            print("   ✗ 未找到歌曲表格")
    else:
        print(f"   ✗ 请求失败")
        
except Exception as e:
    print(f"   ✗ 错误: {e}")

print("\n=== 测试完成 ===")

