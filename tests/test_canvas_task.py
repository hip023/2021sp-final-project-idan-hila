import unittest

import os
from unittest import mock
import requests_mock
from final_project.data_collection.tasks.download_data.canvas_task import DownloadCanvasPdf

from tests.luigi_utils import LuigiTestCase
from tests.other_utils import inside_tempdir

FAKE_ENV = {
    "COURSE_NAME": "my course name",
    "CANVAS_URL": "https://my_url.com",
    "CANVAS_TOKEN": "my token",
    "GITHUB_CLASSROOM": "my classroom",
    "TRAVIS_BUILD_WEB_URL": "travis_url",
    "TRAVIS_BRANCH": "travis_url",
}


@mock.patch.dict(
    os.environ,
    FAKE_ENV,
)
@requests_mock.Mocker()
class TestCanvas(LuigiTestCase):
    mocked_courses = {
        "method": "GET",
        "endpoint": "/courses",
        "data": [
            {"uuid": 913, "name": "no course of mine", "id": 913},
            {"uuid": 912, "name": FAKE_ENV["COURSE_NAME"], "id": 912},
            {"uuid": 914, "name": "SWORDS AND FUNNY STUFF", "id": 914},
        ],
        "status_code": 200,
    }
    mocked_modules = {
        "method": "GET",
        "endpoint": "/courses/912/modules",
        "data": [{"id": 122, "name": "Lecture", "position": 1}],
        "status_code": 200,
    }
    mocked_module_items = {
        "method": "GET",
        "endpoint": "/courses/912/modules/122/items",
        "data": [
            {
                "id": 1,
                "title": "my_pdf.pdf",
                "content_id": 96,
            },
        ],
        "status_code": 200,
    }

    mocked_files = {
        "method": "GET",
        "endpoint": "/courses/912/files/96",
        "data": {
            "id": 96,
            "display_name": "my_pdt.pdf",
            "size": 6144,
            "url": f'{FAKE_ENV["CANVAS_URL"]}/api/v1/file_download',
        },
        "status_code": 200,
    }

    mocked_file_download = {
        "method": "GET",
        "endpoint": "/file_download",
        "data": "THIS IS SPARTAAAAAAA",
        "status_code": 200,
    }

    def register_uri(self, m, mocked_data):
        m.register_uri(
            mocked_data["method"],
            FAKE_ENV["CANVAS_URL"] + "/api/v1" + mocked_data["endpoint"],
            json=(mocked_data.get("data")),
            status_code=(mocked_data.get("status_code", 200)),
        )

    def test_canvas_task(self, m):
        with inside_tempdir():
            self.register_uri(m, self.mocked_courses)
            self.register_uri(m, self.mocked_files)
            self.register_uri(m, self.mocked_modules)
            self.register_uri(m, self.mocked_module_items)
            self.register_uri(m, self.mocked_file_download)
            assert self.run_locally_split(f"{DownloadCanvasPdf.__name__} --pdf-file my_pdf.pdf")
            file_path = os.path.join("lectures/my_pdf.pdf")
            self.assertTrue(os.path.isfile(file_path))
            with open(file_path) as downloaded_file:
                self.assertEqual(downloaded_file.read(), '"THIS IS SPARTAAAAAAA"')
