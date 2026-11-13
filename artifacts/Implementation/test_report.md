# Unit Test and Coverage Report — Cleaning-Gated Dust Boost

## Build

- Production: C11, GCC 16.2.0; tests: C++17/G++ 16.2.0 with GoogleTest 1.18.0.
- Build system: CMake 4.4.5; test runner: CTest.
- Coverage: GCC `gcov-16 -b -c` on `src/rvc_controller.c`.

Reproduction commands:

```sh
cmake -S . -B build \
  -DCMAKE_C_COMPILER=/opt/homebrew/opt/gcc/bin/gcc-16 \
  -DCMAKE_CXX_COMPILER=/opt/homebrew/opt/gcc/bin/g++-16 \
  -DGTEST_SOURCE_ROOT=/opt/homebrew/Cellar/googletest/1.18.0/include/googletest/googletest \
  -DGTEST_INCLUDE_ROOT=/opt/homebrew/Cellar/googletest/1.18.0/include \
  -DRVC_ENABLE_COVERAGE=ON
cmake --build build --parallel 4
ctest --test-dir build --output-on-failure
/opt/homebrew/opt/gcc/bin/gcov-16 -b -c build/CMakeFiles/rvc_controller.dir/src/rvc_controller.c.gcno
```

## TDD Evidence

1. **RED:** Added five tests for five-tick activation/expiry, obstacle/dust independence, refresh, initialization reset, and timer advancement during movement-sequence ticks. With the timer API stubbed but no timer state behavior, these five tests failed on power mode and remaining-tick expectations.
2. **GREEN:** Added `boost_ticks_remaining` to controller state, a Normal/Boost output mode, and `rvc_controller_advance_tick`. Dust sets/refreshes five ticks; no-dust ticks decrement; zero returns Normal. All tests passed.
3. **Refactor:** Extracted timer-state and power-mode helpers; rebuilt and reran all tests.
4. **Cleaning-state correction:** Passed the current cleaning activity into the C tick API. The boost timer continues while stopped, while the effective C output is Normal; it resumes as Boost only if time remains when cleaning resumes.

## Test Cases

| Test | Requirement / behavior |
|---|---|
| StartsInForwardStateAndMovesForwardWhenClear | RVC-01–RVC-02; baseline mode Normal |
| ObstacleTurnsAsideThenContinuesForward | RVC-03 |
| AllDirectionsBlockedMovesBackwardTurnsAndThenMovesForward | RVC-04 |
| DustStartsFiveTickBoostAndReturnsToNormal | RVC-05; five active ticks and expiry |
| DustTimerCanBeActiveWhileObstacleHandlingStopsCleaning | RVC-03/RVC-05; timer can remain active while effective output is Normal |
| DustDetectedDuringBoostRefreshesFiveTickInterval | RVC-05; retrigger resets interval |
| InitializationClearsBoostTimer | RVC-05; starts Normal |
| BoostTimerAdvancesOnEachTickIndependentOfMovementDecision | RVC-05; queued movement does not pause timer |
| BoostOutputResumesOnlyWhenCleaningResumes | RVC-02/RVC-04/RVC-05; stopped cleaning gates output and forward cleaning resumes the remaining interval |
| StateFollowsEachObstacleCondition | Movement FSM transitions |
| ClassifiesEveryFrontLeftRightSensorCombination | All eight obstacle input combinations |
| AppliesEachObstacleConditionFromEveryCurrentState | All nine FSM transitions |
| RejectsNullStepArguments | API input validation |
| RejectsNullTickArguments | API input validation |
| NullInitializationIsSafe | API input validation |

## Test Results

Command: `ctest --test-dir build --output-on-failure`

- Passed: 15 / 15
- Failed: 0
- TDD Red evidence: five new boost-state tests failed against the timer stub before implementation.

## Coverage

- Line coverage: 100% (75 / 75)
- Branch outcomes executed: 100% (46 / 46)
- Calls executed: 100% (9 / 9)

Coverage applies to the C controller library. It does not measure the web adapter or hardware integration.

## System Test Link

The updated C controller was also exercised through the web simulator in 21 scenarios and 117 ticks. Results and per-tick traces are in `artifacts/SystemTest/test_results.md` and `artifacts/SystemTest/execution_traces.json`. Scenario requirement verdicts remain pending human evaluation; the harness does not mark PASS/FAIL.
