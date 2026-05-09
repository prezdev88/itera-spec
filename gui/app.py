from __future__ import annotations

import html
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path

try:
    from fastapi import FastAPI, HTTPException
    from fastapi.responses import HTMLResponse, Response
    import uvicorn
except ModuleNotFoundError as exc:
    print(
        "Falta una dependencia para iniciar la GUI.\n"
        "Instala los requisitos con:\n"
        "  pip install -r requirements.txt",
        file=sys.stderr,
    )
    raise SystemExit(1) from exc


STYLESHEET = """
:root {
  color-scheme: light;
  --bg: #f4efe5;
  --panel: rgba(255, 251, 245, 0.72);
  --text: #1f1c17;
  --muted: #6b6258;
  --accent: #0f766e;
  --accent-strong: #115e59;
  --border: rgba(31, 28, 23, 0.1);
  --shadow: 0 24px 80px rgba(87, 64, 30, 0.16);
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  min-height: 100vh;
  font-family: Georgia, "Times New Roman", serif;
  color: var(--text);
  background:
    radial-gradient(circle at top left, rgba(15, 118, 110, 0.18), transparent 28%),
    radial-gradient(circle at bottom right, rgba(180, 83, 9, 0.16), transparent 30%),
    linear-gradient(135deg, #f8f4eb 0%, #efe4d1 100%);
}

.shell {
  width: min(960px, calc(100% - 32px));
  margin: 0 auto;
  padding: 48px 0 80px;
}

.hero-shell {
  display: grid;
  grid-template-columns: minmax(0, 1.8fr) minmax(280px, 1fr);
  gap: 18px;
}

.hero {
  padding: 48px;
  border: 1px solid var(--border);
  border-radius: 28px;
  background: var(--panel);
  backdrop-filter: blur(16px);
  box-shadow: var(--shadow);
}

.eyebrow {
  margin: 0 0 14px;
  color: var(--accent-strong);
  font-size: 0.82rem;
  font-weight: 700;
  letter-spacing: 0.16em;
  text-transform: uppercase;
}

h1 {
  margin: 0;
  font-size: clamp(2.6rem, 6vw, 5rem);
  line-height: 0.96;
}

.lede {
  max-width: 38rem;
  margin: 20px 0 0;
  color: var(--muted);
  font-size: 1.15rem;
  line-height: 1.7;
}

.status-card {
  display: inline-flex;
  flex-direction: column;
  gap: 6px;
  margin-top: 32px;
  padding: 18px 22px;
  border-radius: 18px;
  background: rgba(15, 118, 110, 0.1);
  border: 1px solid rgba(15, 118, 110, 0.18);
}

.status-label {
  color: var(--accent-strong);
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.14em;
  text-transform: uppercase;
}

.brand-panel {
  padding: 28px;
  border: 1px solid var(--border);
  border-radius: 28px;
  background:
    linear-gradient(160deg, rgba(15, 118, 110, 0.16), rgba(255, 255, 255, 0.55)),
    rgba(255, 251, 245, 0.72);
  box-shadow: var(--shadow);
}

.brand-panel h2 {
  margin: 8px 0 12px;
  font-size: clamp(1.6rem, 3vw, 2.2rem);
  line-height: 1.05;
}

.brand-panel p:last-child {
  margin: 0;
  color: var(--muted);
  line-height: 1.65;
}

.dashboard-grid,
.overview-grid {
  display: grid;
  gap: 18px;
  margin-top: 24px;
}

.dashboard-grid {
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
}

.overview-grid {
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
}

.metric-card,
.overview-card,
.dashboard-focus-card {
  padding: 22px;
  border: 1px solid var(--border);
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.58);
  box-shadow: var(--shadow);
}

.metric-label {
  display: inline-block;
  color: var(--accent-strong);
  font-size: 0.8rem;
  font-weight: 700;
  letter-spacing: 0.14em;
  text-transform: uppercase;
}

.metric-card strong {
  display: block;
  margin-top: 14px;
  font-size: clamp(2rem, 5vw, 3rem);
  line-height: 0.95;
}

.metric-card p,
.overview-card p,
.dashboard-focus-card p {
  color: var(--muted);
}

.overview-card h2,
.dashboard-focus-card h3 {
  margin: 8px 0 12px;
}

.quick-links,
.mini-status-grid {
  display: grid;
  gap: 10px;
  margin-top: 16px;
}

.quick-link,
.primary-link {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: fit-content;
  padding: 0.72rem 1rem;
  border-radius: 999px;
  text-decoration: none;
}

.quick-link {
  background: rgba(31, 28, 23, 0.06);
  color: var(--text);
}

.primary-link {
  margin-top: 16px;
  background: var(--accent);
  color: #f5fbfa;
}

.mini-status-row {
  display: grid;
  gap: 10px;
  padding: 10px 12px;
  border-radius: 14px;
  background: rgba(31, 28, 23, 0.04);
}

.mini-status-topline {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.mini-status-topline strong {
  font-size: 1rem;
}

.mini-status-bar-track {
  width: 100%;
  height: 10px;
  border-radius: 999px;
  background: rgba(31, 28, 23, 0.08);
  overflow: hidden;
}

.mini-status-bar-fill {
  display: block;
  height: 100%;
  border-radius: 999px;
  min-width: 0;
}

.mini-status-bar-fill.todo {
  background: linear-gradient(90deg, #f87171, #dc2626);
}

.mini-status-bar-fill.inprogress {
  background: linear-gradient(90deg, #facc15, #ca8a04);
}

.mini-status-bar-fill.done {
  background: linear-gradient(90deg, #4ade80, #16a34a);
}

.mini-status-bar-fill.blocked {
  background: linear-gradient(90deg, #6b7280, #1f2937);
}

.inventory {
  margin-top: 26px;
  padding: 26px 0 0;
}

.inventory-heading h2 {
  margin: 6px 0 0;
  font-size: clamp(1.8rem, 3vw, 2.4rem);
}

.section-kicker {
  margin: 0;
  color: var(--accent-strong);
  font-size: 0.8rem;
  font-weight: 700;
  letter-spacing: 0.14em;
  text-transform: uppercase;
}

.workspace-grid {
  display: grid;
  gap: 18px;
  margin-top: 20px;
}

.workspace-card,
.empty-state {
  padding: 22px;
  border: 1px solid var(--border);
  border-radius: 22px;
  background: rgba(255, 255, 255, 0.55);
}

.workspace-card header h2 {
  margin: 0;
  font-size: 1.3rem;
}

.workspace-card header p {
  margin: 8px 0 0;
  color: var(--muted);
}

.workspace-card ul {
  list-style: none;
  padding: 0;
  margin: 18px 0 0;
}

.doc-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 0;
  border-top: 1px solid rgba(31, 28, 23, 0.08);
}

.doc-item:first-child {
  border-top: 0;
  padding-top: 0;
}

.doc-kind {
  min-width: 86px;
  padding: 0.22rem 0.55rem;
  border-radius: 999px;
  background: rgba(15, 118, 110, 0.12);
  color: var(--accent-strong);
  font-size: 0.78rem;
  font-weight: 700;
  text-align: center;
  text-transform: uppercase;
}

.doc-name,
.doc-link,
.empty-state p,
.muted {
  color: var(--muted);
}

.doc-link {
  text-decoration: none;
}

.doc-link:hover {
  color: var(--text);
}

.empty-state strong {
  display: block;
  margin-bottom: 10px;
}

.reader-shell {
  display: grid;
  grid-template-columns: minmax(240px, 300px) minmax(0, 1fr);
  width: min(1280px, calc(100% - 32px));
  margin: 0 auto;
  padding: 28px 0 48px;
  gap: 22px;
  align-items: start;
}

.sidebar-toggle-input {
  position: absolute;
  opacity: 0;
  pointer-events: none;
}

.sidebar-toggle {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: fit-content;
  padding: 0.72rem 1rem;
  border-radius: 999px;
  border: 1px solid var(--border);
  background: rgba(255, 255, 255, 0.78);
  color: var(--text);
  cursor: pointer;
  font-weight: 700;
  box-shadow: var(--shadow);
}

.sidebar-toggle::before {
  content: "Ocultar menu";
}

.reader-shell:has(.sidebar-toggle-input:checked) {
  grid-template-columns: minmax(0, 1fr);
}

.reader-shell:has(.sidebar-toggle-input:checked) .sidebar {
  display: none;
}

.reader-shell:has(.sidebar-toggle-input:checked) .sidebar-toggle::before {
  content: "Mostrar menu";
}

.sidebar,
.document-panel {
  border: 1px solid var(--border);
  border-radius: 28px;
  background: var(--panel);
  backdrop-filter: blur(16px);
  box-shadow: var(--shadow);
}

.sidebar {
  padding: 24px 20px;
  align-self: start;
  position: sticky;
  top: 20px;
}

.home-link {
  color: var(--text);
  text-decoration: none;
  font-weight: 700;
}

.sidebar-kicker {
  margin: 18px 0 10px;
  color: var(--accent-strong);
  font-size: 0.8rem;
  font-weight: 700;
  letter-spacing: 0.14em;
  text-transform: uppercase;
}

.sidebar-workspace + .sidebar-workspace {
  margin-top: 18px;
  padding-top: 18px;
  border-top: 1px solid rgba(31, 28, 23, 0.08);
}

.sidebar-workspace h2 {
  margin: 0 0 10px;
  font-size: 1rem;
}

.sidebar-workspace ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.sidebar-doc {
  display: block;
  padding: 10px 12px;
  border-radius: 14px;
  color: var(--muted);
  text-decoration: none;
}

.sidebar-doc:hover,
.sidebar-doc.active {
  background: rgba(15, 118, 110, 0.1);
  color: var(--text);
}

.document-panel {
  padding: 36px 38px;
}

.document-toolbar {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 16px;
}

.document-header {
  padding-bottom: 20px;
  margin-bottom: 20px;
  border-bottom: 1px solid rgba(31, 28, 23, 0.08);
}

.markdown-body {
  font-size: 1.05rem;
  line-height: 1.75;
}

.markdown-body h1,
.markdown-body h2,
.markdown-body h3,
.markdown-body h4,
.markdown-body h5,
.markdown-body h6 {
  line-height: 1.15;
  margin: 1.6em 0 0.6em;
}

.markdown-body h1:first-child,
.markdown-body h2:first-child,
.markdown-body h3:first-child {
  margin-top: 0;
}

.markdown-body p,
.markdown-body ul,
.markdown-body pre {
  margin: 0 0 1rem;
}

.markdown-body ul {
  padding-left: 1.25rem;
}

.markdown-body li + li {
  margin-top: 0.35rem;
}

.markdown-body pre {
  overflow-x: auto;
  padding: 18px;
  border-radius: 18px;
  background: #1d2a2a;
  color: #eef6f4;
}

.specialized-view {
  display: grid;
  gap: 20px;
}

.status-summary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 14px;
}

.status-summary-card,
.focus-card,
.task-panel,
.empty-task-card {
  padding: 18px;
  border-radius: 20px;
  border: 1px solid var(--border);
  background: rgba(255, 255, 255, 0.62);
}

.task-card {
  padding: 0;
  border: 0;
  background: transparent;
  box-shadow: none;
}

.status-summary-card strong {
  display: block;
  margin-top: 14px;
  font-size: 2rem;
  line-height: 1;
}

.backlog-board {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 16px;
}

.backlog-column {
  display: grid;
  gap: 12px;
  align-content: start;
}

.status-chip {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: fit-content;
  gap: 8px;
  padding: 0.32rem 0.7rem;
  border-radius: 999px;
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.03em;
  background: rgba(31, 28, 23, 0.08);
}

.status-chip::before {
  content: "";
  width: 0.9rem;
  height: 0.9rem;
  border-radius: 999px;
  flex: 0 0 auto;
  background: rgba(31, 28, 23, 0.24);
  box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.32);
}

.status-chip.todo {
  background: rgba(220, 38, 38, 0.12);
  color: #991b1b;
}

.status-chip.todo::before {
  background: #dc2626;
}

.status-chip.inprogress {
  background: rgba(202, 138, 4, 0.16);
  color: #854d0e;
}

.status-chip.inprogress::before {
  background: #fbbf24;
}

.status-chip.done {
  background: rgba(22, 163, 74, 0.14);
  color: #166534;
}

.status-chip.done::before {
  background: #22c55e;
}

.status-chip.blocked {
  background: rgba(31, 41, 55, 0.12);
  color: #111827;
}

.status-chip.blocked::before {
  background: #4b5563;
}

.task-card h3,
.task-panel h3,
.focus-card h2 {
  margin: 0 0 12px;
}

.task-card-title-row {
  display: flex;
  align-items: center;
  gap: 10px;
}

.task-card-title-row h3 {
  margin: 0;
}

.task-state-dot {
  width: 10px;
  height: 10px;
  border-radius: 999px;
  flex: 0 0 auto;
  margin-top: -10px;
  background: rgba(31, 28, 23, 0.22);
}

.backlog-column:has(.status-chip.todo) .task-state-dot {
  background: #dc2626;
}

.backlog-column:has(.status-chip.inprogress) .task-state-dot {
  background: #ca8a04;
}

.backlog-column:has(.status-chip.done) .task-state-dot {
  background: #16a34a;
}

.backlog-column:has(.status-chip.blocked) .task-state-dot {
  background: #1f2937;
}

.task-card ul,
.task-panel ul {
  margin: 0;
  padding-left: 1.1rem;
}

.task-card-button {
  display: flex;
  width: 100%;
  padding: 16px 18px;
  border-radius: 20px;
  border: 1px solid var(--border);
  background: rgba(255, 255, 255, 0.62);
  color: var(--text);
  text-decoration: none;
  transition: transform 120ms ease, box-shadow 120ms ease, border-color 120ms ease;
}

.task-card-button:hover {
  transform: translateY(-1px);
  border-color: rgba(15, 118, 110, 0.28);
  box-shadow: 0 18px 40px rgba(87, 64, 30, 0.12);
}

.task-card-button:focus-visible,
.modal-close:focus-visible {
  outline: 2px solid rgba(15, 118, 110, 0.45);
  outline-offset: 3px;
}

.task-card-copy {
  display: grid;
  gap: 4px;
}

.task-card-title {
  margin: 0;
  font-size: 0.98rem;
  font-weight: 400;
  line-height: 1.4;
}

.task-code-chip {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: fit-content;
  padding: 0.22rem 0.56rem;
  border-radius: 999px;
  background: rgba(31, 28, 23, 0.08);
  color: var(--muted);
  font-size: 0.78rem;
  font-weight: 600;
  letter-spacing: 0.04em;
}

.task-card-copy p {
  margin: 0;
  color: var(--muted);
  font-size: 0.92rem;
}

.task-modal {
  position: fixed;
  inset: 0;
  display: none;
  align-items: center;
  justify-content: center;
  padding: 24px;
  background: rgba(17, 24, 39, 0.56);
  z-index: 20;
}

.task-modal:target {
  display: flex;
}

.task-modal-dialog {
  width: min(680px, 100%);
  max-height: min(80vh, 720px);
  overflow: auto;
  padding: 24px;
  border-radius: 28px;
  border: 1px solid rgba(255, 255, 255, 0.28);
  background: rgba(255, 251, 245, 0.98);
  box-shadow: 0 28px 100px rgba(17, 24, 39, 0.28);
}

.task-modal-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 18px;
}

.task-modal-header h3 {
  margin: 8px 0 0;
}

.task-modal-body {
  display: grid;
  gap: 16px;
}

.task-modal-panel {
  padding: 18px;
  border-radius: 20px;
  border: 1px solid var(--border);
  background: rgba(255, 255, 255, 0.72);
}

.task-modal-panel h4 {
  margin: 0 0 12px;
}

.task-modal-panel p,
.task-modal-panel ul {
  margin: 0;
}

.task-modal-panel ul {
  padding-left: 1.1rem;
}

.modal-close {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 44px;
  min-height: 44px;
  padding: 0.72rem 1rem;
  border-radius: 999px;
  background: rgba(31, 28, 23, 0.08);
  color: var(--text);
  text-decoration: none;
  font-weight: 700;
}

.current-task-view {
  gap: 18px;
}

.focus-card {
  padding: 24px;
}

.task-pill {
  display: inline-flex;
  margin: 8px 0 16px;
  padding: 0.35rem 0.7rem;
  border-radius: 999px;
  background: rgba(15, 118, 110, 0.12);
  color: var(--accent-strong);
  font-weight: 700;
}

.focus-objective {
  margin: 0;
  color: var(--muted);
  font-size: 1.05rem;
}

.task-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 16px;
}

code {
  padding: 0.16rem 0.42rem;
  border-radius: 999px;
  background: rgba(31, 28, 23, 0.08);
  font-size: 0.95em;
}

@media (max-width: 640px) {
  .shell {
    width: min(100% - 20px, 960px);
    padding-top: 24px;
  }

  .hero-shell {
    grid-template-columns: 1fr;
  }

  .reader-shell {
    grid-template-columns: 1fr;
    width: min(100% - 20px, 1280px);
    padding-top: 20px;
  }

  .document-toolbar {
    justify-content: flex-start;
  }

  .sidebar {
    position: static;
  }

  .hero {
    padding: 28px 22px;
    border-radius: 22px;
  }

  .document-panel {
    padding: 26px 22px;
  }

  .lede {
    font-size: 1rem;
  }
}
"""

