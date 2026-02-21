import csv
import connectSystems.CS7000.Constants
from hashlib import sha256
import xlsxwriter

class DigitalContacts:

    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file

        self.__fileType = ''
        self.__fileVersion = ''
        self._rows = []

        self._contactDict = {}

        self.__DetermineFileType()
        self.__LoadRows()

    def get_all(self):
        return list(self._rows)

    def find_by_name(self, name):
        return [c for c in self._rows if c[2] == name]

    def find_by_rowId(self, rowId):
        return [c for c in self._rows if c[0] == rowId]

    def remove(self, name):
        self._rowsTemp = [c for c in self._rows if c[2] != name]
        self._rows = self._rowsTemp

        # Rebuild the alias name to row id
        self._buildDict()


    # ------------------------------------------------------------
    # Load all rows into a list so they can be iterated repeatedly
    # ------------------------------------------------------------
    def __LoadRows(self):
        if self.__fileType == "ERROR":
            return

        with open(self.input_file, mode='r', newline='', encoding="utf-8") as infile:
            reader = csv.reader(infile)
            for row in reader:
                self._rows.append(row)

        self.__rowsInFile = len(self._rows)
        self._buildDict()


    def _buildDict(self):
        self._contactDict = {}

        for index, row in enumerate(self._rows):
            key = row[2]          # second element is the Alias
            self._contactDict[key] = index

    def getContact(self, alias):
        try:
            index = self._contactDict[alias]
            return self._rows[index]
        except KeyError:
            raise KeyError(f"Alias '{alias}' not found in contact dictionary")
        except IndexError:
            raise IndexError(f"Index for alias '{alias}' is out of range")
        except Exception as e:
            raise Exception(f"Unexpected error in getContact(): {e}")

    def getNumberContacts(self):
        return self.__rowsInFile



    # ------------------------------------------------------------
    # Convert dispatcher
    # ------------------------------------------------------------
    def Convert(self):
        if self.__fileType == "Anytone":
            self.ConvertAnytoneTalkGroups()

        elif self.__fileType == "CS7000":
            return 0

        elif self.__fileType == "ERROR":
            return -1


    # ------------------------------------------------------------
    # Convert Anytone → CS7000 using in‑memory rows
    # ------------------------------------------------------------
    def ConvertAnytoneTalkGroups(self):
        workbook = xlsxwriter.Workbook(self.output_file)
        worksheet = workbook.add_worksheet("DMR_Contacts")

        rowNum = 0

        for row in self._rows:
            # Skip header row
            if rowNum == 0:
                worksheet.write(rowNum, 0, "No")
                worksheet.write(rowNum, 1, "Call Alias")
                worksheet.write(rowNum, 2, "Call Type")
                worksheet.write(rowNum, 3, "Call ID")
                worksheet.write(rowNum, 4, "Receive Tone")
                rowNum += 1
                continue

            number      = row[0]
            radio_id    = row[1]
            call_alias  = row[2]
            call_type   = row[3]
            receive_tone = "No"

            worksheet.write(rowNum, 0, number)
            worksheet.write(rowNum, 1, call_alias)
            worksheet.write(rowNum, 2, call_type)
            worksheet.write(rowNum, 3, radio_id)
            worksheet.write(rowNum, 4, receive_tone)

            rowNum += 1

        workbook.close()


    # ------------------------------------------------------------
    # Determine file type by hashing header row
    # ------------------------------------------------------------
    def __DetermineFileType(self):

        with open(self.input_file, mode='r', newline='', encoding="utf-8") as infile:
            reader = csv.reader(infile)

            try:
                header = next(reader)
            except StopIteration:
                self.__fileType = "ERROR"
                return

            s = ''.join(header)
            headerHash = sha256(s.encode('utf-8')).hexdigest()

            if headerHash == "3fcf4f8abf1017013669181c3b25ac2662c989e07fd05330250a6348b55baef2":
                self.__fileType = 'Anytone'

            elif headerHash == "32bff94368dad7633889e067a0606cb198d269561faf98e48881a298d04cf4b5":
                self.__fileType = 'CS7000'
                self.__fileVersion = '9.00.93'

            # Previous version of CS7000. Need to confirm version
            elif headerHash == "439f8c974eedd60ad132dc94803757e7a0e6e85093aecdd8ef0e3a26f971ff1d":
                self.__fileType = 'CS7000'

            else:
                print("Could not determine type of input file\nHash of file header is", headerHash)
                self.__fileType = 'ERROR'

