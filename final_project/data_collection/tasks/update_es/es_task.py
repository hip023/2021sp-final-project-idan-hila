from typing import List

from luigi import Parameter
from luigi.contrib.esindex import CopyToIndex

from final_project.data_collection.tasks.data_cleanup.clean_pdf import CleanPdf

MY_INDEX = "scottbot"


class UpdatePdfEs(CopyToIndex):
    """
    Indexes the given .txt (clean pdf format) file to elasticsearch server
    """
    pdf_file = Parameter()
    index = MY_INDEX
    doc_type = "pdf"

    def requires(self):
        return self.clone(CleanPdf)

    def docs(self) -> List[dict]:
        """
        :return: A list of json formatted pdf for elasticsearch to index
        """
        with self.input().open() as file:
            return [{"text": file.read(), "pdf_file": self.pdf_file}]
