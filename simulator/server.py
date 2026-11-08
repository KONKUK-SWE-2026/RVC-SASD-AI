#!/usr/bin/env python3
"""Local web bridge to the actual C11 RVC controller."""

from __future__ import annotations

import ctypes
import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
SIMULATOR_DIR = Path(__file__).resolve().parent
SCENARIOS_FILE = SIMULATOR_DIR / "scenarios.json"
CUSTOM_FILE = SIMULATOR_DIR / "custom_scenarios.json"
RESULTS_DIR = ROOT / "artifacts" / "SystemTest"
STATE_NAMES = ["Forward", "ObstacleAvoidance", "AllDirectionsBlocked"]
MOVEMENT_NAMES = ["FORWARD", "TURN_ASIDE", "BACKWARD"]
CLEANING_NAMES = [
    "CLEANING_AND_MOP",
    "CLEANING_STOP_THEN_CLEAN_AND_MOP",
    "CLEANING_STOP_THEN_UNSPECIFIED",
]
HEADINGS = ("N", "E", "S", "W")
VECTORS = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}


class CSensorInput(ctypes.Structure):
    _fields_ = [
        ("front_obstacle", ctypes.c_bool),
        ("left_obstacle", ctypes.c_bool),
        ("right_obstacle", ctypes.c_bool),
        ("dust_detected", ctypes.c_bool),
    ]


class CController(ctypes.Structure):
    _fields_ = [("state", ctypes.c_int)]


class CControllerOutput(ctypes.Structure):
    _fields_ = [
        ("movement", ctypes.c_int * 3),
        ("movement_count", ctypes.c_size_t),
        ("cleaning_action", ctypes.c_int),
        ("request_temporary_power_boost", ctypes.c_bool),
    ]


def load_c_library() -> ctypes.CDLL:
    build = ROOT / "build"
    candidates = [
        build / "librvc_controller.dylib",
        build / "librvc_controller.so",
        build / "rvc_controller.dll",
    ]
    library = next((path for path in candidates if path.exists()), None)
    if library is None:
        raise RuntimeError(
            "C controller library not found. Build it with: "
            "cmake -S . -B build -DCMAKE_C_COMPILER=gcc "
            "-DCMAKE_CXX_COMPILER=g++ -DRVC_ENABLE_COVERAGE=OFF && "
            "cmake --build build --target rvc_controller_shared"
        )

    c_library = ctypes.CDLL(str(library))
    c_library.rvc_controller_init.argtypes = [ctypes.POINTER(CController)]
    c_library.rvc_controller_init.restype = None
    c_library.rvc_controller_step.argtypes = [
        ctypes.POINTER(CController),
        ctypes.POINTER(CSensorInput),
        ctypes.POINTER(CControllerOutput),
    ]
    c_library.rvc_controller_step.restype = ctypes.c_bool
    return c_library


def load_scenarios() -> list[dict]:
    scenarios = json.loads(SCENARIOS_FILE.read_text())
    if CUSTOM_FILE.exists():
        scenarios.extend(json.loads(CUSTOM_FILE.read_text()))
    return scenarios


def validate_config(config: dict) -> dict:
    position = config.get("initial_position")
    if (
        not isinstance(position, list)
        or len(position) != 2
        or any(not isinstance(value, int) or not 0 <= value < 10 for value in position)
    ):
        raise ValueError("initial_position must be an [x, y] coordinate within 0..9")
    direction = config.get("direction")
    if direction not in HEADINGS:
        raise ValueError("direction must be N, E, S, or W")
    maximum = config.get("max_ticks", 100)
    if not isinstance(maximum, int) or not 1 <= maximum <= 100:
        raise ValueError("max_ticks must be between 1 and 100")

    normalized = dict(config)
    normalized["max_ticks"] = maximum
    for field in ("obstacles", "dust"):
        points = normalized.get(field, [])
        if not isinstance(points, list):
            raise ValueError(f"{field} must be a coordinate list")
        clean_points = []
        for point in points:
            if (
                not isinstance(point, list)
                or len(point) != 2
                or any(not isinstance(value, int) or not 0 <= value < 10 for value in point)
            ):
                raise ValueError(f"{field} coordinates must be within 0..9")
            if point == position and field == "obstacles":
                raise ValueError("the RVC cannot start on an obstacle")
            if point not in clean_points:
                clean_points.append(point)
        normalized[field] = clean_points
    return normalized


