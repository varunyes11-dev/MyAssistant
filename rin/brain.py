from .ai import AIProvider, OllamaProvider
from .config import SYSTEM_PROMPT
from .tool_registry import ToolRegistry


class Brain:
    def __init__(
        self,
        provider: AIProvider | None = None,
        tool_registry: ToolRegistry | None = None,
    ):
        # Use Ollama by default.
        self.provider = provider or OllamaProvider()

        # Use the built-in tool registry by default.
        self.tool_registry = tool_registry or ToolRegistry()

        self.messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            }
        ]

    def ask(self, user_message: str) -> str:
        # Check whether a local tool should handle the request.
        if self._is_datetime_question(user_message):
            tool = self.tool_registry.get("get_current_datetime")

            if tool:
                return f"Today is {tool()}."

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