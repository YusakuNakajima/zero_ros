#include <rclcpp/rclcpp.hpp>
#include <moveit/move_group_interface/move_group_interface.h>
#include <geometry_msgs/msg/pose.hpp>
#include <tf2/LinearMath/Quaternion.h>
#include <chrono>
#include <cmath>
#include <thread>

// 定数: 制御するグループ名 (SRDFに合わせる: "ur_manipulator" や "manipulator" が一般的)
static const std::string PLANNING_GROUP = "ur_manipulator";

int main(int argc, char** argv)
{
  rclcpp::init(argc, argv);
  
  // Nodeの作成
  // MoveIt2は内部でAction通信を行うため、ノードオプションで自動スピン等の設定が必要な場合がありますが、
  // ここではシンプルにMultiThreadedExecutorで回します。
  rclcpp::NodeOptions node_options;
  node_options.automatically_declare_parameters_from_overrides(true);
  auto node = rclcpp::Node::make_shared("ur_moveit_demo_cpp", node_options);
  
  // ログ出力用のヘルパー
  auto logger = node->get_logger();

  // MoveGroupInterfaceの作成
  // これがメインの制御クラスです
  using moveit::planning_interface::MoveGroupInterface;
  auto move_group_interface = MoveGroupInterface(node, PLANNING_GROUP);

  // 安全のため速度・加速度を制限 (0.0 ~ 1.0)
  move_group_interface.setMaxVelocityScalingFactor(0.1);
  move_group_interface.setMaxAccelerationScalingFactor(0.1);

  RCLCPP_INFO(logger, "Planning frame: %s", move_group_interface.getPlanningFrame().c_str());
  RCLCPP_INFO(logger, "End effector link: %s", move_group_interface.getEndEffectorLink().c_str());

  // Executorを別スレッドで回す
  // (MoveItの非同期処理やAction Clientの応答を受け取るために必要)
  rclcpp::executors::MultiThreadedExecutor executor;
  executor.add_node(node);
  std::thread([&executor]() { executor.spin(); }).detach();

  // ---------------------------------------------------------
  // 1. ジョイント（関節）角度指定での移動
  // ---------------------------------------------------------
  RCLCPP_INFO(logger, "1. Moving to Joint Target...");

  // 現在の関節角度を取得（参照用）
  std::vector<double> joint_group_positions = move_group_interface.getCurrentJointValues();

  // 目標角度の設定 (ラジアン)
  // URは6軸: Base, Shoulder, Elbow, Wrist1, Wrist2, Wrist3
  // 例: 直立姿勢に近い場所へ
  std::vector<double> target_joints = {
      0.0,          // Base
      -M_PI / 2.0,  // Shoulder (-90 deg)
      M_PI / 2.0,   // Elbow
      -M_PI / 2.0,  // Wrist 1
      -M_PI / 2.0,  // Wrist 2
      0.0           // Wrist 3
  };

  // 目標セット & 移動実行
  bool success_joint = move_group_interface.setJointValueTarget(target_joints);
  if (success_joint) {
      // plan & execute
      moveit::planning_interface::MoveGroupInterface::Plan my_plan;
      bool success = (move_group_interface.plan(my_plan) == moveit::core::MoveItErrorCode::SUCCESS);
      
      if(success) {
          move_group_interface.execute(my_plan);
          RCLCPP_INFO(logger, "Joint Move Executed!");
      } else {
          RCLCPP_ERROR(logger, "Joint Planning Failed!");
      }
  }

  // 少し待機
  std::this_thread::sleep_for(std::chrono::seconds(2));

  // ---------------------------------------------------------
  // 2. 手先座標 (Pose) 指定での移動
  // ---------------------------------------------------------
  RCLCPP_INFO(logger, "2. Moving to Pose Target...");

  geometry_msgs::msg::Pose target_pose;
  
  // 向きの設定 (四元数)
  // TF2を使ってEuler角から変換 (Roll=180度で下向きにする例)
  tf2::Quaternion q;
  q.setRPY(M_PI, 0, 0); 
  target_pose.orientation.x = q.x();
  target_pose.orientation.y = q.y();
  target_pose.orientation.z = q.z();
  target_pose.orientation.w = q.w();

  // 位置の設定 (メートル) - base_link基準
  target_pose.position.x = 0.4;
  target_pose.position.y = 0.1;
  target_pose.position.z = 0.4;

  move_group_interface.setPoseTarget(target_pose);

  // 計画と実行
  moveit::planning_interface::MoveGroupInterface::Plan my_plan_pose;
  bool success_pose = (move_group_interface.plan(my_plan_pose) == moveit::core::MoveItErrorCode::SUCCESS);

  if (success_pose) {
      RCLCPP_INFO(logger, "Visualizing plan 2 (pose goal)...");
      move_group_interface.execute(my_plan_pose);
      RCLCPP_INFO(logger, "Pose Move Executed!");
  } else {
      RCLCPP_ERROR(logger, "Pose Planning Failed!");
  }

  // 終了
  rclcpp::shutdown();
  return 0;
}
