# macOS Launcher

## Quick Start

1. Install Python 3.8+ (recommended: official installer from `python.org`, which includes Tkinter).
2. Make the launcher executable:
   - `chmod +x MacOS/Run_Chat_Splitter.command`
3. Launch the GUI:
   - Double‑click `MacOS/Run_Chat_Splitter.command`, or
   - Drag your `chat.html` onto it to prefill the path.
4. Gatekeeper may block first run. Control‑click the file, choose **Open**, then **Open** again.

The GUI lets you choose the exported `chat.html` and an output folder.

## CLI Alternative

From the project root:

```bash
python3 chat_extractor.py /path/to/chat.html /path/to/output
```

Use `--quiet` to suppress progress messages.


