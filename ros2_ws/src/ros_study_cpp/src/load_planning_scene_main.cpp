#include <memory>

#include <rclcpp/rclcpp.hpp>

#include "ros_study_cpp/load_planning_scene.hpp"

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);

  rclcpp::NodeOptions options;
  options.automatically_declare_parameters_from_overrides(true);

  auto node = std::make_shared<grinding_scene_description::PlanningSceneLoader>(options);
  rclcpp::spin(node);

  if (rclcpp::ok()) {
    rclcpp::shutdown();
  }

  return 0;
}
