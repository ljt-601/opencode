# OpenCode 配置仓库

个人 OpenCode 全局配置，包含 agents、skills、设置等。

## 目录结构

```
├── AGENTS.md              # Agent 定义入口
├── opencode.json          # OpenCode 主配置
├── oh-my-opencode.json    # oh-my-opencode Agent 定义
├── tui.json               # TUI 配置
├── agents/                # 全局 Agents（OpenCode 格式）
├── skills/                # 全局 Skills
└── scripts/               # 辅助脚本
```

## 同步到本地

```bash
cd ~/gitHub_workplace/opencode
bash scripts/sync.sh
```

## 更新流程

1. 修改本仓库中的文件
2. `git add . && git commit && git push`
3. `bash scripts/sync.sh` 同步到 `~/.config/opencode/`
