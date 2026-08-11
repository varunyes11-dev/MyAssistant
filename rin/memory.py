import json
from pathlib import Path


class Memory:
    """
    Persistent local memory for Rin.
    """

    def __init__(self, file_path: str | Path):
        self.file_path = Path(file_path)

        self.file_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.memories = self._load()

    def _load(self) -> list[str]:
        """
        Load memories from disk.
        """

        if not self.file_path.exists():
            return []

        try:
            with self.file_path.open(
                "r",
                encoding="utf-8",
            ) as file:
                data = json.load(file)

            if isinstance(data, list):
                return data

            return []

        except (
            json.JSONDecodeError,
            OSError,
        ):
            return []

    def _save(self) -> None:
        """
        Save memories to disk.
        """

        with self.file_path.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                self.memories,
                file,
                indent=2,
                ensure_ascii=False,
            )

    def add(self, memory: str) -> None:
        """
        Add a memory if it does not already exist.
        """

        memory = memory.strip()

        if not memory:
            return

        if memory not in self.memories:
            self.memories.append(memory)
            self._save()

    def get_all(self) -> list[str]:
        """
        Return all stored memories.
        """

        return list(self.memories)

    def clear(self) -> None:
        """
        Clear all memories.
        """

        self.memories.clear()
        self._save()
