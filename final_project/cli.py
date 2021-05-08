from luigi import build

from final_project.data_collection.tasks.download_data.canvas import CanvasApiAdapter
from final_project.data_collection.tasks.update_es.es_task import UpdatePdfEs


def main():
    update_lectures()


def update_lectures():
    """
    Runner for luigi tasks for all given PDF files in the course
    """
    lectures = [item.title for item in CanvasApiAdapter().get_module_items("Lecture")]
    tasks = [UpdatePdfEs(pdf_file=lecture) for lecture in lectures]
    build(tasks, local_scheduler=True)
