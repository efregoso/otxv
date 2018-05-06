from elasticsearch import Elasticsearch
from datetime import datetime
import pprint

# start up elasticsearch on host 9200
es = Elasticsearch()
# my APIkey
apikey = "de0e60ea625d2b840e464f5d44299fcd513a3da48d2d7dd8c3214474dc6dbadb"


def main():
    create_sample_index()
    create_sample_doc()
    result = es.get_source(index=apikey, doc_type="pulse", id=28125252463092022477321366342)
    print(result["modified"])
    # signal having finished the process, and then exit
    print("Program done")
    exit()


def test_search():
    result = es.search(index="test", q='_id:16')
    return result


'''
Was unable to debug this successfully. Do not use.
'''
def test_update_by_query():
    q = {
        "script": {
            "inline": "ctx._source.description='hello'",
            "lang": "painless"
        },
        "query": {
            "ids": {
                "type": "doc",
                "values": ["16"]
            }
        }
    }
    es.update_by_query(index="test", doc_type="doc", body=q, conflicts="proceed", refresh=True)
    print("Update successful")


def create_sample_doc():
    # create a sample doc to be added into the demo pulse index
    doc = {
        "name": "scary threat",
        "description": "I'm a scary hacker",
        "timestamp": datetime.now()
    }
    # add this new sample record for access in elasticsearch
    es.index(index="test", doc_type="doc", id=16, body=doc)
    print("Added doc to test")


def create_sample_index():
    es.indices.create(index="test", ignore=400)
    print("Created index 'test'")


def test_get_source():
    result = es.get_source(index="test", doc_type="doc", id=16)
    print(pprint.pformat(result))
    return result


if __name__ == "__main__":
    main()
