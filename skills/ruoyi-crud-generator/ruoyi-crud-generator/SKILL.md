---
name: ruoyi-crud-generator
description: 若依框架CRUD代码自动生成器。基于南华积分商城项目的若依前后端框架，根据ES实体类或MySQL实体类自动生成完整的CRUD管理页面。交互式询问字段配置（列表展示、搜索字段、详情页面等），确认后自动生成：后端代码（Controller、Service、Mapper、Entity）、前端代码（Vue页面、API接口）、菜单管理SQL。适用于快速开发后台管理功能。触发条件：用户要求"生成管理页面"、"创建CRUD"、"生成增删改查"或提供实体类要求生成后台代码时使用。
---

# 若依CRUD代码生成器

## 概述

本技能提供基于若依框架的完整CRUD代码自动生成能力，适用于南华积分商城项目的后台管理系统快速开发。

## 快速开始

### 基本使用流程

**触发条件**：用户要求生成管理页面、CRUD功能，或提供实体类要求生成后台代码时自动触发。

```
用户: 帮我根据Goods实体类生成商品管理页面
→ 自动触发本技能
→ 交互式询问配置
→ 生成完整代码
```

### 核心工作流

```
1. 解析实体类 (ES Model 或 MySQL Entity)
   ↓
2. 交互式配置
   - 列表展示字段
   - 搜索字段
   - 表单字段
   - 详情页面配置
   ↓
3. 生成后端代码
   - Controller
   - Service接口和实现
   - Mapper接口和XML
   - Entity（如需要）
   ↓
4. 生成前端代码
   - Vue页面（列表、表单、详情）
   - API接口文件
   ↓
5. 生成菜单SQL
   - 菜单配置
   - 按钮权限
```

## 实体类解析

### ES实体类解析

**位置**: `six-modules/six-module-es/src/main/java/com/six/es/model/`

**解析规则**:
1. 类名 → 业务名（如 `GoodsModel` → `goods`）
2. 字段注解 `@FieldName` → 数据库列名
3. 字段类型 → Java类型和页面控件类型
4. 字段注释 → 显示标签

**示例**:
```java
@ESDocument(indexName = "goods_index")
public class GoodsModel extends BaseEsModel {
    @FieldName("goods_id")
    private String goodsId;

    @FieldName("goods_name")
    private String goodsName;

    @FieldName("price")
    private BigDecimal price;
}
```

### MySQL实体类解析

**位置**: `six-api/*/src/main/java/com/six/*/model/` 或 `six-modules/*/src/main/java/com/six/*/domain/`

**解析规则**:
1. 类名 → 业务名（如 `Banner` → `banner`）
2. `@Table` 注解 → 表名
3. `@Column` 注解 → 列名
4. 字段类型 → Java类型和页面控件类型
5. 字段注释 → 显示标签

**示例**:
```java
@Table(name = "t_banner")
public class Banner extends BaseModel {
    @Column(name = "banner_id")
    private String bannerId;

    @Column(name = "banner_title")
    private String bannerTitle;

    @Column(name = "banner_url")
    private String bannerUrl;
}
```

## 交互式配置

### 配置流程

解析实体类后，需要询问用户以下配置：

#### 1. 基本信息

```
请确认基本信息：
- 模块名（如：mall, system）
- 业务名（如：goods, banner）
- 功能名称（如：商品管理, 轮播图管理）
- 父菜单ID（默认为1，可在系统管理-菜单管理中查询）
```

#### 2. 列表展示字段

```
请选择列表页展示的列（从实体类字段中选择）：
示例字段：
- goodsId (商品ID)
- goodsName (商品名称)
- price (价格)
- stock (库存)
- createTime (创建时间)

默认行为：主键、名称、创建时间会自动选中
```

#### 3. 搜索字段配置

```
请选择搜索条件字段：
示例字段：
- goodsName (商品名称) - 模糊查询
- price (价格区间) - 范围查询
- status (状态) - 下拉选择

对于每个搜索字段，询问：
- 查询方式（EQ=精确, LIKE=模糊, BETWEEN=区间）
- 是否必填
```

#### 4. 表单字段配置

```
请选择表单中的字段：
示例字段：
- goodsName (商品名称) - input, 必填
- price (价格) - input, 必填
- description (描述) - textarea
- status (状态) - radio/select

对于每个表单字段，询问：
- 页面控件类型（input/textarea/select/radio/checkbox/datetime/upload）
- 是否必填
- 验证规则
- 字典类型（如需要）
```

#### 5. 详情页面配置

```
是否需要详情页面？
- 如需要：选择详情页展示的字段和布局
- 如不需要：使用弹窗查看详情
```

