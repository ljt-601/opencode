---
name: wechat-mp-publisher
description: 微信公众号内容生成与发布工具。支持 AI 自动生成文章内容、格式化用户提供的现有内容，并将单图文消息上传到微信公众号草稿箱。支持 AI 热点快报：自动从 HackerNews/Reddit/Twitter 搜集 48h 内 AI 热点，精选 Top 10，科技杂志风排版后推送草稿箱。触发关键词："生成公众号文章"、"发布到公众号"、"上传到草稿箱"、"写公众号"、"AI 快报"、"热点快报"等。
---

# 微信公众号发布器

## 概述

本 skill 提供完整的微信公众号内容生成与发布工作流，从内容创作（AI 生成或用户提供）到排版美化，再到上传到公众号草稿箱的全流程支持。

### 主要能力

1. **内容生成**：AI 根据主题自动撰写文章
2. **内容格式化**：将用户提供的文本转换为精美的微信公众号格式
3. **图片获取**：从免费图库（Unsplash、Pexels、Pixabay）获取高质量图片
4. **排版美化**：提供 4 种专业排版模板（经典、现代、极简、商务）
5. **草稿箱发布**：直接上传到微信公众号草稿箱

### 工作流程

```
用户请求 → 获取凭证 → 准备内容 → 获取图片 → 格式化排版 → 上传草稿箱 → 完成
```

## 使用前准备

### 第一步：获取微信公众号凭证

在使用本 skill 前，需要提供微信公众号的 `AppId` 和 `AppSecret`：

**获取方式**：
1. 登录微信公众平台 https://mp.weixin.qq.com
2. 进入"开发" → "基本配置"
3. 查看或生成 `AppId` 和 `AppSecret`

**凭证管理**：
- 凭证在当前会话内缓存，无需重复输入
- Token 自动刷新，有效期 2 小时
- 安全提醒：不要在公共场合暴露 `AppSecret`

## 工作流程决策树

### 场景 1：AI 生成并发布

**用户请求示例**：
- "生成一篇关于 AI 的文章并发布到公众号草稿箱"
- "帮我写一篇产品介绍文章，上传到草稿箱"

**执行流程**：
1. 询问文章主题和关键信息
2. AI 生成文章内容（标题、正文）
3. 询问排版风格选择（classic/modern/minimal/business）
4. 根据主题自动获取封面图和配图
5. 格式化文章内容
6. 上传图片素材到微信
7. 创建草稿箱
8. 返回草稿 media_id

### 场景 2：格式化现有内容并发布

**用户请求示例**：
- "把这篇文章上传到公众号草稿箱"
- "格式化并发布这篇内容"

**执行流程**：
1. 接收用户提供的文章内容（文本或文件）
2. 确认或询问标题、作者
3. 询问排版风格选择
4. 询问封面图来源（自动获取或用户提供）
5. 格式化文章内容
6. 上传图片素材到微信
7. 创建草稿箱
8. 返回草稿 media_id

### 场景 3：仅格式化内容

**用户请求示例**：
- "帮我排版这篇公众号文章"
- "生成这篇文章的微信公众号格式"

**执行流程**：
1. 接收用户内容
2. 询问排版风格
3. 生成格式化的 HTML 内容
4. 返回预览

### 场景 4：仅获取图片

**用户请求示例**：
- "帮我找一些关于科技的图片"
- "获取商业主题的封面图"

**执行流程**：
1. 询问图片主题
2. 选择图片来源（Unsplash/Pexels/Pixabay）
3. 下载图片到本地
4. 返回图片路径

### 场景 5：AI 热点快报（自动搜热 + 排版 + 推送）⭐

**触发关键词**："写公众号"、"AI 快报"、"热点快报"、"公众号资讯"、"AI 热点"

**用户请求示例**：
- "帮我写公众号"
- "发一篇 AI 快报到草稿箱"
- "今天的 AI 热点"

**完整工作流**：

#### 第一步：多平台搜热（并行）

使用 `opencli` 从三个平台并行抓取 AI 相关热点：

```bash
# HackerNews — 高票 AI 帖子
opencli hackernews top --limit 30 -f json

# Reddit — r/artificial + r/MachineLearning 热帖
opencli reddit hot -r artificial --limit 20 -f json
opencli reddit hot -r MachineLearning --limit 20 -f json

# Twitter/X — AI 领域热门推文
opencli twitter search --query "AI OR LLM OR GPT OR Claude OR Gemini" -f json
```

