from __future__ import annotations

from elasticsearch import Elasticsearch

from ..input_validation_decorator import validate_string


# TODO: add test here.
class ResultObject:
    @classmethod
    def get_instance_from_dict(cls, search_results_dict: dict) -> ResultObject:
        hits = search_results_dict.get('hits')
        max_score = hits.get('max_score')
        return [ResultObject(hit, max_score) for hit in hits.get('hits')]

    def __init__(self, hit: dict, max_score: float):
        self.file_name = hit.get('_source').get('pdf_file')
        self.score = hit.get('_score')
        self.norm_score = self.normalized_score(max_score)

    def normalized_score(self, max_score: float) -> float:
        return int(100 * self.score / max_score)


@validate_string
def get_es_results(search_query: str) -> dict:
    es = Elasticsearch()
    return es.search(body={"query": {"match": {"text": search_query}}}, size=20)


# TODO: how to re-generate the links from canvas?
# e.g. https://canvas.harvard.edu/courses/81475/files/11640194?module_item_id=856910
def es_results_wrapper(search_query: str):
    search_results_dict = get_es_results(search_query)
    results = ResultObject.get_instance_from_dict(search_results_dict)

    return results
