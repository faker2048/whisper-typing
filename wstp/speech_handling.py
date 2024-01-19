import time
import keyboard
import argparse
from loguru import logger
from wstp.speech_recorder import SpeechRecorder
from wstp.speech_to_text import SpeechToText
from typing import Callable


def start_speech_recording(
    args: argparse.Namespace,
    recorder: SpeechRecorder,
    speech2text: SpeechToText,
    continue_recording: Callable[[], bool],
    text_callback: Callable = None,
):
    """
    Start recording audio from SpeechRecorder and convert it to text using
    speech2text. Stop recording when continue_recording returns False.
    If the text is not empty, call text_callback with the text as argument.
    """
    logger.debug("Recording started...")
    recorder.start_recording()
    while continue_recording():
        time.sleep(0.1)
    logger.debug("Recording stopped...")
    recorder.stop_recording()

    if args.save:
        logger.debug("Saving audio...")
        recorder.save_audio("target/audio.wav")

    duration = recorder.get_audio_duration()
    if duration < 0.5:
        logger.debug("Audio too short, ignoring...")
        return

    audio = recorder.get_audio_data()
    text = speech2text.speech2text(audio, args.language)
    if text_callback:
        text_callback(text)
