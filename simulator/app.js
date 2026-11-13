const $ = (id) => document.getElementById(id);
const api = async (path, body) => {
  const response = await fetch(path, body === undefined ? {} : {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(body),
  });
  const result = await response.json();
  if (!response.ok) throw new Error(result.error || `HTTP ${response.status}`);
  return result;
};

let scenarios = [];
let selectedScenario = null;
let config = null;
let simState = null;
let viewIndex = 0;
let dirty = false;
let started = false;
let playTimer = null;

const samePoint = (a, b) => a[0] === b[0] && a[1] === b[1];
const hasPoint = (points, point) => points.some((candidate) => samePoint(candidate, point));
const togglePoint = (points, point) => hasPoint(points, point)
  ? points.filter((candidate) => !samePoint(candidate, point))
  : [...points, point];
const stateName = (state) => state || "—";

function setStatus(message, kind = "") {
  $("serverStatus").textContent = message;
  $("serverStatus").className = `status-pill ${kind}`;
}

function configFromScenario(scenario) {
  return {
    ...scenario,
    initial_position: [...scenario.initial_position],
    obstacles: (scenario.obstacles || []).map((point) => [...point]),
    dust: (scenario.dust || []).map((point) => [...point]),
    max_ticks: scenario.max_ticks || 8,
  };
}

function populateScenarioSelect() {
  const select = $("scenarioSelect");
  const previous = select.value;
  select.innerHTML = "";
  for (const scenario of scenarios) {
    const option = document.createElement("option");
    option.value = scenario.id;
    option.textContent = `${scenario.id} · ${scenario.name}`;
    select.append(option);
  }
  if (scenarios.some((scenario) => scenario.id === previous)) select.value = previous;
}

async function loadScenario(scenario) {
  pause();
  selectedScenario = scenario;
  config = configFromScenario(scenario);
  $("scenarioSelect").value = scenario.id;
  $("directionSelect").value = config.direction;
  $("tickLimit").value = config.max_ticks;
  simState = await api("/api/load", {id: scenario.id});
  started = false;
  dirty = false;
  viewIndex = 0;
  $("runStatus").textContent = "Ready · tick 0";
  $("evaluationResult").value = "INCONCLUSIVE";
  $("observations").value = "";
  $("evaluationStatus").textContent = "No verdict has been recorded for this run.";
  renderScenario();
  render();
}

function renderScenario() {
  $("scenarioName").textContent = config?.name || "Custom map";
  $("scenarioRequirements").textContent = (config?.requirements || []).join(" · ") || "Custom map; evaluate manually";
  $("scenarioExpected").textContent = config?.expected || "Human evaluator inspects the actual C outputs and simulator state.";
  $("scenarioFunctions").textContent = (config?.functions || []).join(" · ") || "Sensor input · movement · cleaner output";
}

function currentSnapshot() {
  if (!simState) return null;
  return simState.history?.[viewIndex] || simState.current || null;
}

function renderGrid(snapshot = currentSnapshot()) {
  const grid = $("grid");
  grid.innerHTML = "";
  const onInitialMap = !started && (snapshot?.tick || 0) === 0;
  const heading = snapshot?.direction || config.direction;
  for (let y = 0; y < 10; y += 1) {
    for (let x = 0; x < 10; x += 1) {
      const cell = document.createElement("button");
      cell.type = "button";
      cell.className = "cell";
      cell.setAttribute("role", "gridcell");
      cell.title = `(${x}, ${y})`;
      cell.dataset.x = x;
      cell.dataset.y = y;
      const fromSnapshot = snapshot?.grid?.[y]?.[x];
      const obstacle = onInitialMap ? hasPoint(config.obstacles, [x, y]) : Boolean(fromSnapshot?.obstacle);
      const dust = onInitialMap ? hasPoint(config.dust, [x, y]) : Boolean(fromSnapshot?.dust);
      const robot = onInitialMap
        ? samePoint(config.initial_position, [x, y])
        : Boolean(fromSnapshot?.robot);
      if (obstacle) cell.classList.add("obstacle");
      if (dust) cell.classList.add("dusty");
      if (robot) cell.classList.add("robot-cell");
      if (robot) {
        const arrow = {N: "↑", E: "→", S: "↓", W: "←"}[heading] || "↑";
        cell.innerHTML = `<span class="robot-icon">${arrow}</span>${dust ? '<span class="cell-dust">✦</span>' : ""}`;
      } else if (obstacle && dust) {
        cell.innerHTML = '<span class="cell-obstacle">■</span><span class="cell-dust">✦</span>';
      } else if (obstacle) {
        cell.innerHTML = '<span class="cell-obstacle">■</span>';
      } else if (dust) {
        cell.innerHTML = '<span class="cell-dust">✦</span>';
      }
      cell.disabled = started || (simState?.tick || 0) > 0;
      cell.addEventListener("click", () => editCell(x, y));
      grid.append(cell);
    }
  }
}

