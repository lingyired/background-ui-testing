# Background UI Testing

[简体中文](README.zh-Hans.md)

An [Agent Skill](https://agentskills.io/specification) for testing UI while
someone continues using the same computer. It guides an agent to preserve the
user's foreground app, input focus, pointer, and workspace, and to stop when
its tools cannot do that.

The skill governs background execution of the project's CU tests.
The project, its agent, and tools choose the tests, steps, assertions,
functional acceptance, and report format. A prewritten suite is not required;
the skill adds no testing-method requirements.

It is not a desktop driver or a separate input session.
It supplies no Computer Use provider, permissions, or universal background
launcher. A second display alone does not isolate input.

## Install

With the [Skills CLI](https://github.com/vercel-labs/skills):
Node.js 22.20 or newer is required. The command below installs into the
current project; add `-g` for a user-level installation across projects.

```bash
npx skills add lingyired/background-ui-testing --skill background-ui-testing
```

Alternatively, clone the repository and install the whole skill directory
into a location your agent actually discovers. For agents supporting
`~/.agents/skills`, this copy refuses to overwrite an existing installation:

```bash
git clone https://github.com/lingyired/background-ui-testing.git
mkdir -p "$HOME/.agents/skills"
python3 -c 'import shutil; shutil.copytree("background-ui-testing/skills/background-ui-testing", __import__("pathlib").Path.home() / ".agents/skills/background-ui-testing")'
```

The installable directory includes its relative references, optional Codex
metadata, license, and attribution. Install the whole directory, not just
`SKILL.md`. Confirm discovery using your agent's supported mechanism.

## Use

```text
Use $background-ui-testing to run this project's CU test plan without
disrupting my work. Keep its tests, steps, assertions, and report conventions.
Assess the execution route, observe interference, and explain any unsupported
operations and cleanup.
```

For read-only work, do not add mutations as capability probes. File-only work
needs no live attachment. If a supplied operation cannot run in the background,
report the limitation; do not invent replacement tests.

The procedure checks target ownership and tool capabilities, starts bounded
observation, runs the existing authorized workload, and restores only state
still owned by the run. It does not permit activate-and-restore workarounds,
global input, or silent overwrites of concurrent user changes.

Use the project's or test tool's existing reporting format and terminology.
Add background-interference evidence, limitations, and cleanup where needed,
without redefining functional results or introducing a report schema.

## Adopt in a project

Read the [project integration guide](skills/background-ui-testing/references/project-adapter.md)
and the [adapter example](examples/project-adapter.md). The project owns its
test-target identity and state separation, launch or connection route, tool
restrictions, observations, known activating controls, and cleanup procedures.

Projects can choose to make background testing their default for live UI
work. Installing this skill alone does not establish that policy. Start with
an adapter to an existing supported test route; do not invent app flags.

Connect the existing workload to a supported background route. Do not add
toggle/navigation/screenshot checks to qualify for this skill. Existing
harness observations may be sufficient; no new observer, launcher, or
development build is mandatory. Cleanup follows ownership, such as closing
a test context while preserving a shared browser process.

### Does the application need code changes?

Not always. Use existing support first. If adaptation advice is requested,
assess the actual stack and available automation/build routes before
suggesting low-impact, removable options. The developer and their agent
decide whether and how to implement them. No plugin, helper, file count,
or per-window change is required.

Application implementation, production isolation, and release verification
belong to the project. This skill does not initiate those engineering tasks
or prescribe a verification suite. It stops unsupported background operations
and describes assessed fallback options; foreground or isolated-session
fallback requires applicable authorization.

See the [Status Trio macOS implementation example](examples/status-trio.md)
for the actual code changes, source links, launch contract, checks, and
remaining limitations. Its app code and scripts live in the source project.

Use the [evidence and cleanup guide](skills/background-ui-testing/references/evidence-and-cleanup.md)
and [illustrative run report](examples/run-report.md) to keep observations,
functional results, interference results, and restoration conflicts separate.

## Scope and evidence

| Area | What this repository provides |
| --- | --- |
| Core contract | Provider-neutral procedure and explicit stop conditions |
| macOS | Platform guide and a Status Trio implementation example with source links |
| Browser automation | Context, storage, focus, clipboard, and dialog boundaries |
| Windows and Linux desktops | General contract only; no platform adapters or live verification here |
| Particular providers | Capability checks, not a blanket compatibility endorsement |

This skill originated in [Status Trio](https://github.com/lingyired/status-trio).
Its [macOS implementation example](examples/status-trio.md) covers selected
macOS controls under a specific harness. They do not prove other providers,
platforms, text entry, menus, permissions, or every control.

Repository validation checks packaging and references. The
[decision scenarios](evals/scenarios.yaml) assess agent decisions without
operating a live UI; they concern the skill's execution boundaries, not an
application's test design, and do not establish runtime non-interference.
Earlier assessment records describe the scope at that time. The
[prior scenario snapshot](evals/scenarios-before-execution-scope-2026-11-02.yaml)
preserves the definitions before the execution-only scope correction; those
historical criteria are not requirements of the current skill.

## Validate and contribute

```bash
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
python3 scripts/smoke_install.py
```

Development checks require Python 3.10 or newer. The installation smoke
check also requires Node.js, uses a pinned Skills CLI in a temporary project,
and leaves existing skill installations alone. It requires network access
to obtain that CLI.

See [CONTRIBUTING.md](CONTRIBUTING.md) for decision evaluation and the evidence
required for a compatibility claim. To update a CLI installation, use the
CLI's supported update command. For a manual copy, record the source commit,
inspect local edits, and replace the complete directory deliberately.

## Repository layout

```text
skills/background-ui-testing/  Installable skill and all runtime references
examples/                     Project adapter and labeled evidence examples
evals/                        Simulated decision scenarios and scoring rules
scripts/                      Repository validation
tests/                        Validator and portable-package checks
```

## License and origin

Apache-2.0. See [LICENSE](LICENSE) and [NOTICE](NOTICE). The installable skill
also carries these notices so directory-only installations retain them.
Extracted and adapted from Status Trio; see [CHANGELOG.md](CHANGELOG.md).
