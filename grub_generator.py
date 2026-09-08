"""
VIFG - Virtual ISO for GRUB

GRUB script generator.
"""

from pathlib import Path

from config import GRUB_SCRIPT
from iso_manager import list_isos
from iso_inspector import inspect_iso


HEADER = """#!/bin/sh
exec tail -n +3 $0

# ==========================================
# VIFG - Virtual ISO for GRUB
# Generated automatically
# ==========================================

"""


def escape_grub_text(text):
    """Escape text for use inside a GRUB single-quoted string."""
    return text.replace("'", "''")


def generate_iso_entry(iso):
    """Generate a GRUB menu entry for an ISO."""

    name = escape_grub_text(iso.name)
    path = f"/boot/vifg/{name}"

    info = inspect_iso(iso)

    lines = [
        f"    menuentry '{name}' {{",
        f"        echo 'A carregar {name}...'",
        f"        loopback loop '{path}'",
    ]

    if info["kernel"] and info["initrd"]:
        kernel = info["kernel"]
        initrd = info["initrd"]

        lines.append(
            f"        linux (loop){kernel} boot=casper iso-scan/filename={path}"
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
    """Generate the VIFG GRUB script."""

    isos = list_isos(directory)
    lines = [HEADER.rstrip()]

    lines.append("")
    lines.append("menuentry 'VIFG' {")
    lines.append("    echo 'VIFG - Virtual ISO for GRUB'")
    lines.append("}")

    lines.append("")
    lines.append("submenu 'VIFG ISOs' {")

    if not isos:
        lines.append("    menuentry 'Nenhuma ISO encontrada' {")
        lines.append("        echo 'Nenhuma ISO foi adicionada ao VIFG.'")
        lines.append("    }")
    else:
        for iso in isos:
            lines.extend(generate_iso_entry(iso))
            lines.append("")

    lines.append("}")

    return "\n".join(lines) + "\n"


def save_grub_script(content, destination=None):
    """Save the generated GRUB script."""

    if destination is None:
        destination = GRUB_SCRIPT
    else:
        destination = Path(destination)

    try:
        destination.parent.mkdir(parents=True, exist_ok=True)

        with destination.open("w", encoding="utf-8") as file:
            file.write(content)

        destination.chmod(0o755)

        print(f"[✓] Script GRUB guardado em: {destination}")
        return True

    except PermissionError:
        print("[X] Sem permissões para escrever:")
        print(f"    {destination}")
        return False

    except OSError as error:
        print(f"[X] Erro ao guardar o script: {error}")
        return False


def generate_and_save():
    """Generate and save the VIFG GRUB script."""

    print()
    print("[+] A gerar configuração do VIFG...")
    print()

    content = generate_grub_script()

    print("---------- CONFIGURAÇÃO GERADA ----------")
    print(content, end="")
    print("-----------------------------------------")
    print()

    return save_grub_script(content)


if __name__ == "__main__":
    generate_and_save()
