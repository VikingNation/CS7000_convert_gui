#!/bin/env python
import csv
import sys

# Output file columns
# No, Call Alias, Call Type, Call ID, Receive Tone

# Check for correct number of arguments
if len(sys.argv) != 3:
    print("Usage: python script.py input_file output_file")
    print("       Convert Anytone CPS CSV Talk group file into column format to add to Connect System Contacts spreadsheet.");
    sys.exit(1)

# Get input and output file names from arguments
input_file = sys.argv[1]
output_file = sys.argv[2]

# Open the input file for reading
with open(input_file, mode='r', newline='') as infile:
    reader = csv.reader(infile)
    
    # Open the output file for writing
    with open(output_file, mode='w', newline='') as outfile:
        writer = csv.writer(outfile)
        
        # Process each row in the input file
        for row in reader:
            number = row[0]
            radio_id = row[1]
            call_alias = row[2]
            call_type = row[3]
            receive_tone = row[4]
            writer.writerow([number, call_alias, call_type, radio_id, receive_tone])

