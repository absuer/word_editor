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
