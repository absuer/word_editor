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
