"""End-to-end smoke test for the intelligent CS system."""
import os
import tempfile
from modules.file_loader import FileLoader
from modules.vector_store import VectorStoreManager
from modules.agent import AgentManager
from modules.memory import MemoryManager


def test_full_pipeline_with_txt():
    """Test the full pipeline: load file → store → search → agent context."""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_content = "本公司的退货政策规定：客户可在购买后7天内申请退货，商品需保持完好。退货时需提供购买凭证。"
        test_path = os.path.join(tmpdir, "returns_policy.txt")
        with open(test_path, "w", encoding="utf-8") as f:
            f.write(test_content)

        loader = FileLoader()
        docs = loader.load_file(test_path)
        assert len(docs) > 0
        assert "退货" in docs[0].page_content

        store = VectorStoreManager(persist_dir=os.path.join(tmpdir, "chroma"))
        try:
            store.add_documents(docs)
            assert store.count() > 0

            results = store.search("退货政策", k=1)
            assert len(results) > 0
            assert "退货" in results[0].page_content

            agent = AgentManager(vector_store=store)
            assert agent.agent is not None
        finally:
            store.close()

        mem = MemoryManager()
        mem.save_context({"input": "退货需要什么？"}, {"output": "7天内退货，需购买凭证。"})
        vars_ = mem.load_memory_variables({})
        assert "history" in vars_