KNOWN_DOCUMENTS = ("status.md", "specs.md", "backlog.md", "board.md", "current_task.md")
GLOBAL_WORKSPACE_NAME = "_global"
BACKLOG_SECTION_PATTERNS = (
    (re.compile(r"^##\s+`?🔴\s+To Do`?\s*$"), ("todo", "To Do")),
    (re.compile(r"^##\s+`?🟢\s+To Do`?\s*$"), ("todo", "To Do")),
    (re.compile(r"^##\s+`?🟡\s+In Progress`?\s*$"), ("inprogress", "In Progress")),
    (re.compile(r"^##\s+`?🔴\s+Done`?\s*$"), ("done", "Done")),
    (re.compile(r"^##\s+`?🟢\s+Done`?\s*$"), ("done", "Done")),
    (re.compile(r"^##\s+`?⚫\s+Blocked`?\s*$"), ("blocked", "Blocked")),
)
BACKLOG_SECTION_ORDER = (
    ("todo", "To Do"),
    ("inprogress", "In Progress"),
    ("done", "Done"),
    ("blocked", "Blocked"),
)


@dataclass(slots=True)
class IteraSpecDocument:
    name: str
    relative_path: str
    kind: str


@dataclass(slots=True)
class IteraSpecWorkspace:
    name: str
    relative_path: str
    documents: list[IteraSpecDocument]


