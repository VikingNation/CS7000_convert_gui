#!/bin/env python
import tkinter as tk
import csv
import os
import platform
from tkinter import ttk, filedialog
from connectSystems.CS7000.Channels import  Channels
from connectSystems.CS7000.DigitalContacts import DigitalContacts
from connectSystems.CS7000.Zones import Zones

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

def select_input_directory():
    directory = filedialog.askdirectory(title="Chose directory for Anytone input files")
    if directory:
        input_directory_var.set(f"Selected directory: {directory}")
        debug_output('User selected input directory')


def select_output_directory():
    directory = filedialog.askdirectory(title="Chose directory to output CS7000 spreadsheet files")
    if directory:
        output_directory_var.set(f"Selected directory: {directory}")
        debug_output('User selected output directory')


def open_file_explorer(path):
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":  # macOS
        os.system(f"open {path}")
    elif platform.system() == "Linux":
        os.system(f"xdg-open {path}")
    else:
        print("Unsupported operating system")

def getFilename(s):
    return s.replace("Selected file: ", "")

def getDirectoryname(s):
    return s.replace("Selected directory: ", "")

def debug_output(text):
    debug_output_var.set(debug_output_var.get() + '\n' + f'{text}')

def convert_codeplug():
    debug_output('Now converting files into format for CS7000')

    input_directory = getDirectoryname(input_directory_var.get())
    output_directory = getDirectoryname(output_directory_var.get())

    contacts_file = input_directory + "/TalkGroups.CSV"
    channels_file = input_directory + "/Channel.CSV"
    zones_file = input_directory + "/Zone.CSV"

    # Convert contact file
    converted_contacts_file = output_directory + "/CS7000_contacts.xlsx"
    contacts = DigitalContacts(contacts_file, converted_contacts_file)
    contacts.Convert()
    debug_output("Converted talkgroup file in " + converted_contacts_file)

    # Convert channels file
    if ( channel_type_var.get() == "digital_analog"):
        includeAnalogChannels = True
    else:
        includeAnalogChannels = False

    debug_output("Including analog channels in conversion is " + str(includeAnalogChannels))

    converted_channels_file = output_directory + "/CS7000_channels.xlsx"

    if ( default_zones_channels_var.get() == "include" ):
        channels = Channels(stock_analog_channel_file, converted_channels_file, includeAnalogChannels)
        channels.load(stock_digital_channel_file)
        channels.load(channels_file)
    else:
        channels = Channels(channels_file, converted_channels_file, includeAnalogChannels)

    uhfChannels = channels.Convert()
    debug_output("Converted channels to " +  converted_channels_file)

    # Convert zones file
    converted_zones_file = output_directory + "/CS7000_zones.xlsx"
    if ( default_zones_channels_var.get() == "include" ):
        zones = Zones(stock_zones_file, converted_zones_file, uhfChannels)
        zones.load(zones_file)
    else:
        zones = Zones(zones_file, converted_zones_file, uhfChannels)
    zones.Convert()
    debug_output("Converted zones file in " + converted_zones_file)

    open_file_explorer(output_directory)
    debug_output("Now opening folder containing converted output files")

def exit_application():
    input_directory = getDirectoryname(input_directory_var.get())
    output_directory = getDirectoryname(output_directory_var.get())
    channel_type = channel_type_var.get()
    default_settings = default_zones_channels_var.get()
    with open(configFolderPath + '/CS7000_convert_settings.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Input Directory', 'Output Directory', 'Channel Type', 'Default Settings'])
        writer.writerow([input_directory, output_directory, channel_type, default_settings])
   
    file.close()
    root.destroy()

def read_csv_and_set_variables(file_path):
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Read the header row
        data = next(reader)  # Read the first data row

        # Create a dictionary to store the variables
        variables = {header: value for header, value in zip(headers, data)}

        # Set variables
        input_directory = variables.get('Input Directory', '')
        output_directory = variables.get('Output Directory', '')
        channel_type = variables.get('Channel Type', '')
        default_settings = variables.get('Default Settings', 'include')
        input_directory_var.set(f"Selected directory: {input_directory}")
        output_directory_var.set(f"Selected directory: {output_directory}")
        channel_type_var.set(f"{channel_type}")
        default_zones_channels_var.set(f"{default_settings}")
        debug_output('Read settings from CS7000_convert_setting.csv')

