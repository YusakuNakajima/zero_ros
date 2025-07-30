# ゼロからのROS入門 - ROSにおけるシミュレータ

このスライドは、ROSでシミュレータ上でロボットを動かす方法について学ぶ教材です。fake_jointやGazeboといったシミュレータの使い方について詳しく解説します。背景は黒色で統一し、アニメーション効果を削除した構成になっています。

## 対象者
- ROS初級者〜中級者  
- シミュレータを使ってロボットを動かしたい開発者
- fake_jointとGazeboの違いを理解したい方
- ロボットシミュレーションの基礎を学びたいエンジニア

## スライド構成

1. **タイトル・導入**
   - ゼロからのROS入門 - ROSにおけるシミュレータ
   - 背景画像：gazebo.png（黒色背景）

2. **本スライドの担当範囲**  
   - シミュレータ上でロボットを動かす方法の説明

3. **ROSで使われるシミュレータの種類**
   - 動作確認用と物理シミュレータの分類（左右2列レイアウト）
   1. **動作確認：fake_joint**
      - TORK-Aが開発したパッケージ
      - 軽量だが環境との接触は考慮されない
      - 位置制御のみ使える
   2. **物理シミュレータ：Gazebo**
      - 物理法則を含む本格的なシミュレータ
      - 計算重い、GPU必須

4. **fake_joint vs Gazebo 比較**
   - インタラクティブアプリの埋め込み（全画面表示リンク付き）

5. **fake_joint詳細**（縦方向ネスト構造）
   1. **fake_joint概要**
      - 使い方説明へのナビゲーション
   2. **fake_jointの詳細**
      - TORK-A開発のROS1パッケージの説明
      - ROS2ではMockComponentとして公式提供
   3. **ros_control構成図**（新規追加）
      - ros_control_fake_joint.svg.svgを全画面表示
   4. **fake_jointを使うlaunchの例**（新規追加）
      - 具体的なlaunchファイルコードの表示
   5. **対応関係**（新規追加） 
      - 左：SVG図、右：launchコード
      - コードの色分けハイライト
        - 赤色：URDF読み込み・RViz起動部分
        - 水色：コントローラ・MoveIt設定部分  
        - 緑色：fake_joint_driver起動部分

6. **gazebo詳細**
   - 左右レイアウト（左：画像、右：テキスト）
   - ROSの公式シミュレータ
   - センサデータの取得が可能

7. **終了**
   - シリーズ一覧への戻りリンク

## 設計方針

### 視覚的統一
- **背景色**: 全スライド黒色で統一
- **レイアウト**: 原則「左に画像やアプリ、右にテキスト」で統一
- **アニメーション**: 全削除（fragment効果、data-transition効果なし）

### 技術的構成
- **CSS**: ../../assets/common-styles.cssを参照
- **フォント**: Noto Sans JP使用
- **コードハイライト**: highlight.jsによるシンタックスハイライト
- **アプリ埋め込み**: iframeで全画面表示リンク併用

### 主要な更新内容
- スライド5を3つのサブスライドに分割
- ros_control構成図の全画面表示を追加
- launch例の単独スライド化
- SVGとコードの対応関係を色分けで視覚化

## ファイル構成

```
ros-simulator-connection/
├── index.html                                # メインスライドファイル（更新済み）
├── media/
│   ├── gazebo.png                           # タイトル背景
│   ├── fake_joint.png                       # fake_joint画面  
│   ├── ros_control_fake_joint.svg.svg       # ros_control構成図（新規使用）
│   └── CLAUDE.md                            # 旧説明ファイル
├── interactive_app/
│   └── fake_joint_vs_Gazebo.html            # 比較アプリ
└── CLAUDE.md                                # このドキュメント（新規）
```

## 技術実装詳細

### fake_jointのlaunchファイル構成
```xml
<launch>
  <!-- 引数定義 -->
  <arg name="model" default="$(find grinding_descriptions)/urdf/ur/ur5e.urdf"/>
  <arg name="controller_config_file" default="$(find grinding_robot_bringup)/config/ur5e_controllers_fake_joint.yaml" />
  <arg name="controllers" default="joint_state_controller scaled_pos_joint_traj_controller" />
  <arg name="rviz_config" default="$(find grinding_robot_bringup)/etc/display_for_grinding.rviz" />

  <!-- URDF読み込み（赤色ハイライト） -->
  <param name="robot_description" command="$(find xacro)/xacro '$(arg model)'" />
  <node name="robot_state_publisher" pkg="robot_state_publisher" type="robot_state_publisher" />
  
  <!-- RViz起動（赤色ハイライト） -->
  <node name="rviz" pkg="rviz" type="rviz" respawn="false" args="-d $(arg rviz_config)" output="screen"/>
  
  <!-- コントローラ設定（水色ハイライト） -->
  <rosparam file="$(arg controller_config_file)" command="load"/>
  <node name="ros_control_controller_spawner" pkg="controller_manager" type="spawner"
        args="$(arg controllers)" output="screen" respawn="false" />
  
  <!-- MoveIt起動（水色ハイライト） -->
  <include file="$(find ur5e_moveit_config)/launch/move_group.launch">
    <arg name="allow_trajectory_execution" default="true" />
    <arg name="fake_execution" value="false" />
  </include>
  
  <!-- fake_joint_driver起動（緑色ハイライト） -->
  <node name="fake_joint_driver" pkg="fake_joint_driver" type="fake_joint_driver_node" />
</launch>
```

### CSS設定
```css
/* common-styles.cssから継承 */
.slide-layout-image-code {
    display: flex;
    align-items: stretch; 
    justify-content: space-between;
    height: 100%;
    gap: 2%;
}

/* コードハイライト色 */
mark.code-highlight-red {
    background-color: rgba(220, 53, 69, 0.4);
}

mark.code-highlight-blue {
    background-color: rgba(0, 123, 255, 0.4); 
}

mark.code-highlight-green {
    background-color: rgba(40, 167, 69, 0.4);
}
```

## シリーズ内での位置づけ

このスライドは「ゼロからのROS入門シリーズ」のシミュレーション編として、理論学習から実践までをカバー。fake_jointによる軽量な動作確認からGazeboによる本格的な物理シミュレーションまで、開発段階に応じた適切なツール選択の指針を提供します。

## 学習効果の向上

### 視覚的理解の促進
- SVG構成図とlaunchコードの直接対応
- 色分けによるコンポーネント関係の明確化
- 段階的な情報提示（縦ネスト構造）

### 実践的スキルの習得
- 実際のlaunchファイル例の提示
- ros_controlアーキテクチャの理解
- シミュレータ選択基準の習得