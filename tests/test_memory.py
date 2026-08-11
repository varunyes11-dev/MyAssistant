from pathlib import Path

from rin.memory import Memory


TEST_FILE = Path("data/temp/test_memory.json")


if __name__ == "__main__":
    memory = Memory(TEST_FILE)

    memory.clear()

    memory.add("Varun likes Python.")
    memory.add("Varun is building Rin.")

    print("Stored memories:")
    print(memory.get_all())

    memory_again = Memory(TEST_FILE)

    print("\nMemories after reloading:")
    print(memory_again.get_all())

    removed = memory_again.remove(
        "Varun likes Python."
    )

    print("\nRemoved Python memory:")
    print(removed)

    print("\nRemaining memories:")
    print(memory_again.get_all())

    memory_again.clear()

    print("\nAfter clearing:")
    print(memory_again.get_all())