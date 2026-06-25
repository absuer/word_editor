# intelligent-cs-intro - Design Spec

> Human-readable design narrative — rationale, audience, style, color choices, content outline. Read once by downstream roles for context.
>
> Machine-readable execution contract: `spec_lock.md` (color / typography / icon / image short form). Executor re-reads `spec_lock.md` before every SVG page to resist context-compression drift. Keep both in sync; on divergence, `spec_lock.md` wins.

## I. Project Information

| Item | Value |
| ---- | ----- |
| **Project Name** | intelligent-cs-intro |
| **Canvas Format** | PPT 16:9 (1280×720) |
| **Page Count** | 12 |
| **Design Style** | dark-tech — deep navy canvas with cyan/purple glow accents |
| **Target Audience** | 技术人员（开发者/架构师）、项目决策者、潜在用户 |
| **Use Case** | 项目介绍 / 技术宣讲 / 团队内部分享 |
| **Created Date** | 2026-06-14 |

---

## II. Canvas Specification

| Property | Value |
| -------- | ----- |
| **Format** | PPT 16:9 |
| **Dimensions** | 1280×720 |
| **viewBox** | `0 0 1280 720` |
| **Margins** | left/right 60px, top/bottom 50px |
| **Content Area** | 1160×620 |

---

## III. Visual Theme

### Theme Style

- **Mode**: briefing — neutral, complete, scannable tech overview with topic titles and even treatment
- **Visual style**: dark-tech — dark canvas, luminous cyan/purple accents, geometric precision, glow elevation
- **Theme**: Dark theme
- **Tone**: 专业、现代、科技感、精密

### Color Scheme

| Role | HEX | Purpose |
| ---- | --- | ------- |
| **Background** | `#0A0E27` | Page background (deep navy) |
| **Secondary bg** | `#131837` | Card background, section background |
| **Surface** | `#1A1F3D` | Panel lift, elevated containers |
| **Primary** | `#00D4FF` | Title decorations, key sections, icons, glow accents |
| **Accent** | `#7C5CFC` | Data highlights, key information, secondary glow |
| **Secondary accent** | `#FF6B9D` | Secondary emphasis, gradient transitions, rare highlights |
| **Body text** | `#E8E8F0` | Main body text on dark background |
| **Secondary text** | `#A0A4B8` | Captions, annotations, page numbers |
| **Border/divider** | `#2A2E45` | Card borders, divider lines |
| **Grid** | `#1E2244` | Fine grid lines, chart grids |
| **Scrim** | `#0A0E27` | Image overlay for text legibility |
| **Success** | `#00E676` | Positive indicators |
| **Warning** | `#FF5252` | Issue markers |

### AI Image Strategy

- **Image Rendering**: digital-dashboard
- **Image Palette**: tech-neon

### Gradient Scheme

```xml
<!-- Title gradient -->
<linearGradient id="titleGradient" x1="0%" y1="0%" x2="100%" y2="100%">
  <stop offset="0%" stop-color="#00D4FF"/>
  <stop offset="100%" stop-color="#7C5CFC"/>
</linearGradient>

<!-- Background decorative gradient -->
<radialGradient id="bgDecor" cx="80%" cy="20%" r="50%">
  <stop offset="0%" stop-color="#00D4FF" stop-opacity="0.08"/>
  <stop offset="100%" stop-color="#00D4FF" stop-opacity="0"/>
</radialGradient>

<!-- Card glow gradient -->
<linearGradient id="cardGlow" x1="0%" y1="0%" x2="100%" y2="100%">
  <stop offset="0%" stop-color="#00D4FF" stop-opacity="0.06"/>
  <stop offset="100%" stop-color="#7C5CFC" stop-opacity="0.03"/>
</linearGradient>
```

---

## IV. Typography System

### Font Plan

**Typography direction**: clean modern CJK sans — 统一无衬线，简洁现代

