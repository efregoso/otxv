from elasticsearch import Elasticsearch
from datetime import datetime

# start up elasticsearch on host 9200
es = Elasticsearch()


def main():
    create_sample_index()
    create_sample_doc()
    result = test_search()
    print(result)
    test_update_by_query()
    result = test_search()
    print(result)
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


if __name__ == "__main__":
    main()
