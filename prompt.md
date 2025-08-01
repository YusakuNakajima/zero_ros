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
