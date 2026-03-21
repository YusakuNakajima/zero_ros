ARG ROS_DISTRO=humble
FROM osrf/ros:${ROS_DISTRO}-desktop-full

ENV DEBIAN_FRONTEND=noninteractive

RUN ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime     && apt-get update     && apt-get install -y tzdata sudo git curl     && date

COPY docker/install_packages.sh /tmp/install_packages.sh
RUN chmod +x /tmp/install_packages.sh && /tmp/install_packages.sh

RUN useradd -m -s /bin/bash ros     && echo "ros ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

COPY docker/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

USER ros
WORKDIR /home/ros/zero_ros/ros2_ws

RUN echo 'source /opt/ros/${ROS_DISTRO}/setup.bash' >> /home/ros/.bashrc     && echo 'if [ -f /home/ros/zero_ros/ros2_ws/install/setup.bash ]; then source /home/ros/zero_ros/ros2_ws/install/setup.bash; fi' >> /home/ros/.bashrc     && echo 'alias b="cd /home/ros/zero_ros/ros2_ws && colcon build --symlink-install && source install/setup.bash"' >> /home/ros/.bashrc

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["bash"]
