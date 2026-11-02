# Background UI Testing

[English](README.md)

让 Agent 在你继续使用电脑时测试 UI，保留当前前台应用、输入焦点、指针和工作区；工具无法满足条件时，停止受影响的步骤并明确报告原因。

这是一个 Agent Skill，提供操作流程与证据标准，不提供桌面驱动、Computer Use 服务、权限或通用启动器。副屏不会自动隔离输入。

## 安装

通过 [Skills CLI](https://github.com/vercel-labs/skills)：
需要 Node.js 22.20 或更新版本。以下命令安装到当前项目；添加 `-g` 可安装为跨项目使用的用户级技能。

```bash
npx skills add lingyired/background-ui-testing --skill background-ui-testing
```

也可克隆仓库，将 `skills/background-ui-testing/` 完整安装到 Agent 实际支持的位置。支持 `~/.agents/skills` 的环境可使用[英文说明中的复制命令](README.md#install)，该命令会拒绝覆盖已有目录。

请保留全部参考文件、可选的 Codex 元数据、许可证和来源说明，并在实际使用的 Agent 中确认技能已被发现。

## 使用

```text
使用 $background-ui-testing 检查当前应用，保持我继续使用电脑。
采用项目的独立测试实例，分别报告功能、后台干扰、证据范围与清理状态。
```

只读任务不会为了完成检查而修改设置。没有可用 provider 时，受影响的真实 UI 操作标为 `BLOCKED`，已授权且安全的非 GUI 检查可以继续。

流程包括：确认实例与工具能力、启动有截止时间的观察、只执行任务授权的操作、验证结果，并只恢复仍由本次测试持有的状态。禁止激活后再恢复焦点、全局输入，以及覆盖用户的并发修改。

## 项目接入

参考[接入规则](skills/background-ui-testing/references/project-adapter.md)与[适配器示例](examples/project-adapter.md)。具体项目负责定义启动命令、独立身份、provider 限制、观察工具、会激活应用的控件及清理方式。

项目可以自行选择“所有真实 UI 测试默认走后台流程”；安装技能本身不会建立这条项目策略，也不会为应用增加新的启动参数。

### 是否需要修改应用代码？

不一定。如果应用和 provider 已支持实例定向的后台操作，接入现有启动与观察流程即可；只检查源文件或已有截图，也不需要改应用。

如果打开设置、权限恢复或工具 attachment 会使应用主动激活，则可能需要在已授权的开发范围内增加仅供开发使用的后台模式，将窗口展示与激活分开，并保留正常运行行为。只改应用无法让依赖全局键鼠输入的工具安全地进行后台操作。

[Status Trio macOS 实现示例](examples/status-trio.md)列出了实际改动、固定版本源码、启动约束、验证命令和已知限制。应用实现和专属脚本仍由 Status Trio 仓库维护。

使用[证据与清理说明](skills/background-ui-testing/references/evidence-and-cleanup.md)及[示例报告](examples/run-report.md)，分别记录前台激活、输入焦点、指针、工作区和状态恢复。未观测的维度不能宣称通过。

## 支持范围

| 范围 | 当前内容 |
| --- | --- |
| 通用流程 | 不绑定 provider 的能力检查、执行与停止条件 |
| macOS | 平台指南与 Status Trio 实现示例，包含固定版本源码链接 |
| 浏览器 | profile/context、焦点、剪贴板和系统对话框的边界 |
| Windows / Linux 桌面 | 仅有通用规则；尚无平台适配与真实运行验收 |
| 具体 provider | 必须按本次实例和操作验证，不提供整体兼容承诺 |

技能源自 [Status Trio](https://github.com/lingyired/status-trio)。[macOS 实现示例](examples/status-trio.md)中的证据只覆盖特定应用、工具和控件，不推广为其他环境的验收结论。

## 验证与贡献

```bash
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
python3 scripts/smoke_install.py
```

开发检查需要 Python 3.10 或更新版本。安装冒烟检查还需要 Node.js，会通过网络获取固定版本的 Skills CLI，并只在临时项目中安装，不替换已有技能副本。

仓库校验检查格式、文件引用和独立安装完整性。[决策评估场景](evals/scenarios.yaml)用于检查 Agent 如何判断权限、证据和清理，不等同于真实 UI 测试。贡献方式见 [CONTRIBUTING.md](CONTRIBUTING.md)。

通过 CLI 安装的副本使用相应更新机制；手动复制时记录来源 commit，先检查本地修改，再明确替换整个目录。

## 许可证

Apache-2.0，见 [LICENSE](LICENSE) 和 [NOTICE](NOTICE)。可安装目录内也包含许可证和来源说明。
