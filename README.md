# CS7000 Code Plug Utilities

Author:  Jason Johnson (k3jsj@arrl.net)


## Purpose
Utilities to convert Anytone Talk Group, Channels, and Zones CSV files into format the CS7000 CPS uses.  Python programs convert Contacts, Channels, and Zones.  Channels support creation of CSV file for DMR and Analog channels.

## Usage
The following are steps to use the program:

### Anytone CPS
- Open Anytone CPS and explort Talkgroups, Zones, and Channels

## Operating system command prompt
- Launch the gui, python CS7000_convert_gui.py.
- Click the buttons to Select the contacts, channels, and zones file. Click the button to Select the output folder to save converted files.
- Finally, click the Convert Codeplug button to convert files into CSV format the CS700 expects
- Alternativly to gui you can run scripts against talkgroups, zones, and channels to create CSVs 

### CS7000 CPS
- Export Contacts, Channels, and Zones from CS7000 CPS software into spreadsheets.

### Excel
- Open convered talkgroups CSV in Excel and copy values.  Next, do a paste-special into the CS7000 Contacts spreadsheet.  Save the file.
- Open the converted DMR channels CSV in Excel and copy values.  Select the DMR channels worksheets.  Past special into the CS7000 spreadsheet.  Save the file.
- Repeat at above step again for analog channels CSV.
- Open the converted zones CSV in Excel and copy values.  Past special in to the zones spreadsheet. Save the file

### CS7000 CPS
- Open the CS7000 CPS.
- Import the contacts spreadsheet
- Import the channels spreadsheet
- Import the zones spreadsheet
- Verify everthing imported correctly
