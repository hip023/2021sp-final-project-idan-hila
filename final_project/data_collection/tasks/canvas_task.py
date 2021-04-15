import os

from canvasapi.module import ModuleItem
from luigi import  Parameter, Task

from final_project.data_collection.tasks.canvas import CanvasApiAdapter
from final_project.data_collection.tasks.output import TargetOutput


class DownloadCanvasPdf(Task):
    PDF_MODULE = 'Lecture'
    output_dir = Parameter(default='lectures')
    pdf_file = Parameter()

    def run(self):
        api = CanvasApiAdapter()
        pdf_module_item = self.get_pdf_module_item(api)
        self.output().makedirs()
        api.course.get_file(pdf_module_item.content_id).download(self.output().path)

    output = TargetOutput('{task.output_dir}/{task.pdf_file}')

    def get_pdf_module_item(self, api: CanvasApiAdapter) ->ModuleItem:
        lecture_module = next(filter(lambda x: x.name == self.PDF_MODULE, api.course.get_modules()))
        for item in lecture_module.get_module_items():
            if item.title == self.pdf_file:
                return item
        raise Exception(f'could not find pdf: {self.pdf_file}. '
                        f'Found {[item.title for item in lecture_module.get_module_items()]}')


