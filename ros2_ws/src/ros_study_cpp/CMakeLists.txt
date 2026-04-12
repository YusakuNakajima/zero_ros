cmake_minimum_required(VERSION 3.8)
project(ros_study_cpp)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(geometric_shapes REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(moveit_msgs REQUIRED)
find_package(moveit_ros_planning_interface REQUIRED)
find_package(rclcpp REQUIRED)
find_package(shape_msgs REQUIRED)
find_package(tf2 REQUIRED)

add_executable(ur_moveit_demo_cpp src/ur_moveit_demo.cpp)
ament_target_dependencies(ur_moveit_demo_cpp rclcpp moveit_ros_planning_interface geometry_msgs tf2)

add_executable(
  load_planning_scene
  src/load_planning_scene.cpp
  src/load_planning_scene_main.cpp
)
target_include_directories(load_planning_scene PUBLIC include)
ament_target_dependencies(
  load_planning_scene
  geometric_shapes
  geometry_msgs
  moveit_msgs
  rclcpp
  shape_msgs
)

install(
  TARGETS
    load_planning_scene
    ur_moveit_demo_cpp
  DESTINATION lib/${PROJECT_NAME}
)

install(
  DIRECTORY
    config
  DESTINATION share/${PROJECT_NAME}
)

install(
  DIRECTORY
    include/
  DESTINATION include
)

ament_package()
