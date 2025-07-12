import whisper
import pyaudio
import wave
import sys
import os

# 設定
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000 # Whisperが推奨するサンプリングレート
RECORD_SECONDS = 5 # 録音する秒数
WAVE_OUTPUT_FILENAME = "output.wav"

# モデルのロード (初回はダウンロードされます)
# tiny, base, small, medium, large があります。tinyが最速、largeが最高精度。
model = whisper.load_model("base")

print(f"{RECORD_SECONDS}秒間の録音を開始します。")

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("録音終了。")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

print(f"録音ファイルを '{WAVE_OUTPUT_FILENAME}' として保存しました。")
print("音声認識を開始します...")

# 音声認識を実行
result = model.transcribe(WAVE_OUTPUT_FILENAME, language="ja") # 日本語を指定

print("\n--- 認識結果 ---")
print(result["text"])
print("----------------")

# 録音ファイルを削除 (任意)
# os.remove(WAVE_OUTPUT_FILENAME)
# print(f"'{WAVE_OUTPUT_FILENAME}' を削除しました。")