# 代码模板参考

本文件提供基于若依框架的代码生成模板参考。

## 后端代码模板

### Controller模板

**文件路径**: `six-bootstrap/six-admin/src/main/java/com/six/admin/controller/{moduleName}/{ClassName}Controller.java`

```java
package com.six.admin.controller.{moduleName};

import java.util.List;
import javax.servlet.http.HttpServletResponse;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import com.six.common.annotation.Log;
import com.six.common.core.controller.BaseController;
import com.six.common.core.domain.AjaxResult;
import com.six.common.enums.BusinessType;
import com.six.common.utils.poi.ExcelUtil;
import com.six.common.utils.poi.ExcelUtil;
import com.six.common.core.page.TableDataInfo;
import com.six.admin.service.{moduleName}.I{ClassName}Service;
import com.six.api.{moduleName}.model.{ClassName};

/**
 * {functionName}Controller
 *
 * @author {author}
 * @date {date}
 */
@RestController
@RequestMapping("/{moduleName}/{businessName}")
public class {ClassName}Controller extends BaseController {

    @Autowired
    private I{ClassName}Service {className}Service;

    /**
     * 查询{functionName}列表
     */
    @PreAuthorize("@ss.hasPermi('{moduleName}:{businessName}:list')")
    @GetMapping("/list")
    public TableDataInfo list({ClassName} {className}) {
        startPage();
        List<{ClassName}> list = {className}Service.select{ClassName}List({className});
        return getDataTable(list);
    }

    /**
     * 导出{functionName}列表
     */
    @PreAuthorize("@ss.hasPermi('{moduleName}:{businessName}:export')")
    @Log(title = "{functionName}", businessType = BusinessType.EXPORT)
    @PostMapping("/export")
    public void export(HttpServletResponse response, {ClassName} {className}) {
        List<{ClassName}> list = {className}Service.select{ClassName}List({className});
        ExcelUtil<{ClassName}> util = new ExcelUtil<{ClassName}>({ClassName}.class);
        util.exportExcel(response, list, "{functionName}数据");
    }

    /**
     * 获取{functionName}详细信息
     */
    @PreAuthorize("@ss.hasPermi('{moduleName}:{businessName}:query')")
    @GetMapping(value = "/{pkColumn.javaField}")
    public AjaxResult getInfo(@PathVariable("{pkColumn.javaField}") {pkColumn.javaType} {pkColumn.javaField}) {
        return success({className}Service.select{ClassName}By{pkColumn.capJavaField}({pkColumn.javaField}));
    }

    /**
     * 新增{functionName}
     */
    @PreAuthorize("@ss.hasPermi('{moduleName}:{businessName}:add')")
    @Log(title = "{functionName}", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody {ClassName} {className}) {
        return toAjax({className}Service.insert{ClassName}({className}));
    }

    /**
     * 修改{functionName}
     */
    @PreAuthorize("@ss.hasPermi('{moduleName}:{businessName}:edit')")
    @Log(title = "{functionName}", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody {ClassName} {className}) {
        return toAjax({className}Service.update{ClassName}({className}));
    }

    /**
     * 删除{functionName}
     */
    @PreAuthorize("@ss.hasPermi('{moduleName}:{businessName}:remove')")
    @Log(title = "{functionName}", businessType = BusinessType.DELETE)
    @DeleteMapping("/{pkColumn.javaField}s")
    public AjaxResult remove(@PathVariable {pkColumn.javaType}[] {pkColumn.javaField}s) {
        return toAjax({className}Service.delete{ClassName}By{pkColumn.capJavaField}s({pkColumn.javaField}s));
    }
}
```

### Service接口模板

**文件路径**: `six-bootstrap/six-admin/src/main/java/com/six/admin/service/{moduleName}/I{ClassName}Service.java`

