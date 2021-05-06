"""
A test module for ElasticSearch Wrapper
"""
from copy import deepcopy
from unittest import mock, TestCase

import elasticsearch

from final_project.es_wrapper.es_wrapper import ResultObject, get_es_results
from final_project.input_validation_decorator import NoneStringArgument

MOCK_ES_RESULT = {
    "hits": {
        "hits": [
            {'_source': {'pdf_file': 'pdf_1'},
             '_score': 5},
            {'_source': {'pdf_file': 'pdf_2'},
             '_score': 10}
        ],
        "max_score": 10
    }}


class TestResultObject(TestCase):
    def test_result_object_factory_regression(self):
        """
        Test regression for the ResultObject factory (class method)
        """
        es_actual_results = ResultObject.get_instance_from_dict(MOCK_ES_RESULT)

        self.assertTrue(isinstance(e, ResultObject) for e in es_actual_results)
        self.assertEqual(len(es_actual_results), 2)

        self.assertEqual(es_actual_results[0].file_name, 'pdf_1')
        self.assertEqual(es_actual_results[0].score, 5)
        self.assertEqual(es_actual_results[0].norm_score, 50)

        self.assertEqual(es_actual_results[1].file_name, 'pdf_2')
        self.assertEqual(es_actual_results[1].score, 10)
        self.assertEqual(es_actual_results[1].norm_score, 100)

    def test_max_score_is_none_should_raise_value_error(self):
        """
        Test correct assertion of value error when no max score is sent
        """
        mock_es_results_without_max_score = deepcopy(MOCK_ES_RESULT)
        mock_es_results_without_max_score.get("hits").pop("max_score")

        with self.assertRaises(TypeError):
            ResultObject.get_instance_from_dict(mock_es_results_without_max_score)

    def test_get_es_results_raises_error_with_int(self):
        """
        validate the validate_string input decorator
        """
        with self.assertRaises(NoneStringArgument):
            get_es_results(123)

    @mock.patch.object(elasticsearch, "Elasticsearch", return_value=mock.MagicMock())
    def test_get_es_results_with_spaces_in_text(self, m_es):
        """
        Tests a double call in case search query with spaces yields nothing
        :param m_es: MagicMock for ElasticSearch class
        """
        m_es.return_value.search.side_effect = get_mock_es_results
        results = get_es_results("1 2")

        self.assertEqual(results, MOCK_ES_RESULT)
        self.assertEqual(m_es.return_value.search.call_count, 2)


def get_mock_es_results(body: dict, *args, **kwargs):
    """
    Mocks the behavior of ElasticSearch search result
    """
    s = body.get("query").get("match").get("text")
    if " " in s:
        return {"hits": {"hits": []}}
    return MOCK_ES_RESULT
