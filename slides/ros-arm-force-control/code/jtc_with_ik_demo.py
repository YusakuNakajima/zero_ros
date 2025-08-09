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
import time

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

        # パラメータのデフォルト値を設定
        self.attempts = 1
        self.move_step = 0.05  # m単位
        self.duration = 2.0    # 秒単位
        
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

    def solve_ik(self, target_pose):
        rospy.loginfo(f"Solving IK for the target pose with up to {self.attempts} attempts...")
        
        for i in range(self.attempts):
            rospy.loginfo(f"  -> IK attempt #{i + 1}/{self.attempts}")
            
            request = GetPositionIKRequest()
            request.ik_request.group_name = self.move_group.get_name()
            request.ik_request.robot_state = self.move_group.get_current_state()
            request.ik_request.avoid_collisions = True
            
            pose_stamped = PoseStamped()
            pose_stamped.header.frame_id = self.base_frame
            pose_stamped.pose = target_pose
            request.ik_request.pose_stamped = pose_stamped
            
            request.ik_request.timeout = rospy.Duration(0.5)
            
            try:
                start_time = time.time()
                response = self.compute_ik(request)
                end_time = time.time()
                elapsed_ms = (end_time - start_time) * 1000
                rospy.loginfo(f"     IK computation took: {elapsed_ms:.2f} ms")
                
                if response.error_code.val == response.error_code.SUCCESS:
                    rospy.loginfo(f"     -> IK solution found.")
                    joint_positions = response.solution.joint_state.position
                    active_joint_positions = [
                        pos for name, pos in zip(response.solution.joint_state.name, joint_positions) 
                        if name in self.joint_names
                    ]
                    return active_joint_positions
            
            except rospy.ServiceException as e:
                rospy.logerr(f"IK service call failed on attempt #{i + 1}: {e}")
                return None

        rospy.logerr(f"IK failed to find a solution after {self.attempts} attempts.")
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
            durations = [0.0, self.duration]
            trajectory = self.create_trajectory(waypoints, durations)
            self.execute_trajectory(trajectory)
            return True
        else:
            rospy.logerr("Failed to execute relative move because IK solution was not found.")
            return False

    def interactive_demo(self):
        rospy.loginfo("--- Starting Interactive Relative Movement Demo ---")
        
        rospy.loginfo("Moving to a known starting pose...")
        start_joints = [0.0, -1.57, 1.57, -1.57, -1.57, 0.0]
        self.move_group.go(start_joints, wait=True)
        self.move_group.stop()
        rospy.sleep(1)
        
        while not rospy.is_shutdown():
            print("\n" + "="*60)
            print(f"  Frames: [Base: {self.base_frame}] -> [Tool: {self.tool_frame}]")
            print(f"  Current Settings: [Step: {self.move_step*100:.1f} cm] [Time: {self.duration:.1f} s] [IK Attempts: {self.attempts}]")
            print("  " + "-"*58)
            print("  操作メニュー (基準座標系)")
            print("  1: 上 (+Z)      2: 下 (-Z)")
            print("  3: 右 (-Y)      4: 左 (+Y)")
            print("  5: 奥 (+X)      6: 手前 (-X)")
            print("  s: 移動量 (step) を変更")
            print("  t: 移動時間 (time) を変更")
            print("  a: IK試行回数 (attempts) を変更")
            print("  q: 終了")
            print("="*60)
            
            command = input("コマンドを入力してください > ")
            
            if command == '1':
                self.move_relative(dz=self.move_step)
            elif command == '2':
                self.move_relative(dz=-self.move_step)
            elif command == '3':
                self.move_relative(dy=-self.move_step)
            elif command == '4':
                self.move_relative(dy=self.move_step)
            elif command == '5':
                self.move_relative(dx=self.move_step)
            elif command == '6':
                self.move_relative(dx=-self.move_step)
            elif command.lower() == 's':
                try:
                    new_step_cm = float(input(f"新しい移動量(cm)を入力してください (現在値: {self.move_step*100:.1f} cm) > "))
                    if new_step_cm > 0:
                        self.move_step = new_step_cm / 100.0
                        rospy.loginfo(f"移動量が {self.move_step*100:.1f} cm に変更されました。")
                    else:
                        print("無効な入力です。0より大きい数値を入力してください。")
                except ValueError:
                    print("無効な入力です。数値を入力してください。")
            elif command.lower() == 't':
                try:
                    new_duration = float(input(f"新しい移動時間(秒)を入力してください (現在値: {self.duration:.1f} s) > "))
                    if new_duration > 0:
                        self.duration = new_duration
                        rospy.loginfo(f"移動時間が {self.duration:.1f} 秒に変更されました。")
                    else:
                        print("無効な入力です。0より大きい数値を入力してください。")
                except ValueError:
                    print("無効な入力です。数値を入力してください。")
            elif command.lower() == 'a':
                try:
                    new_attempts = int(input(f"新しいIK試行回数を入力してください (現在値: {self.attempts}) > "))
                    if new_attempts > 0:
                        self.attempts = new_attempts
                        rospy.loginfo(f"IK試行回数が {self.attempts} に変更されました。")
                    else:
                        print("無効な入力です。1以上の整数を入力してください。")
                except ValueError:
                    print("無効な入力です。整数を入力してください。")
            elif command.lower() == 'q':
                rospy.loginfo("終了します。")
                break
            else:
                print("無効なコマンドです。1~6, s, t, a, q のいずれかを入力してください。")
                
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