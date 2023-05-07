# main.py

import sys
import time
import keyboard
import os
from loguru import logger
from speech_recorder import SpeechRecorder
from speech_to_text import speech2text


def print_file_size(file_path: str):
    file_size = os.path.getsize(file_path)
    logger.info("File size: {:.2f} MB".format(file_size / 1024 / 1024))


def main():
    recorder = SpeechRecorder(speech2text)

    while True:
        if keyboard.is_pressed("i"):
            logger.info("Recording started...")
            recorder.start_recording()
            while keyboard.is_pressed("i"):
                recorder.record()
                time.sleep(0.01)
            logger.info("Recording stopped...")
            audio_file = recorder.stop_recording()
            text = recorder.process_audio(audio_file)
            logger.info("Conversion result: {}".format(text))

        if keyboard.is_pressed("q"):
            logger.info("Exiting program...")
            sys.exit(0)


if __name__ == "__main__":
    logger.info("Starting program...")
    main()
