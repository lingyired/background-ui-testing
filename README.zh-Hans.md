# Background UI Testing

[English](README.md)

让 Agent 在你继续使用电脑时测试 UI，保留当前前台应用、输入焦点、指针和工作区；工具无法满足条件时，停止受影响的步骤并明确报告原因。

这是一个负责后台执行的 Agent Skill：项目、其 Agent 和测试工具决定测什么、步骤、断言、功能验收和报告格式；skill 负责让这些 CU 测试尽可能在不打扰用户的环境中执行，不增加测试方法要求。使用前不必已有完整测试集，测试规划仍由项目及其 Agent 按任务决定。

skill 不提供桌面驱动、Computer Use 服务、权限或通用启动器。副屏不会自动隔离输入。

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
使用 $background-ui-testing 在不打扰我的情况下执行本项目的 CU 测试计划。
保留项目已有的用例、步骤、断言和报告约定。
评估执行路径，观察干扰，说明无法后台执行的操作及清理情况。
```

只读任务不增加修改操作来探测能力；文件检查无需连接真实 UI。已有操作无法后台执行时，说明限制，不擅自设计替代测试。

流程包括：确认目标与工具能力、建立有时间边界的干扰观察、执行项目已有的授权步骤，并按项目清理约定释放本次拥有的资源。禁止激活后再恢复焦点、借用用户的全局输入，以及覆盖用户的并发修改。

沿用项目或测试工具已有的报告格式与术语，只补充后台干扰、观察局限及清理信息，不重新定义功能结果或报告格式。

## 项目接入

参考[接入规则](skills/background-ui-testing/references/project-adapter.md)与[适配器示例](examples/project-adapter.md)。具体项目负责定义测试目标身份与状态隔离、启动或连接方式、工具限制、观察方式、会激活应用的控件及清理边界。

项目可以自行选择“所有真实 UI 测试默认走后台流程”；安装技能本身不会建立这条项目策略，也不会为应用增加新的启动参数。

把项目现有测试连接到受支持的后台路径，不额外增加开关、导航或截图来满足 skill 的能力门槛。已有工具观察可能已经足够，无需强制新增观察器、启动器或开发构建。清理按资源归属执行，例如只关闭测试 context，保留共享浏览器进程。

### 是否需要修改应用代码？

不一定，先复用已有能力。只有需要适配建议时，才评估实际技术栈、自动化接口及相关构建方式，再提出低侵入、可撤销的选项。开发者与其 Agent 决定是否以及如何实施，不强制插件、helper、文件数量或逐窗口改动。

应用实现、正式构建隔离及发布验证属于项目工程职责；skill 不主动启动这些工程任务，也不规定验证用例。它负责停止不支持的后台操作并说明经过评估的回退选项；切换前台或隔离会话需有相应授权。

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

仓库校验检查格式、文件引用和独立安装完整性。[决策评估场景](evals/scenarios.yaml)只检查 skill 的后台执行边界，不规定应用如何设计测试，也不等同于真实 UI 测试。贡献方式见 [CONTRIBUTING.md](CONTRIBUTING.md)。

旧评估记录反映当时的范围；收窄为“只负责后台执行”之前的场景已[完整归档](evals/scenarios-before-execution-scope-2026-11-02.yaml)，其中的历史标准不作为当前 skill 的要求。

通过 CLI 安装的副本使用相应更新机制；手动复制时记录来源 commit，先检查本地修改，再明确替换整个目录。

## 许可证

Apache-2.0，见 [LICENSE](LICENSE) 和 [NOTICE](NOTICE)。可安装目录内也包含许可证和来源说明。
