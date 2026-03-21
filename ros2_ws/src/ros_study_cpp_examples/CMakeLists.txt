cmake_minimum_required(VERSION 3.8)
project(ros_study_cpp_examples)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(moveit_ros_planning_interface REQUIRED)
find_package(rclcpp REQUIRED)
find_package(tf2 REQUIRED)

add_executable(ur_moveit_demo_cpp src/ur_moveit_demo.cpp)
ament_target_dependencies(ur_moveit_demo_cpp rclcpp moveit_ros_planning_interface geometry_msgs tf2)

add_executable(moveit_example_node src/moveit_example_node.cpp)
ament_target_dependencies(moveit_example_node rclcpp moveit_ros_planning_interface geometry_msgs)

install(TARGETS
  ur_moveit_demo_cpp
  moveit_example_node
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
