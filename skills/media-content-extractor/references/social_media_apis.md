# 社交媒体平台 API 文档

## 概述

本文档总结主流社交媒体平台的内容获取方法和限制。

## 支持的平台

### 1. 抖音 (Douyin)

**域名**: `douyin.com`, `iesdouyin.com`

**链接格式**:
- `https://www.douyin.com/video/{video_id}`
- `https://v.douyin.com/{share_id}`

**支持工具**: `yt-dlp`

**示例**:
```python
import yt_dlp

url = "https://www.douyin.com/video/7123456789"
ydl_opts = {'outtmpl': '%(id)s.%(ext)s'}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(url, download=True)
```

**限制**:
- 部分视频需要登录
- 短链接需要先解析
- 可能有地域限制

---

### 2. 小红书 (Xiaohongshu)

**域名**: `xiaohongshu.com`, `xhslink.com`

**链接格式**:
- `https://www.xiaohongshu.com/explore/{note_id}`
- `https://xhslink.com/{share_id}`

**支持工具**: `yt-dlp`

**示例**:
```python
url = "https://www.xiaohongshu.com/explore/123456789"
```

**内容类型**:
- 图片（多图笔记）
- 视频（视频笔记）

**限制**:
- 部分内容需要登录
- 下载可能有水印

---

### 3. B站 (Bilibili)

**域名**: `bilibili.com`, `b23.tv`

**链接格式**:
- `https://www.bilibili.com/video/BV{video_id}`
- `https://www.bilibili.com/video/av{aid}`
- `https://b23.tv/{short_id}`

**支持工具**: `yt-dlp`, `you-get`

**示例**:
```python
url = "https://www.bilibili.com/video/BV1xx411c7mD"

# 下载最高质量
ydl_opts = {
    'format': 'bestvideo+bestaudio/best',
    'outtmpl': '%(id)s.%(ext)s'
}
```

**质量选项**:
- 360P, 480P, 720P, 1080P, 4K
- 需要 Cookie 才能下载高画质

**限制**:
- 高画质需要大会员
- 部分 UP 主禁止下载
- 需要 Cookie 绕过部分限制

---

### 4. YouTube

**域名**: `youtube.com`, `youtu.be`

**链接格式**:
- `https://www.youtube.com/watch?v={video_id}`
- `https://youtu.be/{video_id}`
- `https://www.youtube.com/shorts/{video_id}`

**支持工具**: `yt-dlp`

**示例**:
```python
url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# 下载字幕
ydl_opts = {
    'writesubtitles': True,
    'subtitleslangs': ['zh', 'en'],
    'skip_download': True
}
```

**限制**:
- 部分视频有地区限制
- 需要 Cookie 下载高画质
- YouTube Shorts 可能需要特殊处理

---

### 5. 微博 (Weibo)

**域名**: `weibo.com`, `weibo.cn`

**链接格式**:
- `https://weibo.com/tv/show/{id}`
- `https://weibo.com/{user}/{status_id}`

**支持工具**: `yt-dlp`

**示例**:
```python
url = "https://weibo.com/tv/show/123456"
```

**限制**:
- 视频有效期有限
- 部分内容需要登录

---

## 通用工具

### yt-dlp

**安装**:
```bash
pip install yt-dlp
```

**基本用法**:
```python
import yt_dlp

url = "https://www.bilibili.com/video/BV1xx"

ydl_opts = {
    'format': 'best',
    'outtmpl': 'downloads/%(title)s.%(ext)s',
    'quiet': True,
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])
```

**高级选项**:
```python
ydl_opts = {
    # 格式选择
    'format': 'bestvideo+bestaudio/best',  # 最佳视频+音频

    # 字幕
    'writesubtitles': True,
    'subtitleslangs': ['zh', 'en'],
    'writeautomaticsub': True,  # 自动生成字幕

    # 元数据
    'writeinfojson': True,  # 保存视频信息
    'writethumbnail': True,  # 保存缩略图

    # Cookie
    'cookiefile': 'cookies.txt',

    # 代理
    'proxy': 'http://127.0.0.1:7890',
}
```

---

## 常见问题

### Q: 下载失败怎么办？

**解决方法**:
1. 更新 yt-dlp：`pip install --upgrade yt-dlp`
2. 检查网络连接
3. 使用代理
4. 检查链接是否可公开访问

### Q: 如何获取 Cookie？

**方法**:
1. 安装浏览器扩展（如 "Get cookies.txt"）
2. 导出 Cookie 到 `cookies.txt`
3. 使用 `cookiefile` 选项

### Q: 如何下载高画质？

**B站**:
- 需要大会员
- 需要 Cookie

**YouTube**:
- 需要 Cookie
- 某些视频需要付费

### Q: 短链接如何处理？

**方法**:
- yt-dlp 会自动解析短链接
- 或手动展开：
  ```python
  import requests
  response = requests.head(url, allow_redirects=True)
  real_url = response.url
  ```

---

## 法律和道德

### 版权

- 仅用于个人学习研究
- 不得用于商业用途
- 尊重原作者版权

### 隐私

- 不要下载私人内容
- 不要传播敏感信息

### 服务条款

- 遵守各平台服务条款
- 不得用于恶意目的

---

## 参考资料

- [yt-dlp GitHub](https://github.com/yt-dlp/yt-dlp)
- [you-get GitHub](https://github.com/soimort/you-get)
- [B站 API 文档](https://github.com/SocialSisterYi/bilibili-API-collect)