class Simulator:
    def __init__(self, c_library: ctypes.CDLL):
        self.c_library = c_library
        self.scenarios = load_scenarios()
        self.load_scenario(self.scenarios[0])

    def load_scenario(self, scenario: dict) -> dict:
        config = validate_config(scenario)
        self.scenario = dict(scenario)
        self.config = config
        self.obstacles = {tuple(point) for point in config["obstacles"]}
        self.dust = {tuple(point) for point in config["dust"]}
        self.initial_obstacles = set(self.obstacles)
        self.initial_dust = set(self.dust)
        self.position = tuple(config["initial_position"])
        self.initial_position = self.position
        self.direction = config["direction"]
        self.initial_direction = self.direction
        self.tick_count = 0
        self.queue: list[int] = []
        self.sequence_cursor = 0
        self.last_output: dict | None = None
        self.last_sensor_sample: dict | None = None
        self.last_obstacle_condition = "Not sampled"
        self.previous_state = "Forward"
        self.c_controller = CController()
        self.c_library.rvc_controller_init(ctypes.byref(self.c_controller))
        self.history = [self._snapshot_initial()]
        self.view_index = 0
        self.stopped = False
        return self.state()

    def _cell_has_obstacle(self, point: tuple[int, int]) -> bool:
        x, y = point
        return 0 <= x < 10 and 0 <= y < 10 and point in self.obstacles

    def _cell_is_open(self, point: tuple[int, int]) -> bool:
        x, y = point
        return 0 <= x < 10 and 0 <= y < 10 and point not in self.obstacles

    def _relative_sensor_position(self, turn: int) -> tuple[int, int]:
        dx, dy = VECTORS[self.direction]
        for _ in range(turn % 4):
            dx, dy = -dy, dx
        return self.position[0] + dx, self.position[1] + dy

    def _sensors(self) -> dict:
        return {
            "front_obstacle": self._cell_has_obstacle(self._relative_sensor_position(0)),
            "left_obstacle": self._cell_has_obstacle(self._relative_sensor_position(3)),
            "right_obstacle": self._cell_has_obstacle(self._relative_sensor_position(1)),
            "dust_detected": self.position in self.dust,
        }

    def _state_name(self) -> str:
        value = int(self.c_controller.state)
        return STATE_NAMES[value] if 0 <= value < len(STATE_NAMES) else "Unknown"

    def _grid(self) -> list[list[dict]]:
        return [
            [
                {
                    "obstacle": (x, y) in self.obstacles,
                    "dust": (x, y) in self.dust,
                    "robot": (x, y) == self.position,
                }
                for x in range(10)
            ]
            for y in range(10)
        ]

    def _base_snapshot(self) -> dict:
        return {
            "tick": self.tick_count,
            "position": list(self.position),
            "direction": self.direction,
            "controller_state": self._state_name(),
            "sensors": self._sensors(),
            "controller_invoked": False,
            "controller_output": self.last_output,
            "motor_output": None,
            "cleaner_output": None,
            "power_timer": "TBD (not represented by C controller)",
            "turn_timer": "TBD (not represented by C controller)",
            "sequence_remaining": list(self.queue),
            "last_obstacle_condition": self.last_obstacle_condition,
            "obstacles": [list(point) for point in sorted(self.obstacles)],
            "dust": [list(point) for point in sorted(self.dust)],
            "grid": self._grid(),
            "map_changes": [],
            "transition": None,
            "notes": [],
        }

    def _snapshot_initial(self) -> dict:
        snapshot = self._base_snapshot()
        snapshot["controller_output"] = None
        snapshot["notes"] = ["Tick 0 initial state; controller has not been called."]
        return snapshot

    def _c_step(self, sensors: dict) -> dict:
        c_input = CSensorInput(
            sensors["front_obstacle"],
            sensors["left_obstacle"],
            sensors["right_obstacle"],
            sensors["dust_detected"],
        )
        c_output = CControllerOutput()
        self.previous_state = self._state_name()
        ok = self.c_library.rvc_controller_step(
            ctypes.byref(self.c_controller), ctypes.byref(c_input), ctypes.byref(c_output)
        )
        if not ok:
            raise RuntimeError("C controller rejected simulator sensor input")
        movement = [
            MOVEMENT_NAMES[c_output.movement[index]]
            for index in range(c_output.movement_count)
        ]
        self.last_output = {
            "movement_sequence": movement,
            "cleaning_action": CLEANING_NAMES[c_output.cleaning_action],
            "request_temporary_power_boost": bool(c_output.request_temporary_power_boost),
        }
        self.last_sensor_sample = dict(sensors)
        self.queue = list(c_output.movement[: c_output.movement_count])
        self.sequence_cursor = 0
        if not any(sensors[key] for key in ("front_obstacle", "left_obstacle", "right_obstacle")):
            self.last_obstacle_condition = "No obstacle"
        elif all(sensors[key] for key in ("front_obstacle", "left_obstacle", "right_obstacle")):
            self.last_obstacle_condition = "All three directions blocked"
        else:
            self.last_obstacle_condition = "Obstacle detected, not all three directions"
        return self.last_output

    def _cleaner_action_for_sequence_step(self, action: int, index: int, length: int) -> str:
        if self.last_output is None:
            return "Not issued"
        cleaning = self.last_output["cleaning_action"]
        if cleaning == "CLEANING_AND_MOP":
            return "Clean and mop"
        if cleaning == "CLEANING_STOP_THEN_CLEAN_AND_MOP":
            return "Clean and mop" if index == length - 1 else "Stop cleaning during obstacle handling"
        if cleaning == "CLEANING_STOP_THEN_UNSPECIFIED":
            return "Unspecified final cleaning state" if index == length - 1 else "Stop cleaning during obstacle handling"
        return "Unknown"

    def _move(self, action: int) -> tuple[list[int], str]:
        before = self.position
        if action == 0:
            dx, dy = VECTORS[self.direction]
            target = (self.position[0] + dx, self.position[1] + dy)
            if self._cell_has_obstacle(target) or not (0 <= target[0] < 10 and 0 <= target[1] < 10):
                return list(before), "FORWARD blocked by map obstacle or grid edge"
            self.position = target
            return list(self.position), "FORWARD"
        if action == 2:
            dx, dy = VECTORS[self.direction]
            target = (self.position[0] - dx, self.position[1] - dy)
            if self._cell_has_obstacle(target) or not (0 <= target[0] < 10 and 0 <= target[1] < 10):
                return list(before), "BACKWARD blocked by map obstacle or grid edge"
            self.position = target
            return list(self.position), "BACKWARD"

        left_heading = HEADINGS[(HEADINGS.index(self.direction) - 1) % 4]
        right_heading = HEADINGS[(HEADINGS.index(self.direction) + 1) % 4]
        left_delta = VECTORS[left_heading]
        right_delta = VECTORS[right_heading]
        left_open = self._cell_is_open((self.position[0] + left_delta[0], self.position[1] + left_delta[1]))
        right_open = self._cell_is_open((self.position[0] + right_delta[0], self.position[1] + right_delta[1]))
        # Simulator adapter convention only: prefer left if open, else right if open.
        self.direction = left_heading if left_open or not right_open else right_heading
        return list(self.position), f"TURN_ASIDE -> {self.direction} (simulator adapter choice)"

    def step(self) -> dict:
        if self.tick_count >= self.config["max_ticks"]:
            self.stopped = True
            return self.state()

        before = list(self.position)
        sensors = self._sensors()
        invoked = not self.queue
        old_state = self._state_name()
        if invoked:
            self._c_step(sensors)
        action_index = self.sequence_cursor
        action = self.queue.pop(0) if self.queue else 0
        sequence_length = len(self.last_output["movement_sequence"]) if self.last_output else 0
        cleaner_output = self._cleaner_action_for_sequence_step(action, action_index, sequence_length)
        boost_request = self.last_output["request_temporary_power_boost"] if invoked and self.last_output else None

        map_changes = []
        if cleaner_output == "Clean and mop" and self.position in self.dust:
            self.dust.remove(self.position)
            map_changes.append({"type": "dust_cleaned", "position": list(self.position)})

        self.sequence_cursor += 1
        new_position, motor_output = self._move(action)
        self.tick_count += 1
        new_state = self._state_name()
        notes = []
        if not invoked:
            notes.append("Executing the remaining action from the last C movement sequence; controller state is held.")
        if invoked and boost_request:
            notes.append("C controller requested a temporary power boost; duration is unspecified.")
        if cleaner_output == "Unspecified final cleaning state":
            notes.append("SA leaves cleaning state for this all-directions-blocked phase unspecified.")

        snapshot = self._base_snapshot()
        snapshot.update(
            {
                "tick": self.tick_count,
                "position_before": before,
                "position": new_position,
                "direction": self.direction,
                "controller_invoked": invoked,
                "controller_sampled_inputs": dict(sensors) if invoked else None,
                "controller_output": self.last_output,
                "motor_output": motor_output,
                "cleaner_output": {
                    "action": cleaner_output,
                    "power_boost_request": boost_request,
                    "power_boost_request_source": "fresh C output" if invoked else "no new C output",
                },
                "sequence_remaining": [MOVEMENT_NAMES[value] for value in self.queue],
                "map_changes": map_changes,
                "transition": f"{old_state} -> {new_state}" if invoked and old_state != new_state else None,
                "notes": notes,
            }
        )
        self.history.append(snapshot)
        self.view_index = len(self.history) - 1
        if self.tick_count >= self.config["max_ticks"]:
            self.stopped = True
        return snapshot

    def reset(self) -> dict:
        scenario = dict(self.scenario)
        # Preserve the currently edited map and start values as the reset baseline.
        scenario.update(
            {
                "initial_position": list(self.initial_position),
                "direction": self.initial_direction,
                "obstacles": [list(point) for point in sorted(self.initial_obstacles)],
                "dust": [list(point) for point in sorted(self.initial_dust)],
            }
        )
        return self.load_scenario(scenario)

    def state(self) -> dict:
        snapshot = self.history[min(self.view_index, len(self.history) - 1)]
        return {
            "scenario": self.scenario,
            "tick": self.tick_count,
            "max_ticks": self.config["max_ticks"],
            "stopped": self.stopped,
            "history": self.history,
            "view_index": self.view_index,
            "current": snapshot,
        }