| Role | Chinese | English | Fallback tail |
| ---- | ------- | ------- | ------------- |
| **Title** | `"Microsoft YaHei", "PingFang SC"` | `Arial` | `sans-serif` |
| **Body** | `"Microsoft YaHei", "PingFang SC"` | `Arial` | `sans-serif` |
| **Emphasis** | same as Body | `Arial` | `sans-serif` |
| **Code** | — | `Consolas, "Courier New"` | `monospace` |

**Per-role font stacks** (CSS `font-family` strings):

- Title: `"Microsoft YaHei", "PingFang SC", Arial, sans-serif`
- Body: `"Microsoft YaHei", "PingFang SC", Arial, sans-serif`
- Emphasis: same as Body
- Code: `Consolas, "Courier New", monospace`

### Font Size Hierarchy

**Baseline**: Body font size = 22px (medium density, suitable for tech content with moderate text volume)

| Purpose | Ratio to body | px (@ body=22) | Weight |
| ------- | ------------- | -------------- | ------ |
| Cover title (hero headline) | 2.5-5x | 55-110px | Bold |
| Chapter / section opener | 2-2.5x | 44-55px | Bold |
| Page title | 1.5-2x | 33-44px | Bold |
| Hero number (consulting KPIs) | 1.5-2x | 33-44px | Bold |
| Subtitle | 1.2-1.5x | 26-33px | SemiBold |
| **Body content** | **1x** | **22px** | Regular |
| Annotation / caption | 0.7-0.85x | 15-19px | Regular |
| Page number / footnote | 0.5-0.65x | 11-14px | Regular |

Formula rendering policy: `text-only` (no formulas in this deck)

---

## V. Layout Principles

### Page Structure

- **Header area**: Top 80px — page title with decorative accent line, 60px margins
- **Content area**: 80px to 680px — main content zone, 600px height
- **Footer area**: Bottom 40px — page number (right-aligned), optional section label (left-aligned)

### Layout Pattern Library

| Pattern | Suitable Scenarios |
| ------- | ----------------- |
| **Single column centered** | Cover (P01), Ending (P12) |
| **Symmetric split (5:5)** | Comparisons, dual-module overview (P08) |
| **Asymmetric split (3:7 / 2:8)** | Architecture diagram + description (P05) |
| **Top-bottom split** | Data flow pipeline (P06) |
| **Three/four column cards** | Tech stack (P04), Features (P10), Core modules (P07) |
| **Matrix grid (2×2)** | Module overview grid (P09 memory context) |
| **Z-pattern / waterfall** | Process storytelling |
| **Full-bleed + floating text** | Cover (P01) with AI background |
| **Negative-space-driven** | Summary page (P12) |

### Spacing Specification

**Universal**:

| Element | Recommended Range | Current Project |
| ------- | ---------------- | --------------- |
| Safe margin from canvas edge | 40-60px | 60px |
| Content block gap | 24-40px | 32px |
| Icon-text gap | 8-16px | 12px |

**Card-based layouts**:

| Element | Value |
| ------- | ----- |
| Card gap | 24px |
| Card padding | 28px |
| Card border radius | 8px |
| Single-row card height | 540px |
| Three-column card width | 360px |

**Non-card containers**:

- Line-height: ~1.6× for body text, ~1.4× for annotations
- Block gap: 36px between content sections
- Divider lines: 1px `#2A2E45` with 16px vertical spacing

---

## VI. Icon Usage Specification

### Source

- **Built-in icon library**: `templates/icons/phosphor-duotone/` — duotone style, main shape + 20% opacity backplate, medium weight, layered contemporary
- **Usage method**: SVG placeholder `<use data-icon="phosphor-duotone/icon-name" .../>`

### Recommended Icon List

