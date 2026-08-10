from .ai import AIProvider, OllamaProvider
from .config import SYSTEM_PROMPT


class Brain:
    def __init__(self, provider: AIProvider | None = None):
        # Use Ollama by default, but Brain doesn't depend on Ollama directly.
        self.provider = provider or OllamaProvider()

        self.messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            }
        ]

    def ask(self, user_message: str) -> str:
        self.messages.append(
            {
                "role": "user",
                "content": user_message,
            }
        )

        try:
            reply = self.provider.chat(self.messages)

        except Exception:
            # Remove the user message if the AI request failed.
            self.messages.pop()
            raise

        self.messages.append(
            {
                "role": "assistant",
                "content": reply,
            }
        )

        return reply