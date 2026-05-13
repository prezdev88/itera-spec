#!/usr/bin/env bash

set -euo pipefail

if [ "$#" -ne 1 ]; then
  printf 'Uso: %s <ruta-del-proyecto-destino>\n' "$(basename "$0")" >&2
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_AGENTS_FILE="${SCRIPT_DIR}/AGENTS.md"
SOURCE_DEVELOPER_CREATION_FILE="${SCRIPT_DIR}/DEVELOPER_PROFILE_CREATION.md"
SOURCE_PROTOCOL_FILE="${SCRIPT_DIR}/ITERASPEC.md"
SOURCE_DEVELOPERS_DIR="${SCRIPT_DIR}/developers"
SOURCE_GUI_DIR="${SCRIPT_DIR}/gui"
TARGET_ROOT="$(realpath -m "$1")"
TARGET_ITERASPEC_DIR="${TARGET_ROOT}/.iteraspec"
TARGET_PROTOCOL_FILE="${TARGET_ITERASPEC_DIR}/ITERASPEC.md"
TARGET_DEVELOPER_CREATION_FILE="${TARGET_ITERASPEC_DIR}/DEVELOPER_PROFILE_CREATION.md"
TARGET_DEVELOPERS_DIR="${TARGET_ITERASPEC_DIR}/developers"
TARGET_WORKSPACES_DIR="${TARGET_ITERASPEC_DIR}/workspaces"
TARGET_GUI_DIR="${TARGET_ITERASPEC_DIR}/gui"
TARGET_LEGACY_BACKUP_DIR="${TARGET_ITERASPEC_DIR}/legacy-backup"
TARGET_STATUS_FILE="${TARGET_WORKSPACES_DIR}/status.md"
LEGACY_PROTOCOL_FILE="${TARGET_ROOT}/ITERASPEC.md"
LEGACY_DEVELOPER_CREATION_FILE="${TARGET_ROOT}/DEVELOPER_PROFILE_CREATION.md"
LEGACY_GUI_DIR="${TARGET_ROOT}/.gui"
LEGACY_STATUS_FILE="${TARGET_ITERASPEC_DIR}/status.md"

if [ ! -f "${SOURCE_AGENTS_FILE}" ]; then
  printf 'No se encontró el archivo fuente: %s\n' "${SOURCE_AGENTS_FILE}" >&2
  exit 1
fi

if [ ! -f "${SOURCE_DEVELOPER_CREATION_FILE}" ]; then
  printf 'No se encontró el archivo fuente: %s\n' "${SOURCE_DEVELOPER_CREATION_FILE}" >&2
  exit 1
fi

if [ ! -f "${SOURCE_PROTOCOL_FILE}" ]; then
  printf 'No se encontró el archivo fuente: %s\n' "${SOURCE_PROTOCOL_FILE}" >&2
  exit 1
fi

if [ ! -d "${SOURCE_DEVELOPERS_DIR}" ]; then
  printf 'No se encontró el directorio fuente: %s\n' "${SOURCE_DEVELOPERS_DIR}" >&2
  exit 1
fi

