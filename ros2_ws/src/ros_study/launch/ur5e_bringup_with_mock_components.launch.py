from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, RegisterEventHandler
from launch.conditions import IfCondition
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    declared_arguments = [
        DeclareLaunchArgument(
            "description_package",
            default_value="ros_study",
            description="Package containing the mock-components Xacro file.",
        ),
        DeclareLaunchArgument(
            "description_file",
            default_value="ur5e_with_ee_mock_components.xacro",
            description="Mock-components Xacro file to load.",
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
            "initial_joint_controller",
            default_value="scaled_joint_trajectory_controller",
            description="Trajectory controller started after the joint state broadcaster.",
        ),
        DeclareLaunchArgument(
            "launch_moveit",
            default_value="false",
            description="Also start MoveIt on top of the mock-components bringup.",
        ),
    ]

    description_package = LaunchConfiguration("description_package")
    description_file = LaunchConfiguration("description_file")
    controllers_file = LaunchConfiguration("controllers_file")
    rviz_config_file = LaunchConfiguration("rviz_config_file")
    initial_joint_controller = LaunchConfiguration("initial_joint_controller")
    launch_moveit = LaunchConfiguration("launch_moveit")

    robot_description_content = Command(
        [
            PathJoinSubstitution([FindExecutable(name="xacro")]),
            " ",
            PathJoinSubstitution([FindPackageShare(description_package), "urdf", description_file]),
        ]
    )
    robot_description = {
        "robot_description": ParameterValue(robot_description_content, value_type=str),
    }

    control_node = Node(
        package="controller_manager",
        executable="ros2_control_node",
        output="screen",
        parameters=[robot_description, controllers_file],
    )

    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[robot_description],
    )

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", rviz_config_file],
    )

    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster", "--controller-manager", "/controller_manager"],
        output="screen",
    )

    trajectory_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[initial_joint_controller, "--controller-manager", "/controller_manager"],
        output="screen",
    )

    moveit_overlay = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution(
                [FindPackageShare("ros_study"), "launch", "ur5e_moveit_overlay.launch.py"]
            )
        ),
        launch_arguments={
            "description_package": description_package,
            "description_file": description_file,
            "launch_rviz": "false",
        }.items(),
        condition=IfCondition(launch_moveit),
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
            control_node,
            robot_state_publisher_node,
            rviz_node,
            joint_state_broadcaster_spawner,
            delayed_trajectory_spawner,
            moveit_overlay,
        ]
    )
