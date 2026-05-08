from __future__ import annotations

import html
import re
from dataclasses import dataclass


BACKLOG_SECTIONS = {
    "## 🔴 To Do": ("todo", "To Do"),
    "## 🟡 In Progress": ("inprogress", "In Progress"),
    "## 🟢 Done": ("done", "Done"),
    "## ⚫ Blocked": ("blocked", "Blocked"),
}


@dataclass(slots=True)
class BacklogTask:
    title: str
    bullets: list[str]


@dataclass(slots=True)
class BacklogSection:
    key: str
    label: str
    tasks: list[BacklogTask]


@dataclass(slots=True)
class CurrentTaskView:
    title: str
    identifier: str
    objective: str
    acceptance: list[str]
    notes: list[str]


def render_specialized_document(document_name: str, content: str) -> str | None:
    if document_name == "backlog.md":
        return render_backlog_view(content)
    if document_name == "current_task.md":
        return render_current_task_view(content)
    return None


def render_backlog_view(content: str) -> str:
    sections = parse_backlog(content)
    summary = "".join(
        (
            "<article class=\"status-summary-card\">"
            f"<span class=\"status-chip {section.key}\">{section.label}</span>"
            f"<strong>{len(section.tasks)}</strong>"
            "<span>tareas</span>"
            "</article>"
        )
        for section in sections
    )
    board = "".join(
        (
            "<section class=\"backlog-column\">"
            f"<header><span class=\"status-chip {section.key}\">{section.label}</span></header>"
            f"{render_backlog_tasks(section.tasks)}"
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


def parse_backlog(content: str) -> list[BacklogSection]:
    sections: list[BacklogSection] = []
    current_key = None
    current_label = None
    current_tasks: list[BacklogTask] = []
    current_task: BacklogTask | None = None

    for raw_line in content.splitlines():
        line = raw_line.rstrip()
        if line in BACKLOG_SECTIONS:
            if current_key is not None:
                sections.append(BacklogSection(current_key, current_label or current_key, current_tasks))
            current_key, current_label = BACKLOG_SECTIONS[line]
            current_tasks = []
            current_task = None
            continue

        if current_key is None:
            continue

        if line.startswith("### "):
            current_task = BacklogTask(title=line[4:].strip(), bullets=[])
            current_tasks.append(current_task)
            continue

        if line.startswith("- ") and current_task is not None:
            current_task.bullets.append(line[2:].strip())
            continue

    if current_key is not None:
        sections.append(BacklogSection(current_key, current_label or current_key, current_tasks))

    return sections


def parse_current_task(content: str) -> CurrentTaskView:
    title = first_heading(content) or "Tarea activa"
    identifier = first_bullet_after_heading(content, "## Identificador")
    objective = collect_section_paragraph(content, "## Objetivo")
    acceptance = collect_section_bullets(content, "## Criterios de Aceptación")
    notes = collect_section_bullets(content, "## Notas de Implementación")
    return CurrentTaskView(title=title, identifier=identifier, objective=objective, acceptance=acceptance, notes=notes)


def render_backlog_tasks(tasks: list[BacklogTask]) -> str:
    if not tasks:
        return "<div class=\"empty-task-card\">Sin tareas en esta columna.</div>"
    return "".join(
        (
            "<article class=\"task-card\">"
            "<div class=\"task-card-title-row\">"
            "<span class=\"task-state-dot\"></span>"
            f"<h3>{html.escape(task.title)}</h3>"
            "</div>"
            f"{render_task_bullets(task.bullets)}"
            "</article>"
        )
        for task in tasks
    )


def render_task_bullets(bullets: list[str]) -> str:
    if not bullets:
        return "<p class=\"muted\">Sin detalle adicional.</p>"
    items = "".join(f"<li>{html.escape(item)}</li>" for item in bullets[:4])
    return f"<ul>{items}</ul>"


def first_heading(content: str) -> str | None:
    match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    return match.group(1).strip() if match else None


def first_bullet_after_heading(content: str, heading: str) -> str:
    section = section_body(content, heading)
    match = re.search(r"^- `?(.+?)`?$", section, re.MULTILINE)
    return match.group(1).strip() if match else ""


def collect_section_paragraph(content: str, heading: str) -> str:
    section = section_body(content, heading)
    for line in section.splitlines():
        if line.strip() and not line.startswith("- "):
            return line.strip()
    return ""


def collect_section_bullets(content: str, heading: str) -> list[str]:
    section = section_body(content, heading)
    return [line[2:].strip() for line in section.splitlines() if line.startswith("- ")]


def section_body(content: str, heading: str) -> str:
    pattern = rf"{re.escape(heading)}\n(.*?)(?:\n## |\Z)"
    match = re.search(pattern, content, re.DOTALL)
    return match.group(1).strip() if match else ""
