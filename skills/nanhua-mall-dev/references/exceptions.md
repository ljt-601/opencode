# 异常处理规范

本文档说明南华积分商城项目的异常处理规范。

## 异常类型

### NestedBusinessException
自定义业务异常，封装错误码和错误信息。

### ResponseCode
错误码枚举，定义系统标准错误码。

## 常用错误码

```java
ERROR_PARAM        // 参数错误
ERROR_DATA         // 数据错误
ERROR_SYSTEM       // 系统错误
ERROR_LOGIN        // 登录错误
ERROR_AUTH         // 认证错误
ERROR_PERMISSION   // 权限错误
```

## 异常抛出规范

### 参数验证异常
```java
if (StringUtils.isBlank(userId)) {
  throw NestedBusinessException.build(ResponseCode.ERROR_PARAM);
}

if (order.getAmount().compareTo(BigDecimal.ZERO) < 0) {
  throw NestedBusinessException.build(ResponseCode.ERROR_PARAM);
}
```

### 业务规则异常
```java
if (order.getStatus().equals("1")) {
  throw NestedBusinessException.build("订单已支付，不能取消");
}

if (goodsNum < exchangeNum) {
  throw NestedBusinessException.build("库存不足");
}

if (userPoints < requiredPoints) {
  throw NestedBusinessException.build("积分不足");
}
```

### 数据不存在异常
```java
Order order = dao.findByOrderId(orderId);
if (order == null) {
  throw NestedBusinessException.build(ResponseCode.ERROR_DATA);
}
```

### 状态流转异常
```java
if (!isValidStatusChange(oldStatus, newStatus)) {
  throw NestedBusinessException.build("状态流转不合法");
}
```

## 异常捕获规范

### Controller 层异常捕获
```java
@ResponseBody
@RequestMapping(value = "/create", method = RequestMethod.POST)
public ApiModel<Order> create(@RequestBody Order order, HttpServletRequest request) {
  ApiModel<Order> model = ApiModel.buildFail();

  try {
    model = orderService.createOrder(order);
  } catch (NestedBusinessException e) {
    logger.error("order create error: {}", e.getMessage());
    model = ApiModel.buildFail(e.getMessage());
  } catch (Exception e) {
    logger.error("order create error", e);
    model = ApiModel.buildFail("系统异常");
  }

  return model;
}
```

### Service 层异常处理
```java
@Override
@Transactional(rollbackFor = Exception.class)
public ApiModel<Order> createOrder(Order order) throws Exception {
  // 业务逻辑
  if (StringUtils.isBlank(order.getUserId())) {
    throw NestedBusinessException.build(ResponseCode.ERROR_PARAM);
  }

  // 调用第三方接口可能抛出异常
  try {
    thirdPartyService.call(order);
  } catch (Exception e) {
    logger.error("call third party error", e);
    throw e; // 重新抛出，让事务回滚
  }
}
```

## 日志规范

### 错误日志
```java
// 必须记录完整的异常堆栈
logger.error("order create error", e);
logger.error("payment process error, orderId={}", orderId, e);
```

### 信息日志
```java
// 记录关键业务操作
logger.info("order created, orderId={}, userId={}", orderId, userId);
logger.info("points changed, userId={}, change={}, before={}, after={}", userId, change, before, after);
```

### 警告日志
```java
// 记录非关键异常
logger.warn("goods stock is low, goodsId={}, stock={}", goodsId, stock);
logger.warn("user points insufficient, userId={}, have={}, need={}", userId, have, need);
```

### 不要记录的信息
```java
// 不要记录敏感信息
// logger.error("password error: {}", password);  // 错误
// logger.error("id card error: {}", identityNo); // 错误
logger.error("login failed, userId={}", userId);  // 正确
```

## 事务回滚

### 使用 @Transactional 确保事务一致性
```java
@Override
@Transactional(rollbackFor = Exception.class)
public void updatePoints(String userId, BigDecimal change) {
  // 更新积分
  Account account = dao.findByUserId(userId);
  account.setPoints(account.getPoints().add(change));
  dao.update(account);

  // 记录流水
  PointsLog log = new PointsLog();
  log.setUserId(userId);
  log.setPointsChange(change);
  logDao.insert(log);

  // 如果这里抛出异常，整个事务会回滚
  if (account.getPoints().compareTo(BigDecimal.ZERO) < 0) {
    throw NestedBusinessException.build("积分不能为负");
  }
}
```

