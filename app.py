"""Intelligent Customer Service System - Streamlit App."""
import logging
import sys
import time
import uuid
import json
import webbrowser
from datetime import datetime
from pathlib import Path
import streamlit as st
from modules.file_loader import FileLoader
from modules.vector_store import VectorStoreManager
from modules.agent import AgentManager
from modules.memory import MemoryManager
from config import DEFAULT_TOP_K, LLM_MODEL, UPLOAD_DIR, VUE_EDITOR_URL

# ── Logging setup ──────────────────────────────────────────
LOG_FILE = "data/app.log"


class _SafeStreamHandler(logging.StreamHandler):
    """StreamHandler that tolerates encoding errors on Windows GBK consoles."""

    def emit(self, record):
        try:
            super().emit(record)
        except (ValueError, OSError):
            pass  # Streamlit reload closed the stream, ignore


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        _SafeStreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger("intelligent-cs")

# ── Page config ──────────────────────────────────────────
st.set_page_config(
    page_title="智能客服系统",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🤖 智能客服系统")

# ── Session state initialization ─────────────────────────
if "file_loader" not in st.session_state:
    logger.info("=" * 50)
    logger.info("🚀 Session started - initializing modules")
    st.session_state.file_loader = FileLoader()
if "vector_store" not in st.session_state:
    t0 = time.time()
    st.session_state.vector_store = VectorStoreManager()
    logger.info(f"VectorStoreManager initialized in {time.time()-t0:.1f}s")
if "agent" not in st.session_state:
    t0 = time.time()
    st.session_state.agent = AgentManager(st.session_state.vector_store)
    logger.info(f"AgentManager initialized in {time.time()-t0:.1f}s")
if "memory" not in st.session_state:
    st.session_state.memory = MemoryManager()
    logger.info("MemoryManager initialized")
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []
    # Restore file list from persisted vector store (survives page refresh)
    existing = getattr(st.session_state.vector_store, "get_source_files", lambda: [])()
    for fname in existing:
        # Reconstruct a fake key — actual content is already in vector store
        st.session_state.uploaded_files.append(f"{fname}_0")
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Sidebar ──────────────────────────────────────────────
with st.sidebar:
    st.header("📁 文件上传")

    uploaded_files = st.file_uploader(
        "拖拽或点击上传文件",
        accept_multiple_files=True,
        type=["pdf", "docx", "txt", "md", "csv", "html", "htm", "png", "jpg", "jpeg"],
        key="file_uploader",
        help="支持 PDF、Word、TXT、Markdown、CSV、HTML、图片",
    )

    if uploaded_files:
        for f in uploaded_files:
            file_key = f"{f.name}_{f.size}"
            if file_key not in st.session_state.uploaded_files:
                logger.info(f"📤 New file: {f.name} ({f.size} bytes, type={f.type})")
                with st.spinner(f"处理中: {f.name}..."):
                    t0 = time.time()
                    file_path = st.session_state.file_loader.save_upload(f)
                    docs = st.session_state.file_loader.load_file(file_path)
                    st.session_state.vector_store.add_documents(docs)
                    st.session_state.uploaded_files.append(file_key)
                    elapsed = time.time() - t0
                    logger.info(f"✅ {f.name} → {len(docs)} chunks, {elapsed:.1f}s, "
                                f"total docs in store: {st.session_state.vector_store.count()}")
                st.toast(f"✅ {f.name} 已处理", icon="✅")

    if st.session_state.uploaded_files:
        with st.expander(f"📚 已上传 ({len(st.session_state.uploaded_files)} 个)", expanded=True):
            for fk in st.session_state.uploaded_files:
                fname = fk.rsplit("_", 1)[0]
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"📄 {fname}")
                with col2:
                    ext = fname.rsplit(".", 1)[-1].lower() if "." in fname else ""
                    if ext in ("docx", "xlsx"):
                        if st.button(f"✏️ 编辑", key=f"edit_btn_{fk}"):
                            # Find the actual file on disk (uuid8_ prefix)
                            upload_dir = Path(UPLOAD_DIR)
                            matches = sorted(upload_dir.glob(f"*_{fname}"))
                            if matches:
                                file_path = matches[0]
                                file_bytes = file_path.read_bytes()

                                # Write to Vite public/temp/ for same-origin fetch
                                session_id = uuid.uuid4().hex[:12]
                                temp_dir = Path(__file__).parent / "vue-word-editor" / "public" / "temp"
                                temp_dir.mkdir(parents=True, exist_ok=True)

                                dest_file = temp_dir / f"{session_id}.{ext}"
                                dest_file.write_bytes(file_bytes)

                                meta = {"fileName": fname, "fieldList": [
                                    {"id": "1", "name": "客户名称", "icon": "👤"},
                                    {"id": "2", "name": "合同金额", "icon": "💰"},
                                    {"id": "3", "name": "签订日期", "icon": "📅"},
                                    {"id": "4", "name": "产品名称", "icon": "📦"},
                                    {"id": "5", "name": "交付地点", "icon": "📍"},
                                ]}
                                (temp_dir / f"{session_id}.json").write_text(
                                    json.dumps(meta, ensure_ascii=False), encoding="utf-8")

                                editor_url = f"{VUE_EDITOR_URL}/?session={session_id}"
                                webbrowser.open(editor_url)
                                st.success(f"编辑器已在新标签页打开: {fname}")
                            else:
                                st.error(f"文件未找到: {fname}")

    if st.session_state.uploaded_files and st.button("🗑 清空全部", type="secondary"):
        logger.info("🗑 Clearing all files and resetting session")
        st.session_state.vector_store.clear()
        st.session_state.uploaded_files = []
        st.session_state.messages = []
        st.session_state.memory = MemoryManager()
        st.rerun()

    with st.expander("⚙️ 设置"):
        top_k = st.slider("检索数量", 1, 10, DEFAULT_TOP_K)
        st.caption(f"模型: {LLM_MODEL}")

    doc_count = st.session_state.vector_store.count()
    st.info(f"📊 已加载 {len(st.session_state.uploaded_files)} 个文件 | 向量库 {doc_count} 条记录")

