"""
VIFG - Virtual ISO for GRUB

Inspects ISO contents using xorriso.
"""

import shutil
import subprocess
from pathlib import Path


def xorriso_available():
    return shutil.which("xorriso") is not None


def get_iso_listing(iso):
    iso = Path(iso)

    if not iso.is_file():
        return []

    if not xorriso_available():
        return []

    try:
        result = subprocess.run(
            [
                "xorriso",
                "-indev",
                str(iso),
                "-find",
                "/",
                "-type",
                "f",
                "-print",
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            return []

        return [
            line.strip()
            for line in result.stdout.splitlines()
            if line.strip()
        ]

    except OSError:
        return []


def inspect_iso(iso):
    files = get_iso_listing(iso)

    kernel = None
    initrd = None
    boot_wim = None

    for file in files:
        normalized = file.lower()

        if normalized.endswith("/vmlinuz"):
            kernel = file

        elif normalized.endswith("/vmlinuz-linux"):
            kernel = file

        elif normalized.endswith("/initrd"):
            initrd = file

        elif normalized.endswith("/initrd.img"):
            initrd = file

        elif normalized.endswith("/initramfs-linux.img"):
            initrd = file

        elif normalized.endswith("/sources/boot.wim"):
            boot_wim = file

    return {
        "kernel": kernel,
        "initrd": initrd,
        "boot_wim": boot_wim,
        "files": files,
    }


def print_inspection(iso):
    info = inspect_iso(iso)

    print()
    print("=" * 42)
    print("             ISO INSPECTOR")
    print("=" * 42)
    print()

    print(f"ISO: {Path(iso).name}")
    print()

    print("Boot files:")

    print(
        f"  Kernel:   "
        f"{info['kernel'] or 'Não encontrado'}"
    )

    print(
        f"  Initrd:   "
        f"{info['initrd'] or 'Não encontrado'}"
    )

    print(
        f"  boot.wim: "
        f"{info['boot_wim'] or 'Não encontrado'}"
    )

    print()
