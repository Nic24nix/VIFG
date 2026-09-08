#!/usr/bin/env python3

"""
VIFG - Virtual ISO for GRUB

Main application.
"""

import os
import platform
import subprocess
import sys
from pathlib import Path

from config import APP_NAME, APP_VERSION
from grub import get_grub_info
from grub_generator import generate_grub_script
from grub_installer import install_and_regenerate
from iso_inspector import inspect_iso
from iso_manager import add_iso


def print_header():
    print()
    print("=" * 48)
    print("                 VIFG")
    print("          Virtual ISO for GRUB")
    print("=" * 48)
    print()


def require_linux():
    if platform.system() != "Linux":

        print(
            "[X] O VIFG só funciona no Linux."
        )

        return False

    return True


def require_root():
    if os.geteuid() != 0:

        print(
            "[X] O VIFG precisa de permissões "
            "de administrador."
        )

        print()
        print(
            "Execute novamente com:"
        )

        print(
            "    sudo vifg"
        )

        return False

    return True


def check_python():
    if sys.version_info < (3, 8):

        print(
            "[X] O VIFG requer Python 3.8+."
        )

        return False

    return True


def choose_iso():
    """
    Try to open a graphical file chooser.
    """

    try:

        import tkinter as tk
        from tkinter import filedialog

        root = tk.Tk()
        root.withdraw()

        path = filedialog.askopenfilename(
            title="Escolher ISO para o VIFG",
            filetypes=[
                ("Imagens ISO", "*.iso"),
                ("Todos os ficheiros", "*.*"),
            ],
        )

        root.destroy()

        if path:
            return Path(path)

    except Exception:
        pass

    print()
    print(
        "Introduza o caminho da ISO:"
    )

    path = input("> ").strip()

    if not path:
        return None

    return Path(path)


def show_iso_info(iso):
    info = inspect_iso(iso)

    print()
    print("=" * 48)
    print("             ISO DETETADA")
    print("=" * 48)
    print()

    print(f"Nome:    {iso.name}")

    print(
        f"Kernel:  "
        f"{info['kernel'] or 'não encontrado'}"
    )

    print(
        f"Initrd:  "
        f"{info['initrd'] or 'não encontrado'}"
    )

    print(
        f"Windows: "
        f"{info['boot_wim'] or 'não encontrado'}"
    )

    print()


def configure_timeout():
    print()
    answer = input(
        "Deseja definir o timeout do GRUB para "
        "5 segundos? [S/n]: "
    ).strip().lower()

    if answer not in ("", "s", "sim", "y", "yes"):
        return True

    grub_file = Path("/etc/default/grub")

    if not grub_file.is_file():

        print(
            "[!] /etc/default/grub não encontrado."
        )

        return False

    try:

        lines = grub_file.read_text(
            encoding="utf-8"
        ).splitlines()

        found = False
        new_lines = []

        for line in lines:

            if line.startswith("GRUB_TIMEOUT="):

                new_lines.append(
                    "GRUB_TIMEOUT=5"
                )

                found = True

            else:

                new_lines.append(line)

        if not found:

            new_lines.append(
                "GRUB_TIMEOUT=5"
            )

        grub_file.write_text(
            "\n".join(new_lines) + "\n",
            encoding="utf-8",
        )

        print(
            "[✓] Timeout definido para 5 segundos."
        )

        return True

    except OSError as error:

        print(
            f"[X] Erro ao alterar timeout: "
            f"{error}"
        )

        return False


def ask_reboot():
    print()

    answer = input(
        "Deseja reiniciar agora? [s/N]: "
    ).strip().lower()

    if answer not in ("s", "sim", "y", "yes"):
        return

    print()
    print("[+] A reiniciar...")

    subprocess.run(
        ["reboot"],
        check=False,
    )


def install_iso(iso):
    print()
    print("[+] A verificar GRUB...")

    grub_info = get_grub_info()

    if not grub_info["grub_installed"]:

        print(
            "[X] GRUB não foi encontrado."
        )

        return False

    if not grub_info["grub_tools"]:

        print(
            "[X] Ferramentas do GRUB não encontradas."
        )

        return False

    show_iso_info(iso)

    print(
        "[+] A adicionar ISO ao VIFG..."
    )

    if not add_iso(iso):
        return False

    print()
    print(
        "[+] A gerar configuração VIFG..."
    )

    script = generate_grub_script()

    print(
        "[✓] Configuração gerada."
    )

    print()
    print(
        "[+] A instalar configuração GRUB..."
    )

    if not install_and_regenerate(script):
        print()
        print(
            "[X] A instalação do VIFG falhou."
        )

        return False

    if not configure_timeout():
        print(
            "[!] Timeout não foi alterado."
        )

    print()
    print("=" * 48)
    print("          VIFG INSTALADO COM SUCESSO")
    print("=" * 48)
    print()

    print(
        "A ISO estará disponível no GRUB em:"
    )

    print(
        "    VIFG → VIFG ISOs"
    )

    return True


def main():
    print_header()

    if not require_linux():
        return 1

    if not check_python():
        return 1

    if not require_root():
        return 1

    print(
        f"VIFG {APP_VERSION}"
    )

    print()

    iso = None

    if len(sys.argv) > 1:
        iso = Path(sys.argv[1])

    else:
        iso = choose_iso()

    if iso is None:

        print(
            "[!] Nenhuma ISO selecionada."
        )

        return 0

    if not iso.is_file():

        print(
            f"[X] Ficheiro não encontrado:"
            f" {iso}"
        )

        return 1

    if iso.suffix.lower() != ".iso":

        print(
            "[X] O ficheiro selecionado "
            "não é uma ISO."
        )

        return 1

    success = install_iso(iso)

    if success:
        ask_reboot()
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
