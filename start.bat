@echo off
echo 啟動酷歌詞爬蟲工具...
echo ====================

cd /d "%~dp0"
python src/lyrics_crawler_app.py

if %errorlevel% neq 0 (
    echo.
    echo 程式執行出現錯誤，請檢查Python環境
    echo 或嘗試運行: python src/lyrics_crawler_app.py
    echo.
    pause
)
