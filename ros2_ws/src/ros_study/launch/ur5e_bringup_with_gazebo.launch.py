import os

from ament_index_python.packages import get_package_prefix
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, RegisterEventHandler, SetEnvironmentVariable
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    resource_paths = [
        os.path.join(get_package_prefix("ur_description"), "share"),
        os.path.join(get_package_prefix("ros_study"), "share"),
    ]
    existing_gz_resource_path = os.environ.get("GZ_SIM_RESOURCE_PATH", "")
    existing_ign_resource_path = os.environ.get("IGN_GAZEBO_RESOURCE_PATH", "")
    gz_resource_path = os.pathsep.join(
        [path for path in [existing_gz_resource_path, *resource_paths] if path]
    )
    ign_resource_path = os.pathsep.join(
        [path for path in [existing_ign_resource_path, *resource_paths] if path]
    )

    declared_arguments = [
        DeclareLaunchArgument(
            "description_package",
            default_value="ros_study",
            description="Package containing the Gazebo Xacro file.",
        ),
        DeclareLaunchArgument(
            "description_file",
            default_value="ur5e_with_ee_gazebo.xacro",
            description="Gazebo Xacro file to load.",
        ),
        DeclareLaunchArgument(
            "controllers_file",
            default_value=PathJoinSubstitution(
                [FindPackageShare("ros_study"), "config", "ur_joint_trajectory_controller.yaml"]
            ),
            description="Controller configuration file.",
        ),
        DeclareLaunchArgument(
            "rviz_config_file",
            default_value=PathJoinSubstitution(
                [FindPackageShare("ros_study"), "rviz", "ur5e.rviz"]
            ),
            description="RViz configuration file.",
        ),
        DeclareLaunchArgument(
            "world_sdf",
            default_value=PathJoinSubstitution(
                [FindPackageShare("ros_study"), "worlds", "obstacle_world.sdf"]
            ),
            description="Gazebo world SDF file to load.",
        ),
        DeclareLaunchArgument(
            "entity_name",
            default_value="ur5e",
            description="Name of the spawned Gazebo entity.",
        ),
        DeclareLaunchArgument(
            "spawn_z",
            default_value="0.1",
            description="Initial Z position used when spawning the robot.",
        ),
    ]

    description_package = LaunchConfiguration("description_package")
    description_file = LaunchConfiguration("description_file")
    controllers_file = LaunchConfiguration("controllers_file")
    rviz_config_file = LaunchConfiguration("rviz_config_file")
    world_sdf = LaunchConfiguration("world_sdf")
    entity_name = LaunchConfiguration("entity_name")
    spawn_z = LaunchConfiguration("spawn_z")

    robot_description_content = Command(
        [
            PathJoinSubstitution([FindExecutable(name="xacro")]),
            " ",
            PathJoinSubstitution([FindPackageShare(description_package), "urdf", description_file]),
            " ",
            "controllers_file:=",
            controllers_file,
        ]
    )
    robot_description = {
        "robot_description": ParameterValue(robot_description_content, value_type=str),
    }

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([FindPackageShare("ros_gz_sim"), "launch", "gz_sim.launch.py"])
        ),
        launch_arguments={"gz_args": ["-r ", world_sdf]}.items(),
    )

    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[robot_description, {"use_sim_time": True}],
    )

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", rviz_config_file],
        parameters=[{"use_sim_time": True}],
    )

    bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=["/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock"],
        output="screen",
    )

    spawn_entity = Node(
        package="ros_gz_sim",
        executable="create",
        arguments=[
            "-topic",
            "robot_description",
            "-name",
            entity_name,
            "-z",
            spawn_z,
        ],
        output="screen",
    )

    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "joint_state_broadcaster",
            "--controller-manager",
            "/controller_manager",
            "--controller-manager-timeout",
            "120",
        ],
        output="screen",
    )

    trajectory_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "scaled_joint_trajectory_controller",
            "--controller-manager",
            "/controller_manager",
            "--controller-manager-timeout",
            "120",
        ],
        output="screen",
    )

    delayed_joint_state_broadcaster_spawner = RegisterEventHandler(
        OnProcessExit(
            target_action=spawn_entity,
            on_exit=[joint_state_broadcaster_spawner],
        )
    )

    delayed_trajectory_spawner = RegisterEventHandler(
        OnProcessExit(
            target_action=joint_state_broadcaster_spawner,
            on_exit=[trajectory_controller_spawner],
        )
    )

    return LaunchDescription(
        declared_arguments
        + [
            SetEnvironmentVariable("GZ_SIM_RESOURCE_PATH", gz_resource_path),
            SetEnvironmentVariable("IGN_GAZEBO_RESOURCE_PATH", ign_resource_path),
            gazebo,
            robot_state_publisher_node,
            rviz_node,
            bridge,
            spawn_entity,
            delayed_joint_state_broadcaster_spawner,
            delayed_trajectory_spawner,
        ]
    )
