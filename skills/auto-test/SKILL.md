---
name: auto-test
description: 南华积分商城自动化测试技能。适用于根据需求或代码改动生成测试方案、测试代码、测试数据和测试报告，支持 Service、Controller、接口与回归测试。前缀触发：使用 "cs" 开头的语句将自动触发此技能。
---

# 自动化测试技能

本技能用于为当前需求或代码改动生成并执行测试方案，最终输出 `.workflow/test-report.md`。

## 适用场景

- Service 方法测试
- Controller / 接口测试
- 回归测试范围梳理
- 边界场景、异常场景、幂等场景设计

## 必须产出

- `.workflow/test-report.md`

## 推荐模板

- `templates/test-report-template.md`

## 执行步骤

1. 先读取 `.workflow/requirement-analysis.md` 和 `.workflow/implementation-plan.md`。
2. 识别本次改动涉及的 Service、Controller、Mapper、第三方接口和数据库影响。
3. 设计最少应覆盖的正常、异常、边界、幂等、回归场景。
4. 如果需要，补充或生成测试代码。
5. 执行相关测试或说明无法执行的原因。
6. 将执行范围、结果、失败原因、未覆盖风险写入 `.workflow/test-report.md`。

## 关键规则

- 不要只给“建议测一下”，必须输出测试结果文档。
- 优先覆盖本次变更直接影响的代码路径。
- 涉及状态流转、金额、库存、权限、会话、缓存时，必须补边界或异常场景。
- 如果无法自动执行测试，也要明确写出建议命令、未执行原因和待人工验证点。

## 测试结果至少包含

- 测试目标
- 覆盖范围
- 执行方式
- 通过 / 失败情况
- 失败原因
- 未覆盖风险
