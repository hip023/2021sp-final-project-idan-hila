import os

from canvasapi.module import ModuleItem
from luigi import  Parameter, Task

from final_project.data_collection.tasks.canvas import CanvasApiAdapter
from final_project.data_collection.tasks.output import TargetOutput


class DownloadCanvasPdf(Task):
    canvas_pdf_module = Parameter(default='Lecture')
    output_dir = Parameter(default='lectures')
    pdf_file = Parameter()

    def run(self):
        api = CanvasApiAdapter()
        pdf_module_item = api.get_module_item(self.canvas_pdf_module, self.pdf_file)
        self.output().makedirs()
        api.course.get_file(pdf_module_item.content_id).download(self.output().path)

    output = TargetOutput('{task.output_dir}/{task.pdf_file}')




