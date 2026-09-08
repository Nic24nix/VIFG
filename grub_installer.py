```python
"""
VIFG - Virtual ISO for GRUB

Safe GRUB script installation module.
"""

import shutil
from pathlib import Path


def backup_file(path):
    """Create a backup of an existing file."""

    path = Path(path)

    if not path.is_file():
        return None

    backup = path.with_suffix(path.suffix + ".backup")

    try:
        shutil.copy2(path, backup)
        print(f"[✓] Backup criado: {backup}")
        return backup
    except OSError as error:
        print(f"[X] Erro ao criar backup: {error}")
        return None


def install_grub_script(content, destination):
    """
    Safely install a generated GRUB script.

    The destination is supplied explicitly so tests can use /tmp.
    """

    destination = Path(destination)

    try:
        destination.parent.mkdir(parents=True, exist_ok=True)

        # Backup existing script before replacing it.
        if destination.exists():
            backup = backup_file(destination)

            if backup is None:
                print("[X] Não foi possível criar o backup.")
                return False

        # Write the new script.
        with destination.open("w", encoding="utf-8") as file:
            file.write(content)

        # GRUB scripts must be executable.
        destination.chmod(0o755)

        print(f"[✓] Script instalado em: {destination}")
        return True

    except PermissionError:
        print(f"[X] Sem permissões para escrever: {destination}")
        return False

    except OSError as error:
        print(f"[X] Erro ao instalar o script: {error}")
        return False
```
