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

スライドを修正します
最後にLPも更新してください
ros-ft-sensor
フォーストルクセンサの使い方
1. a
2. a
3. a
4. a
   1. Leptrinoフォーストルクセンサとは、安価で性能も十分、USB接続で使いやすい
   2. 外部パッケージの使い方 3Steps
      1. clone(git clone https://github.com/hiveground-ros-package/leptrino_force_torque) 
      2. rosdep(rosdep install -i --from-paths src)
      3. build(catkin build; source devel/setup.bash)
   3. USBのセンサのパスの指定方法
      1. /dev/ttyACM* or /dev/ttyUSB*
      2. チップによっては、/dev/serial/by-idで確認をすると製品ごとの固有のパスも可能
   4. センサーデータの確認
      1. roslaunch leptrino_force_torque leptrino.launch
         1. COMポートは先ほど確認したものを指定する
      2. wrench_stampedのデバッグ表示
         1. rostopic echo or rqt_plotで確認

# 新規スライドの作成
ROS2の初心者向けのスライドを作っています
初心者向けに、はまりやすいポイントをに気を付けながら、
実際のrosのコードも交えて、チュートリアルのような形でスライドを作成してください
名称はindex_ros2_ver2.htmlです

以下のコンテンツで新規スライドを作ってください
番号はスライドのページ数を表しています
ネストした番号はスライドの縦方向へのネストを表しています
「」内はスライドタイトルを表しています

「ゼロからのROS2」
1. ゼロからのROS2
    * ROS2におけるシミュレータ
    * 大阪大学 中島優作

「本スライドの担当範囲」
2. 本スライドの担当範囲
    * 前章と本章の決定的な違いは「制御」しているかどうか
    * 前回（モデル表示）：GUIでパラメーターを変えて、単に「表示」を動かしていただけ
    * 今回（シミュレータ）：コントローラ（制御プログラム）が計算して「ロボット」を制御する
    * ここでのコードは、設定を切り替えるだけで「実機」でもそのまま動く

「ROS2のシミュレータの種類」
3. ROS2のシミュレータの種類
    * 比較項目：簡易シミュレーション vs 物理シミュレータ
    * ツール名：Mock Hardware (ros2_control) vs Gazebo
    * 仕組み：物理演算なし（指令通りに動いたことにする） vs 物理演算あり（重力・摩擦・衝突を計算）
    * 特徴・用途：動作が軽い（ロジック・通信確認に最適） vs 処理が重い（現実に近い検証が可能）

「Mock Hardware vs Gazebo」
4. Mock Hardware vs Gazebo
    * インタラクティブ比較アプリへのリンク（全画面表示）

「Mock Hardware (ros2_control)」
5. Mock Hardware (ros2_control)
    1. Mock Hardware (ros2_control)
        * 実機を使わずにロボットの制御をテストするためのROS2標準機能
        * 物理演算は行わないが、「コントローラからの指令を受け取り、動いたことにする」振る舞いをシミュレートする
        * MoveItなどの動作確認によく使われる
    2. 【重要】前のスライドとの違い
        * 前章（モデル表示）：手動でスライダーを動かす、絵として表示されているだけ、自律的に動かない、実機プログラムは動かない
        * 本章（制御シミュレーション）：コントローラが計算して指令を出す、MoveItなどが実際に使える、実機と同じプログラムで動く
    3. Mock Hardware起動用Launch (Python)
        * `use_mock_hardware:=true`：URDF内でMockプラグインを有効化
        * `ros2_control_node`：仮想的な制御ループを回すメインプロセス
        * `spawner`：必要なコントローラを動的にロード
    4. 実行結果の確認
        * 見た目：RViz上の表示はモデル表示と同じに見える
        * 動作：MoveItから「Plan & Execute」で計算された軌道に沿って動く
        * トピック：`/joint_states` は `joint_state_broadcaster` から配信される

「Gazebo」
6. Gazebo
    1. Gazebo
        * ROSで最も広く使われている3D物理シミュレータ
        * 重力、摩擦、衝突、センサデータ（カメラ・LiDAR）などを物理エンジンを用いて計算する
        * 実機を動かす前の「最終確認」として不可欠
    2. 【注意】Gazeboは2種類ある
        * Gazebo Classic (旧)：長年使われてきた、安定している、コマンドは `gazebo`、2025年サポート終了予定
        * Gazebo (New)：次世代のモダンなシミュレータ、軽量・高画質、コマンドは `gz sim`、今後の主流
    3. Gazebo環境のセットアップ
        * ROS 2とGazeboを通信させるパッケージをインストールする
        * モダンなGazebo (推奨)：`ros-${ROS_DISTRO}-ros-gz`
        * Gazebo Classic (旧)：`ros-${ROS_DISTRO}-gazebo-ros-pkgs`
    4. Gazeboの起動確認
        * Humbleの場合：`ign gazebo shapes.sdf`
        * Jazzyの場合：`gz sim shapes.sdf`
        * ⚠️ 初回起動時の注意：モデルダウンロードのため数分間画面が真っ暗になることがある
    5. ros2_controlとの連携
        * どちらのGazeboでもros2_control経由で動かす基本構成は同じ
        * Mock Hardware：実機なし、物理演算なし
        * Gazebo Classic：`gazebo_ros2_control` プラグインを使用
        * Gazebo (New)：`gz_ros2_control` プラグインを使用

「ありがとうございました」
7. ありがとうございました
    * シリーズ一覧に戻る


また、スライド作成後は以下のコマンドを実行してでスライドのpdfを生成して、スライドのpdfを確認してフォーマットの崩れがないか確認してください
崩れがある場合は、スライドの修正を行ってください

npx decktape http://localhost:5500/slides/ros-simulator-connection/index_ros2_ver2.html slides_ros2.pdf

念入りに確認をして、とても丁寧で分かりやすいスライドを心がけてください