---
name: media-content-extractor
description: 媒体内容文字提取工具。支持从图片、视频、社交媒体链接中自动提取文字内容。图片使用 OCR 提取文字，视频使用 ASR（语音识别）和字幕提取。适用于：内容转录、视频字幕生成、图片文字识别、社交媒体内容提取等场景。触发关键词："提取图片文字"、"提取视频文字"、"视频转文字"、"图片转文字"、"提取链接内容"等。
---

# 媒体内容文字提取器

## 概述

本 skill 提供从多种媒体来源自动提取文字内容的能力，支持图片 OCR、视频语音识别、字幕提取，以及主流社交媒体平台的内容解析。

### 主要能力

1. **图片 OCR**：从图片中提取文字（支持中文和英文）
2. **视频转文字**：通过 ASR 将视频语音转换为文字
3. **字幕提取**：提取视频内嵌字幕
4. **社交媒体解析**：支持抖音、小红书、B站等平台的内容下载和文字提取
5. **智能识别**：自动识别 URL 类型并选择最佳提取方法

### 工作流程

```
用户提供链接/文件 → 自动识别类型 → 选择处理方法 → 提取文字 → 返回结果
```

## 使用前准备

### 依赖安装

根据需要安装相应的依赖：

```bash
# 图片 OCR（推荐 PaddleOCR，中文效果好）
pip install paddleocr paddlepaddle

# 或者使用 Tesseract
pip install pytesseract pillow
# macOS
brew install tesseract
# Linux
sudo apt-get install tesseract-ocr

# 视频处理
pip install openai-whisper  # 或 faster-whisper（更快）
pip install pysrt

# 社交媒体下载
pip install yt-dlp

# 视频处理依赖（需要 ffmpeg）
brew install ffmpeg  # macOS
sudo apt install ffmpeg  # Linux
```

### OCR 引擎选择

| 引擎 | 优点 | 缺点 | 推荐场景 |
|------|------|------|----------|
| **PaddleOCR** | 中文效果好，免费开源 | 模型较大 | **中文内容（推荐）** |
| Tesseract | 轻量级，安装简单 | 中文效果一般 | 纯英文内容 |

### ASR 引擎选择

| 引擎 | 优点 | 缺点 | 推荐场景 |
|------|------|------|----------|
| **Whisper** | 准确率高，多语言支持 | 速度较慢 | **通用场景（推荐）** |
| **Faster-Whisper** | 速度快，内存占用低 | 需要额外安装 | 批量处理/长视频 |

## 使用方法

### 方法 1：图片 OCR

**支持的输入**：
- 本地图片文件路径
- 图片 URL（http/https）

**使用示例**：

```python
from scripts.content_extractor import ContentExtractor

extractor = ContentExtractor(use_paddle=True)
result = extractor.extract("/path/to/image.jpg")
print(result["text"])
```

### 方法 2：视频转文字

**提取方法**：
- `auto`：自动选择（优先字幕，失败则 ASR）
- `subtitle`：仅提取内嵌字幕
- `asr`：强制使用 ASR 语音识别

**使用示例**：

```python
extractor = ContentExtractor(asr_engine="whisper")

# 自动选择方法
result = extractor.extract("/path/to/video.mp4", method="auto")

# 强制使用 ASR
result = extractor.extract("/path/to/video.mp4", method="asr")
print(result["text"])
```

### 方法 3：社交媒体链接

**支持的平台**：
- 抖音 (douyin.com)
- 小红书 (xiaohongshu.com)
- B站 (bilibili.com)
- YouTube (youtube.com)
- 微博 (weibo.com)

**使用示例**：

```python
extractor = ContentExtractor()

# 抖音视频
result = extractor.extract("https://www.douyin.com/video/12345")
print(result["text"])

# B站视频
result = extractor.extract("https://www.bilibili.com/video/BV1xx")
print(result["text"])
```

### 方法 4：便捷函数

```python
from scripts.content_extractor import extract_text

text = extract_text("https://example.com/image.jpg")
print(text)
```

## 工作流程详解

### 步骤 1：URL 类型识别

系统会自动识别输入类型：

| 输入 | 识别结果 |
|------|----------|
| `https://example.com/image.jpg` | 图片 URL |
| `https://example.com/video.mp4` | 视频 URL |
| `https://www.douyin.com/...` | 社交媒体链接 |
| `/Users/test/photo.png` | 本地图片 |
| `/Users/test/movie.mp4` | 本地视频 |

### 步骤 2：内容提取

#### 图片处理流程

1. 下载图片（如果是 URL）
2. 使用 OCR 引擎提取文字
3. 返回文字内容
4. 清理临时文件

#### 视频处理流程

**方法：subtitle**
1. 使用 ffmpeg 提取字幕轨道
2. 解析 SRT 字幕文件
3. 返回字幕文本

