# ゼロからのROS入門 ~アーム位置制御とモーションプランニング~

このスライドは、ROSを使ったロボットアームの制御方法について学ぶ教材です。MoveItフレームワーク、JointTrajectoryController実装、waypointsの可視化について詳しく解説します。約50枚のスライドで構成され、4つの実装デモが含まれています。

## 対象者
- ROS中級者〜上級者
- ロボットアーム制御を実装したい開発者
- MoveItやJointTrajectoryControllerを学びたい方
- モーションプランニングアルゴリズムに興味がある研究者・エンジニア

## スライド構成（4つの主要セクション・約50スライド）

### 1. 導入部（水平スライド1-4）
1. **タイトル・導入**
   - 背景画像：MoveIt
2. **ロボット制御の書籍**
   - 縦配列：上「イラストで学ぶロボット工学」/ 下「実践ロボット制御」
3. **ROSを使う利点**
   - ROS生成モーションとメーカー提供モーションの比較
4. **アームの軌道制御概要**
   - 実装方法1: MoveIt（障害物回避あり）
   - 実装方法2: JointTrajectoryController（障害物回避なし）

### 2. 前提知識編（水平スライド5 + 縦スライド）
**スライド5: アーム制御の前提知識**（メインスライド）
- **縦スライド5-1**: アーム制御は組合せ（制御方法×座標系×制御種類の表）
- **縦スライド5-2**: よく使うROSの関節空間アームコントローラ
- **縦スライド5-3**: よく使うROSの直交空間アームコントローラ
- **縦スライド5-4**: 市販だと位置/速度制御が多い
- **縦スライド5-5**: トルク制御できるロボットもある
- **縦スライド5-13**: **MoveItCommanderによる実装**（コード表示）

### 3. MoveItによるアーム制御編（水平スライド6 + 縦スライド）
**スライド6: MoveItによるアーム制御**（メインスライド）
- **縦スライド6-1**: MoveItとは
- **縦スライド6-2**: MoveIt 3 Steps
- **縦スライド6-3**: ステップ1: 手先の姿勢の表現
- **縦スライド6-4**: 姿勢の表現 - オススメの実装
- **縦スライド6-5**: オイラー角による表現と課題
- **縦スライド6-6**: クォータニオンによる表現
- **縦スライド6-7**: クォータニオン補間の利点
- **縦スライド6-8**: クォータニオンを扱う方法
- **縦スライド6-9**: Step2: モーションプランニング
- **縦スライド6-10**: サンプリングベースの手法（RRT）
- **縦スライド6-11**: 最適化ベースの手法（CHOMP）
- **縦スライド6-12**: 最適化ベースの手法（STOMP）

### 4. JointTrajectoryControllerによるアーム制御編（水平スライド7 + 縦スライド）
**スライド7: JointTrajectoryControllerによるアーム制御の基本**（メインスライド）
- **縦スライド7-1**: JTCの実装4ステップ
- **縦スライド7-2**: step1: waypointsの計算
- **縦スライド7-3**: step2: 逆運動学（IK）
- **縦スライド7-4**: 逆運動学の解き方（IKソルバー）
- **縦スライド7-5**: MoveItのIKソルバー
- **縦スライド7-6**: Pythonで使えるIKソルバー
- **縦スライド7-7**: 軌跡・軌道生成
- **縦スライド7-8**: JointTrajectoryの送信方法
- **縦スライド7-9**: JointTrajectoryControllerのテスト方法
- **縦スライド7-10**: JTCの実装例
- **縦スライド7-12**: **JointTrajectoryControllerの実装**（コード表示）

### 5. JointTrajectoryControllerによるアームの速度制御編（水平スライド8 + 縦スライド）
**スライド8: JointTrajectoryControllerによるアームの速度・加速度制御**（メインスライド）
- **縦スライド8-1**: 手先の速度制御はなぜ必要か？
- **縦スライド8-2**: 軌道補間の方法
- **縦スライド8-3**: 線形補間
- **縦スライド8-4**: 3次スプライン補間
- **縦スライド8-5**: 5次スプライン補間
- **縦スライド8-6**: 補間方法の比較まとめ
- **縦スライド8-7**: 関節速度の計算方法
- **縦スライド8-8**: 逆ヤコビアンによる手先速度の計算
- **縦スライド8-9**: JointTrajectoryControllerにvelocityとaccelerationを追加
- **縦スライド8-10**: JointTrajectoryControllerでの設定例（ur_joint_trajectory_controller.yamlから読み込み）

### 6. waypointsの表示編（水平スライド9 + 縦スライド）
**スライド9: waypointsの表示**（メインスライド）
- **縦スライド9-1**: デバッグ用にwaypointsを表示したいことはよくある、方法を紹介
- **縦スライド9-2**: **VisualizationMarkerを使った表示**（画像表示）
- **縦スライド9-3**: **TFを使った表示**（画像表示）

