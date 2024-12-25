import csv
from hashlib import sha256

class DigitalContacts:

    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file

        self.__fileType = ''
        self.__DetermineFileType()

    def Convert(self):
        if self.__fileType == "Anytone":
            self.ConvertAnytoneTalkGroups()

    def ConvertAnytoneTalkGroups(self):
        input_file = self.input_file
        output_file = self.output_file

        # Open the input file for reading
        with open(input_file, mode='r', newline='') as infile:
            reader = csv.reader(infile)
            
            # Open the output file for writing
            with open(output_file, mode='w', newline='') as outfile:
                writer = csv.writer(outfile)
                
                # Process each row in the input file
                for row in reader:
                    number = row[0]
                    radio_id = row[1]
                    call_alias = row[2]
                    call_type = row[3]
                    receive_tone = row[4]
                    writer.writerow([number, call_alias, call_type, radio_id, receive_tone])

        outfile.close()
        infile.close()


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

                numRows = numRows + 1

            self.__rowsInFile = numRows

        infile.close()
