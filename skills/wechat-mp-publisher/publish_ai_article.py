#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI热点文章生成并发布到微信公众号草稿箱
"""

import sys
import os

# 添加 scripts 目录到 Python 路径
script_dir = os.path.join(os.path.dirname(__file__), 'scripts')
sys.path.insert(0, script_dir)

from wechat_auth import WeChatAuth
from wechat_draft import WeChatDraft
from article_formatter import ArticleFormatter
from image_fetcher import ImageFetcher
import json

# 从统一凭证文件加载
with open(os.path.expanduser("~/.config/credentials.json"), 'r') as f:
    config = json.load(f)

app_id = config['wechat']['app_id']
app_secret = config['wechat']['app_secret']

print("=" * 60)
print("📝 开始生成AI热点文章并发布到微信公众号")
print("=" * 60)

# 步骤1: 认证
print("\n[1/5] 正在进行微信认证...")
auth = WeChatAuth(app_id, app_secret)
token = auth.get_access_token()
print(f"✓ 认证成功！Token: {token[:20]}...")

# 步骤2: 生成文章内容
print("\n[2/5] 正在生成文章内容...")

article_title = "2026年2月AI智能体大战：Claude 4.6 vs GPT-5.3 vs Gemini 3"

article_content = """
2026年2月，AI行业迎来了史无前例的"模型大战"——七大主流AI模型在同一个月内密集发布，标志着AI从"聊天机器人"时代正式迈入"智能体"时代。

## 史上最激烈的AI发布月

今年2月，OpenAI、Anthropic、Google DeepMind、智谱AI等巨头几乎同时发布了各自的最新模型：

- **Claude Opus 4.6**（Anthropic）：推理性最强，首度引入100万token上下文窗口
- **GPT-5.3-Codex**（OpenAI）：编程能力特化，具备自我改善功能
- **Gemini 3系列**（Google）：智能体操作优化，Deep Think模式登场
- **GLM-5**（智谱AI）：745B参数超大规模模型，中国AI力量崛起

这场"你追我赶"的发布节奏，让人联想到当年浏览器大战的激烈程度。

## 从对话到行动：智能体时代的黎明

与之前的"聊天机器人"不同，这一代模型的核心突破在于**自主执行能力**：

### Agent Teams功能
Claude 4.6引入的革命性功能，让多个AI智能体并行协作。例如在编程任务中，代码编写、测试、文档编写可由不同"角色"的AI同时进行，互相协调。

### 100万token超长上下文
Claude Opus 4.6首次在Opus系列中实现100万token上下文窗口（测试版）。这意味着AI可以一次性处理约75万汉字（相当于7-8本新书的体量），并在海量信息中精准定位细节。

在长文检索基准测试MRCR v2中，Opus 4.6达到76%的准确率，而前代Sonnet 4.5仅为18.5%。

### 编程能力质变
GPT-5.3-Codex专注于代码生成与优化，能够自我审查和调试错误。在Tom's Guide的评测中，Claude 4.6在9项测试中赢得6项，尤其在复杂系统设计和推理任务上表现突出。

## 中国AI的强势崛起

值得关注的是，本次发布潮中中国模型占据三席：智谱GLM-5、通义千问Qwen 3.5、深度求索DeepSeek v4。

**GLM-5**尤其引人注目：745B参数（44B激活）的MoE架构，完全基于华为昇腾芯片训练，不依赖美国半导体。在性能测试中，它已经逼近Claude Opus 4.5的水平。

这标志着中美AI竞争已经从"应用层"深入到"模型层"。

## 专业特化型AI的崛起趋势

行业观察发现，2026年的趋势并非追求通用AGI，而是**专业特化型AI**的实用化：

- **OpenScholar**：学术论文特化
- **BrainIAC**：医学影像诊断
- **Codex系列**：编程开发

这种"术业有专攻"的路线，更符合企业实际需求，也更容易实现商业化落地。

## 竞争格局生变

根据多家科技媒体的横向评测，各模型优势领域逐渐清晰：

| 模型 | 最强领域 | 典型应用场景 |
|------|----------|--------------|
| Claude 4.6 | 深度推理、长文分析 | 研究报告、合同审查、代码库分析 |
| GPT-5.3 | 编程、事实核查 | 软件开发、知识问答 |
| Gemini 3 | 多模态、智能体控制 | 视频创作、自动化工作流 |
| GLM-5 | 中文理解、性价比 | 国内企业应用、成本敏感场景 |

