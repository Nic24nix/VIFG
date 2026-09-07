"""
VIFG - Virtual ISO for GRUB

GRUB detection and information module.

Esta versão é apenas de diagnóstico.
Não modifica o GRUB.
"""

import shutil
from pathlib import Path

from config import GRUB_SCRIPT


# ==========================================
# Caminhos do GRUB
# ==========================================

GRUB_CONFIG = Path("/etc/default/grub")
GRUB_DIR = Path("/etc/grub.d")
UPDATE_GRUB = shutil.which("update-grub")


# ==========================================
# Deteção
# ==========================================

def grub_installed():
    """Check whether the GRUB configuration directory exists."""

    return GRUB_DIR.is_dir()


def grub_config_exists():
    """Check whether /etc/default/grub exists."""

    return GRUB_CONFIG.is_file()


def update_grub_available():
    """Check whether update-grub is available."""

    return UPDATE_GRUB is not None


def vifg_script_exists():
    """Check whether VIFG's GRUB script already exists."""

    return GRUB_SCRIPT.is_file()


# ==========================================
# GRUB Timeout
# ==========================================

def get_grub_timeout():
    """Read the current GRUB_TIMEOUT value."""

    if not grub_config_exists():
        return None

    try:
        with GRUB_CONFIG.open("r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                if line.startswith("GRUB_TIMEOUT="):
                    value = line.split("=", 1)[1].strip()

                    # Remove possible quotes
                    value = value.strip("\"'")

                    try:
                        return int(value)
                    except ValueError:
                        return value

    except PermissionError:
        print("[X] Sem permissões para ler o GRUB.")
        return None

    except OSError as error:
        print(f"[X] Erro ao ler o GRUB: {error}")
        return None

    return None


# ==========================================
# Informações
# ==========================================

def get_grub_info():
    """Return information about the GRUB installation."""

    return {
        "grub_installed": grub_installed(),
        "grub_config": grub_config_exists(),
        "update_grub": update_grub_available(),
        "vifg_script": vifg_script_exists(),
        "timeout": get_grub_timeout(),
    }


def print_grub_info():
    """Display GRUB information."""

    print()
    print("=" * 42)
    print("             GRUB STATUS")
    print("=" * 42)
    print()

    info = get_grub_info()

    if info["grub_installed"]:
        print("[✓] Diretório do GRUB encontrado.")
    else:
        print("[X] Diretório do GRUB não encontrado.")

    if info["grub_config"]:
        print("[✓] /etc/default/grub encontrado.")
    else:
        print("[X] /etc/default/grub não encontrado.")

    if info["update_grub"]:
        print("[✓] update-grub encontrado.")
    else:
        print("[X] update-grub não encontrado.")

    if info["vifg_script"]:
        print("[!] Script 40_vifg já existe.")
    else:
        print("[✓] Script 40_vifg ainda não existe.")

    timeout = info["timeout"]

    if timeout is not None:
        print(f"[+] GRUB_TIMEOUT = {timeout}")
    else:
        print("[!] GRUB_TIMEOUT não definido.")

    print()


# ==========================================
# Teste
# ==========================================

if __name__ == "__main__":
    print_grub_info()
```
