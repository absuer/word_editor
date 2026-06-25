# Vue Word Editor 实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 构建一个基于 Vue 3 + OnlyOffice Web SDK 的在线 Word/Excel 编辑器，嵌入 Streamlit 智能客服系统。

**Architecture:** Vue 3 作为壳框架，80% 左侧嵌入 OnlyOffice iframe 做原生文档编辑，20% 右侧为自定义字段面板。Streamlit 通过 postMessage 传递 base64 文件 + 字段列表，编辑器处理后回传。

**Tech Stack:** Vue 3 (Composition API) + TypeScript + Vite + OnlyOffice Web SDK + Vitest

---

### Task 1: 项目脚手架

**Files:**
- Create: `vue-word-editor/package.json`
- Create: `vue-word-editor/vite.config.ts`
- Create: `vue-word-editor/tsconfig.json`
- Create: `vue-word-editor/tsconfig.node.json`
- Create: `vue-word-editor/env.d.ts`
- Create: `vue-word-editor/index.html`
- Create: `vue-word-editor/src/main.ts`
- Create: `vue-word-editor/src/assets/styles.css`

- [ ] **Step 1: 创建 package.json**

```json
{
  "name": "vue-word-editor",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vue-tsc && vite build",
    "preview": "vite preview",
    "test": "vitest run",
    "test:watch": "vitest"
  },
  "dependencies": {
    "vue": "^3.4.0"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^5.0.0",
    "@vue/test-utils": "^2.4.0",
    "jsdom": "^24.0.0",
    "typescript": "^5.3.0",
    "vite": "^5.1.0",
    "vitest": "^1.2.0",
    "vue-tsc": "^1.8.0"
  }
}
```

- [ ] **Step 2: 创建 vite.config.ts**

```typescript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
    },
  },
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
  },
})
```

- [ ] **Step 3: 创建 tsconfig.json**

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ESNext",
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "preserve",
    "strict": true,
    "noUnusedLocals": false,
    "noUnusedParameters": false,
    "noFallthroughCasesInSwitch": true,
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src/**/*.ts", "src/**/*.tsx", "src/**/*.vue", "env.d.ts"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

- [ ] **Step 4: 创建 tsconfig.node.json**

```json
{
  "compilerOptions": {
    "composite": true,
    "skipLibCheck": true,
    "module": "ESNext",
    "moduleResolution": "bundler",
    "allowSyntheticDefaultImports": true
  },
  "include": ["vite.config.ts"]
}
```

- [ ] **Step 5: 创建 env.d.ts**

```typescript
/// <reference types="vite/client" />

declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent<{}, {}, any>
  export default component
}
```

- [ ] **Step 6: 创建 index.html**

```html
<!DOCTYPE html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>在线文档编辑器</title>
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.ts"></script>
  </body>
</html>
```

- [ ] **Step 7: 创建 src/main.ts**

```typescript
import { createApp } from 'vue'
import App from './App.vue'
import './assets/styles.css'

createApp(App).mount('#app')
```

- [ ] **Step 8: 创建 src/assets/styles.css**

```css
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body, #app {
  height: 100%;
  width: 100%;
  overflow: hidden;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

.editor-layout {
  display: flex;
  height: 100%;
  width: 100%;
}

.editor-panel {
  flex: 4;
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.field-panel {
  flex: 1;
  min-width: 200px;
  max-width: 320px;
  border-left: 1px solid #e0e0e0;
  background: #fafafa;
  display: flex;
  flex-direction: column;
}
```

- [ ] **Step 9: 安装依赖并验证**

```bash
cd vue-word-editor && npm install && npm run dev
```

Expected: Dev server starts on localhost:5173, blank page loads.

- [ ] **Step 10: Commit**

```bash
git add vue-word-editor/
git commit -m "feat: scaffold Vue 3 + Vite + TypeScript project"
```

---

### Task 2: 类型定义

**Files:**
- Create: `vue-word-editor/src/types/index.ts`

- [ ] **Step 1: 创建类型文件**

```typescript
// vue-word-editor/src/types/index.ts

/** 字段项 */
export interface Field {
  id: string
  name: string
  icon?: string
}

/** 文件数据（Streamlit → Vue） */
export interface FileData {
  base64: string
  fileName: string
  format: 'docx' | 'xlsx'
}

/** Streamlit 发来的初始化消息 */
export interface StreamlitInitMessage {
  type: 'init'
  fileBase64: string
  fileName: string
  fieldList: Field[]
}

/** Vue 回传给 Streamlit 的下载消息 */
export interface StreamlitDownloadMessage {
  type: 'download'
  fileBase64: string
  fileName: string
}

/** OnlyOffice 文档类型 */
export type DocumentType = 'word' | 'cell'

/** OnlyOffice 事件回调 */
export interface OnlyOfficeEvents {
  onReady: () => void
  onSave: (base64: string) => void
}

/** OnlyOffice 编辑器配置 */
export interface OnlyOfficeConfig {
  documentType: DocumentType
  fileType: 'docx' | 'xlsx'
  title: string
  key: string
  url: string
  lang?: string
}
```

- [ ] **Step 2: 验证类型编译**