for file in "${SOURCE_DEVELOPERS_DIR}"/*.md; do
  if [ ! -f "${file}" ]; then
    printf 'No se encontraron perfiles de developer en: %s\n' "${SOURCE_DEVELOPERS_DIR}" >&2
    exit 1
  fi
done

for file in app.py run.sh requirements.txt; do
  if [ ! -f "${SOURCE_GUI_DIR}/${file}" ]; then
    printf 'No se encontró el archivo fuente: %s\n' "${SOURCE_GUI_DIR}/${file}" >&2
    exit 1
  fi
done

is_legacy_gui_installation() {
  [ -d "${LEGACY_GUI_DIR}" ] || return 1
  [ -f "${LEGACY_GUI_DIR}/app.py" ] || return 1
  [ -f "${LEGACY_GUI_DIR}/run.sh" ] || return 1
  [ -f "${LEGACY_GUI_DIR}/requirements.txt" ] || return 1
}

backup_legacy_file() {
  local source_path="$1"
  local backup_name="$2"

  [ -f "${source_path}" ] || return 0
  mkdir -p "${TARGET_LEGACY_BACKUP_DIR}"
  mv "${source_path}" "${TARGET_LEGACY_BACKUP_DIR}/${backup_name}"
}

backup_legacy_directory() {
  local source_path="$1"
  local backup_name="$2"

  [ -d "${source_path}" ] || return 0
  mkdir -p "${TARGET_LEGACY_BACKUP_DIR}"
  rm -rf "${TARGET_LEGACY_BACKUP_DIR:?}/${backup_name}"
  mv "${source_path}" "${TARGET_LEGACY_BACKUP_DIR}/${backup_name}"
}

migrate_workspace_directories() {
  local candidate
  local candidate_name

  mkdir -p "${TARGET_WORKSPACES_DIR}"
  for candidate in "${TARGET_ITERASPEC_DIR}"/*; do
    [ -d "${candidate}" ] || continue
    candidate_name="$(basename "${candidate}")"
    case "${candidate_name}" in
      developers|gui|legacy-backup|workspaces)
        continue
        ;;
    esac
    if [ -e "${TARGET_WORKSPACES_DIR}/${candidate_name}" ]; then
      backup_legacy_directory "${candidate}" "workspace-${candidate_name}"
      continue
    fi
    mv "${candidate}" "${TARGET_WORKSPACES_DIR}/"
  done
}

migrate_status_file() {
  if [ -f "${LEGACY_STATUS_FILE}" ] && [ ! -f "${TARGET_STATUS_FILE}" ]; then
    mv "${LEGACY_STATUS_FILE}" "${TARGET_STATUS_FILE}"
    return
  fi

  if [ -f "${LEGACY_STATUS_FILE}" ]; then
    backup_legacy_file "${LEGACY_STATUS_FILE}" "status.md"
  fi
}

mkdir -p "${TARGET_ROOT}"
mkdir -p "${TARGET_ITERASPEC_DIR}"
mkdir -p "${TARGET_DEVELOPERS_DIR}"
mkdir -p "${TARGET_WORKSPACES_DIR}"
mkdir -p "${TARGET_GUI_DIR}"

cp "${SOURCE_DEVELOPER_CREATION_FILE}" "${TARGET_DEVELOPER_CREATION_FILE}"
cp "${SOURCE_PROTOCOL_FILE}" "${TARGET_PROTOCOL_FILE}"
cp "${SOURCE_DEVELOPERS_DIR}"/*.md "${TARGET_DEVELOPERS_DIR}/"
cp "${SOURCE_GUI_DIR}/app.py" "${TARGET_GUI_DIR}/app.py"
cp "${SOURCE_GUI_DIR}/run.sh" "${TARGET_GUI_DIR}/run.sh"
cp "${SOURCE_GUI_DIR}/requirements.txt" "${TARGET_GUI_DIR}/requirements.txt"

python3 - <<'PY' "${SOURCE_AGENTS_FILE}" "${TARGET_ROOT}/AGENTS.md" "${TARGET_PROTOCOL_FILE}"
from pathlib import Path
import sys

source_agents = Path(sys.argv[1])
target_agents = Path(sys.argv[2])
target_protocol = Path(sys.argv[3])

content = source_agents.read_text(encoding="utf-8")
content = content.replace("`ITERASPEC.md`", "`.iteraspec/ITERASPEC.md`")
content = content.replace("`DEVELOPER_PROFILE_CREATION.md`", "`.iteraspec/DEVELOPER_PROFILE_CREATION.md`")
content = content.replace("`gui/`", "`.iteraspec/gui/`")
content = content.replace(
    "This repository uses `.iteraspec/ITERASPEC.md` as the main working protocol.",
    "This repository uses `.iteraspec/ITERASPEC.md` as the main working protocol after installation.",
)
content = content.replace(
    "- `.iteraspec/gui/` is reserved for the IteraSpec GUI in this repository and must not be repurposed for product work unless the user explicitly requests changes there.",
    "- `.iteraspec/gui/` is reserved for the IteraSpec GUI in this installed repository and must not be repurposed for product work unless the user explicitly requests changes there.",
)
content = content.replace(
    "- The repository documentation currently references `.iteraspec/gui/` as the visible GUI directory.",
    "- The installed repository layout keeps the visible GUI directory under `.iteraspec/gui/`.",
)
target_agents.write_text(content, encoding="utf-8")

protocol_content = target_protocol.read_text(encoding="utf-8")
protocol_content = protocol_content.replace("`DEVELOPER_PROFILE_CREATION.md`", "`.iteraspec/DEVELOPER_PROFILE_CREATION.md`")
protocol_content = protocol_content.replace("`gui/`", "`.iteraspec/gui/`")
protocol_content = protocol_content.replace("the root `.iteraspec/gui/` directory", "the `.iteraspec/gui/` directory")
protocol_content = protocol_content.replace("a `.iteraspec/gui/` directory exists at the root of the project", "a `.iteraspec/gui/` directory exists in the project")
target_protocol.write_text(protocol_content, encoding="utf-8")
PY

backup_legacy_file "${LEGACY_PROTOCOL_FILE}" "ITERASPEC.md"
backup_legacy_file "${LEGACY_DEVELOPER_CREATION_FILE}" "DEVELOPER_PROFILE_CREATION.md"

if is_legacy_gui_installation; then
  backup_legacy_directory "${LEGACY_GUI_DIR}" ".gui"
fi

migrate_workspace_directories
migrate_status_file

printf 'IteraSpec instalado en:\n'
printf '  %s\n' "${TARGET_ROOT}/AGENTS.md"
printf '  %s\n' "${TARGET_PROTOCOL_FILE}"
printf '  %s\n' "${TARGET_DEVELOPER_CREATION_FILE}"
printf '  %s\n' "${TARGET_DEVELOPERS_DIR}"
printf '  %s\n' "${TARGET_WORKSPACES_DIR}"
printf '  %s\n' "${TARGET_GUI_DIR}"
if [ -d "${TARGET_LEGACY_BACKUP_DIR}" ]; then
  printf '  %s\n' "${TARGET_LEGACY_BACKUP_DIR}"
fi
if [ -f "${LEGACY_PROTOCOL_FILE}" ] || [ -f "${LEGACY_DEVELOPER_CREATION_FILE}" ] || [ -d "${LEGACY_GUI_DIR}" ]; then
  printf '\nAtencion: quedaron residuos legacy no reconocidos automaticamente. Revisa manualmente:\n'
  [ -f "${LEGACY_PROTOCOL_FILE}" ] && printf '  %s\n' "${LEGACY_PROTOCOL_FILE}"
  [ -f "${LEGACY_DEVELOPER_CREATION_FILE}" ] && printf '  %s\n' "${LEGACY_DEVELOPER_CREATION_FILE}"
  [ -d "${LEGACY_GUI_DIR}" ] && printf '  %s\n' "${LEGACY_GUI_DIR}"
fi
printf '\nUsa esta instrucción con tu asistente:\n'
printf '  Sigue estrictamente `.iteraspec/ITERASPEC.md` como protocolo principal de este proyecto. Léelo completo antes de actuar y obedécelo literalmente.\n'
