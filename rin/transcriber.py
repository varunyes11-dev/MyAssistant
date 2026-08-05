from pathlib import Path

import mlx_whisper

from .config import WHISPER_MODEL


def transcribe(audio_file: str | Path) -> str:
    """
    Transcribe an audio file using Whisper.
    """

    result = mlx_whisper.transcribe(
        str(audio_file),
        path_or_hf_repo=WHISPER_MODEL,
    )

    text = result.get("text", "").strip()

    return text