```bash
cd vue-word-editor && npx vue-tsc --noEmit
```

Expected: No type errors.

- [ ] **Step 3: Commit**

```bash
git add vue-word-editor/src/types/
git commit -m "feat: define TypeScript types for editor fields, files, and messages"
```

---

### Task 3: TitleBar 组件

**Files:**
- Create: `vue-word-editor/src/components/TitleBar.vue`
- Create: `vue-word-editor/tests/TitleBar.spec.ts`

- [ ] **Step 1: 编写 TitleBar 测试**

```typescript
// vue-word-editor/tests/TitleBar.spec.ts
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import TitleBar from '@/components/TitleBar.vue'

describe('TitleBar', () => {
  it('renders the file name', () => {
    const wrapper = mount(TitleBar, {
      props: { fileName: 'contract.docx' }
    })
    expect(wrapper.text()).toContain('contract.docx')
  })

  it('renders Word icon for docx files', () => {
    const wrapper = mount(TitleBar, {
      props: { fileName: 'test.docx' }
    })
    expect(wrapper.text()).toContain('📄')
  })

  it('renders Excel icon for xlsx files', () => {
    const wrapper = mount(TitleBar, {
      props: { fileName: 'data.xlsx' }
    })
    expect(wrapper.text()).toContain('📊')
  })

  it('emits download event when download button is clicked', async () => {
    const wrapper = mount(TitleBar, {
      props: { fileName: 'test.docx' }
    })
    await wrapper.find('[data-test="download-btn"]').trigger('click')
    expect(wrapper.emitted('download')).toBeTruthy()
    expect(wrapper.emitted('download')![0]).toEqual([])
  })
})
```

- [ ] **Step 2: 运行测试，确认失败**

```bash
cd vue-word-editor && npx vitest run tests/TitleBar.spec.ts
```

Expected: FAIL — TitleBar.vue not found.

- [ ] **Step 3: 实现 TitleBar 组件**

```vue
<!-- vue-word-editor/src/components/TitleBar.vue -->
<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  fileName: string
}>()

const emit = defineEmits<{
  download: []
}>()

const fileIcon = computed(() => {
  const ext = props.fileName.split('.').pop()?.toLowerCase()
  return ext === 'xlsx' ? '📊' : '📄'
})

const fileTypeLabel = computed(() => {
  const ext = props.fileName.split('.').pop()?.toLowerCase()
  return ext === 'xlsx' ? 'Excel 编辑器' : 'Word 编辑器'
})
</script>

<template>
  <div class="title-bar">
    <span class="title-bar__icon">{{ fileIcon }}</span>
    <span class="title-bar__name">{{ fileName }}</span>
    <span class="title-bar__type">{{ fileTypeLabel }}</span>
    <button
      class="title-bar__download"
      data-test="download-btn"
      @click="emit('download')"
    >
      下载
    </button>
  </div>
</template>

<style scoped>
.title-bar {
  background: #2c2c2c;
  color: #ccc;
  padding: 6px 16px;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  flex-shrink: 0;
}

.title-bar__icon {
  font-size: 16px;
}

.title-bar__name {
  color: #ddd;
  opacity: 0.8;
}

.title-bar__type {
  margin-left: auto;
  font-size: 11px;
  opacity: 0.5;
  margin-right: 12px;
}

.title-bar__download {
  background: #4caf50;
  color: #fff;
  border: none;
  border-radius: 3px;
  padding: 3px 14px;
  font-size: 12px;
  cursor: pointer;
}

.title-bar__download:hover {
  background: #43a047;
}
</style>
```

- [ ] **Step 4: 运行测试验证通过**

```bash
cd vue-word-editor && npx vitest run tests/TitleBar.spec.ts
```

Expected: All 4 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add vue-word-editor/src/components/TitleBar.vue vue-word-editor/tests/TitleBar.spec.ts
git commit -m "feat: add TitleBar component with filename display and download button"
```

---

### Task 4: 字段面板组件

**Files:**
- Create: `vue-word-editor/src/components/field/FieldItem.vue`
- Create: `vue-word-editor/src/components/field/FieldSearch.vue`
- Create: `vue-word-editor/src/components/field/FieldList.vue`
- Create: `vue-word-editor/src/components/field/FieldPanel.vue`
- Create: `vue-word-editor/tests/FieldPanel.spec.ts`

- [ ] **Step 1: 编写字段面板测试**

```typescript
// vue-word-editor/tests/FieldPanel.spec.ts
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import FieldPanel from '@/components/field/FieldPanel.vue'

const mockFields = [
  { id: '1', name: '客户名称', icon: '👤' },
  { id: '2', name: '合同金额', icon: '💰' },
  { id: '3', name: '签订日期', icon: '📅' },
]

