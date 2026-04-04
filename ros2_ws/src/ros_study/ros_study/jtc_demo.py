#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time

import rclpy
from rclpy.action import ActionClient
from rclpy.duration import Duration
from rclpy.node import Node

from control_msgs.action import FollowJointTrajectory
from sensor_msgs.msg import JointState
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint


class JTCDemo(Node):
    def __init__(self):
        super().__init__('jtc_demo')

        self.declare_parameter('controller_name', 'scaled_joint_trajectory_controller')
        controller_name = self.get_parameter('controller_name').get_parameter_value().string_value

        self.client = ActionClient(
            self,
            FollowJointTrajectory,
            f'/{controller_name}/follow_joint_trajectory',
        )

        self.joint_names = [
            'shoulder_pan_joint', 'shoulder_lift_joint',
            'elbow_joint', 'wrist_1_joint',
            'wrist_2_joint', 'wrist_3_joint'
        ]
        self.latest_joint_state = None
        self.create_subscription(JointState, '/joint_states', self._joint_state_cb, 10)

    def _joint_state_cb(self, msg):
        self.latest_joint_state = msg

    def wait_for_server(self):
        self.get_logger().info('Waiting for the FollowJointTrajectory action server...')
        self.client.wait_for_server()
        self.get_logger().info('Connected to the FollowJointTrajectory action server.')

        self.get_logger().info('Waiting for /joint_states...')
        start = time.time()
        while rclpy.ok() and self.latest_joint_state is None:
            rclpy.spin_once(self, timeout_sec=0.1)
            if time.time() - start > 5.0:
                self.get_logger().warn('Still waiting for /joint_states...')
                start = time.time()
        self.get_logger().info('Received /joint_states.')

    def current_joint_positions(self):
        if self.latest_joint_state is None:
            raise RuntimeError('No joint state has been received yet.')

        joint_map = dict(zip(self.latest_joint_state.name, self.latest_joint_state.position))
        return [joint_map[name] for name in self.joint_names]

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
        current = self.current_joint_positions()
        waypoints = [
            current,
            [0.55, -1.35, 1.20, -1.70, -0.10, 0.25],
            [-0.40, -0.95, 0.85, -1.30, -0.65, -0.20],
            current,
        ]
        durations = [0.0, 2.5, 5.0, 7.5]

        self.get_logger().info('Sending a comparison-friendly position-only trajectory.')
        self.get_logger().info('JointTrajectoryController will interpolate between sharp waypoint direction changes.')
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
