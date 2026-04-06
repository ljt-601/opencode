---
name: second-brain
description: 当任务涉及用户长期偏好、工作层状态、项目延续、知识整理、生活事项或跨会话记忆时，优先读取统一第二大脑目录。
---

# 第二大脑技能

当用户提到以下意图时，优先读取第二大脑：

- 记住我
- 我的偏好
- 我的工作重点
- 我之前说过什么
- 项目上下文
- 长期记忆
- 第二大脑

优先读取顺序：

1. `/Users/bryle/second-brain/dashboard.md`
2. `/Users/bryle/second-brain/user/preferences.md`
3. `/Users/bryle/second-brain/work/current-focus.md`

按需继续读取：

- `/Users/bryle/second-brain/projects/`
- `/Users/bryle/second-brain/knowledge/`
- `/Users/bryle/second-brain/life/`
- `/Users/bryle/second-brain/inbox/`

回答这类问题前，不要直接说“不知道”。
先检查第二大脑里是否有相关记录。

写入规则：

- 用户偏好 -> `user/`
- 当前工作状态 -> `work/`
- 项目上下文 -> `projects/`
- 通用知识 -> `knowledge/`
- 生活事项 -> `life/`
- 未整理内容 -> `inbox/`
