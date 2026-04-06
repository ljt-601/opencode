# 字段类型映射表

## Java类型 → 页面控件映射

### 基础类型

| Java类型 | 默认控件 | 查询方式 | 说明 |
|---------|---------|---------|------|
| String | input | LIKE | 文本输入框，默认模糊查询 |
| Integer | input | EQ | 数字输入框，精确查询 |
| Long | input | EQ | 长整型输入框，精确查询 |
| BigDecimal | input | BETWEEN | 金额输入框，范围查询 |
| Date | datetime | BETWEEN | 日期选择器，范围查询 |
| LocalDate | datetime | BETWEEN | 日期选择器，范围查询 |
| LocalDateTime | datetime | BETWEEN | 日期时间选择器，范围查询 |
| Boolean | radio | EQ | 单选框（是/否） |
| Enum | select | EQ | 下拉选择框 |

### 特殊类型

| Java类型 | 默认控件 | 说明 |
|---------|---------|------|
| List<String> | checkbox | 多选框 |
| Map<String, Object> | textarea | JSON文本域 |
| byte[] | upload | 文件上传 |

## 字段名模式识别

### 主键字段

| 模式 | 控件类型 | 是否必填 | 是否列表 | 是否查询 |
|------|---------|---------|---------|---------|
| `*_id`, `*Id` | input (隐藏) | 是 | 是 | EQ |

### 名称字段

| 模式 | 控件类型 | 是否必填 | 是否列表 | 是否查询 |
|------|---------|---------|---------|---------|
| `*_name`, `*Name`, `name` | input | 是 | 是 | LIKE |

### 时间字段

| 模式 | 控件类型 | 是否列表 | 查询方式 |
|------|---------|---------|---------|
| `*_time`, `*Time`, `*Date`, `create_time`, `update_time` | datetime | 是 | BETWEEN |

### 状态字段

| 模式 | 控件类型 | 字典类型 | 查询方式 |
|------|---------|---------|---------|
| `status`, `*Status`, `state` | select/radio | sys_normal_disable | EQ |

### 类型字段

| 模式 | 控件类型 | 字典类型 | 查询方式 |
|------|---------|---------|---------|
| `type`, `*Type` | select/radio | 自定义 | EQ |

### 描述字段

| 模式 | 控件类型 | 是否列表 | 查询方式 |
|------|---------|---------|---------|
| `*Desc`, `*Description`, `desc`, `description`, `remark` | textarea | 否（可配置） | LIKE |

### URL字段

| 模式 | 控件类型 | 说明 |
|------|---------|------|
| `*Url`, `*Path`, `url`, `path` | input | URL路径输入 |
| `*Image`, `*Img`, `image` | upload | 图片上传 |
| `*File`, `file` | upload | 文件上传 |

### 内容字段

| 模式 | 控件类型 | 说明 |
|------|---------|------|
| `content`, `*Content` | editor | 富文本编辑器 |
| `detail`, `*Detail` | textarea | 详细信息 |

### 排序字段

| 模式 | 控件类型 | 默认值 | 说明 |
|------|---------|--------|------|
| `order_num`, `sort`, `order` | input | 0 | 排序字段 |

## 页面控件详细说明

### input - 文本输入框

**适用场景**：短文本、数字、日期等

**属性配置**:
- `placeholder`: 占位符
- `maxlength`: 最大长度
- `disabled`: 是否禁用

**示例**:
```html
<el-input v-model="form.goodsName" placeholder="请输入商品名称" />
```

### textarea - 文本域

**适用场景**：长文本、描述、备注等

**属性配置**:
- `rows`: 行数（默认3）
- `maxlength`: 最大长度

**示例**:
```html
<el-input v-model="form.remark" type="textarea" :rows="3" placeholder="请输入备注" />
```

### select - 下拉选择

**适用场景**：枚举值、字典数据

**属性配置**:
- `multiple`: 是否多选
- `dictType`: 字典类型（若依系统）

**示例**:
```html
<el-select v-model="form.status" placeholder="请选择状态">
  <el-option label="正常" value="0" />
  <el-option label="停用" value="1" />
</el-select>
```

### radio - 单选框

**适用场景**：布尔值、互斥选项

