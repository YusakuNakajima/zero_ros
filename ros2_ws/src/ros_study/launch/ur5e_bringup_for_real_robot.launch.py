# ur5e_with_pestle_bringup.launch.py
#
# ros_study/launch/ur_control.launch.py (ドライバ + コントローラ) と
# ur_moveit_config/launch/ur_moveit.launch.py (MoveIt) をまとめて起動する。

from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    GroupAction,
    IncludeLaunchDescription,
    OpaqueFunction,
)
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import (
    AndSubstitution,
    LaunchConfiguration,
    NotSubstitution,
    PathJoinSubstitution,
)
from launch_ros.substitutions import FindPackageShare

# ur_control.launch.py の choices と同じもの
UR_TYPES = [
    "ur3",
    "ur5",
    "ur10",
    "ur3e",
    "ur5e",
    "ur7e",
    "ur10e",
    "ur12e",
    "ur16e",
    "ur8long",
    "ur15",
    "ur18",
    "ur20",
    "ur30",
]

JOINT_CONTROLLERS = [
    "scaled_joint_trajectory_controller",
    "joint_trajectory_controller",
    "forward_velocity_controller",
    "forward_position_controller",
    "freedrive_mode_controller",
    "passthrough_trajectory_controller",
]


def launch_setup(context, *args, **kwargs):
    # --- Launch Configuration ---
    ur_type = LaunchConfiguration("ur_type")
    robot_ip = LaunchConfiguration("robot_ip")
    use_fake_hardware = LaunchConfiguration("use_fake_hardware")
    fake_sensor_commands = LaunchConfiguration("fake_sensor_commands")
    initial_joint_controller = LaunchConfiguration("initial_joint_controller")
    activate_joint_controller = LaunchConfiguration("activate_joint_controller")
    headless_mode = LaunchConfiguration("headless_mode")
    launch_dashboard_client = LaunchConfiguration("launch_dashboard_client")
    controller_spawner_timeout = LaunchConfiguration("controller_spawner_timeout")
    use_moveit = LaunchConfiguration("use_moveit")
    launch_rviz = LaunchConfiguration("launch_rviz")

    # --- ur_control (ドライバ + コントローラ) ---
    # RViz は MoveIt を使うときは MoveIt 側で起動し、
    # MoveIt を使わないときだけ ur_control 側 (view_robot.rviz) で起動する。
    ur_control_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([FindPackageShare("ros_study"), "launch", "ur_control.launch.py"])
        ),
        launch_arguments={
            "ur_type": ur_type,
            "robot_ip": robot_ip,
            "use_fake_hardware": use_fake_hardware,
            "fake_sensor_commands": fake_sensor_commands,
            "initial_joint_controller": initial_joint_controller,
            "activate_joint_controller": activate_joint_controller,
            "headless_mode": headless_mode,
            "launch_dashboard_client": launch_dashboard_client,
            "controller_spawner_timeout": controller_spawner_timeout,
            "launch_rviz": AndSubstitution(launch_rviz, NotSubstitution(use_moveit)),
        }.items(),
    )

    # --- ur_moveit (MoveIt) ---
    ur_moveit_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution(
                [FindPackageShare("ur_moveit_config"), "launch", "ur_moveit.launch.py"]
            )
        ),
        launch_arguments={
            "ur_type": ur_type,
            "launch_rviz": launch_rviz,
        }.items(),
        condition=IfCondition(use_moveit),
    )

    # IncludeLaunchDescription は launch_arguments を共有コンテキストに書き込むため、
    # そのままだと ur_control に渡した launch_rviz:=false が ur_moveit 側にも漏れて
    # MoveIt の RViz まで起動しなくなる。scoped な GroupAction で囲んで隔離する。
    return [
        GroupAction([ur_control_launch], scoped=True),
        GroupAction([ur_moveit_launch], scoped=True),
    ]


def generate_launch_description():
    declared_arguments = []

    declared_arguments.append(
        DeclareLaunchArgument(
            "ur_type",
            default_value="ur5e",
            choices=UR_TYPES,
            description="Robot model of the used UR robot.",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "robot_ip",
            default_value="192.168.58.42",
            description="IP address by which the robot can be reached.",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "use_fake_hardware",
            default_value="true",
            description="Start robot with fake hardware mirroring command to its states.",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "fake_sensor_commands",
            default_value="true",
            description="Enable fake command interfaces for sensors used for simple simulations. "
            "Used only if 'use_fake_hardware' parameter is true.",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "initial_joint_controller",
            default_value="scaled_joint_trajectory_controller",
            choices=JOINT_CONTROLLERS,
            description="Initially loaded robot controller.",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "activate_joint_controller",
            default_value="true",
            description="Activate loaded joint controller.",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "headless_mode",
            default_value="false",
            description="Enable headless mode for robot control.",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "launch_dashboard_client",
            default_value="true",
            description="Launch Dashboard Client? (ignored when use_fake_hardware is true)",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "controller_spawner_timeout",
            default_value="10",
            description="Timeout used when spawning controllers.",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "use_moveit",
            default_value="true",
            description="Whether to launch MoveIt related nodes.",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "launch_rviz",
            default_value="true",
            description="Launch RViz? Uses the MoveIt config if use_moveit is true, "
            "otherwise the plain robot view config from ur_control.",
        )
    )

    return LaunchDescription(declared_arguments + [OpaqueFunction(function=launch_setup)])
