# macOS implementation example: Status Trio

[Status Trio](https://github.com/lingyired/status-trio) is the source project
for this skill. It demonstrates an app-side integration: an opt-in Debug
mode and project-owned scripts allow selected UI operations to be tested
without the app deliberately activating itself.

All implementation links below are pinned to the extraction baseline,
`67bdc1a42b0b0b2f256d095d6239728ee7732431`. The original Apache-2.0 attribution
is retained in NOTICE. The application and its scripts are maintained in
Status Trio, not copied into this skill package.

## When an application needs changes

| Existing capability | Integration needed |
| --- | --- |
| App and provider already support the requested background operation | Connect the supported launch, identity, observation, and cleanup routes |
| App activates itself along the requested route | Consider a scoped, opt-in development mode, with authorization to edit the app |
| Provider offers only global input, or the required system dialog needs focus | App changes alone cannot meet the contract; stop the affected step or use an explicitly authorized foreground test |

Saved screenshots and source inspection need no live app mode. A Debug
background mode is one implementation strategy, not a requirement imposed
on every application by this skill.

## App-side implementation

| Concern | What Status Trio changes | Source |
| --- | --- | --- |
| Explicit test mode | Parse immutable launch configuration only under `DEBUG`; invalid arguments disable it and Release ignores the flags | [BackgroundUITestingConfiguration.swift](https://github.com/lingyired/status-trio/blob/67bdc1a42b0b0b2f256d095d6239728ee7732431/Sources/StatusTrioCore/App/BackgroundUITestingConfiguration.swift) |
| Startup and dependency injection | Pass configuration through the environment and controllers; preserve the real first-run guide policy, otherwise open Settings | [AppEnvironment.swift](https://github.com/lingyired/status-trio/blob/67bdc1a42b0b0b2f256d095d6239728ee7732431/Sources/StatusTrioCore/App/AppEnvironment.swift) |
| Window lifecycle | Select background presentation; skip the temporary activation-policy change and permission resurfacing; preserve normal frame autosave | [SettingsWindowController.swift](https://github.com/lingyired/status-trio/blob/67bdc1a42b0b0b2f256d095d6239728ee7732431/Sources/StatusTrioCore/UI/Settings/SettingsWindowController.swift), [OnboardingWindowController.swift](https://github.com/lingyired/status-trio/blob/67bdc1a42b0b0b2f256d095d6239728ee7732431/Sources/StatusTrioCore/UI/OnboardingWindowController.swift) |
| Placement | Resolve current displays by ID and visible frame on presentation; handle negative coordinates and a missing secondary display | [BackgroundUIWindowPlacement](https://github.com/lingyired/status-trio/blob/67bdc1a42b0b0b2f256d095d6239728ee7732431/Sources/StatusTrioCore/App/BackgroundUITestingConfiguration.swift#L66) |
| Attachment and reopen | Special-case the exact observed native service sender in Debug background mode; preserve physical Dock, unknown sender, and normal-mode routing | [DockActivationAction.swift](https://github.com/lingyired/status-trio/blob/67bdc1a42b0b0b2f256d095d6239728ee7732431/Sources/StatusTrioCore/App/DockActivationAction.swift), [AppDelegate.swift](https://github.com/lingyired/status-trio/blob/67bdc1a42b0b0b2f256d095d6239728ee7732431/Sources/StatusTrioCore/App/AppDelegate.swift) |

The presentation policy is a small seam in the existing controllers. This
excerpt is the actual policy at the pinned commit:

```swift
enum SettingsWindowPresentation: Equatable {
    case activating
    case background

    @MainActor
    func present(_ window: NSWindow) {
        switch self {
        case .activating:
            window.makeKeyAndOrderFront(nil)
            window.orderFrontRegardless()
            NSApp.activate(ignoringOtherApps: true)
        case .background:
            window.orderFront(nil)
        }
    }
}
```

This is an integration point, not a drop-in guarantee. Status Trio also
changes controller paths that would otherwise request activation, and
checks the actual controls through its provider. It keeps its existing
window/controllers; it does not replace every window with a special panel.

The attachment exception recognizes the observed service identifier
`com.openai.sky.CUAService`. That identifier is historical, provider-specific
evidence, not a stable universal API. Other providers and service versions
require their own capability checks and evidence.

## Project-owned launcher and observation

The project adapter connects three scripts:

| Resource | Responsibility |
| --- | --- |
| [launch-computer-use.sh](https://github.com/lingyired/status-trio/blob/67bdc1a42b0b0b2f256d095d6239728ee7732431/scripts/launch-computer-use.sh) | Require a named development branch, build through the dev-bundle route, check identity and Debug capability, and serialize launcher invocations |
| [computer-use-instance.swift](https://github.com/lingyired/status-trio/blob/67bdc1a42b0b0b2f256d095d6239728ee7732431/scripts/computer-use-instance.swift) | Check exact bundle/executable paths and arguments; reject identity collisions; launch with a token and confirm the resulting instance |
| [measure-ui-focus.swift](https://github.com/lingyired/status-trio/blob/67bdc1a42b0b0b2f256d095d6239728ee7732431/scripts/measure-ui-focus.swift) | Observe foreground applications and target windows with a hard timeout, timestamps, activation events, and actual sampling-gap reporting |

The launcher derives a development Bundle ID from the branch. Its build
checks include source HEAD, dirty state reporting, and the development
codename. It can gracefully stop only a matching owned test instance; it
rejects a non-test instance or another checkout using the same identity.
The source adapter documents the remaining LaunchServices race boundary.

The observer is an external diagnostic, not resident application polling.
It accepts a bounded duration of more than zero and at most 120 seconds.
Its foreground/window evidence does not, by itself, measure keyboard input
routing, pointer motion, or every workspace effect.

## Exercise the existing integration

Follow the project's current
[adapter](https://github.com/lingyired/status-trio/blob/67bdc1a42b0b0b2f256d095d6239728ee7732431/docs/background-computer-use-testing.md)
and its documented macOS/Xcode requirements. These are commands for a
Status Trio development checkout, not this skill repository.

1. Prepare an isolated worktree on a named development branch and identify its
   development Bundle ID. Do not use the production app or another agent's
   checkout.
2. Establish the provider's capabilities without disruptive probing. Build
   the Debug bundle without opening it if necessary, then start a bounded
   observer and confirm it is ready before launch or attachment.
3. Use the supported launcher and verify its returned PID, path, source
   identity, and actual connected displays:

   ```bash
   bash scripts/launch-computer-use.sh --display secondary
   ```

4. Confirm the trace still covers the actions after the build/launch.
   Exercise only authorized controls, navigation, and target screenshots.
   A missing secondary display is a fallback, not secondary-display coverage.
5. Record each interference dimension separately, restore only still-owned
   mutations, gracefully stop the owned test instance and observers, and
   verify cleanup.

The build can consume an observation window. An expired trace cannot cover
later actions; establish a fresh bounded trace when needed and mark any
uncovered launch/attachment separately. Do not infer zero interference from
the launch command returning successfully.

To restore normal development behavior, stop the owned test instance and
follow the project's normal launch route without test flags. The normal
foreground route remains an intentional, separate acceptance path.

## Verify the code separately from live behavior

These existing commands check the Debug/Release flag contract, launcher
fixtures, and focused configuration/controller/routing behavior:

```bash
bash scripts/test-background-ui-configuration.sh
bash scripts/test-launch-computer-use.sh
bash scripts/test.sh 'BackgroundUITestingTests|SettingsWindowControllerTests|GuideWindowLifecycleTests|DockActivationActionTests'
```

They are not live focus or input measurements. Use the project's risk-sized
local verification profile when changing that application.

## Evidence and limits

The source adapter records selected Settings and first-run guide operations
under native CU, including state changes, navigation, screenshots, and
display placement with bounded foreground observations. The integrated
acceptance matrix also contains BLOCKED and NOT RUN entries.

Text input, shortcut recording, real Dock interactions, system permission
dialogs, and unexercised controls do not inherit those results. The source
adapter identifies two Bluetooth visibility controls that explicitly activate
the app; they remain outside background checks.

The standalone skill repository has not independently repeated these live
checks. Reviewing the code, validating the package, or passing simulated
decision scenarios does not establish broader runtime compatibility.

Keep current launch and provider policy in the source project's instructions.
The reusable part is the separation of configuration, presentation, ownership,
observation, and evidence; app flags, service IDs, and control exceptions stay
project-specific.
