# main.py

import sys
import time
import keyboard
import argparse
from loguru import logger
from wstp.speech_recorder import SpeechRecorder
from wstp.speech_to_text import SpeechToText
from typing import Callable
from vrchat.vrchat_client import VRChatClient


def handle_record(
    args: argparse.Namespace,
    recorder: SpeechRecorder,
    speech2text: SpeechToText,
    text_callback: Callable = None,
):
    logger.debug("Recording started...")
    recorder.start_recording()
    while keyboard.is_pressed(args.keyboard_key):
        time.sleep(0.1)
    logger.debug("Recording stopped...")
    recorder.stop_recording()

    if args.save:
        logger.debug("Saving audio...")
        recorder.save_audio("target/audio.wav")

    audio = recorder.get_audio_data()
    text = speech2text.speech2text(audio, args.language)
    if text_callback:
        text_callback(text)


def handle_exit():
    logger.info("Exiting program...")
    sys.exit(0)


def parse_args():
    parser = argparse.ArgumentParser(description="Speech Recorder")
    parser.add_argument(
        "-r", "--rate", type=int, default=16000, help="Sampling rate (default: 16000)"
    )
    parser.add_argument(
        "-k",
        "--keyboard-key",
        type=str,
        default="i",
        help="Keyboard key to start/stop recording (default: 'F10')",
    )
    parser.add_argument(
        "-l",
        "--language",
        type=str,
        default=None,
        help="Language code (default: None)",
    )
    parser.add_argument(
        "-s",
        "--save",
        type=bool,
        default=False,
        help="Save recorded audio (default: False)",
    )
    parser.add_argument(
        "-t",
        "--translate",
        type=bool,
        default=False,
        help="Translate text (default: False)",
    )
    parser.add_argument(
        "-m",
        "--model-name",
        type=str,
        default="large-v2",
        help="Model name (default: 'large-v2')",
    )

    return parser.parse_args()


def main():
    args = parse_args()

    recorder = SpeechRecorder(
        rate=args.rate,
    )
    speech2text = SpeechToText(
        model_name=args.model_name,
        download_root="F:/youtube",
        in_memory=True,
    )
    vrchat_client = VRChatClient()

    while True:
        keyboard.wait(args.keyboard_key)
        if keyboard.is_pressed(args.keyboard_key):
            handle_record(args, recorder, speech2text, vrchat_client.input_to_chatbox)

        time.sleep(0.1)


if __name__ == "__main__":
    logger.info("Starting program...")
    main()
