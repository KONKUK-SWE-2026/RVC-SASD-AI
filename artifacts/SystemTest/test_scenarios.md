# RVC System Test Scenarios

Simulator grid: 10x10 (x,y = 0..9); default start convention: (4,4).
Each run is capped at 8 ticks (global maximum: 100). Expected behavior is for human evaluation; no automatic verdict is assigned.
Requirement references use RVC-01–RVC-07 from `docs/preliminary_requirments.md`.

## ST-01 — Clear floor baseline

- Initial position/direction: `[4, 4]` / `N`
- Obstacles: `[]`; dust: `[]`
- Tick cap: 8; executed: 5; grid: 10x10
- Essential functions: sensor inputs report a clear path, forward movement selection, automatic clean and mop output
- Preliminary requirements: RVC-01, RVC-02
- Expected behavior: With no adjacent obstacles or dust, the C controller selects forward movement and clean-and-mop behavior.
- SA artifacts: Event List, Context Diagram, DFD Levels 0–4/FSM, Data Dictionary, Process Specifications.
- Human evaluation: Pending

## ST-02 — Dust at initial position

- Initial position/direction: `[4, 4]` / `N`
- Obstacles: `[]`; dust: `[[4, 4]]`
- Tick cap: 8; executed: 5; grid: 10x10
- Essential functions: dust sensor input, five-tick boost state, forward movement and clean/mop output
- Preliminary requirements: RVC-01, RVC-02, RVC-05
- Expected behavior: Dust is detected on the first tick; Boost remains active for the five active ticks, with remaining ticks visible in the C state.
- SA artifacts: Event List, Context Diagram, DFD Levels 0–4/FSM, Data Dictionary, Process Specifications.
- Human evaluation: Pending

## ST-03 — Front obstacle

- Initial position/direction: `[4, 4]` / `N`
- Obstacles: `[[4, 3]]`; dust: `[]`
- Tick cap: 8; executed: 5; grid: 10x10
- Essential functions: front obstacle sensing, obstacle-avoidance movement sequence, stop then resume cleaning
- Preliminary requirements: RVC-01, RVC-03
- Expected behavior: The controller selects turn-aside followed by forward movement and reports stop-then-clean-and-mop behavior.
- SA artifacts: Event List, Context Diagram, DFD Levels 0–4/FSM, Data Dictionary, Process Specifications.
- Human evaluation: Pending

## ST-04 — Left obstacle

- Initial position/direction: `[4, 4]` / `N`
- Obstacles: `[[3, 4]]`; dust: `[]`
- Tick cap: 8; executed: 5; grid: 10x10
- Essential functions: left obstacle sensing, obstacle-avoidance movement sequence, cleaning response
- Preliminary requirements: RVC-01, RVC-03
- Expected behavior: Any detected obstacle selects the general avoidance sequence; the C output leaves the turn side abstract.
- SA artifacts: Event List, Context Diagram, DFD Levels 0–4/FSM, Data Dictionary, Process Specifications.
- Human evaluation: Pending

## ST-05 — Right obstacle

- Initial position/direction: `[4, 4]` / `N`
- Obstacles: `[[5, 4]]`; dust: `[]`
- Tick cap: 8; executed: 5; grid: 10x10
- Essential functions: right obstacle sensing, obstacle-avoidance movement sequence, cleaning response
- Preliminary requirements: RVC-01, RVC-03
- Expected behavior: Any detected obstacle selects the general avoidance sequence and stop-then-clean-and-mop output.
- SA artifacts: Event List, Context Diagram, DFD Levels 0–4/FSM, Data Dictionary, Process Specifications.
- Human evaluation: Pending

## ST-06 — Front and left obstacles

- Initial position/direction: `[4, 4]` / `N`
- Obstacles: `[[4, 3], [3, 4]]`; dust: `[]`
- Tick cap: 8; executed: 5; grid: 10x10
- Essential functions: multi-direction obstacle sensing, partial-obstacle classification, avoidance and cleaner outputs
- Preliminary requirements: RVC-01, RVC-03
- Expected behavior: Because fewer than all three sensed directions are blocked, the general turn-aside and forward sequence is selected.
- SA artifacts: Event List, Context Diagram, DFD Levels 0–4/FSM, Data Dictionary, Process Specifications.
- Human evaluation: Pending

## ST-07 — Front and right obstacles

- Initial position/direction: `[4, 4]` / `N`
- Obstacles: `[[4, 3], [5, 4]]`; dust: `[]`
- Tick cap: 8; executed: 5; grid: 10x10
- Essential functions: multi-direction obstacle sensing, partial-obstacle classification, avoidance and cleaner outputs
- Preliminary requirements: RVC-01, RVC-03
- Expected behavior: The partial-obstacle response is selected; the map lets the evaluator inspect the simulator's turn-side convention.
- SA artifacts: Event List, Context Diagram, DFD Levels 0–4/FSM, Data Dictionary, Process Specifications.
- Human evaluation: Pending

