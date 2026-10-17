# ゼロからのROS入門 ~力制御とコンプライアンス~

このスライドは、ROSを使ったロボットアームの力制御方法について学ぶ教材です。インピーダンス制御、アドミッタンス制御、ROS2での実装について詳しく解説します。約50枚のスライドで構成され、4つの実装デモが含まれています。

## 対象者
- ROS中級者〜上級者
- ロボットアーム力制御を実装したい開発者
- インピーダンス制御やアドミッタンス制御を学びたい方
- 接触作業や人間協調作業に興味がある研究者・エンジニア

## スライド構成（4つの主要セクション・約50スライド）

### 1. 導入部（水平スライド1-4）
1. **タイトル・導入**
   - 背景動画：media/hand_guiding.mp4（手で押すと戻る UR。章タイトルは同じ場面の静止画 media/hand_guiding.webp）
2. **力制御参考資料**
   - 縦配列：上「イラストで学ぶロボット工学」/ 下「実践ロボット制御」
3. **なぜ力制御が必要なのか？**
   - アプリ `interactive_app/position_control_limit.html`: 研磨で位置制御は位置ずれ・凹凸で力が急増/離れる、力制御は一定の力に倣う。位置制御/力制御のボタンで実行中に切り替え（初期は位置制御、グラフは方式ごとに色分け）
   - **受動 vs 能動コンプライアンス**（比較表）→ 縦: 用語の整理（コンプライアンス/受動/能動。能動は山野辺2017 図1にそって 間接的力制御＝インピーダンス（トルク制御ベース）・アドミッタンス（位置制御ベース）／直接的力制御＝ハイブリッド でグループ化）/ 用語の整理：ロボットの例（同じ箱構成（間接/直接のグループ付き）に写真。受動＝乳鉢粉砕ロボット media/robotic_powder_grinding.png（Nakajima et al., Digital Discovery 2024）、インピーダンス＝Franka、アドミッタンス＝UR、ハイブリッド＝Franka・UR 両方）/ 受動コンプライアンス制御 / 能動コンプライアンス制御
     - コラム2枚（本当に力"制御"が必要か？／受動で力を制御した事例）は力制御のハードウェアと制御の注意点の章（5章）の縦の末尾へ移動
4. **力制御の実装概要**
   - 実装方法1: インピーダンス制御（仮想スプリングダンパーシステム）
   - 実装方法2: アドミッタンス制御（力入力から位置出力）

### 2. 前提知識編（水平スライド5 + 縦スライド）
**スライド5: 力制御の前提知識**（メインスライド）
- **縦スライド5-1**: 力制御の種類と組み合わせ（制御方式×座標系×制御対象の表）
- **縦スライド5-2**: ROS2の力制御コントローラ（admittance_controller は Humble（Ubuntu 22）から標準）
- **縦スライド5-3**: コンプライアンス制御用のOSSコントローラ（FZI cartesian_controllers。compliance はハイブリッド的にも使える）
- **縦スライド5-3b**: インピーダンス制御用のOSSコントローラ（matthias-mayr/Cartesian-Impedance-Controller。トルク指令ロボット向け）
- **縦スライド5-13**: **アドミッタンスコントローラの実装**（コード表示）

### 2.5 力制御のハードウェアと制御の注意点（ROS2版: 水平スライド5。章タイトル「力制御のハードウェアと制御の注意点」）
- **縦スライド**: 力制御に必要なハードウェア（UR / Franka の小さな写真付き。A: 位置制御ロボット＋手先FTセンサ→アドミッタンスのみ / B: トルク制御ロボット→インピーダンスもアドミッタンスも。直交空間では F = J^-T τ で変換）
- **縦スライド（ROS2版）**: 力制御は制御周波数が効く（硬い物に当てたときの力：125 Hz は行き過ぎて跳ね、1 kHz はすっと落ち着くイメージ図。周期の間は前の指令のまま／安定に出せる硬さは周期におおよそ反比例 K < 2b/T, Colgate & Schenkel 1997）
- **縦スライド（ROS2版）**: 何 Hz あればいい？（目安）：対数軸に人（手の動き〜10 Hz、感じる力・振動〜1 kHz、パチニ小体 200〜300 Hz）・作業・ロボット（産業用ロボット 125 Hz / e-Series 500 Hz / Franka 1 kHz）を並べた図と表（位置 100〜125 Hz、やわらかい接触 125〜500 Hz、硬い物・研磨 500 Hz〜1 kHz、力触覚伝送 最低 1 kHz）。最後に注意書き「UR・Franka など研究用以外は外部指令周期が 125〜250 Hz が多い」
- **縦スライド（ROS2版）**: 硬い物ほど不安定 → 間にゲルを挟む（直接当てると力が振動／ゲル（ばね＋ダンパ）を挟むと落ち着く図。硬いほど高い制御周波数が必要、上げられないとき（アドミッタンス制御など）はゲル・ゴムで見かけの硬さを下げ振動を吸収）

