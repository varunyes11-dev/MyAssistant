from pathlib import Path

from rin.memory import Memory
from rin.tool_registry import ToolRegistry


TEST_FILE = Path("data/temp/test_registry_memory.json")


if __name__ == "__main__":
    memory = Memory(TEST_FILE)

    memory.clear()

    registry = ToolRegistry(memory)

    print("Registered tools:")
    print(registry.list_tools())

    print("\nTool descriptions:")
    print(registry.get_descriptions())

    print("\nSaving memory:")
    print(
        registry.execute(
            "save_memory",
            {
                "memory": "Varun likes Python.",
            },
        )
    )

    print("\nStored memories:")
    print(
        registry.execute(
            "get_memories",
        )
    )

    print("\nForgetting memory:")
    print(
        registry.execute(
            "forget_memory",
            {
                "memory": "Varun likes Python.",
            },
        )
    )

    print("\nRemaining memories:")
    print(
        registry.execute(
            "get_memories",
        )
    )

    memory.clear()