function editCell(x, y) {
  if (started || (simState?.tick || 0) > 0) return;
  const point = [x, y];
  const mode = $("editMode").value;
  if (mode === "start") {
    if (hasPoint(config.obstacles, point)) {
      setStatus("The RVC cannot start on an obstacle.", "error");
      return;
    }
    config.initial_position = point;
  } else if (mode === "obstacle") {
    if (samePoint(config.initial_position, point)) {
      setStatus("Move the RVC start before placing an obstacle there.", "error");
      return;
    }
    config.obstacles = togglePoint(config.obstacles, point);
  } else if (mode === "dust") {
    config.dust = togglePoint(config.dust, point);
  } else if (mode === "erase") {
    config.obstacles = config.obstacles.filter((candidate) => !samePoint(candidate, point));
    config.dust = config.dust.filter((candidate) => !samePoint(candidate, point));
  }
  dirty = true;
  renderGrid();
  renderScenario();
  setStatus("Map edited · reset or start to apply this configuration.", "warn");
}

function renderHistory(snapshot) {
  const rows = $("historyRows");
  rows.innerHTML = "";
  const history = simState?.history || [];
  history.forEach((item, index) => {
    const tr = document.createElement("tr");
    if (index === viewIndex) tr.className = "selected-row";
    const sensors = item.sensors || {};
    const values = [sensors.front_obstacle, sensors.left_obstacle, sensors.right_obstacle, sensors.dust_detected]
      .map((value) => value ? "1" : "0").join(" / ");
    const cells = [
      item.tick,
      item.position ? `(${item.position.join(",")})` : "—",
      item.direction || "—",
      item.controller_state || "—",
      values,
      item.motor_output || "—",
      `${item.cleaner_output?.action || "—"} · ${item.cleaner_output?.power_mode || "—"}`,
      item.transition || (item.controller_invoked ? "decision" : "sequence continuation"),
    ];
    for (const value of cells) {
      const td = document.createElement("td");
      td.textContent = value;
      tr.append(td);
    }
    tr.addEventListener("click", () => {
      pause();
      viewIndex = index;
      render();
    });
    rows.append(tr);
  });
  $("historyCount").textContent = `${history.length} snapshot${history.length === 1 ? "" : "s"}`;
}

