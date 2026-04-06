# MySQL 表结构参考

本文档提供南华期货 MySQL 表结构的快速查找指南。

## 如何查找表结构

### 1. 通过 Mapper XML 查找

Mapper XML 文件位于：`six-bootstrap/*/src/main/resources/mapper/*.xml`

示例查找 UserNotice 表结构：
```bash
find /Users/bryle/Public/WorkProject/nanhua-mall -name "*UserNoticeMapper.xml"
```

### 2. 通过实体类查找

实体类位于：`six-api/*/src/main/java/com/six/*/model/*.java`

示例查找 UserNotice 实体：
```bash
find /Users/bryle/Public/WorkProject/nanhua-mall -name "UserNotice.java" -path "*/model/*"
```

### 3. 通过 Dao 接口查找

Dao 接口位于：`six-bootstrap/*/src/main/java/com/six/*/dao/*Dao.java`

示例查找 UserNoticeDao：
```bash
find /Users/bryle/Public/WorkProject/nanhua-mall -name "*UserNoticeDao.java"
```

## 常见表映射关系

| 表名 | Mapper XML | 实体类 | Dao 接口 | 模块 |
|------|-----------|--------|---------|------|
| UserNotice | UserNoticeMapper.xml | UserNotice.java | UserNoticeDao.java | six-module-mall |
| CmsMember | CmsMemberMapper.xml | CmsMember.java | CmsMemberDao.java | six-api-auth |
| Banner | BannerMapper.xml | Banner.java | BannerDao.java | six-module-admin |

## 表结构信息提取

从 Mapper XML 中提取的典型信息：
- 表名（通过 `from table_name`）
- 字段列表（`resultMap` 中的 `result` 标签）
- 主键（通常为 `id`）
- 索引（通过 `select * from table_name where id = #{id}` 推断）

从实体类中提取的典型信息：
- 字段名称和类型
- 字段注释（`@ApiModelProperty` 注解）
- 表注解（`@Table` 注解）

## 生成 SQL 示例

### 查询表结构
```sql
DESC table_name;
SHOW CREATE TABLE table_name;
```

### 查询索引
```sql
SHOW INDEX FROM table_name;
```

## 注意事项

1. **主键字段**：大多数表使用 `id`（Long 类型）作为主键
2. **业务主键**：部分表有业务主键（如 `userNoticeId`），使用 String 类型
3. **时间字段**：创建时间、更新时间通常使用 `Date` 类型
4. **逻辑删除**：部分表可能有 `delFlag` 字段标识删除状态