@dataclass(slots=True)
class IteraSpecDocumentContent:
    workspace_name: str
    document: IteraSpecDocument
    content: str
    size_bytes: int


@dataclass(slots=True)
class BacklogTask:
    identifier: str
    title: str
    refinement_id: str
    bullets: list[str]
    detail_lines: list[str]


@dataclass(slots=True)
class BacklogSection:
    key: str
    label: str
    tasks: list[BacklogTask]


@dataclass(slots=True)
class BoardItem:
    identifier: str
    note: str


@dataclass(slots=True)
class BoardSection:
    key: str
    label: str
    items: list[BoardItem]


@dataclass(slots=True)
class CurrentTaskView:
    title: str
    identifier: str
    objective: str
    acceptance: list[str]
    notes: list[str]


class DocumentNotFoundError(Exception):
    pass


class InvalidDocumentRequestError(Exception):
    pass


def create_app() -> FastAPI:
    app = FastAPI(title="IteraSpec GUI Viewer")
    iteraspec_root = resolve_iteraspec_root()

    @app.get("/styles.css")
    async def stylesheet() -> Response:
        return Response(content=STYLESHEET, media_type="text/css")

    @app.get("/", response_class=HTMLResponse)
    async def home() -> str:
        workspaces = discover_workspaces(iteraspec_root)
        workspace_markup = _render_workspaces(workspaces)
        dashboard_markup = _render_dashboard(workspaces, iteraspec_root)
        status_title = "Visualizador read-only"
        return """<!doctype html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>IteraSpec GUI Viewer</title>
    <link rel="stylesheet" href="/styles.css">
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
          <span class="status-label">Modo</span>
          <strong>__STATUS__</strong>
        </div>
      </section>
      <aside class="brand-panel">
        <p class="section-kicker">Built With IteraSpec</p>
        <h2>Una capa visual autocontenida sobre el flujo IteraSpec.</h2>
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
</html>""".replace("__WORKSPACES__", workspace_markup).replace("__DASHBOARD__", dashboard_markup).replace("__STATUS__", status_title)

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

        return _render_document_page(
            workspaces,
            loaded.workspace_name,
            loaded.document.name,
            loaded.content,
            iteraspec_root,
        )

    return app


