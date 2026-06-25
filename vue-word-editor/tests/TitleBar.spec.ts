import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import TitleBar from '@/components/TitleBar.vue'

describe('TitleBar', () => {
  it('renders the file name', () => {
    const wrapper = mount(TitleBar, {
      props: { fileName: 'contract.docx' }
    })
    expect(wrapper.text()).toContain('contract.docx')
  })

  it('renders Word icon for docx files', () => {
    const wrapper = mount(TitleBar, {
      props: { fileName: 'test.docx' }
    })
    expect(wrapper.text()).toContain('📄')
  })

  it('renders Excel icon for xlsx files', () => {
    const wrapper = mount(TitleBar, {
      props: { fileName: 'data.xlsx' }
    })
    expect(wrapper.text()).toContain('📊')
  })

  it('emits download event when download button is clicked', async () => {
    const wrapper = mount(TitleBar, {
      props: { fileName: 'test.docx' }
    })
    await wrapper.find('[data-test="download-btn"]').trigger('click')
    expect(wrapper.emitted('download')).toBeTruthy()
    expect(wrapper.emitted('download')![0]).toEqual([])
  })
})
