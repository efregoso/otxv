from OTXv2 import OTXv2
from elasticsearch import Elasticsearch
from ipwhois import IPWhois
import pprint
from pandas.io.json import json_normalize
from datetime import datetime, timedelta
import ip_lookup

# method for retrieving OTX pulses & placing them into the cache file
# IN PROGRESS - currently developing

# API Key used for logging in -- BETA VERSION. still altering for custom credentials
otx = OTXv2("de0e60ea625d2b840e464f5d44299fcd513a3da48d2d7dd8c3214474dc6dbadb")
# an instance of ElasticSearch for sending data to.  Must be initialized after ElasticSearch has already been started up
es = Elasticsearch()
# OTX password -- currently set to "password"
OTX_PASSWORD = "password"
# name of the cache file
cache = "cache.txt"


def main():
    # open file stream to cache document
    cachep = open("cache_pulses.txt", "w")
    cacheh = open("cache_hits.txt", "w")
    # get all subscribed pulses
    pulses = otx.getall()
    # WIP: save all indicator data to cache document & send to Elasticsearch with incremental IDs
    # DEBUGGING: index indicator hits in separate index, "hits"
    i = 1
    # DEBUGGING: just the first ten?
    for pulse in pulses[0:200]:
        # DEBUGGING: not creating cache for now
        # cache_pulse(pulse)
        # cache_indicator_data(pulse)
        j = 1
        for indicator in pulse["indicators"]:
            if indicator["type"] == "IPv4" or indicator["type"] == "IPv6":
                ipgeocode = ip_lookup.lookup_ip_info(indicator["indicator"])
                # DEBUGGING: print the ipgeocode
                # convert the address to a coordinate location
                indicator.update([("location", ipgeocode)])
                # DEBUGGING: print the location and make sure that it is working
                # print(indicator["location"])
                # DEBUGGING - make a separate index for indicators to see if this affects mapping location
                es.index(index="indicators", doc_type="indicator", id=j, body=indicator)
                j = j + 1
        es.index(index="pulses", doc_type="pulse", id=i, body=pulse)
        i = i + 1
    # close the filestream for the caches
    cachep.close()
    cacheh.close()
    # signal that the program is done
    print("System done")
    exit()


# Lookup DNS information about a given IP address using the whois API.
def lookup_ip_info(ip):
    # create a whois instance for the given IP
    whois = IPWhois(ip)
    # lookup the information for this IP & place it in ipresults in a "pretty print" format
    # DEBUGGING: maybe try not doing the pretty print to make it bypass the error?
    ipresults = pprint.pformat(whois.lookup_rdap());
    # open a file stream for a demo lookup cache
    lookupf = open("lookup.txt", "w")
    # write the results into the demo lookup cache
    lookupf.write(ipresults)


# A debugging function for printing the keys in an indicator object in the pulse list
def print_keys(pulses):
    print(str(pulses[1]["indicators"][1].keys()))


# A debugging function for printing all indicators in a pulse
def cache_indicator_data(pulse):
    for indicator in pulse["indicators"]:
        cacheh.write("indicator: " + indicator["indicator"] + "\ndescription: " + str(indicator["description"]) + "\ncreated: " + str(indicator["created"]) + "\ntitle: " + str(indicator["title"]) + "\ncontent: " + str(indicator["content"]) + "\ntype: " + str(indicator["type"]) + "\nid: " + str(indicator["id"]) + "\n\n")


# Function for putting a pulse in the cache
def cache_pulses(pulse):
    cachep.write(pprint.pformat(pulse))
    cachep.write("\n")


# Main method for starting up the program
if __name__ == '__main__':
    main()