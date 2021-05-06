from functools import partial

from luigi import LocalTarget


class TargetOutput:
    factory = LocalTarget

    def __init__(self, path_format="{task.field}"):
        self.path_format = path_format

    def __get__(self, task, cls):  # make it look like a method
        return partial(self, task)

    def __call__(self, task):
        path = self.path_format.format(task=task)
        return self.factory(path)
