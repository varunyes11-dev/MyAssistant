import subprocess

from .config import ASSISTANT_NAME


def speak(text: str):
    """
    Speak the given text using macOS.
    """

    if not text.strip():
        return

    print(f"{ASSISTANT_NAME}: {text}")

    subprocess.run(
        ["say", text],
        check=False
    )