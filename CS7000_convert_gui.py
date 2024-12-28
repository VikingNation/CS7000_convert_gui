#!/bin/env python
import tkinter as tk
from tkinter import ttk, filedialog
import csv

# CS7000_convert_gui.py
#
# Author: Jason Johnson <k3jsj@arrl.net>
# Purpose:  GUI to convert Anytone Talkgroups, Channels, and Zones into format for CS7000 CPS
#           Program prompts for directory and assumes files are called talkgroups.csv, channels.csv, and zones.csv
#           Program outputs contactsc.csv, channels.csv, and zones.csv into directory selected
#
#           This source code was generated using Microsoft Co-Pilot


def select_output_folder():
    folder = filedialog.askdirectory()
    if folder:
        output_folder_var.set(f"Selected output folder: {folder}")

def select_input_folder():
    folder = filedialog.askdirectory()
    if folder:
        input_folder_var.set(f"Selected input folder: {folder}")

def convert_codeplug():
    print("Convert codeplug button clicked")

def exit_application():
    input_folder = input_folder_var.get().replace("Selected input folder: ", "")
    output_folder = output_folder_var.get().replace("Selected output folder: ", "")
    
    with open('cs7000_convert_settings.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Input Folder', 'Output Folder'])
        writer.writerow([input_folder, output_folder])
    
    root.destroy()

def read_csv_and_set_variables(file_path):
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Read the header row
        data = next(reader)  # Read the first data row

        # Create a dictionary to store the variables
        variables = {header: value for header, value in zip(headers, data)}

        # Set variables
        input_folder = variables.get('Input Folder', '')
        output_folder = variables.get('Output Folder', '')

        input_folder_var.set(f"Selected input folder: {input_folder}")
        output_folder_var.set(f"Selected output folder: {output_folder}")

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


# Create StringVar variables to hold folder paths
output_folder_var = tk.StringVar()
input_folder_var = tk.StringVar()

# Create buttons
btn_select_output = ttk.Button(left_frame, text="Select Output Folder", command=select_output_folder)
btn_select_input = ttk.Button(left_frame, text="Select Input Folder", command=select_input_folder)
btn_convert_codeplug = ttk.Button(left_frame, text="Convert Codeplug", command=convert_codeplug)
btn_exit = ttk.Button(left_frame, text="Exit", command=exit_application)

# Pack buttons and labels
btn_select_output.pack(padx=10, pady=5, fill="x")
ttk.Label(left_frame, textvariable=output_folder_var).pack(padx=10, pady=5, fill="x")
btn_select_input.pack(padx=10, pady=5, fill="x")
ttk.Label(left_frame, textvariable=input_folder_var).pack(padx=10, pady=5, fill="x")
btn_convert_codeplug.pack(padx=10, pady=5, fill="x")
btn_exit.pack(padx=10, pady=5, fill="x")


# Create a frame for the debug output
debug_frame = ttk.LabelFrame(right_frame, text="Debug Output")
debug_frame.pack(side="right", padx=10, pady=10, fill="both", expand=True)

# Create a StringVar for the debug output
debug_output_var = tk.StringVar()

# Create a label to display the debug output
debug_output_label = ttk.Label(debug_frame, textvariable=debug_output_var)
debug_output_label.pack(padx=10, pady=10)


root.geometry("800x400")

# Read CSV and set variables if the file exists
try:
    read_csv_and_set_variables('cs7000_convert_settings.csv')
except FileNotFoundError:
    pass


# Start the main event loop
root.mainloop()