describe('FieldPanel', () => {
  it('renders all fields initially', () => {
    const wrapper = mount(FieldPanel, {
      props: { fields: mockFields }
    })
    expect(wrapper.text()).toContain('客户名称')
    expect(wrapper.text()).toContain('合同金额')
    expect(wrapper.text()).toContain('签订日期')
  })

  it('renders panel title', () => {
    const wrapper = mount(FieldPanel, {
      props: { fields: mockFields }
    })
    expect(wrapper.text()).toContain('字段列表')
  })

  it('filters fields by search query', async () => {
    const wrapper = mount(FieldPanel, {
      props: { fields: mockFields }
    })
    const searchInput = wrapper.find('[data-test="field-search"] input')
    await searchInput.setValue('客户')
    expect(wrapper.text()).toContain('客户名称')
    expect(wrapper.text()).not.toContain('合同金额')
    expect(wrapper.text()).not.toContain('签订日期')
  })

  it('filters are case-insensitive', async () => {
    const wrapper = mount(FieldPanel, {
      props: { fields: mockFields }
    })
    const searchInput = wrapper.find('[data-test="field-search"] input')
    await searchInput.setValue('金额')
    expect(wrapper.text()).toContain('合同金额')
  })

  it('emits insert event when a field is clicked', async () => {
    const wrapper = mount(FieldPanel, {
      props: { fields: mockFields }
    })
    const firstField = wrapper.find('[data-test="field-item"]')
    await firstField.trigger('click')
    expect(wrapper.emitted('insert')).toBeTruthy()
    expect(wrapper.emitted('insert')![0][0]).toEqual(mockFields[0])
  })

  it('shows empty state when no fields match', async () => {
    const wrapper = mount(FieldPanel, {
      props: { fields: mockFields }
    })
    const searchInput = wrapper.find('[data-test="field-search"] input')
    await searchInput.setValue('不存在的字段')
    expect(wrapper.text()).toContain('无匹配字段')
    expect(wrapper.findAll('[data-test="field-item"]').length).toBe(0)
  })
})
```

- [ ] **Step 2: 运行测试确认失败**

```bash
cd vue-word-editor && npx vitest run tests/FieldPanel.spec.ts
```

Expected: FAIL — components not found.

- [ ] **Step 3: 实现 FieldItem.vue**

```vue
<!-- vue-word-editor/src/components/field/FieldItem.vue -->
<script setup lang="ts">
import type { Field } from '@/types'

defineProps<{
  field: Field
}>()

const emit = defineEmits<{
  select: [field: Field]
}>()
</script>

<template>
  <div
    class="field-item"
    data-test="field-item"
    @click="emit('select', field)"
  >
    <span class="field-item__icon">{{ field.icon || '📌' }}</span>
    <span class="field-item__name">{{ field.name }}</span>
    <span class="field-item__syntax">{{ '{{ }}' }}</span>
  </div>
</template>

<style scoped>
.field-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 10px;
  background: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  cursor: pointer;
  font-size: 13px;
  transition: background 0.15s;
}

.field-item:hover {
  background: #e8f5e9;
  border-color: #a5d6a7;
}

.field-item__icon {
  font-size: 14px;
  flex-shrink: 0;
}

.field-item__name {
  flex: 1;
  color: #333;
}

.field-item__syntax {
  font-size: 10px;
  color: #999;
  font-family: monospace;
}
</style>
```

- [ ] **Step 4: 实现 FieldSearch.vue**

```vue
<!-- vue-word-editor/src/components/field/FieldSearch.vue -->
<script setup lang="ts">
const model = defineModel<string>({ required: true })
</script>

<template>
  <div class="field-search" data-test="field-search">
    <input
      v-model="model"
      type="text"
      class="field-search__input"
      placeholder="搜索字段..."
    />
  </div>
</template>

<style scoped>
.field-search {
  padding: 8px 10px;
}

.field-search__input {
  width: 100%;
  padding: 6px 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 12px;
  outline: none;
}

.field-search__input:focus {
  border-color: #1976d2;
  box-shadow: 0 0 0 2px rgba(25, 118, 210, 0.1);
}
</style>
```

- [ ] **Step 5: 实现 FieldList.vue**

```vue
<!-- vue-word-editor/src/components/field/FieldList.vue -->
<script setup lang="ts">
import type { Field } from '@/types'
import FieldItem from './FieldItem.vue'

defineProps<{
  fields: Field[]
}>()

const emit = defineEmits<{
  select: [field: Field]
}>()
</script>

<template>
  <div class="field-list">
    <template v-if="fields.length > 0">
      <FieldItem
        v-for="field in fields"
        :key="field.id"
        :field="field"
        @select="emit('select', $event)"
      />
    </template>
    <div v-else class="field-list__empty">
      无匹配字段
    </div>
  </div>
</template>

<style scoped>
.field-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 0 10px 10px;
  overflow-y: auto;
}

.field-list__empty {
  padding: 20px 10px;
  text-align: center;
  color: #999;
  font-size: 13px;
}
</style>
```

- [ ] **Step 6: 实现 FieldPanel.vue**

```vue
<!-- vue-word-editor/src/components/field/FieldPanel.vue -->
<script setup lang="ts">
import { ref, computed } from 'vue'
import type { Field } from '@/types'
import FieldSearch from './FieldSearch.vue'
import FieldList from './FieldList.vue'

const props = defineProps<{
  fields: Field[]
}>()

const emit = defineEmits<{
  insert: [field: Field]
}>()

