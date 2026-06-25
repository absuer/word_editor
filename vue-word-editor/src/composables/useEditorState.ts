import { ref } from 'vue'
import type { Field, FileData } from '@/types'

/** Standalone editor state — no Streamlit dependency. */
export function useEditorState() {
  const fileData = ref<FileData | null>(null)
  const fieldList = ref<Field[]>([
    { id: '1', name: '客户名称', icon: '👤' },
    { id: '2', name: '合同金额', icon: '💰' },
    { id: '3', name: '签订日期', icon: '📅' },
    { id: '4', name: '产品名称', icon: '📦' },
    { id: '5', name: '交付地点', icon: '📍' },
  ])

  function detectFormat(fileName: string): 'docx' | 'xlsx' {
    const ext = fileName.split('.').pop()?.toLowerCase()
    return ext === 'xlsx' ? 'xlsx' : 'docx'
  }

  function openFile(fileBase64: string, fileName: string) {
    fileData.value = {
      base64: fileBase64,
      fileName,
      format: detectFormat(fileName),
    }
  }

  /** Trigger browser download from base64 data. */
  function downloadFile(base64: string, fileName: string) {
    const mimeType = fileName.endsWith('.xlsx')
      ? 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
      : 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'

    const byteString = atob(base64)
    const ab = new ArrayBuffer(byteString.length)
    const ia = new Uint8Array(ab)
    for (let i = 0; i < byteString.length; i++) {
      ia[i] = byteString.charCodeAt(i)
    }
    const blob = new Blob([ab], { type: mimeType })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = fileName
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  return { fileData, fieldList, detectFormat, openFile, downloadFile }
}
