from submission.canvas_submission import CanvasApi, get_assignment_submission_type, get_assignment_comment

ASSIGNMENT = "Final Project"


if __name__ == '__main__':
    client = CanvasApi(assignment_name=ASSIGNMENT)
    with client.create_quiz_submission() as quiz_submission:
        client.submit_assignment(
            get_assignment_submission_type(),
            get_assignment_comment(quiz_submission),
        )
