---
name: release-notes
description: 发布说明生成技能。适用于根据实现结果、数据库改动、配置改动、接口变更、测试结果生成标准发布说明。
---

# 发布说明生成技能

根据 `.workflow/change-summary.json`、`.workflow/implementation-plan.md`、`.workflow/test-report.md`、`.workflow/api-doc.md` 输出 `.workflow/release-notes.md`。

## 输出要求

- 使用 `templates/release-notes-template.md` 作为基础模板
- 必须包含：需求摘要、代码改动摘要、数据库改动、配置改动、接口变更、测试结果、发布注意事项、回滚提示
- 如果没有数据库或配置改动，也要明确写“无”

## 执行规则

1. 数据库改动必须列出表名、字段、脚本文件或 SQL 摘要。
2. 配置改动必须列出环境、配置项、默认值变化、是否需要运维配合。
3. 接口变更必须说明新增、修改还是兼容性调整。
4. 测试结果必须说明执行方式、覆盖范围、通过情况和未覆盖风险。
5. 如果存在高风险点或手工操作项，要单独加粗提示。
