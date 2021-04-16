import os
import unittest


from tests.luigi_utils import LuigiTestCase
from tests.other_utils import inside_tempdir

class MyTestCase(LuigiTestCase):
    def test_something(self):
        with inside_tempdir():
            os.mkdir('clean_pdfs')
            with open(os.path.join("clean_pdfs", "my_pdf.txt"),'w') as file:
                file.write('You talking to me?')

            # assert self.run_locally_split(f'{UpdatePdfEs.__name__} --pdf-file my_pdf.pdf')
            # TODO: use pytest-mock (may require docker) https://medium.com/expedia-group-tech/testing-elasticsearch-applications-bbf7107dba9f
            #example https://github.com/yanglinz/django-pytest-elasticsearch-example





if __name__ == '__main__':
    unittest.main()

