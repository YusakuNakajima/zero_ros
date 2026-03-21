#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TF Display Demo for ROS2 Waypoints Visualization
Based on tf_publisher.py from powder_grinding_ros2
"""

import rclpy
from rclpy.node import Node
import tf2_ros
import geometry_msgs.msg


class TfPublisher(Node):
    def __init__(self, node_name="tf_publisher_node", parent_link="base_link", child_link="debug_tf_") -> None:
        super().__init__(node_name)
        self.broadcaster = tf2_ros.TransformBroadcaster(self)
        self.tf_stamped = geometry_msgs.msg.TransformStamped()
        self.parent_link = parent_link
        self.child_link_prefix = child_link

    def broadcast_tf_with_waypoints(self, waypoints: list):
        if not waypoints:
            self.get_logger().warn("Waypoints list is empty. Nothing to broadcast.")
            return

        for index, pose_values in enumerate(waypoints):
            if not isinstance(pose_values, list) or len(pose_values) != 7:
                self.get_logger().error(
                    f"Waypoint at index {index} is not a list of 7 floats. Skipping."
                )
                continue

            current_transform = geometry_msgs.msg.Transform()
            current_transform.translation.x = float(pose_values[0])
            current_transform.translation.y = float(pose_values[1])
            current_transform.translation.z = float(pose_values[2])
            current_transform.rotation.x = float(pose_values[3])
            current_transform.rotation.y = float(pose_values[4])
            current_transform.rotation.z = float(pose_values[5])
            current_transform.rotation.w = float(pose_values[6])

            child_frame_id = self.child_link_prefix + str(index)
            self._broadcast_single_tf(current_transform, self.parent_link, child_frame_id)

        self.get_logger().info(
            f"Broadcasted TFs for {len(waypoints)} waypoints with prefix '{self.child_link_prefix}'."
        )

    def _broadcast_single_tf(
        self,
        transform_msg: geometry_msgs.msg.Transform,
        parent_link: str,
        child_link: str,
    ):
        self.tf_stamped.header.stamp = self.get_clock().now().to_msg()
        self.tf_stamped.header.frame_id = parent_link
        self.tf_stamped.child_frame_id = child_link
        self.tf_stamped.transform.translation = transform_msg.translation
        self.tf_stamped.transform.rotation = transform_msg.rotation
        self.broadcaster.sendTransform(self.tf_stamped)


class TFDisplayDemo(TfPublisher):
    def __init__(self):
        super().__init__(node_name="tf_display_demo", parent_link="base_link", child_link="waypoint_")
        self.waypoints = [
            [0.30, -0.20, 0.40, 0.0, 0.0, 0.0, 1.0],
            [0.45, 0.00, 0.50, 0.0, 0.0, 0.0, 1.0],
            [0.35, 0.20, 0.30, 0.0, 0.0, 0.0, 1.0],
        ]
        self.timer = self.create_timer(0.1, self._timer_cb)

    def _timer_cb(self):
        self.broadcast_tf_with_waypoints(self.waypoints)


def main():
    rclpy.init()
    node = TFDisplayDemo()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
