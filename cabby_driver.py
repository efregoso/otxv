from OTXv2 import OTXv2
import json
from OTXv2 import IndicatorTypes
from pandas.io.json import json_normalize
from datetime import datetime, timedelta

# method for retrieving OTX pulses & placing them into the cache file
# IN PROGRESS - currently developing

# API Key used for logging in -- BETA VERSION. still altering for custom credentials
otx = OTXv2("de0e60ea625d2b840e464f5d44299fcd513a3da48d2d7dd8c3214474dc6dbadb")
# OTX password -- currently set to "password"
OTX_PASSWORD = "password"
# name of the cache file
cache = "testcache.txt"

def main():

    #open file stream to cache document
    cachef = open(cache, "w")
    #get all subscribed pulses
    pulses = otx.getall()
    #WIP: save to cache document
    for indicator in pulses:
        cachef.write(indicator["name"] + "\n")
    #signal that the program is done
    print("System done")
    exit()


if __name__ == '__main__':
    main()

