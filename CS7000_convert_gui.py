#!/bin/env python
import os
import sys
import csv
import platform
import tkinter as tk
from tkinter import filedialog, messagebox

import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.widgets.scrolled import ScrolledText
from ttkbootstrap.dialogs import Messagebox

from connectSystems.CS7000.Constants import Const
from connectSystems.CS7000.Channels import Channels
from connectSystems.CS7000.DigitalContacts import DigitalContacts
from connectSystems.CS7000.Zones import Zones

from Deduper import Deduper
# CS7000_convert_gui.py
#
# Author: Jason Johnson <k3jsj@arrl.net>
# Purpose:  GUI to convert Anytone Talkgroups, Channels, and Zones into format for CS7000 CPS
#           Program prompts for directory of Anytone Talkgroups, Channel, and Zone files
#           Program outputs spreadsheets in format for CS7000
#
#           Portions of this source code were generated using Microsoft Co-Pilot
#           This version of the applicatation has been updated for
#           CPS verseion 1.2.19.00 Beta and CS7000 Firmware version 9.00.93

APP_VERSION = "1.3.2-beta"

# DEBUG FLAG
DEBUG = True
# Global variables
root = None
debug_output_var = None
debug_output_text = None

icon_file="K3JSJ_avatar_256_by_256.png"

# Location of stock Zones and Analog and Digital Channels CSV files that come pre-loaded with CS7000
stock_zones_file = "codeplugs\\CS7000_M17_PLUS_V9.00.93_zones.csv"
stock_analog_channel_file = "codeplugs\\CS7000_M17_PLUS_V9.00.93_analog_channels.csv"
stock_digital_channel_file = "codeplugs\\CS7000_M17_PLUS_V9.00.93_digital_channels.csv"

def resource_path(filename):
    """Return absolute path to resource, works for dev and PyInstaller EXE."""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(os.path.abspath("."), filename)

def update_debug_output(text: str):
    """
    Global debug logger.
    - Always appends to debug_output_var (StringVar).
    - If the debug ScrolledText widget exists, it is updated too.
    Safe to call before the UI is fully built.
    """
    global debug_output_var, debug_output_text

    if debug_output_var is not None:
        current = debug_output_var.get()
        if current:
            debug_output_var.set(current + "\n" + text)
        else:
            debug_output_var.set(text)

    # Only update the widget if it exists
    if debug_output_text is not None:
        debug_output_text.delete("1.0", "end")
        debug_output_text.insert("end", debug_output_var.get())
        debug_output_text.see("end")


def check_files_closed(file_list):
    """
    Checks whether each file in file_list is currently open/locked.
    Returns:
        0  if all files are closed
       -1  if one or more files are open
    """
    open_files = []

    for filename in file_list:
        if not os.path.exists(filename):
            continue

        try:
            with open(filename, "a"):
                pass
        except Exception:
            open_files.append(filename)

    if open_files:
        root.withdraw()
        msg = (
            "Cannot convert the Codeplug.\n\n"
            "The following files are open and need to be closed before you can continue:\n\n"
            + "\n".join(open_files)
        )
        messagebox.showerror("Files Are Open", msg, parent=root)
        root.deiconify()
        return -1

    return 0


def delete_file(filename):
    """
    Deletes the specified file if it exists.
    Returns:
        0  if the file was deleted
        1  if the file did not exist
       -1  if deletion failed (e.g., file is open or locked)
    """
    if not os.path.exists(filename):
        return 1

    try:
        os.remove(filename)
        return 0
    except Exception:
        return -1


def select_input_directory():
    directory = filedialog.askdirectory(
        title="Choose directory for Anytone input files",
        parent=root
    )
    if directory:
        input_directory_var.set(f"Selected directory: {directory}")
        update_debug_output("User selected input directory")


def select_output_directory():
    directory = filedialog.askdirectory(
        title="Choose directory to output CS7000 spreadsheet files",
        parent=root
    )
    if directory:
        output_directory_var.set(f"Selected directory: {directory}")
        update_debug_output("User selected output directory")


def open_file_explorer(path):
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":
        os.system(f"open '{path}'")
    elif platform.system() == "Linux":
        os.system(f"xdg-open '{path}'")
    else:
        print("Unsupported operating system")