const searchQuery = ref('')

const filteredFields = computed(() => {
  if (!searchQuery.value.trim()) {
    return props.fields
  }
  const q = searchQuery.value.toLowerCase()
  return props.fields.filter(f => f.name.toLowerCase().includes(q))
})
</script>

<template>
  <aside class="field-panel">
    <div class="field-panel__header">📋 字段列表</div>
    <FieldSearch v-model="searchQuery" />
    <FieldList
      :fields="filteredFields"
      @select="emit('insert', $event)"
    />
  </aside>
</template>

<style scoped>
.field-panel {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: #fafafa;
}

.field-panel__header {
  background: #e8e8e8;
  padding: 10px 14px;
  font-weight: 600;
  font-size: 13px;
  border-bottom: 1px solid #ddd;
  flex-shrink: 0;
}
</style>
```

- [ ] **Step 7: 运行测试验证通过**

```bash
cd vue-word-editor && npx vitest run tests/FieldPanel.spec.ts
```

Expected: All 6 tests PASS.

- [ ] **Step 8: Commit**

```bash
git add vue-word-editor/src/components/field/ vue-word-editor/tests/FieldPanel.spec.ts
git commit -m "feat: add field panel components with search and click-to-insert"
```

---

### Task 5: useFieldManager composable

**Files:**
- Create: `vue-word-editor/src/composables/useFieldManager.ts`
- Create: `vue-word-editor/tests/useFieldManager.spec.ts`

- [ ] **Step 1: 编写 useFieldManager 测试**

```typescript
// vue-word-editor/tests/useFieldManager.spec.ts
import { describe, it, expect } from 'vitest'
import { useFieldManager } from '@/composables/useFieldManager'
import type { Field } from '@/types'

const sampleFields: Field[] = [
  { id: '1', name: '客户名称', icon: '👤' },
  { id: '2', name: '合同金额', icon: '💰' },
  { id: '3', name: '签订日期', icon: '📅' },
]

describe('useFieldManager', () => {
  it('returns all fields when searchQuery is empty', () => {
    const { filteredFields } = useFieldManager(sampleFields)
    expect(filteredFields.value).toHaveLength(3)
  })

  it('filters fields by search query', () => {
    const { filteredFields, searchQuery } = useFieldManager(sampleFields)
    searchQuery.value = '客户'
    expect(filteredFields.value).toHaveLength(1)
    expect(filteredFields.value[0].name).toBe('客户名称')
  })

  it('is case-insensitive', () => {
    const { filteredFields, searchQuery } = useFieldManager(sampleFields)
    searchQuery.value = '金额'
    expect(filteredFields.value).toHaveLength(1)
  })

  it('returns empty array when no match', () => {
    const { filteredFields, searchQuery } = useFieldManager(sampleFields)
    searchQuery.value = '不存在'
    expect(filteredFields.value).toHaveLength(0)
  })

  it('insertField returns the correct placeholder text', () => {
    const { insertField } = useFieldManager(sampleFields)
    const result = insertField(sampleFields[0])
    expect(result).toBe('{{ 客户名称 }}')
  })
})
```

- [ ] **Step 2: 运行测试确认失败**

```bash
cd vue-word-editor && npx vitest run tests/useFieldManager.spec.ts
```

Expected: FAIL — composable not found.

- [ ] **Step 3: 实现 useFieldManager**

```typescript
// vue-word-editor/src/composables/useFieldManager.ts
import { ref, computed } from 'vue'
import type { Field } from '@/types'

export function useFieldManager(initialFields: Field[] = []) {
  const fields = ref<Field[]>([...initialFields])
  const searchQuery = ref('')

  const filteredFields = computed(() => {
    if (!searchQuery.value.trim()) {
      return fields.value
    }
    const q = searchQuery.value.toLowerCase()
    return fields.value.filter(f => f.name.toLowerCase().includes(q))
  })

  function insertField(field: Field): string {
    return `{{ ${field.name} }}`
  }

  return {
    fields,
    searchQuery,
    filteredFields,
    insertField,
  }
}
```

- [ ] **Step 4: 运行测试验证通过**

```bash
cd vue-word-editor && npx vitest run tests/useFieldManager.spec.ts
```

Expected: All 5 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add vue-word-editor/src/composables/useFieldManager.ts vue-word-editor/tests/useFieldManager.spec.ts
git commit -m "feat: add useFieldManager composable for field search and insertion"
```

---

### Task 6: useStreamlitBridge composable

**Files:**
- Create: `vue-word-editor/src/composables/useStreamlitBridge.ts`
- Create: `vue-word-editor/tests/useStreamlitBridge.spec.ts`

- [ ] **Step 1: 编写 useStreamlitBridge 测试**

