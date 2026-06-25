import { describe, it, expect } from 'vitest'
import { useFieldManager } from '@/composables/useFieldManager'
import type { Field } from '@/types'

const sampleFields: Field[] = [
  { id: '1', name: '客户名称', icon: '👤' },
  { id: '2', name: '合同金额', icon: '💰' },
  { id: '3', name: '签订日期', icon: '📅' },
]

describe('useFieldManager', () => {
  it('returns all fields when searchQuery is empty', () => {
    const { filteredFields } = useFieldManager(sampleFields)
    expect(filteredFields.value).toHaveLength(3)
  })

  it('filters fields by search query', () => {
    const { filteredFields, searchQuery } = useFieldManager(sampleFields)
    searchQuery.value = '客户'
    expect(filteredFields.value).toHaveLength(1)
    expect(filteredFields.value[0].name).toBe('客户名称')
  })

  it('is case-insensitive', () => {
    const { filteredFields, searchQuery } = useFieldManager(sampleFields)
    searchQuery.value = '金额'
    expect(filteredFields.value).toHaveLength(1)
  })

  it('returns empty array when no match', () => {
    const { filteredFields, searchQuery } = useFieldManager(sampleFields)
    searchQuery.value = '不存在'
    expect(filteredFields.value).toHaveLength(0)
  })

  it('insertField returns the correct placeholder text', () => {
    const { insertField } = useFieldManager(sampleFields)
    const result = insertField(sampleFields[0])
    expect(result).toBe('{{ 客户名称 }}')
  })
})
