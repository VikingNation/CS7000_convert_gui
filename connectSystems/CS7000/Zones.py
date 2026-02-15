#!/bin/env python
import csv
from hashlib import sha256
import xlsxwriter

class Zones:

    def __init__(self, input_file, output_file, uhfChannels):
        self.input_file = input_file
        self.output_file = output_file

        self._fileType = ''
        self._setArrays()

        self._uhfChannels = uhfChannels.copy()

        # This will hold the list of Zones and channels for each zone
        self._zonesDict = {}   # key = zone name, value = list of channels
        self._channelFilterProvide = False

        if len(self._uhfChannels) == 0:
            self._channelFilterProvided = False
        else:
            self._channelFilterProvided = True

        self.load(input_file)

    def getNumberZones(self):
        return len(self._zonesDict)

    def load(self, input_file):
        self.input_file = input_file
        self._DetermineFileType()

        if (self._fileType == "Anytone"):
            self._loadAnytoneFile(self.input_file)

        if (self._fileType == "CS7000"):
            self._loadCS7000File(self.input_file)

    def _loadCS7000File(self, input_file):
        with open(input_file, mode='r', newline='') as infile:
            reader = csv.reader(infile)

            rowsRead = 0
            for row in reader:
                rowsRead += 1

                # Skip header row
                if rowsRead == 1:
                    continue

                if not row:
                    continue  # skip empty rows

                key = row[1].strip()
                values = [col.strip() for col in row[2:] if col.strip() != ""]

                # Store in dictionary
                self._zonesDict[key] = values

    def _loadAnytoneFile(self, input_file):

        """
        Load the Anytone Zones CSV into a dictionary:
        {
            "Zone Name": ["CH1", "CH2", ...],
            ...
        }
        """
        with open(input_file, mode='r', newline='') as infile:
            reader = csv.reader(infile)

            rowsRead = 0
            for row in reader:
                rowsRead += 1

                # Skip header row
                if rowsRead == 1:
                    continue

                zoneName = row[1]
                zoneList = row[2]
                parsedZones = zoneList.split("|")

                # Filter channels if needed
                filtered = []
                for ch in parsedZones:
                    if self._channelFilterProvided:
                        if ch in self._uhfChannels:
                            filtered.append(ch)
                    else:
                        filtered.append(ch)

                # Only store zones that have at least one valid channel
                if len(filtered) > 0:
                    self._zonesDict[zoneName] = filtered

    def Convert(self):
        if self._fileType in ("Anytone", "CS7000"):
            self.writeToSpreadsheet()
        else:
            print(f"Error: Cannot convert input file of type {self._fileType}")

    def writeToSpreadsheet(self):
        """
        Convert the loaded zone dictionary into an XLSX spreadsheet.
        Assumes load() has already been called.
        """

        workbook = xlsxwriter.Workbook(self.output_file)
        worksheet = workbook.add_worksheet("Zones")

        # Write header row
        col = 0
        for colVal in self._zoneHeader:
            worksheet.write(0, col, colVal)
            col += 1

        # Write zone rows
        rowNum = 1
        for zoneName, channelList in self._zonesDict.items():
            col = 0
            worksheet.write(rowNum, col, rowNum)      # Row number
            col += 1
            worksheet.write(rowNum, col, zoneName)    # Zone name
            col += 1

            # Write channels
            for ch in channelList:
                worksheet.write(rowNum, col, ch)
                col += 1

            rowNum += 1

        workbook.close()

    def ConvertAnytoneZones(self):
        # Read and parse input file
        # Get input and output file names from arguments
        input_file = self.input_file
        output_file = self.output_file

        workbook = xlsxwriter.Workbook(output_file)
        worksheet = workbook.add_worksheet("Zones")

        # Open the input file for reading
        with open(input_file, mode='r', newline='') as infile:
            reader = csv.reader(infile)

            rowNum = 1
            rowsRead = 1

            # Output the header row
            col = 0
            for colVal in self._zoneHeader:
                worksheet.write(0, col, colVal)
                col = col + 1

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
                    if self._channelFilterProvided:
                        if element in self._uhfChannels:
                          outputRow.append(element)
                    else:
                        outputRow.append(element)

                # Check if there are any UHF channels in this zone
                # first two elements of row are row number and zonename
                if (rowsRead > 1) and (len(outputRow) >= 3):
                    # There are UHF channels.  Output row and increment row number
                    col = 0
                    for colVal in outputRow:
                        worksheet.write(rowNum, col, colVal)
                        col = col + 1
                    rowNum = rowNum + 1

                rowsRead = rowsRead + 1

        infile.close()
        workbook.close()

    def _DetermineFileType(self):

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
                        self._fileType = 'Anytone'
                    else:
                        if (headerHash == "2605fff2695866bc2a595bb607044cd15829cb5f9e6e4056ad9eb792b761704a"):
                            self._fileType = 'CS7000'
                        else:
                            self._fileType = 'UNKNOWN'
                            print(f"Error: Unknown CSV input file. Header hash is {headerHash}")

                numRows = numRows + 1

            self._rowsInFile = numRows

        infile.close(

                )
    def _setArrays(self):
        # Constrcut header row
        channels = [f"Channel {i}" for i in range(1, 2001)]

        self._zoneHeader = [
            "No.",
            "Zone Alias",
        ]

        for element in channels:
            self._zoneHeader.append(element)


