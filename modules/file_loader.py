"""Multi-format file loader with automatic type detection and chunking."""
import os
import uuid
from typing import List, Optional
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import CHUNK_SIZE, CHUNK_OVERLAP, UPLOAD_DIR

SUPPORTED_TYPES = {
    "pdf": "PyPDFLoader",
    "docx": "Docx2txtLoader",
    "txt": "TextLoader",
    "csv": "CSVLoader",
    "markdown": "UnstructuredMarkdownLoader",
    "html": "WebBaseLoader",
    "image": "OCRLoader",
}


def detect_file_type(file_path: str) -> Optional[str]:
    """Detect file type from extension. Returns None if unsupported."""
    ext = os.path.splitext(file_path)[1].lower()
    mapping = {
        ".pdf": "pdf",
        ".docx": "docx",
        ".txt": "txt",
        ".md": "markdown",
        ".csv": "csv",
        ".html": "html",
        ".htm": "html",
        ".png": "image",
        ".jpg": "image",
        ".jpeg": "image",
    }
    return mapping.get(ext)


class FileLoader:
    """Load and chunk files of various formats."""

    def __init__(self, chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", "。", ".", " ", ""],
        )
        os.makedirs(UPLOAD_DIR, exist_ok=True)

    def load_file(self, file_path: str) -> List[Document]:
        """Load a file, auto-detect type, parse, and split into chunks."""
        file_type = detect_file_type(file_path)
        if file_type is None:
            raise ValueError(f"Unsupported file type: {file_path}")

        raw_docs = self._load_raw(file_path, file_type)
        chunks = self.text_splitter.split_documents(raw_docs)

        file_name = os.path.basename(file_path)
        upload_time = self._get_upload_time()
        for i, chunk in enumerate(chunks):
            chunk.metadata.update({
                "source": file_name,
                "file_type": file_type,
                "chunk_index": i,
                "upload_time": upload_time,
            })
        return chunks

    def _load_raw(self, file_path: str, file_type: str) -> List[Document]:
        """Dispatch to the appropriate loader based on file type."""
        if file_type == "pdf":
            from langchain_community.document_loaders import PyPDFLoader
            loader = PyPDFLoader(file_path)
            return loader.load()

        elif file_type == "docx":
            from langchain_community.document_loaders import Docx2txtLoader
            loader = Docx2txtLoader(file_path)
            return loader.load()

        elif file_type == "txt":
            from langchain_community.document_loaders import TextLoader
            loader = TextLoader(file_path, encoding="utf-8")
            return loader.load()

        elif file_type == "csv":
            from langchain_community.document_loaders import CSVLoader
            loader = CSVLoader(file_path, encoding="utf-8")
            return loader.load()

        elif file_type == "markdown":
            from langchain_community.document_loaders import UnstructuredMarkdownLoader
            loader = UnstructuredMarkdownLoader(file_path)
            return loader.load()

        elif file_type == "html":
            from langchain_community.document_loaders import WebBaseLoader
            loader = WebBaseLoader(f"file://{file_path}")
            return loader.load()

        elif file_type == "image":
            return self._ocr_image(file_path)

        raise ValueError(f"Unsupported file type: {file_type}")

    def _ocr_image(self, file_path: str) -> List[Document]:
        """Extract text from image using pytesseract OCR."""
        try:
            import pytesseract
            from PIL import Image
        except ImportError:
            raise ImportError("pytesseract and Pillow are required for image OCR. pip install pytesseract Pillow")

        img = Image.open(file_path)
        text = pytesseract.image_to_string(img, lang="chi_sim+eng")
        doc = Document(
            page_content=text,
            metadata={"source": os.path.basename(file_path), "page": 1}
        )
        return [doc]

    def save_upload(self, uploaded_file) -> str:
        """Save an uploaded file to data/uploads/ with a unique name."""
        safe_name = f"{uuid.uuid4().hex[:8]}_{uploaded_file.name}"
        dest_path = os.path.join(UPLOAD_DIR, safe_name)
        with open(dest_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return dest_path

    @staticmethod
    def _get_upload_time() -> str:
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M")
