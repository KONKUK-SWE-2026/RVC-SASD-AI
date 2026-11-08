# Implementation Module Traceability

| SD Module | C Implementation | SA Trace | Notes |
|---|---|---|---|
| Main | Not included in the portable controller library | Structure Chart root | The project has no defined sensor acquisition, actuator adapter, start event, or sampling loop. The preliminary requirements exclude detailed hardware controls. A platform `main()` must call `rvc_controller_step` with sensor snapshots and deliver its abstract output. |
| Controller | `rvc_controller_init`, `rvc_controller_step` in `src/rvc_controller.c` | Process 0; DFD Level 4 FSM | Coordinates movement and cleaning outputs for each supplied sensor snapshot. |
| Determine Movement Response | `determine_movement_response` | Process 1 | Coordinates obstacle classification, sequence selection, and command production. |
| Classify Obstacle Condition | `classify_obstacle_condition` | Process 1.1 | Distinguishes clear, partial obstacle, and all-three-directions-blocked conditions. |
| Select Movement Sequence | `select_movement_sequence` | Process 1.2.1 | Maps the condition to an abstract movement sequence. `TURN_ASIDE` leaves left/right selection unspecified. |
| Produce Movement Command | `produce_movement_command` | Process 1.2.2 | Copies the selected sequence into the output command. |
| Control Cleaning Behavior | `control_cleaning_behavior` | Process 2 | Combines obstacle-related cleaning action with the independent dust power request. |
| Determine Obstacle Cleaning Action | `determine_obstacle_cleaning_action` | Process 2.1 | Returns clean-and-mop, stop-then-clean-and-mop, or stop-then-unspecified. |
| Determine Dust Power Adjustment | `determine_dust_power_adjustment` | Process 2.2 | Requests a temporary boost when dust is detected; no duration is defined. |
| Generate Cleaning Control Command | Implemented in `control_cleaning_behavior` | Process 2.3 | Produces the abstract cleaning action and boost request fields. |

## Design Deviations and Limits

- The C implementation is a portable controller library. It does not provide a hardware-bound `main()` loop because the approved artifacts define neither hardware APIs nor sensor polling/start timing, and hardware-control detail is out of scope.
- The abstract `RVC_MOVE_TURN_ASIDE` command preserves the requirement to turn left or right without inventing a side-selection policy.
- The all-directions-blocked output marks the final cleaning state as unspecified, consistent with the Process Specifications.
- A dust boost request is a boolean output; boost duration and level remain unspecified.
- No hardware drivers or external libraries are added to production code.