def main() -> None:
    port = int(os.environ.get("PORT", "8001"))
    uvicorn.run(create_app(), host="127.0.0.1", port=port)


def resolve_iteraspec_root() -> Path:
    configured = os.environ.get("ITERASPEC_ROOT")
    if configured:
        return Path(configured).expanduser().resolve()
    return Path(__file__).resolve().parent.parent.joinpath(".iteraspec")


def discover_workspaces(base_dir: Path | None = None) -> list[IteraSpecWorkspace]:
    root = (base_dir or Path(".iteraspec")).resolve()
    if not root.exists() or not root.is_dir():
        return []

    workspaces: list[IteraSpecWorkspace] = []
    global_workspace = _discover_global_workspace(root)
    if global_workspace is not None:
        workspaces.append(global_workspace)
    for candidate in sorted(root.iterdir(), key=lambda path: path.name):
        if not candidate.is_dir():
            continue
        workspaces.append(
            IteraSpecWorkspace(
                name=candidate.name,
                relative_path=candidate.relative_to(root.parent).as_posix(),
                documents=_discover_workspace_documents(candidate, root),
            )
        )
    return workspaces


def _discover_global_workspace(root_dir: Path) -> IteraSpecWorkspace | None:
    status_path = root_dir / "status.md"
    if not status_path.exists() or not status_path.is_file():
        return None

    return IteraSpecWorkspace(
        name=GLOBAL_WORKSPACE_NAME,
        relative_path=root_dir.relative_to(root_dir.parent).as_posix(),
        documents=[
            IteraSpecDocument(
                name="status.md",
                relative_path=status_path.relative_to(root_dir.parent).as_posix(),
                kind="status",
            )
        ],
    )


def _discover_workspace_documents(workspace_dir: Path, root_dir: Path) -> list[IteraSpecDocument]:
    documents: list[IteraSpecDocument] = []
    for markdown_file in sorted(workspace_dir.glob("*.md"), key=lambda path: path.name):
        documents.append(
            IteraSpecDocument(
                name=markdown_file.name,
                relative_path=markdown_file.relative_to(root_dir.parent).as_posix(),
                kind=_document_kind(markdown_file.name),
            )
        )
    return documents


def _document_kind(filename: str) -> str:
    if filename in KNOWN_DOCUMENTS:
        return filename.removesuffix(".md")
    return "markdown"


def read_workspace_document(
    workspace_name: str,
    document_name: str,
    base_dir: Path | None = None,
) -> IteraSpecDocumentContent:
    _validate_name(workspace_name, "workspace")
    _validate_name(document_name, "document")

    root = (base_dir or Path(".iteraspec")).resolve()
    workspaces = discover_workspaces(root)
    workspace = next((item for item in workspaces if item.name == workspace_name), None)
    if workspace is None:
        raise DocumentNotFoundError(f"No existe el workspace '{workspace_name}'.")

    document = next((item for item in workspace.documents if item.name == document_name), None)
    if document is None:
        raise DocumentNotFoundError(
            f"No existe el documento '{document_name}' dentro de '{workspace_name}'."
        )

    document_path = (root.parent / document.relative_path).resolve()
    _ensure_within_root(document_path, root)

    try:
        content = document_path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise DocumentNotFoundError(
            f"El documento '{document_name}' no está disponible actualmente."
        ) from exc

    return IteraSpecDocumentContent(
        workspace_name=workspace_name,
        document=document,
        content=content,
        size_bytes=len(content.encode("utf-8")),
    )


def _validate_name(value: str, label: str) -> None:
    if not value or "/" in value or "\\" in value or value in {".", ".."}:
        raise InvalidDocumentRequestError(f"El nombre de {label} solicitado no es válido.")


def _ensure_within_root(candidate: Path, root: Path) -> None:
    try:
        candidate.relative_to(root.resolve())
    except ValueError as exc:
        raise InvalidDocumentRequestError(
            "La ruta solicitada queda fuera de .iteraspec/."
        ) from exc


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
    return _replace_code_spans(escaped)


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


def render_specialized_document(
    document_name: str,
    content: str,
    workspace_name: str,
    iteraspec_root: Path,
) -> str | None:
    if document_name == "status.md":
        return render_status_view(content)
    if document_name == "board.md":
        return render_board_view(content, workspace_name, iteraspec_root)
    if document_name == "backlog.md":
        return render_backlog_view(content)
    if document_name == "current_task.md":
        return render_current_task_view(content)
    return None


def render_status_view(content: str) -> str:
    key_values = parse_status_key_values(content)
    if not key_values:
        return (
            "<div class=\"specialized-view\">"
            "<section class=\"focus-card\">"
            "<p class=\"section-kicker\">Estado Global</p>"
            "<h2>status.md</h2>"
            "<p>No se detectó una estructura resumible. Se muestra como Markdown estándar.</p>"
            "</section>"
            f"{render_markdown(content)}"
            "</div>"
        )

    cards = "".join(
        (
            "<article class=\"status-summary-card\">"
            f"<span>{html.escape(label)}</span>"
            f"<strong>{html.escape(value)}</strong>"
            "</article>"
        )
        for label, value in key_values[:8]
    )
    return (
        "<div class=\"specialized-view\">"
        "<section class=\"focus-card\">"
        "<p class=\"section-kicker\">Estado Global</p>"
        "<h2>Resumen de reanudación</h2>"
        "<p>Checkpoint persistido en <code>.iteraspec/status.md</code>.</p>"
        "</section>"
        f"<section class=\"status-summary-grid\">{cards}</section>"
        "</div>"
    )


def render_backlog_view(content: str) -> str:
    tasks = parse_task_catalog(content)
    tasks_by_id = {task.identifier: task for task in tasks if task.identifier}
    refinement_index = build_refinement_index(tasks_by_id)
    summary = (
        "<article class=\"status-summary-card\">"
        "<span>Catalogo</span>"
        f"<strong>{len(tasks)}</strong>"
        "<span>tareas definidas</span>"
        "</article>"
    )
    board = (
        "<section class=\"backlog-column\">"
        "<header><span class=\"status-chip done\">Task Catalog</span></header>"
        f"{render_backlog_tasks(tasks, 'catalog', refinement_index, tasks_by_id)}"
        "</section>"
    )
    return (
        "<div class=\"specialized-view\">"
        "<section class=\"status-summary-grid\">"
        f"{summary}"
        "</section>"
        "<section class=\"backlog-board\">"
        f"{board}"
        "</section>"
        "</div>"
    )