## 実装デモファイル

### 1. moveit_demo.py
MoveItCommanderを使った基本的な実装例（スライド上に直接コード表示）
- 関節角度指定での移動
- 姿勢指定での移動
- カルテシアン軌道での移動
- moveit_executor.pyを参考にした教育用簡略版

### 2. jtc_demo.py
JointTrajectoryControllerを使った実装例（スライド上に直接コード表示）
- ActionClientでFollowJointTrajectoryを使用
- 軌道の作成（位置・速度・加速度設定）
- 複数waypoints対応
- JTC_executor.pyを参考にした教育用簡略版

### 3. ur_joint_trajectory_controller.yaml
JointTrajectoryControllerの設定ファイル（スライド上に直接YAML表示）
- UR5eロボット用の設定例
- 制約、ゲイン、パブリッシュレートの設定
- 実際のロボット制御で使用される設定パラメータ

### 4. visualization_marker.png / tf_visualization.png
waypointsの可視化例（画像表示）
- VisualizationMarkerによる表示例
- TFによる座標フレーム表示例
- RVizでの実際の表示画面

## 主要な学習ポイント

### 制御システム理解

#### アーム制御の基本
- **制御方法**: 位置制御、速度制御、トルク制御
- **座標系**: 関節座標系、直交座標系（デカルト座標系）
- **制御対象**: 位置、速度、力（トルク）

#### ROSコントローラ
- **JointTrajectoryController**: ROS標準のアームコントローラ
- **CartesianControllers**: 直交座標系での位置/力制御
- **命名規則**: `[制御タイプ]_controllers/[コントローラ名]`

### MoveItフレームワーク

#### 主要機能
- **モーションプランニング**: 衝突回避経路の自動生成
- **逆運動学**: 手先座標から関節角度への変換
- **衝突検出**: 障害物や自己干渉の検出

#### プランニング手法
- **サンプリングベース**: RRT、RRT*、PRM
- **最適化ベース**: CHOMP、STOMP
- **産業用**: 直線補間、円弧補間

#### IKソルバー
- **TRACK-IK**: Track-based Inverse Kinematics
- **IKFast**: 解析解ベースの高速ソルバー

### JointTrajectoryController

#### 実装フロー
1. **目標姿勢計算**: 逆運動学による関節角度計算
2. **軌跡生成**: 時間パラメータ付きの滑らかな軌道
3. **メッセージ送信**: trajectory_msgs/JointTrajectory
4. **実行監視**: アクションサーバーでの進捗確認

#### 軌道生成
- **補間方法**: 線形、3次スプライン、5次多項式
- **時間設定**: 速度・加速度制約の考慮
- **同期制御**: 複数関節の協調動作

### waypoints可視化

#### VisualizationMarker
- **形状**: 球形、矢印、線、立方体など
- **属性**: 色、サイズ、透明度
- **用途**: 位置の表示、軌道確認
- **表示**: RVizでの実際の可視化例を画像で確認

#### TF（Transform）
- **座標系管理**: ロボットや環境の座標関係
- **姿勢表示**: 位置+向きの可視化
- **時間同期**: 動的な座標変換
- **表示**: RVizでの座標フレーム表示例を画像で確認

## 技術的詳細

### 姿勢表現
```python
# RPYからクオータニオン変換
from tf.transformations import quaternion_from_euler
roll, pitch, yaw = 0.0, 0.0, 1.57  # ラジアン
quaternion = quaternion_from_euler(roll, pitch, yaw)
```

### MoveIt Python API
```python
import moveit_commander
group = moveit_commander.MoveGroupCommander("manipulator")
group.set_pose_target(target_pose)
plan = group.plan()
group.execute(plan)
```

### JointTrajectoryController
```python
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
traj = JointTrajectory()
traj.joint_names = ['joint1', 'joint2', 'joint3']
point = JointTrajectoryPoint()
point.positions = [0.1, 0.2, 0.3]
point.time_from_start = rospy.Duration(1.0)
traj.points.append(point)
```

### VisualizationMarker
```python
from visualization_msgs.msg import Marker
marker = Marker()
marker.type = Marker.SPHERE
marker.pose.position.x = 0.5
marker.color.r = 1.0
```

### YAML設定ファイル
```yaml
# ur_joint_trajectory_controller.yaml
pos_joint_traj_controller:
  type: position_controllers/JointTrajectoryController
  joints:
    - shoulder_pan_joint
    - shoulder_lift_joint
  constraints:
    goal_time: 0.6
    stopped_velocity_tolerance: 0.05
```

## 実践演習

### 基本演習
1. **MoveIt設定**: ロボットのMoveIt設定パッケージ作成
2. **簡単なモーション**: pick-and-place動作の実装
3. **軌道計画**: 障害物回避経路の生成
4. **waypoints可視化**: VisualizationMarkerとTFを使った表示

