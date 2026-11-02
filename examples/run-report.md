# Illustrative background-execution note

All identities, timings, evidence paths, and outcomes below are synthetic.
This example does not establish runtime compatibility. It illustrates a note
alongside an existing project report, not a test plan or required format.

```text
Run: example-001
Target: ExampleDesk test target, PID 4242
Harness: ExampleProvider <record version>, remote AX input
Environment: macOS <record version>, one display, no secondary requested
Observation: monotonic t=0..60 seconds, foreground events and samples
             actual maximum sampling gap 32 ms; logs/example-001.jsonl
Workload: the project's existing CU steps ran at t=10..18
Project result: refer to the project's own test report and criteria
Foreground activation: none observed for t=0..60 within observer resolution
Input focus: could not be measured; observer cannot measure input routing
Pointer: could not be measured; no pointer observer available
Clipboard: could not be measured; no clipboard observer available
Workspace: could not be measured; no workspace observer available
Overall requested non-interference acceptance: not established; dimensions unmeasured
Cleanup: observer exited at deadline; owned test instance stopped
         restoration withheld because later user mutation owns the value
```

Do not collapse this example into an unqualified background success claim. The
foreground evidence covers one dimension for a bounded interval.

If an action occurs at t=75, state that its interference was not measured
because the trace ended at t=60. A new bounded trace may observe the same
still-owned instance; there is no need to restart merely to get a new recording.

Use the project's cleanup procedure and actual ownership evidence.
