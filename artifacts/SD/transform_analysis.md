# Transform Analysis

## 1. Objective

Identify input, decision, and output regions from the revised SA, including the timer update that occurs every simulation tick.

## 2. Transform Regions

### Afferent Flow (Input)

| Process | Input | Output |
|---|---|---|
| 1.1 Classify Obstacle Condition | Obstacle Detection Input | Obstacle Response Condition |
| 2.2.1 Update Dust Boost Timer State | Dust Detection Input; Simulation Tick; Previous Remaining Boost Ticks | Updated Remaining Boost Ticks |

### Central Transformation

| Process | Input | Output |
|---|---|---|
| 1.2.1 Select Movement Sequence | Obstacle Response Condition | Selected Movement Sequence |
| 2.1 Determine Obstacle Cleaning Action | Obstacle Detection Input | Obstacle-Related Cleaning Action |
| 2.2.2 Determine Active Power Mode | Updated Remaining Boost Ticks; Cleaning Active Indicator | Effective Dust Power State |

### Efferent Flow (Output)

| Process | Input | Output |
|---|---|---|
| 1.2.2 Produce Movement Command | Selected Movement Sequence | Movement Command |
| 2.3 Generate Cleaning Control Command | Obstacle-Related Cleaning Action; Effective Dust Power State | Cleaning Control Command |

## 3. Transform Boundaries

- Afferent-to-central: sensor inputs and the internal Simulation Tick enter the controller. The Simulation Tick is temporal control information, not a new external hardware flow.
- Central transformations classify/select movement, maintain the boost interval, and derive effective power from cleaning activity and remaining time.
- Central-to-efferent: selected movement sequence and combined cleaning action/power mode become abstract commands.
- D1 stores the transient remaining tick count inside the controller.

## 4. Transform Analysis Diagram

```mermaid
flowchart LR
    Sensors["Sensors"]
    Clock(("Internal Simulation Tick"))
    D1[("D1: Dust Boost Timer State")]

    subgraph A["Afferent Flow"]
        P11(("1.1 Classify Obstacle Condition"))
        P221(("2.2.1 Update Dust Boost Timer State"))
    end
    subgraph C["Central Transformation"]
        P121(("1.2.1 Select Movement Sequence"))
        P21(("2.1 Determine Obstacle Cleaning Action"))
        P222(("2.2.2 Determine Active Power Mode"))
    end
    subgraph E["Efferent Flow"]
        P122(("1.2.2 Produce Movement Command"))
        P23(("2.3 Generate Cleaning Control Command"))
    end
    Hardware["Drive and Cleaning Hardware"]

    Sensors -->|Obstacle Detection Input| P11
    Sensors -->|Obstacle Detection Input| P21
    Sensors -->|Dust Detection Input| P221
    Clock -.->|Simulation Tick| P221
    D1 -->|Previous Remaining Boost Ticks| P221
    P221 -->|Updated Remaining Boost Ticks| D1
    P11 -->|Obstacle Response Condition| P121
    P121 -->|Selected Movement Sequence| P122
    P122 -->|Movement Command| Hardware
    P21 -->|Obstacle-Related Cleaning Action| P23
    P221 -->|Updated Remaining Boost Ticks| P222
    P21 -->|Cleaning Active Indicator| P222
    P222 -->|Effective Dust Power State| P23
    P23 -->|Cleaning Control Command| Hardware
```

## 5. Analysis Rules

- Process IDs and data flows follow SA DFD Levels 2–3.
- D1 is transient controller state; numeric actuator power remains unspecified.
- Main must advance the timer on every simulation tick, even when no new movement sequence is selected.
- Module calls are defined separately in `structure_chart.md`.
