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

ur_tipsにスライドを追加
- URの回転表現はデフォルトで回転ベクトルです、RPY(ロールピッチヨー)で使うには変換が必要(scipy rotationとか),rot_vector.htmlを埋め込み
- servoJ/Lは最速で姿勢まで動くので危ないです！
  - 事前にmoveJ/Lでゆっくり動かして、意図しない姿勢をとっていないのかを事前確認してください！,move_vs_servo.htmlを埋め込み
