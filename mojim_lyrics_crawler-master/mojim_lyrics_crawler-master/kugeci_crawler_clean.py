"""
酷歌词爬虫 - 最终版（清洁歌词）
只保存纯净的歌词内容，去除所有网页元素
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import os
from urllib.parse import urljoin
import re

class KugeciCrawlerClean:
    def __init__(self, output_dir='lyrics_clean', start_page=1, end_page=3, delay=2.0):
        self.base_url = "https://www.kugeci.com"
        self.output_dir = output_dir
        self.start_page = start_page
        self.end_page = end_page
        self.delay = delay
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
        self.stats = {
            'writers_processed': 0,
            'songs_downloaded': 0,
            'errors': []
        }
        
        os.makedirs(output_dir, exist_ok=True)
    
    def safe_filename(self, name):
        return re.sub(r'[<>:"/\\|?*]', '_', name)[:100]
    
    def clean_lyrics(self, raw_text):
        """
        智能清理歌词，只保留元数据和歌词内容
        """
        lines = raw_text.split('\n')
        clean_lines = []
        
        # 过滤规则
        skip_keywords = [
            'English Version', '日本語版', '首页', '今日热门', '热门歌曲', 
            '最新歌曲', '歌手', '作词', '作曲', 'lrc/lyrics', 'txt 文档',
            '下载lyrics', '下载txt', '更多', '歌手最新歌曲', '歌手热门歌曲',
            '最近30天', '点击:', '收录:', '演唱：', '热门推荐', 'Get it on'
        ]
        
        for line in lines:
            # 移除时间轴
            clean_line = re.sub(r'\[\d{2}:\d{2}\.\d{2,3}\]', '', line).strip()
            
            # 跳过空行
            if not clean_line:
                continue
            
            # 跳过包含关键字的行
            if any(keyword in clean_line for keyword in skip_keywords):
                continue
            
            # 跳过只有数字的行（如推荐列表的序号）
            if clean_line.isdigit():
                continue
            
            # 跳过单个字符的行（通常是列表标记）
            if len(clean_line) == 1 and clean_line in ['#', '-', '*']:
                continue
            
            # 保留元数据行（作词、作曲、编曲、后期等）
            if any(prefix in clean_line for prefix in ['作词', '作曲', '编曲', '后期', '监制', '制作']):
                clean_lines.append(clean_line)
                continue
            
            # 保留歌词行（长度大于2的文本）
            if len(clean_line) > 2:
                clean_lines.append(clean_line)
        
        return '\n'.join(clean_lines)
    
    def get_writers_from_page(self, page_num):
        url = f"{self.base_url}/writers?page={page_num}"
        print(f"\n{'='*60}")
        print(f"获取第 {page_num} 页作词人...")
        
        try:
            time.sleep(self.delay)
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')
            
            writers = []
            for link in soup.find_all('a', href=True):
                href = link.get('href', '')
                if '/writer/' in href:
                    name = link.get_text(strip=True)
                    if name:
                        writers.append({
                            'name': name,
                            'url': urljoin(self.base_url, href),
                            'id': href.split('/')[-1]
                        })
            
            unique_writers = list({w['id']: w for w in writers}.values())
            print(f"✓ 找到 {len(unique_writers)} 个作词人")
            return unique_writers
            
        except Exception as e:
            print(f"✗ 失败: {e}")
            return []
    
    def get_songs_from_writer(self, writer_url):
        try:
            time.sleep(self.delay)
            response = self.session.get(writer_url, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')
            
            songs = []
            table = soup.find('table', {'class': 'table'}) or soup.find('table', {'id': 'tablesort'})
            
            if table:
                rows = table.find_all('tr')[1:]
                for row in rows:
                    cells = row.find_all('td')
                    if len(cells) >= 4:
                        song_link = cells[1].find('a')
                        if song_link:
                            songs.append({
                                'title': f"{cells[2].get_text(strip=True)} - {song_link.get_text(strip=True)}",
                                'url': urljoin(self.base_url, song_link['href'])
                            })
            
            return songs
            
        except Exception as e:
            print(f"  ✗ 获取歌曲失败: {e}")
            return []
    
    def download_lyrics(self, song_url):
        try:
            time.sleep(self.delay)
            response = self.session.get(song_url, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')
            
            # 查找歌词
            lyrics_text = ""
            for elem in soup.find_all(['div', 'pre']):
                text = elem.get_text(strip=False)
                if '[00:' in text and len(text) > 100:
                    if len(text) > len(lyrics_text):
                        lyrics_text = text
            
            if lyrics_text:
                # 清理歌词
                return self.clean_lyrics(lyrics_text)
            
            return None
            
        except Exception as e:
            return None
    
    def crawl(self):
        print(f"\n{'='*60}")
        print("🎵 酷歌词爬虫 - 清洁版")
        print(f"{'='*60}")
        print(f"输出: {self.output_dir}")
        print(f"页码: {self.start_page}-{self.end_page}")
        print(f"{'='*60}")
        
        for page_num in range(self.start_page, self.end_page + 1):
            page_dir = os.path.join(self.output_dir, f"page_{page_num}")
            os.makedirs(page_dir, exist_ok=True)
            
            writers = self.get_writers_from_page(page_num)
            if not writers:
                continue
            
            for idx, writer in enumerate(writers, 1):
                writer_name = self.safe_filename(writer['name'])
                writer_dir = os.path.join(page_dir, writer_name)
                os.makedirs(writer_dir, exist_ok=True)
                
                print(f"\n[{idx}/{len(writers)}] {writer['name']}")
                
                songs = self.get_songs_from_writer(writer['url'])
                print(f"  歌曲: {len(songs)}首")
                
                if not songs:
                    continue
                
                for song_idx, song in enumerate(songs, 1):
                    song_title = self.safe_filename(song['title'])
                    lyrics_file = os.path.join(writer_dir, f"{song_title}.txt")
                    
                    if os.path.exists(lyrics_file):
                        print(f"    [{song_idx}/{len(songs)}] {song['title']} - 已存在")
                        continue
                    
                    print(f"    [{song_idx}/{len(songs)}] {song['title']}")
                    
                    lyrics = self.download_lyrics(song['url'])
                    
                    if lyrics:
                        with open(lyrics_file, 'w', encoding='utf-8') as f:
                            f.write(lyrics)
                        print(f"      ✓ 已保存")
                        self.stats['songs_downloaded'] += 1
                    else:
                        print(f"      ✗ 失败")
                
                self.stats['writers_processed'] += 1
        
        print(f"\n{'='*60}")
        print("✅ 完成！")
        print(f"作词人: {self.stats['writers_processed']}")
        print(f"歌曲: {self.stats['songs_downloaded']}")
        print(f"{'='*60}")


if __name__ == '__main__':
    crawler = KugeciCrawlerClean(
        output_dir='lyrics_clean',
        start_page=1,
        end_page=1,  # 先测试1页
        delay=2.0
    )
    crawler.crawl()

