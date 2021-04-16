"""
A test module for PDF cleanup
"""

from unittest import TestCase

from luigi.parameter import MissingParameterException

from final_project.data_collection.tasks.data_cleanup.clean_pdf import (
    get_text_without_non_ascii_chars,
    CleanPdf,
    DEFAULT_CLEAN_PDF_DIRECTORY,
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

    def test_clean_pdf_requires_file_parameter(self):
        """
        Test error is raised when pdf_file path is not specified
        """
        with self.assertRaises(MissingParameterException):
            CleanPdf(file_directory="file_dir", save_directory="save_dir")

    def test_clean_pdf_changes_file_prefix_default_save_dir(self):
        """
        Test the correct file path creation with default save directory
        """
        expected_default_file_path = f"{DEFAULT_CLEAN_PDF_DIRECTORY}/i_am_file.txt"
        clean_pdf_default = CleanPdf(pdf_file="i_am_file.pdf")
        self.assertEqual(expected_default_file_path, clean_pdf_default.output().path)

    def test_clean_pdf_changes_file_prefix_with_save_dir_parameter(self):
        """
        Test the correct file path creation with changed save directory
        """
        expected_file_path = f"save_dir/i_am_file.txt"
        clean_pdf = CleanPdf(save_directory="save_dir", pdf_file="i_am_file.pdf")
        self.assertEqual(expected_file_path, clean_pdf.output().path)
