from OTXv2 import OTXv2
from elasticsearch import Elasticsearch
from ipwhois import IPWhois
import pprint
import ip_lookup
import warnings
import socket
import base64

# method for retrieving OTX pulses & placing them into the cache file
# IN PROGRESS - currently developing

# DEBUGGING: API Key used for logging in -- BETA VERSION. still altering for custom credentials
# otx = OTXv2("de0e60ea625d2b840e464f5d44299fcd513a3da48d2d7dd8c3214474dc6dbadb")
# an instance of ElasticSearch for sending data to.  Must be initialized after ElasticSearch has already been started up
es = Elasticsearch()
# OTX password -- currently set to "password"
OTX_PASSWORD = "password"
# cache file streams to pulses and hits
cachep = open("cache_pulses.txt", "w")
cacheh = open("cache_hits.txt", "w")


def main():
    # retrieve API key from login page
    HOST = 'localhost'
    PORT = 10000

    print("Initializing socket.")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Binding socket.")
    s.bind((HOST, PORT))
    print("Listening for connections.")
    s.listen(10)
    conn, addr = s.accept()
    print("Accepted connection")
    print("Receiving data.")
    data = conn.recv(1024)
    print("Received: ")
    print(data)
    apikey = base64.b64decode(data)
    print("Decoded to: ")
    print(apikey)
    # try using the api key to open a connection
    # if it works, resume code
    # if not, send "False" back to the PHP server
    try:
        otx = OTXv2(apikey)
    except:
        bool = b'False'
        conn.sendall(bool)
        print("APIKey not valid")
    bool = b'True'
    conn.sendall(bool)
    print("APIKey valid.")
    print("Closing socket.")
    conn.close()
    # get all subscribed pulses
    print("Beginning pulse import.")
    pulses = otx.getall()
    print("Finished pulse import.")
    # WIP: save all indicator data to cache document & send to Elasticsearch with incremental IDs
    # DEBUGGING: index indicator hits in separate index, "hits"
    i = 1
    # DEBUGGING: creating the index before adding things to it so that the mapping can be customized
    es.indices.create(index="pulses", ignore=400)
    mapping = {
        "properties": {
            "adversary": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                }
            },
            "author_name": {
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
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
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
                        "type": "geo_point",
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
                        "ignore_above": 256
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
                        "ignore_above": 256
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
                        "ignore_above": 256
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
                        "ignore_above": 256
                    }
                }
            },
            "targeted_countries": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                }
            },
            "tlp": {
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
    es.indices.put_mapping(index="pulses", doc_type="pulse", body=mapping)
    # Create an index mapping to use map visualization
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
                "type": "geo_point",
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
        # DEBUGGING: not creating cache for now
        # cache_pulse(pulse)
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
                    # the returned result has "lng" instead of "lon", so change that first
                    lng = ipgeocode["lng"]
                    ipgeocode.update([("lon", lng)])
                    del ipgeocode["lng"]
                    # DEBUG: print(pprint.pformat(ipgeocode))
                    indicator.update([("location", ipgeocode)])
                    # DEBUGGING: print(indicator["location"])
            # DEBUGGING: to deal with indicators that don't currently have location data, substitute coordinate (0, 0)
            # ERROR: "failed to parse"
            else:
                # DEBUG: print("Updating indicator with no location.")
                indicator.update([("location", {"lat": 0.0, "lon": 0.0})])
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


# Function for adding a pulse to a user's favorites on OTX & in the app
def add_favorite(pulse):
    # add to a collection named "Favorites" or have the ability to customize collections
    print("Function not yet implemented.")


# Main method for starting up the program
if __name__ == '__main__':
    main()


