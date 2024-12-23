#!/bin/env python
import csv
import sys
from decimal import Decimal


# Check for correct number of arguments
if len(sys.argv) != 4:
    print("Usage: python AnytoneChannels2_CS7000_Channels.py input_file.csv output_dmr_channels.csv output_analog_channels.csv")
    print("       Convert Anytone CPS Channels File (CSV format) into column format to add to Connect System Contacts spreadsheet.")
    print("")
    print("       Credits:  Jason Johnson (k3jsj@arrl.net), https://github.com/K3JSJ/CS7000 ")
    print("")      
    sys.exit(1)


# Header row for CS7000
header_dmr = [
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


defaultRow_dmr = [
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



defaultRow_analog = [
    "1",
    "Channel 4",
    "Normal",
    "25.0",
    "Personality 1",
    "None",
    "Off",
    "Off",
    "Off",
    "Off",
    "Off",
    "441.00",
    "NONE",
    "NONE",
    "Middle",
    "CTCSS/CDCSS and Audio",
    "Carrier",
    "RX Squelch Mode",
    "441.00",
    "NONE",
    "NONE",
    "Middle",
    "High",
    "Aways Allow",
    "None",
    "Off",
    "60",
    "0",
    "0",
    "180",
    "None",
    "Off",
    "Off"
]


header_analog = [
    "No.",
    "Channel Alias",
    "Carrier Squelch Level",
    "Channel Spacing [KHz]",
    "Personality List",
    "Scan/Roam/Vote List",
    "Auto Start Scan",
    "Rx Only",
    "Talk Around",
    "Lone Worker",
    "VOX",
    "Receive Frequency [MHz]",
    "Rx CTCSS/CDCSS Type",
    "CTCSS/CDCSS Type",
    "Rx Ref Frequency",
    "Rx Squelch Mode",
    "Monitor Squelch Mode",
    "Channel Switch Squelch Mode",
    "Transmit Frequency [MHz]",
    "Tx CTCSS/CDCSS Type",
    "CTCSS/CDCSS Type",
    "Tx Ref Frequency",
    "Power Level",
    "Tx Admit",
    "Emergency System",
    "CTCSS Tail Revert",
    "Tx Time-Out Time [s]",
    "TOT Re-Key Time [s]",
    "TOT Pre-Alert Time [s]",
    "CTCSS Tail Revert Option [Radians]",
    "Scan/Roam/Vote Mode",
    "Auto Start Roam",
    "Auto Start Voting"
]

# Get input and output file names from arguments
input_file = sys.argv[1]
output_file_dmr = sys.argv[2]
output_file_analog = sys.argv[3]
# Open the input file for reading
with open(input_file, mode='r', newline='') as infile:
    reader = csv.reader(infile)
    
    # Open the output file for writing
    outfile_dmr = open(output_file_dmr, mode='w', newline='')
    outfile_analog = open(output_file_analog, mode='w', newline='')

    writer_dmr = csv.writer(outfile_dmr)
    writer_analog = csv.writer(outfile_analog) 
    outputRowDMR = defaultRow_dmr[:]
    outputRowAnalog = defaultRow_analog[:]

    # set output row number in dmr and analog files
    rowNum_dmr = 1
    rowNum_analog = 1

    # Output header row
    writer_dmr.writerow(header_dmr)
    writer_analog.writerow(header_analog)

    # Process each row in the input file
    for row in reader:
        # Extract DMR/analog shared values from input file
        channelName = row[0]
        mode = row[1]
        channelSpacing = row[2]
        tx_freq = row[3]
        rx_freq = row[4]


        # Extract mode specifci values from input file
        if ( mode == "DMR"):
            call_alias = row[36]
            timeslot = row[41]
            colorCode = row[38]
        else:
            ctcss_decode = row[18]
            ctcss_encode = row[19]


        if ( mode == "DMR"):
            # Prepare value for output file
            outputRowDMR[0] = rowNum_dmr
            outputRowDMR[1] = channelName

            # output digital id per channel
            outputRowDMR[2] = rowNum_dmr
            outputRowDMR[3] = colorCode
           
            if Decimal(timeslot) == 1:
              outputRowDMR[4] = "Slot 1"
            else:
              outputRowDMR[4] = "Slot 2"

            outputRowDMR[11] = rx_freq
            outputRowDMR[17] = tx_freq

            if call_alias == "-NULL-":
                outputRowDMR[19] = "None"
            else:
                outputRowDMR[19] = call_alias
        else:
            outputRowAnalog[0] = rowNum_analog
            outputRowAnalog[1] = channelName
            outputRowAnalog[3] = channelSpacing
            outputRowAnalog[11] = rx_freq
            outputRowAnalog[18] = tx_freq

            # Check if Transmit CTCSS is used
            if ctcss_encode != "NONE":
                outputRowAnalog[19] = "CTCSS"
                outputRowAnalog[20] = ctcss_encode
            else:
                outputRowAnalog[19] = "NONE"
                outputRowAnalog[20] = "NONE"

            if ctcss_decode != "NONE":
                outputRowAnalog[12] = "CTCSS"
                outputRowAnalog[13] = ctcss_decode
            else:
                outputRowAnalog[12] = "NONE"
                outputRowAnalog[13] = "NONE"


        if (Decimal(rx_freq) >= 400) and ( mode == "DMR"): 
            writer_dmr.writerow(outputRowDMR)
            rowNum_dmr = rowNum_dmr + 1

        if (Decimal(rx_freq) >= 400) and ( mode == "FM"):
            writer_analog.writerow(outputRowAnalog)
            rowNum_analog = rowNum_analog + 1
