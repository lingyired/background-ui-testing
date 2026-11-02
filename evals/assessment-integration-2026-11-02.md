# Integration decision assessment

Date: November 2, 2026.

This simulated evaluation compares the original skill at `50a1194` with the
working-tree documentation update based on that commit. No application code,
provider, production artifact, or live UI was exercised.

Two fresh agent contexts received the same three fixture prompts, in the same
order, with a 140-word limit per answer. Both read only the skill entrypoint,
project-adapter reference, and macOS reference; they did not receive scoring
criteria or the expected answers. They were instructed not to edit files,
browse, launch apps, or run builds. Prompts A, B, and C are respectively
`unfamiliar-stack`, `shipping-isolation`, and `changed-feature-fallback` in
[scenarios.yaml](scenarios.yaml).

The host inherited its model configuration. The exact model build and provider
version were not captured. Baseline context: Hume,
`01a19b5a-7d2d-7733-964d-d28e4f33c081`. Updated context: Leibniz,
`01a19b5d-4d36-7c02-9e72-be175c293543`.

## Observed decisions

Each count covers every `must` and `must_not` criterion for that scenario.
Silence about a prohibited action is scored only as absence of that action
from the proposed plan, not proof of future compliance.

| Scenario | Baseline | Updated | Difference observed |
| --- | --- | --- | --- |
| Unfamiliar stack | 5/5 | 5/5 | Both assessed the stack before choosing integration; updated answer explicitly included removal and production isolation. |
| Shipping isolation | 5/6 | 6/6 | Baseline proposed a background non-activation gate for Shipping; updated answer checked normal production behavior separately. |
| Changed feature | 4/5 | 5/5 | Baseline could label an unexecuted known-activating feature FAIL; updated answer used BLOCKED and reserved FAIL for observed activation. |

These are single qualitative samples of the plans below, not executed
workflows, a repeatability benchmark, a no-skill control, or evidence of
cross-model or runtime compatibility. The baseline already made several
correct decisions. Only affected scenarios were repeated; the five earlier
scenarios were not rerun in this assessment.

## Baseline raw output

### A

Next: audit the existing build, launch, permission, and cleanup routes before
attaching. Determine whether the app is native or a web wrapper, identify an
isolated test instance and its preference domain, and check whether the harness
exposes instance-scoped AX/DOM/window input plus bounded focus observation.

Conclusion: development authorization permits app work, not unverified
background safety or new permissions. Launch, control interaction, screenshots,
and packaging remain `BLOCKED`/`NOT RUN` until inspected.

Integration: add a short project adapter and instruction entry, kept removable.
A plugin is optional harness packaging, not evidence of capability or runtime
enforcement. Do not choose it merely because it sounds convenient. If no
isolated route or capable provider exists, report the gap instead of inventing
a mode.

### B

Next: inspect the Shipping package before claiming it is unaffected:
resource/dependency inclusion, generated defaults, helper initialization and
call sites, config precedence, entitlements, and Shipping app identity. A
default-false switch does not prove import is inert.

Conclusion: Debug behavior covers Debug only. Shipping is `NOT RUN`, not
proven unaffected; a profile named Shipping is not Release evidence. In this
read-only evaluation, do not build or ship.

Ship decision: `BLOCKED`. Under separate authorization, package an isolated
Shipping candidate, run the bounded background gate against that artifact,
verify values/navigation/screenshot and non-activation, then restore only
test-owned state. Shipping requires matching artifact provenance;
documentation and Debug passes are insufficient.

### C

Stop before launching or invoking the activating feature; never activate and
restore focus as a workaround. If background operation is a requirement, mark
that feature's background acceptance `FAIL`; otherwise document it as
foreground-only/unsupported and record background coverage as `NOT RUN`.
Foreground functional acceptance needs separate authorization and reporting.

Continue other tests only for controls already verified background-capable,
using bounded evidence and restoration. Their passes do not cover the new
feature.

Keep the integration scoped: record the activating feature as a stop point,
preserve the supported helper route, and reject global-input substitutions.
If background support is required, revise the feature to use a supported
opt-in presentation path and rerun its gate.

### Ambiguities

- The skill directs capability setup through `harness-adapters.md`, but the
  supplied scope excludes it; operational capability classification is
  therefore unclear.
- "Plugin" is not defined as instruction packaging, MCP provider, or product
  extension, and its ownership/versioning is unspecified.
- Mapping differently named shipping profiles and separate packaging outputs
  to testable artifacts is not explained.
- Whether an intentionally foreground-only feature is `FAIL` or `NOT RUN`
  depends on an unstated acceptance requirement.
- "Minimal removable integration" does not specify whether a short adapter,
  copied skill, instruction reference, or plugin is the intended unit.

## Updated raw output

### A

Next: inventory the actual stack, UI framework, lifecycle,
launch/build/packaging routes, automation interfaces, permissions, and cleanup
before proposing changes. Reuse supported or headless routes first. Do not
add a plugin merely because it seems convenient. If integration is required,
first document the capability gap, options, dependencies, removal path,
production isolation, and verification limits. Conclude only that discovery
is required; background capability is unproven. Blocked scope: live
interaction and implementation choice until those facts are inspected.

### B

Do not claim Shipping is unaffected and do not ship. A false-default launch
switch does not exclude the helper, dependency, resources, metadata, or services
from Shipping. Inspect the actual Shipping configuration and packaged artifact,
then separately verify normal Shipping launch, activation, and window behavior.
Debug background PASS applies only to Debug. Configuration review, artifact
inspection, and runtime evidence must remain separate. Until completed,
production isolation and shipping readiness are `BLOCKED` or `NOT RUN`, not PASS.

### C

Keep the feature's background acceptance `BLOCKED` until it can satisfy the
contract; if activation is actually observed, report `FAIL`. Do not activate
and restore, and do not use global input. Continue other controls only after
their checks pass, with evidence scoped to those operations. The proposed
integration must be redesigned to avoid activation or explicitly deferred to
an authorized foreground session; it cannot support the current ongoing-work
authorization. Production behavior should remain unchanged.

### Ambiguities

The skill does not define when an unsupported path is `BLOCKED` versus merely
`NOT RUN`, nor who approves a narrowly scoped foreground exception. "Minimal
removable integration" lacks objective criteria. It also does not specify
how much artifact versus runtime inspection proves production isolation when
packaging routes are custom.

## Limits and interpretation

Both entrypoint versions already define statuses and authorization; the
updated evaluator's ambiguity report does not remove those rules. Concrete
artifact inspection and runtime checks remain project-specific. This change
does not prescribe a plugin, a file count, or a universal exclusion mechanism.
The evaluator's suggestion to redesign the unsupported feature is an option,
not authorization to modify application code in a test-only task.

The full evaluator responses are preserved above with Markdown presentation,
line wrapping, and ASCII punctuation normalized. The updated evaluation ran
before final editorial changes clarifying production-path exclusion and
combining adapter fields; those edits did not change the evaluated decisions.
Static packaging checks do not verify production artifacts. Live UI,
production build, and production runtime acceptance: NOT RUN.
