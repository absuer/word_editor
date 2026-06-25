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

  const bridgeLoading = ref(false)
  const bridgeError = ref('')

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

  /**
   * Load file from public/temp/ via session ID.
   * Streamlit writes files to Vite's public/temp/ directory,
   * which Vite serves as static assets (same origin, no CORS).
   */
  async function loadFromSession(sessionId: string): Promise<void> {
    bridgeLoading.value = true
    bridgeError.value = ''

    try {
      // 1. Fetch metadata JSON
      const metaResp = await fetch(`/temp/${sessionId}.json`)
      if (!metaResp.ok) {
        throw new Error(`元数据加载失败 (HTTP ${metaResp.status})`)
      }
      const meta = await metaResp.json() as {
        fileName: string
        fieldList?: Field[]
      }

      // 2. Determine file extension
      const ext = meta.fileName.split('.').pop()?.toLowerCase() || 'docx'

      // 3. Fetch file bytes
      const fileResp = await fetch(`/temp/${sessionId}.${ext}`)
      if (!fileResp.ok) {
        throw new Error(`文件加载失败 (HTTP ${fileResp.status})`)
      }
      const blob = await fileResp.blob()

      // 4. Convert blob to base64
      const base64 = await new Promise<string>((resolve, reject) => {
        const reader = new FileReader()
        reader.onloadend = () => {
          const result = reader.result as string
          const commaIdx = result.indexOf(',')
          resolve(commaIdx >= 0 ? result.substring(commaIdx + 1) : result)
        }
        reader.onerror = () => reject(new Error('文件读取失败'))
        reader.readAsDataURL(blob)
      })

      // 5. Update state
      if (meta.fieldList && meta.fieldList.length > 0) {
        fieldList.value = meta.fieldList
      }
      openFile(base64, meta.fileName)
    } catch (e: any) {
      bridgeError.value = e?.message || '未知错误'
      throw e
    } finally {
      bridgeLoading.value = false
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

  return {
    fileData,
    fieldList,
    bridgeLoading,
    bridgeError,
    detectFormat,
    openFile,
    loadFromSession,
    downloadFile,
  }
}
