import { describe, it, expect, beforeEach, vi } from 'vitest'
import { useStreamlitBridge } from '@/composables/useStreamlitBridge'
import type { StreamlitInitMessage } from '@/types'

const mockMessage: StreamlitInitMessage = {
  type: 'init',
  fileBase64: 'UEsDBBQAAAAIAAAAA==',
  fileName: 'contract.docx',
  fieldList: [
    { id: '1', name: '客户名称', icon: '👤' },
    { id: '2', name: '合同金额', icon: '💰' },
  ],
}

describe('useStreamlitBridge', () => {
  beforeEach(() => {
    vi.restoreAllMocks()
  })

  it('initializes with null fileData and empty fieldList', () => {
    const { fileData, fieldList } = useStreamlitBridge()
    expect(fileData.value).toBeNull()
    expect(fieldList.value).toEqual([])
  })

  it('receiveFromStreamlit parses init message correctly via postMessage', () => {
    const { fileData, fieldList, receiveFromStreamlit } = useStreamlitBridge()

    receiveFromStreamlit(mockMessage)

    expect(fileData.value).toEqual({
      base64: 'UEsDBBQAAAAIAAAAA==',
      fileName: 'contract.docx',
      format: 'docx',
    })
    expect(fieldList.value).toHaveLength(2)
    expect(fieldList.value[0].name).toBe('客户名称')
  })

  it('receiveFromStreamlit detects xlsx format', () => {
    const { fileData, receiveFromStreamlit } = useStreamlitBridge()

    receiveFromStreamlit({
      ...mockMessage,
      fileName: 'data.xlsx',
    })

    expect(fileData.value!.format).toBe('xlsx')
  })

  it('sendToStreamlit posts download message to parent window', () => {
    const mockPostMessage = vi.fn()

    // Use vi.stubGlobal BEFORE calling useStreamlitBridge
    vi.stubGlobal('window', {
      parent: {
        postMessage: mockPostMessage,
      },
    })

    // Re-create after stubbing
    const { sendToStreamlit } = useStreamlitBridge()

    sendToStreamlit('base64content', 'output.docx')

    expect(mockPostMessage).toHaveBeenCalledWith(
      {
        type: 'download',
        fileBase64: 'base64content',
        fileName: 'output.docx',
      },
      '*'
    )
  })
})
