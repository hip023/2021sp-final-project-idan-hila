"""
A luigi task for PDF cleanup
"""
import os
import re
from typing import Union

import pdfplumber
from luigi import Parameter, Task, LocalTarget
from luigi.format import Nop

from data_cleanup.constants_characters import *

FILE_PATH_TYPE = Union[str, os.PathLike]
DEFAULT_CLEAN_PDF_DIRECTORY = "clean_pdfs"
DEFAULT_PDF_DIRECTORY = "lectures"


class MockLocalPath(Task):
    pdf_file = Parameter()
    file_directory = Parameter()

    def output(self) -> LocalTarget:
        local_file_path = os.path.join(self.file_directory, self.pdf_file)
        return LocalTarget(local_file_path, format=Nop)


class CleanPdf(Task):
    pdf_file = Parameter()
    file_directory = DEFAULT_PDF_DIRECTORY
    save_directory = DEFAULT_CLEAN_PDF_DIRECTORY

    def requires(self):
        """
        A locally downloaded PDF file
        """
        # return DownloadCanvasPdf(pdf_file=self.pdf_file,
        #                          output_dir=self.file_directory)
        return self.clone(MockLocalPath)

    def output(self):
        """
        :return: a TargetOutput object to saved txt file
        """
        clean_name = self.pdf_file.split(os.extsep, 1)[0] + ".txt"
        local_file_path = os.path.join(self.save_directory, clean_name)

        return LocalTarget(local_file_path)

    def run(self):
        """
        Convert PDF file object to clean txt file
        """
        if not os.path.isdir(self.save_directory):
            os.mkdir(self.save_directory)

        with pdfplumber.open(self.input().path) as pdf:
            raw_texts = "\n".join([page.extract_text() for page in pdf.pages])
            texts = transform_camel_case_to_space(raw_texts)

        with open(self.output().path, mode="w") as f:
            f.write(texts)


def transform_camel_case_to_space(text: str):
    """
    :param text: a potentially camelCase text representation
    :return: a text without
    """
    clean_text = re.sub(rf"[^{ASCII_VALUE_RANGE}]+", " ", text)
    clean_text = re.sub(rf"{NULL_ASCII}+", " ", clean_text)
    text_without_duplicated_spaces = re.sub("\s+", " ", clean_text)
    return text_without_duplicated_spaces
