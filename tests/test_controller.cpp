#include "rvc_controller.h"

#include <gtest/gtest.h>

TEST(RvcController, StartsInForwardStateAndMovesForwardWhenClear)
{
    RvcController controller{};
    RvcControllerOutput output{};
    const RvcSensorInput input{};

    rvc_controller_init(&controller);
    ASSERT_EQ(controller.state, RVC_STATE_FORWARD);
    ASSERT_TRUE(rvc_controller_step(&controller, &input, &output));

    EXPECT_EQ(output.movement_count, 1U);
    EXPECT_EQ(output.movement[0], RVC_MOVE_FORWARD);
    EXPECT_EQ(output.cleaning_action, RVC_CLEANING_AND_MOP);
    EXPECT_FALSE(output.request_temporary_power_boost);
}

TEST(RvcController, ObstacleTurnsAsideThenContinuesForward)
{
    RvcController controller{};
    RvcControllerOutput output{};
    const RvcSensorInput input{true, false, false, false};

    rvc_controller_init(&controller);
    ASSERT_TRUE(rvc_controller_step(&controller, &input, &output));

    ASSERT_EQ(output.movement_count, 2U);
    EXPECT_EQ(output.movement[0], RVC_MOVE_TURN_ASIDE);
    EXPECT_EQ(output.movement[1], RVC_MOVE_FORWARD);
    EXPECT_EQ(output.cleaning_action, RVC_CLEANING_STOP_THEN_CLEAN_AND_MOP);
    EXPECT_EQ(controller.state, RVC_STATE_OBSTACLE_AVOIDANCE);
}

TEST(RvcController, AllDirectionsBlockedMovesBackwardTurnsAndThenMovesForward)
{
    RvcController controller{};
    RvcControllerOutput output{};
    const RvcSensorInput input{true, true, true, false};

    rvc_controller_init(&controller);
    ASSERT_TRUE(rvc_controller_step(&controller, &input, &output));

    ASSERT_EQ(output.movement_count, 3U);
    EXPECT_EQ(output.movement[0], RVC_MOVE_BACKWARD);
    EXPECT_EQ(output.movement[1], RVC_MOVE_TURN_ASIDE);
    EXPECT_EQ(output.movement[2], RVC_MOVE_FORWARD);
    EXPECT_EQ(output.cleaning_action, RVC_CLEANING_STOP_THEN_UNSPECIFIED);
    EXPECT_EQ(controller.state, RVC_STATE_ALL_DIRECTIONS_BLOCKED);
}

TEST(RvcController, DustRequestsTemporaryCleaningPowerBoost)
{
    RvcController controller{};
    RvcControllerOutput output{};
    const RvcSensorInput input{false, false, false, true};

    rvc_controller_init(&controller);
    ASSERT_TRUE(rvc_controller_step(&controller, &input, &output));

    EXPECT_TRUE(output.request_temporary_power_boost);
    EXPECT_EQ(output.cleaning_action, RVC_CLEANING_AND_MOP);
}

TEST(RvcController, ObstacleAndDustOutputsRemainIndependent)
{
    RvcController controller{};
    RvcControllerOutput output{};
    const RvcSensorInput input{true, false, false, true};

    rvc_controller_init(&controller);
    ASSERT_TRUE(rvc_controller_step(&controller, &input, &output));

    EXPECT_EQ(output.cleaning_action, RVC_CLEANING_STOP_THEN_CLEAN_AND_MOP);
    EXPECT_TRUE(output.request_temporary_power_boost);
}

TEST(RvcController, StateFollowsEachObstacleCondition)
{
    RvcController controller{};
    RvcControllerOutput output{};
    const RvcSensorInput blocked{true, true, true, false};
    const RvcSensorInput obstacle{false, true, false, false};
    const RvcSensorInput clear{};

    rvc_controller_init(&controller);
    ASSERT_TRUE(rvc_controller_step(&controller, &blocked, &output));
    EXPECT_EQ(controller.state, RVC_STATE_ALL_DIRECTIONS_BLOCKED);

    ASSERT_TRUE(rvc_controller_step(&controller, &obstacle, &output));
    EXPECT_EQ(controller.state, RVC_STATE_OBSTACLE_AVOIDANCE);

    ASSERT_TRUE(rvc_controller_step(&controller, &clear, &output));
    EXPECT_EQ(controller.state, RVC_STATE_FORWARD);
}

TEST(RvcController, ClassifiesEveryFrontLeftRightSensorCombination)
{
    for (unsigned int mask = 0; mask < 8; ++mask) {
        RvcController controller{};
        RvcControllerOutput output{};
        const RvcSensorInput input{
            (mask & 1U) != 0,
            (mask & 2U) != 0,
            (mask & 4U) != 0,
            false};

        rvc_controller_init(&controller);
        ASSERT_TRUE(rvc_controller_step(&controller, &input, &output));

        if (mask == 0U) {
            EXPECT_EQ(output.movement_count, 1U);
            EXPECT_EQ(controller.state, RVC_STATE_FORWARD);
        } else if (mask == 7U) {
            EXPECT_EQ(output.movement_count, 3U);
            EXPECT_EQ(controller.state, RVC_STATE_ALL_DIRECTIONS_BLOCKED);
        } else {
            EXPECT_EQ(output.movement_count, 2U);
            EXPECT_EQ(controller.state, RVC_STATE_OBSTACLE_AVOIDANCE);
        }
    }
}

TEST(RvcController, AppliesEachObstacleConditionFromEveryCurrentState)
{
    const RvcControllerState states[] = {
        RVC_STATE_FORWARD,
        RVC_STATE_OBSTACLE_AVOIDANCE,
        RVC_STATE_ALL_DIRECTIONS_BLOCKED};
    const RvcSensorInput inputs[] = {
        {},
        {true, false, false, false},
        {true, true, true, false}};
    const RvcControllerState expected[] = {
        RVC_STATE_FORWARD,
        RVC_STATE_OBSTACLE_AVOIDANCE,
        RVC_STATE_ALL_DIRECTIONS_BLOCKED};

    for (const auto state : states) {
        for (size_t i = 0; i < 3; ++i) {
            RvcController controller{state};
            RvcControllerOutput output{};
            ASSERT_TRUE(rvc_controller_step(&controller, &inputs[i], &output));
            EXPECT_EQ(controller.state, expected[i]);
        }
    }
}

TEST(RvcController, RejectsNullStepArguments)
{
    RvcController controller{};
    RvcControllerOutput output{};
    const RvcSensorInput input{};

    rvc_controller_init(&controller);
    EXPECT_FALSE(rvc_controller_step(nullptr, &input, &output));
    EXPECT_FALSE(rvc_controller_step(&controller, nullptr, &output));
    EXPECT_FALSE(rvc_controller_step(&controller, &input, nullptr));
}

TEST(RvcController, NullInitializationIsSafe)
{
    EXPECT_NO_THROW(rvc_controller_init(nullptr));
}
