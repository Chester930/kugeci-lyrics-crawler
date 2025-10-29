"""
酷歌词爬虫 - 完美版
根据用户标准：
1. 第一行：歌名
2. 第二行开始：作词、作曲等元数据
3. 遇到第二次"作词"或"词"就停止（表示重复）
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import os
from urllib.parse import urljoin
import re

class KugeciPerfect:
    def __init__(self, output_dir='lyrics_perfect', start_page=1, end_page=3, delay=2.0):
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
    
    def clean_and_format(self, raw_text, song_name, singer, writer_name):
        """
        根据用户标准清理和格式化
        """
        lines = raw_text.split('\n')
        output = []
        metadata_count = 0  # 记录"作词"出现次数
        in_metadata = True
        
        # 第一行：歌名
        output.append(f"歌名：{song_name}")
        output.append(f"演唱：{singer}")
        
        # 处理元数据和歌词
        for line in lines:
            # 移除时间轴
            clean_line = re.sub(r'\[\d{2}:\d{2}\.\d{2,3}\]', '', line).strip()
            
            if not clean_line:
                continue
            
            # 检查是否包含"作词"或"词："
            if re.search(r'(作词|^词)\s*[:：]', clean_line):
                metadata_count += 1
                if metadata_count > 1:
                    # 第二次出现，停止处理
                    break
                # 第一次出现，添加到输出
                output.append(clean_line)
                continue
            
            # 处理其他元数据（作曲、编曲等）
            if in_metadata and re.match(r'(作曲|曲|编曲|后期|监制|制作)\s*[:：]', clean_line):
                output.append(clean_line)
                continue
            
            # 跳过网页元素
            skip_keywords = [
                'English Version', '日本語版', '首页', '今日热门', '热门歌曲',
                '最新歌曲', 'lrc/lyrics', 'txt 文档', '下载', '更多',
                'Get it on', 'Google Play', '演唱：', '歌手：'
            ]
            
            if any(keyword in clean_line for keyword in skip_keywords):
                continue
            
            # 跳过纯数字或单字符
            if clean_line.isdigit() or len(clean_line) == 1:
                continue
            
            # 跳过歌曲标题重复
            if clean_line == song_name or clean_line == f"{singer} - {song_name}":
                continue
            
            # 如果遇到元数据行，标记进入歌词部分
            if not re.match(r'(作词|词|作曲|曲|编曲|后期|监制|制作)\s*[:：]', clean_line):
                if in_metadata and len(clean_line) > 5:
                    # 添加分隔线
                    if output and output[-1] and not output[-1].startswith('='):
                        output.append('')
                        output.append('='*40)
                        output.append('')
                    in_metadata = False
            
            # 保留有效歌词行
            if not in_metadata and len(clean_line) >= 2:
                output.append(clean_line)
        
        return '\n'.join(output)
    
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
                            href = song_link['href']
                            songs.append({
                                'song_name': song_link.get_text(strip=True),
                                'singer': cells[2].get_text(strip=True),
                                'url': href if href.startswith('http') else urljoin(self.base_url, href)
                            })
            
            return songs
            
        except Exception as e:
            return []
    
    def download_and_process(self, song_url, song_name, singer, writer_name):
        try:
            time.sleep(self.delay)
            response = self.session.get(song_url, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')
            
            # 提取原始歌词
            raw_lyrics = ""
            for elem in soup.find_all(['div', 'pre']):
                text = elem.get_text(strip=False)
                if '[00:' in text and len(text) > 100:
                    if len(text) > len(raw_lyrics):
                        raw_lyrics = text
            
            if raw_lyrics:
                return self.clean_and_format(raw_lyrics, song_name, singer, writer_name)
            
            return None
            
        except Exception as e:
            return None
    
    def crawl(self):
        print(f"\n{'='*60}")
        print("🎵 酷歌词爬虫 - 完美版")
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
                
                for song_idx, song in enumerate(songs, 1):
                    full_title = f"{song['singer']} - {song['song_name']}"
                    safe_title = self.safe_filename(full_title)
                    lyrics_file = os.path.join(writer_dir, f"{safe_title}.txt")
                    
                    if os.path.exists(lyrics_file):
                        print(f"    [{song_idx}/{len(songs)}] {full_title} - 已存在")
                        continue
                    
                    print(f"    [{song_idx}/{len(songs)}] {full_title}")
                    
                    final_lyrics = self.download_and_process(
                        song['url'], song['song_name'], 
                        song['singer'], writer['name']
                    )
                    
                    if final_lyrics:
                        with open(lyrics_file, 'w', encoding='utf-8') as f:
                            f.write(final_lyrics)
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
    crawler = KugeciPerfect(
        output_dir='lyrics_perfect',
        start_page=1,
        end_page=1,  # 先测试1页
        delay=2.0
    )
    crawler.crawl()