```java
package com.six.admin.service.{moduleName};

import java.util.List;
import com.six.api.{moduleName}.model.{ClassName};

/**
 * {functionName}Service接口
 *
 * @author {author}
 * @date {date}
 */
public interface I{ClassName}Service {

    /**
     * 查询{functionName}
     *
     * @param {pkColumn.javaField} {functionName}主键
     * @return {functionName}
     */
    public {ClassName} select{ClassName}By{pkColumn.capJavaField}({pkColumn.javaType} {pkColumn.javaField});

    /**
     * 查询{functionName}列表
     *
     * @param {className} {functionName}
     * @return {functionName}集合
     */
    public List<{ClassName}> select{ClassName}List({ClassName} {className});

    /**
     * 新增{functionName}
     *
     * @param {className} {functionName}
     * @return 结果
     */
    public int insert{ClassName}({ClassName} {className});

    /**
     * 修改{functionName}
     *
     * @param {className} {functionName}
     * @return 结果
     */
    public int update{ClassName}({ClassName} {className});

    /**
     * 批量删除{functionName}
     *
     * @param {pkColumn.javaField}s 需要删除的{functionName}主键集合
     * @return 结果
     */
    public int delete{ClassName}By{pkColumn.capJavaField}s({pkColumn.javaType}[] {pkColumn.javaField}s);

    /**
     * 删除{functionName}信息
     *
     * @param {pkColumn.javaField} {functionName}主键
     * @return 结果
     */
    public int delete{ClassName}By{pkColumn.capJavaField}({pkColumn.javaType} {pkColumn.javaField});
}
```

### Service实现模板

**文件路径**: `six-bootstrap/six-admin/src/main/java/com/six/admin/service/{moduleName}/impl/{ClassName}ServiceImpl.java`

```java
package com.six.admin.service.{moduleName}.impl;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import com.six.api.{moduleName}.model.{ClassName};
import com.six.admin.dao.{moduleName}.{ClassName}Dao;
import com.six.admin.service.{moduleName}.I{ClassName}Service;

/**
 * {functionName}Service业务层处理
 *
 * @author {author}
 * @date {date}
 */
@Service
public class {ClassName}ServiceImpl implements I{ClassName}Service {

    @Autowired
    private {ClassName}Dao {className}Dao;

    /**
     * 查询{functionName}
     *
     * @param {pkColumn.javaField} {functionName}主键
     * @return {functionName}
     */
    @Override
    public {ClassName} select{ClassName}By{pkColumn.capJavaField}({pkColumn.javaType} {pkColumn.javaField}) {
        return {className}Dao.select{ClassName}By{pkColumn.capJavaField}({pkColumn.javaField});
    }

    /**
     * 查询{functionName}列表
     *
     * @param {className} {functionName}
     * @return {functionName}
     */
    @Override
    public List<{ClassName}> select{ClassName}List({ClassName} {className}) {
        return {className}Dao.select{ClassName}List({className});
    }

    /**
     * 新增{functionName}
     *
     * @param {className} {functionName}
     * @return 结果
     */
    @Transactional(rollbackFor = Exception.class)
    @Override
    public int insert{ClassName}({ClassName} {className}) {
        // 生成主键
        {className}.set{pkColumn.capJavaField}(KeyGen.randomSeqNum());
        {className}.setCreateTime(new Date());
        return {className}Dao.insert{ClassName}({className});
    }

    /**
     * 修改{functionName}
     *
     * @param {className} {functionName}
     * @return 结果
     */
    @Transactional(rollbackFor = Exception.class)
    @Override
    public int update{ClassName}({ClassName} {className}) {
        {className}.setUpdateTime(new Date());
        return {className}Dao.update{ClassName}({className});
    }

    /**
     * 批量删除{functionName}
     *
     * @param {pkColumn.javaField}s 需要删除的{functionName}主键
     * @return 结果
     */
    @Transactional(rollbackFor = Exception.class)
    @Override
    public int delete{ClassName}By{pkColumn.capJavaField}s({pkColumn.javaType}[] {pkColumn.javaField}s) {
        return {className}Dao.delete{ClassName}By{pkColumn.capJavaField}s({pkColumn.javaField}s);
    }

    /**
     * 删除{functionName}信息
     *
     * @param {pkColumn.javaField} {functionName}主键
     * @return 结果
     */
    @Transactional(rollbackFor = Exception.class)
    @Override
    public int delete{ClassName}By{pkColumn.capJavaField}({pkColumn.javaType} {pkColumn.javaField}) {
        return {className}Dao.delete{ClassName}By{pkColumn.capJavaField}({pkColumn.javaField});
    }
}
```

