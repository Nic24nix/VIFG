"""
VIFG - Virtual ISO for GRUB

ISO inspection module.

Analisa o conteúdo real de uma ISO usando xorriso.
Não modifica o sistema.
"""

import shutil
import subprocess
from pathlib import Path


def list_iso_files(iso):
    """Return the files contained in an ISO."""

    iso = Path(iso)

    if not iso.is_file():
        return []

    xorriso = shutil.which("xorriso")

    if xorriso is None:
        return []

    try:
        result = subprocess.run(
            [
                xorriso,
                "-indev",
                str(iso),
                "-find",
                "/",
                "-type",
                "f",
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            return []

        files = []

        for line in result.stdout.splitlines():
            line = line.strip()

            if line.startswith("'") and line.endswith("'"):
                line = line[1:-1]

            if line:
                files.append(line)

        return files

    except OSError:
        return []


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

    if not result["exists"]:
        return result

    files = list_iso_files(iso)

    normalized_files = {
        file.lower(): file
        for file in files
    }

    # Ubuntu / Debian live ISO
    for file in files:
        lower = file.lower()

        if lower == "/casper/vmlinuz":
            result["kernel"] = file
            result["casper"] = True

        elif lower in [
            "/casper/initrd",
            "/casper/initrd.lz",
            "/casper/initrd.gz",
        ]:
            result["initrd"] = file
            result["casper"] = True

    # Windows ISO
    for file in files:
        if file.lower() == "/sources/boot.wim":
            result["boot_wim"] = file

    # Detect type from actual ISO contents
    if result["boot_wim"]:
        result["type"] = "windows"

    elif result["kernel"] and result["initrd"]:
        result["type"] = "debian"

    else:
        # Fallback to filename detection
        name = iso.name.lower()

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
    print(f"  Kernel:   {info['kernel'] or 'Não encontrado'}")
    print(f"  Initrd:   {info['initrd'] or 'Não encontrado'}")
    print(f"  boot.wim: {info['boot_wim'] or 'Não encontrado'}")
    print()


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Uso:")
        print("  python3 iso_inspector.py ficheiro.iso")
        sys.exit(1)

    print_iso_info(sys.argv[1])
