# Service 层规范

本文档提供 Service 层开发的规范和标准模板。

## 接口定义规范

- 接口命名: 业务名 + Service
- 继承 `BaseService<实体类型>`
- 方法命名: find/get/save/update/delete 开头

## Service 接口模板

```java
package com.six.service.order;

import java.util.List;

import com.six.common.base.response.ApiModel;
import com.six.common.model.Order;
import com.six.core.orm.BaseService;

public interface OrderService extends BaseService<Order> {

  Order findLastByUserId(String userId);

  List<Order> getOrderList(Order order);

  ApiModel<Order> createOrder(Order order);

  void updateOrderStatus(String orderId, String status);

  void deleteOrder(String orderId);
}
```

## Service 实现规范

- 类命名: 接口名 + Impl
- 使用 `@Service` 注解
- 继承 `BaseServiceImpl<实体类型, DAO类型>`
- 使用 `@Transactional(rollbackFor = Exception.class)` 管理事务
- 使用 `@Autowired` 注入依赖

## Service 实现模板

```java
package com.six.service.order.impl;

import org.apache.commons.lang3.StringUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.six.common.base.response.ApiModel;
import com.six.common.base.response.ResponseCode;
import com.six.common.core.exception.NestedBusinessException;
import com.six.common.model.Order;
import com.six.core.orm.BaseServiceImpl;
import com.six.dao.OrderDao;
import com.six.service.order.OrderService;

@Service("orderService")
public class OrderServiceImpl extends BaseServiceImpl<Order, OrderDao> implements OrderService {

  @Autowired
  private UserService userService;

  @Override
  public Order findLastByUserId(String userId) {
    if (StringUtils.isBlank(userId)) {
      throw NestedBusinessException.build(ResponseCode.ERROR_PARAM);
    }
    return dao.findLastByUserId(userId);
  }

  @Override
  public List<Order> getOrderList(Order order) {
    return dao.getList(order);
  }

  @Override
  @Transactional(rollbackFor = Exception.class)
  public ApiModel<Order> createOrder(Order order) {
    ApiModel<Order> model = ApiModel.buildFail();

    try {
      order.initPrimaryKey();
      this.save(order);
      model = ApiModel.buildSuccess(order);
    } catch (Exception e) {
      logger.error("createOrder error", e);
    }

    return model;
  }

  @Override
  @Transactional(rollbackFor = Exception.class)
  public void updateOrderStatus(String orderId, String status) {
    if (StringUtils.isBlank(orderId) || StringUtils.isBlank(status)) {
      throw NestedBusinessException.build(ResponseCode.ERROR_PARAM);
    }

    Order order = new Order();
    order.setOrderId(orderId);
    order.setStatus(status);
    this.update(order);
  }

  @Override
  @Transactional(rollbackFor = Exception.class)
  public void deleteOrder(String orderId) {
    if (StringUtils.isBlank(orderId)) {
      throw NestedBusinessException.build(ResponseCode.ERROR_PARAM);
    }

    Order order = new Order();
    order.setOrderId(orderId);
    this.delete(order);
  }
}
```

## 事务管理

### 事务注解规范

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

## 业务逻辑模式

### 查询模式

```java
@Override
public Order findLastByUserId(String userId) {
  if (StringUtils.isBlank(userId)) {
    throw NestedBusinessException.build(ResponseCode.ERROR_PARAM);
  }
  return dao.findLastByUserId(userId);
}
```

### 创建模式

```java
@Override
@Transactional(rollbackFor = Exception.class)
public ApiModel<Order> createOrder(Order order) {
  ApiModel<Order> model = ApiModel.buildFail();

  try {
    order.initPrimaryKey();
    this.save(order);
    model = ApiModel.buildSuccess(order);
  } catch (Exception e) {
    logger.error("createOrder error", e);
  }

  return model;
}
```

### 更新模式

```java
@Override
@Transactional(rollbackFor = Exception.class)
public void updateOrderStatus(String orderId, String newStatus) {
  Order order = dao.findByOrderId(orderId);
  if (order == null) {
    throw NestedBusinessException.build(ResponseCode.ERROR_DATA);
  }

  // 验证状态流转
  if (!isValidStatusChange(order.getStatus(), newStatus)) {
    throw NestedBusinessException.build("状态流转不合法");
  }

  order.setStatus(newStatus);
  dao.update(order);
}
```

### 删除模式

```java
@Override
@Transactional(rollbackFor = Exception.class)
public void deleteOrder(String orderId) {
  if (StringUtils.isBlank(orderId)) {
    throw NestedBusinessException.build(ResponseCode.ERROR_PARAM);
  }

  Order order = new Order();
  order.setOrderId(orderId);
  this.delete(order);
}
```

## 注意事项

1. **异常处理**: 使用 `NestedBusinessException` 抛出业务异常
2. **参数验证**: Service 层进行参数验证
3. **日志记录**: 关键操作记录日志
4. **事务边界**: 一个事务方法完成一个完整的业务操作
5. **DAO 调用**: 通过继承的 `dao` 成员变量访问