def getDirectoryname(s):
    return s.replace("Selected directory: ", "")


def convert_codeplug():
    update_debug_output("Now converting files into format for CS7000")

    input_directory = getDirectoryname(input_directory_var.get())
    output_directory = getDirectoryname(output_directory_var.get())

    contacts_file = os.path.join(input_directory, "TalkGroups.CSV")
    channels_file = os.path.join(input_directory, "Channel.CSV")
    zones_file = os.path.join(input_directory, "Zone.CSV")

    converted_contacts_file = os.path.join(output_directory, "CS7000_contacts.xlsx")
    converted_channels_file = os.path.join(output_directory, "CS7000_channels.xlsx")
    converted_zones_file = os.path.join(output_directory, "CS7000_zones.xlsx")

    if check_files_closed(
        [converted_contacts_file, converted_channels_file, converted_zones_file]
    ):
        update_debug_output(
            "Cannot convert codeplug. One of the output files is open. "
            "Please close the file before attempting to convert again"
        )
        return

    # Convert contact file
    contacts = DigitalContacts(contacts_file, converted_contacts_file)
    numberContacts = contacts.getNumberContacts()

    if numberContacts <= Const.MAXCONTACTS:
        contacts.Convert()
        errorMakingContacts = False
        update_debug_output(f"Converted talkgroup file to {converted_contacts_file}")
    else:
        errorMakingContacts = True
        update_debug_output(
            f"Cannot convert talkgroups file. You have {numberContacts} talkgroups "
            f"which exceeds the maximum allowed size of {Const.MAXCONTACTS}"
        )

    # Convert channels file
    includeAnalogChannels = channel_type_var.get() == "digital_analog"
    update_debug_output("Including analog channels in conversion is " + str(includeAnalogChannels))

    if default_zones_channels_var.get() == "include":
        channels = Channels(stock_analog_channel_file, converted_channels_file, includeAnalogChannels)
        channels.load(stock_digital_channel_file)
        channels.load(channels_file)
    else:
        channels = Channels(channels_file, converted_channels_file, includeAnalogChannels)

    # Get any debug output from previous channel methods and clear that debug buffer
    update_debug_output(channels.getDebugOutput())
    channels.clear_log_output()

    # Run Deduper
    dedupe = Deduper(root, icon_file, contacts, channels)
    dedupe.run()

    # Get any debug from dedupe and output
    update_debug_output(dedupe.getDebugOutput())
    dedupe.clear_log_output()

    numberChannels = channels.getNumberChannels()
    if numberChannels <= Const.MAXCHANNELS:
        if IdMethod_var.get() == "direct":
            uhfChannels = channels.ConvertDirectMode(contacts)
        else:
            uhfChannels = channels.Convert()

        # Get any output from channels from previous methods
        update_debug_output(channels.getDebugOutput())
        channels.clear_log_output()

        errorMakingChannels = False
        update_debug_output(f"Converted channels to {converted_channels_file}")

        VhfChannels = channels.getVhfChannels()
        update_debug_output("Excluded the following VHF channels")
        if len(VhfChannels) > 0:
            for key in sorted(VhfChannels):
                update_debug_output(key)
    else:
        errorMakingChannels = True
        update_debug_output(
            f"Cannot convert channels file. You have {numberChannels} channels "
            f"which exceeds the maximum allowed size of {Const.MAXCHANNELS}"
        )
        uhfChannels = {}

    # Convert zones file
    if default_zones_channels_var.get() == "include":
        zones = Zones(stock_zones_file, converted_zones_file, uhfChannels)
        zones.load(zones_file)
    else:
        zones = Zones(zones_file, converted_zones_file, uhfChannels)

    numberZones = zones.getNumberZones()
    if numberZones <= Const.MAXZONES:
        zones.Convert()
        errorMakingZones = False
        update_debug_output(f"Converted zones file to {converted_zones_file}")
    else:
        errorMakingZones = True
        update_debug_output(
            f"Cannot convert zones file. You have {numberZones} zones "
            f"which exceeds the maximum allowed size of {Const.MAXZONES}"
        )

    if IdMethod_var.get() == "direct":
        delete_file(converted_contacts_file)
        messagebox.showinfo(
            "Information",
            "You selected the Direct method to output ID to the channel. "
            "For this case there is no contacts spreadsheet to import into the CS7000 CPS",
            parent=root,
        )

    open_file_explorer(output_directory)
    update_debug_output("Now opening folder containing converted output files")


