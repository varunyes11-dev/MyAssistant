from .ai import AIProvider, OllamaProvider
from .config import DATA_DIR, SYSTEM_PROMPT
from .conversation import ConversationHistory
from .memory import Memory
from .tool_registry import ToolRegistry


class Brain:
    def __init__(self, provider: AIProvider | None = None):
        self.provider = provider or OllamaProvider()

        self.memory = Memory(
            DATA_DIR / "memory.json"
        )

        self.tool_registry = ToolRegistry(
            self.memory
        )

        self.conversation = ConversationHistory(
            SYSTEM_PROMPT
        )

    @property
    def messages(self):
        """
        Provide access to the current conversation messages.
        """
        return self.conversation.get_messages()

    def ask(self, user_message: str) -> str:
        self.conversation.add_user_message(
            user_message
        )

        try:
            response = self.provider.chat(
                self.messages,
                tools=self._get_tool_definitions(),
            )

            tool_calls = response.get(
                "tool_calls",
                [],
            )

            if tool_calls:
                return self._handle_tool_calls(
                    response,
                    tool_calls,
                )

            reply = response.get(
                "content",
                "",
            ).strip()

            self.conversation.add_assistant_message(
                reply
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

        for name, tool in self.tool_registry.tools.items():
            tools.append(
                {
                    "type": "function",
                    "function": {
                        "name": name,
                        "description": tool["description"],
                        "parameters": tool["parameters"],
                    },
                }
            )

        return tools

    def _handle_tool_calls(
        self,
        response: dict,
        tool_calls: list[dict],
    ) -> str:

        self.conversation.add_tool_call(
            response.get("content", ""),
            tool_calls,
        )

        for tool_call in tool_calls:
            function = tool_call.get(
                "function",
                {}
            )

            tool_name = function.get(
                "name"
            )

            function_arguments = function.get(
                "arguments",
                {}
            )

            result = self.tool_registry.execute(
                tool_name,
                function_arguments,
            )

            self.conversation.add_tool_result(
                result
            )

        final_response = self.provider.chat(
            self.messages,
            tools=self._get_tool_definitions(),
        )

        reply = final_response.get(
            "content",
            "",
        ).strip()

        self.conversation.add_assistant_message(
            reply
        )

        return reply