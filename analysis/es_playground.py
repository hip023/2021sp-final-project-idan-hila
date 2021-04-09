# TRIAL FOR ELASTIC_SEARCH SEARCH ENGINE
from datetime import datetime
from elasticsearch import Elasticsearch
# import pdftotext # DIDNT WORK
import textract

# WEB ENDPOINT. CAN WE CONNECT TO S3?
# ENDPOINT = 'https://i-o-optimized-deployment-188296.es.eastus.azure.elastic-cloud.com:9243'
DEFAULT_ENDPOINT = 'http://localhost:9200/'

# BEFORE INITIALIZING THE SCRIPT, IF WORKING WITH LOCAL HOST, RESTART BY
# NAVIGATING TO downloads/elastic...
# THEN RUN bin/elasticsearch

SAMPLE_TERMS = [
    'cookie-cutter',
    'luigi',
    'air-flow',
    'pset-1',
    'pset-2',
    'pset-3',
    'final project',
    'midterm exam'
]


def load_sample_data(es_client):
    i=1
    for term in SAMPLE_TERMS:
        # SAMPLE_DOCS[i] = {"text": term.replace('-',' ')}
        es_client.index(index=f"text-{i}", id=i, body={"text": term.replace('-',' '),
                                                       "type": "pdf",
                                                       "page": 2})
        i += 1


if __name__ == '__main__':
    es = Elasticsearch()

    # IF YOU WANT TO LOAD DATA
    # load_sample_data(es)

    # Retrieve a document
    res = es.get(index="text-2", id=2)
    print(res['_source'])

    # TODO: understand what it means
    # es.indices.refresh(index="test-index")

    # RETRIVE ALL DOCUMENTS:
    search_res = es.search(body={"query": {"match_all": {}}})
    print(search_res['hits'])

    # for a specific index
    search_res2 = es.search(index="test-index", body={"query": {"match_all": {}}})
    print(search_res2['hits'])

    # DELETE A DOCUMENT
    # res = es.delete(index='megacorp', doc_type='employee', id=3)

    # SAMPLE SEARCH
    search_res = es.search(body={"query": {"match": {"text": "cookie"}}})
    for hit in search_res['hits']['hits']:
        print(hit['_source']['text'])
        print(hit['_score'])
        print('**********************')


    search_res2 = es.search(body={"query": {"match": {"text": "pset"}}})


    print('done')