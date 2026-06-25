"""Vector store management using Chroma with local embeddings."""
import os
from typing import List, Optional

# Speed up HuggingFace model loading: prefer local cache, use mirror, short timeout
os.environ.setdefault("HF_HUB_ENABLE_HF_TRANSFER", "0")
os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")
os.environ.setdefault("HF_HUB_DOWNLOAD_TIMEOUT", "10")

from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from config import CHROMA_PERSIST_DIR, DEFAULT_TOP_K


class VectorStoreManager:
    """Manages Chroma vector store for document retrieval."""

    def __init__(self, persist_dir: str = CHROMA_PERSIST_DIR):
        self.persist_dir = persist_dir
        os.makedirs(persist_dir, exist_ok=True)
        self.embeddings = self._load_embeddings()
        self._store: Optional[Chroma] = None

    @staticmethod
    def _load_embeddings():
        """Load embeddings with fallback: mirror → local cache only."""
        common = {
            "model_name": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
            "model_kwargs": {"device": "cpu"},
            "encode_kwargs": {"normalize_embeddings": True},
        }
        try:
            return HuggingFaceEmbeddings(**common)
        except Exception:
            common["model_kwargs"]["local_files_only"] = True
            return HuggingFaceEmbeddings(**common)

    @property
    def store(self) -> Chroma:
        """Lazy-load the Chroma store."""
        if self._store is None:
            self._store = Chroma(
                persist_directory=self.persist_dir,
                embedding_function=self.embeddings,
            )
        return self._store

    def add_documents(self, documents: List[Document]) -> None:
        """Add documents to the vector store with deduplication."""
        if not documents:
            return
        existing_count = self.count()
        if existing_count > 0:
            existing_sources = self._get_existing_sources()
            new_docs = []
            for doc in documents:
                doc_key = f"{doc.metadata.get('source', '')}_{doc.metadata.get('chunk_index', '')}"
                if doc_key not in existing_sources:
                    new_docs.append(doc)
            documents = new_docs
        if documents:
            self.store.add_documents(documents)

    def search(self, query: str, k: int = DEFAULT_TOP_K) -> List[Document]:
        """Search for documents similar to the query."""
        if self.count() == 0:
            return []
        return self.store.similarity_search(query, k=k)

    def clear(self) -> None:
        """Delete all documents from the collection."""
        if self.count() > 0:
            self.store.delete_collection()
            self._store = None

    def close(self) -> None:
        """Release Chroma resources (required on Windows to avoid file locks)."""
        if self._store is not None:
            try:
                self._store._client._system.stop()
            except Exception:
                pass
            self._store = None

    def count(self) -> int:
        """Return the number of documents in the store."""
        try:
            collection = self.store._collection
            return collection.count()
        except Exception:
            return 0

    def get_source_files(self) -> list:
        """Return unique source filenames currently in the vector store.
        Used to restore the file list after a page refresh."""
        try:
            collection = self.store._collection
            results = collection.get(include=["metadatas"])
            if results and results["metadatas"]:
                sources = set()
                for m in results["metadatas"]:
                    src = m.get("source", "")
                    if src:
                        sources.add(src)
                return sorted(sources)
        except Exception:
            return []

    def _get_existing_sources(self) -> set:
        """Get set of existing (source, chunk_index) keys to avoid duplicates."""
        try:
            collection = self.store._collection
            results = collection.get(include=["metadatas"])
            if results and results["metadatas"]:
                return {
                    f"{m.get('source', '')}_{m.get('chunk_index', '')}"
                    for m in results["metadatas"]
                }
        except Exception:
            pass
        return set()
