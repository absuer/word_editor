<script setup lang="ts">
import { ref, watch, onBeforeUnmount, nextTick } from 'vue'
import { useEditor, EditorContent } from '@tiptap/vue-3'
import StarterKit from '@tiptap/starter-kit'
import Underline from '@tiptap/extension-underline'
import TextAlign from '@tiptap/extension-text-align'
import { Color } from '@tiptap/extension-color'
import { Highlight } from '@tiptap/extension-highlight'
import { TextStyle } from '@tiptap/extension-text-style'
import mammoth from 'mammoth'
import { Document, Packer, Paragraph, TextRun } from 'docx'

const props = defineProps<{
  fileData: { base64: string; fileName: string; format: 'docx' | 'xlsx' } | null
}>()

const emit = defineEmits<{
  save: [base64: string, fileName: string]
}>()

const isReady = ref(false)
const isLoading = ref(false)

const editor = useEditor({
  extensions: [
    StarterKit,
    Underline,
    TextAlign.configure({ types: ['heading', 'paragraph'] }),
    TextStyle,
    Color,
    Highlight,
  ],
  content: '',
  editorProps: {
    attributes: {
      class: 'tiptap-editor',
    },
  },
  onUpdate: () => { /* content changes handled live */ },
})

async function loadDocx() {
  if (!props.fileData || !editor.value) return
  isLoading.value = true

  try {
    if (props.fileData.format === 'docx') {
      const byteString = atob(props.fileData.base64)
      const bytes = new Uint8Array(byteString.length)
      for (let i = 0; i < byteString.length; i++) {
        bytes[i] = byteString.charCodeAt(i)
      }
      const result = await mammoth.convertToHtml({ arrayBuffer: bytes.buffer })
      editor.value.commands.setContent(result.value || '<p></p>')
    } else {
      editor.value.commands.setContent('<p>（Excel 编辑暂不支持，请使用 .docx 文件）</p>')
    }
    isReady.value = true
  } catch (e) {
    console.error('Failed to load document:', e)
    editor.value.commands.setContent('<p>文档加载失败</p>')
  } finally {
    isLoading.value = false
  }
}

watch(() => props.fileData, async () => {
  await nextTick()
  loadDocx()
}, { immediate: true })

/** Insert text at cursor — called from FieldPanel */
function insertText(text: string) {
  editor.value?.commands.insertContent(text)
}

/** Generate .docx and emit save */
async function requestSave() {
  if (!editor.value) return

  try {
    const doc = new Document({
      sections: [{
        children: [new Paragraph({ children: [new TextRun(editor.value.getText())] })],
      }],
    })
    const blob = await Packer.toBlob(doc)
    const reader = new FileReader()
    reader.onloadend = () => {
      const base64 = (reader.result as string).split(',')[1]
      emit('save', base64, props.fileData?.fileName || 'document.docx')
    }
    reader.readAsDataURL(blob)
  } catch (e) {
    console.error('Failed to generate docx:', e)
  }
}

defineExpose({ insertText, requestSave })

onBeforeUnmount(() => {
  editor.value?.destroy()
})
</script>

<template>
  <div class="word-editor">
    <div v-if="isLoading" class="word-editor__loading">加载中...</div>
    <div v-if="editor" class="word-editor__toolbar">
      <button @click="editor.chain().focus().toggleBold().run()" :class="{ active: editor.isActive('bold') }"><b>B</b></button>
      <button @click="editor.chain().focus().toggleItalic().run()" :class="{ active: editor.isActive('italic') }"><i>I</i></button>
      <button @click="editor.chain().focus().toggleUnderline().run()" :class="{ active: editor.isActive('underline') }"><u>U</u></button>
      <button @click="editor.chain().focus().toggleStrike().run()" :class="{ active: editor.isActive('strike') }"><s>S</s></button>
      <span class="sep">|</span>
      <button @click="editor.chain().focus().toggleHeading({ level: 1 }).run()" :class="{ active: editor.isActive('heading', { level: 1 }) }">H1</button>
      <button @click="editor.chain().focus().toggleHeading({ level: 2 }).run()" :class="{ active: editor.isActive('heading', { level: 2 }) }">H2</button>
      <button @click="editor.chain().focus().toggleHeading({ level: 3 }).run()" :class="{ active: editor.isActive('heading', { level: 3 }) }">H3</button>
      <button @click="editor.chain().focus().setParagraph().run()">正文</button>
      <span class="sep">|</span>
      <button @click="editor.chain().focus().setTextAlign('left').run()" :class="{ active: editor.isActive({ textAlign: 'left' }) }">≡</button>
      <button @click="editor.chain().focus().setTextAlign('center').run()" :class="{ active: editor.isActive({ textAlign: 'center' }) }">≡</button>
      <button @click="editor.chain().focus().setTextAlign('right').run()" :class="{ active: editor.isActive({ textAlign: 'right' }) }">≡</button>
      <span class="sep">|</span>
      <button @click="editor.chain().focus().toggleBulletList().run()" :class="{ active: editor.isActive('bulletList') }">•</button>
      <button @click="editor.chain().focus().toggleOrderedList().run()" :class="{ active: editor.isActive('orderedList') }">1.</button>
    </div>
    <EditorContent :editor="editor" class="word-editor__content" />
  </div>
</template>

<style scoped>
.word-editor {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
  background: #fff;
}

.word-editor__loading {
  padding: 12px 16px;
  color: #999;
  font-size: 13px;
}

.word-editor__toolbar {
  display: flex;
  flex-wrap: wrap;
  gap: 3px;
  padding: 6px 12px;
  background: #f5f5f5;
  border-bottom: 1px solid #e0e0e0;
  flex-shrink: 0;
}

.word-editor__toolbar button {
  background: #fff;
  border: 1px solid #ccc;
  border-radius: 3px;
  padding: 3px 8px;
  font-size: 12px;
  cursor: pointer;
  min-width: 24px;
}

.word-editor__toolbar button:hover {
  background: #e8e8e8;
}

.word-editor__toolbar button.active {
  background: #1976d2;
  color: #fff;
  border-color: #1976d2;
}

.word-editor__toolbar .sep {
  color: #ddd;
  margin: 0 2px;
  align-self: center;
}

.word-editor__content {
  flex: 1;
  overflow-y: auto;
  padding: 24px 32px;
}

.word-editor__content :deep(.tiptap-editor) {
  outline: none;
  min-height: 100%;
  font-size: 14px;
  line-height: 1.7;
}

.word-editor__content :deep(h1) { font-size: 24px; margin: 16px 0 8px; }
.word-editor__content :deep(h2) { font-size: 20px; margin: 14px 0 6px; }
.word-editor__content :deep(h3) { font-size: 16px; margin: 12px 0 4px; }
.word-editor__content :deep(p) { margin: 4px 0; }
.word-editor__content :deep(ul), .word-editor__content :deep(ol) { padding-left: 24px; }
</style>
