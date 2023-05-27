import whisper
from numpy import ndarray
from loguru import logger


class SpeechToText:
    def __init__(
        self,
        model_name: str = "large-v2",
        model_dir: str = None,
        in_memory: bool = False,
    ):
        logger.info("Load model...")
        self.model = whisper.load_model(
            name=model_name, download_root=model_dir, in_memory=in_memory
        )
        logger.info("Model loaded.")

    def load_audio(self, audio_file: str):
        audio = whisper.load_audio(audio_file)
        return audio

    def speechfile2text(self, audio_file: str) -> str:
        logger.info(" Load audio...")
        audio = self.load_audio(audio_file)
        return self.speech2text(audio)

    def speech2text(self, audio: ndarray, language: str) -> str:
        audio = whisper.pad_or_trim(audio)

        # make log-Mel spectrogram and move to the same device as the model
        mel = whisper.log_mel_spectrogram(audio).to(self.model.device)

        # decode the audio
        logger.info("Decoding... use language: {}.".format(language))
        options = whisper.DecodingOptions(task="translate", language=language)
        result = whisper.decode(self.model, mel, options)
        return result.text
