import requests
from bs4 import BeautifulSoup

base_url = "https://mojigeci.com"

# 探索 /list 页面
print("=== Exploring /list page ===")
r = requests.get(f"{base_url}/list", timeout=10)
soup = BeautifulSoup(r.text, 'lxml')
print(f"Status: {r.status_code}")
print(f"Title: {soup.find('title').text if soup.find('title') else 'No title'}")

# 查看页面结构
print("\n=== Page structure ===")
# 查找所有链接，特别是带日期或年份的
links = soup.find_all('a', href=True)
year_links = []
for link in links:
    href = link.get('href', '')
    text = link.get_text(strip=True)
    # 查找包含年份的链接
    if any(str(year) in href or str(year) in text for year in range(2020, 2026)):
        year_links.append(f"{text}: {href}")

print(f"Found {len(year_links)} links with years 2020-2025:")
for link in year_links[:20]:
    print(link)

# 查看是否有新歌、排行榜等链接
print("\n=== Looking for recent songs sections ===")
for link in links[:100]:
    text = link.get_text(strip=True)
    href = link.get('href', '')
    if any(keyword in text.lower() or keyword in href.lower() 
           for keyword in ['新歌', 'new', '最新', 'latest', '排行', 'chart', '月', 'month']):
        print(f"{text}: {href}")

