# Web-Based RVC Simulator Specification — Dust Boost State

## Execution architecture

The HTML/CSS/JavaScript UI communicates with `simulator/server.py` over a local HTTP API. Python `ctypes` loads `build/librvc_controller.dylib`; the C11 controller performs movement decisions and maintains the boost countdown. JavaScript contains no controller decision logic.

## Tick and C interface mapping

A simulation tick is one call to the server's `/api/tick`. On every tick the adapter derives the current dust sensor value and calls C `rvc_controller_advance_tick`, even when a movement sequence still has queued actions. If no movement action is queued, the adapter also calls `rvc_controller_step` to select a fresh movement sequence. It executes one queued action and records the combined cleaner action and current power mode.

Each dust-positive tick initializes or refreshes the five-tick interval. The interval decrements on every later simulation tick, including movement-sequence continuation ticks and ticks while cleaning is stopped. Effective output is `BOOST` only when the current action is cleaning and the interval remains positive; stopped-cleaning actions report `NORMAL`. RVC-04 recovery stops cleaning during backward/turn actions and resumes during forward movement. Power magnitude remains abstract.

## Map, controls, and inspection

- 10x10 map, coordinates 0..9, default start `(4,4)` facing north.
- Obstacles, dust, RVC location and heading; editable obstacles, dust, start position, and heading.
- Start, pause, single step, history navigation, reset, restart, playback speed, custom-map save, and trace export.
- Scenario limit is configurable from 1 to 100 ticks.
- Every snapshot includes position, heading, obstacle/dust sensors, movement decision status, C-selected sequence, current cleaner action, power mode, remaining boost ticks, movement sequence progress, map changes, controller state, and transition notes. Timers not implemented in C remain marked TBD.

The turn-side selection remains a deterministic adapter convention (left when open, otherwise right); it is not C controller policy.

## System testing and limits

The 21 scenarios are requirement-traceable and use the actual compiled C implementation. Execution history is saved in `artifacts/SystemTest/execution_traces.json`. The test oracle remains human; no scenario receives automatic PASS or FAIL. Automated checks validate simulator integration, history, C cleaning-action/power-mode consistency, and tick limits, not scenario verdicts. Hardware drivers and numeric power levels remain outside scope. The turn-side rule remains unspecified.
