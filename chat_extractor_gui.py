"""
A tiny GUI for splitting an exported ChatGPT chats HTML file into one HTML per conversation.

Usage:
- Run this file directly, or double‑click the provided Run_Chat_Splitter.bat on Windows.
- Choose the exported chats HTML (usually named chat.html) and an output folder.

No external dependencies; uses the existing split_chat_html function.
"""

import os
import sys
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

try:
    # Import the core splitter from the CLI module
    from chat_extractor import split_chat_html
    from claude_chat_extractor import extract_claude_chats
except Exception as import_error:
    split_chat_html = None
    extract_claude_chats = None
    _IMPORT_ERROR = import_error
else:
    _IMPORT_ERROR = None


class ChatExtractorGUI:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Chat Export Splitter")
        self.root.resizable(False, False)

        # Variables
        self.input_path_var = tk.StringVar()
        self.output_dir_var = tk.StringVar()

        # Prefill from argv if present (drag-and-drop onto .bat passes path as argv[1])
        if len(sys.argv) >= 2:
            candidate = Path(sys.argv[1]).expanduser()
            if candidate.exists() and candidate.is_file():
                self.input_path_var.set(str(candidate))

        # Layout
        main = tk.Frame(self.root, padx=12, pady=12)
        main.grid(row=0, column=0, sticky="nsew")

        # Platform selection
        tk.Label(main, text="Select Platform exporter:").grid(row=0, column=0, sticky="w")
        self.platform_var = tk.StringVar(value="ChatGPT")
        platform_menu = tk.OptionMenu(main, self.platform_var, "ChatGPT", "Claude")
        platform_menu.grid(row=0, column=1, columnspan=2, sticky="we")

        # Input file row
        tk.Label(main, text="Exported chats file:").grid(row=1, column=0, sticky="w")
        input_entry = tk.Entry(main, textvariable=self.input_path_var, width=50)
        input_entry.grid(row=2, column=0, sticky="we", padx=(0, 8))
        tk.Button(main, text="Browse...", command=self.browse_input).grid(row=2, column=1, sticky="we")

        # Output dir row
        tk.Label(main, text="Output folder:").grid(row=3, column=0, sticky="w", pady=(10, 0))
        output_entry = tk.Entry(main, textvariable=self.output_dir_var, width=50)
        output_entry.grid(row=4, column=0, sticky="we", padx=(0, 8))
        tk.Button(main, text="Select...", command=self.browse_output).grid(row=4, column=1, sticky="we")

        # Actions
        button_row = tk.Frame(main)
        button_row.grid(row=5, column=0, columnspan=2, sticky="e", pady=(14, 0))
        self.run_button = tk.Button(button_row, text="Run Extractor", command=self.run_extractor)
        self.run_button.grid(row=0, column=0, padx=(0, 8))
        tk.Button(button_row, text="Quit", command=self.quit_app).grid(row=0, column=1)

        # Status
        self.status_var = tk.StringVar(value="Idle")
        status = tk.Label(main, textvariable=self.status_var, anchor="w")
        status.grid(row=6, column=0, columnspan=2, sticky="we", pady=(10, 0))

        # Resize config
        main.columnconfigure(0, weight=1)

        # If import failed, surface immediately
        if _IMPORT_ERROR is not None:
            messagebox.showerror(
                "Import error",
                f"Could not import splitter: {_IMPORT_ERROR}\n\n"
                "Make sure chat_extractor.py is in the same folder and Python 3.8+ is installed.")

    def browse_input(self) -> None:
        platform = self.platform_var.get()
        if platform == "ChatGPT":
            filetypes = [("HTML files", "*.html"), ("All files", "*.*")]
            title = "Select exported chats HTML"
        elif platform == "Claude":
            filetypes = [("JSON files", "*.json"), ("All files", "*.*")]
            title = "Select Claude conversations.json"
        else:
            filetypes = [("All files", "*.*")]
            title = "Select file"

        initial_dir = None
        if self.input_path_var.get():
            try:
                initial_dir = str(Path(self.input_path_var.get()).expanduser().resolve().parent)
            except Exception:
                initial_dir = None
        filename = filedialog.askopenfilename(
            title=title,
            filetypes=filetypes,
            initialdir=initial_dir or os.getcwd(),
        )
        if filename:
            self.input_path_var.set(filename)
            # Offer a default output dir next to input
            if not self.output_dir_var.get():
                if platform == "ChatGPT":
                    default_out = str(Path(filename).parent / "split_chats")
                elif platform == "Claude":
                    default_out = str(Path(filename).parent / "claude_chats")
                else:
                    default_out = str(Path(filename).parent / "output")
                self.output_dir_var.set(default_out)

    def browse_output(self) -> None:
        initial_dir = None
        if self.output_dir_var.get():
            try:
                initial_dir = str(Path(self.output_dir_var.get()).expanduser().resolve())
            except Exception:
                initial_dir = None
        dirname = filedialog.askdirectory(title="Choose output folder", initialdir=initial_dir or os.getcwd())
        if dirname:
            self.output_dir_var.set(dirname)

    def quit_app(self) -> None:
        self.root.destroy()
        sys.exit(0)

    def run_extractor(self) -> None:
        platform = self.platform_var.get()
        if platform == "ChatGPT":
            self.run_split()
        elif platform == "Claude":
            self.run_split_claude()

    def run_split(self) -> None:
        if split_chat_html is None:
            messagebox.showerror("Unavailable", "Splitter function not available.")
            return

        input_path = self.input_path_var.get().strip()
        output_dir = self.output_dir_var.get().strip()

        if not input_path:
            messagebox.showwarning("Missing file", "Please select the exported chats HTML file.")
            return
        if not Path(input_path).exists():
            messagebox.showerror("Not found", f"Input file does not exist:\n{input_path}")
            return

        if not output_dir:
            # Default next to input
            output_dir = str(Path(input_path).parent / "split_chats")
            self.output_dir_var.set(output_dir)

        self.run_button.config(state=tk.DISABLED)
        self.status_var.set("Processing...")
        self.root.update_idletasks()

        try:
            if not input_path.endswith(".html"):
                raise ValueError("Invalid file type for ChatGPT. Please select an HTML file.")
            ok = split_chat_html(input_path, output_dir, verbose=True)
        except Exception as e:
            self.status_var.set("Error")
            messagebox.showerror("Error", f"An error occurred while splitting:\n{e}")
        else:
            self.status_var.set("Done" if ok else "Completed with errors")
            if ok:
                messagebox.showinfo(
                    "Finished",
                    f"Chats split successfully into:\n{output_dir}")
            else:
                messagebox.showwarning(
                    "Finished with errors",
                    f"Some chats may not have been written. See console for details.\nOutput folder:\n{output_dir}")
        finally:
            self.run_button.config(state=tk.NORMAL)



    def run_split_claude(self) -> None:
        if extract_claude_chats is None:
            messagebox.showerror("Unavailable", "Claude splitter function not available.")
            return

        input_path = self.input_path_var.get().strip()
        output_dir = self.output_dir_var.get().strip()

        if not input_path:
            messagebox.showwarning("Missing file", "Please select the conversations.json file.")
            return
        if not Path(input_path).exists():
            messagebox.showerror("Not found", f"Input file does not exist:\n{input_path}")
            return

        if not output_dir:
            # Default next to input
            output_dir = str(Path(input_path).parent / "claude_chats")
            self.output_dir_var.set(output_dir)

        self.run_button.config(state=tk.DISABLED)
        self.status_var.set("Processing Claude chats...")
        self.root.update_idletasks()

        try:
            if not input_path.endswith(".json"):
                raise ValueError("Invalid file type for Claude. Please select a JSON file.")
            ok = extract_claude_chats(input_path, output_dir, verbose=True)
        except Exception as e:
            self.status_var.set("Error")
            messagebox.showerror("Error", f"An error occurred while splitting:\n{e}")
        else:
            self.status_var.set("Done" if ok else "Completed with errors")
            if ok:
                messagebox.showinfo(
                    "Finished",
                    f"Claude chats split successfully into:\n{output_dir}")
            else:
                messagebox.showwarning(
                    "Finished with errors",
                    f"Some Claude chats may not have been written. See console for details.\nOutput folder:\n{output_dir}")
        finally:
            self.run_button.config(state=tk.NORMAL)


def main() -> None:
    root = tk.Tk()
    app = ChatExtractorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()