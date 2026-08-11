from rin.ai.ollama import OllamaProvider


provider = OllamaProvider()

messages = [
    {
        "role": "user",
        "content": "What time is it?",
    }
]

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_datetime",
            "description": "Get the current local date and time.",
            "parameters": {
                "type": "object",
                "properties": {},
            },
        },
    }
]

result = provider.chat(
    messages,
    tools=tools,
)

print("Ollama response:")
print(result)
