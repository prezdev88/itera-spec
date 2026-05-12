#!/usr/bin/env bash

set -euo pipefail

if [ "$#" -ne 1 ]; then
  printf 'Uso: %s <ruta-del-proyecto-destino>\n' "$(basename "$0")" >&2
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_AGENTS_FILE="${SCRIPT_DIR}/AGENTS.md"
SOURCE_PROTOCOL_FILE="${SCRIPT_DIR}/ITERASPEC.md"
SOURCE_DEVELOPERS_DIR="${SCRIPT_DIR}/developers"
SOURCE_GUI_DIR="${SCRIPT_DIR}/gui"
TARGET_ROOT="$(realpath -m "$1")"
TARGET_ITERASPEC_DIR="${TARGET_ROOT}/.iteraspec"
TARGET_DEVELOPERS_DIR="${TARGET_ITERASPEC_DIR}/developers"
TARGET_GUI_DIR="${TARGET_ROOT}/.gui"

if [ ! -f "${SOURCE_AGENTS_FILE}" ]; then
  printf 'No se encontró el archivo fuente: %s\n' "${SOURCE_AGENTS_FILE}" >&2
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

mkdir -p "${TARGET_ROOT}"
mkdir -p "${TARGET_ITERASPEC_DIR}"
mkdir -p "${TARGET_DEVELOPERS_DIR}"
mkdir -p "${TARGET_GUI_DIR}"

cp "${SOURCE_AGENTS_FILE}" "${TARGET_ROOT}/AGENTS.md"
cp "${SOURCE_PROTOCOL_FILE}" "${TARGET_ROOT}/ITERASPEC.md"
cp "${SOURCE_DEVELOPERS_DIR}"/*.md "${TARGET_DEVELOPERS_DIR}/"
cp "${SOURCE_GUI_DIR}/app.py" "${TARGET_GUI_DIR}/app.py"
cp "${SOURCE_GUI_DIR}/run.sh" "${TARGET_GUI_DIR}/run.sh"
cp "${SOURCE_GUI_DIR}/requirements.txt" "${TARGET_GUI_DIR}/requirements.txt"

printf 'IteraSpec instalado en:\n'
printf '  %s\n' "${TARGET_ROOT}/AGENTS.md"
printf '  %s\n' "${TARGET_ROOT}/ITERASPEC.md"
printf '  %s\n' "${TARGET_DEVELOPERS_DIR}"
printf '  %s\n' "${TARGET_GUI_DIR}"
printf '\nUsa esta instrucción con tu asistente:\n'
printf '  Sigue estrictamente `ITERASPEC.md` como protocolo principal de este proyecto. Léelo completo antes de actuar y obedécelo literalmente.\n'
