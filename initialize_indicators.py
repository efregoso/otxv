from OTXv2 import OTXv2
from elasticsearch import Elasticsearch
import warnings
import socket
import base64
import stylometry_tools.stylo_key as stylo_key
import stylometry_tools.stylo_ngrams as stylo_ngrams
import port_checker
import ip_lookup
import asyncio
from utils import ELASTICSEARCH_MAPPING, ELASTICSEARCH_INDICATOR_MAPPING, TEST_API_KEY

# Global instance of ElasticSearch for sending/organizing data
es = Elasticsearch()

# cache file streams to pulses and hits
cache_pulses_filestream = open("cache_pulses.txt", "w")
cache_hits_filestream = open("cache_hits.txt", "w")

# HOST & PORT for the login socket
HOST = 'localhost'
PORT = 10000

is_validated = False
s: socket.socket
conn: socket.socket
addr: tuple
apikey: bytes
otx: OTXv2
pulses: list

'''
Main method for the program. 
Collects and validates API key from browser, initializes ElasticSearch, 
& loads all pulse objects into the cache.
'''
def main():
    print("Initializing socket.")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Binding socket.")
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    
    # TODO: MAKE ASYNC: retrieve API key from login page & validate
    while is_validated is False:
        is_validated = validate_apikey()

    # send result back to the PHP server
    result = b'True'
    bool = base64.b64encode(result)
    conn.sendall(bool)
    print("Closing socket.")
    conn.close()
    print("Configuring indeces...")
    # Creating the index before adding things to it so that the mapping can be customized
    if es.indices.exists(index=apikey):
        # go through each pulse & check when it was last modified & if a pulse by that name exists in the index already.
        # if not, copy. if there is, update from last modified date from the index
        for pulse in pulses[0:300]:
            print("Have pulse already?: " + str(es.exists(index=apikey, doc_type="pulse", id=int(pulse["id"], 16))))
            if es.exists(index=apikey, doc_type="pulse", id=int(pulse["id"], 16)):
                pulse_match = es.get_source(index=apikey, doc_type="pulse", id=int(pulse["id"], 16))
                if pulse["modified"] != pulse_match["modified"]:
                    es.index(index=apikey, doc_type="pulse", id=int(pulse["id"], 16), body=pulse)
                    print("Updated pulse with ID: " + str(int(pulse["id"], 16)))
            else:
                print("Adding location data to indicators for pulse ID: " + str(int(pulse["id"], 16)))
                add_loc_to_indicators(pulse)
                es.index(index=apikey, doc_type="pulse", id=int(pulse["id"], 16), body=pulse)
                print("Added new pulse with ID: " + str(int(pulse["id"], 16)))
            print("Ops done for pulse with ID: " + str(int(pulse["id"], 16)))
    # If index does not already exist, create the index and begin loading mapping & pulse information
    else:
        print("Creating new index: ",  apikey)
        es.indices.create(index=apikey, ignore=400)
        # New mapping to include qualitative location as well as geopoint location
        mapping = ELASTICSEARCH_MAPPING
        es.indices.put_mapping(index=("indicators" + str(apikey)), doc_type="pulse", body=mapping)
        # Create an indicator mapping to get more useful list visualization
        es.indices.create(index="indicators"+str(apikey), ignore=400)
        mapping = ELASTICSEARCH_INDICATOR_MAPPING
        es.indices.put_mapping(index="indicators" + str(apikey), doc_type="indicator", body=mapping)
        print("Mappings created.  Beginning pulse loading.")
        # DEBUGGING: just the first 200 for now
        for pulse in pulses[0:200]:
            add_loc_to_indicators(pulse)
            # convert the pulse's hexadecimal ID to an integer & index
            es.index(index=apikey, doc_type="pulse", id=int(pulse["id"], 16), body=pulse)
            print("Added pulse with ID: " + str(int(pulse["id"], 16)))
    # signal that the program is done
    print("Pulse loading finished!")
    print("Waiting for any requests on port ", str(PORT), "...")
    while True:
        handle_requests()
    exit()


'''
A debugging function for printing the keys in an indicator object in the pulse list

:param pulses: An array of pulses from the OTX module
:returns: Prints one set of keys from the first indicator of each pulse object in pulses
'''
def print_keys(pulses):
    print(str(pulses[1]["indicators"][1].keys()))


'''
A debugging function for printing all indicators in a pulse

:param pulse: A pulse object with indicators to be added to the indicator data cache
:returns: A boolean on if the indicator was successfully cached
'''
def cache_indicator_data(pulse):
    for indicator in pulse["indicators"]:
        cache_hits_filestream.write(
            "indicator: " + indicator["indicator"] + 
            "\ndescription: " + str(indicator["description"]) + 
            "\ncreated: " + str(indicator["created"]) + 
            "\ntitle: " + str(indicator["title"]) + 
            "\ncontent: " + str(indicator["content"]) + 
            "\ntype: " + str(indicator["type"]) + 
            "\nid: " + str(indicator["id"]) + 
            "\n\n"
        )


'''
Function for putting a pulse in the cache

:param pulse: A pulse object to be added to the cache
:returns: A boolean on if the pulse was successfully cached
'''
def cache_pulses(pulse):
    try:
        cache_pulses_filestream.write(str(pulse) + '\n')
        return True
    except:
        raise Exception("Failed to write pulse to cache.")