### Mapper接口模板

**文件路径**: `six-bootstrap/six-admin/src/main/java/com/six/admin/dao/{moduleName}/{ClassName}Dao.java`

```java
package com.six.admin.dao.{moduleName};

import java.util.List;
import com.six.api.{moduleName}.model.{ClassName};

/**
 * {functionName}Mapper接口
 *
 * @author {author}
 * @date {date}
 */
public interface {ClassName}Dao {

    /**
     * 查询{functionName}
     *
     * @param {pkColumn.javaField} {functionName}主键
     * @return {functionName}
     */
    public {ClassName} select{ClassName}By{pkColumn.capJavaField}({pkColumn.javaType} {pkColumn.javaField});

    /**
     * 查询{functionName}列表
     *
     * @param {className} {functionName}
     * @return {functionName}集合
     */
    public List<{ClassName}> select{ClassName}List({ClassName} {className});

    /**
     * 新增{functionName}
     *
     * @param {className} {functionName}
     * @return 结果
     */
    public int insert{ClassName}({ClassName} {className});

    /**
     * 修改{functionName}
     *
     * @param {className} {functionName}
     * @return 结果
     */
    public int update{ClassName}({ClassName} {className});

    /**
     * 删除{functionName}
     *
     * @param {pkColumn.javaField} {functionName}主键
     * @return 结果
     */
    public int delete{ClassName}By{pkColumn.capJavaField}({pkColumn.javaType} {pkColumn.javaField});

    /**
     * 批量删除{functionName}
     *
     * @param {pkColumn.javaField}s 需要删除的数据主键集合
     * @return 结果
     */
    public int delete{ClassName}By{pkColumn.capJavaField}s({pkColumn.javaType}[] {pkColumn.javaField}s);
}
```

### Mapper XML模板

**文件路径**: `six-bootstrap/six-admin/src/main/resources/mapper/{moduleName}/{ClassName}Mapper.xml`

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE mapper
PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
"http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="{packageName}.dao.{moduleName}.{ClassName}Dao">

    <resultMap type="{packageName}.{moduleName}.model.{ClassName}" id="{ClassName}Result">
#foreach ($column in $columns)
#if ($column.isPk)
        <id property="${column.javaField}" column="${column.columnName}" />
#else
        <result property="${column.javaField}" column="${column.columnName}" />
#end
#end
    </resultMap>

    <sql id="select{ClassName}Vo">
        select#foreach ($column in $columns) ${column.columnName}#if($foreach.hasNext),#end#end from ${tableName}
    </sql>

    <select id="select{ClassName}List" parameterType="{packageName}.{moduleName}.model.{ClassName}" resultMap="{ClassName}Result">
        <include refid="select{ClassName}Vo"/>
        <where>
#foreach ($column in $columns)
#if ($column.isQuery)
            <if test="$column.javaField != null#if($column.javaType == 'String') and $column.javaField != ''#end">
                AND ${column.columnName} = #{$column.javaField}
            </if>
#end
#end
        </where>
    </select>

    <select id="select{ClassName}By{pkColumn.capJavaField}" parameterType="${pkColumn.javaType}" resultMap="{ClassName}Result">
        <include refid="select{ClassName}Vo"/>
        where ${pkColumn.columnName} = #{$pkColumn.javaField}
    </select>

    <insert id="insert{ClassName}" parameterType="{packageName}.{moduleName}.model.{ClassName}" useGeneratedKeys="true" keyProperty="$pkColumn.javaField">
        insert into ${tableName}
        <trim prefix="(" suffix=")" suffixOverrides=",">
#foreach ($column in $columns)
#if ($column.isInsert)
            <if test="$column.javaField != null#if($column.javaType == 'String') and $column.javaField != ''#end">
                ${column.columnName},
            </if>
#end
#end
        </trim>
        <trim prefix="values (" suffix=")" suffixOverrides=",">
