以下の指示通りにスライドを作ってください
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

1. 
2. 
3. 
4. 
5. a
   1. a
   2. a
   3. ros_control_fake_joint.svg.svgを全画面表示
   4. fake_jointを使うlaunchの例
   5. 対応関係、左に3枚目のsvg表示、右に4枚目のlaunchを表示、
   背景に色を付けて、
   以下は赤色の背景で
   	  <!-- Load URDF -->
  <param name="robot_description" command="$(find xacro)/xacro '$(arg model)'" />
  <node name="robot_state_publisher" pkg="robot_state_publisher" type="robot_state_publisher" />
 
    <!-- launch rviz -->
  <node name="rviz" pkg="rviz" type="rviz" respawn="false" args="-d $(arg rviz_config)" output="screen"/>
  以下は水色
	  <!-- Load controllers -->
  <rosparam file="$(arg controller_config_file)" command="load"/>
  <node name="ros_control_controller_spawner" pkg="controller_manager" type="spawner"
  args="$(arg controllers)" output="screen" respawn="false" />
 
    <!-- Launch moveit -->
  <include file="$(find ur5e_moveit_config)/launch/move_group.launch">
    <arg name="allow_trajectory_execution" default="true" />
    <arg name="fake_execution" value="false" />
  </include>
  以下は緑
   <!--Run Fake joint driver -->
  <node name="fake_joint_driver" pkg="fake_joint_driver" type="fake_joint_driver_node" />