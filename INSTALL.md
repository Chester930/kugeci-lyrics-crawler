# 📦 安裝指南

## 🎯 快速安裝（推薦）

### Windows 用戶
1. **下載專案**
   ```bash
   git clone https://github.com/您的用戶名/kugeci-lyrics-crawler.git
   cd kugeci-lyrics-crawler
   ```

2. **一鍵安裝**
   - 雙擊 `install.bat` 檔案
   - 等待安裝完成

3. **啟動程式**
   - 雙擊 `start.bat` 檔案
   - 程式會自動啟動

### Linux/macOS 用戶
1. **下載專案**
   ```bash
   git clone https://github.com/您的用戶名/kugeci-lyrics-crawler.git
   cd kugeci-lyrics-crawler
   ```

2. **安裝依賴**
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

3. **啟動程式**
   ```bash
   python3 run.py
   ```

## 🔧 手動安裝

如果自動安裝腳本無法使用，可以手動安裝：

### 1. 檢查Python環境
```bash
python --version
# 或
python3 --version
```
確保版本為 3.7 或更高

### 2. 安裝依賴套件
```bash
# Windows
pip install -r requirements.txt

# Linux/macOS
pip3 install -r requirements.txt
```

### 3. 啟動程式
```bash
# Windows
python run.py
# 或
python src/lyrics_crawler_app.py

# Linux/macOS
python3 run.py
# 或
python3 src/lyrics_crawler_app.py
```

## 🐛 常見問題

### Q: 雙擊bat檔案沒有反應？
A: 請嘗試在命令提示字元中運行：
```bash
cd "專案路徑"
install.bat
start.bat
```

### Q: 提示「python不是內部或外部命令」？
A: 請先安裝Python並確保添加到系統PATH中

### Q: 依賴套件安裝失敗？
A: 嘗試使用管理員權限運行命令提示字元，或使用：
```bash
pip install --user -r requirements.txt
```

### Q: GUI界面沒有顯示？
A: 運行診斷腳本：
```bash
python test_gui.py
```

## 📋 檔案說明

- `install.bat` - Windows安裝腳本
- `install.sh` - Linux/macOS安裝腳本
- `start.bat` - Windows啟動腳本
- `run.py` - 跨平台啟動腳本
- `test_gui.py` - GUI診斷腳本
- `requirements.txt` - 依賴套件清單