def render_board_view(content: str, workspace_name: str, iteraspec_root: Path) -> str:
    sections = parse_board(content)
    tasks_by_id = read_task_catalog(workspace_name, iteraspec_root)
    refinement_index = build_refinement_index(tasks_by_id)
    if not sections:
        legacy = parse_legacy_backlog_board(content)
        if legacy:
            sections = legacy
    sections = order_board_sections(sections)
    summary = "".join(
        (
            "<article class=\"status-summary-card\">"
            f"<span class=\"status-chip {section.key}\">{section.label}</span>"
            f"<strong>{len(section.items)}</strong>"
            "<span>tareas</span>"
            "</article>"
        )
        for section in sections
    )
    board = "".join(
        (
            "<section class=\"backlog-column\">"
            f"<header><span class=\"status-chip {section.key}\">{section.label}</span></header>"
            f"{render_board_items(section.items, section.key, tasks_by_id, refinement_index)}"
            "</section>"
        )
        for section in sections
    )
    return (
        "<div class=\"specialized-view\">"
        "<section class=\"status-summary-grid\">"
        f"{summary}"
        "</section>"
        "<section class=\"backlog-board\">"
        f"{board}"
        "</section>"
        "</div>"
    )


def render_current_task_view(content: str) -> str:
    task = parse_current_task(content)
    acceptance = "".join(f"<li>{html.escape(item)}</li>" for item in task.acceptance) or "<li>Sin criterios detectados.</li>"
    notes = "".join(f"<li>{html.escape(item)}</li>" for item in task.notes) or "<li>Sin notas detectadas.</li>"
    objective = html.escape(task.objective or "Objetivo no detectado.")
    identifier = html.escape(task.identifier or "Sin identificador")
    title = html.escape(task.title or "Tarea activa")
    return (
        "<div class=\"specialized-view current-task-view\">"
        "<section class=\"focus-card\">"
        "<p class=\"section-kicker\">Tarea Activa</p>"
        f"<h2>{title}</h2>"
        f"<div class=\"task-pill\">{identifier}</div>"
        f"<p class=\"focus-objective\">{objective}</p>"
        "</section>"
        "<section class=\"task-grid\">"
        "<article class=\"task-panel\">"
        "<h3>Criterios de aceptación</h3>"
        f"<ul>{acceptance}</ul>"
        "</article>"
        "<article class=\"task-panel\">"
        "<h3>Notas de implementación</h3>"
        f"<ul>{notes}</ul>"
        "</article>"
        "</section>"
        "</div>"
    )


def parse_task_catalog(content: str) -> list[BacklogTask]:
    tasks: list[BacklogTask] = []
    current_task: BacklogTask | None = None
    global_refinement_id = extract_global_refinement_id(content)

    for raw_line in content.splitlines():
        line = raw_line.rstrip()

        if line.startswith("### "):
            identifier, _ = split_task_title(line[4:].strip())
            current_task = BacklogTask(
                identifier=identifier,
                title=line[4:].strip(),
                refinement_id="",
                bullets=[],
                detail_lines=[],
            )
            tasks.append(current_task)
            continue

        if current_task is None:
            continue

        if line.startswith("## "):
            current_task = None
            continue

        stripped = line.strip()
        if not stripped:
            continue

        current_task.detail_lines.append(stripped)
        if stripped.startswith("- "):
            current_task.bullets.append(stripped[2:].strip())

    for task in tasks:
        task.refinement_id = extract_refinement_id(task.detail_lines)
        if not task.refinement_id and global_refinement_id:
            task.refinement_id = global_refinement_id

    if tasks:
        return tasks

    return parse_task_catalog_table(content, global_refinement_id)


def parse_task_catalog_table(content: str, global_refinement_id: str) -> list[BacklogTask]:
    tasks: list[BacklogTask] = []
    for raw_line in content.splitlines():
        line = raw_line.strip()
        if not line.startswith("|") or line.count("|") < 6:
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) < 5:
            continue
        if cells[0].lower() == "id" or set("".join(cells)) <= {":", "-", " "}:
            continue
        identifier = normalize_task_identifier(cells[0])
        if not identifier:
            continue
        title = cells[1] or identifier
        detail_lines = []
        refinement_id = global_refinement_id
        if refinement_id:
            detail_lines.append(f"- Refinement: {refinement_id}")
        if cells[2]:
            detail_lines.append(f"- Description: {cells[2]}")
        if cells[3]:
            detail_lines.append(f"- Acceptance Criteria: {cells[3]}")
        if len(cells) > 4 and cells[4]:
            detail_lines.append(f"- Dependencies: {cells[4]}")
        tasks.append(
            BacklogTask(
                identifier=identifier,
                title=f"{identifier} - {title}",
                refinement_id=refinement_id,
                bullets=[line[2:].strip() for line in detail_lines if line.startswith("- ")],
                detail_lines=detail_lines,
            )
        )
    return tasks


def parse_board(content: str) -> list[BoardSection]:
    sections: list[BoardSection] = []
    current_key = None
    current_label = None
    current_items: list[BoardItem] = []

    for raw_line in content.splitlines():
        line = raw_line.rstrip()
        section = _match_backlog_section(line)
        if section is not None:
            if current_key is not None:
                sections.append(BoardSection(current_key, current_label or current_key, current_items))
            current_key, current_label = section
            current_items = []
            continue

        if current_key is None:
            continue

        item = _parse_board_item(line)
        if item is not None:
            current_items.append(item)

    if current_key is not None:
        sections.append(BoardSection(current_key, current_label or current_key, current_items))

    return sections


def parse_legacy_backlog_board(content: str) -> list[BoardSection]:
    sections: list[BoardSection] = []
    current_key = None
    current_label = None
    current_items: list[BoardItem] = []

    for raw_line in content.splitlines():
        line = raw_line.rstrip()
        section = _match_backlog_section(line)
        if section is not None:
            if current_key is not None:
                sections.append(BoardSection(current_key, current_label or current_key, current_items))
            current_key, current_label = section
            current_items = []
            continue

        if current_key is None:
            continue

        if line.startswith("### "):
            identifier, _ = split_task_title(line[4:].strip())
            if identifier:
                current_items.append(BoardItem(identifier=identifier, note=""))

    if current_key is not None:
        sections.append(BoardSection(current_key, current_label or current_key, current_items))

    return sections


def _match_backlog_section(line: str) -> tuple[str, str] | None:
    for pattern, section in BACKLOG_SECTION_PATTERNS:
        if pattern.match(line):
            return section
    return None