### 3. インピーダンス制御編（ROS2版: 水平スライド6）
- **縦スライド6-1**: インピーダンス制御とは（図 media/impedance_msd.svg：目標 x_d と手先 M を K・D でつないだモデル）
- **縦スライド6-1b**: 間接的力制御の比較（アプリ interactive_app/force_control_demo.html：アームの先端をドラッグ、アドミッタンス/インピーダンス切替。旧アドミッタンス制御とはから移動）
- **縦スライド6-2**: インピーダンス制御の数式（M a + D(v − v_d) + K(x − x_d) = F。アドミッタンスと同じ式・同じレイアウトで、x=手先位置（入力）、F=出す力（出力）、計算の4ステップ τ = JᵀF まで）
- **縦スライド6-2b**: 手先の力 ⇔ 関節トルク：ヤコビアン（τ = Jᵀ F、F = J⁻ᵀ τ。アプリ interactive_app/jacobian_force.html：2リンクの手先に力をかけて必要な関節トルクを表示、特異姿勢の注意）
- **縦スライド6-3**: インピーダンスパラメータの調整（図 media/impedance_params.svg：K・D・M を変えたときの押して離した応答）
- **縦スライド6-7**: ROS2でのインピーダンス制御実装（構成図 media/ros2_impedance_arch.svg：アドミッタンスの構成図と同じ体裁。matthias-mayr/Cartesian-Impedance-Controller、State=関節の位置・速度・トルク、Command=effort、FTセンサ不要、~/reference_pose・~/set_cartesian_stiffness 等のトピック）
- **縦スライド6-8**: インピーダンス制御の設定（README の YAML 抜粋。K=stiffness、D=係数×2√K、M は無くロボット自身の重さ、実行中にトピックで変更可）
- **縦スライド6-9**: インピーダンス制御の実装の中身（tau_task + tau_nullspace + tau_ext と saturateTorqueRate のコード抜粋と数式との対応。重力補償はロボット側）

### 3.5 アドミッタンス制御編（ROS2版: 水平スライド7）
- **縦スライド7-1**: アドミッタンス制御とは（図 media/impedance_vs_admittance_flow.svg：インピーダンス＝位置を測って力を出す（薄く）／アドミッタンス＝力を測って位置指令を出す。入出力が逆）
- **縦スライド7-1a**: アドミッタンス制御を動かしてみる（6-1b と同じアプリ force_control_demo.html を再掲）
- **縦スライド7-1b**: インピーダンス vs アドミッタンス（アプリ impedance_vs_admittance.html。方式の比較の章から移動）
- **縦スライド7-2**: アドミッタンス制御の数式（M a_c + D(v_c − v_d) + K(x_c − x_d) = F。インピーダンスと同じ式で入出力が逆。F=測った外力、x_c=位置指令、x_d=目標、M/D/K=仮想パラメータ、計算の4ステップ）
- **縦スライド7-2b**: 数式の比較：インピーダンス vs アドミッタンス（同じ式で 測る＝緑／計算して出す＝橙 に色分け。測るもの・出すもの→行き先の表）
- **縦スライド7-5**: ROS2でのアドミッタンス制御実装（構成図 media/ros2_force_control_arch.drawio.svg: hardware_interface・State/Command Interface・admittance_controller・FTブロードキャスタ・トピック。draw.io で編集可）
- **縦スライド7-6**: アドミッタンス制御の設定
- **縦スライド7-7**: アドミッタンスコントローラの実装（コード表示）
- **縦スライド（ROS2版）章末コラム5枚**: コラム「アドミッタンス制御も色々」（ros2_controllers の admittance_controller と FZI の cartesian_compliance_controller を比較。どちらも K=500 N/m。①比較表：減衰 200 vs 約20 N·s/m、力入力の遅れ 約0.4 s vs 20 Hz フィルタ ②制御則の中身（M·a+D·v+K·x=F の実時間積分 / 軽い仮想ロボットの順動力学） ②b 実装の比較：仮想の重さをどこに置くか（普通のアドミッタンス＝手先の6自由度仮想質点→IK / FDCC＝ごく軽い仮想ロボット全体を関節空間で τ=JᵀF→順動力学→積分、IK不要。軽くする理由） ②c 違いのまとめ（表：重さの場所・関節角の求め方・特異点・冗長性・見かけの重さ ＋ 直感イメージ。Scherzinger et al. IROS 2017） ③10 N で押して離したときの応答グラフ（admittance は式どおり、FZI は手先1 kg・並進の概算。実機測定ではない）と、admittance を軽くする設定 damping_ratio 0.7〜1・filter_coefficient 0.05）

