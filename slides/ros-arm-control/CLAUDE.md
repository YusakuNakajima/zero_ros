# ゼロからのROS入門 ~アーム位置制御とモーションプランニング~

このスライドは、ROSを使ったロボットアームの制御方法について学ぶ教材です。MoveItを活用した軌道計画と実際の制御実装について詳しく解説します。

## 対象者
- ROS中級者〜上級者
- ロボットアーム制御を実装したい開発者
- MoveItやJointTrajectoryControllerを学びたい方
- モーションプランニングに興味がある研究者・エンジニア

## スライド構成（階層構造）

### 導入部（水平スライド1-2）
1. **タイトル・導入**
   - 背景画像：MoveIt
2. **ロボット制御の書籍**
   - 2列レイアウト：左「イラストで学ぶロボット工学」(image4.png) / 右「実践ロボット制御」(image2.png)

### 前提知識編（水平スライド3-9）
3. **アーム制御の前提知識**
4. **ロボットアームの構造**
   - 2列レイアウト：左に画像(image13.png) / 右に説明文
5. **アーム制御は組合せ**
   - 制御方法×座標系×制御種類の表
6. **多くのロボットは位置/速度制御**
   - 画像配置：image2,5,8,12,15をバランス良く配置
7. **よく使うROSのアームコントローラ**
   - JointTrajectoryController、CartesianControllers
8. **ROSのアームコントローラの命名規則**
   - 図を削除、テキストのみ
9. **本編の内容**
   - MoveIt、JointTrajectoryController

### MoveItによるアーム制御編（水平スライド10 + 縦スライド）
10. **MoveItによるアーム制御** （メインスライド）
    - **縦スライド11**: MoveItで何ができるか
    - **縦スライド12**: MoveItのモーションプランニングの手順
    - **縦スライド13**: 手先の姿勢の表現（image13を30%サイズに縮小）
    - **縦スライド14**: 姿勢の表現 - オススメの実装
    - **縦スライド15**: 逆運動学の必要性
    - **縦スライド16**: 逆運動学の解き方（IKソルバー）
    - **縦スライド17**: MoveIt2で使えるIKソルバー
    - **縦スライド18**: Pythonで使えるIKソルバー
    - **縦スライド19**: MoveIt2で使えるパスプランニング
    - **縦スライド20**: サンプリングベースの手法（RRT）
    - **縦スライド21**: 最適化ベースの手法（CHOMP）
    - **縦スライド22**: 最適化ベースの手法（STOMP）

### JointTrajectoryControllerによるアーム制御編（水平スライド23 + 縦スライド）
23. **JointTrajectoryControllerによるアーム制御** （メインスライド）
    - **縦スライド24**: JTCでの実装の流れは5ステップ
    - **縦スライド25**: 目標姿勢の計算
    - **縦スライド26**: 軌跡・軌道生成
    - **縦スライド27**: 実行
    - **縦スライド28**: JTCの実装例

### 終了部
29. **終了**

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
- **pick_ik**: 高速で柔軟な数値解法
- **TRACK-IK**: Track-based Inverse Kinematics
- **IKFast**: 解析解ベースの高速ソルバー

### JointTrajectoryController

#### 実装フロー
1. **目標姿勢計算**: 逆運動学による関節角度計算
2. **軌跡生成**: 時間パラメータ付きの滑らかな軌道
3. **メッセージ送信**: trajectory_msgs/JointTrajectory
4. **実行監視**: アクションサーバーでの進捗確認
5. **結果処理**: 成功/失敗の判定

#### 軌道生成
- **補間方法**: 線形、3次スプライン、5次多項式
- **時間設定**: 速度・加速度制約の考慮
- **同期制御**: 複数関節の協調動作

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
group = moveit_commander.MoveGroupCommander("arm")
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

## 実践演習

### 基本演習
1. **MoveIt設定**: ロボットのMoveIt設定パッケージ作成
2. **簡単なモーション**: pick-and-place動作の実装
3. **軌道計画**: 障害物回避経路の生成
4. **IK確認**: 逆運動学の動作確認

### 応用演習
1. **カスタムプランナー**: 独自のプランニングアルゴリズム実装
2. **力制御**: CartesianControllersを使った力制御
3. **視覚フィードバック**: カメラ情報を使った制御
4. **マルチアーム**: 複数アームの協調制御

## パフォーマンス考慮

### プランニング最適化
- **プランナー選択**: 用途に応じたアルゴリズム選択
- **パラメータ調整**: プランニング時間と品質のトレードオフ
- **事前計算**: よく使う軌道の事前生成

### 実時間制御
- **制御周期**: ロボットに応じた適切な制御頻度
- **遅延対策**: 通信遅延とタイムスタンプ管理
- **エラーハンドリング**: 異常時の安全停止

## トラブルシューティング

### よくある問題
- **IK解なし**: 到達不可能な目標姿勢
- **プランニング失敗**: 障害物による経路閉塞
- **実行エラー**: ハードウェア制約の超過

### デバッグ方法
- **RVizでの可視化**: 軌道と障害物の確認
- **ログ解析**: MoveItのデバッグ出力確認
- **ステップ実行**: 段階的な動作確認

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
- [CartesianControllers](https://github.com/UniversalRobots/Universal_Robots_ROS_Driver)

### 推奨教材
- **MoveItチュートリアル**: 公式チュートリアル
- **実践ロボット制御**: 制御理論の詳細
- **ROSプログラミング**: 実装パターン集

## ファイル構成

```
ros-arm-control/
├── index.html          # メインスライドファイル
├── media/              # 画像・動画ファイル
│   ├── image1.jpg     # タイトル背景
│   ├── image4.png     # ロボット構造図
│   ├── image8.png     # コントローラ命名規則
│   └── ...
└── CLAUDE.md          # このドキュメント
```

## シリーズ内での位置づけ

このスライドは「ゼロからのROS入門シリーズ」の実践編で、ロボットモデル表示の知識を基に実際の制御実装を学びます。理論と実装のバランスを重視し、実用的なロボットアーム制御システムの構築方法を習得できます。