**方法：asr**
1. 使用 ffmpeg 提取音频（WAV 格式）
2. 使用 Whisper 转录音频
3. 返回识别的文字

**方法：auto**
1. 尝试提取字幕
2. 如果字幕为空，自动切换到 ASR
3. 返回结果

#### 社交媒体处理流程

1. 使用 yt-dlp 下载媒体内容
2. 根据文件类型选择提取方法
3. 执行图片 OCR 或视频转文字
4. 返回结果
5. 清理下载的临时文件

## 返回结果格式

### 成功结果

```python
{
    "text": "提取的文字内容",
    "metadata": {
        "type": "image|video|social_media",
        "source": "原始 URL 或路径",
        "method": "asr|subtitle",
        "platform": "douyin|xiaohongshu|bilibili|...",
        "media_type": "image|video"
    }
}
```

### 错误结果

```python
{
    "text": "",
    "error": "错误描述",
    "metadata": {
        "type": "unknown|unsupported"
    }
}
```

## 常见问题

### Q: OCR 识别不准确怎么办？

**解决方法**：
1. 图片清晰度：确保图片分辨率足够高
2. 尝试不同 OCR 引擎（PaddleOCR vs Tesseract）
3. 图片预处理：调整对比度、去噪
4. 中英文混合：使用 `lang='ch+en'` 参数

### Q: 视频 ASR 速度太慢？

**解决方法**：
1. 使用 `faster-whisper` 引擎
2. 使用更小的模型（`tiny` 或 `base`）
3. 对于长视频，先提取字幕，失败再用 ASR

### Q: 社交媒体链接下载失败？

**可能原因**：
1. 平台限制或隐私设置
2. yt-dlp 版本过旧
3. 链接格式不正确

**解决方法**：
1. 更新 yt-dlp：`pip install --upgrade yt-dlp`
2. 检查链接是否可公开访问
3. 尝试使用浏览器开发者工具获取直链

### Q: ffmpeg 未找到？

**安装方法**：
```bash
# macOS
brew install ffmpeg

# Linux (Ubuntu/Debian)
sudo apt update
sudo apt install ffmpeg

# 验证安装
ffmpeg -version
```

### Q: 内存不足？

**优化方法**：
1. 使用 `faster-whisper` 代替 `whisper`
2. 使用更小的模型
3. 分段处理长视频

## 性能参考

| 任务 | 预计时间 | 资源占用 |
|------|----------|----------|
| 图片 OCR (PaddleOCR) | 2-5 秒 | ~500MB |
| 图片 OCR (Tesseract) | 1-3 秒 | ~100MB |
| 视频 ASR (1分钟) | 30-60 秒 | ~2GB |
| 视频 ASR (10分钟) | 5-10 分钟 | ~2GB |
| 字幕提取 | < 5 秒 | ~100MB |
| 社交媒体下载 | 取决于文件大小 | 取决于下载速度 |

## 限制和注意事项

1. **平台限制**：某些社交媒体平台可能有反爬限制
2. **版权**：仅用于合法内容提取，遵守平台服务条款
3. **隐私**：不要提取包含个人隐私的内容
4. **文件大小**：超大文件可能需要更长时间
5. **网络**：URL 下载需要稳定的网络连接

## 高级用法

### 批量处理

```python
from scripts.content_extractor import extract_text

urls = [
    "https://example.com/image1.jpg",
    "https://example.com/video1.mp4",
    "https://www.douyin.com/video/123"
]

results = []
for url in urls:
    result = extract_text(url)
    results.append(result)

print(results)
```

### 自定义 OCR 引擎参数

```python
from scripts.image_ocr import ImageOCR

ocr = ImageOCR(use_paddle=True)
text = ocr.extract_text("/path/to/image.jpg")
```

### 自定义 ASR 引擎

```python
from scripts.video_processor import VideoProcessor

processor = VideoProcessor(asr_engine="faster-whisper")
text = processor.extract_text("/path/to/video.mp4", method="asr")
```

## 技术栈

- **OCR**: PaddleOCR / Tesseract
- **ASR**: OpenAI Whisper / Faster-Whisper
- **视频处理**: ffmpeg, pysrt
- **社交媒体**: yt-dlp
- **HTTP**: requests

## 资源文件说明

### scripts/

- `url_detector.py` - URL 类型检测器
- `image_ocr.py` - 图片 OCR 文字提取
- `video_processor.py` - 视频处理和 ASR
- `social_media_parser.py` - 社交媒体链接解析
- `content_extractor.py` - 主入口（整合所有功能）

### references/

- `ocr_engines.md` - OCR 引擎对比和选择指南
- `asr_models.md` - ASR 模型对比和性能测试
- `social_media_apis.md` - 社交媒体平台 API 文档

## 触发关键词

- "提取图片文字"
- "提取视频文字"
- "视频转文字"
- "图片转文字"
- "提取链接内容"
- "识别图片文字"
- "转录视频"
