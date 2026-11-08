#ifndef RVC_CONTROLLER_H
#define RVC_CONTROLLER_H

#include <stdbool.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

#define RVC_MAX_MOVEMENT_COMMANDS 3

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
    RVC_CLEANING_STOP_THEN_CLEAN_AND_MOP,
    RVC_CLEANING_STOP_THEN_UNSPECIFIED
} RvcCleaningAction;

typedef struct {
    bool front_obstacle;
    bool left_obstacle;
    bool right_obstacle;
    bool dust_detected;
} RvcSensorInput;

typedef struct {
    RvcControllerState state;
} RvcController;

typedef struct {
    RvcMovementAction movement[RVC_MAX_MOVEMENT_COMMANDS];
    size_t movement_count;
    RvcCleaningAction cleaning_action;
    bool request_temporary_power_boost;
} RvcControllerOutput;

void rvc_controller_init(RvcController *controller);
bool rvc_controller_step(RvcController *controller,
                         const RvcSensorInput *input,
                         RvcControllerOutput *output);

#ifdef __cplusplus
}
#endif

#endif
