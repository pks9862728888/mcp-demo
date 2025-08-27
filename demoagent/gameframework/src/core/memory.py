from typing import List, Dict


class Memory:
    def __init__(self):
        self.items: List[Dict] = []

    def add(self, memory: dict):
        """Add items to memory"""
        self.items.append(memory)

    def get(self, limit: int | None = None) -> List[Dict]:
        """Get items from memory"""
        return self.items[:limit] if limit else self.items

    def copy_without_system_memories(self) -> "Memory":
        """Create a copy of memory without system memories"""
        memory = Memory()
        memory.items = [item for item in self.items if not item.get("type") == "system"]
        return memory
