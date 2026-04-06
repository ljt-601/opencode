# 数据库连接信息

## MySQL数据库连接

### 开发环境

```yaml
url: jdbc:mysql://localhost:3306/six_db?useUnicode=true&characterEncoding=utf8&zeroDateTimeBehavior=convertToNull&useSSL=true&serverTimezone=GMT%2B8
username: root
password: (请查看配置文件)
driver-class-name: com.mysql.cj.jdbc.Driver
```

### 配置文件位置

```
six-bootstrap/six-admin/src/main/resources/application-dev.yml
```

### 查询连接信息

```bash
# 查看开发环境配置
cat /Users/bryle/Public/WorkProject/nanhua-mall/six-parent/six-bootstrap/six-admin/src/main/resources/application-dev.yml | grep -A 5 "datasource"
```

## ES数据库连接

### 开发环境

```yaml
elasticsearch:
  rest:
    uris: http://localhost:9200
    username: (如有)
    password: (如有)
```

### 配置文件位置

```
six-bootstrap/six-admin/src/main/resources/application-dev.yml
```

## 数据库工具

### MySQL命令行

```bash
# 登录MySQL
mysql -h localhost -u root -p

# 选择数据库
use six_db;

# 查看表结构
show tables;
desc t_banner;

# 执行SQL文件
source /path/to/sql/file.sql;
```

### ES命令行

```bash
# 查看索引
curl -X GET "localhost:9200/_cat/indices?v"

# 查看索引结构
curl -X GET "localhost:9200/goods_index?pretty"

# 查询数据
curl -X GET "localhost:9200/goods_index/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": { "match_all": {} }
}
'
```

## 常用数据库表

### 商城模块表

| 表名 | 说明 | 实体类 |
|------|------|--------|
| t_banner | 轮播图 | Banner |
| t_goods | 商品 | Goods |
| t_goods_category | 商品分类 | GoodsCategory |
| t_order | 订单 | Order |
| t_order_goods | 订单商品 | OrderGoods |
| t_user | 用户 | User |

### 系统管理表

| 表名 | 说明 |
|------|------|
| sys_menu | 菜单表 |
| sys_user | 用户表 |
| sys_role | 角色表 |
| sys_dept | 部门表 |

## 数据库操作权限

执行数据库操作前，请确认：

1. **数据备份**: 修改数据前先备份
2. **测试环境**: 先在测试环境验证
3. **权限确认**: 确认有修改权限
4. **变更记录**: 重要变更记录到日志

## 参考技能

- [nanhua-database-ops](nanhua-database-ops) - 完整的数据库操作技能
- [nanhua-mall-dev](nanhua-mall-dev) - 南华项目开发技能
