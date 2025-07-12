import pyaudio
import wave
import sys
import os
import select
from faster_whisper import WhisperModel
from huggingface_hub import snapshot_download

# 設定 (変更なし)
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000 # Whisperが推奨するサンプリングレート
WAVE_OUTPUT_FILENAME = "output.wav"

# モデルのロード
# 新しいモデルを指定
model_id = "whisper-large-v3-turbo-ct2"

# device="cuda" でGPUを使用します。CPUを使用する場合は device="cpu" に変更してください。
# compute_typeは推論の精度を設定します。
# GPUの場合は"float16"が一般的で高速です。CPUの場合は"int8"なども検討できます。
device = "cpu" # または "cpu"
compute_type = "float32" # GPUなら"float16"、CPUなら"int8"や"float32"

print(f"モデル {model_id} をロード中...")
# model_path = snapshot_download(repo_id=model_id)
# print("モデルダウンロード完了。")

# print(f"モデル {model_path} をロード中...")
model = WhisperModel(model_id, device=device, compute_type=compute_type)
print("モデルロード完了。")

# 録音処理 (変更なし)
print("Enterキーを押して録音を開始してください...")
input()

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
frames = []

print("録音中... Enterキーを押して録音を終了してください。")
print("Ctrl+C または Enterキーを押すと録音が終了します。")

try:
    while True:
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            line = sys.stdin.readline()
            if line == '\n':
                break
        data = stream.read(CHUNK)
        frames.append(data)
except KeyboardInterrupt:
    pass

print("録音終了。")

stream.stop_stream()
stream.close()
p.terminate()

if not frames:
    print("録音データがありませんでした。")
    sys.exit()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

print(f"録音ファイルを '{WAVE_OUTPUT_FILENAME}' として保存しました。")
print("音声認識を開始します...")

# 音声認識を実行 (変更なし)
# 日本語に特化しているので language="ja" は必須ではありませんが、明示的に指定すると安心です
segments, info = model.transcribe(WAVE_OUTPUT_FILENAME, language="ja")

print("\n--- 認識結果 ---")
for segment in segments:
    print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")
print("----------------")

# 録音ファイルを削除 (任意)
# os.remove(WAVE_OUTPUT_FILENAME)
# print(f"'{WAVE_OUTPUT_FILENAME}' を削除しました。")