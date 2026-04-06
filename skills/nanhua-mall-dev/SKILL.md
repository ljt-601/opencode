---
name: nanhua-mall-dev
description: 南华积分商城项目开发技能。适用于各模块业务开发、接口开发、问题排查、代码评审与需求落地，提供与当前项目结构、分层模式、编码规范一致的开发指引。前缀触发：使用 "yf" 开头的语句将自动触发此技能。
---

# 南华积分商城项目开发技能

本技能用于在当前项目中落地后端需求，优先保证实现与现有架构、常量体系、返回结构、异常处理、构建方式一致。

## 使用场景

- 新增或改造业务功能
- 新增或修改 Controller / Service / Mapper / DTO / VO / Enum / Constant
- 排查现有业务逻辑、接口行为、数据库映射
- 根据需求分析与实现方案开始编码

## 关键约束

- 真正的 Maven 根目录是 `six-parent`
- Controller 保持轻量，复杂逻辑优先下沉到 Service / HandleService
- 先判断改动属于 Admin 还是 Web 链路，再决定返回结构、认证方式、基类和权限控制
- 优先复用现有工具类、常量、枚举、Service，不要平地起新模式
- 不要硬编码状态值、类型值、错误码、分隔符、缓存 key、缓存时长
- Redis 相关 key、前缀、TTL 优先复用 `RedisConts`
- 通用常量优先复用 `Conts`，第三方相关优先复用 `ThirdConts`、`H5Conts`
- 集合判空优先使用 `CollUtil.isEmpty()` / `CollUtil.isNotEmpty()`
- 字符串处理优先使用 `StrUtil` 或项目内 `StringUtils`
- Bean 拷贝优先使用 `BeanUtil`，日期处理优先使用 `DateUtil` 或 `DateUtils`，JSON 处理优先使用 `JSONUtil`
- Java 改动后必须补齐 import，清理无用 import

## 分层规则

- `six-bootstrap`：启动类、Controller、Config、资源配置
- `six-modules`：业务实现、Service、DAO、领域对象
- `six-common`：公共组件、工具、配置
- `six-api`：DTO、接口契约、跨服务模型

## 服务差异

- Admin：`/console/mall`，JWT 无状态认证，常见返回 `AjaxResult`、`TableDataInfo`
- Web：`/mall/nh`，Session 风格，常见返回 `ApiModel<T>`

## 开发流程

1. 先阅读需求分析与实现方案文档。
2. 搜索现有相似实现，确定改动模块和分层位置。
3. 按现有模式完成代码实现。
4. 若涉及数据库变更，配合 `nanhua-database-ops` 补充脚本或数据变更说明。
5. 若涉及接口变更，配合 `api-doc-export` 整理接口文档。
6. 若涉及测试，配合 `auto-test` 输出 `.workflow/test-report.md`。

## 最低校验要求

- 至少完成受影响模块编译验证
- 公共模块改动要做联动编译
- 输出改动摘要、验证结果和剩余风险
