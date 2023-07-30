from loguru import logger
from numpy import ndarray

from .model import initialize_whisper_model


class SpeechToText:
    def __init__(
        self,
        model_name: str = "large-v2",
        model_dir: str = None,
        translate: bool = False,
    ):
        self.model = initialize_whisper_model(model_name, model_root=model_dir)
        logger.info(f"🛫 Model Loaded: {model_name}")
        self.translate = translate

    def speech2text(self, audio: ndarray, language: str) -> str:
        segs, _ = self.model.transcribe(
            audio,
            language=language,
            task="translate" if self.translate else "transcribe",
        )

        text = " ".join(seg.text.strip() for seg in segs)

        return text.strip()
