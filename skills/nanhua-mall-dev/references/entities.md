# 数据库实体参考

本文档列出南华积分商城项目的核心数据库实体及字段说明。

## 用户相关实体

### t_cms_member (会员表)
存储用户账户信息。

| 字段名 | 类型 | 说明 |
|--------|------|------|
| account | varchar | 账户 |
| password | varchar | 密码 |
| nick_name | varchar | 昵称 |
| account_type | int | 账户类型 |
| phone | varchar | 手机号 |
| email | varchar | 邮箱 |
| reg_time | varchar | 注册时间 |
| lst_upd_time | varchar | 最后更新时间 |
| state | int | 状态 |
| login_error_count | bigint | 登录错误次数 |
| client_no | varchar | 客户号 |
| identity_no | varchar | 身份证号 |
| client_name | varchar | 客户姓名 |
| head_img_url | varchar | 头像URL |
| logintime | varchar | 登录时间 |
| loginip | varchar | 登录IP |
| lstlogintime | varchar | 最后登录时间 |
| lstloginip | varchar | 最后登录IP |
| open_id | varchar | 微信OpenID |

## 商品相关实体

### t_goods (商品表)
存储积分商城商品信息。

| 字段名 | 类型 | 说明 |
|--------|------|------|
| goods_id | char(32) | 商品ID |
| goods_code | varchar | 商品编码 |
| goods_name | varchar | 商品名称 |
| goods_category_id | varchar | 商品分类ID |
| goods_category_name | varchar | 商品分类名称 |
| goods_point | decimal | 积分值 |
| origin_point | decimal | 原积分 |
| price | decimal | 价格 |
| origin_price | decimal | 原价 |
| goods_num | decimal | 库存数量 |
| exchange_num | decimal | 已兑换数量 |
| begin_time | datetime | 开始时间 |
| end_time | datetime | 结束时间 |
| status | char(1) | 状态 0-下架 1-上架 |
| sort_no | int | 排序 |
| recommend | char(1) | 是否推荐 0-否 1-是 |
| icon_url | varchar | 图标URL |
| picture_url | varchar | 图片URL |
| goods_desc | varchar | 商品描述 |
| page_url | varchar | 详情页URL |
| tag_one | int | 商品特殊属性 2-无需录入地址 4-增加录入第三方账号 |
| tags | varchar | 标签 |
| limit_num | int | 限购数量 |
| day_limit_num | int | 每日限购数量 |
| day_stat_time | varchar | 每日限购开始时间 |
| day_end_time | varchar | 每日限购结束时间 |

### t_goods_category (商品分类表)
存储商品分类信息。

| 字段名 | 类型 | 说明 |
|--------|------|------|
| category_id | char(32) | 分类ID |
| category_code | varchar | 分类编码 |
| category_name | varchar | 分类名称 |
| parent_id | char(32) | 父分类ID |
| level | int | 层级 |
| sort_no | int | 排序 |
| status | char(1) | 状态 |

## 订单相关实体

### t_order (订单表)
存储订单信息。

| 字段名 | 类型 | 说明 |
|--------|------|------|
| order_id | char(32) | 订单ID |
| order_no | varchar | 订单编号 |
| user_id | char(32) | 用户ID |
| user_account | varchar | 用户账户 |
| user_nick_name | varchar | 用户昵称 |
| order_type | varchar | 订单类型 A-社区订单 B-积分商品兑换 C-商品订单 |
| order_amount | decimal(19,2) | 订单金额 |
| pay_amount | decimal(19,2) | 支付金额 |
| exchange_amount | decimal(19,4) | 兑换积分 |
| status | char(1) | 状态 0-初始化 1-待支付 2-支付成功 3-支付失败 4-待积分兑换 5-兑换成功 6-兑换失败 9-订单完成 90-用户取消 91-系统取消 |
| order_pay_type | char(1) | 支付类型 1-支付 2-积分兑换 3-支付+积分兑换 |
| apply_time | datetime | 下单时间 |
| cancel_time | datetime | 取消时间 |
| expire_time | datetime | 失效时间 |
| client_no | varchar | 客户号 |
| client_name | varchar | 客户名 |
| order_name | varchar | 订单名称 |
| cancel_type | varchar | 取消类型 |
| cancel_reason | varchar | 取消原因 |
| user_remark | varchar | 用户备注 |

### t_order_item (订单明细表)
存储订单商品明细。

| 字段名 | 类型 | 说明 |
|--------|------|------|
| item_id | char(32) | 明细ID |
| order_id | char(32) | 订单ID |
| goods_id | char(32) | 商品ID |
| goods_code | varchar | 商品编码 |
| goods_name | varchar | 商品名称 |
| goods_price | decimal(19,2) | 商品价格 |
| goods_point | decimal | 商品积分 |
| quantity | int | 数量 |
| total_amount | decimal(19,2) | 总金额 |

## 内容相关实体

### t_banner (轮播图表)
存储轮播图信息。

