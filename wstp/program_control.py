# main.py

import time
import keyboard
from loguru import logger
from client.vrchat_client import VRChatClient
from wstp.argument_parsing import parse_command_line_arguments
from wstp.speech_handling import start_speech_recording
from wstp.speech_recorder import SpeechRecorder
from wstp.speech_to_text import SpeechToText


def start_program():
    args = parse_command_line_arguments()

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
            start_speech_recording(
                args, recorder, speech2text, vrchat_client.input_to_chatbox
            )

        time.sleep(0.1)


if __name__ == "__main__":
    logger.info("Starting program...")
    start_program()
