// load_planning_scene.hpp
#ifndef ROS_STUDY_CPP__LOAD_PLANNING_SCENE_HPP_
#define ROS_STUDY_CPP__LOAD_PLANNING_SCENE_HPP_

#include <string>
#include <vector>

#include <rclcpp/rclcpp.hpp>
#include <geometry_msgs/msg/pose.hpp>
#include <shape_msgs/msg/solid_primitive.hpp>
#include <moveit_msgs/msg/planning_scene.hpp>
#include <moveit_msgs/msg/attached_collision_object.hpp>
#include <moveit_msgs/srv/apply_planning_scene.hpp>


namespace grinding_scene_description
{
class PlanningSceneLoader : public rclcpp::Node
{
public:
  explicit PlanningSceneLoader(const rclcpp::NodeOptions & options);
  virtual ~PlanningSceneLoader();
  void load_scene();

private:
  rclcpp::Node::SharedPtr node_;
  rclcpp::Publisher<moveit_msgs::msg::PlanningScene>::SharedPtr planning_scene_diff_publisher_;
  rclcpp::TimerBase::SharedPtr timer_;
  rclcpp::TimerBase::SharedPtr shutdown_timer_;
  static const rclcpp::Logger LOGGER;
  void clear_all_objects();
  void _add_table(const std::vector<double>& table_scale, const std::vector<double>& table_pos);
  void _add_mortar(const std::string& file_path, const std::vector<double>& mortar_pos);
  void _add_mortar_box(const std::vector<double>& mortar_pos, const std::vector<double>& mortar_scale);

};

} // namespace grinding_scene_description

#endif  // ROS_STUDY_CPP__LOAD_PLANNING_SCENE_HPP_
