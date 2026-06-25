<script setup lang="ts">
import type { Field } from '@/types'

defineProps<{
  field: Field
}>()

const emit = defineEmits<{
  select: [field: Field]
}>()

const syntaxHint = '{{ }}'
</script>

<template>
  <div
    class="field-item"
    data-test="field-item"
    @click="emit('select', field)"
  >
    <span class="field-item__icon">{{ field.icon || '📌' }}</span>
    <span class="field-item__name">{{ field.name }}</span>
    <span class="field-item__syntax">{{ syntaxHint }}</span>
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
