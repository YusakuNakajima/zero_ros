# 🤖 ゼロからのロボット入門シリーズ

## 🌐 オンラインで今すぐ学習開始！

**📖 GitHub Pages で直接アクセス**

🔗 **[https://yusakunakajima.github.io/zero_ros/](https://yusakunakajima.github.io/zero_ros/)**

- ✅ ブラウザですぐにアクセス可能
- ✅ ローカル環境設定不要
- ✅ モバイル・タブレット対応
- ✅ 全スライドを順次学習可能

**大阪大学 中島優作**

ロボティクス分野の基礎から応用まで、実践的な内容を学べるスライド集です。

📋 適切な表示を行い、非営利目的での利用に限り、改変せずにそのままの形での再配布が可能です。

## 📚 スライド一覧

### 0. [📖 RevealJSスライドの使い方](slides/revealjs-usage-guide/)
**対象**: 全ユーザー  
**内容**: RevealJSの基本操作方法とナビゲーション  
**学習目標**: スライドを効果的に使いこなす方法を習得

### 1. [⚙️ ロボットアーム入門 - ハードウェアインテグレーション](slides/robot-arm-hardware-integration/)
**対象**: 初心者〜中級者  
**内容**: ロボットアームのシステム統合方法。LAN接続・ティーチングペンダント・グリッパ配線・RS485通信規格  
**学習目標**: ロボットを動かす前段階で必要なハードウェア構築を習得

### 2. [🦾 ロボットアーム入門 - ロボット操作の基本](slides/robot-arm-basic-control/)
**対象**: 初心者〜中級者  
**内容**: ロボットアーム操作の基礎から選定まで。ティーチングペンダント・プログラミング・TCP・モーション種類・シミュレーション  
**学習目標**: ティーチングペンダントとプログラミングでの基本操作をマスター

### 3. [🔧 ゼロからのROS入門](slides/ros-introduction/)
**対象**: 初学者〜中級者  
**内容**: ROSの基礎概念とロボットアーム制御入門。学習戦略・推奨教材・ROS1とROS2の違い  
**学習目標**: ROS開発の全体像と適切な学習戦略を理解

### 4. [🤖 ゼロからのROS入門 - ロボットモデルの表示](slides/ros-model-display/)
**対象**: 中級者  
**内容**: ROSでのロボット3Dモデル表示技術。URDF・XACRO記述方法・RViz可視化・TF座標変換システム  
**学習目標**: 3Dロボットモデルの作成と表示技術を習得

### 5. [🎮 ゼロからのROS入門 - アーム位置制御とモーションプランニング](slides/ros-arm-position-control/)
**対象**: 中級者〜上級者  
**内容**: ROSアーム制御の実践技術。MoveItによるモーションプランニング・逆運動学・JointTrajectoryController  
**学習目標**: 高度なロボットアーム制御システムの構築

### 6. [🔗 ゼロからのROS入門 - シミュレータや実機との接続](slides/ros-simulator-connection/)
**対象**: 中級者〜上級者  
**内容**: ROSシステム統合技術の実践。ros_control・Bringupパッケージ・Gazeboシミュレータ・実機接続  
**学習目標**: シミュレータと実機を統合した開発環境の構築

## 🎯 推奨学習フロー

### 初学者向け
```
RevealJS使い方 → ハードウェアインテグレーション → ロボット操作の基本 → ROS入門
```

### ROS実践者向け
```
ロボットモデル表示 → アーム位置制御 → シミュレータ接続
```

### システム構築者向け
```
ハードウェアインテグレーション → ロボット操作の基本 → ロボットモデル表示 → シミュレータ接続
```

### 上級者向け
```
必要な部分を選択的に学習
```

## 🚀 スライドの使い方

1. **GitHub Pagesで閲覧（推奨）**
   
   最も簡単な方法！ブラウザで直接アクセス：
   
   🔗 **[https://yusakunakajima.github.io/zero_ros/](https://yusakunakajima.github.io/zero_ros/)**

2. **ローカル環境で起動**

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

## 📊 学習進捗の目安

| スライド | 所要時間 | 前提知識 | 達成目標 |
|---------|----------|----------|----------|
| RevealJS使い方 | 10分 | なし | 操作習得 |
| ハードウェアインテグレーション | 2-3時間 | なし | 実機統合スキル |
| ロボット操作の基本 | 2-3時間 | ロボット基礎 | 基本操作理解 |
| ROS入門 | 1-2時間 | なし | 学習戦略確立 |
| ロボットモデル表示 | 3-4時間 | ROS基礎 | 3D可視化スキル |
| アーム制御 | 4-6時間 | ROS中級 | 制御システム構築 |
| シミュレータ接続 | 3-5時間 | ROS中級 | 統合開発環境 |

---

## 📄 ライセンス

[![License: CC BY-NC-ND 4.0](https://img.shields.io/badge/License-CC%20BY--NC--ND%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-nd/4.0/)

この作品は[クリエイティブ・コモンズ 表示 - 非営利 - 改変禁止 4.0 国際 ライセンス](http://creativecommons.org/licenses/by-nc-nd/4.0/)の下に提供されています。

このスライド資料は2025年7/28~7/31のロボット勉強会用に作成されました。適切な表示を行い、非営利目的での利用に限り、改変せずにそのままの形での再配布が可能です。

---

**Made with ❤️ for Robotics Education**

© 2025 大阪大学 中島優作 | 小野研究室

🌐 小野研究室ホームページ: [https://nano-ap.eng.osaka-u.ac.jp/](https://nano-ap.eng.osaka-u.ac.jp/)

📧 お問い合わせ先: yusaku_nakajima@ap.eng.osaka-u.ac.jp

このスライド集があなたのロボット工学・ROS学習の一助となれば幸いです。質問やフィードバックはお気軽にIssueでお知らせください。