#### 6. 其他配置

```
- 是否启用树形结构
- 是否启用分页
- 是否需要导出功能
- 权限标识前缀（如：mall:goods）
```

## 代码生成规则

### 后端代码生成

**目录结构**:
```
six-bootstrap/six-admin/src/main/java/com/six/admin/
├── controller/{moduleName}/
│   └── {ClassName}Controller.java
├── service/{moduleName}/
│   ├── I{ClassName}Service.java
│   └── impl/{ClassName}ServiceImpl.java
├── dao/{moduleName}/
│   └── {ClassName}Dao.java
└── resources/mapper/{moduleName}/
    └── {ClassName}Mapper.xml
```

**生成规范**:
- 遵循 [nanhua-mall-dev](nanhua-mall-dev) 代码规范
- 2空格缩进
- 120字符行宽
- 中文注释
- 使用 `CollUtil.isEmpty()` 判断集合
- 使用 `StringUtils.isNotBlank()` 判断字符串
- 使用 `Conts` 常量替代硬编码分隔符
- 使用 `RedisConts` 常量替代硬编码Redis Key

**关键注解**:
- `@RestController`
- `@RequestMapping("/{moduleName}/{businessName}")`
- `@PreAuthorize("@ss.hasPermi('{module}:{business}:list')")`
- `@Log(title = "{功能名}", businessType = BusinessType.INSERT)`
- `@Transactional(rollbackFor = Exception.class)`

### 前端代码生成

**目录结构**:
```
nanhua-mall-ui/src/
├── api/{moduleName}/
│   └── {businessName}.js
└── views/{moduleName}/
    └── {businessName}/
        └── index.vue
```

**生成规范**:
- 使用若依Vue模板风格
- Element UI组件
- 标准CRUD操作按钮
- 分页组件
- 搜索表单
- 数据表格

**API接口**:
```javascript
import request from '@/utils/request'

// 查询列表
export function list{ClassName}(query) {
  return request({
    url: '/{moduleName}/{businessName}/list',
    method: 'get',
    params: query
  })
}

// 查询详情
export function get{ClassName}(id) {
  return request({
    url: '/{moduleName}/{businessName}/' + id,
    method: 'get'
  })
}

// 新增
export function add{ClassName}(data) {
  return request({
    url: '/{moduleName}/{businessName}',
    method: 'post',
    data: data
  })
}

// 修改
export function update{ClassName}(data) {
  return request({
    url: '/{moduleName}/{businessName}',
    method: 'put',
    data: data
  })
}

// 删除
export function del{ClassName}(id) {
  return request({
    url: '/{moduleName}/{businessName}/' + id,
    method: 'delete'
  })
}
```

### 菜单SQL生成

**SQL结构**:
```sql
-- 主菜单
INSERT INTO sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, remark)
VALUES ('{功能名称}', {parentMenuId}, {orderNum}, '{businessName}', '{moduleName}/{businessName}/index', 1, 0, 'C', '0', '0', '{moduleName}:{businessName}:list', '{icon}', 'admin', NOW(), '{功能名称}菜单');

-- 获取父菜单ID
SET @parentId = LAST_INSERT_ID();

-- 按钮
INSERT INTO sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, remark)
VALUES
('{功能名}查询', @parentId, 1, '#', '', 1, 0, 'F', '0', '0', '{moduleName}:{businessName}:query', '#', 'admin', NOW(), ''),
('{功能名}新增', @parentId, 2, '#', '', 1, 0, 'F', '0', '0', '{moduleName}:{businessName}:add', '#', 'admin', NOW(), ''),
('{功能名}修改', @parentId, 3, '#', '', 1, 0, 'F', '0', '0', '{moduleName}:{businessName}:edit', '#', 'admin', NOW(), ''),
('{功能名}删除', @parentId, 4, '#', '', 1, 0, 'F', '0', '0', '{moduleName}:{businessName}:remove', '#', 'admin', NOW(), ''),
('{功能名}导出', @parentId, 5, '#', '', 1, 0, 'F', '0', '0', '{moduleName}:{businessName}:export', '#', 'admin', NOW(), '');
```

## 字段类型映射

### Java类型 → 页面控件映射

| Java类型 | 默认控件 | 说明 |
|---------|---------|------|
| String | input | 文本输入框 |
| Integer/Long | input | 数字输入框 |
| BigDecimal | input | 金额输入框 |
| Date/LocalDate | datetime | 日期选择器 |
| LocalDateTime | datetime | 日期时间选择器 |
| Boolean | radio | 单选框（是/否） |

### 特殊字段识别

