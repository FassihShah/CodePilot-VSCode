from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage
from langchain_core.runnables import Runnable
from langchain_google_genai import ChatGoogleGenerativeAI


class SimpleExplainerState(TypedDict):
    selected_code: str
    full_code: str
    explanation: str


llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.4)


def explain_code_node(state: SimpleExplainerState) -> SimpleExplainerState:
    prompt = f"""
You are a programming assistant.

Selected Code:
{state['selected_code']}

Full File Content:
{state['full_code']}


Explain clearly what the selected code does in the context of the full file.
Use beginner-friendly language but keep technical accuracy.
Explain concisely.
"""

    result = llm.invoke([HumanMessage(content=prompt)])
    return {
        "selected_code": state["selected_code"],
        "full_code": state["full_code"],
        "explanation": result.content
    }


def build_code_explainer_graph() -> Runnable:
    builder = StateGraph(SimpleExplainerState)
    builder.add_node("ExplainCode", explain_code_node)
    builder.set_entry_point("ExplainCode")
    builder.add_edge("ExplainCode", END)
    return builder.compile()
