#!/bin/env python
import sys
from connectSystems.CS7000.Channels import Channels

# ---------------------------------------------------------
# PARSE ARGUMENTS
# ---------------------------------------------------------

include_default = False   # default behavior

stock_analog_channel_file = "codeplugs\\CS7000_M17_PLUS_V9.00.93_analog_channels.csv"
stock_digital_channel_file = "codeplugs\\CS7000_M17_PLUS_V9.00.93_digital_channels.csv"

# Minimum args = script + input + output
# Optional args = -i / --include-default
args = sys.argv[1:]

if len(args) < 2:
    print("Usage: python AnytoneChannels2_CS7000_Channels.py [options] input_file.csv output.xlsx")
    print("")
    print("Options:")
    print("   -i, --include-default    Include default channels in output")
    print("")
    print("Convert Anytone CPS Channels File (CSV format) into column xlsx format")
    print("to import into the Connect Systems CS7000 channels.")
    print("")
    print("Credits: Jason Johnson (k3jsj@arrl.net), https://github.com/K3JSJ/CS7000")
    print("")
    sys.exit(1)

# Detect optional flag
if args[0] in ("-i", "--include-default"):
    include_default = True
    args = args[1:]  # shift remaining args

# After shifting, args must contain exactly 2 items
if len(args) != 2:
    print("Error: Missing input or output file.")
    print("Usage: python AnytoneChannels2_CS7000_Channels.py [options] input_file.csv output.xlsx")
    sys.exit(1)

print(f"Args is {args}")
input_file = args[0]
output_file = args[1]

if include_default:
    print("Including default channels (stub logic here)")
    # ---------------------------------------------------------
    # TODO: Add your logic here to include default channels
    # Example:
    # channels.addDefaultChannels()
    # ---------------------------------------------------------
    channels = Channels(stock_analog_channel_file, output_file, True)
    channels.load(stock_digital_channel_file)
    channels.load(input_file)
else:
    channels = Channels(input_file, output_file, True)

channels.Convert()