def exit_application():
    input_directory = getDirectoryname(input_directory_var.get())
    output_directory = getDirectoryname(output_directory_var.get())
    channel_type = channel_type_var.get()
    default_settings = default_zones_channels_var.get()
    idMethod = IdMethod_var.get()

    with open(os.path.join(configFolderPath, "CS7000_convert_settings.csv"), mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            ["Input Directory", "Output Directory", "Channel Type", "Default Settings", "ID Method"]
        )
        writer.writerow([input_directory, output_directory, channel_type, default_settings, idMethod])

    root.destroy()


def read_csv_and_set_variables(file_path):
    with open(file_path, mode="r") as file:
        reader = csv.reader(file)
        headers = next(reader)
        data = next(reader)

        variables = {header: value for header, value in zip(headers, data)}

        input_directory = variables.get("Input Directory", "")
        output_directory = variables.get("Output Directory", "")
        channel_type = variables.get("Channel Type", "digital")
        default_settings = variables.get("Default Settings", "include")
        idMethod = variables.get("ID Method", "direct")

        input_directory_var.set(f"Selected directory: {input_directory}")
        output_directory_var.set(f"Selected directory: {output_directory}")
        channel_type_var.set(channel_type)
        default_zones_channels_var.set(default_settings)
        IdMethod_var.set(idMethod)


def getConfigFolderPath():
    home_dir = os.path.expanduser("~")
    config_folder_path = os.path.join(home_dir, "CS7000_convert_gui")

    if not os.path.exists(config_folder_path):
        os.makedirs(config_folder_path)
        update_debug_output(f"Application profile folder '{config_folder_path}' created successfully!")
    else:
        update_debug_output(f"Found application profile folder '{config_folder_path}'")

    return config_folder_path


def raise_above_all(window):
    window.attributes("-topmost", 1)
    window.attributes("-topmost", 0)


