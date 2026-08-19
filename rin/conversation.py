class ConversationHistory:
    """
    Stores the messages belonging to Rin's current conversation.
    """

    def __init__(self, system_prompt: str):
        self.messages = [
            {
                "role": "system",
                "content": system_prompt,
            }
        ]

    def add_user_message(self, content: str):
        self.messages.append(
            {
                "role": "user",
                "content": content,
            }
        )

    def add_assistant_message(self, content: str):
        self.messages.append(
            {
                "role": "assistant",
                "content": content,
            }
        )

    def add_tool_call(
        self,
        content: str,
        tool_calls: list[dict],
    ):
        self.messages.append(
            {
                "role": "assistant",
                "content": content,
                "tool_calls": tool_calls,
            }
        )

    def add_tool_result(self, content: str):
        self.messages.append(
            {
                "role": "tool",
                "content": content,
            }
        )

    def get_messages(self) -> list[dict]:
        return self.messages

    def clear(self):
        system_message = self.messages[0]

        self.messages = [
            system_message
        ]

    def __len__(self):
        return len(self.messages)
