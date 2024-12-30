#!/bin/env python
import sys
from connectSystems.CS7000.Zones import Zones


# Check for correct number of arguments
if len(sys.argv) != 3:
    print("Usage: python AnytoneZones2_CS7000_Zones.py input_file.csv output_file.csv")
    print("       Convert Anytone CPS Zones File (CSV format) into column format to add to Connect System Zones spreadsheet.");
    print("       Note:  if there are VHF channels they will not be eliminated using this utility")
    print("")
    print("       Credits:  Jason Johnson (k3jsj@arrl.net), https://github.com/K3JSJ/CS7000 ")
    print("")      
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

zones = Zones(input_file, output_file, [])
zones.Convert()