**筛选规则**：
- 时间窗口：48 小时内（根据帖子时间戳过滤）
- 关键词过滤：AI、LLM、GPT、Claude、Gemini、模型、大模型、智能体、Agent 等
- 去重：同一事件跨平台只保留热度最高的来源

#### 第二步：AI 精选 Top 10

从抓取结果中：
1. 去重合并（同一事件取热度最高的源）
2. AI 判断新闻价值，精选 10 条
3. 为每条新闻撰写：
   - **标题**（简洁有力，≤20 字）
   - **摘要**（2-3 句话概述核心要点）
   - **来源标签**（HackerNews / Reddit / Twitter）
   - **原文链接**

#### 第三步：提取配图

对精选的 10 条新闻：
1. 访问原文链接，提取文章配图（优先选首图或信息图）
2. 图片要求：
   - 宽度 ≥ 600px
   - 格式 JPG/PNG
   - 大小 ≤ 2MB
3. 无合适配图则跳过（不是每条都必须有图）
4. 将图片 URL 记录到 news_items 的 `image_url` 字段

#### 第四步：科技杂志排版

使用 `tech_magazine` 模板自动排版：

```python
from scripts.article_formatter import ArticleFormatter

formatter = ArticleFormatter()
result = formatter.format_news_brief(
    news_items=[
        {
            "title": "GPT-6 发布震撼全球",
            "summary": "OpenAI 发布了新一代旗舰模型，在多项基准测试中刷新纪录。",
            "source": "HackerNews",
            "image_url": "https://...",
            "link": "https://..."
        },
        # ... 共 10 条
    ],
    date="2026.04.03",   # 自动生成，可省略
    author="AI 编辑部"    # 默认值，可省略
)
# result 包含: formatted_content, digest, title
```

#### 第五步：上传封面图 + 推送草稿箱

```python
from scripts.wechat_auth import WeChatAuth
from scripts.wechat_draft import WeChatDraft
from scripts.image_fetcher import ImageFetcher

# 认证
auth = WeChatAuth(app_id, app_secret)

# 获取封面图（AI 主题）
fetcher = ImageFetcher()
cover = fetcher.search_and_download("artificial intelligence technology", count=1, source="unsplash")

# 上传封面
draft = WeChatDraft(auth)
thumb_media_id = draft.upload_image(cover[0], image_type="thumb")["media_id"]

# 正文中的配图需要先上传到微信获取 URL
# draft.upload_image(image_path, image_type="image") → 返回微信图片 URL
# 用微信返回的 URL 替换 HTML 中的原始图片 URL

# 创建草稿
media_id = draft.create_draft(articles=[{
    "title": result["title"],
    "author": "AI 编辑部",
    "digest": result["digest"],
    "content": result["formatted_content"],
    "thumb_media_id": thumb_media_id,
    "need_open_comment": True,
    "only_fans_can_comment": False
}])
```

#### 关键注意事项

1. **图片上传**：正文 HTML 中的配图必须先通过 `upload_image` 上传到微信，用返回的微信 URL 替换原始 URL（微信不支持外链图片）
2. **封面图**：从 Unsplash 获取通用 AI 主题图即可
3. **时间窗口**：严格过滤 48h 内的资讯，避免旧闻
4. **去重**：同一事件可能同时出现在 HN + Reddit + Twitter，只保留一条

## 详细工作流程

### 步骤 1：初始化认证

**何时执行**：首次请求或凭证过期时

**操作**：
```python
from scripts.wechat_auth import WeChatAuth

auth = WeChatAuth(app_id, app_secret)
token = auth.get_access_token()
```

**参考**: [references/wechat_api_guide.md](references/wechat_api_guide.md) 中的认证机制说明

### 步骤 2：准备内容

#### AI 生成内容

**生成原则**：
- 标题不超过 20 字
- 正文 800-1500 字
- 包含 2-4 个小标题
- 语言简洁、专业

#### 格式化现有内容

**支持的输入格式**：
- 纯文本（Markdown 格式）
- HTML（会进行清理和优化）

**格式化规则**：
- `##` → H2 标题
- `###` → H3 标题
- `- ` → 无序列表
- 空行 → 分段

**操作**：
```python
from scripts.article_formatter import ArticleFormatter

formatter = ArticleFormatter()
result = formatter.format_article(
    title="文章标题",
    content="文章内容",
    author="作者名",
    template="modern"
)
# result["formatted_content"] - HTML 内容
# result["digest"] - 摘要
```

