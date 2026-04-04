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
cd ~/ros2_ws
colcon build --symlink-install
source install/setup.bash
```

## パッケージ構成

- `ros_study`: URDF/Xacro、mesh、RViz、モデル表示 launch、MoveIt / UR driver / mock components 用 launch と controller 設定、Python / C++ サンプルノードをまとめた単一パッケージ

## 代表コマンド

```bash
ros2 launch ros_study view_ur.launch.py
ros2 launch ros_study view_ur_with_ee.launch.py
ros2 launch ros_study ur5e_bringup_with_moveit.launch.py
ros2 launch ros_study ur5e_bringup_with_mock_components.launch.py
ros2 run ros_study jtc_demo
ros2 run ros_study ur_moveit_demo_cpp
```

## 実装確認

追加した Mock Components / JointTrajectoryController / MoveIt2 / Gazebo の確認手順は
[`docs/implementation_check.md`](docs/implementation_check.md)
を参照してください。

## スライドとの対応

- `ros-model-display`: `ros_study`
- `ros-arm-position-control`: `ros_study`
- `ros-simulator-connection`: `ros_study`
- `ros-arm-force-control`: `ros_study`
