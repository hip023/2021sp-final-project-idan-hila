import os

import pdfplumber

from canvas_scrape.canvas import CanvasApiAdapter
import textract
PDF_DIR = 'lectures'

def main():
    api = CanvasApiAdapter()
    lecture_module = next(filter( lambda x: x.name == "Lecture",  api.course.get_modules()))
    if not os.path.isdir(PDF_DIR):
        os.mkdir(PDF_DIR)
    for module_item in lecture_module.get_module_items():
        path = os.path.join(PDF_DIR, module_item.title)
        if not os.path.exists(path):
            api.course.get_file(module_item.content_id).download(path)
    pdf_data = {}
    for file in sorted(os.listdir(PDF_DIR)):
        pdf_data[file] = {}
        path = os.path.join(PDF_DIR, file)
        with pdfplumber.open(path) as pdf:
            for i, page in enumerate(pdf.pages):
                pdf_data[f'page-{i}'] = page.extract_text()
    a= 2




if __name__ == '__main__':
    main()
