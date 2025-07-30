#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
JointTrajectoryController Demo for ROS Arm Position Control
Based on JTC_executor.py from powder_grinding project
"""

import rospy
import actionlib
from control_msgs.msg import FollowJointTrajectoryAction, FollowJointTrajectoryGoal
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from sensor_msgs.msg import JointState
import numpy as np
from math import pi

class JTCDemo:
    def __init__(self):
        rospy.init_node('jtc_demo', anonymous=True)
        
        # JointTrajectoryControllerのActionクライアント
        self.client = actionlib.SimpleActionClient(
            '/arm_controller/follow_joint_trajectory',
            FollowJointTrajectoryAction
        )
        
        # 関節名の設定（ur5eの場合）
        self.joint_names = [
            'shoulder_pan_joint',
            'shoulder_lift_joint', 
            'elbow_joint',
            'wrist_1_joint',
            'wrist_2_joint',
            'wrist_3_joint'
        ]
        
        # 現在の関節状態を保存
        self.current_joint_state = None
        
        # JointStateサブスクライバー
        self.joint_state_sub = rospy.Subscriber(
            '/joint_states',
            JointState,
            self.joint_state_callback
        )
        
        print("Waiting for action server...")
        self.client.wait_for_server()
        print("Action server connected!")

    def joint_state_callback(self, msg):
        """現在の関節状態を更新"""
        self.current_joint_state = msg

    def get_current_joint_positions(self):
        """現在の関節角度を取得"""
        if self.current_joint_state is None:
            rospy.logwarn("No joint state received yet")
            return [0.0] * len(self.joint_names)
        
        positions = []
        for joint_name in self.joint_names:
            try:
                idx = self.current_joint_state.name.index(joint_name)
                positions.append(self.current_joint_state.position[idx])
            except ValueError:
                rospy.logwarn(f"Joint {joint_name} not found in joint state")
                positions.append(0.0)
        
        return positions

    def create_trajectory(self, waypoints, durations):
        """軌道を作成"""
        trajectory = JointTrajectory()
        trajectory.joint_names = self.joint_names
        
        for i, (waypoint, duration) in enumerate(zip(waypoints, durations)):
            point = JointTrajectoryPoint()
            point.positions = waypoint
            point.time_from_start = rospy.Duration(duration)
            
            # 速度と加速度も設定（簡単な計算）
            if i == 0:
                point.velocities = [0.0] * len(self.joint_names)
                point.accelerations = [0.0] * len(self.joint_names)
            else:
                # 前の点との差分から速度を計算
                dt = duration - durations[i-1]
                velocities = []
                for j in range(len(self.joint_names)):
                    vel = (waypoint[j] - waypoints[i-1][j]) / dt
                    velocities.append(vel)
                point.velocities = velocities
                point.accelerations = [0.0] * len(self.joint_names)
            
            trajectory.points.append(point)
        
        return trajectory

    def execute_trajectory(self, trajectory):
        """軌道を実行"""
        goal = FollowJointTrajectoryGoal()
        goal.trajectory = trajectory
        goal.goal_time_tolerance = rospy.Duration(0.1)
        
        self.client.send_goal(goal)
        self.client.wait_for_result()
        
        result = self.client.get_result()
        return result

    def move_to_joint_positions(self, target_positions, duration=5.0):
        """指定した関節角度に移動"""
        current_positions = self.get_current_joint_positions()
        
        waypoints = [current_positions, target_positions]
        durations = [0.0, duration]
        
        trajectory = self.create_trajectory(waypoints, durations)
        result = self.execute_trajectory(trajectory)
        
        return result

    def demo_sequence(self):
        """デモシーケンス"""
        print("============ Starting JTC Demo Sequence")
        
        # 待機
        rospy.sleep(2.0)
        
        # 1. ホームポジションに移動
        print("Moving to home position...")
        home_position = [0, -pi/4, 0, -pi/2, 0, pi/3]
        self.move_to_joint_positions(home_position, 3.0)
        
        rospy.sleep(1.0)
        
        # 2. 別の姿勢に移動
        print("Moving to target position...")
        target_position = [pi/4, -pi/3, pi/6, -pi/2, -pi/4, pi/2]
        self.move_to_joint_positions(target_position, 4.0)
        
        rospy.sleep(1.0)
        
        # 3. 複数waypoints軌道
        print("Executing multi-waypoint trajectory...")
        current_pos = self.get_current_joint_positions()
        
        waypoints = [
            current_pos,
            [pi/6, -pi/4, pi/8, -pi/3, -pi/6, pi/4],
            [-pi/6, -pi/4, -pi/8, -pi/3, pi/6, -pi/4],
            home_position
        ]
        durations = [0.0, 2.0, 4.0, 6.0]
        
        trajectory = self.create_trajectory(waypoints, durations)
        self.execute_trajectory(trajectory)
        
        print("============ JTC Demo Complete!")

    def simple_example(self):
        """シンプルな例"""
        print("Simple JTC example:")
        print("1. Get current joint positions")
        current = self.get_current_joint_positions()
        print(f"Current: {[round(x, 3) for x in current]}")
        
        print("2. Create trajectory to new position")
        target = [0.5, -1.0, 1.0, -1.5, -0.5, 0.0]
        self.move_to_joint_positions(target, 3.0)
        
        print("3. Move back to home")
        home = [0, -pi/2, 0, -pi/2, 0, 0]
        self.move_to_joint_positions(home, 3.0)

def main():
    try:
        demo = JTCDemo()
        
        # シンプルな例を実行
        demo.simple_example()
        
        # フルデモを実行する場合
        # demo.demo_sequence()
        
    except rospy.ROSInterruptException:
        return
    except KeyboardInterrupt:
        return

if __name__ == '__main__':
    main()