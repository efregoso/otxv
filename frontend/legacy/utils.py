from enum import Enum

TEST_API_KEY = 'de0e60ea625d2b840e464f5d44299fcd513a3da48d2d7dd8c3214474dc6dbadb'

class AvailableMethods(Enum):
    STYLO_UNIGRAM = 'stylo_unigram'
    STYLO_NGRAM = 'stylo_ngram'
    IP_LOOKUP = 'ip_lookup'
    PORT_CHECK = 'port_check'

ELASTICSEARCH_MAPPING =  {
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

ELASTICSEARCH_INDICATOR_MAPPING = {
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
