import csv
from hashlib import sha256
import xlsxwriter

class DigitalContacts:

    def __init__(self, input_file, output_file, maxContacts):
        self.input_file = input_file
        self.output_file = output_file

        self.maxContacts = maxContacts
        self.numImported = 0
        self.numNotImported = 0
        self.__dictNotImported = None
        self.__fileType = ''
        self.__DetermineFileType()

    def Convert(self):
        if self.__fileType == "Anytone":
            self.ConvertAnytoneTalkGroups()
        if self.__fileType == "CS7000":
            print("Input file is all ready is format for the CS7000.  Nothing to convert.")
        if self.__fileType == "ERROR":
            print("Error!  Input file is not the CSV format expected from Anytone CPS.")
            return (-1)

    def outputTalkGroupsNotImported(self,output_file):
        # If there were no talk group not imported exit this method
        if (self.numNotImported == 0):
            return 0

        # There were talk groups that could not be imported
        # Write the talk groups to a worksheet
        workbook = xlsxwriter.Workbook(output_file)
        worksheet = workbook.add_worksheet("ContactsNotImported")

        worksheet.write(0,0,"Call alias")
        worksheet.write(0,1,"Radio ID")
        worksheet.write(0,2,"Call type")
        worksheet.write(0,3,"Receive tone")
        rowNum = 1
        for k in self.__dictNotImported.keys():
            worksheet.write(rowNum,0,k)
            colNum = 1
            for col in self.__dictNotImported[k]:
                worksheet.write(rowNum,colNum,col)
                colNum = colNum + 1
            rowNum = rowNum + 1

        workbook.close()

    def checkNotImported(self, talkgroup):
        if talkgroup in self.__dictNotImported:
            return False
        else:
            return True

    def ConvertAnytoneTalkGroups(self):
        input_file = self.input_file
        output_file = self.output_file

        workbook = xlsxwriter.Workbook(output_file)
        worksheet = workbook.add_worksheet("DMR_Contacts")

        # Open the input file for reading
        with open(input_file, mode='r', newline='') as infile:
            reader = csv.reader(infile)
            
            # Process each row in the input file
            # the first row contains the header row
            # subsequent rows contain talk groups
            rowNum = 0
            self.numImported = 0
            for row in reader:
                number = row[0]
                radio_id = row[1]
                call_alias = row[2]
                call_type = row[3]
                if rowNum == 0:
                    receive_tone = "Receive Tone"
                else:
                    receive_tone = "No"

                if (self.numImported <= self.maxContacts):
                    worksheet.write(rowNum, 0, number)
                    worksheet.write(rowNum, 1, call_alias)
                    worksheet.write(rowNum, 2, call_type)
                    worksheet.write(rowNum, 3, radio_id)
                    worksheet.write(rowNum, 4, receive_tone)
                    self.numImported = self.numImported + 1
                else:
                    # We have imported maximum number of records the radio supports
                    #     save list of talk groups not imported.
                    #     index will be the call_alias
                    if (self.__dictNotImported == None):
                        self.__dictNotImported = { call_alias: [ radio_id, call_type, receive_tone] }
                    else:
                        self.__dictNotImported[call_alias] = [ radio_id, call_type, receive_tone ]

                    self.numNotImported = self.numNotImported + 1

                rowNum = rowNum + 1

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
                   
                    if (headerHash == "3fcf4f8abf1017013669181c3b25ac2662c989e07fd05330250a6348b55baef2"):
                        self.__fileType = 'Anytone'
                    else:
                        if (headerHash == "439f8c974eedd60ad132dc94803757e7a0e6e85093aecdd8ef0e3a26f971ff1d"):
                            self.__fileType = 'CS7000'
                        else:
                            print("Could not determine type of input file\nHash of file header is ", headerHash)
                            self.__fileType = 'ERROR'

                numRows = numRows + 1

            self.__rowsInFile = numRows

        infile.close()
