#!/bin/env python
import tkinter as tk
import csv
import os
import sys
import platform
from tkinter import ttk, filedialog
from connectSystems.CS7000.Channels import Channels
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

class DisclaimerFrame(tk.Frame):
    def __init__(self, master=None, disclaimText="Press accept button to continue", acceptCallBack=None, rejectCallBack=None):
        super().__init__(master)
        self.acceptCallBack = acceptCallBack
        self.rejectCallBack = rejectCallBack
        self.master = master
        self.pack()
        self.disclaimText = disclaimText
        self.create_widgets()

    def create_widgets(self):
        self.textbox = tk.Text(self, height=32, width=80, padx=10, pady=10)
        self.textbox.insert(tk.END, self.disclaimText)
        self.textbox.pack(pady=10, padx=10)
        self.accept_button = tk.Button(self, text="Accept", command=self.acceptCallBack)
        self.accept_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.reject_button = tk.Button(self, text="Reject", command=self.rejectCallBack)
        self.reject_button.pack(side=tk.RIGHT, padx=10, pady=10)

class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CS7000 Code Plug Utility - By Jason Johnson (K3JSJ) <k3jsj@arrl.net>  Version 1.2.1")

        #### Start define class variables
        self.__configFolderPath = self.__setConfigFolderPath()

        # Get radio specifications
        self.__specs = Specs()

        self.__channel_type_var = tk.StringVar(value="digital")
        self.__input_directory_var = tk.StringVar()
        self.__output_directory_var = tk.StringVar()

        # Variables for firmware selection
        self.__firmware_version_var = tk.StringVar()

        # Create a StringVar for the debug output
        self.__debug_output_var = tk.StringVar()

        # Create and display disclaimer frame 
        self.__disclaimText = self.__getDisclaimerText()
        self.__disclaimFrame = DisclaimerFrame(self,self.__disclaimText, accept_terms, reject_terms)

        self.__comboBox = None

        # Set geometry of window
        self.geometry("800x700+0+0")
        self.__raise_above_all()

    def getConfigFolderPath(self):
        return self.__configFolderPath

    def getInput_directory(self):
        return self.__input_directory_var.get()

    def getOutput_directory(self):
        return self.__output_directory_var.get()

    def getChannel_type(self):
        return self.__channel_type_var.get()

    def getFirmware_version(self):
        return self.__firmware_version_var.get()

    def setInput_directory(self,val):
        self.__input_directory_var.set(val)

    def setOutput_directory(self,val):
        self.__output_directory_var.set(val)

    def setChannel_type(self,val):
        self.__channel_type_var.set(val)

    def getMaxContacts(self):
        return self.__specs.getSpecs(self.getFirmware_version() )['maxContacts']

    def getMaxChannels(self):
        return self.__specs.getSpecs(self.getFirmware_version() )['maxChannels']

    def getMaxZones(self):
        return self.__specs.getSpecs(self.getFirmware_version() )['maxZones']

    def __select_input_directory(self):
        directory = filedialog.askdirectory(title="Chose directory for Anytone input files")
        if directory:
            self.setInput_directory(f"Selected directory: {directory}")
            self.debug_output('User selected input directory')


    def __select_output_directory(self):
        directory = filedialog.askdirectory(title="Chose directory to output CS7000 spreadsheet files")
        if directory:
            self.setOutput_directory(f"Selected directory: {directory}")
            self.debug_output('User selected output directory')

    def debug_output(self,text):
        self.__debug_output_var.set(self.__debug_output_var.get() + '\n' + f'{text}')

    def __debug_DisplaySpecs(self):
        value1 = self.getMaxContacts()
        self.debug_output(f'Maximum contacts for radio: {value1}')
        value2 = self.getMaxChannels()
        self.debug_output(f'Maximum channels for radio: {value2}')
        value3 = self.getMaxZones()
        self.debug_output(f'Maximum zones for radio: {value3}')
    
    def __setConfigFolderPath(self):
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

    def getConfigFolderPath(self):
        return(self.__configFolderPath)

    def createMainWindow(self):
        # Destroy all existing widgets
        for widget in self.winfo_children():
            widget.destroy()

        # Create left and right frames
        left_frame = ttk.Frame(self)
        right_frame = ttk.Frame(self)

        # Pack the frames
        left_frame.pack(side="left", padx=10, pady=10, fill="both", expand=True)
        right_frame.pack(side="right", padx=10, pady=10, fill="both", expand=True)

        # Create a frame for the radio buttons
        frame = ttk.LabelFrame(left_frame, text="Select Type of channels to import")
        frame.pack(padx=10, pady=10, fill="x")

        # Create radio buttons
        radio_digital = ttk.Radiobutton(frame, text="Digital", variable=self.__channel_type_var, value="digital")
        radio_digital_analog = ttk.Radiobutton(frame, text="Digital & Analog", variable=self.__channel_type_var, value="digital_analog")

        # Pack radio buttons
        radio_digital.pack(anchor="w", padx=10, pady=5)
        radio_digital_analog.pack(anchor="w", padx=10, pady=5)
        
        # Display dropbox to pick firmware version
        firmwareFrame = ttk.LabelFrame(left_frame, text="Select firmware version")
        firmwareFrame.pack(padx=10, pady=10, fill="x")
        firmwareOptions = self.__specs.getFirmwareVersions()
        firmwareComboBox = ttk.Combobox(firmwareFrame, values=firmwareOptions)
        firmwareComboBox.set(firmwareOptions[0])
        self.__firmware_version_var.set(firmwareOptions[0])
        firmwareComboBox.pack(side="left", pady=10)
        self.__combobox = firmwareComboBox
        firmwareComboBox.bind("<<ComboboxSelected>>", self.__assignFirmwareVersion)

        # Set directories buttons
        directoryFrame = ttk.LabelFrame(left_frame, text="Select directories")
        directoryFrame.pack(padx=10, pady=10, fill="x")

        btn_select_input_dir = ttk.Button(directoryFrame, text="Select input directory", command=self.__select_input_directory)
        btn_select_output_dir = ttk.Button(directoryFrame, text="Select output directory", command=self.__select_output_directory)

        # Convert codeplug and exit buttons
        actionFrame = ttk.LabelFrame(left_frame, text="Select action")
        actionFrame.pack(padx=10, pady=10, fill="x")

        btn_convert_codeplug = ttk.Button(actionFrame, text="Convert Codeplug", command=convert_codeplug)
        btn_exit = ttk.Button(actionFrame, text="Exit", command=exit_application)

        # Pack buttons and labels
        btn_select_input_dir.pack(padx=10, pady=5, fill="x")
        ttk.Label(directoryFrame, textvariable=self.__input_directory_var).pack(padx=10, pady=5, fill="x")

        btn_select_output_dir.pack(padx=10, pady=5, fill="x")
        ttk.Label(directoryFrame, textvariable=self.__output_directory_var).pack(padx=10, pady=5, fill="x")

        btn_convert_codeplug.pack(padx=10, pady=5, fill="x")
        btn_exit.pack(padx=10, pady=5, fill="x")


        # Create a frame for the debug output
        debug_frame = ttk.LabelFrame(right_frame, text="Debug Output")
        debug_frame.pack(side="left", padx=10, pady=10, fill="both", expand=True)

        # Create a label to display the debug output
        debug_output_label = ttk.Label(debug_frame, textvariable=self.__debug_output_var)
        debug_output_label.pack(side="top", padx=10, pady=10)


        # Read CSV and set variables if the file exists
        try:
            self.__read_csv_and_set_variables(self.__configFolderPath + '/CS7000_convert_settings.csv')

            # Config file is present.  Set value of combo box to last value used
            firmwareComboBox.set(self.__firmware_version_var.get() )


        except FileNotFoundError:
            debug_output('Did not find CS7000_covert_setting.csv.  Please select location of files')
            pass

        #
        self.__debug_DisplaySpecs()
        # resize the window
        self.geometry("1200x500+0+0")
        self.__raise_above_all()

    def __assignFirmwareVersion(self,event):
        self.__firmware_version_var.set(self.__combobox.get())
        self.__debug_DisplaySpecs()
        print("Selected firmware version: " + self.__firmware_version_var.get())


    def __read_csv_and_set_variables(self,file_path):
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
            firmware_version = variables.get('Firmware Version' , '')

            # Check if firmware_version from config file is blank.  If so set it to default firmware version
            if ( firmware_version == ''):
                firmware_version = self.__specs.getFirmwareVersions()[0]
            
            self.__input_directory_var.set(f"Selected directory: {input_directory}")
            self.__output_directory_var.set(f"Selected directory: {output_directory}")
            self.__channel_type_var.set(f"{channel_type}")
            self.__firmware_version_var.set(f"{firmware_version}")

            self.debug_output('Read settings from CS7000_convert_setting.csv')
        file.close()


    def __getDisclaimerText(self):
        # Read in DISCLAIMER statement
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")

        file_path = os.path.join(base_path, "DISCLAIMER.txt.asc")
        with open(file_path, 'r') as file:
            disclaim_text = file.read()
        file.close()
        return disclaim_text

    def __raise_above_all(window):
        window.attributes('-topmost', 1)
        window.attributes('-topmost', 0)


