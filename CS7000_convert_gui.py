#!/bin/env python
import tkinter as tk
import csv
import os
import sys
import platform
from tkinter import ttk, filedialog
from connectSystems.CS7000.Channels import  Channels
from connectSystems.CS7000.DigitalContacts import DigitalContacts
from connectSystems.CS7000.Zones import Zones
from connectSystems.CS7000.Specs import Specs

# CS7000_convert_gui.py
#
# Author: Jason Johnson <k3jsj@arrl.net>
# Purpose:  GUI to convert Anytone Talkgroups, Channels, and Zones into format for CS7000 CPS
#           Program prompts for directory of Anytone Talkgroups, Channel, and Zone files
#           Program outputs spreadsheets in format for CS7000
#
#           Portions of this source code were generated using Microsoft Co-Pilot

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

    contacts_file = input_directory + "/Talkgroups.CSV"
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
    channels = Channels(channels_file, converted_channels_file, includeAnalogChannels)
    uhfChannels = channels.Convert()
    debug_output("Converted channels to " +  converted_channels_file)

    # Convert zones file
    converted_zones_file = output_directory + "/CS7000_zones.xlsx"
    zones = Zones(zones_file, converted_zones_file, uhfChannels)
    zones.Convert()
    debug_output("Converted zones file in " + converted_zones_file)
    
    open_file_explorer(output_directory)
    debug_output("Now opening folder containing converted output files")

def exit_application():
    input_directory = getDirectoryname(input_directory_var.get())
    output_directory = getDirectoryname(output_directory_var.get())
    channel_type = channel_type_var.get()

    with open(configFolderPath + '/CS7000_convert_settings.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Input Directory', 'Output Directory', 'Channel Type'])
        writer.writerow([input_directory, output_directory, channel_type ])
   
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
        input_directory_var.set(f"Selected directory: {input_directory}")
        output_directory_var.set(f"Selected directory: {output_directory}")
        channel_type_var.set(f"{channel_type}")
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
    root.title("CS7000 Code Plug Utility - By Jason Johnson (K3JSJ) <k3jsj@arrl.net>  Version 1.2.1")

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
    frame = ttk.LabelFrame(left_frame, text="Select Type of channels to import")
    frame.pack(padx=10, pady=10, fill="x")

    # Create radio buttons
    radio_digital = ttk.Radiobutton(frame, text="Digital", variable=channel_type_var, value="digital")
    radio_digital_analog = ttk.Radiobutton(frame, text="Digital & Analog", variable=channel_type_var, value="digital_analog")

    # Pack radio buttons
    radio_digital.pack(anchor="w", padx=10, pady=5)
    radio_digital_analog.pack(anchor="w", padx=10, pady=5)
    
    # Display dropbox to pick firmware version
    firmwareFrame = ttk.LabelFrame(left_frame, text="Select firmware version")
    firmwareFrame.pack(padx=10, pady=10, fill="x")
    firmwareOptions = specs.getFirmwareVersions()
    firmwareComboBox = ttk.Combobox(firmwareFrame, values=firmwareOptions)
    firmwareComboBox.set(firmwareOptions[0])
    firmwareComboBox.pack(side="left", pady=10)
    firmwareComboBox.bind("<<ComboboxSelected>>", assignFirmwareVersion)

    # Set directories buttons
    directoryFrame = ttk.LabelFrame(left_frame, text="Select directories")
    directoryFrame.pack(padx=10, pady=10, fill="x")

    btn_select_input_dir = ttk.Button(directoryFrame, text="Select input directory", command=select_input_directory)
    btn_select_output_dir = ttk.Button(directoryFrame, text="Select output directory", command=select_output_directory)

    # Convert codeplug and exit buttons
    actionFrame = ttk.LabelFrame(left_frame, text="Select action")
    actionFrame.pack(padx=10, pady=10, fill="x")

    btn_convert_codeplug = ttk.Button(actionFrame, text="Convert Codeplug", command=convert_codeplug)
    btn_exit = ttk.Button(actionFrame, text="Exit", command=exit_application)

    # Pack buttons and labels
    btn_select_input_dir.pack(padx=10, pady=5, fill="x")
    ttk.Label(directoryFrame, textvariable=input_directory_var).pack(padx=10, pady=5, fill="x")

    btn_select_output_dir.pack(padx=10, pady=5, fill="x")
    ttk.Label(directoryFrame, textvariable=output_directory_var).pack(padx=10, pady=5, fill="x")

    btn_convert_codeplug.pack(padx=10, pady=5, fill="x")
    btn_exit.pack(padx=10, pady=5, fill="x")


    # Create a frame for the debug output
    debug_frame = ttk.LabelFrame(right_frame, text="Debug Output")
    debug_frame.pack(side="left", padx=10, pady=10, fill="both", expand=True)

    # Create a label to display the debug output
    debug_output_label = ttk.Label(debug_frame, textvariable=debug_output_var)
    debug_output_label.pack(side="top", padx=10, pady=10)


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

def assignFirmwareVersion(event):
    firmwareVersion_var.set(firmwareComboBox.get())
    print(firmwareVersion_var.get())


#### Start of application

# Create the main application window
try:
    import pyi_splash
    pyi_splash.close()
except:
    pass

root = tk.Tk()
root.title("CS7000 Code Plug Utility - By Jason Johnson (K3JSJ) <k3jsj@arrl.net>  Version 1.2")

# Read in DISCLAIMER statement
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.abspath(".")

file_path = os.path.join(base_path, "DISCLAIMER.txt.asc")
with open(file_path, 'r') as file:
    disclaim_text = file.read()
file.close()

# Global variables to hold user selections from application window
configFolderPath = getConfigFolderPath()

# Get radio specifications
specs = Specs()

channel_type_var = tk.StringVar(value="digital")
input_directory_var = tk.StringVar()
output_directory_var = tk.StringVar()

# Variables for firmware selection
firmwareComboBox = None
firmwareVersion_var = tk.StringVar()

# Create a StringVar for the debug output
debug_output_var = tk.StringVar()

# Widget for disclaimer
disclaimFrame = ttk.LabelFrame(root)
disclaimFrame.pack(padx=10, pady=10, fill="x")

textbox = tk.Text(disclaimFrame, height=32, width=80, padx=10, pady=10)
textbox.insert(tk.END, disclaim_text)
textbox.pack(pady=10, padx=10)
accept_button = tk.Button(disclaimFrame, text="Accept", command=clear_and_rebuild)
accept_button.pack(side=tk.LEFT, padx=10, pady=10)

reject_button = tk.Button(disclaimFrame, text="Reject", command=reject_terms)
reject_button.pack(side=tk.RIGHT, padx=10, pady=10)
root.geometry("800x700+0+0")

raise_above_all(root)


# Start the main event loop
root.mainloop()