function renderInspector(snapshot) {
  if (!snapshot) return;
  $("tickNumber").textContent = snapshot.tick;
  $("historyBadge").textContent = `Tick ${snapshot.tick}`;
  $("position").textContent = snapshot.position ? `(${snapshot.position.join(", ")})` : "—";
  $("direction").textContent = snapshot.direction || "—";
  $("controllerState").textContent = stateName(snapshot.controller_state);
  $("cCalled").textContent = `${snapshot.timer_update_invoked ? "Timer yes" : "Timer not yet"} · ${snapshot.movement_decision_invoked ? "Decision yes" : "No new decision"}`;
  $("sensorState").textContent = JSON.stringify({
    current_map_reading: snapshot.sensors,
    sampled_by_C_this_tick: snapshot.controller_sampled_inputs ?? "No new C call",
    dust_sampled_by_timer_this_tick: snapshot.timer_sampled_dust ?? false,
  }, null, 2);
  $("motorState").textContent = JSON.stringify({
    last_C_sequence: snapshot.controller_output?.movement_sequence ?? "No C output yet",
    executed_action: snapshot.motor_output ?? "No motor action yet",
    remaining_sequence: snapshot.sequence_remaining,
  }, null, 2);
  $("cleanerState").textContent = JSON.stringify({
    output: snapshot.cleaner_output ?? "No cleaner command yet",
    last_C_cleaning_action: snapshot.controller_output?.cleaning_action ?? "No C output yet",
    active_power_mode: snapshot.power_mode ?? "NORMAL",
    boost_ticks_remaining: snapshot.power_timer ?? 0,
  }, null, 2);
  $("internalState").textContent = JSON.stringify({
    previous_state: snapshot.transition?.split(" -> ")[0] ?? "Not changed this tick",
    current_state: snapshot.controller_state,
    last_obstacle_condition: snapshot.last_obstacle_condition,
    movement_decision_invoked: snapshot.movement_decision_invoked ?? false,
    timer_update_invoked: snapshot.timer_update_invoked ?? false,
    sequence_remaining: snapshot.sequence_remaining,
  }, null, 2);
  $("timerState").textContent = JSON.stringify({
    active_power_mode: snapshot.power_mode,
    boost_ticks_remaining: snapshot.power_timer,
    turn_completion: snapshot.turn_timer,
  }, null, 2);
  $("transitionState").textContent = JSON.stringify({
    transition: snapshot.transition,
    map_changes: snapshot.map_changes,
    notes: snapshot.notes,
  }, null, 2);
  const selected = viewIndex === (simState?.history?.length || 1) - 1;
  $("runStatus").textContent = selected
    ? (simState.stopped ? `Stopped at tick ${snapshot.tick}` : playTimer !== null ? `Running · tick ${snapshot.tick}` : `Ready · tick ${snapshot.tick}`)
    : `History view · tick ${snapshot.tick}`;
}

function render() {
  const snapshot = currentSnapshot();
  renderGrid(snapshot);
  renderInspector(snapshot);
  renderHistory(snapshot);
}

async function refreshState() {
  simState = await api("/api/state");
  viewIndex = simState.history.length - 1;
  render();
}

function currentConfig() {
  config.direction = $("directionSelect").value;
  config.max_ticks = Number($("tickLimit").value);
  if (config.max_ticks < 1 || config.max_ticks > 100 || !Number.isInteger(config.max_ticks)) {
    throw new Error("Tick limit must be an integer between 1 and 100.");
  }
  return config;
}

async function prepareRun() {
  pause();
  const current = currentConfig();
  if (dirty || selectedScenario?.id?.startsWith("CUSTOM-")) {
    simState = await api("/api/custom-map", current);
  } else {
    simState = await api("/api/load", {id: selectedScenario.id});
  }
  started = true;
  dirty = false;
  viewIndex = 0;
  renderScenario();
  render();
}

async function runOneTick() {
  if (!started) await prepareRun();
  const result = await api("/api/tick", {});
  if (result.history) {
    simState = result;
    viewIndex = simState.history.length - 1;
  } else {
    simState = await api("/api/state");
    viewIndex = simState.history.length - 1;
  }
  render();
  const reachedLimit = simState.tick >= simState.max_ticks;
  const noPending = !simState.current?.sequence_remaining?.length;
  if (reachedLimit || (simState.stopped && noPending)) {
    pause();
    setStatus(reachedLimit ? "Stopped at the 100-tick limit or scenario limit." : "Scenario sequence complete.", "warn");
  }
}

function pause() {
  if (playTimer !== null) window.clearInterval(playTimer);
  playTimer = null;
  $("startButton").textContent = "Start";
}

function start() {
  if (playTimer !== null) {
    pause();
    return;
  }
  playTimer = window.setInterval(async () => {
    try {
      await runOneTick();
    } catch (error) {
      pause();
      setStatus(error.message, "error");
    }
  }, Number($("speed").value));
  $("startButton").textContent = "Running…";
}

async function stepForward() {
  if (viewIndex < (simState.history.length - 1)) {
    viewIndex += 1;
    render();
    return;
  }
  await runOneTick();
}

