# RVC System Test Scenarios

Simulator grid: 10x10 (x,y = 0..9); default start convention: (4,4).
Each run is capped at 8 ticks (global maximum: 100). Expected behavior is for human evaluation; no automatic verdict is assigned.
Requirement references below use the numbered bullets in `docs/preliminary_requirments.md` because that source has no stable REQ identifiers.

## ST-01 — Clear floor baseline

- Initial position/direction: `[4, 4]` / `N`
- Obstacles: `[]`; dust: `[]`
- Tick cap: 8; executed: 5
- Essential functions: sensor inputs report a clear path, forward movement selection, automatic clean and mop output
- Preliminary requirements: Preliminary bullet 1, Preliminary bullet 2
- Expected behavior: With no adjacent obstacles or dust, the C controller selects forward movement and clean-and-mop behavior.
- SA artifacts: Event List, Context Diagram, DFD Levels 0–4/FSM, Data Dictionary, Process Specifications.
- Human evaluation: Pending

## ST-02 — Dust at initial position

- Initial position/direction: `[4, 4]` / `N`
- Obstacles: `[]`; dust: `[[4, 4]]`
- Tick cap: 8; executed: 5
- Essential functions: dust sensor input, forward movement selection, clean and mop with boost request
- Preliminary requirements: Preliminary bullet 1, Preliminary bullet 2, Preliminary bullet 5
- Expected behavior: The controller selects forward movement and clean-and-mop behavior and requests temporary power increase when dust is detected.
- SA artifacts: Event List, Context Diagram, DFD Levels 0–4/FSM, Data Dictionary, Process Specifications.
- Human evaluation: Pending

## ST-03 — Front obstacle

- Initial position/direction: `[4, 4]` / `N`
- Obstacles: `[[4, 3]]`; dust: `[]`
- Tick cap: 8; executed: 5
- Essential functions: front obstacle sensing, obstacle-avoidance movement sequence, stop then resume cleaning
- Preliminary requirements: Preliminary bullet 1, Preliminary bullet 3
- Expected behavior: The controller selects turn-aside followed by forward movement and reports stop-then-clean-and-mop behavior.
- SA artifacts: Event List, Context Diagram, DFD Levels 0–4/FSM, Data Dictionary, Process Specifications.
- Human evaluation: Pending

## ST-04 — Left obstacle

- Initial position/direction: `[4, 4]` / `N`
- Obstacles: `[[3, 4]]`; dust: `[]`
- Tick cap: 8; executed: 5
- Essential functions: left obstacle sensing, obstacle-avoidance movement sequence, cleaning response
- Preliminary requirements: Preliminary bullet 1, Preliminary bullet 3
- Expected behavior: Any detected obstacle selects the general avoidance sequence; the C output leaves the turn side abstract.
- SA artifacts: Event List, Context Diagram, DFD Levels 0–4/FSM, Data Dictionary, Process Specifications.
- Human evaluation: Pending

## ST-05 — Right obstacle

- Initial position/direction: `[4, 4]` / `N`
- Obstacles: `[[5, 4]]`; dust: `[]`
- Tick cap: 8; executed: 5
- Essential functions: right obstacle sensing, obstacle-avoidance movement sequence, cleaning response
- Preliminary requirements: Preliminary bullet 1, Preliminary bullet 3
- Expected behavior: Any detected obstacle selects the general avoidance sequence and stop-then-clean-and-mop output.
- SA artifacts: Event List, Context Diagram, DFD Levels 0–4/FSM, Data Dictionary, Process Specifications.
- Human evaluation: Pending

## ST-06 — Front and left obstacles

- Initial position/direction: `[4, 4]` / `N`
- Obstacles: `[[4, 3], [3, 4]]`; dust: `[]`
- Tick cap: 8; executed: 5
- Essential functions: multi-direction obstacle sensing, partial-obstacle classification, avoidance and cleaner outputs
- Preliminary requirements: Preliminary bullet 1, Preliminary bullet 3
- Expected behavior: Because fewer than all three sensed directions are blocked, the general turn-aside and forward sequence is selected.
- SA artifacts: Event List, Context Diagram, DFD Levels 0–4/FSM, Data Dictionary, Process Specifications.
- Human evaluation: Pending

## ST-07 — Front and right obstacles

