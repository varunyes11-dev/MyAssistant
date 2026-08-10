import json
import urllib.request

from .base import AIProvider
from ..config import OLLAMA_MODEL


class OllamaProvider(AIProvider):

    def __init__(
        self,
        host: str = "http://127.0.0.1:11434",
    ):
        self.host = host.rstrip("/")

    def chat(self, messages: list[dict]) -> str:
        data = json.dumps(
            {
                "model": OLLAMA_MODEL,
                "messages": messages,
                "stream": False,
            }
        ).encode("utf-8")

        request = urllib.request.Request(
            f"{self.host}/api/chat",
            data=data,
            headers={
                "Content-Type": "application/json"
            },
        )

        try:
            with urllib.request.urlopen(
                request,
                timeout=60,
            ) as response:

                result = json.loads(
                    response.read().decode("utf-8")
                )

            return result["message"]["content"].strip()

        except Exception as error:
            raise RuntimeError(
                f"Could not connect to Ollama: {error}"
            ) from error