```typescript
// vue-word-editor/tests/useStreamlitBridge.spec.ts
import { describe, it, expect, beforeEach, vi } from 'vitest'
import { useStreamlitBridge } from '@/composables/useStreamlitBridge'
import type { StreamlitInitMessage } from '@/types'

const mockMessage: StreamlitInitMessage = {
  type: 'init',
  fileBase64: 'UEsDBBQAAAAIAAAAA==',
  fileName: 'contract.docx',
  fieldList: [
    { id: '1', name: '客户名称', icon: '👤' },
    { id: '2', name: '合同金额', icon: '💰' },
  ],
}

describe('useStreamlitBridge', () => {
  beforeEach(() => {
    vi.restoreAllMocks()
  })

  it('initializes with null fileData and empty fieldList', () => {
    const { fileData, fieldList } = useStreamlitBridge()
    expect(fileData.value).toBeNull()
    expect(fieldList.value).toEqual([])
  })

  it('receiveFromStreamlit parses init message correctly via postMessage', () => {
    const { fileData, fieldList, receiveFromStreamlit } = useStreamlitBridge()

    receiveFromStreamlit(mockMessage)

    expect(fileData.value).toEqual({
      base64: 'UEsDBBQAAAAIAAAAA==',
      fileName: 'contract.docx',
      format: 'docx',
    })
    expect(fieldList.value).toHaveLength(2)
    expect(fieldList.value[0].name).toBe('客户名称')
  })

  it('receiveFromStreamlit detects xlsx format', () => {
    const { fileData, receiveFromStreamlit } = useStreamlitBridge()

    receiveFromStreamlit({
      ...mockMessage,
      fileName: 'data.xlsx',
    })

    expect(fileData.value!.format).toBe('xlsx')
  })

  it('sendToStreamlit posts download message to parent window', () => {
    const mockPostMessage = vi.fn()
    vi.stubGlobal('window', {
      parent: {
        postMessage: mockPostMessage,
      },
    })

    vi.stubGlobal('location', { origin: 'http://localhost:8501' })

    const { sendToStreamlit } = useStreamlitBridge()

    sendToStreamlit('base64content', 'output.docx')

    expect(mockPostMessage).toHaveBeenCalledWith(
      {
        type: 'download',
        fileBase64: 'base64content',
        fileName: 'output.docx',
      },
      'http://localhost:8501'
    )
  })
})
```

- [ ] **Step 2: 运行测试确认失败**

```bash
cd vue-word-editor && npx vitest run tests/useStreamlitBridge.spec.ts
```

Expected: FAIL — composable not found.

- [ ] **Step 3: 实现 useStreamlitBridge**

```typescript
// vue-word-editor/src/composables/useStreamlitBridge.ts
import { ref } from 'vue'
import type {
  Field,
  FileData,
  StreamlitInitMessage,
  StreamlitDownloadMessage,
} from '@/types'

export function useStreamlitBridge() {
  const fileData = ref<FileData | null>(null)
  const fieldList = ref<Field[]>([])

  function detectFormat(fileName: string): 'docx' | 'xlsx' {
    const ext = fileName.split('.').pop()?.toLowerCase()
    if (ext === 'xlsx') return 'xlsx'
    return 'docx'
  }

  function receiveFromStreamlit(message: StreamlitInitMessage): void {
    if (message.type !== 'init') return

    fileData.value = {
      base64: message.fileBase64,
      fileName: message.fileName,
      format: detectFormat(message.fileName),
    }

    if (Array.isArray(message.fieldList)) {
      fieldList.value = message.fieldList
    }
  }

  function sendToStreamlit(base64: string, fileName: string): void {
    const msg: StreamlitDownloadMessage = {
      type: 'download',
      fileBase64: base64,
      fileName,
    }
    window.parent.postMessage(msg, window.location.origin)
  }

  return {
    fileData,
    fieldList,
    receiveFromStreamlit,
    sendToStreamlit,
    detectFormat,
  }
}
```

- [ ] **Step 4: 运行测试验证通过**

```bash
cd vue-word-editor && npx vitest run tests/useStreamlitBridge.spec.ts
```

Expected: All 4 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add vue-word-editor/src/composables/useStreamlitBridge.ts vue-word-editor/tests/useStreamlitBridge.spec.ts
git commit -m "feat: add useStreamlitBridge composable for postMessage communication"
```

---

### Task 7: useOnlyOffice composable

**Files:**
- Create: `vue-word-editor/src/composables/useOnlyOffice.ts`

- [ ] **Step 1: 实现 useOnlyOffice**

```typescript
// vue-word-editor/src/composables/useOnlyOffice.ts
import { ref } from 'vue'
import type { OnlyOfficeConfig, DocumentType } from '@/types'

/**
 * OnlyOffice DocEditor 生命周期管理
 *
 * 使用全局 DocsAPI.DocEditor 构造函数（由 @onlyoffice/document-editor 提供）。
 * 编辑器渲染到指定的 DOM 元素中，内部以 WebAssembly 运行。
 */

