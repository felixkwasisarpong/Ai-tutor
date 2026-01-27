from collections import deque
from typing import Deque, List
from app.memory.models import MemoryEntry


MAX_MEMORY_TURNS = 3
class ConversationMemory:
    def __init__(self):
        self._entries: Deque[MemoryEntry] = deque(maxlen=MAX_MEMORY_TURNS)

    def add(self, entry: MemoryEntry):
        self._entries.append(entry)

    def get(self) -> List[MemoryEntry]:
        return list(self._entries)

    def list(self) -> List[MemoryEntry]:
        return self.get()

    def clear(self):
        self._entries.clear()
