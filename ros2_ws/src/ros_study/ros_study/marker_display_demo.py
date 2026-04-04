#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Marker Display Demo for ROS2 Waypoints Visualization
Based on marker_publisher.py from powder_grinding_ros2
"""

import time
import numpy as np
import rclpy
from rclpy.node import Node

from visualization_msgs.msg import Marker
from visualization_msgs.msg import MarkerArray
from geometry_msgs.msg import Pose, Quaternion
from builtin_interfaces.msg import Duration
from tf_transformations import quaternion_from_euler, quaternion_multiply


class MarkerPublisher(Node):
    def __init__(self, marker_publisher_name="debug_marker", node_name="marker_display"):
        super().__init__(node_name)
        self.publisher = self.create_publisher(MarkerArray, marker_publisher_name, 1)
        self.index = 0

    def wait_for_connection(self):
        self.get_logger().info(
            f'Waiting for a subscriber to connect to the marker publisher on topic "{self.publisher.topic_name}"'
        )
        while self.publisher.get_subscription_count() == 0:
            time.sleep(1)
        self.get_logger().info(
            f'Subscriber connected to the marker publisher on topic "{self.publisher.topic_name}"!'
        )

    def display_waypoints(self, waypoints, scale=0.002, marker_type=None, clear=False):
        marker_array = MarkerArray()

        if clear:
            delete_marker = Marker()
            delete_marker.header.frame_id = "world"
            delete_marker.header.stamp = self.get_clock().now().to_msg()
            delete_marker.ns = "waypoints"
            delete_marker.action = Marker.DELETEALL
            marker_array.markers.append(delete_marker)
            self.publisher.publish(marker_array)
            return

        if marker_type is None:
            marker_type = Marker.SPHERE

        for index, points in enumerate(waypoints):
            if not isinstance(points, Pose):
                point_pose = Pose()
                point_pose.position.x = points[0]
                point_pose.position.y = points[1]
                point_pose.position.z = points[2]
                point_pose.orientation.x = points[3]
                point_pose.orientation.y = points[4]
                point_pose.orientation.z = points[5]
                point_pose.orientation.w = points[6]
                points = point_pose

            marker = Marker()
            marker.header.frame_id = "world"
            marker.header.stamp = self.get_clock().now().to_msg()
            marker.ns = "waypoints"
            self.index += 1
            marker.id = self.index
            marker.action = Marker.ADD

            marker.pose.position = points.position
            marker.pose.orientation = points.orientation

            red_strength = 1.0 * index / (len(waypoints) - 1)
            blue_strength = 1.0 * (len(waypoints) - index - 1) / (len(waypoints) - 1)
            marker.color.r = red_strength
            marker.color.g = 0.0
            marker.color.b = blue_strength
            marker.color.a = 1.0

            if marker_type == marker.ARROW:
                marker.scale.x = scale
                marker.scale.y = scale * 0.1
                marker.scale.z = scale * 0.1

                quat = [
                    marker.pose.orientation.x,
                    marker.pose.orientation.y,
                    marker.pose.orientation.z,
                    marker.pose.orientation.w,
                ]
                q_orig = np.array(quat)
                q_rot = quaternion_from_euler(0, np.pi / 2, 0)
                q_new = quaternion_multiply(q_rot, q_orig)
                marker.pose.orientation = Quaternion(
                    x=q_new[0], y=q_new[1], z=q_new[2], w=q_new[3]
                )
            else:
                marker.scale.x = scale
                marker.scale.y = scale
                marker.scale.z = scale

            marker.type = marker_type
            marker.lifetime = Duration(sec=60)
            marker_array.markers.append(marker)

        self.wait_for_connection()
        self.publisher.publish(marker_array)
        self.get_logger().info("Published!")


def main():
    rclpy.init()
    node = MarkerPublisher()

    waypoints = [
        [0.30, -0.20, 0.40, 0.0, 0.0, 0.0, 1.0],
        [0.45, 0.00, 0.50, 0.0, 0.0, 0.0, 1.0],
        [0.35, 0.20, 0.30, 0.0, 0.0, 0.0, 1.0],
    ]

    node.display_waypoints(waypoints, scale=0.02, marker_type=Marker.SPHERE)
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
