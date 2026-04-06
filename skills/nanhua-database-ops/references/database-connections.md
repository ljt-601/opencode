# 数据库连接信息

本文档提供南华积分商城项目 MySQL 和 ES 数据库的连接信息。

## MySQL 连接信息

### 开发环境

**配置文件路径**: `six-bootstrap/six-web/src/main/resources/application-dev.yml`

```yaml
spring:
  datasource:
    url: jdbc:mysql://121.43.56.42:3306/nanhua_points?useUnicode=true&characterEncoding=utf8
    username: maxusc2bauth
    password: <YOUR_DEV_PASSWORD>
```

**连接信息**:
- 主机: 121.43.56.42
- 端口: 3306
- 数据库: nanhua_points
- 用户名: maxusc2bauth
- 密码: <YOUR_DEV_PASSWORD>

### UAT 环境

**配置文件路径**: `six-bootstrap/six-web/src/main/resources/application-uat.yml`

```yaml
spring:
  datasource:
    url: jdbc:mysql://10.151.92.39:3306/nhjfdb?useUnicode=true&characterEncoding=utf8
    username: mallTest
    password: <YOUR_UAT_PASSWORD>
```

**连接信息**:
- 主机: 10.151.92.39
- 端口: 3306
- 数据库: nhjfdb
- 用户名: mallTest
- 密码: <YOUR_UAT_PASSWORD>

## ES 连接信息

### 开发环境

**配置文件路径**: `six-common/six-common-elasticsearch/src/main/resources/application-elasticsearch-dev.yml`

```yaml
spring:
  elasticsearch:
    uris: 121.43.56.42:9292
    username: elastic
    password: <YOUR_ES_DEV_PASSWORD>
```

**连接信息**:
- 主机: 121.43.56.42
- 端口: 9292
- 用户名: elastic
- 密码: <YOUR_ES_DEV_PASSWORD>

### UAT 环境

**配置文件路径**: `six-common/six-common-elasticsearch/src/main/resources/application-elasticsearch-uat.yml`

```yaml
spring:
  elasticsearch:
    uris: 10.151.92.38:8080
```

**连接信息**:
- 主机: 10.151.92.38
- 端口: 8080
- 用户名: 无
- 密码: 无

## 使用方式

### 命令行连接

**MySQL 连接**:
```bash
# 开发环境
mysql -h 121.43.56.42 -P 3306 -u maxusc2bauth -p nanhua_points

# UAT 环境
mysql -h 10.151.92.39 -P 3306 -u mallTest -p nhjfdb
```

**ES 连接**:
```bash
# 开发环境
curl -u elastic:<YOUR_ES_DEV_PASSWORD> http://121.43.56.42:9292

# UAT 环境
curl http://10.151.92.38:8080
```

### 客户端连接

推荐使用以下客户端工具：
- MySQL: Navicat、DBeaver、MySQL Workbench
- ES: Kibana、ElasticHQ

## 其他环境配置

其他环境（pre、prd）的配置文件路径：
- `application-pre.yml` - 预发布环境
- `application-prd.yml` - 生产环境

**注意**: 生产环境连接信息需要单独获取，未包含在此文档中。

## 安全提示

1. **不要**将数据库密码提交到版本控制系统
2. **定期更换**数据库密码
3. **限制**数据库访问 IP 白名单
4. **记录**重要数据库变更操作
