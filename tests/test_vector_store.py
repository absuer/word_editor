"""Tests for vector_store module."""
import tempfile
import pytest
from langchain_core.documents import Document
from modules.vector_store import VectorStoreManager


@pytest.fixture
def sample_docs():
    return [
        Document(
            page_content="Python是一种解释型编程语言，广泛用于数据科学和人工智能领域。",
            metadata={"source": "test1.txt", "file_type": "txt", "chunk_index": 0}
        ),
        Document(
            page_content="LangChain是一个用于构建LLM应用的框架，支持链式调用和Agent。",
            metadata={"source": "test2.txt", "file_type": "txt", "chunk_index": 0}
        ),
        Document(
            page_content="Chroma是一个开源的向量数据库，适合小型项目和原型开发。",
            metadata={"source": "test3.txt", "file_type": "txt", "chunk_index": 0}
        ),
    ]


class TestVectorStoreManager:
    def test_add_documents_and_search(self, sample_docs):
        with tempfile.TemporaryDirectory() as tmpdir:
            store = VectorStoreManager(persist_dir=tmpdir)
            try:
                store.add_documents(sample_docs)
                results = store.search("Python编程", k=2)
                assert len(results) == 2
                assert any("Python" in doc.page_content for doc in results)
            finally:
                store.close()

    def test_search_returns_top_match(self, sample_docs):
        with tempfile.TemporaryDirectory() as tmpdir:
            store = VectorStoreManager(persist_dir=tmpdir)
            try:
                store.add_documents(sample_docs)
                results = store.search("向量数据库", k=1)
                assert len(results) == 1
                assert "Chroma" in results[0].page_content
            finally:
                store.close()

    def test_collection_stats(self, sample_docs):
        with tempfile.TemporaryDirectory() as tmpdir:
            store = VectorStoreManager(persist_dir=tmpdir)
            try:
                store.add_documents(sample_docs)
                count = store.count()
                assert count == 3
            finally:
                store.close()

    def test_clear_collection(self, sample_docs):
        with tempfile.TemporaryDirectory() as tmpdir:
            store = VectorStoreManager(persist_dir=tmpdir)
            try:
                store.add_documents(sample_docs)
                assert store.count() == 3
                store.clear()
                assert store.count() == 0
            finally:
                store.close()

    def test_duplicate_documents_not_added(self, sample_docs):
        with tempfile.TemporaryDirectory() as tmpdir:
            store = VectorStoreManager(persist_dir=tmpdir)
            try:
                store.add_documents(sample_docs)
                assert store.count() == 3
                store.add_documents(sample_docs)
                results = store.search("Python", k=1)
                assert len(results) == 1
            finally:
                store.close()
