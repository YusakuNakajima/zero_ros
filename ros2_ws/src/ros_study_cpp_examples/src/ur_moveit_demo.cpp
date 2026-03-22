#include <rclcpp/rclcpp.hpp>
#include <moveit/move_group_interface/move_group_interface.h>
#include <geometry_msgs/msg/pose.hpp>
#include <tf2/LinearMath/Quaternion.h>
#include <chrono>
#include <cmath>
#include <thread>
#include <vector>

namespace
{
constexpr char kDefaultPlanningGroup[] = "ur_manipulator";
constexpr double kDefaultVelocityScaling = 0.1;
constexpr double kDefaultAccelerationScaling = 0.1;

bool plan_and_execute(
  moveit::planning_interface::MoveGroupInterface & move_group_interface,
  const rclcpp::Logger & logger,
  const std::string & label)
{
  moveit::planning_interface::MoveGroupInterface::Plan plan;
  const auto result = move_group_interface.plan(plan);
  if (result != moveit::core::MoveItErrorCode::SUCCESS) {
    RCLCPP_ERROR(logger, "[%s] Planning failed.", label.c_str());
    return false;
  }

  const auto execute_result = move_group_interface.execute(plan);
  if (execute_result != moveit::core::MoveItErrorCode::SUCCESS) {
    RCLCPP_ERROR(logger, "[%s] Execution failed.", label.c_str());
    return false;
  }

  RCLCPP_INFO(logger, "[%s] Planning and execution succeeded.", label.c_str());
  return true;
}
}  // namespace

int main(int argc, char** argv)
{
  rclcpp::init(argc, argv);

  rclcpp::NodeOptions node_options;
  node_options.automatically_declare_parameters_from_overrides(true);
  auto node = rclcpp::Node::make_shared("ur_moveit_demo_cpp", node_options);
  auto logger = node->get_logger();

  const auto planning_group =
    node->declare_parameter<std::string>("planning_group", kDefaultPlanningGroup);
  const auto velocity_scaling =
    node->declare_parameter<double>("velocity_scaling", kDefaultVelocityScaling);
  const auto acceleration_scaling =
    node->declare_parameter<double>("acceleration_scaling", kDefaultAccelerationScaling);

  rclcpp::executors::MultiThreadedExecutor executor;
  executor.add_node(node);
  std::thread executor_thread([&executor]() { executor.spin(); });

  using moveit::planning_interface::MoveGroupInterface;
  auto move_group_interface = MoveGroupInterface(node, planning_group);
  move_group_interface.startStateMonitor();
  move_group_interface.setPlanningTime(5.0);
  move_group_interface.setNumPlanningAttempts(5);
  move_group_interface.setMaxVelocityScalingFactor(velocity_scaling);
  move_group_interface.setMaxAccelerationScalingFactor(acceleration_scaling);

  RCLCPP_INFO(logger, "Planning group: %s", planning_group.c_str());
  RCLCPP_INFO(logger, "Planning frame: %s", move_group_interface.getPlanningFrame().c_str());
  RCLCPP_INFO(logger, "End effector link: %s", move_group_interface.getEndEffectorLink().c_str());
  RCLCPP_INFO(
    logger,
    "This demo is intended for `ur5e_bringup_with_mock_components.launch.py launch_moveit:=true`.");

  if (!move_group_interface.getCurrentState(5.0)) {
    RCLCPP_ERROR(logger, "Failed to receive the current robot state from MoveIt.");
    executor.cancel();
    executor_thread.join();
    rclcpp::shutdown();
    return 1;
  }

  RCLCPP_INFO(logger, "1. Moving to a joint target...");
  std::vector<double> target_joints = {
      0.0,
      -M_PI / 2.0,
      M_PI / 2.0,
      -M_PI / 2.0,
      -M_PI / 2.0,
      0.0
  };
  if (!move_group_interface.setJointValueTarget(target_joints)) {
    RCLCPP_ERROR(logger, "Failed to set the joint target.");
  } else {
    move_group_interface.setStartStateToCurrentState();
    plan_and_execute(move_group_interface, logger, "joint_target");
  }

  std::this_thread::sleep_for(std::chrono::seconds(2));

  RCLCPP_INFO(logger, "2. Moving to a pose target...");

  geometry_msgs::msg::Pose target_pose;
  tf2::Quaternion q;
  q.setRPY(M_PI, 0.0, 0.0);
  q.normalize();
  target_pose.orientation.x = q.x();
  target_pose.orientation.y = q.y();
  target_pose.orientation.z = q.z();
  target_pose.orientation.w = q.w();
  target_pose.position.x = 0.35;
  target_pose.position.y = 0.10;
  target_pose.position.z = 0.35;

  move_group_interface.setStartStateToCurrentState();
  move_group_interface.setPoseTarget(target_pose);
  plan_and_execute(move_group_interface, logger, "pose_target");
  move_group_interface.clearPoseTargets();

  executor.cancel();
  executor_thread.join();
  rclcpp::shutdown();
  return 0;
}
