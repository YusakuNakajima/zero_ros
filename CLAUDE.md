このリポジトリは、ロボット工学とROS (Robot Operating System) の基礎を学ぶためのReveal.js製スライドです。

* **`/` (ルート)**: `index.html`がランディングページになっています。
* **`origin_slides/`**: スライド作成の元となったPowerPoint (`.pptx`) やテキストファイル (`.txt`) が保管されています。これらのファイルは参照用であり、**変更は行わないでください**。
* **`slides/`**: 作成したスライドがディレクトリ分けされて管理されています

#### スライド作成の基本方針

* 1スライドあたりのテキストは**最大8行**を目安とします（コードブロックは行数に含めません）。
* 図やイラストを多用し、直感的な理解を促します。
* アニメーションはシンプルにしたいので、スライド遷移は縦か横だけにしてください。

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

-----

## 4\. JavaScript設定

Reveal.jsのプレゼンテーションに機能を追加するため、以下のライブラリとプラグインを読み込み、初期化設定を行います。

### Reveal.jsライブラリ

  * `dist/reveal.js`: Reveal.jsのコアライブラリです。

### プラグイン

以下のプラグインを追加で読み込みます。これらはスライドの機能性を高めます。

  * `plugin/zoom/zoom.js`: スライドの特定領域を拡大表示する機能を提供します。
  * `plugin/menu/menu.js`: プレゼンテーションの目次や便利な機能を提供するメニューを表示します。
  * `plugin/chalkboard/plugin.js`: スライド上への書き込み（描画）や黒板モードを可能にします。

### 初期化設定

`Reveal.initialize()`を使ってReveal.jsをセットアップします。ここでは、表示オプションとプラグインの有効化、さらに各プラグインの基本的な設定を含めます。

```javascript
Reveal.initialize({
    // 基本的な表示設定
    controls: true,  // ナビゲーションUIを表示
    progress: true,  // 進捗バーを表示
    center: true,    // スライドを中央揃え
    hash: true,      // URLにスライド番号を反映

    // プラグインの有効化
    plugins: [
        RevealZoom,      // Zoomプラグインを有効化
        RevealMenu,      // Menuプラグインを有効化
        RevealChalkboard // Chalkboardプラグインを有効化
    ],

    // 各プラグインの設定（任意）
    menu: {
        numbers: true, // 目次にスライド番号を表示
        title: 'プレゼンテーション目次' // メニューのタイトル
    },
    chalkboard: {
        showControls: true, 
        // その他、ブラシの色や線の太さなどを設定可能
    },
    // キーボードショートカットのカスタマイズ
    keyboard: {
        'm': function() { RevealMenu.toggle(); }, // 'm'キーでメニューを切り替え
        // その他のChalkboardショートカットはデフォルトで有効
    }
});
```

#### 5. 非機能要件

* アセット（CSS, JS）はCDNから取得し、高速な読み込みを実現する。
* モバイル端末でも快適に閲覧できるよう、レスポンシブデザインを適用する。
* 高速なパフォーマンスを維持する。

---

## スライド概要

このリポジトリには、ロボット工学とROSの学習に必要な5つのスライドが含まれています。

### スライド一覧

1. **[ゼロからのロボットアーム入門](slides/robot-arm-introduction/)** - ロボットアームの基礎知識と選定方法
2. **[ゼロからのROS入門](slides/ros-introduction/)** - ROSの基礎概念と学習リソース
3. **[ロボットモデルの表示](slides/ros-model-display/)** - URDFとTFを使ったロボット可視化
4. **[アーム位置制御とモーションプランニング](slides/ros-arm-control/)** - MoveItとJTCによる制御実装
5. **[シミュレータや実機との接続](slides/ros-simulator-connection/)** - ros_controlとBringupパッケージ

### 学習順序

- **初学者**: ロボットアーム入門 → ROS入門
- **ROS実践者**: ロボットモデル表示 → シミュレータ接続 → アーム制御 
- **上級者**: 必要な部分を選択的に学習

各スライドディレクトリには詳細な`CLAUDE.md`ファイルがあり、学習内容や構成を確認できます。
**テキスト**と囲われている部分が1スライドを表しています。
目次は階層によって異なる遷移方向を表します。1層目が横に遷移、2層目は縦に遷移します。
