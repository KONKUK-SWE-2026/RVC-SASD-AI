cmake_minimum_required(VERSION 3.20)
project(rvc_controller LANGUAGES C CXX)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_C_EXTENSIONS OFF)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

option(RVC_ENABLE_COVERAGE "Enable GCC line and branch coverage" ON)

add_library(rvc_controller STATIC src/rvc_controller.c)
target_include_directories(rvc_controller PUBLIC include)
target_compile_options(rvc_controller PRIVATE -Wall -Wextra -Werror -pedantic)

add_library(rvc_controller_shared SHARED src/rvc_controller.c)
target_include_directories(rvc_controller_shared PUBLIC include)
target_compile_options(rvc_controller_shared PRIVATE -Wall -Wextra -Werror -pedantic)
set_target_properties(rvc_controller_shared PROPERTIES OUTPUT_NAME rvc_controller)

if(RVC_ENABLE_COVERAGE AND CMAKE_C_COMPILER_ID STREQUAL "GNU")
    target_compile_options(rvc_controller PRIVATE --coverage -O0 -g)
endif()

set(GTEST_SOURCE_ROOT "" CACHE PATH "GoogleTest source root for toolchain-compatible builds")
if(GTEST_SOURCE_ROOT)
    set(GTEST_INCLUDE_ROOT "${GTEST_SOURCE_ROOT}/include" CACHE PATH
        "GoogleTest include root for source builds")
    add_library(rvc_gtest STATIC ${GTEST_SOURCE_ROOT}/src/gtest-all.cc)
    target_include_directories(rvc_gtest PUBLIC ${GTEST_INCLUDE_ROOT}
                                           PRIVATE ${GTEST_SOURCE_ROOT})

    add_library(rvc_gtest_main STATIC ${GTEST_SOURCE_ROOT}/src/gtest_main.cc)
    target_include_directories(rvc_gtest_main PUBLIC ${GTEST_INCLUDE_ROOT})
    target_link_libraries(rvc_gtest_main PUBLIC rvc_gtest)
    add_library(GTest::gtest_main ALIAS rvc_gtest_main)
else()
    find_package(GTest CONFIG REQUIRED)
endif()
include(CTest)
include(GoogleTest)

add_executable(rvc_controller_tests tests/test_controller.cpp)
target_compile_options(rvc_controller_tests PRIVATE -Wall -Wextra -Werror -pedantic)
target_link_libraries(rvc_controller_tests PRIVATE rvc_controller GTest::gtest_main)

if(RVC_ENABLE_COVERAGE AND CMAKE_C_COMPILER_ID STREQUAL "GNU")
    target_link_options(rvc_controller_tests PRIVATE --coverage)
endif()

gtest_discover_tests(rvc_controller_tests)