| Purpose | Icon Path | Page |
| ------- | --------- | ---- |
| 智能客服/机器人 | `phosphor-duotone/robot` | P01, P03 |
| 文档处理 | `phosphor-duotone/file-doc` | P04, P07 |
| 向量数据库 | `phosphor-duotone/database` | P04, P08 |
| 搜索引擎 | `phosphor-duotone/magnifying-glass` | P06, P08 |
| 数据分析 | `phosphor-duotone/chart-bar` | P10 |
| 代码/技术 | `phosphor-duotone/code` | P04, P11 |
| 配置 | `phosphor-duotone/gear` | P11 |
| 功能特性 | `phosphor-duotone/check-circle` | P10 |
| 终端命令 | `phosphor-duotone/terminal-window` | P11 |
| 网络搜索 | `phosphor-duotone/globe-hemisphere-east` | P06, P08 |
| 系统架构 | `phosphor-duotone/tree-structure` | P05 |
| AI/智能 | `phosphor-duotone/brain` | P03, P08 |
| 文件上传 | `phosphor-duotone/cloud-arrow-up` | P06 |
| 亮点 | `phosphor-duotone/rocket` | P10 |
| 安全可靠 | `phosphor-duotone/shield-check` | P10 |
| 集成 | `phosphor-duotone/puzzle-piece` | P03 |
| CPU/处理 | `phosphor-duotone/cpu` | P04 |
| 用户 | `phosphor-duotone/users-three` | P09 |
| 文件夹 | `phosphor-duotone/folder-simple` | P07 |
| 灯泡/洞察 | `phosphor-duotone/lightbulb` | P08 |
| 分层架构 | `phosphor-duotone/stack` | P05 |
| Git | `phosphor-duotone/git-branch` | P11 |
| 书籍/文档 | `phosphor-duotone/book-open` | P07 |
| 列表 | `phosphor-duotone/list-checks` | P02 |
| 信息 | `phosphor-duotone/info` | P03 |
| 内存/记忆 | `phosphor-duotone/cpu` | P09 |

---

## VII. Visualization Reference List

Catalog read: 71 templates

| Page | Template | Path | Summary-quote (verbatim from `charts_index.json`) | Usage |
| ---- | -------- | ---- | ------------------------------------------------- | ----- |
| P04 | icon_grid | `templates/charts/icon_grid.svg` | "Pick for 4-9 parallel features/capabilities/services as icon cards — feature grid, service lineup, benefits matrix, brand values, product highlights. Skip for sequential ordering (use numbered_steps) or hierarchical layers (use pyramid_chart)." | 8 tech stack items displayed as icon cards |
| P05 | layered_architecture | `templates/charts/layered_architecture.svg` | "Pick for 3-4 horizontal architecture layers (presentation/service/data), 2-4 module cards per layer, each card = title + 1-line description (description required, even if source brief). Skip if no per-module descriptions (use icon_grid) or no horizontal layering (use module_composition)." | 3-layer system architecture: UI → Agent → Storage |
| P06 | pipeline_with_stages | `templates/charts/pipeline_with_stages.svg` | "Pick for 3-5 horizontal pipeline stages, each = title + 1-line description + output artifact, connected by arrows (data pipelines, ETL, build pipelines). Skip if any stage lacks an artifact (use process_flow or numbered_steps)." | 4-stage data processing pipeline |

**Runners-up considered** (3 entries minimum):

- `process_flow` | rejected for P06: pipeline stages have clear output artifacts (chunks, vectors, answers) — `pipeline_with_stages` captures this better
- `module_composition` | rejected for P05: system has distinct horizontal layers (presentation/agent/storage), not just one parent container
- `numbered_steps` | rejected for P06: data flow is a pipeline, not just numbered sequential steps without interconnections

---

## VIII. Image Resource List

| Filename | Dimensions | Ratio | Purpose | Type | Layout pattern | Acquire Via | Status | Reference | text_policy | page_role |
| -------- | --------- | ----- | ------- | ---- | -------------- | ----------- | ------ | --------- | ----------- | --------- |
| cover_bg.png | 1280×720 | 1.78 | Atmospheric tech cover backdrop — SVG title and subtitle float over calm dark region | Background | #1 full-bleed background with floating title + #29 two-stop scrim | ai | Pending | Futuristic AI/data center abstract — flowing cyan and purple light streams across a dark navy field, subtle hexagonal grid pattern at low opacity, calm central upper zone reserved for title overlay, luminous particles scattered at edges | none | hero_page |
| architecture_bg.png | 1280×720 | 1.78 | Subtle tech texture backdrop for system architecture page — low-contrast atmosphere behind layered diagram | Background | #44 background image + native network/architecture diagram | ai | Pending | Abstract tech network mesh on deep navy, subtle connected nodes with faint cyan glow lines, low contrast and minimal detail so SVG architecture diagram reads clearly on top, dark gradient at edges fading to canvas background | none | local |

