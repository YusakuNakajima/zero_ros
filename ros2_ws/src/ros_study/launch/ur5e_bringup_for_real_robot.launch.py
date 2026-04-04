from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    declared_arguments = [
        DeclareLaunchArgument(
            "description_package",
            default_value="ros_study",
            description="Package containing the JTC-focused Xacro file.",
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

    bringup = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution(
                [FindPackageShare("ros_study"), "launch", "ur5e_bringup_with_mock_components.launch.py"]
            )
        ),
        launch_arguments={
            "description_package": LaunchConfiguration("description_package"),
            "description_file": "ur5e_with_ee_for_real_robot.xacro",
            "controllers_file": LaunchConfiguration("controllers_file"),
            "rviz_config_file": LaunchConfiguration("rviz_config_file"),
            "initial_joint_controller": LaunchConfiguration("initial_joint_controller"),
            "launch_moveit": LaunchConfiguration("launch_moveit"),
        }.items(),
    )

    return LaunchDescription(declared_arguments + [bringup])
