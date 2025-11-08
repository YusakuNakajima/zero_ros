from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    declared_arguments = []

    # 1. ロボットモデルが入っているパッケージ名 (自作パッケージ)
    description_package_arg = DeclareLaunchArgument(
        "description_package",
        default_value="ros_study",
        description="Description package with robot URDF/XACRO files.",
    )
    declared_arguments.append(description_package_arg)

    # 2. URDF/XACROファイル名
    declared_arguments.append(
        DeclareLaunchArgument(
            "description_file",
            default_value="ur5e.urdf",
            description="URDF/XACRO description file with the robot.",
        )
    )
    
    # 3. xacroに渡すための一般的な必須引数を宣言
    declared_arguments.append(
        DeclareLaunchArgument(
            "name", 
            default_value="robot", 
            description="Robot name/prefix passed to xacro.",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "tf_prefix", 
            default_value='""', 
            description="TF prefix for the robot model.",
        )
    )

    # ★ 4. RViz設定ファイル名を追加
    declared_arguments.append(
        DeclareLaunchArgument(
            "rviz_config_file",
            default_value="display.rviz", # あなたの .rviz ファイル名に設定
            description="Rviz configuration file.",
        )
    )


    # LaunchConfigurationの初期化
    description_package = LaunchConfiguration("description_package")
    description_file = LaunchConfiguration("description_file")
    name = LaunchConfiguration("name")
    tf_prefix = LaunchConfiguration("tf_prefix")
    rviz_config_file_name = LaunchConfiguration("rviz_config_file")
    
    # URDF/XACROファイルのパスを構築
    robot_description_file = PathJoinSubstitution(
        [FindPackageShare(description_package), "urdf", description_file]
    )

    # RViz設定ファイルのパスを構築 (rvizフォルダにあると仮定)
    rviz_config_file = PathJoinSubstitution(
        [FindPackageShare(description_package), "rviz", rviz_config_file_name]
    )


    # XACROコマンドを実行してURDFを生成
    robot_description_content = Command(
        [
            PathJoinSubstitution([FindExecutable(name="xacro")]),
            " ",
            robot_description_file,
            " ",
            "name:=", name,
            " ",
            "tf_prefix:=", tf_prefix,
        ]
    )
    robot_description = {
        "robot_description": ParameterValue(value=robot_description_content, value_type=str)
    }

    # ノードの定義
    
    joint_state_publisher_node = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
    )
    
    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[robot_description],
    )
    
    # ★ RViz2ノードを修正: '-d' オプションで設定ファイルを渡す
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", rviz_config_file], # 設定ファイルパスを追加
    )

    nodes_to_start = [
        joint_state_publisher_node,
        robot_state_publisher_node,
        rviz_node,
    ]

    return LaunchDescription(declared_arguments + nodes_to_start)