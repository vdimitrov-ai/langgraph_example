from typing import Literal

from utils import InterviewState


def validate_yes_no_llm(user_answer, current_question):
    if len(user_answer) > 1:
        return True
    return False

def should_continue_from_greeting(
    state: InterviewState,
) -> Literal["ask_age", "end_call", "greeting"]:
    user_answer = state.get("user_answer", "").lower().strip()
    current_question = state.get("current_question", "")
    result = validate_yes_no_llm(user_answer, current_question)
    retry_count = state.get("retry_count", 0)

    if result:
        return "ask_age"
    else:
        if retry_count > 2:
            return 'end_call'
        return 'greeting'

def should_continue_from_age(
    state: InterviewState,
) -> Literal["end_call"]:
    return "end_call"
