#include <chrono>
#include <vector>

#include <geometry_msgs/msg/pose.hpp>
#include <moveit/planning_scene_interface/planning_scene_interface.h>
#include <moveit_msgs/msg/collision_object.hpp>
#include <rclcpp/rclcpp.hpp>
#include <shape_msgs/msg/solid_primitive.hpp>

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  auto node = rclcpp::Node::make_shared("planning_scene_example_node");

  RCLCPP_WARN(
    node->get_logger(),
    "This example only becomes meaningful after MoveIt is running. "
    "Launch Gazebo first, then the MoveIt overlay.");

  // Give the ROS graph a moment to discover the MoveIt side before applying.
  rclcpp::sleep_for(std::chrono::milliseconds(500));

  moveit::planning_interface::PlanningSceneInterface planning_scene_interface;

  moveit_msgs::msg::CollisionObject box_obstacle;
  box_obstacle.header.frame_id = "world";
  box_obstacle.id = "box_obstacle";

  shape_msgs::msg::SolidPrimitive box_primitive;
  box_primitive.type = shape_msgs::msg::SolidPrimitive::BOX;
  box_primitive.dimensions = {0.3, 0.6, 0.4};

  geometry_msgs::msg::Pose box_pose;
  box_pose.orientation.w = 1.0;
  box_pose.position.x = 0.7;
  box_pose.position.y = 0.0;
  box_pose.position.z = 0.2;

  box_obstacle.primitives.push_back(box_primitive);
  box_obstacle.primitive_poses.push_back(box_pose);
  box_obstacle.operation = moveit_msgs::msg::CollisionObject::ADD;

  const bool success = planning_scene_interface.applyCollisionObjects({box_obstacle});

  if (success) {
    RCLCPP_INFO(
      node->get_logger(),
      "Added collision object `box_obstacle` to the Planning Scene in the `world` frame.");
  } else {
    RCLCPP_ERROR(
      node->get_logger(),
      "Failed to apply the collision object. Check whether MoveIt is running and exposing "
      "the planning scene services.");
  }

  rclcpp::shutdown();
  return success ? 0 : 1;
}
