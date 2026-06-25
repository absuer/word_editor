<script setup lang="ts">
const model = defineModel<string>({ required: true })
</script>

<template>
  <div class="field-search" data-test="field-search">
    <input
      v-model="model"
      type="text"
      class="field-search__input"
      placeholder="搜索字段..."
    />
  </div>
</template>

<style scoped>
.field-search {
  padding: 8px 10px;
}

.field-search__input {
  width: 100%;
  padding: 6px 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 12px;
  outline: none;
}

.field-search__input:focus {
  border-color: #1976d2;
  box-shadow: 0 0 0 2px rgba(25, 118, 210, 0.1);
}
</style>