### 3.7 ハイブリッド位置/力制御（ROS2版のみ、水平スライド8。アドミッタンス章の後）
- 章タイトル（背景 media/hand_guiding.webp）
- ハイブリッド位置/力制御とは（インピーダンス/アドミッタンスと同じ構成。図 media/hybrid_overview.svg：研磨で Z＝力 10 N・X/Y＝軌道どおり）
- ハイブリッド位置/力制御の数式（u = (I − S)K_p(x_d − x) + S K_f(F_d − F)。位置＝緑・力＝赤、変数と4ステップ、比例のみの簡略形と注記）
- 仮想仕事の原理（τᵀδq = Fᵀδx から τ = JᵀF、外力の打ち消し、F = J⁻ᵀτ）
- 選択行列 S：方向ごとに位置か力か（0=位置・1=力、(I−S)位置＋S力、直交で非干渉、Raibert & Craig 1981）
- 位置と力をどう合成するか（ブロック図：xd/Fd → 誤差 → (I−S)/S → 位置/力制御則 → 和 u → 「指令に変換（次のスライド）」 → ロボット、順運動学と FTセンサのフィードバック。合成の話だけ：u = (I−S)u_pos + S u_frc、選ばれない方向の誤差は使わない）
- トルク制御でも位置制御でも実装できる（トルク制御（Franka）：u＝手先の力 → τ = Jᵀu。位置制御（UR）：u＝手先の速度 → 速度指令 関節速度 = J⁻¹u（実際はこちらが多い、制御性のため）または積分→IK→位置指令。例 UR force_mode、cambel/ur3 hybrid_controller.py）

### 3.75 方式の比較（ROS2版のみ、水平スライド9。ハイブリッド章の後。旧3章から移動）
- 章タイトル（背景 hand_guiding.webp）
- 能動コンプライアンス3方式の比較表 / 3方式比較アプリ（three_methods_compare.html：3リンク平面アームで研磨。押し付け力と横ずれのプロット、「横から押す」外乱、×10 拡大窓）

### 3.8 活用事例：フリードライブ（ROS2版のみ、水平スライド10 + 縦スライド）
- **縦スライド8-1**: 活用事例：フリードライブ（手で掴んで動かすモード、中身は多くがアドミッタンス制御）
- **縦スライド8-2**: フリードライブの実装方法（Franka: 関節トルクセンサ＋重力補償のインピーダンス型 / UR: FTセンサ・関節電流→速度指令のアドミッタンス型。内部実装は非公開で制御方式からの推定と明記）
- **縦スライド8-3**: フリードライブと接触作業の制御的な違い（同じ式でばね K の有無が違い。K=0: その場に止まる、K>0: 目標に戻る。重さ=M、軸ロック=selected_axes で軸を計算から外す）

### 3.9 コラム：位置精度と力制御は両立しにくい（ROS2版のみ、水平スライド11 + 縦スライド。フリードライブの後）
- 章タイトル（コラム表記、背景 media/hand_guiding.webp）
- 位置が得意か、力が得意か（位置精度×力制御のしやすさの図に 産業用（media/denso_industrial_robot.webp）・UR・Franka・CRANE-X7（イラスト。Commons に写真なし）を配置。配置はイメージ）
- 繰り返し精度で比べる（産業用 ±0.02 mm 前後＝小型機の代表値、UR5e ±0.03 mm、Franka FR3 ±0.1 mm（いずれも ISO 9283 データシート）、CRANE-X7 公称値なし。産業用・UR は硬い物との接触が苦手）
- なぜ？① 関節の剛性（トルクセンサはたわみで力を測る → 剛性・位置精度が下がる図）
- なぜ？② ギア比と摩擦（高減速＝押されても動かない、低減速（QDD・DD）＝外力で位置がずれる図）
- どう選ぶ？（作業×向くロボット×足りない側の補い方の表）

> ※ 以下の 4〜6（旧「スライド7〜9」）は現在の index_ros1.html / index_ros2.html には無い（旧構成の記録）。ROS2版の現在の8章はハイブリッド、9章は方式の比較、10章はフリードライブ。ROS1版の章構成は旧来のまま（6章にインピーダンス/アドミッタンスをまとめている）。

### 4. 力制御システムの実装編（水平スライド7 + 縦スライド）
**スライド7: 力制御システムの実装基本**（メインスライド）
- **縦スライド7-1**: 力制御実装4ステップ
- **縦スライド7-2**: step1: 力/トルクセンサーのセットアップ
- **縦スライド7-3**: step2: インピーダンス/アドミッタンスパラメータ設定
- **縦スライド7-4**: step3: 安全性チェックと力制限設定
- **縦スライド7-5**: step4: 実行とモニタリング
- **縦スライド7-6**: 力制御コントローラの種類
- **縦スライド7-7**: センサーキャリブレーション
- **縦スライド7-8**: 安全機能の実装
- **縦スライド7-9**: 力制御のデバッグ方法
- **縦スライド7-10**: 力制御の実装例
- **縦スライド7-12**: **アドミッタンス制御の実装**（コード表示）