def _parse_board_item(line: str) -> BoardItem | None:
    stripped = line.strip()
    if not stripped.startswith("- "):
        return None
    body = stripped[2:].strip()
    match = re.match(r"^`?(T\d{2}|R\d{2})`?(?:\s*[:\-]\s*(.*))?$", body)
    if not match:
        return None
    return BoardItem(identifier=match.group(1), note=(match.group(2) or "").strip())


def order_board_sections(sections: list[BoardSection]) -> list[BoardSection]:
    by_key = {section.key: section for section in sections}
    ordered: list[BoardSection] = []
    for key, label in BACKLOG_SECTION_ORDER:
        ordered.append(by_key.get(key, BoardSection(key=key, label=label, items=[])))
    return ordered


def parse_current_task(content: str) -> CurrentTaskView:
    title = first_heading(content) or "Tarea activa"
    identifier = first_value_after_heading(content, "Identificador")
    objective = (
        collect_section_paragraph(content, "Objetivo")
        or collect_section_paragraph(content, "Descripcion")
        or collect_section_paragraph(content, "Descripción")
        or collect_section_paragraph(content, "Nombre")
    )
    acceptance = collect_section_bullets(content, "Criterios de aceptacion") or collect_section_bullets(
        content, "Criterios de aceptación"
    )
    notes = collect_section_bullets(content, "Notas de implementacion") or collect_section_bullets(
        content, "Notas de implementación"
    )
    return CurrentTaskView(
        title=title,
        identifier=identifier,
        objective=objective,
        acceptance=acceptance,
        notes=notes,
    )


def parse_status_key_values(content: str) -> list[tuple[str, str]]:
    parsed: list[tuple[str, str]] = []
    for raw_line in content.splitlines():
        line = raw_line.strip()
        if line.startswith("- "):
            line = line[2:].strip()
        match = re.match(r"^([^:]+):\s*(.+)$", line)
        if not match:
            continue
        key = match.group(1).strip().strip("`")
        value = match.group(2).strip().strip("`")
        if key and value:
            parsed.append((key, value))
    return parsed


def split_task_title(title: str) -> tuple[str, str]:
    cleaned = title.strip()
    match = re.match(r"^`?(T\d{2}|R\d{2})`?\s*[:\-]?\s*(.*)$", cleaned)
    if match:
        identifier = match.group(1).strip()
        summary = match.group(2).strip() or identifier
        return identifier, summary
    return "", cleaned


def extract_refinement_id(detail_lines: list[str]) -> str:
    for line in detail_lines:
        cleaned = line.strip()
        if cleaned.startswith("- "):
            cleaned = cleaned[2:].strip()
        match = re.match(
            r"^(Refinement|Refinamiento)\s*:\s*`?(R\d{2})`?\s*$",
            cleaned,
            re.IGNORECASE,
        )
        if match:
            return match.group(2).upper()
    return ""


def extract_global_refinement_id(content: str) -> str:
    normalized = content.replace("*", "")
    match = re.search(
        r"(?:Refinement Group|Grupo de refinamiento|Refinamiento)\s*:?\s*`?(R\d{2})`?",
        normalized,
        re.IGNORECASE,
    )
    return match.group(1).upper() if match else ""


def normalize_task_identifier(value: str) -> str:
    match = re.search(r"\b(T\d{2})\b", value.strip(), re.IGNORECASE)
    return match.group(1).upper() if match else ""


def build_refinement_index(tasks: dict[str, BacklogTask]) -> dict[str, list[str]]:
    refinement_index: dict[str, list[str]] = {}
    for identifier, task in tasks.items():
        if not task.refinement_id:
            continue
        refinement_index.setdefault(task.refinement_id, []).append(identifier)
    return refinement_index


def read_task_catalog(workspace_name: str, iteraspec_root: Path) -> dict[str, BacklogTask]:
    if not workspace_name or workspace_name == GLOBAL_WORKSPACE_NAME:
        return {}
    try:
        loaded = read_workspace_document(workspace_name, "backlog.md", iteraspec_root)
    except (InvalidDocumentRequestError, DocumentNotFoundError):
        return {}
    catalog = parse_task_catalog(loaded.content)
    mapped: dict[str, BacklogTask] = {}
    for task in catalog:
        identifier, _ = split_task_title(task.title)
        if identifier:
            mapped[identifier] = task
    return mapped


def render_backlog_tasks(
    tasks: list[BacklogTask],
    section_key: str,
    refinement_index: dict[str, list[str]],
    tasks_by_id: dict[str, BacklogTask],
) -> str:
    if not tasks:
        return "<div class=\"empty-task-card\">Sin tareas en esta columna.</div>"
    rendered: list[str] = []
    for index, task in enumerate(tasks, start=1):
        modal_id = task_modal_id(task.identifier or f"{section_key}-{index}")
        identifier, summary = split_task_title(task.title)
        code_markup = (
            f"<span class=\"task-code-chip\">{html.escape(identifier)}</span>"
            if identifier
            else ""
        )
        rendered.append(
            "<article class=\"task-card\">"
            f"<a class=\"task-card-button\" href=\"#{modal_id}\">"
            "<div class=\"task-card-title-row\">"
            "<span class=\"task-state-dot\"></span>"
            "<div class=\"task-card-copy\">"
            f"{code_markup}"
            f"<div class=\"task-card-title\">{html.escape(summary)}</div>"
            "<p>Ver detalle</p>"
            "</div>"
            "</div>"
            "</a>"
            f"{render_task_modal(modal_id, task, None, refinement_index, tasks_by_id)}"
            "</article>"
        )
    return "".join(rendered)


def render_board_items(
    items: list[BoardItem],
    section_key: str,
    tasks_by_id: dict[str, BacklogTask],
    refinement_index: dict[str, list[str]],
) -> str:
    if not items:
        return "<div class=\"empty-task-card\">Sin tareas en esta columna.</div>"
    rendered: list[str] = []
    for index, item in enumerate(items, start=1):
        modal_id = task_modal_id(item.identifier or f"{section_key}-{index}")
        task = tasks_by_id.get(item.identifier)
        summary = split_task_title(task.title)[1] if task else item.identifier
        note_markup = f"<p>{html.escape(item.note)}</p>" if item.note else "<p>Ver detalle</p>"
        rendered.append(
            "<article class=\"task-card\">"
            f"<a class=\"task-card-button\" href=\"#{modal_id}\">"
            "<div class=\"task-card-title-row\">"
            "<span class=\"task-state-dot\"></span>"
            "<div class=\"task-card-copy\">"
            f"<span class=\"task-code-chip\">{html.escape(item.identifier)}</span>"
            f"<div class=\"task-card-title\">{html.escape(summary)}</div>"
            f"{note_markup}"
            "</div>"
            "</div>"
            "</a>"
            f"{render_task_modal(modal_id, task, item, refinement_index, tasks_by_id)}"
            "</article>"
        )
    return "".join(rendered)


