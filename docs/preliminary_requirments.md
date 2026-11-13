# Preliminary Requirements — RVC Automatic Cleaning

- **RVC-01** The RVC automatically cleans and mops household surfaces.
- **RVC-02** While cleaning, the RVC moves straight forward.
- **RVC-03** When an obstacle is detected, the RVC stops cleaning, turns aside left or right, and then moves forward while cleaning.
- **RVC-04** When obstacles are detected in front, left, and right, the RVC stops cleaning while it moves backward and turns aside left or right, then resumes cleaning as it moves forward.
- **RVC-05** When dust is detected, cleaning power is raised temporarily:
  1. The controller starts or refreshes a five-simulation-tick boost interval on every dust-positive tick, counting that tick as the first interval tick.
  2. The interval advances on every simulation tick, including ticks that execute remaining actions from a previously selected movement sequence and ticks when cleaning is stopped.
  3. The effective cleaning-power output is **Boost** only while cleaning is active and the interval has time remaining. It is **Normal** while cleaning is stopped, even if the internal interval has time remaining.
  4. If cleaning resumes before the interval expires, the remaining interval is applied; at expiry the effective mode is **Normal**.
  5. The controller reports Normal or Boost mode; numeric power levels and hardware actuator details remain outside scope.
- **RVC-06** Detailed hardware control design and implementation are outside scope.
- **RVC-07** This project focuses on the automatic cleaning function.

## Simulation-tick definition for RVC-05

A simulation tick is one discrete simulator update. A tick advances the boost timer exactly once. The controller may select a new movement sequence on a subset of ticks, but that does not pause the boost timer. Effective power output is gated by whether the current movement-sequence action is cleaning.

## Clarification record

RVC-05 was clarified during implementation review: five simulation ticks; dust detected during an active interval refreshes the interval; the timer continues while cleaning is stopped, but Boost is commanded only while cleaning is active. The power increase is represented abstractly because no numeric level was specified.
