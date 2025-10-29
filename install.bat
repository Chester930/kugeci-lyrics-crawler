@echo off
echo 酷歌詞爬蟲工具安裝腳本
echo ========================

echo 正在檢查Python環境...
python --version
if %errorlevel% neq 0 (
    echo 錯誤：未找到Python，請先安裝Python 3.7+
    pause
    exit /b 1
)

echo.
echo 正在安裝依賴套件...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo 錯誤：依賴套件安裝失敗
    pause
    exit /b 1
)

echo.
echo 安裝完成！
echo 使用 python run.py 啟動程式
echo.
pause
