"""
VIFG - Virtual ISO for GRUB

Central configuration for the VIFG application.
"""

from pathlib import Path


# ==========================================
# Application
# ==========================================

APP_NAME = "VIFG"
APP_VERSION = "0.1.0"
APP_DESCRIPTION = "Virtual ISO for GRUB"


# ==========================================
# Directories
# ==========================================

# Where VIFG stores ISO files
ISO_DIR = Path("/boot/vifg")
TEST_ISO_DIR = Path("/tmp/vifg-test")

# Main VIFG installation directory
VIFG_DIR = Path("/opt/vifg")


# ==========================================
# GRUB
# ==========================================

# VIFG's GRUB script
GRUB_SCRIPT = Path("/etc/grub.d/40_vifg")


# ==========================================
# Limits
# ==========================================

# Maximum number of ISOs VIFG should display
# This is only a UI limit for now.
MAX_ISOS = 100


# ==========================================
# Helper functions
# ==========================================

def get_iso_directory() -> Path:
    """Return the directory where VIFG stores ISO files."""
    return ISO_DIR


def get_vifg_directory() -> Path:
    """Return the VIFG installation directory."""
    return VIFG_DIR


def get_grub_script() -> Path:
    """Return the VIFG GRUB script path."""
    return GRUB_SCRIPT
