"""
VIFG - Virtual ISO for GRUB

GRUB script generator.

Esta versão apenas gera o ficheiro 40_vifg.
Não executa update-grub.
"""

from pathlib import Path

from config import GRUB_SCRIPT
from iso_manager import list_isos


# ==========================================
# Cabeçalho
# ==========================================

HEADER = """#!/bin/sh
exec tail -n +3 $0

# ==========================================
# VIFG - Virtual ISO for GRUB
# Generated automatically
# ==========================================

"""


# ==========================================
# Gerar menu
# ==========================================

def generate_grub_script():
    """Generate the VIFG GRUB script."""

    isos = list_isos()

    lines = [HEADER]

    lines.append("menuentry 'VIFG' {")

    lines.append("    echo 'VIFG - Virtual ISO for GRUB'")
    lines.append("}")

    lines.append("")

    # Submenu
    lines.append("submenu 'VIFG ISOs' {")

    if not isos:
        lines.append("    menuentry 'Nenhuma ISO encontrada' {")
        lines.append("        echo 'Nenhuma ISO foi adicionada ao VIFG.'")
        lines.append("    }")
    else:
        for iso in isos:
            name = iso.name

            lines.append(f"    menuentry '{name}' {{")
            lines.append(f"        echo 'ISO selecionada: {name}'")
            lines.append("    }")

    lines.append("}")

    return "\n".join(lines) + "\n"


# ==========================================
# Guardar ficheiro
# ==========================================

def save_grub_script(content):
    """Save the generated GRUB script."""

    try:
        GRUB_SCRIPT.parent.mkdir(parents=True, exist_ok=True)

        with GRUB_SCRIPT.open("w", encoding="utf-8") as file:
            file.write(content)

        # Tornar o script executável
        GRUB_SCRIPT.chmod(0o755)

        return True

    except PermissionError:
        print("[X] Sem permissões para escrever:")
        print(f"    {GRUB_SCRIPT}")
        print()
        print("Este ficheiro normalmente requer permissões de administrador.")
        return False

    except OSError as error:
        print(f"[X] Erro ao guardar o script: {error}")
        return False


# ==========================================
# Função principal
# ==========================================

def generate_and_save():
    """Generate and save the VIFG GRUB script."""

    print()
    print("[+] A gerar configuração do VIFG...")

    content = generate_grub_script()

    print()
    print("---------- CONFIGURAÇÃO GERADA ----------")
    print(content, end="")
    print("-----------------------------------------")
    print()

    return save_grub_script(content)


# ==========================================
# Teste
# ==========================================

if __name__ == "__main__":
    generate_and_save()
