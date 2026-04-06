#!/usr/bin/env python3
"""
媒体内容提取器 - 快速开始示例
"""

import sys
import os

# 添加 scripts 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts'))


def example_image_ocr():
    """示例 1：图片 OCR"""
    print("=" * 60)
    print("示例 1：从图片中提取文字")
    print("=" * 60)
    print()
    print("代码：")
    print("-----")
    print("""
from scripts.content_extractor import extract_text

# 本地图片
text = extract_text("/path/to/image.jpg")
print(text)

# 图片 URL
text = extract_text("https://example.com/image.png")
print(text)
    """)
    print()


def example_video_asr():
    """示例 2：视频 ASR"""
    print("=" * 60)
    print("示例 2：从视频中提取文字（语音识别）")
    print("=" * 60)
    print()
    print("代码：")
    print("-----")
    print("""
from scripts.content_extractor import extract_text

# 自动选择方法（优先字幕，失败则 ASR）
text = extract_text("/path/to/video.mp4")

# 强制使用 ASR
text = extract_text("/path/to/video.mp4", method="asr")
print(text)

# 视频URL
text = extract_text("https://example.com/video.mp4")
print(text)
    """)
    print()


def example_social_media():
    """示例 3：社交媒体链接"""
    print("=" * 60)
    print("示例 3：从社交媒体提取内容")
    print("=" * 60)
    print()
    print("支持的平台：抖音、小红书、B站、YouTube、微博")
    print()
    print("代码：")
    print("-----")
    print("""
from scripts.content_extractor import extract_text

# 抖音视频
text = extract_text("https://www.douyin.com/video/12345")
print(text)

# B站视频
text = extract_text("https://www.bilibili.com/video/BV1xx")
print(text)

# YouTube 视频
text = extract_text("https://www.youtube.com/watch?v=xxxxx")
print(text)
    """)
    print()


def example_advanced():
    """示例 4：高级用法"""
    print("=" * 60)
    print("示例 4：高级用法")
    print("=" * 60)
    print()
    print("代码：")
    print("-----")
    print("""
from scripts.content_extractor import ContentExtractor

# 创建提取器（自定义参数）
extractor = ContentExtractor(
    asr_engine="faster-whisper",  # 使用更快的 ASR
    use_paddle=True               # 使用 PaddleOCR
)

# 提取内容并获取元数据
result = extractor.extract(
    "https://www.bilibili.com/video/BV1xx",
    method="auto"
)

# 输出结果
print(f"类型: {result['metadata']['type']}")
print(f"平台: {result['metadata'].get('platform', 'N/A')}")
print(f"文字: {result['text']}")
    """)
    print()


def example_batch():
    """示例 5：批量处理"""
    print("=" * 60)
    print("示例 5：批量处理多个链接")
    print("=" * 60)
    print()
    print("代码：")
    print("-----")
    print("""
from scripts.content_extractor import extract_text

urls = [
    "https://example.com/image1.jpg",
    "https://example.com/video1.mp4",
    "https://www.douyin.com/video/123",
    "https://www.bilibili.com/video/BV1xx"
]

for i, url in enumerate(urls, 1):
    print(f"\\n处理 {i}/{len(urls)}: {url}")
    text = extract_text(url)
    print(f"提取的文字（前 100 字）：")
    print(text[:100] + "...")
    print("-" * 40)
    """)
    print()


def main():
    """运行所有示例"""
    print("\n媒体内容提取器 - 使用示例\n")

    example_image_ocr()
    example_video_asr()
    example_social_media()
    example_advanced()
    example_batch()

    print("=" * 60)
    print("安装依赖")
    print("=" * 60)
    print()
    print("图片 OCR（推荐 PaddleOCR）：")
    print("  pip install paddleocr paddlepaddle")
    print()
    print("视频 ASR（推荐 Whisper）：")
    print("  pip install openai-whisper")
    print()
    print("社交媒体下载：")
    print("  pip install yt-dlp")
    print()
    print("视频处理（需要 ffmpeg）：")
    print("  brew install ffmpeg  # macOS")
    print("  sudo apt install ffmpeg  # Linux")
    print()
    print("=" * 60)
    print("快速测试")
    print("=" * 60)
    print()
    print("运行以下命令测试基本功能：")
    print("  cd ~/.config/opencode/skills/media-content-extractor/scripts")
    print("  python3 url_detector.py  # 测试 URL 检测")
    print("  python3 test_all.py /path/to/your/file  # 测试完整功能")
    print()


if __name__ == "__main__":
    main()
