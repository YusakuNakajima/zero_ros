#!/bin/bash
set -eux

: "${ROS_DISTRO:=humble}"

apt-get update && apt-get install -y     build-essential     git     iputils-ping     nano     net-tools     python3-colcon-common-extensions     python3-numpy     python3-pip     python3-rosdep     python3-vcstool     tmux     vim     wget     xterm

apt-get update && apt-get install -y     ros-${ROS_DISTRO}-joint-state-publisher-gui     ros-${ROS_DISTRO}-moveit     ros-${ROS_DISTRO}-moveit-visual-tools     ros-${ROS_DISTRO}-ros2-control     ros-${ROS_DISTRO}-ros2-controllers     ros-${ROS_DISTRO}-rqt-controller-manager     ros-${ROS_DISTRO}-rqt-joint-trajectory-controller     ros-${ROS_DISTRO}-rqt-tf-tree     ros-${ROS_DISTRO}-tf-transformations     ros-${ROS_DISTRO}-tf2-ros-py     ros-${ROS_DISTRO}-ur     ros-${ROS_DISTRO}-xacro

apt-get clean
rm -rf /var/lib/apt/lists/*
