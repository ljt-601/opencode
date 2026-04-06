# OCR 引擎对比和选择指南

## 概述

本文档对比主流 OCR 引擎的特性，帮助选择最适合的工具。

## 主流 OCR 引擎

### 1. PaddleOCR

**开发者**: 百度飞桨

**特点**:
- 中文识别效果优秀
- 免费开源
- 支持倾斜矫正、弯曲文字
- 模型精度高

**安装**:
```bash
pip install paddleocr paddlepaddle
```

**使用**:
```python
from paddleocr import PaddleOCR

ocr = PaddleOCR(use_angle_cls=True, lang='ch')
result = ocr.ocr('image.jpg')
```

**优点**:
- 中文识别准确率高（95%+）
- 支持中英文混合
- 倾斜矫正效果好
- 活跃的社区支持

**缺点**:
- 模型较大（~200MB）
- 首次加载较慢
- 内存占用较高（~500MB）

**适用场景**:
- 中文文档识别
- 复杂排版文字
- 低质量图片

---

### 2. Tesseract

**开发者**: Google

**特点**:
- 轻量级
- 多语言支持
- 成熟稳定

**安装**:
```bash
pip install pytesseract pillow

# macOS
brew install tesseract

# Linux
sudo apt-get install tesseract-ocr

# 可选: 下载中文语言包
```

**使用**:
```python
import pytesseract
from PIL import Image

text = pytesseract.image_to_string(Image.open('image.jpg'), lang='chi_sim+eng')
```

**优点**:
- 安装简单
- 内存占用低（~100MB）
- 速度快

**缺点**:
- 中文识别效果一般（70-80%）
- 对图片质量要求高
- 不支持倾斜矫正

**适用场景**:
- 纯英文内容
- 高质量扫描件
- 资源受限环境

---

## 性能对比

| 指标 | PaddleOCR | Tesseract |
|------|-----------|-----------|
| 中文准确率 | 95%+ | 70-80% |
| 英文准确率 | 90%+ | 85%+ |
| 处理速度（1张图） | 2-5秒 | 1-3秒 |
| 内存占用 | ~500MB | ~100MB |
| 模型大小 | ~200MB | ~20MB |
| 倾斜矫正 | ✓ | ✗ |

## 推荐选择

### 中文内容

**推荐**: PaddleOCR

理由: 中文识别准确率高，支持复杂场景。

### 英文内容

**推荐**: Tesseract 或 PaddleOCR

理由:
- 简单场景：Tesseract 足够
- 复杂场景：PaddleOCR 更准确

### 资源受限

**推荐**: Tesseract

理由: 轻量级，内存占用低。

### 批量处理

**推荐**: PaddleOCR（如果资源允许）

理由: 准确率高，减少后期人工校对。

## 优化建议

### 提高识别准确率

1. **图片预处理**:
   - 调整对比度和亮度
   - 去噪
   - 二值化

2. **调整图片尺寸**:
   - 分辨率至少 300 DPI
   - 最小边长 1000px

3. **选择合适的语言**:
   - PaddleOCR: `lang='ch'`（中文）、`lang='en'`（英文）
   - Tesseract: `lang='chi_sim+eng'`（中英混合）

4. **使用方向分类器**:
   - PaddleOCR: `use_angle_cls=True`
   - 自动旋转倾斜图片

## 故障排查

### PaddleOCR 问题

**Q: 首次运行慢？**
A: 首次下载模型，后续会缓存。

**Q: 内存不足？**
A: 使用更小的模型或切换到 Tesseract。

### Tesseract 问题

**Q: 中文识别差？**
A: 安装中文语言包 `chi_sim`，或切换到 PaddleOCR。

**Q: 找不到 tesseract 命令？**
A: 设置路径:
```python
pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'
```

## 参考资料

- [PaddleOCR GitHub](https://github.com/PaddlePaddle/PaddleOCR)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [pytesseract 文档](https://pypi.org/project/pytesseract/)
