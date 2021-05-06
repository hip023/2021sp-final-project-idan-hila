"""Utils for accessing and submitting to Canvas"""
import datetime
import json
import os
from contextlib import contextmanager
from typing import Dict, Optional, Tuple

from canvasapi import Canvas
from canvasapi.assignment import Assignment
from canvasapi.course import Course
from canvasapi.module import ModuleItem
from canvasapi.quiz import Quiz, QuizSubmission, QuizSubmissionQuestion
from canvasapi.user import User
from environs import Env

env = Env()


class ModuleNotFoundException(Exception):
    pass


class ModuleItemNotFoundException(Exception):
    pass


class CanvasApiAdapter:
    def __init__(self):
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

    def get_module(self, name):
        for module in self.course.get_modules():
            if module.name == name:
                return module
        raise ModuleNotFoundException(
            f"could not find pdf: {name}. " f"Found {self.get_all_module_names()}"
        )

    def get_all_module_names(self):
        return [item.title for item in self.course.modules()]

    def get_module_item(self, module_name, item_name) -> ModuleItem:
        module = self.get_module(module_name)
        for item in module.get_module_items():
            if item.title == item_name:
                return item
        raise ModuleItemNotFoundException(
            f"could not find item: {item_name}. "
            f"Found {[item.title for item in module.get_module_items()]}"
        )

    def get_module_items(self, name):
        return self.get_module(name).get_module_items()
