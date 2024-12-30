#!/bin/env python
import sys
from connectSystems.CS7000.Channels import Channels

# Check for correct number of arguments
if len(sys.argv) != 4:
    print("Usage: python AnytoneChannels2_CS7000_Channels.py input_file.csv output_dmr_channels.csv output_analog_channels.csv")
    print("       Convert Anytone CPS Channels File (CSV format) into column format to add to Connect System Contacts spreadsheet.")
    print("")
    print("       Credits:  Jason Johnson (k3jsj@arrl.net), https://github.com/K3JSJ/CS7000 ")
    print("")      
    sys.exit(1)



input_file = sys.argv[1]
output_file_dmr = sys.argv[2]
output_file_analog = sys.argv[3]

channels = Channels(input_file, output_file_dmr, output_file_analog, True)
channels.Convert()

