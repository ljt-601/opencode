# API 接口文档参考

本文档说明南华积分商城项目的 API 接口开发规范。

## 接口规范

### 请求方式
- `GET`: 查询操作
- `POST`: 创建/更新操作
- `PUT`: 更新操作
- `DELETE`: 删除操作

### 请求路径规范
```
/api/{模块}/{操作}

示例:
/api/order/getList      # 订单列表
/api/order/create        # 创建订单
/api/order/updateStatus  # 更新订单状态
/api/goods/detail        # 商品详情
/api/user/addressList    # 用户地址列表
```

### 请求参数规范

#### 查询接口 (POST)
```java
@ResponseBody
@ApiOperation(value = "订单列表", notes = "")
@RequestMapping(value = "/getList", method = RequestMethod.POST)
public ApiModel<Order> getList(@RequestBody Order order, HttpServletRequest request) {
  // ...
}
```

**请求体 (JSON)**:
```json
{
  "orderId": "1234567890",
  "orderNo": "ORD20240101123456",
  "userId": "user001",
  "status": "1",
  "beginDate": "2024-01-01",
  "endDate": "2024-12-31"
}
```

#### 创建接口
```java
@ResponseBody
@ApiOperation(value = "创建订单", notes = "")
@RequestMapping(value = "/create", method = RequestMethod.POST)
public ApiModel<Order> create(@RequestBody Order order, HttpServletRequest request) {
  // ...
}
```

**请求体 (JSON)**:
```json
{
  "userId": "user001",
  "goodsId": "goods001",
  "quantity": 1,
  "addressId": "addr001",
  "couponId": "coupon001",
  "remark": "请尽快发货"
}
```

#### 更新接口
```java
@ResponseBody
@ApiOperation(value = "更新订单", notes = "")
@RequestMapping(value = "/update", method = RequestMethod.POST)
public ApiModel<Order> update(@RequestBody Order order, HttpServletRequest request) {
  // ...
}
```

**请求体 (JSON)**:
```json
{
  "orderId": "1234567890",
  "status": "2",
  "remark": "用户备注"
}
```

### 响应格式规范

#### 成功响应
```json
{
  "code": "200",
  "message": "success",
  "data": {
    "orderId": "1234567890",
    "orderNo": "ORD20240101123456",
    "status": "1",
    "orderAmount": 100.00,
    "createTime": "2024-01-01 12:00:00"
  }
}
```

#### 失败响应
```json
{
  "code": "500",
  "message": "库存不足",
  "data": null
}
```

#### 列表响应
```json
{
  "code": "200",
  "message": "success",
  "data": [
    {
      "orderId": "1234567890",
      "orderNo": "ORD20240101123456",
      "status": "1",
      "orderAmount": 100.00
    },
    {
      "orderId": "1234567891",
      "orderNo": "ORD20240101123457",
      "status": "2",
      "orderAmount": 200.00
    }
  ]
}
```

### 分页响应
```json
{
  "code": "200",
  "message": "success",
  "data": {
    "rows": [
      {
        "orderId": "1234567890",
        "orderNo": "ORD20240101123456"
      }
    ],
    "total": 100,
    "pageNum": 1,
    "pageSize": 10
  }
}
```

## 常用接口示例

### 订单相关接口

#### 1. 订单列表
**接口**: POST /api/order/getList

**请求**:
```json
{
  "userId": "user001",
  "status": "1",
  "beginDate": "2024-01-01",
  "endDate": "2024-12-31"
}
```

**响应**:
```json
{
  "code": "200",
  "message": "success",
  "data": [
    {
      "orderId": "1234567890",
      "orderNo": "ORD20240101123456",
      "userId": "user001",
      "userNickName": "张三",
      "orderType": "C",
      "orderAmount": 100.00,
      "payAmount": 0.00,
      "exchangeAmount": 1000.00,
      "status": "1",
      "statusName": "待支付",
      "orderPayType": "2",
      "applyTime": "2024-01-01 12:00:00",
      "createTime": "2024-01-01 12:00:00"
    }
  ]
}
```

#### 2. 创建订单
**接口**: POST /api/order/create

