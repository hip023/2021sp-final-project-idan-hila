"""Utils for accessing and submitting to Canvas"""
import datetime
import json
import os
from contextlib import contextmanager
from typing import Dict
from typing import Optional
from typing import Tuple

from canvasapi import Canvas
from canvasapi.assignment import Assignment
from canvasapi.course import Course
from canvasapi.quiz import Quiz, QuizSubmissionQuestion
from canvasapi.quiz import QuizSubmission
from canvasapi.user import User
from environs import Env


GITHUB_COMMIT_URL_FORMAT = "https://github.com/{}/{}/commit/{}"
PSET_ASSIGNMENT_NAME_FORMAT = "Pset {}"
PSET_QUIZ_NAME_FORMAT = "Pset {} Answers"

env = Env()


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

    def get_assignment(self, name: str) -> Optional[Assignment]:
        """

        :param course:
        :param name:
        :return: the searched Assignment if found. If not found returns None
        """
        assignments = self.course.get_assignments()
        for assign in assignments:
            if assign.name == name:
                return assign
        return None

    def get_quiz(self, name) -> Optional[Quiz]:
        """
        :param course:
        :param name:
        :return: the searched Quiz if found. If not found returns None
        """
        quizzes = self.course.get_quizzes()
        for quiz in quizzes:
            if quiz.title == name:
                return quiz
        return None

    def get_user(self, name) -> Optional[User]:
        """
        :param course:
        :param name:
        :return: the searched Quiz if found. If not found returns None
        """

        users = self.course.get_users()
        for user in users:
            if user.name == name:
                return user
        return None

    def get_pset(self, pset_num: int) -> Tuple[Quiz, Assignment]:
        """

        :param pset_num:
        :return: the pset quiz (answers) and assignment
        """
        (
            assignment_name,
            quiz_name,
        ) = self.get_quiz_and_assignment_name_according_to_pset(pset_num)
        quiz = self.get_quiz(quiz_name)
        assignment = self.get_assignment(assignment_name)
        return quiz, assignment

    def get_quiz_and_assignment_name_according_to_pset(self, pset_num):
        if pset_num == 2:
            quiz_name = "CSCI Utils Answers"
            assignment_name = "CSCI Utils"
        else:
            quiz_name = PSET_QUIZ_NAME_FORMAT.format(pset_num)
            assignment_name = PSET_ASSIGNMENT_NAME_FORMAT.format(pset_num)
        return assignment_name, quiz_name