## ST-08 — Both sides blocked, front clear

- Initial position/direction: `[4, 4]` / `N`
- Obstacles: `[[3, 4], [5, 4]]`; dust: `[]`
- Tick cap: 8; executed: 5; grid: 10x10
- Essential functions: left/right obstacle sensing, not-all-directions classification, forward and cleaning output
- Preliminary requirements: RVC-01, RVC-02, RVC-03
- Expected behavior: The all-three-directions condition is false, so the controller selects the general obstacle response.
- SA artifacts: Event List, Context Diagram, DFD Levels 0–4/FSM, Data Dictionary, Process Specifications.
- Human evaluation: Pending

## ST-09 — Front and both sides blocked

- Initial position/direction: `[4, 4]` / `N`
- Obstacles: `[[4, 3], [3, 4], [5, 4]]`; dust: `[]`
- Tick cap: 8; executed: 6; grid: 10x10
- Essential functions: three-direction obstacle sensing, all-blocked classification, backward recovery sequence
- Preliminary requirements: RVC-03, RVC-04
- Expected behavior: The controller selects backward, turn-aside, then forward; cleaning is stopped during backward/turn and resumes during forward.
- SA artifacts: Event List, Context Diagram, DFD Levels 0–4/FSM, Data Dictionary, Process Specifications.
- Human evaluation: Pending

## ST-10 — Front obstacle with dust

- Initial position/direction: `[4, 4]` / `N`
- Obstacles: `[[4, 3]]`; dust: `[[4, 4]]`
- Tick cap: 8; executed: 6; grid: 10x10
- Essential functions: obstacle and dust sensing, obstacle response, effective boost only while cleaning
- Preliminary requirements: RVC-03, RVC-05
- Expected behavior: Cleaning power is NORMAL during the turn while cleaning is stopped, then uses the remaining Boost interval when forward cleaning resumes. The timer advances on each movement-sequence tick.
- SA artifacts: Event List, Context Diagram, DFD Levels 0–4/FSM, Data Dictionary, Process Specifications.
- Human evaluation: Pending

## ST-11 — Left obstacle with dust

- Initial position/direction: `[4, 4]` / `N`
- Obstacles: `[[3, 4]]`; dust: `[[4, 4]]`
- Tick cap: 8; executed: 6; grid: 10x10
- Essential functions: left obstacle and dust sensing, movement response, boost state and countdown
- Preliminary requirements: RVC-03, RVC-05
- Expected behavior: The C controller selects obstacle response; cleaning power is NORMAL during the turn and becomes BOOST when forward cleaning resumes if the interval remains active.
- SA artifacts: Event List, Context Diagram, DFD Levels 0–4/FSM, Data Dictionary, Process Specifications.
- Human evaluation: Pending

## ST-12 — Right obstacle with dust

- Initial position/direction: `[4, 4]` / `N`
- Obstacles: `[[5, 4]]`; dust: `[[4, 4]]`
- Tick cap: 8; executed: 6; grid: 10x10
- Essential functions: right obstacle and dust sensing, movement response, boost state and countdown
- Preliminary requirements: RVC-03, RVC-05
- Expected behavior: The C controller selects obstacle response; cleaning power is NORMAL during the turn and becomes BOOST when forward cleaning resumes if the interval remains active.
- SA artifacts: Event List, Context Diagram, DFD Levels 0–4/FSM, Data Dictionary, Process Specifications.
- Human evaluation: Pending

## ST-13 — All directions blocked with dust

- Initial position/direction: `[4, 4]` / `N`
- Obstacles: `[[4, 3], [3, 4], [5, 4]]`; dust: `[[4, 4]]`
- Tick cap: 8; executed: 6; grid: 10x10
- Essential functions: all-direction obstacle sensing, backward recovery, cleaning stop and resume, effective boost power only while cleaning
- Preliminary requirements: RVC-04, RVC-05
- Expected behavior: The timer starts on the dust tick and advances on every tick. Effective power is NORMAL during backward and turn-aside while cleaning is stopped, then BOOST during forward cleaning while the interval remains active.
- SA artifacts: Event List, Context Diagram, DFD Levels 0–4/FSM, Data Dictionary, Process Specifications.
- Human evaluation: Pending

## ST-14 — East-facing front obstacle

- Initial position/direction: `[4, 4]` / `E`
- Obstacles: `[[5, 4]]`; dust: `[]`
- Tick cap: 8; executed: 5; grid: 10x10
- Essential functions: direction-relative front sensing, obstacle response, cleaner response
- Preliminary requirements: RVC-02, RVC-03
- Expected behavior: The obstacle directly east is reported as front relative to heading; partial-obstacle movement is selected.
- SA artifacts: Event List, Context Diagram, DFD Levels 0–4/FSM, Data Dictionary, Process Specifications.
- Human evaluation: Pending