- Initial position/direction: `[4, 4]` / `N`
- Obstacles: `[[4, 3], [5, 4]]`; dust: `[]`
- Tick cap: 8; executed: 5
- Essential functions: multi-direction obstacle sensing, partial-obstacle classification, avoidance and cleaner outputs
- Preliminary requirements: Preliminary bullet 1, Preliminary bullet 3
- Expected behavior: The partial-obstacle response is selected; the map lets the evaluator inspect the simulator's turn-side convention.
- SA artifacts: Event List, Context Diagram, DFD Levels 0–4/FSM, Data Dictionary, Process Specifications.
- Human evaluation: Pending

## ST-08 — Both sides blocked, front clear

- Initial position/direction: `[4, 4]` / `N`
- Obstacles: `[[3, 4], [5, 4]]`; dust: `[]`
- Tick cap: 8; executed: 5
- Essential functions: left/right obstacle sensing, not-all-directions classification, forward and cleaning output
- Preliminary requirements: Preliminary bullet 1, Preliminary bullet 2, Preliminary bullet 3
- Expected behavior: The all-three-directions condition is false, so the controller selects the general obstacle response.
- SA artifacts: Event List, Context Diagram, DFD Levels 0–4/FSM, Data Dictionary, Process Specifications.
- Human evaluation: Pending

## ST-09 — Front and both sides blocked

- Initial position/direction: `[4, 4]` / `N`
- Obstacles: `[[4, 3], [3, 4], [5, 4]]`; dust: `[]`
- Tick cap: 8; executed: 6
- Essential functions: three-direction obstacle sensing, all-blocked classification, backward recovery sequence
- Preliminary requirements: Preliminary bullet 3, Preliminary bullet 4
- Expected behavior: The controller selects backward, turn-aside, then forward and reports the final cleaning state as unspecified.
- SA artifacts: Event List, Context Diagram, DFD Levels 0–4/FSM, Data Dictionary, Process Specifications.
- Human evaluation: Pending

## ST-10 — Front obstacle with dust

- Initial position/direction: `[4, 4]` / `N`
- Obstacles: `[[4, 3]]`; dust: `[[4, 4]]`
- Tick cap: 8; executed: 6
- Essential functions: obstacle and dust sensing, avoidance sequence, independent cleaning and boost outputs
- Preliminary requirements: Preliminary bullet 3, Preliminary bullet 5
- Expected behavior: The movement response is obstacle avoidance and the C output independently requests a dust power boost; priority is not defined.
- SA artifacts: Event List, Context Diagram, DFD Levels 0–4/FSM, Data Dictionary, Process Specifications.
- Human evaluation: Pending

## ST-11 — Left obstacle with dust

- Initial position/direction: `[4, 4]` / `N`
- Obstacles: `[[3, 4]]`; dust: `[[4, 4]]`
- Tick cap: 8; executed: 6
- Essential functions: left obstacle and dust sensing, movement response, cleaner boost request
- Preliminary requirements: Preliminary bullet 3, Preliminary bullet 5
- Expected behavior: The C controller selects partial-obstacle movement and requests temporary power increase for the detected dust.
- SA artifacts: Event List, Context Diagram, DFD Levels 0–4/FSM, Data Dictionary, Process Specifications.
- Human evaluation: Pending

## ST-12 — Right obstacle with dust

- Initial position/direction: `[4, 4]` / `N`
- Obstacles: `[[5, 4]]`; dust: `[[4, 4]]`
- Tick cap: 8; executed: 6
- Essential functions: right obstacle and dust sensing, movement response, cleaner boost request
- Preliminary requirements: Preliminary bullet 3, Preliminary bullet 5
- Expected behavior: The C controller selects partial-obstacle movement and requests temporary power increase for the detected dust.
- SA artifacts: Event List, Context Diagram, DFD Levels 0–4/FSM, Data Dictionary, Process Specifications.
- Human evaluation: Pending

## ST-13 — All directions blocked with dust

- Initial position/direction: `[4, 4]` / `N`
- Obstacles: `[[4, 3], [3, 4], [5, 4]]`; dust: `[[4, 4]]`
- Tick cap: 8; executed: 6
- Essential functions: all-direction obstacle sensing, backward recovery, dust boost request
- Preliminary requirements: Preliminary bullet 4, Preliminary bullet 5
- Expected behavior: The controller selects backward recovery and reports the boost request; cleaning behavior in this combined case requires human evaluation.
- SA artifacts: Event List, Context Diagram, DFD Levels 0–4/FSM, Data Dictionary, Process Specifications.
- Human evaluation: Pending

## ST-14 — East-facing front obstacle

