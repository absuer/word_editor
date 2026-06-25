"""Configuration for the intelligent customer service system."""
import os
from dotenv import load_dotenv

load_dotenv()

# LLM & Embedding
LLM_MODEL = os.getenv("ANTHROPIC_MODEL", "deepseek-v4-pro")
LLM_API_KEY = os.getenv("ANTHROPIC_AUTH_TOKEN", "")
LLM_BASE_URL = os.getenv("ANTHROPIC_BASE_URL", "https://api.deepseek.com/anthropic")
LLM_OPENAI_BASE_URL = "https://api.deepseek.com/v1"  # OpenAI-compatible endpoint

# Chroma
CHROMA_PERSIST_DIR = os.path.join(os.path.dirname(__file__), "data", "chroma_db")
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "data", "uploads")

# Chunking
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150

# Retrieval
DEFAULT_TOP_K = 4

# Memory
MEMORY_MAX_TOKEN_LIMIT = 4000
MEMORY_KEEP_RECENT = 4

# Vue Word Editor
VUE_EDITOR_URL = os.getenv("VUE_EDITOR_URL", "http://localhost:5173")
