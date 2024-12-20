#!/bin/env python
import csv
import sys
from decimal import Decimal


# Check for correct number of arguments
if len(sys.argv) != 3:
    print("Usage: python AnytoneChannels2_CS7000_Channels.py input_file.csv output_file.csv")
    print("       Convert Anytone CPS Channels File (CSV format) into column format to add to Connect System Contacts spreadsheet.");
    print("")
    print("       Credits:  Jason Johnson (k3jsj@arrl.net), https://github.com/K3JSJ/CS7000 ")
    print("")      
    sys.exit(1)


# Header row for CS7000
header = [
    "No.",
    "Channel Alias",
    "Digital ID [Per Each Channel]",
    "Color Code",
    "Slot Operation",
    "Scan/Roam/Vote List",
    "Auto Start Scan",
    "Rx Only",
    "Talk Around",
    "Lone Worker",
    "VOX",
    "Receive Frequency [MHz]",
    "Rx Ref Frequency",
    "Rx Group List",
    "Emergency Alarm Indication",
    "Emergency Alarm Ack",
    "Emergency Call Indication",
    "Transmit Frequency [MHz]",
    "Tx Ref Frequency",
    "Tx Contact Name",
    "Emergency System",
    "Power Level",
    "Tx Admit",
    "Tx Time-Out Time [s]",
    "TOT Re-Key Time [s]",
    "TOT Pre-Alert Time [s]",
    "Private Call Confirmed",
    "Data Call Confirmed",
    "Encryption",
    "Encryption Type",
    "Encryption Key List",
    "Pseudo Trunk",
    "Pseudo Trunk Designated TX",
    "Pilot_Freq Direct Mode",
    "Easy Trunking Mode",
    "Easy Trunking Sites",
    "TDMA Direct Mode",
    "Digital Channel Type",
    "IP Multi-site Connect",
    "Scan/Roam/Vote Mode",
    "Auto Start Roam",
    "Auto Start Voting",
    "In Call Criteria",
    "Text Message Format",
    "Encryption Ignore RX Clear Voice",
    "Compressed UDP Data Header"
]


defaultRow = [
    "1",
    "DMR Smplx 441",
    "4",
    "1",
    "Slot 2",
    "None",
    "Off",
    "Off",
    "Off",
    "Off",
    "Off",
    "441",
    "Middle",
    "None",
    "Off",
    "Off",
    "Off",
    "441",
    "Middle",
    "None",
    "None",
    "High",
    "Always",
    "60",
    "0",
    "0",
    "Off",
    "Off",
    "Off",
    "Full",
    "Key 1",
    "Off",
    "Fixed",
    "Off",
    "Single-Repeater",
    "None",
    "Off",
    "Digital Channel",
    "Off",
    "None",
    "Off",
    "Off",
    "Follow Admit Criteria",
    "DMR Standard",
    "Off",
    "None"
]


# Get input and output file names from arguments
input_file = sys.argv[1]
output_file = sys.argv[2]

# Open the input file for reading
with open(input_file, mode='r', newline='') as infile:
    reader = csv.reader(infile)
    
    # Open the output file for writing
    with open(output_file, mode='w', newline='') as outfile:
        writer = csv.writer(outfile)
       
        outputRow = defaultRow[:]
        rowNum = 1
        # Output header row
        writer.writerow(header)
        # Process each row in the input file
        for row in reader:
            # Extract values from input file
            channelName = row[0]
            mode = row[1]
            rx_freq = row[4]
            tx_freq = row[3]
            call_alias = row[36]
            timeslot = row[41]
            colorCode = row[38]

           
	        # Prepare value for output file
            outputRow[0] = rowNum
            outputRow[1] = channelName

            # output digital id per channel
            outputRow[2] = rowNum
            outputRow[3] = colorCode
	   
            if Decimal(timeslot) == 1:
              outputRow[4] = "Slot 1"
            else:
              outputRow[4] = "Slot 2"

            outputRow[11] = rx_freq
            outputRow[17] = tx_freq

            if call_alias == "-NULL-":
                outputRow[19] = "None"
            else:
                outputRow[19] = call_alias

	        # If frequency UHF and mode DMR then output record
            if (Decimal(rx_freq) >= 400) and ( mode == "DMR"): 
                writer.writerow(outputRow)
                rowNum = rowNum + 1
