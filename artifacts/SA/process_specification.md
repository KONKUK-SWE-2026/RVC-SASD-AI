# Process Specifications

## DFD Level 0

### Process 0 — Perform Automatic Cleaning

#### Process Identification

| Field | Description |
|---|---|
| Process ID | 0 |
| Process Name | Perform Automatic Cleaning |
| DFD Level | Level 0 |
| Parent Process | None — system process |

#### Purpose
Automatically clean and mop the household surface while directing RVC movement and cleaning behavior in response to obstacle and dust detections.

#### Inputs
- Obstacle Detection Input
- Dust Detection Input

#### Outputs
- Movement Command
- Cleaning Control Command

#### Trigger / Execution Condition
The function operates automatically. The requirements do not specify an external start trigger, sampling interval, or execution schedule.

#### Processing Logic
1. Receive obstacle detections for the front, left, and right directions and dust detection from Sensors.
2. During automatic cleaning, direct forward movement and cleaning/mopping.
3. If an obstacle is detected, direct cleaning to stop and direct the RVC to turn aside left or right, then move forward with cleaning.
4. If obstacles are detected in the front, left, and right directions, direct the RVC to move backward, turn aside left or right, and then move forward. The requirements do not explicitly state the cleaning state during this final forward movement.
5. If dust is detected, direct cleaning power to increase temporarily. The duration and power level are unspecified.

The requirements do not define how a left/right turn is selected, how simultaneous dust and obstacle detections are prioritized, or the exact timing of sensor evaluation and cleaning commands.

#### Relevant Requirements
- Preliminary requirements, bullet 1: automatic cleaning and mopping.
- Preliminary requirements, bullet 2: forward movement while cleaning.
- Preliminary requirements, bullets 3–4: obstacle response and all-directions-blocked response.
- Preliminary requirements, bullet 5: temporarily increase cleaning power when dust is detected.

## DFD Level 1

### Process 1 — Determine Movement Response

#### Process Identification

| Field | Description |
|---|---|
| Process ID | 1 |
| Process Name | Determine Movement Response |
| DFD Level | Level 1 |
| Parent Process | 0 — Perform Automatic Cleaning |

#### Purpose
Direct RVC movement in response to obstacle detections.

#### Inputs
- Obstacle Detection Input

#### Outputs
- Movement Command

#### Trigger / Execution Condition
During automatic cleaning and when obstacle detections are received. The requirements do not specify the sensor sampling interval.

#### Processing Logic
1. Receive obstacle detections for the front, left, and right directions.
2. If obstacles are detected in all three directions, direct the RVC to move backward, turn aside left or right, and then move forward.
3. Otherwise, if an obstacle is detected, direct the RVC to turn aside left or right and then move forward.
4. If no obstacle is detected, direct the RVC to move forward.

The requirements do not specify how to choose left or right. The all-three-directions-blocked case uses the separately stated backward response.

#### Relevant Requirements
- Preliminary requirements, bullet 2: move forward while cleaning.
- Preliminary requirements, bullets 3–4: turn aside on obstacle detection and move backward when the front, left, and right are blocked.

### Process 2 — Control Cleaning Behavior

#### Process Identification

| Field | Description |
|---|---|
| Process ID | 2 |
| Process Name | Control Cleaning Behavior |
| DFD Level | Level 1 |
| Parent Process | 0 — Perform Automatic Cleaning |

#### Purpose
Direct cleaning and mopping during automatic operation, including the stated obstacle response and temporary cleaning power increase for dust.

#### Inputs
- Obstacle Detection Input
- Dust Detection Input

#### Outputs
- Cleaning Control Command

#### Trigger / Execution Condition
During automatic cleaning and when obstacle or dust detections are received. The requirements do not specify the sensor sampling interval.

#### Processing Logic
1. During automatic cleaning, direct cleaning and mopping.
2. When an obstacle is detected, direct cleaning to stop during obstacle handling; for the general avoidance case, direct cleaning to resume as the RVC goes forward with cleaning.
3. When dust is detected, direct cleaning power to increase for a while.

The requirements do not specify how obstacle handling and dust detection are prioritized when simultaneous, how long cleaning power is increased, or whether cleaning is active during the final forward movement in the all-three-directions-blocked case.

#### Relevant Requirements
- Preliminary requirements, bullet 1: automatically clean and mop.
- Preliminary requirements, bullet 3: stop cleaning during obstacle handling and resume cleaning while moving forward.
- Preliminary requirements, bullet 5: increase cleaning power temporarily when dust is detected.

## DFD Level 2

### Process 1.1 — Classify Obstacle Condition

#### Process Identification

| Field | Description |
|---|---|
| Process ID | 1.1 |
| Process Name | Classify Obstacle Condition |
| DFD Level | Level 2 |
| Parent Process | 1 — Determine Movement Response |

#### Purpose
Classify the obstacle sensor results into conditions needed to select the movement response stated in the requirements.

#### Inputs
- Obstacle Detection Input

#### Outputs
- Obstacle Response Condition

#### Trigger / Execution Condition
When obstacle detections are received during automatic cleaning.

#### Processing Logic
1. Examine the reported front, left, and right obstacle detections.
2. If all three directions report obstacles, output the all-three-directions-blocked condition.
3. Otherwise, if any obstacle is reported, output the obstacle-detected condition.
4. If no obstacle is reported, output the no-obstacle condition.

#### Relevant Requirements
- Preliminary requirements, bullets 2–4.

### Process 1.2 — Issue Movement Command

#### Process Identification

