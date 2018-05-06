from OTXv2 import OTXv2
from elasticsearch import Elasticsearch
import initialize_indicators


# OTX object prepopulated with my API key.
otx = OTXv2("de0e60ea625d2b840e464f5d44299fcd513a3da48d2d7dd8c3214474dc6dbadb")
# An instance of Elasticsearch
es = Elasticsearch()


'''
Function for creating & starting up the demo cache for demo purposes.

'''
def main():
    print("Downloading pulses from OTX...")
    pulses = otx.getall()
    print("Configuring indeces...")
    # DEBUGGING: Save all indicator data to cache document & send to Elasticsearch with incremental IDs
    # Creating the index before adding things to it so that the mapping can be customized
    if es.indices.exists(index="demo"):
        # go through each pulse & check when it was last modified & if a pulse by that name exists in the index already.
        # if not, copy. if there is, update from last modified date from the index
        for pulse in pulses[0:20]:
            # cache_pulses(pulse)
            # cache_indicator_data(pulse)
            try:
                pulse_match = es.get(index="demo", q="_id:" + str(int(pulse["id"], 16)))
                if pulse["modified"] > pulse_match["modified"]:
                    es.index(index="demo", doc_type="pulse", id=int(pulse["id"], 16), body=pulse)
                    print("Updated pulse with ID: " + str(int(pulse["id"], 16)))
            except:
                initialize_indicators.add_loc_to_indicators(pulse)
                es.index(index="demo", doc_type="pulse", id=int(pulse["id"], 16), body=pulse)
                print("Added new pulse with ID: " + str(int(pulse["id"], 16)))
    # If index does not already exist, create the index and begin loading mapping & pulse information
    else:
        print("Creating new index: demo")
        es.indices.create(index="demo", ignore=400)
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
        es.indices.put_mapping(index="demo", doc_type="pulse", body=mapping)
        # Create an indicator mapping to get more useful list visualization
        es.indices.create(index="indicator_demo", ignore=400)
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
        es.indices.put_mapping(index="indicator_demo", doc_type="indicator", body=mapping)
        print("Mappings created. Beginning pulse loading.")
        # DEBUGGING: just the first thousand for now
        for pulse in pulses[0:20]:
            # cache the pulse & its indicator data
            # cache_pulses(pulse)
            # cache_indicator_data(pulse)
            initialize_indicators.add_loc_to_indicators(pulse)
            # convert the pulse's natural hexadecimal ID to an integer ID
            es.index(index="demo", doc_type="pulse", id=int(pulse["id"], 16), body=pulse)
            print("Added pulse with ID: " + str(int(pulse["id"], 16)))
    # signal that the program is done
    print("System done")
    exit()

if __name__ == "__main__":
    main()