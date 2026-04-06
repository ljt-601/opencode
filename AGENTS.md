## 语言和风格

- 始终使用简体中文回复
- 直接回答问题，不要客套话
- 代码注释也用中文

## 代码规范

- 使用 2 空格缩进
- 变量名用驼峰命名（camelCase）
- 函数名用动词开头（如 getUserById）

### 编码规则

1. 尽量不采用硬编码，采用枚举或常量的形式（中文错误提醒除外）
2. 采用代码最优最简化原则，考虑性能的同时用优雅高级方式编写代码
3. 遇到列表为空判断时统一使用 CollUtil.isEmpty()
4. 编码完成检查是否有错误的地方和格式出问题的地方

## 工作习惯

- 修改代码前先阅读相关文件
- 不确定时先问，不要猜测
- 每次只做最小必要的修改
- **修改任何文件前必须先使用 Read 工具查看最新文件内容，在最新内容基础上进行操作（重要：每次编辑前都要重新读取文件，确保看到的是最新版本）**
- 修改或新增代码时要注意在合适的位置加上注释

## 第二大脑规则

- 当用户问“我的偏好”“我之前说过什么”“现在工作重点是什么”“记住这个”这类问题时，优先读取统一第二大脑
- 优先读取：
  - `/Users/bryle/second-brain/dashboard.md`
  - `/Users/bryle/second-brain/user/preferences.md`
  - `/Users/bryle/second-brain/work/current-focus.md`
- 按需继续读取：
  - `/Users/bryle/second-brain/projects/`
  - `/Users/bryle/second-brain/knowledge/`
  - `/Users/bryle/second-brain/life/`
  - `/Users/bryle/second-brain/inbox/`
- 不要在未读取第二大脑的情况下，直接回答“不知道用户偏好”
