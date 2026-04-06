#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成 OpenCode 介绍文章并发布到公众号草稿箱
"""

import sys
import os

# 添加 scripts 目录到路径
sys.path.insert(0, os.path.dirname(__file__))

from wechat_auth import WeChatAuth
from wechat_draft import WeChatDraft
from article_formatter import ArticleFormatter
from enhanced_image_fetcher import EnhancedImageFetcher


def generate_opencode_article():
    """生成并发布 OpenCode 介绍文章"""

    # 从统一凭证文件加载
    import json as _json
    _creds_path = os.path.expanduser("~/.config/credentials.json")
    with open(_creds_path, 'r') as _f:
        _creds = _json.load(_f)
    app_id = _creds["wechat"]["app_id"]
    app_secret = _creds["wechat"]["app_secret"]

    auth = WeChatAuth(app_id, app_secret)
    draft = WeChatDraft(auth)
    formatter = ArticleFormatter()
    fetcher = EnhancedImageFetcher()

    # 生成文章内容
    title = "OpenCode：AI 编程伙伴"

    content = """
OpenCode 是一个革命性的 AI 辅助编程工具，它将 Claude 的强大能力无缝集成到你的开发工作流中。

## 什么是 OpenCode？

OpenCode 是一个开源的开发环境扩展，它允许开发者直接在代码编辑器中与 Claude AI 进行交互。不同于传统的聊天式 AI 工具，OpenCode 理解代码的上下文，能够提供更精准、更有针对性的建议。

## 核心特性

### 智能代码补全
OpenCode 能够理解你的代码意图，提供智能的代码补全建议。它不仅仅是简单的自动补全，而是基于对整个项目结构的理解，给出符合最佳实践的代码片段。

### 实时代码审查
在编写代码的过程中，OpenCode 会实时检查潜在的问题，包括性能优化建议、安全漏洞检测、代码风格统一等。这就像身边有一位经验丰富的代码审查专家。

### 上下文感知的问答
不同于传统的 AI 聊天机器人，OpenCode 完全理解你的代码库。当你问"这个函数是做什么的？"时，它能够准确地解释代码的功能，并给出改进建议。

### 自动化测试生成
编写测试往往是开发中最耗时的部分之一。OpenCode 可以根据你的代码自动生成单元测试，大大提高测试覆盖率。

## 工作流程

使用 OpenCode 的工作流程非常简单：

1. **编写代码** - 在你熟悉的编辑器中编写代码
2. **AI 辅助** - OpenCode 在后台提供实时建议
3. **交互改进** - 通过自然语言与 AI 对话，优化代码
4. **持续学习** - OpenCode 从你的编码风格中学习，提供个性化的建议

## 适用场景

OpenCode 特别适合以下场景：

- **学习新技术** - 快速理解陌生的代码库
- **代码重构** - 智能识别可优化的代码片段
- **调试辅助** - 快速定位和修复 bug
- **文档生成** - 自动生成代码文档和注释
- **最佳实践** - 确保代码符合行业标准

## 安全与隐私

OpenCode 非常重视用户隐私：

- 所有代码分析都在本地进行
- 可选择性地发送代码片段到 AI
- 支持私有代码库模式
- 企业级的数据加密保护

## 开始使用

安装 OpenCode 非常简单，只需要几分钟即可完成配置。访问官方网站获取详细安装指南。

## 未来展望

OpenCode 团队正在持续开发新功能，包括：

- 多语言支持扩展
- 团队协作功能
- 自定义 AI 模型训练
- 与更多开发工具的集成

OpenCode 不仅仅是一个工具，它是编程方式的革新。让 AI 成为你的编程伙伴，释放创造力，专注于真正重要的工作。

---

**OpenCode - 重新定义编程体验**
"""

    # 格式化文章
    print("正在格式化文章...")
    result = formatter.format_article(
        title=title,
        content=content,
        author="OpenCode",
        template="modern"
    )

    formatted_content = result["formatted_content"]
    # 不设置摘要，让微信自动生成
    digest = ""

    print(f"摘要: {digest or '(自动生成)'}")

    # 获取封面图
    print("\n正在获取封面图...")
    cover_image = None

    # 使用增强版图片获取器，自动尝试多个免费源
    try:
        print("自动搜索高质量封面图...")
        image_paths = fetcher.search_and_download("technology computer", count=1, prefer_source="auto")
        if image_paths:
            cover_image = image_paths[0]
            print(f"✓ 封面图已下载: {os.path.basename(cover_image)}")
    except Exception as e:
        print(f"✗ 自动获取图片失败: {str(e)}")

    # 如果自动获取失败，创建默认封面图
    if not cover_image:
        print("\n正在创建默认封面图...")

        # 创建一个简单的纯色封面图
        try:
            from PIL import Image, ImageDraw, ImageFont

            # 创建图片
            img = Image.new('RGB', (900, 383), color='#667eea')
            draw = ImageDraw.Draw(img)

            # 添加文字
            title_text = "OpenCode"
            subtitle_text = "AI-Powered Development"

            try:
                # 尝试使用系统字体
                font_large = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 60)
                font_small = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 30)
            except:
                # 如果找不到字体，使用默认字体
                font_large = ImageFont.load_default()
                font_small = ImageFont.load_default()

            # 计算文字位置（居中）
            bbox_large = draw.textbbox((0, 0), title_text, font=font_large)
            bbox_small = draw.textbbox((0, 0), subtitle_text, font=font_small)

            x_large = (900 - bbox_large[2]) / 2
            y_large = 150
            x_small = (900 - bbox_small[2]) / 2
            y_small = 220

            # 绘制文字
            draw.text((x_large, y_large), title_text, fill='white', font=font_large)
            draw.text((x_small, y_small), subtitle_text, fill='white', font=font_small)

            # 保存图片
            cover_image = "/tmp/wechat_mp_images/default_cover.jpg"
            os.makedirs(os.path.dirname(cover_image), exist_ok=True)
            img.save(cover_image)
            print(f"✓ 默认封面图已创建: {os.path.basename(cover_image)}")

        except ImportError:
            print("无法创建默认封面图（需要安装 PIL/Pillow）")
            return None
        except Exception as e:
            print(f"创建默认封面图失败: {str(e)}")
            return None

    # 上传封面图
    print("\n正在上传封面图...")
    try:
        thumb_media_id = draft.upload_image(cover_image, image_type="thumb")
        print(f"封面图上传成功, media_id: {thumb_media_id}")
    except Exception as e:
        print(f"上传封面图失败: {str(e)}")
        return None

    # 创建草稿
    print("\n正在创建草稿...")
    article = {
        "title": title,
        "content": formatted_content,
        "thumb_media_id": thumb_media_id,
        "need_open_comment": True,
        "only_fans_can_comment": False
    }

    # 只有当 digest 不为空时才添加
    if digest:
        article["digest"] = digest

    try:
        media_id = draft.create_draft(articles=[article])
        print(f"\n✅ 草稿创建成功!")
        print(f"草稿 media_id: {media_id}")
        print("\n你可以在微信公众号后台的草稿箱中查看和编辑这篇文章。")
        return media_id
    except Exception as e:
        print(f"\n❌ 创建草稿失败: {str(e)}")
        return None


if __name__ == "__main__":
    print("=" * 60)
    print("OpenCode 介绍文章生成器")
    print("=" * 60)
    print()

    media_id = generate_opencode_article()

    if media_id:
        print("\n" + "=" * 60)
        print("任务完成！")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("任务失败，请检查错误信息")
        print("=" * 60)
        sys.exit(1)
