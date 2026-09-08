"""
VIFG - Virtual ISO for GRUB

ISO inspection module.
Inspects the real contents of an ISO using xorriso and 7z.
"""

import shutil
import subprocess
from pathlib import Path

from iso_detector import get_iso_info


def xorriso_available():
    """Check whether xorriso is installed."""
    return shutil.which("xorriso") is not None


def seven_zip_available():
    """Check whether 7z is installed."""
    return shutil.which("7z") is not None


def list_iso_files_xorriso(iso):
    """
    Return a list of files contained in the ISO using xorriso.
    """

    iso = Path(iso)

    if not iso.is_file():
        return []

    if not xorriso_available():
        return []

    command = [
        "xorriso",
        "-indev",
        str(iso),
        "-find",
        "/",
        "-type",
        "f",
    ]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            return []

        files = []

        for line in result.stdout.splitlines():
            line = line.strip()

            if line.startswith("/"):
                files.append(line)

        return files

    except OSError:
        return []


def list_iso_files_7z(iso):
    """
    Return a list of files contained in the ISO using 7z.

    This supports UDF ISOs such as modern Windows installation media.
    """

    iso = Path(iso)

    if not iso.is_file():
        return []

    if not seven_zip_available():
        return []

    command = [
        "7z",
        "l",
        "-slt",
        str(iso),
    ]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            return []

        files = []

        for line in result.stdout.splitlines():
            if not line.startswith("Path = "):
                continue

            path = line[len("Path = "):].strip()

            if not path:
                continue

            if path == iso.name:
                continue

            files.append("/" + path.lstrip("/"))

        return files

    except OSError:
        return []


def list_iso_files(iso):
    """
    Return a list of files contained in the ISO.

    Tries xorriso first and then 7z.
    """

    files = list_iso_files_xorriso(iso)

    if files:
        return files

    files = list_iso_files_7z(iso)

    return files


def find_file(files, names):
    """Find a file by checking its basename."""

    names = {name.lower() for name in names}

    for file in files:
        if Path(file).name.lower() in names:
            return file

    return None


def find_boot_files(files):
    """
    Detect common Linux and Windows boot files.

    Returns:
        kernel
        initrd
        boot_wim
        boot_efi
    """

    kernel = None
    initrd = None
    boot_wim = None
    boot_efi = None

    # -------------------------------------------------
    # Linux kernels
    # -------------------------------------------------

    kernel_names = {
        "vmlinuz",
        "vmlinuz.efi",
        "vmlinuz-linux",
        "vmlinuz-linux-lts",
    }

    kernel = find_file(files, kernel_names)

    if kernel is None:
        for file in files:
            filename = Path(file).name.lower()

            if filename.startswith("vmlinuz"):
                kernel = file
                break

    # -------------------------------------------------
    # Linux initrd / initramfs
    # -------------------------------------------------

    initrd_names = {
        "initrd",
        "initrd.img",
        "initrd.lz",
        "initrd.gz",
        "initrd.xz",
        "initrd.zst",
        "initramfs",
        "initramfs.img",
        "initramfs-linux.img",
        "initramfs-linux-lts.img",
    }

    initrd = find_file(files, initrd_names)

    if initrd is None:
        for file in files:
            filename = Path(file).name.lower()

            if (
                filename.startswith("initrd")
                or filename.startswith("initramfs")
            ):
                initrd = file
                break

    # -------------------------------------------------
    # Windows boot.wim
    # -------------------------------------------------

    for file in files:
        normalized = file.lower()

        if normalized == "/sources/boot.wim":
            boot_wim = file
            break

    if boot_wim is None:
        for file in files:
            if Path(file).name.lower() == "boot.wim":
                boot_wim = file
                break

    # -------------------------------------------------
    # Windows EFI bootloader
    # -------------------------------------------------

    for file in files:
        normalized = file.lower()

        if normalized == "/efi/boot/bootx64.efi":
            boot_efi = file
            break

    return {
        "kernel": kernel,
        "initrd": initrd,
        "boot_wim": boot_wim,
        "boot_efi": boot_efi,
    }


def inspect_iso(iso):
    """
    Inspect an ISO and determine its boot files and type.
    """

    iso = Path(iso)

    detected = get_iso_info(iso)

    result = {
        "name": iso.name,
        "path": iso,
        "type": detected["type"],
        "type_name": detected["type_name"],
        "kernel": None,
        "initrd": None,
        "boot_wim": None,
        "boot_efi": None,
    }

    if not iso.is_file():
        return result

    files = list_iso_files(iso)

    if not files:
        return result

    boot_files = find_boot_files(files)

    result.update(boot_files)

    # -------------------------------------------------
    # Determine type from real contents
    # -------------------------------------------------

    if result["boot_wim"] or result["boot_efi"]:
        result["type"] = "windows"
        result["type_name"] = "Microsoft Windows"

    elif result["kernel"] and result["initrd"]:
        result["type"] = "debian"
        result["type_name"] = "Linux / Debian-based"

    return result


def print_iso_inspection(iso):
    """Print human-readable ISO inspection information."""

    iso = Path(iso)

    print()
    print("=" * 42)
    print("             ISO INSPECTION")
    print("=" * 42)
    print()

    if not iso.is_file():
        print("[X] Ficheiro não encontrado.")
        return

    print("[✓] Ficheiro encontrado.")
    print(f"Nome: {iso.name}")

    info = inspect_iso(iso)

    print(f"Tipo: {info['type']}")

    print()
    print("Boot files:")
    print(f"  Kernel:   {info['kernel'] or 'Não encontrado'}")
    print(f"  Initrd:   {info['initrd'] or 'Não encontrado'}")
    print(f"  boot.wim: {info['boot_wim'] or 'Não encontrado'}")
    print(f"  EFI:      {info['boot_efi'] or 'Não encontrado'}")
    print()

    if info["kernel"] and info["initrd"]:
        print("[✓] Kernel e initrd encontrados.")
        print("[✓] ISO Linux preparada para boot pelo VIFG.")

    elif info["boot_wim"] and info["boot_efi"]:
        print("[✓] boot.wim encontrado.")
        print("[✓] EFI bootloader encontrado.")
        print("[✓] ISO Windows reconhecida pelo VIFG.")
        print("[!] Boot Windows pelo VIFG ainda não implementado.")

    elif info["boot_wim"]:
        print("[✓] boot.wim encontrado.")
        print("[!] Boot Windows pelo VIFG ainda não implementado.")

    else:
        print("[X] Não foi possível determinar como arrancar esta ISO.")

    print()


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Uso:")
        print("  python3 iso_inspector.py <ISO>")
        sys.exit(1)

    print_iso_inspection(sys.argv[1])
