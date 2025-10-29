@echo off
echo ========================================
echo    酷歌詞爬蟲工具 - 快速開始
echo ========================================
echo.

echo 步驟1: 檢查Python環境...
python --version
if %errorlevel% neq 0 (
    echo 錯誤：未找到Python，請先安裝Python 3.7+
    echo 下載地址：https://www.python.org/downloads/
    pause
    exit /b 1
)

echo.
echo 步驟2: 安裝依賴套件...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo 警告：依賴套件安裝可能不完整，但程式仍可嘗試運行
)

echo.
echo 步驟3: 啟動程式...
echo 正在啟動酷歌詞爬蟲工具...
python src/lyrics_crawler_app.py

echo.
echo 程式已結束
pause