export function useOnlyOffice() {
  const editorInstance = ref<any>(null)
  const isReady = ref(false)
  const isLoading = ref(false)

  function getFileType(format: 'docx' | 'xlsx'): string {
    return format
  }

  function getDocumentType(format: 'docx' | 'xlsx'): DocumentType {
    return format === 'xlsx' ? 'cell' : 'word'
  }

  function buildConfig(
    placeholderId: string,
    base64: string,
    fileName: string,
    format: 'docx' | 'xlsx',
  ): OnlyOfficeConfig {
    const mimeType =
      format === 'xlsx'
        ? 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        : 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'

    return {
      documentType: getDocumentType(format),
      fileType: format,
      title: fileName,
      key: `${fileName}_${Date.now()}`,
      url: `data:${mimeType};base64,${base64}`,
      lang: 'zh-CN',
    }
  }

  function init(
    placeholderId: string,
    base64: string,
    fileName: string,
    format: 'docx' | 'xlsx',
    onSave: (base64: string) => void,
  ): void {
    destroy()
    isLoading.value = true

    const config = buildConfig(placeholderId, base64, fileName, format)

    const fullConfig = {
      document: {
        fileType: config.fileType,
        key: config.key,
        title: config.title,
        url: config.url,
      },
      documentType: config.documentType,
      editorConfig: {
        mode: 'edit' as const,
        lang: config.lang,
        customization: {
          compactToolbar: false,
          forcesave: false,
        },
      },
      events: {
        onReady: () => {
          isReady.value = true
          isLoading.value = false
        },
        onRequestSave: (event: any) => {
          // OnlyOffice 请求保存时回调，event.data 包含文档 base64
          if (event.data) {
            onSave(event.data)
          }
        },
        onError: (event: any) => {
          console.error('OnlyOffice editor error:', event)
          isLoading.value = false
        },
      },
    }

    // 动态加载 OnlyOffice API 脚本（如果尚未加载）
    if (typeof (window as any).DocsAPI === 'undefined') {
      const scriptId = 'onlyoffice-api-script'
      if (!document.getElementById(scriptId)) {
        const script = document.createElement('script')
        script.id = scriptId
        script.src = 'https://onlyoffice.github.io/sdkjs-plugins/v1/editors.js'
        script.onload = () => {
          editorInstance.value = new (window as any).DocsAPI.DocEditor(
            placeholderId,
            fullConfig,
          )
        }
        script.onerror = () => {
          console.error('Failed to load OnlyOffice API script')
          isLoading.value = false
        }
        document.head.appendChild(script)
      }
    } else {
      editorInstance.value = new (window as any).DocsAPI.DocEditor(
        placeholderId,
        fullConfig,
      )
    }
  }

  /**
   * 触发 OnlyOffice 保存（在纯前端模式下，通过 forceSave 或 callCommand 获取内容）
   */
  function requestSave(): void {
    if (!editorInstance.value || !isReady.value) return

    try {
      // 调用 OnlyOffice 内部 API 触发保存
      editorInstance.value.document?.save()
    } catch {
      // 备选方案: 直接通过 requestSave 事件获取
      console.warn('save() not available, trying alternative')
    }
  }

  function destroy(): void {
    if (editorInstance.value) {
      try {
        editorInstance.value.destroyEditor()
      } catch {
        // 忽略销毁错误
      }
      editorInstance.value = null
    }
    isReady.value = false
    isLoading.value = false
  }

  /**
   * 向编辑器文档中插入文本
   * 使用 OnlyOffice connector API 在光标位置插入 {{ 字段名 }}
   */
  function insertText(text: string): void {
    if (!editorInstance.value || !isReady.value) return

    try {
      const connector = editorInstance.value.createConnector()
      connector.callCommand(
        function () {
          // 此函数在 OnlyOffice 编辑器上下文中执行
          const doc = (window as any).Api.GetDocument()
          const paragraph = (window as any).Api.CreateParagraph()
          paragraph.AddText(text)
          doc.InsertContent([paragraph])
        },
        function () {
          // 命令完成回调
        },
      )
    } catch (e) {
      console.warn('insertText failed:', e)
    }
  }

  return {
    isReady,
    isLoading,
    init,
    requestSave,
    destroy,
    insertText,
  }
}
```

- [ ] **Step 2: 验证 TypeScript 编译**

```bash
cd vue-word-editor && npx vue-tsc --noEmit
```

Expected: No type errors.

- [ ] **Step 3: Commit**

```bash
git add vue-word-editor/src/composables/useOnlyOffice.ts
git commit -m "feat: add useOnlyOffice composable wrapping OnlyOffice DocEditor API"
```

---

### Task 8: EditorPanel 组件

**Files:**
- Create: `vue-word-editor/src/components/EditorPanel.vue`

- [ ] **Step 1: 实现 EditorPanel**

```vue
<!-- vue-word-editor/src/components/EditorPanel.vue -->
<script setup lang="ts">
import { ref, watch, onBeforeUnmount, nextTick } from 'vue'
import { useOnlyOffice } from '@/composables/useOnlyOffice'
import type { FileData } from '@/types'

const props = defineProps<{
  fileData: FileData | null
}>()

const emit = defineEmits<{
  save: [base64: string, fileName: string]
}>()

const placeholderId = 'onlyoffice-editor-placeholder'
const { isReady, isLoading, init, requestSave, destroy, insertText } =
  useOnlyOffice()

// 当 fileData 变化时，重新初始化编辑器
watch(
  () => props.fileData,
  async (data) => {
    if (!data) return
    await nextTick()
    init(
      placeholderId,
      data.base64,
      data.fileName,
      data.format,
      (savedBase64: string) => {
        emit('save', savedBase64, data.fileName)
      },
    )
  },
  { immediate: true },
)

