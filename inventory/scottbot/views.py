from django.shortcuts import render
from elasticsearch import Elasticsearch

from django.http import HttpResponse


def index(request):


    return render(request, 'index.html')
    # return HttpResponse(f"{results['hits']['hits']}")


def search(request):
    if request.method == 'GET':
        query = request.GET.get('word')
        if query:
            es = Elasticsearch()
            results = es.search(index="scottbot", body={"query": {"match": {"text": query}}})
            return HttpResponse(f"{list(map(search_response_beautifier,results['hits']['hits']))}")


def search_response_beautifier(result):
    return {'pdf_file': result['_source']['pdf_file'],
            'score': result['_score']}

