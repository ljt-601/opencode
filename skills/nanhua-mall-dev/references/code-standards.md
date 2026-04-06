# 代码规范

本文档提供南华积分商城项目的完整代码规范。

## 基础规范

- **缩进**: 2 空格
- **行宽**: 120 字符
- **编码**: UTF-8
- **注释**: 必须使用中文注释

## 命名规范

### 包命名 (小写字母，点分隔)

```java
com.six.web.controller.banner
com.six.service.order.service
com.six.mall.tzzx.mapper
```

### 类命名 (大驼峰 PascalCase)

```java
BannerApiController
OrderService
ApplyOrderServiceImpl
```

### 接口命名

```java
OrderService              // 业务名 + Service
IApplyOrderService        // I + 业务名 + Service (可选前缀)
BannerDao                 // 业务名 + Dao
```

### 实现类命名

```java
OrderServiceImpl          // 接口名 + Impl
ApplyOrderServiceImpl     // 接口名 + Impl
```

### Mapper XML 命名

```java
OrderMapper.xml
BannerMapper.xml
ApplyOrderMapper.xml
```

### VO/DTO 命名

```java
GoodsDetailVo             // 功能描述 + Vo
OrderQueryParam           // 功能描述 + Param
UserLoginResult           // 功能描述 + Result
```

### 方法命名 (动词开头，驼峰)

```java
findLastByUserId          // 查找最后一条记录
getGoodsList              // 获取商品列表
saveOrder                 // 保存订单
updateStatus              // 更新状态
deleteById                // 根据ID删除
```

### 变量命名 (驼峰)

```java
userId                    // 用户ID
goodsId                   // 商品ID
orderId                   // 订单ID
createTime                // 创建时间
status                    // 状态
```

### 常量命名 (全大写，下划线分隔)

```java
MAX_SIZE
DEFAULT_TIMEOUT
ORDER_STATUS_PENDING
```

## 导入顺序

1. JDK 标准库导入
2. 第三方库导入 (Spring、Apache Commons、Guava 等)
3. 项目内部导入 (com.six.*)
4. 静态导入

```java
import java.util.Date;
import java.util.List;

import org.apache.commons.lang3.StringUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.six.common.model.ApplyFundUser;
import com.six.core.orm.BaseService;
```

## 注释规范

### 类注释

```java
/**
 * 项目名称：six-web
 * 类名称：TestServiceTest
 * 类描述：服务测试类
 * 创建人：xuhui
 * 创建时间：2018年9月8日 下午9:37:12
 */
```

### 方法注释

使用 JavaDoc，包含参数和返回值说明：

```java
/**
 * 根据用户ID查找最新记录
 * @param userId 用户ID
 * @return 最新记录对象，如果不存在返回null
 */
public Order findLastByUserId(String userId) {
  // ...
}
```

### 字段注释

使用 `@ApiModelProperty` 注解：

```java
@ApiModelProperty(value = "用户ID")
private String userId;

@ApiModelProperty(value = "订单金额")
private BigDecimal amount;

@ApiModelProperty(value = "创建时间", dateFormat = "yyyy-MM-dd HH:mm:ss")
private Date createTime;
```
