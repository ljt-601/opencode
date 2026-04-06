# Controller 层规范

本文档提供 Controller 层开发的规范和标准模板。

## Controller 模板

```java
package com.six.web.controller.order;

import javax.servlet.http.HttpServletRequest;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;

import com.six.common.base.controller.BasicController;
import com.six.common.base.response.ApiModel;
import com.six.common.model.Order;
import com.six.service.order.OrderService;

import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;

@Api(tags = "订单管理")
@Controller
@RequestMapping({"/api/order"})
public class OrderApiController extends BasicController {

  @Autowired
  private OrderService orderService;

  @ResponseBody
  @ApiOperation(value = "订单列表", notes = "")
  @RequestMapping(value = "/getList", method = RequestMethod.POST)
  public ApiModel<Order> getList(@RequestBody Order order, HttpServletRequest request) {
    ApiModel<Order> model = ApiModel.buildFail();

    try {
      model = ApiModel.buildSuccess(orderService.getOrderList(order));
    } catch (Exception e) {
      logger.error("order getList error", e);
    }

    return model;
  }

  @ResponseBody
  @ApiOperation(value = "创建订单", notes = "")
  @RequestMapping(value = "/create", method = RequestMethod.POST)
  public ApiModel<Order> create(@RequestBody Order order, HttpServletRequest request) {
    ApiModel<Order> model = ApiModel.buildFail();

    try {
      model = orderService.createOrder(order);
    } catch (Exception e) {
      logger.error("order create error", e);
    }

    return model;
  }

  @ResponseBody
  @ApiOperation(value = "更新订单状态", notes = "")
  @RequestMapping(value = "/updateStatus", method = RequestMethod.POST)
  public ApiModel<String> updateStatus(@RequestBody Order order, HttpServletRequest request) {
    ApiModel<String> model = ApiModel.buildFail();

    try {
      orderService.updateOrderStatus(order.getOrderId(), order.getStatus());
      model = ApiModel.buildSuccess("更新成功");
    } catch (Exception e) {
      logger.error("order updateStatus error", e);
    }

    return model;
  }
}
```

## Controller 规范

- 使用 `@Controller` 注解
- 使用 `@RequestMapping` 定义路径
- 使用 `@ResponseBody` 返回 JSON
- 使用 `@ApiOperation` 文档化接口
- 返回统一的 `ApiModel` 对象
- 异常处理使用 try-catch 并记录日志
- Controller 继承 `BasicController` 获取通用方法（logger 等）

## 参数验证

### 基本验证

```java
if (StringUtils.isBlank(userId)) {
  return ApiModel.buildFail("用户ID不能为空");
}
```

### 对象验证

```java
if (order == null) {
  return ApiModel.buildFail("订单信息不能为空");
}
```

## 返回值封装

### 成功返回

```java
// 返回数据
return ApiModel.buildSuccess(data);

// 返回成功消息
return ApiModel.buildSuccess("操作成功", data);
```

### 失败返回

```java
// 失败（无消息）
return ApiModel.buildFail();

// 失败（带消息）
return ApiModel.buildFail("操作失败");
```

## 常用注解

### 路径映射

```java
@RequestMapping({"/api/order"})           // 模块路径
@RequestMapping(value = "/getList")         // 方法路径
@RequestMapping(value = "/{id}")           // 路径参数
```

### 请求方法

```java
@RequestMapping(method = RequestMethod.POST)   // POST
@RequestMapping(method = RequestMethod.GET)    // GET
@RequestMapping(method = RequestMethod.PUT)    // PUT
@RequestMapping(method = RequestMethod.DELETE) // DELETE
```

### 参数绑定

```java
@RequestBody Order order        // 请求体
@RequestParam String id         // 查询参数
@PathVariable String id         // 路径变量
```

## 异常处理

### 标准 try-catch 模式

```java
@ResponseBody
@ApiOperation(value = "操作", notes = "")
@RequestMapping(value = "/method", method = RequestMethod.POST)
public ApiModel<DataType> method(@RequestBody Entity entity, HttpServletRequest request) {
  ApiModel<DataType> model = ApiModel.buildFail();

  try {
    // 业务逻辑
    model = ApiModel.buildSuccess(result);
  } catch (Exception e) {
    logger.error("method error", e);
  }

  return model;
}
```

## 注意事项

1. **异常处理**: 必须使用 try-catch 捕获异常
2. **日志记录**: 异常需要记录完整堆栈信息
3. **返回封装**: 统一使用 `ApiModel` 封装返回值
4. **路径设计**: 模块路径 + 功能路径，避免冲突
5. **接口文档**: 使用 `@ApiOperation` 注解描述接口功能
