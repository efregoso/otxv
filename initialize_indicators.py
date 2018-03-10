from OTXv2 import OTXv2
from OTXv2 import IndicatorTypes
from elasticsearch import Elasticsearch
from ipwhois import IPWhois
import pprint
import json
from pandas.io.json import json_normalize
from datetime import datetime, timedelta

# method for retrieving OTX pulses & placing them into the cache file
# IN PROGRESS - currently developing

# API Key used for logging in -- BETA VERSION. still altering for custom credentials
otx = OTXv2("de0e60ea625d2b840e464f5d44299fcd513a3da48d2d7dd8c3214474dc6dbadb")
#an instance of ElasticSearch for sending data to.  Must be initialized after ElasticSearch has already been started up
es = Elasticsearch()
# OTX password -- currently set to "password"
OTX_PASSWORD = "password"
# name of the cache file
cache = "cache.txt"

def main():

    #open file stream to cache document
    cachef = open(cache, "w")
    #get all subscribed pulses
    pulses = otx.getall()
    #DEBUGGING: print the keys of the dictionary object in the list object in the indicators dictionary entry in each pulse object
    #print(str(pulses[1]["indicators"][1].keys()))
    #WIP: save all indicator data to cache document
    for pulse in pulses:
        cachef.write(pprint.pformat(pulse))
        #DEBUGGING: writing only indicator data to the testcache
        #for indicator in pulse["indicators"]:
        #    cachef.write("indicator: " + indicator["indicator"] + "\ndescription: " + str(indicator["description"]) + "\ncreated: " + str(indicator["created"]) + "\ntitle: " + str(indicator["title"]) + "\ncontent: " + str(indicator["content"]) + "\ntype: " + str(indicator["type"]) + "\nid: " + str(indicator["id"]) + "\n\n")
    print(json_normalize(pulses[0:5]))
    cachef.close()
    # send the pulses to elasticsearch

    #signal that the program is done
    print("System done")
    exit()

#Lookup DNS information about a given IP address using the whois API.
def lookup_ip_info(ip):
    #create a whois instance for the given IP
    whois = IPWhois(ip)
    #lookup the information for this IP & place it in ipresults in a "pretty print" format
    ipresults = pprint.pformat(whois.lookup_rdap());
    #open a file stream for a demo lookup cache
    lookupf = open("lookup.txt", "w")
    #write the results into the demo lookup cache
    lookupf.write(ipresults)


if __name__ == '__main__':
    main()

