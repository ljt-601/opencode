#!/usr/bin/env python3
"""
功能测试脚本
测试各个模块的基本功能
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))


def test_url_detector():
    """测试 URL 检测器"""
    from url_detector import URLDetector, ContentType

    print("=" * 50)
    print("测试 URL 检测器")
    print("=" * 50)

    detector = URLDetector()

    test_cases = [
        ("https://example.com/image.jpg", ContentType.IMAGE),
        ("https://example.com/video.mp4", ContentType.VIDEO),
        ("https://www.douyin.com/video/123", ContentType.SOCIAL_MEDIA),
        ("/Users/test/photo.png", ContentType.IMAGE),
        ("/Users/test/movie.mp4", ContentType.VIDEO),
        ("https://unknown.com/file", ContentType.UNKNOWN),
    ]

    for url, expected_type in test_cases:
        detected_type, _ = detector.detect(url)
        status = "✓" if detected_type == expected_type else "✗"
        print(f"{status} {url:50} -> {detected_type.value}")

    print()


def test_image_ocr():
    """测试图片 OCR（需要已安装依赖）"""
    print("=" * 50)
    print("测试图片 OCR")
    print("=" * 50)

    try:
        from image_ocr import ImageOCR

        ocr = ImageOCR(use_paddle=False)

        print("提示: 请提供一个图片路径进行测试")
        print("示例: python test_all.py /path/to/test_image.jpg")

        if len(sys.argv) > 1 and sys.argv[1].endswith(('.jpg', '.png', '.jpeg')):
            image_path = sys.argv[1]
            print(f"\n正在处理: {image_path}")
            text = ocr.extract_text(image_path)
            print(f"提取的文字:\n{text}")
        else:
            print("跳过 OCR 测试（需要提供图片路径）")

    except ImportError as e:
        print(f"✗ 依赖未安装: {e}")
    except Exception as e:
        print(f"✗ 测试失败: {e}")

    print()


def test_video_processor():
    """测试视频处理器（需要已安装依赖）"""
    print("=" * 50)
    print("测试视频处理器")
    print("=" * 50)

    try:
        from video_processor import VideoProcessor

        processor = VideoProcessor(asr_engine="whisper")

        print("提示: 请提供一个视频路径进行测试")
        print("示例: python test_all.py /path/to/test_video.mp4")

        if len(sys.argv) > 1 and sys.argv[1].endswith(('.mp4', '.mov', '.avi')):
            video_path = sys.argv[1]
            print(f"\n正在处理: {video_path}")
            print("使用方法: auto（优先字幕，失败则 ASR）")
            text = processor.extract_text(video_path, method="auto")
            print(f"提取的文字:\n{text}")
        else:
            print("跳过视频测试（需要提供视频路径）")

    except ImportError as e:
        print(f"✗ 依赖未安装: {e}")
    except Exception as e:
        print(f"✗ 测试失败: {e}")

    print()


def test_content_extractor():
    """测试主提取器"""
    print("=" * 50)
    print("测试主提取器")
    print("=" * 50)

    try:
        from content_extractor import ContentExtractor

        extractor = ContentExtractor()

        print("提示: 提供文件路径或 URL 进行测试")

        if len(sys.argv) > 1:
            test_input = sys.argv[1]
            print(f"\n正在处理: {test_input}")
            result = extractor.extract(test_input)

            if "error" in result:
                print(f"✗ 错误: {result['error']}")
            else:
                print(f"✓ 提取成功")
                print(f"类型: {result['metadata'].get('type')}")
                print(f"文字内容:\n{result['text'][:200]}...")
        else:
            print("跳过测试（需要提供输入路径）")

    except ImportError as e:
        print(f"✗ 依赖未安装: {e}")
    except Exception as e:
        print(f"✗ 测试失败: {e}")

    print()


def main():
    """运行所有测试"""
    print("\n媒体内容提取器 - 功能测试\n")

    test_url_detector()

    if len(sys.argv) > 1:
        test_image_ocr()
        test_video_processor()
        test_content_extractor()
    else:
        print("提示: 运行时提供文件路径可测试完整功能")
        print("示例: python test_all.py /path/to/file.jpg")
        print()


if __name__ == "__main__":
    main()
