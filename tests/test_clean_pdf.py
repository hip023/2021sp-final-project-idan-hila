"""
A test module for PDF cleanup
"""

from unittest import TestCase

from final_project.data_collection.tasks.data_cleanup.clean_pdf import (
    get_text_without_non_ascii_chars,
)


class TestCleanPdf(TestCase):
    def test_text_with_non_ascii_values_should_get_clean_text(self):
        """
        Tests the correct removal of non-ascii symbols
        """
        dirty_text = "Hello\000 World !"
        expected_text = "Hello World !"
        actual_text = get_text_without_non_ascii_chars(dirty_text)

        self.assertEqual(expected_text, actual_text)
