#!/bin/env python
import csv
import sys
from decimal import Decimal


# Check for correct number of arguments
if len(sys.argv) != 3:
    print("Usage: python AnytoneZones2_CS7000_Zones.py input_file.csv output_file.csv")
    print("       Convert Anytone CPS Zones File (CSV format) into column format to add to Connect System Zones spreadsheet.");
    print("")
    print("       Credits:  Jason Johnson (k3jsj@arrl.net), https://github.com/K3JSJ/CS7000 ")
    print("")      
    sys.exit(1)

# Constrcut header row

channels = [f"Channel {i}" for i in range(1, 2001)]

header = [
    "No.",
    "Zone Alias",
]

for element in channels:
    header.append(element)


# Read and parse input file

# Get input and output file names from arguments
input_file = sys.argv[1]
output_file = sys.argv[2]

# Open the input file for reading
with open(input_file, mode='r', newline='') as infile:
    reader = csv.reader(infile)
    
    # Open the output file for writing
    with open(output_file, mode='w', newline='') as outfile:
        writer = csv.writer(outfile)
       
        rowNum = 1
        rowsRead = 1
        # Output header row
        writer.writerow(header)
        # Process each row in the input file
        for row in reader:

            outputRow = []
            # Extract values from input file
            zoneName = row[1]
            zoneList = row[2]

            # Append row number, Zone Name, and List of channels in Zone
            outputRow.append(rowNum)
            outputRow.append(zoneName)


            parsedZones = zoneList.split("|")
            for element in parsedZones:
                outputRow.append(element)

            if rowsRead > 1:
                writer.writerow(outputRow)
                rowNum = rowNum + 1

            rowsRead = rowsRead + 1
