#!/bin/env python
import sys
from DigitalContacts import DigitalContacts

# Output file columns
# No, Call Alias, Call Type, Call ID, Receive Tone

# Check for correct number of arguments
if len(sys.argv) != 3:
    print("Usage: python AnytonTalkGroups2_CS7000_Contacts.py input_file.csv output_file.csv")
    print("       Convert Anytone CPS Talk group file (CSV format) into column format to add to Connect System Contacts spreadsheet.");
    print("")
    print("       Credits:  Jason Johnson (k3jsj@arrl.net), https://github.com/K3JSJ/CS7000 ")
    print("")
    sys.exit(1)


# Get input and output file names from arguments
input_file = sys.argv[1]
output_file = sys.argv[2]


# 
contacts = DigitalContacts(input_file, output_file)
contacts.Convert()
