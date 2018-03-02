from OTXv2 import OTXv2
from OTXv2 import IndicatorTypes

# method for retrieving OTX pulses & placing them into the cache file
# IN PROGRESS - currently developing

# API Key used for logging in -- BETA VERSION. still altering for custom credentials
otx = OTXv2("de0e60ea625d2b840e464f5d44299fcd513a3da48d2d7dd8c3214474dc6dbadb")
# OTX password -- currently set to "password"
OTX_PASSWORD = "password"
# buffer object for pulses
pulses = []
# name of the cache file
cache = 'stixtest.xml'

def main():

    #get all indicators associated with a pulse
    indicators = otx.get_pulse_indicators("")

def findServices():



if __name__ == '__main__':
    main()

