from __future__ import annotations

import html


def render_markdown(markdown_text: str) -> str:
    lines = markdown_text.splitlines()
    parts: list[str] = []
    paragraph: list[str] = []
    list_items: list[str] = []
    code_block: list[str] = []
    in_code_block = False

    def flush_paragraph() -> None:
        if paragraph:
            text = " ".join(segment.strip() for segment in paragraph if segment.strip())
            if text:
                parts.append(f"<p>{_render_inline(text)}</p>")
            paragraph.clear()

    def flush_list() -> None:
        if list_items:
            items = "".join(f"<li>{_render_inline(item)}</li>" for item in list_items)
            parts.append(f"<ul>{items}</ul>")
            list_items.clear()

    def flush_code_block() -> None:
        if code_block:
            code = "\n".join(code_block)
            parts.append(f"<pre><code>{html.escape(code)}</code></pre>")
            code_block.clear()

    for line in lines:
        stripped = line.rstrip()

        if stripped.startswith("```"):
            flush_paragraph()
            flush_list()
            if in_code_block:
                flush_code_block()
                in_code_block = False
            else:
                in_code_block = True
            continue

        if in_code_block:
            code_block.append(line)
            continue

        if not stripped.strip():
            flush_paragraph()
            flush_list()
            continue

        if stripped.startswith("#"):
            flush_paragraph()
            flush_list()
            level = min(len(stripped) - len(stripped.lstrip("#")), 6)
            content = stripped[level:].strip()
            parts.append(f"<h{level}>{_render_inline(content)}</h{level}>")
            continue

        if stripped.lstrip().startswith(("- ", "* ")):
            flush_paragraph()
            item = stripped.lstrip()[2:].strip()
            list_items.append(item)
            continue

        paragraph.append(stripped)

    if in_code_block:
        flush_code_block()
    flush_paragraph()
    flush_list()

    return "\n".join(parts) if parts else "<p class=\"muted\">Documento vacío.</p>"


def _render_inline(text: str) -> str:
    escaped = html.escape(text)
    escaped = _replace_code_spans(escaped)
    return escaped


def _replace_code_spans(text: str) -> str:
    parts = text.split("`")
    if len(parts) == 1:
        return text

    rendered: list[str] = []
    for index, part in enumerate(parts):
        if index % 2 == 0:
            rendered.append(part)
        else:
            rendered.append(f"<code>{part}</code>")
    return "".join(rendered)