- `*_id`, `*Id` → 主键，隐藏字段
- `*_name`, `*Name` → 名称，input，必填
- `*_time`, `*Time`, `*Date` → 日期时间，datetime
- `status`, `*Status` → 状态，radio/select，字典类型
- `type`, `*Type` → 类型，radio/select，字典类型
- `*Desc`, `*Description`, `remark` → 描述，textarea
- `*Url`, `*Path`, `*Image`, `*File` → URL/路径，input或upload
- `content`, `*Content` → 内容，富文本编辑器

## 项目路径

### 后端项目
```
/Users/bryle/Public/WorkProject/nanhua-mall/six-parent/six-bootstrap/six-admin
```

### 前端项目
```
/Users/bryle/Public/WorkProject/nanhua-mall-ui
```

## 代码生成后操作

### 1. 代码校验

生成代码后，必须执行以下校验：

```bash
# 编译检查
cd /Users/bryle/Public/WorkProject/nanhua-mall/six-parent
mvn spotless:check -pl six-bootstrap/six-admin -am
```

### 2. 手动检查

- [ ] 缩进是否使用2空格
- [ ] 行宽是否超过120字符
- [ ] 命名是否符合规范
- [ ] 是否添加中文注释
- [ ] 分隔符是否使用Conts常量
- [ ] Redis Key是否使用RedisConts常量
- [ ] 是否使用CollUtil.isEmpty()判断集合
- [ ] 是否使用StringUtils.isNotBlank()判断字符串
- [ ] 金额是否使用BigDecimal
- [ ] 事务是否添加@Transactional
- [ ] 异常是否记录完整日志
- [ ] 大括号数量是否匹配

### 3. 数据库操作

如需要创建表或修改表结构，参考 [nanhua-database-ops](nanhua-database-ops) 技能。

### 4. 导入菜单SQL

```bash
# 登录数据库
mysql -h {host} -u {user} -p {database}

# 执行菜单SQL
source /path/to/menu.sql;
```

### 5. 刷新前端

```bash
cd /Users/bryle/Public/WorkProject/nanhua-mall-ui
npm run dev  # 或 npm run build
```

## 参考资源

### 若依框架
- [若依官方文档](http://doc.ruoyi.vip/)
- 代码生成模板位置：`/Users/bryle/Public/WorkProject/RuoYi-Vue/ruoyi-generator/src/main/resources/vm/`

### 南华项目
- [nanhua-mall-dev](nanhua-mall-dev) - 南华项目开发规范
- [nanhua-database-ops](nanhua-database-ops) - 数据库操作技能

### 参考模板
- [field-mapping.md](references/field-mapping.md) - 字段类型映射表
- [code-templates.md](references/code-templates.md) - 代码模板参考
- [database-connections.md](references/database-connections.md) - 数据库连接信息

## 最佳实践

### 1. 复用现有代码

在生成代码前，先查看项目中是否已有类似功能，参考其实现：
- 查找相同模块的Controller
- 参考已有的Service实现
- 复用公共工具类

### 2. 遵循项目规范

生成代码必须遵循南华项目规范：
- 使用2空格缩进
- 中文注释
- 使用Conts常量替代硬编码分隔符
- 使用RedisConts常量替代硬编码Redis Key

### 3. 分步验证

生成代码后，按以下步骤验证：
1. 编译检查
2. 启动后端服务
3. 访问前端页面
4. 测试CRUD功能
5. 检查权限控制

### 4. 安全考虑

- 所有接口必须添加权限注解
- 敏感操作记录操作日志
- 参数验证和异常处理
- SQL注入防护（使用MyBatis参数绑定）

## 常见问题

### Q1: 实体类找不到？

**A**: 检查实体类路径：
- ES实体类：`six-modules/six-module-es/src/main/java/com/six/es/model/`
- MySQL实体类：`six-api/*/src/main/java/com/six/*/model/`

### Q2: 生成的代码编译失败？

**A**: 检查：
- 依赖是否完整
- 包名是否正确
- 导入语句是否完整
- 运行 `mvn spotless:apply` 格式化代码

### Q3: 前端页面无法访问？

**A**: 检查：
- 菜单SQL是否导入
- 菜单路径是否正确
- 用户是否有权限
- 前端是否重新编译

### Q4: 数据库表不存在？

**A**: 参考 [nanhua-database-ops](nanhua-database-ops) 技能创建表结构。

## 技术栈

- **后端**: Spring Boot 2.7.13 + MyBatis + Dubbo 3.1.11
- **前端**: Vue2 + Element UI
- **数据库**: MySQL 5.1.34 + Elasticsearch
- **缓存**: Redis
- **工具库**: Hutool, Fastjson, Guava, Apache Commons
