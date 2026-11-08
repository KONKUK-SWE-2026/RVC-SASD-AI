# System Test Execution Results

- Execution time (UTC): 2026-11-06T06:54:36.294045+00:00
- Execution path: Web simulator HTTP API -> Python ctypes -> compiled C11 controller library.
- Human test oracle: required; verdicts remain pending (no automatic PASS/FAIL).
- Existing GCC/CMake C unit suite: 10/10 passed (`ctest --test-dir build --output-on-failure`).
- Scenarios executed: 20 / 20.
- Automated harness checks: scenario loaded at tick 0; 10x10 grid; contiguous tick history; valid positions/state values; C output present; custom start/map; reset restoration; exact 100-tick stop; no tick beyond limit; invalid start overlap rejected.
- These harness checks validate simulator execution and trace integrity, not requirement conformance.

| ID | Scenario | Ticks | C decision calls | Human verdict |
|---|---|---:|---:|---|
| ST-01 | Clear floor baseline | 5 | 5 | Pending human evaluation |
| ST-02 | Dust at initial position | 5 | 5 | Pending human evaluation |
| ST-03 | Front obstacle | 5 | 4 | Pending human evaluation |
| ST-04 | Left obstacle | 5 | 4 | Pending human evaluation |
| ST-05 | Right obstacle | 5 | 4 | Pending human evaluation |
| ST-06 | Front and left obstacles | 5 | 4 | Pending human evaluation |
| ST-07 | Front and right obstacles | 5 | 4 | Pending human evaluation |
| ST-08 | Both sides blocked, front clear | 5 | 3 | Pending human evaluation |
| ST-09 | Front and both sides blocked | 6 | 3 | Pending human evaluation |
| ST-10 | Front obstacle with dust | 6 | 5 | Pending human evaluation |
| ST-11 | Left obstacle with dust | 6 | 5 | Pending human evaluation |
| ST-12 | Right obstacle with dust | 6 | 5 | Pending human evaluation |
| ST-13 | All directions blocked with dust | 6 | 3 | Pending human evaluation |
| ST-14 | East-facing front obstacle | 5 | 4 | Pending human evaluation |
| ST-15 | South-facing front obstacle | 5 | 4 | Pending human evaluation |
| ST-16 | West-facing front obstacle | 5 | 4 | Pending human evaluation |
| ST-17 | East-facing all directions blocked | 6 | 3 | Pending human evaluation |
| ST-18 | South-facing obstacle with dust | 6 | 5 | Pending human evaluation |
| ST-19 | Dust with two side obstacles | 6 | 4 | Pending human evaluation |
| ST-20 | Dust encountered after forward movement | 6 | 6 | Pending human evaluation |

## Limitations and observations

- Left/right choice for `TURN_ASIDE` is supplied by the simulator adapter (left if open, otherwise right); it is not a C controller requirement.
- Power-boost duration and turn timing are not specified in the approved requirements/controller interface and are shown as TBD.
- Final cleaning behavior in the all-directions-blocked sequence is unspecified; the trace preserves that state.
- No hardware drivers are present; sensor input and abstract motor/cleaner actions are represented on the grid.
- Human review is needed to assign a verdict to each execution trace.

Full per-tick records: `execution_traces.json`.