**请求**:
```json
{
  "userId": "user001",
  "goodsId": "goods001",
  "quantity": 1,
  "addressId": "addr001",
  "couponId": "coupon001",
  "remark": "请尽快发货"
}
```

**响应**:
```json
{
  "code": "200",
  "message": "success",
  "data": {
    "orderId": "1234567890",
    "orderNo": "ORD20240101123456",
    "orderAmount": 100.00,
    "payAmount": 0.00,
    "exchangeAmount": 1000.00,
    "status": "0",
    "statusName": "初始化"
  }
}
```

#### 3. 更新订单状态
**接口**: POST /api/order/updateStatus

**请求**:
```json
{
  "orderId": "1234567890",
  "status": "2"
}
```

**响应**:
```json
{
  "code": "200",
  "message": "success",
  "data": "更新成功"
}
```

#### 4. 取消订单
**接口**: POST /api/order/cancel

**请求**:
```json
{
  "orderId": "1234567890",
  "cancelReason": "不需要了"
}
```

**响应**:
```json
{
  "code": "200",
  "message": "success",
  "data": "取消成功"
}
```

### 商品相关接口

#### 1. 商品列表
**接口**: POST /api/goods/getList

**请求**:
```json
{
  "categoryId": "cat001",
  "status": "1",
  "recommend": "1",
  "keyword": "手机"
}
```

**响应**:
```json
{
  "code": "200",
  "message": "success",
  "data": [
    {
      "goodsId": "goods001",
      "goodsName": "iPhone 15",
      "goodsCode": "G001",
      "goodsCategoryName": "数码产品",
      "goodsPoint": 10000.00,
      "originPoint": 12000.00,
      "price": 6999.00,
      "originPrice": 7999.00,
      "goodsNum": 100.00,
      "exchangeNum": 50.00,
      "status": "1",
      "statusName": "上架",
      "recommend": "1",
      "iconUrl": "https://example.com/icon.jpg",
      "pictureUrl": "https://example.com/pic.jpg",
      "sortNo": 1
    }
  ]
}
```

#### 2. 商品详情
**接口**: POST /api/goods/detail

**请求**:
```json
{
  "goodsId": "goods001"
}
```

**响应**:
```json
{
  "code": "200",
  "message": "success",
  "data": {
    "goodsId": "goods001",
    "goodsName": "iPhone 15",
    "goodsCode": "G001",
    "goodsCategoryId": "cat001",
    "goodsCategoryName": "数码产品",
    "goodsPoint": 10000.00,
    "originPoint": 12000.00,
    "price": 6999.00,
    "originPrice": 7999.00,
    "goodsNum": 100.00,
    "exchangeNum": 50.00,
    "beginTime": "2024-01-01 00:00:00",
    "endTime": "2024-12-31 23:59:59",
    "status": "1",
    "statusName": "上架",
    "recommend": "1",
    "iconUrl": "https://example.com/icon.jpg",
    "pictureUrl": "https://example.com/pic.jpg",
    "goodsDesc": "苹果最新款手机",
    "pageUrl": "https://example.com/detail",
    "tags": "热销,新品",
    "limitNum": 5,
    "dayLimitNum": 1,
    "dayStatTime": "00:00",
    "dayEndTime": "23:59"
  }
}
```

### 用户相关接口

#### 1. 用户信息
**接口**: POST /api/user/info

**请求**:
```json
{
  "userId": "user001"
}
```

**响应**:
```json
{
  "code": "200",
  "message": "success",
  "data": {
    "userId": "user001",
    "account": "zhangsan",
    "nickName": "张三",
    "phone": "13800138000",
    "email": "zhangsan@example.com",
    "clientNo": "C001",
    "clientName": "张三",
    "headImgUrl": "https://example.com/avatar.jpg",
    "regTime": "2024-01-01 12:00:00"
  }
}
```

#### 2. 收货地址列表
**接口**: POST /api/user/addressList

**请求**:
```json
{
  "userId": "user001"
}
```

**响应**:
```json
{
  "code": "200",
  "message": "success",
  "data": [
    {
      "addressId": "addr001",
      "receiverName": "张三",
      "receiverPhone": "13800138000",
      "province": "广东省",
      "provinceName": "广东省",
      "city": "深圳市",
      "cityName": "深圳市",
      "district": "南山区",
      "districtName": "南山区",
      "detailAddress": "科技园南区1001号",
      "isDefault": "1"
    }
  ]
}
```

