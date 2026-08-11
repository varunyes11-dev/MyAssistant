from .ai import AIProvider, OllamaProvider
from .config import SYSTEM_PROMPT
from .tools import get_current_datetime


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
        # Handle date/time questions using the real system clock.
        if self._is_datetime_question(user_message):
            return f"Today is {get_current_datetime()}."

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

    @staticmethod
    def _is_datetime_question(message: str) -> bool:
        text = message.lower().strip()

        date_keywords = (
            "what date is today",
            "what's today's date",
            "what is today's date",
            "today's date",
            "todays date",
            "what day is today",
            "what day today",
            "current date",
            "today date",
        )

        time_keywords = (
            "what time is it",
            "what's the time",
            "current time",
            "what time",
        )

        return any(
            keyword in text
            for keyword in date_keywords + time_keywords
        )