### 応用演習
1. **カスタムプランナー**: 独自のプランニングアルゴリズム実装
2. **複合制御**: MoveItとJTCの組み合わせ
3. **視覚フィードバック**: カメラ情報を使った制御
4. **リアルタイム表示**: 動的waypoints表示

## パフォーマンス考慮

### プランニング最適化
- **プランナー選択**: 用途に応じたアルゴリズム選択
- **パラメータ調整**: プランニング時間と品質のトレードオフ
- **事前計算**: よく使う軌道の事前生成

### 実時間制御
- **制御周期**: ロボットに応じた適切な制御頻度
- **遅延対策**: 通信遅延とタイムスタンプ管理
- **エラーハンドリング**: 異常時の安全停止

### 可視化最適化
- **マーカー数制限**: 過多な表示による性能低下防止
- **更新頻度調整**: 必要最小限の更新頻度
- **メモリ管理**: 不要なマーカーの削除

## トラブルシューティング

### よくある問題
- **IK解なし**: 到達不可能な目標姿勢
- **プランニング失敗**: 障害物による経路閉塞
- **実行エラー**: ハードウェア制約の超過
- **表示されない**: フレーム設定やトピック名の誤り

### デバッグ方法
- **RVizでの可視化**: 軌道と障害物の確認
- **ログ解析**: MoveItのデバッグ出力確認
- **ステップ実行**: 段階的な動作確認
- **トピック確認**: rostopicでのメッセージ確認

## 次のステップ

このスライド完了後の推奨学習順序：

1. **シミュレータ接続**: Gazebo連携での検証
2. **実機接続**: 実際のロボットアームとの統合
3. **高度な制御**: 力制御、視覚フィードバック制御
4. **システム統合**: 全体システムでの運用

## 関連リソース

### 公式ドキュメント
- [MoveIt Documentation](https://moveit.ros.org/)
- [JointTrajectoryController](http://wiki.ros.org/joint_trajectory_controller)
- [visualization_msgs](http://wiki.ros.org/visualization_msgs)
- [tf2](http://wiki.ros.org/tf2)

### 参考実装
- [powder_grinding moveit_executor.py](https://github.com/quantumbeam/powder_grinding/blob/develop/grinding_motion_routines/src/grinding_motion_routines/moveit_executor.py)
- [powder_grinding JTC_executor.py](https://github.com/quantumbeam/powder_grinding/blob/develop/grinding_motion_routines/src/grinding_motion_routines/JTC_executor.py)
- [powder_grinding marker_display.py](https://github.com/quantumbeam/powder_grinding/blob/develop/grinding_motion_routines/src/grinding_motion_routines/marker_display.py)
- [powder_grinding tf_publisher.py](https://github.com/quantumbeam/powder_grinding/blob/develop/grinding_motion_routines/src/grinding_motion_routines/tf_publisher.py)

### 推奨教材
- **MoveItチュートリアル**: 公式チュートリアル
- **実践ロボット制御**: 制御理論の詳細
- **ROSプログラミング**: 実装パターン集

## ファイル構成

```
ros-arm-position-control/
├── index.html              # メインスライドファイル
├── moveit_demo.py          # MoveItCommander実装デモ
├── jtc_demo.py            # JointTrajectoryController実装デモ
├── marker_display_demo.py  # DisplayMarker可視化デモ
├── tf_display_demo.py     # TF可視化デモ
├── media/                 # 画像・動画ファイル
│   ├── moveit.png        # タイトル背景
│   ├── robot_arm_structure.png
│   ├── moveit_algorithm.png
│   └── ...
└── CLAUDE.md             # このドキュメント
```

## レイアウト設計

### 全体方針
- **背景**: 黒色で統一
- **レイアウト**: 左に画像/アプリ、右にテキスト
- **アニメーション**: なし（シンプルな表示）
- **スタイル**: assets/common-styles.cssを使用

### 埋め込み形式
```html
<div class="slide-layout-image">
    <div class="image-section">
        <p style="text-align: center; margin-bottom: 10px;">
            <strong>→ <a href="demo_file.py" target="_blank"
                    style="color: #3b82f6; text-decoration: underline;">全画面表示</a></strong>
        </p>
        <iframe data-src="demo_file.py" width="100%" height="400px"
            frameborder="0" style="background: white;"></iframe>
    </div>
    <div class="text-section">
        <ul>
            <li>説明項目</li>
        </ul>
    </div>
</div>
```

## シリーズ内での位置づけ

このスライドは「ゼロからのROS入門シリーズ」の実践編で、ロボットモデル表示の知識を基に実際の制御実装を学びます。理論と実装のバランスを重視し、実用的なロボットアーム制御システムの構築方法を習得できます。特に、waypoints可視化による直感的なデバッグ手法も含まれており、実際の開発現場で役立つ実践的なスキルを身につけることができます。