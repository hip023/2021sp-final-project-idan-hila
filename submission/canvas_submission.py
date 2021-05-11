"""
Utils for accessing and submitting to Canvas

Not supported:
* kwargs: such as test student

"""
import json
import logging
import os
from contextlib import contextmanager
from typing import List

from canvasapi import Canvas
from canvasapi.assignment import Assignment
from canvasapi.course import Course
from canvasapi.quiz import Quiz
from canvasapi.quiz import QuizSubmission
from canvasapi.quiz import QuizSubmissionQuestion
from environs import Env

from git import Repo

E_29_PREFIX = "https://github.com/csci-e-29"

logger = logging.getLogger(__name__)


class CanvasApi(object):
    class CanvasConfigurations(object):
        """
        class to track all required configurations
        """

        def __init__(self):
            self.env = Env()
            self.url = self.env.str("CANVAS_URL")
            self.token = self.env.str("CANVAS_TOKEN")

    def __init__(
        self,
        course_name: str = "Advanced Python for Data Science",
        quiz_name: str = "Test Quiz",
        assignment_name: str = "Test Assignment",
    ):
        self.config = self.CanvasConfigurations()
        self.client = self._get_client(self.config.url, self.config.token)
        self.course = self._get_course(course_name)
        self.quiz = self._get_quiz(quiz_name)
        self.assignment = self._get_assignment(assignment_name)

    def get_course_uuid(self):
        """
        :return: the loaded course uuid
        """
        return self.course.uuid

    @contextmanager
    def create_quiz_submission(self):
        """
        a contextmanager based quiz submission. will close the submission event even if the submission fails.
        """
        quiz_submission = self.quiz.create_submission()
        logger.info(f"started submission attempt {quiz_submission.attempt}.")
        try:
            yield quiz_submission
        finally:
            quiz_submission.complete()
            logger.info(f"successfully closed submission for {str(quiz_submission)}")

    @staticmethod
    def get_submission_questions(
        quiz_submission: QuizSubmission,
    ) -> List[QuizSubmissionQuestion]:
        """
        :param quiz_submission: an opened QuizSubmission object
        :return: a list of the quiz's questions
        """
        return quiz_submission.get_submission_questions()

    @staticmethod
    def submit_quiz(quiz_submission: QuizSubmission, answers: List[dict]):
        """
        execute a quiz answers submission
        :param quiz_submission: a QuizSubmission object
        :param answers: calculated answers for all submission questions.
        """
        quiz_submission.answer_submission_questions(quiz_questions=answers)
        logger.info(f"successfully sent answers for quiz {str(quiz_submission)}")

    def submit_assignment(self, submission_type: dict, submission_comment: dict):
        """
        :param submission_type: a dict of the type submission.
        for example:
        {"submission_type": "online_url", "url": https://url.com}
        :param submission_comment: a dict of the submission comments.
        for example:
        {"comment_1": "i am a comment"}
        """
        self.assignment.submit(submission_type, comment=submission_comment)
        logger.info(f"successfully sent answers for assignment {str(self.assignment)}")

    @staticmethod
    def _get_client(url, token):
        """
        initiate an API call to Canvas with configured url and token
        :return:
        """
        return Canvas(url, token)

    def _get_course(self, course_name: str) -> Course:
        """
        :return: the course object for the initialized assignment id
        :raises: ValueError if name doesn't exist in the course names.
        """
        course_list = self.client.get_courses()
        try:
            return filter(lambda x: x.name == course_name, course_list).__next__()
        except StopIteration:
            courses_names = list(map(lambda x: x.name, course_list))
            raise ValueError(
                f"cannot trace course by name. "
                f"available courses are {courses_names}"
            )

    def _get_assignment(self, assignment_name: str) -> Assignment:
        """
        :return: the assignment object for the initialized assignment name
        :raises: ValueError if name doesn't exist in the assignments names.
        """
        assignment_list = self.course.get_assignments()
        try:
            return filter(
                lambda x: x.name == assignment_name, assignment_list
            ).__next__()
        except StopIteration:
            assignment_names = list(map(lambda x: x.name, assignment_list))
            raise ValueError(
                f"cannot trace assignment by name. "
                f"available assignments are {assignment_names}"
            )

    def _get_quiz(self, quiz_name: str) -> Quiz:
        """
        :return: the quiz object for the initialized quiz name
        :raises: ValueError if name doesn't exist in the quiz names.
        """
        quiz_list = self.course.get_quizzes()
        try:
            return filter(lambda x: x.title == quiz_name, quiz_list).__next__()
        except StopIteration:
            quizes_names = list(map(lambda x: x.title, quiz_list))
            raise ValueError(
                f"cannot trace quiz by name. " f"available quizes are {quizes_names}"
            )


def get_assignment_submission_type():
    """
    :return: a basic submission type format to include the git repo url.
    """
    git_client = Repo('.')
    git_username = os.getenv("GIT_USER")
    base_url = f"https://github.com/csci-e-29/2021sp-final-project-{git_username}/commit/{git_client.head.commit.hexsha}"
    return {"submission_type": "online_url", "url": base_url}


def get_assignment_comment(quiz_submission: QuizSubmission):
    """
    follows E-29 spec for desired comment keys. consumes information from two sources: git and canvas.
    :return: a dictionary with nested json-based dictionary. key is "text_comment".
    """
    git_client = Repo('.')
    git_information = {
        "hexsha": git_client.head.commit.hexsha[:8],
        "submitted_from": git_client.remotes.origin.url,
        "dt": git_client.head.commit.committed_datetime.isoformat(),
        "branch": Env().str("TRAVIS_BRANCH", None),
        "is_dirty": git_client.is_dirty(),
    }
    quiz_information = {
        "quiz_submission_id": quiz_submission.id,
        "quiz_attempt": quiz_submission.attempt,
    }
    return {"text_comment": json.dumps({**git_information, **quiz_information})}