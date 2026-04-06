# 常用模式

本文档提供开发中常用的模式和方法。

## 数据验证

### 字符串判断

```java
// 判断字符串是否为空
if (StringUtils.isBlank(userId)) {
  throw NestedBusinessException.build(ResponseCode.ERROR_PARAM);
}

// 判断字符串是否不为空
if (StringUtils.isNotBlank(userId)) {
  // 处理逻辑
}
```

### 集合判断

```java
// 判断集合是否为空
if (CollUtil.isEmpty(list)) {
  return new ArrayList<>();
}

// 判断集合是否不为空
if (CollUtil.isNotEmpty(list)) {
  // 处理逻辑
}
```

### 对象判断

```java
// 判断对象是否为空
if (entity == null) {
  return ApiModel.buildFail("对象不能为空");
}
```

### 多条件判断

```java
// 使用 && 判断多个条件
if (StringUtils.isNotBlank(userId) && StringUtils.isNotBlank(orderId)) {
  // 处理逻辑
}
```

## 异常处理

### 使用自定义异常

```java
// 抛出业务异常
if (StringUtils.isBlank(userId)) {
  throw NestedBusinessException.build(ResponseCode.ERROR_PARAM);
}
```

### 异常类型

- `NestedBusinessException`: 业务异常
- `ResponseCode.ERROR_PARAM`: 参数错误
- `ResponseCode.ERROR_DATA`: 数据错误
- `ResponseCode.ERROR_SYSTEM`: 系统错误
- `ResponseCode.ERROR_AUTH`: 认证失败
- `ResponseCode.ERROR_BUSINESS`: 业务错误

### 异常处理最佳实践

```java
try {
  // 业务逻辑
  return ApiModel.buildSuccess(data);
} catch (NestedBusinessException e) {
  // 业务异常，直接返回错误信息
  return ApiModel.buildFail(e.getMessage());
} catch (Exception e) {
  // 系统异常，记录日志
  logger.error("操作异常", e);
  return ApiModel.buildFail("系统异常");
}
```

## 事务管理

### Service 层事务注解

```java
@Override
@Transactional(rollbackFor = Exception.class)
public void deleteAndSave(String userName, ApplyFundUser t) {
  this.deleteByApplyFundAuthId(t);
  this.save(userName, t);
}
```

### 事务规范

- 在 Service 实现类方法上使用 `@Transactional` 注解
- 明确指定 `rollbackFor = Exception.class`
- 不要在 Controller 或 DAO 层使用事务
- 事务方法应该是 public 的
- 事务边界要合理，一个方法完成一个完整的业务操作

## 日志记录

### 使用 logger

```java
// 错误日志（记录堆栈）
logger.error("order getList error", e);

// 信息日志
logger.info("user login success, userId={}", userId);

// 调试日志
logger.debug("order status: {}", order.getStatus());
```

### 日志级别

- `logger.error`: 错误信息，记录完整堆栈
- `logger.info`: 关键业务操作
- `logger.debug`: 调试信息
- 不要在日志中输出敏感信息（密码、身份证号等）

### 日志最佳实践

```java
// ✅ 正确：使用占位符
logger.info("order created, userId={}, orderId={}", userId, orderId);

// ❌ 错误：字符串拼接
logger.info("order created, userId=" + userId + ", orderId=" + orderId);
```

## 金额计算

### 使用 BigDecimal

```java
// 金额计算
BigDecimal totalAmount = orderAmount.add(payAmount);

// 金额比较
if (payAmount.compareTo(BigDecimal.ZERO) > 0) {
  // 支付金额大于0
}

// 金额相减
BigDecimal balance = currentBalance.subtract(amount);

// 保留两位小数
BigDecimal amount = amount.setScale(2, BigDecimal.ROUND_HALF_UP);
```

### 金额格式化

```java
// 显示金额（保留2位小数）
String amountStr = amount.setScale(2, BigDecimal.ROUND_HALF_UP).toString();

// 转换为元
BigDecimal yuan = fen.divide(new BigDecimal(100));
```

## 时间处理

### 日期比较

```java
// 判断是否在有效期
if (new Date().before(order.getExpireTime())) {
  // 订单已过期
}

// 判断时间范围
if (order.getBeginTime() != null && order.getEndTime() != null) {
  Date now = new Date();
  if (now.after(order.getBeginTime()) && now.before(order.getEndTime())) {
    // 在有效期内
  }
}
```

### 时间计算

```java
// 日期格式化
String dateStr = DateUtils.formatDatetime(new Date());

// 日期解析
Date date = DateUtils.parse(dateStr);

// 计算时间差（毫秒）
long diff = endTime.getTime() - startTime.getTime();
```

## 主键生成

### 使用 KeyGen

```java
// 生成随机主键
String id = KeyGen.randomSeqNum();

// 在实体类中初始化主键
@Override
public void initPrimaryKey() {
  this.setEntityId(KeyGen.randomSeqNum());
}
```

## 集合操作

### 列表处理

```java
// 使用 stream 处理列表
List<String> accountList = accounts.stream()
    .map(String::trim)
    .filter(StringUtils::isNotBlank)
    .distinct()
    .collect(Collectors.toList());

// 按条件过滤
List<Order> paidOrders = orderList.stream()
    .filter(order -> "2".equals(order.getStatus()))
    .collect(Collectors.toList());

// 转换为 Map
Map<String, Order> orderMap = orderList.stream()
    .collect(Collectors.toMap(Order::getOrderId, order -> order));
```

### 去重

```java
// 字符串去重
List<String> distinctAccounts = accounts.stream()
    .distinct()
    .collect(Collectors.toList());

// 按属性去重
List<Order> distinctOrders = orderList.stream()
    .collect(Collectors.collectingAndThen(
        Collectors.toMap(Order::getOrderId, Function.identity(),
        Collectors.toList()
    ));
```

## 字符串处理

### 分割

```java
// 按逗号分割
String[] parts = str.split(Conts.SPLIT_COMMA_REG);

// 去除空字符串并 trim
List<String> list = Arrays.stream(str.split(","))
    .map(String::trim)
    .filter(StringUtils::isNotBlank)
    .collect(Collectors.toList());
```

### 拼接

```java
// 字符串拼接
String result = StrUtil.join("、", list1, list2);

// 格式化字符串
String message = String.format("用户%s的订单%s已创建", userName, orderId);
```

## 状态流转

### 状态验证

```java
// 验证状态流转合法性
private boolean isValidStatusChange(String currentStatus, String newStatus) {
  // 定义状态流转规则
  Map<String, List<String>> rules = new HashMap<>();
  rules.put("0", Arrays.asList("1", "2")); // 初始化 -> 待支付/审核通过
  rules.put("1", Arrays.asList("2", "90")); // 待支付 -> 完成/取消

  List<String> allowedStatus = rules.getOrDefault(currentStatus, new ArrayList<>());
  return allowedStatus.contains(newStatus);
}
```

### 状态更新

```java
// 更新状态
order.setStatus(newStatus);
dao.update(order);
```

## 注意事项

1. **NPE 防范**: 对可能为 null 的对象进行判空处理
2. **精度丢失**: 金额计算使用 `BigDecimal`，避免使用 `double` 或 `float`
3. **并发安全**: 集合操作考虑线程安全
4. **性能优化**: 使用 `stream()` 替代循环
5. **代码简洁**: 使用工具类方法（如 `CollUtil`、`StringUtils`）
