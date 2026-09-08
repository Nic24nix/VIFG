"""
VIFG - Virtual ISO for GRUB

Central configuration.
"""

from pathlib import Path


APP_NAME = "VIFG"
APP_VERSION = "0.2.0"
APP_DESCRIPTION = "Virtual ISO for GRUB"

ISO_DIR = Path("/boot/vifg")
VIFG_DIR = Path("/opt/vifg")
GRUB_SCRIPT = Path("/etc/grub.d/40_vifg")
GRUB_CONFIG = Path("/etc/default/grub")
GRUB_CFG = Path("/boot/grub/grub.cfg")

MAX_ISOS = 100


def get_iso_directory():
    return ISO_DIR


def get_vifg_directory():
    return VIFG_DIR


def get_grub_script():
    return GRUB_SCRIPT


def get_grub_config():
    return GRUB_CONFIG


def get_grub_cfg():
    return GRUB_CFG
