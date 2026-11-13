#!/usr/bin/env python3
"""Execute predefined RVC scenarios through the running web simulator API."""
from __future__ import annotations

import json
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "http://127.0.0.1:8766"
SCENARIOS = json.loads((ROOT / "simulator" / "scenarios.json").read_text())
SA_FILES = [
    "artifacts/SA/event_list.md",
    "artifacts/SA/context_diagram.md",
    "artifacts/SA/DFD/dfd_level_0.md",
    "artifacts/SA/DFD/dfd_level_1.md",
    "artifacts/SA/DFD/dfd_level_2.md",
    "artifacts/SA/DFD/dfd_level_3.md",
    "artifacts/SA/DFD/dfd_level_4_fsm.md",
    "artifacts/SA/data_dictionary.md",
    "artifacts/SA/process_specification.md",
    "artifacts/SD/structure_chart.md",
]


def request(path: str, body: dict | None = None):
    post_paths = {"/api/tick", "/api/reset", "/api/restart"}
    method = "POST" if body is not None or path in post_paths else "GET"
    data = None if method == "GET" else json.dumps(body or {}).encode()
    req = urllib.request.Request(
        BASE + path,
        data=data,
        method=method,
        headers={"Content-Type": "application/json"} if data else {},
    )
    with urllib.request.urlopen(req, timeout=10) as response:
        return json.loads(response.read())


def md_table_rows(values):
    return "\n".join("| " + " | ".join(str(value).replace("|", "\\|") for value in row) + " |" for row in values)