**属性配置**:
- `dictType`: 字典类型（若依系统）

**示例**:
```html
<el-radio-group v-model="form.status">
  <el-radio label="0">正常</el-radio>
  <el-radio label="1">停用</el-radio>
</el-radio-group>
```

### checkbox - 复选框

**适用场景**：多选、标签等

**属性配置**:
- `dictType`: 字典类型（若依系统）

**示例**:
```html
<el-checkbox-group v-model="form.tags">
  <el-checkbox label="热销">热销</el-checkbox>
  <el-checkbox label="新品">新品</el-checkbox>
</el-checkbox-group>
```

### datetime - 日期时间选择器

**适用场景**：日期、时间选择

**属性配置**:
- `type`: date/time/datetime/datetimerange
- `format`: 格式化（yyyy-MM-dd HH:mm:ss）
- `value-format`: 值格式

**示例**:
```html
<el-date-picker
  v-model="form.createTime"
  type="datetime"
  placeholder="选择日期时间"
  value-format="yyyy-MM-dd HH:mm:ss"
/>
```

### upload - 文件上传

**适用场景**：图片、文件上传

**属性配置**:
- `action`: 上传地址
- `list-type`: 文件列表类型
- `accept`: 接受的文件类型

**示例**:
```html
<el-upload
  :action="uploadUrl"
  :headers="headers"
  :on-success="handleSuccess"
>
  <el-button size="small" type="primary">点击上传</el-button>
</el-upload>
```

### editor - 富文本编辑器

**适用场景**：文章内容、详情信息

**属性配置**:
- `min-height`: 最小高度
- `upload-url`: 图片上传地址

**示例**:
```html
<editor v-model="form.content" :min-height="300" />
```

## 查询方式说明

| 查询方式 | 代码 | 说明 | 适用场景 |
|---------|------|------|---------|
| 精确查询 | EQ | `=`, `!=` | ID、状态、类型等 |
| 模糊查询 | LIKE | `LIKE %value%` | 名称、描述等 |
| 左模糊 | LEFT_LIKE | `LIKE %value` | 手机号、编码等 |
| 右模糊 | RIGHT_LIKE | `LIKE value%` | 分类、前缀等 |
| 区间查询 | BETWEEN | `BETWEEN start AND end` | 金额、日期、数量等 |
| 大于 | GT | `>` | 金额、数量等 |
| 大于等于 | GTE | `>=` | 金额、数量等 |
| 小于 | LT | `<` | 金额、数量等 |
| 小于等于 | LTE | `<=` | 金额、数量等 |

## 字段属性配置

### 列表属性

```java
// 实体类字段
@Excel(name = "商品名称")
private String goodsName;

// GenTableColumn配置
genTableColumn.setIsList("1");  // 是否列表字段
genTableColumn.setIsQuery("1"); // 是否查询字段
genTableColumn.setQueryType("LIKE"); // 查询方式
```

### 表单属性

```java
// 实体类字段
@NotBlank(message = "商品名称不能为空")
@Size(max = 50, message = "商品名称长度不能超过50个字符")
private String goodsName;

// GenTableColumn配置
genTableColumn.setIsInsert("1"); // 是否插入字段
genTableColumn.setIsEdit("1");   // 是否编辑字段
genTableColumn.setIsRequired("1"); // 是否必填
genTableColumn.setHtmlType("input"); // 页面控件
genTableColumn.setDictType(""); // 字典类型（如需要）
```

## 常用字典类型

### 若依系统内置字典

| 字典类型 | 说明 | 选项 |
|---------|------|------|
| sys_normal_disable | 正常/停用 | 0=正常, 1=停用 |
| sys_show_hide | 显示/隐藏 | 0=显示, 1=隐藏 |
| sys_yes_no | 是/否 | Y=是, N=否 |
| sys_user_sex | 用户性别 | 0=男, 1=女, 2=未知 |
| sys_job_status | 岗位状态 | 0=正常, 1=停用 |

### 商城业务字典

| 字典类型 | 说明 |
|---------|------|
| mall_goods_status | 商品状态 |
| mall_order_status | 订单状态 |
| mall_payment_status | 支付状态 |
| mall_shipping_status | 物流状态 |
