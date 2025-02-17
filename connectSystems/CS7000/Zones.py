#!/bin/env python
import csv
from hashlib import sha256
import xlsxwriter

class Zones:

    def __init__(self, input_file, output_file, maxZones, channels):
        self.input_file = input_file
        self.output_file = output_file

        self.__maxZones = maxZones
        self.__fileType = ''
        self.__DetermineFileType()
        self.__setArrays()
        self.__channels = channels

        self.numNotImported = 0
        self.numImported = 0

        self.__dictZonesNotImported = None

    def checkNotImported(self, zoneName):
        if (self.__dictNotImported == None):
            return False

        if (zoneName in self.__dictZonesNotImported):
            return True
        else:
            return False
    
    def outputZonesNotImported(self,output_file):
        if (self.numNotImported == 0):
            return 0

        # Write list of Zones not imported
        colNum = 0
        
        workbook = xlsxwriter.Workbook(output_file)
        worksheet = workbook.add_worksheet("ZonesNotImported")
        
        colNum=0
        for col in self.__zoneHeader:
            worksheet.write(0,colNum,col)
            colNum = colNum + 1
        rowNum = 1
        for k in self.__dictZonesNotImported.keys():
            zone = self.__dictZonesNotImported[k]
            worksheet.write(rowNum,0,rowNum)
            worksheet.write(rowNum,1,zone)

            rowNum = rowNum + 1
        workbook.close()

    def Convert(self):
        if self.__fileType == "Anytone":
            try:
                self.ConvertAnytoneZones()
            except Exception as e:
                print(f"In Zones.py.Convert() caught an exception {type(e).__name__}")
                print(f"{e}")
                raise e

    def ConvertAnytoneZones(self):
        # Read and parse input file
        # Get input and output file names from arguments
        input_file = self.input_file
        output_file = self.output_file

        encounteredException = False
        try:
            workbook = xlsxwriter.Workbook(output_file)
        except Exception as e:
            encounteredException = True
            raise e

        if (encounteredException == True):
            print(f"In Zones.py.ConvertAnytoneZones() encountered exception")
            return -1

        worksheet = workbook.add_worksheet("Zones")

        # Open the input file for reading
        with open(input_file, mode='r', newline='') as infile:
            reader = csv.reader(infile)

            rowNum = 1
            rowsRead = 1

            # Output the header row
            col = 0
            for colVal in self.__zoneHeader:
                worksheet.write(0, col, colVal)
                col = col + 1

            # Process each row in the input file
            for row in reader:
                outputRow = []
                # Extract values from input file
                zoneName = row[1]
                zoneList = row[2]
                # Append row number, Zone Name, and List of channels in Zone
                outputRow.append(rowsRead)
                outputRow.append(zoneName)
                parsedZones = zoneList.split("|")
                for element in parsedZones:
                    # Verify that channel is UHF before we add it to the Zone list
                    if self.__channels.checkNotImported(element):
                        print("Filtering out channel " + element + " from zone ")
                    else:
                        outputRow.append(element)

                # Check if there are any UHF channels in this zone
                # first two elements of row are row number and zonename
                if (rowsRead > 1) and (len(outputRow) >= 3):
                    # There are UHF channels.  Output row and increment row number
                    col = 1
                    if (rowNum <= self.__maxZones):
                        worksheet.write(rowNum,0,rowNum)
                        for colVal in outputRow[1:]:
                            worksheet.write(rowNum, col, colVal)
                            col = col + 1
                        self.numImported = self.numImported + 1
                        rowNum = rowNum + 1
                    else:
                        self.numNotImported = self.numNotImported + 1
                        print("Filtering out zone " + outputRow[1] + " exceeded maximum zones")

                        if (self.__dictZonesNotImported == None):
                            self.__dictZonesNotImported = { outputRow[0] : outputRow[1]}
                        else:
                            self.__dictZonesNotImported[outputRow[0]] = outputRow[1]
                else:
                    # Check to skip over the header row
                    if (rowsRead > 1) and (len(outputRow) < 3):
                        # Zone does not contain any channels
                        #   add it to not import list
                        print("Filtering out zone " + outputRow[1] + " does not contain any channels. " + str(outputRow[0]))
                        self.numNotImported = self.numNotImported + 1
                        if (self.__dictZonesNotImported == None):
                            self.__dictZonesNotImported = { outputRow[0] : outputRow[1]}
                        else:
                            self.__dictZonesNotImported[outputRow[0]] = outputRow[1]
                
                rowsRead = rowsRead + 1

        infile.close()
        workbook.close()

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


