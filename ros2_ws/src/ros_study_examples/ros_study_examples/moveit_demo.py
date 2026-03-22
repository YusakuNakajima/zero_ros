#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reference entry for the MoveIt2 demo used in the zero_ros slides.

The working end-to-end planning example in this repository is implemented in
ros_study_cpp_examples/src/ur_moveit_demo.cpp. This file remains as a small
ROS 2 helper so that the Python examples package no longer contains ROS 1 code.
"""

import rclpy
from rclpy.node import Node


class MoveItDemoReference(Node):
    def __init__(self):
        super().__init__('moveit_demo_reference')
        self.get_logger().info(
            'Prerequisite: start the mock-components simulator and MoveIt overlay first.'
        )
        self.get_logger().info(
            'Example: `ros2 launch ros_study_bringup ur5e_bringup_with_mock_components.launch.py launch_moveit:=true`'
        )
        self.get_logger().info('Use `ros2 run ros_study_cpp_examples ur_moveit_demo_cpp` for the MoveIt2 planning demo.')
        self.get_logger().info('This Python file is kept as a pointer from the slide materials to the canonical C++ example.')


def main():
    rclpy.init()
    node = MoveItDemoReference()
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
