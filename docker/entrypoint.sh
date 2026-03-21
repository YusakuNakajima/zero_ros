#!/bin/bash
set -e

source /opt/ros/${ROS_DISTRO:-humble}/setup.bash
if [ -f /home/ros/zero_ros/ros2_ws/install/setup.bash ]; then
  source /home/ros/zero_ros/ros2_ws/install/setup.bash
fi

exec "$@"
