#!/usr/bin/env python3
"""
媒体内容文字提取器主入口
整合图片 OCR、视频处理、社交媒体解析功能
"""

from url_detector import URLDetector, ContentType, SocialPlatform
from image_ocr import ImageOCR
from video_processor import VideoProcessor
from social_media_parser import SocialMediaParser
from typing import Optional


class ContentExtractor:
    """媒体内容文字提取器"""

    def __init__(self, asr_engine: str = "whisper", use_paddle: bool = True):
        """
        初始化内容提取器

        Args:
            asr_engine: ASR 引擎（whisper, faster-whisper）
            use_paddle: 是否使用 PaddleOCR
        """
        self.detector = URLDetector()
        self.ocr = ImageOCR(use_paddle=use_paddle)
        self.video_processor = VideoProcessor(asr_engine=asr_engine)
        self.social_parser = SocialMediaParser()

    def extract(self, url_or_path: str, method: str = "auto") -> dict:
        """
        从 URL 或本地文件提取文字

        Args:
            url_or_path: URL 或本地文件路径
            method: 提取方法（auto, asr, subtitle）

        Returns:
            包含 text 和 metadata 的字典
        """
        content_type, platform = self.detector.detect(url_or_path)

        if content_type == ContentType.UNKNOWN:
            return {
                "text": "",
                "error": "无法识别的内容类型",
                "metadata": {"type": "unknown"}
            }

        if content_type == ContentType.IMAGE:
            text = self.ocr.extract_text(url_or_path)
            return {
                "text": text,
                "metadata": {
                    "type": "image",
                    "source": url_or_path
                }
            }

        if content_type == ContentType.VIDEO:
            text = self.video_processor.extract_text(url_or_path, method)
            return {
                "text": text,
                "metadata": {
                    "type": "video",
                    "source": url_or_path,
                    "method": method
                }
            }

        if content_type == ContentType.SOCIAL_MEDIA:
            filepath, media_type = self.social_parser.download_media(url_or_path)

            try:
                if media_type == "image":
                    text = self.ocr.extract_text(filepath)
                elif media_type == "video":
                    text = self.video_processor.extract_text(filepath, method)
                else:
                    text = ""

                return {
                    "text": text,
                    "metadata": {
                        "type": "social_media",
                        "platform": platform.value if platform else "unknown",
                        "media_type": media_type,
                        "source": url_or_path
                    }
                }
            finally:
                import os
                if os.path.exists(filepath):
                    os.unlink(filepath)

        return {
            "text": "",
            "error": "不支持的内容类型",
            "metadata": {"type": "unsupported"}
        }


def extract_text(url_or_path: str, **kwargs) -> str:
    """
    便捷函数：直接提取文字

    Args:
        url_or_path: URL 或本地文件路径
        **kwargs: 传递给 ContentExtractor 的参数

    Returns:
        提取的文字内容
    """
    extractor = ContentExtractor(**kwargs)
    result = extractor.extract(url_or_path)
    return result.get("text", "")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python content_extractor.py <url_or_path> [method]")
        print("Methods: auto (default), asr, subtitle")
        sys.exit(1)

    method = sys.argv[2] if len(sys.argv) > 2 else "auto"
    extractor = ContentExtractor()
    result = extractor.extract(sys.argv[1], method)

    if "error" in result:
        print(f"错误: {result['error']}")
        sys.exit(1)

    print("提取的文字内容：")
    print(result["text"])
    print(f"\n元数据: {result['metadata']}")
