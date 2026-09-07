```python
#!/usr/bin/env python3

"""
VIFG - Virtual ISO for GRUB

Main application entry point.
"""

import os
import platform
import sys


# ==========================================
# VIFG
# ==========================================

VERSION = "0.1.0"
NAME = "VIFG"
DESCRIPTION = "Virtual ISO for GRUB"


def print_header():
    """Display the VIFG header."""

    print()
    print("=" * 42)
    print("                 VIFG")
    print("        Virtual ISO for GRUB")
    print("=" * 42)
    print()


def check_system():
    """Check whether VIFG is running on Linux."""

    if platform.system() != "Linux":
        print("[X] O VIFG só pode ser executado no Linux.")
        return False

    return True


def check_python():
    """Check the Python version."""

    if sys.version_info < (3, 8):
        print("[X] O VIFG requer Python 3.8 ou superior.")
        print(
            f"[!] Versão atual: "
            f"{sys.version_info.major}.{sys.version_info.minor}"
        )
        return False

    return True


def show_system_info():
    """Display basic system information."""

    print("[+] Informações do sistema")
    print()
    print(f"    Sistema:      {platform.system()}")
    print(f"    Distribuição: Linux")
    print(f"    Arquitetura:  {platform.machine()}")
    print(f"    Python:       {platform.python_version()}")
    print()


def main():
    """Start VIFG."""

    print_header()

    # Check operating system
    if not check_system():
        sys.exit(1)

    # Check Python
    if not check_python():
        sys.exit(1)

    print("[✓] Sistema compatível.")
    print("[✓] Python compatível.")
    print()

    show_system_info()

    print("[✓] VIFG iniciado com sucesso!")
    print()
    print("🚧 O VIFG ainda está em desenvolvimento.")
    print("   Funcionalidades de ISO e GRUB serão adicionadas")
    print("   nas próximas versões.")
    print()


# ==========================================
# Entry point
# ==========================================

if __name__ == "__main__":
    main()
```
