from .ai import AIProvider, OllamaProvider
from .config import SYSTEM_PROMPT
from .tool_registry import ToolRegistry


class Brain:
    def __init__(self, provider: AIProvider | None = None):
        self.provider = provider or OllamaProvider()
        self.tool_registry = ToolRegistry()

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
            response = self.provider.chat(
                self.messages,
                tools=self._get_tool_definitions(),
            )

            tool_calls = response.get("tool_calls", [])

            if tool_calls:
                return self._handle_tool_calls(
                    response,
                    tool_calls,
                )

            reply = response.get("content", "").strip()

            self.messages.append(
                {
                    "role": "assistant",
                    "content": reply,
                }
            )

            return reply

        except Exception:
            self.messages.pop()
            raise

    def _get_tool_definitions(self) -> list[dict]:
        """
        Convert registered tools into Ollama's tool format.
        """

        tools = []

        for name, description in self.tool_registry.get_descriptions().items():

            tools.append(
                {
                    "type": "function",
                    "function": {
                        "name": name,
                        "description": description,
                        "parameters": {
                            "type": "object",
                            "properties": {},
                        },
                    },
                }
            )

        return tools

    def _handle_tool_calls(
        self,
        response: dict,
        tool_calls: list[dict],
    ) -> str:

        self.messages.append(
            {
                "role": "assistant",
                "content": response.get("content", ""),
                "tool_calls": tool_calls,
            }
        )

        for tool_call in tool_calls:

            function = tool_call.get("function", {})
            tool_name = function.get("name")

            function_arguments = function.get("arguments", {})
            result = self.tool_registry.execute(tool_name, function_arguments)

            self.messages.append(
                {
                    "role": "tool",
                    "content": result,
                }
            )

        final_response = self.provider.chat(
            self.messages,
            tools=self._get_tool_definitions(),
        )

        reply = final_response.get("content", "").strip()

        self.messages.append(
            {
                "role": "assistant",
                "content": reply,
            }
        )

        return reply