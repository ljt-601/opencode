---
name: delivery-workflow
description: 南华积分商城端到端交付工作流技能。适用于用户提供需求文档或口头需求后，需要完成需求分析、实现方案、代码实现、接口文档、PDF 导出、自动化测试、发布说明等整套交付动作。
---

# 端到端交付工作流

将用户输入的需求推进为可交付结果，并在项目根目录下产出标准化交付文件。

## 输入

- 用户口头描述的需求
- 需求文档路径
- 已有设计稿、表结构、接口说明（如果用户提供）

## 必须产出的文件

- `.workflow/change-summary.json`
- `.workflow/requirement-analysis.md`
- `.workflow/implementation-plan.md`
- `.workflow/api-doc.md`
- `.workflow/test-report.md`
- `.workflow/release-notes.md`
- `.workflow/api-doc.pdf`

## 执行顺序

1. 先使用 `requirement-analysis` 生成需求分析文档。
2. 再使用 `implementation-planning` 生成实现方案。
3. 根据实现方案落地代码，优先复用项目内既有模式、常量、枚举、工具类和 Service。
4. 如果涉及数据库改动、测试数据、迁移脚本，复用 `nanhua-database-ops`。
5. 如果涉及自动化测试，复用 `auto-test`，并把结果整理到 `.workflow/test-report.md`。
6. 如果涉及接口变更，使用 `api-doc-export` 输出 Markdown 接口文档并生成 PDF。
7. 最后使用 `release-notes` 输出发布说明，必须包含数据库改动、配置改动、接口变更、验证结果、风险提示。

## 复用现有技能

- 项目开发上下文优先参考 `nanhua-mall-dev`
- 测试优先复用 `auto-test`
- PDF 导出优先复用 `pdf`
- 数据库与 ES 操作优先复用 `nanhua-database-ops`

## 执行规则

- 不要跳过需求分析直接写代码。
- 不要只给思路，必须产出文档文件。
- 数据库改动和配置改动必须同步写入 `.workflow/change-summary.json` 和 `.workflow/release-notes.md`。
- 接口文档必须从最终代码和 DTO/返回结构反推，不要只按需求臆测。
- 如果用户只要求执行某个阶段，可以只执行对应阶段，但要显式说明跳过了哪些后续产物。

## 参考模板

- 需求分析模板：`templates/requirement-analysis-template.md`
- 实现方案模板：`templates/implementation-plan-template.md`
- 接口文档模板：`templates/api-doc-template.md`
- 发布说明模板：`templates/release-notes-template.md`
- 变更摘要模板：`templates/change-summary-template.json`
