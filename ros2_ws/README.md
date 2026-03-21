# zero_ros ROS2 Workspace

この `ros2_ws` が、ROS2 スライドの canonical source です。`slides/.../code/ros2` は過去の slide-local copy として残し、新規編集はこの workspace 側に集約します。

## 使い方

```bash
cd ~/zero_ros/ros2_ws
colcon build --symlink-install
source install/setup.bash
```

Docker を使う場合は、リポジトリ直下から以下を実行します。

```bash
docker compose -f docker/compose.yaml up --build
```

## Dockerから入る場合

```bash
docker compose -f docker/compose.yaml up -d --build
docker compose -f docker/compose.yaml exec ros_study bash
cd /home/ros/zero_ros/ros2_ws
colcon build --symlink-install
source install/setup.bash
```

## パッケージ構成

- `ros_study_description`: URDF/Xacro、mesh、RViz、モデル表示 launch
- `ros_study_bringup`: MoveIt / UR driver / mock components 用 launch と controller 設定
- `ros_study_examples`: Python サンプルノード
- `ros_study_cpp_examples`: C++ サンプルノード

## 代表コマンド

```bash
ros2 launch ros_study_description view_ur.launch.py
ros2 launch ros_study_description view_ur_with_ee.launch.py
ros2 launch ros_study_bringup ur5e_bringup_with_moveit.launch.py
ros2 launch ros_study_bringup ur5e_bringup_with_mock_components.launch.py
ros2 run ros_study_examples jtc_demo
ros2 run ros_study_cpp_examples ur_moveit_demo_cpp
```

## スライドとの対応

- `ros-model-display`: `ros_study_description`
- `ros-arm-position-control`: `ros_study_bringup`, `ros_study_examples`, `ros_study_cpp_examples`
- `ros-simulator-connection`: `ros_study_bringup`, `ros_study_description`, `ros_study_cpp_examples`
- `ros-arm-force-control`: `ros_study_examples`, `ros_study_bringup`