def render_task_modal(
    modal_id: str,
    task: BacklogTask | None,
    board_item: BoardItem | None = None,
    refinement_index: dict[str, list[str]] | None = None,
    tasks_by_id: dict[str, BacklogTask] | None = None,
) -> str:
    if task is not None:
        identifier, summary = split_task_title(task.title)
        detail_markup = render_task_detail(task)
    else:
        identifier = board_item.identifier if board_item is not None else ""
        summary = board_item.identifier if board_item is not None else "Tarea"
        detail_markup = "<p>No se encontró detalle en <code>backlog.md</code> para esta tarea.</p>"
    refinement_panel = render_refinement_panel(
        identifier,
        task.refinement_id if task is not None else "",
        refinement_index or {},
        tasks_by_id or {},
    )
    note_panel = ""
    if board_item is not None and board_item.note:
        note_panel = (
            "<article class=\"task-modal-panel\">"
            "<h4>Nota de estado</h4>"
            f"<p>{html.escape(board_item.note)}</p>"
            "</article>"
        )
    return (
        f"<section id=\"{modal_id}\" class=\"task-modal\">"
        "<div class=\"task-modal-dialog\">"
        "<header class=\"task-modal-header\">"
        "<div>"
        "<p class=\"section-kicker\">Detalle de tarea</p>"
        f"{f'<span class=\"task-code-chip\">{html.escape(identifier)}</span>' if identifier else ''}"
        f"<h3>{html.escape(summary)}</h3>"
        "</div>"
        "<a class=\"modal-close\" href=\"#\">Cerrar</a>"
        "</header>"
        "<div class=\"task-modal-body\">"
        "<article class=\"task-modal-panel\">"
        "<h4>Detalle</h4>"
        f"{detail_markup}"
        "</article>"
        f"{refinement_panel}"
        f"{note_panel}"
        "</div>"
        "</div>"
        "</section>"
    )


def render_task_detail(task: BacklogTask) -> str:
    if task.detail_lines:
        return render_markdown("\n".join(task.detail_lines))
    return "<p>Esta tarea no tiene detalle adicional en el backlog.</p>"


def render_refinement_panel(
    task_identifier: str,
    refinement_id: str,
    refinement_index: dict[str, list[str]],
    tasks_by_id: dict[str, BacklogTask],
) -> str:
    if not refinement_id:
        return ""
    sibling_ids = [identifier for identifier in refinement_index.get(refinement_id, []) if identifier != task_identifier]
    related_links = "".join(
        (
            f"<li><a class=\"doc-link\" href=\"#{task_modal_id(identifier)}\">"
            f"{html.escape(identifier)} - {html.escape(split_task_title(tasks_by_id[identifier].title)[1])}"
            "</a></li>"
        )
        for identifier in sibling_ids
        if identifier in tasks_by_id
    )
    related_markup = (
        f"<ul>{related_links}</ul>"
        if related_links
        else "<p>No hay otras tareas asociadas a este refinamiento.</p>"
    )
    return (
        "<article class=\"task-modal-panel\">"
        "<h4>Refinamiento</h4>"
        f"<p><span class=\"task-code-chip\">{html.escape(refinement_id)}</span></p>"
        "<h4>Tareas relacionadas</h4>"
        f"{related_markup}"
        "</article>"
    )


def task_modal_id(identifier: str) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9_-]+", "-", identifier.strip()) or "task"
    return f"task-detail-{normalized}"


def render_task_bullets(bullets: list[str]) -> str:
    if not bullets:
        return "<p class=\"muted\">Sin detalle adicional.</p>"
    items = "".join(f"<li>{html.escape(item)}</li>" for item in bullets[:4])
    return f"<ul>{items}</ul>"


def first_heading(content: str) -> str | None:
    match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    return match.group(1).strip() if match else None


def first_value_after_heading(content: str, heading: str) -> str:
    section = section_body(content, heading)
    match = re.search(r"^- `?(.+?)`?$", section, re.MULTILINE)
    if match:
        return match.group(1).strip()
    match = re.search(r"^`?(.+?)`?$", section, re.MULTILINE)
    return match.group(1).strip() if match else ""


def collect_section_paragraph(content: str, heading: str) -> str:
    section = section_body(content, heading)
    for line in section.splitlines():
        if line.strip() and not line.startswith("- ") and not line.startswith("`"):
            return line.strip()
        if line.strip().startswith("`") and line.strip().endswith("`"):
            return line.strip().strip("`").strip()
    return ""


def collect_section_bullets(content: str, heading: str) -> list[str]:
    section = section_body(content, heading)
    return [line[2:].strip() for line in section.splitlines() if line.startswith("- ")]


def section_body(content: str, heading: str) -> str:
    pattern = rf"^##\s+{re.escape(heading)}\s*$\n(.*?)(?:\n##\s+|\Z)"
    match = re.search(pattern, content, re.DOTALL)
    if not match:
        normalized_heading = _normalize_heading(heading)
        current_heading = None
        lines: list[str] = []
        collecting = False
        for raw_line in content.splitlines():
            line = raw_line.rstrip()
            if line.startswith("## "):
                heading_text = _normalize_heading(line[3:])
                if collecting:
                    break
                if heading_text == normalized_heading:
                    collecting = True
                current_heading = heading_text
                continue
            if collecting and current_heading == normalized_heading:
                lines.append(raw_line)
        if lines:
            return "\n".join(lines).strip()
    return match.group(1).strip() if match else ""


def _normalize_heading(value: str) -> str:
    normalized = value.strip().strip("`").lower()
    replacements = str.maketrans(
        {
            "á": "a",
            "é": "e",
            "í": "i",
            "ó": "o",
            "ú": "u",
            "ü": "u",
            "ñ": "n",
        }
    )
    return normalized.translate(replacements)


def _render_workspaces(workspaces: list[IteraSpecWorkspace]) -> str:
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
            f"<header><h2>{html.escape(_workspace_label(workspace.name))}</h2><p>{html.escape(workspace.relative_path)}</p></header>"
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
            f"<span class=\"doc-kind\">{html.escape(document.kind)}</span>"
            f"<a class=\"doc-link\" href=\"/workspaces/{workspace_name}/documents/{document.name}\">{html.escape(document.name)}</a>"
            "</li>"
        )
        for document in documents
    )


