from elasticsearch import Elasticsearch
from datetime import datetime

def main():
    #start up elasticsearch on host 9200
    es = Elasticsearch()

    #create a sample doc to be added into the demo pulse index
    doc = {
        "name":"scary threat",
        "description":"I'm a scary hacker",
        "timestamp": datetime.now()
    }

    #add this new sample record for access in elasticsearch
    #DEBUGGING: including record number here.
    #in the program, will likely have to replace all record numbers & increment the ID as more pulses are added
    res = es.index(index="pulses", doc_type="pulse", id=1, body=doc)
    #DEBUGGING: print result. Key Error here.
    print(res["created"])

    #signal having finished the process, and then exit
    print("System done")
    exit()

if __name__ == "__main__":
    main()