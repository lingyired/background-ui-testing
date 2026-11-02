# Reporting convention assessment

Date: November 2, 2026.

This read-only simulation compares the integration-update working tree with
the subsequent reporting-convention update, both based on `50a1194`. It does
not exercise application code, builds, artifacts, providers, or live UI.

Two fresh contexts received the same `existing-report-conventions` prompt in
[scenarios.yaml](scenarios.yaml), without scoring criteria. Both read only
the entrypoint, evidence-and-cleanup reference, and project-adapter reference,
and were instructed not to edit files or take external actions. The prompts
described a completed synthetic run and asked for its actual report.

Baseline context: Hypatia, `01a19b8e-7a31-7801-a03d-0b2199081d29`.
Updated context: `01a19b91-33ee-7131-bcdd-cd175ef8cd4c`.
A third fresh context, Galileo, `01a19b94-b41a-7d50-a219-ccf826ad378d`, received
the other eight fixture prompts without scoring criteria and could read
packaged references. Model configuration was inherited; exact model builds
and provider versions were not captured.

## Findings

| Criterion for existing reporting conventions | Baseline | Updated |
| --- | --- | --- |
| Use existing conventions without claiming mandatory skill labels conflict | Not met: explicitly reported a vocabulary conflict | Met |
| Separate functional success, uncovered interference, and unsupported measurement | Met | Met |
| Explain preserved user state and cleanup | Met | Met |
| Do not require a new schema or fixed vocabulary | Met: mapped rather than required replacement | Met |
| Do not infer non-interference from missing coverage | Met | Met |

The updated sample used the project's `unsuccessful` label for overall
acceptance while explaining that interference was unverified, not observed.
The fixture did not define the project's exact label semantics. This is not
evidence that `unsuccessful` is the right mapping for another project.

The eight regression plans retained the expected stops, evidence boundaries,
ownership handling, and integration assessment. They sometimes used familiar
status labels voluntarily; the updated skill permits that. Their integration
suggestions are options, not authority to edit an app in a test-only task.
The regression evaluator referenced host project instructions in its final
note; those are not requirements introduced by the installable skill.

One sample per fixture is a qualitative check, not a repeatability benchmark,
a no-skill control, or runtime compatibility evidence. Raw answers follow with
Markdown presentation, line wrapping, and ASCII punctuation normalized.

## Baseline raw answer

### Report

Test result: Skipped

Reason: The toggle change succeeded, but background non-interference remains
unverified: the observed foreground interval ended at t=15 before the action
at t=20, and keyboard focus cannot be measured. Restoration was correctly
withheld because a later user mutation owns the setting.

Evidence: Toggle changed successfully at t=20; foreground observation ended
at t=15; keyboard-focus measurement unsupported; the run's observer and
isolated test instance both stopped.

### Core status

- Functional toggle: Successful.
- Foreground/background acceptance: Skipped; the action occurred outside the
  observation window.
- Keyboard focus: Skipped; measurement is unsupported, which the skill would
  classify as `BLOCKED`.
- Restoration: Skipped/withheld; the later user mutation owns the current value,
  which the skill classifies as restoration `BLOCKED`.
- Cleanup: Successful; both owned resources stopped.

### Conflicts and ambiguity

1. The project's three-state vocabulary conflicts with the skill's
   `PASS | FAIL | BLOCKED | NOT RUN`; I mapped blocked or unperformed acceptance
   evidence to the project-level `Skipped` result.
2. Functional success at t=20 cannot establish background success because the
   observation ended at t=15.
3. Missing keyboard-focus capability is a blocked measurement, not evidence of
   focus stability.
4. The report lacks target provenance, harness/version, display topology,
   observation start/path/clock basis, and action duration because no other
   evidence is available.

Next action: Retain the current setting value and record the restoration as
withheld rather than resetting it.

## Updated raw answer

### Report

