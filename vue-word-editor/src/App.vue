<script setup lang="ts">
import { ref, onMounted } from 'vue'
import TitleBar from '@/components/TitleBar.vue'
import EditorPanel from '@/components/EditorPanel.vue'
import FileUploader from '@/components/FileUploader.vue'
import FieldPanel from '@/components/field/FieldPanel.vue'
import { useEditorState } from '@/composables/useEditorState'
import type { Field } from '@/types'

const {
  fileData,
  fieldList,
  bridgeLoading,
  bridgeError,
  openFile,
  loadFromSession,
  downloadFile,
} = useEditorState()
const editorRef = ref<InstanceType<typeof EditorPanel> | null>(null)

// Detect ?session= from URL (launched by Streamlit)
onMounted(async () => {
  const params = new URLSearchParams(window.location.search)
  const sessionId = params.get('session')
  if (sessionId) {
    try {
      await loadFromSession(sessionId)
    } catch {
      // error is already set in bridgeError by loadFromSession
    }
  }
})

function handleUpload(payload: { fileBase64: string; fileName: string }) {
  openFile(payload.fileBase64, payload.fileName)
}

function handleNewFile() {
  fileData.value = null
}

function handleInsertField(field: Field) {
  editorRef.value?.insertText(`{{ ${field.name} }}`)
}

function handleDownload() {
  editorRef.value?.requestSave()
}

function handleSave(base64: string, fileName: string) {
  downloadFile(base64, fileName)
}
</script>

<template>
  <div class="editor-layout">
    <div class="editor-main">
      <!-- Loading: fetching file from bridge -->
      <div v-if="bridgeLoading" class="editor-status">
        <div class="editor-status__spinner" />
        <p>正在加载文档...</p>
      </div>

      <!-- Error: bridge fetch failed -->
      <div v-else-if="bridgeError" class="editor-status editor-status--error">
        <p>❌ {{ bridgeError }}</p>
        <p class="editor-status__hint">
          请确保智能客服系统已启动，或直接上传文件开始编辑
        </p>
      </div>

      <!-- Editor loaded -->
      <template v-else-if="fileData">
        <TitleBar
          :file-name="fileData.fileName"
          @download="handleDownload"
          @new-file="handleNewFile"
        />
        <EditorPanel
          ref="editorRef"
          :file-data="fileData"
          @save="handleSave"
        />
      </template>

      <!-- No file data: standalone mode -->
      <FileUploader v-else @upload="handleUpload" />
    </div>
    <FieldPanel
      v-if="fileData"
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

.editor-status {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  color: #666;
  font-size: 14px;
}

.editor-status--error {
  color: #c62828;
}

.editor-status__hint {
  font-size: 12px;
  color: #999;
}

.editor-status__spinner {
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
</style>