def _render_dashboard(workspaces: list[IteraSpecWorkspace], iteraspec_root: Path) -> str:
    workspace_count = len(workspaces)
    document_count = sum(len(workspace.documents) for workspace in workspaces)
    global_workspace = next((workspace for workspace in workspaces if workspace.name == GLOBAL_WORKSPACE_NAME), None)
    active_workspace = next((workspace for workspace in workspaces if workspace.name != GLOBAL_WORKSPACE_NAME), None)
    active_name = active_workspace.name if active_workspace else "Sin workspace"
    active_label = _workspace_label(active_name)

    backlog_stats = _read_board_stats(active_name, iteraspec_root) if active_workspace else {}
    current_task = _read_current_task_snapshot(active_name, iteraspec_root) if active_workspace else None

    max_backlog_value = max(backlog_stats.values(), default=0)
    backlog_summary = "".join(
        _render_backlog_bar(key, label, backlog_stats.get(label, 0), max_backlog_value)
        for key, label in BACKLOG_SECTION_ORDER
    )

    quick_links = _render_quick_links(active_workspace)
    if global_workspace is not None:
        quick_links = (
            f"<a class=\"quick-link\" href=\"/workspaces/{GLOBAL_WORKSPACE_NAME}/documents/status.md\">status.md</a>"
            + quick_links
        )
    board_doc_name = _preferred_board_document(active_workspace)
    board_doc_label = "board" if board_doc_name == "board.md" else "backlog"
    escaped_active_name = html.escape(active_label)
    current_task_markup = (
        "<article class=\"dashboard-focus-card\">"
        "<p class=\"section-kicker\">Tarea Activa</p>"
        f"<h3>{html.escape(current_task['title'])}</h3>"
        f"<div class=\"task-pill\">{html.escape(current_task['identifier'])}</div>"
        f"<p>{html.escape(current_task['objective'])}</p>"
        f"<a class=\"primary-link\" href=\"/workspaces/{active_name}/documents/current_task.md\">Abrir tarea activa</a>"
        "</article>"
        if current_task
        else (
            "<article class=\"dashboard-focus-card\">"
            "<p class=\"section-kicker\">Tarea Activa</p>"
            "<h3>No hay una tarea activa detectable</h3>"
            "<p>Cuando exista <code>current_task.md</code>, aparecerá aquí con foco prioritario.</p>"
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
          <strong>{escaped_active_name}</strong>
          <p>Resumen operativo prioritario en la portada.</p>
        </article>
      </section>
      <section class="overview-grid">
        <article class="overview-card">
          <p class="section-kicker">Workspace Prioritario</p>
          <h2>{escaped_active_name}</h2>
          <p>Accesos rápidos a los artefactos más importantes del ciclo actual.</p>
          <div class="quick-links">{quick_links}</div>
        </article>
        <article class="overview-card">
          <p class="section-kicker">Estado del Backlog</p>
          <h2>Lectura ejecutiva</h2>
          <div class="mini-status-grid">{backlog_summary}</div>
          <a class="primary-link" href="/workspaces/{active_name}/documents/{board_doc_name}">Abrir {board_doc_label}</a>
        </article>
        {current_task_markup}
      </section>
    """


def _render_backlog_bar(key: str, label: str, value: int, max_value: int) -> str:
    width = 0 if max_value == 0 else max(8, round((value / max_value) * 100))
    return (
        "<div class=\"mini-status-row\">"
        "<div class=\"mini-status-topline\">"
        f"<span class=\"status-chip {key}\">{html.escape(label)}</span>"
        f"<strong>{value}</strong>"
        "</div>"
        "<div class=\"mini-status-bar-track\">"
        f"<span class=\"mini-status-bar-fill {key}\" style=\"width: {width}%\"></span>"
        "</div>"
        "</div>"
    )


def _render_quick_links(workspace: IteraSpecWorkspace | None) -> str:
    if workspace is None:
        return "<p class=\"muted\">No hay documentos detectados.</p>"
    priority = ["specs.md", "board.md", "backlog.md", "current_task.md"]
    available = {document.name: document for document in workspace.documents}
    links = []
    for name in priority:
        if name in available:
            links.append(
                f"<a class=\"quick-link\" href=\"/workspaces/{workspace.name}/documents/{name}\">{html.escape(name)}</a>"
            )
    return "".join(links) if links else "<p class=\"muted\">Sin accesos prioritarios detectados.</p>"


def _preferred_board_document(workspace: IteraSpecWorkspace | None) -> str:
    if workspace is None:
        return "board.md"
    available = {document.name for document in workspace.documents}
    return "board.md" if "board.md" in available else "backlog.md"


def _read_board_stats(workspace_name: str, iteraspec_root: Path) -> dict[str, int]:
    try:
        loaded = read_workspace_document(workspace_name, "board.md", iteraspec_root)
    except (InvalidDocumentRequestError, DocumentNotFoundError):
        return _read_legacy_backlog_stats(workspace_name, iteraspec_root)
    parsed = parse_board(loaded.content)
    return {section.label: len(section.items) for section in parsed}


def _read_legacy_backlog_stats(workspace_name: str, iteraspec_root: Path) -> dict[str, int]:
    try:
        loaded = read_workspace_document(workspace_name, "backlog.md", iteraspec_root)
    except (InvalidDocumentRequestError, DocumentNotFoundError):
        return {}
    parsed = parse_legacy_backlog_board(loaded.content)
    return {section.label: len(section.items) for section in parsed}


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
    workspaces: list[IteraSpecWorkspace],
    current_workspace_name: str,
    current_document_name: str,
    content: str,
    iteraspec_root: Path,
) -> str:
    navigation = _render_sidebar(workspaces, current_workspace_name, current_document_name)
    article = (
        render_specialized_document(
            current_document_name,
            content,
            current_workspace_name,
            iteraspec_root,
        )
        or render_markdown(content)
    )
    return f"""<!doctype html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{html.escape(current_document_name)} · IteraSpec GUI Viewer</title>
    <link rel="stylesheet" href="/styles.css">
  </head>
  <body>
    <main class="reader-shell">
      <input id="sidebar-toggle" class="sidebar-toggle-input" type="checkbox">
      <aside class="sidebar">
        <a class="home-link" href="/">IteraSpec GUI Viewer</a>
        <p class="sidebar-kicker">Documentos</p>
        {navigation}
      </aside>
      <section class="document-panel">
        <div class="document-toolbar">
          <label class="sidebar-toggle" for="sidebar-toggle"></label>
        </div>
        <header class="document-header">
          <p class="eyebrow">Desarrollado con IteraSpec</p>
          <h1>{html.escape(current_document_name)}</h1>
          <p class="lede">Workspace activo: <code>{html.escape(_workspace_label(current_workspace_name))}</code></p>
        </header>
        <article class="markdown-body">
          {article}
        </article>
      </section>
    </main>
  </body>
</html>"""


def _render_sidebar(
    workspaces: list[IteraSpecWorkspace],
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
                f"<li><a class=\"{' '.join(classes)}\" href=\"/workspaces/{workspace.name}/documents/{document.name}\">{html.escape(document.name)}</a></li>"
            )
        sections.append(
            "<section class=\"sidebar-workspace\">"
            f"<h2>{html.escape(_workspace_label(workspace.name))}</h2>"
            f"<ul>{''.join(items) if items else '<li class=\"muted\">Sin documentos.</li>'}</ul>"
            "</section>"
        )
    return "".join(sections)


def _workspace_label(name: str) -> str:
    return "Global" if name == GLOBAL_WORKSPACE_NAME else name


if __name__ == "__main__":
    main()