async function saveCustomScenario() {
  try {
    const name = window.prompt("Name this custom test scenario:", "Custom RVC map");
    if (!name) return;
    const saved = await api("/api/save-scenario", {
      ...currentConfig(),
      id: `CUSTOM-${Date.now()}`,
      name,
      run_ticks: Math.min(8, Number($("tickLimit").value)),
    });
    scenarios = saved.scenarios;
    populateScenarioSelect();
    const customScenario = saved.saved;
    selectedScenario = customScenario;
    $("scenarioSelect").value = customScenario.id;
    simState = await api("/api/load", {id: customScenario.id});
    config = configFromScenario(customScenario);
    started = false;
    dirty = false;
    viewIndex = 0;
    renderScenario();
    render();
    setStatus("Custom scenario saved.", "ok");
  } catch (error) {
    setStatus(error.message, "error");
  }
}

async function saveEvaluation() {
  try {
    const data = {
      scenario_id: selectedScenario.id,
      scenario_name: selectedScenario.name,
      result: $("evaluationResult").value,
      evaluator: $("evaluator").value,
      observations: $("observations").value,
      related_tick: currentSnapshot()?.tick ?? 0,
      evaluated_requirements: selectedScenario.requirements || [],
      evaluated_at: new Date().toISOString(),
    };
    await api("/api/evaluation", data);
    $("evaluationStatus").textContent = `${data.result} saved for ${data.scenario_id} at tick ${data.related_tick}.`;
  } catch (error) {
    $("evaluationStatus").textContent = error.message;
  }
}

function exportTrace() {
  const blob = new Blob([JSON.stringify({
    scenario: selectedScenario,
    history: simState.history,
    human_verdict: $("evaluationResult").value,
    observations: $("observations").value,
  }, null, 2)], {type: "application/json"});
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = `${selectedScenario.id}-execution-trace.json`;
  link.click();
  URL.revokeObjectURL(link.href);
}

async function reset() {
  pause();
  try {
    if (dirty) {
      simState = await api("/api/custom-map", currentConfig());
    } else {
      simState = await api("/api/reset", {});
    }
    started = false;
    viewIndex = 0;
    render();
    setStatus("Controller, position, direction, dust and history reset.", "ok");
  } catch (error) {
    setStatus(error.message, "error");
  }
}

async function restart() {
  pause();
  try {
    if (selectedScenario.id.startsWith("CUSTOM-")) {
      await loadScenario(selectedScenario);
    } else {
      simState = await api("/api/restart", {});
      config = configFromScenario(selectedScenario);
      started = false;
      dirty = false;
      viewIndex = 0;
      renderScenario();
      render();
    }
  } catch (error) {
    setStatus(error.message, "error");
  }
}

$("scenarioSelect").addEventListener("change", async (event) => {
  const scenario = scenarios.find((item) => item.id === event.target.value);
  if (scenario) await loadScenario(scenario);
});
$("directionSelect").addEventListener("change", () => { if (!started && config) { config.direction = $("directionSelect").value; dirty = true; renderGrid(); } });
$("tickLimit").addEventListener("change", () => { if (!started && config) { config.max_ticks = Number($("tickLimit").value); dirty = true; } });
$("clearMap").addEventListener("click", () => { if (!started) { config.obstacles = []; config.dust = []; dirty = true; renderGrid(); renderScenario(); } });
$("saveScenario").addEventListener("click", saveCustomScenario);
$("startButton").addEventListener("click", start);
$("pauseButton").addEventListener("click", pause);
$("stepButton").addEventListener("click", async () => { pause(); try { await stepForward(); } catch (error) { setStatus(error.message, "error"); } });
$("backButton").addEventListener("click", () => { pause(); viewIndex = Math.max(0, viewIndex - 1); render(); });
$("forwardButton").addEventListener("click", async () => { pause(); try { await stepForward(); } catch (error) { setStatus(error.message, "error"); } });
$("resetButton").addEventListener("click", reset);
$("restartButton").addEventListener("click", restart);
$("exportButton").addEventListener("click", exportTrace);
$("speed").addEventListener("input", (event) => {
  $("speedLabel").textContent = `${event.target.value} ms`;
  if (playTimer !== null) {
    pause();
    start();
  }
});
$("saveEvaluation").addEventListener("click", saveEvaluation);

(async function init() {
  try {
    scenarios = await api("/api/scenarios");
    populateScenarioSelect();
    await loadScenario(scenarios[0]);
    setStatus("Connected · compiled C controller", "ok");
  } catch (error) {
    setStatus(error.message, "error");
  }
})();
