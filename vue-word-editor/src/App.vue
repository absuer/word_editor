<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'
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

// Listen for Streamlit init messages via postMessage
function handleMessage(event: MessageEvent) {
  const msg = event.data as StreamlitInitMessage
  if (msg?.type === 'init') {
    receiveFromStreamlit(msg)
  }
}

onMounted(() => {
  window.addEventListener('message', handleMessage)
})

onBeforeUnmount(() => {
  window.removeEventListener('message', handleMessage)
})

// 处理字段插入：点击字段面板 → 插入 {{ 字段名 }} 到编辑器
function handleInsertField(field: Field) {
  const text = `{{ ${field.name} }}`
  editorRef.value?.insertText(text)
}

// 处理下载：触发 OnlyOffice 保存 → onSave 回调 → sendToStreamlit
function handleDownload() {
  editorRef.value?.requestSave()
}

// 处理来自 EditorPanel 的保存事件（OnlyOffice onDownloadAs 完成后触发）
function handleSave(base64: string, fileName: string) {
  sendToStreamlit(base64, fileName)
}
</script>

<template>
  <div class="editor-layout">
    <div class="editor-main">
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

.editor-main {
  flex: 4;
  display: flex;
  flex-direction: column;
  min-width: 0;
  height: 100%;
}
</style>
