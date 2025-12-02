# ゼロからのROS入門 - ロボットモデルの表示

このスライドは、ROSにおけるロボットの3Dモデル表示と可視化技術について学ぶための教材です。URDF/XACROによるロボットモデリング、TFシステム、RVizでの可視化について詳しく解説します。約25枚のスライドで構成され、2つのインタラクティブなアプリケーションが含まれています。

## 対象者
- ROS中級者
- ロボットモデリングを学びたい方
- URDF/XACROを理解したい開発者
- RVizやTFシステムを使いたい方

## スライド構成（スライド1-27）

**注意**: 黒背景テーマを使用、アニメーション効果なし、左画像・右テキストレイアウト

1. **タイトル・導入** - joint_state_publisher_on_rviz.pngを背景に使用
   - ゼロからのROS入門 - ロボットモデルの表示
2. **本スライドのゴール**
   - ロボットモデルをRviz上に表示できるようになる
3. **ロボットモデルとは？** - arm_and_end_effector.pngを使用（左右レイアウト）
   - メーカーからコードが提供されている
   - ロボットモデルがすでに表示されている場合はとばしてok
4. **Rvizとは？** - robot_on_rviz.pngを使用（左右レイアウト）
   - ロボットのモデルやセンサ情報などを3次元で可視化するためのツール
   - デバッグや動作確認で使用
   - あくまで可視化ツールなので、これがなくてもロボットの動作は可能
5. **ロボットモデルを表示するまでの流れ**
   - ステップ1：URDFでロボットモデルを書く
   - ステップ2：URDFを読み込ませて表示
6. **ステップ1：URDFの書き方（縦階層構造）**
   - 6.1 **そもそもロボットの構造（復習）** - robot_structure.pngを使用（左右レイアウト）
   - 6.2 **ロボットモデル = ロボットアームの構造** - arm_and_end_effector.pngを使用（左右レイアウト）
     - ジョイント（関節）：モーターが入って動く
     - リンク：ジョイントを繋ぐ、剛性が重要
     - エンドエフェクタ（手先効果器）：作業用、付け替え可能
   - 6.3 **URDF（Unified Robot Description Format）**
     - Joint：自由度、親リンクと子リンク
     - Link：Visual、Collision、Inertial
   - 6.4 **XACRO（XML Macros for Robots）** - xacro_example.pngを使用（左右レイアウト）
     - URDFの効率化（マクロ機能追加）
     - 変数渡し、関数での繰り返し構造簡素化
   - 6.5 **エンドエフェクタを追加したい場合**
     - XACROのinclude機能活用
     - 実装例コード付き
7. **ステップ2：URDFの表示launchコード例（縦階層構造）**
   - launchファイルの実装例
   - 7.1 **URDFの表示デモ** - joint_state_publisher_on_rviz.pngを使用（左右レイアウト）
     - このデモの裏で動いているのがTF(座標変換)です。次のセクションで詳しく見ていきましょう。
8. **TF：モデルを「動かす」ための座標情報（縦階層構造）**
   - 8.1 **なぜTFが必要？**
     - URDFだけでは「形状」と「関節がどう繋がっているか」しか分かりません。
     - 「各関節が何度曲がった結果、手先がどこにあるか」という**リアルタイムの位置・姿勢情報**、それがTFです。
     - RvizはURDF（形）とTF（位置）を組み合わせて初めてモデルを表示できます。
   - 8.2 **TFの役割1：座標変換 (ツリー構造)** - tf_viewer.pngを使用（左右レイアウト）
     - TF (Transform) は、ロボットの各パーツ（Link）の相対的な位置関係を**ツリー構造**で管理します。
     - **`robot_state_publisher`ノードが、URDFを読み込み、このTFツリーを計算して配信する張本人です。**
   - 8.3 **モデル表示のデータの流れ** - joint_states_workflow.pngを使用
     - 1. **`joint_state_publisher_gui`**: スライダーを動かすと、各関節の角度 (`/joint_states`) を配信します。
     - 2. **`robot_state_publisher`**: `/joint_states` と URDF (`/robot_description`) を購読します。
     - 3.  **`robot_state_publisher`**: 関節角度とリンク長から順運動学を計算し、結果を座標変換情報 (`/tf`) として配信します。
     - 4. **`Rviz`**: `/tf` を元に、URDFで定義されたモデルを動かします。
   - 8.4 **Rvizでの重要設定：Fixed Frame**
     - Rvizでモデルを表示するには、「どのリンクを座標の基準（根っこ）にするか」を指定する必要があります。
     - これが **Fixed Frame** 設定です。通常は `base_link` や `world` を指定します。
     - これが正しくないと、モデルが表示されない・エラーが出る原因No.1です。
   - 8.5 **TFの役割2：座標管理（時間）**
     - TFは「いつの時点」の座標かというタイムスタンプ情報も管理しています。
     - これは複数のセンサやPCが連携する複雑なシステムで重要になります。
     - **今回のデモではあまり気にする必要はありません。**（詳細は `ros-arm-position-control` スライドで解説）
9. **余談：ロボットモデルの数式表現（縦階層構造）**
   - ロボットの構造を行列で表現する方法としてDHパラメータがあります
   - URDFで読み込んだロボットの制御の裏ではDHパラメータを使って計算しています
   - 9.1 **DHパラメータとは？** - dh_parameter.htmlのインタラクティブアプリを使用（左右レイアウト）
     - ロボットの関節とリンクの相対的な位置関係を表すためのパラメータです
     - たった4つのパラメータでロボットの構造を表現でき、行列を使ってロボットの運動学を効率的に計算できます
     - 実際にはDHパラメータを改良した修正DHパラメータが使われています

