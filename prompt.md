スライドを完全に作り直します、以下の指示通りにスライドを作ってください
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
タイトル：ゼロからのROS入門シミュレータや実機との接続
バックグラウンド：gazebo.png
5. a
   14. MoveItCommanderによる実装
   slides/ros-model-display/index.htmlを参考にmoveit_demo.pyを埋め込み
https://github.com/quantumbeam/powder_grinding/blob/develop/grinding_motion_routines/src/grinding_motion_routines/moveit_executor.pyを参考にmoveit_demo.pyを作成
6. a
   12. JointTrajectoryControllerの実装
   まともに書くと大変なので、https://github.com/quantumbeam/powder_grinding/blob/develop/grinding_motion_routines/src/grinding_motion_routines/JTC_executor.pyを使うと簡単に書ける
   slides/ros-model-display/index.htmlを参考にjtc_demo.pyを埋め込み
   同時にjtc_demo.pyを作成
7. 
8. waypointsの表示
   1. デバッグ用にwaypointsを表示したいことはよくある、方法を紹介
   2. DisplayMarkerを使った表示
      1. RVizの可視化ツールであるDisplayMarkerが便利
      2. 位置の表示には適しているが、姿勢の表示には適していない
      3. 実装、   slides/ros-model-display/index.htmlを参考にmarker_display_demo.pyを埋め込み
      https://github.com/quantumbeam/powder_grinding/blob/develop/grinding_motion_routines/src/grinding_motion_routines/marker_display.pyを参考にmarker_display_demo.pyを作成
   3. TFを使った表示
      1. Markerは主に位置の表示だが、座標管理のTFを使うことで位置+向きの姿勢を知ることができる
      2. TFは本来ロボットや環境の座標管理用なので、あまり良くないかも(Poseを使うべきかもしれない)
      3. 実装、   slides/ros-model-display/index.htmlを参考にtf_display_demo.pyを埋め込み
   https://github.com/quantumbeam/powder_grinding/blob/develop/grinding_motion_routines/src/grinding_motion_routines/tf_publisher.pyを参考にtf_display_demo.pyを作成