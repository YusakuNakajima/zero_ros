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

スライドタイトルが右に寄っているところは中央に来るように修正
3. 参考書籍の書き方は他のスライドを参考に
4. [![alt text](image.png)](https://vimeo.com/639235111?autoplay=1&muted=1&stream_id=Y2xpcHN8MTU3MTA2MDd8aWQ6ZGVzY3xbXQ%3D%3D)を左ぬ埋め込んで
5. ROSbag
   1. データの可視化
      plot_juggler.pngを左に設置
6. オーダーリストに変更して、もっと短い言葉で