### 注意事项
1. 在 Service 层方法上使用 `@Transactional`
2. 明确指定 `rollbackFor = Exception.class`
3. 不要在 Controller 或 DAO 层使用事务
4. 抛出异常时确保事务能正确回滚

## 常见业务异常场景

### 用户相关
```java
// 用户不存在
if (user == null) {
  throw NestedBusinessException.build("用户不存在");
}

// 密码错误
if (!password.equals(user.getPassword())) {
  throw NestedBusinessException.build("密码错误");
}

// 账户已锁定
if (user.getLoginErrorCount() >= 5) {
  throw NestedBusinessException.build("账户已锁定，请联系客服");
}
```

### 商品相关
```java
// 商品不存在
if (goods == null) {
  throw NestedBusinessException.build("商品不存在");
}

// 商品已下架
if ("0".equals(goods.getStatus())) {
  throw NestedBusinessException.build("商品已下架");
}

// 库存不足
if (goods.getGoodsNum().compareTo(quantity) < 0) {
  throw NestedBusinessException.build("库存不足");
}

// 商品已过期
if (new Date().after(goods.getEndTime())) {
  throw NestedBusinessException.build("商品已过期");
}
```

### 订单相关
```java
// 订单不存在
if (order == null) {
  throw NestedBusinessException.build("订单不存在");
}

// 订单已支付
if ("2".equals(order.getStatus())) {
  throw NestedBusinessException.build("订单已支付，不能重复支付");
}

// 订单已取消
if ("90".equals(order.getStatus()) || "91".equals(order.getStatus())) {
  throw NestedBusinessException.build("订单已取消");
}

// 订单已过期
if (new Date().after(order.getExpireTime())) {
  throw NestedBusinessException.build("订单已过期");
}
```

### 积分相关
```java
// 积分不足
if (userPoints.compareTo(requiredPoints) < 0) {
  throw NestedBusinessException.build("积分不足");
}

// 积分变动异常
if (beforePoints.add(change).compareTo(afterPoints) != 0) {
  throw NestedBusinessException.build("积分变动异常");
}
```

### 支付相关
```java
// 支付金额异常
if (payAmount.compareTo(orderAmount) > 0) {
  throw NestedBusinessException.build("支付金额异常");
}

// 支付状态异常
if (!"1".equals(payStatus)) {
  throw NestedBusinessException.build("支付失败");
}
```

### 地址相关
```java
// 地址不存在
if (address == null) {
  throw NestedBusinessException.build("收货地址不存在");
}

// 不支持该地区
if (isSupportRegion(address.getProvince(), address.getCity())) {
  throw NestedBusinessException.build("不支持该地区配送");
}
```

## 异常处理最佳实践

### 1. 验证前置条件
```java
public void updateOrderStatus(String orderId, String newStatus) {
  // 参数验证
  if (StringUtils.isBlank(orderId) || StringUtils.isBlank(newStatus)) {
    throw NestedBusinessException.build(ResponseCode.ERROR_PARAM);
  }

  // 数据验证
  Order order = dao.findByOrderId(orderId);
  if (order == null) {
    throw NestedBusinessException.build(ResponseCode.ERROR_DATA);
  }

  // 业务规则验证
  if (!isValidStatusChange(order.getStatus(), newStatus)) {
    throw NestedBusinessException.build("状态流转不合法");
  }

  // 执行业务逻辑
  order.setStatus(newStatus);
  dao.update(order);
}
```

### 2. 提供友好的错误信息
```java
// 差的写法
throw NestedBusinessException.build("error");

// 好的写法
throw NestedBusinessException.build("积分不足，当前积分100，需要200积分");
```

### 3. 使用枚举定义错误码
```java
public enum OrderErrorCode {
  ORDER_NOT_FOUND("E001", "订单不存在"),
  ORDER_PAID("E002", "订单已支付"),
  ORDER_EXPIRED("E003", "订单已过期"),
  STOCK_INSUFFICIENT("E004", "库存不足");

  private String code;
  private String message;

  // ...
}
```

### 4. 统一异常处理
```java
@ControllerAdvice
public class GlobalExceptionHandler {

  @ExceptionHandler(NestedBusinessException.class)
  @ResponseBody
  public ApiModel<String> handleBusinessException(NestedBusinessException e) {
    logger.error("business exception: {}", e.getMessage());
    return ApiModel.buildFail(e.getMessage());
  }

  @ExceptionHandler(Exception.class)
  @ResponseBody
  public ApiModel<String> handleException(Exception e) {
    logger.error("system exception", e);
    return ApiModel.buildFail("系统异常");
  }
}
```
