#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
李诞风格文章生成器
基于虚无主义底色的温和解构主义
"""

import sys
import os
import json

# 添加 scripts 目录到路径
sys.path.insert(0, os.path.dirname(__file__))

from wechat_auth import WeChatAuth
from wechat_draft import WeChatDraft
from article_formatter import ArticleFormatter
from enhanced_image_fetcher import EnhancedImageFetcher


def load_li_dan_style():
    """加载李诞风格配置"""
    style_path = "/Users/bryle/.config/opencode/skills/wechat-mp-publisher/references/li_dan_style.json"
    with open(style_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def generate_li_dan_style_article(topic, style_config, image_urls=None):
    """
    生成李诞风格的文章（带图片）

    Args:
        topic: 文章主题
        style_config: 李诞风格配置
        image_urls: 图片 URL 列表

    Returns:
        文章内容（标题和正文）
    """

    # 李诞风格的核心要素
    必备元素 = style_config["综合模仿指南"]["风格核心要素"]
    模仿步骤 = style_config["综合模仿指南"]["模仿步骤"]

    # 确保有图片 URL 列表
    if image_urls is None:
        image_urls = []

    # 生成图片占位符，避免被 format_text 转义
    image_placeholders = []
    for i, url in enumerate(image_urls):
        placeholder = f"[[IMAGE_{i}]]"
        image_placeholders.append(placeholder)

    # 生成标题（短促、直接、带点虚无感）
    titles = [
        f"{topic}这回事",
        f"关于{topic}的一些实话",
        f"{topic}，也就那么回事",
        f"我为什么对{topic}没什么期待",
    ]
    title = titles[0]  # 选择第一个标题

    # 生成正文（按照模仿步骤），使用占位符
    content = f"""
{topic}这事儿，其实挺没劲的。

真的。

我师父说，人类的大部分痛苦都来自于对意义的过度追寻。{topic}也不例外。我们总觉得它应该有什么深刻的意义，应该改变点什么，应该让我们成为更好的人。

但说实话，它就是一回事。

{image_placeholders[0] if len(image_placeholders) > 0 else ''}

就像我最近在用这个叫 OpenCode 的工具写代码。它帮你写代码，优化代码，甚至帮你写测试。听起来挺美好的对吧？

但我问自己一个问题：这有什么意义呢？

代码写得更快了，然后呢？bug 更少了，然后呢？工作效率提高了，然后呢？

然后你就能更早地下班，去面对家里更大的虚无。

这没什么不好。真的。

OpenCode 这个东西，我就这么看它：它是个工具，挺专业的工具。它不跟你谈梦想，不跟你谈改变世界，它就是帮你干活。

这种态度我挺欣赏的。

现在的世界，谈梦想的人太多了，谈工具的人太少了。谈情怀的人太多了，谈专业的人太少了。

{image_placeholders[1] if len(image_placeholders) > 1 else ''}

OpenCode 就是很直白地告诉你：我能帮你写代码，能帮你省时间，能让你少掉几根头发。至于你用省下来的时间干什么，那是你的事。

这就是专业。

这就是我对 OpenCode 的全部评价。

它不是什么革命性的产品，不会让你的生活发生翻天覆地的变化。它就是有点用，挺好用的，然后就没别的了。

但在这个充满宏大叙事的世界里，一个工具老老实实承认自己就是个工具，这本身就是一种美德。

所以，如果你问我推不推荐 OpenCode。

我的答案是：推荐。

但别抱太大期待。它就是个工具，帮你干活用的。用了它，你不会变成编程大师，不会改变世界，也不会突然找到人生的意义。

你只会写代码写得快一点。

然后呢？

然后你就得面对下一个问题了。

{image_placeholders[2] if len(image_placeholders) > 2 else ''}

人生就是这样，问题套着问题。OpenCode 帮你解决了一个，仅此而已。

但也够了。

毕竟，能解决一个问题，就已经比大部分只能制造问题的东西强了。

就这样吧。

说了这么多，其实就一句话：OpenCode 挺好用的，用了就知道。别想太多，想太多没用。

反正最后我们都会忘记今天写过什么代码，解决过什么 bug。

但这不妨碍我们现在先把这活干完。

而且，既然有工具能让这活干得轻松点，为什么不用呢？

这就是我的人生哲学：在无意义的人生中，找点轻松的方式熬过去。

OpenCode，就是这么个轻松的方式。

用用看吧。

