#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
import actionlib
from control_msgs.msg import FollowJointTrajectoryAction, FollowJointTrajectoryGoal
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
import sys
import moveit_commander
from geometry_msgs.msg import Pose, PoseStamped
from moveit_msgs.srv import GetPositionIK, GetPositionIKRequest

class JTCWithIKSolverDemo:
    def __init__(self):
        # MoveIt! Commanderの初期化
        moveit_commander.roscpp_initialize(sys.argv)
        
        rospy.init_node('jtc_with_ik_solver_demo', anonymous=True)
        
        # ActionClient作成 (関節角度制御用)
        self.client = actionlib.SimpleActionClient(
            '/scaled_pos_joint_traj_controller/follow_joint_trajectory',
            FollowJointTrajectoryAction
        )
        
        rospy.loginfo("Waiting for the FollowJointTrajectory action server...")
        self.client.wait_for_server()
        rospy.loginfo("Connected to the FollowJointTrajectory action server.")
        
        # MoveIt! のMoveGroupCommanderを準備
        group_name = "manipulator"
        self.move_group = moveit_commander.MoveGroupCommander(group_name)
        
        # IK計算サービスを待機
        self.ik_service_name = "/compute_ik"
        rospy.loginfo(f"Waiting for IK service: {self.ik_service_name}")
        rospy.wait_for_service(self.ik_service_name)
        self.compute_ik = rospy.ServiceProxy(self.ik_service_name, GetPositionIK)
        rospy.loginfo("Connected to IK service.")

        # === 修正箇所 ===
        # フレーム名と関節名をクラス変数として保存
        self.base_frame = self.move_group.get_planning_frame()
        self.tool_frame = self.move_group.get_end_effector_link()
        self.joint_names = self.move_group.get_active_joints()
        
        # 起動時に一度、ロボット情報を表示
        rospy.loginfo("--- Robot Information ---")
        rospy.loginfo(f"  - Base Frame: {self.base_frame}")
        rospy.loginfo(f"  - Tool Frame: {self.tool_frame}")
        rospy.loginfo(f"  - Active Joints: {self.joint_names}")
        rospy.loginfo("-------------------------")
        # === 修正箇所ここまで ===

    def solve_ik(self, target_pose):
        """指定された手先姿勢からIKを計算し、関節角度を返す"""
        request = GetPositionIKRequest()
        request.ik_request.group_name = self.move_group.get_name()
        request.ik_request.robot_state = self.move_group.get_current_state()
        request.ik_request.avoid_collisions = True
        
        pose_stamped = PoseStamped()
        pose_stamped.header.frame_id = self.base_frame # クラス変数を使用
        pose_stamped.pose = target_pose
        request.ik_request.pose_stamped = pose_stamped
        
        request.ik_request.timeout = rospy.Duration(1.0)

        try:
            response = self.compute_ik(request)
            if response.error_code.val == response.error_code.SUCCESS:
                joint_positions = response.solution.joint_state.position
                active_joint_positions = [
                    pos for name, pos in zip(response.solution.joint_state.name, joint_positions) 
                    if name in self.joint_names
                ]
                rospy.loginfo("IK solution found.")
                return active_joint_positions
            else:
                rospy.logerr(f"IK failed with error code: {response.error_code.val}")
                return None
        except rospy.ServiceException as e:
            rospy.logerr(f"IK service call failed: {e}")
            return None

    def create_trajectory(self, waypoints, durations):
        """軌道を作成"""
        trajectory = JointTrajectory()
        trajectory.joint_names = self.joint_names
        for i, waypoint in enumerate(waypoints):
            point = JointTrajectoryPoint()
            point.positions = waypoint
            point.time_from_start = rospy.Duration(durations[i])
            trajectory.points.append(point)
        return trajectory

    def execute_trajectory(self, trajectory):
        """軌道を実行"""
        goal = FollowJointTrajectoryGoal()
        goal.trajectory = trajectory
        rospy.loginfo("Sending trajectory goal to JTC...")
        self.client.send_goal(goal)
        rospy.loginfo("Waiting for result...")
        self.client.wait_for_result()
        result = self.client.get_result()
        if result and result.error_code == result.SUCCESSFUL:
            rospy.loginfo("Trajectory execution finished successfully.")
        else:
            rospy.logwarn(f"Trajectory execution failed with error code: {result.error_code if result else 'N/A'}")
        return result

    def move_relative(self, dx=0, dy=0, dz=0):
        """現在の姿勢から相対的に移動する"""
        rospy.loginfo(f"Attempting to move relatively by dx={dx}, dy={dy}, dz={dz}")
        current_pose = self.move_group.get_current_pose().pose

        target_pose = Pose()
        target_pose.position.x = current_pose.position.x + dx
        target_pose.position.y = current_pose.position.y + dy
        target_pose.position.z = current_pose.position.z + dz
        target_pose.orientation = current_pose.orientation

        joint_goal = self.solve_ik(target_pose)

        if joint_goal:
            current_joints = self.move_group.get_current_joint_values()
            waypoints = [current_joints, joint_goal]
            durations = [0.0, 2.0]  # 2秒かけて移動
            trajectory = self.create_trajectory(waypoints, durations)
            self.execute_trajectory(trajectory)
            return True
        else:
            rospy.logerr("Failed to execute relative move because IK solution was not found.")
            return False

    def interactive_demo(self):
        """ユーザーのキーボード入力に応じて相対移動を行うインタラクティブなデモ"""
        rospy.loginfo("--- Starting Interactive Relative Movement Demo ---")
        
        rospy.loginfo("Moving to a known starting pose...")
        start_joints = [0.0, -1.57, 1.57, -1.57, -1.57, 0.0]
        self.move_group.go(start_joints, wait=True)
        self.move_group.stop()
        rospy.sleep(1)

        move_step = 0.05  # 5cm

        while not rospy.is_shutdown():
            # === 修正箇所 ===
            # 操作メニューを表示
            print("\n" + "="*45)
            # フレーム情報を毎回答表示
            print(f"  Frames: [Base: {self.base_frame}] -> [Tool: {self.tool_frame}]")
            print("  " + "-"*43)
            print("  操作メニュー (基準座標系)")
            print("  1: 上 (+Z)      2: 下 (-Z)")
            print("  3: 右 (-Y)      4: 左 (+Y)")
            print("  5: 奥 (+X)      6: 手前 (-X)")
            print("  q: 終了")
            print("="*45)
            # === 修正箇所ここまで ===
            
            command = input("コマンドを入力してください > ")

            if command == '1':
                self.move_relative(dz=move_step)
            elif command == '2':
                self.move_relative(dz=-move_step)
            elif command == '3':
                self.move_relative(dy=-move_step)
            elif command == '4':
                self.move_relative(dy=move_step)
            elif command == '5':
                self.move_relative(dx=move_step)
            elif command == '6':
                self.move_relative(dx=-move_step)
            elif command.lower() == 'q':
                rospy.loginfo("終了します。")
                break
            else:
                print("無効なコマンドです。1~6またはqを入力してください。")

        rospy.loginfo("--- Interactive Demo Finished ---")


if __name__ == '__main__':
    try:
        demo = JTCWithIKSolverDemo()
        demo.interactive_demo()
    except rospy.ROSInterruptException:
        rospy.loginfo("ROS node interrupted.")
    except Exception as e:
        rospy.logerr(f"An error occurred: {e}")
    finally:
        moveit_commander.roscpp_shutdown()
        rospy.loginfo("MoveIt Commander has been shut down.")