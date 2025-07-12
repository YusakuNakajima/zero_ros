import pyaudio
import numpy as np
import sys
from faster_whisper import WhisperModel
import io

# --- 設定 ---
# マイク入力の設定
CHUNK = 1024  # 一度に読み込むデータサイズ
FORMAT = pyaudio.paInt16  # 音声のフォーマット
CHANNELS = 1  # チャンネル数 (モノラル)
RATE = 16000  # サンプリングレート (Whisperが推奨)

# VAD (Voice Activity Detection) の設定
# この秒数、音声がなければ発話が終了したとみなす
VAD_SILENCE_DURATION_S = 1.5
# 音声と判断する音量の閾値（環境に合わせて調整してください）
VAD_THRESHOLD = 0.02

# --- モデルのロード ---
# 使用するモデルを指定
model_id = "whisper-large-v3-turbo-ct2"

# device="cuda" でGPUを使用します。CPUの場合は device="cpu" に変更してください。
# compute_typeは推論の精度を設定します。
# GPUの場合は"float16"が一般的で高速です。CPUの場合は"int8"なども検討できます。
device = "cpu"  # または "cuda"
compute_type = "float32"  # GPUなら"float16"、CPUなら"int8"や"float32"

try:
    print(f"モデル {model_id} をロード中...")
    model = WhisperModel(model_id, device=device, compute_type=compute_type)
    print("✅ モデルロード完了。")
except Exception as e:
    print(f"❌ モデルのロード中にエラーが発生しました: {e}")
    sys.exit(1)


# --- リアルタイム文字起こし処理 ---
p = pyaudio.PyAudio()

try:
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
except Exception as e:
    print(f"❌ マイクストリームのオープンに失敗しました: {e}")
    print("マイクが接続されているか、アクセス許可があるか確認してください。")
    p.terminate()
    sys.exit(1)

print("\n🎤 リアルタイム文字起こしを開始します。話しかけてください。(終了するには Ctrl+C)")

# 一時的な発話データを保持するバッファ
speech_buffer = io.BytesIO()
# 最後に音声が検出されてからの無音チャンクのカウンター
silent_chunks = 0
# 1回の発話とみなす無音チャンクの数
silence_limit = int(VAD_SILENCE_DURATION_S * RATE / CHUNK)
# 画面表示用の状態
is_speaking = False

try:
    while True:
        # マイクから音声データを読み込む
        data = stream.read(CHUNK)
        
        # 読み込んだデータをnumpy配列に変換し、-1.0から1.0の範囲に正規化
        audio_np = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0

        # 音声があるかどうかの判定
        if np.abs(audio_np).max() > VAD_THRESHOLD:
            if not is_speaking:
                is_speaking = True
                print("...🤔 (聞き取り中)", end="", flush=True)
            silent_chunks = 0
            speech_buffer.write(data)
        else:
            # 無音状態の処理
            silent_chunks += 1
            if is_speaking:
                 # 発話中だった場合は、無音が続いても少しの間は録音を続ける
                 speech_buffer.write(data)

            # 発話が終了したと判断
            if is_speaking and silent_chunks > silence_limit:
                is_speaking = False

                # ★★★ 変更点：変換中メッセージを表示 ★★★
                sys.stdout.write("\r...✍️ (変換中)   ")
                sys.stdout.flush()

                # バッファの先頭に戻る
                speech_buffer.seek(0)
                
                # バッファ全体をnumpy配列として読み込む
                audio_data = speech_buffer.read()
                audio_np_full = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0

                # 音声認識を実行
                segments, info = model.transcribe(
                    audio_np_full,
                    language="ja",
                    beam_size=5,
                    vad_filter=True,
                    vad_parameters=dict(min_silence_duration_ms=500)
                )

                # 認識結果を連結して表示
                full_text = "".join(segment.text for segment in segments)
                
                # カーソルを行頭に戻し、変換中表示を消してから結果を表示
                sys.stdout.write("\r" + " " * 20 + "\r")
                if full_text.strip():
                    print(f"➡️ {full_text}")
                else:
                    # 何も認識されなかった場合
                    print("... (音声が認識できませんでした)")

                # 次の認識のためにバッファとカウンターをリセット
                speech_buffer = io.BytesIO()
                silent_chunks = 0
                
except KeyboardInterrupt:
    print("\n👋 プログラムを終了します。")

finally:
    # ストリームとPyAudioをクリーンアップ
    print("クリーンアップ中...")
    if 'stream' in locals() and stream.is_active():
        stream.stop_stream()
        stream.close()
    if 'p' in locals():
        p.terminate()
    print("完了。")