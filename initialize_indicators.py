from OTXv2 import OTXv2
from OTXv2 import IndicatorTypes
from elasticsearch import Elasticsearch
import ip_lookup
import warnings
import socket
import base64
import datetime

# DEBUGGING: my API key is "de0e60ea625d2b840e464f5d44299fcd513a3da48d2d7dd8c3214474dc6dbadb"
# an instance of ElasticSearch for sending/organizing data
es = Elasticsearch()
# cache file streams to pulses and hits
cachep = open("cache_pulses.txt", "w")
cacheh = open("cache_hits.txt", "w")
# HOST & PORT for the login socket
HOST = 'localhost'
PORT = 10000

'''
Main method for the program. Collects apikey from the browser, validates it, initializes ElasticSearch, & loads
all pulse objects into the cache. 
'''
def main():
    # a boolean for validating the API key
    isValidated = False
    # retrieve API key from login page & validate
    while isValidated is False:
        isValidated = validate_apikey()
    # send result back to the PHP server
    result = b'True'
    bool = base64.b64encode(result)
    conn.sendall(bool)
    print("APIKey valid.")
    print("Closing socket.")
    conn.close()
    # DEBUGGING: Save all indicator data to cache document & send to Elasticsearch with incremental IDs
    global i
    i = 1
    # get all pulses
    pulses = otx.getall()
    # Creating the index before adding things to it so that the mapping can be customized
    # DEBUGGING: If index already exists, only update pulses not updated
    if es.exists(apikey):
        # start updating by last modified date. go through each pulse & check when it was last modified & if a pulse
        # by that name exists in the index already.  if not, copy. if there is, update from last modified date from the
        # index.
        # only retrieve pulses from a certain date
        for pulse in pulses[0:1000]:
            # cache the pulse & its indicator data
            # cache_pulses(pulse)
            # cache_indicator_data(pulse)
            j = 1
            for indicator in pulse["indicators"]:
                if indicator["type"] == "IPv4" or indicator["type"] == "IPv6":
                    print("Updating indicator with location.")
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore")
                        ipgeocode = ip_lookup.lookup_ip_info(indicator["indicator"])
                        # DEBUGL print the ip's geocode
                        print(ipgeocode)
                        if ipgeocode is not None:
                            # the returned result has "lng" instead of "lon", so change that first
                            lng = ipgeocode["lng"]
                            ipgeocode.update([("lon", lng)])
                            del ipgeocode["lng"]
                        indicator.update([("location", ipgeocode)])
                        # WIP: adding the qualitative location to the indicator data
                        # This will need to be done from within the ip_lookup.py module.
                        # ip_lookup.lookup_qual_ip_info(indicator["indicator"])
                        # indicator.update([("qual_location", )])
                        # DEBUGGING: print(indicator["location"])
                else:
                    indicator.update([("location", None)])
                es.index(index="indicators", doc_type="indicator", id=j, body=indicator)
                j = j + 1
            # update the pulse information with the current date & time that this pulse was updated
            pulse.update([("changed_by_es", datetime.utcnow())])
            # convert the pulse's natural hexadecimal ID to an integer ID
            es.index(index=apikey, doc_type="pulse", id=int(pulse["id"], 16), body=pulse)
            i = i + 1
    # If index does not already exist, create the index and begin loading mapping & pulse information
    else:
        es.indices.create(index=apikey, ignore=400)
        # New mapping to include qualitative location as well as geopoint location
        mapping = {
            "properties": {
                "changed_in_es": {
                    "type": "date"
                },
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
        es.indices.create(index="indicators", ignore=400)
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
        es.indices.put_mapping(index="indicators", doc_type="indicator", body=mapping)
        print("Mappings created.  Beginning pulse loading.")
        # DEBUGGING: just the first thousand for now
        for pulse in pulses[0:1000]:
            # cache the pulse & its indicator data
            cache_pulses(pulse)
            # cache_indicator_data(pulse)
            j = 1
            for indicator in pulse["indicators"]:
                if indicator["type"] == "IPv4" or indicator["type"] == "IPv6":
                    print("Updating indicator with location.")
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore")
                        ipgeocode = ip_lookup.lookup_ip_info(indicator["indicator"])
                        # DEBUG:
                        print(ipgeocode)
                        if ipgeocode is not None:
                            # the returned result has "lng" instead of "lon", so change that first
                            lng = ipgeocode["lng"]
                            ipgeocode.update([("lon", lng)])
                            del ipgeocode["lng"]
                            # DEBUG: print(pprint.pformat(ipgeocode))
                        indicator.update([("location", ipgeocode)])
                        # WIP: adding the qualitative location to the indicator data
                        # This will need to be done from within the ip_lookup.py module.
                        # ip_lookup.lookup_qual_ip_info(indicator["indicator"])
                        # indicator.update([("qual_location", )])
                        # DEBUGGING: print(indicator["location"])
                # DEBUGGING: to deal with indicators that don't currently have location data, substitute coordinate (0, 0)
                else:
                    # DEBUG: print("Updating indicator with no location.")
                    indicator.update([("location", None)])
                es.index(index="indicators", doc_type="indicator", id=j, body=indicator)
                j = j + 1
            # convert the pulse's natural hexadecimal ID to an integer ID
            es.index(index=apikey, doc_type="pulse", id=int(pulse["id"], 16), body=pulse)
            i = i + 1
    # close the filestream for the caches
    cachep.close()
    cacheh.close()
    # signal that the program is done
    print("System done")
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
    print("Initializing socket.")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Binding socket.")
    s.bind((HOST, PORT))
    print("Listening for connections.")
    s.listen(10)
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
        otx = OTXv2(apikey)
        print("Attempting pulse query test...")
        global pulses
        pulses = otx.get_indicator_details_full(IndicatorTypes.DOMAIN, "google.com")
    except:
        print("APIKey not valid")
        result = b'False'
        bool = base64.b64encode(result)
        conn.sendall(bool)
        return False
    print("Finished pulse import!")
    return True


'''
Main method for starting up the program
'''
if __name__ == '__main__':
    main()