| 字段名 | 类型 | 说明 |
|--------|------|------|
| banner_id | char(32) | BannerID |
| banner_type | char(1) | Banner类型 1-首页banner 2-底栏Banner 3-积分商城Banner 4-日报Banner 5-微信Banner 6-APP启动屏 7-中栏 8-活动 |
| banner_name | varchar | Banner名称 |
| image_path | varchar | 图片路径 |
| redirect_type | char(1) | 跳转类型 1-产品页面 2-链接 3-APP页面 |
| redirect_url | varchar | 跳转链接 |
| sort_no | int | 排序 |
| status | char(1) | 状态 0-禁用 1-启用 |
| rolling_flag | char(1) | 是否轮播 0-否 1-是 |
| banner_roll_interval | int | 轮播间隔 (秒) |
| web_site | char(1) | 站点 1-睿南华 2-横华国际 |
| app_env | varchar | APP环境 prd-生产环境 uat-测试环境 |
| app_name | varchar | APP名称 |
| open_rule | varchar | 开户规则 1-仅开户 0-仅未开户 无-所有 |

### t_article (文章表)
存储文章资讯信息。

| 字段名 | 类型 | 说明 |
|--------|------|------|
| article_id | char(32) | 文章ID |
| article_title | varchar | 文章标题 |
| article_content | text | 文章内容 |
| article_type | varchar | 文章类型 |
| cover_url | varchar | 封面图片URL |
| author | varchar | 作者 |
| publish_time | datetime | 发布时间 |
| view_count | int | 浏览次数 |
| status | char(1) | 状态 |

## 资金相关实体

### t_account (账户表)
存储用户账户资金信息。

| 字段名 | 类型 | 说明 |
|--------|------|------|
| account_id | char(32) | 账户ID |
| user_id | char(32) | 用户ID |
| client_no | varchar | 客户号 |
| total_points | decimal(19,4) | 总积分 |
| available_points | decimal(19,4) | 可用积分 |
| frozen_points | decimal(19,4) | 冻结积分 |
| total_balance | decimal(19,2) | 总余额 |
| available_balance | decimal(19,2) | 可用余额 |
| frozen_balance | decimal(19,2) | 冻结余额 |

### t_points_log (积分流水表)
存储积分变动记录。

| 字段名 | 类型 | 说明 |
|--------|------|------|
| log_id | char(32) | 流水ID |
| user_id | char(32) | 用户ID |
| client_no | varchar | 客户号 |
| points_change | decimal(19,4) | 积分变动 (+增加 -减少) |
| before_points | decimal(19,4) | 变动前积分 |
| after_points | decimal(19,4) | 变动后积分 |
| change_type | varchar | 变动类型 |
| change_desc | varchar | 变动说明 |
| order_id | char(32) | 关联订单ID |
| create_time | datetime | 创建时间 |

## 地址相关实体

### t_address (收货地址表)
存储用户收货地址。

| 字段名 | 类型 | 说明 |
|--------|------|------|
| address_id | char(32) | 地址ID |
| user_id | char(32) | 用户ID |
| receiver_name | varchar | 收货人姓名 |
| receiver_phone | varchar | 收货人手机号 |
| province | varchar | 省份 |
| province_name | varchar | 省份名称 |
| city | varchar | 城市 |
| city_name | varchar | 城市名称 |
| district | varchar | 区县 |
| district_name | varchar | 区县名称 |
| detail_address | varchar | 详细地址 |
| is_default | char(1) | 是否默认地址 0-否 1-是 |

## 优惠券相关实体

### t_coupon (优惠券表)
存储优惠券信息。

| 字段名 | 类型 | 说明 |
|--------|------|------|
| coupon_id | char(32) | 优惠券ID |
| coupon_code | varchar | 优惠券编码 |
| coupon_name | varchar | 优惠券名称 |
| coupon_type | varchar | 优惠券类型 |
| coupon_value | decimal | 优惠券面值 |
| min_amount | decimal | 最低消费金额 |
| begin_time | datetime | 开始时间 |
| end_time | datetime | 结束时间 |
| total_count | int | 总数量 |
| used_count | int | 已使用数量 |
| status | char(1) | 状态 |

### t_user_coupon (用户优惠券表)
存储用户领取的优惠券。

| 字段名 | 类型 | 说明 |
|--------|------|------|
| user_coupon_id | char(32) | 用户优惠券ID |
| user_id | char(32) | 用户ID |
| coupon_id | char(32) | 优惠券ID |
| coupon_code | varchar | 优惠券编码 |
| status | char(1) | 状态 0-未使用 1-已使用 2-已过期 |
| use_time | datetime | 使用时间 |
| order_id | char(32) | 订单ID |

## 活动相关实体

### t_activity (活动表)
存储营销活动信息。

| 字段名 | 类型 | 说明 |
|--------|------|------|
| activity_id | char(32) | 活动ID |
| activity_name | varchar | 活动名称 |
| activity_type | varchar | 活动类型 |
| activity_desc | varchar | 活动描述 |
| begin_time | datetime | 开始时间 |
| end_time | datetime | 结束时间 |
| status | char(1) | 状态 |

### t_activity_goods (活动商品表)
存储活动关联的商品。

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | bigint | 主键 |
| activity_id | char(32) | 活动ID |
| goods_id | char(32) | 商品ID |
| activity_price | decimal | 活动价格 |
| activity_points | decimal | 活动积分 |
| sort_no | int | 排序 |

## 统一字段说明

所有表都包含以下审计字段：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | bigint | 主键 (自增) |
| isvalid | char(1) | 有效标识 0-无效 1-有效 |
| create_time | datetime | 创建时间 |
| create_by | varchar | 创建人 |
| create_byer | varchar | 创建人姓名 |
| update_time | datetime | 更新时间 |
| update_by | varchar | 更新人 |
| update_byer | varchar | 更新人姓名 |
