# 免费图库资源列表

本文档列出可用于微信公众号的免费图库资源。

## 国际免费图库

### Unsplash ⭐ 推荐

**网址**: https://unsplash.com

**特点**:
- 完全免费，无需注册
- 高质量照片
- 每周更新
- 支持中文搜索

**使用方式**:
- 直接下载: 浏览搜索后下载
- API 调用: 免费公开 API（每小时 50 次）
- 热链引用: `https://source.unsplash.com/featured/?{keyword}`

**授权**: Unsplash License（可免费使用，包括商业用途）

**图片规格**:
- 支持多种分辨率
- 原图通常 3-5MB

**最佳用途**:
- 封面图
- 文章配图
- 品牌素材

---

### Pexels

**网址**: https://www.pexels.com

**特点**:
- 完全免费，无需注册
- 视频和图片
- 支持中文搜索
- API 可用

**使用方式**:
- 直接下载: 网站搜索下载
- API 调用: 需要免费 API Key（每小时 200 次）

**授权**: Pexels License（免费使用，可修改，商业用途）

**图片规格**:
- 多种分辨率可选
- 原图通常 2-4MB

**最佳用途**:
- 文章配图
- 插图
- 背景图

---

### Pixabay

**网址**: https://pixabay.com

**特点**:
- 完全免费
- 支持中文搜索
- 图片、矢量图、视频
- API 可用

**使用方式**:
- 直接下载: 网站搜索下载
- API 调用: 需要免费 API Key（每小时 5000 次）

**授权**: Pixabay License（免费使用，可修改）

**图片规格**:
- 多种分辨率
- 原图通常 1-3MB

**最佳用途**:
- 插图
- 图标
- 背景图

---

## 国内免费图库

### Pixso

**网址**: https://pixso.cn

**特点**:
- 国内访问速度快
- 中文界面
- 部分免费

### Huaban（花瓣网）

**网址**: https://huaban.com

**特点**:
- 中文搜索
- 国内访问快
- 需注意版权

### ZCOOL（站酷）

**网址**: https://www.zcool.com.cn

**特点**:
- 设计师作品
- 中文搜索
- 需注意版权

## 使用建议

### 封面图选择

- 尺寸: 2.35:1 比例（推荐 900x383 或 1080x460）
- 主体: 清晰、有冲击力
- 色彩: 鲜明但不刺眼
- 文字: 留出空间放置标题

### 配图选择

- 风格: 与文章主题一致
- 质量: 高清晰度
- 尺寸: 宽度 900px
- 格式: JPG 或 PNG

### 版权注意事项

⚠️ **重要提醒**:

1. **图库授权**: 确认图库的授权范围
2. **人物肖像**: 如有人物，需确认肖像权授权
3. **商标品牌**: 避免使用包含商标的图片
4. **修改权限**: 确认是否允许修改图片
5. **署名要求**: 部分图库可能需要署名

### 图片优化

- 压缩大小: 控制在 500KB 以内
- 格式选择: 照片用 JPG，图标用 PNG
- 色彩模式: RGB
- DPI: 72（网页显示）

### API 使用示例

#### Unsplash API

```python
import requests

url = "https://api.unsplash.com/photos/random"
params = {
    "client_id": "YOUR_ACCESS_KEY",
    "query": "nature",
    "orientation": "landscape"
}
response = requests.get(url, params=params)
data = response.json()
image_url = data["urls"]["regular"]
```

#### Pexels API

```python
import requests

url = "https://api.pexels.com/v1/search"
headers = {"Authorization": "YOUR_API_KEY"}
params = {
    "query": "business",
    "per_page": 1,
    "orientation": "horizontal"
}
response = requests.get(url, headers=headers, params=params)
data = response.json()
image_url = data["photos"][0]["src"]["large"]
```

## 常见问题

### Q: 这些图片可以商用吗？

A: 列出的国际图库（Unsplash, Pexels, Pixabay）都允许商用，但请仔细阅读具体的授权协议。

### Q: 需要署名吗？

A: 大部分免费图库不需要署名，但署名是一种良好的做法。

### Q: 图片可以修改吗？

A: 可以，你可以裁剪、调色、添加文字等。

### Q: 国内图库推荐吗？

A: 国内图库访问速度快，但版权情况复杂，建议优先使用国际知名免费图库。

### Q: 图片找不到合适的怎么办？

A: 尝试不同的关键词、使用同义词、切换图库平台。
