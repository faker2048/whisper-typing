# main.py

import sys
import time
import keyboard
from loguru import logger
from speech_recorder import SpeechRecorder
from speech_to_text import speech2text


def handle_record(keyboard_key: str, recorder: SpeechRecorder):
    logger.info("Recording started...")
    recorder.start_recording()
    while keyboard.is_pressed(keyboard_key):
        recorder.record()
        time.sleep(0.01)
    logger.info("Recording stopped...")
    recorder.stop_recording()
    audio_file = recorder.save_audio("target/audio.wav")
    logger.info("Audio file saved: {}".format(audio_file))
    text = recorder.process_audio(audio_file)
    logger.info("Conversion result: {}".format(text))


def handle_exit():
    logger.info("Exiting program...")
    sys.exit(0)


def main():
    recorder = SpeechRecorder(speech2text)

    while True:
        keyboard.wait("i")
        if keyboard.is_pressed("i"):
            handle_record("i", recorder)
        if keyboard.is_pressed("q"):
            handle_exit()
        time.sleep(0.1)


if __name__ == "__main__":
    logger.info("Starting program...")
    main()
