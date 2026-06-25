import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import FieldPanel from '@/components/field/FieldPanel.vue'

const mockFields = [
  { id: '1', name: '客户名称', icon: '👤' },
  { id: '2', name: '合同金额', icon: '💰' },
  { id: '3', name: '签订日期', icon: '📅' },
]

describe('FieldPanel', () => {
  it('renders all fields initially', () => {
    const wrapper = mount(FieldPanel, {
      props: { fields: mockFields }
    })
    expect(wrapper.text()).toContain('客户名称')
    expect(wrapper.text()).toContain('合同金额')
    expect(wrapper.text()).toContain('签订日期')
  })

  it('renders panel title', () => {
    const wrapper = mount(FieldPanel, {
      props: { fields: mockFields }
    })
    expect(wrapper.text()).toContain('字段列表')
  })

  it('filters fields by search query', async () => {
    const wrapper = mount(FieldPanel, {
      props: { fields: mockFields }
    })
    const searchInput = wrapper.find('[data-test="field-search"] input')
    await searchInput.setValue('客户')
    expect(wrapper.text()).toContain('客户名称')
    expect(wrapper.text()).not.toContain('合同金额')
    expect(wrapper.text()).not.toContain('签订日期')
  })

  it('filters are case-insensitive', async () => {
    const wrapper = mount(FieldPanel, {
      props: { fields: mockFields }
    })
    const searchInput = wrapper.find('[data-test="field-search"] input')
    await searchInput.setValue('金额')
    expect(wrapper.text()).toContain('合同金额')
  })

  it('emits insert event when a field is clicked', async () => {
    const wrapper = mount(FieldPanel, {
      props: { fields: mockFields }
    })
    const firstField = wrapper.find('[data-test="field-item"]')
    await firstField.trigger('click')
    expect(wrapper.emitted('insert')).toBeTruthy()
    expect(wrapper.emitted('insert')![0][0]).toEqual(mockFields[0])
  })

  it('shows empty state when no fields match', async () => {
    const wrapper = mount(FieldPanel, {
      props: { fields: mockFields }
    })
    const searchInput = wrapper.find('[data-test="field-search"] input')
    await searchInput.setValue('不存在的字段')
    expect(wrapper.text()).toContain('无匹配字段')
    expect(wrapper.findAll('[data-test="field-item"]').length).toBe(0)
  })
})
