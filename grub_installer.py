"""
VIFG - Virtual ISO for GRUB

Safe GRUB installation.
"""

import shutil
import subprocess
from datetime import datetime
from pathlib import Path

from config import GRUB_CFG, GRUB_SCRIPT


def backup_file(path):
    path = Path(path)

    if not path.is_file():
        return None

    timestamp = datetime.now().strftime(
        "%Y%m%d-%H%M%S"
    )

    backup = Path(
        f"{path}.vifg-backup-{timestamp}"
    )

    try:
        shutil.copy2(path, backup)

        print(
            f"[✓] Backup criado: {backup}"
        )

        return backup

    except OSError as error:
        print(
            f"[X] Não foi possível criar backup: "
            f"{error}"
        )

        return None


def validate_grub_script(script):
    checker = shutil.which("grub-script-check")

    if checker is None:
        print(
            "[!] grub-script-check não encontrado."
        )

        return True

    result = subprocess.run(
        [checker, str(script)],
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:

        print("[X] O script GRUB falhou na validação.")

        if result.stderr:
            print(result.stderr)

        return False

    print("[✓] Script GRUB válido.")
    return True


def install_grub_script(content):
    destination = GRUB_SCRIPT

    try:

        if destination.exists():
            backup_file(destination)

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
            f"[✓] Script instalado em "
            f"{destination}"
        )

        return True

    except PermissionError:
        print(
            "[X] Sem permissões para instalar "
            "o script GRUB."
        )

        return False

    except OSError as error:
        print(
            f"[X] Erro ao instalar script: "
            f"{error}"
        )

        return False


def regenerate_grub():
    """
    Regenerate grub.cfg using the distro's tool.
    """

    update_grub = shutil.which("update-grub")
    grub_mkconfig = shutil.which("grub-mkconfig")

    if update_grub:

        command = [update_grub]

    elif grub_mkconfig:

        command = [
            grub_mkconfig,
            "-o",
            str(GRUB_CFG),
        ]

    else:

        print(
            "[X] Nem update-grub nem "
            "grub-mkconfig foram encontrados."
        )

        return False

    print()
    print("[+] A regenerar o GRUB...")

    result = subprocess.run(
        command,
        text=True,
        check=False,
    )

    if result.returncode != 0:

        print(
            "[X] A regeneração do GRUB falhou."
        )

        return False

    print("[✓] GRUB regenerado com sucesso.")

    return True


def install_and_regenerate(content):
    """
    Full safe installation.
    """

    if not install_grub_script(content):
        return False

    if not validate_grub_script(GRUB_SCRIPT):
        return False

    if GRUB_CFG.exists():
        print()
        print("[+] A criar backup do grub.cfg...")

        if backup_file(GRUB_CFG) is None:
            print(
                "[X] Backup do grub.cfg falhou."
            )

            return False

    return regenerate_grub()
