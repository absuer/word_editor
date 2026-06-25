import { ref } from 'vue'
import type { OnlyOfficeConfig, DocumentType } from '@/types'

/**
 * OnlyOffice DocEditor 生命周期管理
 *
 * 使用全局 DocsAPI.DocEditor 构造函数。
 * 编辑器渲染到指定的 DOM 元素中，内部以 WebAssembly 运行。
 * API 脚本从 OnlyOffice CDN 动态加载。
 */

// 声明全局 DocsAPI 类型
declare global {
  interface Window {
    DocsAPI: {
      DocEditor: new (placeholderId: string, config: any) => any
    }
  }
}

export function useOnlyOffice() {
  const editorInstance = ref<any>(null)
  const isReady = ref(false)
  const isLoading = ref(false)

  function getFileType(format: 'docx' | 'xlsx'): string {
    return format
  }

  function getDocumentType(format: 'docx' | 'xlsx'): DocumentType {
    return format === 'xlsx' ? 'cell' : 'word'
  }

  function buildConfig(
    placeholderId: string,
    base64: string,
    fileName: string,
    format: 'docx' | 'xlsx',
  ): OnlyOfficeConfig {
    return {
      documentType: getDocumentType(format),
      fileType: format,
      title: fileName,
      key: `${fileName}_${Date.now()}`,
      url: '',
      lang: 'zh-CN',
    }
  }

  function getMimeType(format: 'docx' | 'xlsx'): string {
    return format === 'xlsx'
      ? 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
      : 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
  }

  function loadApiScript(): Promise<void> {
    return new Promise((resolve, reject) => {
      if (typeof window.DocsAPI !== 'undefined') {
        resolve()
        return
      }

      const scriptId = 'onlyoffice-api-script'
      if (document.getElementById(scriptId)) {
        // Script is already loading, poll until available
        const interval = setInterval(() => {
          if (typeof window.DocsAPI !== 'undefined') {
            clearInterval(interval)
            resolve()
          }
        }, 100)
        return
      }

      const script = document.createElement('script')
      script.id = scriptId
      script.src = 'https://onlyoffice.github.io/sdkjs-plugins/v1/editors.js'
      script.onload = () => resolve()
      script.onerror = () => reject(new Error('Failed to load OnlyOffice API script'))
      document.head.appendChild(script)
    })
  }

  async function init(
    placeholderId: string,
    base64: string,
    fileName: string,
    format: 'docx' | 'xlsx',
    onSave: (base64: string) => void,
  ): Promise<void> {
    destroy()
    isLoading.value = true

    try {
      await loadApiScript()

      const config = buildConfig(placeholderId, base64, fileName, format)
      const mimeType = getMimeType(format)
      const dataUrl = `data:${mimeType};base64,${base64}`

      const fullConfig = {
        document: {
          fileType: config.fileType,
          key: config.key,
          title: config.title,
          url: dataUrl,
        },
        documentType: config.documentType,
        editorConfig: {
          mode: 'edit' as const,
          lang: config.lang,
          customization: {
            compactToolbar: false,
            forcesave: false,
          },
        },
        events: {
          onReady: () => {
            isReady.value = true
            isLoading.value = false
          },
          onRequestSave: (event: any) => {
            if (event.data) {
              onSave(event.data)
            }
          },
          onError: (event: any) => {
            console.error('OnlyOffice editor error:', event)
            isLoading.value = false
          },
        },
      }

      editorInstance.value = new window.DocsAPI.DocEditor(placeholderId, fullConfig)
    } catch (e) {
      console.error('Failed to initialize OnlyOffice editor:', e)
      isLoading.value = false
    }
  }

  /**
   * 触发 OnlyOffice 保存。在纯前端模式下通过 requestSave 事件获取内容。
   */
  function requestSave(): void {
    if (!editorInstance.value || !isReady.value) return

    try {
      editorInstance.value.document?.save()
    } catch {
      console.warn('save() not available')
    }
  }

  function destroy(): void {
    if (editorInstance.value) {
      try {
        editorInstance.value.destroyEditor()
      } catch {
        // 忽略销毁错误
      }
      editorInstance.value = null
    }
    isReady.value = false
    isLoading.value = false
  }

  /**
   * 向编辑器文档中插入文本。
   * 使用 OnlyOffice connector API 在光标位置插入内容。
   */
  function insertText(text: string): void {
    if (!editorInstance.value || !isReady.value) return

    try {
      const connector = editorInstance.value.createConnector()
      connector.callCommand(
        function () {
          // 此函数在 OnlyOffice 编辑器上下文中执行
          const doc = (window as any).Api.GetDocument()
          const paragraph = (window as any).Api.CreateParagraph()
          paragraph.AddText(text)
          doc.InsertContent([paragraph])
        },
        function () {
          // 命令完成回调（可选）
        },
      )
    } catch (e) {
      console.warn('insertText failed:', e)
    }
  }

  return {
    isReady,
    isLoading,
    init,
    requestSave,
    destroy,
    insertText,
  }
}
