# Example project adapter

This is an illustrative adapter for a hypothetical app named ExampleDesk.
Adapt it to the existing project instructions; it is not a mandatory checklist
and supplies no launcher, test plan, or runtime capability.

## Existing workload

Reference the project's task or test procedure if available. Its agent and
tools determine cases, steps, assertions, functional acceptance, and reporting.
An existing suite is not required. This adapter supplies only background
execution information and must not add probe tests or reset procedures.

## Identity and lifecycle

Identify the authorized test target, relevant state separation, and resources
the run may create, use, and release. For a desktop
app this may be an executable path/PID and test data directory; for a web app
it may be a dedicated browser context and test account. A separate context
does not prove that backend data or other shared resources are isolated.

Name the existing launch or connection route and its assessed background
behavior. A supported packaged build or already-running owned test context
may be sufficient; a new launcher or development identity is optional.
If the route cannot safely select a test target, explain that gap before
proceeding. Never infer a flag from another project.

## Provider and observation

Select a provider exposed to this session that meets the capability record.
An installation on disk is not sufficient. Document whether attachment can
reopen or activate the app before attempting it.

Use existing project or harness observations if suitable. Bound coverage by
target identity, start/deadline, clock basis, evidence location, and owner;
an external observer or new output file is optional. Any observer started by
the run needs a hard timeout and stop method. Identify which of foreground
activation, input focus, pointer, and workspace it actually observes.

## Background limits

Record known disruptive routes relevant to the supplied workload and stop
before invoking them. Describe assessed fallback options without silently
changing the tests or taking foreground control. If display placement is
requested, document a supported route and any missing-display fallback.

Use the existing test report to explain interference coverage and limitations.
Functional results remain those of the project's test procedure.

## Cleanup

Restore only mutations still owned by the run. Preserve later user changes
or unknown ownership and explain why restoration was withheld. Release and
verify only resources within the run's cleanup scope: for example, close its
browser context rather than the shared browser. Preserve pre-existing test
targets unless stopping them is within that scope.

Put real commands and known exceptions in the project's own adapter, and
reference the installed skill from its actual instruction entry point.
