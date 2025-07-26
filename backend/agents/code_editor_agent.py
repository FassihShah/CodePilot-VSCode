from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict
from dotenv import load_dotenv

load_dotenv()


class CodeEditState(TypedDict):
    full_code: str
    selected_code: str
    updated_selection: str
    instruction: str
    updated_code: str
    explanation: str



llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")


def clarify_instruction_node(state: CodeEditState) -> CodeEditState:
    """
    Clarifies vague or ambiguous user instructions.
    """

    instruction = state["instruction"]
    selected_code = state["selected_code"]

    prompt = f"""
You are a helpful assistant clarifying vague or ambiguous instructions.

The user selected this code:
{selected_code}

And gave this instruction:
"{instruction}"

Clarify this instruction so it's clear, specific, and directly actionable on the selected code. 

Only return the improved instruction — nothing else.
"""

    response = llm.invoke(prompt)

    return {"instruction": response.content}


def fix_code_node(state: CodeEditState) -> CodeEditState:
    """
    Applies the clarified instruction to the selected code.
    Returns only the modified selected portion.
    """

    full_code = state["full_code"]
    selected_code = state["selected_code"]
    instruction = state["instruction"]

    prompt = f"""
You are a helpful coding assistant.

The full code file is:
{full_code}

The selected code is:
{selected_code}

The instruction (already clarified) is:
"{instruction}"

Apply the instruction ONLY to the selected portion. Return ONLY the updated version of the selected code — no explanation, no extra output.
"""

    response = llm.invoke(prompt)
    return {
        "updated_code": full_code.replace(selected_code, response.content.strip()),
        "updated_selection": response.content.strip()
    }


def explain_changes_node(state: CodeEditState) -> CodeEditState:
    """
    Explains what was changed in the updated code vs the original selected code.
    """

    original = state["selected_code"]
    updated = state["updated_selection"]
    complete = state["full_code"]

    prompt = f"""
You are a helpful assistant that explains code edits **briefly and clearly**.

Original selected code:
{original}

Updated selected code:
{updated}

Full code file:
{complete}

Explain:
1. What was changed.
2. Why it was changed.

Use concise and simple language.
"""


    response = llm.invoke(prompt)
    return {"explanation": response.content}



def get_code_editor_graph():
    builder = StateGraph(CodeEditState)

    builder.add_node("clarify_instruction", clarify_instruction_node)
    builder.add_node("fix_code", fix_code_node)
    builder.add_node("explain_changes", explain_changes_node)

    builder.set_entry_point("clarify_instruction")

    builder.add_edge("clarify_instruction", "fix_code")
    builder.add_edge("fix_code", "explain_changes")
    builder.set_finish_point("explain_changes")

    return builder.compile()

