# 数据库设计参考

本文档说明南华积分商城项目的数据库设计规范。

## 数据库命名规范

### 表命名
- 表名前缀: `t_`
- 使用下划线分隔小写字母
- 示例: `t_order`, `t_goods`, `t_user`

### 字段命名
- 使用下划线分隔小写字母
- 主键字段: `id` (自增 bigint) 或 `xxx_id` (char(32))
- 外键字段: `xxx_id`
- 时间字段: `xxx_time`
- 状态字段: `status`
- 标识字段: `is_valid`, `is_default`

### 索引命名
- 普通索引: `idx_表名_字段名`
- 唯一索引: `uk_表名_字段名`
- 示例: `idx_order_user_id`, `uk_goods_code`

## 统一字段说明

所有业务表都包含以下审计字段：

| 字段名 | 类型 | 说明 | 默认值 |
|--------|------|------|--------|
| id | bigint | 主键 (自增) | AUTO_INCREMENT |
| isvalid | char(1) | 有效标识 0-无效 1-有效 | '1' |
| create_time | datetime | 创建时间 | CURRENT_TIMESTAMP |
| create_by | varchar(64) | 创建人ID | - |
| create_byer | varchar(64) | 创建人姓名 | - |
| update_time | datetime | 更新时间 | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP |
| update_by | varchar(64) | 更新人ID | - |
| update_byer | varchar(64) | 更新人姓名 | - |

## 字段类型规范

### 字符串类型
- `varchar(32)`: ID、编码等短字符串
- `varchar(64)`: 名称、描述等中等长度字符串
- `varchar(255)`: 长文本
- `text`: 超长文本
- `char(1)`: 状态、标识等单字符
- `char(32)`: UUID

### 数值类型
- `tinyint`: 0-255 的整数
- `int`: 普通整数
- `bigint`: 主键、大整数
- `decimal(19,2)`: 金额 (保留2位小数)
- `decimal(19,4)`: 积分 (保留4位小数)

### 时间类型
- `datetime`: 日期时间 (不自动更新)
- `timestamp`: 日期时间 (自动更新)

## 常用状态值说明

### 通用状态
```sql
-- isvalid 有效标识
'0' -- 无效
'1' -- 有效

-- status 状态
'0' -- 禁用/下架/初始化
'1' -- 启用/上架/待支付
'2' -- 成功/支付成功
'3' -- 失败/支付失败
'9' -- 完成/订单完成
```

### 订单状态
```sql
'0'  -- 初始化
'1'  -- 待支付
'2'  -- 支付成功
'3'  -- 支付失败
'4'  -- 待积分兑换
'5'  -- 兑换成功
'6'  -- 兑换失败
'9'  -- 订单完成
'90' -- 用户取消
'91' -- 系统取消
```

### 商品状态
```sql
'0' -- 下架
'1' -- 上架
```

### Banner类型
```sql
'1' -- 首页banner
'2' -- 底栏Banner
'3' -- 积分商城Banner
'4' -- 日报Banner
'5' -- 微信Banner
'6' -- APP启动屏
'7' -- 中栏
'8' -- 活动
```

### 跳转类型
```sql
'1' -- 产品页面
'2' -- 链接
'3' -- APP页面
```

### 订单类型
```sql
'A' -- 社区订单
'B' -- 积分商品兑换
'C' -- 商品订单
```

### 支付类型
```sql
'1' -- 支付
'2' -- 积分兑换
'3' -- 支付+积分兑换
```

## 表设计示例

