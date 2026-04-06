#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from article_formatter import ArticleFormatter

formatter = ArticleFormatter()

# 模拟使用占位符生成内容
content_with_placeholders = """
这是第一段文字。

[[IMAGE_0]]

这是第二段文字。

[[IMAGE_1]]

这是第三段文字。
"""

# 替换占位符
image_urls = [
    "http://example.com/image1.jpg",
    "http://example.com/image2.jpg"
]

for i, url in enumerate(image_urls):
    content_with_placeholders = content_with_placeholders.replace(
        f"[[IMAGE_{i}]]",
        f'<img src="{url}" style="width: 100%;" />'
    )

print("替换后的内容:")
print("=" * 80)
print(content_with_placeholders)
print("=" * 80)

# 格式化
result = formatter.format_article(
    title="测试",
    content=content_with_placeholders,
    author="测试作者",
    template="minimal"
)

print("\n格式化后的内容:")
print("=" * 80)
print(result["formatted_content"])
print("=" * 80)

# 检查 img 标签是否正确
if "< img" in result["formatted_content"]:
    print("\n❌ 失败：仍然有空格 '< img'")
elif "<img" in result["formatted_content"]:
    print("\n✓ 成功：标签正确 '<img'")
else:
    print("\n⚠️ 警告：没有找到 img 标签")
