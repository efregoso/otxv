from OTXv2 import OTXv2
from elasticsearch import Elasticsearch
import warnings
import socket
import base64
import stylo_key
import stylo_unigram
import stylo_bigram
import port_checker
import ip_lookup

# an instance of ElasticSearch for sending/organizing data
es = Elasticsearch()
# cache file streams to pulses and hits
cachep = open("cache_pulses.txt", "w")
cacheh = open("cache_hits.txt", "w")
# HOST & PORT for the login socket
HOST = 'localhost'
PORT = 10000
# DEBUGGING: my API key is "de0e60ea625d2b840e464f5d44299fcd513a3da48d2d7dd8c3214474dc6dbadb"


'''
Main method for the program. Collects API key from the browser, validates it, initializes ElasticSearch, & loads
all pulse objects into the cache. 
'''
def main():
    # a boolean for validating the API key
    is_validated = False
    print("Initializing socket.")
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Binding socket.")
    s.bind((HOST, PORT))
    # retrieve API key from login page & validate
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
        print("Creating new index: " + apikey)
        es.indices.create(index=apikey, ignore=400)
        # New mapping to include qualitative location as well as geopoint location
        mapping = {
            "properties": {
                "adversary": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 50
                        }
                    }
                },
                "author_name": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 50
                        }
                    }
                },
                "created": {
                    "type": "date"
                },
                "description": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 1000
                        }
                    }
                },
                "id": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 50
                        }
                    }
                },
                "indicators": {
                    "properties": {
                        "content": {
                            "type": "text",
                            "fields": {
                                "keyword": {
                                    "type": "keyword",
                                    "ignore_above": 1000
                                }
                            }
                        },
                        "created": {
                            "type": "date"
                        },
                        "description": {
                            "type": "text",
                            "fields": {
                                "keyword": {
                                    "type": "keyword",
                                    "ignore_above": 1000
                                }
                            }
                        },
                        "id": {
                            "type": "long"
                        },
                        "indicator": {
                            "type": "text",
                            "fields": {
                                "keyword": {
                                    "type": "keyword",
                                    "ignore_above": 50
                                }
                            }
                        },
                        "location": {
                            "type": "geo_point"
                        },
                        "qual_location": {
                            "type": "text",
                            "fields": {
                                "keyword": {
                                    "type": "keyword",
                                    "ignore_above": 500
                                }
                            }
                        },
                        "title": {
                            "type": "text",
                            "fields": {
                                "keyword": {
                                    "type": "keyword",
                                    "ignore_above": 256
                                }
                            }
                        },
                        "type": {
                            "type": "text",
                            "fields": {
                                "keyword": {
                                    "type": "keyword",
                                    "ignore_above": 256
                                }
                            }
                        }
                    }
                },
                "industries": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 1000
                        }
                    }
                },
                "modified": {
                    "type": "date"
                },
                "more_indicators": {
                    "type": "boolean"
                },
                "name": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 1000
                        }
                    }
                },
                "public": {
                    "type": "long"
                },
                "references": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 1000
                        }
                    }
                },
                "revision": {
                    "type": "long"
                },
                "tags": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 1000
                        }
                    }
                },
                "targeted_countries": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 1000
                        }
                    }
                },
                "tlp": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 1000
                        }
                    }
                }
            }
        }
        es.indices.put_mapping(index="indicators"+apikey, doc_type="pulse", body=mapping)
        # Create an indicator mapping to get more useful list visualization
        es.indices.create(index="indicators"+apikey, ignore=400)
        mapping = {
            "properties": {
                "content": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    }
                },
                "created": {
                    "type": "date"
                },
                "description": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    }
                },
                "id": {
                    "type": "long"
                },
                "indicator": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    }
                },
                "location": {
                    "type": "geo_point"
                },
                "qual_location": {
                    "type" : "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    }
                },
                "title": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    }
                },
                "type": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    }
                }
            }
        }
        es.indices.put_mapping(index="indicators" + apikey, doc_type="indicator", body=mapping)
        print("Mappings created.  Beginning pulse loading.")
        # DEBUGGING: just the first 200 for now
        for pulse in pulses[0:200]:
            add_loc_to_indicators(pulse)
            # convert the pulse's natural hexadecimal ID to an integer ID & index
            es.index(index=apikey, doc_type="pulse", id=int(pulse["id"], 16), body=pulse)
            print("Added pulse with ID: " + str(int(pulse["id"], 16)))
    # signal that the program is done
    print("Pulse loading finished!")
    print("Waiting for any requests on port " + str(PORT) + "...")
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
        cacheh.write("indicator: " + indicator["indicator"] + "\ndescription: " + str(indicator["description"]) + "\ncreated: " + str(indicator["created"]) + "\ntitle: " + str(indicator["title"]) + "\ncontent: " + str(indicator["content"]) + "\ntype: " + str(indicator["type"]) + "\nid: " + str(indicator["id"]) + "\n\n")