def build_main_ui():
    global debug_output_text

    root.title(
        f"CS7000 Code Plug Utility - By Jason Johnson (K3JSJ) <k3jsj@arrl.net>  Version {APP_VERSION}"
    )

    root.iconphoto(False, tk.PhotoImage(file=resource_path(icon_file)))

    for widget in root.winfo_children():
        widget.destroy()

    # Menu bar with Help / About
    menubar = tk.Menu(root)
    helpmenu = tk.Menu(menubar, tearoff=0)
    helpmenu.add_command(label="Show Help", command=show_help)
    helpmenu.add_separator()
    helpmenu.add_command(label="About", command=show_about)
    helpmenu.add_command(label="Exit App", command=exit_application)
    menubar.add_cascade(label="Help", menu=helpmenu)
    root.config(menu=menubar)

    left_frame = tb.Frame(root, padding=10)
    right_frame = tb.Frame(root, padding=10)

    left_frame.pack(side="left", padx=10, pady=10, fill="both", expand=True)
    right_frame.pack(side="right", padx=10, pady=10, fill="both", expand=True)

    # Import channels frame
    frame = tb.Labelframe(left_frame, text="Import channels", padding=10)
    frame.pack(padx=10, pady=10, fill="x")

    radio_digital = tb.Radiobutton(
        frame, text="Digital", variable=channel_type_var, value="digital", bootstyle="primary-toolbutton"
    )
    radio_digital_analog = tb.Radiobutton(
        frame,
        text="Digital & Analog",
        variable=channel_type_var,
        value="digital_analog",
        bootstyle="primary-toolbutton",
    )

    radio_digital.pack(anchor="w", padx=10, pady=5)
    radio_digital_analog.pack(anchor="w", padx=10, pady=5)

    # Default Zones/Channels frame
    frame_default = tb.Labelframe(
        left_frame, text="Include radio default Zones & Channels", padding=10
    )
    frame_default.pack(padx=10, pady=10, fill="x")

    radio_include_default = tb.Radiobutton(
        frame_default,
        text="Include",
        variable=default_zones_channels_var,
        value="include",
        bootstyle="success-toolbutton",
    )
    radio_exclude_default = tb.Radiobutton(
        frame_default,
        text="Exclude",
        variable=default_zones_channels_var,
        value="exclude",
        bootstyle="secondary-toolbutton",
    )
    radio_include_default.pack(anchor="w", padx=10, pady=5)
    radio_exclude_default.pack(anchor="w", padx=10, pady=5)

    # ID method frame
    frame_IdMethod = tb.Labelframe(
        left_frame, text="Method to populate ID in channel", padding=10
    )
    frame_IdMethod.pack(padx=10, pady=10, fill="x")

    radio_direct_method = tb.Radiobutton(
        frame_IdMethod,
        text="Direct",
        variable=IdMethod_var,
        value="direct",
        bootstyle="info-toolbutton",
    )
    radio_table_method = tb.Radiobutton(
        frame_IdMethod,
        text="Table",
        variable=IdMethod_var,
        value="table",
        bootstyle="info-toolbutton",
    )
    radio_direct_method.pack(anchor="w", padx=10, pady=5)
    radio_table_method.pack(anchor="w", padx=10, pady=5)

    # Buttons
    btn_select_input_dir = tb.Button(
        left_frame,
        text="Select input directory",
        command=select_input_directory,
        bootstyle="secondary",
    )
    btn_select_output_dir = tb.Button(
        left_frame,
        text="Select output directory",
        command=select_output_directory,
        bootstyle="secondary",
    )
    btn_convert_codeplug = tb.Button(
        left_frame,
        text="Convert Codeplug",
        command=convert_codeplug,
        bootstyle="success",
    )
    btn_exit = tb.Button(
        left_frame,
        text="Exit",
        command=exit_application,
        bootstyle="danger",
    )

    btn_select_input_dir.pack(padx=10, pady=5, fill="x")
    tb.Label(left_frame, textvariable=input_directory_var).pack(
        padx=10, pady=5, fill="x"
    )

    btn_select_output_dir.pack(padx=10, pady=5, fill="x")
    tb.Label(left_frame, textvariable=output_directory_var).pack(
        padx=10, pady=5, fill="x"
    )

    btn_convert_codeplug.pack(padx=10, pady=5, fill="x")
    btn_exit.pack(padx=10, pady=5, fill="x")

    # Debug output frame
    debug_frame = tb.Labelframe(right_frame, text="Debug Output", padding=10)
    debug_frame.pack(side="left", padx=10, pady=10, fill="both", expand=True)

    debug_output_text = ScrolledText(
        debug_frame,
        autohide=True,
        padding=5,
        wrap="word",
        height=10,
    )
    debug_output_text.pack(fill="both", expand=True)

    # After creating the widget, refresh it with any existing log
    if debug_output_var.get():
        debug_output_text.insert("end", debug_output_var.get())
        debug_output_text.see("end")

    # Load previous settings if present
    try:
        read_csv_and_set_variables(os.path.join(configFolderPath, "CS7000_convert_settings.csv"))
    except FileNotFoundError:
        update_debug_output("Did not find CS7000_convert_settings.csv. Please select location of files")

    # Let Tk compute natural size, then lock minimum
    root.update_idletasks()
    root.minsize(root.winfo_width(), root.winfo_height())

    raise_above_all(root)

