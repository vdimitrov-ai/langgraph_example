import operator
from typing import Annotated, TypedDict

class InterviewState(TypedDict):
    messages: Annotated[list, operator.add]
    current_question: str
    user_answer: str
    stage: str
    retry_count: int
    question: bool


def get_attr_interview(state: InterviewState) -> tuple:
    retry_count = state.get("retry_count", 0)
    return retry_count