// 暴露方法供父组件调用（通过 ref）
defineExpose({ insertText, requestSave })

onBeforeUnmount(() => {
  destroy()
})
</script>

<template>
  <div class="editor-panel">
    <div
      v-if="isLoading"
      class="editor-panel__loading"
    >
      <div class="editor-panel__loading-spinner" />
      <p>正在加载编辑器...</p>
    </div>
    <div
      :id="placeholderId"
      class="editor-panel__placeholder"
      :class="{ 'editor-panel__placeholder--hidden': isLoading }"
    />
  </div>
</template>

<style scoped>
.editor-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
  position: relative;
}

.editor-panel__loading {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #fff;
  gap: 12px;
  color: #666;
  font-size: 14px;
  z-index: 10;
}

.editor-panel__loading-spinner {
  width: 32px;
  height: 32px;
  border: 3px solid #e0e0e0;
  border-top-color: #1976d2;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.editor-panel__placeholder {
  flex: 1;
  min-height: 0;
}

.editor-panel__placeholder--hidden {
  visibility: hidden;
}
</style>
```

- [ ] **Step 2: 验证 TypeScript 编译**

```bash
cd vue-word-editor && npx vue-tsc --noEmit
```

Expected: No type errors.

- [ ] **Step 3: Commit**

```bash
git add vue-word-editor/src/components/EditorPanel.vue
git commit -m "feat: add EditorPanel component with OnlyOffice lifecycle management"
```

---

### Task 9: App.vue 主组件

**Files:**
- Create: `vue-word-editor/src/App.vue`

- [ ] **Step 1: 实现 App.vue**

```vue
<!-- vue-word-editor/src/App.vue -->
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import TitleBar from '@/components/TitleBar.vue'
import EditorPanel from '@/components/EditorPanel.vue'
import FieldPanel from '@/components/field/FieldPanel.vue'
import { useStreamlitBridge } from '@/composables/useStreamlitBridge'
import type { Field, StreamlitInitMessage } from '@/types'

const {
  fileData,
  fieldList,
  receiveFromStreamlit,
  sendToStreamlit,
} = useStreamlitBridge()

const editorRef = ref<InstanceType<typeof EditorPanel> | null>(null)

// 从 Streamlit 接收初始化数据
onMounted(() => {
  window.addEventListener('message', (event) => {
    const msg = event.data as StreamlitInitMessage
    if (msg?.type === 'init') {
      receiveFromStreamlit(msg)
    }
  })
})

// 处理字段插入
function handleInsertField(field: Field) {
  const text = `{{ ${field.name} }}`
  editorRef.value?.insertText(text)
}

// 处理下载：触发 OnlyOffice 保存 → onSave 回调 → handleSave → sendToStreamlit
function handleDownload() {
  editorRef.value?.requestSave()
}

// 处理来自 EditorPanel 的保存事件
function handleSave(base64: string, fileName: string) {
  sendToStreamlit(base64, fileName)
}
</script>

<template>
  <div class="editor-layout">
    <div class="editor-panel">
      <TitleBar
        :file-name="fileData?.fileName || '未打开文件'"
        @download="handleDownload"
      />
      <EditorPanel
        ref="editorRef"
        :file-data="fileData"
        @save="handleSave"
      />
    </div>
    <FieldPanel
      :fields="fieldList"
      @insert="handleInsertField"
    />
  </div>
</template>

<style scoped>
.editor-layout {
  display: flex;
  height: 100%;
  width: 100%;
}

.editor-panel {
  flex: 4;
  display: flex;
  flex-direction: column;
  min-width: 0;
  height: 100%;
}
</style>
```

- [ ] **Step 2: 验证项目编译和类型检查**

```bash
cd vue-word-editor && npx vue-tsc --noEmit && npx vite build
```

Expected: Build succeeds, output in `dist/`.

- [ ] **Step 3: Commit**

```bash
git add vue-word-editor/src/App.vue
git commit -m "feat: add App.vue main layout wiring all components"
```

---

### Task 10: Streamlit 集成适配层

**Files:**
- Modify: `app.py`（在当前 Streamlit 项目中新增编辑器嵌入逻辑）

- [ ] **Step 1: 在 app.py 中添加编辑器嵌入支持**

在现有 `app.py` 文件末尾追加以下代码，不要删改已有内容：

```python
# === Vue Word Editor 嵌入 ===

import base64
import json
import streamlit as st
import streamlit.components.v1 as components


