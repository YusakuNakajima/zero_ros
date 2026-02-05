#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from rclpy.duration import Duration

from control_msgs.action import FollowJointTrajectory
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint


class JTCDemo(Node):
    def __init__(self):
        super().__init__('jtc_demo')

        self.client = ActionClient(
            self,
            FollowJointTrajectory,
            '/scaled_pos_joint_traj_controller/follow_joint_trajectory',
        )

        self.joint_names = [
            'shoulder_pan_joint', 'shoulder_lift_joint',
            'elbow_joint', 'wrist_1_joint',
            'wrist_2_joint', 'wrist_3_joint'
        ]

    def wait_for_server(self):
        self.get_logger().info('Waiting for the FollowJointTrajectory action server...')
        self.client.wait_for_server()
        self.get_logger().info('Connected to the FollowJointTrajectory action server.')

    def create_trajectory(self, waypoints, durations):
        trajectory = JointTrajectory()
        trajectory.joint_names = self.joint_names

        for waypoint, duration in zip(waypoints, durations):
            point = JointTrajectoryPoint()
            point.positions = waypoint
            point.time_from_start = Duration(seconds=duration).to_msg()
            trajectory.points.append(point)

        return trajectory

    def execute_trajectory(self, trajectory):
        goal = FollowJointTrajectory.Goal()
        goal.trajectory = trajectory

        self.get_logger().info('Sending trajectory goal...')
        goal_future = self.client.send_goal_async(goal)
        rclpy.spin_until_future_complete(self, goal_future)
        goal_handle = goal_future.result()

        if not goal_handle.accepted:
            self.get_logger().error('Trajectory goal was rejected.')
            return None

        self.get_logger().info('Waiting for result...')
        result_future = goal_handle.get_result_async()
        rclpy.spin_until_future_complete(self, result_future)
        result = result_future.result().result

        if result:
            self.get_logger().info(f'Trajectory execution finished with status: {result.error_code}')
        else:
            self.get_logger().warn('Trajectory execution failed or no result received.')
        return result

    def demo_sequence(self):
        waypoints = [
            [0.0, -1.57, 0.0, -1.57, 0.0, 0.0],
            [0.5, -1.0, 1.0, -1.5, -0.5, 0.0]
        ]
        durations = [0.0, 3.0]

        trajectory = self.create_trajectory(waypoints, durations)
        self.execute_trajectory(trajectory)


def main():
    rclpy.init()
    node = JTCDemo()
    try:
        node.wait_for_server()
        node.demo_sequence()
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