## 未来展望

AI分析师认为，2026年将是"AI智能体元年"。我们正在见证：

1. **从对话到行动**：AI不再只是"说话"，而是"做事"
2. **从通用到专精**：专业领域模型成为主流
3. **从实验室到生产线**：AI深度集成到企业业务系统
4. **从中美竞争到全球合作**：开源与闭源模型并存发展

这场战争没有终点，但最大的赢家可能是每一位用户——因为我们正在见证技术改变世界的速度，比以往任何时候都快。

---

**结语**：AI的进化不是科幻电影，而是正在发生的现实。2026年2月这场"智能体大战"，或许会在未来被标记为AI发展史上的关键转折点。

*本文基于2026年2月公开资料整理，数据来源包括各公司官方发布及第三方评测报告。*
"""

article_author = "AI观察员"

print(f"✓ 文章标题：{article_title}")
print(f"✓ 字数：约{len(article_content)}字")

# 步骤3: 获取图片
print("\n[3/5] 正在获取封面图和插图...")
fetcher = ImageFetcher()

# 获取封面图
print("  - 获取封面图（AI主题）...")
cover_images = fetcher.search_and_download("artificial intelligence technology", count=1, source="unsplash")
if cover_images:
    cover_path = cover_images[0]
    print(f"  ✓ 封面图已下载：{cover_path}")
else:
    print("  ✗ 封面图下载失败，使用备用方案")
    cover_path = None

# 获取插图
print("  - 获取插图（机器人主题）...")
illustration_images = fetcher.search_and_download("robot automation future", count=2, source="unsplash")
if illustration_images:
    illu1_path = illustration_images[0]
    print(f"  ✓ 插图1已下载：{illu1_path}")
    if len(illustration_images) > 1:
        illu2_path = illustration_images[1]
        print(f"  ✓ 插图2已下载：{illu2_path}")
    else:
        illu2_path = None
else:
    print("  ✗ 插图下载失败")
    illu1_path = None
    illu2_path = None

# 步骤4: 格式化文章
print("\n[4/5] 正在格式化文章...")
formatter = ArticleFormatter()

# 在文章中插入图片
formatted_content_text = article_content

# 在开头插入封面图展示（如果需要）
# 插入插图到内容中
if illu1_path:
    # 这里我们暂时不上传插图，因为需要先上传才能得到media_id
    pass

result = formatter.format_article(
    title=article_title,
    content=formatted_content_text,
    author=article_author,
    template="modern"
)

formatted_html = result["formatted_content"]
digest = result["digest"]

print(f"✓ 文章已格式化（模板：modern）")
print(f"✓ 摘要：{digest[:50]}...")

# 步骤5: 上传素材并创建草稿
print("\n[5/5] 正在上传素材并创建草稿...")
draft = WeChatDraft(auth)

# 上传封面图
if cover_path:
    print("  - 上传封面图...")
    try:
        thumb_result = draft.upload_image(cover_path, image_type="thumb")
        thumb_media_id = thumb_result["media_id"]
        print(f"  ✓ 封面图已上传，media_id: {thumb_media_id}")
    except Exception as e:
        print(f"  ✗ 封面图上传失败: {str(e)}")
        thumb_media_id = None
else:
    thumb_media_id = None
    print("  - 跳过封面图上传")

# 构建文章数据
article_data = {
    "title": article_title,
    "author": article_author,
    "digest": digest,
    "content": formatted_html,
    "thumb_media_id": thumb_media_id,
    "need_open_comment": True,
    "only_fans_can_comment": False
}

# 创建草稿
print("  - 创建草稿...")
try:
    media_id = draft.create_draft(articles=[article_data])
    print(f"\n{'=' * 60}")
    print(f"🎉 成功！文章已上传到微信公众号草稿箱")
    print(f"{'=' * 60}")
    print(f"\n📌 草稿信息：")
    print(f"  - Media ID: {media_id}")
    print(f"  - 标题: {article_title}")
    print(f"  - 作者: {article_author}")
    print(f"\n💡 下一步操作：")
    print(f"  1. 登录微信公众平台：https://mp.weixin.qq.com")
    print(f"  2. 进入「草稿箱」")
    print(f"  3. 找到文章《{article_title}》")
    print(f"  4. 预览、编辑或发布")
    print(f"\n{'=' * 60}\n")
except Exception as e:
    print(f"\n✗ 创建草稿失败: {str(e)}")
    import traceback
    traceback.print_exc()
