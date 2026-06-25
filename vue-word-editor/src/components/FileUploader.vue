<script setup lang="ts">
import { ref } from 'vue'

const emit = defineEmits<{
  upload: [payload: { fileBase64: string; fileName: string }]
}>()

const isDragOver = ref(false)
const uploadError = ref('')
const fileInput = ref<HTMLInputElement | null>(null)

function detectFormat(fileName: string): 'docx' | 'xlsx' {
  const ext = fileName.split('.').pop()?.toLowerCase()
  return ext === 'xlsx' ? 'xlsx' : 'docx'
}

function readFile(file: File) {
  const format = detectFormat(file.name)
  if (!['docx', 'xlsx'].includes(format)) {
    uploadError.value = '仅支持 .docx 和 .xlsx 格式'
    return
  }
  uploadError.value = ''

  const reader = new FileReader()
  reader.onload = () => {
    const base64 = (reader.result as string).split(',')[1]
    emit('upload', { fileBase64: base64, fileName: file.name })
  }
  reader.onerror = () => {
    uploadError.value = '文件读取失败，请重试'
  }
  reader.readAsDataURL(file)
}

function onFileChange(e: Event) {
  const input = e.target as HTMLInputElement
  if (input.files && input.files[0]) {
    readFile(input.files[0])
  }
}

function onDrop(e: DragEvent) {
  isDragOver.value = false
  const file = e.dataTransfer?.files?.[0]
  if (file) readFile(file)
}

function onDragOver(e: DragEvent) {
  e.preventDefault()
  isDragOver.value = true
}

function onDragLeave() {
  isDragOver.value = false
}

function triggerFileInput() {
  fileInput.value?.click()
}
</script>

<template>
  <div class="uploader">
    <div class="uploader__header">
      <h1>📝 在线文档编辑器</h1>
      <p>支持 Word (.docx) 和 Excel (.xlsx) 文件</p>
    </div>
    <div
      class="uploader__zone"
      :class="{ 'uploader__zone--active': isDragOver }"
      @drop.prevent="onDrop"
      @dragover.prevent="onDragOver"
      @dragleave="onDragLeave"
      @click="triggerFileInput"
    >
      <input
        ref="fileInput"
        type="file"
        accept=".docx,.xlsx"
        class="uploader__input"
        @change="onFileChange"
      />
      <div class="uploader__icon">📁</div>
      <div class="uploader__text">
        <strong>点击选择文件</strong> 或拖拽文件到此处
      </div>
      <div class="uploader__hint">支持 .docx / .xlsx</div>
    </div>
    <div v-if="uploadError" class="uploader__error">{{ uploadError }}</div>
  </div>
</template>

<style scoped>
.uploader {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  padding: 40px 20px;
  background: #fff;
}

.uploader__header {
  text-align: center;
  margin-bottom: 32px;
}

.uploader__header h1 {
  font-size: 28px;
  color: #333;
  margin: 0 0 8px;
}

.uploader__header p {
  font-size: 14px;
  color: #999;
  margin: 0;
}

.uploader__zone {
  width: 100%;
  max-width: 420px;
  padding: 48px 24px;
  border: 2px dashed #ccc;
  border-radius: 12px;
  text-align: center;
  cursor: pointer;
  transition: border-color 0.2s, background 0.2s;
}

.uploader__zone:hover {
  border-color: #1976d2;
  background: #f5f8ff;
}

.uploader__zone--active {
  border-color: #1976d2;
  background: #e3f2fd;
}

.uploader__input {
  display: none;
}

.uploader__icon {
  font-size: 48px;
  margin-bottom: 12px;
}

.uploader__text {
  font-size: 15px;
  color: #555;
  margin-bottom: 6px;
}

.uploader__hint {
  font-size: 12px;
  color: #aaa;
}

.uploader__error {
  margin-top: 16px;
  padding: 8px 16px;
  background: #ffebee;
  color: #c62828;
  border-radius: 6px;
  font-size: 13px;
}
</style>
