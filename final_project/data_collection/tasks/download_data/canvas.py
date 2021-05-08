"""Utils for accessing and submitting to Canvas"""
from typing import Optional, List

from canvasapi import Canvas
from canvasapi.course import Course
from canvasapi.module import ModuleItem, Module
from environs import Env

env = Env()


class ModuleNotFoundException(Exception):
    """
    Extends the basic Exception class
    Raised when canvas module is not found
    """
    pass


class ModuleItemNotFoundException(Exception):
    """
    Extends the basic Exception class
    Raised when canvas module item is not found
    """
    pass


class CanvasApiAdapter:
    """
    Adapts canvasapi package to work with CSCI-E29 desired convention
    """
    def __init__(self):
        """
        No arguments, reads from .env file.
        """
        self.canvas = Canvas(env("CANVAS_URL"), env("CANVAS_TOKEN"))
        self.course = self.get_course(env("COURSE_NAME"))

    def get_course(self, name: str) -> Optional[Course]:
        """
        :param name :str the course name to find
        :return: the searched Course if found. If not found returns None
        """

        courses = self.canvas.get_courses()
        for course in courses:
            if course.name == name:
                return course
        return None

    def get_module(self, name: str) -> Module:
        """
        :param name: str, the desired name of the module object
        :return: the module object with the desired name
        :raises: ModuleNotFoundException if given name doesn't match
        any module.
        This is case sensitive, so make sure capitalization is correct.
        """
        for module in self.course.get_modules():
            if module.name == name:
                return module
        raise ModuleNotFoundException(
            f"could not find pdf: {name}. " f"Found {self.get_all_module_names()}"
        )

    def get_all_module_names(self) -> List[str]:
        """
        :return: A list of all existing module names given the initialized course
        """
        return [item.title for item in self.course.modules()]

    def get_module_item(self, module_name: str, item_name: str) -> ModuleItem:
        """
        :param module_name: str, the desired name of the module object
        :param item_name: str, the desired name of the module item object
        :return: the module item object with the desired name
        :raises: ModuleNotFoundException if given name doesn't match
        any module.
        This is case sensitive, so make sure capitalization is correct.
        """
        module = self.get_module(module_name)
        for item in module.get_module_items():
            if item.title == item_name:
                return item
        raise ModuleItemNotFoundException(
            f"could not find item: {item_name}. "
            f"Found {[item.title for item in module.get_module_items()]}"
        )

    def get_module_items(self, name: str) -> List[ModuleItem]:
        """
        :param name: str, the desired name of the module object
        :return: A list of all items in the module
        """
        return self.get_module(name).get_module_items()