class RequestHandler(BaseHTTPRequestHandler):
    simulator: Simulator

    def _send(self, payload: object, status: int = 200, content_type: str = "application/json") -> None:
        data = payload if isinstance(payload, bytes) else json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def _body(self) -> dict:
        length = int(self.headers.get("Content-Length", "0"))
        if length > 1_000_000:
            raise ValueError("request body is too large")
        return json.loads(self.rfile.read(length) or b"{}")

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path == "/api/scenarios":
            self._send(load_scenarios())
            return
        if path == "/api/state":
            self._send(self.simulator.state())
            return
        static = {"/": "index.html", "/app.js": "app.js", "/style.css": "style.css"}
        filename = static.get(path)
        if filename is None:
            self._send({"error": "not found"}, 404)
            return
        content_type = "text/html; charset=utf-8" if filename.endswith(".html") else "text/javascript; charset=utf-8" if filename.endswith(".js") else "text/css; charset=utf-8"
        self._send((SIMULATOR_DIR / filename).read_bytes(), content_type=content_type)

    def do_POST(self) -> None:
        path = urlparse(self.path).path
        try:
            body = self._body()
            if path == "/api/load":
                scenario = next((item for item in load_scenarios() if item["id"] == body.get("id")), None)
                if scenario is None:
                    raise ValueError("unknown scenario")
                self._send(self.simulator.load_scenario(scenario))
            elif path == "/api/custom-map":
                config = validate_config(body)
                self._send(self.simulator.load_scenario(config))
            elif path == "/api/tick":
                self._send(self.simulator.step())
            elif path == "/api/reset":
                self._send(self.simulator.reset())
            elif path == "/api/restart":
                scenario = next((item for item in load_scenarios() if item["id"] == self.simulator.scenario["id"]), None)
                self._send(self.simulator.load_scenario(scenario or self.simulator.scenario))
            elif path == "/api/save-scenario":
                custom = dict(validate_config(body))
                custom.setdefault("id", f"CUSTOM-{len(load_scenarios()) + 1:02d}")
                custom.setdefault("name", "Custom map")
                custom.setdefault("functions", ["sensor input inspection", "movement response", "cleaning output"])
                custom.setdefault("requirements", ["User-defined map; evaluate against selected SA requirements"])
                custom.setdefault("expected", "Human evaluator inspects the actual C outputs and simulator state.")
                custom.setdefault("run_ticks", min(8, custom["max_ticks"]))
                custom_items = json.loads(CUSTOM_FILE.read_text()) if CUSTOM_FILE.exists() else []
                custom_items = [item for item in custom_items if item["id"] != custom["id"]]
                custom_items.append(custom)
                CUSTOM_FILE.write_text(json.dumps(custom_items, indent=2) + "\n")
                self._send({"saved": custom, "scenarios": load_scenarios()})
            elif path == "/api/evaluation":
                result = body.get("result")
                if result not in ("PASS", "FAIL", "INCONCLUSIVE"):
                    raise ValueError("result must be PASS, FAIL, or INCONCLUSIVE")
                RESULTS_DIR.mkdir(parents=True, exist_ok=True)
                result_file = RESULTS_DIR / "human_evaluations.json"
                existing = json.loads(result_file.read_text()) if result_file.exists() else []
                existing.append(body)
                result_file.write_text(json.dumps(existing, indent=2) + "\n")
                self._send({"saved": True})
            else:
                self._send({"error": "not found"}, 404)
        except (ValueError, KeyError, json.JSONDecodeError) as error:
            self._send({"error": str(error)}, 400)

    def log_message(self, format_string: str, *args) -> None:
        if os.environ.get("RVC_SIMULATOR_QUIET") != "1":
            super().log_message(format_string, *args)


def main() -> None:
    c_library = load_c_library()
    RequestHandler.simulator = Simulator(c_library)
    port = int(os.environ.get("RVC_SIMULATOR_PORT", "8765"))
    print(f"RVC Simulator: http://127.0.0.1:{port}")
    HTTPServer(("127.0.0.1", port), RequestHandler).serve_forever()


if __name__ == "__main__":
    main()
