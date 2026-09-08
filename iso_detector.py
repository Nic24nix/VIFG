"""
VIFG - Virtual ISO for GRUB

ISO type detection module.
"""

from pathlib import Path


def detect_iso_type(iso):
    """
    Detect the type of an ISO.

    Returns:
        str: Detected ISO type.
    """

    iso = Path(iso)

    if not iso.is_file():
        return "unknown"

    name = iso.name.lower()

    # Ubuntu / Debian based
    if any(word in name for word in [
        "ubuntu",
        "kubuntu",
        "xubuntu",
        "lubuntu",
        "linuxmint",
        "debian",
    ]):
        return "debian"

    # Arch based
    if any(word in name for word in [
        "arch",
        "manjaro",
        "endeavouros",
        "garuda",
    ]):
        return "arch"

    # Fedora based
    if any(word in name for word in [
        "fedora",
        "nobara",
    ]):
        return "fedora"

    # Windows
    if any(word in name for word in [
        "windows",
        "win10",
        "win11",
        "win7",
    ]):
        return "windows"

    return "unknown"


def get_iso_type_name(iso_type):
    """Return a human-readable ISO type name."""

    names = {
        "debian": "Debian/Ubuntu",
        "arch": "Arch Linux",
        "fedora": "Fedora",
        "windows": "Windows",
        "unknown": "Desconhecido",
    }

    return names.get(iso_type, "Desconhecido")


def get_iso_info(iso):
    """Return detection information about an ISO."""

    iso_type = detect_iso_type(iso)

    return {
        "path": Path(iso),
        "type": iso_type,
        "type_name": get_iso_type_name(iso_type),
    }


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Uso:")
        print("  python3 iso_detector.py ficheiro.iso")
        sys.exit(1)

    iso = Path(sys.argv[1])
    info = get_iso_info(iso)

    print()
    print("=" * 42)
    print("             ISO DETECTOR")
    print("=" * 42)
    print()
    print(f"ISO:   {info['path'].name}")
    print(f"Tipo:  {info['type_name']}")
    print()
