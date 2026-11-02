# Illustrative run report

All identities, timings, evidence paths, and outcomes below are synthetic.
This example does not establish runtime compatibility.

```text
Run: example-001
Target: ExampleDesk dev build, PID 4242, commit <record real commit>
Harness: ExampleProvider <record version>, remote AX input
Environment: macOS <record version>, one display, no secondary requested
Observation: monotonic t=0..60 seconds, foreground events and samples
             actual maximum sampling gap 32 ms; logs/example-001.jsonl
Action A1: target PID 4242, t=10..11, authorized toggle false -> true
Action A2: target PID 4242, t=15..16, intended page visibly reached
Action A3: target PID 4242, t=18, target-window screenshot captured
Functional result: PASS for A1/A2/A3 with matching state evidence
Foreground activation: PASS for t=0..60 within observer resolution
Input focus: BLOCKED; observer cannot measure input routing
Pointer: BLOCKED; no pointer observer available
Workspace: BLOCKED; no workspace observer available
Overall requested non-interference acceptance: BLOCKED by missing dimensions
Cleanup: observer exited at deadline; owned test instance stopped
         restoration BLOCKED because later user mutation owns the value
```

Do not collapse this example into an unqualified "background PASS." The
foreground evidence covers one dimension for a bounded interval.

If an action occurs at t=75, its interference measurement is NOT RUN because
the trace ended at t=60. A new bounded trace may observe the same still-owned
instance; there is no need to restart the app merely to get a new recording.

The exact outcome of a user change can differ from this example. Record the
actual ownership evidence instead of inferring ownership from equal values.
