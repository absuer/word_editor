"""Tests for memory module."""
from modules.memory import MemoryManager
from langchain_core.messages import HumanMessage, AIMessage


class TestMemoryManager:
    def test_initialization(self):
        mm = MemoryManager()
        assert mm is not None
        assert mm.memory is not None

    def test_save_and_load_context(self):
        mm = MemoryManager(k=10)
        mm.save_context(
            {"input": "什么是Python？"},
            {"output": "Python是一种解释型编程语言。"}
        )
        mm.save_context(
            {"input": "它有什么优点？"},
            {"output": "Python语法简洁，生态丰富，适合快速开发。"}
        )

        history = mm.memory.load_memory_variables({})
        assert "history" in history
        assert len(history["history"]) > 0

    def test_custom_window_size(self):
        mm = MemoryManager(k=3)
        assert mm.k == 3

    def test_chat_history_format(self):
        mm = MemoryManager()
        mm.chat_memory.add_user_message("你好")
        mm.chat_memory.add_ai_message("你好！有什么可以帮你的？")

        messages = mm.chat_memory.messages
        assert len(messages) == 2
        assert isinstance(messages[0], HumanMessage)
        assert isinstance(messages[1], AIMessage)
        assert messages[0].content == "你好"
        assert messages[1].content == "你好！有什么可以帮你的？"