- Initial position/direction: `[4, 4]` / `E`
- Obstacles: `[[5, 4]]`; dust: `[]`
- Tick cap: 8; executed: 5
- Essential functions: direction-relative front sensing, obstacle response, cleaner response
- Preliminary requirements: Preliminary bullet 2, Preliminary bullet 3
- Expected behavior: The obstacle directly east is reported as front relative to heading; partial-obstacle movement is selected.
- SA artifacts: Event List, Context Diagram, DFD Levels 0–4/FSM, Data Dictionary, Process Specifications.
- Human evaluation: Pending

## ST-15 — South-facing front obstacle

- Initial position/direction: `[4, 4]` / `S`
- Obstacles: `[[4, 5]]`; dust: `[]`
- Tick cap: 8; executed: 5
- Essential functions: direction-relative front sensing, obstacle response, cleaner response
- Preliminary requirements: Preliminary bullet 2, Preliminary bullet 3
- Expected behavior: The obstacle directly south is reported as front relative to heading; partial-obstacle movement is selected.
- SA artifacts: Event List, Context Diagram, DFD Levels 0–4/FSM, Data Dictionary, Process Specifications.
- Human evaluation: Pending

## ST-16 — West-facing front obstacle

- Initial position/direction: `[4, 4]` / `W`
- Obstacles: `[[3, 4]]`; dust: `[]`
- Tick cap: 8; executed: 5
- Essential functions: direction-relative front sensing, obstacle response, cleaner response
- Preliminary requirements: Preliminary bullet 2, Preliminary bullet 3
- Expected behavior: The obstacle directly west is reported as front relative to heading; partial-obstacle movement is selected.
- SA artifacts: Event List, Context Diagram, DFD Levels 0–4/FSM, Data Dictionary, Process Specifications.
- Human evaluation: Pending

## ST-17 — East-facing all directions blocked

- Initial position/direction: `[4, 4]` / `E`
- Obstacles: `[[5, 4], [4, 3], [4, 5]]`; dust: `[]`
- Tick cap: 8; executed: 6
- Essential functions: rotated three-direction sensing, all-blocked classification, backward recovery
- Preliminary requirements: Preliminary bullet 4, Preliminary bullet 1
- Expected behavior: Front, left, and right relative to east are all blocked; backward recovery is selected.
- SA artifacts: Event List, Context Diagram, DFD Levels 0–4/FSM, Data Dictionary, Process Specifications.
- Human evaluation: Pending

## ST-18 — South-facing obstacle with dust

- Initial position/direction: `[4, 4]` / `S`
- Obstacles: `[[4, 5], [5, 4]]`; dust: `[[4, 4]]`
- Tick cap: 8; executed: 6
- Essential functions: direction-relative sensing, partial-obstacle classification, dust boost request
- Preliminary requirements: Preliminary bullet 3, Preliminary bullet 5
- Expected behavior: The side obstacle keeps this out of the all-blocked case; dust detection requests temporary power increase.
- SA artifacts: Event List, Context Diagram, DFD Levels 0–4/FSM, Data Dictionary, Process Specifications.
- Human evaluation: Pending

## ST-19 — Dust with two side obstacles

- Initial position/direction: `[4, 4]` / `W`
- Obstacles: `[[4, 3], [4, 5]]`; dust: `[[4, 4]]`
- Tick cap: 8; executed: 6
- Essential functions: direction-relative side sensing, movement response, cleaning and boost request
- Preliminary requirements: Preliminary bullet 1, Preliminary bullet 3, Preliminary bullet 5
- Expected behavior: The two side obstacles do not meet the all-three condition; the controller selects general avoidance and requests a dust boost.
- SA artifacts: Event List, Context Diagram, DFD Levels 0–4/FSM, Data Dictionary, Process Specifications.
- Human evaluation: Pending

## ST-20 — Dust encountered after forward movement

- Initial position/direction: `[4, 4]` / `N`
- Obstacles: `[[4, 7]]`; dust: `[[4, 3]]`
- Tick cap: 8; executed: 6
- Essential functions: repeated sensor sampling, forward movement, dust-triggered boost
- Preliminary requirements: Preliminary bullet 1, Preliminary bullet 2, Preliminary bullet 5
- Expected behavior: After moving forward onto the dust cell, a subsequent C-controller decision should report dust and request temporary power increase.
- SA artifacts: Event List, Context Diagram, DFD Levels 0–4/FSM, Data Dictionary, Process Specifications.
- Human evaluation: Pending