#foreach ($column in $columns)
#if ($column.isInsert)
            <if test="$column.javaField != null#if($column.javaType == 'String') and $column.javaField != ''#end">
                #{$column.javaField,jdbcType=$column.jdbcType},
            </if>
#end
#end
        </trim>
    </insert>

    <update id="update{ClassName}" parameterType="{packageName}.{moduleName}.model.{ClassName}">
        update ${tableName}
        <trim prefix="SET" suffixOverrides=",">
#foreach ($column in $columns)
#if ($column.isEdit)
            <if test="$column.javaField != null">
                ${column.columnName} = #{$column.javaField,jdbcType=$column.jdbcType},
            </if>
#end
#end
        </trim>
        where ${pkColumn.columnName} = #{$pkColumn.javaField}
    </update>

    <delete id="delete{ClassName}By{pkColumn.capJavaField}" parameterType="${pkColumn.javaType}">
        delete from ${tableName} where ${pkColumn.columnName} = #{$pkColumn.javaField}
    </delete>

    <delete id="delete{ClassName}By{pkColumn.capJavaField}s" parameterType="${pkColumn.javaType}">
        delete from ${tableName} where ${pkColumn.columnName} in
        <foreach item="$pkColumn.javaField" collection="array" open="(" separator="," close=")">
            #{$pkColumn.javaField}
        </foreach>
    </delete>
</mapper>
```

## 前端代码模板

### API接口模板

**文件路径**: `nanhua-mall-ui/src/api/{moduleName}/{businessName}.js`

```javascript
import request from '@/utils/request'

// 查询{functionName}列表
export function list{ClassName}(query) {
  return request({
    url: '/{moduleName}/{businessName}/list',
    method: 'get',
    params: query
  })
}

// 查询{functionName}详细
export function get{ClassName}({pkColumn.javaField}) {
  return request({
    url: '/{moduleName}/{businessName}/' + {pkColumn.javaField},
    method: 'get'
  })
}

// 新增{functionName}
export function add{ClassName}(data) {
  return request({
    url: '/{moduleName}/{businessName}',
    method: 'post',
    data: data
  })
}

// 修改{functionName}
export function update{ClassName}(data) {
  return request({
    url: '/{moduleName}/{businessName}',
    method: 'put',
    data: data
  })
}

// 删除{functionName}
export function del{ClassName}({pkColumn.javaField}) {
  return request({
    url: '/{moduleName}/{businessName}/' + {pkColumn.javaField},
    method: 'delete'
  })
}

// 导出{functionName}
export function export{ClassName}(query) {
  return request({
    url: '/{moduleName}/{businessName}/export',
    method: 'post',
    params: query
  })
}
```

### Vue页面模板

**文件路径**: `nanhua-mall-ui/src/views/{moduleName}/{businessName}/index.vue`

```vue
<template>
  <div class="app-container">
    <!-- 搜索表单 -->
    <el-form :model="queryParams" ref="queryForm" size="small" :inline="true" v-show="showSearch">
#foreach ($column in $columns)
#if ($column.isQuery)
      <el-form-item label="${column.columnComment}" prop="$column.javaField">
#set($htmlType = $column.htmlType)
#if ($htmlType == 'input')
        <el-input
          v-model="queryParams.$column.javaField"
          placeholder="请输入${column.columnComment}"
          clearable
          @keyup.enter.native="handleQuery"
        />
#elseif ($htmlType == 'select')
        <el-select v-model="queryParams.$column.javaField" placeholder="请选择${column.columnComment}" clearable>
          <el-option label="请选择字典生成" value="" />
        </el-select>
#elseif ($htmlType == 'datetime')
        <el-date-picker
          v-model="queryParams.$column.javaField"
          type="date"
          placeholder="选择${column.columnComment}"
          value-format="yyyy-MM-dd"
        />
#end
      </el-form-item>
