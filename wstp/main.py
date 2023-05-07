# main.py
import sys
import time
import keyboard
from speech_recorder import SpeechRecorder


def print_file_size(file_path: str):
    import os

    file_size = os.path.getsize(file_path)
    print(f"file_size: {file_size / 1024 / 1024:.2f} MB")


def speech2text(audio_file: str) -> str:
    # 实现speech2text的具体逻辑
    # 返回 audio_file 的时长和文件大小
    print(f"audio_file: {audio_file}")
    pass


def main():
    recorder = SpeechRecorder(speech2text)

    while True:
        if keyboard.is_pressed("i"):
            print("开始录音...")
            recorder.start_recording()
            while keyboard.is_pressed("i"):
                recorder.record()
                time.sleep(0.01)
            print("停止录音...")
            audio_file = recorder.stop_recording()
            text = recorder.process_audio(audio_file)
            print(f"转换结果：{text}")

        if keyboard.is_pressed("q"):
            print("退出程序...")
            sys.exit(0)

        time.sleep(0.1)


if __name__ == "__main__":
    main()
