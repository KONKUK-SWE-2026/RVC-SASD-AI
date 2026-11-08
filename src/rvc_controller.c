#include "rvc_controller.h"

typedef enum {
    OBSTACLE_CLEAR,
    OBSTACLE_DETECTED,
    OBSTACLE_ALL_DIRECTIONS
} ObstacleCondition;

typedef struct {
    RvcMovementAction actions[RVC_MAX_MOVEMENT_COMMANDS];
    size_t count;
} MovementSequence;

static ObstacleCondition classify_obstacle_condition(const RvcSensorInput *input)
{
    if (input->front_obstacle && input->left_obstacle && input->right_obstacle) {
        return OBSTACLE_ALL_DIRECTIONS;
    }
    if (input->front_obstacle || input->left_obstacle || input->right_obstacle) {
        return OBSTACLE_DETECTED;
    }
    return OBSTACLE_CLEAR;
}

static MovementSequence select_movement_sequence(ObstacleCondition condition)
{
    MovementSequence sequence = {{RVC_MOVE_FORWARD}, 1};

    if (condition == OBSTACLE_DETECTED) {
        sequence.actions[0] = RVC_MOVE_TURN_ASIDE;
        sequence.actions[1] = RVC_MOVE_FORWARD;
        sequence.count = 2;
    } else if (condition == OBSTACLE_ALL_DIRECTIONS) {
        sequence.actions[0] = RVC_MOVE_BACKWARD;
        sequence.actions[1] = RVC_MOVE_TURN_ASIDE;
        sequence.actions[2] = RVC_MOVE_FORWARD;
        sequence.count = 3;
    }

    return sequence;
}

static void produce_movement_command(const MovementSequence *sequence,
                                     RvcControllerOutput *output)
{
    output->movement_count = sequence->count;
    for (size_t i = 0; i < sequence->count; ++i) {
        output->movement[i] = sequence->actions[i];
    }
}

static RvcCleaningAction determine_obstacle_cleaning_action(ObstacleCondition condition)
{
    if (condition == OBSTACLE_DETECTED) {
        return RVC_CLEANING_STOP_THEN_CLEAN_AND_MOP;
    }
    if (condition == OBSTACLE_ALL_DIRECTIONS) {
        return RVC_CLEANING_STOP_THEN_UNSPECIFIED;
    }
    return RVC_CLEANING_AND_MOP;
}

static bool determine_dust_power_adjustment(const RvcSensorInput *input)
{
    return input->dust_detected;
}

static ObstacleCondition determine_movement_response(const RvcSensorInput *input,
                                                      RvcControllerOutput *output)
{
    const ObstacleCondition condition = classify_obstacle_condition(input);
    const MovementSequence sequence = select_movement_sequence(condition);
    produce_movement_command(&sequence, output);
    return condition;
}

static void control_cleaning_behavior(ObstacleCondition condition,
                                      const RvcSensorInput *input,
                                      RvcControllerOutput *output)
{
    output->cleaning_action = determine_obstacle_cleaning_action(condition);
    output->request_temporary_power_boost = determine_dust_power_adjustment(input);
}

void rvc_controller_init(RvcController *controller)
{
    if (controller != NULL) {
        controller->state = RVC_STATE_FORWARD;
    }
}

bool rvc_controller_step(RvcController *controller,
                         const RvcSensorInput *input,
                         RvcControllerOutput *output)
{
    if (controller == NULL || input == NULL || output == NULL) {
        return false;
    }

    RvcControllerOutput result = {0};
    const ObstacleCondition condition = determine_movement_response(input, &result);
    control_cleaning_behavior(condition, input, &result);

    if (condition == OBSTACLE_CLEAR) {
        controller->state = RVC_STATE_FORWARD;
    } else if (condition == OBSTACLE_DETECTED) {
        controller->state = RVC_STATE_OBSTACLE_AVOIDANCE;
    } else {
        controller->state = RVC_STATE_ALL_DIRECTIONS_BLOCKED;
    }

    *output = result;
    return true;
}
