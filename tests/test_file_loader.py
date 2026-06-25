"""Tests for file_loader module."""
import os
import tempfile
import pytest
from modules.file_loader import FileLoader, detect_file_type, SUPPORTED_TYPES


class TestDetectFileType:
    def test_detects_pdf(self):
        assert detect_file_type("contract.pdf") == "pdf"

    def test_detects_docx(self):
        assert detect_file_type("report.docx") == "docx"

    def test_detects_txt(self):
        assert detect_file_type("notes.txt") == "txt"

    def test_detects_md(self):
        assert detect_file_type("README.md") == "markdown"

    def test_detects_csv(self):
        assert detect_file_type("data.csv") == "csv"

    def test_detects_html(self):
        assert detect_file_type("page.html") == "html"

    def test_detects_image_png(self):
        assert detect_file_type("photo.png") == "image"

    def test_detects_image_jpg(self):
        assert detect_file_type("scan.jpg") == "image"

    def test_detects_image_jpeg(self):
        assert detect_file_type("img.jpeg") == "image"

    def test_returns_none_for_unknown(self):
        assert detect_file_type("file.xyz") is None

    def test_case_insensitive(self):
        assert detect_file_type("FILE.PDF") == "pdf"


class TestFileLoader:
    def test_load_txt_file(self):
        content = "Hello, this is a test document.\nIt has multiple lines.\n第三行中文内容。"
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8") as f:
            f.write(content)
            tmp_path = f.name

        try:
            loader = FileLoader()
            docs = loader.load_file(tmp_path)
            assert len(docs) > 0
            assert "Hello" in docs[0].page_content
            assert docs[0].metadata["source"] == os.path.basename(tmp_path)
            assert docs[0].metadata["file_type"] == "txt"
        finally:
            os.unlink(tmp_path)

    def test_load_csv_file(self):
        content = "name,age,city\nAlice,30,Beijing\nBob,25,Shanghai"
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8") as f:
            f.write(content)
            tmp_path = f.name

        try:
            loader = FileLoader()
            docs = loader.load_file(tmp_path)
            assert len(docs) > 0
        finally:
            os.unlink(tmp_path)

    def test_unsupported_file_type(self):
        loader = FileLoader()
        with pytest.raises(ValueError, match="Unsupported file type"):
            loader.load_file("test.xyz")
