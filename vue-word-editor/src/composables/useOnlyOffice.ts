import { ref } from 'vue'
import type { OnlyOfficeConfig, DocumentType } from '@/types'
import type { DocEditor } from '@onlyoffice/doceditor-types'

/**
 * OnlyOffice DocEditor lifecycle management.
 *
 * Uses global DocsAPI.DocEditor constructor.
 * Editor renders into a specified DOM element, runs internally via WebAssembly.
 * // TODO: verify correct OnlyOffice Web SDK URL for pure frontend mode
 * API script is dynamically loaded from OnlyOffice CDN.
 */

declare global {
  interface Window {
    DocsAPI: {
      DocEditor: new (placeholderId: string, config: any) => DocEditor
    }
  }
}

/**
 * Module-level save callback so onDownloadAs can access it
 * without relying on closure serialization.
 */
let onSaveCallback: ((base64: string) => void) | null = null

export function useOnlyOffice() {
  const editorInstance = ref<DocEditor | null>(null)
  const isReady = ref(false)
  const isLoading = ref(false)
  const error = ref('')

  function getDocumentType(format: 'docx' | 'xlsx'): DocumentType {
    return format === 'xlsx' ? 'cell' : 'word'
  }

  function buildConfig(
    placeholderId: string,
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
    // TODO: verify correct OnlyOffice Web SDK URL for pure frontend mode
    return new Promise((resolve, reject) => {
      if (typeof window.DocsAPI !== 'undefined') {
        resolve()
        return
      }

      const scriptId = 'onlyoffice-api-script'
      if (document.getElementById(scriptId)) {
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
      script.src = 'http://localhost:8080/web-apps/apps/api/documents/api.js'
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
    onSaveCallback = onSave

    try {
      await loadApiScript()

      const config = buildConfig(placeholderId, fileName, format)
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
          onDownloadAs: async (event: any) => {
            if (event.data?.url && onSaveCallback) {
              try {
                const response = await fetch(event.data.url)
                const blob = await response.blob()
                const reader = new FileReader()
                reader.onloadend = () => {
                  const result = reader.result as string
                  const commaIndex = result.indexOf(',')
                  const base64Data = commaIndex >= 0 ? result.substring(commaIndex + 1) : result
                  if (onSaveCallback) {
                    onSaveCallback(base64Data)
                  }
                }
                reader.readAsDataURL(blob)
              } catch (e) {
                console.error('Failed to download document:', e)
              }
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
      error.value = 'OnlyOffice 编辑器加载失败。请确认 Docker 已启动且 OnlyOffice Document Server 正在运行（docker run -d -p 8080:80 onlyoffice/documentserver）。'
      console.error('Failed to initialize OnlyOffice editor:', e)
      isLoading.value = false
    }
  }

  /**
   * Trigger OnlyOffice save. In pure frontend mode, calls downloadAs()
   * which triggers the onDownloadAs event to retrieve document data.
   */
  function requestSave(): void {
    if (!editorInstance.value || !isReady.value) return

    try {
      editorInstance.value.downloadAs()
    } catch {
      console.warn('downloadAs() not available')
    }
  }

  function destroy(): void {
    if (editorInstance.value) {
      try {
        editorInstance.value.destroyEditor()
      } catch {
        // ignore destroy errors
      }
      editorInstance.value = null
    }
    isReady.value = false
    isLoading.value = false
    onSaveCallback = null
  }

  /**
   * Insert text into the editor document at cursor position.
   * Uses OnlyOffice connector API. Closures do not survive serialization,
   * so text is passed as a command argument rather than captured via scope.
   */
  function insertText(text: string): void {
    if (!editorInstance.value || !isReady.value) return

    try {
      const connector = editorInstance.value.createConnector()
      connector.callCommand(
        function (t: string) {
          // Executes in the OnlyOffice editor context
          const doc = (window as any).Api.GetDocument()
          const paragraph = (window as any).Api.CreateParagraph()
          paragraph.AddText(t)
          doc.InsertContent([paragraph])
        } as any,
        undefined,
        [text] as any,
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
