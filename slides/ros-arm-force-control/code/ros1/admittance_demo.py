#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Admittance Controller Demo for ROS2 Force Control
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Wrench, TwistStamped
from sensor_msgs.msg import JointState
from control_msgs.action import FollowJointTrajectory
from std_msgs.msg import Float64MultiArray
import numpy as np
import math

class AdmittanceControlDemo(Node):
    def __init__(self):
        super().__init__('admittance_control_demo')
        
        # Publishers
        self.admittance_pub = self.create_publisher(
            TwistStamped, '/admittance_controller/reference', 10)
        
        # Subscribers
        self.ft_sub = self.create_subscription(
            Wrench, '/force_torque_sensor_broadcaster/wrench', 
            self.force_callback, 10)
        
        # Admittance parameters (M, D, K matrices)
        self.mass = np.diag([10.0, 10.0, 10.0, 1.0, 1.0, 1.0])
        self.damping = np.diag([100.0, 100.0, 100.0, 10.0, 10.0, 10.0])
        self.stiffness = np.diag([500.0, 500.0, 500.0, 50.0, 50.0, 50.0])
        
        # Safety limits
        self.max_force = 50.0  # N
        self.max_velocity = 0.1  # m/s
        
        # Current force measurement
        self.current_wrench = Wrench()
        
        self.get_logger().info('Admittance Control Demo initialized')

    def force_callback(self, msg):
        """Force/torque sensor callback"""
        self.current_wrench = msg
        
        # Safety check
        force_magnitude = math.sqrt(
            msg.force.x**2 + msg.force.y**2 + msg.force.z**2)
        
        if force_magnitude > self.max_force:
            self.get_logger().warn(f'Force too high: {force_magnitude:.2f} N')
            self.emergency_stop()
            return
        
        # Compute admittance response
        self.compute_admittance_response(msg)

    def compute_admittance_response(self, wrench):
        """Calculate admittance response based on force input"""
        # Convert wrench to numpy array
        force_vector = np.array([
            wrench.force.x, wrench.force.y, wrench.force.z,
            wrench.torque.x, wrench.torque.y, wrench.torque.z
        ])
        
        # Admittance equation: M*xdd + D*xd + K*x = F
        # Solving for acceleration: xdd = M^-1 * (F - D*xd - K*x)
        
        # For simplicity, assume current position and velocity are zero
        # In practice, you would get these from robot state
        current_pos = np.zeros(6)
        current_vel = np.zeros(6)
        
        # Calculate desired acceleration
        desired_acc = np.linalg.inv(self.mass) @ (
            force_vector - self.damping @ current_vel - self.stiffness @ current_pos
        )
        
        # Integrate to get velocity (simple integration)
        dt = 0.01  # 100 Hz control loop
        desired_vel = current_vel + desired_acc * dt
        
        # Apply velocity limits
        desired_vel = np.clip(desired_vel, -self.max_velocity, self.max_velocity)
        
        # Publish velocity command
        self.publish_velocity_command(desired_vel)

    def publish_velocity_command(self, velocity):
        """Publish velocity command to admittance controller"""
        twist_msg = TwistStamped()
        twist_msg.header.stamp = self.get_clock().now().to_msg()
        twist_msg.header.frame_id = 'base_link'
        
        twist_msg.twist.linear.x = velocity[0]
        twist_msg.twist.linear.y = velocity[1]
        twist_msg.twist.linear.z = velocity[2]
        twist_msg.twist.angular.x = velocity[3]
        twist_msg.twist.angular.y = velocity[4]
        twist_msg.twist.angular.z = velocity[5]
        
        self.admittance_pub.publish(twist_msg)

    def emergency_stop(self):
        """Emergency stop function"""
        # Send zero velocity
        zero_velocity = np.zeros(6)
        self.publish_velocity_command(zero_velocity)
        self.get_logger().error('EMERGENCY STOP ACTIVATED')

    def set_impedance_parameters(self, mass, damping, stiffness):
        """Update impedance parameters during runtime"""
        self.mass = np.diag(mass)
        self.damping = np.diag(damping)
        self.stiffness = np.diag(stiffness)
        
        self.get_logger().info('Impedance parameters updated')

def main(args=None):
    rclpy.init(args=args)
    
    demo = AdmittanceControlDemo()
    
    try:
        rclpy.spin(demo)
    except KeyboardInterrupt:
        demo.get_logger().info('Demo stopped by user')
    finally:
        demo.emergency_stop()
        demo.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()