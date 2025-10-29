#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
方文山專用爬蟲
根據 https://www.kugeci.com/writer/WQY6QJC3 頁面結構設計
"""

import requests
from bs4 import BeautifulSoup
import os
import re
import time
from urllib.parse import urljoin

class FangWenshanCrawler:
    def __init__(self):
        self.base_url = "https://www.kugeci.com"
        self.writer_url = "https://www.kugeci.com/writer/WQY6QJC3"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.output_dir = "fangwenshan_output"
        os.makedirs(self.output_dir, exist_ok=True)

    def safe_filename(self, name):
        """將檔案名轉換為安全的檔案系統名稱"""
        return re.sub(r'[<>:"/\\|?*]', '_', name)[:100]

    def get_songs_from_page(self):
        """從方文山頁面獲取所有歌曲列表"""
        try:
            print(f"正在訪問: {self.writer_url}")
            response = requests.get(self.writer_url, headers=self.headers, timeout=15)
            print(f"響應狀態碼: {response.status_code}")
            
            if response.status_code != 200:
                print(f"錯誤: HTTP {response.status_code}")
                return []
            
            soup = BeautifulSoup(response.text, 'lxml')
            
            # 尋找歌曲表格
            table = soup.find('table')
            if not table:
                print("未找到歌曲表格")
                return []
            
            songs = []
            rows = table.find_all('tr')[1:]  # 跳過標題行
            
            print(f"找到 {len(rows)} 行歌曲資料")
            
            for i, row in enumerate(rows):
                cells = row.find_all('td')
                if len(cells) >= 4:
                    # 解析歌曲信息
                    song_name = ""
                    singer_name = ""
                    song_url = ""
                    
                    # 歌曲名稱和連結（通常在第二個欄位）
                    song_cell = cells[1]
                    song_link = song_cell.find('a', href=True)
                    if song_link:
                        song_name = song_link.get_text(strip=True)
                        song_url = song_link.get('href')
                        if not song_url.startswith('http'):
                            song_url = urljoin(self.base_url, song_url)
                    
                    # 歌手名稱（第三個欄位）
                    if len(cells) >= 3:
                        singer_cell = cells[2]
                        singer_links = singer_cell.find_all('a')
                        if singer_links:
                            singer_names = [link.get_text(strip=True) for link in singer_links]
                            singer_name = ' '.join(singer_names)
                        else:
                            singer_name = singer_cell.get_text(strip=True)
                    
                    if song_name and song_url:
                        songs.append({
                            'name': song_name,
                            'singer': singer_name or "未知歌手",
                            'url': song_url
                        })
                        print(f"  {i+1}. {song_name} - {singer_name or '未知歌手'}")
            
            return songs
            
        except Exception as e:
            print(f"獲取歌曲列表錯誤: {e}")
            return []

    def download_lyrics(self, url, delay=2.0):
        """下載歌詞內容。

        首選：提取「下載txt文檔」到「更多」。
        回退：若未命中標記，改為保存整頁純文字（不轉化）。
        """
        try:
            time.sleep(delay)
            response = requests.get(url, headers=self.headers, timeout=15)
            soup = BeautifulSoup(response.text, 'lxml')
            
            # 獲取完整文本
            text = soup.get_text()
            lines = text.split('\n')
            
            # 查找標記位置
            start_idx = None
            end_idx = None
            
            for i, line in enumerate(lines):
                line = line.strip()
                # 尋找開始標記：下載txt文檔
                if '下載txt文檔' in line or 'txt 文檔' in line or '下载txt文档' in line:
                    start_idx = i + 1
                    print(f"      找到開始標記: {line}")
                # 尋找結束標記：更多
                elif '更多' in line and start_idx is not None:
                    end_idx = i
                    print(f"      找到結束標記: {line}")
                    break
            
            if start_idx and end_idx and start_idx < end_idx:
                extracted = lines[start_idx:end_idx]
                clean_lines = [line.strip() for line in extracted if line.strip()]
                print(f"      提取了 {len(clean_lines)} 行歌詞")
                return '\n'.join(clean_lines)
            else:
                print(f"      未找到標記，改為保存原始頁面文字（不轉化）")
                clean_full = [ln.strip() for ln in lines if ln.strip()]
                return '\n'.join(clean_full)
            
        except Exception as e:
            print(f"      下載歌詞錯誤: {e}")
            return None

    def crawl_all_songs(self, delay=2.0):
        """爬取所有歌曲"""
        print("=== 方文山專用爬蟲 ===")
        
        # 獲取歌曲列表
        songs = self.get_songs_from_page()
        if not songs:
            print("未找到任何歌曲")
            return 0
        
        print(f"\n開始下載 {len(songs)} 首歌曲...")
        
        # 創建方文山資料夾
        writer_dir = os.path.join(self.output_dir, "方文山")
        os.makedirs(writer_dir, exist_ok=True)
        
        count = 0
        for i, song in enumerate(songs, 1):
            print(f"\n[{i}/{len(songs)}] 下載: {song['name']}")
            
            # 生成檔案名
            filename = f"{self.safe_filename(song['singer'])} - {self.safe_filename(song['name'])}.txt"
            filepath = os.path.join(writer_dir, filename)
            
            # 檢查檔案是否已存在
            if os.path.exists(filepath):
                print(f"  檔案已存在，跳過")
                continue
            
            # 下載歌詞
            lyrics = self.download_lyrics(song['url'], delay)
            if lyrics:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(lyrics)
                count += 1
                print(f"  ✓ 下載成功")
            else:
                print(f"  ✗ 下載失敗")
        
        print(f"\n=== 完成 ===")
        print(f"成功下載 {count} 首歌曲")
        print(f"保存位置: {writer_dir}")
        return count

def main():
    crawler = FangWenshanCrawler()
    crawler.crawl_all_songs(delay=2.0)

if __name__ == "__main__":
    main()
