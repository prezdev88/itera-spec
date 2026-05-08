from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from .discovery import IteraSpecDocument, discover_workspaces
from .markdown import render_markdown
from .reader import (
    DocumentNotFoundError,
    InvalidDocumentRequestError,
    read_workspace_document,
)
from .specialized_views import BACKLOG_SECTIONS, parse_backlog, parse_current_task
from .specialized_views import render_specialized_document


def create_app() -> FastAPI:
    app = FastAPI(title="IteraSpec GUI Viewer")
    app.mount("/static", StaticFiles(directory="static"), name="static")
    iteraspec_root = Path(".iteraspec")

    @app.get("/", response_class=HTMLResponse)
    async def home() -> str:
        workspaces = discover_workspaces(iteraspec_root)
        workspace_markup = _render_workspaces(workspaces)
        dashboard_markup = _render_dashboard(workspaces, iteraspec_root)
        return """<!doctype html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>IteraSpec GUI Viewer</title>
    <link rel="stylesheet" href="/static/styles.css">
  </head>
  <body>
    <main class="shell">
      <section class="hero-shell">
      <section class="hero">
        <p class="eyebrow">Desarrollado con IteraSpec</p>
        <h1>IteraSpec GUI Viewer</h1>
        <p class="lede">
          Un dashboard visual para recorrer especificaciones, backlog y contexto activo de
          <code>.iteraspec/</code> sin leer Markdown plano.
        </p>
        <div class="status-card">
          <span class="status-label">Fase activa</span>
          <strong>T8. Dashboard e identidad visual</strong>
        </div>
      </section>
      <aside class="brand-panel">
        <p class="section-kicker">Built With IteraSpec</p>
        <h2>Una capa visual read-only sobre el flujo IteraSpec.</h2>
        <p>
          Este GUI existe para hacer visible el estado del proyecto, no para modificarlo.
          La fuente de verdad sigue estando en los artefactos Markdown del protocolo.
        </p>
      </aside>
      </section>
      __DASHBOARD__
      <section class="inventory">
        <div class="inventory-heading">
          <p class="section-kicker">Inventario Detectado</p>
          <h2>Workspaces IteraSpec disponibles</h2>
        </div>
        <div class="workspace-grid">__WORKSPACES__</div>
      </section>
    </main>
  </body>
</html>""".replace("__WORKSPACES__", workspace_markup).replace("__DASHBOARD__", dashboard_markup)

    @app.get("/api/workspaces")
    async def workspaces() -> dict[str, object]:
        discovered = discover_workspaces(iteraspec_root)
        return {
            "workspace_count": len(discovered),
            "workspaces": [
                {
                    "name": workspace.name,
                    "relative_path": workspace.relative_path,
                    "documents": [
                        {
                            "name": document.name,
                            "relative_path": document.relative_path,
                            "kind": document.kind,
                        }
                        for document in workspace.documents
                    ],
                }
                for workspace in discovered
            ],
        }

    @app.get("/api/workspaces/{workspace_name}/documents/{document_name}")
    async def workspace_document(workspace_name: str, document_name: str) -> dict[str, object]:
        try:
            loaded = read_workspace_document(workspace_name, document_name, iteraspec_root)
        except InvalidDocumentRequestError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        except DocumentNotFoundError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

        return {
            "workspace_name": loaded.workspace_name,
            "document": {
                "name": loaded.document.name,
                "relative_path": loaded.document.relative_path,
                "kind": loaded.document.kind,
            },
            "content": loaded.content,
            "size_bytes": loaded.size_bytes,
        }

    @app.get("/workspaces/{workspace_name}/documents/{document_name}", response_class=HTMLResponse)
    async def workspace_document_page(workspace_name: str, document_name: str) -> str:
        workspaces = discover_workspaces(iteraspec_root)
        try:
            loaded = read_workspace_document(workspace_name, document_name, iteraspec_root)
        except InvalidDocumentRequestError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        except DocumentNotFoundError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

        return _render_document_page(workspaces, loaded.workspace_name, loaded.document.name, loaded.content)

    return app