# ── Main chat area ───────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("💬 输入你的问题..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        logger.info(f"👤 User asked: {prompt[:100]}...")
        t_start = time.time()

        with st.spinner("思考中..."):
            try:
                mem_vars = st.session_state.memory.load_memory_variables({})
                chat_history = mem_vars.get("history", [])
                logger.info(f"📝 Chat history: {len(chat_history)} messages")

                response_container = st.empty()
                full_response = ""
                chunk_count = 0
                for chunk in st.session_state.agent.stream_chat(prompt, chat_history):
                    full_response = chunk
                    chunk_count += 1
                    response_container.markdown(full_response)

                elapsed = time.time() - t_start
                logger.info(f"🤖 Response: {len(full_response)} chars, "
                            f"{chunk_count} streaming chunks, {elapsed:.1f}s total")

                # Show retrieved source documents below the response
                retrieved = getattr(st.session_state.agent, "last_retrieved_docs", [])
                if retrieved:
                    with st.expander("📄 检索到的原文内容", expanded=False):
                        for i, doc in enumerate(retrieved, 1):
                            src = doc.metadata.get("source", "unknown")
                            page = doc.metadata.get("page", "")
                            page_label = f" — 第{page}页" if page else ""
                            st.caption(f"来源 {i}: {src}{page_label}")
                            st.text(doc.page_content[:1000])
                            if i < len(retrieved):
                                st.divider()

                st.session_state.memory.save_context(
                    {"input": prompt},
                    {"output": full_response},
                )
                logger.info(f"💾 Saved to memory (total turns: {len(st.session_state.memory.chat_memory.messages)//2})")

                st.session_state.messages.append({"role": "assistant", "content": full_response})

            except Exception as e:
                elapsed = time.time() - t_start
                logger.error(f"❌ Error after {elapsed:.1f}s: {type(e).__name__}: {e}", exc_info=True)
                error_msg = f"⚠️ 出错了: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
