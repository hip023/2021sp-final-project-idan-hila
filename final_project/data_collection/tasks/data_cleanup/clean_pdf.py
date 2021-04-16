"""
A luigi task for PDF cleanup
"""
import os
import re
from typing import Union

import pdfplumber
from luigi import Parameter, Task

from final_project.data_collection.tasks.data_cleanup.constants_characters import *
from final_project.data_collection.tasks.download_data.canvas_task import (
    DownloadCanvasPdf,
)
from final_project.data_collection.tasks.output import TargetOutput

FILE_PATH_TYPE = Union[str, os.PathLike]
DEFAULT_CLEAN_PDF_DIRECTORY = "clean_pdfs"
DEFAULT_PDF_DIRECTORY = "lectures"


class CleanPdf(Task):
    pdf_file = Parameter()
    file_directory = Parameter(DEFAULT_PDF_DIRECTORY)
    save_directory = Parameter(DEFAULT_CLEAN_PDF_DIRECTORY)

    def requires(self):
        """
        A locally downloaded PDF file
        """
        return DownloadCanvasPdf(pdf_file=self.pdf_file, output_dir=self.file_directory)

    output = TargetOutput("{task.get_clean_txt_path}")

    @property
    def get_clean_txt_path(self):
        clean_name = self.pdf_file.split(os.extsep, 1)[0] + ".txt"
        local_file_path = os.path.join(self.save_directory, clean_name)
        return local_file_path

    def run(self):
        """
        Convert PDF file object to clean txt file
        """
        if not os.path.isdir(self.save_directory):
            os.mkdir(self.save_directory)

        with pdfplumber.open(self.input().path) as pdf:
            raw_texts = "\n".join([page.extract_text() for page in pdf.pages])
            texts = get_text_without_non_ascii_chars(raw_texts)

        with open(self.output().path, mode="w") as f:
            f.write(texts)


def get_text_without_non_ascii_chars(
        text: str,
) -> str:
    """
    :param text: a string containing non-ascii values
    :return: a text with only ascii characters
    """
    clean_text = re.sub(rf"[^{ASCII_VALUE_RANGE}]+", " ", text)
    clean_text = re.sub(rf"{NULL_ASCII}+", " ", clean_text)

    # remove duplicated spaces resulted from multiple non-ascii values
    text_without_duplicated_spaces = re.sub("\s+", " ", clean_text)

    return text_without_duplicated_spaces
