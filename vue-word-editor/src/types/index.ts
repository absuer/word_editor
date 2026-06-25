/** 字段项 */
export interface Field {
  id: string
  name: string
  icon?: string
}

/** 文件数据（Streamlit → Vue） */
export interface FileData {
  base64: string
  fileName: string
  format: 'docx' | 'xlsx'
}

/** Streamlit 发来的初始化消息 */
export interface StreamlitInitMessage {
  type: 'init'
  fileBase64: string
  fileName: string
  fieldList: Field[]
}

/** Vue 回传给 Streamlit 的下载消息 */
export interface StreamlitDownloadMessage {
  type: 'download'
  fileBase64: string
  fileName: string
}

/** OnlyOffice 文档类型 */
export type DocumentType = 'word' | 'cell'

/** OnlyOffice 事件回调 */
export interface OnlyOfficeEvents {
  onReady: () => void
  onSave: (base64: string) => void
}

/** OnlyOffice 编辑器配置 */
export interface OnlyOfficeConfig {
  documentType: DocumentType
  fileType: 'docx' | 'xlsx'
  title: string
  key: string
  url: string
  lang?: string
}