**参考**: [references/article_style_templates.md](references/article_style_templates.md) 中的模板和排版规范

### 步骤 3：获取图片

**图片来源**：

| 图库 | 特点 | API 限制 | 推荐度 |
|------|------|----------|--------|
| Unsplash | 高质量、免费 | 公开 API 50 次/小时 | ⭐⭐⭐⭐⭐ |
| Pexels | 图片+视频 | 免费注册 200 次/小时 | ⭐⭐⭐⭐ |
| Pixabay | 资源丰富 | 免费注册 5000 次/小时 | ⭐⭐⭐⭐ |

**操作**：
```python
from scripts.image_fetcher import ImageFetcher

fetcher = ImageFetcher()
# 自动搜索并下载图片
filepaths = fetcher.search_and_download(
    query="nature",
    count=1,
    source="unsplash"
)
```

**参考**: [references/free_image_sources.md](references/free_image_sources.md) 中的详细图库列表和使用建议

### 步骤 4：上传素材

**操作**：
```python
from scripts.wechat_draft import WeChatDraft

draft = WeChatDraft(auth)
# 上传封面图
thumb_media_id = draft.upload_image(image_path, image_type="thumb")
# 上传正文配图
image_media_id = draft.upload_image(image_path, image_type="image")
```

**图片要求**：
- 封面图：2.35:1 比例，建议 900x383px
- 正文图：宽度 900px
- 格式：JPG 或 PNG
- 大小：不超过 2MB

### 步骤 5：创建草稿

**操作**：
```python
article = {
    "title": "文章标题",
    "author": "作者",
    "digest": "摘要",
    "content": "HTML 内容",
    "thumb_media_id": thumb_media_id,
    "need_open_comment": False,
    "only_fans_can_comment": False
}

media_id = draft.create_draft(articles=[article])
```

**返回**：
- 成功：返回 `media_id`
- 失败：抛出异常（包含错误码和错误信息）

## 排版模板选择

### 模板对比

| 模板 | 风格 | 适用场景 |
|------|------|----------|
| classic | 经典稳重 | 技术文章、教程、报告 |
| modern ⭐ | 现代简约 | 生活方式、品牌宣传、创意内容 |
| minimal | 极简优雅 | 文学作品、深度思考 |
| business | 商务专业 | 企业公告、产品介绍 |
| tech_magazine | 科技杂志 | AI 热点快报、科技资讯合集、行业周报 |

**选择建议**：
- 默认使用 `modern` 模板
- 技术类文章使用 `classic`
- 文学类使用 `minimal`
- 商业类使用 `business`
- **AI 热点快报 → 使用 `tech_magazine`**（Scene 5 自动使用）

## 常见问题

### Q: 上传失败怎么办？

**错误排查**：
1. 检查 `AppId` 和 `AppSecret` 是否正确
2. 检查图片大小是否超过 2MB
3. 检查网络连接
4. 查看错误码（参考 API 文档）

### Q: access_token 过期怎么办？

**自动处理**：Token 在会话内自动管理，提前 5 分钟刷新，无需手动处理。

### Q: 图片可以商用吗？

**授权确认**：
- Unsplash/Pexels/Pixabay 的图片可免费商用
- 详见 [references/free_image_sources.md](references/free_image_sources.md)

### Q: 支持多图文吗？

**当前版本**：仅支持单图文消息。多图文支持计划在未来版本添加。

### Q: 如何预览草稿？

**查看方式**：
1. 登录微信公众平台
2. 进入"草稿箱"
3. 找到对应的草稿进行预览和编辑

## 资源文件说明

### scripts/

- `wechat_auth.py` - 微信认证和 access_token 管理
- `wechat_draft.py` - 草稿箱操作（上传素材、创建草稿）
- `image_fetcher.py` - 图片获取（支持 Unsplash、Pexels、Pixabay）
- `article_formatter.py` - 文章格式化和排版

### references/

- `wechat_api_guide.md` - 微信公众号 API 完整使用指南
- `article_style_templates.md` - 排版模板和样式规范
- `free_image_sources.md` - 免费图库资源列表

## 限制和注意事项

1. **频率限制**：微信 API 有调用频率限制（通常每小时几千次）
2. **图片版权**：使用图片时需确认授权范围
3. **HTML 限制**：微信公众号不支持 JavaScript、iframe 等高级特性
4. **字符限制**：标题不超过 64 字，摘要不超过 120 字
5. **账号类型**：仅支持已认证的服务号和订阅号
