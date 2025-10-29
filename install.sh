#!/bin/bash
# 酷歌詞爬蟲工具安裝腳本 (Linux/macOS)

echo "酷歌詞爬蟲工具安裝腳本"
echo "========================"

# 檢查Python環境
echo "正在檢查Python環境..."
if ! command -v python3 &> /dev/null; then
    echo "錯誤：未找到Python3，請先安裝Python 3.7+"
    exit 1
fi

python3 --version

echo ""
echo "正在安裝依賴套件..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "錯誤：依賴套件安裝失敗"
    exit 1
fi

echo ""
echo "安裝完成！"
echo "使用 python3 run.py 啟動程式"
echo ""
