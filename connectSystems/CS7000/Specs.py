import json
from util.verifySignature import verifySignature
class Specs:

    def __init__(self):

        # Specify the path to your JSON file
        json_file_path = 'cs7000.specs.json'
        json_file_sig = 'cs7000.specs.json.sig'

        v = verifySignature()
        if v.verifyFile (json_file_path, json_file_sig):
            print ("Signature of " + json_file_path + " is valid.")
        else:
            print ("Signature of " + json_file_path + " is invalid.")


        # Open the JSON file and load its contents into a dictionary
        with open(json_file_path, 'r') as json_file:
            self.specs = json.load(json_file)

        # Print the dictionary to verify the contents
        print(self.specs)
        json_file.close()

    def printSpecs(self, firmwareVersion):
        # Accessing the device_info for firmware 3.0.1
        device_info = self.specs[firmwareVersion]
        print(device_info)

    def getFirmwareVersions(self):
        values = [key for key in self.specs.keys()]
        return(values)

    def getSpecs (self, firmwareVersion):
        return(self.specs[ firmwareVersion ])

    
             