def getConfigFolderPath():

    # Determine if config folder has been created if not.  create it
    # Get the user's home directory
    home_dir = os.path.expanduser("~")

    # Define the folder path
    config_folder_path = os.path.join(home_dir, "CS7000_convert_gui")

    # Check if the folder exists
    if not os.path.exists(config_folder_path):
        # Create the folder if it doesn't exist
        os.makedirs(config_folder_path)
        print(f"Application profile folder '{config_folder_path}' created successfully!")
    else:
        print(f"Found application profile folder '{config_folder_path}'")

    return config_folder_path

def raise_above_all(window):
    window.attributes('-topmost', 1)
    window.attributes('-topmost', 0)

def clear_and_rebuild():
    root.title("CS7000 Code Plug Utility - By Jason Johnson (K3JSJ) <k3jsj@arrl.net>  Version 1.3")

    # Destroy all existing widgets
    for widget in root.winfo_children():
        widget.destroy()

    # Create left and right frames
    left_frame = ttk.Frame(root)
    right_frame = ttk.Frame(root)

    # Pack the frames
    left_frame.pack(side="left", padx=10, pady=10, fill="both", expand=True)
    right_frame.pack(side="right", padx=10, pady=10, fill="both", expand=True)

    # Create a frame for the radio buttons
    frame = ttk.LabelFrame(left_frame, text="Import channels")
    frame.pack(padx=10, pady=10, fill="x")

    # Create radio buttons
    radio_digital = ttk.Radiobutton(frame, text="Digital", variable=channel_type_var, value="digital")
    radio_digital_analog = ttk.Radiobutton(frame, text="Digital & Analog", variable=channel_type_var, value="digital_analog")

    # Pack radio buttons
    radio_digital.pack(anchor="w", padx=10, pady=5)
    radio_digital_analog.pack(anchor="w", padx=10, pady=5)

    # Create frame for Default Zones/Channels
    frame_default = ttk.LabelFrame(left_frame, text="Default Zones & Channels")
    frame_default.pack(padx=10, pady=10, fill="x")
    # Create radio button for including firmware Zones & Channels
    radio_include_default = ttk.Radiobutton(frame_default, text="Include", variable=default_zones_channels_var, value="include")
    radio_exclude_default = ttk.Radiobutton(frame_default, text="Exclude", variable=default_zones_channels_var, value="exclude")
    radio_include_default.pack(anchor="w", padx=10, pady=5)
    radio_exclude_default.pack(anchor="w", padx=10, pady=10)

    # Create buttons
    btn_select_input_dir = ttk.Button(left_frame, text="Select input directory", command=select_input_directory)
    btn_select_output_dir = ttk.Button(left_frame, text="Select output directory", command=select_output_directory)

    btn_convert_codeplug = ttk.Button(left_frame, text="Convert Codeplug", command=convert_codeplug)
    btn_exit = ttk.Button(left_frame, text="Exit", command=exit_application)

    # Pack buttons and labels
    btn_select_input_dir.pack(padx=10, pady=5, fill="x")
    ttk.Label(left_frame, textvariable=input_directory_var).pack(padx=10, pady=5, fill="x")

    btn_select_output_dir.pack(padx=10, pady=5, fill="x")
    ttk.Label(left_frame, textvariable=output_directory_var).pack(padx=10, pady=5, fill="x")

    btn_convert_codeplug.pack(padx=10, pady=5, fill="x")
    btn_exit.pack(padx=10, pady=5, fill="x")


    # Create a frame for the debug output
    debug_frame = ttk.LabelFrame(right_frame, text="Debug Output")
    debug_frame.pack(side="left", padx=10, pady=10, fill="both", expand=True)

    # Create a label to display the debug output
    debug_output_label = ttk.Label(debug_frame, textvariable=debug_output_var)
    debug_output_label.pack(padx=10, pady=10)


    # Read CSV and set variables if the file exists
    try:
        read_csv_and_set_variables(configFolderPath + '/CS7000_convert_settings.csv')
    except FileNotFoundError:
        debug_output('Did not find CS7000_covert_setting.csv.  Please select location of files')
        pass

    # resize the window
    root.geometry("1200x500+0+0")

    raise_above_all(root)


