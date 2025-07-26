from typing import TypedDict, Dict
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph
from dotenv import load_dotenv
import json
import re

load_dotenv()


class AgentState(TypedDict, total=False):
    user_input: str
    enhanced_prompt: str
    files: Dict[str, str]


llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")



def enhance_prompt_node(state: AgentState) -> AgentState:
    """Enhance user's prompt for beter results"""

    user_input = state["user_input"]

    enhancement_prompt = f"""
You are a helpful assistant improving short developer prompts.

Your job is to enhance the user's vague request into a **detailed instruction** 
that can be used to generate **new code files for a fresh setup**.

The goal is to create all necessary boilerplate and starter files for the described functionality.

---

Examples:

Short: "fastapi crud users"  
Enhanced: "Create a FastAPI project with CRUD operations for a User model. 
Include route handlers, Pydantic schemas, SQLAlchemy models, and SQLite database setup."

Short: "react login page"  
Enhanced: "Generate a React component for a login page using Tailwind CSS. 
Include controlled inputs for email and password, form validation, and a submit handler."

---

Now enhance this prompt:
Short: "{user_input}"  
Enhanced:
"""

    result = llm.invoke(enhancement_prompt)
    return {"enhanced_prompt": result.content.strip()}



def boilerplate_node(state: AgentState) -> AgentState:
    """Generate code files based on enhanced prompt"""

    enhanced_prompt = state["enhanced_prompt"]

    generation_prompt = f"""
You are a code generation assistant.

Generate the necessary code files for the following prompt:

{enhanced_prompt}

Return a Python dictionary of filename → code in **valid JSON format**.

Example:
{{
  "main.py": "<code>",
  "models.py": "<code>"
}}

IMPORTANT: Do not include triple backticks or markdown formatting. Just return raw JSON.
"""


    result = llm.invoke(generation_prompt)

    raw_output = result.content.strip()

    # Extract just the JSON blob from any wrapping markdown/backticks/etc
    match = re.search(r"\{.*\}", raw_output, re.DOTALL)

    try:
        if match:
            files = json.loads(match.group())
        else:
            raise ValueError("No valid JSON found in LLM output.")
    except Exception as e:
        files = {
            "error.txt": f"Failed to parse files from LLM output.\nError: {str(e)}\n\nRaw output:\n{raw_output}"
        }

    return {"files": files}


def get_boilerplate_graph():
    builder = StateGraph(AgentState)

    builder.add_node("enhance_prompt", enhance_prompt_node)
    builder.add_node("generate_files", boilerplate_node)

    builder.set_entry_point("enhance_prompt")
    builder.add_edge("enhance_prompt", "generate_files")
    builder.set_finish_point("generate_files")

    return builder.compile()
