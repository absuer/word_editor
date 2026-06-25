<script setup lang="ts">
import { ref } from 'vue'
import TitleBar from '@/components/TitleBar.vue'
import EditorPanel from '@/components/EditorPanel.vue'
import FileUploader from '@/components/FileUploader.vue'
import FieldPanel from '@/components/field/FieldPanel.vue'
import { useEditorState } from '@/composables/useEditorState'
import type { Field } from '@/types'

const { fileData, fieldList, openFile, downloadFile } = useEditorState()
const editorRef = ref<InstanceType<typeof EditorPanel> | null>(null)

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
      <template v-if="fileData">
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
</style>