def reject_terms():
    print("Rejected terms of use")
    root.destroy()

# Create the main application window
try:
    import pyi_splash
    pyi_splash.close()
except:
    pass

root = tk.Tk()
root.title("CS7000 Code Plug Utility - By Jason Johnson (K3JSJ) <k3jsj@arrl.net>  Version 1.3")


# Global variables to hold user selections from application window

# Location of stock Zones and Analog and Digital Channels CSV files that come pre-loaded with
# CS7000 
stock_zones_file = "codeplugs\\CS7000_M17_PLUS_V9.00.93_zones.csv"
stock_analog_channel_file = "codeplugs\\CS7000_M17_PLUS_V9.00.93_analog_channels.csv"
stock_digital_channel_file = "codeplugs\\CS7000_M17_PLUS_V9.00.93_digital_channels.csv"


configFolderPath = getConfigFolderPath()

channel_type_var = tk.StringVar(value="digital")
input_directory_var = tk.StringVar()
output_directory_var = tk.StringVar()

# Create a StringVar for the debug output
debug_output_var = tk.StringVar()

# Variable to hold if user wants to include stock Zones & channels that come preloaded with firmware
default_zones_channels_var = tk.StringVar()

disclaim_text = "-----BEGIN PGP SIGNED MESSAGE-----\nHash: SHA512\n\n"

disclaim_text = disclaim_text + "DISCLAIMER and TERMS OF USE:\nBy using this software, you acknowledge and agree that you do so at your own risk. The author of this software makes no guarantees, representations, or warranties of any kind, express or implied, regarding the accuracy, reliability, or completeness of the software's output. The author shall not be held liable for any errors, omissions, or any losses, injuries, or damages arising from the use of this software.  Users are solely responsible for verifying the correctness of the software's output and for any decisions made based on such output."

disclaim_text = "\n" + disclaim_text + "Portions of this software are derived from open-source projects, and elements of the source code were generated using artificial intelligence. The author acknowledges the contributions of the open-source community and the advancements in AI technology that have made this software possible."

disclaim_text = "\n" + disclaim_text + "\n\nSource code for this applicaion is avaialble at\nhttps://github.com/VikingNation/CS7000_convert_gui\n\n"
disclaim_text = disclaim_text + "If you do not accept these terms press the Reject button to exit.\nPressing the Accept button reflects acceptance of the terms of use.\n"

disclaim_text = disclaim_text + "-----BEGIN PGP SIGNATURE-----\n\niHUEARYKAB0WIQR+IRDUkGkAJUU5yYJZwtXH9CXoAgUCZ3g+9AAKCRBZwtXH9CXo\nAiHpAQCY2cQ/T5kN6T2dd1p/E/08SMcZUVSq6BGqsiW4RB4isQD/fOCoRZxwVpLa\nJ95DoRyRMoCQj/vacDUb3vtB/K5Isgg=\n=nm48\n-----END PGP SIGNATURE-----\n"

textbox = tk.Text(root, height=32, width=80)
textbox.insert(tk.END, disclaim_text)
textbox.pack(pady=10, padx=10)
accept_button = tk.Button(root, text="Accept", command=clear_and_rebuild)
accept_button.pack(side=tk.LEFT, padx=20, pady=10)

reject_button = tk.Button(root, text="Reject", command=reject_terms)
reject_button.pack(side=tk.RIGHT, padx=20, pady=10)
root.geometry("800x700+0+0")

raise_above_all(root)


# Start the main event loop
root.mainloop()
