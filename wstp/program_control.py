# main.py

import time
import keyboard
from loguru import logger
from wstp.argument_parsing import parse_command_line_arguments
from wstp.speech_handling import start_speech_recording
from wstp.speech_recorder import SpeechRecorder
from wstp.speech_to_text import SpeechToText
import pyperclip


def to_clipboard(text: str):
    pyperclip.copy(text)
    logger.debug("Text copied to clipboard")


def start_program():
    args = parse_command_line_arguments()

    recorder = SpeechRecorder(
        rate=args.rate,
    )
    speech2text = SpeechToText(
        model_name=args.model_name,
        model_dir=args.model_dir,
        in_memory=True,
    )

    while True:
        keyboard.wait(args.keyboard_key)
        if keyboard.is_pressed(args.keyboard_key):
            start_speech_recording(
                args, recorder, speech2text, text_callback=to_clipboard
            )
        time.sleep(0.1)


if __name__ == "__main__":
    logger.info("Starting program...")
    start_program()
