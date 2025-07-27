スライドを完全に作り直します、以下の指示通りにスライドを作ってください
cssはassets/common-styles.cssを参照してください
claude.mdをスライドの内容に合わて作成してください。


# 全体的な方針
- 背景は黒色で統一する。
- 全てのスライドからアニメーション効果を削除する。
- 背景画像を除き、レイアウトは原則として「左に画像やアプリ、右にテキスト」で統一する。iframeも同様。
- アプリを埋め込む場合は以下のようにする
```html
<p style="text-align: center; margin-bottom: 10px;">
                    <strong>→ <a href="interactive_app/app_name.html" target="_blank"
                            style="color: #3b82f6; text-decoration: underline;">全画面表示</a></strong>
                </p>
                <iframe data-src="interactive_app/app_name.html" width="100%" height="200px"
                    frameborder="0"></iframe>
```
# 具体的な変更点
番号はスライドのページ数を表しています
ネストした番号はスライドの縦方向へのネストを表しています
「」内はスライドタイトルを表しています
空白は修正なし
タイトル：ゼロからのROS入門シミュレータや実機との接続
バックグラウンド：gazebo.png
1. 本スライドの担当範囲
   - 本スライドではシミュレータ上でロボットを動かす方法を説明します。
2. ROSで使われるシミュレータの種類
   1. 動作確認：fake_joint(https://github.com/tork-a/fake_joint)
  ロボットと周りの環境との接触は考慮されませんが動作が軽いです
   2. 物理シミュレータ：Gazebo(https://gazebosim.org/home)
   -  ロボットと周りの環境との接触等を含めた物理シミュレータ
ロボットと周りの環境との接触も考慮します(計算重い、GPU必須)

1. fake_joint
   1. fake_jointはTORK-A(東京オープンソースロボティクス協会)が開発したROS1のパッケージで、Rviz上で直接ロボットの動きをシミュレーションできます。
      - 元々ROSにはない仕組みでしたが、ROS2ではMockComponentという名前で公式から同様の機能が提供されています。
   2. 使い方
   ```xml
      <launch>
  <arg name="model" default="$(find grinding_descriptions)/urdf/ur/ur5e.urdf"/>
   <arg name="controller_config_file" default="$(find grinding_robot_bringup)/config/ur5e_controllers_fake_joint.yaml" />
  <arg name="controllers" default="joint_state_controller scaled_pos_joint_traj_controller" />
    <arg name="rviz_config" default="$(find grinding_robot_bringup)/etc/display_for_grinding.rviz" />

    <!-- Load URDF -->
  <param name="robot_description" command="$(find xacro)/xacro '$(arg model)'" />
  <node name="robot_state_publisher" pkg="robot_state_publisher" type="robot_state_publisher" />
     
  <!-- Controllers config -->
  <rosparam file="$(arg controller_config_file)" command="load"/>

  <!-- Load controllers -->
  <node name="ros_control_controller_spawner" pkg="controller_manager" type="spawner"
    args="$(arg controllers)" output="screen" respawn="false" />

   <!--Run Fake joint driver -->
    <node name="fake_joint_driver" pkg="fake_joint_driver" type="fake_joint_driver_node" />

    <!-- Launch moveit -->
  <include file="$(find ur5e_moveit_config)/launch/move_group.launch">
    <arg name="allow_trajectory_execution" default="true" />
    <arg name="fake_execution" value="false" />
  </include>

  <!-- launch rviz -->
  <node name="rviz" pkg="rviz" type="rviz" respawn="false" args="-d $(arg rviz_config)" output="screen"/>
</launch>
      ```

1. gazebo
   - GazeboはROSの公式なシミュレータで、3D環境でロボットを動かすことができます。
   - GazeboはROSと密接に統合されており、センサデータやロボットの状態をリアルタイムで取得できます。