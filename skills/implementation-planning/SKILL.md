---
name: implementation-planning
description: 实现方案规划技能。适用于基于需求分析结果，产出分模块、分层次、可执行的开发方案与验证方案。
---

# 实现方案规划技能

基于 `.workflow/requirement-analysis.md` 输出 `.workflow/implementation-plan.md`。

## 输出要求

- 使用 `templates/implementation-plan-template.md` 作为结构模板
- 明确列出涉及的 Controller、Service、Mapper、Entity、DTO、VO、配置文件、SQL 或脚本
- 明确数据库、缓存、配置、接口文档、测试和发布说明需要补哪些内容
- 方案要可执行，不能只写抽象建议

## 规划步骤

1. 把需求拆成后端逻辑、接口、数据结构、测试、文档五个维度。
2. 对每个维度列出改动文件或目标类的预期位置。
3. 判断哪些改动必须联动编译或联动测试。
4. 同步更新 `.workflow/change-summary.json` 中的影响模块、接口、数据库和配置变更草稿。

## 关键要求

- 实现方案必须服务于后续编码，不能写成纯汇报文档。
- 如果发现需求与现有架构冲突，要在方案中直接指出替代实现。
- 若涉及接口变更，要预留接口文档和 PDF 导出步骤。