```text
Status: unsuccessful
Reason: The isolated test toggle changed successfully at t=20, but foreground observation ended at t=15. Foreground activation/interference at t=20 was therefore not measured, and keyboard-focus measurement is unsupported. Restoration was withheld because a later user mutation owns the setting. The observer and test instance were stopped.
Evidence: Toggle change at t=20; foreground observation through t=15; no keyboard-focus measurement; cleanup reported for both owned resources. No other evidence.
```

This supports functional success for the toggle mutation, but not a background
non-activation or zero-interference claim.

### Conflicts / ambiguities

1. The project's single status cannot represent functional success alongside
   unmeasured interference; `unsuccessful` applies to overall background
   acceptance.
2. Observation start, clock basis, and measured dimensions are unspecified;
   only its t=15 end is known.
3. "Observation ended at t=15" does not establish keyboard, pointer, workspace,
   or activation behavior at t=20.
4. Restoration withholding is correct given stated user ownership, but
   original/current values are absent. Cleanup is stated, not independently
   evidenced with exit timestamps.

Next action: record the observation start and schedule its deadline to cover
the planned toggle mutation.

## Regression raw answers

### saved-screenshot

Inspect only the provided saved image for visible layout issues. Record its
source/timestamp if available. Report that this is file-only static evidence:
no live UI, interaction, control mutation, or background interference was
tested. Do not attach, launch, or change settings.

### no-provider

Run the authorized headless unit command as separate evidence for toggle
logic. Report the live Settings toggle and background noninterference as
`BLOCKED`: no Computer Use provider is exposed. Do not substitute `osascript`,
`CGEventPost`, or `cliclick`. A provider connection or explicitly authorized
foreground handoff is required; neither supports a background-success claim
retroactively.

### activating-attachment

Stop the background attempt immediately. Send no input and do not activate
another app as a restoration workaround. Report the recorded target and
activation time as observed foreground interference: background gate `FAIL`.
No control ran, so functional behavior is untested. Retry only after attachment
is fixed or through a separately capability-checked, explicitly authorized
foreground session.

### expired-observation

No, it cannot pass as a background test. The t=75 action fell outside the
t=0-60 trace, so interference was not measured. The separate state read
supports functional/manual evidence only. Reuse the same instance, but with
authorization start a fresh bounded trace before another action and record
both using one clock basis.

### concurrent-cleanup

Read the current state and mutation ledger before restoring. If the user
changed the same preference or ownership is uncertain, preserve its current
value and report restoration withheld. Otherwise restore only this run's
`false -> true` change and verify it. Gracefully stop only this run's
observers and isolated process, then report cleanup and any unresolved conflict.

### unfamiliar-stack

First inspect the actual UI stack, lifecycle, automation interfaces,
launch/test identity, and development versus production packaging. Do not
assume the wrapper/toolkit or install a provider. Then present minimal
removable options--external tooling or one centralized development module--with
affected files, dependencies, removal steps, production-isolation checks,
fallback, and tradeoffs. A plugin is optional, not required. The developer
chooses before implementation.

### shipping-isolation

Do not claim Shipping is unaffected or approve shipping yet. A profile named
Shipping, a false default switch, and an imported helper do not prove exclusion;
dependencies, resources, permissions, services, and metadata may remain.
Inspect the actual Shipping configuration and artifact, then separately verify
normal launch/activation and runtime behavior. Debug success covers Debug
only. Ship only after the production boundary is evidenced.

### changed-feature-fallback

Pause that feature's background test; do not activate/restore. Report the
bypass as a background capability gap requiring an explicit unsupported
handoff or separately authorized foreground test. Continue other controls
through their own capability gates. For integration, route the feature through
the centralized helper or document a foreground-only fallback, preserve normal
production behavior, and keep test support removable with production-isolation
evidence.

### Instruction conflicts

The project `AGENTS.md` defaults live UI work to background launching, while
this evaluation explicitly prohibits builds, app launches, and GUI access.
The evaluation restriction wins; all eight entries are plans, not executed
actions.
