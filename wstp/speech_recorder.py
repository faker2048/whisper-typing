# speech_recorder.py

import pyaudio
import wave
import tempfile
from typing import Callable


class SpeechRecorder:
    def __init__(self, speech2text: Callable[[str], str]):
        self.speech2text = speech2text
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.frames = []

        self.rate = 16000
        self.format = pyaudio.paInt16
        self.buffer_size = 1024

    def start_recording(self):
        self.stream = self.audio.open(
            format=self.format,
            channels=1,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.buffer_size,
        )
        self.frames = []

    def record(self):
        data = self.stream.read(self.buffer_size)
        self.frames.append(data)

    def stop_recording(self):
        self.stream.stop_stream()
        self.stream.close()

    def __open_file(file_name: str = None):
        return (
            open(file_name, "wb")
            if file_name
            else tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        )

    def save_audio(self, file_name: str = None):
        with self.__open_file(file_name) as f:
            wf = wave.open(f, "wb")
            wf.setnchannels(1)
            wf.setsampwidth(self.audio.get_sample_size(self.format))
            wf.setframerate(self.rate)
            wf.writeframes(b"".join(self.frames))
            wf.close()
            return f.name

    def process_audio(self, audio_file: str):
        text = self.speech2text(audio_file)
        return text
