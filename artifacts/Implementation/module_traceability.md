# Implementation Module Traceability

| SD Module | C Implementation | SA Trace | Notes |
|---|---|---|---|
| Main | No platform `main()` is included | Structure Chart root | Host must call the tick API once for every simulation/control tick and request a movement decision when a prior sequence is consumed. |
| Controller | `rvc_controller_init`, `rvc_controller_step`, `rvc_controller_advance_tick` | Process 0; Movement FSM; Dust Boost Interval FSM | Owns obstacle state and the in-memory boost countdown. `advance_tick` advances it once per simulation tick and gates effective Boost by the caller's current `cleaning_active` state. |
| Determine Movement Response | `determine_movement_response` | Process 1 | Coordinates classification, sequence selection, and command production. |
| Classify Obstacle Condition | `classify_obstacle_condition` | Process 1.1 | Distinguishes clear, partial, and all-three-directions-blocked. |
| Select Movement Sequence | `select_movement_sequence` | Process 1.2.1 | Maps obstacle condition to an abstract sequence; turn side remains unspecified. |
| Produce Movement Command | `produce_movement_command` | Process 1.2.2 | Copies the selected sequence into the output command. |
| Control Cleaning Behavior | `control_cleaning_behavior` | Process 2 | Selects obstacle-related cleaning action; power state is reported alongside it. |
| Determine Obstacle Cleaning Action | `determine_obstacle_cleaning_action` | Process 2.1 | Returns the required abstract stop/resume action. |
| Update Dust Boost Timer State | `update_dust_boost_timer`, called by `rvc_controller_advance_tick` | Process 2.2.1; D1 | Dust-positive tick sets five; dust-negative tick decrements once; initialization resets to zero. |
| Determine Active Power Mode | `determine_active_power_mode` | Process 2.2.2; Dust Boost Interval FSM | Returns Boost iff cleaning is active and remaining ticks >0, else Normal. |
| Generate Cleaning Control Command | Cleaning action and power-mode output assembly in `rvc_controller_step`; power-mode state returned by `rvc_controller_advance_tick` | Process 2.3 | Movement decisions report cleaning action with the current Normal/Boost mode. Each simulation-tick call returns updated mode and remaining duration; numeric actuator level remains abstract. |

## Design Limits

- Hardware-bound `main()`, sensor acquisition, actuator APIs, and physical tick cadence are not specified and remain outside this controller library.
- The integration contract requires one `rvc_controller_advance_tick` call per logical simulation tick, even while movement sequence actions continue, and an accurate `cleaning_active` value for the current action.
- The movement command remains abstract `TURN_ASIDE`; the simulator selects a side only as an adapter convention.
- Numeric boost magnitude remains unspecified.
