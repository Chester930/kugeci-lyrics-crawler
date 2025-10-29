#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
酷歌詞爬蟲工具安裝配置
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="kugeci-lyrics-crawler",
    version="1.0.0",
    author="Kugeci Lyrics Crawler Team",
    author_email="",
    description="一個功能強大的圖形界面歌詞爬蟲工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/kugeci-lyrics-crawler",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "kugeci-crawler=src.lyrics_crawler_app:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
