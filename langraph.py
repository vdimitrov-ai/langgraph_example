from langgraph.graph import END, StateGraph
from langsmith import traceable

from transition import (
    should_continue_from_greeting,
    should_continue_from_age
)
from utils import get_attr_interview, InterviewState


@traceable(
    name="👋 Приветствие",
    tags=["interview-stage", "greeting"],
    metadata={"stage": "1", "expected_response": "yes/no"},
)
def greeting(state: InterviewState) -> InterviewState:
    retry_count = get_attr_interview(state)
    return {
        **state,
        "current_question": 'Привет',
        "stage": "greeting",
        "messages": [{"role": "assistant", "content": 'Привет'}],
        "retry_count": retry_count + 1,
    }


@traceable(
    name="🎂 Вопрос о возрасте",
    tags=["interview-stage", "age-question"],
    metadata={"stage": "3", "expected_response": "age_number"},
)
def ask_age(state: InterviewState) -> InterviewState:
    retry_count = get_attr_interview(state)
    return {
        **state,
        "current_question": 'Сколько тебе лет?',
        "stage": "ask_age",
        "messages": state.get("messages", [])
        + [{"role": "assistant", "content": 'Сколько тебе лет?'}],
        "retry_count": retry_count + 1,
    }

@traceable(
    name="❌ Завершение звонка",
    tags=["interview-stage", "end-call"],
    metadata={"stage": "end", "reason": "end_call"},
)
def end_call(state: InterviewState) -> InterviewState:
    return {
        **state,
        "current_question": 'Пока',
        "stage": "end_call",
        "messages": state.get("messages", [])
        + [{"role": "assistant", "content": 'Пока'}],
    }

workflow = StateGraph(InterviewState)

# Добавляем все ноды
workflow.add_node("greeting", greeting)
workflow.add_node("ask_age", ask_age)
workflow.add_node("end_call", end_call)


workflow.set_entry_point("greeting")

workflow.add_conditional_edges(
    "greeting",
    should_continue_from_greeting,
    {"ask_age": "ask_age", "end_call": "end_call", "greeting": "greeting"},
)

workflow.add_conditional_edges(
    "ask_age",
    should_continue_from_age,
    {"end_call": "end_call"},
)

workflow.add_edge("end_call", END)

app = workflow.compile()


with open("workflow_graph.png", "wb") as f:
    f.write(app.get_graph().draw_mermaid_png())