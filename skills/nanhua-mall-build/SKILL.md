---
name: nanhua-mall-build
description: 南华积分商城项目自动化构建打包工具。当用户请求"打生产包"、"打测试包"、"需要打生产包"、"打包uat"等类似表述时，自动执行Vite构建命令，将构建产物（web目录）压缩为ZIP文件，并保存到文稿目录（/Users/bryle/Documents）。支持生产环境（prod）和UAT测试环境（uat）两种构建模式。
---

# 南华积分商城构建打包

## 快速使用

当用户提到以下关键词时触发此技能：

- "打生产包" / "打包生产" / "生产环境打包"
- "打测试包" / "打包uat" / "uat环境打包"
- "需要打生产包" / "需要打测试包"

## 构建流程

### 1. 确定构建类型

根据用户请求判断构建环境：

- **生产环境**: "生产包" → `npm run build:prod`
- **UAT测试环境**: "测试包" / "uat" → `npm run build:uat`

### 2. 执行构建脚本

使用 `scripts/build.sh` 脚本自动化执行以下步骤：

```bash
./scripts/build.sh [prod|uat]
```

脚本自动完成：

- 进入项目目录 `/Users/bryle/Public/WorkProject/nanhua-mall-ui`
- 清理旧的构建产物（`web/` 目录）
- 执行对应的构建命令
- 验证构建产物是否生成
- 压缩构建产物为ZIP文件
- 将ZIP保存到文稿目录 `/Users/bryle/Documents`

### 3. 输出结果

构建成功后，ZIP文件固定命名为：`web.zip`（可直接上传）

## 脚本说明

### `scripts/build.sh`

自动化构建打包脚本，参数：

- `prod`: 生产环境构建
- `uat`: UAT测试环境构建

**关键配置**：

- 项目根目录: `/Users/bryle/Public/WorkProject/nanhua-mall-ui`
- 构建输出: `web/` 目录
- 输出位置: `/Users/bryle/Documents/`

**错误处理**：

- 验证构建类型参数
- 检查构建产物目录是否生成
- 检查ZIP文件是否创建成功

## 使用示例

**用户请求**: "帮我打一个生产包"

**执行步骤**:

1. 判断为生产环境构建
2. 运行 `./scripts/build.sh prod`
3. 构建完成后，ZIP文件位于 `/Users/bryle/Documents/web.zip`
4. 向用户报告文件路径和大小

**用户请求**: "打uat测试包"

**执行步骤**:

1. 判断为UAT环境构建
2. 运行 `./scripts/build.sh uat`
3. 构建完成后，ZIP文件位于 `/Users/bryle/Documents/web.zip`
4. 向用户报告文件路径和大小


