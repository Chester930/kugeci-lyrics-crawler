"""
酷歌詞爬蟲 - 圖形界面應用
功能：
1. 按頁數範圍爬取
2.選擇爬取類型:歌手、作詞、作曲
3. 按類型人名爬取
4.輸入人名或頁數
5. 選擇保存位置
"""

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import requests
from bs4 import BeautifulSoup
import os
import re
import time
import threading
from urllib.parse import urljoin

class LyricsCrawlerApp:
    def __init__(self, root):
        """初始化爬蟲應用程式"""
        self.root = root
        self.root.title("酷歌詞爬蟲 v1.0")
        self.root.geometry("700x600")
        self.root.resizable(False, False)
        
        # 爬蟲配置
        self.base_url = "https://www.kugeci.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.is_crawling = False
        
        self.create_widgets()
    
    def create_widgets(self):
        """創建界面組件"""
        
        # 標題
        title_frame = tk.Frame(self.root, bg="#4A90E2", height=60)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame, 
            text="🎵 酷歌詞爬蟲工具", 
            font=("微軟雅黑", 18, "bold"),
            bg="#4A90E2", 
            fg="white"
        )
        title_label.pack(pady=15)
        
        # 主容器
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 類型選擇
        type_frame = tk.LabelFrame(main_frame, text="選擇爬取類型", font=("微軟雅黑", 11, "bold"), padx=10, pady=10)
        type_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.type_var = tk.StringVar(value="writer")
        
        tk.Radiobutton(
            type_frame, 
            text="👤 作詞人", 
            variable=self.type_var, 
            value="writer",
            font=("微軟雅黑", 10),
            command=self.toggle_type
        ).grid(row=0, column=0, sticky=tk.W, pady=5, padx=(0, 20))
        
        tk.Radiobutton(
            type_frame, 
            text="🎼 作曲人", 
            variable=self.type_var, 
            value="composer",
            font=("微軟雅黑", 10),
            command=self.toggle_type
        ).grid(row=0, column=1, sticky=tk.W, pady=5, padx=(0, 20))
        
        tk.Radiobutton(
            type_frame, 
            text="🎤 歌手", 
            variable=self.type_var, 
            value="singer",
            font=("微軟雅黑", 10),
            command=self.toggle_type
        ).grid(row=0, column=2, sticky=tk.W, pady=5)
        
        # 爬取模式選擇
        mode_frame = tk.LabelFrame(main_frame, text="爬取模式", font=("微軟雅黑", 11, "bold"), padx=10, pady=10)
        mode_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.mode_var = tk.StringVar(value="name")
        
        tk.Radiobutton(
            mode_frame, 
            text="📝 按人名爬取", 
            variable=self.mode_var, 
            value="name",
            font=("微軟雅黑", 10),
            command=self.toggle_mode
        ).grid(row=0, column=0, sticky=tk.W, pady=5, padx=(0, 20))
        
        tk.Radiobutton(
            mode_frame, 
            text="📄 按頁數範圍爬取", 
            variable=self.mode_var, 
            value="pages",
            font=("微軟雅黑", 10),
            command=self.toggle_mode
        ).grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # 參數輸入區
        param_frame = tk.LabelFrame(main_frame, text="參數設置", font=("微軟雅黑", 11, "bold"), padx=10, pady=10)
        param_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 人名輸入
        self.name_frame = tk.Frame(param_frame)
        self.name_frame.pack(fill=tk.X, pady=5)
        
        self.name_label = tk.Label(self.name_frame, text="人名:", font=("微軟雅黑", 10))
        self.name_label.grid(row=0, column=0, padx=(0, 5))
        self.name_entry = tk.Entry(self.name_frame, width=30, font=("微軟雅黑", 10))
        self.name_entry.grid(row=0, column=1)
        
        self.name_hint = tk.Label(
            self.name_frame, 
            text="(例: 林夕、周杰倫、周深)", 
            font=("微軟雅黑", 8),
            fg="gray"
        )
        self.name_hint.grid(row=0, column=2, padx=(5, 0))
        
        # 頁數範圍輸入
        self.page_frame = tk.Frame(param_frame)
        
        tk.Label(self.page_frame, text="起始頁:", font=("微軟雅黑", 10)).grid(row=0, column=0, padx=(0, 5))
        self.start_page_entry = tk.Entry(self.page_frame, width=10, font=("微軟雅黑", 10))
        self.start_page_entry.grid(row=0, column=1, padx=(0, 20))
        self.start_page_entry.insert(0, "1")
        
        tk.Label(self.page_frame, text="結束頁:", font=("微軟雅黑", 10)).grid(row=0, column=2, padx=(0, 5))
        self.end_page_entry = tk.Entry(self.page_frame, width=10, font=("微軟雅黑", 10))
        self.end_page_entry.grid(row=0, column=3)
        self.end_page_entry.insert(0, "1")
        
        # 延遲設置
        delay_frame = tk.Frame(param_frame)
        delay_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(delay_frame, text="請求延遲:", font=("微軟雅黑", 10)).grid(row=0, column=0, padx=(0, 5))
        self.delay_entry = tk.Entry(delay_frame, width=10, font=("微軟雅黑", 10))
        self.delay_entry.grid(row=0, column=1)
        self.delay_entry.insert(0, "2.0")
        tk.Label(delay_frame, text="秒 (建議2-3秒)", font=("微軟雅黑", 8), fg="gray").grid(row=0, column=2, padx=(5, 0))
        
        # 保存位置
        path_frame = tk.LabelFrame(main_frame, text="保存位置", font=("微軟雅黑", 11, "bold"), padx=10, pady=10)
        path_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.path_var = tk.StringVar(value=os.path.join(os.getcwd(), "lyrics_output"))
        
        tk.Entry(
            path_frame, 
            textvariable=self.path_var, 
            font=("微軟雅黑", 9),
            state="readonly",
            width=60
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        tk.Button(
            path_frame, 
            text="📁 選擇", 
            command=self.select_folder,
            font=("微軟雅黑", 9),
            bg="#5CB85C",
            fg="white",
            cursor="hand2"
        ).pack(side=tk.RIGHT)
        
        # 控制按鈕
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.start_button = tk.Button(
            button_frame,
            text="🚀 開始爬取",
            command=self.start_crawling,
            font=("微軟雅黑", 12, "bold"),
            bg="#4A90E2",
            fg="white",
            height=2,
            cursor="hand2"
        )
        self.start_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        self.stop_button = tk.Button(
            button_frame,
            text="⏹ 停止",
            command=self.stop_crawling,
            font=("微軟雅黑", 12, "bold"),
            bg="#D9534F",
            fg="white",
            height=2,
            state=tk.DISABLED,
            cursor="hand2"
        )
        self.stop_button.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(5, 0))
        
        # 日誌顯示
        log_frame = tk.LabelFrame(main_frame, text="運行日誌", font=("微軟雅黑", 11, "bold"), padx=10, pady=10)
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=12,
            font=("Consolas", 9),
            wrap=tk.WORD
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # 版權提示
        copyright_label = tk.Label(
            self.root,
            text="⚠️ 僅供學習研究使用 | 請遵守版權法規 | 不得用於商業用途",
            font=("微軟雅黑", 8),
            fg="red"
        )
        copyright_label.pack(pady=5)
        
        # 初始化界面狀態
        self.toggle_type()
        self.toggle_mode()
    
    def toggle_type(self):
        """根據選擇的類型更新提示文字"""
        type_name = self.type_var.get()
        if type_name == "writer":
            self.name_label.config(text="作詞人名:")
            self.name_hint.config(text="(例: 林夕、方文山)")
        elif type_name == "composer":
            self.name_label.config(text="作曲人名:")
            self.name_hint.config(text="(例: 周杰倫、林俊傑)")
        elif type_name == "singer":
            self.name_label.config(text="歌手名:")
            self.name_hint.config(text="(例: 周深、薛之謙)")
    
    def toggle_mode(self):
        """根據選擇的模式顯示對應的輸入框"""
        # 隱藏所有輸入框
        self.name_frame.pack_forget()
        self.page_frame.pack_forget()
        
        # 根據選擇的模式顯示對應的輸入框
        if self.mode_var.get() == "name":
            self.name_frame.pack(fill=tk.X, pady=5)
        elif self.mode_var.get() == "pages":
            self.page_frame.pack(fill=tk.X, pady=5)
    
    def select_folder(self):
        """開啟資料夾選擇對話框，讓使用者選擇保存位置"""
        folder = filedialog.askdirectory(title="選擇保存位置")
        if folder:
            self.path_var.set(folder)
            self.log(f"📁 保存位置: {folder}")
    
    def log(self, message):
        """添加日誌訊息到顯示區域"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update()
    
    def start_crawling(self):
        """驗證輸入參數並開始爬取作業"""
        # 驗證輸入
        if self.mode_var.get() == "pages":
            try:
                start_page = int(self.start_page_entry.get())
                end_page = int(self.end_page_entry.get())
                if start_page < 1 or end_page < start_page:
                    messagebox.showerror("錯誤", "頁數範圍無效！")
                    return
            except ValueError:
                messagebox.showerror("錯誤", "請輸入有效的頁數！")
                return
        elif self.mode_var.get() == "name":
            name = self.name_entry.get().strip()
            if not name:
                type_name = self.type_var.get()
                if type_name == "writer":
                    messagebox.showerror("錯誤", "請輸入作詞人名！")
                elif type_name == "composer":
                    messagebox.showerror("錯誤", "請輸入作曲人名！")
                elif type_name == "singer":
                    messagebox.showerror("錯誤", "請輸入歌手名！")
                return
        
        try:
            delay = float(self.delay_entry.get())
            if delay < 1:
                messagebox.showwarning("警告", "建議延遲至少1秒，避免被封禁！")
        except ValueError:
            messagebox.showerror("錯誤", "請輸入有效的延遲時間！")
            return
        
        # 確認開始
        if not messagebox.askyesno(
            "確認", 
            "開始爬取？\n\n⚠️ 請確保:\n- 僅用於個人學習研究\n- 遵守版權法規\n- 不用於商業用途"
        ):
            return
        
        # 啟動爬蟲執行緒
        self.is_crawling = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        
        thread = threading.Thread(target=self.crawl_thread, daemon=True)
        thread.start()
    
    def stop_crawling(self):
        """停止爬取作業"""
        self.is_crawling = False
        self.log("\n⏹ 正在停止...")
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
    
    def crawl_thread(self):
        """在背景執行緒中執行爬取作業"""
        try:
            if self.mode_var.get() == "pages":
                self.crawl_by_pages()
            elif self.mode_var.get() == "name":
                self.crawl_by_name()
        except Exception as e:
            self.log(f"\n❌ 錯誤: {e}")
        finally:
            self.is_crawling = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
    
    def crawl_by_pages(self):
        """根據指定的頁數範圍爬取指定類型的所有歌曲"""
        start_page = int(self.start_page_entry.get())
        end_page = int(self.end_page_entry.get())
        delay = float(self.delay_entry.get())
        output_dir = self.path_var.get()
        type_name = self.type_var.get()
        
        type_text = {"writer": "作詞人", "composer": "作曲人", "singer": "歌手"}[type_name]
        
        self.log("="*60)
        self.log(f"🚀 開始按頁數爬取{type_text} (第{start_page}-{end_page}頁)")
        self.log("="*60)
        
        stats = {'people': 0, 'songs': 0}
        
        for page_num in range(start_page, end_page + 1):
            if not self.is_crawling:
                break
            
            self.log(f"\n📄 處理第 {page_num} 頁...")
            
            if type_name == "writer":
                people = self.get_writers_from_page(page_num, delay)
            elif type_name == "composer":
                people = self.get_composers_from_page(page_num, delay)
            elif type_name == "singer":
                people = self.get_singers_from_page(page_num, delay)
            
            if not people:
                continue
            
            page_dir = os.path.join(output_dir, f"page_{page_num}")
            os.makedirs(page_dir, exist_ok=True)
            
            for idx, person in enumerate(people, 1):
                if not self.is_crawling:
                    break
                
                self.log(f"  [{idx}/{len(people)}] {person['name']}")
                
                if type_name == "writer":
                    count = self.crawl_writer_songs(person, page_dir, delay)
                elif type_name == "composer":
                    count = self.crawl_composer_songs(person, page_dir, delay)
                elif type_name == "singer":
                    count = self.crawl_singer_songs(person, page_dir, delay)
                
                stats['songs'] += count
                stats['people'] += 1
        
        self.log("\n" + "="*60)
        self.log(f"✅ 完成！{type_text}: {stats['people']} | 歌曲: {stats['songs']}")
        self.log("="*60)
        messagebox.showinfo("完成", f"爬取完成！\n\n{type_text}: {stats['people']}\n歌曲: {stats['songs']}")
    
    def crawl_by_name(self):
        """根據選擇的類型和輸入的人名搜尋並爬取其所有歌曲"""
        name = self.name_entry.get().strip()
        delay = float(self.delay_entry.get())
        output_dir = self.path_var.get()
        type_name = self.type_var.get()
        
        type_text = {"writer": "作詞人", "composer": "作曲人", "singer": "歌手"}[type_name]
        
        self.log("="*60)
        self.log(f"🚀 開始爬取{type_text}: {name}")
        self.log("="*60)
        
        # 搜尋指定類型的人
        self.log(f"\n🔍 搜尋{type_text}...")
        
        if type_name == "writer":
            person_info = self.search_writer(name, delay)
        elif type_name == "composer":
            person_info = self.search_composer(name, delay)
        elif type_name == "singer":
            person_info = self.search_singer(name, delay)
        
        if not person_info:
            self.log(f"❌ 未找到{type_text}: {name}")
            messagebox.showerror("錯誤", f"未找到{type_text}: {name}")
            return
        
        self.log(f"✓ 找到: {person_info['name']}")
        
        person_dir = os.path.join(output_dir, self.safe_filename(person_info['name']))
        os.makedirs(person_dir, exist_ok=True)
        
        # 爬取歌曲
        if type_name == "writer":
            count = self.crawl_writer_songs(person_info, output_dir, delay)
        elif type_name == "composer":
            count = self.crawl_composer_songs(person_info, output_dir, delay)
        elif type_name == "singer":
            count = self.crawl_singer_songs(person_info, output_dir, delay)
        
        self.log("\n" + "="*60)
        self.log(f"✅ 完成！下載歌曲: {count}")
        self.log("="*60)
        messagebox.showinfo("完成", f"爬取完成！\n\n下載歌曲: {count}")
    
    
    def get_writers_from_page(self, page_num, delay):
        """從指定頁數獲取所有作詞人資訊"""
        try:
            time.sleep(delay)
            url = f"{self.base_url}/writers?page={page_num}"
            response = requests.get(url, headers=self.headers, timeout=15)
            soup = BeautifulSoup(response.text, 'lxml')
            
            writers = []
            for link in soup.find_all('a', href=True):
                if '/writer/' in link.get('href', ''):
                    name = link.get_text(strip=True)
                    if name:
                        writers.append({
                            'name': name,
                            'url': urljoin(self.base_url, link['href'])
                        })
            
            return list({w['url']: w for w in writers}.values())
        except Exception as e:
            self.log(f"  ✗ 錯誤: {e}")
            return []
    
    def get_composers_from_page(self, page_num, delay):
        """從指定頁數獲取所有作曲人資訊"""
        try:
            time.sleep(delay)
            url = f"{self.base_url}/composers?page={page_num}"
            self.log(f"    請求URL: {url}")
            response = requests.get(url, headers=self.headers, timeout=15)
            soup = BeautifulSoup(response.text, 'lxml')
            
            composers = []
            links = soup.find_all('a', href=True)
            self.log(f"    找到 {len(links)} 個連結")
            
            for link in links:
                href = link.get('href', '')
                if '/composer/' in href:
                    name = link.get_text(strip=True)
                    if name:
                        composers.append({
                            'name': name,
                            'url': urljoin(self.base_url, href)
                        })
                        self.log(f"      作曲人: {name}")
            
            self.log(f"    總共找到 {len(composers)} 個作曲人")
            return list({c['url']: c for c in composers}.values())
        except Exception as e:
            self.log(f"  ✗ 錯誤: {e}")
            return []
    
    def get_singers_from_page(self, page_num, delay):
        """從指定頁數獲取所有歌手資訊"""
        try:
            time.sleep(delay)
            url = f"{self.base_url}/singers?page={page_num}"
            response = requests.get(url, headers=self.headers, timeout=15)
            soup = BeautifulSoup(response.text, 'lxml')
            
            singers = []
            for link in soup.find_all('a', href=True):
                if '/singer/' in link.get('href', ''):
                    name = link.get_text(strip=True)
                    if name:
                        singers.append({
                            'name': name,
                            'url': urljoin(self.base_url, link['href'])
                        })
            
            return list({s['url']: s for s in singers}.values())
        except Exception as e:
            self.log(f"  ✗ 錯誤: {e}")
            return []
    
    def search_writer(self, writer_name, delay):
        """在前5頁中搜尋指定的作詞人"""
        # 簡化版：遍歷前5頁查找
        for page in range(1, 6):
            time.sleep(delay)
            writers = self.get_writers_from_page(page, 0)
            for writer in writers:
                if writer_name in writer['name'] or writer['name'] in writer_name:
                    return writer
        return None
    
    def search_composer(self, composer_name, delay):
        """在前5頁中搜尋指定的作曲人"""
        # 遍歷前5頁查找作曲人
        for page in range(1, 6):
            time.sleep(delay)
            self.log(f"    搜尋第{page}頁...")
            composers = self.get_composers_from_page(page, 0)
            self.log(f"    找到 {len(composers)} 個作曲人")
            
            for composer in composers:
                self.log(f"    檢查: {composer['name']}")
                if composer_name in composer['name'] or composer['name'] in composer_name:
                    self.log(f"    ✓ 匹配: {composer['name']}")
                    return composer
        return None
    
    def search_singer(self, singer_name, delay):
        """在前5頁中搜尋指定的歌手"""
        # 遍歷前5頁查找歌手
        for page in range(1, 6):
            time.sleep(delay)
            singers = self.get_singers_from_page(page, 0)
            for singer in singers:
                if singer_name in singer['name'] or singer['name'] in singer_name:
                    return singer
        return None
    
    def crawl_writer_songs(self, writer_info, base_dir, delay):
        """爬取指定作詞人的所有歌曲並保存到檔案"""
        try:
            time.sleep(delay)
            response = requests.get(writer_info['url'], headers=self.headers, timeout=15)
            soup = BeautifulSoup(response.text, 'lxml')
            
            table = soup.find('table', {'class': 'table'})
            if not table:
                return 0
            
            songs = []
            rows = table.find_all('tr')[1:]
            for row in rows:
                cells = row.find_all('td')
                if len(cells) >= 4:
                    song_link = cells[1].find('a')
                    if song_link:
                        href = song_link['href']
                        songs.append({
                            'name': song_link.get_text(strip=True),
                            'singer': cells[2].get_text(strip=True),
                            'url': href if href.startswith('http') else urljoin(self.base_url, href)
                        })
            
            self.log(f"    找到 {len(songs)} 首歌曲")
            
            writer_dir = os.path.join(base_dir, self.safe_filename(writer_info['name']))
            os.makedirs(writer_dir, exist_ok=True)
            
            count = 0
            for song in songs:
                if not self.is_crawling:
                    break
                
                filename = f"{self.safe_filename(song['singer'])} - {self.safe_filename(song['name'])}.txt"
                filepath = os.path.join(writer_dir, filename)
                
                if os.path.exists(filepath):
                    continue
                
                lyrics = self.download_lyrics(song['url'], delay)
                if lyrics:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(lyrics)
                    count += 1
            
            return count
            
        except Exception as e:
            self.log(f"    ✗ 錯誤: {e}")
            return 0
    
    def crawl_composer_songs(self, composer_info, base_dir, delay):
        """爬取指定作曲人的所有歌曲並保存到檔案"""
        try:
            time.sleep(delay)
            response = requests.get(composer_info['url'], headers=self.headers, timeout=15)
            soup = BeautifulSoup(response.text, 'lxml')
            
            # 先嘗試找表格
            table = soup.find('table', {'class': 'table'})
            if not table:
                # 如果沒有找到表格，嘗試其他可能的選擇器
                table = soup.find('table')
                if not table:
                    self.log(f"    ✗ 未找到歌曲表格")
                    return 0
            
            songs = []
            rows = table.find_all('tr')[1:]  # 跳過標題行
            
            self.log(f"    解析到 {len(rows)} 行資料")
            
            for i, row in enumerate(rows):
                cells = row.find_all('td')
                self.log(f"    第{i+1}行有 {len(cells)} 個欄位")
                
                if len(cells) >= 2:  # 至少需要2個欄位
                    # 嘗試不同的欄位組合
                    song_name = ""
                    singer_name = ""
                    song_url = ""
                    
                    # 尋找歌曲連結
                    for cell in cells:
                        link = cell.find('a', href=True)
                        if link and ('/song/' in link.get('href', '') or '/lyric/' in link.get('href', '')):
                            song_name = link.get_text(strip=True)
                            song_url = link.get('href')
                            break
                    
                    # 如果沒找到歌曲連結，嘗試其他方式
                    if not song_name and len(cells) >= 2:
                        # 嘗試從不同欄位獲取歌曲名稱
                        for j, cell in enumerate(cells):
                            link = cell.find('a', href=True)
                            if link:
                                song_name = link.get_text(strip=True)
                                song_url = link.get('href')
                                break
                        
                        # 如果還是沒找到，使用第二個欄位的文字
                        if not song_name and len(cells) >= 2:
                            song_name = cells[1].get_text(strip=True)
                    
                    # 無論是否找到歌曲連結，都要嘗試獲取歌手名稱（第3個欄位是歌手名稱）
                    if len(cells) >= 3:
                        singer_name = cells[2].get_text(strip=True)
                    elif len(cells) >= 4:
                        singer_name = cells[3].get_text(strip=True)
                    
                    if song_name:
                        songs.append({
                            'name': song_name,
                            'singer': singer_name or "未知歌手",
                            'url': song_url if song_url and song_url.startswith('http') else urljoin(self.base_url, song_url) if song_url else ""
                        })
                        self.log(f"      找到歌曲: {song_name} - {singer_name or '未知歌手'}")
            
            self.log(f"    總共找到 {len(songs)} 首歌曲")
            
            composer_dir = os.path.join(base_dir, self.safe_filename(composer_info['name']))
            os.makedirs(composer_dir, exist_ok=True)
            
            count = 0
            for song in songs:
                if not self.is_crawling:
                    break
                
                filename = f"{self.safe_filename(song['singer'])} - {self.safe_filename(song['name'])}.txt"
                filepath = os.path.join(composer_dir, filename)
                
                if os.path.exists(filepath):
                    continue
                
                lyrics = self.download_lyrics(song['url'], delay)
                if lyrics:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(lyrics)
                    count += 1
                    self.log(f"      下載: {song['name']}")
                else:
                    self.log(f"      ✗ 無法下載: {song['name']}")
            
            return count
            
        except Exception as e:
            self.log(f"    ✗ 错误: {e}")
            return 0
    
    def crawl_singer_songs(self, singer_info, base_dir, delay):
        """爬取指定歌手的所有歌曲並保存到檔案"""
        try:
            time.sleep(delay)
            response = requests.get(singer_info['url'], headers=self.headers, timeout=15)
            soup = BeautifulSoup(response.text, 'lxml')
            
            # 先嘗試找表格
            table = soup.find('table', {'class': 'table'})
            if not table:
                # 如果沒有找到表格，嘗試其他可能的選擇器
                table = soup.find('table')
                if not table:
                    self.log(f"    ✗ 未找到歌曲表格")
                    return 0
            
            songs = []
            rows = table.find_all('tr')[1:]  # 跳過標題行
            
            self.log(f"    解析到 {len(rows)} 行資料")
            
            for i, row in enumerate(rows):
                cells = row.find_all('td')
                self.log(f"    第{i+1}行有 {len(cells)} 個欄位")
                
                if len(cells) >= 2:  # 至少需要2個欄位
                    # 嘗試不同的欄位組合
                    song_name = ""
                    singer_name = ""
                    song_url = ""
                    
                    # 尋找歌曲連結
                    for cell in cells:
                        link = cell.find('a', href=True)
                        if link and ('/song/' in link.get('href', '') or '/lyric/' in link.get('href', '')):
                            song_name = link.get_text(strip=True)
                            song_url = link.get('href')
                            break
                    
                    # 如果沒找到歌曲連結，嘗試其他方式
                    if not song_name and len(cells) >= 2:
                        for cell in cells:
                            link = cell.find('a', href=True)
                            if link:
                                song_name = link.get_text(strip=True)
                                song_url = link.get('href')
                                break
                        
                        if not song_name and len(cells) >= 2:
                            song_name = cells[1].get_text(strip=True)
                    
                    # 無論是否找到歌曲連結，都要嘗試獲取歌手名稱（第3個欄位是歌手名稱）
                    if len(cells) >= 3:
                        singer_name = cells[2].get_text(strip=True)
                    elif len(cells) >= 4:
                        singer_name = cells[3].get_text(strip=True)
                    
                    if song_name:
                        songs.append({
                            'name': song_name,
                            'singer': singer_name or singer_info['name'],  # 使用歌手名稱作為預設值
                            'url': song_url if song_url and song_url.startswith('http') else urljoin(self.base_url, song_url) if song_url else ""
                        })
                        self.log(f"      找到歌曲: {song_name} - {singer_name or singer_info['name']}")
            
            self.log(f"    總共找到 {len(songs)} 首歌曲")
            
            singer_dir = os.path.join(base_dir, self.safe_filename(singer_info['name']))
            os.makedirs(singer_dir, exist_ok=True)
            
            count = 0
            for song in songs:
                if not self.is_crawling:
                    break
                
                filename = f"{self.safe_filename(song['singer'])} - {self.safe_filename(song['name'])}.txt"
                filepath = os.path.join(singer_dir, filename)
                
                if os.path.exists(filepath):
                    continue
                
                lyrics = self.download_lyrics(song['url'], delay)
                if lyrics:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(lyrics)
                    count += 1
            
            return count
            
        except Exception as e:
            self.log(f"    ✗ 错误: {e}")
            return 0
    
    def download_lyrics(self, url, delay):
        """從指定URL下載歌詞內容（提取「下載txt文檔」到「更多」之間的內容）"""
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
                    self.log(f"      找到開始標記: {line}")
                # 尋找結束標記：更多
                elif '更多' in line and start_idx is not None:
                    end_idx = i
                    self.log(f"      找到結束標記: {line}")
                    break
            
            if start_idx and end_idx and start_idx < end_idx:
                extracted = lines[start_idx:end_idx]
                clean_lines = [line.strip() for line in extracted if line.strip()]
                self.log(f"      提取了 {len(clean_lines)} 行歌詞")
                return '\n'.join(clean_lines)
            else:
                self.log(f"      未找到標記，start_idx: {start_idx}, end_idx: {end_idx}")
                return None
            
        except Exception as e:
            self.log(f"      下載歌詞錯誤: {e}")
            return None
    
    def safe_filename(self, name):
        """將檔案名轉換為安全的檔案系統名稱"""
        return re.sub(r'[<>:"/\\|?*]', '_', name)[:100]


def main():
    """主程式入口點"""
    root = tk.Tk()
    LyricsCrawlerApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()

