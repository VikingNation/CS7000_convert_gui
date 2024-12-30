#!/bin/env python
import csv
from hashlib import sha256

class Zones:

    def __init__(self, input_file, output_file, uhfChannels):
        self.input_file = input_file
        self.output_file = output_file

        self.__fileType = ''
        self.__DetermineFileType()
        self.__setArrays()
        self.__uhfChannels = uhfChannels.copy()

        if len(self.__uhfChannels) == 0:
            self.__channelFilterProvided = False
        else:
            self.__channelFilterProvided = True



    def Convert(self):
        if self.__fileType == "Anytone":
            self.ConvertAnytoneZones()

    def ConvertAnytoneZones(self):
        # Read and parse input file
        # Get input and output file names from arguments
        input_file = self.input_file
        output_file = self.output_file

        # Open the input file for reading
        with open(input_file, mode='r', newline='') as infile:
            reader = csv.reader(infile)

            # Open the output file for writing
            with open(output_file, mode='w', newline='') as outfile:
                writer = csv.writer(outfile)
                rowNum = 1
                rowsRead = 1
                # Output header row
                writer.writerow(self.__zoneHeader)
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
                        # Verify that channel is UHF before we add it to the Zone list
                        if self.__channelFilterProvided:
                            if element in self.__uhfChannels:
                              outputRow.append(element)
                            else:
                                print("Channel ", element, " is not a UHF channel")
                        else:
                            outputRow.append(element)

                    # Check if there are any UHF channels in this zone
                    # first two elements of row are row number and zonename
                    if (rowsRead > 1) and (len(outputRow) >= 3):
                        # There are UHF channels.  Output row and increment row number
                        writer.writerow(outputRow)
                        rowNum = rowNum + 1

                    rowsRead = rowsRead + 1

        infile.close()
        outfile.close()

    def __DetermineFileType(self):

        with open(self.input_file, mode='r', newline='') as infile:
            reader = csv.reader(infile)
            numRows = 0
            for row in reader:
                if numRows == 0:
                    s = ''

                    for e in enumerate(row):
                        s = s + e[1]

                    headerHash = sha256(s.encode('utf-8')).hexdigest()
                    if (headerHash == "172acbf54bc6379f2a53781c1f6f486b92c8b0b229ea9778b8b328c9158a04da"):
                        self.__fileType = 'Anytone'

                numRows = numRows + 1

            self.__rowsInFile = numRows

        infile.close(

                )
    def __setArrays(self):
        # Constrcut header row
        channels = [f"Channel {i}" for i in range(1, 2001)]

        self.__zoneHeader = [
            "No.",
            "Zone Alias",
        ]

        for element in channels:
            self.__zoneHeader.append(element)


