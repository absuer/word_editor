import { ref, computed } from 'vue'
import type { Field } from '@/types'

export function useFieldManager(initialFields: Field[] = []) {
  const fields = ref<Field[]>([...initialFields])
  const searchQuery = ref('')

  const filteredFields = computed(() => {
    if (!searchQuery.value.trim()) {
      return fields.value
    }
    const q = searchQuery.value.toLowerCase()
    return fields.value.filter(f => f.name.toLowerCase().includes(q))
  })

  function insertField(field: Field): string {
    return `{{ ${field.name} }}`
  }

  return {
    fields,
    searchQuery,
    filteredFields,
    insertField,
  }
}
