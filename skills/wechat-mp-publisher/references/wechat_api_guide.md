# 微信公众号 API 使用指南

本文档介绍微信公众号草稿箱相关 API 的使用方法。

## 认证机制

### 获取 access_token

**接口地址**: `GET https://api.weixin.qq.com/cgi-bin/token`

**请求参数**:
- `grant_type`: 固定值 "client_credential"
- `appid`: 公众号的 AppId
- `secret`: 公众号的 AppSecret

**返回示例**:
```json
{
  "access_token": "ACCESS_TOKEN",
  "expires_in": 7200
}
```

**注意事项**:
- access_token 有效期为 7200 秒（2 小时）
- 建议提前 5 分钟刷新 token
- access_token 在会话内缓存，避免频繁请求

## 素材上传

### 上传图片

**接口地址**: `POST https://api.weixin.qq.com/cgi-bin/material/add_material`

**请求参数**:
- `access_token`: 调用接口凭证
- `type`: 素材类型，这里填写 "thumb"（缩略图）或 "image"（图片）
- `media`: form-data 中媒体文件标识

**返回示例**:
```json
{
  "media_id": "MEDIA_ID",
  "url": "http://mmbiz.qpic.cn/..."
}
```

**注意事项**:
- 图片格式: JPG, PNG
- 图片大小: 不超过 2MB
- 缩略图尺寸: 建议尺寸 400x400 像素

## 草稿箱操作

### 新建草稿

**接口地址**: `POST https://api.weixin.qq.com/cgi-bin/draft/add`

**请求参数**:
```json
{
  "articles": [
    {
      "title": "标题",
      "author": "作者",
      "digest": "摘要",
      "content": "HTML 内容",
      "content_source_url": "原文链接（可选）",
      "thumb_media_id": "封面图片素材 ID",
      "need_open_comment": true,
      "only_fans_can_comment": false
    }
  ]
}
```

**返回示例**:
```json
{
  "media_id": "MEDIA_ID"
}
```

**字段说明**:
- `title`: 标题，不超过 64 字符
- `author`: 作者，不超过 16 字符
- `digest`: 摘要，不超过 120 字符
- `content`: 正文内容，HTML 格式
- `thumb_media_id`: 封面图片素材 ID（必需）
- `need_open_comment`: 是否打开评论（默认 false）
- `only_fans_can_comment`: 是否只有粉丝可以评论（默认 false）

### 更新草稿

**接口地址**: `POST https://api.weixin.qq.com/cgi-bin/draft/update`

**请求参数**:
```json
{
  "media_id": "草稿 media_id",
  "index": 0,
  "article": {
    "title": "新标题",
    ...
  }
}
```

**字段说明**:
- `media_id`: 要更新的草稿 ID
- `index`: 要更新的文章索引（从 0 开始）
- `article`: 新的文章内容

## 常见错误码

| 错误码 | 说明 |
|--------|------|
| 40001 | access_token 无效 |
| 40002 | 不合法的凭证类型 |
| 40003 | 不合法的 OpenID |
| 40004 | 不合法的媒体文件类型 |
| 40005 | 不合法的文件类型 |
| 40006 | 不合法的文件大小 |
| 40007 | 不合法的媒体文件 ID |
| 45009 | 接口调用次数超限 |
| 46001 | 媒体文件不存在 |

## HTML 内容规范

### 支持的标签

- 基础标签: `<p>`, `<br>`, `<strong>`, `<em>`, `<u>`
- 标题: `<h1>`, `<h2>`, `<h3>`
- 列表: `<ul>`, `<ol>`, `<li>`
- 表格: `<table>`, `<tr>`, `<td>`, `<th>`
- 容器: `<div>`, `<section>`, `<span>`
- 图片: `<img>`
- 链接: `<a>`

### CSS 支持

- 基础样式: color, font-size, font-weight, text-align
- 布局: margin, padding, width, height
- 装饰: background, border, border-radius

### 不支持的特性

- JavaScript
- iframe
- form
- 外部样式表（内联样式才支持）
- 部分高级 CSS3 特性
