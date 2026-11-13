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
    EXPECT_EQ(output.cleaning_power_mode, RVC_POWER_NORMAL);
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
    EXPECT_EQ(output.cleaning_action, RVC_CLEANING_STOP_THEN_CLEAN_AND_MOP);
    EXPECT_EQ(controller.state, RVC_STATE_ALL_DIRECTIONS_BLOCKED);
}

TEST(RvcController, DustStartsFiveTickBoostAndReturnsToNormal)
{
    RvcController controller{};
    RvcCleaningPowerState power{};

    rvc_controller_init(&controller);
    ASSERT_TRUE(rvc_controller_advance_tick(&controller, true, true, &power));
    EXPECT_EQ(power.mode, RVC_POWER_BOOST);
    EXPECT_EQ(power.remaining_ticks, 5U);

    for (unsigned int remaining = 4U; remaining > 0U; --remaining) {
        ASSERT_TRUE(rvc_controller_advance_tick(&controller, false, true, &power));
        EXPECT_EQ(power.mode, RVC_POWER_BOOST);
        EXPECT_EQ(power.remaining_ticks, remaining);
    }
    ASSERT_TRUE(rvc_controller_advance_tick(&controller, false, true, &power));
    EXPECT_EQ(power.mode, RVC_POWER_NORMAL);
    EXPECT_EQ(power.remaining_ticks, 0U);
}

TEST(RvcController, DustTimerCanBeActiveWhileObstacleHandlingStopsCleaning)
{
    RvcController controller{};
    RvcControllerOutput output{};
    RvcCleaningPowerState power{};
    const RvcSensorInput input{true, false, false, true};

    rvc_controller_init(&controller);
    ASSERT_TRUE(rvc_controller_advance_tick(&controller, input.dust_detected, false, &power));
    ASSERT_TRUE(rvc_controller_step(&controller, &input, &output));

    EXPECT_EQ(output.cleaning_action, RVC_CLEANING_STOP_THEN_CLEAN_AND_MOP);
    EXPECT_EQ(output.cleaning_power_mode, RVC_POWER_NORMAL);
    EXPECT_EQ(power.mode, RVC_POWER_NORMAL);
    EXPECT_EQ(power.remaining_ticks, 5U);
}

TEST(RvcController, DustDetectedDuringBoostRefreshesFiveTickInterval)
{
    RvcController controller{};
    RvcCleaningPowerState power{};
    rvc_controller_init(&controller);

    ASSERT_TRUE(rvc_controller_advance_tick(&controller, true, true, &power));
    ASSERT_TRUE(rvc_controller_advance_tick(&controller, false, true, &power));
    EXPECT_EQ(power.remaining_ticks, 4U);
    ASSERT_TRUE(rvc_controller_advance_tick(&controller, true, true, &power));
    EXPECT_EQ(power.mode, RVC_POWER_BOOST);
    EXPECT_EQ(power.remaining_ticks, 5U);

    for (unsigned int remaining = 4U; remaining > 0U; --remaining) {
        ASSERT_TRUE(rvc_controller_advance_tick(&controller, false, true, &power));
        EXPECT_EQ(power.remaining_ticks, remaining);
        EXPECT_EQ(power.mode, RVC_POWER_BOOST);
    }
    ASSERT_TRUE(rvc_controller_advance_tick(&controller, false, true, &power));
    EXPECT_EQ(power.mode, RVC_POWER_NORMAL);
}

TEST(RvcController, InitializationClearsBoostTimer)
{
    RvcController controller{};
    RvcCleaningPowerState power{};
    rvc_controller_init(&controller);
    ASSERT_TRUE(rvc_controller_advance_tick(&controller, true, true, &power));
    ASSERT_EQ(controller.boost_ticks_remaining, 5U);

    rvc_controller_init(&controller);
    EXPECT_EQ(controller.boost_ticks_remaining, 0U);
    ASSERT_TRUE(rvc_controller_advance_tick(&controller, false, true, &power));
    EXPECT_EQ(power.mode, RVC_POWER_NORMAL);
}

TEST(RvcController, BoostTimerAdvancesOnEachTickIndependentOfMovementDecision)
{
    RvcController controller{};
    RvcControllerOutput output{};
    RvcCleaningPowerState power{};
    const RvcSensorInput obstacle{true, false, false, false};
    rvc_controller_init(&controller);
    ASSERT_TRUE(rvc_controller_advance_tick(&controller, true, false, &power));
    ASSERT_TRUE(rvc_controller_step(&controller, &obstacle, &output));
    ASSERT_EQ(output.movement_count, 2U);

    for (unsigned int remaining = 4U; remaining > 0U; --remaining) {
        ASSERT_TRUE(rvc_controller_advance_tick(&controller, false, false, &power));
        EXPECT_EQ(power.remaining_ticks, remaining);
        EXPECT_EQ(power.mode, RVC_POWER_NORMAL);
    }
}

TEST(RvcController, BoostOutputResumesOnlyWhenCleaningResumes)
{
    RvcController controller{};
    RvcCleaningPowerState power{};
    rvc_controller_init(&controller);

    ASSERT_TRUE(rvc_controller_advance_tick(&controller, true, false, &power));
    EXPECT_EQ(power.mode, RVC_POWER_NORMAL);
    EXPECT_EQ(power.remaining_ticks, 5U);

    ASSERT_TRUE(rvc_controller_advance_tick(&controller, false, false, &power));
    EXPECT_EQ(power.mode, RVC_POWER_NORMAL);
    EXPECT_EQ(power.remaining_ticks, 4U);

    ASSERT_TRUE(rvc_controller_advance_tick(&controller, false, true, &power));
    EXPECT_EQ(power.mode, RVC_POWER_BOOST);
    EXPECT_EQ(power.remaining_ticks, 3U);
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
            RvcController controller{state, 0U};
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

TEST(RvcController, RejectsNullTickArguments)
{
    RvcController controller{};
    RvcCleaningPowerState power{};
    EXPECT_FALSE(rvc_controller_advance_tick(nullptr, false, false, &power));
    EXPECT_FALSE(rvc_controller_advance_tick(&controller, false, false, nullptr));
}

TEST(RvcController, NullInitializationIsSafe)
{
    EXPECT_NO_THROW(rvc_controller_init(nullptr));
}
