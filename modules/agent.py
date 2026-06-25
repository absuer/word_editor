"""LangGraph agent with retriever and web search tools."""
import logging
import time
from typing import List, Optional
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from modules.vector_store import VectorStoreManager
from config import LLM_MODEL, LLM_API_KEY, LLM_OPENAI_BASE_URL, DEFAULT_TOP_K

logger = logging.getLogger("intelligent-cs.agent")

SYSTEM_PROMPT = """你是一个智能客服助手。你可以：
1. 优先从用户上传的文档中检索答案
2. 文档不足时，使用 web_search 工具搜索网络（最多尝试 1 次，失败后直接告知用户而不是反复重试）
3. 礼貌地告知你不知道，而不是编造答案
4. 当搜索工具不可用时，直接说明"当前网络搜索暂时不可用，请稍后再试"，不要换关键词反复调用

规则：
- 回答时注明信息来源（文件名、页码）
- 使用中文回答
- 不要暴露系统内部细节
- web_search 失败后禁止再次调用，直接基于已有知识回答或告知无法搜索"""


def build_retriever_tool(vector_store: VectorStoreManager, results_sink: list = None):
    """Create a retriever tool bound to a specific vector store.

    Args:
        vector_store: The vector store to search.
        results_sink: Optional list to append raw Document results into (for UI display).
    """

    @tool
    def retriever(query: str) -> str:
        """Retrieve relevant documents from the user's uploaded files.
        Use this tool FIRST when the user asks about content that might be in their documents.
        Args:
            query: The search query string to find relevant documents.
        """
        t0 = time.time()
        logger.info(f"[retriever] Searching for: '{query[:80]}...' (k={DEFAULT_TOP_K})")
        docs = vector_store.search(query, k=DEFAULT_TOP_K)
        if not docs:
            logger.info(f"[retriever] No results found ({time.time()-t0:.2f}s)")
            return "未在已上传文档中找到相关内容。"

        # Store raw docs for UI display
        if results_sink is not None:
            results_sink.clear()
            results_sink.extend(docs)

        results = []
        for doc in docs:
            source = doc.metadata.get("source", "unknown")
            page = doc.metadata.get("page", "")
            page_info = f" (第{page}页)" if page else ""
            results.append(f"[来源: {source}{page_info}]\n{doc.page_content}")
        logger.info(f"[retriever] Found {len(docs)} docs: "
                    f"{[d.metadata.get('source','?') for d in docs]} ({time.time()-t0:.2f}s)")
        return "\n\n---\n\n".join(results)

    return retriever


def build_web_search_tool():
    """Create a web search tool using DuckDuckGo (html/lite backends, avoids Bing)."""

    @tool
    def web_search(query: str) -> str:
        """Search the web for information not found in uploaded documents.
        Use this tool ONLY when retriever returns no relevant results.
        Args:
            query: The search query string.
        """
        t0 = time.time()
        logger.info(f"[web_search] Searching web for: '{query[:80]}...'")

        def _format_results(results: list) -> str:
            return "\n\n".join(
                f"[来源: web] {r['title']}\n{r['body']}"
                for r in results
            )

        try:
            from duckduckgo_search import DDGS

            with DDGS(timeout=15) as ddgs:
                # Try html backend first (direct DDG, avoids Bing which is blocked in China)
                for backend_name, fetcher in [
                    ("html", ddgs._text_html),
                    ("lite", ddgs._text_lite),
                ]:
                    try:
                        results = fetcher(query, max_results=5)
                        if results:
                            logger.info(
                                f"[web_search] {backend_name} backend: {len(results)} results "
                                f"({time.time() - t0:.2f}s)"
                            )
                            return _format_results(results)
                    except Exception as inner_err:
                        logger.warning(f"[web_search] {backend_name} backend failed: {inner_err}")

                # Fallback: try the default text() method (uses bing, may not work)
                results = list(ddgs.text(query, max_results=5))
                if results:
                    logger.info(f"[web_search] default backend: {len(results)} results ({time.time()-t0:.2f}s)")
                    return _format_results(results)

                logger.info(f"[web_search] No results ({time.time()-t0:.2f}s)")
                return "未找到相关的网络搜索结果。"

        except Exception as e:
            logger.error(f"[web_search] Failed: {e}")
            return ("网络搜索服务暂时不可用。请告知用户当前无法连接搜索引擎（可能被限流或网络不通），"
                    "建议用户稍后再试，或直接基于你已有的知识回答问题。不要再重复调用 web_search。")

    return web_search


class AgentManager:
    """Manages the LangGraph agent lifecycle."""

    def __init__(self, vector_store: VectorStoreManager):
        self.vector_store = vector_store
        self.last_retrieved_docs = []  # populated by retriever tool
        logger.info(f"Initializing ChatOpenAI: model={LLM_MODEL}, base_url={LLM_OPENAI_BASE_URL}")
        self.llm = ChatOpenAI(
            model=LLM_MODEL,
            openai_api_key=LLM_API_KEY,
            openai_api_base=LLM_OPENAI_BASE_URL,
            temperature=0.3,
        )
        self.tools = [
            build_retriever_tool(vector_store, results_sink=self.last_retrieved_docs),
            build_web_search_tool(),
        ]
        logger.info(f"Creating ReAct agent with {len(self.tools)} tools: "
                    f"{[t.name for t in self.tools]}")
        self.agent = create_react_agent(
            model=self.llm,
            tools=self.tools,
            prompt=SYSTEM_PROMPT,
        )
        logger.info("Agent created successfully")

    def chat(self, message: str, chat_history: List = None) -> str:
        """Send a message to the agent and get the complete response."""
        config = {"configurable": {"thread_id": "default"}}
        inputs = {"messages": [("user", message)]}
        result = self.agent.invoke(inputs, config=config)

        # Log tool calls from the result messages
        for msg in result["messages"]:
            if hasattr(msg, "tool_calls") and msg.tool_calls:
                for tc in msg.tool_calls:
                    logger.info(f"[agent] Tool call: {tc.get('name', '?')}")

        for msg in reversed(result["messages"]):
            if hasattr(msg, "content") and msg.type == "ai":
                return msg.content
        return "抱歉，我无法回答这个问题。"

    def stream_chat(self, message: str, chat_history: List = None):
        """Stream the agent response token by token."""
        t0 = time.time()
        self.last_retrieved_docs.clear()
        config = {"configurable": {"thread_id": "default"}}
        inputs = {"messages": [("user", message)]}

        tool_count = 0
        for chunk in self.agent.stream(inputs, config=config, stream_mode="values"):
            if "messages" in chunk:
                last_msg = chunk["messages"][-1]
                # Log tool calls
                if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
                    for tc in last_msg.tool_calls:
                        tool_count += 1
                        logger.info(f"[agent] 🛠️ Invoking tool: {tc.get('name', '?')}")
                # Log tool results
                if hasattr(last_msg, "type") and last_msg.type == "tool":
                    result_preview = str(last_msg.content)[:100]
                    logger.info(f"[agent] 📋 Tool result: {result_preview}...")

                if hasattr(last_msg, "content") and last_msg.type == "ai":
                    yield last_msg.content

        logger.info(f"[agent] Stream completed: {tool_count} tool calls, {time.time()-t0:.1f}s total")
