#ifndef RVC_CONTROLLER_H
#define RVC_CONTROLLER_H

#include <stdbool.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

#define RVC_MAX_MOVEMENT_COMMANDS 3
#define RVC_DUST_BOOST_DURATION_TICKS 5U

typedef enum {
    RVC_STATE_FORWARD,
    RVC_STATE_OBSTACLE_AVOIDANCE,
    RVC_STATE_ALL_DIRECTIONS_BLOCKED
} RvcControllerState;

typedef enum {
    RVC_MOVE_FORWARD,
    RVC_MOVE_TURN_ASIDE,
    RVC_MOVE_BACKWARD
} RvcMovementAction;

typedef enum {
    RVC_CLEANING_AND_MOP,
    RVC_CLEANING_STOP_THEN_CLEAN_AND_MOP
} RvcCleaningAction;

typedef enum {
    RVC_POWER_NORMAL,
    RVC_POWER_BOOST
} RvcCleaningPowerMode;

typedef struct {
    RvcCleaningPowerMode mode;
    unsigned int remaining_ticks;
} RvcCleaningPowerState;

typedef struct {
    bool front_obstacle;
    bool left_obstacle;
    bool right_obstacle;
    bool dust_detected;
} RvcSensorInput;

typedef struct {
    RvcControllerState state;
    unsigned int boost_ticks_remaining;
} RvcController;

typedef struct {
    RvcMovementAction movement[RVC_MAX_MOVEMENT_COMMANDS];
    size_t movement_count;
    RvcCleaningAction cleaning_action;
    RvcCleaningPowerMode cleaning_power_mode;
    unsigned int boost_ticks_remaining;
} RvcControllerOutput;

void rvc_controller_init(RvcController *controller);
/* Select movement/cleaning action when a movement decision is due. */
bool rvc_controller_step(RvcController *controller,
                         const RvcSensorInput *input,
                         RvcControllerOutput *output);
/* Must be called each simulation tick; power is Boost only when cleaning_active. */
bool rvc_controller_advance_tick(RvcController *controller,
                                 bool dust_detected,
                                 bool cleaning_active,
                                 RvcCleaningPowerState *power_state);

#ifdef __cplusplus
}
#endif

#endif