def accept_terms():
    print("Accepted terms of user")
    app.createMainWindow()

def reject_terms():
    print("Rejected terms of use")
    app.destroy()


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

def convert_codeplug():
    app.debug_output('Now converting files into format for CS7000')

    input_directory = getDirectoryname(app.getInput_directory() )
    output_directory = getDirectoryname(app.getOutput_directory() )

    contacts_file = input_directory + "/Talkgroups.CSV"
    channels_file = input_directory + "/Channel.CSV"
    zones_file = input_directory + "/Zone.CSV"

    # Convert contact file
    converted_contacts_file = output_directory + "/CS7000_contacts.xlsx"
    contacts = DigitalContacts(contacts_file, converted_contacts_file, app.getMaxContacts())
    contacts.Convert()
    app.debug_output("Converted talkgroup file in " + converted_contacts_file)

    # Check if there were talk groups not imported
    #     output talk groups not imported to notImported.xls

    if (contacts.numNotImported != 0):
        app.debug_output("WARNING:  Did not import " + str(contacts.numNotImported) + " talkgroups.  Check notImported.xls")
        contacts.outputTalkGroupsNotImported( output_directory + "/CS7000_notImported.xlsx")


    # Convert channels file
    if ( app.getChannel_type() == "digital_analog"):
        includeAnalogChannels = True
    else:
        includeAnalogChannels = False

    app.debug_output("Including analog channels in conversion is " + str(includeAnalogChannels))

    converted_channels_file = output_directory + "/CS7000_channels.xlsx"
    channels = Channels(channels_file, converted_channels_file, includeAnalogChannels)
    uhfChannels = channels.Convert()
    app.debug_output("Converted channels to " +  converted_channels_file)

    # Convert zones file
    converted_zones_file = output_directory + "/CS7000_zones.xlsx"
    zones = Zones(zones_file, converted_zones_file, uhfChannels)
    zones.Convert()
    app.debug_output("Converted zones file in " + converted_zones_file)
    
    open_file_explorer(output_directory)
    app.debug_output("Now opening folder containing converted output files")

def exit_application():
    input_directory = getDirectoryname(app.getInput_directory() )
    output_directory = getDirectoryname(app.getOutput_directory() )
    channel_type = app.getChannel_type()
    firmware_version = app.getFirmware_version()

    with open(app.getConfigFolderPath() + '/CS7000_convert_settings.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Input Directory', 'Output Directory', 'Channel Type', 'Firmware Version'])
        writer.writerow([input_directory, output_directory, channel_type, firmware_version])
   
    file.close()
    app.destroy()

#### Start of application

# Create the main application window
try:
    import pyi_splash
    pyi_splash.close()
except:
    pass

# Create app
app = MyApp()


# Start the main event loop
app.mainloop()
