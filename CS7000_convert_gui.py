#!/bin/env python
import tkinter as tk
from tkinter import ttk, filedialog
import csv

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

# Create the main application window
root = tk.Tk()
root.title("CS7000 Code Plug Utility")

# Create a frame for the radio buttons
frame = ttk.LabelFrame(root, text="Import channels")
frame.pack(padx=10, pady=10, fill="x")

# Create radio button variables
channel_type = tk.StringVar(value="analog")

# Create radio buttons
radio_analog = ttk.Radiobutton(frame, text="Analog", variable=channel_type, value="analog")
radio_digital_analog = ttk.Radiobutton(frame, text="Digital & Analog", variable=channel_type, value="digital_analog")

# Pack radio buttons
radio_analog.pack(anchor="w", padx=10, pady=5)
radio_digital_analog.pack(anchor="w", padx=10, pady=5)

# Create StringVar variables to hold folder paths
output_folder_var = tk.StringVar()
input_folder_var = tk.StringVar()

# Create buttons
btn_select_output = ttk.Button(root, text="Select Output Folder", command=select_output_folder)
btn_select_input = ttk.Button(root, text="Select Input Folder", command=select_input_folder)
btn_convert_codeplug = ttk.Button(root, text="Convert Codeplug", command=convert_codeplug)
btn_exit = ttk.Button(root, text="Exit", command=exit_application)

# Pack buttons and labels
btn_select_output.pack(padx=10, pady=5, fill="x")
ttk.Label(root, textvariable=output_folder_var).pack(padx=10, pady=5, fill="x")
btn_select_input.pack(padx=10, pady=5, fill="x")
ttk.Label(root, textvariable=input_folder_var).pack(padx=10, pady=5, fill="x")
btn_convert_codeplug.pack(padx=10, pady=5, fill="x")
btn_exit.pack(padx=10, pady=5, fill="x")

# Start the main event loop
root.mainloop()

