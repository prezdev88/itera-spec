from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .discovery import IteraSpecDocument, discover_workspaces


@dataclass(slots=True)
class IteraSpecDocumentContent:
    workspace_name: str
    document: IteraSpecDocument
    content: str
    size_bytes: int


class DocumentNotFoundError(Exception):
    pass


class InvalidDocumentRequestError(Exception):
    pass


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
