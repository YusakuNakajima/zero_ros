#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MoveIt Commander Demo for ROS Arm Position Control
Basic implementation example using MoveIt
"""

import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from math import pi
import sys

class MoveItDemo:
    def __init__(self):
        # MoveItCommanderの初期化
        moveit_commander.roscpp_initialize(sys.argv)
        rospy.init_node('moveit_demo', anonymous=True)
        
        # ロボットとシーンのインターフェース
        self.robot = moveit_commander.RobotCommander()
        self.scene = moveit_commander.PlanningSceneInterface()
        
        # アームグループの設定（ur5eの場合）
        group_name = "manipulator"
        self.move_group = moveit_commander.MoveGroupCommander(group_name)
        
        print("============ Robot Groups:")
        print(self.robot.get_group_names())
        print("============ Current Pose:")
        print(self.move_group.get_current_pose().pose)

    def go_to_joint_state(self, joint_goal):
        """関節角度を指定して移動"""
        self.move_group.go(joint_goal, wait=True)
        self.move_group.stop()
        
    def go_to_pose_goal(self, pose_goal):
        """姿勢を指定して移動"""
        self.move_group.set_pose_target(pose_goal)
        plan = self.move_group.go(wait=True)
        self.move_group.stop()
        self.move_group.clear_pose_targets()
        return plan

    def plan_cartesian_path(self, waypoints):
        """カルテシアン軌道でのプランニング"""
        (plan, fraction) = self.move_group.compute_cartesian_path(
            waypoints, 0.01, 0.0)
        return plan, fraction

    def demo_sequence(self):
        """デモシーケンス"""
        print("============ Demo Start")
        
        # 1. ホームポジションに移動
        joint_goal = [0, -pi/4, 0, -pi/2, 0, pi/3]
        self.go_to_joint_state(joint_goal)
        
        # 2. 姿勢指定での移動
        pose_goal = geometry_msgs.msg.Pose()
        pose_goal.orientation.w = 1.0
        pose_goal.position.x = 0.4
        pose_goal.position.y = 0.1
        pose_goal.position.z = 0.4
        self.go_to_pose_goal(pose_goal)
        
        print("============ Demo Complete!")

def main():
    try:
        demo = MoveItDemo()
        demo.demo_sequence()
    except rospy.ROSInterruptException:
        return

if __name__ == '__main__':
    main()