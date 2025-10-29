"""
酷歌词爬虫 - 按作词人分类爬取
结构: page_X/作词人名/歌曲名.txt
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import os
from urllib.parse import urljoin, unquote
import re

class KugeciCrawler:
    def __init__(self, output_dir='lyrics_data', start_page=1, end_page=3, delay=1.5):
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
            'errors': []
        }
        
        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)
    
    def safe_filename(self, name):
        """创建安全的文件名"""
        # 移除不安全的字符
        name = re.sub(r'[<>:"/\\|?*]', '_', name)
        # 限制长度
        return name[:100] if len(name) > 100 else name
    
    def get_writers_from_page(self, page_num):
        """
        获取某一页的所有作词人
        :param page_num: 页码
        :return: 作词人列表 [{name, url, clicks}]
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
                    if name:  # 排除空名称
                        writer_url = urljoin(self.base_url, href)
                        writers.append({
                            'name': name,
                            'url': writer_url,
                            'id': href.split('/')[-1]
                        })
            
            # 去重（同一个作词人可能出现多次）
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
    
    def get_songs_from_writer(self, writer_url):
        """
        获取某个作词人的所有歌曲
        :param writer_url: 作词人页面URL
        :return: 歌曲列表 [{title, url}]
        """
        try:
            time.sleep(self.delay)
            response = self.session.get(writer_url, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')
            
            songs = []
            for link in soup.find_all('a', href=True):
                href = link.get('href', '')
                if '/song/' in href:
                    title = link.get_text(strip=True)
                    if title and ' - ' in title:  # 格式通常是 "歌手 - 歌名"
                        song_url = urljoin(self.base_url, href)
                        songs.append({
                            'title': title,
                            'url': song_url
                        })
            
            # 去重
            unique_songs = list({song['url']: song for song in songs}.values())
            return unique_songs
            
        except Exception as e:
            print(f"  ✗ 获取歌曲列表失败: {e}")
            return []
    
    def download_lyrics_txt(self, song_url):
        """
        从歌曲页面提取歌词文本
        :param song_url: 歌曲页面URL
        :return: 歌词文本内容
        """
        try:
            time.sleep(self.delay)
            response = self.session.get(song_url, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')
            
            # 查找包含歌词的主要容器
            # 通常歌词在页面的主要div中，包含LRC格式
            lyrics_text = ""
            
            # 方法1: 查找包含LRC格式的文本块
            for elem in soup.find_all(['div', 'pre', 'p']):
                text = elem.get_text(strip=False)
                # LRC格式特征：[00:00.00]
                if '[00:' in text or '[01:' in text:
                    if len(text) > len(lyrics_text):
                        lyrics_text = text
            
            # 清理歌词文本
            if lyrics_text:
                # 移除LRC时间轴，只保留歌词
                lines = lyrics_text.split('\n')
                clean_lines = []
                for line in lines:
                    # 移除时间轴 [00:00.00]
                    clean_line = re.sub(r'\[\d{2}:\d{2}\.\d{2}\]', '', line).strip()
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
        print("🎵 酷歌词爬虫启动")
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
                
                # 获取该作词人的所有歌曲
                songs = self.get_songs_from_writer(writer['url'])
                print(f"  找到 {len(songs)} 首歌曲")
                
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
                        # 保存到文件
                        with open(lyrics_file, 'w', encoding='utf-8') as f:
                            f.write(lyrics)
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
        if self.stats['errors']:
            print("\n前10个错误:")
            for error in self.stats['errors'][:10]:
                print(f"  - {error}")
        print("="*60)


if __name__ == '__main__':
    # 配置参数
    crawler = KugeciCrawler(
        output_dir='lyrics_data',  # 输出目录
        start_page=1,              # 起始页码
        end_page=2,                # 结束页码（测试用，建议先用小范围）
        delay=1.5                  # 请求延迟（秒）
    )
    
    # 开始爬取
    crawler.crawl()

