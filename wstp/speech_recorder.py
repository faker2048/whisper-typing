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

    def start_recording(self):
        self.stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=1024,
        )
        self.frames = []

    def record(self):
        data = self.stream.read(1024)
        self.frames.append(data)

    def stop_recording(self):
        self.stream.stop_stream()
        self.stream.close()
        return self.save_audio()

    def save_audio(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
            wf = wave.open(f, "wb")
            wf.setnchannels(1)
            wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
            wf.setframerate(16000)
            wf.writeframes(b"".join(self.frames))
            wf.close()
            return f.name

    def process_audio(self, audio_file: str):
        text = self.speech2text(audio_file)
        return text
