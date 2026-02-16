# Constants.py
#
# Author: Jason Johnson <k3jsj@arrl.net>
# Purpose:  Constants file for radio specifications for CS7000 M17 PLUS radio
class Const:

    MAXCONTACTS=500000
    MAXCHANNELS=4000
    MAXZONES=250

    def __setattr__(self, name, value): raise AttributeError("Constants are read-only")
