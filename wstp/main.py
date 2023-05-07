# main.py

import sys
import time
import keyboard
import os
from loguru import logger
from speech_recorder import SpeechRecorder
from speech_to_text import speech2text


def main():
    recorder = SpeechRecorder(speech2text)

    while True:
        keyboard.wait("i")
        if keyboard.is_pressed("i"):
            logger.info("Recording started...")
            recorder.start_recording()
            while keyboard.is_pressed("i"):
                recorder.record()
                time.sleep(0.01)
            logger.info("Recording stopped...")
            recorder.stop_recording()
            audio_file = recorder.save_audio("target/audio.wav")
            logger.info("Audio file saved: {}".format(audio_file))
            text = recorder.process_audio(audio_file)
            logger.info("Conversion result: {}".format(text))

        if keyboard.is_pressed("q"):
            logger.info("Exiting program...")
            sys.exit(0)
        time.sleep(0.1)


if __name__ == "__main__":
    logger.info("Starting program...")
    main()
