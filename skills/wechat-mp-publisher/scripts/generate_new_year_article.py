#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
李诞风格文章生成器 - 过年主题
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


def load_config():
    """加载凭证文件"""
    config_path = os.path.expanduser("~/.config/credentials.json")
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_li_dan_style():
    """加载李诞风格配置"""
    style_path = "/Users/bryle/.config/opencode/skills/wechat-mp-publisher/references/li_dan_style.json"
    with open(style_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def generate_li_dan_style_new_year_article(style_config, image_urls=None):
    """
    生成李诞风格的过年文章

    Args:
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

    # 生成图片占位符
    image_placeholders = []
    for i, url in enumerate(image_urls):
        placeholder = f"[[IMAGE_{i}]]"
        image_placeholders.append(placeholder)

    # 生成标题（短促、直接、带点虚无感）
    title = "过年，也就那么回事"

    # 生成正文（按照模仿步骤），800-1000字
    content = f"""
过年这事儿，其实挺没劲的。

真的。

## 抢票：一场集体行为艺术

首先你得抢票。

每年春运，几亿人在同一时间抢同一批票。这本身就是一个巨大的社会学实验。你盯着手机屏幕，刷新，等待，焦虑，然后可能什么都没有。

这时候你就会想，我这是干什么呢？

为了那顿年夜饭？为了那些一年见一次面的亲戚？为了那种传说中的"年味"？

年味这东西，我小时候是信过的。

鞭炮啊，红包啊，新衣服啊，确实挺美好的。但后来我发现，年味不是什么神秘的东西，它就是一群人在同一时间假装很开心。

{image_placeholders[0] if len(image_placeholders) > 0 else ''}

这也没什么不好。

## 春晚：看的人骂，骂的人看

春节联欢晚会，年年有人骂，年年有人看。

骂的人和看的人经常是同一拨。这挺有意思的。

大家好像都默认，过年不看点烂节目，就不算过年。

就像过年不跟亲戚吵几句，就不算过完一样。

{image_placeholders[1] if len(image_placeholders) > 1 else ''}

亲戚问你：有对象了吗？工资多少？什么时候买房？

你心里想：关你什么事。

嘴上却说：还在看，还行，快了。

这就是成年人的过年。

我们都在演，都知道对方在演，但谁也不戳破。

因为戳破了就没法玩了。

## 压岁钱：礼尚往来的交易

压岁钱这个事也挺有意思。

小时候觉得压岁钱是惊喜，长大了发现是交易。你给别人的孩子五百，别人给你的孩子五百。

钱转了一圈，最后还是那些钱，但大家都觉得自己付出了什么。

这叫礼尚往来。

礼尚往来这个词挺好，它把赤裸裸的利益交换包装成了礼仪。但我们都知道，它就是交换。

这也没什么不好。

至少它承认了一个事实：人与人之间的关系，本质上就是交换关系。情感交换，利益交换，或者什么也不交换，就是走个过场。

{image_placeholders[2] if len(image_placeholders) > 2 else ''}

过年，就是最大的过场。

## 真实的瞬间

但我也发现了一些有意思的事情。

虽然过年本身挺无聊的，但在过年的过程中，还是有一些瞬间是真实的。

比如一家人坐在一起吃饭，虽然大部分时间在吵架，但偶尔也会有一刻，大家都安静地吃着，然后你突然觉得，嗯，这顿饭还行。

比如给小孩发红包，看着他们开心的样子，你也会觉得，嗯，这个钱花得还行。

{image_placeholders[3] if len(image_placeholders) > 3 else ''}

比如跟朋友喝酒，虽然大部分时间在抱怨，但偶尔也会有一刻，大家都笑了，然后你突然觉得，嗯，这个朋友还行。

这些瞬间不伟大，不深刻，不改变任何东西。

但它们是真实的。

而这已经很难得了。

在一个充满表演的世界里，真实本身就是一种奢侈。

## 结语

过年这事儿，我也就这么看：它是一个大规模的集体表演，大部分人都在演，包括我。但在表演的过程中，偶尔会有一些真实的瞬间，这些瞬间不值得写进书里，不值得发朋友圈，但它们值得你记住。

如果你问我喜不喜欢过年。

我的答案是：不喜欢。

但我会过。

不是因为有什么意义，而是因为大家都在过。我只想普普通通地活着，过个普普通通的年，吃个普普通通的年夜饭，然后明年继续普普通通地活着。

没什么期待，就是最大的期待。

就这样吧。

"""

    # 替换占位符为真实的图片标签
    for i, url in enumerate(image_urls):
        content = content.replace(f"[[IMAGE_{i}]]",
            f'<img src="{url}" style="width: 100%; max-width: 900px; display: block; margin: 20px 0;" />')

    return title, content.strip()


def generate_and_publish():
    """生成并发布李诞风格的过年文章"""

    # 从配置文件加载凭证
    print("加载配置文件...")
    config = load_config()
    app_id = config["wechat"]["app_id"]
    app_secret = config["wechat"]["app_secret"]
    print("✓ 配置加载成功")

    # 初始化组件
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
    image_count = 4  # 获取4张图片
    image_paths = []
    image_keywords = ["chinese new year fireworks", "family dinner", "red lanterns", "spring festival"]  # 不同的关键词

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
    print(f"\n正在生成李诞风格的过年文章...")
    title, content = generate_li_dan_style_new_year_article(style_config, image_urls)

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

            # 创建极简风格封面（红色调，春节氛围）
            img = Image.new('RGB', (900, 383), color='#c8102e')
            draw = ImageDraw.Draw(img)

            # 添加文字
            title_text = "过年，也就那么回事"
            subtitle_text = "没什么期待，就是最大的期待"

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
            draw.text((x_large, y_large), title_text, fill='#ffffff', font=font_large)
            draw.text((x_small, y_small), subtitle_text, fill='#ffcccc', font=font_small)

            # 保存图片
            cover_image = "/tmp/wechat_mp_images/new_year_default_cover.jpg"
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
        print(f"主题：过年（800-1000字）")
        print(f"你可以在微信公众号后台的草稿箱中查看和编辑。")
        return media_id
    except Exception as e:
        print(f"\n❌ 创建草稿失败: {str(e)}")
        return None


if __name__ == "__main__":
    print("=" * 60)
    print("李诞风格文章生成器 - 过年主题")
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
