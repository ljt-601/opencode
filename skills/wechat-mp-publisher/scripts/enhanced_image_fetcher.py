#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版图片获取器
支持多个免费图片源，确保稳定性
"""

import requests
import os
import re
from typing import List, Optional
from urllib.parse import urlparse
import random


class EnhancedImageFetcher:
    """增强版图片获取器，支持更多免费源"""

    def __init__(self, temp_dir: str = "/tmp/wechat_mp_images", pixabay_api_key: Optional[str] = None):
        self.temp_dir = temp_dir
        # 默认使用用户的 Pixabay API Key
        self.pixabay_api_key = pixabay_api_key if pixabay_api_key else "os.environ.get("PIXABAY_API_KEY", "")"
        os.makedirs(temp_dir, exist_ok=True)

    def fetch_from_pixabay(self, query: str, count: int = 5) -> List[str]:
        """
        从 Pixabay 获取图片（使用 API）

        Args:
            query: 搜索关键词
            count: 获取数量

        Returns:
            图片 URL 列表
        """
        if not self.pixabay_api_key:
            print("  ✗ Pixabay API Key 未配置")
            return []

        api_url = "https://pixabay.com/api/"
        # Pixabay per_page 参数范围是 3-200
        per_page = max(3, min(count, 200))
        params = {
            "key": self.pixabay_api_key,
            "q": query,
            "per_page": per_page
        }

        try:
            # 手动构建 URL 以避免编码问题
            from urllib.parse import urlencode
            full_url = f"{api_url}?{urlencode(params)}"
            response = requests.get(full_url, timeout=10)

            # 打印调试信息
            if response.status_code != 200:
                print(f"  ✗ Pixabay 返回错误 {response.status_code}: {response.text[:200]}")

            response.raise_for_status()
            data = response.json()

            if "hits" in data and len(data["hits"]) > 0:
                urls = []
                for hit in data["hits"][:count]:
                    # 使用大尺寸图片
                    image_url = hit["webformatURL"]
                    urls.append(image_url)
                return urls
            else:
                print(f"  ✗ Pixabay 没有找到 '{query}' 的图片")
                return []

        except Exception as e:
            print(f"  ✗ Pixabay API 调用失败: {str(e)}")
            return []

    def fetch_from_loremflickr(self, query: str, count: int = 5) -> List[str]:
        """
        从 LoremFlickr 获取图片（无需 API Key，非常稳定）

        Args:
            query: 搜索关键词
            count: 获取数量

        Returns:
            图片 URL 列表
        """
        urls = []
        for i in range(count):
            # LoremFlickr 提供稳定的随机图片服务
            url = f"https://loremflickr.com/900/383/{query}?random={i}"
            urls.append(url)
        return urls

    def fetch_from_picsum(self, count: int = 5) -> List[str]:
        """
        从 Picsum 获取高质量随机图片（无需 API Key）

        Args:
            count: 获取数量

        Returns:
            图片 URL 列表
        """
        urls = []
        for i in range(count):
            url = f"https://picsum.photos/900/383?random={i}"
            urls.append(url)
        return urls

    def fetch_from_unsplash_source(self, query: str, count: int = 5) -> List[str]:
        """
        从 Unsplash Source 获取图片（备用方案）

        Args:
            query: 搜索关键词
            count: 获取数量

        Returns:
            图片 URL 列表
        """
        urls = []
        keywords = query.replace(" ", ",").split(",")
        for i in range(count):
            keyword = random.choice(keywords) if keywords else query
            url = f"https://source.unsplash.com/900x383/?{keyword}&sig={i}"
            urls.append(url)
        return urls

    def fetch_from_bing_wallpaper(self, query: str, count: int = 5) -> List[str]:
        """
        使用 Bing 壁纸 API（需要模拟浏览器）

        注意：这个方法可能不稳定，建议使用前三个方法

        Args:
            query: 搜索关键词
            count: 获取数量

        Returns:
            图片 URL 列表
        """
        # Bing 壁纸 API（简化版）
        urls = []
        for i in range(count):
            url = f"https://bing.com/th?id=OHR.{query}{i}_1920x1080.jpg"
            urls.append(url)
        return urls

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
            # 设置 User-Agent，避免被拒绝
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=30, stream=True)
            response.raise_for_status()

            # 确定文件名
            if not filename:
                parsed_url = urlparse(url)
                filename = os.path.basename(parsed_url.path)
                if not filename or "." not in filename:
                    filename = f"image_{random.randint(1000, 9999)}.jpg"

            filepath = os.path.join(self.temp_dir, filename)

            # 保存文件
            with open(filepath, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            return filepath

        except Exception as e:
            raise Exception(f"下载图片失败: {str(e)}")

    def search_and_download(self, query: str, count: int = 1, prefer_source: str = "auto") -> List[str]:
        """
        搜索并下载图片（自动尝试多个源）

        Args:
            query: 搜索关键词
            count: 下载数量
            prefer_source: 优先使用的源（loremflickr, picsum, unsplash, auto）

        Returns:
            本地文件路径列表
        """
        # 定义图片源策略
        sources = []

        if prefer_source == "auto":
            # 自动模式：按优先级尝试（Pixabay 优先）
            sources = [
                ("pixabay", lambda q, c: self.fetch_from_pixabay(q, c)),
                ("loremflickr", lambda q, c: self.fetch_from_loremflickr(q, c)),
                ("picsum", lambda q, c: self.fetch_from_picsum(c)),
            ]
        else:
            # 指定源
            if prefer_source == "pixabay":
                sources = [("pixabay", lambda q, c: self.fetch_from_pixabay(q, c))]
            elif prefer_source == "loremflickr":
                sources = [("loremflickr", lambda q, c: self.fetch_from_loremflickr(q, c))]
            elif prefer_source == "picsum":
                sources = [("picsum", lambda q, c: self.fetch_from_picsum(c))]

        # 尝试每个源
        for source_name, fetch_func in sources:
            try:
                print(f"尝试从 {source_name} 获取图片...")
                urls = fetch_func(query, count)

                filepaths = []
                for i, url in enumerate(urls):
                    try:
                        ext = self._guess_extension(url)
                        filename = f"{query.replace(' ', '_')}_{source_name}_{i}{ext}"
                        filepath = self.download_image(url, filename)
                        filepaths.append(filepath)
                        print(f"  ✓ 成功下载: {os.path.basename(filepath)}")
                    except Exception as e:
                        print(f"  ✗ 下载第 {i+1} 张失败: {str(e)}")
                        continue

                if filepaths:
                    print(f"✓ 从 {source_name} 成功获取 {len(filepaths)} 张图片")
                    return filepaths

            except Exception as e:
                print(f"✗ 从 {source_name} 获取失败: {str(e)}")
                continue

        # 所有源都失败
        raise Exception("所有图片源都失败了，请稍后重试或提供本地图片")

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
        print("Usage: python enhanced_image_fetcher.py <query> [count] [source]")
        print("Sources: pixabay, loremflickr, picsum, auto")
        print("Note: pixabay requires API key (already configured)")
        sys.exit(1)

    query = sys.argv[1]
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    source = sys.argv[3] if len(sys.argv) > 3 else "auto"

    fetcher = EnhancedImageFetcher()
    try:
        filepaths = fetcher.search_and_download(query, count, source)
        print("\n下载完成:")
        for fp in filepaths:
            print(f"  {fp}")
    except Exception as e:
        print(f"\n错误: {str(e)}")
        sys.exit(1)
