from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, RegisterEventHandler
from launch.conditions import IfCondition, UnlessCondition
from launch.event_handlers import OnProcessExit
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue, ParameterFile # ParameterFileが必須

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
            "robot_ip",
            default_value="0.0.0.0",
            description="IP address by which the robot can be reached.",
        )
    )
    # コントローラ設定ファイル内で使われているため必須
    declared_arguments.append(
        DeclareLaunchArgument(
            "tf_prefix",
            default_value="",
            description="tf_prefix of the joint names.",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "rviz_config_file",
            default_value="display.rviz",
            description="Rviz configuration file.",
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
    robot_ip = LaunchConfiguration("robot_ip")
    tf_prefix = LaunchConfiguration("tf_prefix") # ★取得
    initial_joint_controller = LaunchConfiguration("initial_joint_controller")
    rviz_config_file = LaunchConfiguration("rviz_config_file")

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

    # URDF生成用ファイル
    description_package = FindPackageShare("ur_description")
    description_file = PathJoinSubstitution([description_package, "urdf", "ur.urdf.xacro"])
    
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
            "robot_ip:=", robot_ip,
            " ",
            "tf_prefix:=", tf_prefix, # ★URDF生成時にも渡す
            " ",
            "script_filename:=", script_filename, " ",
            "input_recipe_filename:=", input_recipe_filename, " ",
            "output_recipe_filename:=", output_recipe_filename, " ",
        ]
    )
    robot_description = {"robot_description": ParameterValue(robot_description_content, value_type=str)}

    # ★重要: 設定ファイル内の $(var ...) を展開するために ParameterFile でラップする
    controllers_file_param = ParameterFile(controllers_file, allow_substs=True)

    # --- 5. ノードの定義 ---

    # [A-1] Mock用: 標準の ros2_control_node
    control_node_mock = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[
            robot_description,
            update_rate_config_file,
            controllers_file_param, # ★修正: 生のパスではなくParameterFileオブジェクトを渡す
        ],
        output="screen",
        condition=IfCondition(use_fake_hardware),
    )

    # [A-2] 実機用: UR専用の ur_ros2_control_node
    control_node_real = Node(
        package="ur_robot_driver",
        executable="ur_ros2_control_node",
        parameters=[
            robot_description,
            update_rate_config_file,
            controllers_file_param, # ★修正
        ],
        output="screen",
        condition=UnlessCondition(use_fake_hardware),
    )

    # [A-3] 実機用: Dashboard Client
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

    # [C] RViz2
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", rviz_config_file],
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
            rviz_node,
            joint_state_broadcaster_spawner,
            delay_rviz_after_joint_state_broadcaster_spawner,
        ]
    )