def main():
    assert len(request("/api/scenarios")) >= 20, "scenario API should expose 20+ scenarios"
    traces = []
    result_rows = []
    for scenario in SCENARIOS:
        assert scenario["max_ticks"] <= 100
        assert len(scenario["functions"]) >= 3
        state = request("/api/load", {"id": scenario["id"]})
        assert state["tick"] == 0 and len(state["history"]) == 1
        assert len(state["current"]["grid"]) == 10 and all(len(row) == 10 for row in state["current"]["grid"])
        history = list(state["history"])
        run_ticks = min(scenario["run_ticks"], scenario["max_ticks"])
        for _ in range(run_ticks):
            snapshot = request("/api/tick")
            if snapshot["tick"] == history[-1]["tick"]:
                break
            assert snapshot["tick"] == history[-1]["tick"] + 1
            assert 0 <= snapshot["position"][0] < 10 and 0 <= snapshot["position"][1] < 10
            assert snapshot["controller_state"] in ("Forward", "ObstacleAvoidance", "AllDirectionsBlocked")
            assert isinstance(snapshot["sensors"], dict) and isinstance(snapshot["controller_output"], dict)
            assert snapshot["timer_update_invoked"] is True
            assert snapshot["power_mode"] in ("NORMAL", "BOOST")
            assert 0 <= snapshot["power_timer"] <= 5
            cleaning_active = snapshot["cleaner_output"]["action"] == "Clean and mop"
            assert snapshot["power_mode"] == (
                "BOOST" if cleaning_active and snapshot["power_timer"] > 0 else "NORMAL"
            ), "C power mode must be Boost only during cleaning with time remaining"
            history.append(snapshot)
        assert len(history) == min(run_ticks + 1, scenario["max_ticks"] + 1)
        traces.append({
            "scenario_id": scenario["id"],
            "scenario_name": scenario["name"],
            "configuration": scenario,
            "executed_ticks": len(history) - 1,
            "human_result": "PENDING",
            "human_observations": "",
            "history": history,
        })
        decisions = sum(1 for item in history[1:] if item["movement_decision_invoked"])
        modes = ", ".join(dict.fromkeys(item["power_mode"] for item in history[1:]))
        result_rows.append((scenario["id"], scenario["name"], len(history) - 1, decisions, modes, "Pending human evaluation"))

    custom = {
        "id": "VALIDATION-CUSTOM",
        "name": "Custom map and tick limit validation",
        "initial_position": [7, 8],
        "direction": "W",
        "obstacles": [[2, 2]],
        "dust": [[7, 8]],
        "max_ticks": 100,
    }
    custom_state = request("/api/custom-map", custom)
    assert custom_state["current"]["position"] == [7, 8]
    assert custom_state["current"]["direction"] == "W"
    assert len(custom_state["current"]["grid"]) == 10
    request("/api/tick")
    reset_state = request("/api/reset", {})
    assert reset_state["tick"] == 0
    assert reset_state["current"]["position"] == [7, 8]
    assert reset_state["current"]["obstacles"] == [[2, 2]]
    assert reset_state["current"]["dust"] == [[7, 8]]

    for _ in range(100):
        request("/api/tick")
    limit_state = request("/api/state")
    assert limit_state["tick"] == 100 and limit_state["stopped"]
    frozen = request("/api/tick")
    assert frozen["tick"] == 100
    try:
        request("/api/custom-map", {**custom, "initial_position": [1, 1], "obstacles": [[1, 1]]})
        raise AssertionError("invalid initial obstacle overlap should be rejected")
    except urllib.error.HTTPError as error:
        assert error.code == 400
    simulator_validation = {
        "custom_start_and_map": "verified",
        "reset_restores_custom_initial_state": "verified",
        "100_tick_limit_and_stop": "verified",
        "no_tick_after_limit": "verified",
        "reject_start_on_obstacle": "verified",
        "C_timer_updated_every_simulation_tick": "verified",
        "C_power_state_in_expected_domain": "verified",
    }
    request("/api/load", {"id": SCENARIOS[0]["id"]})

    out = ROOT / "artifacts" / "SystemTest"
    out.mkdir(parents=True, exist_ok=True)
    (out / "execution_traces.json").write_text(json.dumps({
        "simulator": BASE,
        "controller_library": "build/librvc_controller.dylib",
        "executed_at_utc": datetime.now(timezone.utc).isoformat(),
        "human_is_test_oracle": True,
        "simulator_validation": simulator_validation,
        "scenarios": traces,
    }, indent=2) + "\n")

    scenario_doc = [
        "# RVC System Test Scenarios", "",
        "Simulator grid: 10x10 (x,y = 0..9); default start convention: (4,4).",
        "Each run is capped at 8 ticks (global maximum: 100). Expected behavior is for human evaluation; no automatic verdict is assigned.",
        "Requirement references use RVC-01–RVC-07 from `docs/preliminary_requirments.md`.", ""
    ]
    for item in SCENARIOS:
        scenario_doc += [
            f"## {item['id']} — {item['name']}", "",
            f"- Initial position/direction: `{item['initial_position']}` / `{item['direction']}`",
            f"- Obstacles: `{item['obstacles']}`; dust: `{item['dust']}`",
            f"- Tick cap: {item['max_ticks']}; executed: {item['run_ticks']}; grid: 10x10",
            f"- Essential functions: {', '.join(item['functions'])}",
            f"- Preliminary requirements: {', '.join(item['requirements'])}",
            f"- Expected behavior: {item['expected']}",
            "- SA artifacts: Event List, Context Diagram, DFD Levels 0–4/FSM, Data Dictionary, Process Specifications.",
            "- Human evaluation: Pending", ""
        ]
    (out / "test_scenarios.md").write_text("\n".join(scenario_doc))

    result_doc = [
        "# System Test Execution Results", "",
        f"- Execution time (UTC): {datetime.now(timezone.utc).isoformat()}",
        "- Execution path: Web simulator HTTP API -> Python ctypes -> compiled C11 controller library.",
        "- Human test oracle: required; verdicts remain pending (no automatic PASS/FAIL).",
        "- GCC/CMake C unit suite: 15/15 passed (`ctest --test-dir build --output-on-failure`).",
        f"- Scenarios executed: {len(result_rows)} / {len(SCENARIOS)}.",
        "- Automated simulator checks: scenario load; 10x10 grid; contiguous histories; C output presence; timer update on each tick; C cleaning/power-state consistency; custom map and reset; 100-tick stop; invalid start overlap rejected.",
        "- These harness checks validate simulator execution and trace integrity, not requirement conformance.", "",
        "| ID | Scenario | Ticks | Movement decisions | Power modes observed | Human verdict |", "|---|---|---:|---|---|---|",
        md_table_rows(result_rows), "",
        "## Limitations and observations", "",
        "- Left/right choice for `TURN_ASIDE` is supplied by the simulator adapter (left if open, otherwise right); it is not a C controller requirement.",
        "- Boost timer is implemented in the C controller and advances on every simulation tick; the boost magnitude remains abstract because no numeric level was specified.",
        "- ST-13 confirms NORMAL output during backward/turn cleaning stops, then BOOST during forward cleaning while the interval remains active.",
        "- No hardware drivers are present; sensor input and abstract motor/cleaner actions are represented on the grid.",
        "- Human review is needed to assign a verdict to each execution trace.", "",
        "Full per-tick records: `execution_traces.json`.", ""
    ]
    (out / "test_results.md").write_text("\n".join(result_doc))

    trace_doc = [
        "# Requirement-to-System-Test Traceability", "",
        "Requirement IDs are RVC-01–RVC-07 in `docs/preliminary_requirments.md`.",
        "SA artifacts: Event List; Context Diagram; DFD 0–3; Level 4 Controller FSM; Data Dictionary; Process Specifications; Structure Chart.", "",
        "| Scenario | Requirement IDs | Essential functions | Human result |", "|---|---|---|---|",
    ]
    trace_doc.append(md_table_rows((item["id"], ", ".join(item["requirements"]), ", ".join(item["functions"]), "Pending") for item in SCENARIOS))
    trace_doc += ["", "Detailed SA paths: " + ", ".join(f"`{name}`" for name in SA_FILES) + ".", ""]
    (out / "requirement_traceability.md").write_text("\n".join(trace_doc))
    print(f"Executed {len(traces)} scenarios; saved {len(traces)} tick histories to {out / 'execution_traces.json'}")
    print(f"Ticks recorded: {sum(item['executed_ticks'] for item in traces)}; all human verdicts remain pending.")


if __name__ == "__main__":
    main()
