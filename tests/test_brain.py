from rin.brain import Brain

brain = Brain()

while True:
    question = input("You: ")

    if question.lower() == "exit":
        break

    reply = brain.ask(question)

    print("Rin:", reply)