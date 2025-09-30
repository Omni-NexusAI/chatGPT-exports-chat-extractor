# LLM Exports Chat Extractor

A simple and user-friendly utility to split exported HTML/JSON files from ChatGPT and Claude into individual files for each conversation. Perfect for organizing and managing your conversation history from multiple LLM platforms.

## ✨ Features

- **Easy-to-use GUI** (Windows/macOS/Linux via Tkinter)
- **Cross-platform CLI** for advanced users
- **Drag-and-drop support** for quick file processing
- **No external dependencies** - uses only Python's standard library
- **Smart filename handling** - automatically sanitizes and deduplicates filenames
- **Preserves original formatting** - keeps the look and feel of your ChatGPT conversations

## 🚀 Quick Start

### Option 1: Windows GUI (Recommended for most users)

1. **Install Python 3.8+** if you haven't already
   - Download from [python.org](https://www.python.org/downloads/)
   - Make sure to check "Add Python to PATH" during installation

2. **Download and extract** this repository to any folder

3. **Launch the tool**:
   - **Method A**: Double-click `Run_Chat_Splitter.bat`
   - **Method B**: Drag your chat file (`chat.html` or `conversations.json`) onto `Run_Chat_Splitter.bat`

4. **Use the GUI**:
   - Select the platform (ChatGPT or Claude) from the dropdown menu.
   - Click "Browse..." to select your exported chat file.
   - Choose your output directory.
   - Click "Run Extractor" and wait for completion.

### Option 1B: macOS GUI

1. Install Python 3.8+ (recommended from `python.org`).
2. Make the launcher executable:
   - `chmod +x MacOS/Run_Chat_Splitter.command`
3. Launch:
   - Double-click `MacOS/Run_Chat_Splitter.command`, or
   - Drag your `chat.html` onto it to prefill the path.
4. If macOS blocks the script (Gatekeeper), Control-click → Open.

### Option 1C: Linux GUI

1. Install Python 3.8+ and Tkinter (e.g., Debian/Ubuntu: `sudo apt-get install -y python3-tk`).
2. Make the launcher executable:
   - `chmod +x Linux/run.sh`
3. Launch:
   - `./Linux/run.sh` (optionally pass `/path/to/chat.html`).

### Option 2: Command Line (Cross-platform)

```bash
# Basic usage with custom input and output
python chat_extractor.py path/to/your/chat.html path/to/output/directory

# Quick usage with defaults (looks for chat.html in current directory)
python chat_extractor.py

# Silent mode (no progress messages)
python chat_extractor.py --quiet

# Get help
python chat_extractor.py --help
```

**Note**: On Windows, you can use `py` instead of `python`. On macOS/Linux, you might need `python3`.

## 📋 How to Export Your Data

### ChatGPT

1. Go to [ChatGPT Settings](https://chat.openai.com/) → Data Controls → Export
2. Request your data export
3. Download the ZIP file when ready
4. Extract the ZIP and locate the `chat.html` file

### Claude

1. Log in to your Claude account.
2. Click on your profile icon in the top right corner.
3. Select "Account Settings".
4. Click on the "Export Data" button.
5. You will receive an email with a link to download your data.
6. Download the ZIP file and extract it to find the `conversations.json` file.

## 🛠 How It Works

The tool:
1. Reads your exported `chat.html` file
2. Extracts the embedded JSON data containing all conversations
3. Creates individual HTML files for each conversation
4. Preserves the original ChatGPT styling and formatting
5. Generates clean, filesystem-friendly filenames

## 📁 File Structure

After running the tool, you'll get:
```
your-output-directory/
├── How_to_learn_Python_programming.html
├── Recipe_for_chocolate_cake.html
├── Travel_tips_for_Japan.html
└── ... (one file per conversation)
```

## 🔧 Advanced Usage

### Command Line Options

```bash
python llm_exports_chat_extractor.py [input_file] [output_dir] [--quiet]
```

- `input_file`: Path to your chat.html (default: `chat.html`)
- `output_dir`: Output directory (default: `split_chats`)
- `--quiet`: Suppress progress messages

### Examples

```bash
# Process a specific file to a custom directory
python chat_extractor.py ~/Downloads/chat.html ~/Documents/ChatGPT_Conversations

# Use current directory's chat.html, output to custom folder
python chat_extractor.py chat.html my_conversations

# Silent processing
python chat_extractor.py --quiet
```

## 💡 Tips & Best Practices

- **Large exports**: Very large chat histories may take a few minutes to process
- **File organization**: Consider creating dated folders for multiple exports
- **Backup**: Keep your original `chat.html` file as a backup
- **Portable**: You can copy this tool to any directory and run it there
- **Updates**: Check back for updates if you encounter any issues

## 🐛 Troubleshooting

### GUI won't launch
- **Check Python installation**: Run `python --version` or `py --version` in Command Prompt
- **PATH issues**: Reinstall Python and ensure "Add to PATH" is checked
- **Try CLI**: If GUI fails, try the command line version

### "Could not find jsonData" error
- **Wrong file**: Make sure you're selecting the correct `chat.html` from your ChatGPT export
- **Corrupted export**: Try re-exporting your data from ChatGPT
- **File encoding**: Ensure the file wasn't modified or corrupted during download

### Permission errors
- **Output directory**: Make sure you have write permissions to the output directory
- **Admin rights**: Try running as administrator if needed
- **Different location**: Try saving to a different directory (like Desktop)

### Performance issues
- **Large files**: Very large exports (>100MB) may take several minutes
- **Memory**: Close other applications if you're running low on RAM
- **Progress**: Remove `--quiet` flag to see progress messages

## 🤝 Contributing

Found a bug or have a suggestion? Feel free to:
- Open an issue on GitHub
- Submit a pull request
- Share your feedback

## 📄 License

This project is open source and available under the MIT License.

---

**Happy organizing! 🎉**



