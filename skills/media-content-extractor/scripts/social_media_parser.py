#!/usr/bin/env python3
"""
社交媒体链接解析器
支持抖音、小红书、B站等平台的视频/图片下载
"""

import os
import tempfile
from typing import Optional
from urllib.parse import urlparse


class SocialMediaParser:
    """社交媒体链接解析器"""

    def __init__(self):
        pass

    def download_media(self, url: str) -> tuple[str, str]:
        """
        下载社交媒体的媒体内容

        Args:
            url: 社交媒体链接

        Returns:
            (本地文件路径, 媒体类型) 元组
        """
        try:
            import yt_dlp
        except ImportError:
            raise ImportError(
                "yt-dlp 未安装。请运行: pip install yt-dlp"
            )

        output_template = os.path.join(tempfile.gettempdir(), "media_%(id)s.%(ext)s")

        ydl_opts = {
            'format': 'best',
            'outtmpl': output_template,
            'quiet': True,
            'no_warnings': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filepath = ydl.prepare_filename(info)

            if info.get('ext'):
                media_type = self._determine_media_type(filepath)
            else:
                media_type = 'video'

            return filepath, media_type

    def _determine_media_type(self, filepath: str) -> str:
        """根据文件扩展名确定媒体类型"""
        ext = os.path.splitext(filepath)[1].lower()

        image_exts = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
        video_exts = {'.mp4', '.mov', '.avi', '.mkv', '.webm'}

        if ext in image_exts:
            return 'image'
        elif ext in video_exts:
            return 'video'
        else:
            return 'unknown'


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python social_media_parser.py <social_media_url>")
        sys.exit(1)

    parser = SocialMediaParser()
    filepath, media_type = parser.download_media(sys.argv[1])
    print(f"下载完成: {filepath} (类型: {media_type})")
