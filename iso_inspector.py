"""
VIFG - Virtual ISO for GRUB

ISO inspection module.

Esta versão analisa a estrutura de uma ISO
sem modificar o sistema.
"""

from pathlib import Path


def inspect_iso(iso):
    """
    Inspect an ISO and look for common boot files.

    Returns:
        dict: Information found inside the ISO.
    """

    iso = Path(iso)

    result = {
        "exists": iso.is_file(),
        "type": "unknown",
        "kernel": None,
        "initrd": None,
        "boot_wim": None,
        "casper": False,
    }

    if not iso.is_file():
        return result

    name = iso.name.lower()

    # Detection based on filename for now.
    if any(word in name for word in [
        "ubuntu",
        "kubuntu",
        "xubuntu",
        "lubuntu",
        "debian",
        "linuxmint",
    ]):
        result["type"] = "debian"

    elif any(word in name for word in [
        "arch",
        "manjaro",
        "endeavouros",
        "garuda",
    ]):
        result["type"] = "arch"

    elif any(word in name for word in [
        "fedora",
        "nobara",
    ]):
        result["type"] = "fedora"

    elif any(word in name for word in [
        "windows",
        "win10",
        "win11",
        "win7",
    ]):
        result["type"] = "windows"

    return result


def print_iso_info(iso):
    """Print information about an ISO."""

    info = inspect_iso(iso)

    print()
    print("=" * 42)
    print("             ISO INSPECTOR")
    print("=" * 42)
    print()

    print(f"ISO:       {Path(iso).name}")

    if info["exists"]:
        print("[✓] Ficheiro encontrado.")
    else:
        print("[X] Ficheiro não encontrado.")
        return

    print(f"Tipo:      {info['type']}")

    print()
    print("Boot files:")
    print(f"  Kernel:  {info['kernel'] or 'Não encontrado'}")
    print(f"  Initrd:  {info['initrd'] or 'Não encontrado'}")
    print(f"  boot.wim: {info['boot_wim'] or 'Não encontrado'}")
    print()


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Uso:")
        print("  python3 iso_inspector.py ficheiro.iso")
        sys.exit(1)

    print_iso_info(sys.argv[1])