| Field | Description |
|---|---|
| Process ID | 1.2 |
| Process Name | Issue Movement Command |
| DFD Level | Level 2 |
| Parent Process | 1 — Determine Movement Response |

#### Purpose
Produce movement commands based on the classified obstacle condition.

#### Inputs
- Obstacle Response Condition

#### Outputs
- Movement Command

#### Trigger / Execution Condition
When an Obstacle Response Condition is received.

#### Processing Logic
1. For the no-obstacle condition, direct forward movement.
2. For the obstacle-detected condition, direct a left or right turn aside, then forward movement.
3. For the all-three-directions-blocked condition, direct backward movement, a left or right turn aside, then forward movement.

The requirements do not specify how to choose left or right.

#### Relevant Requirements
- Preliminary requirements, bullets 2–4.

### Process 2.1 — Determine Obstacle Cleaning Action

#### Process Identification

| Field | Description |
|---|---|
| Process ID | 2.1 |
| Process Name | Determine Obstacle Cleaning Action |
| DFD Level | Level 2 |
| Parent Process | 2 — Control Cleaning Behavior |

#### Purpose
Determine the cleaning actions required by obstacle handling.

#### Inputs
- Obstacle Detection Input

#### Outputs
- Obstacle-Related Cleaning Action

#### Trigger / Execution Condition
When obstacle detections are received during automatic cleaning.

#### Processing Logic
1. If an obstacle is detected, direct cleaning to stop during obstacle handling.
2. For the general avoidance case, indicate that cleaning resumes during the following forward movement, as stated in the requirements.
3. For the all-three-directions-blocked case, preserve the stated movement-specific response. The requirements do not clarify whether the general stop/resume cleaning behavior also applies to this case, including its final forward movement.

#### Relevant Requirements
- Preliminary requirements, bullets 1, 3, and 4.

### Process 2.2 — Determine Dust Power Adjustment

#### Process Identification

| Field | Description |
|---|---|
| Process ID | 2.2 |
| Process Name | Determine Dust Power Adjustment |
| DFD Level | Level 2 |
| Parent Process | 2 — Control Cleaning Behavior |

#### Purpose
Determine whether dust detection calls for temporarily increased cleaning power.

#### Inputs
- Dust Detection Input

#### Outputs
- Dust Power Adjustment

#### Trigger / Execution Condition
When a dust detection result is received during automatic cleaning.

#### Processing Logic
1. If dust is detected, output a request to increase cleaning power temporarily.
2. If dust is not detected, output no dust-related power increase request.

The requirements do not specify the power level or duration.

#### Relevant Requirements
- Preliminary requirements, bullet 5.

### Process 2.3 — Generate Cleaning Control Command

#### Process Identification

| Field | Description |
|---|---|
| Process ID | 2.3 |
| Process Name | Generate Cleaning Control Command |
| DFD Level | Level 2 |
| Parent Process | 2 — Control Cleaning Behavior |

#### Purpose
Produce the cleaning control command for automatic cleaning and mopping, applying obstacle-related cleaning actions and any requested dust-related power increase.

#### Inputs
- Obstacle-Related Cleaning Action
- Dust Power Adjustment

#### Outputs
- Cleaning Control Command

#### Trigger / Execution Condition
During automatic cleaning. The requirements do not define sensor sampling, input update timing, or synchronization.

#### Processing Logic
1. Direct automatic cleaning and mopping as the stated baseline behavior.
2. Apply the specified stop/resume action from Obstacle-Related Cleaning Action. Preserve as unspecified the cleaning state during the final forward movement in the all-three-directions-blocked case.
3. Apply a temporary cleaning power increase when Dust Power Adjustment requests it.

The requirements do not specify how simultaneous obstacle-related actions and dust-related power increases are prioritized or combined, or the cleaning state during the final forward movement in the all-three-directions-blocked case.

#### Relevant Requirements
- Preliminary requirements, bullets 1, 3–5.

## DFD Level 3

### Process 1.2.1 — Select Movement Sequence

#### Process Identification

| Field | Description |
|---|---|
| Process ID | 1.2.1 |
| Process Name | Select Movement Sequence |
| DFD Level | Level 3 |
| Parent Process | 1.2 — Issue Movement Command |

#### Purpose
Select the movement action sequence corresponding to the obstacle response condition.

#### Inputs
- Obstacle Response Condition

#### Outputs
- Selected Movement Sequence

#### Trigger / Execution Condition
When an Obstacle Response Condition is received.

#### Processing Logic
1. For no obstacle, select forward movement.
2. For an obstacle condition other than all three specified directions being blocked, select turning aside left or right followed by forward movement.
3. When obstacles are detected in front, left, and right, select backward movement followed by turning aside left or right and then forward movement.

The requirements do not specify how to choose left or right.

#### Relevant Requirements
- Preliminary requirements, bullets 2–4.

### Process 1.2.2 — Produce Movement Command

#### Process Identification

| Field | Description |
|---|---|
| Process ID | 1.2.2 |
| Process Name | Produce Movement Command |
| DFD Level | Level 3 |
| Parent Process | 1.2 — Issue Movement Command |

#### Purpose
Produce the abstract movement command for the selected movement sequence.

#### Inputs
- Selected Movement Sequence

#### Outputs
- Movement Command

#### Trigger / Execution Condition
When a Selected Movement Sequence is received.

#### Processing Logic
1. Receive the selected movement sequence.
2. Produce a Movement Command representing that sequence for Drive and Cleaning Hardware.

The requirements do not define command encoding, timing, or hardware control details.

#### Relevant Requirements
- Preliminary requirements, bullets 2–4.

