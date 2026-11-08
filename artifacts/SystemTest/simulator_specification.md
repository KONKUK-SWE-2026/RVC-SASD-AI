# Web-Based RVC Simulator Specification

## Execution architecture

The HTML/CSS/JavaScript UI communicates with `simulator/server.py` over a local HTTP API. The Python adapter loads `build/librvc_controller.dylib` with `ctypes` and calls the implemented C11 `rvc_controller_init` and `rvc_controller_step` functions. The UI does not implement controller decisions.

## Map and controls

- 10x10 grid, `(x,y)` coordinates `0..9`, initial default `(4,4)` facing north.
- Empty, obstacle, dust, and RVC display; obstacles and dust may overlap.
- Edit obstacle, dust, initial RVC position, or erase; choose initial direction; clear and save custom maps.
- Start, pause, single step, inspect previous/next snapshots, reset, restart, change playback delay, export trace.
- Each scenario accepts 1–100 ticks; predefined scenarios use a maximum of 8.
- A turn-side adapter convention is documented in the UI and trace; the C command remains `TURN_ASIDE`.

## Deterministic tick adapter

At a decision tick the adapter derives front/left/right obstacle and current-cell dust inputs from the map and heading, then calls the C controller once. It records the returned state and output and executes one abstract movement action. A multi-action movement sequence is continued on later ticks without another C invocation until that sequence is consumed. This is the simulator's adapter mapping, since the C interface returns a sequence rather than defining hardware timing or action-completion events.

Each history snapshot records tick, position, heading, controller state, current sensor readings, inputs sampled by C on that tick (when invoked), C movement and cleaner outputs, executed motor action, boost request, remaining sequence, map changes, timers as unavailable/TBD, transitions, and explanatory notes. Tick 0 records initialization before the first C call.

## Test oracle and limitations

Scenarios provide expected behavior and requirement references. The simulator records observations and execution history but never assigns PASS/FAIL automatically; a human evaluator records PASS, FAIL, or INCONCLUSIVE with notes. The requirements do not specify sampling cadence, turn direction, boost level/duration, or final cleaning state in the all-blocked case. Hardware drivers are outside scope. No fabricated values are shown for unavailable timers.

## Validation evidence

The simulator API is exercised by `simulator/run_system_tests.py`; every predefined scenario reloads the C controller, verifies the 10x10 grid, advances with contiguous ticks, checks valid state/position and C output presence, and preserves the full trace. Boundary checks also cover custom start/map configuration, reset restoration, the exact 100-tick stop, no further tick after the limit, and rejection of an obstacle under the initial RVC. These checks validate the adapter and trace integrity, not requirement conformance.
