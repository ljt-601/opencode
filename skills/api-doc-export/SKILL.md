---
name: api-doc-export
description: 接口文档与 PDF 导出技能。适用于根据最终 Controller、DTO、返回结构整理接口文档，并生成 PDF 版接口文档。
---

# 接口文档与 PDF 导出技能

根据最终代码生成 `.workflow/api-doc.md`，再导出 `.workflow/api-doc.pdf`。

## 输出要求

- 使用 `templates/api-doc-template.md` 作为基础模板
- 只记录真实存在或本次改动涉及的接口
- 文档内容至少包含：接口名称、路径、请求方式、请求头、请求参数、返回结构、错误码、注意事项
- PDF 导出优先复用现有 `pdf` 技能能力

## 执行规则

1. 先根据最终 Controller、DTO、VO、返回结构整理 Markdown 文档。
2. 区分 Admin 接口和 Web / App 接口，返回结构要分别说明。
3. 若接口依赖认证，写清楚 `Authorization` 或 Session 要求。
4. 若接口涉及分页、文件上传、导出、幂等、限流等特殊行为，要单独标注。
5. Markdown 完成后再导出 PDF，不要直接从需求文档生成 PDF。
