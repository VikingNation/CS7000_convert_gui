class Specs:

    def __init__(self):
        self.specs = {
            "9.00.05": {
                "maxContacts": 2000,
                "maxChannels": 2000,
                "maxChannelsPerZone": 160,
                "maxZones" : 250
            }
        }

    def printSpecs(self, firmwareVersion):
        # Accessing the device_info for firmware 3.0.1
        device_info = self.specs[firmwareVersion]
        print(device_info)

    def getFirmwareVersions(self):
        values = [key for key in self.specs.keys()]
        return(values)

    def getSpecs (self, firmwareVersion):
        return(self.specs[ firmwareVersion ])

    
             
