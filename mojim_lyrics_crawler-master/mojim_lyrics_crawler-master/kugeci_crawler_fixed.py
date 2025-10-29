"""
酷歌词爬虫 - 修复版
正确提取作词人的歌曲列表（从表格中获取）
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import os
from urllib.parse import urljoin
import re

class KugeciCrawlerFixed:
    def __init__(self, output_dir='lyrics_data_fixed', start_page=1, end_page=3, delay=1.5):
        """
        初始化爬虫
        :param output_dir: 输出目录
        :param start_page: 起始页码
        :param end_page: 结束页码
        :param delay: 请求延迟（秒）
        """
        self.base_url = "https://www.kugeci.com"
        self.output_dir = output_dir
        self.start_page = start_page
        self.end_page = end_page
        self.delay = delay
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
        # 统计信息
        self.stats = {
            'writers_processed': 0,
            'songs_downloaded': 0,
            'errors': [],
            'writer_details': []  # 记录每个作词人的歌曲数
        }
        
        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)
    
    def safe_filename(self, name):
        """创建安全的文件名"""
        name = re.sub(r'[<>:"/\\|?*]', '_', name)
        return name[:100] if len(name) > 100 else name
    
    def get_writers_from_page(self, page_num):
        """
        获取某一页的所有作词人
        """
        url = f"{self.base_url}/writers?page={page_num}"
        print(f"\n{'='*60}")
        print(f"正在获取第 {page_num} 页作词人列表...")
        print(f"URL: {url}")
        
        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')
            
            writers = []
            # 查找作词人链接
            for link in soup.find_all('a', href=True):
                href = link.get('href', '')
                if '/writer/' in href:
                    name = link.get_text(strip=True)
                    if name:
                        writer_url = urljoin(self.base_url, href)
                        writers.append({
                            'name': name,
                            'url': writer_url,
                            'id': href.split('/')[-1]
                        })
            
            # 去重
            unique_writers = []
            seen_ids = set()
            for writer in writers:
                if writer['id'] not in seen_ids:
                    unique_writers.append(writer)
                    seen_ids.add(writer['id'])
            
            print(f"✓ 找到 {len(unique_writers)} 个作词人")
            return unique_writers
            
        except Exception as e:
            print(f"✗ 获取第 {page_num} 页失败: {e}")
            self.stats['errors'].append(f"Page {page_num}: {e}")
            return []
    
    def get_songs_from_writer(self, writer_url, writer_name):
        """
        【修复】从表格中获取作词人的歌曲列表
        """
        try:
            time.sleep(self.delay)
            response = self.session.get(writer_url, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')
            
            songs = []
            
            # 【关键修复】只从表格中提取歌曲
            table = soup.find('table', {'class': 'table'}) or soup.find('table', {'id': 'tablesort'})
            
            if table:
                # 遍历表格行（跳过表头）
                rows = table.find_all('tr')[1:]  # 跳过第一行（表头）
                
                for row in rows:
                    cells = row.find_all('td')
                    if len(cells) >= 4:  # 确保有足够的列
                        # 列结构：收录日期、歌名、歌手、作曲、点击
                        song_link = cells[1].find('a')  # 歌名在第2列
                        if song_link and '/song/' in song_link.get('href', ''):
                            song_title = song_link.get_text(strip=True)
                            singer = cells[2].get_text(strip=True)  # 歌手
                            composer = cells[3].get_text(strip=True)  # 作曲
                            
                            # 组合完整标题：歌手 - 歌名
                            full_title = f"{singer} - {song_title}" if singer else song_title
                            
                            songs.append({
                                'title': full_title,
                                'song_name': song_title,
                                'singer': singer,
                                'composer': composer,
                                'url': urljoin(self.base_url, song_link['href'])
                            })
            else:
                print(f"  ⚠️  未找到歌曲表格")
            
            return songs
            
        except Exception as e:
            print(f"  ✗ 获取歌曲列表失败: {e}")
            self.stats['errors'].append(f"{writer_name}: {e}")
            return []
    
    def download_lyrics_txt(self, song_url):
        """
        从歌曲页面提取歌词文本
        """
        try:
            time.sleep(self.delay)
            response = self.session.get(song_url, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')
            
            lyrics_text = ""
            
            # 查找包含LRC格式的文本块
            for elem in soup.find_all(['div', 'pre', 'p']):
                text = elem.get_text(strip=False)
                if '[00:' in text or '[01:' in text:
                    if len(text) > len(lyrics_text):
                        lyrics_text = text
            
            # 清理歌词文本
            if lyrics_text:
                lines = lyrics_text.split('\n')
                clean_lines = []
                for line in lines:
                    # 移除时间轴 [00:00.00]
                    clean_line = re.sub(r'\[\d{2}:\d{2}\.\d{2,3}\]', '', line).strip()
                    if clean_line:
                        clean_lines.append(clean_line)
                
                return '\n'.join(clean_lines)
            
            return None
            
        except Exception as e:
            print(f"    ✗ 下载歌词失败: {e}")
            return None
    
    def crawl(self):
        """主爬取函数"""
        print("\n" + "="*60)
        print("🎵 酷歌词爬虫启动（修复版）")
        print("="*60)
        print(f"输出目录: {self.output_dir}")
        print(f"页码范围: {self.start_page} - {self.end_page}")
        print(f"请求延迟: {self.delay} 秒")
        print("="*60)
        
        # 遍历每一页
        for page_num in range(self.start_page, self.end_page + 1):
            page_dir = os.path.join(self.output_dir, f"page_{page_num}")
            os.makedirs(page_dir, exist_ok=True)
            
            # 获取该页的所有作词人
            writers = self.get_writers_from_page(page_num)
            
            if not writers:
                print(f"第 {page_num} 页无作词人数据，跳过")
                continue
            
            # 遍历每个作词人
            for idx, writer in enumerate(writers, 1):
                writer_name = self.safe_filename(writer['name'])
                writer_dir = os.path.join(page_dir, writer_name)
                os.makedirs(writer_dir, exist_ok=True)
                
                print(f"\n[{idx}/{len(writers)}] 处理作词人: {writer['name']}")
                print(f"  URL: {writer['url']}")
                
                # 【修复】从表格中获取歌曲列表
                songs = self.get_songs_from_writer(writer['url'], writer['name'])
                print(f"  找到 {len(songs)} 首歌曲")
                
                # 记录作词人信息
                writer_info = {
                    'name': writer['name'],
                    'song_count': len(songs),
                    'songs': [song['title'] for song in songs]
                }
                self.stats['writer_details'].append(writer_info)
                
                if len(songs) == 0:
                    print(f"  ⚠️  该作词人暂无收录歌曲")
                    continue
                
                # 下载每首歌的歌词
                for song_idx, song in enumerate(songs, 1):
                    song_title = self.safe_filename(song['title'])
                    lyrics_file = os.path.join(writer_dir, f"{song_title}.txt")
                    
                    # 如果文件已存在，跳过
                    if os.path.exists(lyrics_file):
                        print(f"    [{song_idx}/{len(songs)}] {song['title']} - 已存在，跳过")
                        continue
                    
                    print(f"    [{song_idx}/{len(songs)}] 下载: {song['title']}")
                    
                    # 下载歌词
                    lyrics = self.download_lyrics_txt(song['url'])
                    
                    if lyrics:
                        # 添加元数据
                        metadata = f"歌名: {song['song_name']}\n"
                        metadata += f"演唱: {song['singer']}\n"
                        metadata += f"作词: {writer['name']}\n"
                        metadata += f"作曲: {song['composer']}\n"
                        metadata += f"\n{'='*40}\n\n"
                        
                        full_content = metadata + lyrics
                        
                        # 保存到文件
                        with open(lyrics_file, 'w', encoding='utf-8') as f:
                            f.write(full_content)
                        print(f"      ✓ 已保存")
                        self.stats['songs_downloaded'] += 1
                    else:
                        print(f"      ✗ 无法获取歌词")
                        self.stats['errors'].append(f"{writer['name']} - {song['title']}")
                
                self.stats['writers_processed'] += 1
                
                # 保存进度
                self.save_stats()
        
        # 最终统计
        self.print_summary()
    
    def save_stats(self):
        """保存统计信息"""
        stats_file = os.path.join(self.output_dir, 'crawl_stats.json')
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(self.stats, f, ensure_ascii=False, indent=2)
    
    def print_summary(self):
        """打印爬取摘要"""
        print("\n" + "="*60)
        print("🎉 爬取完成！")
        print("="*60)
        print(f"处理作词人数: {self.stats['writers_processed']}")
        print(f"下载歌曲数: {self.stats['songs_downloaded']}")
        print(f"错误数: {len(self.stats['errors'])}")
        
        # 显示作词人歌曲统计
        if self.stats['writer_details']:
            print("\n作词人歌曲统计（前10位）:")
            for detail in self.stats['writer_details'][:10]:
                print(f"  {detail['name']}: {detail['song_count']}首")
        
        if self.stats['errors']:
            print(f"\n前10个错误:")
            for error in self.stats['errors'][:10]:
                print(f"  - {error}")
        print("="*60)


if __name__ == '__main__':
    # 配置参数
    crawler = KugeciCrawlerFixed(
        output_dir='lyrics_data_fixed',
        start_page=1,
        end_page=2,  # 测试用
        delay=1.5
    )
    
    # 开始爬取
    crawler.crawl()

