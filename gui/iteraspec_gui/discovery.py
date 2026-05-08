from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


KNOWN_DOCUMENTS = ("specs.md", "backlog.md", "current_task.md")


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


def discover_workspaces(base_dir: Path | None = None) -> list[IteraSpecWorkspace]:
    root = (base_dir or Path(".iteraspec")).resolve()
    if not root.exists() or not root.is_dir():
        return []

    workspaces: list[IteraSpecWorkspace] = []
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
