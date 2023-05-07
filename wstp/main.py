# main.py

import sys
import time
import keyboard
import argparse
from loguru import logger
from speech_recorder import SpeechRecorder
from speech_to_text import SpeechToText


def handle_record(
    keyboard_key: str, recorder: SpeechRecorder, speech2text: SpeechToText
):
    logger.info("Recording started...")
    recorder.start_recording()
    while keyboard.is_pressed(keyboard_key):
        recorder.record()
    logger.info("Recording stopped...")
    recorder.stop_recording()
    audio_file = recorder.save_audio("target/audio.wav")
    logger.info("Audio file saved: {}".format(audio_file))
    text = speech2text.speech2text(audio_file)
    logger.info("Text: {}".format(text))


def handle_exit():
    logger.info("Exiting program...")
    sys.exit(0)


def parse_args():
    parser = argparse.ArgumentParser(description="Speech Recorder")
    parser.add_argument(
        "-r", "--rate", type=int, default=16000, help="Sampling rate (default: 16000)"
    )
    parser.add_argument(
        "-b",
        "--buffer-size",
        type=int,
        default=1024,
        help="Buffer size (default: 1024)",
    )
    parser.add_argument(
        "-k",
        "--keyboard-key",
        type=str,
        default="i",
        help="Keyboard key to start/stop recording (default: 'i')",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    recorder = SpeechRecorder(
        rate=args.rate,
        buffer_size=args.buffer_size,
    )
    speech2text = SpeechToText(
        model_name="large-v2",
        download_root="F:/youtube",
        in_memory=True,
    )

    while True:
        keyboard.wait(args.keyboard_key)
        if keyboard.is_pressed(args.keyboard_key):
            handle_record(args.keyboard_key, recorder, speech2text)

        if keyboard.is_pressed("q"):
            handle_exit()
        time.sleep(0.1)


if __name__ == "__main__":
    logger.info("Starting program...")
    main()
