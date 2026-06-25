<script setup lang="ts">
import { ref } from 'vue'
import WordEditorCore from './WordEditorCore.vue'

defineProps<{
  fileData: { base64: string; fileName: string; format: 'docx' | 'xlsx' } | null
}>()

const emit = defineEmits<{
  save: [base64: string, fileName: string]
}>()

const coreRef = ref<InstanceType<typeof WordEditorCore> | null>(null)

function insertText(text: string) {
  coreRef.value?.insertText(text)
}

function requestSave() {
  coreRef.value?.requestSave()
}

defineExpose({ insertText, requestSave })
</script>

<template>
  <WordEditorCore
    v-if="fileData"
    ref="coreRef"
    :file-data="fileData"
    @save="(base64: string, fileName: string) => emit('save', base64, fileName)"
  />
</template>
