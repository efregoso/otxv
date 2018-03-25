from datetime import datetime
from elasticsearch import Elasticsearch

def main():
    # start up Elasticsearch on host 9200
    # then, start up Kibana on host 5601
    # create a pulse index in the user's instance of Kibana
    # VERIFY THAT THIS INDEX HAS BEEN CREATED
    # after verification, begin uploading pulse objects from initialize_indicators.py
    es = Elasticsearch()
    doc = {
        'author': 'Elizabeth',
        'text': 'Testing pulse information & elasticsearch indexing with timestamps.',
        'timestamp': datetime.now(),
    }
    res = es.index(index="test-index", doc_type='tweet', id=1, body=doc)
    print(res['created'])

    res = es.get(index="test-index", doc_type='tweet', id=1)
    print(res['_source'])

    es.indices.refresh(index="test-index")

    res = es.search(index="test-index", body={"query": {"match_all": {}}})
    print("Got %d Hits:" % res['hits']['total'])
    for hit in res['hits']['hits']:
        print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])

if __name__ == '__main__':
    main()