#### 3. 我的积分
**接口**: POST /api/user/points

**请求**:
```json
{
  "userId": "user001"
}
```

**响应**:
```json
{
  "code": "200",
  "message": "success",
  "data": {
    "totalPoints": 10000.00,
    "availablePoints": 8000.00,
    "frozenPoints": 2000.00
  }
}
```

### 轮播图相关接口

#### 1. 轮播图列表
**接口**: POST /api/banner/getList

**请求**:
```json
{
  "bannerType": "1",
  "status": "1",
  "webSite": "1"
}
```

**响应**:
```json
{
  "code": "200",
  "message": "success",
  "data": [
    {
      "bannerId": "banner001",
      "bannerType": "1",
      "bannerTypeName": "首页banner",
      "bannerName": "活动banner",
      "imageUrl": "https://example.com/banner.jpg",
      "redirectType": "2",
      "redirectTypeName": "链接",
      "redirectUrl": "https://example.com",
      "sortNo": 1,
      "status": "1",
      "statusName": "启用",
      "rollingFlag": "1",
      "bannerRollInterval": 5
    }
  ]
}
```

### 优惠券相关接口

#### 1. 可用优惠券列表
**接口**: POST /api/coupon/available

**请求**:
```json
{
  "userId": "user001",
  "orderId": "1234567890",
  "orderAmount": 100.00
}
```

**响应**:
```json
{
  "code": "200",
  "message": "success",
  "data": [
    {
      "userCouponId": "uc001",
      "couponId": "coupon001",
      "couponCode": "C001",
      "couponName": "满100减20",
      "couponType": "1",
      "couponValue": 20.00,
      "minAmount": 100.00,
      "status": "0",
      "statusName": "未使用"
    }
  ]
}
```

#### 2. 领取优惠券
**接口**: POST /api/coupon/receive

**请求**:
```json
{
  "userId": "user001",
  "couponId": "coupon001"
}
```

**响应**:
```json
{
  "code": "200",
  "message": "success",
  "data": "领取成功"
}
```

## API 文档工具

项目使用 Knife4j (Swagger 增强版) 生成 API 文档。

### 访问地址
- 开发环境: `http://localhost:8080/doc.html`
- 测试环境: `http://uat.example.com/doc.html`
- 生产环境: `http://prd.example.com/doc.html`

### 常用注解

#### @Api
描述接口类：
```java
@Api(tags = "订单管理")
public class OrderApiController extends BasicController {
  // ...
}
```

#### @ApiOperation
描述接口方法：
```java
@ApiOperation(value = "订单列表", notes = "查询用户订单列表")
public ApiModel<Order> getList(@RequestBody Order order, HttpServletRequest request) {
  // ...
}
```

#### @ApiModelProperty
描述参数字段：
```java
public class Order {
  @ApiModelProperty(value = "订单ID", required = true)
  private String orderId;

  @ApiModelProperty(value = "订单金额")
  private BigDecimal orderAmount;

  @ApiModelProperty(value = "状态 0-初始化 1-待支付 2-支付成功")
  private String status;
}
```

#### @ApiParam
描述单个参数：
```java
public ApiModel<Order> getOrder(
  @ApiParam(value = "订单ID", required = true) @RequestParam String orderId) {
  // ...
}
```

## 错误码说明

| 错误码 | 说明 |
|--------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 401 | 未认证 |
| 403 | 无权限 |
| 404 | 资源不存在 |
| 500 | 系统内部错误 |

## 注意事项

1. 所有接口统一使用 POST 请求
2. 请求体使用 JSON 格式
3. 响应体统一使用 ApiModel 封装
4. 时间格式: `yyyy-MM-dd HH:mm:ss`
5. 金额字段使用 `BigDecimal`，保留2位小数
6. 积分字段使用 `BigDecimal`，保留4位小数
7. 主键类型: `String` (32位UUID)
8. 状态字段: `String` 类型
9. 所有接口都需要记录日志
10. 敏感信息不要在响应中返回 (密码、身份证号等)
