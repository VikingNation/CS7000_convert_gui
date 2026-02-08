#!/bin/env python
import os
import sys
from connectSystems.CS7000.Zones import Zones

def delete_if_exists(filename):
        if os.path.exists(filename):
            try:
                os.remove(filename)
                print(f"Deleted existing file: {filename}")
            except PermissionError:
                print(f"Cannot delete '{filename}' — the file is open or locked.")
            except Exception as e:
                print(f"Unexpected error deleting '{filename}': {e}")
        else:
            print(f"No existing file to delete: {filename}")

# ---------------------------------------------------------
# PARSE ARGUMENTS
# ---------------------------------------------------------

include_default = False   # default behavior

stock_zones_file = "codeplugs\\CS7000_M17_PLUS_V9.00.93_zones.csv"

# Minimum args = script + input + output
# Optional args = -i / --include-default
args = sys.argv[1:]

if len(args) > 0 and args[0] in ("-i", "--include-default"):
    include_default = True
    args = args[1:] # shift remaining args

# Check for correct number of arguments
if len(args) != 2:
    print("Usage: python AnytoneZones2_CS7000_Zones.py [options] input_file.csv output_file.xlsx")
    print("")
    print("Options:")
    print("   -i, --include-default    Include default zones from the firmware in output")
    print("")
    print("Convert Anytone CPS Zones File (CSV format) into spreadsheet to import into Connect System CPS.");
    print("Note:  if there are VHF channels they will not be eliminated using this utility")
    print("")
    print("Credits:  Jason Johnson (k3jsj@arrl.net), https://github.com/K3JSJ/CS7000 ")
    print("")
    sys.exit(1)

input_file = args[0]
output_file = args[1]

if include_default:
    delete_if_exists(output_file)
    print(f"Loading stock firmware zones from {stock_zones_file}")
    zones = Zones(stock_zones_file, output_file, [])
    print(f"Loading Anytone Zones file {input_file}")
    zones.load(input_file)
else:
    print(f"Loading Anytone Zones file {input_file}")
    zones = Zones(input_file, output_file, [])

print(f"Saving converted Zones for CS7000 into file {output_file}")
zones.Convert()
