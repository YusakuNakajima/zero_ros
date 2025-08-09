#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import rospy
import actionlib
from control_msgs.msg import FollowJointTrajectoryAction, FollowJointTrajectoryGoal
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

class JTCDemo:
    def __init__(self):
        rospy.init_node('jtc_demo', anonymous=True)
        
        # ActionClient作成
        self.client = actionlib.SimpleActionClient(
            '/scaled_pos_joint_traj_controller/follow_joint_trajectory',
            FollowJointTrajectoryAction
        )
        
        # サーバーが起動するまで待機
        rospy.loginfo("Waiting for the FollowJointTrajectory action server to come up...")
        self.client.wait_for_server()
        rospy.loginfo("Connected to the FollowJointTrajectory action server.")
        
        self.joint_names = [
            'shoulder_pan_joint', 'shoulder_lift_joint', 
            'elbow_joint', 'wrist_1_joint', 
            'wrist_2_joint', 'wrist_3_joint'
        ]

    def create_trajectory(self, waypoints, durations):
        """軌道を作成"""
        trajectory = JointTrajectory()
        trajectory.joint_names = self.joint_names
        
        for waypoint, duration in zip(waypoints, durations):
            point = JointTrajectoryPoint()
            point.positions = waypoint
            point.time_from_start = rospy.Duration(duration)
            trajectory.points.append(point)
        
        return trajectory

    def execute_trajectory(self, trajectory):
        """軌道を実行"""
        goal = FollowJointTrajectoryGoal()
        goal.trajectory = trajectory
        
        rospy.loginfo("Sending trajectory goal...")
        self.client.send_goal(goal)
        
        rospy.loginfo("Waiting for result...")
        self.client.wait_for_result()
        
        result = self.client.get_result()
        if result:
            rospy.loginfo(f"Trajectory execution finished with status: {result.error_code}")
        else:
            rospy.logwarn("Trajectory execution failed or no result received.")
        return result

    def demo_sequence(self):
        """デモシーケンス"""
        waypoints = [
            [0.0, -1.57, 0.0, -1.57, 0.0, 0.0],      # ホーム (ラジアン)
            [0.5, -1.0, 1.0, -1.5, -0.5, 0.0] # 目標 (ラジアン)
        ]
        # 各ウェイポイントに到達するまでの総時間
        # 最初のウェイポイントは通常0.0秒で設定し、次のウェイポイントまでの時間を累計で指定
        durations = [0.0, 3.0] 
        
        trajectory = self.create_trajectory(waypoints, durations)
        self.execute_trajectory(trajectory)

if __name__ == '__main__':
    try:
        demo = JTCDemo()
        demo.demo_sequence()
    except rospy.ROSInterruptException:
        rospy.loginfo("ROS node interrupted.")