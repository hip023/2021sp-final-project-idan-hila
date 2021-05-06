"""
A test module for PDF cleanup
"""
from contextlib import contextmanager
from unittest import mock

from luigi.parameter import MissingParameterException

from final_project.data_collection.tasks.data_cleanup.clean_pdf import (
    DEFAULT_CLEAN_PDF_DIRECTORY,
    CleanPdf,
    get_text_without_non_ascii_chars,
)
from tests.luigi_utils import LuigiTestCase
from tests.other_utils import inside_tempdir


class TestCleanPdf(LuigiTestCase):
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

    @mock.patch(
        "final_project.data_collection." "tasks.data_cleanup.clean_pdf.pdfplumber"
    )
    def test_clean_pdf_writes_clean_file(self, mock_pdf_plumber):
        """
        Test the correct write to file of clean output
        """
        mock_pdf_plumber.open.side_effect = get_mock_file

        with inside_tempdir():
            download_canvas = CleanPdf(
                pdf_file="i_am_file.pdf", save_directory="save_dir"
            )
            with download_canvas.input().open(mode="w") as f:
                f.write("hi")

            self.assertTrue(
                self.run_locally_split(
                    "CleanPdf --pdf-file i_am_file.pdf --save-directory save_dir"
                )
            )

            with open("save_dir/i_am_file.txt", mode="r") as out:
                self.assertEqual(out.read(), "Hello World !")


@contextmanager
def get_mock_file(*args, **kwargs):
    try:
        mock_page = mock.MagicMock()
        mock_page.extract_text.return_value = "Hello\000 World !"
        mock_pdf = mock.MagicMock()
        mock_pdf.pages = [mock_page]
        yield mock_pdf
    except:
        pass
    finally:
        pass
