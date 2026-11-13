# Requirement-to-System-Test Traceability

Requirement IDs are RVC-01–RVC-07 in `docs/preliminary_requirments.md`.
SA artifacts: Event List; Context Diagram; DFD 0–3; Level 4 Controller FSM; Data Dictionary; Process Specifications; Structure Chart.

| Scenario | Requirement IDs | Essential functions | Human result |
|---|---|---|---|
| ST-01 | RVC-01, RVC-02 | sensor inputs report a clear path, forward movement selection, automatic clean and mop output | Pending |
| ST-02 | RVC-01, RVC-02, RVC-05 | dust sensor input, five-tick boost state, forward movement and clean/mop output | Pending |
| ST-03 | RVC-01, RVC-03 | front obstacle sensing, obstacle-avoidance movement sequence, stop then resume cleaning | Pending |
| ST-04 | RVC-01, RVC-03 | left obstacle sensing, obstacle-avoidance movement sequence, cleaning response | Pending |
| ST-05 | RVC-01, RVC-03 | right obstacle sensing, obstacle-avoidance movement sequence, cleaning response | Pending |
| ST-06 | RVC-01, RVC-03 | multi-direction obstacle sensing, partial-obstacle classification, avoidance and cleaner outputs | Pending |
| ST-07 | RVC-01, RVC-03 | multi-direction obstacle sensing, partial-obstacle classification, avoidance and cleaner outputs | Pending |
| ST-08 | RVC-01, RVC-02, RVC-03 | left/right obstacle sensing, not-all-directions classification, forward and cleaning output | Pending |
| ST-09 | RVC-03, RVC-04 | three-direction obstacle sensing, all-blocked classification, backward recovery sequence | Pending |
| ST-10 | RVC-03, RVC-05 | obstacle and dust sensing, obstacle response, effective boost only while cleaning | Pending |
| ST-11 | RVC-03, RVC-05 | left obstacle and dust sensing, movement response, boost state and countdown | Pending |
| ST-12 | RVC-03, RVC-05 | right obstacle and dust sensing, movement response, boost state and countdown | Pending |
| ST-13 | RVC-04, RVC-05 | all-direction obstacle sensing, backward recovery, cleaning stop and resume, effective boost power only while cleaning | Pending |
| ST-14 | RVC-02, RVC-03 | direction-relative front sensing, obstacle response, cleaner response | Pending |
| ST-15 | RVC-02, RVC-03 | direction-relative front sensing, obstacle response, cleaner response | Pending |
| ST-16 | RVC-02, RVC-03 | direction-relative front sensing, obstacle response, cleaner response | Pending |
| ST-17 | RVC-04, RVC-01 | rotated three-direction sensing, all-blocked classification, backward recovery | Pending |
| ST-18 | RVC-03, RVC-05 | direction-relative sensing, partial-obstacle response, dust power mode duration | Pending |
| ST-19 | RVC-01, RVC-03, RVC-05 | direction-relative side sensing, movement response, boost power mode | Pending |
| ST-20 | RVC-01, RVC-02, RVC-05 | repeated sensor sampling, forward movement, dust-triggered boost state | Pending |
| ST-21 | RVC-01, RVC-02, RVC-05 | dust detection on consecutive controller decisions, five-tick boost refresh, normal-power transition after expiry | Pending |

Detailed SA paths: `artifacts/SA/event_list.md`, `artifacts/SA/context_diagram.md`, `artifacts/SA/DFD/dfd_level_0.md`, `artifacts/SA/DFD/dfd_level_1.md`, `artifacts/SA/DFD/dfd_level_2.md`, `artifacts/SA/DFD/dfd_level_3.md`, `artifacts/SA/DFD/dfd_level_4_fsm.md`, `artifacts/SA/data_dictionary.md`, `artifacts/SA/process_specification.md`, `artifacts/SD/structure_chart.md`.
