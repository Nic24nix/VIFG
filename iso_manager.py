```python
"""
VIFG - Virtual ISO for GRUB

ISO management module.
"""

import shutil
from pathlib import Path

from config import ISO_DIR


# ==========================================
# ISO Manager
# ==========================================

def ensure_iso_directory():
    """Create the ISO directory if it does not exist."""

    try:
        ISO_DIR.mkdir(parents=True, exist_ok=True)
        return True

    except PermissionError:
        print("[X] Sem permissões para criar o diretório das ISOs.")
        print(f"    Diretório: {ISO_DIR}")
        return False

    except OSError as error:
        print(f"[X] Erro ao criar o diretório das ISOs: {error}")
        return False


def list_isos():
    """Return a list of ISO files stored by VIFG."""

    if not ensure_iso_directory():
        return []

    isos = []

    for file in ISO_DIR.iterdir():
        if file.is_file() and file.suffix.lower() == ".iso":
            isos.append(file)

    return sorted(isos, key=lambda path: path.name.lower())


def iso_exists(name):
    """Check whether an ISO already exists."""

    iso_path = ISO_DIR / name
    return iso_path.is_file()


def add_iso(source):
    """Copy an ISO into the VIFG ISO directory."""

    source = Path(source)

    if not source.exists():
        print(f"[X] Ficheiro não encontrado: {source}")
        return False

    if not source.is_file():
        print("[X] O caminho indicado não é um ficheiro.")
        return False

    if source.suffix.lower() != ".iso":
        print("[X] O ficheiro indicado não é uma ISO.")
        return False

    if not ensure_iso_directory():
        return False

    destination = ISO_DIR / source.name

    if destination.exists():
        print(f"[X] Já existe uma ISO com esse nome:")
        print(f"    {destination.name}")
        return False

    try:
        print()
        print(f"[+] A copiar: {source.name}")
        print(f"    Destino: {destination}")

        shutil.copy2(source, destination)

        print("[✓] ISO adicionada com sucesso.")
        return True

    except PermissionError:
        print("[X] Sem permissões para copiar a ISO.")
        return False

    except OSError as error:
        print(f"[X] Erro ao copiar a ISO: {error}")
        return False


def remove_iso(name):
    """Remove an ISO from the VIFG ISO directory."""

    iso_path = ISO_DIR / name

    if not iso_path.is_file():
        print(f"[X] ISO não encontrada: {name}")
        return False

    if iso_path.suffix.lower() != ".iso":
        print("[X] O ficheiro indicado não é uma ISO.")
        return False

    try:
        iso_path.unlink()

        print(f"[✓] ISO removida: {name}")
        return True

    except PermissionError:
        print("[X] Sem permissões para remover a ISO.")
        return False

    except OSError as error:
        print(f"[X] Erro ao remover a ISO: {error}")
        return False


def get_iso_size(iso):
    """Return the size of an ISO in bytes."""

    iso = Path(iso)

    try:
        return iso.stat().st_size

    except OSError:
        return 0


def format_size(size):
    """Convert bytes into a human-readable size."""

    units = ["B", "KB", "MB", "GB", "TB"]

    size = float(size)

    for unit in units:
        if size < 1024:
            return f"{size:.1f} {unit}"

        size /= 1024

    return f"{size:.1f} PB"


def get_iso_info(iso):
    """Return basic information about an ISO."""

    iso = Path(iso)

    return {
        "name": iso.name,
        "path": iso,
        "size": get_iso_size(iso),
        "size_formatted": format_size(get_iso_size(iso)),
    }
```
