import threading
import tkinter as tk
from tkinter import ttk

from capture import run_capture
from window_selector import get_open_windows


class GameTranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Translator")
        self.root.geometry("520x390")
        self.root.resizable(False, False)

        self.windows = []

        self.stop_event = threading.Event()
        self.capture_thread = None

        self.create_ui()
        self.refresh_windows()

    def create_ui(self):
        # Title
        title = ttk.Label(
            self.root,
            text="GAME TRANSLATOR",
            font=("Segoe UI", 20, "bold"),
        )
        title.pack(pady=(25, 5))

        subtitle = ttk.Label(
            self.root,
            text="Real-time game translation",
            font=("Segoe UI", 10),
        )
        subtitle.pack(pady=(0, 25))

        # Window selection
        frame = ttk.Frame(self.root)
        frame.pack(fill="x", padx=40)

        ttk.Label(
            frame,
            text="Game / Window",
        ).pack(anchor="w")

        self.window_combo = ttk.Combobox(
            frame,
            state="readonly",
            width=50,
        )
        self.window_combo.pack(fill="x", pady=(5, 8))

        ttk.Button(
            frame,
            text="Refresh Windows",
            command=self.refresh_windows,
        ).pack(anchor="e")

        # Languages
        language_frame = ttk.Frame(self.root)
        language_frame.pack(pady=25)

        self.source_language = ttk.Combobox(
            language_frame,
            values=["English"],
            state="readonly",
            width=15,
        )
        self.source_language.set("English")
        self.source_language.grid(row=0, column=0)

        ttk.Label(
            language_frame,
            text="  →  ",
            font=("Segoe UI", 14),
        ).grid(row=0, column=1)

        self.target_language = ttk.Combobox(
            language_frame,
            values=["Turkish"],
            state="readonly",
            width=15,
        )
        self.target_language.set("Turkish")
        self.target_language.grid(row=0, column=2)

        # Start button
        self.start_button = ttk.Button(
            self.root,
            text="Start Translation",
            command=self.start_translation,
        )
        self.start_button.pack(pady=(5, 5))

        # Stop button
        self.stop_button = ttk.Button(
            self.root,
            text="Stop Translation",
            command=self.stop_translation,
            state="disabled",
        )
        self.stop_button.pack(pady=5)

        # Status
        self.status = ttk.Label(
            self.root,
            text="Status: Ready",
        )
        self.status.pack(pady=15)

    def refresh_windows(self):
        self.windows = get_open_windows()

        titles = [
            window["title"]
            for window in self.windows
        ]

        self.window_combo["values"] = titles

        if titles:
            self.window_combo.current(0)
            self.status.config(
                text=f"Status: Found {len(titles)} windows"
            )
        else:
            self.window_combo.set("")
            self.status.config(
                text="Status: No windows found"
            )

    def start_translation(self):
        index = self.window_combo.current()

        if index == -1:
            self.status.config(
                text="Status: Select a window first"
            )
            return

        # Prevent starting another capture thread
        if self.capture_thread and self.capture_thread.is_alive():
            return

        selected = self.windows[index]

        print("Starting capture...")
        print("Title:", selected["title"])
        print("HWND:", selected["hwnd"])

        self.stop_event.clear()

        self.capture_thread = threading.Thread(
            target=run_capture,
            args=(
                selected["hwnd"],
                self.stop_event,
            ),
            daemon=True,
        )

        self.capture_thread.start()

        self.start_button.config(
            state="disabled"
        )

        self.stop_button.config(
            state="normal"
        )

        self.status.config(
            text=f"Running: {selected['title']}"
        )

    def stop_translation(self):
        self.stop_event.set()

        self.start_button.config(
            state="normal"
        )

        self.stop_button.config(
            state="disabled"
        )

        self.status.config(
            text="Status: Stopped"
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = GameTranslatorApp(root)
    root.mainloop()