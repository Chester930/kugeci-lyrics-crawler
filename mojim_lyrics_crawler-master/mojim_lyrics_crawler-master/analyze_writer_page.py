"""
分析作词人页面的正确结构
找到歌曲列表的准确位置
"""

import requests
from bs4 import BeautifulSoup

# 测试李奎的页面
url = "https://www.kugeci.com/writer/N3vdNEOq"

print("=== 分析作词人页面结构 ===\n")
print(f"URL: {url}\n")

r = requests.get(url, timeout=10)
soup = BeautifulSoup(r.text, 'lxml')

# 1. 查找页面标题
print("1. 页面标题")
title = soup.find('title')
if title:
    print(f"   {title.text}\n")

# 2. 查找所有包含"收录"、"歌曲"等关键字的区域
print("2. 查找歌曲列表区域")
for elem in soup.find_all(['div', 'section', 'table']):
    text = elem.get_text(strip=True)
    if any(keyword in text for keyword in ['收录', '歌名', '歌手', '作曲', '点击']):
        classes = ' '.join(elem.get('class', []))
        elem_id = elem.get('id', '')
        print(f"\n   找到可能的歌曲列表容器:")
        print(f"   标签: <{elem.name}>")
        print(f"   class: {classes}")
        print(f"   id: {elem_id}")
        print(f"   文本预览: {text[:200]}")
        
        # 查看其中的链接
        links = elem.find_all('a', href=True)
        song_links = [link for link in links if '/song/' in link.get('href', '')]
        print(f"   包含歌曲链接数: {len(song_links)}")
        if song_links:
            print(f"   歌曲链接示例:")
            for link in song_links[:3]:
                print(f"     - {link.get_text(strip=True)}: {link['href']}")

# 3. 查找表格结构
print("\n\n3. 查找表格结构")
tables = soup.find_all('table')
print(f"   找到 {len(tables)} 个表格")
for i, table in enumerate(tables):
    print(f"\n   表格 {i+1}:")
    headers = table.find_all('th')
    if headers:
        print(f"   表头: {[th.get_text(strip=True) for th in headers]}")
    
    rows = table.find_all('tr')[:3]  # 只看前3行
    print(f"   数据行数: {len(table.find_all('tr'))}")
    for j, row in enumerate(rows):
        cells = row.find_all(['td', 'th'])
        if cells:
            cell_texts = [cell.get_text(strip=True) for cell in cells]
            print(f"   行{j+1}: {cell_texts}")

# 4. 查找所有歌曲链接及其父容器
print("\n\n4. 所有歌曲链接及其父容器")
all_song_links = soup.find_all('a', href=lambda x: x and '/song/' in x)
print(f"   总共找到 {len(all_song_links)} 个歌曲链接\n")

# 按父容器分组
from collections import defaultdict
by_parent = defaultdict(list)

for link in all_song_links:
    text = link.get_text(strip=True)
    href = link.get('href', '')
    
    # 找到最近的有class的父元素
    parent = link.parent
    while parent and not parent.get('class'):
        parent = parent.parent
        if parent.name == 'body':
            break
    
    parent_class = ' '.join(parent.get('class', [])) if parent else 'no-parent'
    by_parent[parent_class].append({'text': text, 'href': href})

print(f"   歌曲链接按父容器分组:")
for parent_class, links in by_parent.items():
    print(f"\n   父容器 class='{parent_class}': {len(links)} 个链接")
    for link in links[:3]:
        print(f"     - {link['text']}: {link['href']}")

print("\n=== 分析完成 ===")