def show_about():
    import webbrowser

    # Create window minimized first (prevents flicker)
    about_win = tb.Toplevel(root)
    about_win.title("About CS7000 Code Plug Utility")
    about_win.withdraw()
    about_win.iconify()

    # Load icon image
    icon_img = tk.PhotoImage(file=resource_path(icon_file))
    about_win.iconphoto(False, icon_img)

    about_win.resizable(False, False)
    about_win.transient(root)
    about_win.grab_set()

    # --- MAIN FRAME ---
    frame = tb.Frame(about_win, padding=20)
    frame.pack(fill="both", expand=True)

    # --- LEFT COLUMN: ICON ---
    icon_label = tb.Label(frame, image=icon_img)
    icon_label.image = icon_img  # prevent garbage collection
    icon_label.grid(row=0, column=0, rowspan=6, padx=(0, 20), sticky="n")

    # --- RIGHT COLUMN: TEXT ---
    tb.Label(
        frame,
        text="CS7000 Code Plug Utility",
        font="-size 16 -weight bold"
    ).grid(row=0, column=1, sticky="w", pady=(0, 10))

    tb.Label(
        frame,
        text=f"Version {APP_VERSION}",
        font="-size 12"
    ).grid(row=1, column=1, sticky="w", pady=(0, 10))

    tb.Label(
        frame,
        text="Author: Jason Johnson (K3JSJ)",
        font="-size 11"
    ).grid(row=2, column=1, sticky="w", pady=(0, 10))

    tb.Label(
        frame,
        text="Convert Anytone talkgroups, channels, and zones into CS7000 format.\n\nProject Repository:",
        wraplength=400,
        justify="left"
    ).grid(row=3, column=1, sticky="w", pady=(0, 10))

    # --- CLICKABLE LINK ---
    link = tb.Label(
        frame,
        text="https://github.com/VikingNation/CS7000_convert_gui",
        foreground="blue",
        cursor="hand2",
        font="-underline 1"
    )
    link.grid(row=4, column=1, sticky="w", pady=(0, 20))

    def open_repo(event):
        webbrowser.open("https://github.com/VikingNation/CS7000_convert_gui")

    link.bind("<Button-1>", open_repo)

    # --- OK BUTTON ---
    tb.Button(
        frame,
        text="OK",
        bootstyle="primary",
        command=about_win.destroy
    ).grid(row=5, column=1, sticky="e")

    # --- Compute size while hidden ---
    about_win.update_idletasks()

    # --- Restore from iconified state ---
    about_win.deiconify()

    # --- Center relative to root ---
    x = root.winfo_x() + (root.winfo_width() - about_win.winfo_width()) // 2
    y = root.winfo_y() + (root.winfo_height() - about_win.winfo_height()) // 2
    about_win.geometry(f"+{x}+{y}")

    raise_above_all(about_win)

def show_help():
    import webbrowser

    help_win = tb.Toplevel(root)
    help_win.title(f"Help - CS7000 Code Plug Utility - Version {APP_VERSION}")
    help_win.iconphoto(False, tk.PhotoImage(file=resource_path(icon_file)))

    help_text = (
        "CS7000 Code Plug Utility Help\n\n"
        "- Select the input directory containing Anytone TalkGroups.CSV, Channel.CSV, and Zone.CSV.\n"
        "- Select the output directory where CS7000 spreadsheets will be written.\n"
        "- Choose whether to include Digital only or Digital & Analog channels.\n"
        "- Choose whether to include the radio's default Zones & Channels.\n"
        "- Choose the method to populate ID in the channel (Direct or Table).\n"
        "- Click 'Convert Codeplug' to generate CS7000-compatible spreadsheets.\n\n"
        "For more details, see the project repository:\n"
        "https://github.com/VikingNation/CS7000_convert_gui\n"
    )

    text = ScrolledText(help_win, autohide=True, padding=10, wrap="word")
    text.pack(fill="both", expand=True)

    # Insert text normally
    text.insert("end", help_text)

    # --- MAKE THE LINK CLICKABLE ---
    link_url = "https://github.com/VikingNation/CS7000_convert_gui"
    start_index = "end-2l linestart"   # start of the second-to-last line
    end_index = "end-1l lineend"       # end of the second-to-last line

    # Tag the hyperlink
    text.text.tag_add("hyperlink", start_index, end_index)
    text.text.tag_config(
        "hyperlink",
        foreground="blue",
        underline=True
    )

    # Bind click event
    def open_link(event):
        webbrowser.open(link_url)

    text.text.tag_bind("hyperlink", "<Button-1>", open_link)
    text.text.tag_bind("hyperlink", "<Enter>", lambda e: text.text.config(cursor="hand2"))
    text.text.tag_bind("hyperlink", "<Leave>", lambda e: text.text.config(cursor=""))

    # Disable editing
    text.text.configure(state="disabled")

    # Center relative to root
    help_win.update_idletasks()
    x = root.winfo_x() + 50
    y = root.winfo_y() + 50
    help_win.geometry(f"+{x}+{y}")

    raise_above_all(help_win)

def reject_terms():
    root.destroy()


