ARG ROS_DISTRO=humble
FROM osrf/ros:${ROS_DISTRO}-desktop-full

ARG ROS_DISTRO=humble
ARG NVM_VERSION=v0.40.3
ARG NODE_VERSION=22

ENV DEBIAN_FRONTEND=noninteractive
ENV NVM_DIR=/home/ros/.nvm

RUN ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime     && apt-get update     && apt-get install -y tzdata sudo git curl ca-certificates     && date

COPY docker/install_packages.sh /tmp/install_packages.sh
RUN chmod +x /tmp/install_packages.sh && /tmp/install_packages.sh

RUN useradd -m -s /bin/bash ros     && mkdir -p /home/ros/.nvm     && ln -s /home/ros/zero_ros/ros2_ws /home/ros/ros2_ws     && chown -R ros:ros /home/ros     && echo "ros ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

COPY docker/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

USER ros
WORKDIR /home/ros/ros2_ws

RUN bash -lc 'curl -fsSL https://raw.githubusercontent.com/nvm-sh/nvm/${NVM_VERSION}/install.sh | bash     && source "$NVM_DIR/nvm.sh"     && nvm install ${NODE_VERSION}     && nvm alias default ${NODE_VERSION}     && nvm use default     && npm install -g @openai/codex'

RUN echo 'export NVM_DIR="/home/ros/.nvm"' >> /home/ros/.bashrc     && echo '[ -s "$NVM_DIR/nvm.sh" ] && source "$NVM_DIR/nvm.sh"' >> /home/ros/.bashrc     && echo '[ -s "$NVM_DIR/bash_completion" ] && source "$NVM_DIR/bash_completion"' >> /home/ros/.bashrc     && echo 'export ROS2_WS="/home/ros/ros2_ws"' >> /home/ros/.bashrc     && echo 'source /opt/ros/${ROS_DISTRO}/setup.bash' >> /home/ros/.bashrc     && echo 'if [ -f "$ROS2_WS/install/setup.bash" ]; then source "$ROS2_WS/install/setup.bash"; fi' >> /home/ros/.bashrc     && echo 'alias b="cd $ROS2_WS && colcon build --symlink-install && source install/setup.bash"' >> /home/ros/.bashrc

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["bash"]