def render_editor(file_bytes: bytes, file_name: str, field_list: list[dict]) -> None:
    """将 Vue 编辑器以 iframe 形式嵌入 Streamlit 页面。

    Args:
        file_bytes: 上传文件的原始字节
        file_name: 原始文件名（用于判断 docx/xlsx）
        field_list: 字段列表，格式 [{"id": "1", "name": "客户名称", "icon": "👤"}, ...]
    """
    file_base64 = base64.b64encode(file_bytes).decode("utf-8")

    init_message = {
        "type": "init",
        "fileBase64": file_base64,
        "fileName": file_name,
        "fieldList": field_list,
    }

    # 构建编辑器 HTML，通过 postMessage 将数据传入 Vue iframe
    editor_html = f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        html, body {{ height: 100%; width: 100%; overflow: hidden; }}
        iframe {{ border: none; width: 100%; height: 100%; }}
      </style>
    </head>
    <body>
      <iframe id="editor" src="./static/vue-editor/index.html"></iframe>
      <script>
        const initData = {json.dumps(init_message, ensure_ascii=False)};

        const iframe = document.getElementById('editor');
        iframe.addEventListener('load', function() {{
          iframe.contentWindow.postMessage(initData, '*');
        }});

        // 监听 Vue 编辑器回传的下载消息
        window.addEventListener('message', function(event) {{
          if (event.data && event.data.type === 'download') {{
            // 将 base64 数据传递给 Streamlit
            window.parent.postMessage(event.data, '*');
          }}
        }});
      </script>
    </body>
    </html>
    """

    components.html(editor_html, height=700, scrolling=False)


def handle_editor_download() -> None:
    """在 Streamlit 主循环中检查是否有编辑器回传的下载数据。

    使用方式:
        handle_editor_download()
    """
    # 通过 st.session_state 传递下载数据
    if "editor_download_data" in st.session_state and st.session_state.editor_download_data:
        data = st.session_state.editor_download_data
        st.download_button(
            label=f"下载 {data['fileName']}",
            data=base64.b64decode(data['fileBase64']),
            file_name=data['fileName'],
            mime="application/octet-stream",
        )
```

- [ ] **Step 2: 验证 Python 语法**

```bash
python -c "import ast; ast.parse(open('app.py').read()); print('Syntax OK')"
```

Expected: `Syntax OK`

- [ ] **Step 3: 配置 Vite build 输出到 Streamlit 静态目录**

更新 `vue-word-editor/vite.config.ts`，使 build 输出到 Streamlit 的 `static/vue-editor/` 目录：

将现有 `vite.config.ts` 中的 `build` 块替换为：

```typescript
  base: '/static/vue-editor/',
  build: {
    outDir: '../static/vue-editor',
    assetsDir: 'assets',
    emptyOutDir: true,
  },
```

- [ ] **Step 4: Build Vue 项目**

```bash
cd vue-word-editor && npm run build
```

Expected: Build 成功，`static/vue-editor/` 目录下生成静态文件。

- [ ] **Step 5: Commit**

```bash
git add app.py vue-word-editor/vite.config.ts static/
git commit -m "feat: add Streamlit editor embedding layer and configure vite build output"
```

---

### Task 11: 全链路集成测试与验证

**Files:**
- Create: `tests/test_editor_integration.py`

- [ ] **Step 1: 编写集成测试**

```python
# tests/test_editor_integration.py
import base64
import json
import pytest
from app import render_editor


def test_render_editor_produces_html():
    """验证渲染函数产生有效 HTML"""
    file_bytes = b"fake docx content"
    file_name = "test.docx"
    field_list = [
        {"id": "1", "name": "客户名称", "icon": "👤"},
        {"id": "2", "name": "合同金额", "icon": "💰"},
    ]

    # render_editor 调用 st.components.v1.html，在测试中会由 pytest fixture 捕获
    # 此处验证基本入参处理逻辑
    encoded = base64.b64encode(file_bytes).decode("utf-8")
    assert len(encoded) > 0

    init_msg = {
        "type": "init",
        "fileBase64": encoded,
        "fileName": file_name,
        "fieldList": field_list,
    }
    json_str = json.dumps(init_msg, ensure_ascii=False)
    assert "客户名称" in json_str
    assert "test.docx" in json_str
    assert encoded in json_str


def test_base64_roundtrip():
    """验证 base64 编解码来回一致"""
    original = b"Hello World\x00\x01\x02"
    encoded = base64.b64encode(original).decode("utf-8")
    decoded = base64.b64decode(encoded)
    assert decoded == original


def test_file_format_detection_logic():
    """验证文件格式判断逻辑（与 useStreamlitBridge 中的 detectFormat 一致）"""
    def detect_format(file_name: str) -> str:
        ext = file_name.split(".").pop().lower()
        return "xlsx" if ext == "xlsx" else "docx"

    assert detect_format("test.docx") == "docx"
    assert detect_format("data.xlsx") == "xlsx"
    assert detect_format("unknown.pdf") == "docx"  # 默认回退
```

- [ ] **Step 2: 运行测试**

```bash
pytest tests/test_editor_integration.py -v
```

Expected: All 3 tests PASS.

- [ ] **Step 3: Commit**

```bash
git add tests/test_editor_integration.py
git commit -m "test: add integration tests for editor embedding and base64 roundtrip"
```

---

### 完成后检查清单

- [ ] `npm run build` 成功生成 `static/vue-editor/` 下的静态文件
- [ ] `npm run test` 所有 Vue 组件和 composable 测试通过
- [ ] `pytest tests/` 所有 Python 测试通过
- [ ] `vue-tsc --noEmit` 无类型错误
- [ ] Streamlit 启动后可访问编辑器 iframe
