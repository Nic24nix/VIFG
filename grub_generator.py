"""
VIFG - Virtual ISO for GRUB

GRUB configuration generator.
"""

from pathlib import Path

from config import GRUB_SCRIPT
from grub import get_grub_iso_path
from iso_inspector import inspect_iso
from iso_manager import list_isos


HEADER = """#!/bin/sh
exec tail -n +3 $0

# ==========================================
# VIFG - Virtual ISO for GRUB
# Generated automatically
# ==========================================

"""


def escape_grub_text(text):
    """
    Escape text for a GRUB single-quoted string.
    """

    return str(text).replace("'", "''")


def generate_iso_entry(iso):
    iso = Path(iso)

    name = escape_grub_text(iso.name)
    grub_path = get_grub_iso_path(iso.name)

    info = inspect_iso(iso)

    lines = [
        f"    menuentry '{name}' {{",
        f"        echo 'A carregar {name}...'",
        f"        loopback loop '{grub_path}'",
    ]

    if info["kernel"] and info["initrd"]:

        kernel = info["kernel"]
        initrd = info["initrd"]

        lines.append(
            f"        linux (loop){kernel} "
            f"boot=casper "
            f"iso-scan/filename={grub_path}"
        )

        lines.append(
            f"        initrd (loop){initrd}"
        )

    elif info["boot_wim"]:

        lines.append(
            "        echo 'ISO Windows detetada.'"
        )

        lines.append(
            "        echo 'Boot Windows ainda não implementado.'"
        )

    else:

        lines.append(
            "        echo 'Não foi possível determinar como arrancar esta ISO.'"
        )

    lines.append("    }")

    return lines


def generate_grub_script(directory=None):
    isos = list_isos(directory)

    lines = [HEADER.rstrip()]

    lines.append("")
    lines.append("menuentry 'VIFG' {")
    lines.append("    echo 'VIFG - Virtual ISO for GRUB'")
    lines.append("}")

    lines.append("")
    lines.append("submenu 'VIFG ISOs' {")

    if not isos:

        lines.append(
            "    menuentry 'Nenhuma ISO encontrada' {"
        )

        lines.append(
            "        echo 'Nenhuma ISO foi adicionada ao VIFG.'"
        )

        lines.append("    ")

    else:

        for iso in isos:
            lines.extend(generate_iso_entry(iso))
            lines.append("")

    lines.append("}")

    return "\n".join(lines) + "\n"


def save_grub_script(content, destination=None):
    if destination is None:
        destination = GRUB_SCRIPT
    else:
        destination = Path(destination)

    try:
        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with destination.open(
            "w",
            encoding="utf-8",
        ) as file:
            file.write(content)

        destination.chmod(0o755)

        print(
            f"[✓] Script GRUB guardado em: "
            f"{destination}"
        )

        return True

    except PermissionError:
        print(
            f"[X] Sem permissões para escrever: "
            f"{destination}"
        )
        return False

    except OSError as error:
        print(f"[X] Erro ao guardar script: {error}")
        return False