---

## IX. Content Outline

> Mode: briefing — topic titles, even treatment, complete coverage for scanning and lookup.

### Part 1: 项目介绍 (Project Introduction)

#### P01 — 封面 (Cover)

- **Rhythm**: `anchor`
- **Layout**: Full-bleed AI background image + centered title overlay
- **Title**: 🤖 智能客服系统
- **Subtitle**: 基于 RAG 的智能问答平台 — 技术架构解析
- **Info**: 2026.06

#### P02 — 目录 (Agenda)

- **Rhythm**: `breathing`
- **Layout**: Single column numbered list with icons
- **Title**: 目录
- **Core message**: 本次分享涵盖项目概述、技术栈、系统架构、核心模块、运行部署五大板块
- **Content**: numbered agenda items:
  - 01 / 项目概述
  - 02 / 技术栈一览
  - 03 / 系统架构总览
  - 04 / 数据处理流程
  - 05 / 核心模块解析
  - 06 / 运行与部署
  - 07 / 总结

#### P03 — 项目概述 (Project Overview)

- **Rhythm**: `dense`
- **Layout**: Left text description + right feature badges
- **Title**: 项目概述
- **Core message**: 智能客服系统是一个基于 RAG（检索增强生成）架构的智能问答平台，支持多格式文档上传、语义检索与联网回退
- **Content**:
  - 基于 RAG（Retrieval-Augmented Generation）架构，将用户上传的文档作为知识库，结合大语言模型进行智能问答
  - 支持 PDF、DOCX、TXT、Markdown、CSV、HTML、图片（OCR）共 7 种文件格式
  - 优先从文档中检索答案；文档不足时自动回退至 DuckDuckGo 网络搜索
  - 多轮对话记忆，保持上下文连贯
- **Visualization**: none

---

### Part 2: 技术架构 (Technical Architecture)

#### P04 — 技术栈一览 (Tech Stack)

- **Rhythm**: `dense`
- **Layout**: 2×4 icon card grid
- **Title**: 技术栈一览
- **Core message**: 系统基于 Streamlit + LangChain/LangGraph + ChromaDB 三大核心技术栈构建
- **Content**: 8 tech items as icon cards:
  - Streamlit / 前端框架 / Web UI + 会话管理
  - LangChain + LangGraph / Agent 框架 / ReAct agent + tool orchestration
  - ChromaDB / 向量数据库 / 文档嵌入存储与相似度检索
  - HuggingFace Embeddings / 嵌入模型 / paraphrase-multilingual-MiniLM-L12-v2 (CPU 本地运行)
  - DeepSeek LLM / 大语言模型 / DeepSeek-v4-pro via OpenAI-compatible API
  - DuckDuckGo Search / 网络搜索 / 文档外知识回退查询
  - python-dotenv / 配置管理 / 环境变量与密钥安全
  - pytest / 测试框架 / 全流程端到端测试
- **Visualization**: `icon_grid`

#### P05 — 系统架构总览 (System Architecture)

- **Rhythm**: `dense`
- **Layout**: Asymmetric split — architecture diagram on left (70%), description on right (30%)
- **Title**: 系统架构总览
- **Core message**: 系统采用三层水平架构：展示层 (Streamlit UI) → 代理层 (LangGraph ReAct Agent) → 存储层 (ChromaDB + 文件系统)
- **Content**:
  - **展示层 (Presentation)**: Streamlit Web UI — 文件上传、聊天界面、会话状态管理、侧边栏设置
  - **代理层 (Agent)**: LangGraph ReAct Agent — retriever 工具（文档检索）+ web_search 工具（联网回退）+ MemoryManager（对话记忆）
  - **存储层 (Storage)**: ChromaDB 向量库 + HuggingFace Embeddings + FileLoader 多格式解析
