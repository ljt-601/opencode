# 实体类规范

本文档提供实体类开发的规范和标准模板。

## 基础要求

- 所有实体类必须继承 `BaseModel`
- 主键类型: `String` (使用 `KeyGen.randomSeqNum()` 生成) 或 `Long`
- 金额字段使用 `BigDecimal`
- 时间字段使用 `Date` 或 `LocalDateTime`
- 使用 `@ApiModelProperty` 注解描述字段

## 数据库字段规范

### 表命名规范
- 表名前缀: `t_`
- 使用下划线分隔: `t_order`, `t_goods`, `t_banner`, `t_apply_order`

### 字段命名规范
- 使用下划线分隔: `order_id`, `goods_name`, `user_id`, `create_time`
- 主键字段: `id` (自增 Long) 或 `xxx_id` (String UUID)
- 统一审计字段:
  - `isvalid` (有效标识 0-无效 1-有效)
  - `create_time` (创建时间)
  - `create_by` (创建人)
  - `create_byer` (创建人姓名)
  - `update_time` (更新时间)
  - `update_by` (更新人)
  - `update_byer` (更新人姓名)

### 字段类型规范
- **主键**: `bigint` (自增) 或 `char(32)` (UUID)
- **字符串**: `varchar` (根据长度选择)
- **金额**: `decimal(19,2)` 或 `decimal(19,4)`
- **状态**: `char(1)` 或 `varchar(10)`
- **时间**: `datetime` 或 `timestamp`
- **文本**: `text`

## 标准实体类模板

### MySQL 数据库实体类模板

```java
package com.six.common.model;

import com.six.common.base.model.BaseModel;
import com.six.common.base.utils.KeyGen;
import io.swagger.annotations.ApiModelProperty;
import lombok.Data;
import lombok.EqualsAndHashCode;

/**
 * 用户触达统计表
 */
@EqualsAndHashCode(callSuper = true)
@Data
public class UserNoticeStat extends BaseModel {

    @ApiModelProperty(value = "用户触达统计ID")
    private String userNoticeStatId;

    @ApiModelProperty(value = "")
    private Long id;

    @ApiModelProperty(value = "用户触达ID")
    private String userNoticeId;

    @ApiModelProperty(value = "发送方式：1-短信 2-推送")
    private String sendType;

    @ApiModelProperty(value = "app名")
    private String appName;

    @ApiModelProperty(value = "app系统")
    private String appOs;

    @ApiModelProperty(value = "标题")
    private String title;

    @ApiModelProperty(value = "内容")
    private String content;

    @ApiModelProperty(value = "友盟ID")
    private String thirdId;

    @ApiModelProperty(value = "计划发送数")
    private Integer planCount;

    @ApiModelProperty(value = "实际发送数")
    private Integer sendCount;

    @ApiModelProperty(value = "实际点击数")
    private Integer clickCount;

    @Override
    public void initPrimaryKey() {
        this.setUserNoticeStatId(KeyGen.randomSeqNum());
    }
}
```

**MySQL 实体规范要点：**
1. 继承 `BaseModel`
2. 使用 Lombok 注解：`@Data`、`@EqualsAndHashCode(callSuper = true)`
3. 添加类注释：简要描述实体用途
4. 所有字段使用 `@ApiModelProperty` 注解说明
5. 重写 `initPrimaryKey()` 方法，使用 `KeyGen.randomSeqNum()` 生成主键
6. 主键字段命名：`xxxId` 格式（如 `userNoticeStatId`）
7. Long类型主键（自增）直接使用 `id` 字段

### ES 实体类模板

