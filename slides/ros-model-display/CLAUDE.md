# ゼロからのROS入門 - ロボットモデルの表示

このスライドは、ROSにおけるロボットの3Dモデル表示と可視化技術について学ぶための教材です。URDFファイルの活用とシミュレーション環境での表示方法を詳しく解説します。

## 対象者
- ROS中級者
- ロボットモデリングを学びたい方
- URDF/XACROを理解したい開発者
- RVizやGazeboを使いたい方

## スライド構成（スライド1-7）

**注意**: 黒背景テーマを使用

1. **タイトル・導入**
   - ゼロからのROS入門 - ロボットモデルの表示
2. **本スライドのゴール**
   - ロボットモデルをRviz上に表示できるようになる
3. **Rvizとは？**
   - ロボットのモデルやセンサ情報などを3次元で可視化するためのツール
   - デバッグや動作確認で使用
   - RVizなしでもROS自体は動作可能
4. **表示をするまでの全体像**
   - ①URDFでロボットモデルを書く
   - ②URDFを読み込ませて表示
5. **ステップ1：URDFの書き方（縦階層構造）**
   - 5.1 **そもそもロボットの構造（復習）** - image5を引用
   - 5.2 **ロボットモデル = ロボットアームの構造** - image6を引用
     - ジョイント（関節）：モーターが入って動く
     - リンク：ジョイントを繋ぐ、剛性が重要
     - エンドエフェクタ（手先効果器）：作業用、付け替え可能
   - 5.3 **URDF（Unified Robot Description Format）**
     - Joint：自由度、親リンクと子リンク
     - Link：Visual、Collision、Inertial
   - 5.4 **XACRO（XML Macros for Robots）** - image8を引用
     - URDFの効率化（マクロ機能追加）
     - 変数渡し、関数での繰り返し構造簡素化
   - 5.5 **エンドエフェクタを追加したい場合**
     - XACROのinclude機能活用
     - 実装例コード付き
6. **ステップ2：URDFの表示launchコード例（縦階層構造）**
   - launchファイルの実装例
   - 6.1 **URDFの表示デモ** - image8を引用
     - TFを見るとURDFで記述したjointとlinkが動いているのが見える
7. **RVizで表示を確認したTFとは何か？（縦階層構造）**
   - 7.1 **TF（Transformation）機能1：座標変換** - image9を引用
     - ROS標準搭載のシステム（実際はTF2を使用）
     - エンドエフェクタのベース座標系・ツール座標系計算
   - 7.2 **TF機能2：座標管理**
     - 座標をツリー構造で管理（開ループのみ、閉ループ不可）
     - 時系列座標データの管理
     - TF完全理解資料の紹介

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
├── index.html          # メインスライドファイル
├── media/              # 画像・動画ファイル
│   ├── image1.png     # タイトル背景
│   ├── image2.png     # （未使用）
│   ├── image3.png     # （未使用）
│   ├── image4.png     # 座標変換例（TFスライドで使用）
│   ├── image5.png     # ロボット構造復習（URDFスライドで使用）
│   ├── image6.png     # ロボットアーム構造図（URDFスライドで使用）
│   ├── image7.png     # （未使用）
│   ├── image8.png     # XACRO例・表示デモ（URDFスライドで使用）
│   └── image9.png     # （未使用）
└── CLAUDE.md          # このドキュメント
```

## シリーズ内での位置づけ

このスライドは「ゼロからのROS入門シリーズ」の中核部分で、ロボットの3D表現とROSでの扱い方を学びます。制御（ros-arm-control）やシミュレーション（ros-simulator-connection）の基礎となる重要な内容です。