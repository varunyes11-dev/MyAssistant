from rin.ai import OllamaProvider


provider = OllamaProvider()

messages = [
    {
        "role": "user",
        "content": "Say hello to Varun in one short sentence.",
    }
]

reply = provider.chat(messages)

print("Rin:", reply)