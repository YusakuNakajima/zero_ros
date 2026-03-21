from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, RegisterEventHandler, IncludeLaunchDescription
from launch.conditions import IfCondition, UnlessCondition
from launch.event_handlers import OnProcessExit
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue, ParameterFile

def generate_launch_description():
    declared_arguments = []

    # --- 1. 引数の宣言 ---
    declared_arguments.append(
        DeclareLaunchArgument(
            "ur_type",
            default_value="ur5e",
            description="Type/series of used UR robot.",
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
            "use_fake_sensor_commands",
            default_value="true",
            description="Use fake sensor commands if true.",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "robot_ip",
            default_value="0.0.0.0",
            description="IP address by which the robot can be reached.",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "tf_prefix",
            default_value="",
            description="tf_prefix of the joint names.",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "initial_joint_controller",
            default_value="scaled_joint_trajectory_controller", 
            description="Initially loaded robot controller.",
        )
    )

    # --- 2. 変数の取得 ---
    ur_type = LaunchConfiguration("ur_type")
    use_fake_hardware = LaunchConfiguration("use_fake_hardware")
    use_fake_sensor_commands = LaunchConfiguration("use_fake_sensor_commands")
    robot_ip = LaunchConfiguration("robot_ip")
    tf_prefix = LaunchConfiguration("tf_prefix")
    initial_joint_controller = LaunchConfiguration("initial_joint_controller")

    # --- 3. 設定ファイルのパス ---
    robot_driver_package = FindPackageShare("ur_robot_driver")
    
    # コントローラ設定ファイル
    controllers_file = PathJoinSubstitution(
        [robot_driver_package, "config", "ur_controllers.yaml"]
    )
    
    # 更新レートの設定ファイル
    update_rate_config_file = PathJoinSubstitution(
        [robot_driver_package, "config", "ur5e_update_rate.yaml"]
    )

    # URDF生成用ファイル (ros_study_description パッケージを使用)
    description_package_name = "ros_study_description"
    description_file_name = "ur5e_with_ee.xacro"
    
    description_package = FindPackageShare(description_package_name)
    description_file = PathJoinSubstitution([description_package, "urdf", description_file_name])
    
    # 実機接続用のスクリプトファイルなど
    script_filename = PathJoinSubstitution(
        [FindPackageShare("ur_client_library"), "resources", "external_control.urscript"]
    )
    input_recipe_filename = PathJoinSubstitution(
        [robot_driver_package, "resources", "rtde_input_recipe.txt"]
    )
    output_recipe_filename = PathJoinSubstitution(
        [robot_driver_package, "resources", "rtde_output_recipe.txt"]
    )

    # --- 4. Robot Description (URDF) の生成 ---
    robot_description_content = Command(
        [
            PathJoinSubstitution([FindExecutable(name="xacro")]),
            " ",
            description_file,
            " ",
            "name:=", ur_type,
            " ",
            "ur_type:=", ur_type,
            " ",
            "use_fake_hardware:=", use_fake_hardware,
            " ",
            "fake_sensor_commands:=", use_fake_sensor_commands, 
            " ",
            "robot_ip:=", robot_ip,
            " ",
            "tf_prefix:=", tf_prefix,
            " ",
            "script_filename:=", script_filename, " ",
            "input_recipe_filename:=", input_recipe_filename, " ",
            "output_recipe_filename:=", output_recipe_filename, " ",
        ]
    )
    robot_description = {"robot_description": ParameterValue(robot_description_content, value_type=str)}

    controllers_file_param = ParameterFile(controllers_file, allow_substs=True)

    # --- 5. ノードの定義 ---

    # [A-1] Mock用
    control_node_mock = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[
            robot_description,
            update_rate_config_file,
            controllers_file_param,
        ],
        output="screen",
        condition=IfCondition(use_fake_hardware),
    )

    # [A-2] 実機用
    control_node_real = Node(
        package="ur_robot_driver",
        executable="ur_ros2_control_node",
        parameters=[
            robot_description,
            update_rate_config_file,
            controllers_file_param,
        ],
        output="screen",
        condition=UnlessCondition(use_fake_hardware),
    )

    # [A-3] Dashboard Client
    dashboard_client_node = Node(
        package="ur_robot_driver",
        executable="dashboard_client",
        name="dashboard_client",
        output="screen",
        emulate_tty=True,
        parameters=[{"robot_ip": robot_ip}],
        condition=UnlessCondition(use_fake_hardware),
    )

    # [B] Robot State Publisher
    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="both",
        parameters=[robot_description],
    )

    # [C] MoveItの起動
    ur_moveit_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([FindPackageShare("ur_moveit_config"), "launch", "ur_moveit.launch.py"])
        ),
        launch_arguments={
            "ur_type": ur_type,
            "launch_rviz": "true",
            "description_package": description_package_name, # カスタムパッケージを指定
            "description_file": description_file_name,       # カスタムURDFファイルを指定
            "prefix": tf_prefix,                             # tf_prefixを渡す
            # 独自のMoveIt Configパッケージがある場合はここで "moveit_config_package" を指定
            # "use_sim_time": "false", 
        }.items(),
    )

    # [D] Spawner: Joint State Broadcaster
    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster", "--controller-manager", "/controller_manager"],
    )

    # [E] Spawner: Trajectory Controller
    initial_joint_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[initial_joint_controller, "--controller-manager", "/controller_manager"],
    )

    # 遅延実行の設定
    delay_rviz_after_joint_state_broadcaster_spawner = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=joint_state_broadcaster_spawner,
            on_exit=[initial_joint_controller_spawner],
        )
    )

    # --- 6. 実行リスト ---
    return LaunchDescription(
        declared_arguments
        + [
            control_node_mock,
            control_node_real,
            dashboard_client_node,
            robot_state_publisher_node,
            ur_moveit_launch,
            joint_state_broadcaster_spawner,
            delay_rviz_after_joint_state_broadcaster_spawner,
        ]
    )