- **Visualization**: `layered_architecture`

#### P06 — 数据处理流程 (Data Flow)

- **Rhythm**: `dense`
- **Layout**: Top-bottom split — pipeline diagram at top, description at bottom
- **Title**: 数据处理流程
- **Core message**: 从文件上传到智能回答，数据经四个阶段流转：上传 → 解析分块 → 向量化存储 → 检索生成
- **Content**: 4-stage pipeline:
  - Stage 1: 文件上传 — 用户上传文件到 data/uploads/ (去重 key: name_size)
  - Stage 2: 解析分块 — FileLoader 自动识别格式，RecursiveCharacterTextSplitter 中文感知分割 (chunk=1000, overlap=150)
  - Stage 3: 向量化存储 — HuggingFace Embeddings → ChromaDB 持久化到 data/chroma_db/
  - Stage 4: 检索生成 — retriever 优先检索文档 → web_search 回退 → LLM 流式生成回答
- **Visualization**: `pipeline_with_stages`

---

### Part 3: 核心模块 (Core Modules)

#### P07 — 核心模块：文件加载器 (FileLoader)

- **Rhythm**: `dense`
- **Layout**: Three-column cards — supported formats / chunking strategy / metadata
- **Title**: 文件加载器 · FileLoader
- **Core message**: FileLoader 支持 7 种格式自动检测与解析，采用中文感知的分块策略，为每个分块注入完整元数据
- **Content**:
  - 7 种格式支持: PyPDFLoader (PDF), Docx2txtLoader (DOCX), TextLoader (TXT), CSVLoader (CSV), UnstructuredMarkdownLoader (MD), WebBaseLoader (HTML), OCR via pytesseract (图片)
  - 智能分块: RecursiveCharacterTextSplitter, chunk_size=1000, chunk_overlap=150, 中文分隔符: \n\n → \n → 。→ . → 空格
  - 完整元数据: source (文件名), file_type (格式), chunk_index (序号), upload_time (上传时间) — 每个分块可溯源
- **Visualization**: none

#### P08 — 核心模块：向量存储 + 智能代理 (VectorStore & Agent)

- **Rhythm**: `dense`
- **Layout**: Symmetric split — left: VectorStore, right: Agent
- **Title**: 向量存储 & 智能代理 · VectorStore & Agent
- **Core message**: VectorStore 提供基于 ChromaDB 的语义检索，Agent 通过 LangGraph ReAct 编排 retriever + web_search 双工具协同
- **Content** (left):
  - ChromaDB + HuggingFace Embeddings (paraphrase-multilingual-MiniLM-L12-v2)
  - 懒加载初始化, 去重逻辑, 本地 CPU 运行
  - similarity_search(query, k=4), get_source_files() 页面刷新恢复
- **Content** (right):
  - LangGraph create_react_agent + ChatOpenAI (DeepSeek /v1 endpoint)
  - 双工具: retriever（文档优先）→ web_search（DuckDuckGo 回退）
  - values 模式流式输出, 记录检索来源 (文件名+页码)
- **Visualization**: none

#### P09 — 核心模块：记忆管理 (MemoryManager)

- **Rhythm**: `dense`
- **Layout**: 2×2 grid — concept / implementation / conversation flow / config
- **Title**: 记忆管理 · MemoryManager
- **Core message**: ConversationBufferWindowMemory 保持最近 4 轮对话上下文，实现多轮连贯问答
- **Content**:
  - 滑动窗口记忆: k=4 (MEMORY_KEEP_RECENT), 保留最近 4 轮对话
  - 回合式存储: save_context({"input": ...}, {"output": ...}) 逐轮保存
  - 透传注入: load_memory_variables() → Agent stream_chat() 将历史注入 prompt
  - 配置灵活: MEMORY_MAX_TOKEN_LIMIT=4000, session_state 持久化
