# ES 索引结构参考

本文档提供南华积分商城项目 ES 索引结构的快速查找指南。

## 如何查找索引结构

### 1. 通过 ES Model 查找

ES Model 位于：`six-modules/six-module-es/src/main/java/com/six/es/model/*.java`

示例查找 EsUserNoticePlan：
```bash
find /Users/bryle/Public/WorkProject/nanhua-mall -name "EsUserNoticePlan.java" -path "*/es/model/*"
```

### 2. 通过 ES Service 查找

ES Service 位于：`six-modules/six-module-es/src/main/java/com/six/es/service/*Service.java`

示例查找 EsUserNoticePlanService：
```bash
find /Users/bryle/Public/WorkProject/nanhua-mall -name "*UserNoticePlanService.java" -path "*/es/service/*"
```

### 3. 通过 ES ServiceImpl 查找

ES ServiceImpl 位于：`six-modules/six-module-es/src/main/java/com/six/es/service/impl/*ServiceImpl.java`

示例查找查询实现：
```bash
find /Users/bryle/Public/WorkProject/nanhua-mall -name "*UserNoticePlanServiceImpl.java"
```

## 常用索引映射关系

| 索引名 | Model 类 | Service 类 | 模块 |
|--------|---------|-----------|------|
| EsUserNoticePlan | EsUserNoticePlan.java | EsUserNoticePlanService.java | six-module-es |
| EsUserNoticeSend | EsUserNoticeSend.java | EsUserNoticeSendService.java | six-module-es |
| EsShortLink | EsShortLink.java | EsShortLinkService.java | six-module-es |
| EsUserTag | EsUserTag.java | EsUserTagService.java | six-module-es |

## 索引结构信息提取

从 ES Model 中提取的典型信息：
- 字段名称和类型
- 字段注释（`@ApiModelProperty` 注解）
- 继承关系（继承 `EsBaseModel`）

从 ES Service 中提取的典型信息：
- 查询方法（`getList`, `findById`, `save`, `delete`）
- 批量操作（`saveAll`, `deleteByIds`）
- 自定义查询方法

## ES 查询操作示例

### 基础查询
```java
// 查询单个
EsUserNoticePlan query = new EsUserNoticePlan();
query.setUserNoticeId("xxx");
List<EsUserNoticePlan> list = esUserNoticePlanService.getList(query);

// 通过 ID 查询
EsUserNoticePlan plan = esUserNoticePlanService.findById("id");

// 查询所有
List<EsUserNoticePlan> all = esUserNoticePlanService.getAll();
```

### 批量操作
```java
// 批量保存
List<EsUserNoticePlan> planList = ...;
esUserNoticePlanService.saveAll(planList);

// 批量删除
esUserNoticePlanService.deleteByIds(Arrays.asList("id1", "id2"));
```

### 自定义查询
```java
// 通过业务字段查询
List<EsUserNoticePlan> list = esUserNoticePlanService.getListByUserNoticeId("xxx");
```

## ES API 调用示例

### 查询 DSL
```json
{
  "query": {
    "bool": {
      "must": [
        { "match": { "userNoticeId": "xxx" } }
      ]
    }
  }
}
```

### 批量插入
```json
POST _bulk
{ "index": { "_index": "es_user_notice_plan" } }
{ "userNoticeId": "xxx", "account": "13800138000" }
```

## 注意事项

1. **ID 字段**：ES 文档使用 `id`（String 类型）作为唯一标识
2. **时间字段**：ES 中时间通常使用字符串或 Long 类型存储
3. **分页查询**：使用 `Page` 对象进行分页查询
4. **索引名称**：索引名通常与类名对应（驼峰转下划线）
5. **批量操作**：大量数据操作时使用 bulk API 提高性能
