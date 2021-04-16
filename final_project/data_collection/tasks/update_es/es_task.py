from luigi import Parameter
from luigi.contrib.esindex import CopyToIndex

from final_project.data_collection.tasks.data_cleanup.clean_pdf import CleanPdf

MY_INDEX = "scottbot"


class UpdatePdfEs(CopyToIndex):
    pdf_file = Parameter()
    index = MY_INDEX
    doc_type = "pdf"

    def requires(self):
        return self.clone(CleanPdf)

    def docs(self):
        with self.input().open() as file:
            return [{"text": file.read(), "pdf_file": self.pdf_file}]
