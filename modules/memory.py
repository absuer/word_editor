"""Conversation memory management with buffer window."""
from typing import Dict, Any
from langchain_classic.memory import ConversationBufferWindowMemory
from config import MEMORY_KEEP_RECENT


class MemoryManager:
    """Wraps ConversationBufferWindowMemory for the intelligent CS system."""

    def __init__(self, k: int = MEMORY_KEEP_RECENT):
        self.k = k
        self.memory = ConversationBufferWindowMemory(
            k=k,
            return_messages=True,
            memory_key="history",
        )

    def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, Any]) -> None:
        """Save a conversation turn to memory."""
        self.memory.save_context(inputs, outputs)

    def load_memory_variables(self, inputs: Dict[str, Any] = None) -> Dict[str, Any]:
        """Load memory variables for prompt injection."""
        return self.memory.load_memory_variables(inputs or {})

    @property
    def chat_memory(self):
        """Direct access to the underlying chat message history."""
        return self.memory.chat_memory
