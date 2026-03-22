from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    declared_arguments = [
        DeclareLaunchArgument(
            "description_package",
            default_value="ros_study_description",
            description="Package containing the robot description used by MoveIt.",
        ),
        DeclareLaunchArgument(
            "description_file",
            default_value="ur5e_with_ee_mock_components.xacro",
            description="Xacro file matching the already-running mock-components setup.",
        ),
        DeclareLaunchArgument(
            "launch_rviz",
            default_value="false",
            description="Whether MoveIt should start its own RViz instance.",
        ),
        DeclareLaunchArgument(
            "ur_type",
            default_value="ur5e",
            description="Type/series of used UR robot.",
        ),
        DeclareLaunchArgument(
            "tf_prefix",
            default_value="",
            description="tf_prefix of the joint names.",
        ),
    ]

    moveit_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([FindPackageShare("ur_moveit_config"), "launch", "ur_moveit.launch.py"])
        ),
        launch_arguments={
            "ur_type": LaunchConfiguration("ur_type"),
            "launch_rviz": LaunchConfiguration("launch_rviz"),
            "description_package": LaunchConfiguration("description_package"),
            "description_file": LaunchConfiguration("description_file"),
            "prefix": LaunchConfiguration("tf_prefix"),
        }.items(),
    )

    return LaunchDescription(declared_arguments + [moveit_launch])
