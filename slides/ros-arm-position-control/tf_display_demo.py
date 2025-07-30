#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TF Display Demo for ROS Waypoints Visualization
Based on tf_publisher.py from powder_grinding project
"""

import rospy
import tf2_ros
import tf
from geometry_msgs.msg import TransformStamped, Pose
from tf.transformations import quaternion_from_euler
import numpy as np
from math import pi, sin, cos

class TFDisplayDemo:
    def __init__(self):
        rospy.init_node('tf_display_demo', anonymous=True)
        
        # TF2ブロードキャスター
        self.tf_broadcaster = tf2_ros.TransformBroadcaster()
        
        # TFリスナー
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer)
        
        print("TF Display Demo initialized!")

    def publish_transform(self, parent_frame, child_frame, position, orientation):
        """TF変換をパブリッシュ"""
        transform = TransformStamped()
        
        transform.header.stamp = rospy.Time.now()
        transform.header.frame_id = parent_frame
        transform.child_frame_id = child_frame
        
        # 位置設定
        transform.transform.translation.x = position[0]
        transform.transform.translation.y = position[1]
        transform.transform.translation.z = position[2]
        
        # 向き設定
        transform.transform.rotation.x = orientation[0]
        transform.transform.rotation.y = orientation[1]
        transform.transform.rotation.z = orientation[2]
        transform.transform.rotation.w = orientation[3]
        
        self.tf_broadcaster.sendTransform(transform)

    def publish_waypoint_frames(self, waypoints, base_frame="base_link"):
        """waypoint群をTFフレームとしてパブリッシュ"""
        for i, waypoint in enumerate(waypoints):
            # フレーム名を生成
            frame_name = f"waypoint_{i:02d}"
            
            # 位置
            position = waypoint[:3]
            
            # 向き（ここでは簡単な例として、Z軸回転のみ）
            if len(waypoint) >= 4:
                # waypointに向きの情報が含まれている場合
                yaw = waypoint[3]
            else:
                # デフォルトの向き
                yaw = 0.0
            
            # クォータニオンに変換
            quat = quaternion_from_euler(0, 0, yaw)
            
            # TF変換をパブリッシュ
            self.publish_transform(base_frame, frame_name, position, quat)

    def listen_transform(self, target_frame, source_frame):
        """TF変換を取得"""
        try:
            transform = self.tf_buffer.lookup_transform(
                target_frame, source_frame, rospy.Time()
            )
            return transform
        except (tf2_ros.LookupException, 
                tf2_ros.ConnectivityException, 
                tf2_ros.ExtrapolationException) as e:
            rospy.logwarn(f"Failed to lookup transform: {e}")
            return None

    def publish_pose_as_tf(self, pose, frame_name, parent_frame="base_link"):
        """Poseメッセージ型をTFフレームとしてパブリッシュ"""
        position = [
            pose.position.x,
            pose.position.y, 
            pose.position.z
        ]
        
        orientation = [
            pose.orientation.x,
            pose.orientation.y,
            pose.orientation.z,
            pose.orientation.w
        ]
        
        self.publish_transform(parent_frame, frame_name, position, orientation)

    def create_circular_waypoints(self):
        """円形のwaypointを生成"""
        waypoints = []
        center = [0.4, 0.0, 0.4]
        radius = 0.2
        
        for i in range(8):
            angle = 2 * pi * i / 8
            x = center[0] + radius * cos(angle)
            y = center[1] + radius * sin(angle)
            z = center[2]
            yaw = angle + pi/2  # 円の接線方向を向く
            waypoints.append([x, y, z, yaw])
        
        return waypoints

    def create_linear_waypoints(self):
        """直線状のwaypointを生成"""
        waypoints = []
        for i in range(5):
            x = 0.3 + i * 0.1
            y = 0.0
            z = 0.4
            yaw = 0.0  # すべて同じ方向
            waypoints.append([x, y, z, yaw])
        
        return waypoints

    def demo_sequence(self):
        """デモシーケンス"""
        print("============ Starting TF Display Demo")
        
        rate = rospy.Rate(10)  # 10Hz
        
        # 1. 直線状のwaypoints
        print("1. Publishing linear waypoints as TF frames...")
        linear_waypoints = self.create_linear_waypoints()
        
        for _ in range(50):  # 5秒間パブリッシュ
            self.publish_waypoint_frames(linear_waypoints)
            rate.sleep()
        
        # 2. 円形のwaypoints
        print("2. Publishing circular waypoints as TF frames...")
        circular_waypoints = self.create_circular_waypoints()
        
        for _ in range(50):  # 5秒間パブリッシュ
            self.publish_waypoint_frames(circular_waypoints)
            rate.sleep()
        
        # 3. 動的なTFフレーム（回転する例）
        print("3. Publishing dynamic rotating frame...")
        for i in range(100):
            angle = 2 * pi * i / 100
            x = 0.4 + 0.1 * cos(angle)
            y = 0.1 * sin(angle)
            z = 0.4 + 0.05 * sin(2 * angle)
            yaw = angle
            
            position = [x, y, z]
            quat = quaternion_from_euler(0, 0, yaw)
            
            self.publish_transform("base_link", "rotating_frame", position, quat)
            rate.sleep()
        
        print("============ TF Display Demo Complete!")

    def simple_example(self):
        """シンプルな例"""
        print("Simple TF display example:")
        print("Publishing 3 waypoint frames...")
        
        waypoints = [
            [0.3, -0.2, 0.4, 0.0],      # waypoint_00
            [0.5, 0.0, 0.6, pi/4],      # waypoint_01  
            [0.4, 0.2, 0.3, pi/2]       # waypoint_02
        ]
        
        rate = rospy.Rate(10)
        
        # 10秒間パブリッシュ
        for _ in range(100):
            self.publish_waypoint_frames(waypoints)
            rate.sleep()
        
        print("Demo finished. TF frames should be visible in RViz!")
        print("Add 'TF' display in RViz to see the coordinate frames")

    def continuous_publish(self):
        """継続的にTFをパブリッシュ（ROSspinで使用）"""
        waypoints = [
            [0.3, -0.2, 0.4, 0.0],
            [0.5, 0.0, 0.6, pi/4],
            [0.4, 0.2, 0.3, pi/2]
        ]
        
        rate = rospy.Rate(10)
        
        while not rospy.is_shutdown():
            self.publish_waypoint_frames(waypoints)
            
            # 追加で動的フレームもパブリッシュ
            current_time = rospy.Time.now().to_sec()
            angle = current_time * 0.5  # ゆっくり回転
            x = 0.4 + 0.1 * cos(angle)
            y = 0.1 * sin(angle)
            z = 0.4
            yaw = angle
            
            position = [x, y, z]
            quat = quaternion_from_euler(0, 0, yaw)
            self.publish_transform("base_link", "dynamic_frame", position, quat)
            
            rate.sleep()

def main():
    try:
        demo = TFDisplayDemo()
        
        # シンプルな例を実行
        # demo.simple_example()
        
        # 継続的にパブリッシュ（RVizで確認用）
        print("Publishing TF frames continuously...")
        print("Open RViz and add 'TF' display to see the frames")
        demo.continuous_publish()
        
    except rospy.ROSInterruptException:
        return
    except KeyboardInterrupt:
        return

if __name__ == '__main__':
    main()