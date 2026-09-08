"""
VIFG - Virtual ISO for GRUB

GRUB diagnostics and path detection.
"""

import shutil
from pathlib import Path

from config import GRUB_CONFIG, GRUB_SCRIPT


GRUB_DIR = Path("/etc/grub.d")
UPDATE_GRUB = shutil.which("update-grub")
GRUB_MKCONFIG = shutil.which("grub-mkconfig")
GRUB_SCRIPT_CHECK = shutil.which("grub-script-check")


def grub_installed():
    return GRUB_DIR.is_dir()


def grub_config_exists():
    return GRUB_CONFIG.is_file()


def grub_tools_available():
    return (
        GRUB_MKCONFIG is not None
        or UPDATE_GRUB is not None
    )


def vifg_script_exists():
    return GRUB_SCRIPT.is_file()


def get_grub_timeout():
    if not grub_config_exists():
        return None

    try:
        with GRUB_CONFIG.open("r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                if line.startswith("GRUB_TIMEOUT="):
                    value = line.split("=", 1)[1]
                    value = value.strip("\"'")

                    try:
                        return int(value)
                    except ValueError:
                        return value

    except OSError:
        return None

    return None


def boot_is_separate():
    """
    Detect whether /boot is a separate mount point.
    """

    return Path("/boot").is_mount()


def get_grub_iso_path(filename):
    """
    Return the path GRUB should use for an ISO.
    """

    if boot_is_separate():
        return f"/vifg/{filename}"

    return f"/boot/vifg/{filename}"


def get_grub_info():
    return {
        "grub_installed": grub_installed(),
        "grub_config": grub_config_exists(),
        "grub_tools": grub_tools_available(),
        "grub_script": vifg_script_exists(),
        "timeout": get_grub_timeout(),
        "boot_separate": boot_is_separate(),
    }


def print_grub_info():
    info = get_grub_info()

    print()
    print("=" * 42)
    print("             GRUB STATUS")
    print("=" * 42)
    print()

    print(
        "[✓] GRUB encontrado."
        if info["grub_installed"]
        else "[X] GRUB não encontrado."
    )

    print(
        "[✓] /etc/default/grub encontrado."
        if info["grub_config"]
        else "[X] /etc/default/grub não encontrado."
    )

    print(
        "[✓] Ferramentas GRUB disponíveis."
        if info["grub_tools"]
        else "[X] Ferramentas GRUB não encontradas."
    )

    if info["boot_separate"]:
        print("[+] /boot é uma partição/mount separado.")
        print("    Caminho GRUB VIFG: /vifg/")
    else:
        print("[+] /boot está dentro da raiz.")
        print("    Caminho GRUB VIFG: /boot/vifg/")

    if info["timeout"] is not None:
        print(f"[+] GRUB_TIMEOUT = {info['timeout']}")

    print()
