# MyBatis Mapper 规范

本文档提供 MyBatis Mapper 开发的规范和标准模板。

## Mapper XML 规范

1. 使用 `<resultMap>` 定义结果映射
2. 使用 `<sql>` 定义可复用的 SQL 片段
3. 使用 `<where>` 和 `<if>` 动态 SQL
4. 指定 `jdbcType` 类型
5. 软删除: 更新 `isvalid = '0'`

## Mapper XML 模板

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="com.six.mapper.OrderMapper">

  <resultMap type="Order" id="OrderResult">
    <result property="orderId" column="order_id"/>
    <result property="orderNo" column="order_no"/>
    <result property="userId" column="user_id"/>
    <result property="status" column="status"/>
    <result property="createTime" column="create_time"/>
    <result property="updateTime" column="update_time"/>
  </resultMap>

  <sql id="selectOrderVo">
    select order_id, order_no, user_id, status, create_time, update_time
    from t_order
  </sql>

  <select id="getList" parameterType="Order" resultMap="OrderResult">
    select <include refid="selectOrderVo"/>
    from t_order
    <where>
      <if test="orderId != null and orderId != ''">
        and order_id = #{orderId,jdbcType=CHAR}
      </if>
      <if test="orderNo != null and orderNo != ''">
        and order_no = #{orderNo,jdbcType=CHAR}
      </if>
      <if test="userId != null and userId != ''">
        and user_id = #{userId,jdbcType=CHAR}
      </if>
      <if test="status != null and status != ''">
        and status = #{status,jdbcType=CHAR}
      </if>
      <choose>
        <when test="isvalid != null and isvalid != ''">
          and isvalid = #{isvalid,jdbcType=CHAR}
        </when>
        <otherwise>
          and isvalid = '1'
        </otherwise>
      </choose>
    </where>
    order by create_time desc
  </select>

  <select id="findByOrderId" parameterType="String" resultMap="OrderResult">
    <include refid="selectOrderVo"/>
    where order_id = #{orderId,jdbcType=CHAR}
  </select>

  <insert id="insert" parameterType="Order">
    insert into t_order
    <trim prefix="(" suffix=")" suffixOverrides=",">
      <if test="orderId != null">order_id,</if>
      <if test="orderNo != null and orderNo != ''">order_no,</if>
      <if test="userId != null and userId != ''">user_id,</if>
      <if test="status != null and status != ''">status,</if>
      <if test="createTime != null">create_time,</if>
      <if test="updateTime != null">update_time,</if>
      <if test="isvalid != null">isvalid,</if>
    </trim>
    <trim prefix="values (" suffix=")" suffixOverrides=",">
      <if test="orderId != null">#{orderId,jdbcType=CHAR},</if>
      <if test="orderNo != null and orderNo != ''">#{orderNo,jdbcType=VARCHAR},</if>
      <if test="userId != null and userId != ''">#{userId,jdbcType=CHAR},</if>
      <if test="status != null and status != ''">#{status,jdbcType=CHAR},</if>
      <if test="createTime != null">#{createTime,jdbcType=TIMESTAMP},</if>
      <if test="updateTime != null">#{updateTime,jdbcType=TIMESTAMP},</if>
      <if test="isvalid != null">#{isvalid,jdbcType=CHAR},</if>
    </trim>
  </insert>

  <update id="update" parameterType="Order">
    update t_order
    <trim prefix="SET" suffixOverrides=",">
      <if test="orderNo != null and orderNo != ''">order_no = #{orderNo,jdbcType=VARCHAR},</if>
      <if test="status != null and status != ''">status = #{status,jdbcType=CHAR},</if>
      <if test="updateTime != null">update_time = #{updateTime,jdbcType=TIMESTAMP},</if>
    </trim>
    where order_id = #{orderId,jdbcType=CHAR}
  </update>

  <update id="delete" parameterType="Order">
    update t_order set isvalid = '0', update_time = now()
    where order_id = #{orderId,jdbcType=CHAR}
  </update>

</mapper>
```

## 常用标签说明

### resultMap
定义查询结果映射到实体类的字段对应关系：
- `property`: 实体类属性名（驼峰）
- `column`: 数据库字段名（下划线）

### sql
定义可复用的 SQL 片段，通过 `<include refid="xxx"/>` 引用。

### where
动态条件判断：
- `<if test="field != null">` - 判断字段不为空
- `<if test="field != null and field != ''">` - 判断字段不为空且不为空字符串

### choose/when/otherwise
多条件选择：
```xml
<choose>
  <when test="isvalid != null and isvalid != ''">
    and isvalid = #{isvalid,jdbcType=CHAR}
  </when>
  <otherwise>
    and isvalid = '1'
  </otherwise>
</choose>
```

### trim
动态 SQL 构建：
- `prefix`: 前缀（如 "SET "）
- `suffix`: 后缀（如 ","）
- `suffixOverrides`: 覆盖后缀（去除最后一个逗号）

## jdbcType 类型映射

| Java 类型 | jdbcType |
|----------|-----------|
| String | CHAR / VARCHAR |
| Long | BIGINT |
| Integer | INTEGER |
| BigDecimal | DECIMAL |
| Date | TIMESTAMP / DATETIME |
| Boolean | CHAR |

## 注意事项

1. **动态 SQL**: 使用 `<where>` 和 `<if>` 实现条件判断
2. **jdbcType**: 必须指定，避免类型转换错误
3. **软删除**: 使用 update 语句更新 `isvalid = '0'`
4. **SQL 片段**: 使用 `<sql>` 和 `<include>` 复用代码
5. **字段映射**: resultMap 中的 property 和 column 要对应
