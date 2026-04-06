#!/usr/bin/env python3
"""
图片获取工具
支持从免费图库获取高质量图片
"""

import requests
import os
import re
from typing import List, Optional
from urllib.parse import urlparse


class ImageFetcher:
    """图片获取器"""

    def __init__(self, temp_dir: str = "/tmp/wechat_mp_images"):
        """
        初始化图片获取器

        Args:
            temp_dir: 临时保存目录
        """
        self.temp_dir = temp_dir
        os.makedirs(temp_dir, exist_ok=True)

    def fetch_from_unsplash(self, query: str, count: int = 5) -> List[str]:
        """
        从 Unsplash 获取图片

        Args:
            query: 搜索关键词
            count: 获取数量

        Returns:
            图片 URL 列表
        """
        unsplash_api = "https://source.unsplash.com/random"
        urls = []

        for i in range(count):
            url = f"{unsplash_api}?{query}&sig={i}"
            urls.append(url)

        return urls

    def fetch_from_pexels(self, query: str, count: int = 5, api_key: Optional[str] = None) -> List[str]:
        """
        从 Pexels 获取图片

        Args:
            query: 搜索关键词
            count: 获取数量
            api_key: Pexels API Key（可选，需要免费注册）

        Returns:
            图片 URL 列表
        """
        if not api_key:
            # 无 API Key 时使用直接搜索 URL
            urls = []
            for i in range(count):
                urls.append(f"https://images.pexels.com/photos/placeholder/{query}?sig={i}")
            return urls

        api_url = "https://api.pexels.com/v1/search"
        headers = {"Authorization": api_key}
        params = {"query": query, "per_page": count, "orientation": "landscape"}

        try:
            response = requests.get(api_url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            urls = [photo["src"]["large"] for photo in data.get("photos", [])]
            return urls

        except Exception as e:
            print(f"Pexels API 调用失败: {str(e)}")
            return []

    def fetch_from_pixabay(self, query: str, count: int = 5, api_key: Optional[str] = None) -> List[str]:
        """
        从 Pixabay 获取图片

        Args:
            query: 搜索关键词
            count: 获取数量
            api_key: Pixabay API Key（可选，需要免费注册）

        Returns:
            图片 URL 列表
        """
        if not api_key:
            return []

        api_url = "https://pixabay.com/api/"
        params = {
            "key": api_key,
            "q": query,
            "image_type": "photo",
            "per_page": count,
            "safesearch": "true"
        }

        try:
            response = requests.get(api_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            urls = [hit["webformatURL"] for hit in data.get("hits", [])]
            return urls

        except Exception as e:
            print(f"Pixabay API 调用失败: {str(e)}")
            return []

    def download_image(self, url: str, filename: Optional[str] = None) -> str:
        """
        下载图片到本地

        Args:
            url: 图片 URL
            filename: 保存文件名（可选）

        Returns:
            本地文件路径
        """
        try:
            response = requests.get(url, timeout=30, stream=True)
            response.raise_for_status()

            # 确定文件名
            if not filename:
                parsed_url = urlparse(url)
                filename = os.path.basename(parsed_url.path)
                if not filename or "." not in filename:
                    filename = f"image_{int(os.times()[4])}.jpg"

            filepath = os.path.join(self.temp_dir, filename)

            # 保存文件
            with open(filepath, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            return filepath

        except Exception as e:
            raise Exception(f"下载图片失败: {str(e)}")

    def search_and_download(self, query: str, count: int = 1, source: str = "unsplash") -> List[str]:
        """
        搜索并下载图片

        Args:
            query: 搜索关键词
            count: 下载数量
            source: 图片来源（unsplash, pexels, pixabay）

        Returns:
            本地文件路径列表
        """
        # 获取图片 URL
        if source == "unsplash":
            urls = self.fetch_from_unsplash(query, count)
        elif source == "pexels":
            urls = self.fetch_from_pexels(query, count)
        elif source == "pixabay":
            urls = self.fetch_from_pixabay(query, count)
        else:
            raise ValueError(f"不支持的图片来源: {source}")

        # 下载图片
        filepaths = []
        for i, url in enumerate(urls):
            try:
                ext = self._guess_extension(url)
                filename = f"{query}_{i}{ext}"
                filepath = self.download_image(url, filename)
                filepaths.append(filepath)
            except Exception as e:
                print(f"下载第 {i+1} 张图片失败: {str(e)}")
                continue

        return filepaths

    def _guess_extension(self, url: str) -> str:
        """猜测图片扩展名"""
        if ".jpg" in url.lower() or ".jpeg" in url.lower():
            return ".jpg"
        elif ".png" in url.lower():
            return ".png"
        elif ".webp" in url.lower():
            return ".webp"
        else:
            return ".jpg"


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python image_fetcher.py <query> [count] [source]")
        sys.exit(1)

    query = sys.argv[1]
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    source = sys.argv[3] if len(sys.argv) > 3 else "unsplash"

    fetcher = ImageFetcher()
    filepaths = fetcher.search_and_download(query, count, source)

    for fp in filepaths:
        print(f"Downloaded: {fp}")