def _render_workspaces(workspaces: list[object]) -> str:
    if not workspaces:
        return (
            "<div class=\"empty-state\">"
            "<strong>No se detectaron workspaces IteraSpec.</strong>"
            "<p>La aplicación seguirá funcionando aunque <code>.iteraspec/</code> esté vacío o incompleto.</p>"
            "</div>"
        )

    return "".join(
        (
            "<article class=\"workspace-card\">"
            f"<header><h2>{workspace.name}</h2><p>{workspace.relative_path}</p></header>"
            f"<ul>{_render_documents(workspace.name, workspace.documents)}</ul>"
            "</article>"
        )
        for workspace in workspaces
    )


def _render_documents(workspace_name: str, documents: list[IteraSpecDocument]) -> str:
    if not documents:
        return "<li class=\"doc-item muted\">Sin archivos Markdown detectados.</li>"

    return "".join(
        (
            "<li class=\"doc-item\">"
            f"<span class=\"doc-kind\">{document.kind}</span>"
            f"<a class=\"doc-link\" href=\"/workspaces/{workspace_name}/documents/{document.name}\">{document.name}</a>"
            "</li>"
        )
        for document in documents
    )


def _render_dashboard(workspaces: list[object], iteraspec_root: Path) -> str:
    workspace_count = len(workspaces)
    document_count = sum(len(workspace.documents) for workspace in workspaces)
    active_workspace = workspaces[0] if workspaces else None
    active_name = active_workspace.name if active_workspace else "Sin workspace"

    backlog_stats = _read_backlog_stats(active_name, iteraspec_root) if active_workspace else {}
    current_task = _read_current_task_snapshot(active_name, iteraspec_root) if active_workspace else None

    max_backlog_value = max(backlog_stats.values(), default=0)
    backlog_summary = "".join(
        _render_backlog_bar(key, label, backlog_stats.get(label, 0), max_backlog_value)
        for _, (key, label) in BACKLOG_SECTIONS.items()
    )

    quick_links = _render_quick_links(active_workspace)
    current_task_markup = (
        "<article class=\"dashboard-focus-card\">"
        "<p class=\"section-kicker\">Tarea Activa</p>"
        f"<h3>{current_task['title']}</h3>"
        f"<div class=\"task-pill\">{current_task['identifier']}</div>"
        f"<p>{current_task['objective']}</p>"
        f"<a class=\"primary-link\" href=\"/workspaces/{active_name}/documents/current_task.md\">Abrir tarea activa</a>"
        "</article>"
        if current_task
        else (
            "<article class=\"dashboard-focus-card\">"
            "<p class=\"section-kicker\">Tarea Activa</p>"
            "<h3>No hay una tarea activa detectable</h3>"
            "<p>Cuando exista `current_task.md`, aparecerá aquí con foco prioritario.</p>"
            "</article>"
        )
    )

    return f"""
      <section class="dashboard-grid">
        <article class="metric-card">
          <span class="metric-label">Workspaces</span>
          <strong>{workspace_count}</strong>
          <p>Features detectadas dentro de <code>.iteraspec/</code>.</p>
        </article>
        <article class="metric-card">
          <span class="metric-label">Documentos</span>
          <strong>{document_count}</strong>
          <p>Artefactos Markdown disponibles para visualización.</p>
        </article>
        <article class="metric-card">
          <span class="metric-label">Workspace Activo</span>
          <strong>{active_name}</strong>
          <p>Resumen operativo prioritario en la portada.</p>
        </article>
      </section>
      <section class="overview-grid">
        <article class="overview-card">
          <p class="section-kicker">Workspace Prioritario</p>
          <h2>{active_name}</h2>
          <p>Accesos rápidos a los artefactos más importantes del ciclo actual.</p>
          <div class="quick-links">{quick_links}</div>
        </article>
        <article class="overview-card">
          <p class="section-kicker">Estado del Backlog</p>
          <h2>Lectura ejecutiva</h2>
          <div class="mini-status-grid">{backlog_summary}</div>
          <a class="primary-link" href="/workspaces/{active_name}/documents/backlog.md">Abrir backlog</a>
        </article>
        {current_task_markup}
      </section>
    """