### 5. 高度な力制御技術編（水平スライド8 + 縦スライド）
**スライド8: 高度な力制御技術**（メインスライド）
- **縦スライド8-1**: 複合力制御はなぜ必要か？
- **縦スライド8-2**: ハイブリッド位置/力制御
- **縦スライド8-3**: 適応インピーダンス制御
- **縦スライド8-4**: 外力推定技術
- **縦スライド8-5**: 接触検出アルゴリズム
- **縦スライド8-6**: 力制御手法の比較まとめ
- **縦スライド8-7**: 安全性確保の方法
- **縦スライド8-8**: 力制御の応用例
- **縦スライド8-9**: パラメータチューニング方法
- **縦スライド8-10**: 力制御設定例（force_control_config.yamlから読み込み）

### 6. 力制御のデバッグと可視化編（水平スライド8 + 縦スライド）
**スライド9: 力制御のデバッグと可視化**（メインスライド）
- **縦スライド8-1**: 力制御のデバッグ用可視化が重要な理由
- **縦スライド8-2**: **VisualizationMarkerを使った力ベクトル表示**（画像表示）
- **縦スライド8-3**: **TFを使ったコンプライアンス表示**（画像表示）

## 実装デモファイル

### 1. admittance_demo.py
ROS2 Admittance Controllerを使った基本的な実装例（スライド上に直接コード表示）
- 力/トルクセンサーデータの取得
- アドミッタンス制御の実装
- 安全性チェックと緊急停止機能
- 実用的な力制御アプリケーション例

### 2. impedance_demo.py
インピーダンス制御を使った実装例（スライド上に直接コード表示）
- 仮想スプリングダンパーシステムの実装
- 位置誤差からの力計算
- パラメータ調整機能
- 接触作業での実装例

### 3. force_control_config.yaml
力制御コントローラの設定ファイル（スライド上に直接YAML表示）
- Admittance Controllerの設定例
- 力/トルクセンサーの設定
- 安全制限値とパラメータ
- 実際の力制御システムで使用される設定

### 4. force_visualization.png / compliance_visualization.png
力制御の可視化例（画像表示）
- 力ベクトルのVisualizationMarker表示例
- コンプライアンス動作のTF表示例
- RVizでの実際の力制御デバッグ画面

## 主要な学習ポイント

### 力制御システム理解

#### 力制御の基本
- **制御方式**: インピーダンス制御、アドミッタンス制御、ハイブリッド制御
- **座標系**: 直交座標系（デカルト座標系）での力制御
- **制御対象**: 力、トルク、コンプライアンス

#### ROS2力制御コントローラ
- **AdmittanceController**: ROS2標準の力制御コントローラ
- **CartesianForceControllers**: 直交座標系での力制御
- **命名規則**: `admittance_controller`, `cartesian_force_controller`

### インピーダンス制御理論

#### 主要概念
- **仮想慣性**: Mass行列による動的応答の制御
- **仮想粘性**: Damping行列による振動抑制
- **仮想弾性**: Stiffness行列による復元力

#### 制御手法
- **インピーダンス制御**: 位置入力から力出力（F = M*a + D*v + K*x）
- **アドミッタンス制御**: 力入力から位置出力（a = M^-1*(F - D*v - K*x)）
- **ハイブリッド制御**: 方向別の位置/力制御切り替え

#### センサー技術
- **6軸力センサー**: 手先での力/トルク検出
- **関節トルクセンサー**: 各関節でのトルク測定

### 力制御システム

#### 実装フロー
1. **センサー設定**: 力/トルクセンサーのキャリブレーション
2. **パラメータ設定**: インピーダンス/アドミッタンスパラメータ
3. **安全制限**: 力制限値と緊急停止機能
4. **実行監視**: 力フィードバックとモニタリング

#### 制御計算
- **力測定**: センサーデータの取得と処理
- **制御則**: インピーダンス/アドミッタンス演算
- **安全監視**: 異常検出と保護機能

### 力制御可視化

#### 力ベクトル表示
- **形状**: 矢印、円錐、球形など
- **属性**: 力の大きさに応じた色、サイズ
- **用途**: 接触力の表示、力分布確認
- **表示**: RVizでの実際の力制御可視化例を画像で確認

#### コンプライアンス表示
- **座標系管理**: 力制御フレームの座標関係
- **変形表示**: コンプライアンス動作の可視化
- **時間同期**: 動的な力応答変化
- **表示**: RVizでのコンプライアンス表示例を画像で確認

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