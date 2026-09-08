"""
VIFG - Virtual ISO for GRUB

Basic ISO type detection.
"""

from pathlib import Path


def detect_iso_type(iso):
    """
    Detect a basic ISO family from its contents.

    This function is intentionally conservative.
    """

    iso = Path(iso)

    if not iso.is_file():
        return "unknown"

    name = iso.name.lower()

    if "windows" in name:
        return "windows"

    if "ubuntu" in name:
        return "ubuntu"

    if "debian" in name:
        return "debian"

    if "fedora" in name:
        return "fedora"

    if "arch" in name:
        return "arch"

    return "unknown"


def get_iso_type_name(iso_type):
    names = {
        "ubuntu": "Ubuntu",
        "debian": "Debian",
        "fedora": "Fedora",
        "arch": "Arch Linux",
        "windows": "Windows",
        "unknown": "Desconhecido",
    }

    return names.get(iso_type, "Desconhecido")


def get_iso_info(iso):
    iso_type = detect_iso_type(iso)

    return {
        "path": Path(iso),
        "type": iso_type,
        "type_name": get_iso_type_name(iso_type),
    }
