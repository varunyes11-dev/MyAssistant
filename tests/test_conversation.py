from rin.conversation import ConversationHistory


conversation = ConversationHistory(
    "You are Rin."
)

print("Initial messages:")
print(conversation.get_messages())

conversation.add_user_message(
    "Hello Rin."
)

conversation.add_assistant_message(
    "Hello Varun!"
)

conversation.add_user_message(
    "What can you do?"
)

print("\nConversation:")
print(conversation.get_messages())

print("\nMessage count:")
print(len(conversation))

conversation.clear()

print("\nAfter clearing:")
print(conversation.get_messages())