def show_disclaimer():
    disclaim_text = (
        "-----BEGIN PGP SIGNED MESSAGE-----\nHash: SHA512\n\n"
        "DISCLAIMER and TERMS OF USE:\n"
        "By using this software, you acknowledge and agree that you do so at your own risk. "
        "The author of this software makes no guarantees, representations, or warranties of any kind, "
        "express or implied, regarding the accuracy, reliability, or completeness of the software's output. "
        "The author shall not be held liable for any errors, omissions, or any losses, injuries, or damages "
        "arising from the use of this software. Users are solely responsible for verifying the correctness "
        "of the software's output and for any decisions made based on such output.\n\n"
        "Portions of this software are derived from open-source projects, and elements of the source code "
        "were generated using artificial intelligence. The author acknowledges the contributions of the "
        "open-source community and the advancements in AI technology that have made this software possible.\n\n"
        "Source code for this application is available at\n"
        "https://github.com/VikingNation/CS7000_convert_gui\n\n"
        "If you do not accept these terms press the Reject button to exit.\n"
        "Pressing the Accept button reflects acceptance of the terms of use.\n\n"
        "-----BEGIN PGP SIGNATURE-----\n"
        "iHUEARYKAB0WIQR+IRDUkGkAJUU5yYJZwtXH9CXoAgUCZ3g+9AAKCRBZwtXH9CXo\n"
        "AiHpAQCY2cQ/T5kN6T2dd1p/E/08SMcZUVSq6BGqsiW4RB4isQD/fOCoRZxwVpLa\n"
        "J95DoRyRMoCQj/vacDUb3vtB/K5Isgg=\n"
        "=nm48\n"
        "-----END PGP SIGNATURE-----\n"
    )

    dialog = tb.Toplevel(root)
    dialog.title("Disclaimer and Terms of Use")
    dialog.iconphoto(False, tk.PhotoImage(file=resource_path(icon_file)))

    dialog.transient(root)
    dialog.grab_set()

    # --- MAIN FRAME ---
    main_frame = tb.Frame(dialog, padding=10)
    main_frame.pack(fill="both", expand=True)

    # --- TEXT AREA ---
    textbox = ScrolledText(
        main_frame,
        wrap="word",
        autohide=True,
        padding=5,
    )
    textbox.insert("end", disclaim_text)
    textbox.text.configure(state="disabled")
    textbox.pack(fill="both", expand=True)

    # --- BUTTON BAR ---
    button_frame = tb.Frame(dialog, padding=10)
    button_frame.pack(fill="x")

    accept_button = tb.Button(
        button_frame,
        text="Accept",
        bootstyle="success",
        command=lambda: (dialog.destroy(), build_main_ui()),
    )
    accept_button.pack(side="left", padx=20, pady=10)

    reject_button = tb.Button(
        button_frame,
        text="Reject",
        bootstyle="danger",
        command=lambda: (dialog.destroy(), reject_terms()),
    )
    reject_button.pack(side="right", padx=20, pady=10)

    # Let Tk compute size, then lock minimum
    dialog.update_idletasks()
    dialog.minsize(dialog.winfo_width(), dialog.winfo_height())

    # Optional: center relative to root
    x = root.winfo_x() + 50
    y = root.winfo_y() + 50
    dialog.geometry(f"+{x}+{y}")

    raise_above_all(dialog)


# --- Application startup ---

try:
    import pyi_splash
    pyi_splash.close()
except Exception:
    pass

root = tb.Window(themename="flatly")
root.title(
    f"CS7000 Code Plug Utility - By Jason Johnson (K3JSJ) <k3jsj@arrl.net>  Version {APP_VERSION}"
)
root.iconphoto(False, tk.PhotoImage(file=resource_path(icon_file)))

# Initialize variables BEFORE any debug logging
debug_output_var = tk.StringVar(value="")
channel_type_var = tk.StringVar(value="digital")
input_directory_var = tk.StringVar()
output_directory_var = tk.StringVar()
default_zones_channels_var = tk.StringVar(value="include")
IdMethod_var = tk.StringVar(value="direct")

configFolderPath = getConfigFolderPath()

raise_above_all(root)

if (DEBUG == False):
    show_disclaimer()
else:
    build_main_ui()

root.mainloop()

