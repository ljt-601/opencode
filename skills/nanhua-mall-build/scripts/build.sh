#!/bin/bash
# 南华积分商城项目自动打包脚本

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 项目根目录
PROJECT_DIR="/Users/bryle/Public/WorkProject/nanhua-mall-ui"
# 构建输出目录
BUILD_DIR="${PROJECT_DIR}/web"
# 文稿目录（存放zip）
DOCS_DIR="/Users/bryle/Documents"

# 获取构建类型参数
BUILD_TYPE="${1:-prod}"

# 验证构建类型
if [[ "$BUILD_TYPE" != "prod" && "$BUILD_TYPE" != "uat" ]]; then
    echo -e "${RED}错误: 构建类型必须是 'prod' 或 'uat'${NC}"
    exit 1
fi

# 确定构建命令和输出文件名
if [[ "$BUILD_TYPE" == "prod" ]]; then
    BUILD_CMD="npm run build:prod"
else
    BUILD_CMD="npm run build:uat"
fi
# 固定输出文件名为web.zip
ZIP_NAME="web.zip"

echo -e "${YELLOW}========================================${NC}"
echo -e "${YELLOW}南华积分商城 - ${BUILD_TYPE} 环境打包${NC}"
echo -e "${YELLOW}========================================${NC}"

# 进入项目目录
cd "$PROJECT_DIR" || exit 1

# 清理旧的构建产物
if [[ -d "$BUILD_DIR" ]]; then
    echo -e "${YELLOW}清理旧构建产物...${NC}"
    rm -rf "$BUILD_DIR"
fi

# 执行构建
echo -e "${YELLOW}开始构建 (${BUILD_CMD})...${NC}"
$BUILD_CMD

# 检查构建是否成功
if [[ ! -d "$BUILD_DIR" ]]; then
    echo -e "${RED}构建失败：未找到构建产物目录${NC}"
    exit 1
fi

# 压缩构建产物
echo -e "${YELLOW}压缩构建产物...${NC}"
ZIP_PATH="${DOCS_DIR}/${ZIP_NAME}"
cd "$PROJECT_DIR"
# 使用ditto命令压缩，与MacZip应用一致，大小稳定在16M
ditto -c -k --keepParent --sequesterRsrc web "$ZIP_PATH"

# 检查压缩是否成功
if [[ ! -f "$ZIP_PATH" ]]; then
    echo -e "${RED}压缩失败${NC}"
    exit 1
fi

# 获取文件大小
FILE_SIZE=$(du -h "$ZIP_PATH" | cut -f1)

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}打包成功！${NC}"
echo -e "${GREEN}文件名: ${ZIP_NAME}${NC}"
echo -e "${GREEN}路径: ${ZIP_PATH}${NC}"
echo -e "${GREEN}大小: ${FILE_SIZE}${NC}"
echo -e "${GREEN}========================================${NC}"
