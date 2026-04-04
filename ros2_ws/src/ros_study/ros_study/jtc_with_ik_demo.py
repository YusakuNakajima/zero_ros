#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from rclpy.duration import Duration
from rclpy.time import Time

from control_msgs.action import FollowJointTrajectory
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from geometry_msgs.msg import Pose, PoseStamped
from sensor_msgs.msg import JointState
from moveit_msgs.msg import RobotState
from moveit_msgs.srv import GetPositionIK
from tf2_ros import Buffer, TransformException, TransformListener


class JTCWithIKSolverDemo(Node):
    def __init__(self):
        super().__init__('jtc_with_ik_solver_demo')

        # 設定値（実環境に合わせて変更）
        self.group_name = 'ur_manipulator'
        self.base_frame = 'base_link'
        self.tool_frame = 'tool0'
        self.joint_names = [
            'shoulder_pan_joint', 'shoulder_lift_joint',
            'elbow_joint', 'wrist_1_joint',
            'wrist_2_joint', 'wrist_3_joint'
        ]

        self.client = ActionClient(
            self,
            FollowJointTrajectory,
            '/scaled_joint_trajectory_controller/follow_joint_trajectory',
        )

        self.ik_client = self.create_client(GetPositionIK, '/compute_ik')
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self, spin_thread=False)
        self.joint_state = None
        self.create_subscription(JointState, '/joint_states', self._joint_state_cb, 10)

        self.attempts = 1
        self.duration = 2.0

    def _joint_state_cb(self, msg):
        self.joint_state = msg

    def wait_for_server(self):
        self.get_logger().info('Waiting for the FollowJointTrajectory action server...')
        self.client.wait_for_server()
        self.get_logger().info('Connected to the FollowJointTrajectory action server.')

        self.get_logger().info('Waiting for IK service: /compute_ik')
        self.ik_client.wait_for_service()
        self.get_logger().info('Connected to IK service.')

        self.get_logger().info('Waiting for /joint_states...')
        start = time.time()
        while rclpy.ok() and self.joint_state is None:
            rclpy.spin_once(self, timeout_sec=0.1)
            if time.time() - start > 5.0:
                self.get_logger().warn('Still waiting for /joint_states...')
                start = time.time()
        self.get_logger().info('Received /joint_states.')

    def solve_ik(self, target_pose):
        if self.joint_state is None:
            self.get_logger().error('No joint state received; cannot compute IK.')
            return None

        request = GetPositionIK.Request()
        request.ik_request.group_name = self.group_name
        request.ik_request.ik_link_name = self.tool_frame
        request.ik_request.robot_state = RobotState(joint_state=self.joint_state)
        request.ik_request.avoid_collisions = True

        pose_stamped = PoseStamped()
        pose_stamped.header.frame_id = self.base_frame
        pose_stamped.header.stamp = self.get_clock().now().to_msg()
        pose_stamped.pose = target_pose
        request.ik_request.pose_stamped = pose_stamped
        request.ik_request.timeout = Duration(seconds=0.5).to_msg()

        for i in range(self.attempts):
            self.get_logger().info(f'IK attempt #{i + 1}/{self.attempts}')
            future = self.ik_client.call_async(request)
            rclpy.spin_until_future_complete(self, future)
            response = future.result()

            if response is None:
                self.get_logger().error('IK service call failed.')
                return None

            if response.error_code.val == response.error_code.SUCCESS:
                joint_positions = response.solution.joint_state.position
                joint_names = response.solution.joint_state.name
                solution_map = dict(zip(joint_names, joint_positions))
                active_positions = [solution_map[name] for name in self.joint_names]
                return active_positions

        self.get_logger().error('IK failed to find a solution.')
        return None

    def get_current_joint_positions(self):
        if self.joint_state is None:
            self.get_logger().error('No joint state received.')
            return None

        joint_map = dict(zip(self.joint_state.name, self.joint_state.position))
        try:
            return [joint_map[name] for name in self.joint_names]
        except KeyError as exc:
            self.get_logger().error(f'Missing joint in /joint_states: {exc}')
            return None

    def get_current_tool_pose(self):
        deadline = time.time() + 2.0
        last_error = None
        transform = None

        while rclpy.ok() and time.time() < deadline:
            rclpy.spin_once(self, timeout_sec=0.1)
            try:
                transform = self.tf_buffer.lookup_transform(
                    self.base_frame,
                    self.tool_frame,
                    Time(),
                    timeout=Duration(seconds=0.0),
                )
                break
            except TransformException as exc:
                last_error = exc

        if transform is None:
            self.get_logger().error(
                f'Failed to lookup TF from {self.base_frame} to {self.tool_frame}: {last_error}'
            )
            return None

        pose = Pose()
        pose.position.x = transform.transform.translation.x
        pose.position.y = transform.transform.translation.y
        pose.position.z = transform.transform.translation.z
        pose.orientation = transform.transform.rotation
        return pose

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

        self.get_logger().info('Sending trajectory goal to JTC...')
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

        if result and result.error_code == result.SUCCESSFUL:
            self.get_logger().info('Trajectory execution finished successfully.')
        else:
            self.get_logger().warn(
                f'Trajectory execution failed with error code: {result.error_code if result else "N/A"}'
            )
        return result

    def move_relative_and_back(self, dx=0.0, dy=0.0, dz=0.0):
        current_joints = self.get_current_joint_positions()
        if current_joints is None:
            self.get_logger().error('Failed to read current joints.')
            return False

        current_pose = self.get_current_tool_pose()
        if current_pose is None:
            self.get_logger().error('Failed to read current tool pose from TF.')
            return False

        target_pose = Pose()
        target_pose.position.x = current_pose.position.x + dx
        target_pose.position.y = current_pose.position.y + dy
        target_pose.position.z = current_pose.position.z + dz
        target_pose.orientation = current_pose.orientation

        joint_goal = self.solve_ik(target_pose)
        if not joint_goal:
            self.get_logger().error('Failed to execute move because IK solution was not found.')
            return False

        waypoints = [current_joints, joint_goal, current_joints]
        durations = [0.0, self.duration, self.duration * 2.0]
        trajectory = self.create_trajectory(waypoints, durations)
        self.execute_trajectory(trajectory)
        return True

    def demo_sequence(self):
        self.get_logger().info('Starting IK + JTC demo: move current tool pose by z=+0.1 and return.')
        self.move_relative_and_back(dz=0.1)


def main():
    rclpy.init()
    node = JTCWithIKSolverDemo()
    try:
        node.wait_for_server()
        node.demo_sequence()
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
