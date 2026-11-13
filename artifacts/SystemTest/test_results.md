# System Test Execution Results

- Execution time (UTC): 2026-11-13T04:44:54.042812+00:00
- Execution path: Web simulator HTTP API -> Python ctypes -> compiled C11 controller library.
- Human test oracle: required; verdicts remain pending (no automatic PASS/FAIL).
- GCC/CMake C unit suite: 15/15 passed (`ctest --test-dir build --output-on-failure`).
- Scenarios executed: 21 / 21.
- Automated simulator checks: scenario load; 10x10 grid; contiguous histories; C output presence; timer update on each tick; C cleaning/power-state consistency; custom map and reset; 100-tick stop; invalid start overlap rejected.
- These harness checks validate simulator execution and trace integrity, not requirement conformance.

| ID | Scenario | Ticks | Movement decisions | Power modes observed | Human verdict |
|---|---|---:|---|---|---|
| ST-01 | Clear floor baseline | 5 | 5 | NORMAL | Pending human evaluation |
| ST-02 | Dust at initial position | 5 | 5 | BOOST | Pending human evaluation |
| ST-03 | Front obstacle | 5 | 4 | NORMAL | Pending human evaluation |
| ST-04 | Left obstacle | 5 | 4 | NORMAL | Pending human evaluation |
| ST-05 | Right obstacle | 5 | 4 | NORMAL | Pending human evaluation |
| ST-06 | Front and left obstacles | 5 | 4 | NORMAL | Pending human evaluation |
| ST-07 | Front and right obstacles | 5 | 4 | NORMAL | Pending human evaluation |
| ST-08 | Both sides blocked, front clear | 5 | 3 | NORMAL | Pending human evaluation |
| ST-09 | Front and both sides blocked | 6 | 3 | NORMAL | Pending human evaluation |
| ST-10 | Front obstacle with dust | 6 | 5 | NORMAL, BOOST | Pending human evaluation |
| ST-11 | Left obstacle with dust | 6 | 5 | NORMAL, BOOST | Pending human evaluation |
| ST-12 | Right obstacle with dust | 6 | 5 | NORMAL, BOOST | Pending human evaluation |
| ST-13 | All directions blocked with dust | 6 | 3 | NORMAL, BOOST | Pending human evaluation |
| ST-14 | East-facing front obstacle | 5 | 4 | NORMAL | Pending human evaluation |
| ST-15 | South-facing front obstacle | 5 | 4 | NORMAL | Pending human evaluation |
| ST-16 | West-facing front obstacle | 5 | 4 | NORMAL | Pending human evaluation |
| ST-17 | East-facing all directions blocked | 6 | 3 | NORMAL | Pending human evaluation |
| ST-18 | South-facing obstacle with dust | 6 | 5 | NORMAL, BOOST | Pending human evaluation |
| ST-19 | Dust with two side obstacles | 6 | 4 | NORMAL, BOOST | Pending human evaluation |
| ST-20 | Dust encountered after forward movement | 6 | 6 | NORMAL, BOOST | Pending human evaluation |
| ST-21 | Boost refresh and normal-power recovery | 8 | 8 | BOOST, NORMAL | Pending human evaluation |

## Limitations and observations

- Left/right choice for `TURN_ASIDE` is supplied by the simulator adapter (left if open, otherwise right); it is not a C controller requirement.
- Boost timer is implemented in the C controller and advances on every simulation tick; the boost magnitude remains abstract because no numeric level was specified.
- ST-13 confirms NORMAL output during backward/turn cleaning stops, then BOOST during forward cleaning while the interval remains active.
- No hardware drivers are present; sensor input and abstract motor/cleaner actions are represented on the grid.
- Human review is needed to assign a verdict to each execution trace.

Full per-tick records: `execution_traces.json`.
