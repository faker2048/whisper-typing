# speech_recorder.py

import sounddevice as sd
import numpy as np
import wave
import tempfile


class SpeechRecorder:
    def __init__(
        self,
        rate=16000,
        format=np.int16,
    ):
        self.rate = rate
        self.format = format
        self.frames = []

    def start_recording(self):
        self.frames = []
        self.stream = sd.InputStream(
            samplerate=self.rate,
            channels=1,
            dtype=self.format,
            callback=self.__callback,
        )
        self.stream.start()

    def __callback(self, indata, frames, time, status):
        self.frames.append(indata.copy())

    def stop_recording(self):
        self.stream.stop()
        self.stream.close()

    def __open_file(self, file_name: str = None):
        return (
            open(file_name, "wb")
            if file_name
            else tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        )

    def save_audio(self, file_name: str = None):
        with self.__open_file(file_name) as f:
            wf = wave.open(f, "wb")
            wf.setnchannels(1)
            wf.setsampwidth(np.dtype(self.format).itemsize)
            wf.setframerate(self.rate)
            wf.writeframes(b"".join([frame.tobytes() for frame in self.frames]))
            wf.close()
            return f.name
