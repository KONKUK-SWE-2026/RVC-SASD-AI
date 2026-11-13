# Process Specifications

## DFD Level 0

### Process 0 — Perform Automatic Cleaning

- **Purpose:** Automatically clean and mop household surfaces, directing movement and cleaning behavior from sensor inputs.
- **Inputs:** Obstacle Detection Input; Dust Detection Input.
- **Outputs:** Movement Command; Cleaning Control Command.
- **Trigger:** Automatic operation. A logical Simulation Tick occurs for each simulator update; wall-clock cadence is outside scope.
- **Processing logic:**
  1. Receive front/left/right obstacle detections and the current tick's dust detection.
  2. Direct forward movement and cleaning/mopping when no obstacle is detected.
  3. For a partial obstacle, direct cleaning stop, turn aside, and forward movement with cleaning.
  4. For all three specified directions blocked, stop cleaning during backward and turn-aside actions, then resume cleaning during forward movement.
  5. On each Simulation Tick, update the dust boost timer. A positive dust input sets remaining ticks to 5. With no dust, decrement a positive count once.
  6. Emit Boost only when cleaning is active and the updated count is positive; emit Normal when cleaning is stopped or the count is zero. Dust while Boost is active refreshes the timer to 5.
- **Requirements:** RVC-01–RVC-05.

## DFD Level 1

### Process 1 — Determine Movement Response

- **Purpose:** Direct movement in response to obstacle detections.
- **Inputs:** Obstacle Detection Input.
- **Outputs:** Movement Command.
- **Trigger:** Obstacle sensor snapshot during automatic operation.
- **Processing logic:** If all front/left/right are blocked, issue backward, turn-aside, forward. Else if any is blocked, issue turn-aside, forward. Otherwise issue forward. The left/right choice remains unspecified.
- **Requirements:** RVC-02–RVC-04.

### Process 2 — Control Cleaning Behavior

- **Purpose:** Direct cleaning/mopping and maintain the dust-based power mode.
- **Inputs:** Obstacle Detection Input; Dust Detection Input; internal Simulation Tick.
- **Outputs:** Cleaning Control Command.
- **Trigger:** Every simulation tick, including ticks executing a queued movement action.
- **Processing logic:** Determine the current action's cleaning activity; update D1 every tick; combine cleaning activity with the updated boost interval. Emit Boost only during active cleaning while the interval remains positive. A dust-positive tick refreshes the interval even when already Boosting.
- **Requirements:** RVC-01, RVC-03–RVC-05.

## DFD Level 2

### Process 1.1 — Classify Obstacle Condition

- **Parent:** Process 1.
- **Inputs:** Obstacle Detection Input.
- **Outputs:** Obstacle Response Condition.
- **Logic:** All three true → all-directions-blocked; any true → partial obstacle; all false → clear.
- **Requirement:** RVC-02–RVC-04.

### Process 1.2 — Issue Movement Command

- **Parent:** Process 1.
- **Inputs:** Obstacle Response Condition.
- **Outputs:** Movement Command.
- **Logic:** Clear → forward; partial → turn aside then forward; all blocked → backward, turn aside, then forward. Side selection is unspecified.
- **Requirement:** RVC-02–RVC-04.

### Process 2.1 — Determine Obstacle Cleaning Action

- **Parent:** Process 2.
- **Inputs:** Obstacle Detection Input.
- **Outputs:** Obstacle-Related Cleaning Action; Cleaning Active Indicator for the current movement-sequence action.
- **Logic:** Stop cleaning during turn-aside obstacle handling and resume while moving forward. For all-directions-blocked recovery, stop during backward and turn-aside actions, then resume while moving forward.
- **Requirements:** RVC-01, RVC-03, RVC-04.

### Process 2.2 — Maintain Dust Boost State

- **Parent:** Process 2.
- **Inputs:** Dust Detection Input; Simulation Tick; Cleaning Active Indicator; Previous Remaining Boost Ticks from D1.
- **Outputs:** Updated Remaining Boost Ticks to D1; effective Dust Power State.
- **Logic:** On dust-positive tick set count to 5. Else decrement once if positive. Report Boost only when cleaning is active and updated count >0; otherwise report Normal. This process runs every tick, regardless of whether Process 1 selects a new movement sequence.
- **Requirement:** RVC-05.

### Process 2.3 — Generate Cleaning Control Command

- **Parent:** Process 2.
- **Inputs:** Obstacle-Related Cleaning Action; effective Dust Power State.
- **Outputs:** Cleaning Control Command.
- **Logic:** Combine the obstacle cleaning action with effective Normal/Boost power mode. Do not command Boost while cleaning is stopped. Do not assign a numeric power magnitude.
- **Requirements:** RVC-01, RVC-03–RVC-05.

## DFD Level 3

### Process 1.2.1 — Select Movement Sequence

- **Parent:** Process 1.2.
- **Inputs:** Obstacle Response Condition.
- **Outputs:** Selected Movement Sequence.
- **Logic:** Clear → forward; partial → turn-aside then forward; all blocked → backward, turn-aside, forward. Left/right choice is unspecified.
- **Requirements:** RVC-02–RVC-04.

### Process 1.2.2 — Produce Movement Command

- **Parent:** Process 1.2.
- **Inputs:** Selected Movement Sequence.
- **Outputs:** Movement Command.
- **Logic:** Encode and deliver the abstract selected sequence; hardware encoding remains outside scope.
- **Requirements:** RVC-02–RVC-04.

### Process 2.2.1 — Update Dust Boost Timer State

- **Parent:** Process 2.2.
- **Inputs:** Dust Detection Input; Simulation Tick; Previous Remaining Boost Ticks from D1.
- **Outputs:** Updated Remaining Boost Ticks to D1 and Process 2.2.2.
- **Logic:** On a dust-positive tick set count to 5, including a retrigger during Boost. Otherwise decrement once when count is positive. Do not pause the count while queued movement actions execute.
- **Requirement:** RVC-05.

### Process 2.2.2 — Determine Active Power Mode

- **Parent:** Process 2.2.
- **Inputs:** Updated Remaining Boost Ticks; Cleaning Active Indicator.
- **Outputs:** Effective Dust Power State to Process 2.3.
- **Logic:** Cleaning active and count >0 → Boost; otherwise → Normal.
- **Requirement:** RVC-05.

The process interfaces and state-store interactions match DFD Levels 2–3 and the Data Dictionary. No Process Specification is generated for the Level 4 FSM itself.
