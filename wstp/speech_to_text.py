import whisper
from numpy import ndarray
from loguru import logger


class SpeechToText:
    def __init__(
        self,
        model_name: str = "large-v2",
        download_root: str = None,
        in_memory: bool = False,
    ):
        logger.info("Load model...")
        self.model = whisper.load_model(
            name=model_name, download_root=download_root, in_memory=in_memory
        )
        logger.info("Model loaded.")

    def load_audio(self, audio_file: str):
        audio = whisper.load_audio(audio_file)
        return audio

    def speechfile2text(self, audio_file: str) -> str:
        logger.info(" Load audio...")
        audio = self.load_audio(audio_file)
        return self.speech2text(audio)

    def speech2text(self, audio: ndarray) -> str:
        audio = whisper.pad_or_trim(audio)

        # make log-Mel spectrogram and move to the same device as the model
        mel = whisper.log_mel_spectrogram(audio).to(self.model.device)

        # detect the spoken language
        logger.info("Detecting language...")
        _, probs = self.model.detect_language(mel)
        logger.info(f"Detected language: {max(probs, key=probs.get)}")

        # decode the audio
        logger.info("Decoding...")
        options = whisper.DecodingOptions()
        result = whisper.decode(self.model, mel, options)
        logger.info("Decode over.")
        return result.text
