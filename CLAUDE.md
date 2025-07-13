このリポジトリは、ロボット工学とROS (Robot Operating System) の基礎を学ぶためのReveal.js製スライドです。

* **`/` (ルート)**: `index.html`がランディングページになっています。
* **`origin_slides/`**: スライド作成の元となったPowerPoint (`.pptx`) やテキストファイル (`.txt`) が保管されています。これらのファイルは参照用であり、**変更は行わないでください**。
* **`slides/`**: 作成したスライドがディレクトリ分けされて管理されています

#### スライド作成の基本方針

* 1スライドあたりのテキストは**最大8行**を目安とします（コードブロックは行数に含めません）。
* 図やイラストを多用し、直感的な理解を促します。
* アニメーションはシンプルにしたいので、スライド遷移は横だけにしてください。

---

### `index.html` 技術仕様書

#### 1. ドキュメント基本設定

* **文書型**: `<!DOCTYPE html>`
* **言語**: 日本語 (`lang="ja"`)
* **文字コード**: `UTF-8`
* **ビューポート**: レスポンシブ対応 (`width=device-width, initial-scale=1.0, user-scalable=no`)
---

#### 2. CSS/フォント設定

* **Reveal.js CSS**:
    * `reset.css`
    * `reveal.css`
    * `white.css` (テーマ)
* **Webフォント**:
    * `Noto Sans JP` (Google Fontsより読み込み)
* **カスタムスタイル**:
    * 基本フォントを`Noto Sans JP`, `42px`, `normal`に設定。
    * `h1`〜`h4`のテキスト変換を無効化 (`text-transform: none;`)。
    * 画像の枠線と影を無効化 (`border: none;`, `box-shadow: none;`)。

---

#### 3. スライド構成 (`<body>`内部)

各スライド（section）の具体的なテキスト内容は記載せず、構造のみを定義します。
スライドの枚数は内容によって変動します。

* **スライド 1: タイトル**
    * `data-background-image`: 背景画像URL
    * `data-background-opacity`: 背景の透明度
    * `<h1>`, `<p>`

* **スライド 2: 導入/目的**
    * `<h2>`
    * `<ul>` (各`<li>`に`.fragment`クラスを適用)

* **スライド 3: 概要説明**
    * `data-transition="convex"`
    * `<h2>`, `<p>`, `<img>`

* **スライド 4~n: 詳細説明 2**
    * `data-transition="zoom"`
    * `<h2>`, `<ul>`, `<img>`

* **スライド n+1: まとめ**
    * `<h2>`, `<p>`, `<p class="fragment">`

* **スライド n+2: 参考資料**
    * `<h2>`, `<ul>`

---

#### 4. JavaScript設定

* **Reveal.jsライブラリ**:
    * `reveal.js`
* **プラグイン**:
    * `zoom.js`
* **初期化設定**:
    * `controls: true` (ナビゲーションUIを表示)
    * `progress: true` (進捗バーを表示)
    * `center: true` (スライドを中央揃え)
    * `hash: true` (URLにスライド番号を反映)
    * `plugins: [ RevealZoom ]` (Zoomプラグインを有効化)

---

#### 5. 非機能要件

* アセット（CSS, JS）はCDNから取得し、高速な読み込みを実現する。
* モバイル端末でも快適に閲覧できるよう、レスポンシブデザインを適用する。
* 高速なパフォーマンスを維持する。