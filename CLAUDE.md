# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run the Streamlit app
streamlit run app.py

# Run all tests (pytest discovers tests/ automatically)
pytest tests/

# Run a single test file
pytest tests/test_agent.py

# Run a specific test function or class
pytest tests/test_agent.py::TestTools::test_retriever_tool_has_correct_name

# Install dependencies
pip install -r requirements.txt
```

## Architecture

This is a **RAG-powered intelligent customer service system (智能客服系统)** built with Streamlit + LangChain/LangGraph + ChromaDB.

### Data flow

```
User uploads file → FileLoader (parse + chunk) → VectorStoreManager (Chroma + HuggingFace embeddings)
                                                                          ↓
User asks question → AgentManager (LangGraph ReAct agent) ←── retriever tool (search Chroma)
                                              ↓                        ↓
                                         web_search tool (DuckDuckGo fallback)
                                              ↓
                                         MemoryManager (buffer window) ←→ Streamlit session_state
```

### Key components

- **`app.py`** — Streamlit UI. Manages uploads, chat display, and session state. Uploaded files are tracked by `f"{name}_{size}"` key to prevent duplicates. Logs go to `data/app.log` and are viewable in the sidebar.
- **`config.py`** — All configuration from env vars. Uses `python-dotenv` to load `.env`. The LLM base URL points to DeepSeek's **OpenAI-compatible endpoint** (`/v1`), not Anthropic's native API.
- **`modules/file_loader.py`** — `FileLoader` handles 7 formats (PDF, DOCX, TXT, MD, CSV, HTML, images via OCR). Uses `RecursiveCharacterTextSplitter` with Chinese-aware separators (`\n\n`, `\n`, `。`, `.`, ` `). Adds `source`, `file_type`, `chunk_index`, `upload_time` metadata to every chunk.
- **`modules/vector_store.py`** — `VectorStoreManager` wraps ChromaDB with `HuggingFaceEmbeddings` (`paraphrase-multilingual-MiniLM-L12-v2`) running locally on CPU. Uses **lazy initialization**: the Chroma client is only created on first access via `self.store` property. Always call `store.close()` in tests to release resources.
- **`modules/agent.py`** — `AgentManager` creates a LangGraph ReAct agent via `create_react_agent`. The LLM is `ChatOpenAI` (not Anthropic SDK) pointed at DeepSeek's `/v1` endpoint. Two tools: `retriever` (document search, used first) and `web_search` (DuckDuckGo, used as fallback). System prompt is in Chinese. `stream_chat()` streams in `"values"` mode, yielding the full response text each time the AI message updates.
- **`modules/memory.py`** — Thin wrapper around `ConversationBufferWindowMemory` (default `k=4`). Stores conversation turns in Streamlit session state.

### Tests

Tests in `tests/` use `pytest` and create temporary directories with `tempfile.TemporaryDirectory` for isolation. Vector stores in tests must call `store.close()` in a `finally` block to release ChromaDB file locks. The e2e test (`test_e2e.py`) validates the full pipeline: file load → vector store → search → agent creation → memory.

### Config notes

- `.env` is gitignored. The app requires `ANTHROPIC_AUTH_TOKEN` (the API key), `ANTHROPIC_BASE_URL`, and `ANTHROPIC_MODEL` env vars to be set.
- Despite the `ANTHROPIC_` prefix, the actual protocol is OpenAI-compatible — `ChatOpenAI` talks to the `/v1` endpoint of DeepSeek.
- ChromaDB persists to `data/chroma_db/`. Uploaded files are saved to `data/uploads/`. Both directories are gitignored.
