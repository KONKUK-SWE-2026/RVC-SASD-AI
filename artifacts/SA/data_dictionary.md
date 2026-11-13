# Data Dictionary

## 1. External Events and Interface Flows

| Name | Description | Format / Type | Flow Category | Source | Destination | Level | Requirement |
|---|---|---|---|---|---|---|---|
| Obstacle Detection Input | Front, left, and right obstacle detections. | Three Boolean values. | External data | Sensors | Process 0; Processes 1 and 2 | Context, 0–2 | RVC-03, RVC-04 |
| Dust Detection Input | Whether dust is detected on the current simulation tick. | Boolean. | External data | Sensors | Process 0; Process 2; Process 2.2.1 | Context, 0–3 | RVC-05 |
| Movement Command | Forward, turn-aside, or backward movement sequence. | One or more abstract movement actions; left/right choice is unspecified. | External output | Process 0; Process 1; Process 1.2.2 | Context, 0–3 | RVC-02–RVC-04 |
| Cleaning Control Command | Cleaning/mopping action plus effective Normal/Boost power mode. | Abstract action and enum power mode; Boost only while cleaning is active; numeric power levels unspecified. | External output | Process 0; Process 2; Process 2.3 | Context, 0–3 | RVC-01, RVC-03–RVC-05 |

## 2. Internal Events, Data, and Control Flows

| Name | Description | Format / Type | Flow Category | Source | Destination | Level | Requirement |
|---|---|---|---|---|---|---|---|
| Simulation Tick | One discrete simulator update; advances the boost timer once regardless of movement sequence progress. | Temporal control event. | Control | Simulator scheduler / Main | Processes 2.2 and 2.2.1 | 2–3 | RVC-05 |
| Obstacle Response Condition | Classification of obstacle readings: clear, partial obstacle, or all three specified directions blocked. | Enum condition. | Data | Process 1.1 | Process 1.2; Process 1.2.1 | 2–3 | RVC-02–RVC-04 |
| Obstacle-Related Cleaning Action | Cleaning stop/resume action associated with obstacle handling; all-blocked recovery resumes cleaning during forward movement. | Abstract action sequence. | Data | Process 2.1 | Process 2.2.2; Process 2.3 | 2 | RVC-01, RVC-03, RVC-04 |
| Cleaning Active Indicator | Whether the current movement-sequence action is cleaning. | Boolean. | Data | Process 2.1 | Process 2.2.2 / Process 2.3 | 2–3 | RVC-01–RVC-04 |
| Previous Remaining Boost Ticks | Boost timer count before processing the current tick. | Integer 0–5. | Data | D1 | Process 2.2; Process 2.2.1 | 2–3 | RVC-05 |
| Updated Remaining Boost Ticks | Timer count after dust refresh or one-tick decrement. | Integer 0–5. | Data | Process 2.2; Process 2.2.1 | D1; Process 2.2.2 | 2–3 | RVC-05 |
| Boost Availability | Whether D1 has a positive remaining count, independent of current cleaning activity. | Boolean derived from D1. | Data | Process 2.2.2 | Process 2.3 | 2–3 | RVC-05 |
| Dust Power State | Effective cleaning-power mode, gated by Cleaning Active Indicator and Boost Availability. | `NORMAL` or `BOOST`. | Data | Process 2.2.2 | Process 2.3 | 2–3 | RVC-05 |
| Selected Movement Sequence | Sequence selected for an obstacle response condition. | Sequence of abstract movement actions. | Data | Process 1.2.1 | Process 1.2.2 | 3 | RVC-02–RVC-04 |

## 3. Data Store

| Store | Contents | Initial State | Update Rule | Owner | Requirement |
|---|---|---|---|---|---|
| D1 — Dust Boost Timer State | Remaining boost-interval ticks. | 0 (inactive). | Dust-positive tick sets count to 5. Otherwise decrement once per tick while positive. | Process 2.2 / 2.2.1 | RVC-05 |

## 4. Detailed Definitions

### Simulation Tick
- Meaning: One discrete simulator update.
- Timing: Exactly one event per simulator step. The event continues while queued movement actions are executing.
- Use: Updates D1; the effective power mode also depends on the Cleaning Active Indicator.
- Requirement: RVC-05.

### Dust Boost Timer State (D1)
- Type: Unsigned integer, valid range 0–5.
- Meaning: Number of boost-interval ticks remaining, including the current tick.
- Initialization: 0.
- Transition: On a tick with `dust_detected=true`, set to 5. Otherwise, if greater than 0, decrement by 1. Zero remains zero.
- Boost availability: true iff the updated count is greater than zero.
- Effective mode: Boost iff cleaning is active and boost availability is true; otherwise Normal.
- Retrigger: Any dust-positive tick while the interval is active refreshes the count to 5.
- Expiration: After five active ticks without a dust-positive refresh, the following tick produces Normal.

### Dust Power State
- Type: Enum `{NORMAL, BOOST}`.
- Meaning: Abstract power mode derived from D1 after processing the current tick, and gated to Normal when cleaning is stopped.
- Numeric power magnitude: Unspecified; hardware actuator detail is out of scope.
- Requirement: RVC-05.

### Cleaning Control Command
- Contents: Obstacle-related cleaning action and current Dust Power State.
- Cleaning action values: clean/mop, stop during obstacle handling, resume cleaning during forward movement.
- Power mode: Normal or Boost, updated every simulation tick; Boost is output only while cleaning is active.
- Requirement: RVC-01, RVC-03–RVC-05.

### Movement Command
- Contents: Forward; turn aside followed by forward; or backward, turn aside, then forward.
- Left/right selection policy: Unspecified.
- Requirement: RVC-02–RVC-04.

## 5. Data Store Definitions

There are no external database or persistent-file stores. D1 is a transient in-memory controller state store, reset to 0 by controller initialization.
