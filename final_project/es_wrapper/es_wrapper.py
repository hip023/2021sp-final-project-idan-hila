from __future__ import annotations

from typing import List

import elasticsearch

from ..input_validation_decorator import validate_string


class ResultObject:
    """
    A class to hold a readable structure for elasticsearch results
    """

    @classmethod
    def get_instance_from_dict(cls, search_results_dict: dict) -> List[ResultObject]:
        """
        A factory to create a lit of ResultObject instances
        given an expected ES result dict
        :param search_results_dict:
        :return: List[ResultObject]
        :raises: TypeError if max_score is none
        """
        hits = search_results_dict.get("hits")
        max_score = hits.get("max_score")
        return [ResultObject(hit, max_score) for hit in hits.get("hits")]

    def __init__(self, hit: dict, max_score: float):
        self.file_name = hit.get("_source").get("pdf_file")
        self.score = hit.get("_score")
        self.norm_score = self.normalized_score(max_score)

    def normalized_score(self, max_score: float) -> float:
        return int(100 * self.score / max_score)


@validate_string
def get_es_results(search_query: str) -> dict:
    """
    :param search_query: required
    :return:
    :raises: NoneStringArgument if search_query is not a string
    """
    es = elasticsearch.Elasticsearch()
    results = es.search(body={"query": {"match": {"text": search_query}}}, size=20)

    # If no sufficient results for the search query, trying another attempt
    # after space removal
    if len(results.get("hits").get("hits")) < 1:
        results = es.search(
            body={"query": {"match": {"text": search_query.replace(" ", "")}}}, size=20
        )
    return results


def es_results_wrapper(search_query: str):
    search_results_dict = get_es_results(search_query)
    results = ResultObject.get_instance_from_dict(search_results_dict)

    return results
