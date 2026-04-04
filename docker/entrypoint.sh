#!/bin/bash
set -e

export NVM_DIR=${NVM_DIR:-/home/ros/.nvm}
export ROS2_WS=${ROS2_WS:-/home/ros/ros2_ws}

ln -sfn /home/ros/zero_ros/ros2_ws "$ROS2_WS"

if [ -s "$NVM_DIR/nvm.sh" ]; then
  source "$NVM_DIR/nvm.sh"
  nvm use default >/dev/null 2>&1 || true
fi
if [ -s "$NVM_DIR/bash_completion" ]; then
  source "$NVM_DIR/bash_completion"
fi

source /opt/ros/${ROS_DISTRO:-humble}/setup.bash
if [ -f "$ROS2_WS/install/setup.bash" ]; then
  source "$ROS2_WS/install/setup.bash"
fi

add_resource_path() {
  local var_name="$1"
  local path="$2"
  local current="${!var_name:-}"
  if [ -z "$path" ] || [ ! -d "$path" ]; then
    return
  fi
  case ":$current:" in
    *":$path:"*) ;;
    "")
      export "${var_name}=$path"
      ;;
    *)
      export "${var_name}=${current}:$path"
      ;;
  esac
}

add_resource_path GZ_SIM_RESOURCE_PATH /opt/ros/${ROS_DISTRO:-humble}/share
add_resource_path GZ_SIM_RESOURCE_PATH "$ROS2_WS/install/ros_study/share"
add_resource_path IGN_GAZEBO_RESOURCE_PATH /opt/ros/${ROS_DISTRO:-humble}/share
add_resource_path IGN_GAZEBO_RESOURCE_PATH "$ROS2_WS/install/ros_study/share"

exec "$@"
