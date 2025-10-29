#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
酷歌詞爬蟲工具啟動腳本
Kugeci Lyrics Crawler Launcher
"""

import sys
import os

# 添加src目錄到Python路徑
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# 導入並運行主應用
from lyrics_crawler_app import main

if __name__ == '__main__':
    main()
