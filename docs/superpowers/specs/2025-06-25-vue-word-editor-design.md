# Vue Online Word 编辑器 — 设计文档

**日期**: 2025-06-25  
**状态**: 设计完成，待审核  
**参考项目**: [ranuts/document](https://github.com/ranuts/document)

---

## 1. 概述

构建一个基于 Vue 3 + OnlyOffice Web SDK 的在线 Word/Excel 编辑器，嵌入到现有 Streamlit 智能客服系统中。用户上传 .docx 或 .xlsx 文件后进行在线编辑，编辑完成后可下载。

### 核心需求

1. **100% 文档还原** — 上传的文件和显示的内容完全一致（格式、排版、字体、颜色等）
2. **Word + Excel 支持** — 根据文件扩展名自动切换编辑器
3. **80/20 分栏布局** — 编辑器占 80%，右侧字段列表面板占 20%
4. **字段插入** — 点击右侧字段项，将 `{{ 字段名 }}` 插入编辑器光标位置
5. **嵌入 Streamlit** — 通过 iframe 嵌入，base64 传递文件内容

---

## 2. 技术选型

| 技术 | 用途 | 协议 |
|------|------|------|
| Vue 3 (Composition API) | 应用壳框架 | MIT |
| Vite | 构建工具 | MIT |
| OnlyOffice Web SDK (@onlyoffice/document-editor) | Word/Excel 原生编辑引擎 | AGPL-3.0 |
| Vitest | 单元测试 | MIT |
| TypeScript | 类型安全 | — |

### 选型理由

- **OnlyOffice** — 唯一能在浏览器中 100% 还原 Word/Excel 格式的方案，ranuts/document 已验证可行
- **Vue 3** — 做壳的理想选择，负责布局、字段面板、通信桥接
- **纯前端** — 编辑器在浏览器本地运行，无需后端服务；Streamlit 仅做文件上传/下载的中转

---

## 3. 架构

### 3.1 整体架构

```
┌─────────────────────────────────────────────────┐
│  Streamlit (app.py)                              │
│  - 文件上传 (st.file_uploader)                   │
│  - base64 编码 → 注入 iframe                     │
│  - 接收编辑结果 → st.download_button             │
│  - 字段列表注入                                  │
├─────────────────────────────────────────────────┤
│  Vue 3 壳 (iframe 内)                            │
│  ┌──────────────────────┬──────────────────────┐ │
│  │  EditorPanel (80%)   │  FieldPanel (20%)    │ │
│  │  ┌────────────────┐  │  ┌────────────────┐  │ │
│  │  │ TitleBar       │  │  │ FieldSearch    │  │ │
│  │  │ (文件名+下载)  │  │  │ (搜索框)       │  │ │
│  │  ├────────────────┤  │  ├────────────────┤  │ │
│  │  │                │  │  │ FieldList      │  │ │
│  │  │ OnlyOffice     │  │  │ (字段列表)     │  │ │
│  │  │ iframe         │  │  │ 点击 → 插入    │  │ │
│  │  │ (原生编辑器)   │  │  └────────────────┘  │ │
│  │  └────────────────┘  │                      │ │
│  └──────────────────────┴──────────────────────┘ │
└─────────────────────────────────────────────────┘
```

### 3.2 数据流

```
① 上传: Streamlit 读文件 bytes → base64 → 注入 Vue iframe URL params
② 加载: Vue 接收 → useOnlyOffice.openDocument(base64, format) → OnlyOffice 渲染
③ 编辑: 用户在 OnlyOffice 内编辑，所有修改在浏览器本地
④ 插字段: 用户点字段面板 → postMessage → OnlyOffice API 插入 {{ 字段名 }}
⑤ 下载: 用户点下载 → OnlyOffice save() → base64 → postMessage → Vue → Streamlit → download
```

### 3.3 通信协议

| 方向 | 通道 | 数据格式 |
|------|------|----------|
| Streamlit → Vue | `window.parent.postMessage`（Streamlit 侧发到 iframe） | `{ type: 'init', fileBase64: string, fileName: string, fieldList: Field[] }` |
| Vue → OnlyOffice | postMessage（OnlyOffice API） | OnlyOffice API 调用 |
| OnlyOffice → Vue | postMessage 回调 | `{ status: string, data?: string }` |
| Vue → Streamlit | `window.parent.postMessage`（iframe 回传父窗口） | `{ type: 'download', fileBase64: string, fileName: string }` |

> **注意**: 文件内容通过 postMessage 传递 base64，避免 URL 长度限制。小文件亦可用 URL query params 作为备选。

---

## 4. 组件树

```
App.vue                         # 80/20 分栏容器 (display: flex)
├── EditorPanel.vue             # 左侧 80%
│   ├── TitleBar.vue            # 标题栏：文件图标 + 文件名 + 下载按钮
│   └── OnlyOffice 挂载点       # 动态创建/销毁 OnlyOffice iframe
└── FieldPanel.vue              # 右侧 20%
    ├── FieldSearch.vue         # 搜索框（本地筛选）
    └── FieldList.vue           # 字段列表
        └── FieldItem.vue       # 单个字段项（图标 + 名称 + {{ }} 标记）
```

### 组件职责

**App.vue** — 顶层容器，管理编辑器类型（Word/Excel）切换，持有全局状态。

**EditorPanel.vue** — 管理 OnlyOffice 生命周期（初始化、加载文档、销毁）。根据文件扩展名传正确的 `documentType` 给 OnlyOffice。

**TitleBar.vue** — Props: `fileName`。Emit: `download`。深色背景，显示文件类型图标 + 文件名 + 绿色下载按钮。

**FieldPanel.vue** — 接收 `fieldList` prop。管理搜索过滤状态。

**FieldList.vue** — 渲染字段项。Emit: `insert(field)`。点击某项触发插入。

**FieldItem.vue** — 单个字段展示：emoji 图标 + 字段名 + 灰色 `{{ }}` 标记。hover 高亮，点击触发 `insert`。

---

## 5. 核心模块

### 5.1 useOnlyOffice.ts

OnlyOffice 生命周期管理的 composable：

```typescript
// 伪代码
function useOnlyOffice(mountEl: Ref<string>) {
  const docEditor = ref(null)

  async function init(config: OnlyOfficeConfig)     // 初始化编辑器
  function openDocument(data: DocData)              // 加载文档
  function getContent(): Promise<base64>            // 获取编辑结果
  function insertText(text: string)                 // 在光标处插入文本
  function destroy()                                // 销毁实例

  return { init, openDocument, getContent, insertText, destroy }
}
```

### 5.2 useStreamlitBridge.ts

与 Streamlit 通信的 composable：

```typescript
function useStreamlitBridge() {
  const fileData = ref<FileData | null>(null)
  const fieldList = ref<Field[]>([])

  function receiveFromStreamlit()    // 从 URL/JS bridge 解析数据
  function sendToStreamlit(data)     // 回传编辑结果

  return { fileData, fieldList, receiveFromStreamlit, sendToStreamlit }
}
```

### 5.3 useFieldManager.ts

字段列表状态管理：

```typescript
function useFieldManager(initialFields: Field[]) {
  const fields = ref<Field[]>(initialFields)
  const searchQuery = ref('')

  const filteredFields = computed(() => /* 按 searchQuery 筛选 */)

  function insertField(field: Field) // 调用 useOnlyOffice.insertText(`{{ ${field.name} }}`)

  return { fields, searchQuery, filteredFields, insertField }
}
```

---

## 6. 项目结构

```
vue-word-editor/
├── package.json
├── vite.config.ts
├── tsconfig.json
├── index.html
├── src/
│   ├── main.ts
│   ├── App.vue
│   ├── components/
│   │   ├── TitleBar.vue
│   │   ├── EditorPanel.vue
│   │   └── field/
│   │       ├── FieldPanel.vue
│   │       ├── FieldSearch.vue
│   │       ├── FieldList.vue
│   │       └── FieldItem.vue
│   ├── composables/
│   │   ├── useOnlyOffice.ts
│   │   ├── useStreamlitBridge.ts
│   │   └── useFieldManager.ts
│   ├── types/
│   │   └── index.ts
│   └── assets/
│       └── styles.css
├── dist/                            # Vite build 输出
└── tests/
    ├── FieldPanel.spec.ts
    ├── useOnlyOffice.spec.ts
    └── useStreamlitBridge.spec.ts
```

---

## 7. 类型定义

```typescript
// types/index.ts

interface Field {
  id: string
  name: string        // 字段名称，如 "客户名称"
  icon?: string       // emoji 图标，如 "👤"
}

interface FileData {
  base64: string
  fileName: string
  format: 'docx' | 'xlsx'
}

interface OnlyOfficeConfig {
  documentType: 'word' | 'cell'
  height: string
  width: string
}

interface StreamlitMessage {
  type: 'init' | 'download'
  fileBase64?: string
  fileName?: string
  fieldList?: Field[]
}
```

---

## 8. 测试策略

- **单元测试** (Vitest): FieldPanel 搜索过滤逻辑、useFieldManager 状态管理、useStreamlitBridge 数据解析
- **组件测试**: FieldItem 渲染、点击事件触发、TitleBar 下载按钮 emit
- **手动验证**: OnlyOffice 加载/编辑/下载的实际行为（OnlyOffice 在 jsdom 中无法完整运行）
- **E2E**: Streamlit → Vue iframe → OnlyOffice → 编辑 → 下载 全链路

---

## 9. 边界与限制

1. **OnlyOffice Web SDK 体积约 30MB** — 首次加载需数秒，建议 Streamlit 端显示 loading 状态
2. **AGPL-3.0 协议** — 如果对外分发，衍生代码需开源
3. **字段插入通过 postMessage** — 依赖 OnlyOffice API 的 `insertText` 或类似方法，跨 iframe 通信有延迟
4. **仅支持 .docx 和 .xlsx** — 旧版 .doc 和 .xls 格式需要 Streamlit 侧预先转换
5. **字段面板是 Vue 原生组件** — 不依赖 OnlyOffice，可以独立开发和测试
6. **下载由 Vue 端触发** — 用户点 TitleBar 中的下载按钮 → OnlyOffice save 生成 base64 → postMessage 回传 Streamlit → Streamlit 侧 `st.download_button` 触发浏览器下载。流式路径是单向的：上传(S→V) → 编辑(V内部) → 下载(V→S)

---

## 10. 里程碑

| 阶段 | 内容 |
|------|------|
| M1 | Vue 项目脚手架 + 80/20 布局 + 字段面板（静态数据） |
| M2 | 集成 OnlyOffice Web SDK + docx 加载/编辑/下载 |
| M3 | xlsx 支持 + 自动格式切换 |
| M4 | Streamlit 桥接层（base64 通信） |
| M5 | Streamlit 集成 + 全链路联调 |
| M6 | 测试 + 修复 |
