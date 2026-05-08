from __future__ import annotations

import os
import sys

try:
    import uvicorn
except ModuleNotFoundError as exc:
    print(
        "Falta una dependencia para iniciar la GUI.\n"
        "Instala los requisitos con:\n"
        "  pip install -r requirements.txt",
        file=sys.stderr,
    )
    raise SystemExit(1) from exc

from iteraspec_gui.web import create_app


def main() -> None:
    port = int(os.environ.get("PORT", "8001"))
    uvicorn.run(create_app(), host="127.0.0.1", port=port)


if __name__ == "__main__":
    main()
