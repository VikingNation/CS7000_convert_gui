import csv
import sys
from hashlib import sha256
from decimal import Decimal


class Channels:

    def __init__(self, input_file,output_file_dmr, output_file_analog, includeAnalogChannels):
        self.input_file = input_file
        self.output_file_dmr = output_file_dmr
        self.output_file_analog = output_file_analog

        self.__fileType = ''
        self.__DetermineFileType()

        self.__includeAnalogChannels = includeAnalogChannels
        self.__UhfChannels = {}
        # Setup header and default row records
        self.__SetArrays()

    def Convert(self):
        if self.__fileType == "Anytone":
            print("Converting anytone channels file")
            self.ConvertAnytoneChannels()
            self.LoadChannelNames(self.output_file_dmr, self.output_file_analog)
            return (self.__UhfChannels.copy())

        if self.__fileType == "CS7000":
            print("Input file is all ready is format for the CS7000.  Nothing to convert.")
        if self.__fileType == "ERROR":
            print("Error!  Input file is not the CSV format expected from Anytone CPS.")
            return (-1)


    def ConvertAnytoneChannels(self):
        # Get input and output file names from arguments
        input_file = self.input_file
        output_file_dmr = self.output_file_dmr 
        output_file_analog = self.output_file_analog

        # Open the input file for reading
        with open(input_file, mode='r', newline='') as infile:
            reader = csv.reader(infile)
            
            # Open the output file for writing
            outfile_dmr = open(output_file_dmr, mode='w', newline='')
            outfile_analog = open(output_file_analog, mode='w', newline='')

            writer_dmr = csv.writer(outfile_dmr)
            writer_analog = csv.writer(outfile_analog) 
            outputRowDMR = self.__defaultRow_dmr[:]
            outputRowAnalog = self.__defaultRow_analog[:]

            # set output row number in dmr and analog files
            rowNum_dmr = 1
            rowNum_analog = 1

            # Output header row
            writer_dmr.writerow(self.__header_dmr)
            writer_analog.writerow(self.__header_analog)

            readHeaderRow = 0
            # Process each row in the input file
            for row in reader:

                # Skip over the header row of the file
                if readHeaderRow == 0:
                    readHeaderRow = 1
                else:
                    # Extract DMR/analog shared values from input file
                    channelName = row[1]
                    mode = row[4]

                    if ( mode == "A-Analog"):
                        mode = "FM"
                    if ( mode == "D-Digital"):
                        mode = "DMR"

                    channelSpacing = row[6]

                    if ( channelSpacing == "25K"):
                        channelSpacing = 25.0
                    else:
                        channelSpacing = 12.5

                    tx_freq = row[3]
                    rx_freq = row[2]


                    # Extract mode specifci values from input file
                    if ( mode == "DMR"):
                        call_alias = row[9]
                        timeslot = row[21]
                        colorCode = row[20]
                    else:
                        ctcss_decode = row[7]
                        ctcss_encode = row[8]


                    if ( mode == "DMR"):
                        # Prepare value for output file
                        outputRowDMR[0] = rowNum_dmr
                        outputRowDMR[1] = channelName

                        # output digital id per channel
                        outputRowDMR[2] = rowNum_dmr
                        outputRowDMR[3] = colorCode
                       
                        if Decimal(timeslot) == 1:
                          outputRowDMR[4] = "Slot 1"
                        else:
                          outputRowDMR[4] = "Slot 2"

                        outputRowDMR[11] = rx_freq
                        outputRowDMR[17] = tx_freq

                        if call_alias == "-NULL-":
                            outputRowDMR[19] = "None"
                        else:
                            outputRowDMR[19] = call_alias
                    else:
                        outputRowAnalog[0] = rowNum_analog
                        outputRowAnalog[1] = channelName
                        outputRowAnalog[3] = channelSpacing
                        outputRowAnalog[11] = rx_freq
                        outputRowAnalog[18] = tx_freq

                        # Check if Transmit CTCSS is used
                        if ctcss_encode != "Off":
                            outputRowAnalog[19] = "CTCSS"
                            outputRowAnalog[20] = ctcss_encode
                        else:
                            outputRowAnalog[19] = "NONE"
                            outputRowAnalog[20] = "NONE"

                        if ctcss_decode != "Off":
                            outputRowAnalog[12] = "CTCSS"
                            outputRowAnalog[13] = ctcss_decode
                        else:
                            outputRowAnalog[12] = "NONE"
                            outputRowAnalog[13] = "NONE"


                    if (Decimal(rx_freq) >= 400) and ( mode == "DMR"):
                        writer_dmr.writerow(outputRowDMR)
                        rowNum_dmr = rowNum_dmr + 1

                    if (Decimal(rx_freq) >= 400) and ( mode == "FM") and self.__includeAnalogChannels:
                        writer_analog.writerow(outputRowAnalog)
                        rowNum_analog = rowNum_analog + 1

        infile.close()
        outfile_analog.close()
        outfile_dmr.close()

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
                    if (headerHash == "0599f2862ac011669d18fb17ecd7077bfa5e0b57584c3f7385fe0231d8b1e033"):
                        self.__fileType = 'Anytone'
                    else:
                        if (headerHash == "0f5e98e8c8aa9beb2dba3ad016070b300fb65b2c6cb2c5e6c4c8c2df7d1d9d4f"):
                            self.__fileType = 'CS7000'
                        else:
                            print("Could not determine type of input file\nHash of file header is ", headerHash)
                            self.__fileType = 'ERROR'

                numRows = numRows + 1

            self.__rowsInFile = numRows

        infile.close()

    def LoadChannelNames(self, dmr_channels, analog_channels):
        inputs = []
        inputs.append(dmr_channels)

        if (self.__includeAnalogChannels):
            inputs.append(analog_channels)

        processing_dmr_file = True
        for input_file in inputs:
            with open(input_file, mode='r', newline='') as infile:
                reader = csv.reader(infile)
                next(reader)
                for row in reader:
                    channelName = row[1]
                    channelSpacing = row[3]
                    rx_freq = row[11]
                    rx = Decimal(rx_freq)

                    if processing_dmr_file == True:
                        tx_freq = row[17]
                    else:
                        tx_freq = row[18]

                    tx = Decimal(tx_freq)
                    if ( (rx >= 400) and (rx <= 512)) and ((tx >= 400) and (tx <=512)):
                        self.__UhfChannels[channelName] = True
                infile.close()
                processing_dmr_file = False

    def __SetArrays(self):

        # Header row for CS7000
        self.__header_dmr = [
            "No.",
            "Channel Alias",
            "Digital ID [Per Each Channel]",
            "Color Code",
            "Slot Operation",
            "Scan/Roam/Vote List",
            "Auto Start Scan",
            "Rx Only",
            "Talk Around",
            "Lone Worker",
            "VOX",
            "Receive Frequency [MHz]",
            "Rx Ref Frequency",
            "Rx Group List",
            "Emergency Alarm Indication",
            "Emergency Alarm Ack",
            "Emergency Call Indication",
            "Transmit Frequency [MHz]",
            "Tx Ref Frequency",
            "Tx Contact Name",
            "Emergency System",
            "Power Level",
            "Tx Admit",
            "Tx Time-Out Time [s]",
            "TOT Re-Key Time [s]",
            "TOT Pre-Alert Time [s]",
            "Private Call Confirmed",
            "Data Call Confirmed",
            "Encryption",
            "Encryption Type",
            "Encryption Key List",
            "Pseudo Trunk",
            "Pseudo Trunk Designated TX",
            "Pilot_Freq Direct Mode",
            "Easy Trunking Mode",
            "Easy Trunking Sites",
            "TDMA Direct Mode",
            "Digital Channel Type",
            "IP Multi-site Connect",
            "Scan/Roam/Vote Mode",
            "Auto Start Roam",
            "Auto Start Voting",
            "In Call Criteria",
            "Text Message Format",
            "Encryption Ignore RX Clear Voice",
            "Compressed UDP Data Header"
        ]


        self.__defaultRow_dmr = [
            "1",
            "DMR Smplx 441",
            "4",
            "1",
            "Slot 2",
            "None",
            "Off",
            "Off",
            "Off",
            "Off",
            "Off",
            "441",
            "Middle",
            "None",
            "Off",
            "Off",
            "Off",
            "441",
            "Middle",
            "None",
            "None",
            "High",
            "Always",
            "60",
            "0",
            "0",
            "Off",
            "Off",
            "Off",
            "Full",
            "Key 1",
            "Off",
            "Fixed",
            "Off",
            "Single-Repeater",
            "None",
            "Off",
            "Digital Channel",
            "Off",
            "None",
            "Off",
            "Off",
            "Follow Admit Criteria",
            "DMR Standard",
            "Off",
            "None"
        ]



        self.__defaultRow_analog = [
            "1",
            "Channel 4",
            "Normal",
            "25.0",
            "Personality 1",
            "None",
            "Off",
            "Off",
            "Off",
            "Off",
            "Off",
            "441.00",
            "NONE",
            "NONE",
            "Middle",
            "CTCSS/CDCSS and Audio",
            "Carrier",
            "RX Squelch Mode",
            "441.00",
            "NONE",
            "NONE",
            "Middle",
            "High",
            "Aways Allow",
            "None",
            "Off",
            "60",
            "0",
            "0",
            "180",
            "None",
            "Off",
            "Off"
        ]


        self.__header_analog = [
            "No.",
            "Channel Alias",
            "Carrier Squelch Level",
            "Channel Spacing [KHz]",
            "Personality List",
            "Scan/Roam/Vote List",
            "Auto Start Scan",
            "Rx Only",
            "Talk Around",
            "Lone Worker",
            "VOX",
            "Receive Frequency [MHz]",
            "Rx CTCSS/CDCSS Type",
            "CTCSS/CDCSS Type",
            "Rx Ref Frequency",
            "Rx Squelch Mode",
            "Monitor Squelch Mode",
            "Channel Switch Squelch Mode",
            "Transmit Frequency [MHz]",
            "Tx CTCSS/CDCSS Type",
            "CTCSS/CDCSS Type",
            "Tx Ref Frequency",
            "Power Level",
            "Tx Admit",
            "Emergency System",
            "CTCSS Tail Revert",
            "Tx Time-Out Time [s]",
            "TOT Re-Key Time [s]",
            "TOT Pre-Alert Time [s]",
            "CTCSS Tail Revert Option [Radians]",
            "Scan/Roam/Vote Mode",
            "Auto Start Roam",
            "Auto Start Voting"
        ]


