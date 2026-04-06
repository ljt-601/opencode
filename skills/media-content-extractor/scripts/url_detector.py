#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
URL 类型检测和识别
支持识别 URL 类型（图片、视频、社交媒体等）
"""

import re
from enum import Enum
from urllib.parse import urlparse
from typing import Optional


class ContentType(Enum):
    """内容类型枚举"""
    IMAGE = "image"
    VIDEO = "video"
    SOCIAL_MEDIA = "social_media"
    UNKNOWN = "unknown"


class SocialPlatform(Enum):
    """社交媒体平台枚举"""
    DOUYIN = "douyin"
    XIAOHONGSHU = "xiaohongshu"
    BILIBILI = "bilibili"
    YOUTUBE = "youtube"
    WEIBO = "weibo"


class URLDetector:
    """URL 类型检测器"""

    IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg'}

    VIDEO_EXTENSIONS = {'.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm', '.m4v'}

    SOCIAL_PATTERNS = {
        SocialPlatform.DOUYIN: [
            r'douyin\.com',
            r'iesdouyin\.com'
        ],
        SocialPlatform.XIAOHONGSHU: [
            r'xiaohongshu\.com',
            r'xhslink\.com'
        ],
        SocialPlatform.BILIBILI: [
            r'bilibili\.com',
            r'b23\.tv'
        ],
        SocialPlatform.YOUTUBE: [
            r'youtube\.com',
            r'youtu\.be'
        ],
        SocialPlatform.WEIBO: [
            r'weibo\.com',
            r'weibo\.cn'
        ]
    }

    def __init__(self):
        pass

    def detect(self, url_or_path: str) -> tuple[ContentType, Optional[SocialPlatform]]:
        """
        检测 URL 或本地路径的内容类型

        Args:
            url_or_path: URL 或本地文件路径

        Returns:
            (内容类型, 社交平台) 元组
        """
        if self._is_local_file(url_or_path):
            return self._detect_local_file(url_or_path)

        platform = self._detect_social_platform(url_or_path)
        if platform:
            return (ContentType.SOCIAL_MEDIA, platform)

        if self._is_image_url(url_or_path):
            return (ContentType.IMAGE, None)

        if self._is_video_url(url_or_path):
            return (ContentType.VIDEO, None)

        return (ContentType.UNKNOWN, None)

    def _is_local_file(self, path: str) -> bool:
        """检查是否是本地文件路径"""
        return not path.startswith(('http://', 'https://', 'ftp://'))

    def _detect_local_file(self, path: str) -> tuple[ContentType, Optional[SocialPlatform]]:
        """检测本地文件类型"""
        ext = self._get_extension(path).lower()

        if ext in self.IMAGE_EXTENSIONS:
            return (ContentType.IMAGE, None)
        elif ext in self.VIDEO_EXTENSIONS:
            return (ContentType.VIDEO, None)

        return (ContentType.UNKNOWN, None)

    def _detect_social_platform(self, url: str) -> Optional[SocialPlatform]:
        """检测社交媒体平台"""
        url_lower = url.lower()

        for platform, patterns in self.SOCIAL_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, url_lower):
                    return platform

        return None

    def _is_image_url(self, url: str) -> bool:
        """检查是否是图片 URL"""
        ext = self._get_extension(url).lower()
        return ext in self.IMAGE_EXTENSIONS

    def _is_video_url(self, url: str) -> bool:
        """检查是否是视频 URL"""
        ext = self._get_extension(url).lower()
        return ext in self.VIDEO_EXTENSIONS

    def _get_extension(self, path: str) -> str:
        """获取文件扩展名"""
        parsed = urlparse(path)
        path = parsed.path

        _, ext = path.rsplit('.', 1) if '.' in path else ('', '')
        return f'.{ext}' if ext else ''

if __name__ == "__main__":
    import sys

    detector = URLDetector()

    test_cases = [
        "https://example.com/image.jpg",
        "https://example.com/video.mp4",
        "https://www.douyin.com/video/12345",
        "https://www.bilibili.com/video/BV1xx",
        "/Users/test/local_photo.png",
        "/Users/test/local_movie.mp4",
        "https://unknown.com/file"
    ]

    print("URL 类型检测测试：\n")
    for test_url in test_cases:
        content_type, platform = detector.detect(test_url)
        platform_str = f" ({platform.value})" if platform else ""
        print(f"{test_url:50} -> {content_type.value}{platform_str}")