def _render_backlog_bar(key: str, label: str, value: int, max_value: int) -> str:
    width = 0 if max_value == 0 else max(8, round((value / max_value) * 100))
    return (
        "<div class=\"mini-status-row\">"
        "<div class=\"mini-status-topline\">"
        f"<span class=\"status-chip {key}\">{label}</span>"
        f"<strong>{value}</strong>"
        "</div>"
        "<div class=\"mini-status-bar-track\">"
        f"<span class=\"mini-status-bar-fill {key}\" style=\"width: {width}%\"></span>"
        "</div>"
        "</div>"
    )


def _render_quick_links(workspace: object | None) -> str:
    if workspace is None:
        return "<p class=\"muted\">No hay documentos detectados.</p>"
    priority = ["specs.md", "backlog.md", "current_task.md"]
    available = {document.name: document for document in workspace.documents}
    links = []
    for name in priority:
        if name in available:
            links.append(
                f"<a class=\"quick-link\" href=\"/workspaces/{workspace.name}/documents/{name}\">{name}</a>"
            )
    return "".join(links) if links else "<p class=\"muted\">Sin accesos prioritarios detectados.</p>"


def _read_backlog_stats(workspace_name: str, iteraspec_root: Path) -> dict[str, int]:
    try:
        loaded = read_workspace_document(workspace_name, "backlog.md", iteraspec_root)
    except (InvalidDocumentRequestError, DocumentNotFoundError):
        return {}
    parsed = parse_backlog(loaded.content)
    return {section.label: len(section.tasks) for section in parsed}


def _read_current_task_snapshot(workspace_name: str, iteraspec_root: Path) -> dict[str, str] | None:
    try:
        loaded = read_workspace_document(workspace_name, "current_task.md", iteraspec_root)
    except (InvalidDocumentRequestError, DocumentNotFoundError):
        return None
    parsed = parse_current_task(loaded.content)
    return {
        "title": parsed.title or "Tarea activa",
        "identifier": parsed.identifier or "Sin identificador",
        "objective": parsed.objective or "Sin objetivo detectado.",
    }


def _render_document_page(
    workspaces: list[object],
    current_workspace_name: str,
    current_document_name: str,
    content: str,
) -> str:
    navigation = _render_sidebar(workspaces, current_workspace_name, current_document_name)
    article = render_specialized_document(current_document_name, content) or render_markdown(content)
    return f"""<!doctype html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{current_document_name} · IteraSpec GUI Viewer</title>
    <link rel="stylesheet" href="/static/styles.css">
  </head>
  <body>
    <main class="reader-shell">
      <aside class="sidebar">
        <a class="home-link" href="/">IteraSpec GUI Viewer</a>
        <p class="sidebar-kicker">Documentos</p>
        {navigation}
      </aside>
      <section class="document-panel">
        <header class="document-header">
          <p class="eyebrow">Desarrollado con IteraSpec</p>
          <h1>{current_document_name}</h1>
          <p class="lede">Workspace activo: <code>{current_workspace_name}</code></p>
        </header>
        <article class="markdown-body">
          {article}
        </article>
      </section>
    </main>
  </body>
</html>"""


def _render_sidebar(
    workspaces: list[object],
    current_workspace_name: str,
    current_document_name: str,
) -> str:
    sections: list[str] = []
    for workspace in workspaces:
        items = []
        for document in workspace.documents:
            classes = ["sidebar-doc"]
            if workspace.name == current_workspace_name and document.name == current_document_name:
                classes.append("active")
            items.append(
                f"<li><a class=\"{' '.join(classes)}\" href=\"/workspaces/{workspace.name}/documents/{document.name}\">{document.name}</a></li>"
            )
        sections.append(
            "<section class=\"sidebar-workspace\">"
            f"<h2>{workspace.name}</h2>"
            f"<ul>{''.join(items) if items else '<li class=\"muted\">Sin documentos.</li>'}</ul>"
            "</section>"
        )
    return "".join(sections)
