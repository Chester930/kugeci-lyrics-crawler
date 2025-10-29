import requests
from bs4 import BeautifulSoup

base_url = "https://mojigeci.com"
song_url = f"{base_url}/lyrics/%E5%86%8D%E8%A6%8B%20Rainy%20Days"

print(f"=== Analyzing lyrics page structure ===")
r = requests.get(song_url, timeout=10)
soup = BeautifulSoup(r.text, 'lxml')

# 查找所有可能包含大量文本的元素
print("\n=== Analyzing text-heavy elements ===")
all_elements = soup.find_all(['div', 'pre', 'p', 'article', 'section'])

text_elements = []
for elem in all_elements:
    text = elem.get_text(strip=True)
    if len(text) > 50:  # 至少50个字符
        text_elements.append({
            'tag': elem.name,
            'id': elem.get('id', ''),
            'class': ' '.join(elem.get('class', [])),
            'text_length': len(text),
            'text_preview': text[:100].replace('\n', ' ')
        })

# 按文本长度排序
text_elements.sort(key=lambda x: x['text_length'], reverse=True)

print(f"\nFound {len(text_elements)} elements with substantial text:")
for i, elem in enumerate(text_elements[:15]):
    print(f"\n[{i+1}] <{elem['tag']} id='{elem['id']}' class='{elem['class']}'>")
    print(f"    Length: {elem['text_length']} chars")
    print(f"    Preview: {elem['text_preview']}")

# 特别查找可能的歌词内容区域
print("\n\n=== Looking for specific lyrics container ===")
# 查找包含换行符多的元素（歌词通常多行）
for elem in soup.find_all(['div', 'pre']):
    html_content = str(elem)
    text_content = elem.get_text()
    # 计算换行符数量
    br_count = html_content.count('<br')
    newline_count = text_content.count('\n')
    
    if br_count > 5 or newline_count > 5:
        classes = ' '.join(elem.get('class', []))
        elem_id = elem.get('id', '')
        print(f"\n<{elem.name} id='{elem_id}' class='{classes}'>")
        print(f"  BR tags: {br_count}, Newlines: {newline_count}")
        print(f"  Text preview: {text_content[:150].replace(chr(10), '|')}")

