# Contributing

Keep the core contract independent of a product, machine, and provider.
Project launch commands and exceptions belong in project adapters. New
guidance should address a demonstrated decision failure or capability gap.

## Before opening a pull request

1. Install the development requirements and run the checks in the README.
2. Exercise the affected decision scenarios with a fresh agent context.
3. Report changed decisions, limitations, and any real UI checks separately.

Run each scenario in `evals/scenarios.yaml` with the installable skill and
its references available. Supply the `prompt` without its scoring rules.
Do not expose an actual GUI provider or allow external side effects during
this simulated evaluation.

Evaluate the resulting action plan against every `must` and `must_not`
criterion. Record the model/harness/version, skill commit, raw output, and
each criterion's result. Use an unmodified baseline when changing behavior;
repeat ambiguous cases with fresh contexts. Never present a validator pass
or simulated decision as runtime compatibility evidence.

## Provider or platform evidence

State the app/build, OS, provider/version, exposed interfaces, attachment
route, displays, exact actions, observation window, resolution, blind spots,
and cleanup result. Separate functionality from each interference dimension.
Mark unsupported and untested routes explicitly. Do not generalize a button
test to text input, menus, shortcuts, permissions, or other apps.

Live checks need a supported isolated test instance and a capability gate
before launch/attachment/input. Do not collect evidence by disrupting an
active user's session. Use an explicitly authorized isolated calibration
when the provider's behavior is unknown.

## Files and versions

Edit `skills/background-ui-testing/` as the canonical skill package.
Keep all runtime references inside that directory. Preserve the embedded
license and attribution when distributing it separately.

Update the changelog for meaningful behavior or compatibility changes.
Before publishing a version, update `metadata.version` in `SKILL.md` and
verify the same frozen commit. Repository workflows validate only; they do
not publish releases or rewrite installed copies.

Contributions use this repository's Apache-2.0 license. Report security or
privacy issues without including credentials or sensitive screenshots; a
minimal redacted description is sufficient for initial discussion.
