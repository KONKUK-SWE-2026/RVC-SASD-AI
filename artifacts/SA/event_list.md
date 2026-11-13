# Event List

| Event | Kind | Description | Requirement |
|---|---|---|---|
| Obstacle Detection Input | Input | Sensors report obstacle detection for the front, left, and right directions. | RVC-03, RVC-04 |
| Dust Detection Input | Input | Sensors report whether dust is detected for the current simulation tick. | RVC-05 |
| Simulation Tick | Temporal / internal | Each discrete simulation update advances the dust boost interval once, including while a selected movement sequence is still being executed. It is an internal scheduling event, not a new external sensor or hardware input. | RVC-05 |
| Movement Command | Output | Directs the RVC to move forward, turn aside left or right, or move backward as required by obstacles. | RVC-02–RVC-04 |
| Cleaning Control Command | Output | Directs cleaning/mopping behavior and reports effective power mode (Boost only while cleaning is active; otherwise Normal). | RVC-01, RVC-03–RVC-05 |

The boost interval lasts five simulation ticks beginning with the dust-detection tick. A dust-positive tick refreshes the interval. The effective output is Boost only while cleaning is active; timer progression continues while cleaning is stopped. After the five-tick interval expires, output remains Normal. Numeric actuator power levels remain outside scope.
