# 🤖 ゼロからのROS入門シリーズ

## 🌐 オンラインで今すぐ学習開始！

**📖 GitHub Pages で直接アクセス**

🔗 **[https://yusakunakajima.github.io/zero_ros/](https://yusakunakajima.github.io/zero_ros/)**

- ✅ ブラウザですぐにアクセス可能
- ✅ ローカル環境設定不要
- ✅ モバイル・タブレット対応
- ✅ 全スライドを順次学習可能

**大阪大学 中島優作**

ロボットアーム制御の基礎から応用まで、実践的な内容を学べるスライド集です。
ロボットアームを触ったことがあり、次のステップとしてROSを使ってみたい方に向けた構成となっています。

📋 適切な表示を行い、非営利目的での利用に限り、改変せずにそのままの形での再配布が可能です。

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

## 🐳 ROS2 Docker環境の使い方

ROS2 の実行環境はリポジトリ直下の `docker/` と `ros2_ws/` に同梱しています。
スライド閲覧だけなら不要ですが、RViz や `ros2 launch` を試す場合はこの環境を使ってください。

### 事前準備

```bash
sudo apt install docker.io docker-compose-plugin
xhost +local:docker
```

### 起動

```bash
git clone https://github.com/yusakunakajima/zero_ros.git
cd zero_ros
docker compose -f docker/compose.yaml up --build --remove-orphans
```

### よく使うDockerコマンド

```bash
# コンテナをバックグラウンドで起動
docker compose -f docker/compose.yaml up -d --build --remove-orphans

# コンテナ内に入る
docker compose -f docker/compose.yaml exec ros_study bash

# ログを見る
docker compose -f docker/compose.yaml logs -f

# 停止する
docker compose -f docker/compose.yaml down --remove-orphans

# イメージを作り直す
docker compose -f docker/compose.yaml build --no-cache
```

### コンテナ内での基本操作

```bash
cd /home/ros/zero_ros/ros2_ws
colcon build --symlink-install
source install/setup.bash

ros2 launch ros_study_description view_ur.launch.py
ros2 launch ros_study_bringup ur5e_bringup_with_mock_components.launch.py
ros2 run ros_study_examples jtc_demo
```

### 起動後の次の進め方

`ros_study_humble Started` まで出たら、次は次のどちらかで進めます。

1. ターミナルから入る

```bash
docker compose -f docker/compose.yaml exec ros_study bash
cd /home/ros/zero_ros/ros2_ws
colcon build --symlink-install
source install/setup.bash
```

2. VSCode から attach する

- Dev Containers 拡張を入れる
- `Dev Containers: Attach to Running Container...` を開く
- `ros_study_humble` を選ぶ
- 開いたターミナルで `cd /home/ros/zero_ros/ros2_ws` して作業する

詳しい Docker 手順は [docker/README.md](/home/user/zero_ros/docker/README.md)、workspace の使い方は [ros2_ws/README.md](/home/user/zero_ros/ros2_ws/README.md) を参照してください。

初回や service 名変更後は orphan コンテナ警告が出ることがありますが、上の `--remove-orphans` 付きコマンドで一緒に整理できます。

ローカル限定の UI から操作したい場合は [environment-setup/index.html](/home/user/zero_ros/environment-setup/index.html) を開き、先に `python3 tools/ros_study_env_server.py` を起動してください。ページ上では Docker ビルド中にスピナーが回り、ターミナルログをそのまま確認できます。

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