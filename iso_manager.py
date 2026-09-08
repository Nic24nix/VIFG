"""
VIFG - Virtual ISO for GRUB

ISO management.
"""

import shutil
from pathlib import Path

from config import ISO_DIR, MAX_ISOS


def ensure_iso_directory():
    try:
        ISO_DIR.mkdir(parents=True, exist_ok=True)
        return True

    except PermissionError:
        print("[X] Sem permissões para criar:")
        print(f"    {ISO_DIR}")
        return False

    except OSError as error:
        print(f"[X] Erro ao criar diretório: {error}")
        return False


def list_isos(directory=None):
    if directory is None:
        directory = ISO_DIR
    else:
        directory = Path(directory)

    if not directory.is_dir():
        return []

    return sorted(
        [
            file
            for file in directory.iterdir()
            if file.is_file()
            and file.suffix.lower() == ".iso"
        ],
        key=lambda path: path.name.lower(),
    )


def iso_exists(name):
    return (ISO_DIR / name).is_file()


def add_iso(source):
    source = Path(source)

    if not source.exists():
        print(f"[X] ISO não encontrada: {source}")
        return False

    if not source.is_file():
        print("[X] O caminho não é um ficheiro.")
        return False

    if source.suffix.lower() != ".iso":
        print("[X] O ficheiro não é uma ISO.")
        return False

    if not ensure_iso_directory():
        return False

    current_isos = list_isos()

    if len(current_isos) >= MAX_ISOS:
        print(f"[X] Limite máximo de {MAX_ISOS} ISOs atingido.")
        return False

    destination = ISO_DIR / source.name

    if destination.exists():
        print(f"[X] Já existe:")
        print(f"    {destination}")
        return False

    try:
        print()
        print(f"[+] A copiar {source.name}...")
        print(f"    → {destination}")

        shutil.copy2(source, destination)

        print("[✓] ISO adicionada.")
        return True

    except PermissionError:
        print("[X] Sem permissões para copiar a ISO.")
        return False

    except OSError as error:
        print(f"[X] Erro ao copiar ISO: {error}")
        return False


def remove_iso(name):
    iso = ISO_DIR / name

    if not iso.is_file():
        print(f"[X] ISO não encontrada: {name}")
        return False

    try:
        iso.unlink()
        print(f"[✓] ISO removida: {name}")
        return True

    except OSError as error:
        print(f"[X] Erro ao remover ISO: {error}")
        return False


def get_iso_size(iso):
    try:
        return Path(iso).stat().st_size
    except OSError:
        return 0


def format_size(size):
    units = ["B", "KB", "MB", "GB", "TB"]

    size = float(size)

    for unit in units:
        if size < 1024:
            return f"{size:.1f} {unit}"

        size /= 1024

    return f"{size:.1f} PB"


def get_iso_info(iso):
    iso = Path(iso)

    size = get_iso_size(iso)

    return {
        "name": iso.name,
        "path": iso,
        "size": size,
        "size_formatted": format_size(size),
    }
