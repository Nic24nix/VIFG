"""
VIFG - Virtual ISO for GRUB

GRUB script generator.
"""

from config import GRUB_SCRIPT
from iso_manager import list_isos


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

    return [
        f"    menuentry '{name}' {{",
        f"        echo 'ISO selecionada: {name}'",
        "    }",
    ]


def generate_grub_script(directory=None):
    """Generate the VIFG GRUB script."""
    isos = list_isos(directory)
    lines = [HEADER.rstrip()]

    # Main VIFG entry
    lines.append("")
    lines.append("menuentry 'VIFG' {")
    lines.append("    echo 'VIFG - Virtual ISO for GRUB'")
    lines.append("}")
    # ISO submenu
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


def save_grub_script(content):
    """Save the generated GRUB script."""

    try:
        GRUB_SCRIPT.parent.mkdir(parents=True, exist_ok=True)

        with GRUB_SCRIPT.open("w", encoding="utf-8") as file:
            file.write(content)

        GRUB_SCRIPT.chmod(0o755)

        return True

    except PermissionError:
        print("[X] Sem permissões para escrever:")
        print(f"    {GRUB_SCRIPT}")
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