### 订单表 (t_order)
```sql
CREATE TABLE `t_order` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `order_id` char(32) NOT NULL COMMENT '订单ID',
  `order_no` varchar(64) NOT NULL COMMENT '订单编号',
  `user_id` char(32) NOT NULL COMMENT '用户ID',
  `user_account` varchar(64) DEFAULT NULL COMMENT '用户账户',
  `user_nick_name` varchar(64) DEFAULT NULL COMMENT '用户昵称',
  `order_type` char(1) DEFAULT NULL COMMENT '订单类型 A-社区订单 B-积分商品兑换 C-商品订单',
  `order_amount` decimal(19,2) DEFAULT '0.00' COMMENT '订单金额',
  `pay_amount` decimal(19,2) DEFAULT '0.00' COMMENT '支付金额',
  `exchange_amount` decimal(19,4) DEFAULT '0.0000' COMMENT '兑换积分',
  `status` char(1) DEFAULT '0' COMMENT '状态 0-初始化 1-待支付 2-支付成功 3-支付失败 4-待积分兑换 5-兑换成功 6-兑换失败 9-订单完成 90-用户取消 91-系统取消',
  `order_pay_type` char(1) DEFAULT NULL COMMENT '支付类型 1-支付 2-积分兑换 3-支付+积分兑换',
  `apply_time` datetime DEFAULT NULL COMMENT '下单时间',
  `cancel_time` datetime DEFAULT NULL COMMENT '取消时间',
  `expire_time` datetime DEFAULT NULL COMMENT '失效时间',
  `client_no` varchar(64) DEFAULT NULL COMMENT '客户号',
  `client_name` varchar(64) DEFAULT NULL COMMENT '客户名',
  `order_name` varchar(255) DEFAULT NULL COMMENT '订单名称',
  `cancel_type` varchar(64) DEFAULT NULL COMMENT '取消类型',
  `cancel_reason` varchar(500) DEFAULT NULL COMMENT '取消原因',
  `user_remark` varchar(500) DEFAULT NULL COMMENT '用户备注',
  `isvalid` char(1) DEFAULT '1' COMMENT '有效标识',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `create_by` varchar(64) DEFAULT NULL COMMENT '创建人',
  `create_byer` varchar(64) DEFAULT NULL COMMENT '创建人姓名',
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `update_by` varchar(64) DEFAULT NULL COMMENT '更新人',
  `update_byer` varchar(64) DEFAULT NULL COMMENT '更新人姓名',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_order_id` (`order_id`),
  KEY `idx_order_no` (`order_no`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_status` (`status`),
  KEY `idx_create_time` (`create_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='订单表';
```

### 商品表 (t_goods)
```sql
CREATE TABLE `t_goods` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `goods_id` char(32) NOT NULL COMMENT '商品ID',
  `goods_code` varchar(64) DEFAULT NULL COMMENT '商品编码',
  `goods_name` varchar(255) NOT NULL COMMENT '商品名称',
  `goods_category_id` varchar(64) DEFAULT NULL COMMENT '商品分类ID',
  `goods_category_name` varchar(64) DEFAULT NULL COMMENT '商品分类名称',
  `goods_point` decimal(19,4) DEFAULT '0.0000' COMMENT '积分值',
  `origin_point` decimal(19,4) DEFAULT '0.0000' COMMENT '原积分',
  `price` decimal(19,2) DEFAULT '0.00' COMMENT '价格',
  `origin_price` decimal(19,2) DEFAULT '0.00' COMMENT '原价',
  `goods_num` decimal(19,4) DEFAULT '0.0000' COMMENT '库存数量',
  `exchange_num` decimal(19,4) DEFAULT '0.0000' COMMENT '已兑换数量',
  `begin_time` datetime DEFAULT NULL COMMENT '开始时间',
  `end_time` datetime DEFAULT NULL COMMENT '结束时间',
  `status` char(1) DEFAULT '0' COMMENT '状态 0-下架 1-上架',
  `sort_no` int(11) DEFAULT '0' COMMENT '排序',
  `recommend` char(1) DEFAULT '0' COMMENT '是否推荐 0-否 1-是',
  `icon_url` varchar(500) DEFAULT NULL COMMENT '图标URL',
  `picture_url` varchar(500) DEFAULT NULL COMMENT '图片URL',
  `goods_desc` varchar(500) DEFAULT NULL COMMENT '商品描述',
  `page_url` varchar(500) DEFAULT NULL COMMENT '详情页URL',
  `tag_one` int(11) DEFAULT '0' COMMENT '商品特殊属性 2-无需录入地址 4-增加录入第三方账号',
  `tags` varchar(255) DEFAULT NULL COMMENT '标签',
  `limit_num` int(11) DEFAULT '0' COMMENT '限购数量',
  `day_limit_num` int(11) DEFAULT '0' COMMENT '每日限购数量',
  `day_stat_time` varchar(64) DEFAULT NULL COMMENT '每日限购开始时间',
  `day_end_time` varchar(64) DEFAULT NULL COMMENT '每日限购结束时间',
  `isvalid` char(1) DEFAULT '1' COMMENT '有效标识',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `create_by` varchar(64) DEFAULT NULL COMMENT '创建人',
  `create_byer` varchar(64) DEFAULT NULL COMMENT '创建人姓名',
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `update_by` varchar(64) DEFAULT NULL COMMENT '更新人',
  `update_byer` varchar(64) DEFAULT NULL COMMENT '更新人姓名',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_goods_id` (`goods_id`),
  UNIQUE KEY `uk_goods_code` (`goods_code`),
  KEY `idx_category_id` (`goods_category_id`),
  KEY `idx_status` (`status`),
  KEY `idx_recommend` (`recommend`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品表';
```

### 用户表 (t_cms_member)
```sql
CREATE TABLE `t_cms_member` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `account` varchar(64) DEFAULT NULL COMMENT '账户',
  `password` varchar(255) DEFAULT NULL COMMENT '密码',
  `nick_name` varchar(64) DEFAULT NULL COMMENT '昵称',
  `account_type` int(11) DEFAULT '0' COMMENT '账户类型',
  `phone` varchar(20) DEFAULT NULL COMMENT '手机号',
  `email` varchar(64) DEFAULT NULL COMMENT '邮箱',
  `reg_time` varchar(32) DEFAULT NULL COMMENT '注册时间',
  `lst_upd_time` varchar(32) DEFAULT NULL COMMENT '最后更新时间',
  `state` int(11) DEFAULT '0' COMMENT '状态',
  `login_error_count` bigint(20) DEFAULT '0' COMMENT '登录错误次数',
  `client_no` varchar(64) DEFAULT NULL COMMENT '客户号',
  `identity_no` varchar(64) DEFAULT NULL COMMENT '身份证号',
  `client_name` varchar(64) DEFAULT NULL COMMENT '客户姓名',
  `head_img_url` varchar(500) DEFAULT NULL COMMENT '头像URL',
  `logintime` varchar(32) DEFAULT NULL COMMENT '登录时间',
  `loginip` varchar(64) DEFAULT NULL COMMENT '登录IP',
  `lstlogintime` varchar(32) DEFAULT NULL COMMENT '最后登录时间',
  `lstloginip` varchar(64) DEFAULT NULL COMMENT '最后登录IP',
  `open_id` varchar(64) DEFAULT NULL COMMENT '微信OpenID',
  `isvalid` char(1) DEFAULT '1' COMMENT '有效标识',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `create_by` varchar(64) DEFAULT NULL COMMENT '创建人',
  `create_byer` varchar(64) DEFAULT NULL COMMENT '创建人姓名',
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `update_by` varchar(64) DEFAULT NULL COMMENT '更新人',
  `update_byer` varchar(64) DEFAULT NULL COMMENT '更新人姓名',
  PRIMARY KEY (`id`),
  KEY `idx_account` (`account`),
  KEY `idx_phone` (`phone`),
  KEY `idx_client_no` (`client_no`),
  KEY `idx_open_id` (`open_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='会员表';
```

## 索引设计规范

### 主键索引
- 使用 `id` 自增主键
- 使用 `PRIMARY KEY` 约束

### 唯一索引
- 业务唯一字段使用 `UNIQUE KEY`
- 命名: `uk_表名_字段名`

### 普通索引
- 查询条件字段添加索引
- 命名: `idx_表名_字段名`

### 组合索引
- 多字段联合查询使用组合索引
- 遵循最左前缀原则

### 索引示例
```sql
-- 主键
PRIMARY KEY (`id`)

-- 唯一索引
UNIQUE KEY `uk_order_id` (`order_id`)
UNIQUE KEY `uk_goods_code` (`goods_code`)

-- 普通索引
KEY `idx_user_id` (`user_id`)
KEY `idx_status` (`status`)
KEY `idx_create_time` (`create_time`)

-- 组合索引
KEY `idx_user_status_time` (`user_id`, `status`, `create_time`)
```

## 数据库优化建议

### 1. 字段类型选择
- 能用 `varchar` 不用 `text`
- 能用 `decimal` 不用 `double`
- 能用 `int` 不用 `bigint`

### 2. 索引优化
- 避免在 `select *` 查询中使用索引
- 避免在索引列上使用函数
- 避免在索引列上进行计算

### 3. 查询优化
- 使用 `limit` 限制结果数量
- 避免深度分页
- 使用 `explain` 分析查询计划

### 4. 软删除
- 使用 `isvalid` 字段实现软删除
- 默认查询条件: `isvalid = '1'`

## 数据迁移规范

### 脚本命名
```
YYMMDD-developer.sql

示例:
240101-zhangsan.sql  # 2024年1月1日 张三提交的脚本
```

### 脚本内容
```sql
-- 1. 创建表
CREATE TABLE IF NOT EXISTS `t_example` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) DEFAULT NULL,
  `isvalid` char(1) DEFAULT '1',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='示例表';

-- 2. 添加字段
ALTER TABLE `t_order`
ADD COLUMN `new_field` varchar(64) DEFAULT NULL COMMENT '新字段'
AFTER `old_field`;

-- 3. 添加索引
ALTER TABLE `t_order`
ADD INDEX `idx_new_field` (`new_field`);

-- 4. 修改字段
ALTER TABLE `t_order`
MODIFY COLUMN `field_name` varchar(128) DEFAULT NULL COMMENT '字段说明';
```

### 注意事项
1. 脚本必须可重复执行
2. 使用 `IF NOT EXISTS` 避免重复创建
3. 每个脚本只做一件事
4. 添加注释说明修改内容
5. 脚本提交前在测试环境验证
