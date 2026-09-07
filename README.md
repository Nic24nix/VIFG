# 🚀 VIFG — Virtual ISO for GRUB

**Boot ISO files directly from GRUB.**

VIFG (**Virtual ISO for GRUB**) is a Linux tool designed to make booting ISO files from the GRUB bootloader easier.

Instead of creating a bootable USB every time you want to test or use an ISO, VIFG allows you to add ISO files to your system and access them through a dedicated **VIFG** menu in GRUB.

> 🐧 Built for Linux users who like having control over their system.

---

## ✨ Features

* 📀 Add ISO files to VIFG
* 🗂️ Manage multiple ISOs
* 🥾 Boot ISOs directly from GRUB
* 📋 Dedicated `VIFG` GRUB menu
* ⏱️ Configure the GRUB timeout
* 🔄 Automatically update GRUB configuration
* 🐧 Designed for Linux
* 🛠️ Built with Python

---

## 🧠 How it works

VIFG stores the ISO files in a dedicated directory:

```text
/boot/vifg/
```

It then integrates with GRUB by creating a dedicated menu:

```text
GRUB
│
├── Linux
├── Advanced options
└── VIFG
    ├── Ubuntu ISO
    ├── Arch Linux ISO
    └── Other ISO
```

When an ISO is selected, VIFG configures GRUB to boot it.

---

## 🖥️ Supported systems

VIFG is primarily designed for Linux systems using **GRUB**.

### Currently targeted

* 🟢 Ubuntu
* 🟢 Zorin OS
* 🟢 Debian
* 🟢 Linux Mint
* 🟢 Arch Linux
* 🟢 Manjaro
* 🟢 EndeavourOS

Support for other distributions may be added in the future.

> VIFG compatibility can depend on the ISO itself and how that distribution supports booting from an ISO.

---

## 📦 Installation

VIFG is installed through the separate **VIFG Installer** project.

After installation, the application can be launched with:

```bash
vifg
```

---

## 📁 Project structure

The project is being developed with a modular structure:

```text
VIFG/
├── vifg.py
├── gui.py
├── grub.py
├── iso_manager.py
├── config.py
└── README.md
```

### Modules

| File             | Purpose             |
| ---------------- | ------------------- |
| `vifg.py`        | Main application    |
| `gui.py`         | Graphical interface |
| `grub.py`        | GRUB integration    |
| `iso_manager.py` | ISO management      |
| `config.py`      | Configuration       |

---

## 🛣️ Roadmap

### VIFG 0.1

* [ ] Basic application
* [ ] ISO selection
* [ ] ISO storage
* [ ] Basic GRUB integration

### VIFG 0.2

* [ ] Graphical interface
* [ ] Multiple ISO support
* [ ] ISO management
* [ ] GRUB VIFG submenu

### VIFG 0.3

* [ ] Automatic ISO detection
* [ ] Better compatibility
* [ ] GRUB timeout configuration
* [ ] Reboot option

### Future

* [ ] More Linux distributions
* [ ] Windows ISO support
* [ ] Automatic boot configuration
* [ ] ISO verification
* [ ] ISO removal through the GUI
* [ ] Improved error handling
* [ ] More advanced GRUB configuration

---

## ⚠️ Important

VIFG modifies the system's **GRUB configuration**.

Incorrect GRUB configuration can prevent a system from booting correctly.

VIFG is therefore being designed to:

* Validate configurations before applying them
* Avoid directly editing `grub.cfg`
* Use the appropriate GRUB configuration mechanisms
* Provide clear error messages
* Keep ISO files separate from system files

**Always keep a recovery method available when testing bootloader-related software.**

---

## 🧪 Development

VIFG is currently under active development.

The project is experimental, and some ISO types may not work yet.

Contributions, bug reports and suggestions are welcome.

---

## 📜 License

VIFG is released under the **MIT License**.

---

## 💡 Why VIFG?

USB sticks are great.

But sometimes you just want:

```text
Download ISO
      ↓
Add to VIFG
      ↓
Reboot
      ↓
GRUB
      ↓
VIFG
      ↓
Select ISO
      ↓
🥾 Boot
```

**No USB required.**

---

# 🚀 VIFG

### Virtual ISO for GRUB

**Boot ISOs. Directly. From GRUB.**
