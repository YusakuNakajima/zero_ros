#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Marker Display Demo for ROS Waypoints Visualization
Based on marker_display.py from powder_grinding project
"""

import rospy
from visualization_msgs.msg import Marker, MarkerArray
from geometry_msgs.msg import Point, Pose, Vector3
from std_msgs.msg import ColorRGBA
import numpy as np
from math import pi, sin, cos

class MarkerDisplayDemo:
    def __init__(self):
        rospy.init_node('marker_display_demo', anonymous=True)
        
        # MarkerArrayパブリッシャー
        self.marker_pub = rospy.Publisher(
            '/waypoint_markers',
            MarkerArray,
            queue_size=10
        )
        
        # 個別Markerパブリッシャー
        self.single_marker_pub = rospy.Publisher(
            '/single_marker',
            Marker,
            queue_size=10
        )
        
        print("Marker Display Demo initialized!")

    def create_sphere_marker(self, position, marker_id, color=[1.0, 0.0, 0.0, 1.0], scale=0.05):
        """球形マーカーを作成"""
        marker = Marker()
        marker.header.frame_id = "base_link"
        marker.header.stamp = rospy.Time.now()
        marker.ns = "waypoints"
        marker.id = marker_id
        marker.type = Marker.SPHERE
        marker.action = Marker.ADD
        
        # 位置設定
        marker.pose.position.x = position[0]
        marker.pose.position.y = position[1] 
        marker.pose.position.z = position[2]
        marker.pose.orientation.w = 1.0
        
        # スケール設定
        marker.scale.x = scale
        marker.scale.y = scale
        marker.scale.z = scale
        
        # 色設定
        marker.color.r = color[0]
        marker.color.g = color[1]
        marker.color.b = color[2]
        marker.color.a = color[3]
        
        return marker

    def create_arrow_marker(self, position, orientation, marker_id, color=[0.0, 1.0, 0.0, 1.0]):
        """矢印マーカーを作成"""
        marker = Marker()
        marker.header.frame_id = "base_link"
        marker.header.stamp = rospy.Time.now()
        marker.ns = "directions"
        marker.id = marker_id
        marker.type = Marker.ARROW
        marker.action = Marker.ADD
        
        # 位置と向きの設定
        marker.pose.position.x = position[0]
        marker.pose.position.y = position[1]
        marker.pose.position.z = position[2]
        marker.pose.orientation.x = orientation[0]
        marker.pose.orientation.y = orientation[1]
        marker.pose.orientation.z = orientation[2]
        marker.pose.orientation.w = orientation[3]
        
        # スケール設定
        marker.scale.x = 0.1  # 長さ
        marker.scale.y = 0.01  # 幅
        marker.scale.z = 0.01  # 高さ
        
        # 色設定
        marker.color.r = color[0]
        marker.color.g = color[1]
        marker.color.b = color[2]
        marker.color.a = color[3]
        
        return marker

    def create_line_strip_marker(self, points, marker_id, color=[0.0, 0.0, 1.0, 1.0]):
        """線ストリップマーカーを作成"""
        marker = Marker()
        marker.header.frame_id = "base_link"
        marker.header.stamp = rospy.Time.now()
        marker.ns = "path"
        marker.id = marker_id
        marker.type = Marker.LINE_STRIP
        marker.action = Marker.ADD
        
        # 線の幅
        marker.scale.x = 0.005
        
        # 色設定
        marker.color.r = color[0]
        marker.color.g = color[1]
        marker.color.b = color[2]
        marker.color.a = color[3]
        
        # 点列設定
        for point in points:
            p = Point()
            p.x = point[0]
            p.y = point[1]
            p.z = point[2]
            marker.points.append(p)
        
        return marker

    def display_waypoints_array(self, waypoints):
        """waypoint配列をMarkerArrayで表示"""
        marker_array = MarkerArray()
        
        # 各waypointに球形マーカーを作成
        for i, waypoint in enumerate(waypoints):
            # 色を変化させる（赤→黄→緑）
            if i == 0:
                color = [1.0, 0.0, 0.0, 1.0]  # 赤（開始点）
            elif i == len(waypoints) - 1:
                color = [0.0, 1.0, 0.0, 1.0]  # 緑（終了点）
            else:
                ratio = float(i) / (len(waypoints) - 1)
                color = [1.0 - ratio, ratio, 0.0, 1.0]  # 赤→緑のグラデーション
            
            marker = self.create_sphere_marker(waypoint, i, color, scale=0.03)
            marker_array.markers.append(marker)
        
        # 経路の線を追加
        if len(waypoints) > 1:
            path_marker = self.create_line_strip_marker(waypoints, len(waypoints))
            marker_array.markers.append(path_marker)
        
        # パブリッシュ
        self.marker_pub.publish(marker_array)
        print(f"Published {len(waypoints)} waypoint markers")

    def clear_all_markers(self):
        """すべてのマーカーをクリア"""
        marker_array = MarkerArray()
        
        # 削除用マーカーを作成
        for i in range(100):  # 十分な数のマーカーを削除
            marker = Marker()
            marker.header.frame_id = "base_link"
            marker.ns = "waypoints"
            marker.id = i
            marker.action = Marker.DELETE
            marker_array.markers.append(marker)
            
            marker = Marker()
            marker.header.frame_id = "base_link"
            marker.ns = "directions"
            marker.id = i
            marker.action = Marker.DELETE
            marker_array.markers.append(marker)
        
        # パス用マーカーも削除
        marker = Marker()
        marker.header.frame_id = "base_link"
        marker.ns = "path"
        marker.id = 0
        marker.action = Marker.DELETE
        marker_array.markers.append(marker)
        
        self.marker_pub.publish(marker_array)
        print("Cleared all markers")

    def demo_sequence(self):
        """デモシーケンス"""
        print("============ Starting Marker Display Demo")
        
        rospy.sleep(1.0)
        
        # 1. 直線状のwaypoints
        print("1. Displaying linear waypoints...")
        linear_waypoints = []
        for i in range(5):
            x = 0.3 + i * 0.1
            y = 0.0
            z = 0.4
            linear_waypoints.append([x, y, z])
        
        self.display_waypoints_array(linear_waypoints)
        rospy.sleep(3.0)
        
        # 2. 円形のwaypoints
        print("2. Displaying circular waypoints...")
        circular_waypoints = []
        center = [0.4, 0.0, 0.4]
        radius = 0.15
        for i in range(8):
            angle = 2 * pi * i / 8
            x = center[0] + radius * cos(angle)
            y = center[1] + radius * sin(angle)
            z = center[2]
            circular_waypoints.append([x, y, z])
        
        self.clear_all_markers()
        rospy.sleep(0.5)
        self.display_waypoints_array(circular_waypoints)
        rospy.sleep(3.0)
        
        # 3. 3次元螺旋のwaypoints
        print("3. Displaying spiral waypoints...")
        spiral_waypoints = []
        for i in range(12):
            angle = 2 * pi * i / 12
            radius = 0.1 + 0.1 * (i / 12.0)
            x = 0.4 + radius * cos(angle)
            y = 0.0 + radius * sin(angle)
            z = 0.3 + 0.2 * (i / 12.0)
            spiral_waypoints.append([x, y, z])
        
        self.clear_all_markers()
        rospy.sleep(0.5)
        self.display_waypoints_array(spiral_waypoints)
        rospy.sleep(3.0)
        
        # 4. 個別マーカーの例
        print("4. Displaying individual markers...")
        marker = self.create_sphere_marker([0.5, 0.2, 0.5], 0, [1.0, 1.0, 0.0, 1.0], 0.08)
        self.single_marker_pub.publish(marker)
        
        print("============ Marker Display Demo Complete!")

    def simple_example(self):
        """シンプルな例"""
        print("Simple marker display example:")
        
        # 3つのwaypointを表示
        waypoints = [
            [0.3, -0.2, 0.4],  # 開始点
            [0.5, 0.0, 0.6],   # 中間点
            [0.4, 0.2, 0.3]    # 終了点
        ]
        
        print("Displaying 3 waypoints with connecting path...")
        self.display_waypoints_array(waypoints)
        
        rospy.sleep(5.0)
        print("Demo finished. Markers should be visible in RViz!")

def main():
    try:
        demo = MarkerDisplayDemo()
        
        # シンプルな例を実行
        demo.simple_example()
        
        # フルデモを実行する場合（コメントアウト解除）
        # demo.demo_sequence()
        
        # ROSが終了するまで待機
        rospy.spin()
        
    except rospy.ROSInterruptException:
        return
    except KeyboardInterrupt:
        return

if __name__ == '__main__':
    main()