## 主要な学習ポイント

### 技術概念

#### TF（Transformation）システム
- **座標変換**: 複数の座標系間での位置・姿勢変換
- **座標管理**: ツリー構造での座標系管理
- **時系列管理**: 座標データの時間整合性確保

#### ロボットモデリング
- **URDF**: XMLベースのロボット記述フォーマット
- **XACRO**: URDFの拡張（マクロ、変数、関数）
- **構造要素**: Joint（関節）、Link（リンク）、エンドエフェクタ
- **DHパラメータ**: ロボットの運動学を数式で表現する方法

#### 可視化ツール
- **RViz**: ROSの標準3D可視化ツール
- **RQT**: GUIベースのROSツール群

### 実装スキル

#### URDF記述
```xml
<robot name="sample_robot">
  <link name="base_link"/>
  <joint name="joint1" type="revolute">
    <parent link="base_link"/>
    <child link="link1"/>
  </joint>
  <link name="link1">
    <visual>...</visual>
    <collision>...</collision>
    <inertial>...</inertial>
  </link>
</robot>
```

#### XACRO活用
```xml
<xacro:include filename="$(find package)/urdf/base.xacro"/>
<xacro:macro name="arm_joint" params="name parent child">
  <joint name="${name}" type="revolute">
    <parent link="${parent}"/>
    <child link="${child}"/>
  </joint>
</xacro:macro>
```

#### Launchファイル
```xml
<launch>
  <arg name="model" default="$(find grinding_descriptions)/urdf/ur/ur5e.urdf"/>
  <param name="robot_description" command="$(find xacro)/xacro '$(arg model)'" />
  <node name="joint_state_publisher_gui" pkg="joint_state_publisher_gui" type="joint_state_publisher_gui" />
  <node name="robot_state_publisher" pkg="robot_state_publisher" type="robot_state_publisher" />
</launch>
```

## 重要なコンポーネント

### ROSノード
- **robot_state_publisher**: TFの配信
- **joint_state_publisher**: 関節状態の配信
- **joint_state_publisher_gui**: GUI付き関節状態配信

### ROSトピック
- **/robot_description**: URDFデータ
- **/joint_states**: 関節状態
- **/tf**: 座標変換情報

### ツール
- **RViz**: 3D可視化
- **RQT Node Graph**: ノード構成確認
- **RQT TF Tree**: TF構造確認

## 実践演習

### 基本演習
1. **URDFファイル作成**: 簡単なロボットモデルの記述
2. **XACROでの効率化**: マクロを使った記述の簡素化
3. **RVizでの表示**: 作成したモデルの可視化
4. **TF確認**: 座標変換の動作確認

### 応用演習
1. **エンドエフェクタ追加**: 既存モデルへのツール追加
2. **センサ統合**: カメラやLiDARの追加
3. **物理パラメータ設定**: 慣性・質量の適切な設定

## トラブルシューティング

### よくある問題
- **TFエラー**: 親子関係の循環参照
- **表示されない**: パッケージパスの設定ミス
- **動作しない**: joint_stateとURDFの不整合

### デバッグ方法
- **rosrun tf view_frames**: TF構造の可視化
- **rostopic echo /tf**: TF情報の確認
- **rqt_graph**: ノード接続の確認

## 次のステップ

このスライド完了後の推奨学習順序：

1. **ROSアーム制御**: MoveItでの動作計画
2. **シミュレータ接続**: Gazeboでの物理シミュレーション
3. **センサ統合**: カメラ・LiDARの統合
4. **実機接続**: 実際のロボットとの連携

## 関連リソース

### 公式ドキュメント
- [URDF Specification](http://wiki.ros.org/urdf)
- [XACRO Documentation](http://wiki.ros.org/xacro)
- [TF2 Tutorials](http://wiki.ros.org/tf2/Tutorials)

### 推奨教材
- **TF完全理解**: TFシステムの詳細解説
- **RVizチュートリアル**: 可視化ツールの使い方
- **URDFワークショップ**: 実践的なモデリング演習

## ファイル構成

```
ros-model-display/
├── index.html                          # メインスライドファイル（左右レイアウト対応）
├── media/                              # 画像・動画ファイル
│   ├── joint_state_publisher_on_rviz.png  # タイトル背景・表示デモ（スライド1,7.1で使用）
│   ├── arm_and_end_effector.png        # ロボットモデル説明（スライド3,6.2で使用）
│   ├── robot_on_rviz.png               # Rviz画面（スライド4で使用）
│   ├── robot_structure.png             # ロボット構造復習（スライド6.1で使用）
│   ├── xacro_example.png                # XACRO例（スライド6.4で使用）
│   ├── tf_viewer.png                   # TF座標変換例（スライド8.1で使用）
│   ├── Rviz_logo.png                   # （未使用）
│   ├── joint_states_workflow.png       # データフロー説明（スライド8.3で使用）
│   ├── pestle_tip.png                  # （未使用）
│   └── spatula_tip.png                 # （未使用）
└── CLAUDE.md                           # このドキュメント
```

## シリーズ内での位置づけ

このスライドは「ゼロからのROS入門シリーズ」の中核部分で、ロボットの3D表現とROSでの扱い方を学びます。制御（ros-arm-position-control）やシミュレーション（ros-simulator-connection）の基礎となる重要な内容です。