#end
#end
      <el-form-item>
        <el-button type="primary" icon="el-icon-search" size="mini" @click="handleQuery">搜索</el-button>
        <el-button icon="el-icon-refresh" size="mini" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <!-- 操作按钮 -->
    <el-row :gutter="10" class="mb8">
      <el-col :span="1.5">
        <el-button
          type="primary"
          plain
          icon="el-icon-plus"
          size="mini"
          @click="handleAdd"
          v-hasPermi="['{moduleName}:{businessName}:add']"
        >新增</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="danger"
          plain
          icon="el-icon-delete"
          size="mini"
          :disabled="multiple"
          @click="handleDelete"
          v-hasPermi="['{moduleName}:{businessName}:remove']"
        >删除</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="warning"
          plain
          icon="el-icon-download"
          size="mini"
          @click="handleExport"
          v-hasPermi="['{moduleName}:{businessName}:export']"
        >导出</el-button>
      </el-col>
      <right-toolbar :showSearch.sync="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <!-- 数据表格 -->
    <el-table v-loading="loading" :data="{className}List" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
#foreach ($column in $columns)
#if ($column.isList)
      <el-table-column label="${column.columnComment}" align="center" prop="$column.javaField" />
#end
#end
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template slot-scope="scope">
          <el-button
            size="mini"
            type="text"
            icon="el-icon-edit"
            @click="handleUpdate(scope.row)"
            v-hasPermi="['{moduleName}:{businessName}:edit']"
          >修改</el-button>
          <el-button
            size="mini"
            type="text"
            icon="el-icon-delete"
            @click="handleDelete(scope.row)"
            v-hasPermi="['{moduleName}:{businessName}:remove']"
          >删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <pagination
      v-show="total>0"
      :total="total"
      :page.sync="queryParams.pageNum"
      :limit.sync="queryParams.pageSize"
      @pagination="getList"
    />

    <!-- 添加或修改对话框 -->
    <el-dialog :title="title" :visible.sync="open" width="500px" append-to-body>
      <el-form ref="form" :model="form" :rules="rules" label-width="80px">
#foreach ($column in $columns)
#if ($column.isInsert || $column.isEdit)
#if (!$column.isPk)
        <el-form-item label="${column.columnComment}" prop="$column.javaField">
#set($htmlType = $column.htmlType)
#if ($htmlType == 'input')
          <el-input v-model="form.$column.javaField" placeholder="请输入${column.columnComment}" />
#elseif ($htmlType == 'textarea')
          <el-input v-model="form.$column.javaField" type="textarea" placeholder="请输入${column.columnComment}" />
#elseif ($htmlType == 'select')
          <el-select v-model="form.$column.javaField" placeholder="请选择${column.columnComment}">
            <el-option label="请选择字典生成" value="" />
          </el-select>
#elseif ($htmlType == 'datetime')
          <el-date-picker
            v-model="form.$column.javaField"
            type="datetime"
            placeholder="选择${column.columnComment}"
            value-format="yyyy-MM-dd HH:mm:ss"
          />
#end
        </el-form-item>
#end
#end
#end
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="submitForm">确 定</el-button>
        <el-button @click="cancel">取 消</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { list{ClassName}, get{ClassName}, del{ClassName}, add{ClassName}, update{ClassName} } from "@/api/{moduleName}/{businessName}";

