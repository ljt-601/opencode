#!/usr/bin/env python3
"""
图片 OCR 和文字提取
支持本地文件和 URL 下载
"""

import os
import requests
import tempfile
from pathlib import Path
from typing import Optional


class ImageOCR:
    """图片 OCR 文字提取器"""

    def __init__(self, use_paddle: bool = True):
        """
        初始化 OCR 引擎

        Args:
            use_paddle: 是否使用 PaddleOCR（默认 True）
                       False 时使用 Tesseract
        """
        self.use_paddle = use_paddle
        self.ocr_engine = None
        self._init_engine()

    def _init_engine(self):
        """初始化 OCR 引擎"""
        if self.use_paddle:
            try:
                from paddleocr import PaddleOCR
                self.        ocr_engine = PaddleOCR(
                    use_angle_cls=True,
                    lang='ch'
                )
            except ImportError:
                raise ImportError(
                    "PaddleOCR 未安装。请运行: pip install paddleocr paddlepaddle"
                )
        else:
            try:
                import pytesseract
                from PIL import Image
                self.ocr_engine = pytesseract
            except ImportError:
                raise ImportError(
                    "Tesseract 未安装。请运行: pip install pytesseract && "
                    "brew install tesseract (macOS) 或 apt-get install tesseract-ocr (Linux)"
                )

    def extract_text(self, image_path: str) -> str:
        """
        从图片中提取文字

        Args:
            image_path: 图片本地路径或 URL

        Returns:
            提取的文字内容
        """
        local_path = image_path

        if image_path.startswith(('http://', 'https://')):
            local_path = self._download_image(image_path)

        try:
            if self.use_paddle:
                return self._extract_with_paddle(local_path)
            else:
                return self._extract_with_tesseract(local_path)
        finally:
            if local_path != image_path:
                self._cleanup_file(local_path)

    def _download_image(self, url: str) -> str:
        """下载图片到临时文件"""
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        suffix = Path(url).suffix or '.jpg'
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as f:
            f.write(response.content)
            return f.name

    def _extract_with_paddle(self, image_path: str) -> str:
        """使用 PaddleOCR 提取文字"""
        from PIL import Image

        results = self.ocr_engine.ocr(image_path, cls=True)

        if not results or not results[0]:
            return ""

        texts = []
        for line in results[0]:
            if line and len(line) > 1:
                texts.append(line[1][0])

        return "\n".join(texts)

    def _extract_with_tesseract(self, image_path: str) -> str:
        """使用 Tesseract 提取文字"""
        from PIL import Image

        image = Image.open(image_path)
        text = self.ocr_engine.image_to_string(image, lang='chi_sim+eng')
        return text.strip()

    def _cleanup_file(self, path: str):
        """清理临时文件"""
        try:
            os.unlink(path)
        except Exception:
            pass


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python image_ocr.py <image_path_or_url>")
        sys.exit(1)

    ocr = ImageOCR()
    text = ocr.extract_text(sys.argv[1])
    print("提取的文字内容：")
    print(text)
