# Example project adapter

This is an illustrative adapter for a hypothetical app named ExampleDesk.
It declares the information a real project must supply; it does not provide
an executable launcher or assert any runtime capability.

## Identity and launch

Use only the project's development test build, its separate preference
domain, and the returned executable path/PID. The project launcher must
reject production identity and existing non-test instances before building
or attaching. Record build commit and dirty state.

For a real app, name its existing launch command here and explain its
supported background mode and display placement. If no such route exists,
launch is BLOCKED until a scoped integration or isolated calibration is
authorized. Never infer a flag from another project.

## Provider and observation

Select a provider exposed to this session that meets the capability record.
An installation on disk is not sufficient. Document whether attachment can
reopen or activate the app before attempting it.

The project's external observer must have a hard deadline, target identity,
clock basis, output path, owner, and stop method. Identify which of foreground
activation, input focus, pointer, and workspace it actually observes.

## Actions and results

For an authorized interactive task, check one reversible control and the
relevant navigation, then capture the target window through the approved
provider. Verify actual state. For read-only tasks, omit mutations.

List known activating controls explicitly and stop those steps. Keep system
permissions and foreground acceptance separate. A missing secondary display
is a recorded placement gap, not a successful secondary-display test.

## Cleanup

Restore only mutations still owned by the run. Preserve later user changes
or unknown ownership and record restoration as BLOCKED. Stop and verify exit
of only owned test processes and observers.

Put real commands and known exceptions in the project's own adapter, and
reference the installed skill from its actual instruction entry point.
