import { ref } from 'vue'
import type {
  Field,
  FileData,
  StreamlitInitMessage,
  StreamlitDownloadMessage,
} from '@/types'

export function useStreamlitBridge() {
  const fileData = ref<FileData | null>(null)
  const fieldList = ref<Field[]>([])

  function detectFormat(fileName: string): 'docx' | 'xlsx' {
    const ext = fileName.split('.').pop()?.toLowerCase()
    if (ext === 'xlsx') return 'xlsx'
    return 'docx'
  }

  function receiveFromStreamlit(message: StreamlitInitMessage): void {
    if (message.type !== 'init') return

    fileData.value = {
      base64: message.fileBase64,
      fileName: message.fileName,
      format: detectFormat(message.fileName),
    }

    if (Array.isArray(message.fieldList)) {
      fieldList.value = message.fieldList
    }
  }

  function sendToStreamlit(base64: string, fileName: string): void {
    const msg: StreamlitDownloadMessage = {
      type: 'download',
      fileBase64: base64,
      fileName,
    }
    window.parent.postMessage(msg, '*')
  }

  return {
    fileData,
    fieldList,
    receiveFromStreamlit,
    sendToStreamlit,
    detectFormat,
  }
}
