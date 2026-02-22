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


class ChannelSelector(tk.Toplevel):
    def __init__(self, parent, path_icon_file, entries):
        super().__init__(parent)
        self.title("Select Channel to Keep")
        self.entries = entries
        self.selected = None
        self.path_icon_file = path_icon_file

        # Window icon
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
            "The CS7000 does not allow writing duplicate channel definitions "
            "to the codeplug. Your configuration contains channels with identical "
            "settings.\n\n"
            "You must choose the Channel entry to keep. Your configuration will be "
            "updated to use this channel and the duplicate entries will be deleted. "
            "If you cancel, the first row will be selected.\n\n"
            "You must make a selection in order to proceed."
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
            # Adjust display format depending on your channel row structure
            # Example: entry = [rowId, name, rxFreq, txFreq, slot, cc]
            try:
                bw = str(entry[3])
                if ( (bw == "12.5") or (bw == "25.0")):
                    display = (
                            f"Row: {entry[0]} => Ch: {entry[1]} — RX:{entry[11]} TX:{entry[18]} "
                        f"BW:{entry[3]}"
                    )
                else:
                    display = (
                            f"Row: {entry[0]} => Ch: {entry[1]} — RX:{entry[11]} TX:{entry[17]} "
                        f"ID: {entry[19]} Slot:{entry[4]} CC:{entry[3]}"
                    )
            except Exception:
                # Fallback if structure differs
                display = str(entry)

            self.listbox.insert(tk.END, display)

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
            Messagebox.show_warning("Please select a Channel.", "No Selection")
            return
        self.selected = self.entries[idx[0]]
        self.destroy()

    def on_cancel(self):
        # Default to first entry
        self.selected = self.entries[0]
        self.destroy()

