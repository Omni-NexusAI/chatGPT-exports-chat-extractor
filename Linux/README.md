# Linux Launcher

## Quick Start

1. Ensure Python 3.8+ is installed:
   - Debian/Ubuntu: `sudo apt-get update && sudo apt-get install -y python3 python3-pip`
2. Install Tkinter for your distro (required for the GUI):
   - Debian/Ubuntu: `sudo apt-get install -y python3-tk`
   - Fedora: `sudo dnf install -y python3-tkinter`
   - Arch: `sudo pacman -S tk`
3. Make the launcher executable:
   - `chmod +x Linux/run.sh`
4. Launch the GUI:
   - `./Linux/run.sh` (optionally pass `/path/to/chat.html`)

The GUI will let you browse to your exported `chat.html` and choose an output folder.

## CLI Alternative

You can always use the cross‑platform CLI from the project root:

```bash
python3 chat_extractor.py /path/to/chat.html /path/to/output
```

Use `--quiet` to suppress progress messages.


