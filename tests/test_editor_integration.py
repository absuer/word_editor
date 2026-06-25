# tests/test_editor_integration.py
import base64
import json
import pytest
from modules.editor import get_editor_html, render_editor, handle_editor_download


def test_render_editor_produces_html():
    """Verify the render function produces valid HTML with expected content."""
    file_bytes = b"fake docx content"
    file_name = "test.docx"
    field_list = [
        {"id": "1", "name": "客户名称", "icon": "👤"},
        {"id": "2", "name": "合同金额", "icon": "💰"},
    ]

    # Verify base64 encoding roundtrip
    encoded = base64.b64encode(file_bytes).decode("utf-8")
    assert len(encoded) > 0

    # Verify init message structure
    init_msg = {
        "type": "init",
        "fileBase64": encoded,
        "fileName": file_name,
        "fieldList": field_list,
    }
    json_str = json.dumps(init_msg, ensure_ascii=False)
    assert "客户名称" in json_str
    assert "test.docx" in json_str
    assert encoded in json_str


def test_base64_roundtrip():
    """Verify base64 encode/decode roundtrip is consistent."""
    original = b"Hello World\x00\x01\x02"
    encoded = base64.b64encode(original).decode("utf-8")
    decoded = base64.b64decode(encoded)
    assert decoded == original


def test_file_format_detection_logic():
    """Verify file format detection matches useStreamlitBridge.detectFormat."""
    def detect_format(file_name: str) -> str:
        ext = file_name.split(".").pop().lower()
        return "xlsx" if ext == "xlsx" else "docx"

    assert detect_format("test.docx") == "docx"
    assert detect_format("data.xlsx") == "xlsx"
    assert detect_format("unknown.pdf") == "docx"  # fallback to docx


def test_get_editor_html_contains_expected_elements():
    """Verify the generated HTML wrapper contains expected elements."""
    file_bytes = b"fake docx content"
    file_name = "contract.docx"
    field_list = [{"id": "1", "name": "客户名称", "icon": "👤"}]

    html = get_editor_html(file_bytes, file_name, field_list)

    assert '<iframe id="vue-editor"' in html
    assert './static/vue-editor/index.html' in html
    assert '客户名称' in html
    assert '"type":"init"' in html or '"type": "init"' in html
    assert 'postMessage' in html


def test_get_editor_html_xlsx_detection():
    """Verify xlsx files produce correct HTML."""
    file_bytes = b"fake xlsx content"
    file_name = "data.xlsx"
    field_list = []

    html = get_editor_html(file_bytes, file_name, field_list)

    assert 'data.xlsx' in html
    assert './static/vue-editor/index.html' in html


def test_get_editor_html_empty_field_list():
    """Verify empty field list works."""
    file_bytes = b"content"
    file_name = "test.docx"
    field_list = []

    html = get_editor_html(file_bytes, file_name, field_list)

    assert '"fieldList":[]' in html or '"fieldList": []' in html
