#!/bin/env python
import sys
from connectSystems.CS7000.Channels import Channels

# Check for correct number of arguments
if len(sys.argv) != 3:
    print("Usage: python AnytoneChannels2_CS7000_Channels.py input_file.csv output.xlsx")
    print("       Convert Anytone CPS Channels File (CSV format) into column xlsx format to import into the Connect System channels.")
    print("")
    print("       Credits:  Jason Johnson (k3jsj@arrl.net), https://github.com/K3JSJ/CS7000 ")
    print("")      
    sys.exit(1)



input_file = sys.argv[1]
output_file = sys.argv[2]

channels = Channels(input_file, output_file, True)
channels.Convert()

