"""Vue Word/Excel Editor integration - pure functions for embedding."""

import base64
import json
import streamlit.components.v1 as components


def get_editor_html(file_bytes: bytes, file_name: str, field_list: list[dict]) -> str:
    """Generate the HTML wrapper that embeds the Vue editor iframe.

    Args:
        file_bytes: Raw bytes of the uploaded .docx/.xlsx file.
        file_name: Original filename (used for format detection).
        field_list: List of fields, e.g. [{"id": "1", "name": "客户名称", "icon": "👤"}, ...].

    Returns:
        HTML string ready for st.components.v1.html().
    """
    file_base64 = base64.b64encode(file_bytes).decode("utf-8")

    init_message = {
        "type": "init",
        "fileBase64": file_base64,
        "fileName": file_name,
        "fieldList": field_list,
    }
    init_json = json.dumps(init_message, ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    html, body {{ height: 100%; width: 100%; overflow: hidden; }}
    iframe {{ border: none; width: 100%; height: 100%; }}
  </style>
</head>
<body>
  <iframe id="vue-editor" src="./static/vue-editor/index.html"></iframe>
  <script>
    const initData = {init_json};

    var iframe = document.getElementById('vue-editor');
    iframe.addEventListener('load', function() {{
      iframe.contentWindow.postMessage(initData, '*');
    }});

    // Listen for download messages from the Vue editor
    window.addEventListener('message', function(event) {{
      if (event.data && event.data.type === 'download') {{
        // Forward the download data to Streamlit
        window.parent.postMessage(event.data, '*');
      }}
    }});
  </script>
</body>
</html>"""


def render_editor(file_bytes: bytes, file_name: str, field_list: list[dict], height: int = 700) -> None:
    """Render the Vue Word/Excel editor inside Streamlit.

    Args:
        file_bytes: Raw bytes of the uploaded file.
        file_name: Original filename.
        field_list: Fields for the right-side panel.
        height: iframe height in pixels.
    """
    editor_html = get_editor_html(file_bytes, file_name, field_list)
    components.html(editor_html, height=height, scrolling=False)


def handle_editor_download(key_suffix: str = "editor") -> None:
    """Check for editor download data posted from the iframe and show a download button.

    Uses st.session_state to persist the download data across reruns.
    Call this in the main Streamlit loop after render_editor().

    Args:
        key_suffix: Unique suffix for the session_state key.
    """
    import streamlit as st
    state_key = f"editor_download_{key_suffix}"
    if state_key in st.session_state and st.session_state[state_key]:
        data = st.session_state[state_key]
        st.download_button(
            label=f"📥 下载 {data['fileName']}",
            data=base64.b64decode(data['fileBase64']),
            file_name=data['fileName'],
            mime="application/octet-stream",
            key=f"download_btn_{key_suffix}",
        )
        # Clear after showing
        st.session_state[state_key] = None
