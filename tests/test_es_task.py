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