- **Visualization**: none

---

### Part 4: 总结 (Summary)

#### P10 — 核心特性与亮点 (Key Features)

- **Rhythm**: `dense`
- **Layout**: 3×2 feature cards grid
- **Title**: 核心特性与亮点
- **Core message**: 六大核心优势：多格式支持、中文优化、智能回退、流式响应、去重机制、可溯源回答
- **Content**: 6 feature cards:
  - 📁 多格式支持 / 7 种文件格式一键上传，含图片 OCR
  - 🇨🇳 中文深度优化 / 中文感知分块 + 多语言嵌入模型
  - 🔄 智能回退 / 文档不足时自动联网搜索，无感切换
  - ⚡ 流式响应 / LangGraph values 模式实时流式输出
  - 🛡 去重与持久化 / 文件名+大小去重，ChromaDB 持久化存储
  - 📎 可溯源 / 每个回答附来源文件名与页码，可信可查
- **Visualization**: `icon_grid`

#### P11 — 运行与部署 (Run & Deploy)

- **Rhythm**: `dense`
- **Layout**: Top-bottom — commands at top, config table at bottom
- **Title**: 运行与部署
- **Core message**: 一条命令启动，灵活配置环境变量，pytest 全流程测试覆盖
- **Content**:
  - 启动命令: `streamlit run app.py`
  - 测试命令: `pytest tests/` (e2e + unit tests, temporary directory isolation)
  - 安装依赖: `pip install -r requirements.txt`
  - 环境配置: .env 文件 (ANTHROPIC_AUTH_TOKEN / ANTHROPIC_BASE_URL / ANTHROPIC_MODEL)
  - LLM 端点: DeepSeek OpenAI-compatible /v1 (ChatOpenAI 协议)
  - 数据持久化: data/chroma_db/ (向量库) + data/uploads/ (原始文件) + data/app.log (日志)
- **Visualization**: none

#### P12 — 总结 (Summary)

- **Rhythm**: `anchor`
- **Layout**: Single column centered with large text
- **Title**: 总结
- **Core message**: 智能客服系统 = RAG + LangGraph Agent + ChromaDB，轻量高效、即装即用
- **Content**:
  - Streamlit Web 界面，开箱即用
  - 7 种格式 × 中文优化分块 × 本地嵌入
  - ReAct Agent 双工具编排，智能回退
  - 全流程可溯源，适合企业知识库问答场景
  - GitHub: [项目仓库]
- **Visualization**: none

---

## X. Speaker Notes Requirements

- **Filename**: match SVG name (e.g., `notes/01_cover.md`)
- **Style**: 正式讲解型，中文，每页 3-5 句要点提示
- **Total duration**: ~15-20 minutes
- **Purpose**: inform — 向技术听众系统介绍项目架构与实现

---

## XI. Technical Constraints Reminder

### SVG Generation Must Follow:

1. viewBox: `0 0 1280 720`
2. Background uses `<rect>` elements
3. Text wrapping uses `<tspan>` (`<foreignObject>` FORBIDDEN)
4. Transparency uses `fill-opacity` / `stroke-opacity`; `rgba()` FORBIDDEN
5. FORBIDDEN: `mask`, `<style>`, `class`, `foreignObject`
6. FORBIDDEN: `textPath`, `animate*`, `script`
7. Text characters: write typography & symbols as raw Unicode; HTML named entities FORBIDDEN. XML reserved chars in text MUST be escaped as `&amp;` `&lt;` `&gt;` `&quot;` `&apos;`
8. `marker-start` / `marker-end` conditionally allowed
9. `clipPath` conditionally allowed **only on `<image>` elements**

### PPT Compatibility Rules:

- `<g opacity="...">` FORBIDDEN; set opacity on each child element individually
- Image transparency uses overlay mask layer
- Inline styles only; external CSS and `@font-face` FORBIDDEN
