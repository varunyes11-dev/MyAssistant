from abc import ABC, abstractmethod


class AIProvider(ABC):

    @abstractmethod
    def chat(
        self,
        messages: list[dict],
        tools: list[dict] | None = None,
    ) -> dict:
        """
        Send conversation messages to the AI.

        Returns a structured response containing either
        normal assistant content or a tool call.
        """
        pass