## ST-15 — South-facing front obstacle

- Initial position/direction: `[4, 4]` / `S`
- Obstacles: `[[4, 5]]`; dust: `[]`
- Tick cap: 8; executed: 5; grid: 10x10
- Essential functions: direction-relative front sensing, obstacle response, cleaner response
- Preliminary requirements: RVC-02, RVC-03
- Expected behavior: The obstacle directly south is reported as front relative to heading; partial-obstacle movement is selected.
- SA artifacts: Event List, Context Diagram, DFD Levels 0–4/FSM, Data Dictionary, Process Specifications.
- Human evaluation: Pending

## ST-16 — West-facing front obstacle

- Initial position/direction: `[4, 4]` / `W`
- Obstacles: `[[3, 4]]`; dust: `[]`
- Tick cap: 8; executed: 5; grid: 10x10
- Essential functions: direction-relative front sensing, obstacle response, cleaner response
- Preliminary requirements: RVC-02, RVC-03
- Expected behavior: The obstacle directly west is reported as front relative to heading; partial-obstacle movement is selected.
- SA artifacts: Event List, Context Diagram, DFD Levels 0–4/FSM, Data Dictionary, Process Specifications.
- Human evaluation: Pending

## ST-17 — East-facing all directions blocked

- Initial position/direction: `[4, 4]` / `E`
- Obstacles: `[[5, 4], [4, 3], [4, 5]]`; dust: `[]`
- Tick cap: 8; executed: 6; grid: 10x10
- Essential functions: rotated three-direction sensing, all-blocked classification, backward recovery
- Preliminary requirements: RVC-04, RVC-01
- Expected behavior: Front, left, and right relative to east are all blocked; backward recovery is selected.
- SA artifacts: Event List, Context Diagram, DFD Levels 0–4/FSM, Data Dictionary, Process Specifications.
- Human evaluation: Pending

## ST-18 — South-facing obstacle with dust

- Initial position/direction: `[4, 4]` / `S`
- Obstacles: `[[4, 5], [5, 4]]`; dust: `[[4, 4]]`
- Tick cap: 8; executed: 6; grid: 10x10
- Essential functions: direction-relative sensing, partial-obstacle response, dust power mode duration
- Preliminary requirements: RVC-03, RVC-05
- Expected behavior: The C controller advances the timer on every tick; the output remains NORMAL during stopped-cleaning actions and is BOOST only on active cleaning ticks.
- SA artifacts: Event List, Context Diagram, DFD Levels 0–4/FSM, Data Dictionary, Process Specifications.
- Human evaluation: Pending

## ST-19 — Dust with two side obstacles

- Initial position/direction: `[4, 4]` / `W`
- Obstacles: `[[4, 3], [4, 5]]`; dust: `[[4, 4]]`
- Tick cap: 8; executed: 6; grid: 10x10
- Essential functions: direction-relative side sensing, movement response, boost power mode
- Preliminary requirements: RVC-01, RVC-03, RVC-05
- Expected behavior: The partial obstacle turn reports NORMAL while cleaning is stopped; forward cleaning reports BOOST if the dust interval remains active.
- SA artifacts: Event List, Context Diagram, DFD Levels 0–4/FSM, Data Dictionary, Process Specifications.
- Human evaluation: Pending

## ST-20 — Dust encountered after forward movement

- Initial position/direction: `[4, 4]` / `N`
- Obstacles: `[[4, 7]]`; dust: `[[4, 3]]`
- Tick cap: 8; executed: 6; grid: 10x10
- Essential functions: repeated sensor sampling, forward movement, dust-triggered boost state
- Preliminary requirements: RVC-01, RVC-02, RVC-05
- Expected behavior: When the robot reaches the dust cell while cleaning, a subsequent tick reports dust, starts the five-tick interval, and outputs Boost. The timer advances on every later simulation tick.
- SA artifacts: Event List, Context Diagram, DFD Levels 0–4/FSM, Data Dictionary, Process Specifications.
- Human evaluation: Pending

## ST-21 — Boost refresh and normal-power recovery

- Initial position/direction: `[4, 4]` / `N`
- Obstacles: `[]`; dust: `[[4, 4], [4, 3]]`
- Tick cap: 8; executed: 8; grid: 10x10
- Essential functions: dust detection on consecutive controller decisions, five-tick boost refresh, normal-power transition after expiry
- Preliminary requirements: RVC-01, RVC-02, RVC-05
- Expected behavior: Dust is detected at the start and again on the next cell while Boost is active; the C timer refreshes to five. After dust is cleared and five active ticks elapse, the trace returns to Normal.
- SA artifacts: Event List, Context Diagram, DFD Levels 0–4/FSM, Data Dictionary, Process Specifications.
- Human evaluation: Pending