反正也没别的事可干。
"""

    # 替换占位符为真实的图片标签
    for i, url in enumerate(image_urls):
        content = content.replace(f"[[IMAGE_{i}]]", 
            f'<img src="{url}" style="width: 100%; max-width: 900px; display: block; margin: 20px 0;" />')

    return title, content.strip()


def generate_and_publish():
    """生成并发布李诞风格的 OpenCode 介绍文章"""

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

    # 加载李诞风格
    print("加载李诞风格配置...")
    style_config = load_li_dan_style()
    print("✓ 风格配置加载成功")

    # 获取多张配图
    print("\n正在获取文章配图...")
    image_count = 3  # 获取3张图片
    image_paths = []
    image_keywords = ["minimalist desk", "computer work", "coding screen"]  # 不同的关键词

    for i, keyword in enumerate(image_keywords):
        try:
            print(f"  获取第 {i+1} 张图片（关键词: {keyword}）...")
            paths = fetcher.search_and_download(keyword, count=1, prefer_source="auto")
            if paths:
                image_paths.append(paths[0])
                print(f"    ✓ 成功: {os.path.basename(paths[0])}")
        except Exception as e:
            print(f"    ✗ 失败: {str(e)}")

    print(f"\n✓ 共获取 {len(image_paths)} 张图片")

    # 上传图片到微信并获取 URL
    print("\n正在上传图片到微信...")
    image_urls = []

    for i, image_path in enumerate(image_paths):
        try:
            print(f"  上传第 {i+1} 张图片...")
            result = draft.upload_image(image_path, image_type="image")  # 使用 image 类型
            if result and "url" in result:
                image_urls.append(result["url"])
                print(f"    ✓ 成功获取 URL")
            elif result and "media_id" in result:
                # 如果没有 URL，尝试构造微信 CDN URL
                media_id = result["media_id"]
                # 微信图片 CDN 格式（这是一个备用方案）
                image_urls.append(f"https://mmbiz.qpic.cn/mmbiz_jpg/0/{media_id}/0?wx_fmt=jpeg")
                print(f"    ✓ 使用 media_id: {media_id[:20]}...")
            else:
                print(f"    ✗ 上传失败：未返回 URL")
        except Exception as e:
            print(f"    ✗ 失败: {str(e)}")

    print(f"\n✓ 成功上传 {len(image_urls)} 张图片")

    # 生成文章
    topic = "OpenCode"
    print(f"\n正在生成李诞风格的 {topic} 文章...")
    title, content = generate_li_dan_style_article(topic, style_config, image_urls)

    print(f"标题: {title}")
    print(f"字数: {len(content)} 字\n")

    # 格式化文章（使用极简风格，更符合李诞的调性）
    print("正在格式化文章...")
    result = formatter.format_article(
        title=title,
        content=content,
        author="李诞风格",
        template="minimal"  # 使用极简模板
    )

    formatted_content = result["formatted_content"]

    # 使用第一张配图作为封面图
    cover_image = None
    if image_paths:
        cover_image = image_paths[0]
        print(f"\n✓ 使用第一张配图作为封面: {os.path.basename(cover_image)}")
    else:
        # 如果没有配图，创建默认封面图
        print("\n正在创建默认封面图...")
        try:
            from PIL import Image, ImageDraw, ImageFont

            # 创建极简风格封面（灰色调）
            img = Image.new('RGB', (900, 383), color='#2c2c2c')
            draw = ImageDraw.Draw(img)

            # 添加文字
            title_text = "OpenCode 这回事"
            subtitle_text = "也就那么回事"

            try:
                font_large = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 50)
                font_small = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 25)
            except:
                font_large = ImageFont.load_default()
                font_small = ImageFont.load_default()

            # 计算文字位置（居中）
            bbox_large = draw.textbbox((0, 0), title_text, font=font_large)
            bbox_small = draw.textbbox((0, 0), subtitle_text, font=font_small)

            x_large = (900 - bbox_large[2]) / 2
            y_large = 150
            x_small = (900 - bbox_small[2]) / 2
            y_small = 210

            # 绘制白色文字
            draw.text((x_large, y_large), title_text, fill='#cccccc', font=font_large)
            draw.text((x_small, y_small), subtitle_text, fill='#999999', font=font_small)

            # 保存图片
            cover_image = "/tmp/wechat_mp_images/li_dan_default_cover.jpg"
            os.makedirs(os.path.dirname(cover_image), exist_ok=True)
            img.save(cover_image)
            print(f"✓ 默认封面图已创建: {os.path.basename(cover_image)}")

        except Exception as e:
            print(f"创建默认封面图失败: {str(e)}")
            return None

    # 上传封面图
    print("\n正在上传封面图...")
    try:
        thumb_result = draft.upload_image(cover_image, image_type="thumb")
        if thumb_result and "media_id" in thumb_result:
            thumb_media_id = thumb_result["media_id"]
            print(f"✓ 封面图上传成功")
        else:
            print(f"✗ 上传封面图失败：未返回 media_id")
            return None
    except Exception as e:
        print(f"✗ 上传封面图失败: {str(e)}")
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

    try:
        media_id = draft.create_draft(articles=[article])
        print(f"\n✅ 草稿创建成功!")
        print(f"草稿 media_id: {media_id}")
        print(f"\n这篇文章采用李诞风格：虚无主义底色 + 温和解构 + 职业通透感")
        print(f"你可以在微信公众号后台的草稿箱中查看和编辑。")
        return media_id
    except Exception as e:
        print(f"\n❌ 创建草稿失败: {str(e)}")
        return None


if __name__ == "__main__":
    print("=" * 60)
    print("李诞风格文章生成器")
    print("风格：虚无主义底色 + 温和解构主义")
    print("=" * 60)
    print()

    media_id = generate_and_publish()

    if media_id:
        print("\n" + "=" * 60)
        print("任务完成！")
        print("就这样吧。")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("任务失败")
        print("也没什么大不了的。")
        print("=" * 60)
        sys.exit(1)
