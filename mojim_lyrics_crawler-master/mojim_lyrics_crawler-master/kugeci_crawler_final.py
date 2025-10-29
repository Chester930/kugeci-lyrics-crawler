"""
酷歌词爬虫 - 最终优化版
- 去除重复元数据
- 去除演唱会对话
- 添加完整的歌曲信息头
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import os
from urllib.parse import urljoin
import re

class KugeciCrawlerFinal:
    def __init__(self, output_dir='lyrics_final', start_page=1, end_page=3, delay=2.0):
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
    
    def extract_metadata(self, raw_text):
        """提取元数据（作词、作曲、编曲等）"""
        metadata = {}
        lines = raw_text.split('\n')
        
        for line in lines[:30]:  # 只在前30行查找元数据
            line = line.strip()
            # 匹配 "作词：XXX" 或 "作词 : XXX" 或 "词：XXX"
            if re.match(r'(作词|词)\s*[:：]\s*(.+)', line):
                match = re.match(r'(作词|词)\s*[:：]\s*(.+)', line)
                if '作词' not in metadata:  # 避免重复
                    metadata['作词'] = match.group(2).strip()
            elif re.match(r'(作曲|曲)\s*[:：]\s*(.+)', line):
                match = re.match(r'(作曲|曲)\s*[:：]\s*(.+)', line)
                if '作曲' not in metadata:
                    metadata['作曲'] = match.group(2).strip()
            elif re.match(r'编曲\s*[:：]\s*(.+)', line):
                match = re.match(r'编曲\s*[:：]\s*(.+)', line)
                if '编曲' not in metadata:
                    metadata['编曲'] = match.group(1).strip()
            elif re.match(r'后期\s*[:：]\s*(.+)', line):
                match = re.match(r'后期\s*[:：]\s*(.+)', line)
                if '后期' not in metadata:
                    metadata['后期'] = match.group(1).strip()
        
        return metadata
    
    def clean_lyrics(self, raw_text):
        """智能清理歌词 - 只保留纯歌词"""
        lines = raw_text.split('\n')
        lyrics_lines = []
        
        # 跳过的关键字（网页元素）
        skip_keywords = [
            'English Version', '日本語版', '首页', '今日热门', '热门歌曲', 
            '最新歌曲', 'lrc/lyrics', 'txt 文档', '下载', '更多', 
            '歌手最新歌曲', '歌手热门歌曲', '最近30天', '点击:', '收录:',
            'Get it on', 'Google Play', 'Copyright', '联系我们', 
            'Privacy Policy', '演唱：', '歌手：'
        ]
        
        # 跳过的模式（演唱会对话等）
        skip_patterns = [
            r'观众[：:]',  # 观众：靓仔！
            r'哥哥[：:]',  # 哥哥：哈哈
            r'我今天.*开心',  # 演唱会对话开头
            r'不是因为',
            r'其实好多',
            r'多谢你地',
        ]
        
        in_lyrics = False
        
        for line in lines:
            # 移除时间轴
            clean_line = re.sub(r'\[\d{2}:\d{2}\.\d{2,3}\]', '', line).strip()
            
            if not clean_line:
                continue
            
            # 跳过元数据行
            if re.match(r'(作词|词|作曲|曲|编曲|后期|监制|制作)\s*[:：]', clean_line):
                continue
            
            # 跳过包含关键字的行
            if any(keyword in clean_line for keyword in skip_keywords):
                continue
            
            # 跳过匹配特定模式的行
            if any(re.search(pattern, clean_line) for pattern in skip_patterns):
                break  # 遇到演唱会对话，停止处理
            
            # 跳过纯数字或单字符
            if clean_line.isdigit() or len(clean_line) == 1:
                continue
            
            # 保留歌词行
            if len(clean_line) >= 2:
                lyrics_lines.append(clean_line)
                in_lyrics = True
        
        return '\n'.join(lyrics_lines)
    
    def format_lyrics(self, song_name, singer, writer_name, metadata, lyrics):
        """格式化最终输出"""
        output = []
        output.append(f"歌名：{song_name}")
        output.append(f"演唱：{singer}")
        output.append(f"作词：{writer_name}")
        
        # 添加其他元数据
        if '作曲' in metadata:
            output.append(f"作曲：{metadata['作曲']}")
        if '编曲' in metadata:
            output.append(f"编曲：{metadata['编曲']}")
        if '后期' in metadata:
            output.append(f"后期：{metadata['后期']}")
        
        output.append('')
        output.append('='*40)
        output.append('')
        output.append(lyrics)
        
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
                            songs.append({
                                'song_name': song_link.get_text(strip=True),
                                'singer': cells[2].get_text(strip=True),
                                'url': urljoin(self.base_url, song_link['href'])
                            })
            
            return songs
            
        except Exception as e:
            return []
    
    def download_and_process_lyrics(self, song_url, song_name, singer, writer_name):
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
                # 提取元数据
                metadata = self.extract_metadata(raw_lyrics)
                
                # 清理歌词
                clean = self.clean_lyrics(raw_lyrics)
                
                # 格式化输出
                final_output = self.format_lyrics(
                    song_name, singer, writer_name, metadata, clean
                )
                
                return final_output
            
            return None
            
        except Exception as e:
            return None
    
    def crawl(self):
        print(f"\n{'='*60}")
        print("🎵 酷歌词爬虫 - 最终优化版")
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
                    
                    final_lyrics = self.download_and_process_lyrics(
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
    crawler = KugeciCrawlerFinal(
        output_dir='lyrics_final',
        start_page=1,
        end_page=1,  # 先测试
        delay=2.0
    )
    crawler.crawl()

