# 🎵 酷歌詞爬蟲工具 (Kugeci Lyrics Crawler)

一個功能強大的圖形界面歌詞爬蟲工具，支援按歌手、作詞人、作曲人爬取酷歌詞網站的歌詞內容。

## ✨ 功能特色

- 🎤 **多類型爬取**：支援歌手、作詞人、作曲人三種類型
- 📝 **雙模式搜尋**：按人名搜尋或按頁數範圍爬取
- 🖥️ **圖形界面**：直觀易用的Tkinter GUI界面
- 📁 **自動整理**：自動創建資料夾並按類型分類保存
- 🔍 **智能提取**：精確提取歌詞內容，過濾網頁雜訊
- ⚡ **多執行緒**：背景執行，不阻塞界面操作
- 🛡️ **安全延遲**：可設定請求延遲，避免被封禁

## 🚀 快速開始

### 環境要求

- Python 3.7+
- Windows/Linux/macOS

### 📥 下載專案

```bash
git clone https://github.com/您的用戶名/kugeci-lyrics-crawler.git
cd kugeci-lyrics-crawler
```

### 🔧 安裝步驟

#### Windows 用戶
1. **安裝依賴套件**：
   ```bash
   # 方法一：使用安裝腳本（推薦）
   雙擊 install.bat
   
   # 方法二：手動安裝
   pip install -r requirements.txt
   ```

2. **啟動程式**：
   ```bash
   # 方法一：使用啟動腳本（推薦）
   雙擊 start.bat
   
   # 方法二：手動啟動
   python run.py
   # 或
   python src/lyrics_crawler_app.py
   ```

#### Linux/macOS 用戶
1. **安裝依賴套件**：
   ```bash
   # 使用安裝腳本
   chmod +x install.sh
   ./install.sh
   
   # 或手動安裝
   pip3 install -r requirements.txt
   ```

2. **啟動程式**：
   ```bash
   python3 run.py
   # 或
   python3 src/lyrics_crawler_app.py
   ```

### ⚡ 一鍵啟動（Windows）

如果您是Windows用戶，最簡單的方式就是：
1. 雙擊 `install.bat` 安裝依賴
2. 雙擊 `start.bat` 啟動程式

## 📖 使用說明

### 1. 選擇爬取類型
- **👤 作詞人**：爬取指定作詞人的所有歌曲
- **🎼 作曲人**：爬取指定作曲人的所有歌曲  
- **🎤 歌手**：爬取指定歌手的所有歌曲

### 2. 選擇爬取模式
- **📝 按人名爬取**：輸入具體的人名進行搜尋
- **📄 按頁數範圍爬取**：爬取指定頁數範圍內的所有人員

### 3. 設定參數
- **人名**：輸入要搜尋的歌手/作詞人/作曲人名稱
- **頁數範圍**：設定起始頁和結束頁
- **請求延遲**：建議設定2-3秒，避免被封禁
- **保存位置**：選擇歌詞檔案的保存目錄

### 4. 開始爬取
點擊「🚀 開始爬取」按鈕，程式會在背景執行爬取作業。

## 📁 檔案結構

```
kugeci-lyrics-crawler/
├── src/
│   └── lyrics_crawler_app.py    # 主應用程式
├── docs/
│   └── README.md                # 說明文件
├── examples/
│   └── sample_output/           # 範例輸出
├── requirements.txt             # 依賴套件
├── .gitignore                  # Git忽略檔案
├── LICENSE                     # 授權條款
└── README.md                   # 專案說明
```

## 🎯 輸出格式

### 檔案命名規則
```
歌手名 - 歌曲名.txt
```

### 歌詞內容格式
```
歌曲名 - 歌手名
詞：作詞人
曲：作曲人
編曲：編曲人
後期：後期製作

[歌詞內容]
```

## ⚠️ 重要聲明

- **僅供學習研究使用**
- **請遵守版權法規**
- **不得用於商業用途**
- **請尊重網站服務條款**

## 🔧 技術細節

### 核心技術
- **GUI框架**：Tkinter
- **網頁爬取**：requests + BeautifulSoup
- **多執行緒**：threading
- **檔案處理**：os, re

### 爬取策略
1. 智能解析HTML表格結構
2. 精確提取歌詞內容（「下載txt文檔」到「更多」之間）
3. 自動處理歌手名稱提取
4. 安全的檔案名轉換

## 🐛 問題回報

如果您發現任何問題或有改進建議，請在GitHub上提交Issue。

## 📄 授權條款

本專案採用MIT授權條款，詳見[LICENSE](LICENSE)檔案。

## 🙏 致謝

感謝酷歌詞網站提供豐富的歌詞資源。

---

**免責聲明**：本工具僅供學習和研究使用，使用者需自行承擔使用風險，並遵守相關法律法規。
