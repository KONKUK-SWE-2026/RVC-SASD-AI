# Data Dictionary

## 1. External Input/Output Events

| Input/Output Event | Description | Format / Type |
|---|---|---|
| Obstacle Detection Input | Sensors report obstacle detection for the front, left, and right directions. | Direction-specific Boolean detections; interface details TBD. |
| Dust Detection Input | Sensors report whether dust is detected. | Boolean detection; interface details TBD. |
| Movement Command | The automatic cleaning function directs the RVC to move forward, turn aside left or right, or move backward as required by the detected obstacles. | Movement action/direction; command encoding TBD. |
| Cleaning Control Command | The automatic cleaning function directs cleaning and mopping, stops cleaning during obstacle handling, and temporarily increases cleaning power when dust is detected. | Cleaning action/power command; encoding and boost duration TBD. |

## 2. Internal Data and Control Flows

Internal data flows introduced at DFD Levels 2–3 are listed below. At Level 1, the external Obstacle Detection Input is supplied to both child processes.

| Data Name | Description | Format / Type | Flow Category | Source | Destination | DFD Level | Requirement Reference |
|---|---|---|---|---|---|---|---|
| Obstacle Response Condition | Classification of sensor detections for movement response: no obstacle, obstacle detected, or obstacles in front, left, and right. | Condition; exact representation TBD. | Data | Process 1.1 — Classify Obstacle Condition | Process 1.2 — Issue Movement Command at Level 2; Process 1.2.1 — Select Movement Sequence at Level 3 | 2–3 | Preliminary requirements, bullets 2–4. |
| Obstacle-Related Cleaning Action | Cleaning stop/resume action associated with obstacle handling; whether the general stop/resume behavior applies to the all-three-directions-blocked case, including its final forward movement, is unspecified. | Action sequence; exact representation TBD. | Data | Process 2.1 — Determine Obstacle Cleaning Action | Process 2.3 — Generate Cleaning Control Command | 2 | Preliminary requirements, bullets 1, 3–4. |
| Dust Power Adjustment | Indicates whether dust detection calls for a temporary cleaning power increase. | Adjustment request; power level and duration TBD. | Data | Process 2.2 — Determine Dust Power Adjustment | Process 2.3 — Generate Cleaning Control Command | 2 | Preliminary requirements, bullet 5. |
| Selected Movement Sequence | Movement action sequence selected for the classified obstacle condition. | Sequence of movement actions; exact representation TBD. | Data | Process 1.2.1 — Select Movement Sequence | Process 1.2.2 — Produce Movement Command | 3 | Preliminary requirements, bullets 2–4. |

## 3. Data Store Definitions

No data stores are defined at DFD Levels 0–3.

## 4. Detailed Data Definitions

### Obstacle Detection Input
- Description: Sensor-reported obstacle detections for the front, left, and right directions.
- Format / Type: Direction-specific Boolean detections; exact representation TBD.
- Possible Values: Detected / not detected for each direction.
- Source: Sensors.
- Destination: Process 0 — Perform Automatic Cleaning at Level 0; Process 1 — Determine Movement Response and Process 2 — Control Cleaning Behavior at Level 1.
- DFD Level: Event List, Context Diagram, DFD Levels 0–2.
- Requirement Reference: Preliminary requirements, bullets 3–4.

### Dust Detection Input
- Description: Sensor-reported presence or absence of dust.
- Format / Type: Boolean detection; exact representation TBD.
- Possible Values: Dust detected / dust not detected.
- Source: Sensors.
- Destination: Process 0 — Perform Automatic Cleaning at Level 0; Process 2 — Control Cleaning Behavior at Level 1.
- DFD Level: Event List, Context Diagram, DFD Levels 0–2.
- Requirement Reference: Preliminary requirements, bullet 5.

### Movement Command
- Description: Abstract command for the required movement, including forward movement, turning aside, or moving backward. Stopping cleaning is represented by Cleaning Control Command, not by this movement flow.
- Format / Type: Movement action/direction; exact encoding TBD.
- Possible Values: Forward, turn left, turn right, backward; whether left/right selection follows additional rules is unspecified.
- Source: Process 0 — Perform Automatic Cleaning at Level 0; Process 1 — Determine Movement Response at Level 1; Process 1.2 — Issue Movement Command at Level 2; Process 1.2.2 — Produce Movement Command at Level 3.
- Destination: Drive and Cleaning Hardware.
- DFD Level: Event List, Context Diagram, DFD Levels 0–3.
- Requirement Reference: Preliminary requirements, bullets 2–4.

### Cleaning Control Command
- Description: Abstract command to clean and mop, stop cleaning during obstacle handling, or temporarily increase cleaning power when dust is detected.
- Format / Type: Cleaning action/power command; exact encoding and boost duration TBD.
- Possible Values: Clean and mop, stop cleaning, increase cleaning power.
- Source: Process 0 — Perform Automatic Cleaning at Level 0; Process 2 — Control Cleaning Behavior at Level 1.
- Destination: Drive and Cleaning Hardware.
- DFD Level: Event List, Context Diagram, DFD Levels 0–2.
- Requirement Reference: Preliminary requirements, bullets 1, 3–5.

### Obstacle Response Condition
- Description: Classifies obstacle detections into the conditions needed to apply the explicitly stated movement responses.
- Format / Type: Condition; exact representation TBD.
- Possible Values: No obstacle detected; obstacle detected but not in all three specified directions; obstacles detected in front, left, and right.
- Source: Process 1.1 — Classify Obstacle Condition.
- Destination: Process 1.2 — Issue Movement Command at Level 2; Process 1.2.1 — Select Movement Sequence at Level 3.
- DFD Level: 2–3.
- Requirement Reference: Preliminary requirements, bullets 2–4.

### Selected Movement Sequence
- Description: Movement action sequence selected from the classified obstacle condition.
- Format / Type: Sequence of movement actions; exact representation TBD.
- Possible Values: Forward; turn left or right followed by forward; backward followed by turn left or right and then forward.
- Source: Process 1.2.1 — Select Movement Sequence.
- Destination: Process 1.2.2 — Produce Movement Command.
- DFD Level: 3.
- Requirement Reference: Preliminary requirements, bullets 2–4.

### Obstacle-Related Cleaning Action
- Description: Cleaning action associated with obstacle handling.
- Format / Type: Action sequence; exact representation TBD.
- Possible Values: Stop cleaning during obstacle handling; resume cleaning during the general avoidance forward movement; whether this stop/resume behavior applies to the all-three-directions-blocked case, including its final forward movement, is TBD.
- Source: Process 2.1 — Determine Obstacle Cleaning Action.
- Destination: Process 2.3 — Generate Cleaning Control Command.
- DFD Level: 2.
- Requirement Reference: Preliminary requirements, bullets 1, 3–4.

### Dust Power Adjustment
- Description: Indicates whether dust detection calls for a temporary increase in cleaning power.
- Format / Type: Adjustment request; power level and duration TBD.
- Possible Values: Temporary power increase requested when dust is detected; no increase request otherwise.
- Source: Process 2.2 — Determine Dust Power Adjustment.
- Destination: Process 2.3 — Generate Cleaning Control Command.
- DFD Level: 2.
- Requirement Reference: Preliminary requirements, bullet 5.

