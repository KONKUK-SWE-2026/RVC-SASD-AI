# Unit Test and Coverage Report

## Build

- Production language: C11.
- Compiler: GCC 16.2.0 (`/opt/homebrew/opt/gcc/bin/gcc-16`).
- Test language/compiler: C++17 with G++ 16.2.0.
- Build system: CMake 4.4.5.
- Test framework: GoogleTest 1.18.0, built from the installed source tree with G++ to match the compiler runtime.
- Test runner: CTest.

The local prebuilt GoogleTest library uses Clang's C++ runtime and cannot link with G++. The build supports `GTEST_SOURCE_ROOT` and `GTEST_INCLUDE_ROOT` to build the installed GoogleTest sources with the selected toolchain.

Reproduction commands used in this environment:

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

## TDD Execution

1. **RED:** The initial controller stub built. Six behavior tests failed because `rvc_controller_step` returned `false`; the two null-initialization/validation tests passed.
2. **GREEN:** Implemented the minimum controller behavior and reran the suite; all 10 tests passed.
3. **Coverage refinement:** Added exhaustive front/left/right sensor combinations and all state/condition transitions, then reran the suite and coverage.

## Test Cases

| Test | Requirement / Behavior |
|---|---|
| StartsInForwardStateAndMovesForwardWhenClear | R1–R2; initial forward movement and baseline cleaning |
| ObstacleTurnsAsideThenContinuesForward | R3; turn aside, continue forward, stop then resume cleaning |
| AllDirectionsBlockedMovesBackwardTurnsAndThenMovesForward | R4; backward, turn aside, then forward |
| DustRequestsTemporaryCleaningPowerBoost | R5; dust boost request |
| ObstacleAndDustOutputsRemainIndependent | R3/R5; preserve both outputs without inventing priority |
| StateFollowsEachObstacleCondition | FSM transitions between forward, avoidance, and all-blocked states |
| ClassifiesEveryFrontLeftRightSensorCombination | Exhaustive 8 combinations of the three obstacle inputs |
| AppliesEachObstacleConditionFromEveryCurrentState | All 9 current-state/condition transition combinations |
| RejectsNullStepArguments | Invalid API pointers do not cause dereferences |
| NullInitializationIsSafe | Null initialization is safe |

## Test Execution Results

Command: `ctest --test-dir build --output-on-failure`

- Passed: 10 / 10
- Failed: 0

## Coverage

Measured with GCC 16 `gcov-16 -b -c` on `src/rvc_controller.c`.

- Line coverage: 100% (57 / 57 lines)
- Branch outcomes executed: 100% (34 / 34)
- Calls executed: 100% (7 / 7)

Coverage counts apply to the controller library source only; no hardware integration or `main()` loop is present in this repository.

