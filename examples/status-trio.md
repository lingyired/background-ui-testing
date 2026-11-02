# Origin: Status Trio

The skill was extracted from
[Status Trio](https://github.com/lingyired/status-trio), a macOS app maintained
by lingyired. The original Apache-2.0 attribution is retained in NOTICE.

The extraction baseline is commit
`67bdc1a42b0b0b2f256d095d6239728ee7732431`. Its
[project adapter](https://github.com/lingyired/status-trio/blob/67bdc1a42b0b0b2f256d095d6239728ee7732431/docs/background-computer-use-testing.md)
records selected native CU checks, finite observation, unsupported controls,
and separate functional/background acceptance.

The source project supplies its own Debug launcher, development Bundle ID,
instance validation, display placement, and focus diagnostic. These are
project integrations, not tools bundled with this skill. Do not copy their
flags or identity checks unchanged into another app.

The source adapter reports successful checks for selected Settings and
first-run guide controls. Other routes and providers require separate
evidence. This repository has not independently repeated those live checks.

Keep current Status Trio launch and provider policy in that project's
instructions. This origin note is historical evidence, not an override of
the current project's rules.
