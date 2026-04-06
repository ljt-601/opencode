#!/usr/bin/env python3
"""测试生成的 HTML 内容"""

# 模拟生成文章内容
image_urls = [
    "http://mmbiz.qpic.cn/test1.png",
    "http://mmbiz.qpic.cn/test2.png",
    "http://mmbiz.qpic.cn/test3.png"
]

# 生成内容（使用新的格式）
content = f"""
测试内容

{f'<img src="{image_urls[0]}" style="width: 100%; max-width: 900px; display: block; margin: 20px auto;" />' if len(image_urls) > 0 else ''}

更多内容

{f'<img src="{image_urls[1]}" style="width: 100%; max-width: 900px; display: block; margin: 20px auto;" />' if len(image_urls) > 1 else ''}

继续内容

{f'<img src="{image_urls[2]}" style="width: 100%; max-width: 900px; display: block; margin: 20px auto;" />' if len(image_urls) > 2 else ''}

结束
"""

print("生成的 HTML 内容:")
print("=" * 80)
print(content)
print("=" * 80)

# 检查是否有问题
if "< img" in content:
    print("\n❌ 发现问题：标签中有空格 '< img'")
elif "<img" in content:
    print("\n✓ 标签格式正确：'<img'")

# 导出为文件查看
with open("/tmp/test_html_content.txt", "w", encoding="utf-8") as f:
    f.write(content)
print("\n内容已保存到: /tmp/test_html_content.txt")
