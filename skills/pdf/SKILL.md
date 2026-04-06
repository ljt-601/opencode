---
name: pdf
description: PDF 处理技能。适用于从 Markdown、HTML、现有文档生成 PDF，或对 PDF 进行读取、拆分、合并、提取和表单处理。
---

# PDF 处理技能

本技能在本项目里优先用于接口文档、发布说明等交付文档的 PDF 生成与处理。

## 适用场景

- 将 `.workflow/api-doc.md` 导出为 `.workflow/api-doc.pdf`
- 将发布说明、需求分析等 Markdown 文档导出为 PDF
- 读取现有 PDF 内容
- 拆分、合并、提取 PDF 页面或文本

## 项目内推荐用法

1. 先生成 Markdown 源文件。
2. 再导出 PDF，不要直接从口头描述生成 PDF。
3. 接口文档优先固定输出到 `.workflow/api-doc.pdf`。

## 关键规则

- PDF 内容必须基于最终文档文件，不要跳过 Markdown 草稿阶段。
- 如果文档包含接口信息，必须与最终 Controller、DTO、返回结构一致。
- 如果环境中缺少 PDF 依赖或命令，要明确记录失败原因和替代方案。

## 常见任务

- 读取 PDF 内容并提取文字
- 将 Markdown/HTML 导出为 PDF
- 合并多个 PDF
- 拆分指定页码范围
- 处理表单 PDF
