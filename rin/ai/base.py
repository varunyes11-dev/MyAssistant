from abc import ABC, abstractmethod


class AIProvider(ABC):

    @abstractmethod
    def chat(self, messages: list[dict]) -> str:
        """Send conversation messages to the AI and return its reply."""
        pass