from functools import partial

from luigi import LocalTarget


class TargetOutput:
    """
    Descriptor to create an intelligent local target format
    """
    factory = LocalTarget

    def __init__(self, path_format="{task.field}"):
        """
        :param path_format: an f-string formatable task field
        """
        self.path_format = path_format

    def __get__(self, task, cls):  # makes it look like a method
        """
        :param task: a luigi task to obtain the call method for
        :param cls: class name
        :return: a partial call to __call__ method with the desired task
        """
        return partial(self, task)

    def __call__(self, task) -> LocalTarget:
        """
        :param task: a luigi task to obtain the call method for
        :return LocalTarget or inherited classes with specified path format
        """
        path = self.path_format.format(task=task)
        return self.factory(path)
