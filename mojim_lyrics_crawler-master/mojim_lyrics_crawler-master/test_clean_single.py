"""
测试清洁版歌词提取 - 单曲测试
"""

import requests
from bs4 import BeautifulSoup
import re
import time

def clean_lyrics(raw_text):
    """智能清理歌词"""
    lines = raw_text.split('\n')
    clean_lines = []
    
    # 过滤关键字
    skip_keywords = [
        'English Version', '日本語版', '首页', '今日热门', '热门歌曲', 
        '最新歌曲', '歌手', 'lrc/lyrics', 'txt 文档', '下载lyrics', 
        '下载txt', '更多', '歌手最新歌曲', '歌手热门歌曲', '最近30天', 
        '点击:', '收录:', '演唱：', 'Get it on', 'Google Play'
    ]
    
    for line in lines:
        # 移除时间轴
        clean_line = re.sub(r'\[\d{2}:\d{2}\.\d{2,3}\]', '', line).strip()
        
        if not clean_line:
            continue
        
        # 跳过包含关键字的行
        if any(keyword in clean_line for keyword in skip_keywords):
            continue
        
        # 跳过纯数字行
        if clean_line.isdigit():
            continue
        
        # 跳过单字符行
        if len(clean_line) == 1:
            continue
        
        # 保留元数据和歌词
        if len(clean_line) > 2:
            clean_lines.append(clean_line)
    
    return '\n'.join(clean_lines)

# 测试
print("=== 测试歌词清理功能 ===\n")

song_url = "https://www.kugeci.com/song/a64WYn9U"  # 心语玫瑰
print(f"测试歌曲: {song_url}\n")

time.sleep(2)
r = requests.get(song_url, timeout=10)
soup = BeautifulSoup(r.text, 'lxml')

# 提取原始歌词
raw_lyrics = ""
for elem in soup.find_all(['div', 'pre']):
    text = elem.get_text(strip=False)
    if '[00:' in text and len(text) > 100:
        raw_lyrics = text
        break

if raw_lyrics:
    print("原始内容行数:", len(raw_lyrics.split('\n')))
    
    # 清理歌词
    clean = clean_lyrics(raw_lyrics)
    
    print("清理后行数:", len(clean.split('\n')))
    print("\n--- 清理后的内容 ---")
    print(clean[:500])  # 只显示前500字符
    print("\n...")
    
    # 保存到文件
    with open('test_clean_result.txt', 'w', encoding='utf-8') as f:
        f.write(clean)
    
    print("\n✓ 已保存到: test_clean_result.txt")
else:
    print("✗ 未找到歌词")

print("\n=== 测试完成 ===")

