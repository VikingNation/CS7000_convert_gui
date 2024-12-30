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
#           Program prompts for directory and assumes files are called talkgroups.csv, channels.csv, and zones.csv
#           Program outputs contactsc.csv, channels.csv, and zones.csv into directory selected
#
#           This source code was generated using Microsoft Co-Pilot

def select_output_directory():
    directory = filedialog.askdirectory(title="Chose directorty to output files")
    if directory:
        output_directory_var.set(f"Selected directory: {directory}")
        debug_output('User selected contacts file')


def open_file_explorer(path):
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":  # macOS
        os.system(f"open {path}")
    elif platform.system() == "Linux":
        os.system(f"xdg-open {path}")
    else:
        print("Unsupported operating system")

def select_contacts_file():
    file = filedialog.askopenfilename(title="Select contacts file to import")
    if file:
        contacts_file_var.set(f"Selected file: {file}")
        debug_output('User selected contacts file')

def select_channels_file():
    file = filedialog.askopenfilename(title="Select channels file to import")
    if file:
        channels_file_var.set(f"Selected file: {file}")
        debug_output('User selected channels file')

def select_zones_file():
    file = filedialog.askopenfilename(title = "Select zones file to import")
    if file:
        zones_file_var.set(f"Selected file: {file}")
        debug_output('User selected zones file')

def getFilename(s):
    return s.replace("Selected file: ", "")

def getDirectoryname(s):
    return s.replace("Selected directory: ", "")

def debug_output(text):
    debug_output_var.set(debug_output_var.get() + '\n' + f'{text}')

def convert_codeplug():
    debug_output('Now converting files into format for CS7000')

    output_directory = getDirectoryname(output_directory_var.get())


    # Convert contact file
    converted_contacts_file = output_directory + "/CS7000_contacts.csv"
    contacts = DigitalContacts(getFilename(contacts_file_var.get()), converted_contacts_file)
    contacts.Convert()
    debug_output("Converted talkgroup file in " + converted_contacts_file)

    # Convert channels file
    converted_ch_dmr_file = output_directory + "/CS7000_channels_dmr.csv"
    converted_ch_analog_file = output_directory + "/CS7000_channels_analog.csv"
    channels = Channels(getFilename(channels_file_var.get()), converted_ch_dmr_file, converted_ch_analog_file)
    uhfChannels = channels.Convert()
    print(uhfChannels)
    debug_output("Converted dmr channels to " +  converted_ch_dmr_file)
    debug_output("Converted analog channels to " +  converted_ch_analog_file)

    # Convert zones file
    zone_file = getFilename(zones_file_var.get())
    converted_zones_file = output_directory + "/CS7000_zones.csv"
    zones = Zones(getFilename(zones_file_var.get()), converted_zones_file, uhfChannels)
    zones.Convert()
    debug_output("Converted zones file in " + converted_zones_file)
    
    open_file_explorer(output_directory)
    debug_output("Now opening folder containing converted output files")

def exit_application():
    contacts_file = contacts_file_var.get().replace("Selected file: ", "")
    channels_file = channels_file_var.get().replace("Selected file: ", "")
    zones_file = zones_file_var.get().replace("Selected file: ", "")
    output_directory = getDirectoryname(output_directory_var.get())

    with open('CS7000_convert_settings.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Contacts File', 'Channels File', 'Zone File', 'Output Directory'])
        writer.writerow([contacts_file, channels_file, zones_file, output_directory])
   
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
        contacts_file = variables.get('Contacts File', '')
        channels_file = variables.get('Channels File', '')
        zones_file = variables.get('Zone File', '')
        output_directory = variables.get('Output Directory', '')

        contacts_file_var.set(f"Selected file: {contacts_file}")
        channels_file_var.set(f"Selected file: {channels_file}")
        zones_file_var.set(f"Selected file: {zones_file}")
        output_directory_var.set(f"Selected directory: {output_directory}")
        debug_output('Read settings from CS7000_convert_setting.csv')

# Create the main application window
root = tk.Tk()
root.title("CS7000 Code Plug Utility")



# Create left and right frames
left_frame = ttk.Frame(root)
right_frame = ttk.Frame(root)

# Pack the frames
left_frame.pack(side="left", padx=10, pady=10, fill="both", expand=True)
right_frame.pack(side="right", padx=10, pady=10, fill="both", expand=True)

# Create a frame for the radio buttons
frame = ttk.LabelFrame(left_frame, text="Import channels")
frame.pack(padx=10, pady=10, fill="x")

# Create radio button variables
channel_type = tk.StringVar(value="digital")

# Create radio buttons
radio_analog = ttk.Radiobutton(frame, text="Digital", variable=channel_type, value="digital")
radio_digital_analog = ttk.Radiobutton(frame, text="Digital & Analog", variable=channel_type, value="digital_analog")

# Pack radio buttons
radio_analog.pack(anchor="w", padx=10, pady=5)
radio_digital_analog.pack(anchor="w", padx=10, pady=5)

# Create StringVar variables to hold files paths
contacts_file_var = tk.StringVar()
channels_file_var = tk.StringVar()
zones_file_var = tk.StringVar()
output_directory_var = tk.StringVar()


# Create buttons
btn_select_contacts = ttk.Button(left_frame, text="Select Contacts File", command=select_contacts_file)
btn_select_channels = ttk.Button(left_frame, text="Select Channels File", command=select_channels_file)
btn_select_zone = ttk.Button(left_frame, text="Select Zone File", command=select_zones_file)

btn_select_output_dir = ttk.Button(left_frame, text="Select Output directory", command=select_output_directory)


btn_convert_codeplug = ttk.Button(left_frame, text="Convert Codeplug", command=convert_codeplug)
btn_exit = ttk.Button(left_frame, text="Exit", command=exit_application)

# Pack buttons and labels
btn_select_contacts.pack(padx=10, pady=5, fill="x")
ttk.Label(left_frame, textvariable=contacts_file_var).pack(padx=10, pady=5, fill="x")
btn_select_channels.pack(padx=10, pady=5, fill="x")
ttk.Label(left_frame, textvariable=channels_file_var).pack(padx=10, pady=5, fill="x")
btn_select_zone.pack(padx=10, pady=5, fill="x")
ttk.Label(left_frame, textvariable=zones_file_var).pack(padx=10, pady=5, fill="x")
btn_select_output_dir.pack(padx=10, pady=5, fill="x")
ttk.Label(left_frame, textvariable=output_directory_var).pack(padx=10, pady=5, fill="x")
btn_convert_codeplug.pack(padx=10, pady=5, fill="x")
btn_exit.pack(padx=10, pady=5, fill="x")


# Create a frame for the debug output
debug_frame = ttk.LabelFrame(right_frame, text="Debug Output")
debug_frame.pack(side="left", padx=10, pady=10, fill="both", expand=True)

# Create a StringVar for the debug output
debug_output_var = tk.StringVar()

# Create a label to display the debug output
debug_output_label = ttk.Label(debug_frame, textvariable=debug_output_var)
debug_output_label.pack(padx=10, pady=10)


# Read CSV and set variables if the file exists
try:
    read_csv_and_set_variables('CS7000_convert_settings.csv')
except FileNotFoundError:
    debug_output('Did not find CS7000_covert_setting.csv.  Please select location of files')
    pass

# resize the window
root.geometry("1200x500+0+0")



# Start the main event loop
root.mainloop()