```java
package com.six.es.model;

import io.swagger.annotations.ApiModelProperty;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.elasticsearch.annotations.Document;
import org.springframework.data.elasticsearch.annotations.Field;
import org.springframework.data.elasticsearch.annotations.FieldType;

/**
 * 用户触达点击记录表
 */
@EqualsAndHashCode(callSuper = true)
@Data
@Document(indexName = "nh_user_notice_click", replicas = 2)//indexName 必须小写
public class EsUserNoticeClick extends EsBaseModel {
    private static final long serialVersionUID = -5181070661571389609L;

    @ApiModelProperty(value = "用户触达ID")
    @Field(type = FieldType.Keyword)
    private String userNoticeId;

    @ApiModelProperty(value = "发送方式：1-短信 2-推送")
    @Field(type = FieldType.Keyword)
    private String sendType;

    @ApiModelProperty(value = "app名")
    @Field(type = FieldType.Keyword)
    private String appName;

    @ApiModelProperty(value = "app系统")
    @Field(type = FieldType.Keyword)
    private String appOs;

    @ApiModelProperty(value = "点击账户")
    @Field(type = FieldType.Keyword)
    private String account;

    @ApiModelProperty(value = "用户ID")
    @Field(type = FieldType.Keyword)
    private String uid;
}
```

**ES 实体规范要点：**
1. 继承 `EsBaseModel`（包含 id、isvalid、createTime、updateTime）
2. 使用 Lombok 注解：`@Data`、`@EqualsAndHashCode(callSuper = true)`
3. 添加 `@Document` 注解：
   - `indexName`：索引名称（必须小写，建议使用 `nh_` 前缀）
   - `replicas`：副本数（建议 2）
4. 定义 `serialVersionUID` 常量
5. 所有字段使用 `@ApiModelProperty` 和 `@Field` 双重注解
6. `@Field` 注解指定类型：`FieldType.Keyword`（不分词，用于精确匹配）
7. 主键继承自 `EsBaseModel`，使用 `initPrimaryKey()` 方法生成
8. 字段类型选择：
   - `Keyword`：用于精确匹配、聚合、排序（不分词）
   - `Text`：用于全文搜索（分词）
   - `Date`：时间字段
   - `Integer/Long`：数值字段

## 核心业务实体

详细实体列表和字段说明请参考 [entities.md](entities.md)

### 订单相关
- `Order` - 订单主表
- `OrderGoods` - 订单商品关联
- `OrderPay` - 订单支付记录
- `OrderRefund` - 订单退款记录

### 商品相关
- `Goods` - 商品信息
- `GoodsCategory` - 商品分类

### 用户相关
- `CmsMember` - 会员信息
- `UserNotice` - 用户通知
- `UserNoticeStat` - 用户触达统计

### 申请相关
- `ApplyOrder` - 开户申请订单
- `ApplyFundUser` - 基金用户申请
- `ApplyCredentials` - 凭证信息

## 注意事项

### MySQL 实体注意事项
1. **主键生成**: 必须重写 `initPrimaryKey()` 方法，使用 `KeyGen.randomSeqNum()` 生成
2. **Lombok 优先**: 推荐使用 `@Data`、`@EqualsAndHashCode(callSuper = true)` 等注解，简化代码
3. **字符串 trim**: 如需手动编写 setter，使用 Lombok 时可不处理 trim，必要时在业务层处理
4. **时间格式**: 如需返回给前端，使用 `@JsonFormat` 注解格式化时间
5. **金额精度**: 使用 `BigDecimal` 避免精度丢失
6. **序列化**: 如使用 Lombok 可不显式定义 serialVersionUID，建议添加

### ES 实体注意事项
1. **索引命名**: 必须小写，使用下划线分隔，建议使用 `nh_` 项目前缀
2. **副本数**: 生产环境建议设置 `replicas = 2`
3. **字段类型选择**:
   - `Keyword`：用于精确匹配、聚合、排序、过滤（不分词）
   - `Text`：用于全文搜索、关键词检索（会分词）
   - `Date`：时间字段，需指定格式如 `pattern = "yyyy-MM-dd HH:mm:ss"`
4. **继承关系**: 必须继承 `EsBaseModel`，包含基础字段 id、isvalid、createTime、updateTime
5. **主键生成**: 使用 `initPrimaryKey()` 方法，由 `EsBaseModel` 提供
6. **双重注解**: 所有业务字段必须同时使用 `@ApiModelProperty` 和 `@Field` 注解
7. **serialVersionUID**: 必须定义私有静态常量
8. **字段映射**: ES 字段类型要匹配数据类型，避免类型转换错误
