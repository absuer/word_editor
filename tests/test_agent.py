"""Tests for agent module."""
import tempfile
from langchain_core.documents import Document
from modules.agent import AgentManager, build_retriever_tool, build_web_search_tool
from modules.vector_store import VectorStoreManager


class TestTools:
    def test_retriever_tool_has_correct_name(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            store = VectorStoreManager(persist_dir=tmpdir)
            try:
                tool = build_retriever_tool(store)
                assert tool.name == "retriever"
                assert "retrieve" in tool.description.lower()
            finally:
                store.close()

    def test_retriever_tool_returns_documents(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            store = VectorStoreManager(persist_dir=tmpdir)
            try:
                docs = [
                    Document(
                        page_content="Streamlit是一个用于构建数据应用的Python框架。",
                        metadata={"source": "test.txt", "file_type": "txt", "chunk_index": 0}
                    )
                ]
                store.add_documents(docs)

                tool = build_retriever_tool(store)
                result = tool.invoke({"query": "Streamlit是什么"})
                assert "Streamlit" in result
            finally:
                store.close()

    def test_web_search_tool_has_correct_name(self):
        tool = build_web_search_tool()
        assert tool.name == "web_search"
        assert "search" in tool.description.lower()


class TestAgentManager:
    def test_create_agent(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            store = VectorStoreManager(persist_dir=tmpdir)
            try:
                agent_mgr = AgentManager(vector_store=store)
                assert agent_mgr.agent is not None
            finally:
                store.close()