'''
Function for putting a pulse in the cache

:param pulse: A pulse object to be added to the cache
:returns: A boolean on if the pulse was successfully cached
'''
def cache_pulses(pulse):
    cachep.write(str(pulse))
    cachep.write("\n")
    return True


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
    # retrieve API key from login page
    print("Listening for connections.")
    s.listen()
    global conn
    conn, addr = s.accept()
    print("Accepted connection")
    print("Receiving data.")
    data = conn.recv(1024)
    print("Received: ")
    print(data)
    global apikey
    apikey = base64.b64decode(data)
    print("Decoded to: ")
    print(apikey)
    try:
        global otx
        otx = OTXv2(apikey)
        print("Retrieving pulses from server...")
        global pulses
        pulses = otx.getall()
    except:
        print("APIKey not valid")
        result = b'False'
        bool = base64.b64encode(result)
        conn.sendall(bool)
        return False
    print("API key valid!")
    return True


'''
A function for waiting for requests


'''
def handle_requests():
    print("Awaiting new requests...")
    s.listen()
    global conn
    conn, addr = s.accept()
    print("Accepted connection")
    print("Receiving data.")
    buf = conn.recv(1024)
    print("Received method code: ")
    print(buf)
    method = base64.b64decode(buf)
    print("Decoded to method code:")
    print(str(method))
    if method == b'stylokey':
        print("Method determined as keyword analysis.")
        buf = conn.recv(1024)
        print("Received ctrl data: ")
        print(buf)
        ctrl = base64.b64decode(buf).decode("utf-8")
        print("Decoded to ctrl data: ")
        print(ctrl)
        buf = conn.recv(1024)
        print("Received comp1 data: ")
        print(buf)
        comp1 = base64.b64decode(buf).decode("utf-8")
        print("Decoded to comp1 data: ")
        print(comp1)
        buf = conn.recv(1024)
        print("Received comp2 data: ")
        print(buf)
        comp2 = base64.b64decode(buf).decode("utf-8")
        print("Decoded to comp2 data: ")
        print(comp2)
        buf = conn.recv(1024)
        print("Received comp3 data: ")
        print(buf)
        comp3 = base64.b64decode(buf).decode("utf-8")
        print("Decoded to comp3 data: ")
        print(comp3)
        result = str.encode(str(stylo_key.run_stylometry_on([ctrl, comp1, comp2, comp3])))
    elif method == b'stylounigram':
        print("Method determined as unigram analysis.")
        buf = conn.recv(1024)
        print("Received ctrl data: ")
        print(buf)
        ctrl = base64.b64decode(buf).decode("utf-8")
        print("Decoded to ctrl data: ")
        print(ctrl)
        buf = conn.recv(1024)
        print("Received comp1 data: ")
        print(buf)
        comp1 = base64.b64decode(buf).decode("utf-8")
        print("Decoded to comp1 data: ")
        print(comp1)
        buf = conn.recv(1024)
        print("Received comp2 data: ")
        print(buf)
        comp2 = base64.b64decode(buf).decode("utf-8")
        print("Decoded to comp2 data: ")
        print(comp2)
        buf = conn.recv(1024)
        print("Received comp3 data: ")
        print(buf)
        comp3 = base64.b64decode(buf).decode("utf-8")
        print("Decoded to comp3 data: ")
        print(comp3)
        result = str.encode(str(stylo_unigram.run_stylometry_on([ctrl, comp1, comp2, comp3])))
    elif method == b'stylobigram':
        print("Method determined as bigram analysis.")
        buf = conn.recv(1024)
        print("Received ctrl data: ")
        print(buf)
        ctrl = base64.b64decode(buf).decode("utf-8")
        print("Decoded to ctrl data: ")
        print(ctrl)
        buf = conn.recv(1024)
        print("Received comp1 data: ")
        print(buf)
        comp1 = base64.b64decode(buf).decode("utf-8")
        print("Decoded to comp1 data: ")
        print(comp1)
        buf = conn.recv(1024)
        print("Received comp2 data: ")
        print(buf)
        comp2 = base64.b64decode(buf).decode("utf-8")
        print("Decoded to comp2 data: ")
        print(comp2)
        buf = conn.recv(1024)
        print("Received comp3 data: ")
        print(buf)
        comp3 = base64.b64decode(buf).decode("utf-8")
        print("Decoded to comp3 data: ")
        print(comp3)
        result = str.encode(str(stylo_bigram.run_stylometry_on([ctrl, comp1, comp2, comp3])))
    elif method == b'iplookup':
        print("Method determined as IP lookup.")
        buf = conn.recv(1024)
        print("Received IP data: ")
        print(buf)
        ipaddr = base64.b64decode(buf).decode("utf-8")
        print("Decoded to IP: ")
        print(ipaddr)
        result = str.encode(ip_lookup.lookup_full_ip_info(ipaddr))
    elif method == b'portcheck':
        print("Method determined as port check.")
        buf = conn.recv(1024)
        print("Received IP data: ")
        print(buf)
        ipaddr = base64.b64decode(buf).decode("utf-8")
        print("Decoded to IP: ")
        print(ipaddr)
        result = str.encode(str(port_checker.check_port(ipaddr)))
    else:
        print("Invalid request received.")
        result = b'Invalid request received. Please try again.'
    # send result back to script
    bool = base64.b64encode(result)
    print("Sending result back to script...")
    conn.sendall(bool)
    print("Sent result.")


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