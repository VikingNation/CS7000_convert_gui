import os
import sys
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox

def resource_path(filename):
    """Return absolute path to resource, works for dev and PyInstaller EXE."""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(os.path.abspath("."), filename)



class ContactSelector(tk.Toplevel):
    def __init__(self, parent, path_icon_file, entries):
        super().__init__(parent)
        self.title("Select Contact to Keep")
        self.entries = entries
        self.selected = None
        self.path_icon_file = path_icon_file
        self.iconphoto(False, tk.PhotoImage(file=resource_path(self.path_icon_file)))
        # Modal behavior
        self.transient(parent)
        self.grab_set()

        # Layout
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        frame = ttk.Frame(self, padding=10)
        frame.grid(sticky="nsew")
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)

        # Explanatory text
        explanation = (
            "The CS7000 does not allow writing duplicate IDs (Talkgroups/DMR-IDs) "
            "to the Contacts database. Your codeplug contains duplicate IDs.\n\n"
            "You must choose the Contact name to use. Your channel configuration "
            "will be updated to use this name and the duplicate entires will be."
            "deleted. If you cancel the first row will be selected."
            "\n\nYou must make a selection in order to proceed."
        )

        msg = ttk.Label(
            frame,
            text=explanation,
            wraplength=450,
            justify="left",
            padding=(0, 0, 0, 10)
        )
        msg.grid(row=0, column=0, columnspan=2, sticky="w")

        # Scrollable listbox
        self.listbox = tk.Listbox(frame, height=12)
        self.listbox.grid(row=1, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.listbox.yview)
        scrollbar.grid(row=1, column=1, sticky="ns")
        self.listbox.config(yscrollcommand=scrollbar.set)

        # Populate listbox
        for entry in entries:
            # Adjust display format as needed
            self.listbox.insert(tk.END, f"{entry[2]} — ID: {entry[1]}")

        # Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=(10, 0))

        ttk.Button(btn_frame, text="Select", command=self.on_select).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.on_cancel).grid(row=0, column=1, padx=5)

        # Double-click to select
        self.listbox.bind("<Double-1>", lambda e: self.on_select())

        # Center on parent
        self.update_idletasks()
        x = parent.winfo_rootx() + (parent.winfo_width() // 2) - (self.winfo_width() // 2)
        y = parent.winfo_rooty() + (parent.winfo_height() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")

    def on_select(self):
        idx = self.listbox.curselection()
        if not idx:
            Messagebox.show_warning("Please select a Contact.", "No Selection")
            return
        self.selected = self.entries[idx[0]]
        self.destroy()

    def on_cancel(self):
        self.selected = self.entries[0]
        self.destroy()

