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


class JTCVelocityAccelDemo(Node):
    def __init__(self):
        super().__init__('jtc_velocity_accel_demo')

        self.declare_parameter('controller_name', 'scaled_joint_trajectory_controller')
        self.declare_parameter('segment_duration', 3.0)
        self.declare_parameter('samples_per_segment', 30)

        controller_name = self.get_parameter('controller_name').get_parameter_value().string_value
        self.segment_duration = self.get_parameter('segment_duration').get_parameter_value().double_value
        self.samples_per_segment = self.get_parameter('samples_per_segment').get_parameter_value().integer_value

        self.client = ActionClient(
            self,
            FollowJointTrajectory,
            f'/{controller_name}/follow_joint_trajectory',
        )

        self.joint_names = [
            'shoulder_pan_joint',
            'shoulder_lift_joint',
            'elbow_joint',
            'wrist_1_joint',
            'wrist_2_joint',
            'wrist_3_joint',
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

    def create_point(self, positions, velocities, accelerations, time_from_start):
        point = JointTrajectoryPoint()
        point.positions = positions
        point.velocities = velocities
        point.accelerations = accelerations
        point.time_from_start = Duration(seconds=time_from_start).to_msg()
        return point

    def append_quintic_segment(
        self,
        trajectory,
        start_positions,
        goal_positions,
        segment_start_time,
        duration,
        samples,
        include_start_point,
    ):
        start_index = 0 if include_start_point else 1
        for index in range(start_index, samples + 1):
            tau = index / samples
            s = 10.0 * tau**3 - 15.0 * tau**4 + 6.0 * tau**5
            s_dot = (30.0 * tau**2 - 60.0 * tau**3 + 30.0 * tau**4) / duration
            s_ddot = (60.0 * tau - 180.0 * tau**2 + 120.0 * tau**3) / (duration**2)

            positions = []
            velocities = []
            accelerations = []
            for start, goal in zip(start_positions, goal_positions):
                delta = goal - start
                positions.append(start + delta * s)
                velocities.append(delta * s_dot)
                accelerations.append(delta * s_ddot)

            point_time = segment_start_time + tau * duration
            trajectory.points.append(
                self.create_point(positions, velocities, accelerations, point_time)
            )

    def create_demo_trajectory(self):
        current = self.current_joint_positions()
        middle = [0.35, -1.20, 1.00, -1.45, -0.35, 0.10]
        goal = [0.60, -0.95, 1.15, -1.60, -0.55, 0.20]

        trajectory = JointTrajectory()
        trajectory.joint_names = self.joint_names

        self.append_quintic_segment(
            trajectory=trajectory,
            start_positions=current,
            goal_positions=middle,
            segment_start_time=0.0,
            duration=self.segment_duration,
            samples=self.samples_per_segment,
            include_start_point=True,
        )
        self.append_quintic_segment(
            trajectory=trajectory,
            start_positions=middle,
            goal_positions=goal,
            segment_start_time=self.segment_duration,
            duration=self.segment_duration,
            samples=self.samples_per_segment,
            include_start_point=False,
        )
        self.append_quintic_segment(
            trajectory=trajectory,
            start_positions=goal,
            goal_positions=current,
            segment_start_time=2.0 * self.segment_duration,
            duration=self.segment_duration,
            samples=self.samples_per_segment,
            include_start_point=False,
        )
        return trajectory

    def execute_trajectory(self, trajectory):
        goal = FollowJointTrajectory.Goal()
        goal.trajectory = trajectory

        self.get_logger().info(
            'Sending a trajectory with explicit positions, velocities, and accelerations.'
        )
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
        trajectory = self.create_demo_trajectory()
        total_time = trajectory.points[-1].time_from_start.sec
        self.get_logger().info(
            f'Generated {len(trajectory.points)} points over about {total_time} seconds.'
        )
        self.get_logger().info(
            'This example uses a quintic profile, so waypoint boundaries start and end with zero velocity and acceleration.'
        )
        self.execute_trajectory(trajectory)


def main():
    rclpy.init()
    node = JTCVelocityAccelDemo()
    try:
        node.wait_for_server()
        node.demo_sequence()
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