'''
Function for adding a pulse to a user's favorites on OTX & in the app

:param pulse: A pulse object to be added to favorites
:returns: A boolean on if the pulse was successfully added to favorites
'''
def add_favorite(pulse):
    # add to a collection named "Favorites" or have the ability to customize collections
    print("Function not yet implemented.")


'''
Function for initializing the login process with sockets to the login.php script

:returns: A boolean describing whether or not the apikey was valid 
'''
def validate_apikey():
    print("Receiving data.")
    apikey = base64.b64decode(conn.recv(1024))
    print("Data decoded to: ", apikey)
    try:
        otx = OTXv2(apikey)
    except:
        conn.sendall(base64.b64encode(b'False'))
        raise Exception("Failed to create OTXv2 instance with provided API key:", str(apikey))
    try:
        pulses = otx.getall()
    except:
        conn.sendall(base64.b64encode(b'False'))
        raise Exception("Failed to retrieve pulses with provided API key:", str(apikey))
    print("API key valid!  Retrieving pulses from server...")
    return True


'''
A function for waiting for requests
'''
def handle_requests():
    print("Awaiting new requests...")
    s.listen()
    conn, addr = s.accept()
    print("Accepted connection")
    buf = conn.recv(1024)
    method = base64.b64decode(buf)
    print("Received method code decoded to:", str(method))
    if method == b'stylokey':
        print("Method determined as keyword analysis.")
        buf = conn.recv(1024)
        ctrl = base64.b64decode(buf).decode("utf-8")
        print("Received ctrl data decoded to: ", ctrl)
        buf = conn.recv(1024)
        comp1 = base64.b64decode(buf).decode("utf-8")
        print("Received comp1 data decoded to: ", comp1)
        buf = conn.recv(1024)
        comp2 = base64.b64decode(buf).decode("utf-8")
        print("Received comp2 data decoded to: ", comp2)
        buf = conn.recv(1024)
        comp3 = base64.b64decode(buf).decode("utf-8")
        print("Received comp3 data decoded to: ", comp3)
        result = str.encode(str(stylo_key.run_keyword_stylometry_on_text(ctrl, [comp1, comp2, comp3])))
    elif method == b'stylongram':
        print("Method determined as unigram analysis.")
        buf = conn.recv(1024)
        ctrl = base64.b64decode(buf).decode("utf-8")
        print("Received ctrl data decoded to: ", ctrl)
        buf = conn.recv(1024)
        comp1 = base64.b64decode(buf).decode("utf-8")
        print("Received comp1 data decoded to: ", comp1)
        buf = conn.recv(1024)
        comp2 = base64.b64decode(buf).decode("utf-8")
        print("Received comp2 data decoded to: ", comp2)
        print(comp2)
        buf = conn.recv(1024)
        comp3 = base64.b64decode(buf).decode("utf-8")
        print("Received comp3 data decoded to: ", comp3)
        result = str.encode(str(stylo_ngrams.run_stylometry_on_text(ctrl, [comp1, comp2, comp3], number_of_ngrams=1)))
    elif method == b'iplookup':
        print("Method determined as IP lookup.")
        buf = conn.recv(1024)
        ipaddr = base64.b64decode(buf).decode("utf-8")
        print("Received IP data decoded to: ", ipaddr)
        result = str.encode(ip_lookup.lookup_full_ip_info(ipaddr))
    elif method == b'portcheck':
        print("Method determined as port check.")
        buf = conn.recv(1024)
        domain = base64.b64decode(buf).decode("utf-8")
        print("Received IP data decoded to: ", domain)
        buf = conn.recv(1024)
        count = base64.b64decode(buf).decode("utf-8")
        print("Received count data decoded to: ", count)
        result = str.encode(str(port_checker.check_port(domain, count)))
    else:
        print("Invalid request received.")
        result = b'Invalid request received. Please try again.'
    # send result back to script
    bool = base64.b64encode(result)
    conn.sendall(bool)
    print("Sent result back to script...")


'''
A function for adding geopoint data to indicators with IPv4 & IPv6 type indicators.

:param pulse: The pulse to have indicator location data added to it
:returns: A boolean indicating if the location-adding was successful
'''
def add_loc_to_indicators(pulse):
    for indicator in pulse["indicators"]:
        if indicator['type'] == 'IPv4' or indicator['type'] == 'IPv6':
            print("Updating indicator with location.")
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                ipgeocode = ip_lookup.lookup_ip_info(indicator["indicator"])
                print(ipgeocode)
                if ipgeocode is not None:
                    # the returned result has "lng" instead of "lon", so change that first
                    lng = ipgeocode["lng"]
                    ipgeocode.update([("lon", lng)])
                    del ipgeocode["lng"]
                indicator.update([("location", ipgeocode)])
                # WIP: adding the qualitative location to the indicator data
                qual_loc = ip_lookup.lookup_qual_ip_info(indicator["indicator"])
                indicator.update([("qual_location", qual_loc)])
        else:
            indicator.update([("location", None)])
    return True


'''
Main method for starting up the program
'''
if __name__ == '__main__':
    main()