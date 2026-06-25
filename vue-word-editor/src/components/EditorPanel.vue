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
