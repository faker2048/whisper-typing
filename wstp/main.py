import time

from loguru import logger

from vrchat.vrchat_client import VRChatClient
from vrchat.vrcontroller import VRController
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
        model_dir=args.model_dir,
        translate=args.translate,
    )
    vrchat_client = VRChatClient()
    vr_controller = VRController()

    def continue_recording():
        return vr_controller.is_pressed(hand="right", button="b")

    while True:
        if continue_recording():
            start_speech_recording(
                args,
                recorder,
                speech2text,
                continue_recording,
                text_callback=vrchat_client.input_to_chatbox,
            ) 
        time.sleep(0.1)


if __name__ == "__main__":
    logger.info("Starting program...")
    start_program()
