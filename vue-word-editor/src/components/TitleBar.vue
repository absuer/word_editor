<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  fileName: string
}>()

const emit = defineEmits<{
  download: []
  'new-file': []
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
      class="title-bar__new"
      data-test="new-file-btn"
      @click="emit('new-file')"
    >
      新建
    </button>
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

.title-bar__new {
  background: transparent;
  color: #ccc;
  border: 1px solid #666;
  border-radius: 3px;
  padding: 3px 14px;
  font-size: 12px;
  cursor: pointer;
}

.title-bar__new:hover {
  background: #444;
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
