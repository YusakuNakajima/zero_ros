import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    ros_study_cpp_share = get_package_share_directory('ros_study_cpp')

    planning_scene_loader = Node(
        package='ros_study_cpp',
        executable='load_planning_scene',
        name='load_planning_scene',
        output='screen',
        parameters=[
            os.path.join(
                ros_study_cpp_share,
                'config',
                'planning_scene_config.yaml',
            )
        ],
    )

    return LaunchDescription([planning_scene_loader])
