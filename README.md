# ゼロからのロボットアーム・ROS入門

[![ROS](https://img.shields.io/badge/ROS-Noetic-blue)](http://wiki.ros.org/noetic)
[![ROS2](https://img.shields.io/badge/ROS2-Humble-green)](https://docs.ros.org/en/humble/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

📋 このスライド資料は2025年7/28~7/31のロボット勉強会用に作成されました。現時点での無断転用・無断転載は禁止させていただきます。使いたい場合はご相談ください。

ロボット工学とROS (Robot Operating System) の基礎を学ぶためのReveal.js製教育スライド集です。
初心者から中級者まで、段階的にロボットアーム制御の知識とスキルを身につけることができます。

## 📚 スライド一覧

### 1. [ゼロからのロボットアーム入門](slides/robot-arm-basic-control/)
**対象**: 初心者〜中級者  
**内容**: ロボットアームの基礎知識、操作方法、選定ポイント  
**学習目標**: ティーチングペンダントとプログラミングでの基本操作をマスター

### 2. [ゼロからのROS入門](slides/ros-introduction/)
**対象**: ROS初学者〜中級者  
**内容**: ROSの基礎概念、学習リソース、効果的な学習方法  
**学習目標**: ROS開発の全体像と適切な学習戦略を理解

### 3. [ロボットモデルの表示](slides/ros-model-display/)
**対象**: ROS中級者  
**内容**: URDFとTFを使ったロボット可視化、RVizの活用  
**学習目標**: 3Dロボットモデルの作成と表示技術を習得

### 4. [アーム位置制御とモーションプランニング](slides/ros-arm-position-control/)
**対象**: ROS中級者〜上級者  
**内容**: MoveItとJointTrajectoryControllerによる制御実装  
**学習目標**: 高度なロボットアーム制御システムの構築

### 5. [シミュレータや実機との接続](slides/ros-simulator-connection/)
**対象**: ROS中級者〜上級者  
**内容**: ros_controlとBringupパッケージ、実機統合  
**学習目標**: シミュレータと実機を統合した開発環境の構築

## 🎯 推奨学習フロー

### 初学者向け
```
ロボットアーム入門 → ROS入門 → ロボットモデル表示
```

### ROS経験者向け
```
ロボットモデル表示 → シミュレータ接続 → アーム制御
```

### 上級者向け
```
必要な部分を選択的に学習
```

## 🚀 スライドの使い方

1. **ローカル環境で起動**

   **方法1: VSCode Live Server拡張機能（推奨）**
   ```bash
   # このリポジトリをクローン
   git clone https://github.com/your-username/zero_ros.git
   cd zero_ros
   ```
   1. VSCodeで `zero_ros` フォルダを開く
   2. [Live Server拡張機能](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer)をインストール
   3. `index.html` を右クリック → "Open with Live Server"
   4. ブラウザが自動で開いてスライドが表示されます

   **方法2: Pythonサーバー**
   ```bash
   # ローカルサーバーを起動
   python -m http.server 8000
   
   # ブラウザでアクセス
   open http://localhost:8000
   ```

2. **GitHub Pagesで閲覧**
   - [メインページ](https://YusakuNakajima.github.io/zero_ros/)
   - 各スライドに直接アクセス可能

## 📖 主要な学習内容

### 技術スタック
- **ロボット制御**: PTP/LIN/CIRC モーション、TCP制御
- **ROS基礎**: ノード、トピック、サービス、パッケージ
- **3Dモデリング**: URDF/XACRO、TF、RViz可視化
- **制御システム**: MoveIt、JointTrajectoryController
- **システム統合**: ros_control、Hardware Interface

### 実践スキル
- ティーチングペンダントによるロボット操作
- ROSパッケージの開発と運用
- 3Dロボットモデルの作成と可視化
- モーションプランニングと軌道制御
- シミュレータと実機の統合開発

## 🔧 技術仕様

### スライド仕様
- **フレームワーク**: Reveal.js
- **テーマ**: ホワイトテーマ（一部ブラック）
- **フォント**: Noto Sans JP（Google Fonts）
- **レスポンシブ**: モバイル対応
- **アニメーション**: 縦・横遷移のみ

### 開発環境
- **推奨ブラウザ**: Chrome, Firefox, Safari
- **ROS**: Noetic (Ubuntu 20.04) / Humble (Ubuntu 22.04)
- **シミュレータ**: Gazebo, RViz
- **言語**: Python, C++, XML (URDF/XACRO)

## 📝 参考資料

### 推奨書籍
- 「産業用ロボットTheビギニング」- ロボット基礎
- 「イラストで学ぶロボット工学」- 制御理論
- 「実践ロボット制御」- 高度な制御手法
- 「ROS 2とPythonで作って学ぶAIロボット入門」- ROS実践

### オンラインリソース
- [ROS公式チュートリアル](http://wiki.ros.org/ROS/Tutorials)
- [MoveItドキュメント](https://moveit.ros.org/)
- [Gazeboチュートリアル](http://gazebosim.org/tutorials)

### ライセンス
MIT License - 詳細は[LICENSE](LICENSE)ファイルを参照

## 📊 学習進捗の目安

| スライド | 所要時間 | 前提知識 | 達成目標 |
|---------|----------|----------|----------|
| ロボットアーム入門 | 2-3時間 | なし | 基本操作理解 |
| ROS入門 | 1-2時間 | なし | 学習戦略確立 |
| ロボットモデル表示 | 3-4時間 | ROS基礎 | 3D可視化スキル |
| アーム制御 | 4-6時間 | ROS中級 | 制御システム構築 |
| シミュレータ接続 | 3-5時間 | ROS中級 | 統合開発環境 |

---

**Made with ❤️ for Robotics Education**

このスライド集があなたのロボット工学・ROS学習の一助となれば幸いです。質問やフィードバックはお気軽にIssueでお知らせください。