export default {
  name: "{ClassName}",
  data() {
    return {
      // 遮罩层
      loading: true,
      // 选中数组
      ids: [],
      // 非单个禁用
      single: true,
      // 非多个禁用
      multiple: true,
      // 显示搜索条件
      showSearch: true,
      // 总条数
      total: 0,
      // {functionName}表格数据
      {className}List: [],
      // 弹出层标题
      title: "",
      // 是否显示弹出层
      open: false,
      // 查询参数
      queryParams: {
        pageNum: 1,
        pageSize: 10,
#foreach ($column in $columns)
#if ($column.isQuery)
        $column.javaField: null,
#end
#end
      },
      // 表单参数
      form: {},
      // 表单校验
      rules: {
#foreach ($column in $columns)
#if ($column.isRequired)
        $column.javaField: [
          { required: true, message: "$column.columnComment不能为空", trigger: "blur" }
        ],
#end
#end
      }
    };
  },
  created() {
    this.getList();
  },
  methods: {
    /** 查询{functionName}列表 */
    getList() {
      this.loading = true;
      list{ClassName}(this.queryParams).then(response => {
        this.{className}List = response.rows;
        this.total = response.total;
        this.loading = false;
      });
    },
    // 取消按钮
    cancel() {
      this.open = false;
      this.reset();
    },
    // 表单重置
    reset() {
      this.form = {
#foreach ($column in $columns)
#if ($column.isInsert)
        $column.javaField: null,
#end
#end
      };
      this.resetForm("form");
    },
    /** 搜索按钮操作 */
    handleQuery() {
      this.queryParams.pageNum = 1;
      this.getList();
    },
    /** 重置按钮操作 */
    resetQuery() {
      this.resetForm("queryForm");
      this.handleQuery();
    },
    // 多选框选中数据
    handleSelectionChange(selection) {
      this.ids = selection.map(item => item.${pkColumn.javaField})
      this.single = selection.length !== 1
      this.multiple = !selection.length
    },
    /** 新增按钮操作 */
    handleAdd() {
      this.reset();
      this.open = true;
      this.title = "添加{functionName}";
    },
    /** 修改按钮操作 */
    handleUpdate(row) {
      this.reset();
      const ${pkColumn.javaField} = row.${pkColumn.javaField} || this.ids
      get{ClassName}(${pkColumn.javaField}).then(response => {
        this.form = response.data;
        this.open = true;
        this.title = "修改{functionName}";
      });
    },
    /** 提交按钮 */
    submitForm() {
      this.$refs["form"].validate(valid => {
        if (valid) {
          if (this.form.${pkColumn.javaField} != null) {
            update{ClassName}(this.form).then(response => {
              this.$modal.msgSuccess("修改成功");
              this.open = false;
              this.getList();
            });
          } else {
            add{ClassName}(this.form).then(response => {
              this.$modal.msgSuccess("新增成功");
              this.open = false;
              this.getList();
            });
          }
        }
      });
    },
    /** 删除按钮操作 */
    handleDelete(row) {
      const ${pkColumn.javaField}s = row.${pkColumn.javaField} || this.ids;
      this.$modal.confirm('是否确认删除{functionName}编号为"' + ${pkColumn.javaField}s + '"的数据项？').then(function() {
        return del{ClassName}(${pkColumn.javaField}s);
      }).then(() => {
        this.getList();
        this.$modal.msgSuccess("删除成功");
      }).catch(() => {});
    },
    /** 导出按钮操作 */
    handleExport() {
      this.download('{moduleName}/{businessName}/export', {
        ...this.queryParams
      }, `{className}_${new Date().getTime()}.xlsx`)
    }
  }
};
</script>
```

## 菜单SQL模板

```sql
-- {functionName}菜单
INSERT INTO sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, remark)
VALUES ('{functionName}', {parentMenuId}, {orderNum}, '{businessName}', '{moduleName}/{businessName}/index', 1, 0, 'C', '0', '0', '{moduleName}:{businessName}:list', '{icon}', 'admin', NOW(), '{functionName}菜单');

-- 获取父菜单ID
SET @parentId = LAST_INSERT_ID();

-- 按钮
INSERT INTO sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, remark)
VALUES
('{functionName}查询', @parentId, 1, '#', '', 1, 0, 'F', '0', '0', '{moduleName}:{businessName}:query', '#', 'admin', NOW(), ''),
('{functionName}新增', @parentId, 2, '#', '', 1, 0, 'F', '0', '0', '{moduleName}:{businessName}:add', '#', 'admin', NOW(), ''),
('{functionName}修改', @parentId, 3, '#', '', 1, 0, 'F', '0', '0', '{moduleName}:{businessName}:edit', '#', 'admin', NOW(), ''),
('{functionName}删除', @parentId, 4, '#', '', 1, 0, 'F', '0', '0', '{moduleName}:{businessName}:remove', '#', 'admin', NOW(), ''),
('{functionName}导出', @parentId, 5, '#', '', 1, 0, 'F', '0', '0', '{moduleName}:{businessName}:export', '#', 'admin', NOW(), '');
```
