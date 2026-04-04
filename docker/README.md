# zero_ros Docker Environment

このディレクトリは Ubuntu/Linux + X11 前提の ROS2 Humble 開発環境です。`RViz` や `rqt` をコンテナ内でそのまま起動できます。あわせて `nvm` と `@openai/codex` もイメージ内に入るようにしています。

## 事前準備

```bash
sudo apt install docker.io docker-compose-plugin
xhost +local:docker
```

## 起動

```bash
docker compose -f docker/compose.yaml up --build --remove-orphans
```

バックグラウンド起動にしたい場合:

```bash
docker compose -f docker/compose.yaml up -d --build --remove-orphans
```

## よく使うコマンド

```bash
# コンテナ一覧を確認
docker compose -f docker/compose.yaml ps

# Codex CLI の確認
codex --help

# シェルに入る
docker compose -f docker/compose.yaml exec ros_study bash

# ログを追う
docker compose -f docker/compose.yaml logs -f

# コンテナを停止・削除
docker compose -f docker/compose.yaml down --remove-orphans

# イメージを作り直す
docker compose -f docker/compose.yaml build --no-cache
```

## コンテナ内でのビルド

```bash
cd ~/ros2_ws
colcon build --symlink-install
source install/setup.bash
```

## 起動後の次の進め方

`ros_study_humble Started` まで出たら、次は次のどちらかです。

1. ターミナルで入る

```bash
docker compose -f docker/compose.yaml exec ros_study bash
cd ~/ros2_ws
colcon build --symlink-install
source install/setup.bash
```

2. VSCode から attach する

- Dev Containers 拡張を入れる
- `Dev Containers: Attach to Running Container...` を実行する
- `ros_study_humble` を選ぶ
- 開いたターミナルで `cd ~/ros2_ws` して作業する

## コンテナ内での代表コマンド

```bash
ros2 launch ros_study view_ur.launch.py
ros2 launch ros_study view_ur_with_ee.launch.py
ros2 launch ros_study ur5e_bringup_with_moveit.launch.py
ros2 launch ros_study ur5e_bringup_with_mock_components.launch.py
ros2 run ros_study jtc_demo
ros2 run ros_study ur_moveit_demo_cpp
```

## 注意

- ホスト環境によって `render` グループが存在しないことがあるため、Compose では追加グループ指定を外してあります。
- service 名変更後に orphan 警告が出た場合も、上の `--remove-orphans` 付きコマンドで整理できます。
- GUI は X11 前提です。Wayland 専用の調整は含めていません。
- `host network` と `/dev` マウントを使うため、教材用でも Linux ホスト前提です。
- 初回起動では `zero_ros` リポジトリ全体が `/home/ros/zero_ros` にマウントされます。
- Gazebo デモ用に `ros-${ROS_DISTRO}-ros-gz` と `ros-${ROS_DISTRO}-gz-ros2-control` もイメージへ入るようにしています。
- entrypoint で `GZ_SIM_RESOURCE_PATH` と `IGN_GAZEBO_RESOURCE_PATH` に ROS と workspace の share ディレクトリを追加し、`package://...` / `model://...` の mesh 解決を補助しています。
