## 前準備
スライドのpptxのzip展開したものと、テキストを書きだしたtxtファイルを用意
スライドを画像化してテキスト抽出しようかと思ったけど、画像からテキスト読むことができないんで無理そうだった

## スライド生成の指示だし

slide_name=ゼロからのROS入門で置き換えてください

slide_name_origin/slide_name_pptxはpptxファイルをzip展開してモノです
これと同じ内容のreveal.jsのパワポを作ってもらえないでしょうかslide_name_origin/slide_name.txtにあります
新しいディレクトリを作って、そのなかにhtmlやmediaのコピーをつくってください


## 音声指示だし
sudo apt update
sudo apt install ffmpeg
uv add openai-whisper
uv add pydub
uv add pyaudio